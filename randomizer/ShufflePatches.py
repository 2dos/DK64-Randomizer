"""Shuffle Dirt Patch Locations."""
import random

import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.DKIsles
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Lists.Patches import DirtPatchLocations
from randomizer.LogicClasses import Collectible
from randomizer.Spoiler import Spoiler


def addPatch(patch):
    """Add patch to relevant Logic Region."""
    level_to_enum = {
        Levels.DKIsles: randomizer.CollectibleLogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.CollectibleLogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions,
    }
    level_data = level_to_enum[patch.level_name]
    if patch.logicregion in level_data:
        level_data[patch.logicregion].append(Collectible(Collectibles.coin, Kongs.any, patch.logic, None, 1, True, False))
    else:
        level_data[patch.logicregion] = [Collectible(Collectibles.coin, Kongs.any, patch.logic, None, 1, True, False)]


def removePatches():
    """Remove all patches from Logic regions."""
    level_collectibles = [
        randomizer.CollectibleLogicFiles.DKIsles.LogicRegions,
        randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions,
        randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions,
        randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions,
        randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions,
        randomizer.CollectibleLogicFiles.FungiForest.LogicRegions,
        randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions,
        randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions,
    ]
    for level in level_collectibles:
        for region in level:
            region_data = level[region]
            for collectible in region_data:
                if collectible.type == Collectibles.coin and collectible.kong == Kongs.any:
                    collectible.enabled = False


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

    select_random_dirt_from_area(total_dirt_patch_list[Levels.DKIsles], 4, spoiler, human_spoiler)
    del total_dirt_patch_list[Levels.DKIsles]

    for SingleDirtPatchLocation in range(5):
        area_key = random.choice(list(total_dirt_patch_list.keys()))
        area_dirt = total_dirt_patch_list[area_key]
        select_random_dirt_from_area(area_dirt, 2, spoiler, human_spoiler)
        del total_dirt_patch_list[area_key]

    for area_key in total_dirt_patch_list.keys():
        area_dirt = total_dirt_patch_list[area_key]
        select_random_dirt_from_area(area_dirt, 1, spoiler, human_spoiler)
    return human_spoiler.copy()


def select_random_dirt_from_area(area_dirt, amount, spoiler: Spoiler, human_spoiler):
    """Select <amount> random dirt patches from <area_dirt>, which is a list of dirt patches. Makes sure max 1 dirt patch per group is selected."""
    for iterations in range(amount):
        selected_patch = random.choice(area_dirt)  # selects a random patch from the list
        for patch in DirtPatchLocations:  # enables the selected patch
            if patch.name == selected_patch.name:
                patch.setPatch(True)
                addPatch(patch)
                human_spoiler.append(patch.name)
                spoiler.dirt_patch_placement.append(patch.name)
                area_dirt.remove(selected_patch)
                break
        if amount > 1:  # if multiple patches are picked, remove patches from the same group, prevent them from being picked
            area_dirt = [dirt for dirt in area_dirt if dirt.group != selected_patch.group]
