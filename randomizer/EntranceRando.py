"""Randomize Entrances based on shuffled_exit_instructions"""
import js

from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler

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


def randomize_entrances(spoiler: Spoiler):
    if spoiler.settings.shuffle_loading_zones != "none" and spoiler.shuffled_exit_instructions != None:
        for cont_map in spoiler.shuffled_exit_instructions:
            # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
            cont_map_id = int(cont_map["container_map"])
            cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM().readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM().seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM().readBytes(2), "big")
                # print(lz_type)
                if lz_type in valid_lz_types:
                    ROM().seek(cont_map_lzs_address + start + 0x12)
                    lz_map = int.from_bytes(ROM().readBytes(2), "big")
                    ROM().seek(cont_map_lzs_address + start + 0x14)
                    lz_exit = int.from_bytes(ROM().readBytes(2), "big")
                    for zone in cont_map["zones"]:
                        if lz_map == zone["vanilla_map"]:
                            if lz_exit == zone["vanilla_exit"]:
                                ROM().seek(cont_map_lzs_address + start + 0x12)
                                map_bytes = intToArr(zone["new_map"], 2)
                                ROM().writeBytes(bytearray(map_bytes))
                                ROM().seek(cont_map_lzs_address + start + 0x14)
                                exit_bytes = intToArr(zone["new_exit"], 2)
                                ROM().writeBytes(bytearray(exit_bytes))
