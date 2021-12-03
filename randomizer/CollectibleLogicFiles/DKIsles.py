"""Collectible logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Collectibles import Collectibles
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.Start: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.isdonkey, 3),
        Collectible(Collectibles.coin, Kongs.rainbow, lambda l: l.shockwave),
    ],
}
