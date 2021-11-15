"""Used for setting the troffnscoff values."""


def set_troff(post_data: dict):
    """Set troff ASM value.

    Args:
        post_data (dict): Form dict options.

    Returns:
        tuple: log_data
    """
    finalTNS = post_data.get("finalTNS")
    finalLevels = post_data.get("finalLevels")
    # Set Troff n Scoffs in ASM
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Jungle Japes")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Angry Aztec")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Frantic Factory")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Gloomy Galleon")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Fungi Forest")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Crystal Caves")]) + "\n"
    # asm += "\t" + ".half " + str(finalTNS[finalLevels.index("Creepy Castle")]) + "\n"
    return None
