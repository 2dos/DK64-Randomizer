"""Get move sign data."""
from BuildLib import float_to_hex

sign_data = [
    {
        "map_index": 7,
        "signs": [
            {"sign_type": "cranky", "data": [1695.127, 280, 3998.528, 3]},
            {"sign_type": "funky", "data": [2074.149, 520, 2248.571, 119]},
            {"sign_type": "snide", "data": [2174.763, 680, 2581.554, 288]},
        ],
    },
    {
        "map_index": 0x26,
        "signs": [
            {"sign_type": "candy", "data": [2364.392, 120.5, 414.73, 0]},
            {"sign_type": "cranky", "data": [2697.736, 120.5, 2538.648, 290]},
            {"sign_type": "funky", "data": [2888.978, 121.051, 4546.7, 77]},
            {"sign_type": "snide", "data": [4217.064, 120, 4468.096, 334]},
        ],
    },
    {
        "map_index": 0x1A,
        "signs": [
            {"sign_type": "candy", "data": [192.108, 225.5, 567.249, 38]},
            {"sign_type": "funky", "data": [1426.279, 1131.833, 468.852, 315]},
            {"sign_type": "cranky", "data": [202.208, 225.5, 902.929, 335]},
            {"sign_type": "snide", "data": [1753.705, 826, 2074.416, 34]},
        ],
    },
    {
        "map_index": 0x1E,
        "signs": [
            {"sign_type": "cranky", "data": [3288.249, 1790, 2370.118, 196]},
            {"sign_type": "candy", "data": [2816.421, 1564.253, 553.305, 82]},
            {"sign_type": "funky", "data": [3676.859, 1560.177, 1235.449, 337]},
            {"sign_type": "snide", "data": [2091.915, 1610, 4726.344, 307]},
        ],
    },
    {
        "map_index": 0x30,
        "signs": [
            {"sign_type": "cranky", "data": [1005.894, 247, 263.491, 164]},
            {"sign_type": "funky", "data": [3271.472, 178.69, 93.169, 264]},
            {"sign_type": "snide", "data": [3090.001, 267.011, 3588.082, 194]},
        ],
    },
    {
        "map_index": 0x48,
        "signs": [
            {"sign_type": "cranky", "data": [1127.643, 281.527, 1574.504, 225]},
            {"sign_type": "funky", "data": [2777.721, 280, 1340.63, 86]},
            {"sign_type": "candy", "data": [3285.967, 112.833, 2187.781, 214]},
            {"sign_type": "snide", "data": [1210.936, 64.5, 411.259, 110]},
        ],
    },
    {"map_index": 0x57, "signs": [{"sign_type": "cranky", "data": [235.221, 1135.469, 1412.605, 278]}, {"sign_type": "snide", "data": [784.377, 1794.167, 1362.74, 180]}]},
    {"map_index": 0xB7, "signs": [{"sign_type": "funky", "data": [1456.806, 200, 246.614, 274]}]},
    {"map_index": 0x97, "signs": [{"sign_type": "candy", "data": [1191.144, 300, 2142.678, 269]}]},
    {"map_index": 0xB0, "signs": [{"sign_type": "cranky", "data": [602.935, 75, 1870.478, 309]}]},
    {"map_index": 0xC3, "signs": [{"sign_type": "snide", "data": [449.519, 0, 468.524, 268]}]},
]


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
                id = 0x100
                a_offset = 0
                if sign["sign_type"] == "cranky":
                    id = 0x100
                    a_offset = 180
                elif sign["sign_type"] == "funky":
                    id = 0x101
                    a_offset = 90
                elif sign["sign_type"] == "candy":
                    id = 0x102
                    a_offset = 0
                elif sign["sign_type"] == "snide":
                    id = 0x103
                    a_offset = 270
                sign_arr.append(
                    {
                        "base_byte_stream": base_stream,
                        "type": 70 - 16,
                        "x": convertCoord(sign["data"][0]),
                        "y": convertCoord(sign["data"][1]),
                        "z": convertCoord(sign["data"][2]),
                        "rx": 0,
                        "ry": convertAngle(sign["data"][3] + a_offset) % 4096,
                        "rz": 0,
                        "scale": int(float_to_hex(0.25), 16),
                        "id": id,
                    }
                )
    return sign_arr
