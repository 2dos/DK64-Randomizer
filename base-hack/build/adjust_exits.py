"""Adjust exits to prevent logical problems with LZR."""

import os
import zlib
from typing import BinaryIO

from BuildEnums import TableNames, Maps
from BuildLib import intf_to_float, main_pointer_table_offset

new_caves_portal_coords = [120.997, 50, 1182.974]


class ExitAdjustment:
    """Class to store an exit adjustment."""

    def __init__(self, index: int, coords: list[int]):
        """Initialize with given parameters."""
        self.index = index
        self.coords = coords.copy()


exit_adjustments = {
    Maps.Fungi: [
        ExitAdjustment(3, [3429, 462, 4494]),  # Dark Attic
        ExitAdjustment(6, [4153, 163, 3721]),  # Mill (W1 Exit)
        ExitAdjustment(4, [3982, 115, 2026]),  # DK Barn
        ExitAdjustment(5, [4550, 162, 3646]),  # Mill Rear PPunch Door
    ],
    Maps.Galleon: [
        ExitAdjustment(10, [1524, 1754, 3964]),  # Lighthouse
        ExitAdjustment(19, [3380, 1640, 120]),  # Seal Race
    ],
    Maps.CastleCryptDKDiddyChunky: [
        ExitAdjustment(1, [1515, 80, 2506]),  # Minecart
    ],
    Maps.Isles: [
        ExitAdjustment(3, [3464, 1040, 1716]),  # Aztec Lobby
        ExitAdjustment(5, [1947, 406, 3229]),  # Galleon Lobby
    ],
    Maps.Factory: [
        ExitAdjustment(8, [814, 8, 1334]),  # Crusher
    ],
    Maps.Castle: [
        ExitAdjustment(15, [1293, 472, 238]),  # Tree
        ExitAdjustment(11, [1808, 1406, 1270]),  # Ballroom
    ],
    Maps.Caves: [
        ExitAdjustment(
            11,
            [
                int(new_caves_portal_coords[0] - 25),
                int(new_caves_portal_coords[1]),
                int(new_caves_portal_coords[2] - 12),
            ],
        ),  # Unused 5DI Portal Exit
    ],
}

exit_additions = []

temp_file = "temp.bin"


def shortToUshort(short):
    """Convert Short to Unsigned Short."""
    if short < 0:
        return short + 65536
    return short


def adjustExits(fh):
    """Write new exits."""
    print("Adjusting Exits")
    # Get Setups
    fh.seek(main_pointer_table_offset + (4 * TableNames.Setups))
    setup_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    for map_index in range(216):
        exit_coords = []
        if map_index not in (0x61, 0xAA, 0x11):  # Prevent K. Lumsy exit being generated with fake warp
            fh.seek(setup_table + (4 * map_index))
            setup_start = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            setup_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            setup_size = setup_end - setup_start
            fh.seek(setup_start)
            indicator = int.from_bytes(fh.read(2), "big")
            is_compressed = False
            if indicator == 0x1F8B:
                is_compressed = True
            fh.seek(setup_start)
            data = fh.read(setup_size)
            if is_compressed:
                data = zlib.decompress(data, (15 + 32))
            with open(temp_file, "wb") as fg:
                fg.write(data)
            with open(temp_file, "rb") as fg:
                model2_count = int.from_bytes(fg.read(4), "big")
                for model2_item in range(model2_count):
                    item_start = 4 + (model2_item * 0x30)
                    fg.seek(item_start + 0x28)
                    item_type = int.from_bytes(fg.read(2), "big")
                    item_id = int.from_bytes(fg.read(2), "big")
                    if item_type >= 0x210 and item_type <= 0x214:
                        if item_id == 0x57 and map_index == 0x48:
                            fg.seek(item_start + 4)
                            coords = [int(176.505), int(intf_to_float(int.from_bytes(fg.read(4), "big"))) + 5, int(1089.408)]
                        else:
                            fg.seek(item_start)
                            coords = []
                            for coord_index in range(3):
                                coords.append(int(intf_to_float(int.from_bytes(fg.read(4), "big"))))
                            coords[1] += 5
                        exit_coords.append(coords.copy())
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if map_index == Maps.Isles:
            # Isles
            exit_coords.append([2524, 1724, 3841])  # Top of Krem Isles
        elif map_index == Maps.Galleon:
            # Galleon
            exit_coords.append([2886, 1249, 1121])  # Mech Fish Exit
        elif map_index == Maps.CavesBeetleRace:
            # Caves Beetle
            exit_coords.append([1315, 5130, 485])
        exit_additions.append(exit_coords.copy())
    # Exits
    fh.seek(main_pointer_table_offset + (4 * TableNames.Exits))
    ptr_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    for map_index in range(216):
        fh.seek(ptr_table + (4 * map_index))
        exit_start = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        exit_end = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        exit_size = exit_end - exit_start
        fh.seek(exit_start)
        data = fh.read(exit_size)
        file_name = f"exit{map_index}.bin"
        with open(file_name, "wb") as fg:
            fg.write(data)
            for exit_set in exit_additions[map_index]:
                for coord in exit_set:
                    fg.write(shortToUshort(coord).to_bytes(2, "big"))
                fg.write((0).to_bytes(4, "big"))
        with open(file_name, "r+b") as fg:
            for exit in exit_adjustments.get(map_index, []):
                exit_start = exit.index * 0xA
                fg.seek(exit_start)
                for c in exit.coords:
                    fg.write(shortToUshort(c).to_bytes(2, "big"))
        exit_count = 0
        data = None
        with open(file_name, "rb") as fg:
            data = fg.read()
            exit_count = int(len(data) / 10)
        if exit_count == 0:
            print(f"NO EXITS FOUND FOR {Maps(map_index).name}")
            data = bytes(bytearray([0] * 10))
        default_exit = 0
        if map_index == Maps.Japes:
            default_exit = 15
        elif map_index == Maps.Fungi:
            default_exit = 27
        default_start = default_exit * 10
        print(f"Rewriting exit file with {exit_count} exits:", map_index, data)
        with open(file_name, "wb") as fg:
            fg.write(data[default_start : default_start + 10])
            fg.write(exit_count.to_bytes(2, "big"))
            fg.write(data)
        if os.path.exists(file_name):
            if os.path.getsize(file_name) == 0:
                os.remove(file_name)


class LoadingZone:
    """Class to store information regarding a loading zone."""

    def __init__(self, x: int, y: int, z: int, radius: int, height: int, map_id: Maps, exit: int):
        """Initialize with given parameters."""
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.height = height
        if height is None:
            self.height = 0xFFFF
        self.map_id = map_id
        self.exit = exit

    def writeZone(self, fh: BinaryIO):
        """Write data to file."""
        for value in (self.x, self.y, self.z):
            v = value
            if value < 0:
                v += 0x10000
            fh.write(v.to_bytes(2, "big"))
        fh.write(self.radius.to_bytes(2, "big"))  # 0x6
        fh.write(self.height.to_bytes(2, "big"))  # 0x8
        fh.write((1).to_bytes(2, "big"))  # 0xA
        fh.write((1).to_bytes(2, "big"))  # 0xC
        fh.write((1).to_bytes(1, "big"))  # 0xE
        fh.write((0).to_bytes(1, "big"))  # 0XF
        LZ_TYPE = 9
        fh.write(LZ_TYPE.to_bytes(2, "big"))
        fh.write(self.map_id.to_bytes(2, "big"))
        fh.write(self.exit.to_bytes(2, "big"))
        TRANSITION_TYPE = 0
        fh.write(TRANSITION_TYPE.to_bytes(2, "big"))
        for _ in range(0x38 - 0x18):
            fh.write((0).to_bytes(1, "big"))


mech_fish_triggers = [
    LoadingZone(360, 70, 92, 50, None, Maps.Galleon, 34),
]


def addMechFishLZ():
    """Add mech fish loading zone to the trigger file."""
    with open("mech_fish_triggers.bin", "wb") as fh:
        fh.write(len(mech_fish_triggers).to_bytes(2, "big"))
        for trigger in mech_fish_triggers:
            trigger.writeZone(fh)
