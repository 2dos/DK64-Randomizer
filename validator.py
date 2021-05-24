"""Validate the seed we generated."""
from validator_data import golden_bananas


def validateSeed(
    level_order: list,
    all_kongs: bool,
    all_moves: bool,
    fast_start: bool,
    b_locker_array: dict,
    tns_array: dict,
    castle_kongs: bool,
):
    """Fully validate a seed we have generated.

    Args:
        level_order (list): List of level orders.
        all_kongs (bool): If all kongs should be unlocked from the start.
        all_moves (bool): If all moves should be unlocked from the start.
        fast_start (bool): Defines if we should be skipping early game for a faster game start.
        b_locker_array (dict): The B-Locker requirements for each level.
        tns_array (dict): The standard bannana requirements for each level.
        castle_kongs (bool): If all kongs are unlocked for the castle.

    Returns:
        bool: If we succeeded generation of the seed or not.
    """
    # Validator for a seed in DK64
    # Assumptions:
    # If you can enter a level, you can unlock every move up to that level, coins aren't a problem
    # Your CB count for a level = Kongs x 100

    print("Starting validation")
    print("")
    successful = False
    kongs_unlocked = {
        "dk": True,
        "diddy": all_kongs,
        "lanky": all_kongs,
        "tiny": all_kongs,
        "chunky": all_kongs,
    }
    moves_level_purchasing = [
        # Japes
        [
            "dk_cranky",
            "diddy_cranky",
            "lanky_cranky",
            "tiny_cranky",
            "chunky_cranky",
            "gun_dk",
            "gun_diddy",
            "gun_lanky",
            "gun_tiny",
            "gun_chunky",
        ],
        # Aztec
        ["dk_cranky", "diddy_cranky", "ins_dk", "ins_diddy", "ins_lanky", "ins_tiny", "ins_chunky"],
        # Factory
        ["dk_cranky", "diddy_cranky", "lanky_cranky", "tiny_cranky", "chunky_cranky", "ammo_belt"],
        # Galleon
        [],
        # Fungi
        ["slam", "homing"],
        # Caves
        ["lanky_cranky", "tiny_cranky", "chunky_cranky", "ammo_belt"],
        # Castle
        ["slam", "sniper"],
    ]
    boss_kong_required = ["dk", "diddy", "lanky", "tiny", "chunky", "dk", "lanky"]
    keys_acquired = {
        "key_1": False,
        "key_2": False,
        "key_3": False,
        "key_4": False,
        "key_5": False,
        "key_6": False,
        "key_7": False,
        "key_8": False,
    }
    moves_acquired = {
        "dive": True,
        "orange": True,
        "barrel": True,
        "vine": True,
        "dk_cranky": 0,
        "diddy_cranky": 0,
        "lanky_cranky": 0,
        "tiny_cranky": 0,
        "chunky_cranky": 0,
        "gun_dk": all_moves,
        "gun_diddy": all_moves,
        "gun_lanky": all_moves,
        "gun_tiny": all_moves,
        "gun_chunky": all_moves,
        "ins_dk": all_moves,
        "ins_diddy": all_moves,
        "ins_lanky": all_moves,
        "ins_tiny": all_moves,
        "ins_chunky": all_moves,
        "slam": 1,
        "ammo_belt": 0,
        "homing": all_moves,
        "sniper": all_moves,
    }
    if all_moves:
        moves_acquired["dk_cranky"] = 3
        moves_acquired["diddy_cranky"] = 3
        moves_acquired["lanky_cranky"] = 3
        moves_acquired["tiny_cranky"] = 3
        moves_acquired["chunky_cranky"] = 3
        moves_acquired["ammo_belt"] = 2
        moves_acquired["slam"] = 3
    loop_control = True
    banana_cache = golden_bananas.copy()
    gbs_collected = 0
    levels = ["japes", "aztec", "factory", "galleon", "fungi", "caves", "castle"]
    highest_level_entered = -1
    level_progress = 0
    lobby_access = [level_order[0]]
    castle_order_position = -1
    recheck = False
    for i in range(7):
        if level_order[i] == 6:
            castle_order_position = i
            print(f"Castle Position: {castle_order_position}")

    while loop_control:
        start_gb_count = gbs_collected
        if not recheck:
            print("Level " + str(level_progress + 1) + " / 8:")
        # Check Isles
        for i in range(len(banana_cache["isles"])):
            x = banana_cache["isles"][i]
            if not x["collected"]:
                passes = checkMoves(
                    "isles",
                    x.copy(),
                    moves_acquired.copy(),
                    kongs_unlocked.copy(),
                    lobby_access.copy(),
                    keys_acquired.copy(),
                )
                if passes:
                    gbs_collected += 1
                    x["collected"] = True
                    # print(x["name"])

        # Check if has enough for B. Locker
        if b_locker_array[level_progress] > gbs_collected:
            loop_control = False
            print("Not enough GBs to enter level: " + levels[level_order[level_progress]])
            print("GBs Required: " + str(b_locker_array[level_progress]) + " GBs")
            print("Max GBs possible: " + str(gbs_collected) + " GBs")
        else:
            print("Able to enter next level: " + levels[level_order[level_progress]])
            print("Current GB Count: " + str(gbs_collected))
            # Buy Moves
            new_moves = 0
            if level_order[level_progress] > highest_level_entered:
                for m in range(level_order[level_progress] - highest_level_entered):
                    level_moves = moves_level_purchasing[m + highest_level_entered + 1]
                    for n in level_moves:
                        new_moves += 1
                        if "int" in str(type(moves_acquired[n])):
                            moves_acquired[n] += 1
                        elif "bool" in str(type(moves_acquired[n])):
                            moves_acquired[n] = True
                highest_level_entered = level_order[level_progress]
                print(str(new_moves) + " new moves acquired")

            # Check if can free kongs
            for i in range(7):
                level_name = levels[level_order[i]]
                if level_order[i] in lobby_access:
                    if gbs_collected > b_locker_array[level_order[i]]:
                        if level_order[i] == 6:  # Castle
                            if castle_kongs:
                                castle_cb_req = tns_array[i]
                                kongs_unlocked_count = 0
                                for k in kongs_unlocked.keys():
                                    if kongs_unlocked[k]:
                                        kongs_unlocked_count += 1
                                castle_cb_count = kongs_unlocked_count * 100
                                if castle_cb_req > castle_cb_count:
                                    kong_string = boss_kong_required[level_order[i]]
                                    if kongs_unlocked[kong_string]:
                                        if not kongs_unlocked["dk"]:
                                            print("DK Unlocked")
                                        kongs_unlocked["dk"] = True
                                        if not kongs_unlocked["diddy"]:
                                            print("Diddy Unlocked")
                                        kongs_unlocked["diddy"] = True
                                        if not kongs_unlocked["lanky"]:
                                            print("Lanky Unlocked")
                                        kongs_unlocked["lanky"] = True
                                        if not kongs_unlocked["tiny"]:
                                            print("Tiny Unlocked")
                                        kongs_unlocked["tiny"] = True
                                        if not kongs_unlocked["chunky"]:
                                            print("Chunky Unlocked")
                                        kongs_unlocked["chunky"] = True
                        for j in range(len(banana_cache[level_name])):
                            x = banana_cache[level_name][j]
                            if not x["collected"]:
                                passes = checkMoves(
                                    level_name,
                                    x.copy(),
                                    moves_acquired.copy(),
                                    kongs_unlocked.copy(),
                                    lobby_access.copy(),
                                    keys_acquired.copy(),
                                )
                                if passes:
                                    second_pass = False
                                    if x["frees_dk"]:
                                        second_pass = True
                                        if not kongs_unlocked["dk"]:
                                            print("DK Unlocked")
                                        kongs_unlocked["dk"] = True
                                    elif x["frees_diddy"]:
                                        second_pass = True
                                        if not kongs_unlocked["diddy"]:
                                            print("Diddy Unlocked")
                                        kongs_unlocked["diddy"] = True
                                    elif x["frees_lanky"]:
                                        second_pass = True
                                        if not kongs_unlocked["lanky"]:
                                            print("Lanky Unlocked")
                                        kongs_unlocked["lanky"] = True
                                    elif x["frees_tiny"]:
                                        second_pass = True
                                        if not kongs_unlocked["tiny"]:
                                            print("Tiny Unlocked")
                                        kongs_unlocked["tiny"] = True
                                    elif x["frees_chunky"]:
                                        second_pass = True
                                        if not kongs_unlocked["chunky"]:
                                            print("Chunky Unlocked")
                                        kongs_unlocked["chunky"] = True
                                    if second_pass:
                                        gbs_collected += 1
                                        x["collected"] = True

            # Check if can free kongs
            for i in lobby_access:
                level_name = levels[i]
                for j in range(len(banana_cache[level_name])):
                    x = banana_cache[level_name][j]
                    if not x["collected"]:
                        passes = checkMoves(
                            level_name,
                            x.copy(),
                            moves_acquired.copy(),
                            kongs_unlocked.copy(),
                            lobby_access.copy(),
                            keys_acquired.copy(),
                        )
                        if passes:
                            gbs_collected += 1
                            x["collected"] = True

            kongs_unlocked_count = 0
            for i in kongs_unlocked.keys():
                if kongs_unlocked[i]:
                    kongs_unlocked_count += 1

            cb_count = kongs_unlocked_count * 100
            kong_string = boss_kong_required[level_order[level_progress]]
            if gbs_collected == start_gb_count:
                recheck = False
                if tns_array[level_progress] > cb_count or not kongs_unlocked[kong_string]:
                    loop_control = False
                    if not kongs_unlocked[kong_string]:
                        print("Do not have the kong required to fight boss: " + levels[level_order[level_progress]])
                        print("Kong Required: " + boss_kong_required[level_order[level_progress]])
                    else:
                        print("Not enough CBs to enter boss: " + levels[level_order[level_progress]])
                        print("CBs Required: " + str(tns_array[level_progress]) + " CBs")
                        print("Max CBs possible: " + str(cb_count) + " CBs")

                else:
                    print("End of level GB Count: " + str(gbs_collected))
                    key_string = "key_" + str(level_progress + 1)
                    keys_acquired[key_string] = True
                    if level_progress == 0:  # Key 1
                        lobby_access.append(level_order[1])
                    elif level_progress == 1:  # Key 2
                        lobby_access.append(level_order[2])
                        lobby_access.append(level_order[3])
                    elif level_progress == 3:  # Key 4
                        lobby_access.append(level_order[4])
                    elif level_progress == 4:  # Key 5
                        lobby_access.append(level_order[5])
                        lobby_access.append(level_order[6])
                    if level_progress == 6:
                        loop_control = False
                        successful = True
                    else:
                        level_progress = level_progress + 1
                        print("")
            else:
                recheck = True
                print("Rechecking due to potential difference. Current GB Count: " + str(gbs_collected))

    if successful:
        print("SUCCESSFUL SEED")
        return True
    print("BAD SEED")
    return False


def checkMoves(level, gb_object, moves, kongs, access, keys):
    """Check if moves should be open.

    Args:
        level ([type]): [description]
        gb_object ([type]): [description]
        moves ([type]): [description]
        kongs ([type]): [description]
        access ([type]): [description]
        keys ([type]): [description]

    Returns:
        [type]: [description]
    """
    # print(gb_object)
    passes = True
    if gb_object["dive"] and not moves["dive"]:
        passes = False
    if gb_object["orange"] and not moves["orange"]:
        passes = False
    if gb_object["barrel"] and not moves["barrel"]:
        passes = False
    if gb_object["vine"] and not moves["vine"]:
        passes = False
    if gb_object["slam"] > moves["slam"]:
        passes = False
    if gb_object["dk_cranky"] > moves["dk_cranky"]:
        passes = False
    if gb_object["diddy_cranky"] > moves["diddy_cranky"]:
        passes = False
    if gb_object["lanky_cranky"] > moves["lanky_cranky"]:
        passes = False
    if gb_object["tiny_cranky"] > moves["tiny_cranky"]:
        passes = False
    if gb_object["chunky_cranky"] > moves["chunky_cranky"]:
        passes = False
    if gb_object["gun_dk"] and not moves["gun_dk"]:
        passes = False
    if gb_object["gun_diddy"] and not moves["gun_diddy"]:
        passes = False
    if gb_object["gun_lanky"] and not moves["gun_lanky"]:
        passes = False
    if gb_object["gun_tiny"] and not moves["gun_tiny"]:
        passes = False
    if gb_object["gun_chunky"] and not moves["gun_chunky"]:
        passes = False
    if gb_object["ammo_belt"] > moves["ammo_belt"]:
        passes = False
    if gb_object["homing"] and not moves["homing"]:
        passes = False
    if gb_object["sniper"] and not moves["sniper"]:
        passes = False
    if gb_object["kong_dk"] and not kongs["dk"]:
        passes = False
    if gb_object["kong_diddy"] and not kongs["diddy"]:
        passes = False
    if gb_object["kong_lanky"] and not kongs["lanky"]:
        passes = False
    if gb_object["kong_tiny"] and not kongs["tiny"]:
        passes = False
    if gb_object["kong_chunky"] and not kongs["chunky"]:
        passes = False
    if gb_object["ins_dk"] and not moves["ins_dk"]:
        passes = False
    if gb_object["ins_diddy"] and not moves["ins_diddy"]:
        passes = False
    if gb_object["ins_lanky"] and not moves["ins_lanky"]:
        passes = False
    if gb_object["ins_tiny"] and not moves["ins_tiny"]:
        passes = False
    if gb_object["ins_chunky"] and not moves["ins_chunky"]:
        passes = False
    if level == "isles":
        if gb_object["requires_key1"] and not keys["key_1"]:
            passes = False
        if gb_object["requires_key2"] and not keys["key_2"]:
            passes = False
        if gb_object["requires_key3"] and not keys["key_3"]:
            passes = False
        if gb_object["requires_key4"] and not keys["key_4"]:
            passes = False
        if gb_object["requires_key5"] and not keys["key_5"]:
            passes = False
        if gb_object["requires_key6"] and not keys["key_6"]:
            passes = False
        if gb_object["requires_key7"] and not keys["key_7"]:
            passes = False
        if gb_object["requires_key8"] and not keys["key_8"]:
            passes = False
        for j in range(8):
            lobby_prop = "in_vanillaLobby" + str(j + 1)
            if gb_object[lobby_prop] and j not in access:
                passes = False
    return passes
