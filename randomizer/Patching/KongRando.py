"""Apply cosmetic elements of Kong Rando."""
import random

import js
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Patching.Patcher import ROM, LocalROM


def apply_kongrando_cosmetic(spoiler):
    """Rando write bananaport locations."""
    if Types.Kong in spoiler.settings.shuffled_location_types:
        kong_locations = [x for x in spoiler.item_assignment if x.location in (Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong)]
        kong_flag_data = {
            385: Items.Donkey,
            6: Items.Diddy,
            70: Items.Lanky,
            66: Items.Tiny,
            117: Items.Chunky,
        }
        for x in kong_locations:
            new_item = Items.NoItem
            if x.new_flag in kong_flag_data:
                new_item = kong_flag_data[x.new_flag]
            spoiler.WriteKongPlacement(x.location, new_item)

    if spoiler.settings.kong_rando:
        gunswitches = [0x129, 0x126, 0x128, 0x127, 0x125]
        greenslamswitches = [0x94, 0x93, 0x95, 0x96, 0xB8]
        instrumentpads = [0xA8, 0xA9, 0xAC, 0xAA, 0xAB]
        forceSwitches = [0xE3, 0xE3, 0xE3, 0xE3, 0x70]
        actors = [Enemies.CutsceneDK, Enemies.CutsceneDiddy, Enemies.CutsceneLanky, Enemies.CutsceneTiny, Enemies.CutsceneChunky]

        japesPuzzleKong = spoiler.shuffled_kong_placement["Jungle Japes"]["puzzle"]["kong"]
        japesLockedKong = spoiler.shuffled_kong_placement["Jungle Japes"]["locked"]["kong"]
        if japesLockedKong == Kongs.any:
            japesLockedKong = Kongs.diddy

        tinyTemplePuzzleKong = spoiler.shuffled_kong_placement["Tiny Temple"]["puzzle"]["kong"]
        tinyTempleLockedKong = spoiler.shuffled_kong_placement["Tiny Temple"]["locked"]["kong"]
        if tinyTempleLockedKong == Kongs.any:
            tinyTempleLockedKong = Kongs.tiny

        llamaPuzzleKong = spoiler.shuffled_kong_placement["Llama Temple"]["puzzle"]["kong"]
        llamaLockedKong = spoiler.shuffled_kong_placement["Llama Temple"]["locked"]["kong"]
        if llamaLockedKong == Kongs.any:
            llamaLockedKong = Kongs.lanky

        factoryPuzzleKong = spoiler.shuffled_kong_placement["Frantic Factory"]["puzzle"]["kong"]
        factoryLockedKong = spoiler.shuffled_kong_placement["Frantic Factory"]["locked"]["kong"]
        if factoryLockedKong == Kongs.any:
            factoryLockedKong = Kongs.chunky

        llama_entrance_switch = []
        # if llamaPuzzleKong in [1, 4]:
        #     llama_entrance_switch.append({"index": 0xD, "new_type": gunswitches[llamaPuzzleKong]})

        kongrando_changes = [
            {
                "map_index": 7,
                "model2_changes": [
                    {"index": 0x30, "new_type": gunswitches[japesPuzzleKong]},
                    {"index": 0x31, "new_type": gunswitches[japesPuzzleKong]},
                    {"index": 0x32, "new_type": gunswitches[japesPuzzleKong]},
                ],
                "charspawner_changes": [{"type": Enemies.CutsceneDiddy, "new_type": actors[japesLockedKong]}],
            },
            {"map_index": 0x26, "model2_changes": llama_entrance_switch, "charspawner_changes": []},
            {
                "map_index": 0x14,
                "model2_changes": [{"index": 0x16, "new_type": instrumentpads[llamaPuzzleKong]}, {"index": 0x12, "new_type": gunswitches[llamaPuzzleKong]}],
                "charspawner_changes": [{"type": Enemies.CutsceneLanky, "new_type": actors[llamaLockedKong]}],
            },
            {
                "map_index": 0x10,
                "model2_changes": [
                    # {
                    #     "index": 0x0,
                    #     "new_type": greenslamswitches[tinyTemplePuzzleKong],
                    # },
                    # {
                    #     "index": 0x4,
                    #     "new_type": instrumentpads[tinyTemplePuzzleKong],
                    # },
                    {"index": 0x14, "new_type": forceSwitches[tinyTemplePuzzleKong]}
                ],
                "charspawner_changes": [{"type": Enemies.CutsceneTiny, "new_type": actors[tinyTempleLockedKong]}],
            },
            {
                "map_index": 0x1A,
                "model2_changes": [{"index": 0x24, "new_type": greenslamswitches[factoryPuzzleKong]}],
                "charspawner_changes": [{"type": Enemies.CutsceneChunky, "new_type": actors[factoryLockedKong]}],
            },
        ]

        for kong_map in spoiler.shuffled_kong_placement.keys():
            for link_type in spoiler.shuffled_kong_placement[kong_map].keys():
                LocalROM().seek(spoiler.settings.rom_data + spoiler.shuffled_kong_placement[kong_map][link_type]["write"])
                LocalROM().writeMultipleBytes(spoiler.shuffled_kong_placement[kong_map][link_type]["kong"], 1)

        for cont_map in kongrando_changes:
            cont_map_id = int(cont_map["map_index"])
            # Setup
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            LocalROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                LocalROM().seek(start + 0x2A)
                obj_id = int.from_bytes(LocalROM().readBytes(2), "big")
                has_id = False
                new_type = 0
                for model2 in cont_map["model2_changes"]:
                    if model2["index"] == obj_id:
                        has_id = True
                        new_type = model2["new_type"]
                if has_id:
                    LocalROM().seek(start + 0x28)
                    LocalROM().writeMultipleBytes(new_type, 2)
            # Character Spawners
            cont_map_spawner_address = js.pointer_addresses[16]["entries"][cont_map_id]["pointing_to"]
            LocalROM().seek(cont_map_spawner_address)
            fence_count = int.from_bytes(LocalROM().readBytes(2), "big")
            offset = 2
            if fence_count > 0:
                for x in range(fence_count):
                    LocalROM().seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(LocalROM().readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    LocalROM().seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(LocalROM().readBytes(2), "big")
                    offset += (point0_count * 10) + 6
            LocalROM().seek(cont_map_spawner_address + offset)
            spawner_count = int.from_bytes(LocalROM().readBytes(2), "big")
            offset += 2
            for x in range(spawner_count):
                LocalROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(LocalROM().readBytes(1), "big")
                init_offset = offset
                LocalROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(LocalROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                has_id = False
                new_type = 0
                for char in cont_map["charspawner_changes"]:
                    if char["type"] == enemy_id:
                        has_id = True
                        new_type = char["new_type"]
                if has_id:
                    LocalROM().seek(cont_map_spawner_address + init_offset)
                    LocalROM().writeMultipleBytes(new_type, 1)
