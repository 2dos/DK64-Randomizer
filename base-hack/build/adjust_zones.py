"""Adjust zones to lack of precision issues with DK64."""


class TriggerChange:
    """Class to store information regarding a trigger change."""

    def __init__(self, map: int, init_xyz: list, trigger_type: int, new_xyz: list, new_radius: int):
        """Initialize with given parameters."""
        self.map = map
        self.init_xyz = init_xyz.copy()
        self.trigger_type = trigger_type
        self.new_xyz = new_xyz.copy()
        self.new_radius = new_radius


changes = [
    TriggerChange(0x1A, [1292, 120, 156], 15, [1294, 120, 158], 80),
]


def modifyTriggers(file_name):
    """Change triggers to correct them when seen fit."""
    map_index = int(file_name.split("lz")[1].split(".bin")[0])
    with open(file_name, "r+b") as fh:
        in_map_changes = [x for x in changes if x.map == map_index]
        lz_count = int.from_bytes(fh.read(2), "big")
        for lz_index in range(lz_count):
            lz_start = 2 + (lz_index * 0x38)
            coords = [0] * 3
            for coord_index in range(3):
                fh.seek(lz_start + (2 * coord_index))
                coord_val = int.from_bytes(fh.read(2), "big")
                if coord_val > 32767:
                    coord_val -= 65536
                coords[coord_index] = coord_val
            fh.seek(lz_start + 0x10)
            lz_type = int.from_bytes(fh.read(2), "big")
            for change in in_map_changes:
                match = lz_type == change.trigger_type
                for coord_index in range(3):
                    if change.init_xyz[coord_index] != coords[coord_index]:
                        match = False
                if match:
                    for coord_index, coord_val in enumerate(change.new_xyz):
                        fh.seek(lz_start + (2 * coord_index))
                        val = coord_val
                        if val < 0:
                            val += 65536
                        fh.write(val.to_bytes(2, "big"))
                    fh.seek(lz_start + 0x6)
                    fh.write(change.new_radius.to_bytes(2, "big"))
