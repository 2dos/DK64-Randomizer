from tools.cave_logic.Processor.Classes import ItemNode, EventNode
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Lists.Item import ItemList
import json

import sys
import os

# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(parent_dir)


def build_items():

    edges = {}

    for id, item in ItemList.items():
        if (id == Items.TestItem):
            continue

        i = ItemNode(id.name, item)
        edges[i.id] = i.to_dict()

    # Treat events as items albeit there's not much metadata
    for event in Events:

        # in the absence of a name lets just split the name by camel case
        # we can fix this in the overrides later
        i = EventNode(event)
        edges[i.id] = i.to_dict()
    return edges

world = {
    "item_nodes": build_items()
}

with open('./tools/cave_logic/Deltas/item_nodes.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
