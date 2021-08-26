"""Randomize your seed via your settings."""
from random import seed, shuffle

from browser import document

from object_data.form_options import asm_options
from validator import validateSeed


def randomize(post_data):
    """Randomize the seed.

    Args:
        query_string (dict): Form data query string.

    Returns:
        str: ASM Data.
    """
    for option in post_data:
        if post_data[option] == "True":
            post_data[option] = True
        elif post_data[option] == "False":
            post_data[option] = False
    if post_data.get("recursion", 0) > 3:
        return False
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

    asm = str()
    rando_params = []
    logdata = str()
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
        seed(str(post_data.get("seed")) + str(post_data))
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

    for asm_data in asm_options:
        if asm_data.append == True:
            asm += asm_data.generate_asm(data="randomize_progression")
        else:
            asm += asm_data.generate_asm()

    asm += "\t" + ".half 0" + "\n"  # Null Terminator (required)
    if post_data.get("generate_spoilerlog"):
        document["nav-spoiler-tab"].style.display = ""
        document["spoiler_log_text"].text = logdata
    else:
        document["nav-spoiler-tab"].style.display = "none"
        document["spoiler_log_text"].text = ""
    print("Validating Seeds")
    if validateSeed(
        finalNumerical,
        post_data.get("unlock_all_kongs", False),
        post_data.get("unlock_all_moves", False),
        post_data.get("quality_of_life", False),
        finalBLocker,
        finalTNS,
        True,
    ):
        return asm
    else:
        print("Retrying generation")
        post_data["seed"] = int(post_data.get("seed")) + 1
        post_data["recursion"] = post_data.get("recursion", 0)
        post_data["recursion"] = post_data["recursion"] + 1
        result = randomize(post_data)
        return result
