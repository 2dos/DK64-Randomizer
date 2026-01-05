"""Add instance scripts for portal indicators."""

import json


class PortalInfo:
    """Class about information regarding T&S Portals."""

    def __init__(self, folder, portal_count):
        """Initialize with given data."""
        self.folder = folder
        self.count = portal_count


portal_data = [
    PortalInfo("japes", 3),
    PortalInfo("aztec", 5),
    PortalInfo("factory", 5),
    PortalInfo("galleon", 5),
    PortalInfo("fungi", 5),
    PortalInfo("caves", 5),
    PortalInfo("castle", 3),
    PortalInfo("dungeon_tunnel", 1),
    PortalInfo("crypt_hub", 1),
]

for map in portal_data:
    for portal_index in range(map.count):
        with open(f"assets/instance_scripts/{map.folder}/tns_{portal_index}.json", "w") as fh:
            json_new = {"id": 0x220 + portal_index, "output_version": 2, "script": [{"conditions": [], "executions": [{"function": 7, "parameters": [125, 65532, 0x220 + portal_index]}]}]}
            json.dump(json_new, fh, indent=4)
