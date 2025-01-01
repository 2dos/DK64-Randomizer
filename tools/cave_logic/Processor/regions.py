from tools.cave_logic.Processor.checks import parse_ast_to_dict
from tools.cave_logic.ast_logic import ast_to_json

from randomizer.Enums.HintRegion import HINT_REGION_PAIRING
from randomizer.ShuffleExits import ShufflableExits
from randomizer.Logic import RegionsOriginal
from copy import deepcopy
import json

import sys
import os
import inspect
import ast
import re
# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(parent_dir)

from tools.cave_logic.Processor.Classes import RegionNode, RegionEdge

def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


def region_to_node(id, region):
    node = RegionNode(id.name.lower(), region.name, "Region", "Region")

    regionEdges = {}

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
    for id, region in HINT_REGION_PAIRING.items():
        node = RegionNode(id.name.lower(), region, "Region", "HintRegion")
        nodes[node.id] = node.to_dict()
    return nodes

world = {
    "regions": build_regions(),
}

with open('./tools/cave_logic/Deltas/region_nodes.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
