"""Randomizes Bananaports."""
import random

import js
from randomizer.Enums.Warps import Warps
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Lists.MapsAndExits import Maps


def getShuffleMaps():
    """Produce list of maps which contain a bananaport swap."""
    lst = []
    for x in BananaportVanilla.values():
        if x.map_id not in lst:
            lst.append(x.map_id)
    return lst


def ShuffleWarps(bananaport_replacements, human_ports):
    """Shuffles warps between themselves."""
    map_list = getShuffleMaps()
    for warp_map in map_list:
        shufflable_warps = []
        # Generate list of shufflable warp types (Warp 1, Warp 2 etc.)
        for warp in BananaportVanilla.values():
            if warp.map_id == warp_map and not warp.locked:
                shufflable_warps.append(warp.vanilla_warp)
        random.shuffle(shufflable_warps)
        shuffle_index = 0
        # Apply shuffle
        for warp in BananaportVanilla.keys():
            if BananaportVanilla[warp].map_id == warp_map and not BananaportVanilla[warp].locked:
                BananaportVanilla[warp].setNewWarp(shufflable_warps[shuffle_index])
                shuffle_index += 1
        # Write to spoiler and create array of replacements
        pad_list = []
        pad_temp_list = [[], [], [], [], []]
        for warp in BananaportVanilla.values():
            if warp.map_id == warp_map and not warp.locked:
                pad_temp_list[warp.new_warp].append(warp.obj_id_vanilla)
                human_ports[warp.name] = "Warp " + str(warp.new_warp + 1)
        for warp_index in range(len(pad_temp_list)):
            if len(pad_temp_list[warp_index]) > 0:
                pad_list.append({"warp_index": warp_index, "warp_ids": pad_temp_list[warp_index].copy()})
        bananaport_replacements.append({"containing_map": warp_map, "pads": pad_list.copy()})
