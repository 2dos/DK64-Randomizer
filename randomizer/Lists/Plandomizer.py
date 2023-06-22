"""Various lists to support the plandomizer."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import LocationList
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

def getKongString(kongEnum):
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

def getLevelString(levelEnum):
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
# A list of all hint locations.
HintLocationList = []

##########
# PANELS #
##########

def createPlannableLocationObj():
    return {
        "All Kongs": [],
        "Donkey": [],
        "Diddy": [],
        "Lanky": [],
        "Tiny": [],
        "Chunky": []
    }

def isMinigameLocation(locationEnum):
    return locationEnum in BarrelMetaData

PlandomizerPanels = {
    "DKIsles": {
        "display_name": "D.K. Isles",
        "locations": createPlannableLocationObj()
    },
    "JungleJapes": {
        "display_name": "Jungle Japes",
        "locations": createPlannableLocationObj()
    },
    "AngryAztec": {
        "display_name": "Angry Aztec",
        "locations": createPlannableLocationObj()
    },
    "FranticFactory": {
        "display_name": "Frantic Factory",
        "locations": createPlannableLocationObj()
    },
    "GloomyGalleon": {
        "display_name": "Gloomy Galleon",
        "locations": createPlannableLocationObj()
    },
    "FungiForest": {
        "display_name": "Fungi Forest",
        "locations": createPlannableLocationObj()
    },
    "CrystalCaves": {
        "display_name": "Crystal Caves",
        "locations": createPlannableLocationObj()
    },
    "CreepyCastle": {
        "display_name": "Creepy Castle",
        "locations": createPlannableLocationObj()
    },
    "HideoutHelm": {
        "display_name": "Hideout Helm",
        "locations": createPlannableLocationObj()
    },
    "Shops": {
        "display_name": "Shops",
        "locations": createPlannableLocationObj()
    },
    "Blueprints": {
        "display_name": "Blueprints",
        "locations": createPlannableLocationObj()
    },
    # Minigames are grouped by level, not by Kong.
    "Minigames": {
        "display_name": "Minigames",
        "levels": {
            "DKIsles": {
                "display_name": "D.K. Isles",
                "locations": []
            },
            "JungleJapes": {
                "display_name": "Jungle Japes",
                "locations": []
            },
            "AngryAztec": {
                "display_name": "Angry Aztec",
                "locations": []
            },
            "FranticFactory": {
                "display_name": "Frantic Factory",
                "locations": []
            },
            "GloomyGalleon": {
                "display_name": "Gloomy Galleon",
                "locations": []
            },
            "FungiForest": {
                "display_name": "Fungi Forest",
                "locations": []
            },
            "CrystalCaves": {
                "display_name": "Crystal Caves",
                "locations": []
            },
            "CreepyCastle": {
                "display_name": "Creepy Castle",
                "locations": []
            },
            "HideoutHelm": {
                "display_name": "Hideout Helm",
                "locations": []
            }
        }
    },
    # There are no "All Kongs" hints.
    "Hints": {
        "display_name": "Hints",
        "locations": {
            "Donkey": [],
            "Diddy": [],
            "Lanky": [],
            "Tiny": [],
            "Chunky": []
        }
    }
}
for locationEnum, locationObj in LocationList.items():
    # Do not randomize constant rewards.
    if locationObj.type == Types.Constant:
        continue
    locationJson = {
        "display_name": locationObj.name,
        "enum_name": locationEnum.name
    }
    kongString = getKongString(locationObj.kong)
    if locationObj.type == Types.BlueprintBanana:
        PlandomizerPanels["Blueprints"]["locations"][kongString].append(locationJson)
    elif locationObj.type == Types.Hint:
        PlandomizerPanels["Hints"]["locations"][kongString].append(locationJson)
        HintLocationList.append(locationEnum.name)
    elif locationObj.type == Types.Shop or locationObj.level == Levels.Shops:
        PlandomizerPanels["Shops"]["locations"][kongString].append(locationJson)
        ShopLocationList.append(locationEnum.name)
    else:
        levelName = locationObj.level.name
        PlandomizerPanels[levelName]["locations"][kongString].append(locationJson)
        ItemLocationList.append(locationEnum.name)

        # If this is a minigame location, add it to the Minigames list.
        if isMinigameLocation(locationEnum):
            PlandomizerPanels["Minigames"]["levels"][levelName]["locations"].append({
                "display_name": locationObj.name,
                "enum_name": locationEnum.name,
                "kong": kongString
            })

# Hideout Helm minigame locations get manually added here, as they're not
# locations where rewards can be placed, so they don't get naturally added.
PlandomizerPanels["Minigames"]["levels"]["HideoutHelm"]["locations"] = [
    {
        "display_name": "Helm Donkey 1",
        "enum_name": "HelmDonkey1",
        "kong": "Donkey"
    },
    {
        "display_name": "Helm Donkey 2",
        "enum_name": "HelmDonkey2",
        "kong": "Donkey"
    },
    {
        "display_name": "Helm Diddy 1",
        "enum_name": "HelmDiddy1",
        "kong": "Diddy"
    },
    {
        "display_name": "Helm Diddy 2",
        "enum_name": "HelmDiddy2",
        "kong": "Diddy"
    },
    {
        "display_name": "Helm Lanky 1",
        "enum_name": "HelmLanky1",
        "kong": "Lanky"
    },
    {
        "display_name": "Helm Lanky 2",
        "enum_name": "HelmLanky2",
        "kong": "Lanky"
    },
    {
        "display_name": "Helm Tiny 1",
        "enum_name": "HelmTiny1",
        "kong": "Tiny"
    },
    {
        "display_name": "Helm Tiny 2",
        "enum_name": "HelmTiny2",
        "kong": "Tiny"
    },
    {
        "display_name": "Helm Chunky 1",
        "enum_name": "HelmChunky1",
        "kong": "Chunky"
    },
    {
        "display_name": "Helm Chunky 2",
        "enum_name": "HelmChunky2",
        "kong": "Chunky"
    }
]

#########
# ITEMS #
#########

# These items are not available as starting items.
invalidStartingItems = {
    PlandoItems.NoItem,
    PlandoItems.Donkey,
    PlandoItems.Diddy,
    PlandoItems.Lanky,
    PlandoItems.Tiny,
    PlandoItems.Chunky,
    PlandoItems.GoldenBanana,
    PlandoItems.BananaFairy,
    PlandoItems.BananaMedal,
    PlandoItems.BattleCrown,
    PlandoItems.RainbowCoin,
    PlandoItems.FakeItem,
    PlandoItems.JunkItem,
    PlandoItems.DonkeyBlueprint,
    PlandoItems.DiddyBlueprint,
    PlandoItems.LankyBlueprint,
    PlandoItems.TinyBlueprint,
    PlandoItems.ChunkyBlueprint
}

# The below items may be added multiple times as starting items.
multipleStartingItems = {
    PlandoItems.ProgressiveSlam: 2,
    PlandoItems.ProgressiveAmmoBelt: 2,
    PlandoItems.ProgressiveInstrumentUpgrade: 3,
    PlandoItems.Pearl: 5
}

# These PlandoItems enums have multiple Items enums that map to each of them,
# and so they should not be automatically added to the list of PlannableItems.
# Handle these manually.
doNotAutoAddItemSet = {
    PlandoItems.DonkeyBlueprint,
    PlandoItems.DiddyBlueprint,
    PlandoItems.LankyBlueprint,
    PlandoItems.TinyBlueprint,
    PlandoItems.ChunkyBlueprint,
    PlandoItems.JunkItem
}

PlannableItems = []  # Used to select rewards for locations.
# Starting items are not currently supported, but the code is still here for
# when support for this arrives.
PlannableStartingItems = []  # Used to select starting items.

for itemEnum, itemObj in ItemList.items():
    # Only include items that have a matching item in the plando map.
    if itemEnum not in ItemToPlandoItemMap:
        continue

    plandoItemEnum = ItemToPlandoItemMap[itemEnum]
    # Do not add blueprints or junk items. These will be replaced with generic
    # items.
    if plandoItemEnum in doNotAutoAddItemSet:
        continue
    itemJson = {
        "display_name": itemObj.name,
        "enum_name": plandoItemEnum.name
    }
    PlannableItems.append(itemJson)

    # Add this item to the list of possible starting items, if valid.
    if plandoItemEnum in invalidStartingItems:
        continue
    if plandoItemEnum in multipleStartingItems:
        itemCount = multipleStartingItems[plandoItemEnum]
        for i in range(1, itemCount+1):
            multipleItemJson = {
                "display_name": itemObj.name,
                "enum_name": f"{plandoItemEnum.name}_{i}"
            }
            PlannableStartingItems.append(multipleItemJson)
    else:
        PlannableStartingItems.append(itemJson)

PlannableItems.append({
    "display_name": "Blueprint (Donkey)",
    "enum_name": "DonkeyBlueprint"
})
PlannableItems.append({
    "display_name": "Blueprint (Diddy)",
    "enum_name": "DiddyBlueprint"
})
PlannableItems.append({
    "display_name": "Blueprint (Lanky)",
    "enum_name": "LankyBlueprint"
})
PlannableItems.append({
    "display_name": "Blueprint (Tiny)",
    "enum_name": "TinyBlueprint"
})
PlannableItems.append({
    "display_name": "Blueprint (Chunky)",
    "enum_name": "ChunkyBlueprint"
})
PlannableItems.append({
    "display_name": "Junk Item",
    "enum_name": "JunkItem"
})

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
    # The player will always start with one of the three slams.
    PlandoItems.ProgressiveSlam: 2,
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
    PlandoItems.RainbowCoin: 16,
    PlandoItems.DonkeyBlueprint: 8,
    PlandoItems.DiddyBlueprint: 8,
    PlandoItems.LankyBlueprint: 8,
    PlandoItems.TinyBlueprint: 8,
    PlandoItems.ChunkyBlueprint: 8
}

#############
# MINIGAMES #
#############

PlannableMinigames = []
for minigameEnum, minigameObj in MinigameRequirements.items():
    # NoGame is an invalid selection.
    if minigameEnum == Minigames.NoGame:
        continue
    minigameJson = {
        "display_name": minigameObj.name,
        "enum_name": minigameEnum.name
    }
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
    Levels.CreepyCastle: dict()
}

# Go through each level and add the valid spawn locations.
allSpawnableLevels = [
    DKIslesRegions,
    JungleJapesRegions,
    AngryAztecRegions,
    FranticFactoryRegions,
    GloomyGalleonRegions,
    FungiForestRegions,
    CrystalCavesRegions,
    CreepyCastleRegions
]
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
        _, regionObj = loc
        return hintNameSortDict[regionObj.level][regionObj.hint_name]
    sortedLocations = dict(sorted(filteredLocations.items(), key=spawnKey))

    for regionEnum, regionObj in sortedLocations.items():
        regionJson = {
            "display_name": f"{getLevelString(regionObj.level)}: {regionObj.hint_name} - {regionObj.name}",
            "enum_name": regionEnum.name
        }
        PlannableSpawns.append(regionJson)
