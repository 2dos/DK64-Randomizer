"""Collectible logic file for Jungle Japes."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Collectibles import Collectibles
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesMain: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: l.vines, 5),
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.vines, 3),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut),
    ],
}
