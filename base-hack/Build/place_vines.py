"""Generate vine series with better behavior."""

import math
from BuildEnums import Maps
from BuildClasses import VineSequence, Coordinate

vine_series = [
    VineSequence(Maps.Japes, Coordinate(1786.297, 600.5, 2100.627), Coordinate(1471.689, 600.5, 2100.627), [9, 10, 11]),
    VineSequence(Maps.Japes, Coordinate(915.847, 573.5, 1910.881), Coordinate(804.597, 610, 2241.639), [24, 25, 26]),
    VineSequence(Maps.TrainingGrounds, Coordinate(1629.996, 320.167, 1190.991), Coordinate(2016.762, 300, 1176.268), [0, 1, 2]),
    VineSequence(Maps.Isles, Coordinate(2690.722, 986, 1107.726), Coordinate(3228.038, 986, 1169.691), [1, 2, 3, 4]),
    VineSequence(Maps.Fungi, Coordinate(2056.362, 490.081, 2366.29), Coordinate(2153.628, 471.435, 2662.234), [31, 33, 34]),
    VineSequence(Maps.Fungi, Coordinate(2519.823, 470.453, 2780.688), Coordinate(2270.045, 440, 3045.1), [29, 30, 32]),
    VineSequence(Maps.Galleon, Coordinate(3074.465, 1964, 3409.648), Coordinate(3071.741, 1962.337, 3060.115), [8, 9, 10]),
    VineSequence(Maps.Aztec, Coordinate(2491.337, 340.591, 1072.511), Coordinate(2216.48, 379.958, 1453.899), [19, 20, 22, 23]),
    VineSequence(Maps.Aztec, Coordinate(3113.786, 391.4, 4220.393), Coordinate(3380.865, 392.297, 4262.602), [14, 15, 16]),
    VineSequence(Maps.FungiGiantMushroom, Coordinate(304.701, 1071.474, 518.836), Coordinate(710.539, 1071.5, 510), [3, 4, 5, 6]),
]


def generateVineSeries(map_id: Maps) -> dict:
    """Generate vine placements based on point differences."""
    data = {"change": [], "add": []}
    max_dist = 120
    new_id = 0xF0
    for series in vine_series:
        if series.map_index == map_id:
            chain_delta = series.getSequenceDistance()
            vine_points = [series.point_start]
            point_count = max(math.ceil(chain_delta / max_dist), len(series.ids) - 1)
            for point_index in range(point_count):
                vine_points.append(series.getSequencePoint(point_index, point_count))
            for pt_i, pt in enumerate(vine_points):
                if pt_i >= len(series.ids):
                    data["add"].append({"x": pt.x, "y": pt.y, "z": pt.z, "id_base": series.ids[0], "id": new_id})
                    new_id += 1
                else:
                    data["change"].append({"x": pt.x, "y": pt.y, "z": pt.z, "id": series.ids[pt_i]})
    return data
