"""Module used to handle setting and randomizing kasplats."""
import random
import js

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Lists.Location import LocationList
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs


shufflable = {
    Locations.IslesDonkeyKasplat: Kongs.donkey,
    Locations.IslesDiddyKasplat: Kongs.diddy,
    Locations.IslesLankyKasplat: Kongs.lanky,
    Locations.IslesTinyKasplat: Kongs.tiny,
    Locations.IslesChunkyKasplat: Kongs.chunky,
    Locations.JapesDonkeyKasplat: Kongs.donkey,
    Locations.JapesDiddyKasplat: Kongs.diddy,
    Locations.JapesLankyKasplat: Kongs.lanky,
    Locations.JapesTinyKasplat: Kongs.tiny,
    Locations.AztecDonkeyKasplat: Kongs.donkey,
    Locations.AztecLankyKasplat: Kongs.lanky,
    Locations.AztecTinyKasplat: Kongs.tiny,
    Locations.FactoryDonkeyKasplat: Kongs.donkey,
    Locations.FactoryDiddyKasplat: Kongs.diddy,
    Locations.FactoryLankyKasplat: Kongs.lanky,
    Locations.FactoryTinyKasplat: Kongs.tiny,
    Locations.FactoryChunkyKasplat: Kongs.chunky,
    Locations.GalleonDonkeyKasplat: Kongs.donkey,
    Locations.GalleonDiddyKasplat: Kongs.diddy,
    Locations.GalleonLankyKasplat: Kongs.lanky,
    Locations.GalleonTinyKasplat: Kongs.tiny,
    Locations.GalleonChunkyKasplat: Kongs.chunky,
    Locations.ForestDonkeyKasplat: Kongs.donkey,
    Locations.ForestDiddyKasplat: Kongs.diddy,
    Locations.ForestLankyKasplat: Kongs.lanky,
    Locations.ForestTinyKasplat: Kongs.tiny,
    Locations.ForestChunkyKasplat: Kongs.chunky,
    Locations.CavesDonkeyKasplat: Kongs.donkey,
    Locations.CavesLankyKasplat: Kongs.lanky,
    Locations.CavesTinyKasplat: Kongs.tiny,
    Locations.CavesChunkyKasplat: Kongs.chunky,
    Locations.CastleDiddyKasplat: Kongs.diddy,
    Locations.CastleLankyKasplat: Kongs.lanky,
    Locations.CastleTinyKasplat: Kongs.tiny,
    Locations.CastleChunkyKasplat: Kongs.chunky,
}

constants = {
    # Must be chunky since need to shoot pineapple to lower vines and they don't stay lowered
    Locations.JapesChunkyKasplat: Kongs.chunky,
    # Need jetpack to reach so must be diddy
    Locations.AztecDiddyKasplat: Kongs.diddy,
    # Pineapple doors don't stay open, so need to be chunky
    Locations.AztecChunkyKasplat: Kongs.chunky,
    # Need to jetpack to the warp pad to get to the kasplat... can technically fall onto it but seems awful
    Locations.CavesDiddyKasplat: Kongs.diddy,
    # Coconut gate doesn't stay open
    Locations.CastleDonkeyKasplat: Kongs.donkey,
}


def FindLevel(location):
    """Find the level given a location."""
    for region in Logic.Regions.values():
        for loc in region.locations:
            if loc.id == location:
                return region.level


def ShuffleKasplats(LogicVariables):
    """Shuffles the kong assigned to each kasplat."""
    global kasplat_map
    # Make sure only 1 of each kasplat per level, set up array to track that
    level_kongs = []
    kongs = [x for x in Kongs if x != Kongs.any]
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
    shuffle_locations = [x for x in shufflable.keys()]
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
            if Fill.VerifyWorld(LogicVariables.settings):
                # Successful placement, remove kong
                level_kongs[level].remove(kong)
                success = True
                break
        if not success:
            raise Ex.KasplatOutOfKongs


def KasplatShuffle(LogicVariables):
    """Facilitate the shuffling of kasplat types."""
    if not LogicVariables.settings.kasplat:
        # Just use default kasplat associations.
        LogicVariables.kasplat_map = {}
        LogicVariables.kasplat_map.update(shufflable)
        LogicVariables.kasplat_map.update(constants)
    else:
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
                else:
                    retries += 1
                    js.postMessage("Kasplat placement failed. Retrying. Tries: " + str(retries))
