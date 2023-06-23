"""Randomizes Bananaports."""
import random

import js
import randomizer.Logic as Logic
from randomizer.Enums.Warps import Warps
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Warps import BananaportVanilla, VanillaBananaportSelector
from randomizer.LogicClasses import TransitionFront


def getShuffleMaps():
    """Produce list of maps which contain a bananaport swap."""
    lst = []
    for x in BananaportVanilla.values():
        if x.map_id not in lst:
            lst.append(x.map_id)
    return lst


def verifySelectedWarps(selected_warps):
    """Verify if the selected_warps variable is empty, and fills it with all options if it is."""
    if len(selected_warps) == 0:
        for warp in VanillaBananaportSelector:
            selected_warps.append(Maps[warp["value"]])


def ShuffleWarps(bananaport_replacements, human_ports, selected_warps):
    """Shuffles warps between themselves."""
    verifySelectedWarps(selected_warps)
    map_list = getShuffleMaps()
    for warp_map in map_list:
        if warp_map not in selected_warps:
            # if the warp is in an excluded level, create an entry into bananaport_replacements to point to its vanilla data instead of trying to leave it blank
            # this function could probably work correctly without this safeguard, but i'd rather be safe than sorry
            pad_list = []
            pad_temp_list = [[], [], [], [], []]
            for warp in BananaportVanilla.values():
                if warp.map_id == warp_map:
                    pad_temp_list[warp.vanilla_warp].append(warp.obj_id_vanilla)
                    if len(pad_temp_list[warp.vanilla_warp]) > 1:
                        pad_list.append({"warp_index": warp.vanilla_warp, "warp_ids": pad_temp_list[warp.vanilla_warp].copy()})
            bananaport_replacements.append({"containing_map": warp_map, "pads": pad_list.copy()})
        else:
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
    # After shuffling the warps, make sure the swap indexes are right for warp linking immediately after this method
    # This probably is the least efficient way to do it but it works
    for warp_id, warp in BananaportVanilla.items():
        for paired_warp_id, paired_warp in BananaportVanilla.items():
            # Find the paired warp - we know they're always in the same map here which saves some headache
            if warp_id != paired_warp_id and warp.map_id == paired_warp.map_id and warp.new_warp == paired_warp.new_warp:
                warp.tied_index = paired_warp.swap_index
                break


def getWarpFromSwapIndex(index):
    """Acquire warp name from index."""
    for warp in BananaportVanilla.values():
        if warp.swap_index == index:
            return warp


def ShuffleWarpsCrossMap(bananaport_replacements, human_ports, is_coupled, selected_warps):
    """Shuffles warps with the cross-map setting."""
    verifySelectedWarps(selected_warps)
    for warp in BananaportVanilla.values():
        warp.cross_map_placed = False
        bananaport_replacements.append(0)
    selected_warp_list = []
    for idx, warp in enumerate(BananaportVanilla.values()):
        if warp.map_id not in selected_warps:
            # if the warp is in an excluded level, create an entry into bananaport_replacements to point to its vanilla data instead of trying to leave it blank
            for warp_check in BananaportVanilla.values():
                if warp_check.map_id == warp.map_id and warp_check.vanilla_warp == warp.vanilla_warp and warp_check.name != warp.name:
                    bananaport_replacements[warp.swap_index] = [warp_check.swap_index, warp.vanilla_warp]
                    warp.destination_region_id = warp_check.region_id
        elif not warp.cross_map_placed or not is_coupled:
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
                if warp_check.map_id not in selected_warps:
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


def LinkWarps():
    """Given the current state of warps, create the transitions between them."""
    # Remove all existing transitions that are warp transitions - this prevents warp logic from bleeding between seed gens
    for region in Logic.Regions.values():
        region.exits = [exit for exit in region.exits if not exit.isBananaportTransition]
    # For each warp, identify the source and destination regions
    for warp_data in BananaportVanilla.values():
        destination_warp_data = getWarpFromSwapIndex(warp_data.tied_index)
        if warp_data.region_id != destination_warp_data.region_id:
            source_region = Logic.Regions[warp_data.region_id]
            # The source region gets a transition to the destination region conditionally based on the destination warp being tagged
            source_region.exits.append(TransitionFront(destination_warp_data.region_id, destination_warp_data.event_logic, isBananaportTransition=True))
