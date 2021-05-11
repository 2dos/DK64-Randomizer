"""Generate ROM patch files."""
import os
import shutil
import sys
import subprocess
from random import seed, shuffle
from type_swap import convert_format
import time


debug_printout = False


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

    # Copy ASM Functions to Settings so we have a baseline
    shutil.copy2(
        f"{sys.path[0]}/patchfiles/asmFunctions.asm",
        f"{sys.path[0]}/settings-{submittedForm.get('seed')}.asm",
    )
    # Start modification file
    asm = open(f"{sys.path[0]}/settings-{submittedForm.get('seed')}.asm", "a+")
    logdata = ""
    # Write Settings to Spoiler Log
    logdata += "Randomizer Settings" + "\n"
    logdata += "-------------------" + "\n"
    logdata += "Level Progression Randomized: " + str(submittedForm.get("randomize_progression", "False")) + "\n"
    if submittedForm.get("randomize_progression"):
        logdata += "Seed: " + str(submittedForm.get("seed")) + "\n"
    logdata += "All Kongs Unlocked: " + str(submittedForm.get("unlock_all_kongs", "False")) + "\n"
    logdata += "All Moves Unlocked: " + str(submittedForm.get("unlock_all_moves", "False")) + "\n"
    logdata += "Fairy Queen Camera + Shockwave: " + str(submittedForm.get("unlock_fairy_shockwave", "False")) + "\n"
    logdata += "Tag Anywhere Enabled: " + str(submittedForm.get("enable_tag_anywhere", "False")) + "\n"
    logdata += "Shorter Hideout Helm: " + str(submittedForm.get("shorter_hideout_helm", "False")) + "\n"
    logdata += "Quality of Life Changes: " + str(submittedForm.get("quality_of_life", "False")) + "\n"
    logdata += "\n"

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
        logdata += "Level Order: " + "\n"
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
            logdata += str(finalLevels.index(x) + 1) + ". " + x + " "
            logdata += "(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, "
            logdata += "Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)"
            logdata += "\n"
            asm.write("\t" + ".byte " + str(finalNumerical[finalLevels.index(x)]))
            asm.write("\n")
        logdata += "8. Hideout Helm "
        logdata += "(B Locker: " + str(finalBLocker[7]) + " GB)"
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

    if submittedForm.get("generate_spoilerlog"):
        with open(f"{sys.path[0]}/spoilerlog-{submittedForm.get('seed')}.txt", "w+") as file:
            file.write(logdata)

    asm.close()

    # TODO: Support Linux as well
    print("Applying BPS file")
    convert_format(infile=f"{sys.path[0]}/temprom.rom", outfile=f"{sys.path[0]}/DK64-{submittedForm.get('seed')}.z64")
    if os.path.exists(f"{sys.path[0]}/temprom.rom"):
        os.remove(f"{sys.path[0]}/temprom.rom")
    subprocess.run(
        [
            f"{sys.path[0]}/libs/flips/flips.exe",
            "--apply",
            f"{sys.path[0]}/patchfiles/DK64 Rando Setup Patch.bps",
            f"{sys.path[0]}/DK64-{submittedForm.get('seed')}.z64",
        ]
    )
    time.sleep(5)
    wd = os.getcwd()
    os.chdir(f"{sys.path[0]}/libs/asm2gs")
    process = subprocess.run(
        [
            f"{sys.path[0]}/libs/lua/lua5.1.exe",
            "-l",
            "loadASM",
            "-e",
            f"loadASMPatch('../../settings-{submittedForm.get('seed')}.asm')",
        ],
        shell=True,
    )
    os.chdir(wd)
    time.sleep(5)
    if process.returncode == 0:
        with open("codeOutput.txt", "r") as file:
            for x in file:
                line = x
                segs = line.split(":")
                processBytePatch(f"DK64-{submittedForm.get('seed')}.z64", int(segs[0]), int(segs[1]))
        # apply crc patch
        with open(f"DK64-{submittedForm.get('seed')}.z64", "r+b") as fh:
            fh.seek(0x3154)
            fh.write(bytearray([0, 0, 0, 0]))
        crcresult = subprocess.check_output([f"{sys.path[0]}/libs/n64crc.exe", f"DK64-{submittedForm.get('seed')}.z64"])
        print(crcresult)
    else:
        print("Build failed")
    if debug_printout is False:
        if os.path.exists(f"{sys.path[0]}/codeOutput.txt"):
            os.remove(f"{sys.path[0]}/codeOutput.txt")
        if os.path.exists(f"{sys.path[0]}/settings-{submittedForm.get('seed')}.asm"):
            os.remove(f"{sys.path[0]}/settings-{submittedForm.get('seed')}.asm")


def processBytePatch(rom_name, addr, val):
    """Process Byte addresses."""
    val = bytes([val])
    if addr >= 0x72C and addr < (0x72C + 8):
        diff = addr - 0x72C
        with open(rom_name, "r+b") as fh:
            fh.seek(0x132C + diff)
            fh.write(val)
        # print("Boot hook code")
    elif addr >= 0xA30 and addr < (0xA30 + 1696):
        diff = addr - 0xA30
        with open(rom_name, "r+b") as fh:
            fh.seek(0x1630 + diff)
            fh.write(val)
        # print("Expansion Pak Draw Code")
    elif addr >= 0xDE88 and addr < (0xDE88 + 3920):
        diff = addr - 0xDE88
        with open(rom_name, "r+b") as fh:
            fh.seek(0xEA88 + diff)
            fh.write(val)
        # print("Expansion Pak Picture")
    elif addr >= 0x5DAE00 and addr < (0x5DAE00 + 0x20000):
        diff = addr - 0x5DAE00
        with open(rom_name, "r+b") as fh:
            fh.seek(0x2000000 + diff)
            fh.write(val)
        # print("Heap Shrink Space")
