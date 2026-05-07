"""Store vanilla warp data and write to ROM."""

import json
from typing import BinaryIO


class WarpInfo:
    """Warp Vanilla Information."""

    def __init__(self, map, ids, tied_exits, active_flags, appear_flags=[-1, -1]):
        """Initialize with given data."""
        self.map = map
        self.ids = ids
        self.tied_exits = tied_exits
        self.active_flags = active_flags
        self.appear_flags = appear_flags


warp_info_data = [
    # Isles
    WarpInfo(0x22, [0x0010, 0x0011], [13, 14], [0x01B1, 0x01B2]),  # 00 Ring -> K. Lumsy
    WarpInfo(0x22, [0x0012, 0x0013], [15, 16], [0x01B3, 0x01B4]),  # 02 Ring -> Aztec
    WarpInfo(0x22, [0x0014, 0x0016], [17, 19], [0x01B6, 0x01B5]),  # 04 K. Rool -> Ring
    WarpInfo(0x22, [0x0017, 0x0018], [20, 21], [0x01B7, 0x01B8]),  # 06 Ring -> Top of Kroc Isle
    WarpInfo(0x22, [0x0015, 0x0019], [18, 22], [0x01BA, 0x01B9]),  # 08 Ring -> BFI
    # Japes
    WarpInfo(0x07, [0x0059, 0x005A], [17, 21], [0x0020, 0x0021]),  # 0A Start -> Main
    WarpInfo(0x07, [0x0098, 0x009F], [19, 23], [0x0023, 0x0022]),  # 0C Main -> Top
    WarpInfo(0x07, [0x009E, 0x0097], [20, 22], [0x0024, 0x0025]),  # 0E Right -> Left
    WarpInfo(0x07, [0x005E, 0x006F], [24, 26], [0x0028, 0x0029]),  # 10 Tunnel -> Cranky
    WarpInfo(0x07, [0x012A, 0x012B], [18, 25], [0x0026, 0x0027], [-1, 0x17]),  # 12 Shellhive -> Mountain
    # Aztec
    WarpInfo(0x26, [0x0006, 0x0007], [19, 24], [0x004F, 0x0050]),  # 14 Start -> Oasis
    WarpInfo(0x26, [0x0080, 0x007F], [20, 21], [0x0051, 0x0052]),  # 16 Oasis -> Totem
    WarpInfo(0x26, [0x0098, 0x0095], [23, 26], [0x0054, 0x0053]),  # 18 Totem -> Cranky
    WarpInfo(0x26, [0x0073, 0x00B1], [25, 27], [0x0055, 0x0056]),  # 1A Totem -> Funky
    WarpInfo(0x26, [0x0082, 0x0087], [22, 28], [0x0057, 0x02F5], [-1, 0x3E]),  # 1C Totem -> Snoop Tunnel
    # Llama
    WarpInfo(0x14, [0x0058, 0x004E], [1, 2], [0x0059, 0x0058]),  # 1E Start -> Matching
    WarpInfo(0x14, [0x0099, 0x009A], [3, 4], [0x005A, 0x005B]),  # 20 Lava -> Start
    # Factory
    WarpInfo(0x1A, [0x007D, 0x0142], [25, 26], [0x008D, 0x008E]),  # 22 Start -> Storage
    WarpInfo(0x1A, [0x0141, 0x0144], [18, 20], [0x008F, 0x0090]),  # 24 Start -> R&D
    WarpInfo(0x1A, [0x00D9, 0x0143], [19, 21], [0x0091, 0x0092]),  # 26 Start -> Snide
    WarpInfo(0x1A, [0x010C, 0x0105], [22, 23], [0x0093, 0x0094]),  # 28 Top Prod -> Bottom Prod
    WarpInfo(0x1A, [0x00EE, 0x010B], [24, 27], [0x0095, 0x0096]),  # 2A Funky -> Arcade
    # Galleon
    WarpInfo(0x1E, [0x01F6, 0x01F7], [25, 33], [0x00B1, 0x00B2]),  # 2C Lighthouse -> Start
    WarpInfo(0x1E, [0x005F, 0x006C], [28, 30], [0x00AC, 0x00AB]),  # 2E Start -> 5DS
    WarpInfo(0x1E, [0x0066, 0x0060], [26, 29], [0x00AE, 0x00AD]),  # 30 Cranky -> Snide
    WarpInfo(0x1E, [0x0055, 0x0056], [31, 32], [0x02F6, 0x00AF], [0xA3, -1]),  # 32 Gold Tower -> 5DS
    WarpInfo(0x1E, [0x0015, 0x0016], [24, 27], [0x00A9, 0x00AA]),  # 34 5DS -> Lighthouse
    # Fungi
    WarpInfo(0x30, [0x0036, 0x0035], [28, 29], [0x00EE, 0x00ED]),  # 36 Clock -> Mill
    WarpInfo(0x30, [0x0049, 0x004A], [30, 31], [0x00EF, 0x00F0]),  # 38 Clock -> Beanstalk
    WarpInfo(0x30, [0x004B, 0x004E], [32, 37], [0x00F1, 0x00F2]),  # 3A Clock -> Mushroom
    WarpInfo(0x30, [0x004F, 0x0051], [33, 34], [0x00F3, 0x00F4]),  # 3C Clock -> Owl
    WarpInfo(0x30, [0x0055, 0x0056], [35, 36], [0x00F5, 0x00F6]),  # 3E Mush Bottom -> Mush Top
    # Caves
    WarpInfo(0x48, [0x0022, 0x0021], [32, 34], [0x011C, 0x011B]),  # 40 Start -> 5DI
    WarpInfo(0x48, [0x0037, 0x0036], [33, 35], [0x011D, 0x011E]),  # 42 Start -> 5DC
    WarpInfo(0x48, [0x0056, 0x0057], [37, 38], [0x02F7, 0x0123], [0x127, -1]),  # 44 Bonus -> 5DI
    WarpInfo(0x48, [0x006A, 0x006B], [39, 40], [0x011F, 0x0120]),  # 46 Cave -> Pillar
    WarpInfo(0x48, [0x00B5, 0x0060], [36, 41], [0x0122, 0x0121]),  # 48 Pillar -> 5DC
    # Castle
    WarpInfo(0x57, [0x0024, 0x0022], [24, 26], [0x0147, 0x0148]),  # 4A Start -> Back
    WarpInfo(0x57, [0x0028, 0x002B], [22, 28], [0x0149, 0x014A]),  # 4C Plateau -> Start
    WarpInfo(0x57, [0x002C, 0x0023], [27, 30], [0x014B, 0x014C]),  # 4E Start -> Cranky
    WarpInfo(0x57, [0x0021, 0x0029], [29, 31], [0x014D, 0x014E]),  # 50 Start -> Greenhouse
    WarpInfo(0x57, [0x002A, 0x002D], [23, 25], [0x0150, 0x014F]),  # 52 Top -> Start
    # Crypt
    WarpInfo(0x70, [0x0018, 0x001D], [2, 7], [0x0151, 0x0152]),  # 54 Start -> Diddy
    WarpInfo(0x70, [0x0019, 0x001C], [3, 6], [0x0153, 0x0154]),  # 56 Start -> DK
    WarpInfo(0x70, [0x001A, 0x001B], [4, 5], [0x0155, 0x0156]),  # 58 Start -> Chunky
]

script_folder_list = {0x7: "japes", 0x26: "aztec", 0x14: "llama_temple", 0x1A: "factory", 0x1E: "galleon", 0x30: "fungi", 0x48: "caves", 0x57: "castle", 0x70: "crypt_ddc", 0x22: "isles"}

for pad_pair in warp_info_data:
    for sub_index in range(2):
        pad_id = pad_pair.ids[sub_index]
        script_lines = [f"EXEC 7 | 125 65535 {pad_id}", "ENDBLOCK"]
        with open(f"./assets/instance_scripts/{script_folder_list[pad_pair.map]}/warp{hex(pad_id)[2:]}.json", "w") as script_f:
            json_data = {"id": pad_id, "output_version": 2, "script": [{"conditions": [], "executions": [{"function": 7, "parameters": [125, 65535, pad_id]}]}]}
            json.dump(json_data, script_f)


def generateDefaultPadPairing(fh):
    """Generate the default pad pairing and write to ROM."""
    fh.seek(0x1FF0000)
    for pair_index, pad_pair in enumerate(warp_info_data):
        for sub_index in range(2):
            exit = pad_pair.tied_exits[sub_index]
            fh.write(pad_pair.map.to_bytes(1, "big"))
            fh.write(((pair_index * 2) + (1 - sub_index)).to_bytes(1, "big"))
            fh.write(pad_pair.ids[sub_index].to_bytes(2, "big"))
            fh.write(pad_pair.active_flags[sub_index].to_bytes(2, "big"))
            flag = pad_pair.appear_flags[sub_index]
            if flag < 0:
                flag += 65536
            fh.write(flag.to_bytes(2, "big"))
            fh.write(exit.to_bytes(1, "big"))
            fh.write((0).to_bytes(1, "big"))
