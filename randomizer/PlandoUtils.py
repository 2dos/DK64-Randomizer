"""Includes utility functions for plandomizer support."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems
from randomizer.Enums.Types import Types
from randomizer.Lists.Location import LocationList

bananaFairyPermittedItems = {
    PlandoItems.NoItem.name,
    PlandoItems.Donkey.name,
    PlandoItems.Diddy.name,
    PlandoItems.Lanky.name,
    PlandoItems.Tiny.name,
    PlandoItems.Chunky.name,
    PlandoItems.Vines.name,
    PlandoItems.Swim.name,
    PlandoItems.Oranges.name,
    PlandoItems.Barrels.name,
    PlandoItems.ProgressiveSlam.name,
    PlandoItems.BaboonBlast.name,
    PlandoItems.StrongKong.name,
    PlandoItems.GorillaGrab.name,
    PlandoItems.ChimpyCharge.name,
    PlandoItems.RocketbarrelBoost.name,
    PlandoItems.SimianSpring.name,
    PlandoItems.Orangstand.name,
    PlandoItems.BaboonBalloon.name,
    PlandoItems.OrangstandSprint.name,
    PlandoItems.MiniMonkey.name,
    PlandoItems.PonyTailTwirl.name,
    PlandoItems.Monkeyport.name,
    PlandoItems.HunkyChunky.name,
    PlandoItems.PrimatePunch.name,
    PlandoItems.GorillaGone.name,
    PlandoItems.JungleJapesKey.name,
    PlandoItems.AngryAztecKey.name,
    PlandoItems.FranticFactoryKey.name,
    PlandoItems.GloomyGalleonKey.name,
    PlandoItems.FungiForestKey.name,
    PlandoItems.CrystalCavesKey.name,
    PlandoItems.CreepyCastleKey.name,
    PlandoItems.HideoutHelmKey.name,
    PlandoItems.GoldenBanana.name,
    PlandoItems.BananaFairy.name,
    PlandoItems.BattleCrown.name,
    PlandoItems.FakeItem.name
}

# For every location in LocationList, if the default reward is a Banana Fairy,
# add the string name of that location enum to this set.
bananaFairyLocationSet = {locEnum.name for (locEnum, locObj) in LocationList.items() if locObj.default == Items.BananaFairy}

kongPermittedItemSet = {
    PlandoItems.NoItem.name,
    PlandoItems.Donkey.name,
    PlandoItems.Diddy.name,
    PlandoItems.Lanky.name,
    PlandoItems.Tiny.name,
    PlandoItems.Chunky.name
}

kongLocationSet = {
    Locations.DiddyKong.name,
    Locations.TinyKong.name,
    Locations.LankyKong.name,
    Locations.ChunkyKong.name
}

shopRestrictedItemSet = {
    PlandoItems.JunkItem.name
}

shopLocationSet = set()
for (locEnum, locObj) in LocationList.items():
    if locObj.type == Types.Shop:
        shopLocationSet.add(locEnum.name)
    elif locObj.level == Levels.Shops:
        shopLocationSet.add(locEnum.name)

def PlandoItemFilter(itemList, location):
    """A Jinja filter that returns a filtered list of plando items that are
       permitted at the given location.
       
       Args:
           itemList (dict[]): The list of possible plando items. Each item
               contains "display_name" and "enum_name" string fields.
           location (str): The location where we are trying to place items.
               Equal to the string name of the Location enum.
    """

    # Kong locations (not Kong rewards) are heavily limited.
    if location["enum_name"] in kongLocationSet:
        # For every item in the item list, if it's in our set of permitted items for
        # Kong locations, add it to a new list. Return that new list.
        return [item for item in itemList if item["enum_name"] in kongPermittedItemSet]

    # Banana fairy locations have some limitations.
    if location["enum_name"] in bananaFairyLocationSet:
        # For every item in the item list, if it's in our set of permitted items for
        # Banana Fairy locations, add it to a new list. Return that new list.
        return [item for item in itemList if item["enum_name"] in bananaFairyPermittedItems]
    
    # Shops have very few limitations.
    if location["enum_name"] in shopLocationSet:
        # For every item in the item list, if it's not in our set of restricted
        # items for shop locations, add it to a new list. Return that new list.
        return [item for item in itemList if item["enum_name"] not in shopRestrictedItemSet]

    # If we've gotten to this point, we have no filters to perform.
    # We can return the full list.
    return itemList

# A dictionary indicating which mini-games are unavailable to certain Kongs.
kongMinigameRestrictions = {
    "Donkey": {
        Minigames.DiddyRocketbarrel.name,
        Minigames.TinyPonyTailTwirl.name,
        Minigames.ChunkyHiddenKremling.name
    },
    "Diddy": {
        Minigames.SpeedySwingSortieNormal.name,
        Minigames.DonkeyTarget.name,
        Minigames.TinyPonyTailTwirl.name,
        Minigames.ChunkyHiddenKremling.name
    },
    "Lanky": {
        Minigames.BusyBarrelBarrageEasy.name,
        Minigames.BusyBarrelBarrageNormal.name,
        Minigames.BusyBarrelBarrageHard.name,
        Minigames.SpeedySwingSortieNormal.name,
        Minigames.DonkeyTarget.name,
        Minigames.TinyPonyTailTwirl.name,
        Minigames.ChunkyHiddenKremling.name
    },
    "Tiny": {
        Minigames.DonkeyTarget.name,
        Minigames.ChunkyHiddenKremling.name
    },
    "Chunky": {
        Minigames.SpeedySwingSortieNormal.name,
        Minigames.DonkeyTarget.name,
        Minigames.TinyPonyTailTwirl.name
    }
}

def PlandoMinigameFilter(minigameList, kong):
    """A Jinja filter that returns a filtered list of minigames that can be
       played by each Kong. This will prevent the user from placing impossible
       minigames in locations that only certain Kongs can access.
       
       Args:
           minigameList (str[]): The list of possible minigames.
           kong (str): The Kong who will be playing the minigame.
    """
    if kong == "All Kongs":
        return minigameList
    return [game for game in minigameList if game["enum_name"] not in kongMinigameRestrictions[kong]]

invalidTabPanels = {
    "Blueprints"
}

def PlandoPanelFilter(locationDict):
    """A Jinja filter that returns a filtered dict of plando panels that
       we want the user to interact with. This feeds the list of visible tabs
       and panels on the plando page. (This includes Shops, Blueprints and
       Hints.)

       Currently, we do not want to display the Blueprints tab, as blueprint
       rewards cannot be shuffled.
       
       Args:
           locationDict (dict[]): The dict of possible locations/tabs/panels.
           We are only interested in the keys.
    """
    return {locName:locObj for (locName, locObj) in locationDict.items() if locName not in invalidTabPanels}

# This dictionary allows us to efficiently sort the shop locations. Shops are
# sorted first by level, then by vendor, then by Kong. This sorting is easier
# to visually browse, as a user.
#
# The keys are the enum names, not the enum values, because names are what will
# be provided to the sorting function.
shopLocationOrderingDict = {
    Locations.SimianSlam.name: 1,  # DK Isles Cranky Shared
    Locations.DonkeyIslesPotion.name: 2,  # DK Isles Cranky Donkey
    Locations.DiddyIslesPotion.name: 3,  # DK Isles Cranky Diddy
    Locations.LankyIslesPotion.name: 4,  # DK Isles Cranky Lanky
    Locations.TinyIslesPotion.name: 5,  # DK Isles Cranky Tiny
    Locations.ChunkyIslesPotion.name: 6,  # DK Isles Cranky Chunky

    Locations.SharedJapesPotion.name: 7,  # Japes Cranky Shared
    Locations.BaboonBlast.name: 8,  # Japes Cranky Donkey
    Locations.ChimpyCharge.name: 9,  # Japes Cranky Diddy
    Locations.Orangstand.name: 10,  # Japes Cranky Lanky
    Locations.MiniMonkey.name: 11,  # Japes Cranky Tiny
    Locations.HunkyChunky.name: 12,  # Japes Cranky Chunky
    Locations.SharedJapesGun.name: 13,  # Japes Funky Shared
    Locations.CoconutGun.name: 14,  # Japes Funky Donkey
    Locations.PeanutGun.name: 15,  # Japes Funky Diddy
    Locations.GrapeGun.name: 16,  # Japes Funky Lanky
    Locations.FeatherGun.name: 17,  # Japes Funky Tiny
    Locations.PineappleGun.name: 18,  # Japes Funky Chunky

    Locations.SharedAztecPotion.name: 19,  # Aztec Cranky Shared
    Locations.StrongKong.name: 20,  # Aztec Cranky Donkey
    Locations.RocketbarrelBoost.name: 21,  # Aztec Cranky Diddy
    Locations.LankyAztecPotion.name: 22,  # Aztec Cranky Lanky
    Locations.TinyAztecPotion.name: 23,  # Aztec Cranky Tiny
    Locations.ChunkyAztecPotion.name: 24,  # Aztec Cranky Chunky
    Locations.SharedAztecGun.name: 25,  # Aztec Funky Shared
    Locations.DonkeyAztecGun.name: 26,  # Aztec Funky Donkey
    Locations.DiddyAztecGun.name: 27,  # Aztec Funky Diddy
    Locations.LankyAztecGun.name: 28,  # Aztec Funky Lanky
    Locations.TinyAztecGun.name: 29,  # Aztec Funky Tiny
    Locations.ChunkyAztecGun.name: 30,  # Aztec Funky Chunky
    Locations.SharedAztecInstrument.name: 31,  # Aztec Candy Shared
    Locations.Bongos.name: 32,  # Aztec Candy Donkey
    Locations.Guitar.name: 33,  # Aztec Candy Diddy
    Locations.Trombone.name: 34,  # Aztec Candy Lanky
    Locations.Saxophone.name: 35,  # Aztec Candy Tiny
    Locations.Triangle.name: 36,  # Aztec Candy Chunky

    Locations.SharedFactoryPotion.name: 37,  # Factory Cranky Shared
    Locations.GorillaGrab.name: 38,  # Factory Cranky Donkey
    Locations.SimianSpring.name: 39,  # Factory Cranky Diddy
    Locations.BaboonBalloon.name: 40,  # Factory Cranky Lanky
    Locations.PonyTailTwirl.name: 41,  # Factory Cranky Tiny
    Locations.PrimatePunch.name: 42,  # Factory Cranky Chunky
    Locations.AmmoBelt1.name: 43,  # Factory Funky Shared
    Locations.DonkeyFactoryGun.name: 44,  # Factory Funky Donkey
    Locations.DiddyFactoryGun.name: 45,  # Factory Funky Diddy
    Locations.LankyFactoryGun.name: 46,  # Factory Funky Lanky
    Locations.TinyFactoryGun.name: 47,  # Factory Funky Tiny
    Locations.ChunkyFactoryGun.name: 48,  # Factory Funky Chunky
    Locations.SharedFactoryInstrument.name: 49,  # Factory Candy Shared
    Locations.DonkeyFactoryInstrument.name: 50,  # Factory Candy Donkey
    Locations.DiddyFactoryInstrument.name: 51,  # Factory Candy Diddy
    Locations.LankyFactoryInstrument.name: 52,  # Factory Candy Lanky
    Locations.TinyFactoryInstrument.name: 53,  # Factory Candy Tiny
    Locations.ChunkyFactoryInstrument.name: 54,  # Factory Candy Chunky

    Locations.SharedGalleonPotion.name: 55,  # Galleon Cranky Shared
    Locations.DonkeyGalleonPotion.name: 56,  # Galleon Cranky Donkey
    Locations.DiddyGalleonPotion.name: 57,  # Galleon Cranky Diddy
    Locations.LankyGalleonPotion.name: 58,  # Galleon Cranky Lanky
    Locations.TinyGalleonPotion.name: 59,  # Galleon Cranky Tiny
    Locations.ChunkyGalleonPotion.name: 60,  # Galleon Cranky Chunky
    Locations.SharedGalleonGun.name: 61,  # Galleon Funky Shared
    Locations.DonkeyGalleonGun.name: 62,  # Galleon Funky Donkey
    Locations.DiddyGalleonGun.name: 63,  # Galleon Funky Diddy
    Locations.LankyGalleonGun.name: 64,  # Galleon Funky Lanky
    Locations.TinyGalleonGun.name: 65,  # Galleon Funky Tiny
    Locations.ChunkyGalleonGun.name: 66,  # Galleon Funky Chunky
    Locations.MusicUpgrade1.name: 67,  # Galleon Candy Shared
    Locations.DonkeyGalleonInstrument.name: 68,  # Galleon Candy Donkey
    Locations.DiddyGalleonInstrument.name: 69,  # Galleon Candy Diddy
    Locations.LankyGalleonInstrument.name: 70,  # Galleon Candy Lanky
    Locations.TinyGalleonInstrument.name: 71,  # Galleon Candy Tiny
    Locations.ChunkyGalleonInstrument.name: 72,  # Galleon Candy Chunky

    Locations.SuperSimianSlam.name: 73,  # Forest Cranky Shared
    Locations.DonkeyForestPotion.name: 74,  # Forest Cranky Donkey
    Locations.DiddyForestPotion.name: 75,  # Forest Cranky Diddy
    Locations.LankyForestPotion.name: 76,  # Forest Cranky Lanky
    Locations.TinyForestPotion.name: 77,  # Forest Cranky Tiny
    Locations.ChunkyForestPotion.name: 78,  # Forest Cranky Chunky
    Locations.HomingAmmo.name: 79,  # Forest Funky Shared
    Locations.DonkeyForestGun.name: 80,  # Forest Funky Donkey
    Locations.DiddyForestGun.name: 81,  # Forest Funky Diddy
    Locations.LankyForestGun.name: 82,  # Forest Funky Lanky
    Locations.TinyForestGun.name: 83,  # Forest Funky Tiny
    Locations.ChunkyForestGun.name: 84,  # Forest Funky Chunky

    Locations.SharedCavesPotion.name: 85,  # Caves Cranky Shared
    Locations.DonkeyCavesPotion.name: 86,  # Caves Cranky Donkey
    Locations.DiddyCavesPotion.name: 87,  # Caves Cranky Diddy
    Locations.OrangstandSprint.name: 88,  # Caves Cranky Lanky
    Locations.Monkeyport.name: 89,  # Caves Cranky Tiny
    Locations.GorillaGone.name: 90,  # Caves Cranky Chunky
    Locations.AmmoBelt2.name: 91,  # Caves Funky Shared
    Locations.DonkeyCavesGun.name: 92,  # Caves Funky Donkey
    Locations.DiddyCavesGun.name: 93,  # Caves Funky Diddy
    Locations.LankyCavesGun.name: 94,  # Caves Funky Lanky
    Locations.TinyCavesGun.name: 95,  # Caves Funky Tiny
    Locations.ChunkyCavesGun.name: 96,  # Caves Funky Chunky
    Locations.ThirdMelon.name: 97,  # Caves Candy Shared
    Locations.DonkeyCavesInstrument.name: 98,  # Caves Canky Donkey
    Locations.DiddyCavesInstrument.name: 99,  # Caves Candy Diddy
    Locations.LankyCavesInstrument.name: 100,  # Caves Candy Lanky
    Locations.TinyCavesInstrument.name: 101,  # Caves Candy Tiny
    Locations.ChunkyCavesInstrument.name: 102,  # Caves Candy Chunky

    Locations.SuperDuperSimianSlam.name: 103,  # Castle Cranky Shared
    Locations.DonkeyCastlePotion.name: 104,  # Castle Cranky Donkey
    Locations.DiddyCastlePotion.name: 105,  # Castle Cranky Diddy
    Locations.LankyCastlePotion.name: 106,  # Castle Cranky Lanky
    Locations.TinyCastlePotion.name: 107,  # Castle Cranky Tiny
    Locations.ChunkyCastlePotion.name: 108,  # Castle Cranky Chunky
    Locations.SniperSight.name: 109,  # Castle Funky Shared
    Locations.DonkeyCastleGun.name: 110,  # Castle Funky Donkey
    Locations.DiddyCastleGun.name: 111,  # Castle Funky Diddy
    Locations.LankyCastleGun.name: 112,  # Castle Funky Lanky
    Locations.TinyCastleGun.name: 113,  # Castle Funky Tiny
    Locations.ChunkyCastleGun.name: 114,  # Castle Funky Chunky
    Locations.MusicUpgrade2.name: 115,  # Castle Candy Shared
    Locations.DonkeyCastleInstrument.name: 116,  # Castle Candy Donkey
    Locations.DiddyCastleInstrument.name: 117,  # Castle Candy Diddy
    Locations.LankyCastleInstrument.name: 118,  # Castle Candy Lanky
    Locations.TinyCastleInstrument.name: 119,  # Castle Candy Tiny
    Locations.ChunkyCastleInstrument.name: 120,  # Castle Candy Chunky

    Locations.RarewareCoin.name: 121  # Jetpac
}

def PlandoShopSortFilter(shopLocationList):
    """A Jinja filter that returns a sorted list of shop locations. These are
       sorted by level, then by vendor, then by Kong. This makes the full list
       easier to browse.
       
       Args:
           shopLocationList (str[]): The list of all shop locations.
    """
    def shopKey(shopLocation):
        return shopLocationOrderingDict[shopLocation["enum_name"]]
    
    return sorted(shopLocationList, key=shopKey)
