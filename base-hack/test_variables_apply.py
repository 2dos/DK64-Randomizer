"""Set debugging vars to the build."""
import os

set_variables = {
    "level_order_rando_on": 0,
    # "level_order": [1, 5, 4, 0, 6, 2, 3],
    "troff_scoff_count": [25, 200, 300, 400, 410, 420, 8],
    "blocker_normal_count": [2, 3, 4, 5, 6, 7, 8, 9],
    # "key_flags": [0x4A, 0x8A, 0xA8, 0xEC, 0x124, 0x13D, 0x1A],
    "unlock_kongs": 0x1F,
    "unlock_moves": 1,
    "fast_start_beginning": 1,
    "camera_unlocked": 1,
    "tag_anywhere": 1,
    "fast_start_helm": 1,
    "crown_door_open": 0,
    "coin_door_open": 0,
    "quality_of_life": {
        "reduce_lag": True,
        "remove_cutscenes": True,
        "fast_picture": True,
        "aztec_lobby_bonus": True,
        "dance_skip": True,
        "fast_boot": True,
        "fast_transform": True,
        "ammo_swap": True,
        "cb_indicator": True,
        "galleon_star": True,
        "vanilla_fixes": True,
        "textbox_hold": True,
        "caves_kosha_dead": True,
        "rambi_enguarde_pickup": True,
        "hud_bp_multibunch": True,
        "homing_balloons": True,
    },
    "price_rando_on": 1,
    "k_rool_order": [2, 0, 4, 3, 1],
    "damage_multiplier": 0,
    "fps_on": 1,
    "no_health_refill": 0,
    "slam_prices": [4, 5],
    "gun_prices": [1, 2, 3, 4, 5],
    "instrument_prices": [1, 2, 3, 4, 5],
    "gun_upgrade_prices": [1, 2],
    "ammo_belt_prices": [1, 2],
    "instrument_upgrade_prices": [1, 2, 3],
    "move_rando_on": 1,
    "remove_blockers": 0x7F,
    "resolve_bonus": 0,
    "disable_drops": 0,
    "shop_indicator_on": 2,
    "warp_to_isles_enabled": 1,
    "lobbies_open_bitfield": 0xFF,
    "perma_lose_kongs": 0,
    "jetpac_medal_requirement": 1,
    "free_target_llama": 0,
    "free_source_llama": 3,
    "keys_preturned": 0,
    "short_bosses": 1,
    "fast_warp": 1,
    "activate_all_bananaports": 1,
    "piano_game_order": [5, 0, 1, 3, 5, 5, 3],
    "dartboard_order": [0, 1, 2, 3, 4, 5],
    "fast_gbs": 1,
    "remove_high_requirements": 1,
    "open_level_sections": 1,
    "auto_keys": 0,
    "test_zone": [0xCC, 0],
    "klaptrap_color_bbother": 0x96,
    "kut_out_phases": [3, 2, 0],
    "dpad_visual_enabled": 1,
    "helm_order": [2, 0, 0xFF, 0xFF, 0xFF],
    "disco_chunky": 1,
    "krusha_slot": 3,
    "starting_kong": 3,
    "kut_out_kong_order": [1, 0, 0, 0, 0],
    "helm_hurry_mode": 0,
    "win_condition": 5,
    "version": 2,
    "item_rando": 1,
    "vulture_item": 72,
    "japes_rock_item": 76,
    "medal_cb_req": 5,
    "hard_enemies": 1,
    "remove_oscillation_effects": 1,
    # "starting_map": 0x1E,
    # "starting_exit": 4,
    "rareware_gb_fairies": 1,
    "call_parent_filter": 1,
}


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
        elif x == "quality_of_life":
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
            ]
            for y in set_variables["quality_of_life"]:
                if set_variables["quality_of_life"][y]:
                    index = order.index(y)
                    offset = int(index >> 3)
                    check = int(index % 8)
                    pre = readFromROM(0x1FED020 + 0xB0 + offset, 1)
                    pre_copy = pre
                    pre |= 0x80 >> check
                    print("")
                    print(f"{y} ({index}): {offset} {check} | {pre_copy} -> {pre}")
                    writeToROM(0xB0 + offset, pre, 1, y)
        else:
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
