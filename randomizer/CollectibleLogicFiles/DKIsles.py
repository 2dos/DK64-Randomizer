# fmt: off
"""Collectible logic file for DK Isles."""

from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Kongs import Kongs
from Enums.Collectibles import Collectibles
from LogicClasses import Collectible

LogicRegions = {
    Regions.Start: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.isdonkey, 3),
        Collectible(Collectibles.coin, Kongs.rainbow, lambda l: l.shockwave),
    ],
}
