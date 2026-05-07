"""Get default actor data from the vanilla ROM."""

import json
import zlib
import os
import sys
from BuildLib import ROMName
from typing import BinaryIO


def getFileOffset(addr: int) -> int:
    """Get the static file offset."""
    return addr - 0x744460


def seekFileOffset(fh: BinaryIO, address: int):
    """Seek to the correct file offset based on the RAM address."""
    fh.seek(getFileOffset(address))


PULL_VERSION = 2
ACTOR_DUMP = "actor_data.json"
FORCE_REBUILD = False
if os.path.exists(ACTOR_DUMP):
    with open(ACTOR_DUMP, "r") as fh:
        data = json.load(fh)
        if data["pull_version"] == PULL_VERSION and (not FORCE_REBUILD):
            print(f"Pull version {PULL_VERSION} is the same as file {data['pull_version']}, exiting data pull.")
            sys.exit(0)

DATA_DUMP = "Donkey Kong 64 (USA).bin"
with open(ROMName, "rb") as fh:
    fh.seek(0xC29D4)
    data = zlib.decompress(fh.read(0x949C), (15 + 32))
    with open(DATA_DUMP, "wb") as fg:
        fg.write(data)

with open(DATA_DUMP, "rb") as fh:
    actor_spawner_defs = []
    actor_master_types = []
    actor_interactions = []
    actor_health_stats = []
    actor_collision = []
    actor_functions = []
    actor_paad_ptrs = []
    flag_mapping = []
    for x in range(128):
        seekFileOffset(fh, 0x74E8B0 + (x * 0x30))
        actor_type = int.from_bytes(fh.read(2), "big")
        model = int.from_bytes(fh.read(2), "big")
        unk_vars = []
        for y in range(8):
            unk_vars.append(int.from_bytes(fh.read(1), "big"))
        code = int.from_bytes(fh.read(4), "big")
        unk10 = int.from_bytes(fh.read(4), "big")
        # We don't care about the debug name string lol
        actor_spawner_defs.append(
            {
                "actor_type": actor_type,
                "model": model,
                "unk4": unk_vars,
                "code": code,
                "unk10": unk10,
            }
        )
    for x in range(345):
        seekFileOffset(fh, 0x74D8D4 + x)
        actor_master_types.append(int.from_bytes(fh.read(1), "big"))
        seekFileOffset(fh, 0x74D624 + (2 * x))
        actor_interactions.append(int.from_bytes(fh.read(2), "big"))
        seekFileOffset(fh, 0x74D0C4 + (4 * x))
        init_health = int.from_bytes(fh.read(2), "big")
        dmg_applied = int.from_bytes(fh.read(2), "big")
        actor_health_stats.append(
            {
                "init_health": init_health,
                "damage_applied": dmg_applied,
            }
        )
        seekFileOffset(fh, 0x74C604 + (8 * x))
        collision_info = int.from_bytes(fh.read(4), "big")
        unk_4 = int.from_bytes(fh.read(1), "big")
        actor_collision.append(
            {
                "collision_info": collision_info,
                "unk_4": unk_4,
            }
        )
        seekFileOffset(fh, 0x74C0A0 + (4 * x))
        actor_functions.append(int.from_bytes(fh.read(4), "big"))
        seekFileOffset(fh, 0x74E218 + (4 * x))
        actor_paad_ptrs.append(int.from_bytes(fh.read(4), "big"))
    for x in range(113):
        seekFileOffset(fh, 0x755A20 + (8 * x))
        map_id = int.from_bytes(fh.read(1), "big")
        unk_01 = int.from_bytes(fh.read(1), "big")
        model_2_id = int.from_bytes(fh.read(2), "big")
        flag_index = int.from_bytes(fh.read(2), "big")
        kong = int.from_bytes(fh.read(1), "big")
        unk_07 = int.from_bytes(fh.read(1), "big")
        flag_mapping.append({"map": map_id, "unk_01": unk_01, "model2_id": model_2_id, "flag_index": flag_index, "intended_kong_actor": kong, "unk_07": unk_07})
    init_data = {
        "pull_version": PULL_VERSION,
        "actor_defs": actor_spawner_defs,
        "actor_master_types": actor_master_types,
        "actor_interactions": actor_interactions,
        "actor_health_damage": actor_health_stats,
        "actor_collisions": actor_collision,
        "actor_functions": actor_functions,
        "actor_extra_data_sizes": actor_paad_ptrs,
        "new_flag_mapping": flag_mapping,
    }
    with open(ACTOR_DUMP, "w") as fg:
        json.dump(init_data, fg, indent=4)
