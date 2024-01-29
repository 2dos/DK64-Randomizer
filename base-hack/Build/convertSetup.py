"""Convert file setup."""

import os
import shutil

from BuildLib import float_to_hex, intf_to_float
from getMoveSignLocations import getMoveSignData
from place_vines import generateVineSeries

BUTTON_DIST_NORMAL = 20
CAVES_ITEM_HEIGHT = 20


def convertSetup(file_name):
    """Convert file type setup.

    Args:
        file_name (str): File name to convert.
    """
    with open(file_name, "rb") as source:
        with open("_" + file_name, "wb") as modified:
            modified.write(source.read())
    map_index = int(file_name.split("setup")[1].split(".bin")[0])
    modify("_" + file_name, map_index)
    if os.path.exists(file_name):
        os.remove(file_name)
    shutil.copyfile("_" + file_name.replace(".bin", "_.bin"), file_name)
    if os.path.exists("_" + file_name):
        os.remove("_" + file_name)
    if os.path.exists("_" + file_name.replace(".bin", "_.bin")):
        os.remove("_" + file_name.replace(".bin", "_.bin"))


def writedatatoarr(stream, value, size, location):
    """Write data to an array."""
    for x in range(size):
        stream[location + x] = bytearray(value.to_bytes(size, "big"))[x]
    return stream


base_stream = 0


def modify(file_name, map_index):
    """Modify the file to be updated.

    Args:
        file_name (str): File name.
        map_index (int): Map index.
    """
    global base_stream
    with open(file_name, "r+b") as fh:
        byte_read = fh.read()
        model2_count = int.from_bytes(byte_read[:4], "big")
        read_location = 4
        model2 = []
        mystery = []
        actor = []
        added_model2 = []
        added_actor = []
        model2_index = 0x220
        added_factory_barracade = False
        added_caves_tns = False
        added_helm_faces = False
        added_5di_strongkong = False
        added_library_strongkong = False
        for x in range(model2_count):
            byte_stream = byte_read[read_location : read_location + 0x30]
            _type = int.from_bytes(byte_read[read_location + 0x28 : read_location + 0x2A], "big")
            _id = int.from_bytes(byte_read[read_location + 0x2A : read_location + 0x2C], "big")
            if _type == 0x2AC and map_index != 0x2A:
                if map_index == 0x48 and not added_caves_tns and _id == 0x26:
                    # New T&S Portal
                    for k in range(2):
                        # First add T&S
                        # Second add display
                        portal_y = 50.167
                        added_model2.append(
                            {
                                "base_byte_stream": byte_stream,
                                "type": [0x2AC, 0x2AB][k],
                                "x": int(float_to_hex(120.997), 16),
                                "y": [int(float_to_hex(portal_y), 16), int(float_to_hex(portal_y - 30), 16)][k],
                                "z": int(float_to_hex(1182.974), 16),
                                "rx": 0,
                                "ry": int(float_to_hex(75.146), 16),
                                "rz": 0,
                                "id": [0x170, model2_index][k],
                                "scale": [int(float_to_hex(1), 16), int(float_to_hex(0.35), 16)][k],
                            }
                        )
                    model2_index += 1
                    added_caves_tns = True
                base_stream = byte_stream
                _x = int.from_bytes(byte_read[read_location + 0 : read_location + 4], "big")
                _y = int.from_bytes(byte_read[read_location + 4 : read_location + 8], "big")
                _yf = intf_to_float(_y) - 30
                _y = int(float_to_hex(_yf), 16)
                _z = int.from_bytes(byte_read[read_location + 8 : read_location + 12], "big")
                _ax = int.from_bytes(byte_read[read_location + 0x18 : read_location + 0x1C], "big")
                _ay = int.from_bytes(byte_read[read_location + 0x1C : read_location + 0x20], "big")
                _az = int.from_bytes(byte_read[read_location + 0x20 : read_location + 0x24], "big")
                _id = int.from_bytes(byte_read[read_location + 0x2A : read_location + 0x2C], "big")
                if map_index == 7:
                    if model2_index == 0x220:
                        _x = int(float_to_hex(805.6618), 16)
                        _z = int(float_to_hex(2226.797), 16)
                added_model2.append({"base_byte_stream": byte_stream, "type": 0x2AB, "x": _x, "y": _y, "z": _z, "rx": 0, "ry": _ay, "rz": 0, "id": model2_index, "scale": int(float_to_hex(0.35), 16)})
                model2_index += 1
            if map_index == 0x22 and not added_factory_barracade and _id == 0x6:
                added_factory_barracade = True
                added_model2.append(
                    {
                        "base_byte_stream": byte_stream,
                        "type": 132,
                        "x": int(float_to_hex(2457.471), 16),
                        "y": int(float_to_hex(1280), 16),
                        "z": int(float_to_hex(3458.604), 16),
                        "rx": 0,
                        "ry": int(float_to_hex(166), 16),
                        "rz": 0,
                        "id": 0x100,
                        "scale": int(float_to_hex(1.18), 16),
                    }
                )
            if (map_index == 7 and _id == 0x1A) or (map_index == 0xB0 and _id == 0x39):
                # Type 0x94
                _type = 0xCE
                repl_byte = b""
                for x in range(0x29):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += _type.to_bytes(1, "big")
                for x in range(0x30 - 0x2A):
                    repl_byte += byte_stream[x + 0x2A].to_bytes(1, "big")
                byte_stream = repl_byte
            elif map_index == 7 and _id == 0x52:
                # Mountain GB
                repl_byte = b""
                coords = [1648.095, 990, 2431.953]
                for c in coords:
                    repl_byte += int(float_to_hex(c), 16).to_bytes(4, "big")
                for x in range(0x30 - 0xC):
                    repl_byte += byte_stream[x + 0xC].to_bytes(1, "big")
                byte_stream = repl_byte
            elif map_index == 7 and _id == 0x68:
                # Stump GB
                repl_byte = b""
                new_stump_scale = 0.15
                for x in range(0xC):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += int(float_to_hex(new_stump_scale), 16).to_bytes(4, "big")
                for x in range(0x30 - 0x10):
                    repl_byte += byte_stream[x + 0x10].to_bytes(1, "big")
                byte_stream = repl_byte
            elif (map_index == 0x1A and _id == 0x13E) or (map_index == 5 and _id == 2):
                # Nintendo/Rareware Coin
                repl_byte = b""
                scale = int(float_to_hex(0.2), 16)
                for x in range(0xC):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += scale.to_bytes(4, "big")
                for x in range(0x30 - 0x10):
                    repl_byte += byte_stream[x + 0x10].to_bytes(1, "big")
                byte_stream = repl_byte
            if map_index == 0x1A and _id == 0x24:
                repl_byte = b""
                coord = [0, 0, 0]
                # raw_coords = [1418,725,6.5,522.716]
                raw_coords = [1455.853, 6.5, 522.716]
                coord[0] = int(float_to_hex(raw_coords[0]), 16)
                coord[1] = int(float_to_hex(raw_coords[1]), 16)
                coord[2] = int(float_to_hex(raw_coords[2]), 16)
                _ay = int(float_to_hex(0), 16)
                for x in coord:
                    repl_byte += x.to_bytes(4, "big")
                for x in range(0x1C - 0xC):
                    repl_byte += byte_stream[x + 0xC].to_bytes(1, "big")
                repl_byte += _ay.to_bytes(4, "big")
                for x in range(0x30 - 0x20):
                    repl_byte += byte_stream[x + 0x20].to_bytes(1, "big")
                byte_stream = repl_byte
            if map_index == 0x1A and _id >= 0x67 and _id <= 0x76:
                # Number Game Switches
                repl_byte = b""
                switch_index = _id - 0x67
                switch_y = switch_index % 4
                switch_x = int(switch_index / 4)
                tl_x = 2606.114
                tl_z = 1767.899
                switch_d = 37.7
                coord = [0, 0, 0]
                coord[0] = int(float_to_hex(tl_x + (switch_d * switch_x)), 16)
                coord[1] = int(float_to_hex(1002), 16)
                coord[2] = int(float_to_hex(tl_z + (switch_d * switch_y)), 16)
                for x in coord:
                    repl_byte += x.to_bytes(4, "big")
                for x in range(0x1C - 0xC):
                    repl_byte += byte_stream[x + 0xC].to_bytes(1, "big")
                repl_byte += _ay.to_bytes(4, "big")
                for x in range(0x30 - 0x20):
                    repl_byte += byte_stream[x + 0x20].to_bytes(1, "big")
                byte_stream = repl_byte
                _ay = int(float_to_hex(180), 16)
            if map_index == 0x48:
                if _id == 0x57 or _id == 0xCF:
                    # Move W3 and Tiny bunch near 5DI
                    repl_byte = b""
                    loc_x = 176.505
                    loc_z = 1089.408
                    repl_byte += int(float_to_hex(loc_x), 16).to_bytes(4, "big")
                    for x in range(4):
                        repl_byte += byte_stream[x + 4].to_bytes(1, "big")
                    repl_byte += int(float_to_hex(loc_z), 16).to_bytes(4, "big")
                    for x in range(0x30 - 0xC):
                        repl_byte += byte_stream[x + 0xC].to_bytes(1, "big")
                    byte_stream = repl_byte
            if map_index == 0xCD:
                # Standardize lanky phase buttons
                buttons = (0xE, 0xF, 0x10, 0x11)
                platforms = (0xD, 0x13, 0x14, 0x12)
                button_loc = ((780, 419.629 + BUTTON_DIST_NORMAL), (1135.232 - BUTTON_DIST_NORMAL, 780), (780, 1116.334 - BUTTON_DIST_NORMAL), (438.904 + BUTTON_DIST_NORMAL, 780))
                platform_loc = ((778.365, 396.901 + BUTTON_DIST_NORMAL), (1158.427 - BUTTON_DIST_NORMAL, 778.632), (780.283, 1138.851 - BUTTON_DIST_NORMAL), (416.092 + BUTTON_DIST_NORMAL, 778.456))
                if _id >= 0xD and _id <= 0x14:
                    x = 0
                    z = 0
                    if _id in buttons:
                        index = buttons.index(_id)
                        x = button_loc[index][0]
                        z = button_loc[index][1]
                    else:
                        index = platforms.index(_id)
                        x = platform_loc[index][0]
                        z = platform_loc[index][1]
                    repl_byte = b""
                    repl_byte += int(float_to_hex(x), 16).to_bytes(4, "big")
                    for x in range(4):
                        repl_byte += byte_stream[x + 4].to_bytes(1, "big")
                    repl_byte += int(float_to_hex(z), 16).to_bytes(4, "big")
                    for x in range(0x30 - 0xC):
                        repl_byte += byte_stream[x + 0xC].to_bytes(1, "big")
                    byte_stream = repl_byte
            if map_index == 0x7 and _id == 0xC9:
                repl_byte = b""
                new_y = int(float_to_hex(400), 16)
                for x in range(0x4):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += new_y.to_bytes(4, "big")
                for x in range(0x30 - 0x8):
                    repl_byte += byte_stream[x + 0x8].to_bytes(1, "big")
                byte_stream = repl_byte
            elif map_index == 0x48:
                # Underwater Items, Caves
                ranges = (
                    list(range(0xA5, 0xAF)),  # Lanky underwater CBs
                    list(range(0xC0, 0xCA)),  # Tiny underwater CBs
                    list(range(0x73, 0x76)),  # Chunky underwater coins
                    list(range(0xD8, 0xDB)),  # Tiny underwater coins
                    list(range(0xB7, 0xBA)),  # Lanky underwater coins (1)
                    list(range(0xBD, 0xC0)),  # Lanky underwater coins (2)
                )
                in_range = False
                for selection in ranges:
                    if _id in selection:
                        in_range = True
                if in_range:
                    repl_byte = b""
                    new_y = int(float_to_hex(CAVES_ITEM_HEIGHT), 16)
                    for x in range(0x4):
                        repl_byte += byte_stream[x].to_bytes(1, "big")
                    repl_byte += new_y.to_bytes(4, "big")
                    for x in range(0x30 - 0x8):
                        repl_byte += byte_stream[x + 0x8].to_bytes(1, "big")
                    byte_stream = repl_byte
            elif map_index == 0x1A and _id == 0x2C:
                # Diddy Prod GB
                repl_byte = b""
                new_y = int(float_to_hex(715), 16)
                for x in range(0x4):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += new_y.to_bytes(4, "big")
                for x in range(0x30 - 0x8):
                    repl_byte += byte_stream[x + 0x8].to_bytes(1, "big")
                byte_stream = repl_byte
            elif map_index == 0x1A and _id in [0x1CD, 0x1CE, 0x1CF]:
                # Diddy Storage, Shelved Coins
                repl_byte = b""
                new_y = int(float_to_hex(178.5), 16)
                for x in range(0x4):
                    repl_byte += byte_stream[x].to_bytes(1, "big")
                repl_byte += new_y.to_bytes(4, "big")
                for x in range(0x30 - 0x8):
                    repl_byte += byte_stream[x + 0x8].to_bytes(1, "big")
                byte_stream = repl_byte
            data = {"stream": byte_stream, "type": _type}
            model2.append(data)
            read_location += 0x30
        shop_signs = getMoveSignData(map_index, base_stream)
        vine_data = generateVineSeries(map_index)
        # if len(shop_signs) != 0:
        #     print(shop_signs)
        for sign in shop_signs:
            added_actor.append(sign)
        mystery_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(mystery_count):
            byte_stream = byte_read[read_location : read_location + 0x24]
            data = {"stream": byte_stream}
            mystery.append(data)
            read_location += 0x24
        actor_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(actor_count):
            byte_stream = byte_read[read_location : read_location + 0x38]
            obj_id = int.from_bytes(byte_read[read_location + 0x34 : read_location + 0x36], "big")
            if map_index == 0x1A and obj_id == 13:
                temp = []
                for y in range(0x38):
                    temp.append(byte_stream[y])
                byte_stream = temp.copy()
                new_x = 1237.001
                new_y = 175
                new_z = 840.569
                writedatatoarr(byte_stream, int(float_to_hex(new_x), 16), 4, 0x0)
                writedatatoarr(byte_stream, int(float_to_hex(new_y), 16), 4, 0x4)
                writedatatoarr(byte_stream, int(float_to_hex(new_z), 16), 4, 0x8)
            elif map_index == 0x1E and obj_id == 36:
                # tag barrel near mermaid in galleon
                temp = []
                for y in range(0x38):
                    temp.append(byte_stream[y])
                byte_stream = temp.copy()
                new_y = 383.8333
                writedatatoarr(byte_stream, int(float_to_hex(new_y), 16), 4, 0x4)
            elif map_index == 0x1E and obj_id in (23, 25):
                temp = []
                for y in range(0x38):
                    temp.append(byte_stream[y])
                byte_stream = temp.copy()
                new_x = 1296
                new_y = 1600
                new_z = 2028
                if obj_id == 23:
                    writedatatoarr(byte_stream, int(float_to_hex(new_x), 16), 4, 0x0)
                    writedatatoarr(byte_stream, int(float_to_hex(new_z), 16), 4, 0x8)
                writedatatoarr(byte_stream, int(float_to_hex(new_y), 16), 4, 0x4)
            elif map_index == 0x11 and not added_helm_faces:
                face_z = 5423.538
                face_hi = 160
                face_lo = 104.5
                face_coords = [[575.763, face_hi], [494.518, face_hi], [606.161, face_lo], [534.567, face_lo], [463.642, face_lo]]
                for face_index, face in enumerate(face_coords):
                    added_actor.append(
                        {
                            "base_byte_stream": byte_stream,
                            "x": int(float_to_hex(face[0]), 16),
                            "y": int(float_to_hex(face[1]), 16),
                            "z": int(float_to_hex(face_z), 16),
                            "id": 0x100 + face_index,
                            "type": 70 - 16,
                            "rx": 0,
                            "ry": 0,
                            "rz": 0,
                            "scale": int(float_to_hex(0.35), 16),
                        }
                    )
                added_helm_faces = True
            elif map_index == 0x56 and not added_5di_strongkong:
                added_actor.append(
                    {
                        "base_byte_stream": byte_stream,
                        "x": int(float_to_hex(118.011), 16),
                        "y": int(float_to_hex(20), 16),
                        "z": int(float_to_hex(462.749), 16),
                        "id": 0x20,
                        "type": 0x39 - 16,
                        "rx": 0,
                        "ry": 1024,
                        "rz": 0,
                        "scale": int(float_to_hex(1), 16),
                    }
                )
                added_5di_strongkong = True
            elif map_index == 0x72 and not added_library_strongkong:
                added_actor.append(
                    {
                        "base_byte_stream": byte_stream,
                        "x": int(float_to_hex(2668), 16),
                        "y": int(float_to_hex(216), 16),
                        "z": int(float_to_hex(287), 16),
                        "id": 0x20,
                        "type": 0x39 - 16,
                        "rx": 0,
                        "ry": 1024,
                        "rz": 0,
                        "scale": int(float_to_hex(1), 16),
                    }
                )
                added_library_strongkong = True
            # Vine Memes
            if len(vine_data["add"]) > 0:
                for vine_add in vine_data["add"]:
                    if obj_id == vine_add["id_base"]:
                        added_actor.append(
                            {
                                "base_byte_stream": byte_stream,
                                "x": int(float_to_hex(vine_add["x"]), 16),
                                "y": int(float_to_hex(vine_add["y"]), 16),
                                "z": int(float_to_hex(vine_add["z"]), 16),
                                "id": vine_add["id"],
                                "use_byte_stream": True,
                            }
                        )
            if len(vine_data["change"]) > 0:
                for vine_change in vine_data["change"]:
                    if obj_id == vine_change["id"]:
                        temp = []
                        for y in range(0x38):
                            temp.append(byte_stream[y])
                        byte_stream = temp.copy()
                        writedatatoarr(byte_stream, int(float_to_hex(vine_change["x"]), 16), 4, 0x0)
                        writedatatoarr(byte_stream, int(float_to_hex(vine_change["y"]), 16), 4, 0x4)
                        writedatatoarr(byte_stream, int(float_to_hex(vine_change["z"]), 16), 4, 0x8)
            data = {"stream": byte_stream}
            actor.append(data)
            read_location += 0x38
        for x in added_actor:
            byte_stream_arr = []
            for y in range(0x38):
                if "use_byte_stream" in x and x["use_byte_stream"] and "base_byte_stream" in x:
                    byte_stream_arr.append(x["base_byte_stream"][y])
                else:
                    byte_stream_arr.append(0)
            if "x" in x:
                writedatatoarr(byte_stream_arr, x["x"], 4, 0x0)
            if "y" in x:
                writedatatoarr(byte_stream_arr, x["y"], 4, 0x4)
            if "z" in x:
                writedatatoarr(byte_stream_arr, x["z"], 4, 0x8)
            if "scale" in x:
                writedatatoarr(byte_stream_arr, x["scale"], 4, 0xC)
            if "ry" in x:
                writedatatoarr(byte_stream_arr, x["ry"], 2, 0x30)
            if "type" in x:
                writedatatoarr(byte_stream_arr, x["type"], 2, 0x32)
            if "id" in x:
                writedatatoarr(byte_stream_arr, x["id"], 2, 0x34)
            actor.append({"stream": byte_stream_arr})
        for x in added_model2:
            byte_stream_arr = []
            for y in range(0x10):
                byte_stream_arr.append(0)
            new_data_1 = [0xFF, 0xFB, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x40, 0xC0, 0x00, 0x00, 0x43, 0xB3, 0x00, 0x00]
            for y in new_data_1:
                byte_stream_arr.append(y)
            for y in range(0xC):
                byte_stream_arr.append(0)
            new_data_2 = [0x0, 0x1, 0x0, 0x0]
            for y in new_data_2:
                byte_stream_arr.append(y)
            # byte_stream_arr = []
            # for y in range(0x30):
            # 	byte_stream_arr.append(0)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["type"], 2, 0x28)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["id"], 2, 0x2A)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["scale"], 4, 0xC)

            byte_stream_arr = writedatatoarr(byte_stream_arr, x["x"], 4, 0x0)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["y"], 4, 0x4)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["z"], 4, 0x8)

            byte_stream_arr = writedatatoarr(byte_stream_arr, x["rx"], 4, 0x18)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["ry"], 4, 0x1C)
            byte_stream_arr = writedatatoarr(byte_stream_arr, x["rz"], 4, 0x20)

            model2.append({"stream": byte_stream_arr})
        with open(file_name.replace(".bin", "_.bin"), "wb") as fg:
            fg.write(len(model2).to_bytes(4, "big"))
            for x in model2:
                fg.write(bytearray(x["stream"]))
            fg.write(len(mystery).to_bytes(4, "big"))
            for x in mystery:
                fg.write(bytearray(x["stream"]))
            fg.write(len(actor).to_bytes(4, "big"))
            for x in actor:
                fg.write(bytearray(x["stream"]))
