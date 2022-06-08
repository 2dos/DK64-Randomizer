"""Set debugging vars to the build."""
set_variables = {
    "level_order_rando_on": 0,
    "level_order": [1, 5, 4, 0, 6, 2, 3],
    "troff_scoff_count": [100, 200, 300, 400, 410, 420, 430],
    "blocker_normal_count": [2, 3, 4, 5, 6, 7, 8, 9],
    "key_flags": [0x4A, 0x8A, 0xA8, 0xEC, 0x124, 0x13D, 0x1A],
    "unlock_kongs": 0x1E,
    "unlock_moves": 1,
    "fast_start_beginning": 1,
    "camera_unlocked": 0,
    "tag_anywhere": 1,
    "fast_start_helm": 0,
    "crown_door_open": 0,
    "coin_door_open": 0,
    "quality_of_life": 1,
    "price_rando_on": 1,
    "k_rool_order": [0, 3, 1, 2, 4],
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
    "dk_crankymoves": [0x01, 0x21, 0x41, 0x12, 0x12, 0xFF, 0xFF],
    "dk_candymoves": [0x02, 0x22, 0x42, 0x12, 0x12, 0xFF, 0xFF],
    "dk_funkymoves": [0x03, 0x23, 0x43, 0x12, 0x12, 0xFF, 0xFF],
    "tiny_funkymoves": [0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02],
    "kut_out_kong_order": [0, 0, 0, 0, 0],
    "remove_blockers": 0x7F,
    "resolve_bonus": 0,
    "disable_drops": 1,
    "shop_indicator_on": 1,
    "warp_to_isles_enabled": 1,
    "lobbies_open_bitfield": 0,
    "perma_lose_kongs": 0,
    "jetpac_medal_requirement": 1,
    "kong_recolor_enabled": 1,
    "dk_color": 1,
    "diddy_color": 1,
    "lanky_color": 1,
    "tiny_color": 1,
    "chunky_color": 1,
    "starting_kong": 3,
    "free_target_llama": 0,
    "free_source_llama": 3,
    "keys_preturned": 0x01,
    "special_move_prices": [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 2, 3],
        [4, 5, 6],
    ],
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
        if x == "special_move_prices":
            for y in struct_data2:
                if x == y[2]:
                    size = y[1]
                    offset = y[0]
                    for kong in set_variables["special_move_prices"]:
                        for lvl in kong:
                            writeToROM(offset, lvl, size, x)
                            offset += size

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
