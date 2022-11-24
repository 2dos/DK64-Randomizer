"""Shuffle Crown picks, excluding helm."""

import random
import randomizer.Logic as Logic
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.CrownLocations import CrownLocations
from randomizer.LogicClasses import LocationLogic


def ShuffleCrowns(crown_selection, human_crowns):
    """Generate Crown Placement Assortment."""
    crown_locations = (
        Locations.JapesBattleArena,
        Locations.AztecBattleArena,
        Locations.FactoryBattleArena,
        Locations.GalleonBattleArena,
        Locations.ForestBattleArena,
        Locations.CavesBattleArena,
        Locations.CastleBattleArena,
        Locations.IslesBattleArena2,
        Locations.IslesBattleArena1,
        Locations.HelmBattleArena,
    )
    global_crown_idx = 0
    for level in CrownLocations:
        level_lst = CrownLocations[level]
        index_lst = list(range(len(level_lst)))
        pick_count = 1
        if level == Levels.DKIsles:
            pick_count = 2
        crowns = random.sample(index_lst, pick_count)
        crown_data = {}
        for crown_index in crowns:
            crown_data[crown_index] = 0
        if level == Levels.DKIsles:
            isles_placed = [False, False]
            for crown_index in crowns:
                crown = level_lst[crown_index]
                crown.placement_subindex = crown.default_index
                if crown.is_vanilla:
                    isles_placed[crown.placement_subindex] = True
            for crown_index in crowns:
                crown = level_lst[crown_index]
                if not crown.is_vanilla:
                    if isles_placed[0]:
                        crown.placement_subindex = 1
                        crown_data[crown_index] = 1
                        isles_placed[1] = True
                    else:
                        crown.placement_index = 0
                        crown_data[crown_index] = 0
                        isles_placed[0] = True
        crown_selection[level] = crown_data
        for crown_index, crown in enumerate(crowns):
            crown_name = level.name
            if level == Levels.DKIsles:
                crown_name = f"{level.name} ({2 - level_lst[crown].placement_subindex})"
            human_crowns[crown_name] = level_lst[crown].name
            crown_obj = level_lst[crown]
            crownRegion = Logic.Regions[crown_obj.region]
            crownRegion.locations.append(LocationLogic(crown_locations[global_crown_idx], crown_obj.logic))
            global_crown_idx += 1
