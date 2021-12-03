"""Randomize your seed via your settings."""
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

    asm = str()
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

    startup_pre = str()
    startup_after = str()
    with open("./asm/required/global.asm", "r") as file:
        asm += file.read()
        asm += "\n"
    for asm_data in asm_options:
        if post_data.get(asm_data.form_var) or asm_data.always_run_function is True:
            returned_asm, returned_logs = asm_data.generate_asm(post_data)
            asm += returned_asm
            if returned_logs is not None:
                logdata += returned_logs
            for start_data in asm_data.asm_start:
                for key in start_data:
                    if start_data[key].lower() == "before":
                        startup_pre += f"\n    JAL     {key}\n    NOP\n"
                    else:
                        startup_after += f"\n    JAL     {key}\n    NOP\n"

    with open("./asm/required/startup_pointers.asm", "r") as file:
        asm += file.read().replace("{REPLACE_BEFORE}", startup_pre).replace("{REPLACE_AFTER}", startup_after)
        asm += "\n"

    with open("./asm/required/flags.asm", "r") as file:
        asm += file.read()
        asm += "\n"

    if post_data.get("generate_spoilerlog"):
        document["nav-spoiler-tab"].style.display = ""
        document["spoiler_log_text"].text = logdata
    else:
        document["nav-spoiler-tab"].style.display = "none"
        document["spoiler_log_text"].text = ""
    print("Validating Seeds")
    if validateSeed(
        post_data.get("finalNumerical"),
        post_data.get("unlock_all_kongs", False),
        post_data.get("unlock_all_moves", False),
        post_data.get("quality_of_life", False),
        post_data.get("finalBLocker"),
        post_data.get("finalTNS"),
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
