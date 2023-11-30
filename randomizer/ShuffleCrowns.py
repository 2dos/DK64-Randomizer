"""Shuffle Crown picks, excluding helm."""

import random

from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists import Exceptions
from randomizer.Lists.CustomLocations import CustomLocations, LocationTypes
from randomizer.LogicClasses import LocationLogic


def ShuffleCrowns(spoiler, crown_selection, human_crowns):
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
    level_to_name = {
        Levels.DKIsles: "Isles",
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
        Levels.HideoutHelm: "Helm",
    }
    # Remove crowns from their original logic region
    for id, region in spoiler.RegionList.items():
        region.locations = [loclogic for loclogic in region.locations if loclogic.id not in crown_locations]
    global_crown_idx = 0
    for level in CustomLocations:
        level_lst = CustomLocations[level]
        index_lst = list(range(len(level_lst)))
        index_lst = [x for x in index_lst if level_lst[x].vanilla_crown or (not level_lst[x].selected and LocationTypes.CrownPad not in level_lst[x].banned_types)]
        pick_count = 1
        if level == Levels.DKIsles:
            pick_count = 2
        crowns = random.sample(index_lst, pick_count)
        # Give plandomizer an opportunity to have the final say
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_battle_arenas"] != -1:
            for i in range(pick_count):
                if spoiler.settings.plandomizer_dict["plando_battle_arenas"][crown_locations[global_crown_idx + i]] != -1:
                    crowns[i] = spoiler.settings.plandomizer_dict["plando_battle_arenas"][crown_locations[global_crown_idx + i]]
                if crowns[global_crown_idx] not in index_lst:
                    raise Exceptions.PlandoIncompatibleException(f'Battle arena "{crowns[global_crown_idx + 1]}" not found in {level}.')
        crown_data = {}
        for crown_index in crowns:
            crown_data[crown_index] = 0
        if level == Levels.DKIsles:
            isles_placed = [False, False]
            for crown_index in crowns:
                crown = level_lst[crown_index]
                crown.placement_subindex = crown.default_index
                if crown.vanilla_crown:
                    isles_placed[crown.placement_subindex] = True
            for crown_index in crowns:
                crown = level_lst[crown_index]
                if not crown.vanilla_crown:
                    if isles_placed[0]:
                        crown.placement_subindex = 1
                        crown_data[crown_index] = 1
                        isles_placed[1] = True
                    else:
                        crown.placement_subindex = 0
                        crown_data[crown_index] = 0
                        isles_placed[0] = True
        crown_selection[level] = crown_data
        # In the event that the second crown on the list is IslesBattleArena2, reverse the list
        # because after this, the first crown on the list will get the logic for IslesBattleArena2
        # For plando, this should be prevented in the plando block above
        if len(crowns) == 2 and CustomLocations[level][crowns[1]].placement_subindex == 0:
            crowns.reverse()
        for crown_index, crown in enumerate(crowns):
            crown_name = level.name
            crown_number_string = ""
            if level == Levels.DKIsles:
                crown_name = f"{level.name} ({2 - level_lst[crown].placement_subindex})"
                crown_number_string = f" {2 - level_lst[crown].placement_subindex}"
            human_crowns[crown_name] = level_lst[crown].name
            crown_obj = level_lst[crown]
            crown_obj.setCustomLocation(True)
            spoiler.LocationList[crown_locations[global_crown_idx]].name = f"{level_to_name[level]} Battle Arena{crown_number_string} ({level_lst[crown].name})"
            crownRegion = spoiler.RegionList[crown_obj.logic_region]
            # Add crowns to their updated logic region
            crownRegion.locations.append(LocationLogic(crown_locations[global_crown_idx], crown_obj.logic))
            global_crown_idx += 1
