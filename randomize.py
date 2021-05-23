"""Randomize your seed via your settings."""
from random import seed, shuffle
from validator import validateSeed
from browser import window, document


def randomize(query_string):
    """Randomize the seed.

    Args:
        query_string (str): Form data query string.

    Returns:
        str: ASM Data.
    """
    post_data = dict((itm.split("=")[0], itm.split("=")[1]) for itm in query_string.split("&"))
    levelEntrances = [
        "Jungle Japes",
        "Angry Aztec",
        "Frantic Factory",
        "Gloomy Galleon",
        "Fungi Forest",
        "Crystal Caves",
        "Creepy Castle",
    ]

    # Arrays for Finalized Setting Values
    finalBLocker = []
    finalTNS = []
    finalNumerical = [0, 1, 2, 3, 4, 5, 6]
    finalKeyFlags = [
        "0x001A",
        "0x004A",
        "0x008A",
        "0x00A8",
        "0x00EC",
        "0x0124",
        "0x013D",
    ]
    finalLevels = levelEntrances[:]

    # Open default mod file
    with open("./patches/asmFunctions.asm", "r") as file:
        asm = file.read()
    logdata = ""
    # Write Settings to Spoiler Log
    logdata += "Randomizer Settings" + "\n"
    logdata += "-------------------" + "\n"
    logdata += "Level Progression Randomized: " + str(post_data.get("randomize_progression", "False")) + "\n"
    if post_data.get("randomize_progression"):
        logdata += "Seed: " + str(post_data.get("seed")) + "\n"
    logdata += "All Kongs Unlocked: " + str(post_data.get("unlock_all_kongs", "False")) + "\n"
    logdata += "All Moves Unlocked: " + str(post_data.get("unlock_all_moves", "False")) + "\n"
    logdata += "Fairy Queen Camera + Shockwave: " + str(post_data.get("unlock_fairy_shockwave", "False")) + "\n"
    logdata += "Tag Anywhere Enabled: " + str(post_data.get("enable_tag_anywhere", "False")) + "\n"
    logdata += "Fast Start - Beginning of Game: " + str(post_data.get("fast_start_beginning_of_game", "False")) + "\n"
    logdata += "Fast Start - Hideout Helm: " + str(post_data.get("fast_start_hideout_helm", "False")) + "\n"
    logdata += "Open Crown Door: " + str(post_data.get("crown_door_open", "False")) + "\n"
    logdata += "Open Nintendo + Rareware Coin Door: " + str(post_data.get("coin_door_open", "False")) + "\n"
    logdata += "Quality of Life Changes: " + str(post_data.get("quality_of_life", "False")) + "\n"
    logdata += "\n"

    # Fill Arrays with chosen game length values
    if post_data.get("randomize_progression"):
        for k in post_data:
            if "troff_" in k and k[-1].isnumeric():
                finalTNS.append(int(post_data[k]))
            if "blocker_" in k and k[-1].isnumeric():
                finalBLocker.append(int(post_data[k]))
    else:
        finalBLocker = [1, 5, 15, 30, 50, 65, 80, 100]
        finalTNS = [60, 120, 200, 250, 300, 350, 400]

    # Shuffle Level Progression
    if post_data.get("randomize_progression"):
        asm += ".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 1" + "\n" + "\n"  # Run Randomizer in ASM
        seed(post_data.get("seed"))
        shuffle(finalLevels)
        logdata += "Level Order: " + "\n"
        asm += ".align" + "\n" + "LevelOrder:" + "\n"

        # Set Level Order in ASM and Spoiler Log
        for x in finalLevels:
            if str(x) == "Jungle Japes":
                finalNumerical[finalLevels.index(x)] = 0
            elif str(x) == "Angry Aztec":
                finalNumerical[finalLevels.index(x)] = 1
            elif str(x) == "Frantic Factory":
                finalNumerical[finalLevels.index(x)] = 2
            elif str(x) == "Gloomy Galleon":
                finalNumerical[finalLevels.index(x)] = 3
            elif str(x) == "Fungi Forest":
                finalNumerical[finalLevels.index(x)] = 4
            elif str(x) == "Crystal Caves":
                finalNumerical[finalLevels.index(x)] = 5
            elif str(x) == "Creepy Castle":
                finalNumerical[finalLevels.index(x)] = 6
            logdata += str(finalLevels.index(x) + 1) + ". " + x + " "
            logdata += "(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, "
            logdata += "Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)"
            logdata += "\n"
            asm += "\t" + ".byte " + str(finalNumerical[finalLevels.index(x)])
            asm += "\n"
        logdata += "8. Hideout Helm "
        logdata += "(B Locker: " + str(finalBLocker[7]) + " GB)"
        asm += "\t" + ".byte 7"  # Helm should always be set to position 8 in the array
        asm += "\n" + "\n"
    else:
        asm += ".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 0" + "\n" + "\n"  # Dont run Randomizer in ASM

    # Set B Lockers in ASM
    asm += ".align" + "\n" + "BLockerDefaultAmounts:" + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[7])  # Helm B Locker always uses last value in level array
    asm += "\n" + "\n"

    # ANTI CHEAT (set GB amounts to the B Locker post in-game cheat code)
    asm += ".align" + "\n" + "BLockerCheatAmounts:" + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n"
    asm += "\t" + ".half " + str(finalBLocker[7])  # Helm B Locker always uses last value in level array
    asm += "\n" + "\n"

    # Set Troff n Scoffs in ASM
    asm += ".align" + "\n" + "TroffNScoffAmounts:" + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Jungle Japes")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Angry Aztec")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Frantic Factory")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Gloomy Galleon")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Fungi Forest")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Crystal Caves")]) + "\n"
    asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Creepy Castle")]) + "\n"
    asm += "\t" + ".half 1"  # Isles TNS should always be set to 1
    asm += "\n" + "\n"

    # Set Keys
    asm += ".align" + "\n" + "KeyFlags:" + "\n"
    for x in finalNumerical:
        asm += "\t" + ".half " + str(finalKeyFlags[x]) + "\n"
    asm += "\n" + "\n"

    # Unlock All Kongs
    asm += ".align" + "\n" + "KongFlags:" + "\n"
    if post_data.get("unlock_all_kongs"):
        asm += "\t" + ".half 385" + "\n"  # DK
        asm += "\t" + ".half 6" + "\n"  # Diddy
        asm += "\t" + ".half 70" + "\n"  # Lanky
        asm += "\t" + ".half 66" + "\n"  # Tiny
        asm += "\t" + ".half 117" + "\n"  # Chunky
    asm += "\t" + ".half 0" + "\n" + "\n"  # Null Terminator (required)

    # Unlock All Moves
    asm += ".align" + "\n" + "UnlockAllMoves:" + "\n"
    if post_data.get("unlock_all_moves"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"
    asm += ".align" + "\n" + "SniperValue:" + "\n" + "\t" + ".byte 0x3" + "\n" + "\n"  # Sniper Scope: 3 = off, 7 = on

    # Unlock Camera + Shockwave
    asm += ".align" + "\n" + "FairyQueenRewards:" + "\n"
    if post_data.get("unlock_fairy_shockwave"):
        asm += "\t" + ".half 377" + "\n"  # BFI Camera/Shockwave
    asm += "\t" + ".half 0" + "\n" + "\n"  # Null Terminator (required)

    # Enable Tag Anywhere
    asm += ".align" + "\n" + "TagAnywhereOn:" + "\n"
    if post_data.get("enable_tag_anywhere"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"

    # Fast Start Hideout Helm
    asm += ".align" + "\n" + "FastStartHelmOn:" + "\n"
    if post_data.get("fast_start_hideout_helm"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"

    # Open Crown Door
    asm += ".align" + "\n" + "CrownDoorOption:" + "\n"
    if post_data.get("crown_door_open"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"

    # Open Nintendo + Rareware Coin Door
    asm += ".align" + "\n" + "CoinDoorOption:" + "\n"
    if post_data.get("coin_door_open"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"

    # Quality of Life Changes
    asm += ".align" + "\n" + "QualityChangesOn:" + "\n"
    if post_data.get("quality_of_life"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"

    # Fast Start
    asm += ".align" + "\n" + "FastStartOn:" + "\n"
    if post_data.get("fast_start_beginning_of_game"):
        asm += "\t" + ".byte 1" + "\n" + "\n"
    else:
        asm += "\t" + ".byte 0" + "\n" + "\n"
    asm += ".align" + "\n" + "FastStartFlags:" + "\n"
    if post_data.get("fast_start_beginning_of_game"):
        asm += "\t" + ".half 386" + "\n"  # Dive Barrel
        asm += "\t" + ".half 387" + "\n"  # Vine Barrel
        asm += "\t" + ".half 388" + "\n"  # Orange Barrel
        asm += "\t" + ".half 389" + "\n"  # Barrel Barrel
        asm += "\t" + ".half 0x1BB" + "\n"  # Japes Boulder Smashed
        asm += "\t" + ".half 0x186" + "\n"  # Isles Escape CS
        asm += "\t" + ".half 0x17F" + "\n"  # Training Barrels Spawned
        asm += "\t" + ".half 0x180" + "\n"  # Cranky has given Sim Slam
        asm += "\t" + ".half 385" + "\n"  # DK Free
    asm += "\t" + ".half 0" + "\n"  # Null Terminator (required)
    if post_data.get("generate_spoilerlog"):
        document["nav-spoiler-tab"].style.display = ""
        document["spoiler_log_text"].text = logdata
    else:
        document["nav-spoiler-tab"].style.display = "none"
        document["spoiler_log_text"].text = ""
    # TODO: We need to properly validate the seed and block depending on the results
    validateSeed(
        finalNumerical,
        post_data.get("unlock_all_kongs"),
        post_data.get("unlock_all_moves"),
        post_data.get("quality_of_life"),
        finalBLocker,
        finalTNS,
        True,
    )
    return asm


window.randomize_data = randomize
