"""Shuffles the locations of shops."""
import random
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Levels import Levels
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Regions import Regions


class ShopLocation:
    """Class which stores data for a shop location."""

    def __init__(self, shop, map, locked=False):
        """Initialize with given parameters."""
        self.shop = shop
        self.map = map
        self.locked = locked
        self.new_shop = shop

    def setShop(self, shop):
        """Assign new shop to shop location object."""
        self.new_shop = shop


available_shops = {
    Levels.DKIsles: [
        ShopLocation(Regions.CrankyGeneric, Maps.TrainingGrounds),
        ShopLocation(Regions.Snide, Maps.IslesSnideRoom),
    ],
    Levels.JungleJapes: [
        ShopLocation(Regions.CrankyGeneric, Maps.JungleJapes),
        ShopLocation(Regions.Snide, Maps.JungleJapes),
        ShopLocation(Regions.FunkyGeneric, Maps.JungleJapes),
    ],
    Levels.AngryAztec: [
        ShopLocation(Regions.CrankyGeneric, Maps.AngryAztec),
        ShopLocation(Regions.CandyGeneric, Maps.AngryAztec),
        ShopLocation(Regions.FunkyGeneric, Maps.AngryAztec),
        ShopLocation(Regions.Snide, Maps.AngryAztec),
    ],
    Levels.FranticFactory: [
        ShopLocation(Regions.CrankyGeneric, Maps.FranticFactory),
        ShopLocation(Regions.CandyGeneric, Maps.FranticFactory),
        ShopLocation(Regions.FunkyGeneric, Maps.FranticFactory),
        ShopLocation(Regions.Snide, Maps.FranticFactory),
    ],
    Levels.GloomyGalleon: [
        ShopLocation(Regions.CrankyGeneric, Maps.GloomyGalleon),
        ShopLocation(Regions.CandyGeneric, Maps.GloomyGalleon, locked=True),  # Locked because on water
        ShopLocation(Regions.FunkyGeneric, Maps.GloomyGalleon, locked=True),  # Locked because on water
        ShopLocation(Regions.Snide, Maps.GloomyGalleon),
    ],
    Levels.FungiForest: [
        ShopLocation(Regions.CrankyGeneric, Maps.FungiForest),
        ShopLocation(Regions.FunkyGeneric, Maps.FungiForest),
        ShopLocation(Regions.Snide, Maps.FungiForest),
    ],
    Levels.CrystalCaves: [
        ShopLocation(Regions.CrankyGeneric, Maps.CrystalCaves),
        ShopLocation(Regions.CandyGeneric, Maps.CrystalCaves),
        ShopLocation(Regions.FunkyGeneric, Maps.CrystalCaves),
        ShopLocation(Regions.Snide, Maps.CrystalCaves),
    ],
    Levels.CreepyCastle: [
        ShopLocation(Regions.CrankyGeneric, Maps.CreepyCastle),
        ShopLocation(Regions.CandyGeneric, Maps.CastleUpperCave),
        ShopLocation(Regions.FunkyGeneric, Maps.CastleLowerCave),
        ShopLocation(Regions.Snide, Maps.CreepyCastle),
    ],
}


def ShuffleShopLocations(spoiler: Spoiler):
    """Shuffle Shop locations within their own pool inside the level."""
    # Reset
    for level in available_shops:
        shop_array = available_shops[level]
        for shop in shop_array:
            shop.setShop(shop.shop)
    # Shuffle
    assortment = {}
    for level in available_shops:
        shop_array = available_shops[level]
        # Get list of shops in level
        shops_in_levels = []
        for shop in shop_array:
            if not shop.locked:
                shops_in_levels.append(shop.shop)
        random.shuffle(shops_in_levels)
        # Assign shuffle to data
        assortment_in_level = {}
        placement_index = 0
        for shop_index, shop in enumerate(shop_array):
            if not shop.locked:
                shop.setShop(shops_in_levels[placement_index])
                assortment_in_level[shop.shop] = shop.new_shop
                placement_index += 1
        assortment[level] = assortment_in_level
    # Write Assortment to spoiler
    spoiler.shuffled_shop_locations = assortment
