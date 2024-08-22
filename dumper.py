"""Dump information from various custom location files into a json format in tools/dump."""

import inspect
import json
import os
import sys
import subprocess
from copy import deepcopy
from enum import IntEnum, auto

import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.JungleJapesCBLocations
import randomizer.Lists.CBLocations.DKIslesCBLocations
from randomizer.Enums.Levels import Levels
from randomizer.Lists.BananaCoinLocations import BananaCoinGroupList
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Enums.Maps import Maps

# USAGE OF FILE
# - python ./dumper.py {format} {desired-files}
# Eg: python ./dumper.py json cb door fairy
# Valid formats: "csv", "json", "md"


class Dumpers(IntEnum):
    """Enum for dumper types."""

    ColoredBananas = auto()
    Coins = auto()
    CustomLocations = auto()
    Doors = auto()
    Fairies = auto()
    Kasplats = auto()
    RandomSettings = auto()


def dump_to_dict(class_instance, deleted=[], enum_value=[], enum_name=[], logic_var=None, x_func=None, y_func=None, z_func=None) -> dict:
    """Dump class instance to dictionary and modify accordingly."""
    as_dict = deepcopy(class_instance).__dict__
    for item in deleted:
        if item in as_dict:
            del as_dict[item]
    for item in enum_value:
        if item in as_dict:
            if isinstance(as_dict[item], list):
                for ai, a in enumerate(as_dict[item]):
                    as_dict[item][ai] = int(a)
            else:
                as_dict[item] = int(as_dict[item])
            # elif not isinstance(as_dict[item], int):
            #     as_dict[item] = as_dict[item].value
    for item in enum_name:
        if item in as_dict:
            if isinstance(as_dict[item], list):
                for ai, a in enumerate(as_dict[item]):
                    as_dict[item][ai] = a.name
            else:
                as_dict[item] = as_dict[item].name
    if logic_var is not None:
        if logic_var in as_dict:
            logic_raw = " ".join([x.strip() for x in inspect.getsourcelines(as_dict[logic_var])[0]]).replace("\n", "").replace("\t", "")
            if "lambda l: True" in logic_raw:
                del as_dict[logic_var]
            else:
                logic_raw = logic_raw.strip()
                if logic_raw[-1:] == ",":
                    logic_raw = logic_raw[:-1]
                as_dict[logic_var] = logic_raw.split("lambda l: ")[-1]
    func_dict = {
        "X": x_func,
        "Y": y_func,
        "Z": z_func,
    }
    for coord in func_dict:
        if func_dict[coord] is not None:
            as_dict[coord] = func_dict[coord](as_dict)
    return as_dict


def filterCSVCell(cell_value: str):
    """Filter CSV Cell to not contain commas or invalid characters."""
    return str(cell_value).replace(",", "")


def getLevelName(level_name: Levels):
    """Get level name from level enum."""
    level_dict = {
        Levels.JungleJapes: "Jungle Japes",
        Levels.AngryAztec: "Angry Aztec",
        Levels.FranticFactory: "Frantic Factory",
        Levels.GloomyGalleon: "Gloomy Galleon",
        Levels.FungiForest: "Fungi Forest",
        Levels.CrystalCaves: "Crystal Caves",
        Levels.CreepyCastle: "Creepy Castle",
        Levels.HideoutHelm: "Hideout Helm",
        Levels.DKIsles: "DK Isles",
    }
    if level_name in level_dict:
        return level_dict[level_name]
    return level_name.name


def camelCaseSplit(string: str):
    """Split a camel case joined word into separate words split by capitals."""
    words = [[string[0]]]
    for c in string[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return " ".join(["".join(word) for word in words])


def getMapNameFromIndex(index: int):
    """Get map name from index value."""
    for e in Maps:
        if e.value == index:
            return camelCaseSplit(e.name)
    return "Unknown"


DISPLAY_TOTALS = False
LIST_DIRECTORY = "./wiki/article_markdown/custom_locations"


def dump_to_file(name="temp", data={}, format="json", dumper: Dumpers = Dumpers.ColoredBananas):
    """Dump data to a JSON file."""
    directory = "./tools/dumps"
    if format == "md":
        directory = LIST_DIRECTORY
    if not os.path.exists(directory):
        os.mkdir(directory)
    output_file = f"{directory}/{name}.{format}"
    if format == "md":
        output_file = f"{directory}/CustomLocations{name.title().replace('_','')}.{format.upper()}"
    with open(output_file, "w") as fh:
        if format == "json":
            if DISPLAY_TOTALS:
                if dumper == Dumpers.ColoredBananas:
                    total = 0
                    for x in data:
                        if x["class"] == "cb":
                            for y in x["locations"]:
                                total += y[0]
                        else:
                            total += 10
                    print(total)
                elif dumper == Dumpers.Coins:
                    print(sum([len(x["locations"]) for x in data]))
                else:
                    print(len(data))
            json.dump(data, fh, indent=4)
        elif format == "csv":
            unique = []
            for x in data:
                for attr in x:
                    if attr not in unique:
                        unique.append(attr)
            fh.write(", ".join([filterCSVCell(x) for x in unique]) + "\n")
            for x in data:
                csv_data = []
                for y in unique:
                    if y in x:
                        csv_data.append(x[y])
                    else:
                        csv_data.append("")
                fh.write(", ".join([filterCSVCell(x) for x in csv_data]) + "\n")
        elif format == "md":
            if isinstance(data, dict):
                for x in data:
                    if "Levels." in str(x) or isinstance(x, int):
                        fh.write(f"\n# {getLevelName(x)}\n")
                    else:
                        fh.write(f"\n# {x}\n")
                    headers = {
                        Dumpers.ColoredBananas: "Colored Banana Locations",
                        Dumpers.Coins: "Coin Locations",
                        Dumpers.CustomLocations: "Crown Pad/ Dirt Patch Locations",
                        Dumpers.Doors: "Door Locations",
                        Dumpers.Fairies: "Fairy Locations",
                        Dumpers.Kasplats: "Kasplat Locations",
                    }
                    dumper_header = "Click me"
                    if dumper in headers:
                        dumper_header = headers[dumper]
                    # fh.write(f"<details>\n<summary>{dumper_header}</summary>\n\n")
                    if dumper in (Dumpers.Fairies, Dumpers.Kasplats):
                        fh.write("| Map | Name | Logic |\n")
                        fh.write("| --- | ---- | ----- |\n")
                    elif dumper == Dumpers.CustomLocations:
                        fh.write("| Map | Name | Banned Types | Logic |\n")
                        fh.write("| --- | ---- | ------------ | ----- |\n")
                    elif dumper == Dumpers.Doors:
                        fh.write("| Map | Name | Door types acceptable in location | Logic |\n")
                        fh.write("| --- | ---- | --------------------------------- | ----- |\n")
                    groupings = {}
                    for y in data[x]:
                        logic = ""
                        if "logic" in y:
                            logic = f"`{y['logic']}`"
                        if dumper in (Dumpers.ColoredBananas, Dumpers.Coins):
                            if dumper == Dumpers.Coins:
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | {len(y['locations'])} | {logic} | \n")
                            elif y["class"] == "cb":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | {sum([a[0] for a in y['locations']])} | {logic} | \n")
                            elif y["class"] == "balloon":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | Balloon | {logic} | \n")
                        elif dumper == Dumpers.Fairies:
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {logic} | \n")
                        elif dumper == Dumpers.CustomLocations:
                            banned_types = y.get("banned_types", [])
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {', '.join([x.name for x in banned_types])} | {logic} | \n")
                        elif dumper == Dumpers.Kasplats:
                            if "additional_logic" in y:
                                logic = f"`{y['additional_logic']}`"
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {logic} | \n")
                        elif dumper == Dumpers.Doors:
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {', '.join([z.name.title() for z in y['door_type']])} | {logic} | \n")
                    for group in groupings:
                        if dumper in (Dumpers.ColoredBananas, Dumpers.Coins):
                            # fh.write("<details>\n")
                            # fh.write(f"<summary>{getMapNameFromIndex(group)}</summary>\n\n")
                            fh.write(f"## {getMapNameFromIndex(group)}\n")
                            fh.write("| Name | Amount | Logic |\n")
                            fh.write("| ---- | ------ | ----- |\n")
                            for item in groupings[group]:
                                fh.write(item)
                            # fh.write("</details>\n")
                    # fh.write("</details>\n")


def dump_cb(format: str):
    """Dump colored banana locations."""
    level_data = {
        Levels.JungleJapes: {
            "cb": randomizer.Lists.CBLocations.JungleJapesCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.JungleJapesCBLocations.BalloonList,
        },
        Levels.AngryAztec: {
            "cb": randomizer.Lists.CBLocations.AngryAztecCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.AngryAztecCBLocations.BalloonList,
        },
        Levels.FranticFactory: {
            "cb": randomizer.Lists.CBLocations.FranticFactoryCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.FranticFactoryCBLocations.BalloonList,
        },
        Levels.GloomyGalleon: {
            "cb": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.BalloonList,
        },
        Levels.FungiForest: {
            "cb": randomizer.Lists.CBLocations.FungiForestCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.FungiForestCBLocations.BalloonList,
        },
        Levels.CrystalCaves: {
            "cb": randomizer.Lists.CBLocations.CrystalCavesCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.CrystalCavesCBLocations.BalloonList,
        },
        Levels.CreepyCastle: {
            "cb": randomizer.Lists.CBLocations.CreepyCastleCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.CreepyCastleCBLocations.BalloonList,
        },
        Levels.DKIsles: {
            "cb": randomizer.Lists.CBLocations.DKIslesCBLocations.ColoredBananaGroupList,
            "balloons": randomizer.Lists.CBLocations.DKIslesCBLocations.BalloonList,
        },
    }
    dumps = {}
    for level in level_data:
        level_dump = []
        cb_lst = level_data[level]["cb"]
        for cb in cb_lst:
            as_dict = dump_to_dict(cb, ["group", "selected"], ["map", "kongs"], ["region"], "logic")
            as_dict["class"] = "cb"
            level_dump.append(as_dict)
        bln_lst = level_data[level]["balloons"]
        for bln in bln_lst:
            as_dict = dump_to_dict(bln, ["id", "selected"], ["map", "kongs"], ["region"], "logic")
            as_dict["class"] = "balloon"
            level_dump.append(as_dict)
        if format == "md":
            dumps[level] = level_dump
        else:
            dump_to_file(f"colored_bananas_{level.name}", level_dump, format, Dumpers.ColoredBananas)
    if format == "md":
        dump_to_file("colored_bananas", dumps, format, Dumpers.ColoredBananas)


def getCustomX(item: dict):
    """Get Custom Location X Position."""
    return item["coords"][0]


def getCustomY(item: dict):
    """Get Custom Location Y Position."""
    return item["coords"][1]


def getCustomZ(item: dict):
    """Get Custom Location Z Position."""
    return item["coords"][2]


def dump_custom_location(format: str):
    """Dump custom locations."""
    dumps = {}
    for level in CustomLocations:
        custom_location_data = []
        for custom_location in CustomLocations[level]:
            custom_location_data.append(
                dump_to_dict(custom_location, ["is_vanilla", "is_rotating_room", "default_index", "placement_subindex"], ["map"], ["region"], "logic", getCustomX, getCustomY, getCustomZ)
            )
        if format == "md":
            dumps[level] = custom_location_data
        else:
            dump_to_file(f"custom_locations_{level.name}", custom_location_data, format, Dumpers.CustomLocations)
    if format == "md":
        dump_to_file("miscellaneous", dumps, format, Dumpers.CustomLocations)


def getDoorX(item: dict):
    """Get door X Position."""
    return item["location"][0]


def getDoorY(item: dict):
    """Get door Y Position."""
    return item["location"][1]


def getDoorZ(item: dict):
    """Get door Z Position."""
    return item["location"][2]


def dump_door(format: str):
    """Dump wrinkly and T&S locations."""
    dumps = {}
    for level in door_locations:
        door_data = []
        for door in door_locations[level]:
            door_data.append(
                dump_to_dict(door, ["rx", "rz", "group", "placed", "default_kong", "default_placed", "assigned_kong"], ["map", "kongs"], ["logicregion"], "logic", getDoorX, getDoorY, getDoorZ)
            )
        if format == "md":
            dumps[level] = door_data
        else:
            dump_to_file(f"doors_{level.name}", door_data, format, Dumpers.Doors)
    if format == "md":
        dump_to_file("doors", dumps, format, Dumpers.Doors)


def dump_fairy(format: str):
    """Dump fairy locations."""
    dumps = {}
    for level in fairy_locations:
        fairy_data = []
        for fairy in fairy_locations[level]:
            as_dict = dump_to_dict(fairy, ["fence", "is_5ds_fairy", "is_vanilla", "natural_index"], ["map"], ["region"], "logic")
            if getattr(fairy, "fence") is not None:
                fence_dict = dump_to_dict(fairy.fence)
                for attr in fence_dict:
                    as_dict[f"fence_{attr}"] = fence_dict[attr]
                as_dict["X"] = as_dict["fence_center_x"]
                as_dict["Y"] = as_dict["spawn_y"]
                as_dict["Z"] = as_dict["fence_center_z"]
                del as_dict["fence_center_x"]
                del as_dict["spawn_y"]
                del as_dict["fence_center_z"]
            else:
                as_dict["X"] = as_dict["spawn_xyz"][0]
                as_dict["Y"] = as_dict["spawn_xyz"][1]
                as_dict["Z"] = as_dict["spawn_xyz"][2]
            fairy_data.append(as_dict)
        if format == "md":
            dumps[level] = fairy_data
        else:
            dump_to_file(f"fairies_{level.name}", fairy_data, format, Dumpers.Fairies)
    if format == "md":
        dump_to_file("fairies", dumps, format, Dumpers.Fairies)


def getKasplatX(item: dict):
    """Get Kasplat X-Coordinate."""
    return item["coords"][0]


def getKasplatY(item: dict):
    """Get Kasplat Y-Coordinate."""
    return item["coords"][1]


def getKasplatZ(item: dict):
    """Get Kasplat Z-Coordinate."""
    return item["coords"][2]


def dump_kasplat(format: str):
    """Dump kasplat locations."""
    dumps = {}
    for level in KasplatLocationList:
        kasplat_data = []
        for kasplat in KasplatLocationList[level]:
            kasplat_data.append(dump_to_dict(kasplat, ["selected", "vanilla"], ["map", "kong_lst"], ["region_id"], "additional_logic", getKasplatX, getKasplatY, getKasplatZ))
        if format == "md":
            dumps[level] = kasplat_data
        else:
            dump_to_file(f"kasplats_{level.name}", kasplat_data, format, Dumpers.Kasplats)
    if format == "md":
        dump_to_file("kasplats", dumps, format, Dumpers.Kasplats)


def dump_coin(format: str):
    """Dump coin locations."""
    dumps = {}
    for level in BananaCoinGroupList:
        for coin_group in BananaCoinGroupList[level]:
            as_dict = dump_to_dict(coin_group, ["group"], ["map", "kongs"], ["region"], "logic")
            if level not in dumps:
                dumps[level] = []
            dumps[level].append(as_dict)
    if format == "md":
        dump_to_file("coins", dumps, format, Dumpers.Coins)
    else:
        for level in dumps:
            dump_to_file(f"coins_{level.name}", dumps[level], format, Dumpers.Coins)


def checkIfMatchingList(list1: list, list2: list) -> bool:
    """Check if two lists match in size and items."""
    if len(list1) != len(list2):
        return False
    for item in list1:
        if item not in list2:
            return False
    return True


def getDisplayName(internal_name: str):
    """Get the displayed name on the site for an internal name."""
    directory = "./templates"
    templates = [x for x in os.listdir(directory) if ".html.jinja2" in x and x not in ["spoiler.html.jinja2", "spoiler_new.html.jinja2", "settings.html.jinja2"]]
    old_text = " ".join([x.capitalize() for x in internal_name.split("_")])
    for template in templates:
        with open(f"{directory}/{template}", "r") as jinja:
            original_text = jinja.read()
            text = original_text
            loc = text.find(internal_name)
            if loc < 0:
                continue
            # Get start of element containing name/id
            text = text[:loc]
            angle_open_loc = text.rfind("<")
            if angle_open_loc < 0:
                continue
            text = original_text[angle_open_loc:]
            angle_close_loc = text.find(">")
            if angle_close_loc < 0:
                continue
            # Found Element
            text = text[:angle_close_loc]
            disp_name_text = 'display_name="'
            start_of_disp_name = text.find(disp_name_text)
            if start_of_disp_name < 0:
                continue
            text = text[start_of_disp_name + len(disp_name_text) :]
            end_of_disp_name = text.find('"')
            if end_of_disp_name < 0:
                continue
            text = text[:end_of_disp_name].strip()
            if len(text) > 0:
                return text
    return old_text


def dump_random_settings(format: str):
    """Dump all random settings information."""
    if format != "md":
        print("Not dumping to markdown format, cannot dump random settings.")
        return
    data = None
    with open("./static/presets/weights/weights_files.json") as fh:
        data = json.loads(fh.read())
    if data is None:
        print("Random Setting Data could not be established")
        return
    for file in data:
        with open(f"{LIST_DIRECTORY}/RandomSettings{file['name'].title().replace(' ','')}.MD", "w") as fh:
            fh.write(f"{file['description']}\n")
            excluded_settings = ["name", "description"]
            included_settings = [x for x in list(file.keys()) if x not in excluded_settings]
            always_on = []
            always_off = []
            others = {}
            for setting in included_settings:
                setting_name = getDisplayName(setting)
                setting_desc = file[setting]
                if setting_desc == 0:
                    # Always false (Bool Type)
                    always_off.append(setting_name)
                    continue
                elif setting_desc == 1:
                    # Always True (Bool Type)
                    always_on.append(setting_name)
                    continue
                elif isinstance(setting_desc, float):
                    # Bool type
                    others[setting_name] = f"{int(100 * setting_desc)}%"
                    continue
                elif isinstance(setting_desc, dict):
                    sub_dict_keys = list(setting_desc.keys())
                    if len(sub_dict_keys) == 0:
                        # Empty Dictionary
                        continue
                    elif checkIfMatchingList(["min", "max", "mean"], sub_dict_keys):
                        # Bell Curve Distribution
                        others[setting_name] = f"Between {setting_desc['min']} and {setting_desc['max']}, usually close to {setting_desc['mean']}"
                        continue
                    else:
                        # Multiple Options
                        others[setting_name] = "".join([f"\n\t- {' '.join([x.capitalize() for x in k.split('_')])}: {int(setting_desc[k] * 100)}%" for k in sub_dict_keys])
                        continue
            # Sort lists for tidyness
            # always_off.sort()
            # always_on.sort()
            if len(always_on) > 0:
                fh.write("\n# Always On\n")
                fh.write("\n".join([f"- {x}" for x in always_on]))
                fh.write("\n")
            if len(always_off) > 0:
                fh.write("\n# Always Off\n")
                fh.write("\n".join([f"- {x}" for x in always_off]))
                fh.write("\n")
            if len(others) > 0:
                fh.write("\n# Other Settings\n")
                fh.write("\n".join([f"- {x}: {others[x]}" for x in list(others.keys())]))
                fh.write("\n")


all_args = ["cb", "coin", "custom_location", "door", "fairy", "kasplat", "random_settings"]
valid_args = all_args + ["all"]
args = sys.argv[2:]
if "all" in args:
    args = all_args.copy()
elif sum([1 for x in args if x not in valid_args]) > 0:
    print(f"ERROR: Invalid files \"{', '.join([x for x in args if x not in valid_args])}\". Select from {', '.join(valid_args)}")
    sys.exit()
valid_formats = ["json", "csv", "md"]
if sys.argv[1] not in valid_formats:
    print(f"ERROR: Invalid format \"{sys.argv[1]}\". Select from {', '.join(valid_formats)}")
    sys.exit()
for arg in args:
    print(f"Dumping {arg.title()}...")
    arg_f = globals()[f"dump_{arg}"]
    arg_f(sys.argv[1])
    print("Dumping complete")
subprocess.call(["python", "./update_wiki.py"])
