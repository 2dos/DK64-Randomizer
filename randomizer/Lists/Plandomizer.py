"""Various lists to support the plandomizer."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Songs import Songs
from randomizer.Enums.SongType import SongType
from randomizer.Enums.Types import Types
from randomizer.Enums.VendorType import VendorType
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.MapsAndExits import RegionMapList
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.LogicFiles.AngryAztec import LogicRegions as AngryAztecRegions
from randomizer.LogicFiles.CreepyCastle import LogicRegions as CreepyCastleRegions
from randomizer.LogicFiles.CrystalCaves import LogicRegions as CrystalCavesRegions
from randomizer.LogicFiles.DKIsles import LogicRegions as DKIslesRegions
from randomizer.LogicFiles.FranticFactory import LogicRegions as FranticFactoryRegions
from randomizer.LogicFiles.FungiForest import LogicRegions as FungiForestRegions
from randomizer.LogicFiles.GloomyGalleon import LogicRegions as GloomyGalleonRegions
from randomizer.LogicFiles.JungleJapes import LogicRegions as JungleJapesRegions


def getKongString(kongEnum: Kongs) -> str:
    """Get the string name of the kong from the enum."""
    if kongEnum == Kongs.donkey:
        return "Donkey"
    elif kongEnum == Kongs.diddy:
        return "Diddy"
    elif kongEnum == Kongs.lanky:
        return "Lanky"
    elif kongEnum == Kongs.tiny:
        return "Tiny"
    elif kongEnum == Kongs.chunky:
        return "Chunky"
    else:
        return "All Kongs"


def getLevelString(levelEnum: Levels) -> str:
    """Get the string name of a level from the enum."""
    if levelEnum == Levels.DKIsles:
        return "D.K. Isles"
    elif levelEnum == Levels.JungleJapes:
        return "Jungle Japes"
    elif levelEnum == Levels.AngryAztec:
        return "Angry Aztec"
    elif levelEnum == Levels.FranticFactory:
        return "Frantic Factory"
    elif levelEnum == Levels.GloomyGalleon:
        return "Gloomy Galleon"
    elif levelEnum == Levels.FungiForest:
        return "Fungi Forest"
    elif levelEnum == Levels.CrystalCaves:
        return "Crystal Caves"
    elif levelEnum == Levels.CreepyCastle:
        return "Creepy Castle"
    elif levelEnum == Levels.HideoutHelm:
        return "Hideout Helm"
    elif levelEnum == Levels.Shops:
        return "Shops"
    else:
        return None


# Some useful lists of locations. These will mostly be used for on-the-fly
# input validation. They will be populated as we build out other data
# structures.

# A list of all locations where items can be placed.
ItemLocationList = []
# A list of all shop locations.
ShopLocationList = []
# A list of all minigame locations.
MinigameLocationList = []
# A list of all hint locations.
HintLocationList = []

# Additional lists we need in order to disable certain locations.
CrownLocationList = []
DirtPatchLocationList = []
FairyLocationList = []
KasplatLocationList = []
MelonCrateLocationList = []


def createShopLocationKongMapObj() -> dict:
    """Initialize an entry in the ShopLocationKongMap."""
    return {VendorType.Candy.name: {"shared": None, "individual": []}, VendorType.Cranky.name: {"shared": None, "individual": []}, VendorType.Funky.name: {"shared": None, "individual": []}}


# A map of shop locations, grouped by level and broken into shared/individual.
ShopLocationKongMap = {
    "DKIsles": createShopLocationKongMapObj(),
    "JungleJapes": createShopLocationKongMapObj(),
    "AngryAztec": createShopLocationKongMapObj(),
    "FranticFactory": createShopLocationKongMapObj(),
    "GloomyGalleon": createShopLocationKongMapObj(),
    "FungiForest": createShopLocationKongMapObj(),
    "CrystalCaves": createShopLocationKongMapObj(),
    "CreepyCastle": createShopLocationKongMapObj(),
}

##########
# PANELS #
##########


def createPlannableLocationObj() -> dict:
    """Initialize the plannable location object."""
    return {"All Kongs": [], "Donkey": [], "Diddy": [], "Lanky": [], "Tiny": [], "Chunky": [], "Enemies": []}


def isMinigameLocation(locationEnum: Locations) -> bool:
    """Determine if this location is a minigame location."""
    return locationEnum in BarrelMetaData


PlandomizerPanels = {
    "DKIsles": {"name": "D.K. Isles", "locations": createPlannableLocationObj()},
    "JungleJapes": {"name": "Jungle Japes", "locations": createPlannableLocationObj()},
    "AngryAztec": {"name": "Angry Aztec", "locations": createPlannableLocationObj()},
    "FranticFactory": {"name": "Frantic Factory", "locations": createPlannableLocationObj()},
    "GloomyGalleon": {"name": "Gloomy Galleon", "locations": createPlannableLocationObj()},
    "FungiForest": {"name": "Fungi Forest", "locations": createPlannableLocationObj()},
    "CrystalCaves": {"name": "Crystal Caves", "locations": createPlannableLocationObj()},
    "CreepyCastle": {"name": "Creepy Castle", "locations": createPlannableLocationObj()},
    "HideoutHelm": {"name": "Hideout Helm", "locations": {"All Kongs": [], "Medals": [], "Enemies": []}},
    # Shops, minigames and hints are grouped by level, not by Kong.
    "Shops": {
        "name": "Shops",
        "levels": {
            "DKIsles": {"name": "D.K. Isles", "locations": []},
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
        },
    },
    # "Blueprints": {
    #    "name": "Blueprints",
    #    "locations": createPlannableLocationObj()
    # },
    "Minigames": {
        "name": "Minigames",
        "levels": {
            "DKIsles": {"name": "D.K. Isles", "locations": []},
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
            "HideoutHelm": {"name": "Hideout Helm", "locations": []},
        },
    },
    "Hints": {
        "name": "Hints",
        "levels": {
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
        },
    },
}
for locationEnum, locationObj in LocationList.items():
    # Do not randomize constant rewards.
    if locationObj.type == Types.Constant:
        continue
    # Do not include training barrels or pre-given move locations. We will fill
    # those automatically based on the user's selected starting moves.
    if locationObj.type in [Types.TrainingBarrel, Types.PreGivenMove]:
        continue
    locationJson = {"name": locationObj.name, "value": locationEnum.name}
    kongString = getKongString(locationObj.kong)
    if locationObj.type == Types.BlueprintBanana:
        # PlandomizerPanels["Blueprints"]["locations"][kongString].append(locationJson)
        continue
    elif locationObj.type == Types.Hint:
        levelName = locationObj.level.name
        PlandomizerPanels["Hints"]["levels"][levelName]["locations"].append(locationJson)
        HintLocationList.append(locationEnum.name)
    elif locationObj.type == Types.Shop:
        levelName = locationObj.level.name
        PlandomizerPanels["Shops"]["levels"][levelName]["locations"].append(locationJson)
        ShopLocationList.append(locationEnum.name)
        # Add this to the ShopLocationKongMap, which will be used for validation.
        vendor = locationObj.vendor.name
        if locationObj.kong == Kongs.any:
            ShopLocationKongMap[levelName][vendor]["shared"] = {"name": locationEnum.name, "value": locationObj}
        else:
            ShopLocationKongMap[levelName][vendor]["individual"].append({"name": locationEnum.name, "value": locationObj})
    elif locationObj.level == Levels.Shops:
        # This is the Rareware coin.
        PlandomizerPanels["Shops"]["levels"]["DKIsles"]["locations"].append(locationJson)
        ShopLocationList.append(locationEnum.name)
    else:
        levelName = locationObj.level.name
        if locationObj.level == Levels.HideoutHelm and locationObj.type == Types.Medal:
            PlandomizerPanels[levelName]["locations"]["Medals"].append(locationJson)
        elif locationObj.type == Types.Enemies:
            PlandomizerPanels[levelName]["locations"]["Enemies"].append(locationJson)
        else:
            PlandomizerPanels[levelName]["locations"][kongString].append(locationJson)
        ItemLocationList.append(locationEnum.name)

        # We need to keep track of locations for dirt patches, fairies, arenas,
        # melon crates, and Kasplats.
        if locationObj.type == Types.Crown:
            CrownLocationList.append(locationEnum.name)
        elif locationObj.type == Types.RainbowCoin:
            DirtPatchLocationList.append(locationEnum.name)
        elif locationObj.type == Types.Fairy:
            FairyLocationList.append(locationEnum.name)
        elif locationObj.type == Types.Blueprint:
            KasplatLocationList.append(locationEnum.name)
        elif locationObj.type == Types.CrateItem:
            MelonCrateLocationList.append(locationEnum.name)

        # If this is a minigame location, add it to the Minigames list.
        if isMinigameLocation(locationEnum):
            PlandomizerPanels["Minigames"]["levels"][levelName]["locations"].append({"name": locationObj.name, "value": locationEnum.name, "kong": kongString})
            MinigameLocationList.append(locationEnum.name)

# Hideout Helm minigame locations get manually added here, as they're not
# locations where rewards can be placed, so they don't get naturally added.
PlandomizerPanels["Minigames"]["levels"]["HideoutHelm"]["locations"] = [
    {"name": "Helm Donkey 1", "value": "HelmDonkey1", "kong": "Donkey"},
    {"name": "Helm Donkey 2", "value": "HelmDonkey2", "kong": "Donkey"},
    {"name": "Helm Diddy 1", "value": "HelmDiddy1", "kong": "Diddy"},
    {"name": "Helm Diddy 2", "value": "HelmDiddy2", "kong": "Diddy"},
    {"name": "Helm Lanky 1", "value": "HelmLanky1", "kong": "Lanky"},
    {"name": "Helm Lanky 2", "value": "HelmLanky2", "kong": "Lanky"},
    {"name": "Helm Tiny 1", "value": "HelmTiny1", "kong": "Tiny"},
    {"name": "Helm Tiny 2", "value": "HelmTiny2", "kong": "Tiny"},
    {"name": "Helm Chunky 1", "value": "HelmChunky1", "kong": "Chunky"},
    {"name": "Helm Chunky 2", "value": "HelmChunky2", "kong": "Chunky"},
]
MinigameLocationList += ["HelmDonkey1", "HelmDonkey2", "HelmDiddy1", "HelmDiddy2", "HelmLanky1", "HelmLanky2", "HelmTiny1", "HelmTiny2", "HelmChunky1", "HelmChunky2"]

#########
# ITEMS #
#########

# These PlandoItems enums have multiple Items enums that map to each of them,
# and so they should not be automatically added to the list of PlannableItems.
# Handle these manually.
doNotAutoAddPlandoItemSet = {PlandoItems.DonkeyBlueprint, PlandoItems.DiddyBlueprint, PlandoItems.LankyBlueprint, PlandoItems.TinyBlueprint, PlandoItems.ChunkyBlueprint, PlandoItems.JunkItem}
# These items are extras that map to PlandoItems already covered by other
# Items. Do not add these.
doNotAutoAddItemSet = {Items.ProgressiveSlam2, Items.ProgressiveSlam3, Items.ProgressiveAmmoBelt2, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3}

PlannableItems = []  # Used to select rewards for locations.

for itemEnum, itemObj in ItemList.items():
    # Only include items that have a matching item in the plando map.
    if itemEnum not in ItemToPlandoItemMap:
        continue
    # Do not include items in this set.
    if itemEnum in doNotAutoAddItemSet:
        continue

    plandoItemEnum = ItemToPlandoItemMap[itemEnum]
    # Do not add blueprints or junk items. These will be replaced with generic
    # items.
    if plandoItemEnum in doNotAutoAddPlandoItemSet:
        continue
    itemJson = {"name": itemObj.name, "value": plandoItemEnum.name}
    PlannableItems.append(itemJson)

PlannableItems.append({"name": "Blueprint (Donkey)", "value": "DonkeyBlueprint"})
PlannableItems.append({"name": "Blueprint (Diddy)", "value": "DiddyBlueprint"})
PlannableItems.append({"name": "Blueprint (Lanky)", "value": "LankyBlueprint"})
PlannableItems.append({"name": "Blueprint (Tiny)", "value": "TinyBlueprint"})
PlannableItems.append({"name": "Blueprint (Chunky)", "value": "ChunkyBlueprint"})
PlannableItems.append({"name": "Junk Item", "value": "JunkItem"})
PlannableItems.append({"name": "Random Kong", "value": "RandomKong"})
PlannableItems.append({"name": "Random Move", "value": "RandomMove"})
PlannableItems.append({"name": "Random Kong Move", "value": "RandomKongMove"})
PlannableItems.append({"name": "Random Shared Move", "value": "RandomSharedMove"})
PlannableItems.append({"name": "Random Key", "value": "RandomKey"})
PlannableItems.append({"name": "Random Collectible", "value": "RandomItem"})

# The maximum amount of each item that the user is allowed to place.
# If a plando item is not here, that item has no limit.
PlannableItemLimits = {
    PlandoItems.Donkey: 1,
    PlandoItems.Diddy: 1,
    PlandoItems.Lanky: 1,
    PlandoItems.Tiny: 1,
    PlandoItems.Chunky: 1,
    PlandoItems.Vines: 1,
    PlandoItems.Swim: 1,
    PlandoItems.Oranges: 1,
    PlandoItems.Barrels: 1,
    PlandoItems.ProgressiveSlam: 3,
    PlandoItems.BaboonBlast: 1,
    PlandoItems.StrongKong: 1,
    PlandoItems.GorillaGrab: 1,
    PlandoItems.ChimpyCharge: 1,
    PlandoItems.RocketbarrelBoost: 1,
    PlandoItems.SimianSpring: 1,
    PlandoItems.Orangstand: 1,
    PlandoItems.BaboonBalloon: 1,
    PlandoItems.OrangstandSprint: 1,
    PlandoItems.MiniMonkey: 1,
    PlandoItems.PonyTailTwirl: 1,
    PlandoItems.Monkeyport: 1,
    PlandoItems.HunkyChunky: 1,
    PlandoItems.PrimatePunch: 1,
    PlandoItems.GorillaGone: 1,
    PlandoItems.Coconut: 1,
    PlandoItems.Peanut: 1,
    PlandoItems.Grape: 1,
    PlandoItems.Feather: 1,
    PlandoItems.Pineapple: 1,
    PlandoItems.HomingAmmo: 1,
    PlandoItems.SniperSight: 1,
    PlandoItems.ProgressiveAmmoBelt: 2,
    PlandoItems.Bongos: 1,
    PlandoItems.Guitar: 1,
    PlandoItems.Trombone: 1,
    PlandoItems.Saxophone: 1,
    PlandoItems.Triangle: 1,
    PlandoItems.ProgressiveInstrumentUpgrade: 3,
    PlandoItems.Camera: 1,
    PlandoItems.Shockwave: 1,
    PlandoItems.NintendoCoin: 1,
    PlandoItems.RarewareCoin: 1,
    PlandoItems.JungleJapesKey: 1,
    PlandoItems.AngryAztecKey: 1,
    PlandoItems.FranticFactoryKey: 1,
    PlandoItems.GloomyGalleonKey: 1,
    PlandoItems.FungiForestKey: 1,
    PlandoItems.CrystalCavesKey: 1,
    PlandoItems.CreepyCastleKey: 1,
    PlandoItems.HideoutHelmKey: 1,
    # Forty of these bananas are currently allocated to blueprint rewards.
    PlandoItems.GoldenBanana: 201,
    PlandoItems.BananaFairy: 20,
    PlandoItems.BananaMedal: 40,
    PlandoItems.BattleCrown: 10,
    PlandoItems.Bean: 1,
    PlandoItems.Pearl: 5,
    PlandoItems.FakeItem: 16,
    PlandoItems.JunkItem: 100,
    PlandoItems.RainbowCoin: 16,
    PlandoItems.DonkeyBlueprint: 8,
    PlandoItems.DiddyBlueprint: 8,
    PlandoItems.LankyBlueprint: 8,
    PlandoItems.TinyBlueprint: 8,
    PlandoItems.ChunkyBlueprint: 8,
}

# The maximum amount of items from each group that the user is allowed to
# place. This includes the individual items as well as the "random" item.
PlannableGroupLimits = {
    PlandoItems.RandomKong: 5,
    PlandoItems.RandomMove: 41,
    PlandoItems.RandomKongMove: 25,
    PlandoItems.RandomSharedMove: 16,
    PlandoItems.RandomKey: 8,
    PlandoItems.RandomItem: 293,
}

#############
# MINIGAMES #
#############

PlannableMinigames = []
for minigameEnum, minigameObj in MinigameRequirements.items():
    # NoGame is an invalid selection.
    if minigameEnum == Minigames.NoGame:
        continue
    minigameJson = {"name": minigameObj.name, "value": minigameEnum.name}
    PlannableMinigames.append(minigameJson)

###################
# SPAWN LOCATIONS #
###################

PlannableSpawns = []

# A dictionary for sorting locations by hint_name. This is filled in
# programmatically, because hint regions may change and we don't want to adjust
# this dictionary every time hint regions change.
hintNameSortDict = {
    Levels.DKIsles: dict(),
    Levels.JungleJapes: dict(),
    Levels.AngryAztec: dict(),
    Levels.FranticFactory: dict(),
    Levels.GloomyGalleon: dict(),
    Levels.FungiForest: dict(),
    Levels.CrystalCaves: dict(),
    Levels.CreepyCastle: dict(),
}

# Go through each level and add the valid spawn locations.
allSpawnableLevels = [DKIslesRegions, JungleJapesRegions, AngryAztecRegions, FranticFactoryRegions, GloomyGalleonRegions, FungiForestRegions, CrystalCavesRegions, CreepyCastleRegions]
for level in allSpawnableLevels:
    # Remove locations we should not spawn into (such as the credits).
    filteredLocations = dict(filter(lambda x: x[0] in RegionMapList, level.items()))

    # Populate the sorting dictionary.
    for regionObj in filteredLocations.values():
        hintName = regionObj.hint_name
        hintNameDict = hintNameSortDict[regionObj.level]
        if hintName not in hintNameDict:
            numRegions = len(hintNameDict)
            hintNameDict[hintName] = numRegions + 1

    # Sort by hint name, for better readability.
    def spawnKey(loc):
        """Do something."""
        _, regionObj = loc
        return hintNameSortDict[regionObj.level][regionObj.hint_name]

    sortedLocations = dict(sorted(filteredLocations.items(), key=spawnKey))

    for regionEnum, regionObj in sortedLocations.items():
        regionJson = {"name": f"{getLevelString(regionObj.level)}: {regionObj.hint_name} - {regionObj.name}", "value": regionEnum.name}
        PlannableSpawns.append(regionJson)
