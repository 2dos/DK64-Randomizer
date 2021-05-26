"""Validate the seed we generated."""
from validator_data import golden_bananas
import copy


kong_list = ["dk", "diddy", "lanky", "tiny", "chunky"]


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
    validation_logs = []
    validation_logs.append("Starting validation")
    validation_logs.append("")
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
    keys_acquired = {}
    for key in range(8):
        keys_acquired["key_" + str(key + 1)] = False
    moves_acquired = {
        "dive": True,
        "orange": True,
        "barrel": True,
        "vine": True,
        "slam": 1,
        "ammo_belt": 0,
        "homing": all_moves,
        "sniper": all_moves,
    }
    for kong in kong_list:
        amount = 0
        if all_moves:
            amount = 3
            moves_acquired["ammo_belt"] = 2
            moves_acquired["slam"] = 3
        moves_acquired[kong + "_cranky"] = amount
        moves_acquired["gun_" + kong] = all_moves
        moves_acquired["ins_" + kong] = all_moves

    banana_cache = copy.deepcopy(golden_bananas)
    gbs_collected = 0
    levels = ["japes", "aztec", "factory", "galleon", "fungi", "caves", "castle"]
    highest_level_entered = -1
    level_progress = 0
    lobby_access = [level_order[0]]
    recheck = False

    start_gb_count = 0
    while True:
        start_gb_count = gbs_collected
        if not recheck:
            validation_logs.append("Level " + str(level_progress + 1) + " / 8:")
        # Check Isles EVERY TIME
        for i in range(len(banana_cache["isles"])):
            if not banana_cache["isles"][i]["collected"]:
                if checkMoves(
                    "isles",
                    banana_cache["isles"][i],
                    moves_acquired,
                    kongs_unlocked,
                    lobby_access,
                    keys_acquired,
                ):
                    gbs_collected += 1
                    banana_cache["isles"][i]["collected"] = True

        # Check if has enough for B. Locker
        if b_locker_array[level_progress] > gbs_collected:
            validation_logs.append("Not enough GBs to enter level: " + levels[level_order[level_progress]])
            validation_logs.append("GBs Required: " + str(b_locker_array[level_progress]) + " GBs")
            validation_logs.append("Max GBs possible: " + str(gbs_collected) + " GBs")
            break
        else:
            validation_logs.append("Able to enter next level: " + levels[level_order[level_progress]])
            validation_logs.append("Current GB Count: " + str(gbs_collected))
            # Buy Moves
            new_moves = 0
            if level_order[level_progress] > highest_level_entered:
                moves_allowed = []
                for m in range(level_order[level_progress] - highest_level_entered):
                    for move in moves_level_purchasing[m + highest_level_entered + 1]:
                        moves_allowed.append(move)
                moves_allowed = list(dict.fromkeys(moves_allowed))
                for n in moves_allowed:
                    new_moves += 1
                    if isinstance(moves_acquired[n], int):
                        moves_acquired[n] += 1
                    elif isinstance(moves_acquired[n], bool):
                        moves_acquired[n] = True
                highest_level_entered = level_order[level_progress]
                validation_logs.append(str(new_moves) + " new moves acquired")

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
                                    if kongs_unlocked[boss_kong_required[level_order[i]]]:
                                        for kong in kong_list:
                                            if not kongs_unlocked[kong]:
                                                validation_logs.append(kong + " Unlocked")
                                            kongs_unlocked[kong] = True
                        for j in range(len(banana_cache[level_name])):
                            if not banana_cache[level_name][j]["collected"]:
                                if checkMoves(
                                    level_name,
                                    banana_cache[level_name][j],
                                    moves_acquired,
                                    kongs_unlocked,
                                    lobby_access,
                                    keys_acquired,
                                ):
                                    second_pass = False
                                    for kong in kong_list:
                                        if banana_cache[level_name][j]["frees_" + kong]:
                                            second_pass = True
                                            if not kongs_unlocked[kong]:
                                                validation_logs.append(kong + " Unlocked")
                                            kongs_unlocked[kong] = True
                                    if second_pass:
                                        gbs_collected += 1
                                        banana_cache[level_name][j]["collected"] = True
            # Check if can free kongs
            for i in lobby_access:
                level_name = levels[i]
                for j in range(len(banana_cache[level_name])):
                    if not banana_cache[level_name][j]["collected"]:
                        if checkMoves(
                            level_name,
                            banana_cache[level_name][j],
                            moves_acquired,
                            kongs_unlocked,
                            lobby_access,
                            keys_acquired,
                        ):
                            gbs_collected += 1
                            banana_cache[level_name][j]["collected"] = True

            kongs_unlocked_count = 0
            for i in kongs_unlocked.keys():
                if kongs_unlocked[i]:
                    kongs_unlocked_count += 1
            cb_count = kongs_unlocked_count * 100

            # End of level checks
            if gbs_collected == start_gb_count:
                recheck = False
                if (
                    tns_array[level_progress] > cb_count
                    or not kongs_unlocked[boss_kong_required[level_order[level_progress]]]
                ):
                    if not kongs_unlocked[boss_kong_required[level_order[level_progress]]]:
                        validation_logs.append(
                            "Do not have the kong required to fight boss: " + levels[level_order[level_progress]]
                        )
                        validation_logs.append("Kong Required: " + boss_kong_required[level_order[level_progress]])
                    else:
                        validation_logs.append("Not enough CBs to enter boss: " + levels[level_order[level_progress]])
                        validation_logs.append("CBs Required: " + str(tns_array[level_progress]) + " CBs")
                        validation_logs.append("Max CBs possible: " + str(cb_count) + " CBs")
                    break

                else:
                    validation_logs.append("End of level GB Count: " + str(gbs_collected))
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
                        successful = True
                        break
                    else:
                        level_progress = level_progress + 1
                        validation_logs.append("")
            else:
                recheck = True
                validation_logs.append(
                    "Rechecking due to potential difference. Current GB Count: " + str(gbs_collected)
                )

    if successful:
        validation_logs.append("SUCCESSFUL SEED")
        # print('\n'.join(map(str, validation_logs)))
        return True
    validation_logs.append("BAD SEED")
    # print('\n'.join(map(str, validation_logs)))
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
    if gb_object["ammo_belt"] > moves["ammo_belt"]:
        passes = False
    if gb_object["homing"] and not moves["homing"]:
        passes = False
    if gb_object["sniper"] and not moves["sniper"]:
        passes = False
    for kong in kong_list:
        if gb_object[kong + "_cranky"] > moves[kong + "_cranky"]:
            passes = False
        if gb_object["gun_" + kong] and not moves["gun_" + kong]:
            passes = False
        if gb_object["kong_" + kong] and not kongs[kong]:
            passes = False
        if gb_object["ins_" + kong] and not moves["ins_" + kong]:
            passes = False
    if level == "isles":
        for j in range(8):
            if gb_object["requires_key" + str(j + 1)] and not keys["key_" + str(j + 1)]:
                passes = False
            if gb_object["in_vanillaLobby" + str(j + 1)] and j not in access:
                passes = False
    return passes
