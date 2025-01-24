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
from randomizer.Enums.Regions import Regions
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Collectibles import Collectibles
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
            "logic": location.logic,
            "bonusBarrel": location.bonusBarrel
        }

medal_regions = [Regions.JungleJapesMedals, Regions.AngryAztecMedals, Regions.FranticFactoryMedals,
          Regions.GloomyGalleonMedals, Regions.FungiForestMedals, Regions.CrystalCavesMedals, Regions.CreepyCastleMedals]

def location_to_edge(id, location):


    region = checkList[id]["region"] if id in checkList else None
    source = RegionNode(region, '') if region else None
    
    if region in medal_regions:
        logic_region = RegionsOriginal[region]
        source = logic_region.level.name.lower()

    target = Items.NoItem

    logic = checkList[id]["logic"] if id in checkList else True
    if logic != True:
        logic = parse_ast_to_dict(logic,  None)

    checkId = 'li-'+id.name.lower()

    bb = checkList[id]["bonusBarrel"] if id in checkList else None
    checkMinigameNode = None
    if bb:
        checkMinigameNode = {
            "id":checkId+"-mg",
            "Name": location.name + " Minigame",
            "Class": "Item",
            "Type": "Minigame"
        }

    if bb == MinigameType.HelmBarrel:
        target = id.name.lower()
        logic = { "combinator": "AND", "rules": [ { "Name": checkId+"-mg" } ] }

    return { 
        "node": checkMinigameNode,
        "edge" : CheckEdge(checkId, location.name, source, target, location.type.name, "Check", logic,location.kong.name).to_dict()
    }


def minigame_to_edge(id, minigame):

    req = parse_ast_by_separator(minigame.logic,  "logic=lambda l: ")
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    requires = req2["Requires"] if req2 is not None else True

    id = 'm-'+id.name.lower()
    return CheckEdge(id, minigame.name, "", Items.NoItem, "Minigame", "Check", requires).to_dict()

    # return {
    #     "id": id.name.lower(),
    #     "label": minigame.name,
    #     "source": "",
    #     "target": Items.NoItem.name.lower(),

    #     "cldata": {
    #         "Key": id.name.lower(),
    #         "Name": minigame.name,
    #         "Requires": requires,
    #         "Class": "Minigame",
    #         "Types": minigame.group,
    #     }
    # }


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
    
    reward_type = collectible.type.name
    multiplier = 1

    if collectible.type == Collectibles.bunch:
        reward_type = Collectibles.banana.name
        multiplier = 5
    if collectible.type == Collectibles.balloon:
        reward_type = Collectibles.banana.name
        multiplier = 10

    reward_name = reward_type + "_" + \
        get_level_name(portal_region.level.name) + "_" + collectible.kong.name
    
    if(reward_type == Collectibles.coin.name):
        reward_name = reward_type + "_" + collectible.kong.name

    level_reward = reward_type + "_" + \
        get_level_name(portal_region.level.name) 

    req = parse_ast_by_separator(collectible.logic,  "lambda l: ")
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {})

    req_kong_rules = [
            {
                "Name": collectible.kong.name
            },
        ]

    if req2 is not None and req2['Requires'] is not True:
        req_kong_rules.append(req2['Requires'])

    requires = {
        "combinator": "AND",
        "rules": req_kong_rules
    }

    # requires = req2["Requires"] if req2 is not None else True

    normalised_reward = normalise_name(reward_name.lower())

    coll = CheckEdge(strip_name(name), name, RegionNode(portal_region, ''), normalised_reward, collectible.type.name, "Collectible", requires, {"Name": collectible.kong.name})
    # coll.set_reward_amount(normalised_reward, collectible.amount * multiplier)

    rewards = [
            {
                "Name": reward_name.lower(),
                "Amount": collectible.amount * multiplier
            }
        ]
    
    if(reward_type == Collectibles.banana.name):
        rewards.append({
            "Name": level_reward.lower(),
            "Amount": collectible.amount * multiplier
        })

    coll.set_multiple_rewards({
        "combinator": "AND",
        "rules": rewards
    })

    if coll.source and coll.source == "japest&salcove":
        coll.source = "japestnsalcove"
    if coll.source and coll.source == "r&d":
        coll.source = "randd"
    return coll


def build_checks():

    edges = {}
    nodes = {}


    for id, location in LocationListOriginal.items():
        lte = location_to_edge(id, location)
        edges[lte['edge']['id']] = lte['edge']
        if lte['node']:
            nodes[lte['node']['id']] = lte['node']

    for id, minigame in MinigameRequirements.items():
        e = minigame_to_edge(id, minigame)
        edges[e['id']] = e

    for level in KasplatLocationList:
        kasplats = KasplatLocationList[level]
        for kasplat in kasplats:
            key = strip_name(kasplat.name)
            edges[key] = kasplat_to_edge(key, kasplat).to_dict()

    for region, collectibles in CollectibleRegionsOriginal.items():
        for index, collectible in enumerate(collectibles):
            c = collectible_to_edge(collectible, region, index)
            edges[c.id] = c.to_dict()

    return {'edges': edges, 'nodes': nodes}

bc = build_checks()
world = {
    "checks_edges": bc['edges'],
    "checks_nodes": bc['nodes'],
}

with open('./tools/cave_logic/Deltas/checks_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
