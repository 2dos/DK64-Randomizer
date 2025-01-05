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

from tools.cave_logic.Processor.Classes import ItemNode, EventNode

from tools.cave_logic.ast_logic import level_names

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels

def build_collectibles():
    edges = {}
    for kong in Kongs:
        if kong == Kongs.any:
            continue
        coin =  {
            "id": Collectibles.coin.name + "_" + kong.name,
            "Key": Collectibles.coin.name + "_" + kong.name,
            "Name": kong.name.title() + " " + Collectibles.coin.name.title(),
            "AltNames": [],
            "Type": "Collectible"
            }

        edges[coin['id']] = coin

    for level in level_names:
        
        level_suffix = (level_names[level].lower()) 
        lcb =  {
            "id": Collectibles.banana.name + "_" + level_suffix,
            "Key": Collectibles.banana.name + "_" + level_suffix,
            "Name": level + " " + Collectibles.banana.name.title(),
            "AltNames": [],
            "Type": "Collectible"
                    }
        edges[lcb['id']] = lcb
        

        for kong in Kongs:
                if kong == Kongs.any:
                    continue
                kong_level_suffix = (level_names[level].lower()) + "_" + kong.name
                kong_level_name = level + " " + kong.name.title()
                bana =  {
                    "id": Collectibles.banana.name + "_" + kong_level_suffix,
                    "Key": Collectibles.banana.name + "_" + kong_level_suffix,
                    "Name": kong_level_name + " " + Collectibles.banana.name.title(),
                    "AltNames": [],
                    "Type": "Collectible"
                        }
                edges[bana['id']] = bana
    return edges



# banana_galleon_diddy
with open('./tools/cave_logic/Deltas/collectible_nodes.json', 'w') as json_file:
    json.dump(build_collectibles(), json_file, indent=4)