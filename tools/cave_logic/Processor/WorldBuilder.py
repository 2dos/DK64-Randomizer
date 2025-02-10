
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
levels = build_levels()
collectibles = build_collectibles()

world = {
    "id": "newgen1",
    "world": {
        "worlds": {},
        "regions": {**levels['nodes'], **regions['nodes']},
        "edges": {**levels['edges'],**regions['edges'], **checks['edges'], **build_exits(), **build_events(), **build_warps(), **collectibles['edges']},
        "locations": {},
        "subChecks": {},
        "items": {**build_items(), **collectibles['nodes'], **checks['nodes']},
    },
    "settings": {
        "gameMode": "spoil",
        "precompiled": True,
        "skipCustomIcons": True
    }
}

with open('./tools/cave_logic/Outputs/built_donk.json', 'w') as json_file:
    json.dump(world, json_file, indent=4)
