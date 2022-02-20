# fmt: off
"""Collectible logic file for DK Isles."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.IslesMain: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.isdonkey, [(1, 2, 3), (1, 2, 3), (1, 2, 3), ], 3),
        Collectible(Collectibles.coin, Kongs.rainbow, lambda l: l.shockwave, [(1, 2, 3), ]),
        # Testing
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: True, [(1, 2, 3)], 170),
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: True, [(1, 2, 3)], 170),
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: True, [(1, 2, 3)], 170),
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: True, [(1, 2, 3)], 170),
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: True, [(1, 2, 3)], 170),
    ],
}
