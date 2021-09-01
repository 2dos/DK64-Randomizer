def set_troff(asm: str, post_data: dict):
    finalTNS = post_data.get("finalTNS")
    finalLevels = post_data.get("finalLevels")
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
    return asm, None
