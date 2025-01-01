
import json
from checks import build_checks
from items import build_items
from regions import build_regions
from exits import build_exits

world = {
    "world": {
        "worlds": {},
        "regions": {**build_regions()},
        "edges": {**build_checks(), **build_exits()},
        "locations": {},
        "subChecks": {},
        "items": {**build_items()},
    },
    "settings": {
        "gameMode": "spoil",
        "precompiled": True,
        "skipCustomIcons": True
    }
}

with open('./tools/cave_logic/Outputs/built_donk.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
