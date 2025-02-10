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
from randomizer.Enums.Items import Items

def side_effect_edge(id,source, target, name, amount):
    return {
        "id": id,
        "Name": name,
        "source": source,
        "target": target,
        "type": "sideeffect",
        "sourceType": "Item",
        "targetType": "Item",
        "Types": "Multi",
        "Class": "SideEffect",
        "Requires": True,
        "Persona": None,
        "Rewards": {
            "combinator": "and",
            "rules": [
                {
                    "Name": target,
                    "Amount": amount
                }
            ]
        }
    }

def collectible_node(id, name):
    return {
        "id": id,
        "Key": id,
        "Name": name,
        "AltNames": [],
        "Type": 'Collectible'
    }

def collectible_kong_node_and_side_effect(collectible: Collectibles,level_banana_id, kong_level_suffix, kong_level_name, multiplier):
    kong_level_id = collectible.name + "_" + kong_level_suffix
    bana = collectible_node(kong_level_id, kong_level_name + " " + collectible.name.title())

    b_k_id = kong_level_id + "_se"
    se = side_effect_edge(b_k_id, kong_level_id, level_banana_id, "Banana Level " + kong_level_name, multiplier)

    return [bana, se]

def build_collectibles():
    nodes = {}
    edges = {}
    for kong in Kongs:
        if kong == Kongs.any:
            continue

        coin_id = Collectibles.coin.name + "_" + kong.name
        coin =  {
            "id": coin_id,
            "Key": coin_id,
            "Name": kong.name.title() + " " + Collectibles.coin.name.title(),
            "AltNames": [],
            "Type": "Collectible"
            }

        nodes[coin['id']] = coin

        rc = Items.RainbowCoin.name.lower()
        rc_kong = rc + "_" + kong.name
        
        edges[rc_kong] = side_effect_edge(rc_kong, rc, coin_id, "Rainbow Coin " + kong.name.title(), 5)

    for level in level_names:
        
        level_suffix = (level_names[level].lower()) 
        level_banana_id = Collectibles.banana.name + "_" + level_suffix
        lcb = collectible_node(level_banana_id, level + " " + Collectibles.banana.name.title())
        nodes[lcb['id']] = lcb
        

        for kong in Kongs:
                if kong == Kongs.any:
                    continue
                kong_level_suffix = level_suffix + "_" + kong.name
                kong_level_name = level + " " + kong.name.title()

                arr = collectible_kong_node_and_side_effect(Collectibles.banana,level_banana_id, kong_level_suffix, kong_level_name, 1)
                nodes[arr[0]['id']] = arr[0]
                edges[arr[1]['id']] = arr[1]

                arr = collectible_kong_node_and_side_effect(Collectibles.bunch,level_banana_id, kong_level_suffix, kong_level_name, 5)
                nodes[arr[0]['id']] = arr[0]
                edges[arr[1]['id']] = arr[1]

                arr = collectible_kong_node_and_side_effect(Collectibles.balloon,level_banana_id, kong_level_suffix, kong_level_name, 10)
                nodes[arr[0]['id']] = arr[0]
                edges[arr[1]['id']] = arr[1]
               
    return {'nodes':nodes, 'edges':edges}



# banana_galleon_diddy
with open('./tools/cave_logic/Deltas/collectible_nodes.json', 'w') as json_file:
    json.dump(build_collectibles(), json_file, indent=4)