"""Copies a base shop script to all shops."""
import json

ref_script = "assets/instance_scripts/base_shop_script/shop.json"

shop_db = [
    {"map": "japes", "shops": {"snide": 0x54, "funky": 0x53}},
    {"map": "aztec", "shops": {"snide": 0x2A, "candy": 0x2B, "funky": 0x1F4}},
    {"map": "factory", "shops": {"snide": 0x64, "candy": 0xD1, "funky": 0x65}},
    {"map": "galleon", "shops": {"snide": 0x37}},
    {"map": "fungi", "shops": {"snide": 0x41, "funky": 0x40}},
    {"map": "caves", "shops": {"snide": 0x3B, "candy": 0x3C, "funky": 0x39}},
    {"map": "castle", "shops": {"snide": 0x26}},
    {"map": "dungeon_tunnel", "shops": {"candy": 0x3}},
    {"map": "isles_snide_room", "shops": {"snide": 0x1}},
    {"map": "crypt_hub", "shops": {"funky": 0x1}},
]

with open(ref_script, "r") as fh:
    base_data = json.load(fh)
    for map_obj in shop_db:
        for shop in map_obj["shops"]:
            shop_id = map_obj["shops"][shop]
            with open(f"assets/instance_scripts/{map_obj['map']}/{shop}.json", "w") as fg:
                shop_data = base_data.copy()
                shop_data["id"] = shop_id
                json.dump(shop_data, fg, indent=4)

# Test Shop Script - Doesn't fully work yet
# shop_db = [
#     {"map": "japes", "shops": {"snide": 0x54, "funky": 0x53, "cranky": 0x26}},
#     {"map": "aztec", "shops": {"snide": 0x2A, "candy": 0x2B, "funky": 0x1F4, "cranky": 0x29}},
#     {"map": "factory", "shops": {"snide": 0x64, "candy": 0xD1, "funky": 0x65, "cranky": 0x66}},
#     {"map": "galleon", "shops": {"snide": 0x37, "cranky": 0x53, "candy": 0x36, "funky": 0x1F4}},
#     {"map": "fungi", "shops": {"snide": 0x41, "funky": 0x40, "cranky": 0x3F}},
#     {"map": "caves", "shops": {"snide": 0x3B, "candy": 0x3C, "funky": 0x39, "cranky": 0x3A}},
#     {"map": "castle", "shops": {"snide": 0x26, "cranky": 0x25}},
#     {"map": "dungeon_tunnel", "shops": {"candy": 0x3}},
#     {"map": "isles_snide_room", "shops": {"snide": 0x1}},
#     {"map": "crypt_hub", "shops": {"funky": 0x1}},
#     {"map": "tgrounds", "shops": {"cranky": 0xE}},
# ]
# shop_names = ["cranky", "funky", "candy", "snide"]

# with open(ref_script, "r") as fh:
#     base_data = json.load(fh)
#     for map_obj in shop_db:
#         for shop in map_obj["shops"]:
#             shop_id = map_obj["shops"][shop]
#             with open(f"assets/instance_scripts/{map_obj['map']}/{shop}.json", "w") as fg:
#                 shop_data = base_data.copy()
#                 shop_data["id"] = shop_id
#                 shop_data["script"][0]["executions"][0]["parameters"][1] = 65527 - shop_names.index(shop)
#                 shop_data["script"][0]["executions"][0]["parameters"][2] = shop_id
#                 json.dump(shop_data, fg, indent=4)
