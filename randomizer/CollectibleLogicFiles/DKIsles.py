from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Kongs import Kongs
from Enums.Collectibles import Collectibles
from LogicClasses import Collectible

LogicRegions = {
    Regions.Start: [
        Collectible(Collectibles.coin, Kongs.donkey, 3, lambda l: l.isdonkey),
        Collectible(Collectibles.coin, Kongs.rainbow, 5, lambda l: l.shockwave),
    ],
}
