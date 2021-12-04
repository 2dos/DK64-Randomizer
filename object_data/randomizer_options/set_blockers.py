"""Set B-Locker data."""


def set_blockers(post_data: dict):
    """Set B-Locker ASM code.

    Args:
        post_data (dict): Form dict options.

    Returns:
        tuple: asm, log_data
    """
    # Set B Lockers in ASM
    finalBLocker = post_data.get("finalBLocker")
    finalLevels = post_data.get("finalLevels")
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[7])  # Helm B Locker always uses last value in level array
    # # ANTI CHEAT (set GB amounts to the B Locker post in-game cheat code)
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n"
    # asm += "\t" + ".half " + str(finalBLocker[7])  # Helm B Locker always uses last value in level array
    return None
