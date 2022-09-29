"""Extracts data from a ROM regarding coins, balloons and bananas."""
import zlib
import struct
import json
import os

dk64_rom = "bismuth-balloon-crash.z64"
pointer_table_offset = 0x101C50
setup_table_index = 9
path_table_index = 15

model2_types = [
    {"name": "CB Single (Diddy)", "type": 0xA, "kong": "Kongs.diddy"},
    {"name": "CB Single (DK)", "type": 0xD, "kong": "Kongs.donkey"},
    {"name": "CB Single (Tiny)", "type": 0x16, "kong": "Kongs.tiny"},
    {"name": "CB Single (Lanky)", "type": 0x1E, "kong": "Kongs.lanky"},
    {"name": "CB Single (Chunky)", "type": 0x1F, "kong": "Kongs.chunky"},
    {"name": "CB Bunch (DK)", "type": 0x2B, "kong": "Kongs.donkey"},
    {"name": "CB Bunch (Lanky)", "type": 0x205, "kong": "Kongs.lanky"},
    {"name": "CB Bunch (Chunky)", "type": 0x206, "kong": "Kongs.chunky"},
    {"name": "CB Bunch (Tiny)", "type": 0x207, "kong": "Kongs.tiny"},
    {"name": "CB Bunch (Diddy)", "type": 0x208, "kong": "Kongs.diddy"},
    {"name": "Coin (Tiny)", "type": 0x1C, "kong": "Kongs.tiny"},
    {"name": "Coin (DK)", "type": 0x1D, "kong": "Kongs.donkey"},
    {"name": "Coin (Lanky)", "type": 0x23, "kong": "Kongs.lanky"},
    {"name": "Coin (Diddy)", "type": 0x24, "kong": "Kongs.diddy"},
    {"name": "Coin (Chunky)", "type": 0x27, "kong": "Kongs.chunky"},
]

actor_types = [
    {"name": "Balloon (Diddy)", "type": 91, "kong": "Kongs.diddy"},
    {"name": "Balloon (Chunky)", "type": 111, "kong": "Kongs.chunky"},
    {"name": "Balloon (Tiny)", "type": 112, "kong": "Kongs.tiny"},
    {"name": "Balloon (Lanky)", "type": 113, "kong": "Kongs.lanky"},
    {"name": "Balloon (DK)", "type": 114, "kong": "Kongs.donkey"},
]


def intf_to_float(intf):
    """Int float rep to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex(hex(intf)[2:]))[0]


def ushort_to_short(ushort):
    """Unsigned short to short converter."""
    if ushort > 32767:
        ushort -= 65536
    return ushort


map_data = []

cb_model2_name = "bananas_modeltwo.txt"
cb_actor_name = "bananas_actor.txt"
coin_model2_name = "coins.txt"

files = [cb_model2_name, cb_actor_name, coin_model2_name]
for f in files:
    if os.path.exists(f):
        os.remove(f)


def handleCreate(f_name):
    """Create file."""
    if not os.path.exists(f_name):
        with open(f_name, "w") as fh:
            fh.seek(0)


balloon_id = 0
cb_group = 0
coin_group = 0


def dumpData(data, map):
    """Dump data to file."""
    global balloon_id
    global cb_group
    global coin_group
    if data["object_type"] == "model_two":
        # Model Two Handler
        if "CB" in data["name"]:
            handleCreate(cb_model2_name)
            cb_count = 1
            if "Bunch" in data["name"]:
                cb_count = 5
            with open(cb_model2_name, "a") as fh:
                fh.write(f"ColoredBananaGroup(group={cb_group},map_id={map},name=\"\",konglist=[{data['kong']}], region=\"\", locations=[[{cb_count,data['scale'],data['x'],data['y'],data['z']}]]),\n")
            cb_group += 1
        else:
            handleCreate(coin_model2_name)
            with open(coin_model2_name, "a") as fh:
                fh.write(f"CoinGroup(group={coin_group},map_id={map},name=\"\",konglist=[{data['kong']}], region=\"\", locations=[[{1,data['scale'],data['x'],data['y'],data['z']}]]),\n")
            coin_group += 1
    elif data["object_type"] == "actor":
        handleCreate(cb_actor_name)
        point_lst = []
        for pt_i, point in enumerate(data["path"]["points"]):
            point_lst.append([pt_i, point["x"], point["y"], point["z"]])
        with open(cb_actor_name, "a") as fh:
            fh.write(f"Balloon(id={balloon_id},map_id={map},name=\"\",speed={data['speed']},konglist=[{data['kong']}], region=\"\", points={point_lst}, path={data['path']['id']}),\n")
        balloon_id += 1


with open(dk64_rom, "rb") as fh:
    fh.seek(pointer_table_offset + (setup_table_index * 4))
    setup_table = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    fh.seek(pointer_table_offset + (path_table_index * 4))
    path_table = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    for map_index in range(221):
        balloon_id = 0
        cb_group = 0
        coin_group = 0
        # Base Data
        current_map_data = {"map": map_index, "objects": []}
        # Setup
        fh.seek(setup_table + (map_index * 4))
        setup_map_start = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        setup_map_end = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        setup_map_size = setup_map_end - setup_map_start
        fh.seek(setup_map_start)
        setup_map_compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
        fh.seek(setup_map_start)
        setup_raw = fh.read(setup_map_size)
        if setup_map_compressed:
            setup_raw = zlib.decompress(setup_raw, (15 + 32))
        # Paths
        fh.seek(path_table + (map_index * 4))
        path_map_start = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        path_map_end = pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        path_map_size = path_map_end - path_map_start
        fh.seek(path_map_start)
        path_map_compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
        fh.seek(path_map_start)
        path_raw = fh.read(path_map_size)
        if path_map_compressed:
            path_raw = zlib.decompress(path_raw, (15 + 32))
        # Search Paths
        path_list = []
        fh.seek(path_map_start)
        path_count = int.from_bytes(path_raw[0:2], "big")
        read_location = 2
        for path_index in range(path_count):
            path_id = int.from_bytes(path_raw[read_location + 0 : read_location + 2], "big")
            point_count = int.from_bytes(path_raw[read_location + 2 : read_location + 4], "big")
            unk_0 = int.from_bytes(path_raw[read_location + 4 : read_location + 6], "big")
            read_location += 6
            points = []
            for point_index in range(point_count):
                points.append(
                    {
                        "unk0": int.from_bytes(path_raw[read_location + 0 : read_location + 2], "big"),
                        "x": int.from_bytes(path_raw[read_location + 2 : read_location + 4], "big"),
                        "y": int.from_bytes(path_raw[read_location + 4 : read_location + 6], "big"),
                        "z": int.from_bytes(path_raw[read_location + 6 : read_location + 8], "big"),
                        "speed": int.from_bytes(path_raw[read_location + 8 : read_location + 9], "big"),
                        "unk1": int.from_bytes(path_raw[read_location + 9 : read_location + 10], "big"),
                    }
                )
                read_location += 10
            path_list.append({"id": path_id, "unk0": unk_0, "points": points.copy()})
        # if len(path_list) > 0 and map_index == 0x18:
        #     print(f"{hex(map_index)} ({path_count}): {path_list}")
        # Search Setup
        model2_count = int.from_bytes(setup_raw[0:4], "big")
        read_location = 4
        for model2_index in range(model2_count):
            model2_type = int.from_bytes(setup_raw[read_location + 0x28 : read_location + 0x2A], "big")
            is_good_type = False
            model2_name = ""
            kong_name = ""
            for m2_t in model2_types:
                if m2_t["type"] == model2_type:
                    is_good_type = True
                    model2_name = m2_t["name"]
                    kong_name = m2_t["kong"]
            if is_good_type:
                model2_x = intf_to_float(int.from_bytes(setup_raw[read_location + 0 : read_location + 4], "big"))
                model2_y = intf_to_float(int.from_bytes(setup_raw[read_location + 4 : read_location + 8], "big"))
                model2_z = intf_to_float(int.from_bytes(setup_raw[read_location + 8 : read_location + 12], "big"))
                model2_scale = intf_to_float(int.from_bytes(setup_raw[read_location + 12 : read_location + 16], "big"))
                data = {"name": model2_name, "type": hex(model2_type), "x": model2_x, "y": model2_y, "z": model2_z, "scale": model2_scale, "kong": kong_name, "object_type": "model_two"}
                current_map_data["objects"].append(data)
                dumpData(data, map_index)
            read_location += 0x30
        mystery_count = int.from_bytes(setup_raw[read_location + 0 : read_location + 4], "big")
        read_location += 4
        for mystery_index in range(mystery_count):
            read_location += 0x24
        actor_count = int.from_bytes(setup_raw[read_location + 0 : read_location + 4], "big")
        read_location += 4
        for actor_index in range(actor_count):
            actor_type = int.from_bytes(setup_raw[read_location + 0x32 : read_location + 0x34], "big") + 0x10
            is_good_type = False
            actor_name = ""
            kong_name = ""
            for ac_t in actor_types:
                if ac_t["type"] == actor_type:
                    is_good_type = True
                    actor_name = ac_t["name"]
                    kong_name = ac_t["kong"]

            if is_good_type:
                if map_index == 0x18:
                    with open(f"test{actor_index}.bin", "wb") as fg:
                        fg.write(setup_raw[read_location + 0 : read_location + 0x38])
                actor_x = intf_to_float(int.from_bytes(setup_raw[read_location + 0 : read_location + 4], "big"))
                actor_y = intf_to_float(int.from_bytes(setup_raw[read_location + 4 : read_location + 8], "big"))
                actor_z = intf_to_float(int.from_bytes(setup_raw[read_location + 8 : read_location + 12], "big"))
                actor_speed = int.from_bytes(setup_raw[read_location + 0x16 : read_location + 0x18], "big")
                actor_path = int.from_bytes(setup_raw[read_location + 0x12 : read_location + 0x14], "big")
                found_path = {}
                for path in path_list:
                    if path["id"] == actor_path:
                        found_path = path
                prev_len = len(current_map_data["objects"])
                data = {"name": actor_name, "type": hex(actor_type), "x": actor_x, "y": actor_y, "z": actor_z, "speed": actor_speed, "path": found_path, "kong": kong_name, "object_type": "actor"}
                current_map_data["objects"].append(data)
                dumpData(data, map_index)
            read_location += 0x38
        if len(current_map_data["objects"]) > 0:
            map_data.append(current_map_data)
with open("cb_coin_data.json", "w") as fh:
    fh.write(json.dumps(map_data, indent=4))
print("Dumped vanilla data")
