"""Dump information from various custom location files into a json format in tools/dump."""
import inspect
import json
import os
import sys
from copy import deepcopy
from enum import IntEnum, auto

import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.JungleJapesCBLocations
from randomizer.Enums.Levels import Levels
from randomizer.Lists.BananaCoinLocations import BananaCoinGroupList
from randomizer.Lists.CrownLocations import CrownLocations
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Patches import DirtPatchLocations

# USAGE OF FILE
# - python ./dumper.py {format} {desired-files}
# Eg: python ./dumper.py json cb crown fairy
# Valid formats: "csv", "json", "md"
# Valid files: "all", "cb", "coin", "crown", "door", "fairy", "kasplat", "patch"


class Dumpers(IntEnum):
    """Enum for dumper types."""

    ColoredBananas = auto()
    Coins = auto()
    Crowns = auto()
    Doors = auto()
    Fairies = auto()
    Kasplats = auto()
    Patches = auto()


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
            fh.write(f"# {' '.join(name.split('_')).title()} \n")
            if isinstance(data, dict):
                for x in data:
                    if "Levels." in str(x):
                        fh.write(f"\n## {getLevelName(x)}\n")
                    else:
                        fh.write(f"\n## {x}\n")
                    headers = {
                        Dumpers.ColoredBananas: "Colored Banana Locations",
                        Dumpers.Coins: "Coin Locations",
                        Dumpers.Crowns: "Crown Pad Locations",
                        Dumpers.Doors: "Door Locations",
                        Dumpers.Fairies: "Fairy Locations",
                        Dumpers.Patches: "Dirt Patch Locations",
                        Dumpers.Kasplats: "Kasplat Locations",
                    }
                    dumper_header = "Click me"
                    if dumper in headers:
                        dumper_header = headers[dumper]
                    fh.write(f"<details>\n<summary>{dumper_header}</summary>\n\n")
                    if dumper in (Dumpers.Crowns, Dumpers.Fairies, Dumpers.Kasplats, Dumpers.Patches):
                        fh.write("| Map | Name | Logic |\n")
                        fh.write("| --- | ---- | ----- |\n")
                    elif dumper == Dumpers.Doors:
                        fh.write("| Map | Name | Door types acceptable in location | Logic |\n")
                        fh.write("| --- | ---- | --------------------------------- | ----- |\n")
                    groupings = {}
                    for y in data[x]:
                        if dumper in (Dumpers.ColoredBananas, Dumpers.Coins):
                            if dumper == Dumpers.Coins:
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | {len(y['locations'])} | {y.get('logic', '')} | \n")
                            elif y["class"] == "cb":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | {sum([a[0] for a in y['locations']])} | {y.get('logic', '')} | \n")
                            elif y["class"] == "balloon":
                                if y["map"] not in groupings:
                                    groupings[y["map"]] = []
                                groupings[y["map"]].append(f"| {y['name']} | Balloon | {y.get('logic', '')} | \n")
                        elif dumper in (Dumpers.Crowns, Dumpers.Fairies):
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {y.get('logic', '')} | \n")
                        elif dumper == Dumpers.Kasplats:
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {y.get('additional_logic', '')} | \n")
                        elif dumper == Dumpers.Doors:
                            fh.write(f"| {getMapNameFromIndex(y['map'])} | {y['name']} | {y['door_type'].title()} | {y.get('logic', '')} | \n")
                        elif dumper == Dumpers.Patches:
                            fh.write(f"| {getMapNameFromIndex(y['map_id'])} | {y['name']} | {y.get('logic', '')} | \n")
                    for group in groupings:
                        if dumper in (Dumpers.ColoredBananas, Dumpers.Coins):
                            fh.write("<details>\n")
                            fh.write(f"<summary>{getMapNameFromIndex(group)}</summary>\n\n")
                            fh.write("| Name | Amount | Logic |\n")
                            fh.write("| ---- | ------ | ----- |\n")
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


def getCrownX(item: dict):
    """Get Crown X Position."""
    return item["coords"][0]


def getCrownY(item: dict):
    """Get Crown Y Position."""
    return item["coords"][1]


def getCrownZ(item: dict):
    """Get Crown Z Position."""
    return item["coords"][2]


def dump_crown(format: str):
    """Dump crown pad locations."""
    dumps = {}
    for level in CrownLocations:
        crown_data = []
        for crown in CrownLocations[level]:
            crown_data.append(dump_to_dict(crown, ["is_vanilla", "is_rotating_room", "default_index", "placement_subindex"], ["map"], ["region"], "logic", getCrownX, getCrownY, getCrownZ))
        if format == "md":
            dumps[level] = crown_data
        else:
            dump_to_file(f"crowns_{level.name}", crown_data, format, Dumpers.Crowns)
    if format == "md":
        dump_to_file("crowns", dumps, format, Dumpers.Crowns)


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


def dump_patch(format: str):
    """Dump dirt patch locations."""
    dumps = {}
    for patch in DirtPatchLocations:
        level = patch.level_name
        as_dict = dump_to_dict(patch, ["vanilla", "selected", "group", "level_name"], ["map_id"], ["logicregion"], "logic")
        if level not in dumps:
            dumps[level] = []
        dumps[level].append(as_dict)
    if format == "md":
        dump_to_file("patches", dumps, format, Dumpers.Patches)
    else:
        for level in dumps:
            dump_to_file(f"patches_{level.name}", dumps[level], format, Dumpers.Patches)


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


all_args = ["cb", "coin", "crown", "door", "fairy", "kasplat", "patch"]
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
