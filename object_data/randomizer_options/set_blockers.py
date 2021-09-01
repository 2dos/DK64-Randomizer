def set_blockers(asm: str, post_data: dict):
    # Set B Lockers in ASM
    finalBLocker = post_data.get("finalBLocker")
    finalLevels = post_data.get("finalLevels")
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
    return asm, None
