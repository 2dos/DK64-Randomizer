# fmt: off
"""Collectible logic file for DK Isles."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.TrainingGrounds: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: True, None, 3),  # Cave
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # Cave
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.vines and l.shockwave, None, ),  # Banana hoard

    ],
    Regions.IslesMain: [
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # Below Caves lobby
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave and l.jetpack, None, ),  # On Aztec lobby
    ],
    Regions.Prison: [
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # K. Lumsy

    ],
    Regions.BananaFairyRoom: [

    ],
    Regions.JungleJapesLobby: [

    ],
    Regions.AngryAztecLobby: [

    ],
    Regions.CrocodileIsleBeyondLift: [

    ],
    Regions.IslesSnideRoom: [

    ],
    Regions.FranticFactoryLobby: [

    ],
    Regions.GloomyGalleonLobby: [

    ],
    Regions.CabinIsle: [
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # In front of fungi lobby

    ],
    Regions.FungiForestLobby: [

    ],
    Regions.CrystalCavesLobby: [

    ],
    Regions.CreepyCastleLobby: [
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave and l.balloon, None, ),  # In Castle lobby

    ],
    Regions.HideoutHelmLobby: [

    ],
}
