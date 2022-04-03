# fmt: off
"""Collectible logic file for DK Isles."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.IslesMain: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.isdonkey, None, 3),  # in TG
        Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 4),  # 2 in TG, 1 under caves rock, 1 in Klumsy
    ],
}
