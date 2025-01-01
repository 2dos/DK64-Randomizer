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

from tools.cave_logic.Processor.Utils import parse_ast_by_separator, parse_ast_to_dict
from copy import deepcopy
from randomizer.Enums.Types import Types
from randomizer.Enums.Items import Items
from randomizer.Lists.Location import LocationListOriginal
from randomizer.Lists.Minigame import MinigameRequirements
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Logic import RegionsOriginal, CollectibleRegionsOriginal
from tools.cave_logic.ast_logic import ast_to_json, normalise_name, get_level_name
from tools.cave_logic.Processor.Classes import CheckEdge, RegionNode


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


# build a region to locations mapping
RegionsOriginalCopy = deepcopy(RegionsOriginal)
checkList = {}
for region_id, region in RegionsOriginalCopy.items():
    for location in region.locations:
        checkList[location.id] = {
            "region": region_id,
            "logic": location.logic
        }


def location_to_edge(id, location):

    region = checkList[id]["region"] if id in checkList else None
    source = RegionNode(region, '') if region else None
    target = Items.GoldenBanana

    logic = checkList[id]["logic"] if id in checkList else True
    if logic != True:
        logic = parse_ast_to_dict(logic,  None)

    return CheckEdge(id.name.lower(), location.name, source, target, location.type.name, "Check", logic, {"Name": location.kong.name}).to_dict()


def minigame_to_edge(id, minigame):

    req = parse_ast_by_separator(minigame.logic,  "logic=lambda l: ")
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    requires = req2["Requires"] if req2 is not None else True

    return {
        "id": id.name.lower(),
        "label": minigame.name,
        "source": "",
        "target": Items.NoItem.name.lower(),

        "cldata": {
            "Key": id.name.lower(),
            "Name": minigame.name,
            "Requires": requires,
            "Class": "Minigame",
            "Types": minigame.group,
        }
    }


def kasplat_to_edge(key, kasplat):

    req = parse_ast_by_separator(
        kasplat.additional_logic,  "additional_logic=lambda l: ", "self.additional_logic = lambda l:")
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    requires = req2["Requires"] if req2 is not None else True

    Class = "Custom Check" if kasplat.vanilla else "Check"
    source = RegionNode(kasplat.region_id, '') if region else None

    return CheckEdge(key, kasplat.name,source, Items.NoItem, "Kasplat", Class, requires, {"Name": kasplat.name})


def collectible_to_edge(collectible, region, index):
    portal_region = RegionsOriginal[region]

    name = portal_region.name + " " + collectible.kong.name.capitalize() + " " + \
        collectible.type.name.capitalize() + " " + str(index)
    reward_name = collectible.type.name + "_" + \
        get_level_name(portal_region.level.name) + "_" + collectible.kong.name

    req = parse_ast_by_separator(collectible.logic,  "lambda l: ")
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    requires = req2["Requires"] if req2 is not None else True

    normalised_reward = normalise_name(reward_name.lower())

    coll = CheckEdge(strip_name(name), name, RegionNode(portal_region, ''), normalised_reward, collectible.type.name, "Collectible", requires, {"Name": collectible.kong.name})
    coll.set_reward_amount(normalised_reward, collectible.amount)
    return coll


def build_checks():

    edges = {}


    for id, location in LocationListOriginal.items():
        edges[id.name.lower()] = location_to_edge(id, location)

    # for id, minigame in MinigameRequirements.items():
    #     edges[id.name.lower()] = minigame_to_edge(id, minigame)

    for level in KasplatLocationList:
        kasplats = KasplatLocationList[level]
        for kasplat in kasplats:
            key = strip_name(kasplat.name)
            edges[key] = kasplat_to_edge(key, kasplat).to_dict()

    for region, collectibles in CollectibleRegionsOriginal.items():
        for index, collectible in enumerate(collectibles):
            c = collectible_to_edge(collectible, region, index)
            edges[c.id] = c.to_dict()

    return edges

world = {
    "checks_edges": build_checks()
}

with open('./tools/cave_logic/Deltas/checks_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
