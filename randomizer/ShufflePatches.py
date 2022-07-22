"""Shuffle Dirt Patch Locations."""
import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.DKIsles
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Levels import Levels
from randomizer.LogicClasses import Collectible
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.Patches import DirtPatchLocations
import random
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
    dirt_list = []
    spoiler.dirt_patch_placement = []
    for x in DirtPatchLocations:
        x.setPatch(False)
        dirt_list.append(x.name)
    for x in range(16):
        selected_patch_name = random.choice(dirt_list)
        for y in DirtPatchLocations:
            if y.name == selected_patch_name:
                y.setPatch(True)
                addPatch(y)
                human_spoiler.append(y.name)
                spoiler.dirt_patch_placement.append(y.name)
                dirt_list.remove(selected_patch_name)
    return human_spoiler.copy()
