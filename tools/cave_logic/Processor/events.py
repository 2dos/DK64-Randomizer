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
from randomizer.Logic import RegionsOriginal
from tools.cave_logic.Processor.Classes import CheckEdge, RegionNode

from copy import deepcopy
import json




nodes = {}
edges = {}

# region to exits logic mapping
RegionsOriginalCopy = deepcopy(RegionsOriginal)


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


def build_events():
    edges = {}

    for region_id, region in RegionsOriginalCopy.items():
        for event in region.events:
            source = region_id
            # source_name = strip_name(RegionsOriginal[source].name)
            source_name = strip_name(source.name)

            logic = event.logic if event.logic else True
            if logic != True:
                logic = parse_ast_to_dict(logic,  None)


            id = strip_name(event.name.name)
            # r = exit_to_edge(source,dest,event.name,logic)
            check =  CheckEdge('li-'+id+str(region_id), event.name.name,source_name, id, "Event", "Event", logic)

            edges[check.id] = check.to_dict()
    return edges

world = {
    "edges": build_events()
    }

with open('./tools/cave_logic/Deltas/event_edges.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
