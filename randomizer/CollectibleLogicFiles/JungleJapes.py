from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Kongs import Kongs
from Enums.Collectibles import Collectibles
from LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesMain: [
        Collectible(Collectibles.banana, Kongs.donkey, 5, lambda l: l.vines),
        Collectible(Collectibles.coin, Kongs.donkey, 3, lambda l: l.vines)
    ],
}
