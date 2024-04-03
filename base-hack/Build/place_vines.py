"""Generate vine series with better behavior."""

import math

vine_series = [
    {"map": 0x7, "points": [{"x": 1786.297, "y": 600.5, "z": 2100.627}, {"x": 1471.689, "y": 600.5, "z": 2100.627}], "ids": [9, 10, 11]},
    {"map": 0x7, "points": [{"x": 915.847, "y": 573.5, "z": 1910.881}, {"x": 804.597, "y": 610, "z": 2241.639}], "ids": [24, 25, 26]},
    {"map": 0xB0, "points": [{"x": 1629.996, "y": 320.167, "z": 1190.991}, {"x": 2016.762, "y": 300, "z": 1176.268}], "ids": [0, 1, 2]},
    {"map": 0x22, "points": [{"x": 2690.722, "y": 986, "z": 1107.726}, {"x": 3228.038, "y": 986, "z": 1169.691}], "ids": [1, 2, 3, 4]},
    {"map": 0x30, "points": [{"x": 2056.362, "y": 490.081, "z": 2366.29}, {"x": 2153.628, "y": 471.435, "z": 2662.234}], "ids": [31, 33, 34]},
    {"map": 0x30, "points": [{"x": 2519.823, "y": 470.453, "z": 2780.688}, {"x": 2270.045, "y": 440, "z": 3045.1}], "ids": [29, 30, 32]},
    {"map": 0x1E, "points": [{"x": 3074.465, "y": 1964, "z": 3409.648}, {"x": 3071.741, "y": 1962.337, "z": 3060.115}], "ids": [8, 9, 10]},
    {"map": 0x26, "points": [{"x": 2491.337, "y": 340.591, "z": 1072.511}, {"x": 2216.48, "y": 379.958, "z": 1453.899}], "ids": [19, 20, 22, 23]},
    {"map": 0x26, "points": [{"x": 3113.786, "y": 391.4, "z": 4220.393}, {"x": 3380.865, "y": 392.297, "z": 4262.602}], "ids": [14, 15, 16]},
    {"map": 0x40, "points": [{"x": 304.701, "y": 1071.474, "z": 518.836}, {"x": 710.539, "y": 1071.5, "z": 510}], "ids": [3, 4, 5, 6]},
]


def generateVineSeries(map_id: int) -> dict:
    """Generate vine placements based on point differences."""
    data = {"change": [], "add": []}
    max_dist = 120
    new_id = 0xF0
    for series in vine_series:
        if series["map"] == map_id:
            coords = ["x", "y", "z"]
            delta = {}
            delta_total = 0
            for coord in coords:
                delta[coord] = series["points"][1][coord] - series["points"][0][coord]
                delta_total += delta[coord] * delta[coord]
            chain_delta = math.sqrt(delta_total)
            vine_points = [{"x": series["points"][0]["x"], "y": series["points"][0]["y"], "z": series["points"][0]["z"]}]
            point_count = max(math.ceil(chain_delta / max_dist), len(series["ids"]) - 1)
            for point_index in range(point_count):
                point = {}
                for coord in coords:
                    point[coord] = series["points"][0][coord] + (((point_index + 1) / point_count) * delta[coord])
                vine_points.append(point)
            for pt_i, pt in enumerate(vine_points):
                if pt_i >= len(series["ids"]):
                    data["add"].append({"x": pt["x"], "y": pt["y"], "z": pt["z"], "id_base": series["ids"][0], "id": new_id})
                    new_id += 1
                else:
                    data["change"].append({"x": pt["x"], "y": pt["y"], "z": pt["z"], "id": series["ids"][pt_i]})
    return data
