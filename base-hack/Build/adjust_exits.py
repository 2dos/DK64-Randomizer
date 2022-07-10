"""Adjust exits to prevent logical problems with LZR."""
from typing import BinaryIO

pointer_table_address = 0x101C50
pointer_table_index = 23

exit_adjustments = [
    {
        "containing_map": 0x30,  # Fungi Main
        "exits": [
            {
                # Dark Attic
                "exit_index": 3,
                "x": 3429,
                "y": 462,
                "z": 4494,
            },
            {
                # Mill (W1 Exit)
                "exit_index": 6,
                "x": 4153,
                "y": 163,
                "z": 3721,
            },
            {
                # DK Barn
                "exit_index": 4,
                "x": 3982,
                "y": 115,
                "z": 2026,
            },
            {
                # Mill Rear PPunch Door
                "exit_index": 5,
                "x": 4550,
                "y": 162,
                "z": 3646,
            },
        ],
    },
    {
        "containing_map": 0x1E,  # Galleon
        "exits": [
            {
                # Lighthouse
                "exit_index": 10,
                "x": 1524,
                "y": 1754,
                "z": 3964,
            },
            {
                # Seal Race
                "exit_index": 19,
                "x": 3380,
                "y": 1640,
                "z": 120,
            },
        ],
    },
    {
        "containing_map": 112,  # DDC Crypt
        "exits": [
            {
                # Minecart
                "exit_index": 1,
                "x": 1515,
                "y": 80,
                "z": 2506,
            }
        ],
    },
    {
        "containing_map": 0x22,  # Isles
        "exits": [
            {
                # Aztec Lobby
                "exit_index": 3,
                "x": 3464,
                "y": 1040,
                "z": 1716,
            }
        ],
    },
    {
        "containing_map": 0x1A,  # Factory
        "exits": [
            {
                # Crusher
                "exit_index": 8,
                "x": 814,
                "y": 8,
                "z": 1334,
            }
        ],
    },
    {
        "containing_map": 0x57,  # Castle
        "exits": [
            {
                # Tree
                "exit_index": 15,
                "x": 1293,
                "y": 472,
                "z": 238,
            },
            {
                # Ballroom
                "exit_index": 11,
                "x": 1808,
                "y": 1406,
                "z": 1270,
            },
        ],
    },
]


def adjustExits(fh):
    """Write new exits."""
    print("Adjusting Exits")
    fh.seek(pointer_table_address + (4 * pointer_table_index))
    ptr_table = pointer_table_address + int.from_bytes(fh.read(4), "big")
    for x in exit_adjustments:
        _map = x["containing_map"]
        fh.seek(ptr_table + (4 * _map))
        start = int.from_bytes(fh.read(4), "big") + pointer_table_address
        for exit in x["exits"]:
            fh.seek(start + (exit["exit_index"] * 0xA) + 0)
            fh.write(exit["x"].to_bytes(2, "big"))
            fh.seek(start + (exit["exit_index"] * 0xA) + 2)
            fh.write(exit["y"].to_bytes(2, "big"))
            fh.seek(start + (exit["exit_index"] * 0xA) + 4)
            fh.write(exit["z"].to_bytes(2, "big"))


# with open("../rom/dk64-randomizer-base-dev.z64","r+b") as fh:
# 	adjustExits(fh)
