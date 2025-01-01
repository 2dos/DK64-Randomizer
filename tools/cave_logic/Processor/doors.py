import sys
import os
import inspect
import ast
from ast_logic import ast_to_json



# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(parent_dir)

from randomizer.Enums.Levels import Levels
from randomizer.Enums.DoorType import DoorType
from randomizer.Lists.DoorLocations import door_locations,GetBossLobbyRegionIdForRegion
from randomizer.Enums.Items import Items
from randomizer.Logic import RegionsOriginal


import json
from copy import deepcopy

RegionList = deepcopy(RegionsOriginal)

def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'","").lower()

def door_to_edge(door):

    key = strip_name(door.name)

    portal_region = RegionList[door.logicregion]

    edgeType = "Location"
    edgeTargetType= "Item"
    target = Items.NoItem.name


    if(door.door_type == DoorType.boss):
        target_region = GetBossLobbyRegionIdForRegion(
        door.logicregion, portal_region)
        target = target_region.name
        edgeType = "Neighbourhood"
        edgeTargetType= "Location"

    l = door.logic
    req_str = inspect.getsource(door.logic).strip()
    # req = req.split("lambda l: ")[1]
    # req = req.replace("\n", "")
    req_str = req_str.rstrip(',')

    req = ast.parse(req_str)
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    requires = req2["Requires"] if req2 is not None else True

    return {
        "id": key,
        "Key": key,
        "Name": door.name,
        "source": door.logicregion.name.lower(),
        "target": target.lower(),
        "type": edgeType,
        "targetType": edgeTargetType,
        "Requires": requires,
        "Level": portal_region.level.name,
        "Class": "Door",
    }

def build_doors():
    edges = {}
    for levels in door_locations.values():
        for door in levels:
            edge = door_to_edge(door)
            edges[edge["id"]] = edge
    return edges

world = {
   "door_edges": build_doors()
}

with open('./tools/cave_logic/Deltas/door_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)