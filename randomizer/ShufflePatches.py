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

def addPatch(patch):
    """Add patch to relevant Logic Region."""
    level_to_enum = {
        "DK Isles": randomizer.CollectibleLogicFiles.DKIsles.LogicRegions,
        "Jungle Japes": randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions,
        "Angry Aztec": randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions,
        "Frantic Factory": randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions,
        "Gloomy Galleon": randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions,
        "Fungi Forest": randomizer.CollectibleLogicFiles.FungiForest.LogicRegions,
        "Crystal Caves": randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions,
        "Creepy Castle": randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions,
    }
    level_to_enum[patch.level_name][patch.logicregion].append(Collectible(Collectibles.coin,Kongs.any,patch.logic,None,1,True,False))


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

def ShufflePatches(human_spoiler):
    """Shuffle Dirt Patch Locations."""
    removePatches()
    dirt_list = []
    for x in DirtPatchLocations:
        x.setPatch(False)
        dirt_list.append(x.name)
    for x in range(16):
        selected_patch_name = random.choice(dirt_list)
        for y in DirtPatchLocations:
            if y.name == selected_patch_name:
                y.setPatch(True)
                addPatch(y)
                dirt_list.remove(selected_patch_name)