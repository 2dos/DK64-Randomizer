"""Collectible logic file for Gloomy Galleon."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.GloomyGalleonStart: [
        # Testing
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, [(1,2,3)], 100),
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, [(1,2,3)], 100),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, [(1,2,3)], 100),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, [(1,2,3)], 100),
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, [(1,2,3)], 100),
    ]
}
