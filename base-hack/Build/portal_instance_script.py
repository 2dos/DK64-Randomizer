"""Add instance scripts for portal indicators."""


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
        with open(f"assets/instance_scripts/{map.folder}/tns_{portal_index}.script", "w") as fh:
            lines = [".data", f"id = {0x220 + portal_index}", ".code", f"EXEC 7 | 125 65532 {0x220 + portal_index}", "ENDBLOCK"]
            fh.write("\n".join(lines))
