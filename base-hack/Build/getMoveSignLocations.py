"""Get move sign data."""
import struct

sign_data = [
    {"map_index": 7, "signs": [{"sign_type": "cranky", "data": [1693.203, 280.964, 3934.433, 183.867, 1]}, {"sign_type": "funky", "data": [2048.232, 522.388, 2195.41, 207.861, 1]}]},
    {
        "map_index": 0x26,
        "signs": [
            {"sign_type": "candy", "data": [2365.486, 120, 494.248, 358.418, 1.12]},
            {"sign_type": "cranky", "data": [2755.299, 124.339, 2522.297, 110.654, 1]},
            {"sign_type": "funky", "data": [2902.485, 123.604, 4490.055, 163.125, 1]},
        ],
    },
    {
        "map_index": 0x1A,
        "signs": [
            {"sign_type": "candy", "data": [235.468, 225.5, 620.636, 37.002, 1]},
            {"sign_type": "funky", "data": [1471.488, 1132.888, 516.591, 43.066, 1]},
            {"sign_type": "cranky", "data": [229.027, 228.203, 850.685, 147.832, 1]},
        ],
    },
    {
        "map_index": 0x1E,
        "signs": [
            {"sign_type": "cranky", "data": [3301.647, 1792.776, 2427.058, 16.348, 1]},
            {"sign_type": "candy", "data": [2904.595, 1561.547, 564.17, 71.191, 1.28]},
            {"sign_type": "funky", "data": [3742.295, 1568.709, 1268.402, 64.863, 1.12]},
        ],
    },
    {"map_index": 0x30, "signs": [{"sign_type": "cranky", "data": [984.411, 251.25, 342.849, 342.42, 1.28]}, {"sign_type": "funky", "data": [3261.958, 181.03, 163.222, 353.232, 1.16]}]},
    {
        "map_index": 0x48,
        "signs": [
            {"sign_type": "cranky", "data": [1172.329, 282.911, 1618.7, 37.793, 1]},
            {"sign_type": "funky", "data": [2780.684, 283.12, 1280.243, 179.561, 1.04]},
            {"sign_type": "candy", "data": [3239.475, 112.833, 2120.751, 208.916, 1.26]},
        ],
    },
    {
        "map_index": 0x57,
        "signs": [
            {"sign_type": "cranky", "data": [294.081, 1138.622, 1405.777, 95.625, 1]},
        ],
    },
    {
        "map_index": 0xB7,
        "signs": [
            {"sign_type": "funky", "data": [1463.363, 203.18, 310.011, 359.561, 1.06]},
        ],
    },
    {"map_index": 0x97, "signs": [{"sign_type": "candy", "data": [1077.46, 300, 2140.457, 271.67, 1.7]}]},
    {"map_index": 0xB0, "signs": [{"sign_type": "cranky", "data": [651.318, 77.255, 1834.692, 126.914, 1]}]},
]


def int_to_float(val):
    """Convert a hex int to a float."""
    return struct.unpack("!f", bytes.fromhex(hex(val).split("0x")[1]))[0]


def float_to_hex(f):
    """Convert float to hex."""
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def convertCoord(f):
    """Convert a coord to an int."""
    return int(float_to_hex(f), 16)


def convertAngle(f):
    """Convert an angle to DK64 Angle system."""
    return int(((f / 360) * 4096))


def getMoveSignData(map_index, base_stream):
    """Get current move sign data."""
    sign_arr = []
    for map_data in sign_data:
        if map_data["map_index"] == map_index:
            for sign in map_data["signs"]:
                offset_mult = 40
                id = 0x100
                if sign["sign_type"] == "cranky":
                    offset_mult = 40
                    id = 0x100
                elif sign["sign_type"] == "funky":
                    offset_mult = 40
                    id = 0x101
                elif sign["sign_type"] == "candy":
                    offset_mult = 40
                    id = 0x102
                sign_arr.append(
                    {
                        "base_byte_stream": base_stream,
                        "type": 70 - 16,
                        "x": convertCoord(sign["data"][0]),
                        "y": convertCoord(sign["data"][1] + (offset_mult * sign["data"][4])),
                        "z": convertCoord(sign["data"][2]),
                        "rx": 0,
                        "ry": (convertAngle(sign["data"][3]) + 2048) % 4096,
                        "rz": 0,
                        "scale": int(float_to_hex(0.25), 16),
                        "id": id,
                    }
                )
    return sign_arr
