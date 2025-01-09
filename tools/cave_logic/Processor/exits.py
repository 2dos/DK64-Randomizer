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


from randomizer.LogicFiles.Shops import LogicRegions as ShopRegions
from randomizer.LogicClasses import TransitionFront
from tools.cave_logic.Processor.regions import RegionNode, RegionEdge
from tools.cave_logic.Processor.checks import parse_ast_to_dict
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Logic import RegionsOriginal
from randomizer.Enums.Regions import Regions
from copy import deepcopy
import json

nodes = {}
edges = {}

# region to exits logic mapping
RegionsOriginalCopy = deepcopy(RegionsOriginal)
ShopRegionsCopy = deepcopy(ShopRegions)
regions_to_remove = [Regions.Snide, Regions.CrankyGeneric,
                     Regions.FunkyGeneric, Regions.CandyGeneric]
for region in regions_to_remove:
    ShopRegionsCopy.pop(region)


for region_id, region in RegionsOriginalCopy.items():
    # if one of the keys from ShopRegionsCopy is in region.exits then we need to add the logic for the reverse region as well
    for exit in region.exits:
        if ShopRegionsCopy.keys().__contains__(exit.dest):
            RegionsOriginalCopy[exit.dest].exits.append(
                TransitionFront(region_id, lambda l: True),
            )


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


def exit_to_edge(source, dest, exit_name, logic=True):

    regionEdges = {}

    # get the full region object
    source_region = RegionsOriginal[source]
    dest_region = RegionsOriginal[dest]

    # create the nodes
    source_region_node = RegionNode(
        source, source_region.name, "Region", "Region")
    dest_region_node = RegionNode(dest, dest_region.name, "Region", "Region")

    # if the sourc_region contains this shufflable_exit then lets check
    # for the logic and add that if it exists
    if logic != True:
        logic = parse_ast_to_dict(logic,  None)

    class_id = "tn-"+str(source)+"-"+str(dest)
    forward_edge = RegionEdge(
        class_id, source_region_node, dest_region_node, exit_name, logic)
    regionEdges[forward_edge.id] = forward_edge.to_dict()

    return regionEdges


def build_exits():
    edges = {}

    for region_id, region in RegionsOriginalCopy.items():
        for exit in region.exits:
            if exit.exitShuffleId in ShufflableExits:
                # use the shufflable exit to get the source and dest regions
                # as well as the logic
                shufflable_exit = ShufflableExits[exit.exitShuffleId]
                source = shufflable_exit.region
                dest = shufflable_exit.back.regionId
                exit_name = shufflable_exit.name
            else:
                source = region_id
                dest = exit.dest

                source_name = RegionsOriginal[source].name
                dest_name = RegionsOriginal[dest].name

                # need to construct the exit name
                exit_name = source_name + " to " + dest_name
            logic = exit.logic if exit.logic else True

            r = exit_to_edge(source, dest, exit_name, logic)

            edges.update(r)

            # Add the region 'exit to level' nodes
            if region.level in LevelInfoList:
                exit_to_level = LevelInfoList[region.level].TransitionsFrom
                exit_source = region_id
                exit_dest = ShufflableExits[exit_to_level].region
                exit_name = region.name + " Exit Level"
                rexit = exit_to_edge(exit_source, exit_dest, exit_name, True)

                edges.update(rexit)

    return edges


world = {
    "edges": build_exits()
}

with open('./tools/cave_logic/Deltas/exit_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
