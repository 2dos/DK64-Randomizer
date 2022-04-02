"""Get move sign data."""
import struct

sign_data = [
    {"map_index": 7, "signs": [{"sign_type": "cranky", "data": [1693.203, 280.964, 3934.433, 183.867]}, {"sign_type": "funky", "data": [2048.232, 522.388, 2195.41, 207.861]}]},
    {
        "map_index": 0x26,
        "signs": [
            {"sign_type": "candy", "data": [2364.324, 121.509, 463.447, 358.418]},
            {"sign_type": "cranky", "data": [2750.299, 124.339, 2522.297, 110.654]},
            {"sign_type": "funky", "data": [2902.485, 123.604, 4490.055, 163.125]},
        ],
    },
    {
        "map_index": 0x1A,
        "signs": [
            {"sign_type": "candy", "data": [219.784, 225.851, 604.309, 37.002]},
            {"sign_type": "funky", "data": [1471.488, 1132.888, 516.591, 43.066]},
            {"sign_type": "cranky", "data": [229.027, 228.203, 850.685, 147.832]},
        ],
    },
    {
        "map_index": 0x1E,
        "signs": [
            {"sign_type": "cranky", "data": [3301.647, 1792.776, 2427.058, 16.348]},
            {"sign_type": "candy", "data": [2877.897, 1563.685, 560.159, 71.191]},
            {"sign_type": "funky", "data": [3742.295, 1568.709, 1268.402, 64.863]},
        ],
    },
    {"map_index": 0x30, "signs": [{"sign_type": "cranky", "data": [984.411, 251.25, 332.849, 342.422]}, {"sign_type": "funky", "data": [3261.958, 181.03, 163.222, 353.232]}]},
    {
        "map_index": 0x48,
        "signs": [
            {"sign_type": "cranky", "data": [1172.329, 282.911, 1618.7, 37.793]},
            {"sign_type": "funky", "data": [2780.684, 283.12, 1283.243, 179.561]},
            {"sign_type": "candy", "data": [3248.478, 112.833, 2131.77, 208.916]},
        ],
    },
    {
        "map_index": 0x57,
        "signs": [
            {"sign_type": "cranky", "data": [292.081, 1138.622, 1405.777, 95.625]},
        ],
    },
    {
        "map_index": 0xB7,
        "signs": [
            {"sign_type": "funky", "data": [1461.363, 203.18, 304.011, 359.561]},
        ],
    },
    {"map_index": 0x97, "signs": [{"sign_type": "candy", "data": [1115.306, 326.145, 2139.784, 271.67]}]},
    {"map_index": 0xB0, "signs": [{"sign_type": "cranky", "data": [651.318, 77.255, 1834.692, 126.914]}]},
]


def int_to_float(val):
    """Convert a hex int to a float."""
    return struct.unpack("!f", bytes.fromhex(hex(val).split("0x")[1]))[0]


def float_to_hex(f):
    """Convert float to hex."""
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def convertCoord(f):
    """Convert a cord to an int."""
    return int(float_to_hex(f), 16)


def getMoveSignData(map_index, base_stream):
    """Get current move sign data."""
    sign_arr = []
    for map_data in sign_data:
        if map_data["map_index"] == map_index:
            for sign in map_data["signs"]:
                sign_base = 0x230
                sign_id = sign_base + 3
                if sign["sign_type"] == "cranky":
                    sign_id = sign_base + 0
                elif sign["sign_type"] == "funky":
                    sign_id = sign_base + 1
                elif sign["sign_type"] == "candy":
                    sign_id = sign_base + 2
                sign_arr.append(
                    {
                        "base_byte_stream": base_stream,
                        "type": 0x2AB,
                        "x": convertCoord(sign["data"][0]),
                        "y": convertCoord(sign["data"][1]),
                        "z": convertCoord(sign["data"][2]),
                        "rx": 0,
                        "ry": convertCoord(sign["data"][3]),
                        "rz": 0,
                        "id": sign_id,
                        "scale": int(float_to_hex(0.5), 16),
                    }
                )
    return sign_arr
