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


from tools.cave_logic.ast_logic import ast_to_json
from tools.cave_logic.Processor.checks import parse_ast_to_dict
from tools.cave_logic.Processor.Classes import RegionNode, RegionEdge
from randomizer.Logic import RegionsOriginal
from randomizer.Enums.Regions import Regions
from randomizer.ShuffleExits import ShufflableExits
# from randomizer.Enums.HintRegion import HINT_REGION_PAIRING


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()

regionNameOverrides = {
    Regions.HideoutHelmEntry: "Hideout Helm Entry",
    Regions.HideoutHelmSwitchRoom: "Switch Room",
    Regions.HideoutHelmMiniRoom: "Mini Room",
    Regions.HideoutHelmDonkeyRoom: "Donkey Room",
    Regions.HideoutHelmDiddyRoom: "Diddy Room",
    Regions.HideoutHelmLankyRoom: "Lanky Room",
    Regions.HideoutHelmTinyRoom: "Tiny Room",
    Regions.HideoutHelmChunkyRoom: "Chunky Room",
}

def region_to_node(id, region):
    region_name = regionNameOverrides.get(id, region.name)
    node = RegionNode(id.name.lower(), region_name, "Region", "Region")

    level_id = region.level.name.lower()
    edge_id = "rr-" + id.name.lower() + "-level"
    level_edge = {
        "id": edge_id,
        "Name": region.name + " Level",
        "source": id.name.lower(),
        "target": level_id,
        "sourceType": "Region",
        "targetType":  "Region",
        "Class":  "Region",
        "type":  "Level"
    }
    regionEdges = {
        level_edge['id']: level_edge
    }

    # for rexit in region.exits:
    #     # get the full region object
    #     exit_region = RegionsOriginal[rexit.dest]
    #     exit_transition = ShufflableExits[rexit.exitShuffleId] if rexit.exitShuffleId else None
    #     edge_name = exit_transition.name if exit_transition else None
    #     destination_node = RegionNode(
    #         rexit.dest.name.lower(), exit_region.name, "Region", "Region")
    #     exit_logic = parse_ast_to_dict(rexit.logic,  None)

    #     forward_edge = RegionEdge(
    #         None, node, destination_node, edge_name, exit_logic)
    #     regionEdges[forward_edge.id] = forward_edge.to_dict()

    return {
        "node": node.to_dict(),
        "edges": regionEdges
    }


def build_regions():
    edges = {}
    nodes = {}
    for id, region in RegionsOriginal.items():
        r = region_to_node(id, region)
        nodes[r['node']['id']] = r['node']
        edges.update(r['edges'])
    # for id, region in HINT_REGION_PAIRING.items():
    #     node = RegionNode(id.name.lower(), region, "Region", "HintRegion")
    #     nodes[node.id] = node.to_dict()
    return {
        "nodes": nodes,
        "edges": edges
    }


world = {
    "regions": build_regions()['nodes'],
    "edges": build_regions()['edges']
}

with open('./tools/cave_logic/Deltas/region_nodes.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
