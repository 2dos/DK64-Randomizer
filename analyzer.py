import os
import json
from enum import auto, IntEnum
import sys
import shutil
from zipfile import ZipFile
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
seed_directory = filedialog.askdirectory(title="Select a Folder")
print("Analyzing: ", seed_directory)
sep = "/"
if "\\" in seed_directory:
    sep = "\\"
if seed_directory[-1] == sep:
    seed_directory = seed_directory[:-1]
final_folder = seed_directory.split(sep)[-1]
output = sep.join(seed_directory.split(sep)[:-1])

class DumpData(IntEnum):
    ItemWotH = auto()
    CheckWotH = auto()
    ItemLocations = auto()
    StartingKongs = auto()
    HelmBonuses = auto()
    SphereCount = auto()
    WotHCount = auto()
    LevelOrder = auto()
    LevelGBs = auto()
    MedalWotH = auto()
    CheckWotHPostLvl3 = auto()
    HintType = auto()
    UnhintedScore = auto()
    UnhintedLocations = auto()
    UnhintedWorstLocationScore = auto()

dumps = [
    DumpData.CheckWotH,
    DumpData.ItemWotH,
    DumpData.ItemLocations,
    DumpData.StartingKongs,
    DumpData.HelmBonuses,
    DumpData.SphereCount,
    DumpData.WotHCount,
    DumpData.LevelOrder,
    DumpData.LevelGBs,
    DumpData.MedalWotH,
    DumpData.CheckWotHPostLvl3,
    DumpData.HintType,
    DumpData.UnhintedScore,
    DumpData.UnhintedLocations,
    DumpData.UnhintedWorstLocationScore,
]

def get_substring_after_last_capital(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isupper():
            return s[i:]
    return ""

def get_substring_until_second_capital(s):
    count = 0
    for i in range(len(s)):
        if s[i].isupper():
            count += 1
            if count == 2:
                return s[:i]
    return ""

def check_common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    common_elements = set1.intersection(set2)
    return len(common_elements) > 0

if os.path.exists(f"{output}/analysis/{final_folder}"):
    shutil.rmtree(f"{output}/analysis/{final_folder}")
os.makedirs(f"{output}/analysis/{final_folder}", exist_ok=True)

def post(string: str, dump_file_name: str = None):
    f_n = None
    if dump_file_name is not None:
        if dump_file_name[-4:] != ".txt":
            dump_file_name = f"{dump_file_name}.txt"
        f_n = f"{output}/analysis/{final_folder}/{dump_file_name}"
    if f_n is None:
        return
    mode = "a"
    if not os.path.exists(f_n):
        mode = "w"
    with open(f_n, mode) as fk:
        fk.write(f"{string}\n")


with ZipFile(f"{output}/analysis_{final_folder}.zip", "w") as zObject:
    for dump in dumps:
        total = 0
        data = {
            "woth": {},
            "item_locations": {},
            "checkwoth": {},
            "checkwoth_filtered": {},
            "starting_kongs": {},
            "helm_minigames": {},
            "sphere_count": {},
            "woth_count": {},
            "unhinted_score": {},
            "unhinted_locations": {},
            "unhinted_worst_score": {},
            "unhinted_worst_location": {},
            "level_order": {},
            "gb_counts": {},
            "medal_woth": {},
            "hint_types": {
                "scouring": {},
                "path": {},
                "woth": {},
                "kong": {},
                "foolish": {},
            },
        }

        if dump == None:
            sys.exit()

        for fi, f in enumerate(os.listdir(seed_directory)):
            with open(f"{seed_directory}/{f}", "r") as fh:
                json_data = json.loads(fh.read())
                total += 1
                if dump == DumpData.ItemWotH:
                    hoard = json_data["Way of the Hoard"]
                    slam_count_woth = 0
                    for item in hoard.values():
                        if item != "Progressive Slam":
                            if item not in data["woth"]:
                                data["woth"][item] = 0
                            data["woth"][item] += 1
                        else:
                            slam_count_woth += 1
                    slam_2_woth = slam_count_woth > 0
                    slam_3_woth = slam_count_woth > 1
                    slam_names = ["Super Simian Slam", "Super Duper Simian Slam"]
                    for idx, slam_data in enumerate([slam_2_woth, slam_3_woth]):
                        if slam_data:
                            name = slam_names[idx]
                            if name not in data["woth"]:
                                data["woth"][name] = 0
                            data["woth"][name] += 1
                elif dump in (DumpData.CheckWotH, DumpData.MedalWotH, DumpData.CheckWotHPostLvl3):
                    hoard = json_data["Way of the Hoard"]
                    # if "The End of Helm" not in hoard:
                    #     print(f)
                    slam_count_woth = 0
                    medal_woth_count = 0
                    allowed_first_words = ["Helm", "Hideout"]
                    allowed_full_terms = ["The End of Helm", "Jetpac", "Returning the Banana Fairies"]
                    excluded_terms = ["Isles Dirt: Under Caves Lobby", "Isles Japes Lobby Entrance Item"]
                    for li, l in enumerate(list(json_data["Shuffled Level Order"].values())):
                        if li > 2:
                            allowed_first_words.append(get_substring_after_last_capital(l))
                            allowed_first_words.append(get_substring_until_second_capital(l))
                            if l == "JungleJapes":
                                allowed_full_terms.append("Diddy Kong's Cage")
                            elif l == "AngryAztec":
                                allowed_full_terms.append("Lanky Kong's Cage")
                                allowed_full_terms.append("Tiny Kong's Cage")
                            elif l == "FranticFactory":
                                allowed_full_terms.append("Chunky Kong's Cage")
                                allowed_full_terms.append("DK Arcade Round 2")
                            elif l == "GloomyGalleon":
                                allowed_full_terms.append("Treasure Chest Far Left Clam")
                                allowed_full_terms.append("Treasure Chest Center Clam")
                                allowed_full_terms.append("Treasure Chest Far Right Clam")
                                allowed_full_terms.append("Treasure Chest Close Left Clam")
                                allowed_full_terms.append("Treasure Chest Close Right Clam")

                    for check in hoard.keys():
                        # Check woth
                        if check not in data["checkwoth"]:
                            data["checkwoth"][check] = 0
                        data["checkwoth"][check] += 1
                        # Level-barred woth
                        if check not in excluded_terms:
                            if check.split(" ")[0] in allowed_first_words or check in allowed_full_terms or (check.split(" ")[0] == "Isles" and check_common_elements(check.split(" ")[1:], allowed_first_words)):
                                if check not in data["checkwoth_filtered"]:
                                    data["checkwoth_filtered"][check] = 0
                                data["checkwoth_filtered"][check] += 1 
                        # Medal Check Woth
                        if check[-6:] == " Medal" and check[:5] != "Helm ":
                            medal_woth_count += 1
                    if medal_woth_count not in data["medal_woth"]:
                        data["medal_woth"][medal_woth_count] = 0
                    data["medal_woth"][medal_woth_count] += 1
                elif dump == DumpData.ItemLocations:
                    for cat in json_data["Items (Sorted by Item)"]:
                        for loc in json_data["Items (Sorted by Item)"][cat]:
                            item = json_data["Items (Sorted by Item)"][cat][loc]
                            excluded = ["Enemy Item", "Crate Item"]
                            if item not in excluded:
                                if item == "Junk Item (Melon Slice)":
                                    item = "Junk Item"
                                kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
                                for kong in kongs:
                                    bp_str = f"{kong} Blueprint"
                                    if bp_str in item:
                                        item = bp_str

                                if loc not in data["item_locations"]:
                                    data["item_locations"][loc] = {}
                                if item not in data["item_locations"][loc]:
                                    data["item_locations"][loc][item] = 0
                                data["item_locations"][loc][item] += 1
                elif dump == DumpData.StartingKongs:
                    kongs = json_data["Items (Sorted by Item)"]["Kongs"]
                    for loc, kong in kongs.items():
                        if "Starting Kong" not in loc:
                            continue
                        if kong not in data["starting_kongs"]:
                            data["starting_kongs"][kong] = 0
                        data["starting_kongs"][kong] += 1
                elif dump == DumpData.HelmBonuses:
                    local_population = {}
                    for bonus in json_data["Shuffled Bonus Barrels"]:
                        if bonus[:5] == "Helm ":
                            minigame = json_data["Shuffled Bonus Barrels"][bonus]
                            local_population[minigame] = True
                    for minigame in local_population:
                        if minigame not in data["helm_minigames"]:
                            data["helm_minigames"][minigame] = 0
                        data["helm_minigames"][minigame] += 1
                elif dump == DumpData.SphereCount:
                    sphere_count = len(list(json_data["Playthrough"].keys()))
                    if sphere_count not in data["sphere_count"]:
                        data["sphere_count"][sphere_count] = 0
                    data["sphere_count"][sphere_count] += 1
                elif dump == DumpData.WotHCount:
                    woth_count = len(list(json_data["Way of the Hoard"].keys()))
                    if woth_count not in data["woth_count"]:
                        data["woth_count"][woth_count] = 0
                    data["woth_count"][woth_count] += 1
                elif dump == DumpData.UnhintedScore:
                    unhinted_score = int(10 * json_data["Unhinted Score"]) / 10
                    if unhinted_score not in data["unhinted_score"]:
                        data["unhinted_score"][unhinted_score] = 0
                    data["unhinted_score"][unhinted_score] += 1
                elif dump == DumpData.UnhintedLocations:
                    unhinted_locations = list(json_data["Potentially Awful Locations"].keys())
                    for loc in unhinted_locations:
                        if loc == "HOW TO INTERPRET THIS":
                            continue
                        if loc not in data["unhinted_locations"]:
                            data["unhinted_locations"][loc] = 0
                        data["unhinted_locations"][loc] += 1
                elif dump == DumpData.UnhintedWorstLocationScore:
                    worst_unhinted_score = 0
                    worst_unhinted_location = "empty"
                    unhinted_locations = list(json_data["Potentially Awful Locations"].keys())
                    for loc, score in json_data["Potentially Awful Locations"].items():
                        if loc == "HOW TO INTERPRET THIS":
                            continue
                        if score > worst_unhinted_score:
                            worst_unhinted_score = score
                            worst_unhinted_location = loc
                    worst_unhinted_score = int(worst_unhinted_score * 10) / 10
                    if worst_unhinted_score not in data["unhinted_worst_score"]:
                        data["unhinted_worst_score"][worst_unhinted_score] = 0
                    if worst_unhinted_location not in data["unhinted_worst_location"]:
                        data["unhinted_worst_location"][worst_unhinted_location] = 0
                    data["unhinted_worst_score"][worst_unhinted_score] += 1
                    data["unhinted_worst_location"][worst_unhinted_location] += 1
                elif dump == DumpData.LevelOrder:
                    for li, l in enumerate(list(json_data["Shuffled Level Order"].values())):
                        if l not in data["level_order"]:
                            data["level_order"][l] = {}
                        if li not in data["level_order"][l]:
                            data["level_order"][l][li] = 0
                        data["level_order"][l][li] += 1
                elif dump == DumpData.LevelGBs:
                    gb_counts = [int(x.split(" ")[0]) for x in list(json_data["Requirements"]["B Locker Items"].values())]
                    gb_counts.sort()
                    for li, l in enumerate(gb_counts):
                        name = f"Level {li + 1}"
                        if name not in data["gb_counts"]:
                            data["gb_counts"][name] = {}
                        if l not in data["gb_counts"][name]:
                            data["gb_counts"][name][l] = 0
                        data["gb_counts"][name][l] += 1
                elif dump == DumpData.HintType:
                    hints = list(json_data["Wrinkly Hints"].values())
                    path_hints = len([x for x in hints if "is on the path" in x])
                    woth_hints = len([x for x in hints if "Way of the Hoard" in x])
                    scouring_hints = len([x for x in hints if "Scouring" in x])
                    foolish_hints = len([x for x in hints if "foolish" in x])
                    kong_hints = 35 - (path_hints + woth_hints + scouring_hints + foolish_hints)
                    hint_data = {
                        "scouring": scouring_hints,
                        "woth": woth_hints,
                        "path": path_hints,
                        "foolish": foolish_hints,
                        "kong": kong_hints
                    }
                    for h_type in hint_data:
                        count = hint_data[h_type]
                        if count not in data["hint_types"][h_type]:
                            data["hint_types"][h_type][count] = 0
                        data["hint_types"][h_type][count] += 1

        if dump == DumpData.ItemWotH:
            post("Item Way of the Hoard Chances", dump.name)
            data["woth"] = {k: v for k, v in sorted(data["woth"].items(), key=lambda item: -item[1])}
            for item in data["woth"]:
                woth_count = data["woth"][item]
                post(f"{item}: {woth_count} ({int(10000 * woth_count / total)/100}%)", dump.name)
        elif dump in (DumpData.CheckWotH, DumpData.CheckWotHPostLvl3):
            key_v = "checkwoth"
            if dump == DumpData.CheckWotHPostLvl3:
                post("Check Way of the Hoard Chances (Only for checks after level 3)", dump.name)
                key_v = "checkwoth_filtered"
            else:
                post("Check Way of the Hoard Chances", dump.name)
            data[key_v] = {k: v for k, v in sorted(data[key_v].items(), key=lambda item: -item[1])}
            for check in data[key_v]:
                woth_count = data[key_v][check]
                post(f"{check}: {woth_count} ({int(10000 * woth_count / total)/100}%)", dump.name)
        elif dump == DumpData.ItemLocations:
            post("Item Locations", dump.name)
            for location in data["item_locations"]:
                post(location, dump.name)
                data["item_locations"][location] = {k: v for k, v in sorted(data["item_locations"][location].items(), key=lambda item: -item[1])}
                for item in data["item_locations"][location]:
                    count = data['item_locations'][location][item]
                    post(f"-{item}: {count} ({int(10000 * count / total)/100}%)", dump.name)
                post("", dump.name)
        elif dump == DumpData.StartingKongs:
            post("Starting Kongs", dump.name)
            for kong in data["starting_kongs"]:
                count = data["starting_kongs"][kong]
                post(f"{kong}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.HelmBonuses:
            post("Helm Bonus Minigame Chances", dump.name)
            data["helm_minigames"] = {k: v for k, v in sorted(data["helm_minigames"].items(), key=lambda item: -item[1])}
            for bonus in data["helm_minigames"]:
                count = data["helm_minigames"][bonus]
                post(f"{bonus}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.SphereCount:
            post("Sphere count probabilities", dump.name)
            data["sphere_count"] = {k: v for k, v in sorted(data["sphere_count"].items(), key=lambda item: item[0])}
            for s_c in data["sphere_count"]:
                count = data["sphere_count"][s_c]
                post(f"{s_c}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.WotHCount:
            post("Way of the Hoard count probabilities", dump.name)
            data["woth_count"] = {k: v for k, v in sorted(data["woth_count"].items(), key=lambda item: item[0])}
            for s_c in data["woth_count"]:
                count = data["woth_count"][s_c]
                post(f"{s_c}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.UnhintedScore:
            post("Unhinted Score probabilities", dump.name)
            data["unhinted_score"] = {k: v for k, v in sorted(data["unhinted_score"].items(), key=lambda item: item[0])}
            for s_c in data["unhinted_score"]:
                count = data["unhinted_score"][s_c]
                post(f"{s_c}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.UnhintedLocations:
            post("Unhinted Score probabilities", dump.name)
            data["unhinted_locations"] = {k: v for k, v in sorted(data["unhinted_locations"].items(), key=lambda item: -item[1])}
            for location, count in data["unhinted_locations"].items():
                post(f"-{location}: {count} ({int(10000 * count / total)/100}%)", dump.name)
        elif dump == DumpData.UnhintedWorstLocationScore:
            # Worst Score
            post("Unhinted Worst Score probabilities", dump.name)
            data["unhinted_worst_score"] = {k: v for k, v in sorted(data["unhinted_worst_score"].items(), key=lambda item: item[0])}
            for s_c in data["unhinted_worst_score"]:
                count = data["unhinted_worst_score"][s_c]
                post(f"{s_c}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
            post("", dump.name)
            post("Unhinted Worst Location probabilities", dump.name)
            # Worst Location
            data["unhinted_worst_location"] = {k: v for k, v in sorted(data["unhinted_worst_location"].items(), key=lambda item: -item[1])}
            for location, count in data["unhinted_worst_location"].items():
                post(f"-{location}: {count} ({int(10000 * count / total)/100}%)", dump.name)
        elif dump == DumpData.MedalWotH:
            post("CB-Medal Checks WotH probabilities", dump.name)
            data["medal_woth"] = {k: v for k, v in sorted(data["medal_woth"].items(), key=lambda item: item[0])}
            for s_c in data["medal_woth"]:
                count = data["medal_woth"][s_c]
                post(f"{s_c}: {count} ({int(10000 * count / total) / 100}%)", dump.name)
        elif dump == DumpData.LevelOrder:
            post("Level Order probabilities", dump.name)
            levels = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle"]
            for level in levels:
                post(level, dump.name)
                encoded_level = level.replace(" ","")
                level_data = {k: v for k, v in sorted(data["level_order"][encoded_level].items(), key=lambda item: item[0])}
                for k in level_data:
                    v = level_data[k]
                    post(f"\t{k}: {v} ({int(10000 * v / total) / 100}%)", dump.name)
                post("", dump.name)
        elif dump == DumpData.LevelGBs:
            post("Level GB Count probabilities", dump.name)
            for level in data["gb_counts"]:
                level_data = {k: v for k, v in sorted(data["gb_counts"][level].items(), key=lambda item: item[0])}
                post(f"{level}:", dump.name)
                for k in level_data:
                    v = level_data[k]
                    post(f"\t{k}: {v} ({int(10000 * v / total) / 100}%)", dump.name)
                post("", dump.name)
        elif dump == DumpData.HintType:
            post("Hint Type Count probabilities", dump.name)
            for h_type in data["hint_types"]:
                hint_data = {k: v for k, v in sorted(data["hint_types"][h_type].items(), key=lambda item: item[0])}
                post(f"{h_type}:", dump.name)
                for k in hint_data:
                    v = hint_data[k]
                    post(f"\t{k}: {v} ({int(10000 * v / total) / 100}%)", dump.name)
                post("", dump.name)

        zObject.write(f"{output}/analysis/{final_folder}/{dump.name}.txt", arcname=f"{dump.name}.txt")