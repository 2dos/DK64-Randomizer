"""Apply Boss Locations."""
import random

import js
from randomizer.Lists.EnemyTypes import Enemies, EnemyMetaData
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Enums.Kongs import GetKongs

def randomize_kasplat_locations(spoiler: Spoiler):
    """Write replaced enemies to ROM."""
    kasplat_types = [
        Enemies.KasplatDK,
        Enemies.KasplatDiddy,
        Enemies.KasplatLanky,
        Enemies.KasplatTiny,
        Enemies.KasplatChunky
    ]
    if spoiler.settings.kasplat_rando:
        for level in KasplatLocationList:
            print(level)
            kasplats = KasplatLocationList[level]
            kongs = GetKongs()
            for idx, kong in enumerate(kongs):
                available_for_kong = []
                for kasplat in kasplats:
                    if not kasplat.selected and kong in kasplat.kong_lst:
                        available_for_kong.append(kasplat.name)
                selected_kasplat = random.choice(available_for_kong)
                for kasplat in kasplats:
                    if kasplat.name == selected_kasplat:
                        kasplat.selected = True
                        kasplat.selected_kong_idx = idx
                        kasplat.selected_kong = kong
                        print(selected_kasplat)
        for cont_map_id in range(216):
            cont_map_spawner_address = js.pointer_addresses[16]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_spawner_address)
            fence_count = int.from_bytes(ROM().readBytes(2), "big")
            offset = 2
            fence_bytes = []
            if fence_count > 0:
                for x in range(fence_count):
                    fence = []
                    fence_start = cont_map_spawner_address + offset
                    ROM().seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(ROM().readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM().seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(ROM().readBytes(2), "big")
                    offset += (point0_count * 10) + 6
                    fence_finish = cont_map_spawner_address + offset
                    fence_size = fence_finish - fence_start
                    ROM().seek(fence_start)
                    for y in range(int(fence_size / 2)):
                        fence.append(int.from_bytes(ROM().readBytes(2),"big"))
                    fence_bytes.append(fence)
                    ROM().seek(fence_finish)
            spawner_count_location = cont_map_spawner_address + offset
            ROM().seek(spawner_count_location)
            spawner_count = int.from_bytes(ROM().readBytes(2), "big")
            offset += 2
            spawner_bytes = []
            used_enemy_indexes = []
            for x in range(spawner_count):
                ROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM().readBytes(1), "big")
                ROM().seek(cont_map_spawner_address + offset + 0x13)
                enemy_index = int.from_bytes(ROM().readBytes(1), "big")
                used_enemy_indexes.append(enemy_index)
                init_offset = offset
                ROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                end_offset = offset
                if not enemy_id in kasplat_types:
                    data_bytes = []
                    spawner_size = end_offset - init_offset
                    ROM().seek(cont_map_spawner_address + init_offset)
                    for x in range(spawner_size):
                        data_bytes.append(int.from_bytes(ROM().readBytes(1),"big"))
                    spawner_bytes.append(data_bytes)
            spawn_index = 1
            for level in KasplatLocationList:
                kasplats = KasplatLocationList[level]
                for kasplat in kasplats:
                    while spawn_index in used_enemy_indexes:
                        spawn_index += 1
                    if cont_map_id == kasplat.map and kasplat.selected:
                        data_bytes = []
                        data_bytes.append(kasplat_types[kasplat.selected_kong_idx])
                        data_bytes.append(0x7A)
                        for x in range(2):
                            data_bytes.append(0)
                        for x in kasplat.coords:
                            if x < 0:
                                x += 65536 # Convert to unsigned
                            data_bytes.append(int(x/256))
                            data_bytes.append(int(x%256))
                        for x in range(2):
                            data_bytes.append(0)
                        data_bytes.append(0x23) # Idle Speed
                        data_bytes.append(0x3C) # Aggro Speed
                        data_bytes.append(1) # Pen ID
                        data_bytes.append(0x32) # Scale
                        data_bytes.append(1) # Init Control State
                        data_bytes.append(0) # Extra Data Count
                        data_bytes.append(2) # Init Spawn State
                        data_bytes.append(spawn_index) # Spawn Index
                        data_bytes.append(0x1E) # Init Respawn Timer
                        data_bytes.append(0)
                        spawner_bytes.append(data_bytes)
            print(f"{cont_map_id}: {hex(spawner_count_location)}")
            ROM().seek(spawner_count_location)
            ROM().writeMultipleBytes(len(spawner_bytes),2)
            for x in spawner_bytes:
                for y in x:
                    ROM().writeMultipleBytes(y,1)

                            
                            
