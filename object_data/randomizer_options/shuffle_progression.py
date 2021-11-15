"""Shuffle level order."""
from random import seed, shuffle


def shuffle_progression(post_data: dict):
    """Set the progression order for the seed.

    Args:
        post_data (dict): Form dict options.

    Returns:
        tuple: log_data
    """
    # Shuffle Level Progression
    seed(str(post_data.get("seed")) + str(post_data))
    finalLevels = post_data.get("finalLevels")
    shuffle(finalLevels)
    post_data["finalLevels"] = finalLevels
    logdata = str()
    logdata += "Level Order: " + "\n"
    finalNumerical = post_data.get("finalNumerical")
    finalBLocker = post_data.get("finalBLocker")
    finalTNS = post_data.get("finalTNS")
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
    logdata += "8. Hideout Helm "
    logdata += "(B Locker: " + str(finalBLocker[7]) + " GB)"
    return logdata
