"""Set debugging vars to the build."""

import json
import os
import sys

APPLY_VARIABLES = True

if not APPLY_VARIABLES:
    sys.exit()

set_variables = {}
with open("test.json", "r") as fh:
    set_variables = json.loads(fh.read())


def valtolst(val, size):
    """Convert the values to a list."""
    arr = []
    for x in range(size):
        arr.append(0)
    conv = val
    for x in range(size):
        if conv != 0:
            arr[size - x - 1] = int(conv % 256)
            conv = (conv - (conv % 256)) / 256
    return arr


def readFromROM(offset, size):
    """Read from ROM."""
    with open("rom/dk64-randomizer-base-dev.z64", "rb") as rom:
        rom.seek(offset)
        return int.from_bytes(rom.read(size), "big")


def writeToROMNoOffset(offset, value, size, name):
    """Write to ROM without offset."""
    print("- Writing " + name + " (offset " + hex(offset) + ") to " + str(value))
    with open("rom/dk64-randomizer-base-dev.z64", "r+b") as rom:
        rom.seek(offset)
        rom.write(bytearray(valtolst(value, size)))


def writeToROM(offset, value, size, name):
    """Write byte data to rom."""
    print("- Writing " + name + " (offset " + hex(offset) + ") to " + str(value))
    with open("rom/dk64-randomizer-base-dev.z64", "r+b") as rom:
        rom.seek(0x1FED020 + offset)
        rom.write(bytearray(valtolst(value, size)))


GFX_START = 0x101A40
SCREEN_WD = 366
SCREEN_HD = 208
BOOT_OFFSET = 0xFB20 - 0xEF20

with open("include/variable_space_structs.h", "r") as varspace:
    varlines = varspace.readlines()
    struct_data = []
    for x in varlines:
        start = "ATTR_LINE"
        y = x.replace("\t", start)
        if y[:9] == start:
            struct_data.append(x.split(" //")[0].replace("\n", "").replace("\t", ""))
    struct_data2 = []
    for x in struct_data:
        location = x[3:8]
        other_info = x[12:].split(" ")
        other_data = [int(location, 16), "", "", 1]
        for y in range(len(other_info)):
            if y == (len(other_info) - 1):
                other_data[2] = other_info[y][:-1]
                count_split = other_data[2].split("[")
                if len(count_split) > 1:
                    other_data[2] = count_split[0]
                    other_data[3] = count_split[1].split("]")[0]
            else:
                other_data[1] += other_info[y] + " "
        other_data[1] = other_data[1][:-1]
        data_type = other_data[1]
        if "char" in data_type:
            other_data[1] = 1
        elif "short" in data_type:
            other_data[1] = 2
        elif "int" in data_type:
            other_data[1] = 4
        struct_data2.append(other_data)
    # print(struct_data2)
    test_keys = set_variables.keys()
    for x in test_keys:
        if x == "test_zone":
            ptr_table_offset = 0x101C50
            lz_table = ptr_table_offset + readFromROM(ptr_table_offset + (18 * 4), 4)
            isles_list = ptr_table_offset + readFromROM(lz_table + (0x22 * 4), 4)
            isles_list_end = ptr_table_offset + readFromROM(lz_table + (0x22 * 4) + 4, 4)
            isles_list_size = int((isles_list_end - isles_list) / 0x38)
            isles_list += 2
            for lz_index in range(isles_list_size):
                lz_type = readFromROM(isles_list + (0x38 * lz_index) + 0x10, 2)
                lz_map = readFromROM(isles_list + (0x38 * lz_index) + 0x12, 2)
                lz_exit = readFromROM(isles_list + (0x38 * lz_index) + 0x14, 2)
                if lz_type == 9 and lz_map == 0xB0 and lz_exit == 0:
                    writeToROMNoOffset(isles_list + (0x38 * lz_index) + 0x12, set_variables[x][0], 2, "Isles -> TGrounds Zone Map")
                    writeToROMNoOffset(isles_list + (0x38 * lz_index) + 0x14, set_variables[x][1], 2, "Isles -> TGrounds Zone Exit")
        elif x in ("quality_of_life", "moves_pregiven", "disabled_music", "hard_mode", "rom_flags"):
            if x == "quality_of_life":
                order = [
                    "reduce_lag",
                    "remove_cutscenes",
                    "fast_picture",
                    "aztec_lobby_bonus",
                    "dance_skip",
                    "fast_boot",
                    "fast_transform",
                    "ammo_swap",
                    "cb_indicator",
                    "galleon_star",
                    "vanilla_fixes",
                    "textbox_hold",
                    "caves_kosha_dead",
                    "rambi_enguarde_pickup",
                    "hud_bp_multibunch",
                    "homing_balloons",
                    "save_krool_progress",
                    "cbs_visible",
                    "blueprint_compression",
                    "fast_hints",
                    "brighten_mmm_enemies",
                    "global_instrument",
                    "fast_pause_transitions",
                    "cannon_game_speed",
                ]
                bitfield_offset = 0xB0
            elif x == "moves_pregiven":
                order = [
                    "blast",
                    "strong_kong",
                    "grab",
                    "charge",
                    "rocketbarrel",
                    "spring",
                    "ostand",
                    "balloon",
                    "osprint",
                    "mini",
                    "twirl",
                    "monkeyport",
                    "hunky",
                    "punch",
                    "gone",
                    "slam_upgrade_0",
                    "slam_upgrade_1",
                    "slam_upgrade_2",
                    "coconut",
                    "peanut",
                    "grape",
                    "feather",
                    "pineapple",
                    "bongos",
                    "guitar",
                    "trombone",
                    "sax",
                    "triangle",
                    "belt_upgrade_0",
                    "belt_upgrade_1",
                    "homing",
                    "sniper",
                    "ins_upgrade_0",
                    "ins_upgrade_1",
                    "ins_upgrade_2",
                    "dive",
                    "oranges",
                    "barrels",
                    "vines",
                    "camera",
                    "shockwave",
                ]
                bitfield_offset = 0xD5
            elif x == "disabled_music":
                order = [
                    "wrinkly",
                    "shops",
                    "events",
                    "transform",
                    "pause",
                    "chunk_songs",
                    "unk6",
                    "unk7",
                ]
                bitfield_offset = 0x1B7
            elif x == "hard_mode":
                order = [
                    "easy_fall",
                    "lava_water",
                    "bosses",
                    "enemies",
                    "dark_world",
                    "no_geo",
                    "unk6",
                    "unk7",
                ]
                bitfield_offset = 0xC6
            elif x == "rom_flags":
                order = [
                    "plando",
                    "spoiler",
                    "unk2",
                    "unk3",
                    "unk4",
                    "unk5",
                    "unk6",
                    "unk7",
                ]
                bitfield_offset = 0xC4
            for y in set_variables[x]:
                if set_variables[x][y]:
                    index = order.index(y)
                    offset = int(index >> 3)
                    check = int(index % 8)
                    pre = readFromROM(0x1FED020 + bitfield_offset + offset, 1)
                    pre_copy = pre
                    pre |= 0x80 >> check
                    print("")
                    print(f"{y} ({index}): {offset} {check} | {pre_copy} -> {pre}")
                    writeToROM(bitfield_offset + offset, pre, 1, y)
        else:
            if x == "true_widescreen" and set_variables[x] != 0:
                writeToROMNoOffset(GFX_START + 0x00, SCREEN_WD * 2, 2, "2D Viewport Width")
                writeToROMNoOffset(GFX_START + 0x02, SCREEN_HD * 2, 2, "2D Viewport Height")
                writeToROMNoOffset(GFX_START + 0x08, SCREEN_WD * 2, 2, "2D Viewport X Position")
                writeToROMNoOffset(GFX_START + 0x0A, SCREEN_HD * 2, 2, "2D Viewport Y Position")
                writeToROMNoOffset(GFX_START + 0x9C, (SCREEN_WD << 14) | (SCREEN_HD << 2), 4, "Default Scissor for 2D")
                data_offsets = [0xEF20, 0xF7E0]
                internal_size = 0x50
                internal_offsets = [0, 2]
                for tvi, tv_offset in enumerate(data_offsets):
                    tv_mode = "NTSC"
                    if tvi == 1:
                        tv_mode = "MPAL"
                    for int_offset in internal_offsets:
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x08, SCREEN_WD, 4, f"{tv_mode} VI Width")
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x20, int((SCREEN_WD * 512) / 320), 4, f"{tv_mode} VI X Scale")
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x28, (SCREEN_WD * 2), 4, f"{tv_mode} VI Field 1 Framebuffer Offset")
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x3C, (SCREEN_WD * 2), 4, f"{tv_mode} VI Field 2 Framebuffer Offset")
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x2C, int((SCREEN_HD * 1024) / 240), 4, f"{tv_mode} VI Field 1 Y Scale")
                        writeToROMNoOffset(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x40, int((SCREEN_HD * 1024) / 240), 4, f"{tv_mode} VI Field 2 Y Scale")

                writeToROMNoOffset(BOOT_OFFSET + 0xBC4 + 2, SCREEN_WD * 2, 2, "Row Offset of No Expansion Pak Image")
                writeToROMNoOffset(BOOT_OFFSET + 0xBC8 + 2, SCREEN_WD * SCREEN_HD * 2, 2, "Invalidation Size for Framebuffer 1")

                writeToROMNoOffset(BOOT_OFFSET + 0xE08, 0x24180000 | SCREEN_WD, 4, "Row Pitch for No Expansion Pak Screen Text")
                writeToROMNoOffset(BOOT_OFFSET + 0xE0C, 0x03060019, 4, "Calculate Row Pixel Number for No Expansion Pak Screen Text")
                writeToROMNoOffset(BOOT_OFFSET + 0xE10, 0x0000C012, 4, "Get Row Pixel Number for No Expansion Pak Screen Text")

                writeToROMNoOffset(BOOT_OFFSET + 0x1020 + 2, (SCREEN_WD - 8) * 2, 2, "Text Framebuffer Pitch")

            for y in struct_data2:
                if x == y[2]:
                    if type(set_variables[x]) is int:
                        if y[3] == 1:
                            writeToROM(y[0], set_variables[x], y[1], x)
                        # print(type(set_variables[x]))
                    elif type(set_variables[x]) is list:
                        for z in range(min([int(y[3]), len(set_variables[x])])):
                            writeToROM(y[0] + (z * y[1]), set_variables[x][z], y[1], x)
                    # print(type(set_variables[x]))
    # print(struct_data2)

# Editor: https://docs.google.com/spreadsheets/d/1UokoarKY6C56otoHMRUDCCMveaGUm8bGTOnaxjxDPR0/edit#gid=0
move_csv = "move_placement.csv"
permit = False  # Whether move csv overwrites data
if os.path.exists(move_csv) and permit:
    with open(move_csv, "r") as csv:
        csv_lines = csv.readlines()
        with open("rom/dk64-randomizer-base-dev.z64", "r+b") as rom:
            rom.seek(0x1FEF000)
            for x in csv_lines:
                val = int(x.replace("\n", ""))
                rom.write(val.to_bytes(4, "big"))
