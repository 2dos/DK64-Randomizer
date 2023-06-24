"""Randomize puzzles."""
import random

import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM, LocalROM


def chooseSFX():
    """Choose random SFX from bank of acceptable SFX."""
    banks = [[98, 138], [166, 252], [398, 411], [471, 476], [519, 535], [547, 575], [614, 631], [644, 650]]
    bank = random.choice(banks)
    return random.randint(bank[0], bank[1])


def shiftCastleMinecartRewardZones():
    """Shifts the triggers for the reward point in castle minecart."""
    cont_map_lzs_address = js.pointer_addresses[18]["entries"][Maps.CastleMinecarts]["pointing_to"]
    LocalROM().seek(cont_map_lzs_address)
    lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
    for lz_id in range(lz_count):
        start = (lz_id * 0x38) + 2
        LocalROM().seek(cont_map_lzs_address + start + 0x10)
        lz_type = int.from_bytes(LocalROM().readBytes(2), "big")
        lz_extra_data = int.from_bytes(LocalROM().readBytes(2), "big")
        if lz_type == 0xA and lz_extra_data == 4:
            # Turn around zone
            offsets = [2, 6, 8]
            for offset in offsets:
                LocalROM().seek(cont_map_lzs_address + start + offset)
                LocalROM().writeMultipleBytes(0, 2)
        elif lz_type == 0x0 and lz_extra_data == 5:
            new_location = (3232, 482, 693)
            for c in range(3):
                LocalROM().seek(cont_map_lzs_address + start + (c * 2))
                LocalROM().writeMultipleBytes(new_location[c], 2)
            LocalROM().seek(cont_map_lzs_address + start + 6)
            LocalROM().writeMultipleBytes(40, 2)


def shortenCastleMinecart(spoiler):
    """Shorten Castle Minecart to end at the u-turn point."""
    if not spoiler.settings.fast_gbs:
        return
    shiftCastleMinecartRewardZones()
    new_squawks_coords = (3232, 482, 693)
    old_squawks_coords = (619, 690, 4134)
    cont_map_spawner_address = js.pointer_addresses[16]["entries"][Maps.CastleMinecarts]["pointing_to"]
    LocalROM().seek(cont_map_spawner_address)
    fence_count = int.from_bytes(LocalROM().readBytes(2), "big")
    offset = 2
    fence_bytes = []
    used_fence_ids = []
    fence_4_data = {"fence_6": [], "fence_A": [], "footer": 1}
    if fence_count > 0:
        for x in range(fence_count):
            fence = []
            fence_start = cont_map_spawner_address + offset
            LocalROM().seek(cont_map_spawner_address + offset)
            point_count = int.from_bytes(LocalROM().readBytes(2), "big")
            point_6_offset = offset + 2
            offset += (point_count * 6) + 2
            LocalROM().seek(cont_map_spawner_address + offset)
            point0_count = int.from_bytes(LocalROM().readBytes(2), "big")
            point_A_offset = offset + 2
            offset += (point0_count * 10) + 6
            fence_finish = cont_map_spawner_address + offset
            fence_size = fence_finish - fence_start
            LocalROM().seek(fence_finish - 4)
            fence_id = int.from_bytes(LocalROM().readBytes(2), "big")
            used_fence_ids.append(fence_id)
            LocalROM().seek(fence_start)
            for y in range(int(fence_size / 2)):
                fence.append(int.from_bytes(LocalROM().readBytes(2), "big"))
            fence_bytes.append(fence)
            if fence_id == 4:
                # Vanilla Squawks Fence
                for p in range(point_count):
                    LocalROM().seek(cont_map_spawner_address + point_6_offset + (p * 6))
                    local_coords = []
                    for c in range(3):
                        local_coords.append(int.from_bytes(LocalROM().readBytes(2), "big"))
                    fence_4_data["fence_6"].append(local_coords)
                # for p in range(point0_count):
                #     LocalROM().seek(cont_map_spawner_address + point_A_offset + (p * 10))
                #     local_coords = []
                #     for c in range(5):
                #         local_coords.append(int.from_bytes(LocalROM().readBytes(2), "big"))
                #     fence_4_data["fence_A"].append(local_coords)
            LocalROM().seek(fence_finish)
    spawner_count_location = cont_map_spawner_address + offset
    LocalROM().seek(spawner_count_location)
    spawner_count = int.from_bytes(LocalROM().readBytes(2), "big")
    offset += 2
    spawner_bytes = []
    used_enemy_indexes = []
    # Get new fence index
    fence_index = 1
    if fence_index in used_fence_ids:
        while fence_index in used_fence_ids:
            fence_index += 1
        used_fence_ids.append(fence_index)
    # Read Spawners
    for x in range(spawner_count):
        LocalROM().seek(cont_map_spawner_address + offset)
        enemy_id = int.from_bytes(LocalROM().readBytes(1), "big")
        LocalROM().seek(cont_map_spawner_address + offset + 0x4)
        enemy_coords = []
        for y in range(3):
            coord = int.from_bytes(LocalROM().readBytes(2), "big")
            if coord > 32767:
                coord -= 65536
            enemy_coords.append(coord)
        LocalROM().seek(cont_map_spawner_address + offset + 0x13)
        enemy_index = int.from_bytes(LocalROM().readBytes(1), "big")
        used_enemy_indexes.append(enemy_index)
        init_offset = offset
        LocalROM().seek(cont_map_spawner_address + offset + 0x11)
        extra_count = int.from_bytes(LocalROM().readBytes(1), "big")
        offset += 0x16 + (extra_count * 2)
        end_offset = offset
        # Get New Spawner Bytes
        data_bytes = []
        spawner_size = end_offset - init_offset
        LocalROM().seek(cont_map_spawner_address + init_offset)
        for x in range(spawner_size):
            value = int.from_bytes(LocalROM().readBytes(1), "big")
            if enemy_id == 0x35 and enemy_index == 5:
                if x >= 4 and x < 10:
                    coord_slot = int((x - 4) / 2)
                    coord_top = (x - 4) % 2
                    coord_val = new_squawks_coords[coord_slot]
                    write_val = coord_val & 0xFF
                    if coord_top == 0:
                        write_val = (coord_val >> 8) & 0xFF
                    value = write_val
                elif x == 0xE:
                    value = fence_index
            data_bytes.append(value)
        spawner_bytes.append(data_bytes)
    # Create new fence
    new_fence_bytes = []
    new_fence_bytes.append(len(fence_4_data["fence_6"]))  # 0: Fence Block 0x6 Count, 1: Fence Block 0xA Count
    for point in fence_4_data["fence_6"]:
        for yi, y in enumerate(point):
            diff = y - old_squawks_coords[yi]
            new_fence_bytes.append(new_squawks_coords[yi] + diff)
    new_fence_bytes.append(0)
    new_fence_bytes.append(fence_index)
    new_fence_bytes.append(1)
    fence_bytes.append(new_fence_bytes)
    LocalROM().seek(cont_map_spawner_address)
    LocalROM().writeMultipleBytes(len(fence_bytes), 2)
    for x in fence_bytes:
        for y in x:
            LocalROM().writeMultipleBytes(y, 2)
    LocalROM().writeMultipleBytes(len(spawner_bytes), 2)
    for x in spawner_bytes:
        for y in x:
            LocalROM().writeMultipleBytes(y, 1)


def randomize_puzzles(spoiler):
    """Shuffle elements of puzzles. Currently limited to coin challenge requirements but will be extended in future."""
    sav = spoiler.settings.rom_data
    if spoiler.settings.puzzle_rando:
        race_requirements = {
            "factory_race": [5, 15],
            "castle_race": [5, 15],
            "seal_race": [5, 12],
            "castle_cart": [10, 45],
        }
        if spoiler.settings.fast_gbs:
            race_requirements["factory_race"] = [3, 8]
            race_requirements["castle_race"] = [5, 12]
            race_requirements["seal_race"] = [5, 10]
            race_requirements["castle_cart"] = [5, 30]

        coin_req_info = [
            {"offset": 0x13C, "coins": random.randint(10, 50)},  # Caves Beetle
            {"offset": 0x13D, "coins": random.randint(20, 50)},  # Aztec Beetle
            {"offset": 0x13E, "coins": random.randint(race_requirements["factory_race"][0], race_requirements["factory_race"][1])},  # Factory Car
            {"offset": 0x13F, "coins": random.randint(race_requirements["seal_race"][0], race_requirements["seal_race"][1])},  # Seal Race
            {"offset": 0x140, "coins": random.randint(race_requirements["castle_race"][0], race_requirements["castle_race"][1])},  # Castle Car
            {"offset": 0x141, "coins": random.randint(40, 70)},  # Japes Cart
            {"offset": 0x142, "coins": random.randint(25, 55)},  # Fungi Cart
            {"offset": 0x143, "coins": random.randint(race_requirements["castle_cart"][0], race_requirements["castle_cart"][1])},  # Castle Cart
        ]
        for coinreq in coin_req_info:
            LocalROM().seek(sav + coinreq["offset"])
            LocalROM().writeMultipleBytes(coinreq["coins"], 1)
        chosen_sounds = []
        for matching_head in range(8):
            LocalROM().seek(sav + 0x15C + (2 * matching_head))
            sfx = chooseSFX()
            while sfx in chosen_sounds:
                sfx = chooseSFX()
            chosen_sounds.append(sfx)
            LocalROM().writeMultipleBytes(sfx, 2)
        for piano_item in range(7):
            LocalROM().seek(sav + 0x16C + piano_item)
            key = random.randint(0, 5)
            LocalROM().writeMultipleBytes(key, 1)
        for face_puzzle_square in range(9):
            LocalROM().seek(sav + 0x17E + face_puzzle_square)  # DK Face Puzzle
            if face_puzzle_square == 8:
                LocalROM().writeMultipleBytes(random.choice([0, 1, 3]), 1)  # Lanky for this square glitches out the puzzle. Nice going Loser kong
            else:
                LocalROM().writeMultipleBytes(random.randint(0, 3), 1)
            LocalROM().seek(sav + 0x187 + face_puzzle_square)  # Chunky Face Puzzle
            if face_puzzle_square == 2:
                LocalROM().writeMultipleBytes(random.choice([0, 1, 3]), 1)  # Lanky for this square glitches out the puzzle. Nice going Loser kong again
            else:
                LocalROM().writeMultipleBytes(random.randint(0, 3), 1)
        # Arcade Level Order Rando
        arcade_levels = ["25m", "50m", "75m", "100m"]
        arcade_level_data = {
            "25m": 1,
            "50m": 4,
            "75m": 3,
            "100m": 2,
        }
        random.shuffle(arcade_levels)
        for lvl_index, lvl in enumerate(arcade_levels):
            LocalROM().seek(sav + 0x48 + lvl_index)
            LocalROM().writeMultipleBytes(arcade_level_data[lvl], 1)
