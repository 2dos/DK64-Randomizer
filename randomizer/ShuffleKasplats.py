"""Module used to handle setting and randomizing kasplats."""
import random

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs

kasplat_map = {}

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
    Locations.CastleDonkeyKasplat: Kongs.donkey,
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
    Locations.CastleDonkeyKasplat: Kongs.donkey
}

def KasplatShuffle(settings):
    """Facilitate the shuffling of kasplat types."""
    if not settings.kasplat:
        # Just use default kasplat associations.
        kasplat_map.update(shufflable)
        kasplat_map.update(constants)
