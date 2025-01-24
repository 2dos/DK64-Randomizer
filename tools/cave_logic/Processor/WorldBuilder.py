
import json
from checks import build_checks
from items import build_items
from regions import build_regions
from exits import build_exits
from collectible import build_collectibles
from events import build_events
from warps import build_warps
from levels import build_levels

regions = build_regions()
checks = build_checks()

world = {
    "id": "newgen1",
    "world": {
        "worlds": {},
        "regions": {**build_levels(), **regions['nodes']},
        "edges": {**regions['edges'], **checks['edges'], **build_exits(), **build_events(), **build_warps()},
        "locations": {},
        "subChecks": {},
        "items": {**build_items(), **build_collectibles(), **checks['nodes']},
    },
    "settings": {
        "gameMode": "spoil",
        "precompiled": True,
        "skipCustomIcons": True
    }
}

with open('./tools/cave_logic/Outputs/built_donk.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
