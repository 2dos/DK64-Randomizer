"""Generate ROM patch files."""
import os
import shutil
import sys
from random import seed, shuffle


def randomize(submittedForm):
    """Randomize the rom using the form data.

    Args:
        submittedForm (dict): Post data from the form.
    """
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

    # Start Spoiler Log and ASM Generation
    shutil.copy2(
        os.path.join(sys.path[0], "asmFunctions.asm"),
        os.path.join(sys.path[0], "settings.asm"),
    )
    log = open(os.path.join(sys.path[0], "spoilerlog.txt"), "w+")
    asm = open(os.path.join(sys.path[0], "settings.asm"), "a+")

    # Write Settings to Spoiler Log
    log.write("Randomizer Settings" + "\n")
    log.write("-------------------" + "\n")
    log.write("Level Progression Randomized: " + str(submittedForm.get("randomize_progression", "False")) + "\n")
    if submittedForm.get("randomize_progression"):
        log.write("Seed: " + str(submittedForm.get("seed")) + "\n")
    log.write("All Kongs Unlocked: " + str(submittedForm.get("unlock_all_kongs", "False")) + "\n")
    log.write("All Moves Unlocked: " + str(submittedForm.get("unlock_all_moves", "False")) + "\n")
    log.write("Fairy Queen Camera + Shockwave: " + str(submittedForm.get("unlock_fairy_shockwave", "False")) + "\n")
    log.write("Tag Anywhere Enabled: " + str(submittedForm.get("enable_tag_anywhere", "False")) + "\n")
    log.write("Shorter Hideout Helm: " + str(submittedForm.get("shorter_hideout_helm", "False")) + "\n")
    log.write("Quality of Life Changes: " + str(submittedForm.get("quality_of_life", "False")) + "\n")
    log.write("\n")

    # Fill Arrays with chosen game length values
    if submittedForm.get("randomize_progression"):
        for k in submittedForm:
            if "troff_" in k and k[-1].isnumeric():
                finalTNS.append(str(submittedForm[k]))
            if "blocker_" in k and k[-1].isnumeric():
                finalBLocker.append(str(submittedForm[k]))
    else:
        finalBLocker = [1, 5, 15, 30, 50, 65, 80, 100]
        finalTNS = [60, 120, 200, 250, 300, 350, 400]

    # Shuffle Level Progression
    if submittedForm.get("randomize_progression"):
        asm.write(".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 1" + "\n" + "\n")  # Run Randomizer in ASM
        seed(submittedForm.get("seed"))
        shuffle(finalLevels)
        log.write("Level Order: " + "\n")
        asm.write(".align" + "\n" + "LevelOrder:" + "\n")

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
            log.write(str(finalLevels.index(x) + 1) + ". " + x + " ")
            log.write("(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, ")
            log.write("Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)")
            log.write("\n")
            asm.write("\t" + ".byte " + str(finalNumerical[finalLevels.index(x)]))
            asm.write("\n")
        log.write("8. Hideout Helm ")
        log.write("(B Locker: " + str(finalBLocker[7]) + " GB)")
        asm.write("\t" + ".byte 7")  # Helm should always be set to position 8 in the array
        asm.write("\n" + "\n")
    else:
        asm.write(".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 0" + "\n" + "\n")  # Dont run Randomizer in ASM

    # Set B Lockers in ASM
    asm.write(".align" + "\n" + "BLockerDefaultAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[7]))  # Helm B Locker always uses last value in level array
    asm.write("\n" + "\n")

    # ANTI CHEAT (set GB amounts to the B Locker post in-game cheat code)
    asm.write(".align" + "\n" + "BLockerCheatAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[7]))  # Helm B Locker always uses last value in level array
    asm.write("\n" + "\n")

    # Set Troff n Scoffs in ASM
    asm.write(".align" + "\n" + "TroffNScoffAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half 1")  # Isles TNS should always be set to 1
    asm.write("\n" + "\n")

    # Set Keys
    asm.write(".align" + "\n" + "KeyFlags:" + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\n" + "\n")

    # Unlock All Kongs
    asm.write(".align" + "\n" + "KongFlags:" + "\n")
    if submittedForm.get("unlock_all_kongs"):
        asm.write("\t" + ".half 385" + "\n")  # DK
        asm.write("\t" + ".half 6" + "\n")  # Diddy
        asm.write("\t" + ".half 70" + "\n")  # Lanky
        asm.write("\t" + ".half 66" + "\n")  # Tiny
        asm.write("\t" + ".half 117" + "\n")  # Chunky
    asm.write("\t" + ".half 0" + "\n" + "\n")  # Null Terminator (required)

    # Unlock All Moves
    asm.write(".align" + "\n" + "UnlockAllMoves:" + "\n")
    if submittedForm.get("unlock_all_moves"):
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")
    asm.write(
        ".align" + "\n" + "SniperValue:" + "\n" + "\t" + ".byte 0x3" + "\n" + "\n"
    )  # Sniper Scope: 3 = off, 7 = on

    # Unlock Camera + Shockwave
    asm.write(".align" + "\n" + "FairyQueenRewards:" + "\n")
    if submittedForm.get("unlock_fairy_shockwave"):
        asm.write("\t" + ".half 377" + "\n")  # BFI Camera/Shockwave
    asm.write("\t" + ".half 0" + "\n" + "\n")  # Null Terminator (required)

    # Enable Tag Anywhere
    asm.write(".align" + "\n" + "TagAnywhereOn:" + "\n")
    if submittedForm.get("enable_tag_anywhere"):
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Shorter Hideout Helm
    asm.write(".align" + "\n" + "ShorterHelmOn:" + "\n")
    if submittedForm.get("shorter_hideout_helm"):
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Quality of Life Changes
    asm.write(".align" + "\n" + "QualityChangesOn:" + "\n")
    if submittedForm.get("quality_of_life"):
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Fast Start
    asm.write(".align" + "\n" + "FastStartFlags:" + "\n")
    if submittedForm.get("quality_of_life"):
        asm.write("\t" + ".half 386" + "\n")  # Dive Barrel
        asm.write("\t" + ".half 387" + "\n")  # Vine Barrel
        asm.write("\t" + ".half 388" + "\n")  # Orange Barrel
        asm.write("\t" + ".half 389" + "\n")  # Barrel Barrel
        asm.write("\t" + ".half 0x1BB" + "\n")  # Japes Boulder Smashed
        asm.write("\t" + ".half 0x186" + "\n")  # Isles Escape CS
        asm.write("\t" + ".half 0x17F" + "\n")  # Training Barrels Spawned
        asm.write("\t" + ".half 0x180" + "\n")  # Cranky has given Sim Slam
        asm.write("\t" + ".half 385" + "\n")  # DK Free
    asm.write("\t" + ".half 0" + "\n")  # Null Terminator (required)

    log.close()
    asm.close()
