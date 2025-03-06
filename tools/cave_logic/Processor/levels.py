
import json
import sys
import os
import inspect
import ast
import re
# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../'))
sys.path.append(parent_dir)

from randomizer.Enums.Levels import Levels
from tools.cave_logic.Processor.Classes import RegionNode


def build_levels():
    # levels = {}
    # for level in Levels:

    #     levels[level.name.lower()] = {
    #         "id": level.name.lower(),
    #         "Name": level.name,
    #         "Class": "Region",
    #         "Type": "Level"
    #     }
    # return levels
    levels = {
        "junglejapes": {
            "id": "junglejapes",
            "Name": "Jungle Japes",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#228B22",
        },
        "angryaztec": {
            "id": "angryaztec",
            "Name": "Angry Aztec",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#8B4513",

        },
        "franticfactory": {
            "id": "franticfactory",
            "Name": "Frantic Factory",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#FF4500",
        },
        "gloomygalleon": {
            "id": "gloomygalleon",
            "Name": "Gloomy Galleon",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#000080",
        },
        "fungiforest": {
            "id": "fungiforest",
            "Name": "Fungi Forest",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#006400",
        },
        "crystalcaves": {
            "id": "crystalcaves",
            "Name": "Crystal Caves",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#00FFFF",
        },
        "creepycastle": {
            "id": "creepycastle",
            "Name": "Creepy Castle",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#800080",
        },
        "hideouthelm": {
            "id": "hideouthelm",
            "Name": "Hideout Helm",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#808080",
        },
        "dkisles": {
            "id": "dkisles",
            "Name": "DK Isles",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#FFD700",
        },
        "shops": {
            "id": "shops",
            "Name": "Shops",
            "Class": "Region",
            "Type": "Level",
            "Colour": "#FF00FF",
        }
    }

    level_edges = {}
    for id, region in levels.items():
        level_id = id.lower()
        edge_id = "rr-" + level_id + "-world"
        level_edge = {
            "id": edge_id,
            "Name": region['Name'] + " World",
            "source": "world",
            "target": level_id,
            "sourceType": "Region",
            "targetType":  "Region",
            "Class":  "Region",
            "Type":  "World"
        }
        level_edges[level_edge['id']] = level_edge


    levels['world'] = {
        "id": "world",
        "Name": "World",
        "Class": "Region",
        "Type": "World",
        "Colour": "#FFFFFF",
    }
    return {
        "nodes": levels,
        "edges": level_edges
        }


world = build_levels()

with open('./tools/cave_logic/Deltas/level_nodes.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
