"""Build cutscene files from a series of modifications and return changes to the file dict in CL."""

import json
import os
import zlib
from typing import BinaryIO

from BuildClasses import File
from BuildEnums import TableNames
from BuildLib import ROMName, main_pointer_table_offset

instance_dir = "./assets/cutscene_scripts"
script_table = 0x0
temp_file = "temp.bin"


def arrToInt(arr: list) -> int:
    """Convert list to int."""
    val = 0
    for a in arr:
        val <<= 8
        val += a
    return val


class Item:
    """Class to store information regarding a cutscene item."""

    def __init__(self, unk0: int, command: int, segment: int):
        """Initialize with given parameters."""
        self.unk0 = unk0
        self.command = command
        self.segment = segment
        self.head = []
        self.read = []
        self.points = []
        self.point_start = None
        self.point_end = None
        self.song = None
        self.subcommand = None
        self.params = []

    def pushHead(self, f: BinaryIO, size: int, start: int) -> int:
        """Push header information."""
        f.seek(start + 2)
        self.head = [int.from_bytes(f.read(1), "big") for x in range(2)]
        f.seek(start + 4)
        self.read = [int.from_bytes(f.read(1), "big") for x in range(size)]
        return start + 4 + size

    def pushPoint(self, f: BinaryIO, start: int) -> int:
        """Push camera pan point."""
        if self.command in (4, 5):
            f.seek(start + 4)
            point_count = int.from_bytes(f.read(2), "big")
            if self.command == 4:
                self.pushHead(f, 0x1C, start)
            else:
                self.pushHead(f, 0x10, start)
            start_copy = start + 4
            for point_index in range(point_count + 2):
                f.seek(start_copy)
                coords = [
                    int.from_bytes(f.read(2), "big"),
                    int.from_bytes(f.read(2), "big"),
                    int.from_bytes(f.read(2), "big"),
                ]
                for ci, c in enumerate(coords):
                    if c > 32767:
                        coords[ci] = c - 65536
                if self.command == 4:
                    rot = [
                        int.from_bytes(f.read(2), "big"),
                        int.from_bytes(f.read(2), "big"),
                        int.from_bytes(f.read(2), "big"),
                    ]
                else:
                    rot = [0, 0, 0]
                zoom = int.from_bytes(f.read(1), "big")
                roll = int.from_bytes(f.read(1), "big")
                pan_point = PanPoint(coords.copy(), rot.copy(), zoom, roll)
                if point_index == 0:
                    self.point_start = pan_point
                elif point_index == 1:
                    self.point_end = pan_point
                else:
                    self.points.append(pan_point)
                if self.command == 4:
                    start_copy += 6
                start_copy += 8
            return start_copy
        return start

    def pushSong(self, f: BinaryIO, start: int):
        """Push song data."""
        self.pushHead(f, 2, start)
        f.seek(start + 4)
        self.song = int.from_bytes(f.read(2), "big")
        return start + 6

    def parsePoint(self):
        """Parse point to populate it with additional data."""
        if self.command == 13:
            self.subcommand = arrToInt(self.read[:4])
            param_count = int((len(self.read) - 4) / 2)
            for a in range(param_count):
                p_start = 4 + (a << 1)
                self.params.append(arrToInt(self.read[p_start : p_start + 2]))


class Cutscene:
    """Class to store information regarding a cutscene index."""

    def __init__(self, index: int, point_sequence: list, point_duration: list):
        """Initialize with given parameters."""
        self.index = index
        self.count = len(point_sequence)
        self.point_sequence = point_sequence.copy()
        self.point_duration = point_duration.copy()
        self.point_items = []

    def pushItem(self, item: Item):
        """Push item to cutscene."""
        self.point_items.append(item)


class PanPoint:
    """Class to store information regarding a camera pan point."""

    def __init__(self, position: list, rotation: list, zoom: int, roll: int):
        """Initialize with given parameters."""
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.rot_x = rotation[0]
        self.rot_y = rotation[1]
        self.rot_z = rotation[2]
        self.zoom = zoom
        self.roll = roll


def getPointDataFromModication(point: dict) -> PanPoint:
    """Convert point data from modification dictionary to a PanPoint class."""
    coords = [int(point["x"]), int(point["y"]), int(point["z"])]
    rot = [0, 0, 0]
    if "rot" in point and isinstance(point["rot"], dict):
        rot = [int(point["rot"]["x"]), int(point["rot"]["y"]), int(point["rot"]["z"])]
    return PanPoint(coords.copy(), rot.copy(), int(point["zoom"]), int(point["roll"]))


def buildFile(data: bytes, modifications: list, map_index: int, map_name: str) -> dict:
    """Build cutscene file based on the original file and JSON modifications provided."""
    map_file_name = f"cutscenes_{map_index}.bin"
    with open(map_file_name, "wb") as fg:
        fg.write(data)
    modifications = sorted(modifications, key=lambda d: d["index"])  # Sort modifications by index
    header_end = 0x30
    header_bytes = []
    cutscenes = []
    items = []
    used_segment_indexes = []
    # Convert cutscene file into classes
    with open(map_file_name, "rb") as fg:
        # Get Header
        for x in range(0x18):
            count = int.from_bytes(fg.read(2), "big")
            header_end += count * 0x12
        fg.seek(header_end)
        count = int.from_bytes(fg.read(2), "big")
        header_end += (count * 0x1C) + 2
        # Cutscenes
        fg.seek(header_end)
        cutscene_count = int.from_bytes(fg.read(2), "big")
        fg.seek(0)
        header_bytes = [int.from_bytes(fg.read(1), "big") for _ in range(header_end)]
        read_location = header_end + 2
        for cutscene_index in range(cutscene_count):
            fg.seek(read_location)
            point_count = int.from_bytes(fg.read(2), "big")
            read_location += 2
            point_sequence = []
            point_duration = []
            for _ in range(point_count):
                point_sequence.append(int.from_bytes(fg.read(2), "big"))
                point_duration.append(int.from_bytes(fg.read(2), "big"))
                read_location += 4
            cutscenes.append(Cutscene(cutscene_index, point_sequence.copy(), point_duration.copy()))
        # Items
        fg.seek(read_location)
        item_count = int.from_bytes(fg.read(2), "big")
        read_location += 2
        count_copy = item_count
        segment_index = 0
        while count_copy != 0:
            fg.seek(read_location)
            unk0 = int.from_bytes(fg.read(1), "big")
            command = int.from_bytes(fg.read(1), "big")
            item_data = Item(unk0, command, segment_index)
            used_segment_indexes.append(segment_index)
            segment_index += 1
            count_copy -= 1
            if command == 1:
                read_location = item_data.pushHead(fg, 6, read_location)
            elif command == 2:
                read_location = item_data.pushHead(fg, 8, read_location)
            elif command in (3, 13):
                read_location = item_data.pushHead(fg, 12, read_location)
            elif command in (4, 5):
                read_location = item_data.pushPoint(fg, read_location)
            elif command in (10, 15, 16):
                read_location = item_data.pushHead(fg, 14, read_location)
            elif command == 12:
                read_location = item_data.pushSong(fg, read_location)
            else:
                read_location = item_data.pushHead(fg, 0, read_location)
                count_copy += 1  # Not important cutscene
            item_data.parsePoint()
            items.append(item_data)
        for cs in cutscenes:
            for point in cs.point_sequence:
                found_item = None
                item_matches = [x for x in items if x.segment == point]
                if len(item_matches):
                    found_item = item_matches[0]
                cs.pushItem(found_item)
    # Convert modifications into classes, feed into arrays
    for mod in modifications:
        segments = []
        for point in mod["point_data"]:
            max_seg = max(used_segment_indexes)
            segment_index = min([x for x in range(max_seg + 2) if x not in used_segment_indexes])
            segments.append(segment_index)
            used_segment_indexes.append(segment_index)
            item_data = Item(point["unk0"], point["command"], segment_index)
            item_data.head = point["head"].copy()
            if "read" in point:
                item_data.read = point["read"].copy()
            if "detailed_command" in point:
                item_data.subcommand = point["detailed_command"]["sub_command"]
                item_data.params = point["detailed_command"]["params"].copy()
            for attr in ("point_start", "point_end", "points"):
                if attr in point:
                    if attr == "points":
                        item_data.points = [getPointDataFromModication(x) for x in point["points"]]
                    elif attr == "point_start":
                        item_data.point_start = getPointDataFromModication(point["point_start"])
                    elif attr == "point_end":
                        item_data.point_end = getPointDataFromModication(point["point_end"])
            if "song" in point:
                item_data.song = point["song"]
            items.append(item_data)
        if mod["index"] + 1 > len(cutscenes):
            for filler in range(len(cutscenes), mod["index"] + 1):
                cutscenes.append(Cutscene(filler, [], []))
        print(segments)
        cutscene_data = Cutscene(mod["index"], segments.copy(), [x["duration"] for x in mod["point_data"]])
        cutscenes[mod["index"]] = cutscene_data
    # Recompile
    entry_size = None
    with open(map_file_name, "wb") as fg:
        # Header Bytes
        for val in header_bytes:
            fg.write(val.to_bytes(1, "big"))
        fg.write(len(cutscenes).to_bytes(2, "big"))
        for cutscene in cutscenes:
            fg.write(len(cutscene.point_sequence).to_bytes(2, "big"))
            for x in range(len(cutscene.point_sequence)):
                fg.write(cutscene.point_sequence[x].to_bytes(2, "big"))
                fg.write(cutscene.point_duration[x].to_bytes(2, "big"))
        filter_arr = [1, 2, 3, 4, 5, 10, 15, 16, 12, 13]
        filtered_item_count = len([x for x in items if x.command in filter_arr])
        fg.write(filtered_item_count.to_bytes(2, "big"))
        for item in items:
            fg.write(item.unk0.to_bytes(1, "big"))
            fg.write(item.command.to_bytes(1, "big"))
            fg.write(bytearray(item.head))
            if item.command in (1, 2, 3, 10, 15, 16):
                fg.write(bytearray(item.read))
            elif item.command == 13:
                fg.write(item.subcommand.to_bytes(4, "big"))
                for param in item.params:
                    fg.write(param.to_bytes(2, "big"))
                zero_size = 8 - (2 * len(item.params))
                fg.write((0).to_bytes(zero_size, "big"))
            elif item.command in (4, 5):
                point_series = [item.point_start, item.point_end] + item.points
                for point in point_series:
                    coords = [
                        point.x,
                        point.y,
                        point.z,
                    ]
                    for coord in coords:
                        if coord < 0:
                            fg.write((coord + 65536).to_bytes(2, "big"))
                        else:
                            fg.write(coord.to_bytes(2, "big"))
                    if item.command == 4:
                        rots = [
                            point.rot_x,
                            point.rot_y,
                            point.rot_z,
                        ]
                        for rot in rots:
                            if rot < 0:
                                fg.write((rot + 65536).to_bytes(2, "big"))
                            else:
                                fg.write(rot.to_bytes(2, "big"))
                    fg.write(point.zoom.to_bytes(1, "big"))
                    fg.write(point.roll.to_bytes(1, "big"))
            elif item.command == 12:
                fg.write(item.song.to_bytes(2, "big"))
            else:
                fg.write(bytearray(item.read))
        entry_size = fg.tell()
    return File(
        name=f"Cutscenes ({map_name})",
        pointer_table_index=TableNames.Cutscenes,
        file_index=map_index,
        source_file=map_file_name,
        do_not_delete_source=True,
        do_not_recompress=True,
        target_size=entry_size,
    )


def buildScripts() -> list:
    """Run through cutscenes folder and compile cutscenes to send back to file_dict."""
    print("\nCOMPILING CUTSCENES")
    appended_items = []
    with open(ROMName, "rb") as fh:
        fh.seek(main_pointer_table_offset + (8 * 4))
        script_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        map_data = []

        if script_table != 0:
            folders = [x[0] for x in os.walk(instance_dir)]
            for f in folders:
                if f != "./" and "pycache" not in f and "k_rool_cs" not in f:
                    files = [x[2] for x in os.walk(f)][0]
                    map_index = -1
                    if ".map" in files:
                        with open(f"{f}/.map", "r") as map_info:
                            data = map_info.readlines()
                            map_index = data[0]
                            if "x" in map_index:
                                map_index = int(map_index, 16)
                            else:
                                map_index = int(map_index)
                    script_list = []
                    if map_index > -1:
                        # .Map index found
                        fh.seek(script_table + (map_index * 4))
                        cutscene_start = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
                        cutscene_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
                        cutscene_size = cutscene_end - cutscene_start
                        fh.seek(cutscene_start)
                        indicator = int.from_bytes(fh.read(2), "big")
                        fh.seek(cutscene_start)
                        data = fh.read(cutscene_size)
                        if indicator == 0x1F8B:
                            data = zlib.decompress(data, (15 + 32))
                        mods = []
                        mod_files = [x for x in files if ".json" in x]
                        for x in mod_files:
                            with open(f"{f}/{x}", "r") as fk:
                                mods.append(json.loads(fk.read()))
                        appended_items.append(buildFile(data, mods.copy(), map_index, f.split("\\")[-1].split("/")[-1]))
    return appended_items
