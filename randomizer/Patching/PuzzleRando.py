"""Randomize puzzles."""

import random

import js
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Lib import IsItemSelected
from randomizer.Enums.Settings import FasterChecksSelected


def chooseSFX():
    """Choose random SFX from bank of acceptable SFX."""
    banks = [[98, 138], [166, 252], [398, 411], [471, 476], [519, 535], [547, 575], [614, 631], [644, 650]]
    bank = random.choice(banks)
    return random.randint(bank[0], bank[1])


def shiftCastleMinecartRewardZones():
    """Shifts the triggers for the reward point in castle minecart."""
    cont_map_lzs_address = js.pointer_addresses[18]["entries"][Maps.CastleMinecarts]["pointing_to"]
    ROM_COPY = LocalROM()
    ROM_COPY.seek(cont_map_lzs_address)
    lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    for lz_id in range(lz_count):
        start = (lz_id * 0x38) + 2
        ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
        lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
        lz_extra_data = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if lz_type == 0xA and lz_extra_data == 4:
            # Turn around zone
            offsets = [2, 6, 8]
            for offset in offsets:
                ROM_COPY.seek(cont_map_lzs_address + start + offset)
                ROM_COPY.writeMultipleBytes(0, 2)
        elif lz_type == 0x0 and lz_extra_data == 5:
            new_location = (3232, 482, 693)
            for c in range(3):
                ROM_COPY.seek(cont_map_lzs_address + start + (c * 2))
                ROM_COPY.writeMultipleBytes(new_location[c], 2)
            ROM_COPY.seek(cont_map_lzs_address + start + 6)
            ROM_COPY.writeMultipleBytes(40, 2)


def shortenCastleMinecart(spoiler):
    """Shorten Castle Minecart to end at the u-turn point."""
    if not IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterChecksSelected.castle_minecart):
        return
    shiftCastleMinecartRewardZones()
    new_squawks_coords = (3232, 482, 693)
    old_squawks_coords = (619, 690, 4134)
    cont_map_spawner_address = js.pointer_addresses[16]["entries"][Maps.CastleMinecarts]["pointing_to"]
    ROM_COPY = LocalROM()
    ROM_COPY.seek(cont_map_spawner_address)
    fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset = 2
    fence_bytes = []
    used_fence_ids = []
    fence_4_data = {"fence_6": [], "fence_A": [], "footer": 1}
    if fence_count > 0:
        for x in range(fence_count):
            fence = []
            fence_start = cont_map_spawner_address + offset
            ROM_COPY.seek(cont_map_spawner_address + offset)
            point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            point_6_offset = offset + 2
            offset += (point_count * 6) + 2
            ROM_COPY.seek(cont_map_spawner_address + offset)
            point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset + 2
            offset += (point0_count * 10) + 6
            fence_finish = cont_map_spawner_address + offset
            fence_size = fence_finish - fence_start
            ROM_COPY.seek(fence_finish - 4)
            fence_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            used_fence_ids.append(fence_id)
            ROM_COPY.seek(fence_start)
            for y in range(int(fence_size / 2)):
                fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            fence_bytes.append(fence)
            if fence_id == 4:
                # Vanilla Squawks Fence
                for p in range(point_count):
                    ROM_COPY.seek(cont_map_spawner_address + point_6_offset + (p * 6))
                    local_coords = []
                    for c in range(3):
                        local_coords.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    fence_4_data["fence_6"].append(local_coords)
                # for p in range(point0_count):
                #     ROM_COPY.seek(cont_map_spawner_address + point_A_offset + (p * 10))
                #     local_coords = []
                #     for c in range(5):
                #         local_coords.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                #     fence_4_data["fence_A"].append(local_coords)
            ROM_COPY.seek(fence_finish)
    spawner_count_location = cont_map_spawner_address + offset
    ROM_COPY.seek(spawner_count_location)
    spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
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
        ROM_COPY.seek(cont_map_spawner_address + offset)
        enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(cont_map_spawner_address + offset + 0x4)
        enemy_coords = []
        for y in range(3):
            coord = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if coord > 32767:
                coord -= 65536
            enemy_coords.append(coord)
        ROM_COPY.seek(cont_map_spawner_address + offset + 0x13)
        enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
        used_enemy_indexes.append(enemy_index)
        init_offset = offset
        ROM_COPY.seek(cont_map_spawner_address + offset + 0x11)
        extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        offset += 0x16 + (extra_count * 2)
        end_offset = offset
        # Get New Spawner Bytes
        data_bytes = []
        spawner_size = end_offset - init_offset
        ROM_COPY.seek(cont_map_spawner_address + init_offset)
        for x in range(spawner_size):
            value = int.from_bytes(ROM_COPY.readBytes(1), "big")
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
    ROM_COPY.seek(cont_map_spawner_address)
    ROM_COPY.writeMultipleBytes(len(fence_bytes), 2)
    for x in fence_bytes:
        for y in x:
            ROM_COPY.writeMultipleBytes(y, 2)
    ROM_COPY.writeMultipleBytes(len(spawner_bytes), 2)
    for x in spawner_bytes:
        for y in x:
            ROM_COPY.writeMultipleBytes(y, 1)


class PuzzleRandoBound:
    """Class to store information regarding the bounds of a puzzle requirement."""

    def __init__(self, lower: int, upper: int):
        """Initialize with given parameters."""
        self.lower = lower
        self.upper = upper
        self.selected = None

    def generateRequirement(self) -> int:
        """Generate random requirement between the upper and lower bounds."""
        self.selected = random.randint(self.lower, self.upper)
        return self.selected


class PuzzleItem:
    """Class to store information regarding a puzzle requirement."""

    def __init__(self, name: str, offset: int, normal_bound: PuzzleRandoBound, fast_bound: PuzzleRandoBound = None, fast_check_setting: FasterChecksSelected = None):
        """Initialize with given parameters."""
        self.name = name
        self.offset = offset
        self.normal_bound = normal_bound
        self.fast_bound = fast_bound
        self.fast_check_setting = fast_check_setting
        self.selected_bound = self.normal_bound

    def updateBoundSetting(self, spoiler):
        """Update the settings regarding bounds depending on selected settings."""
        self.selected_bound = self.normal_bound
        if self.fast_check_setting is not None and self.fast_bound is not None:
            if IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, self.fast_check_setting):
                self.selected_bound = self.fast_bound


def randomize_puzzles(spoiler):
    """Shuffle elements of puzzles. Currently limited to coin challenge requirements but will be extended in future."""
    sav = spoiler.settings.rom_data
    if spoiler.settings.puzzle_rando:
        ROM_COPY = LocalROM()
        coin_req_info = [
            PuzzleItem("Caves Beetle Race", 0x13C, PuzzleRandoBound(10, 50)),
            PuzzleItem("Aztec Beetle Race", 0x13D, PuzzleRandoBound(20, 50)),
            PuzzleItem("Factory Car Race", 0x13E, PuzzleRandoBound(5, 15), PuzzleRandoBound(3, 8), FasterChecksSelected.factory_car_race),
            PuzzleItem("Galleon Seal Race", 0x13F, PuzzleRandoBound(5, 12), PuzzleRandoBound(5, 10), FasterChecksSelected.galleon_seal_race),
            PuzzleItem("Castle Car Race", 0x140, PuzzleRandoBound(5, 15), PuzzleRandoBound(5, 12), FasterChecksSelected.castle_car_race),
            PuzzleItem("Japes Minecart", 0x141, PuzzleRandoBound(40, 70)),
            PuzzleItem("Forest Minecart", 0x142, PuzzleRandoBound(25, 55)),
            PuzzleItem("Castle Minecart", 0x143, PuzzleRandoBound(10, 45), PuzzleRandoBound(5, 30), FasterChecksSelected.castle_minecart),
        ]
        for coinreq in coin_req_info:
            coinreq.updateBoundSetting(spoiler)
            ROM_COPY.seek(sav + coinreq.offset)
            ROM_COPY.writeMultipleBytes(coinreq.selected_bound.generateRequirement(), 1)
        chosen_sounds = []
        for matching_head in range(8):
            ROM_COPY.seek(sav + 0x15C + (2 * matching_head))
            sfx = chooseSFX()
            while sfx in chosen_sounds:
                sfx = chooseSFX()
            chosen_sounds.append(sfx)
            ROM_COPY.writeMultipleBytes(sfx, 2)
        for piano_item in range(7):
            ROM_COPY.seek(sav + 0x16C + piano_item)
            key = random.randint(0, 5)
            ROM_COPY.writeMultipleBytes(key, 1)
        spoiler.dk_face_puzzle = [None] * 9
        spoiler.chunky_face_puzzle = [None] * 9
        for face_puzzle_square in range(9):
            ROM_COPY.seek(sav + 0x17E + face_puzzle_square)  # DK Face Puzzle
            value = random.randint(0, 3)
            if face_puzzle_square == 8:
                value = random.choice([0, 1, 3])  # Lanky for this square glitches out the puzzle. Nice going Loser kong
            spoiler.dk_face_puzzle[face_puzzle_square] = value
            ROM_COPY.writeMultipleBytes(value, 1)
            ROM_COPY.seek(sav + 0x187 + face_puzzle_square)  # Chunky Face Puzzle
            value = random.randint(0, 3)
            if face_puzzle_square == 2:
                value = random.choice([0, 1, 3])  # Lanky for this square glitches out the puzzle. Nice going Loser kong again
            ROM_COPY.writeMultipleBytes(value, 1)
            spoiler.chunky_face_puzzle[face_puzzle_square] = value
        # Arcade Level Order Rando
        arcade_levels = ["25m", "50m", "75m", "100m"]
        arcade_level_data = {
            "25m": 1,
            "50m": 4,
            "75m": 3,
            "100m": 2,
        }
        random.shuffle(arcade_levels)
        # Make sure 75m isn't in the first 2 levels if faster arcade is enabled because 75m is hard
        if IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterChecksSelected.arcade):
            for x in range(2):
                if arcade_levels[x] == "75m":
                    temp_level = arcade_levels[2]
                    arcade_levels[2] = arcade_levels[x]
                    arcade_levels[x] = temp_level
        for lvl_index, lvl in enumerate(arcade_levels):
            ROM_COPY.seek(sav + 0x48 + lvl_index)
            ROM_COPY.writeMultipleBytes(arcade_level_data[lvl], 1)
