"""Encoders for updating file data."""

import json
import math
import struct
from typing import BinaryIO

from BuildNames import actor_names, character_spawner_names, cutscene_model_names, maps, model2_names

# Useful for detecting booleans, enums, indexes etc
valueSamples = {}


def sampleValue(tag: str, value):
    """Sample the value."""
    if tag not in valueSamples:
        valueSamples[tag] = {"min": math.inf, "max": -math.inf, "all": {}}
    if isinstance(value, int) or isinstance(value, float):
        valueSamples[tag]["min"] = min(value, valueSamples[tag]["min"])
        valueSamples[tag]["max"] = max(value, valueSamples[tag]["max"])
    if value not in valueSamples[tag]["all"]:
        valueSamples[tag]["all"][value] = 0
    valueSamples[tag]["all"][value] += 1
    return value


dump_struct_debug_info = False


def ScriptHawkSetPosition(x, y, z):
    """Set Scripthawk position."""
    return "Game.setPosition(" + str(x) + "," + str(y) + "," + str(z) + ");"


def getStructSize(struct_fields: list):
    """Get Struct size."""
    totalSize = 0
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["size"] = 1
        elif field["type"] == "short":
            field["size"] = 2
        elif field["type"] == "ushort":
            field["size"] = 2
        elif field["type"] == float:
            field["size"] = 4

        totalSize += field["size"]

    return totalSize


def readStructArray(byte_read: bytes, offset: int, length: int, struct_fields: list):
    """Read Struct Array."""
    decoded_struct_array = []
    read_head = offset
    struct_size = getStructSize(struct_fields)
    for i in range(length):
        decoded_struct_array.append(readStruct(byte_read, read_head, struct_fields))
        read_head += struct_size
    return decoded_struct_array


def readStruct(byte_read: bytes, offset: int, struct_fields: list):
    """Read a particular struct."""
    read_head = offset
    decoded_struct = {}
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        if field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head : read_head + field["size"]], byteorder="big", signed=True)
        elif field["type"] == "uint":
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head : read_head + field["size"]], byteorder="big")
        elif field["type"] == float:
            field["size"] = 4
            decoded_struct[field["name"]] = struct.unpack(">f", byte_read[read_head : read_head + 4])[0]
        elif field["type"] == bool:
            decoded_struct[field["name"]] = True if int.from_bytes(byte_read[read_head : read_head + field["size"]], byteorder="big") else False
        elif field["type"] == bytes:
            decoded_struct[field["name"]] = byte_read[read_head : read_head + field["size"]].hex(" ").upper()
        else:
            print("Unknown field type in readStruct(): " + field["type"])

        if "index_of" in field:
            index_offset = 0
            if "index_offset" in field:
                index_offset = field["index_offset"]

            if decoded_struct[field["name"]] + index_offset < len(field["index_of"]):
                decoded_struct[field["name"] + "_name"] = field["index_of"][decoded_struct[field["name"]] + index_offset]
            else:
                decoded_struct[field["name"] + "_name"] = "Unknown " + hex(decoded_struct[field["name"]] + index_offset)

        if "sample" in field:
            sampleName = field["sample"] if isinstance(field["sample"], str) else field["name"]
            sampleValue(sampleName, decoded_struct[field["name"]])

        read_head += field["size"]

    if dump_struct_debug_info:
        decoded_struct["DEBUG_File_Address"] = hex(offset)
        if "x_pos" in decoded_struct and "y_pos" in decoded_struct and "z_pos" in decoded_struct:
            decoded_struct["DEBUG_Set_Position"] = ScriptHawkSetPosition(decoded_struct["x_pos"], decoded_struct["y_pos"], decoded_struct["z_pos"])

    return decoded_struct


def writeStructArray(fh: BinaryIO, struct_array: list, struct_fields: list, include_count: bool = False, count_bytes: int = 0):
    """Write the struct Array."""
    if include_count:
        fh.write(len(struct_array).to_bytes(count_bytes, byteorder="big"))

    for struct_data in struct_array:
        writeStruct(fh, struct_data, struct_fields)


def writeStruct(fh: BinaryIO, struct_data: dict, struct_fields: list):
    """Write a particular struct."""
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        elif field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big", signed=True))
        elif field["type"] == "uint":
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big"))
        elif field["type"] == float:
            fh.write(struct.pack(">f", struct_data[field["name"]]))
        elif field["type"] == bool:
            fh.write(bytes([1 if struct_data[field["name"]] else 0]))
        elif field["type"] == bytes:
            fh.write(bytes.fromhex(struct_data[field["name"]]))
        else:
            print("Unknown field type in readStruct(): " + field["type"])


lz_object_types = [
    "Unknown 0x0",  # In maps 6,14,30,43,55,106 (Minecarts, Aztec Beetle Race, Galleon, Shipwreck)
    "Unused 0x1",
    "Unknown 0x2",  # In Castle Minecart / MJ / Fungi (Rabbit Race)
    "Boss Door Trigger 0x3",  # Also sets boss fadeout type as fade instead of spin. In toolshed too??
    "Unknown 0x4",  # In Fungi Minecart
    "Cutscene Trigger 0x5",
    "Unknown 0x6",  # In Treehouse / MJ / Fungi. Not phase reset plane
    "Unknown 0x7",  # In Fungi / Fungi Minecart
    "Unknown 0x8",  # In Fungi / Fungi Minecart
    "Loading Zone 0x9",
    "Cutscene Trigger 0xA",
    "Unknown 0xB",  # In Minecart Mayhem
    "Loading Zone + Objects 0xC",  # Alows objects through
    "Loading Zone 0xD",
    "Unused 0xE",
    "Warp Trigger 0xF",  # Factory Poles
    "Loading Zone 0x10",
    "Loading Zone 0x11",  # Snide's, Return to Parent Map?
    "Unused 0x12",
    "Unknown 0x13",  # In maps 7,17,30,34,38,47,48,194 (Japes, Helm, Galleon, Isles, Aztec, Shipwreck, Fungi, Caves)
    "Boss Loading Zone 0x14",  # Takes you to the boss of that level
    "Cutscene Trigger 0x15",
    "Unknown 0x16",  # In Aztec Beetle Race
    "Cutscene Trigger 0x17",
    "Unknown 0x18",  # In Fungi Minecart
    "Trigger 0x19",  # Seal Race
    "Unknown 0x1A",  # In Caves Beetle Race
    "Slide Trigger 0x1B",  # Beetle Races
    "Unknown 0x1C",  # Beetle Races
    "Unused 0x1D",
    "Unused 0x1E",
    "Unused 0x1F",
    "Cutscene Trigger 0x20",
    "Unused 0x21",
    "Unused 0x22",
    "Unused 0x23",
    "Unknown 0x24",  # Cannon Trigger? Also used Aztec Snake Road and maps 7,17,26,34,38,48,72,173
    "Unknown 0x25",  # In Factory
    "Unknown 0x26",  # In BFI & K. Lumsy. Seems to be centred around torches?
]

lz_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "radius", "type": "short"},
    {"name": "height", "type": "short"},
    {"name": "unkA", "type": "ushort"},  # Probably an index, values range from 0-50 except 38 is never seen
    {"name": "activation_type", "type": "byte"},
    {"name": "boolD", "type": bool, "size": 1},  # If set, enter K. Rool LZ is active without all keys
    {"name": "unkE", "type": "byte"},  # Usually 1, but values range from 0-4
    {"name": "unkF", "type": "byte"},  # Usually 0, but other known values are 2,4,5,32,48,50,64,75,80,96,128,144,209,228,255
    {"name": "object_type", "type": "short", "index_of": lz_object_types},
    {"name": "destination_map", "type": "ushort", "index_of": maps},
    {"name": "destination_exit", "type": "ushort"},
    {"name": "transition_type", "type": "ushort"},
    {"name": "unk18", "type": "ushort"},
    {"name": "cutscene_is_tied", "type": "ushort"},
    {"name": "cutscene_index", "type": "ushort"},
    {"name": "shift_camera_to_kong", "type": "ushort"},
    {"name": "unk20", "type": bytes, "size": 0x38 - 0x20},  # TODO: Break this down into smaller fields
]


def decodeLoadingZones(decoded_filename: str, encoded_filename: str):
    """Decode loading zones."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_loading_zones = int.from_bytes(byte_read[0x0:0x2], byteorder="big")

        loading_zones = readStructArray(byte_read, 2, num_loading_zones, lz_struct)
        for lz_data in loading_zones:
            if "Loading Zone" not in lz_data["object_type_name"]:
                del lz_data["destination_map_name"]

        with open(decoded_filename, "w") as fjson:
            json.dump(loading_zones, fjson, indent=4, default=str)


def encodeLoadingZones(decoded_filename: str, encoded_filename: str):
    """Encode loading zones."""
    with open(decoded_filename) as fjson:
        loading_zones = json.load(fjson)

        with open(encoded_filename, "w+b") as fh:
            writeStructArray(fh, loading_zones, lz_struct, include_count=True, count_bytes=2)


exit_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "angle", "type": "short"},
    {"name": "has_autowalk", "type": "byte"},  # Vanilla uses values 0, 1, and 2
    {"name": "size", "type": "byte"},  # Vanilla uses values 0 and 1 (TODO: boolean?)
]


def decodeExits(decoded_filename: str, encoded_filename: str):
    """Decode exits."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_exits = math.floor(len(byte_read) / 0xA)
        exits = readStructArray(byte_read, 0, num_exits, exit_struct)
        with open(decoded_filename, "w") as fjson:
            json.dump(exits, fjson, indent=4, default=str)


def encodeExits(decoded_filename: str, encoded_filename: str):
    """Encode exits."""
    with open(decoded_filename) as fjson:
        exits = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            writeStructArray(fh, exits, exit_struct)


autowalk_point_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "unk6", "type": bytes, "size": 0x12 - 0x6},  # TODO: Break this down into smaller fields
]


def decodeAutowalk(decoded_filename: str, encoded_filename: str):
    """Decode autowalk."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        path_base = 0
        autowalk_paths = []

        num_paths = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        path_base += 2
        for i in range(num_paths):
            num_points = int.from_bytes(byte_read[path_base : path_base + 2], byteorder="big")
            path_base += 2
            path = readStructArray(byte_read, path_base, num_points, autowalk_point_struct)
            path_base += num_points * 0x12
            autowalk_paths.append(path)

        with open(decoded_filename, "w") as fjson:
            json.dump(autowalk_paths, fjson, indent=4, default=str)


def encodeAutowalk(decoded_filename: str, encoded_filename: str):
    """Encode autowalk."""
    with open(decoded_filename) as fjson:
        autowalk_paths = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            fh.write(len(autowalk_paths).to_bytes(2, byteorder="big"))
            for path in autowalk_paths:
                writeStructArray(fh, path, autowalk_point_struct, include_count=True, count_bytes=2)


path_point_struct = [
    {"name": "unk0", "type": "short"},
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "speed", "type": "byte"},  # 1 - 3 in vanilla
    {"name": "unk9", "type": "byte"},  # Ranges from 0-255
]


def decodePaths(decoded_filename: str, encoded_filename: str):
    """Decode paths."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        paths = []
        num_paths = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        path_base = 2
        for i in range(num_paths):
            this_path = byte_read[path_base : path_base + 0x6]
            num_points = int.from_bytes(this_path[0x2:0x4], byteorder="big")
            path = {"id": int.from_bytes(this_path[0x0:0x2], byteorder="big"), "unk4": int.from_bytes(this_path[0x4:0x6], byteorder="big")}
            # sampleValue("path->unk4", path["unk4"])
            path_base += 0x6

            if num_points > 0:
                path["points"] = readStructArray(byte_read, path_base, num_points, path_point_struct)
                path_base += num_points * 0xA

            paths.append(path)

        with open(decoded_filename, "w") as fjson:
            json.dump(paths, fjson, indent=4, default=str)


def encodePaths(decoded_filename: str, encoded_filename: str):
    """Encode Paths."""
    with open(decoded_filename) as fjson:
        paths = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            # File header
            fh.write(len(paths).to_bytes(2, byteorder="big"))

            for path in paths:
                num_points = len(path["points"]) if "points" in path else 0

                # Path header
                fh.write(int(path["id"]).to_bytes(2, byteorder="big"))
                fh.write(num_points.to_bytes(2, byteorder="big"))
                fh.write(int(path["unk4"]).to_bytes(2, byteorder="big"))

                # Path points
                if num_points > 0:
                    writeStructArray(fh, path["points"], path_point_struct)


checkpoint_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "angle", "type": "short"},
    {"name": "unk8", "type": float},  # sin(angle)
    {"name": "unkC", "type": float},  # cos(angle)
    {"name": "visibility", "type": "byte"},  # 0 is goal, seal race is 1 (buoy?), 2 = Car Race Goal
    {"name": "unk11", "type": "byte"},  # Always 0
    {"name": "unk12", "type": "ushort"},  # Always 0
    {"name": "unk14", "type": float},  # Scale
    {"name": "unk18", "type": "byte"},  # Flag Rendering Mode - Always 2
    {"name": "unk19", "type": "byte"},  # Always 0
    {"name": "unk1A", "type": "ushort"},  # Seen values of 26,39,42,43,44,47,48,49,50,53,55,65,89,90,110,124
]


def decodeCheckpoints(decoded_filename: str, encoded_filename: str):
    """Decode Checkpoints."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        checkpoints = []
        num_checkpoints = int.from_bytes(byte_read[0x1:0x3], byteorder="big")
        num_checkpoint_mappings = int.from_bytes(byte_read[0x3:0x5], byteorder="big")

        if num_checkpoints != num_checkpoint_mappings:
            print(" - Error: Number of checkpoints does not match number of checkpoint mappings.")
            return 0

        checkpoint_base = 5 + num_checkpoint_mappings * 2
        for i in range(num_checkpoints):
            mapping = int.from_bytes(byte_read[5 + i * 2 : 7 + i * 2], byteorder="big")
            checkpoint = readStruct(byte_read, checkpoint_base, checkpoint_struct)

            # Only include the mapping in the JSON if it does not match the physical index
            if mapping != i:
                checkpoint["mapping"] = mapping

            checkpoints.append(checkpoint)
            checkpoint_base += 0x1C

        with open(decoded_filename, "w") as fjson:
            json.dump(checkpoints, fjson, indent=4, default=str)


def encodeCheckpoints(decoded_filename: str, encoded_filename: str):
    """Encode Checkpoints."""
    with open(decoded_filename) as fjson:
        checkpoints = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            # File header
            fh.write(bytes([0x1]))  # Seems to always be 1
            fh.write(len(checkpoints).to_bytes(2, byteorder="big"))  # Num Checkpoints
            fh.write(len(checkpoints).to_bytes(2, byteorder="big"))  # Num Mappings

            # Checkpoint index mapping
            for checkpointIndex, checkpoint in enumerate(checkpoints):
                if "mapping" in checkpoint:
                    fh.write(int(checkpoint["mapping"]).to_bytes(2, byteorder="big"))
                else:
                    fh.write(checkpointIndex.to_bytes(2, byteorder="big"))

            # Checkpoint data
            writeStructArray(fh, checkpoints, checkpoint_struct)


character_spawner_point_0x6_struct = [{"name": "x_pos", "type": "short"}, {"name": "y_pos", "type": "short"}, {"name": "z_pos", "type": "short"}]
character_spawner_point_0xA_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "unk6", "type": bytes, "size": 0xA - 0x6},  # TODO: Break this down into smaller fields
]
character_spawner_struct = [
    {"name": "enemy_val", "type": "byte", "index_of": character_spawner_names},
    {"name": "unk1", "type": "byte"},  # Seen values 0-248 with some gaps (most commonly 0,124,125)
    {"name": "y_rot", "type": "ushort"},
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "cutscene_model", "type": "byte", "index_of": cutscene_model_names},
    {"name": "unkB", "type": "byte"},  # Seen values 0-215 with some gaps, 0 and 40 are most common
    {"name": "max_idle_speed", "type": "byte"},
    {"name": "max_aggro_speed", "type": "byte"},
    {"name": "unkE", "type": "byte"},  # Seen values 1-47 with decreasing frequency as the value increases, possibly an index?
    {"name": "scale", "type": "byte"},
    {"name": "aggro", "type": "byte"},
    {"name": "extra_data_count", "type": "byte"},
    {"name": "initial_spawn_state", "type": "byte"},
    {"name": "spawn_trigger", "type": "byte"},
    {"name": "initial_respawn_timer", "type": "byte"},
    {"name": "unk15", "type": "byte"},  # Seen values 0-254 with some gaps, 0 is most common
]


def decodeCharacterSpawners(decoded_filename: str, encoded_filename: str):
    """Decode character Spawners."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        read_header = 0
        extract = {}

        # Fences?
        num_fences = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        read_header += 2

        if num_fences > 0:
            extract["fences"] = []
            for i in range(num_fences):
                fence_data = {}

                # Points_0x6
                num_points = int.from_bytes(byte_read[read_header : read_header + 2], byteorder="big")
                read_header += 2

                if num_points > 0:
                    fence_data["points_0x6"] = readStructArray(byte_read, read_header, num_points, character_spawner_point_0x6_struct)
                    read_header += num_points * 0x6

                # Points_0xA
                num_points_0xA = int.from_bytes(byte_read[read_header : read_header + 2], byteorder="big")
                read_header += 2

                if num_points_0xA > 0:
                    fence_data["points_0xA"] = readStructArray(byte_read, read_header, num_points_0xA, character_spawner_point_0xA_struct)
                    read_header += num_points_0xA * 0xA

                # fence_data["unkFooterAddress"] = hex(read_header)
                fence_data["unkFooter"] = byte_read[read_header : read_header + 0x4].hex(" ").upper()  # TODO: Break this down into smaller fields
                read_header += 4

                extract["fences"].append(fence_data)

        # Spawners
        num_character_spawners = int.from_bytes(byte_read[read_header : read_header + 2], byteorder="big")
        read_header += 2

        if num_character_spawners > 0:
            extract["character_spawners"] = []
            for i in range(num_character_spawners):
                spawner_data = readStruct(byte_read, read_header, character_spawner_struct)

                extra_count = spawner_data["extra_data_count"]
                del spawner_data["extra_data_count"]
                read_header += 0x16

                if spawner_data["enemy_val_name"] != "Cutscene Object":
                    del spawner_data["cutscene_model_name"]

                # TODO: Figure what it does
                if extra_count > 0:
                    spawner_data["extra_data"] = []
                    for j in range(extra_count):
                        spawner_data["extra_data"].append(int.from_bytes(byte_read[read_header : read_header + 2], byteorder="big"))
                        read_header += 2

                extract["character_spawners"].append(spawner_data)

        # Note: This is the case for several maps
        # TODO: Figure out why, and if/how they map fences onto spawners
        # if num_character_spawners != num_fences:
        # print("FENCE COUNT (" + str(num_fences) + ") != SPAWN COUNT (" + str(num_character_spawners) + ") IN " + decoded_filename)

        with open(decoded_filename, "w") as fjson:
            json.dump(extract, fjson, indent=4, default=str)


def encodeCharacterSpawners(decoded_filename: str, encoded_filename: str):
    """Encode Character Spawners."""
    with open(decoded_filename) as fjson:
        spawners = json.load(fjson)

        with open(encoded_filename, "w+b") as fh:
            # Fences
            num_fences = len(spawners["fences"]) if "fences" in spawners else 0
            fh.write(num_fences.to_bytes(2, byteorder="big"))
            if num_fences > 0:
                for fence in spawners["fences"]:
                    num_points = len(fence["points_0x6"]) if "points_0x6" in fence else 0
                    fh.write(num_points.to_bytes(2, byteorder="big"))
                    if "points_0x6" in fence:
                        writeStructArray(fh, fence["points_0x6"], character_spawner_point_0x6_struct)

                    num_points_0xA = len(fence["points_0xA"]) if "points_0xA" in fence else 0
                    fh.write(num_points_0xA.to_bytes(2, byteorder="big"))
                    if "points_0xA" in fence:
                        writeStructArray(fh, fence["points_0xA"], character_spawner_point_0xA_struct)

                    fh.write(bytes.fromhex(fence["unkFooter"]))

            # Spawners
            num_character_spawners = len(spawners["character_spawners"]) if "character_spawners" in spawners else 0
            fh.write(num_character_spawners.to_bytes(2, byteorder="big"))
            if num_character_spawners > 0:
                for spawner in spawners["character_spawners"]:
                    spawner["extra_data_count"] = len(spawner["extra_data"]) if "extra_data" in spawner else 0
                    writeStruct(fh, spawner, character_spawner_struct)
                    if "extra_data" in spawner:
                        for extra_data in spawner["extra_data"]:
                            fh.write(int(extra_data).to_bytes(2, byteorder="big"))


setup_model2_struct = [
    {"name": "x_pos", "type": float},
    {"name": "y_pos", "type": float},
    {"name": "z_pos", "type": float},
    {"name": "scale", "type": float},
    {"name": "unk10", "type": bytes, "size": 0x18 - 0x10},  # TODO: Break this down into smaller fields
    {"name": "angle18", "type": float},
    {"name": "angle1C", "type": float},
    {"name": "angle20", "type": float},
    {"name": "unk24", "type": float},
    {"name": "behaviour", "type": "short", "index_of": model2_names},
    {"name": "unk2A", "type": bytes, "size": 0x30 - 0x2A},  # TODO: Break this down into smaller fields
]
setup_conveyor_data_struct = [
    {"name": "model2Index", "type": int, "size": 4},  # Note: Not included in JSON, instead this struct lives in setup["model2"][index]["conveyorData"]
    {"name": "unk4", "type": float},
    {"name": "unk8", "type": float},
    {"name": "unkC", "type": float},
    {"name": "unk10", "type": float},
    {"name": "unk14", "type": float},
    {"name": "unk18", "type": float},
    {"name": "unk1C", "type": float},
    {"name": "unk20", "type": float},
]
setup_actor_spawner_struct = [
    {"name": "x_pos", "type": float},
    {"name": "y_pos", "type": float},
    {"name": "z_pos", "type": float},
    {"name": "scale", "type": float},
    {"name": "unk10", "type": bytes, "size": 0x32 - 0x10},  # TODO: 0x10 is sometimes a float, how do we integrate this?
    # {"name": "destination_map", "type": "byte"}, # TODO: At 0x13, Only for bonus barrels, how do we integrate this?
    {"name": "behaviour", "type": "ushort", "index_of": actor_names, "index_offset": 0x10},
    {"name": "unk34", "type": bytes, "size": 0x38 - 0x34},  # TODO: Break this down into smaller fields
]


def decodeSetup(decoded_filename: str, encoded_filename: str):
    """Decode Setup."""
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        pointer = 0

        setup = {}

        # Object Model 2
        num_model2 = int.from_bytes(byte_read[pointer : pointer + 0x4], byteorder="big")
        pointer += 4

        if num_model2 > 0:
            setup["model2"] = readStructArray(byte_read, pointer, num_model2, setup_model2_struct)
            pointer += num_model2 * 0x30

        # Conveyor Data
        num_conveyor = int.from_bytes(byte_read[pointer : pointer + 0x4], byteorder="big")
        pointer += 4

        if num_conveyor > 0:
            for i in range(num_conveyor):
                conveyor_data = readStruct(byte_read, pointer, setup_conveyor_data_struct)

                # Put this struct in to the right spot and get rid of unneeded data
                model2_index = conveyor_data["model2Index"]
                del conveyor_data["model2Index"]
                setup["model2"][model2_index]["conveyor_data"] = conveyor_data

                pointer += 0x24

        # Actor Spawners
        num_actor_spawners = int.from_bytes(byte_read[pointer : pointer + 0x4], byteorder="big")
        pointer += 4

        if num_actor_spawners > 0:
            setup["actors"] = readStructArray(byte_read, pointer, num_actor_spawners, setup_actor_spawner_struct)
            pointer += num_actor_spawners * 0x38

        with open(decoded_filename, "w") as fjson:
            json.dump(setup, fjson, indent=4, default=str)


def encodeSetup(decoded_filename: str, encoded_filename: str):
    """Encode Setup."""
    with open(decoded_filename) as fjson:
        setup = json.load(fjson)

        with open(encoded_filename, "w+b") as fh:
            num_conveyors = 0
            num_model2 = len(setup["model2"]) if "model2" in setup else 0
            num_actor_spawners = len(setup["actors"]) if "actors" in setup else 0

            # Model 2
            fh.write(num_model2.to_bytes(4, byteorder="big"))

            if num_model2 > 0:
                for i, this_model2 in enumerate(setup["model2"]):
                    writeStruct(fh, this_model2, setup_model2_struct)
                    if "conveyor_data" in this_model2:
                        num_conveyors += 1

            # Conveyor Data
            fh.write(num_conveyors.to_bytes(4, byteorder="big"))

            if num_conveyors > 0:
                for i, this_model2 in enumerate(setup["model2"]):
                    if "conveyor_data" in this_model2:
                        conveyor_data = this_model2["conveyor_data"]
                        conveyor_data["model2Index"] = i
                        writeStruct(fh, conveyor_data, setup_conveyor_data_struct)

            # Actor Spawners
            fh.write(num_actor_spawners.to_bytes(4, byteorder="big"))

            if num_actor_spawners > 0:
                writeStructArray(fh, setup["actors"], setup_actor_spawner_struct)
