"""Shuffles the locations of shops."""
import random

import randomizer.Logic as Logic
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import ShuffleLoadingZones
from randomizer.Lists.MapsAndExits import Maps
from randomizer.LogicClasses import TransitionFront
from randomizer.Spoiler import Spoiler


class ShopLocation:
    """Class which stores data for a shop location."""

    def __init__(self, shop, map, containing_region, shop_exit, locked=False):
        """Initialize with given parameters."""
        self.shop = shop
        self.map = map
        self.locked = locked
        self.new_shop = shop
        self.containing_region = containing_region
        self.shop_exit = shop_exit
        self.new_shop_exit = shop_exit

    def setShop(self, shop):
        """Assign new shop to shop location object."""
        self.new_shop = shop.shop
        self.new_shop_exit = shop.shop_exit


available_shops = {
    Levels.DKIsles: [
        ShopLocation(Regions.CrankyGeneric, Maps.TrainingGrounds, Regions.TrainingGrounds, Regions.CrankyIsles),
        ShopLocation(Regions.Snide, Maps.IslesSnideRoom, Regions.IslesSnideRoom, Regions.Snide),
    ],
    Levels.JungleJapes: [
        ShopLocation(Regions.CrankyGeneric, Maps.JungleJapes, Regions.JapesBeyondCoconutGate2, Regions.CrankyJapes),
        ShopLocation(Regions.Snide, Maps.JungleJapes, Regions.JungleJapesMain, Regions.Snide),
        ShopLocation(Regions.FunkyGeneric, Maps.JungleJapes, Regions.JungleJapesMain, Regions.FunkyJapes),
    ],
    Levels.AngryAztec: [
        ShopLocation(Regions.CrankyGeneric, Maps.AngryAztec, Regions.AngryAztecConnectorTunnel, Regions.CrankyAztec),
        ShopLocation(Regions.CandyGeneric, Maps.AngryAztec, Regions.AngryAztecOasis, Regions.CandyAztec),
        ShopLocation(Regions.FunkyGeneric, Maps.AngryAztec, Regions.AngryAztecMain, Regions.FunkyAztec),
        ShopLocation(Regions.Snide, Maps.AngryAztec, Regions.AngryAztecMain, Regions.Snide),
    ],
    Levels.FranticFactory: [
        ShopLocation(Regions.CrankyGeneric, Maps.FranticFactory, Regions.BeyondHatch, Regions.CrankyFactory),
        ShopLocation(Regions.CandyGeneric, Maps.FranticFactory, Regions.BeyondHatch, Regions.CandyFactory),
        ShopLocation(Regions.FunkyGeneric, Maps.FranticFactory, Regions.Testing, Regions.FunkyFactory),
        ShopLocation(Regions.Snide, Maps.FranticFactory, Regions.Testing, Regions.Snide),
    ],
    Levels.GloomyGalleon: [
        ShopLocation(Regions.CrankyGeneric, Maps.GloomyGalleon, Regions.GloomyGalleonStart, Regions.CrankyGalleon),
        ShopLocation(Regions.CandyGeneric, Maps.GloomyGalleon, Regions.Shipyard, Regions.CandyGalleon, locked=True),  # Locked because on water
        ShopLocation(Regions.FunkyGeneric, Maps.GloomyGalleon, Regions.Shipyard, Regions.FunkyGalleon, locked=True),  # Locked because on water
        ShopLocation(Regions.Snide, Maps.GloomyGalleon, Regions.LighthouseSnideAlcove, Regions.Snide),
    ],
    Levels.FungiForest: [
        ShopLocation(Regions.CrankyGeneric, Maps.FungiForest, Regions.GiantMushroomArea, Regions.CrankyForest),
        ShopLocation(Regions.FunkyGeneric, Maps.FungiForest, Regions.WormArea, Regions.FunkyForest),
        ShopLocation(Regions.Snide, Maps.FungiForest, Regions.MillArea, Regions.Snide),
    ],
    Levels.CrystalCaves: [
        ShopLocation(Regions.CrankyGeneric, Maps.CrystalCaves, Regions.CrystalCavesMain, Regions.CrankyCaves),
        ShopLocation(Regions.CandyGeneric, Maps.CrystalCaves, Regions.CabinArea, Regions.CandyCaves),
        ShopLocation(Regions.FunkyGeneric, Maps.CrystalCaves, Regions.CrystalCavesMain, Regions.FunkyCaves),
        ShopLocation(Regions.Snide, Maps.CrystalCaves, Regions.CavesSnideArea, Regions.Snide),
    ],
    Levels.CreepyCastle: [
        ShopLocation(Regions.CrankyGeneric, Maps.CreepyCastle, Regions.CreepyCastleMain, Regions.CrankyCastle),
        ShopLocation(Regions.CandyGeneric, Maps.CastleUpperCave, Regions.UpperCave, Regions.CandyCastle),
        ShopLocation(Regions.FunkyGeneric, Maps.CastleLowerCave, Regions.LowerCave, Regions.FunkyCastle),
        ShopLocation(Regions.Snide, Maps.CreepyCastle, Regions.CreepyCastleMain, Regions.Snide),
    ],
}


def ShuffleShopLocations(spoiler: Spoiler):
    """Shuffle Shop locations within their own pool inside the level."""
    # Reset
    for level in available_shops:
        shop_array = available_shops[level]
        for shop in shop_array:
            shop.setShop(shop)
    # Shuffle
    assortment = {}
    for level in available_shops:
        # Don't shuffle Isles shops in entrance rando. This prevents having the one-entrance-locked Isles Snide room from being progression.
        if level == Levels.DKIsles and spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all:
            continue
        shop_array = available_shops[level]
        # Get list of shops in level
        shops_in_levels = []
        for shop in shop_array:
            if not shop.locked:
                # This is a valid shop to shuffle, so we need to remove all preexisting logical access, wherever it is
                possible_containing_region_ids = [shop_location.containing_region for shop_location in shop_array]
                for region_id in possible_containing_region_ids:
                    old_region = Logic.Regions[region_id]
                    old_region.exits = [exit for exit in old_region.exits if exit.dest != shop.shop_exit]
                shops_in_levels.append(shop)
        random.shuffle(shops_in_levels)
        # Assign shuffle to data
        assortment_in_level = {}
        placement_index = 0
        for shop_index, shop in enumerate(shop_array):
            if not shop.locked:
                shop.setShop(shops_in_levels[placement_index])
                assortment_in_level[shop.shop] = shop.new_shop
                placement_index += 1
                # Add exit to new containing region for logical access
                region = Logic.Regions[shop.containing_region]
                region.exits.append(TransitionFront(shop.new_shop_exit, lambda l: True))
        assortment[level] = assortment_in_level
    # Write Assortment to spoiler
    spoiler.shuffled_shop_locations = assortment
