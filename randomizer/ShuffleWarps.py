"""Randomizes Bananaports."""
import random

import js
from randomizer.Enums.Warps import Warps
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Warps import BananaportVanilla


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
            if warp.map_id == warp_map:
                human_ports[warp.name] = "Warp " + str(warp.new_warp + 1)
                if not warp.locked:
                    pad_temp_list[warp.new_warp].append(warp.obj_id_vanilla)
        for warp_index in range(len(pad_temp_list)):
            if len(pad_temp_list[warp_index]) > 0:
                pad_list.append({"warp_index": warp_index, "warp_ids": pad_temp_list[warp_index].copy()})
        bananaport_replacements.append({"containing_map": warp_map, "pads": pad_list.copy()})


def getWarpFromSwapIndex(index):
    """Acquire warp name from index."""
    for warp in BananaportVanilla.values():
        if warp.swap_index == index:
            return warp


def ShuffleWarpsCrossMap(bananaport_replacements, human_ports, is_coupled):
    """Shuffles warps with the cross-map setting."""
    for warp in BananaportVanilla.values():
        warp.cross_map_placed = False
        bananaport_replacements.append(0)
    selected_warp_list = []
    for idx, warp in enumerate(BananaportVanilla.values()):
        if not warp.cross_map_placed or not is_coupled:
            available_warps = []
            full_warps = []
            for warp_check in BananaportVanilla.values():
                is_enabled = True
                if warp_check.swap_index == warp.swap_index:
                    is_enabled = False
                if warp_check.cross_map_placed:
                    is_enabled = False
                else:
                    full_warps.append(warp_check.swap_index)
                if warp.restricted and warp_check.restricted:
                    is_enabled = False
                if is_enabled:
                    available_warps.append(warp_check.swap_index)
            selected_index = random.choice(available_warps)
            warp_type_index = random.randint(0, 4)
            # Place Warp
            warp.tied_index = selected_index
            for warp_check in BananaportVanilla.values():
                if warp_check.swap_index == selected_index:
                    warp_check.cross_map_placed = True
            warp.new_warp = warp_type_index
            destination_warp = getWarpFromSwapIndex(selected_index)
            human_ports[warp.name] = destination_warp.name
            bananaport_replacements[warp.swap_index] = [selected_index, warp_type_index]
            warp.destination_region_id = destination_warp.region_id
            selected_lst = [selected_index]
            selected_warp_list.append(selected_index)
            if is_coupled:
                warp.cross_map_placed = True
                for warp_check in BananaportVanilla.values():
                    if warp_check.swap_index == selected_index:
                        warp_check.tied_index = warp.swap_index
                        selected_lst.append(warp.swap_index)
                        warp_check.new_warp = warp_type_index
                        destination_warp = getWarpFromSwapIndex(warp.swap_index)
                        human_ports[warp_check.name] = destination_warp.name
                        bananaport_replacements[warp_check.swap_index] = [warp.swap_index, warp_type_index]
                        warp_check.destination_region_id = destination_warp.region_id
                        selected_warp_list.append(warp.swap_index)
