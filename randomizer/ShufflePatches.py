"""Shuffle Dirt Patch Locations."""
import random

import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Lists.Patches import DirtPatchLocations
from randomizer.Enums.Locations import Locations
from randomizer.Lists.Location import LocationList
from randomizer.LogicClasses import LocationLogic
from randomizer.Spoiler import Spoiler


def addPatch(patch, global_index, name):
    """Add patch to relevant Logic Region."""
    level_to_enum = {
        Levels.DKIsles: randomizer.LogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.LogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.LogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.LogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.LogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.LogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.LogicFiles.CreepyCastle.LogicRegions,
    }
    level_data = level_to_enum[patch.level_name]
    level_data[patch.logicregion].locations.append(
        LocationLogic(
            Locations.RainbowCoin_Location00 + global_index,
            patch.logic
        )
    )
    LocationList[Locations.RainbowCoin_Location00 + global_index].name = name


def removePatches():
    """Remove all patches from Logic regions."""
    level_logic_regions = [
        randomizer.LogicFiles.DKIsles.LogicRegions,
        randomizer.LogicFiles.JungleJapes.LogicRegions,
        randomizer.LogicFiles.AngryAztec.LogicRegions,
        randomizer.LogicFiles.FranticFactory.LogicRegions,
        randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        randomizer.LogicFiles.FungiForest.LogicRegions,
        randomizer.LogicFiles.CrystalCaves.LogicRegions,
        randomizer.LogicFiles.CreepyCastle.LogicRegions,
    ]
    for level in level_logic_regions:
        for region in level:
            region_data = level[region]
            region_data.locations = [x for x in region_data.locations if x.id < Locations.RainbowCoin_Location00 or x.id > Locations.RainbowCoin_Location15]


def ShufflePatches(spoiler: Spoiler, human_spoiler):
    """Shuffle Dirt Patch Locations."""
    removePatches()
    spoiler.dirt_patch_placement = []
    total_dirt_patch_list = {
        Levels.DKIsles: [],
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
    }

    for SingleDirtPatchLocation in DirtPatchLocations:
        SingleDirtPatchLocation.setPatch(False)
        total_dirt_patch_list[SingleDirtPatchLocation.level_name].append(SingleDirtPatchLocation)
    global_index = select_random_dirt_from_area(total_dirt_patch_list[Levels.DKIsles], 4, spoiler, human_spoiler, 0)
    del total_dirt_patch_list[Levels.DKIsles]

    for SingleDirtPatchLocation in range(5):
        area_key = random.choice(list(total_dirt_patch_list.keys()))
        area_dirt = total_dirt_patch_list[area_key]
        global_index = select_random_dirt_from_area(area_dirt, 2, spoiler, human_spoiler, global_index)
        del total_dirt_patch_list[area_key]

    for area_key in total_dirt_patch_list.keys():
        area_dirt = total_dirt_patch_list[area_key]
        global_index = select_random_dirt_from_area(area_dirt, 1, spoiler, human_spoiler, global_index)
    return human_spoiler.copy()


def select_random_dirt_from_area(area_dirt, amount, spoiler: Spoiler, human_spoiler, starting_global_index: int) -> int:
    """Select <amount> random dirt patches from <area_dirt>, which is a list of dirt patches. Makes sure max 1 dirt patch per group is selected."""
    for iterations in range(amount):
        selected_patch = random.choice(area_dirt)  # selects a random patch from the list
        for patch in DirtPatchLocations:  # enables the selected patch
            if patch.name == selected_patch.name:
                patch.setPatch(True)
                addPatch(patch, starting_global_index, patch.name)
                starting_global_index += 1
                human_spoiler.append(patch.name)
                spoiler.dirt_patch_placement.append(patch.name)
                area_dirt.remove(selected_patch)
                break
        if amount > 1:  # if multiple patches are picked, remove patches from the same group, prevent them from being picked
            area_dirt = [dirt for dirt in area_dirt if dirt.group != selected_patch.group]
    return starting_global_index
