# fmt: off
"""Collectible logic file for Jungle Japes."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesMain: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: l.vines, [(1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), ], 5),
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.vines, [(1, 2, 3), (1, 2, 3), (1, 2, 3), ], 3),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, [(1, 2, 3), ]),
        # Testing
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, [(1, 2, 3)], 100),
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, [(1, 2, 3)], 100),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, [(1, 2, 3)], 100),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, [(1, 2, 3)], 100),
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, [(1, 2, 3)], 100),
    ],
}
