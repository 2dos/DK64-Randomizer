"""Library functions for pointer tables (Heavily WIP)."""

import js
import zlib
import gzip
from randomizer.Patching.Lib import TableNames
from randomizer.Patching.Patcher import ROM, LocalROM


class TableData:
    """Class to store information regarding a pointer table."""

    def __init__(self, vanilla_compressed: bool, rando_compressed: bool, decode_function: function = None, encode_function: function = None):
        """Initialize with given variables."""
        self.vanilla_compressed = vanilla_compressed
        self.rando_compressed = rando_compressed
        self.decode_function = decode_function
        self.encode_function = encode_function


def decoder_exits(data: bytes) -> dict:
    """Decode the exit data."""
    exit_count = int(len(data) / 10)
    ret = {"exits": []}
    for exit_index in range(exit_count):
        exit_data = {}
        ret["exits"].append(exit_data)
    return ret


table_functions = {
    TableNames.MusicMIDI: TableData(False, False, None, None),
    TableNames.MapGeometry: TableData(False, False, None, None),
    TableNames.MapWalls: TableData(False, False, None, None),
    TableNames.MapFloors: TableData(False, False, None, None),
    TableNames.ModelTwoGeometry: TableData(False, False, None, None),
    TableNames.ActorGeometry: TableData(False, False, None, None),
    TableNames.Unknown6: TableData(False, False, None, None),
    TableNames.TexturesUncompressed: TableData(False, False, None, None),
    TableNames.Cutscenes: TableData(False, False, None, None),
    TableNames.Setups: TableData(False, False, None, None),
    TableNames.InstanceScripts: TableData(False, False, None, None),
    TableNames.Animations: TableData(False, False, None, None),
    TableNames.Text: TableData(False, False, None, None),
    TableNames.Unknown13: TableData(False, False, None, None),
    TableNames.TexturesHUD: TableData(False, False, None, None),
    TableNames.Paths: TableData(False, False, None, None),
    TableNames.Spawners: TableData(False, False, None, None),
    TableNames.DKTVInputs: TableData(False, False, None, None),
    TableNames.Triggers: TableData(False, False, None, None),
    TableNames.Unknown19: TableData(False, False, None, None),
    TableNames.Unknown20: TableData(False, False, None, None),
    TableNames.Autowalks: TableData(False, False, None, None),
    TableNames.Unknown22: TableData(False, False, None, None),
    TableNames.Exits: TableData(False, False, None, None),
    TableNames.RaceCheckpoints: TableData(False, False, None, None),
    TableNames.TexturesGeometry: TableData(False, False, None, None),
    TableNames.UncompressedFileSizes: TableData(False, False, None, None),
    TableNames.Unknown27: TableData(False, False, None, None),
    TableNames.Unknown28: TableData(False, False, None, None),
    TableNames.Unknown29: TableData(False, False, None, None),
    TableNames.Unknown30: TableData(False, False, None, None),
    TableNames.Unknown31: TableData(False, False, None, None),
}


class PointerTableFile:
    """Class to store information about a pointer table file."""

    def __init__(self, table: TableNames, start: int, end: int, is_compressed: bool = None):
        """Initialize with given parameters."""
        self.start = start
        self.end = end
        self.size = end - start
        self.is_compressed = is_compressed
        if is_compressed is None:
            self.is_compressed = table_functions[table].rando_compressed


def getPointerFile(table: TableNames, file_index: int, is_compressed: bool = None) -> PointerTableFile:
    """Get pointer table file information."""
    start = js.pointer_addresses[table]["entries"][file_index]["pointing_to"]
    end = js.pointer_addresses[table]["entries"][file_index + 1]["pointing_to"]
    return PointerTableFile(table, start, end, is_compressed)


def getPointerData(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int) -> bytes:
    """Get the data inside a pointer table file."""
    ref_data = getPointerFile(table, file_index)
    ROM_COPY.seek(ref_data.start)
    data = ROM_COPY.readBytes(ref_data.size)
    if ref_data.is_compressed:
        return zlib.decompress(data, (15 + 32))
    return data


def writePointerFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int, data: bytes, is_compressed: bool = False):
    """Write data to a pointer file."""
    ref_file = getPointerFile(table, file_index)
    if is_compressed:
        data = gzip.compress(data, compresslevel=9)
    if len(data) > ref_file.size:
        raise Exception(f"Attempted to write data to a file slot which isn't big enough.\n- Table: {table}\n- File {file_index}\n- Attempt size {hex(len(data))}\n- Capacity: {hex(ref_file.size)}")
    ROM_COPY.seek(ref_file.start)
    ROM_COPY.writeBytes(data)


def decodeFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int) -> dict:
    """Decode a pointer table file."""
    function_data = table_functions.get(table, (None, None))
    file_data = getPointerData(ROM_COPY, table, file_index)
    if function_data.decode_function is None:
        return {
            "data": file_data,
        }
    return function_data.decode_function(file_data)


def encodeFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int, data: dict):
    """Encode a pointer table file."""
    function_data = table_functions.get(table, (None, None))
    ref_data = getPointerFile(table, file_index)
    if function_data.encode_function is None:
        writePointerFile(ROM_COPY, table, file_index, data["data"], ref_data.is_compressed)
        return
    output_data = function_data.encode_function(data)
    writePointerFile(ROM_COPY, table, file_index, output_data, ref_data.is_compressed)
