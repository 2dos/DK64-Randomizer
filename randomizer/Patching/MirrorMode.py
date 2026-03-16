"""Changes for Mirror Mode."""

import js
import gzip
import zlib
import time
from randomizer.Patching.Patcher import LocalROM, ROM
from randomizer.Settings import Settings
from randomizer.Patching.Library.Assets import TableNames, getRawFile, writeRawFile


def FlipDisplayList(ROM_COPY: LocalROM, data: bytearray, start: int, end: int, table: int, file: int):
    """Flip the 2nd and 3rd vertices on any G_TRI, G_TRI2 or G_QUAD f3dex2 call."""
    instruction_count = int((end - start) / 8)
    for ins in range(instruction_count):
        ins_start = start + (8 * ins)
        ins_type = data[ins_start]
        if ins_type in (5, 6, 7):
            for offset in (2, 6):
                v1 = data[ins_start + offset]
                v2 = data[ins_start + offset + 1]
                data[ins_start + offset] = v2
                data[ins_start + offset + 1] = v1
    writeRawFile(table, file, True, data, ROM_COPY)


def readDataFromBytestream(data: bytearray, offset: int, size: int, signed: bool = False) -> int:
    """Read data from a byte stream and output an int."""
    value = 0
    for x in range(size):
        value <<= 8
        value += data[offset + x]
    if signed:
        if value >= (1 << ((8 * size) - 1)):
            value = (1 << (8 * size)) - value
    return value


def writeValueToBytestream(data: bytearray, value: int, offset: int, size: int) -> bytearray:
    """Write data to a byte stream."""
    values = [0] * size
    value = int(value)
    if value < 0:
        value += 1 << (size * 8)
    for x in range(size):
        values[(size - x) - 1] = value & 0xFF
        value >>= 8
        if value == 0:
            break
    for x in range(size):
        data[offset + x] = values[x]
    return data


def ApplyMirrorMode(settings: Settings, ROM_COPY: LocalROM):
    """Apply all Mirror Mode changes."""
    if not settings.mirror_mode:
        return
    for tbl in (TableNames.ActorGeometry, TableNames.ModelTwoGeometry, TableNames.MapGeometry):
        file_count = len(js.pointer_addresses[tbl]["entries"])
        for file_index in range(file_count):
            data = bytearray(getRawFile(ROM_COPY, tbl, file_index, True))
            if len(data) == 0:
                continue
            if tbl == TableNames.MapGeometry:
                dl_start = readDataFromBytestream(data, 0x34, 4)
                dl_end = readDataFromBytestream(data, 0x38, 4)
            elif tbl == TableNames.ActorGeometry:
                addr_offset = readDataFromBytestream(data, 0, 4)
                dl_end = 0x28 + (readDataFromBytestream(data, 4, 4) - addr_offset)
                dl_start = 0x28 + (readDataFromBytestream(data, dl_end, 4) - addr_offset)
            elif tbl == TableNames.ModelTwoGeometry:
                dl_start = readDataFromBytestream(data, 0x40, 4)
                dl_end = readDataFromBytestream(data, 0x48, 4)
            FlipDisplayList(ROM_COPY, data, dl_start, dl_end, tbl, file_index)


MISC_SCALES = {
    0: 1,  # Test Map
    29: 1,  # Power Shed
    31: 1,  # K Rool's ship
    37: 1,  # Japes Blast
    41: 1,  # Aztec Blast
    44: 1,  # Treasure Chest
    45: 1,  # Mermaid Palace
    54: 1,  # Galleon Blast
    89: 1,  # Rotating Room
    171: 1,  # DK's House
    188: 1,  # Fungi Blast
}


def applyCoordTransform(value: float, map_index: int = 0, apply_scaling: bool = False):
    """Apply the flipping coordinate transform."""
    offset = 3000
    if apply_scaling:
        offset *= MISC_SCALES.get(map_index, 3)
    return offset - value


def ApplyMirrorModeNew(ROM_COPY: LocalROM):
    """Apply all Mirror Mode changes (testing)."""
    for map_index in range(216):
        map_geo = bytearray(getRawFile(ROM_COPY, TableNames.MapGeometry, map_index, True))
        print("Flipping Map ", map_index)
        walls_compressed = False
        floors_compressed = False
        walls_count = 0
        floors_count = 0
        if len(map_geo) > 0:
            # Get compression data
            compression_byte = map_geo[9]
            walls_compressed = (compression_byte & 1) != 0
            floors_compressed = (compression_byte & 2) != 0
            walls_count = readDataFromBytestream(map_geo, 0x10, 2) * readDataFromBytestream(map_geo, 0x12, 2)
            floors_count = readDataFromBytestream(map_geo, 0x18, 2) * readDataFromBytestream(map_geo, 0x1A, 2)
            # Invert verts
            vert_start = readDataFromBytestream(map_geo, 0x38, 4)
            vert_end = readDataFromBytestream(map_geo, 0x40, 4)
            vert_count = int((vert_end - vert_start) / 0x10)
            for x in range(vert_count):
                local_vert_start = vert_start + (0x10 * x)
                val = readDataFromBytestream(map_geo, local_vert_start, 2, True)
                map_geo = writeValueToBytestream(map_geo, applyCoordTransform(val, map_index, True), local_vert_start, 2)
            # Invert Map Void
            void_min_x = readDataFromBytestream(map_geo, 0x26, 2, True)
            void_max_x = readDataFromBytestream(map_geo, 0x2A, 2, True)
            map_geo = writeValueToBytestream(map_geo, applyCoordTransform(void_max_x, map_index), 0x26, 2)
            map_geo = writeValueToBytestream(map_geo, applyCoordTransform(void_min_x, map_index), 0x2A, 2)
            # Invert Chunks
            chunk_start = readDataFromBytestream(map_geo, 0x64, 4)
            chunk_count = readDataFromBytestream(map_geo, chunk_start, 4)
            for x in range(chunk_count):
                local_header = chunk_start + 4 + (0xC * x)
                location = chunk_start + readDataFromBytestream(map_geo, local_header, 4)
                x_min = readDataFromBytestream(map_geo, local_header + 0x4, 2, True) / 6
                x_max = readDataFromBytestream(map_geo, local_header + 0x8, 2, True) / 6
                new_x_min = applyCoordTransform(x_max, map_index) * 6
                new_x_max = applyCoordTransform(x_min, map_index) * 6
                map_geo = writeValueToBytestream(map_geo, new_x_min, local_header + 0x4, 2)
                map_geo = writeValueToBytestream(map_geo, new_x_max, local_header + 0x8, 2)
                location0 = chunk_start + readDataFromBytestream(map_geo, local_header + 0xC, 4)
                count = int((location0 - location) / 0x14)
                for y in range(count):
                    local_header_0 = location + (y * 0x14)
                    for z in range(3):
                        value = readDataFromBytestream(map_geo, local_header_0 + (2 * z), 2, True) / 6
                        new_value = applyCoordTransform(value, map_index) * 6
                        map_geo = writeValueToBytestream(map_geo, new_value, local_header_0 + 0x4 - (2 * z), 2)
            # Invert all map coord stuff
            # Flip Tri Render Order
            dl_start = readDataFromBytestream(map_geo, 0x34, 4)
            FlipDisplayList(ROM_COPY, map_geo, dl_start, vert_start, TableNames.MapGeometry, map_index)
        collision_data = [
            {
                "table": TableNames.MapFloors,
                "comp": floors_compressed,
                "count": floors_count,
                "divisor": 6,
            },
            {
                "table": TableNames.MapWalls,
                "comp": walls_compressed,
                "count": walls_count,
                "divisor": 1,
            },
        ]
        for coldata in collision_data:
            tbl = coldata["table"]
            compressed = coldata["comp"]
            file_data = bytearray(getRawFile(ROM_COPY, tbl, map_index, compressed))
            if len(file_data) > 0:
                print("Processing ", tbl.name, " in map ", hex(map_index), " with count ", coldata["count"], " with length ", hex(len(file_data)), ". Compression: ", compressed)
                start = 8
                for x in range(coldata["count"]):
                    print(hex(start))
                    if start >= len(file_data):
                        continue
                    ref = start - 4
                    block_end = readDataFromBytestream(file_data, ref, 4)
                    ref += 4
                    block_count = int((block_end - start) / 0x18)
                    print(
                        hex(block_end),
                        hex(block_count),
                    )
                    for _ in range(block_count):
                        div = coldata["divisor"]
                        for cs in range(3):
                            if tbl == TableNames.MapFloors:
                                value = readDataFromBytestream(file_data, ref, 2, True) / div
                                new_value = applyCoordTransform(value, map_index) * div
                                file_data = writeValueToBytestream(file_data, new_value, ref, 2)
                                ref += 6
                            elif tbl == TableNames.MapWalls:
                                value = readDataFromBytestream(file_data, ref, 2, True) / div
                                new_value = applyCoordTransform(value, map_index) * div
                                file_data = writeValueToBytestream(file_data, new_value, ref, 2)
                                ref += 2
                                if cs == 2:
                                    ref += 12  # Skip Y and Z
                        ref += 6
                    start = block_end + 4
                writeRawFile(tbl, map_index, compressed, file_data, ROM_COPY)
        map_exits = bytearray(getRawFile(ROM_COPY, TableNames.Exits, map_index, False))
        if len(map_exits) > 0:
            exit_count = readDataFromBytestream(map_exits, 10, 2)
            offsets = [0]
            for x in range(exit_count):
                offsets.append(12 + (10 * x))
            for offset in offsets:
                value = readDataFromBytestream(map_exits, offset, 2, True)
                new_value = applyCoordTransform(value, map_index)
                map_exits = writeValueToBytestream(map_exits, new_value, offset, 2)
            writeRawFile(TableNames.Exits, map_index, False, map_exits, ROM_COPY)


def trimData(data: bytes, alignment: int = 0x10, grouping: int = 1) -> bytes:
    """Trim a bytes object to remove trailing null bytes, and then align the size of the object to a certain modulo."""
    if alignment <= 0:
        raise ValueError("alignment must be positive")

    i = len(data) - 1
    while i >= (grouping - 1) and data[i] == 0:
        non_zero_in_grouping = False
        if grouping > 1:
            for x in range(grouping):
                if data[i - x]:
                    non_zero_in_grouping = True
            if non_zero_in_grouping:
                break
        i -= 1
    if i < 0:
        return b""
    trimmed = data[: i + 1]

    pad = (-len(trimmed)) % alignment
    if pad:
        trimmed += b"\x00" * pad

    return trimmed


def truncateFiles(ROM_COPY: ROM):
    """Truncate the size of compressed files."""
    start = time.perf_counter()
    POINTER_OFFSET = 0x101C50
    uncompressed_tables = [
        TableNames.TexturesUncompressed,
        TableNames.Cutscenes,
        TableNames.Setups,
        # TableNames.InstanceScripts,
        TableNames.Text,
        TableNames.Spawners,
        TableNames.Triggers,
        TableNames.Unknown20,
        TableNames.Autowalks,
        TableNames.Exits,
        TableNames.RaceCheckpoints,
    ]
    total_bytes_overwritten = 0
    for table_id in range(26):
        if table_id in uncompressed_tables:
            # These tables are always uncompressed, ignore
            continue
        if table_id in (TableNames.MapWalls, TableNames.MapFloors):
            # messing with these tables causes the game to take a hard angry nap
            continue
        ROM_COPY.seek(POINTER_OFFSET + (32 * 4) + (table_id * 4))
        entry_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        files = []
        ROM_COPY.seek(POINTER_OFFSET + (table_id * 4))
        table_start = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
        please_shift = False
        for entry in range(entry_count):
            ROM_COPY.seek(table_start + (entry * 4))
            file_start = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            file_end = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            file_size = file_end - file_start
            if file_size <= 0:
                files.append(b"")
                continue
            ROM_COPY.seek(file_start)
            data = ROM_COPY.readBytes(file_size)
            ROM_COPY.seek(file_start)
            indicator = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if indicator == 0x1F8B:
                truncated_data = gzip.compress(zlib.decompress(data, (15 + 32)), compresslevel=9)
                if len(data) != len(truncated_data):
                    please_shift = True
            elif table_id == TableNames.MusicMIDI:
                truncated_data = trimData(data, 0x10)
                please_shift = True
            elif table_id == TableNames.InstanceScripts:
                truncated_data = trimData(data, 0x10, 0x10)
                please_shift = True
            else:
                truncated_data = data
            files.append(truncated_data)
        if please_shift:
            ROM_COPY.seek(table_start)
            head = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            total_offset = 0
            for entry in range(entry_count):
                ROM_COPY.seek(table_start + (entry * 4) + 4)
                entry_size = len(files[entry])
                append_byte = False
                if (entry_size % 2) == 1:
                    entry_size += 1
                    append_byte = True
                file_head = head + total_offset
                new_location = (head + total_offset + entry_size) - POINTER_OFFSET
                ROM_COPY.writeMultipleBytes(new_location, 4)
                ROM_COPY.seek(file_head)
                ROM_COPY.writeBytes(files[entry])
                if append_byte:
                    ROM_COPY.write(0)
                total_offset += entry_size
                total_bytes_overwritten += entry_size + 4
    end = time.perf_counter()
    print(f"File truncating took {end - start:.6f} seconds. Processed {hex(total_bytes_overwritten)} bytes")
