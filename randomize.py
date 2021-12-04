"""Randomize your seed via your settings."""
from browser import document, window

from object_data.form_options import form_options
from validator import validateSeed


def randomize(post_data):
    """Randomize the seed.

    Args:
        query_string (dict): Form data query string.
    Returns:
        str: ASM Data.
    """
    if post_data.get("recursion", 0) > 3:
        return False

    # Arrays for Finalized Setting Values
    post_data["finalLevels"] = [
        "Jungle Japes",
        "Angry Aztec",
        "Frantic Factory",
        "Gloomy Galleon",
        "Fungi Forest",
        "Crystal Caves",
        "Creepy Castle",
    ]
    post_data["finalBLocker"] = [1, 5, 15, 30, 50, 65, 80, 100]
    post_data["finalTNS"] = [60, 120, 200, 250, 300, 350, 400]
    post_data["finalNumerical"] = [0, 1, 2, 3, 4, 5, 6]
    # Fill Arrays with chosen game length values
    if post_data.get("randomize_progression"):
        for k in post_data:
            if "troff_" in k and k[-1].isnumeric():
                post_data["finalTNS"][int(k[-1])] = int(post_data[k])
            if "blocker_" in k and k[-1].isnumeric():
                post_data["finalBLocker"][int(k[-1])] = int(post_data[k])

    window.patchData.Clear()
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
    for form_option in form_options:
        if post_data.get(form_option.form_var):
            returned_logs = form_option.run_function(post_data)
            if returned_logs is not None:
                logdata += returned_logs

    if post_data.get("generate_spoilerlog"):
        document["nav-spoiler-tab"].style.display = ""
        document["spoiler_log_text"].text = logdata
    else:
        document["nav-spoiler-tab"].style.display = "none"
        document["spoiler_log_text"].text = ""
    if validateSeed(
        post_data.get("finalNumerical"),
        post_data.get("unlock_all_kongs", False),
        post_data.get("unlock_all_moves", False),
        post_data.get("quality_of_life", False),
        post_data.get("finalBLocker"),
        post_data.get("finalTNS"),
        True,
    ):
        return True
    else:
        print("Retrying generation")
        post_data["seed"] = int(post_data.get("seed")) + 1
        post_data["recursion"] = post_data.get("recursion", 0)
        post_data["recursion"] = post_data["recursion"] + 1
        result = randomize(post_data)
        return result
