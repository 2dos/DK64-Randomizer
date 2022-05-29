"""Module used to handle setting and randomizing kasplats."""
import random

import js
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Enums.Kongs import Kongs, GetKongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations

shufflable = {
    Locations.IslesKasplatHelmLobby: Kongs.donkey,
    Locations.IslesKasplatCastleLobby: Kongs.diddy,
    Locations.IslesKasplatCavesLobby: Kongs.lanky,
    Locations.IslesKasplatFactoryLobby: Kongs.tiny,
    Locations.IslesKasplatGalleonLobby: Kongs.chunky,
    Locations.JapesKasplatLeftTunnelNear: Kongs.donkey,
    Locations.JapesKasplatNearPaintingRoom: Kongs.diddy,
    Locations.JapesKasplatNearLab: Kongs.lanky,
    Locations.JapesKasplatLeftTunnelFar: Kongs.tiny,
    Locations.AztecKasplatSandyBridge: Kongs.donkey,
    Locations.AztecKasplatLlamaTemple: Kongs.lanky,
    Locations.AztecKasplatNearLab: Kongs.tiny,
    Locations.FactoryKasplatProductionTop: Kongs.donkey,
    Locations.FactoryKasplatProductionBottom: Kongs.diddy,
    Locations.FactoryKasplatRandD: Kongs.lanky,
    Locations.FactoryKasplatStorage: Kongs.tiny,
    Locations.FactoryKasplatBlocks: Kongs.chunky,
    Locations.GalleonKasplatGoldTower: Kongs.donkey,
    Locations.GalleonKasplatLighthouseArea: Kongs.diddy,
    Locations.GalleonKasplatCannons: Kongs.lanky,
    Locations.GalleonKasplatNearLab: Kongs.tiny,
    Locations.GalleonKasplatNearSub: Kongs.chunky,
    Locations.ForestKasplatNearBarn: Kongs.donkey,
    Locations.ForestKasplatInsideMushroom: Kongs.diddy,
    Locations.ForestKasplatOwlTree: Kongs.lanky,
    Locations.ForestKasplatLowerMushroomExterior: Kongs.tiny,
    Locations.ForestKasplatUpperMushroomExterior: Kongs.chunky,
    Locations.CavesKasplatNearLab: Kongs.donkey,
    Locations.CavesKasplatPillar: Kongs.lanky,
    Locations.CavesKasplatNearCandy: Kongs.tiny,
    Locations.CavesKasplatOn5DI: Kongs.chunky,
    Locations.CastleKasplatCrypt: Kongs.diddy,
    Locations.CastleKasplatHalfway: Kongs.lanky,
    Locations.CastleKasplatLowerLedge: Kongs.tiny,
    Locations.CastleKasplatNearCandy: Kongs.chunky,
}

constants = {
    # Must be chunky since need to shoot pineapple to lower vines and they don't stay lowered
    Locations.JapesKasplatUnderground: Kongs.chunky,
    # Need jetpack to reach so must be diddy
    Locations.AztecKasplatOnTinyTemple: Kongs.diddy,
    # Pineapple doors don't stay open, so need to be chunky
    Locations.AztecKasplatChunky5DT: Kongs.chunky,
    # Need to jetpack to the warp pad to get to the kasplat... can technically fall onto it but seems awful
    Locations.CavesKasplatNearFunky: Kongs.diddy,
    # Coconut gate doesn't stay open
    Locations.CastleKasplatTree: Kongs.donkey,
}


def FindLevel(location):
    """Find the level given a location."""
    for region in Logic.Regions.values():
        for loc in region.locations:
            if loc.id == location:
                return region.level


def ShuffleKasplats(LogicVariables):
    """Shuffles the kong assigned to each kasplat."""
    # Make sure only 1 of each kasplat per level, set up array to track that
    level_kongs = []
    kongs = GetKongs()
    # Add a list of kongs for each level
    # Excludes Shops level, but will include a useless Helm level
    for i in range(len(Levels) - 1):
        level_kongs.append(kongs.copy())
    # Remove constants
    for loc, kong in constants.items():
        level = FindLevel(loc)
        level_kongs[level].remove(kong)
    # Set up kasplat map
    LogicVariables.kasplat_map = {}
    # Make all shufflable kasplats initially accessible as anyone
    for location in shufflable.keys():
        LogicVariables.kasplat_map[location] = Kongs.any
    LogicVariables.kasplat_map.update(constants)
    # Do the shuffling
    shuffle_locations = list(shufflable.keys())
    random.shuffle(shuffle_locations)
    while len(shuffle_locations) > 0:
        location = shuffle_locations.pop()
        # Get this location's level and available kongs for this level
        level = FindLevel(location)
        kongs = level_kongs[level]
        random.shuffle(kongs)
        # Check each kong to see if placing it here produces a valid world
        success = False
        for kong in kongs:
            LogicVariables.kasplat_map[location] = kong
            # Assuming Successful placement, remove kong
            level_kongs[level].remove(kong)
            success = True
            break
        if not success:
            raise Ex.KasplatOutOfKongs


def KasplatShuffle(LogicVariables):
    """Facilitate the shuffling of kasplat types."""
    if LogicVariables.settings.kasplat_rando:
        retries = 0
        while True:
            try:
                # Shuffle kasplats
                ShuffleKasplats(LogicVariables)
                # Verify world by assuring all locations are still reachable
                if not Fill.VerifyWorld(LogicVariables.settings):
                    raise Ex.KasplatPlacementException
                return
            except Ex.KasplatPlacementException:
                if retries == 5:
                    js.postMessage("Kasplat placement failed, out of retries.")
                    raise Ex.KasplatAttemptCountExceeded
                retries += 1
                js.postMessage("Kasplat placement failed. Retrying. Tries: " + str(retries))


def InitKasplatMap(LogicVariables):
    """Initialize kasplat_map in logic variables with default values."""
    # Just use default kasplat associations.
    LogicVariables.kasplat_map = {}
    LogicVariables.kasplat_map.update(shufflable)
    LogicVariables.kasplat_map.update(constants)
