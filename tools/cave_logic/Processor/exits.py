import sys
import os
import inspect
import ast
import re
# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(parent_dir)

from tools.cave_logic.Processor.regions import RegionNode, RegionEdge
from tools.cave_logic.Processor.checks import parse_ast_to_dict
from tools.cave_logic.ast_logic import ast_to_json
from randomizer.Enums.Items import Items
from randomizer.Enums.HintRegion import HINT_REGION_PAIRING
from randomizer.Lists.ShufflableExit import ShufflableExits, ShufflableExit
from randomizer.Logic import RegionsOriginal
from randomizer.Enums.Transitions import Transitions
from copy import deepcopy
import json




nodes = {}
edges = {}

# region to exits logic mapping
RegionsOriginalCopy = deepcopy(RegionsOriginal)

RegionExitLogic = {}

for region_id, region in RegionsOriginalCopy.items():
    for exit in region.exits:
        if exit.exitShuffleId in ShufflableExits:
            RegionExitLogic[exit.exitShuffleId] = exit.logic


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


def exit_to_edge(id: Transitions, shufflable_exit: ShufflableExit):

    regionEdges = {}

    # enums of Regions
    source = shufflable_exit.region
    dest = shufflable_exit.back.regionId

    # get the full region object
    source_region = RegionsOriginal[source]
    dest_region = RegionsOriginal[dest]

    # create the nodes
    source_region_node = RegionNode(
        source, source_region.name, "Region", "Region")
    dest_region_node = RegionNode(dest, dest_region.name, "Region", "Region")

    # if the sourc_region contains this shufflable_exit then lets check
    # for the logic and add that if it exists

    logic = RegionExitLogic[id] if id in RegionExitLogic else True

    if logic != True:
        logic = parse_ast_to_dict(logic,  None)


    class_id = "tn-"+str(id)
    forward_edge = RegionEdge(
        class_id, source_region_node, dest_region_node, shufflable_exit.name, logic)
    regionEdges[forward_edge.id] = forward_edge.to_dict()

    return regionEdges

def build_exits():
    edges = {}
    for id, shufflable_exit in ShufflableExits.items():
        r = exit_to_edge(id, shufflable_exit)
        edges.update(r)
    return edges

world = {
    "edges": build_exits(),
}

with open('./tools/cave_logic/Deltas/exit_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
