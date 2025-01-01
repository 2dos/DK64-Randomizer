"""
This module contains functions to convert a Python code snippet to a JSON object using the Abstract Syntax Tree (AST).
The main function is ast_to_json, which recursively traverses the AST and converts it to JSON.
The module also contains helper functions such as array_to_object, which converts an array to an object with the array items as values and their names as keys.
"""
import os
import ast
import json
from pathlib import Path

from utils import deep_merge, array_to_object
from ast_logic import ast_to_json

# Define a function to recursively traverse the AST and convert it to JSON


def read_file_as_text(file_path):
    try:
        with open(file_path, 'r') as file:
            file_text = file.read()
        return file_text
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None  # Return None if there was an error


def python_ast_to_json(body, params):
    if (params['special'] in ["Items"]) or (params['file_name'] in ["Location"]):
        json_data = [ast_to_json(item, params) for item in body]
        return {"data": [x for x in json_data if x is not None]}
    if params['file_name'] in ["ShufflableExit", "ShuffleShopLocations"]:
        json_data = [ast_to_json(item, params) for item in body]
        data = [x for x in json_data if x is not None]
        return data[1]

    for item in body:
        json_data = ast_to_json(item, params)
    return json_data


def write_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Define a function to get the file paths for all .py files in a directory

def get_logic_files(directory, filter, extension=".py"):
    logic_files = []
    include = filter.get("include", [])
    exclude = filter.get("exclude", [])

    if "*" in include:
        for file in os.listdir(directory):
            if file.endswith(extension) and file not in exclude:
                logic_files.append(os.path.join(directory, file))
                logic_files.sort()
    else:
        for file in include:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                logic_files.append(file_path)
    return logic_files

# Define a function to process the logic files


def process_logic_files(file_paths, special, special2):
    ast_jsons = []
    for file_path in file_paths:
        # get the filename of the file in file_path
        # without the extension

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_contents = read_file_as_text(file_path)
        parsed_code = ast.parse(file_contents)
        params = {
            "special": special,
            "special2": special2,
            "file_name": file_name
        }
        ast_json = python_ast_to_json(parsed_code.body, params)
        ast_jsons.append(ast_json)
    return ast_jsons


def convert_files(directory, filter, special, special2):
    file_paths = get_logic_files(directory, filter)

    # Process the logic files and join the outputs into a single JSON object
    ast_jsons = process_logic_files(file_paths, special, special2)
    joined_ast_json = {}
    for ast_json in ast_jsons:
        joined_ast_json.update(ast_json)
    return joined_ast_json
    # Write the JSON object to the specified file path


def load_deltas(file_paths):
    deltas = {}
    for file_path in file_paths:
        # import json file from file_path store as json_data
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        deltas.update(json_data)
    return deltas


def create_donk_vanilla(build_data, deltas):
    edges = {**build_data['shuffle']["ShufflableExits"],
             **build_data['shuffle']["available_shops"],
             **deltas['door_edges'], }
    checkRegistry = {**build_data['checkRegistry'],
                     **build_data['collectibleRegistry'],
                     **build_data['minigames']['data'][1]['Minigames'],
                     }
    itemRegistry = deep_merge(
        deltas['item_nodes'], deltas['itemRegistry'])
    return {
        "world": deep_merge(deltas['world'], {"edges": edges, "items": itemRegistry}),
        "locationGraph": deep_merge(build_data['logic'], deltas['locationGraph']),
        # "checkRegistry": checkRegistry,
        "checkRegistry": deltas['checks_edges'],
    }


# Get the file paths for all .py files in the LogicFiles directory
build = [
    {
        "name": "logic",
        "directory": "./randomizer/LogicFiles",
        "filter": {
            "include": ["DKIsles.py", "FranticFactory.py",  "HideoutHelm.py", "CrystalCaves.py", "JungleJapes.py", "FungiForest.py",  "CreepyCastle.py", "AngryAztec.py",  "Shops.py", "GloomyGalleon.py"],
            "exclude": ["__init__.py", ]
        },
        "special": "Regions",
        "special2": None
    },
    {
        "name": "checks",
        "directory": "./randomizer/Lists",
        "filter": {
            "include": ["Location.py"],
            "exclude": []
        },
        "special": "Checks",
        "special2": "Rewards"
    },
    {
        "name": "checkRegistry",
        "directory": "./randomizer/Lists",
        "filter": {
            "include": ["Location.py"],
            "exclude": []
        },
        "special": "Checks",
        "special2": "Registry"
    },
    {
        "name": "items",
        "directory": "./randomizer",
        "filter": {
            "include": ["Settings.py", "Fill.py"],
            "exclude": []
        },
        "special": "Items",
        "special2": None
    },
    {
        "name": "collectibles",
        "directory": "./randomizer/CollectibleLogicFiles",
        "filter": {
            "include": ["FranticFactory.py",  "HideoutHelm.py", "CrystalCaves.py", "JungleJapes.py", "FungiForest.py",  "CreepyCastle.py", "AngryAztec.py",  "DKIsles.py", "Shops.py", "GloomyGalleon.py"],
            "exclude": ["__init__.py", "TestBananaTotals.py"]
        },
        "special": "Collectibles",
        "special2": "Location"
    },
    {
        "name": "collectibleRegistry",
        "directory": "./randomizer/CollectibleLogicFiles",
        "files": ["*"],
        "filter": {
            "include": ["FranticFactory.py",  "HideoutHelm.py", "CrystalCaves.py", "JungleJapes.py", "FungiForest.py",  "CreepyCastle.py", "AngryAztec.py",  "DKIsles.py", "Shops.py", "GloomyGalleon.py"],
            "exclude": ["__init__.py", "TestBananaTotals.py"]
        },
        "special": "Collectibles",
        "special2": "Registry"
    },
    {
        "name": "minigames",
        "directory": "./randomizer/Lists",
        "filter": {
            "include": ["Minigame.py"],
            "exclude": []
        },
        "special": "Items",
        "special2": None
    },
    {
        "name": "shuffle",
        "directory": "./randomizer",
        "filter": {
            "include": ["Lists/CustomLocations.py", "Lists/FairyLocations.py", "Lists/KasplatLocations.py", "Lists/ShufflableExit.py", "ShuffleShopLocations.py", "Lists/DoorLocations.py"],
            "exclude": []
        },
        "special": "Checks",
        "special2": "Registry"
    },
]

outputs = "./tools/cave_logic/Outputs"

build_data = {}
for item in build:
    combined_json = convert_files(
        item['directory'], item["filter"], item['special'], item['special2'])
    build_data.update({item['name']: combined_json})


# iterate over the keys of buid_data.collectibles
# add the values to the respective key in buid_data.logic
# under the attribute 'Collectibles'

for key in build_data['collectibles']:
    location = build_data['collectibles'][key]
    if ('Collectibles' in location):
        build_data['logic'][key]['Collectibles'] = location['Collectibles']
    else:
        build_data['logic'][key]['Collectibles'] = []


checkRegistryKeyName = {}
build_data['checkRegistry'] = build_data['checkRegistry']['data'][1]['LocationListOriginal']
for key in build_data['checkRegistry']:
    check = build_data['checkRegistry'][key]
    if 'Name' in check:
        checkRegistryKeyName[check['Name']] = key

# same for kasplats
for kasplat in build_data['shuffle']['Kasplats']:
    location = kasplat['Region']
    key = kasplat['Key']
    name = kasplat['Name']

    if key not in build_data['checkRegistry']:
        key = checkRegistryKeyName[name] if name in checkRegistryKeyName else key

    new_kasplat = {
        "Key": key,
        "Name": name,
        "Level": build_data['logic'][location]['Level'],
        "Class": kasplat['Class'],
        "Types": kasplat['Class'],
        "Requires": kasplat['Requires'],
    }
    build_data['logic'][location]['Checks'][key] = new_kasplat


# same for fairies
for fairy in build_data['shuffle']['fairy_locations']:
    location = fairy['Region']
    key = fairy['Key']
    name = fairy['Name']

    if key not in build_data['checkRegistry']:
        key = checkRegistryKeyName[name] if name in checkRegistryKeyName else key

    new_fairy = {
        "Key": key,
        "Name": name,
        "Level": build_data['logic'][location]['Level'],
        "Class": fairy['Class'],
        "Types": fairy['Types'],
        "Requires": fairy['Requires'],
    }
    build_data['logic'][location]['Checks'][key] = new_fairy


# same for custom_location
for custom_location in build_data['shuffle']['CustomLocations']:
    location = custom_location['Region']
    key = custom_location['Key']
    name = custom_location['Name']

    if key not in build_data['checkRegistry']:
        key = checkRegistryKeyName[name] if name in checkRegistryKeyName else key

    new_custom_location = {
        "Key": key,
        "Name": name,
        # "Level": custom_location['Level'],
        "Level": build_data['logic'][location]['Level'],
        "Class": custom_location['Class'],
        "Types": custom_location['Class'],
        "Requires": custom_location['Requires'],
    }
    build_data['logic'][location]['Checks'][key] = new_custom_location

# lets build some of the world object for world,levels,regions, and locations
worlds = []
levels = []
regions = []
locations = []

for key in build_data['logic']:
    location = build_data['logic'][key]
    level = {"Key": location['Level']}
    region = {"Key": location['HintName']}

    if level not in levels:
        levels.append(level)
    if region not in regions:
        regions.append(region)
    if location not in locations:
        locations.append(location)

build_data['world'] = {
    "worlds": [],
    "levels": levels,
    "regions": array_to_object(regions),
    "locations": locations
}


# load deltas
file_paths = get_logic_files(
    "./tools/cave_logic/Deltas", {"include": ["*"], "exclude": []}, ".json")
deltas = load_deltas(file_paths)
donk_vanilla = create_donk_vanilla(build_data, deltas)

# Write the JSON object to the specified file path
write_json(build_data, Path(outputs, 'bigly.json'))
write_json(donk_vanilla, Path(outputs, "donk-vanilla.json"))
