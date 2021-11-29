from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Kongs import Kongs
from Enums.Collectibles import Collectibles
from LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesMain: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: l.vines, 5),
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.vines, 3),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut),
    ],
}
