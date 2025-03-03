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


from copy import deepcopy
from randomizer.Logic import RegionsOriginal
from tools.cave_logic.Processor.checks import parse_ast_to_dict
from tools.cave_logic.Processor.regions import RegionNode, RegionEdge

from randomizer.Lists.Warps import BananaportVanilla

nodes = {}
edges = {}

# region to exits logic mapping
RegionsOriginalCopy = deepcopy(RegionsOriginal)

def exit_to_edge(id, source, dest, exit_name, logic=True):
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

    forward_edge = RegionEdge(
        id, source_region_node, dest_region_node, exit_name, 'Warp', logic)
    return forward_edge

def getWarpFromSwapIndex(index):
    """Acquire warp name from index."""
    for id,warp in BananaportVanilla.items():
        if warp.swap_index == index:
            return [id, warp]

def build_warps():
    edges = {}

    for warp_id, warp in BananaportVanilla.items():
        source = warp.region_id

        [dest_id,dest_warp] = getWarpFromSwapIndex(warp.tied_index)

        dest = dest_warp.region_id
        exit_name = warp.name +  ' to ' + dest_warp.name

        id = "tn-"+str(source)+"-"+str(dest)+'-w-'+str(warp_id)+'-'+str(dest_id)

        r = exit_to_edge(id,source, dest, exit_name, True)

        r.Requires = {
            "combinator": "and",
            "rules": [
                {
                    "Name": warp.event.name 
                },
                {
                    "Name": dest_warp.event.name
                }
            ]
        }

        edges[r.id] = r.to_dict()
    
    return edges


world = {
    "edges": build_warps()
}

with open('./tools/cave_logic/Deltas/warp_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
