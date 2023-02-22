"""Dump information from various custom location files into a json format in tools/dump."""
import sys
import inspect
import json
import os
from typing import Callable
from copy import deepcopy
from enum import IntEnum, auto

from randomizer.Enums.Levels import Levels
from randomizer.Lists.MapsAndExits import Maps

import randomizer.Lists.CBLocations.JungleJapesCBLocations
import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
from randomizer.Lists.CrownLocations import CrownLocations
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Lists.KasplatLocations import KasplatLocationList

# USAGE OF FILE
# - python ./dumper.py {format} {desired-files}
# Eg: python ./dumper.py json cb crown fairy
# Valid formats: "csv", "json", "md"
# Valid files: "all", "cb", "crown", "door", "fairy", "kasplat"

class Dumpers(IntEnum):
    """Enum for dumper types."""
    ColoredBananas = auto()
    Crowns = auto()
    Doors = auto()
    Fairies = auto()
    Kasplats = auto()

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
            del as_dict[logic_var]
            # logic_raw = inspect.getsourcelines(as_dict[logic_var])[0][0]
            # if "lambda l: True":
            #     logic_raw = True
            # as_dict[logic_var] = logic_raw
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
    return str(cell_value).replace(",","")

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
    """Splits a camel case joined word into separate words split by capitals."""
    words = [[string[0]]]
    for c in string[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
 
    return " ".join([''.join(word) for word in words])

def getMapNameFromIndex(index: int):
    """Get map name from index value."""
    for e in Maps:
        if e.value == index:
            return camelCaseSplit(e.name)
    return "Unknown"

def dump_to_file(name="temp", data={}, format="json", dumper: Dumpers = Dumpers.ColoredBananas):
    """Dump data to a JSON file."""
    directory = "./tools/dumps"
    if format == "md":
        directory = "./wiki-lists"
    if not os.path.exists(directory):
        os.mkdir(directory)
    output_file = f"{directory}/{name}.{format}"
    if format == "md":
        output_file = f"{directory}/{name.upper()}.{format.upper()}"
    with open(output_file, "w") as fh:
        if format == "json":
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
            fh.write(f"# {' '.join(name.split('_')).title()} \n")
            if isinstance(data, dict):
                for x in data:
                    if "Levels." in str(x):
                        fh.write(f"\n## {getLevelName(x)}\n")
                    else:
                        fh.write(f"\n## {x}\n")
                    headers = {
                        Dumpers.ColoredBananas: "Colored Banana Locations",
                        Dumpers.Crowns: "Crown Pad Locations",
                    }
                    dumper_header = "Click me"
                    if dumper in headers:
                        dumper_header = headers[dumper]
                    fh.write(f"<details>\n<summary>{dumper_header}</summary>\n\n")
                    if dumper in (Dumpers.Crowns, Dumpers.Fairies, Dumpers.Kasplats):
                        fh.write("| Map | Name |\n")
                        fh.write("| --- | ---- |\n")
                    elif dumper == Dumpers.Doors:
                        fh.write("| Map | Name | Door types acceptable in location |\n")
                        fh.write("| --- | ---- | --------------------------------- |\n")
                    groupings = {}
                    for y in data[x]:
                        if dumper == Dumpers.ColoredBananas:
                            if y["class"] == "cb":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | {sum([a[0] for a in y['locations']])} | \n")
                            elif y["class"] == "balloon":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | Balloon |\n")
                        elif dumper in (Dumpers.Crowns, Dumpers.Fairies, Dumpers.Kasplats):
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | \n")
                        elif dumper == Dumpers.Doors:
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {y['door_type'].title()} | \n")
                    for group in groupings:
                        if dumper == Dumpers.ColoredBananas:
                            fh.write("<details>\n")
                            fh.write(f"<summary>{getMapNameFromIndex(group)}</summary>\n\n")
                            fh.write("| Name | Amount |\n")
                            fh.write("| ---- | ------ |\n")
                            for item in groupings[group]:
                                fh.write(item)
                            fh.write("</details>\n")
                    fh.write("</details>\n")


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


def dump_crown(format: str):
    """Dump colored banana locations."""
    dumps = {}
    for level in CrownLocations:
        crown_data = []
        for crown in CrownLocations[level]:
            x_f = lambda x: x["coords"][0]
            y_f = lambda x: x["coords"][1]
            z_f = lambda x: x["coords"][2]
            crown_data.append(dump_to_dict(crown, ["is_vanilla", "is_rotating_room", "default_index", "placement_subindex"], ["map"],["region"], "logic", x_f, y_f, z_f))
        if format == "md":
            dumps[level] = crown_data
        else:
            dump_to_file(f"crowns_{level.name}", crown_data, format, Dumpers.Crowns)
    if format == "md":
        dump_to_file("crowns", dumps, format, Dumpers.Crowns)


def dump_door(format: str):
    """Dump colored banana locations."""
    dumps = {}
    for level in door_locations:
        door_data = []
        for door in door_locations[level]:
            x_f = lambda x: x["location"][0]
            y_f = lambda x: x["location"][1]
            z_f = lambda x: x["location"][2]
            door_data.append(dump_to_dict(door, ["rx", "rz", "group", "placed", "default_kong", "default_placed", "assigned_kong"], ["map", "kongs"], ["logicregion"], "logic", x_f, y_f, z_f))
        if format == "md":
            dumps[level] = door_data
        else:
            dump_to_file(f"doors_{level.name}", door_data, format, Dumpers.Doors)
    if format == "md":
        dump_to_file("doors", dumps, format, Dumpers.Doors)
        


def dump_fairy(format: str):
    """Dump colored banana locations."""
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


def dump_kasplat(format: str):
    """Dump colored banana locations."""
    dumps = {}
    for level in KasplatLocationList:
        kasplat_data = []
        for kasplat in KasplatLocationList[level]:
            x_f = lambda x: x["coords"][0]
            y_f = lambda x: x["coords"][1]
            z_f = lambda x: x["coords"][2]
            kasplat_data.append(dump_to_dict(kasplat, ["selected", "vanilla"], ["map", "kong_lst"], ["region_id"], "additional_logic", x_f, y_f, z_f))
        if format == "md":
            dumps[level] = kasplat_data
        else:
            dump_to_file(f"kasplats_{level.name}", kasplat_data, format, Dumpers.Kasplats)
    if format == "md":
        dump_to_file("kasplats", dumps, format, Dumpers.Kasplats)

all_args = ["cb", "crown", "door", "fairy", "kasplat"]
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
    arg_f = globals()[f"dump_{arg}"]
    arg_f(sys.argv[1])
