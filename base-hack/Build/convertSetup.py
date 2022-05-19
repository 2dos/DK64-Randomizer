"""Convert file setup."""
import os
import shutil
import struct

from getMoveSignLocations import getMoveSignData


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


def int_to_float(val):
    """Convert a hex int to a float."""
    return struct.unpack("!f", bytes.fromhex(hex(val).split("0x")[1]))[0]


def float_to_hex(f):
    """Convert float to hex."""
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


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
        for x in range(model2_count):
            byte_stream = byte_read[read_location : read_location + 0x30]
            _type = int.from_bytes(byte_read[read_location + 0x28 : read_location + 0x2A], "big")
            _id = int.from_bytes(byte_read[read_location + 0x2A : read_location + 0x2C], "big")
            if _type == 0x2AC and map_index != 0x2A:
                base_stream = byte_stream
                _x = int.from_bytes(byte_read[read_location + 0 : read_location + 4], "big")
                _y = int.from_bytes(byte_read[read_location + 4 : read_location + 8], "big")
                _yf = int_to_float(_y) - 30
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
                added_model2.append(
                    {
                        "base_byte_stream": byte_stream,
                        "type": 0x2AB,
                        "x": _x,
                        "y": _y,
                        "z": _z,
                        "rx": 0,
                        "ry": _ay,
                        "rz": 0,
                        "id": model2_index,
                        "scale": int(float_to_hex(0.35), 16),
                    }
                )
                model2_index += 1
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
            data = {
                "stream": byte_stream,
                "type": _type,
            }
            model2.append(data)
            read_location += 0x30
        shop_signs = getMoveSignData(map_index, base_stream)
        # if len(shop_signs) != 0:
        #     print(shop_signs)
        for sign in shop_signs:
            added_actor.append(sign)
        mystery_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(mystery_count):
            byte_stream = byte_read[read_location : read_location + 0x24]
            data = {
                "stream": byte_stream,
            }
            mystery.append(data)
            read_location += 0x24
        actor_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(actor_count):
            byte_stream = byte_read[read_location : read_location + 0x38]
            data = {"stream": byte_stream}
            actor.append(data)
            read_location += 0x38
        for x in added_actor:
            byte_stream_arr = []
            for y in range(0x38):
                byte_stream_arr.append(0)
            writedatatoarr(byte_stream_arr, x["x"], 4, 0x0)
            writedatatoarr(byte_stream_arr, x["y"], 4, 0x4)
            writedatatoarr(byte_stream_arr, x["z"], 4, 0x8)
            writedatatoarr(byte_stream_arr, x["scale"], 4, 0xC)
            writedatatoarr(byte_stream_arr, x["ry"], 2, 0x30)
            writedatatoarr(byte_stream_arr, x["type"], 2, 0x32)
            writedatatoarr(byte_stream_arr, x["id"], 2, 0x34)
            actor.append({"stream": byte_stream_arr})
        for x in added_model2:
            byte_stream_arr = []
            for y in range(0x10):
                byte_stream_arr.append(0)
            new_data_1 = [
                0xFF,
                0xFB,
                0x00,
                0x00,
                0x15,
                0x00,
                0x00,
                0x00,
                0x40,
                0xC0,
                0x00,
                0x00,
                0x43,
                0xB3,
                0x00,
                0x00,
            ]
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
