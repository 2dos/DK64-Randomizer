"""Replace LZs in ROM."""

lz_replacements = [
    {
        "container_map": 0x22,  # DK Isles
        "zones": [
            {
                "vanilla_map": 0xB0,
                "vanilla_exit": 0,
                "new_map": 0x11,
                "new_exit": 1,
            }
        ],
    }
]

valid_lz_types = [9, 12, 13, 16]


def intToArr(val, size):
    """Convert INT to an array.

    Args:
        val (int): Value to convert
        size (int): Size to write as

    Returns:
        array: int array
    """
    tmp = val
    arr = []
    for x in range(size):
        arr.append(0)
    slot = size - 1
    while slot > -1:
        tmpv = tmp % 256
        arr[slot] = tmpv
        slot -= 1
        tmp = int((tmp - tmpv) / 256)
        if slot == -1:
            break
        elif tmp == 0:
            break
    return arr


with open("dk64-randomizer-base-dev.z64", "r+b") as fh:
    for cont_map in lz_replacements:
        dk_isles_lzs = 0x2978CDE
        # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
        fh.seek(dk_isles_lzs)
        lz_count = int.from_bytes(fh.read(2), "big")
        for x in range(lz_count):
            start = (x * 0x38) + 2
            fh.seek(dk_isles_lzs + start + 0x10)
            lz_type = int.from_bytes(fh.read(2), "big")
            # print(lz_type)
            if lz_type in valid_lz_types:
                fh.seek(dk_isles_lzs + start + 0x12)
                lz_map = int.from_bytes(fh.read(2), "big")
                fh.seek(dk_isles_lzs + start + 0x14)
                lz_exit = int.from_bytes(fh.read(2), "big")
                for y in cont_map["zones"]:
                    if lz_map == y["vanilla_map"]:
                        if lz_exit == y["vanilla_exit"]:
                            fh.seek(dk_isles_lzs + start + 0x12)
                            map_bytes = intToArr(y["new_map"], 2)
                            fh.write(bytearray(map_bytes))
                            fh.seek(dk_isles_lzs + start + 0x14)
                            exit_bytes = intToArr(y["new_exit"], 2)
                            fh.write(bytearray(exit_bytes))
