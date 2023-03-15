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