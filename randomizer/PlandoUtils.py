"""Includes utility functions for plandomizer support."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems, PlandoItemToItemMap
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.LogicClasses import Regions

# Some common item sets that may be used in multiple places.
KongSet = {
    PlandoItems.Donkey.name,
    PlandoItems.Diddy.name,
    PlandoItems.Lanky.name,
    PlandoItems.Tiny.name,
    PlandoItems.Chunky.name,
}
KeySet = {
    PlandoItems.JungleJapesKey.name,
    PlandoItems.AngryAztecKey.name,
    PlandoItems.FranticFactoryKey.name,
    PlandoItems.GloomyGalleonKey.name,
    PlandoItems.FungiForestKey.name,
    PlandoItems.CrystalCavesKey.name,
    PlandoItems.CreepyCastleKey.name,
    PlandoItems.HideoutHelmKey.name,
}
MoveSet = {
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
    PlandoItems.Coconut.name,
    PlandoItems.Peanut.name,
    PlandoItems.Grape.name,
    PlandoItems.Feather.name,
    PlandoItems.Pineapple.name,
    PlandoItems.HomingAmmo.name,
    PlandoItems.SniperSight.name,
    PlandoItems.ProgressiveAmmoBelt.name,
    PlandoItems.Bongos.name,
    PlandoItems.Guitar.name,
    PlandoItems.Trombone.name,
    PlandoItems.Saxophone.name,
    PlandoItems.Triangle.name,
    PlandoItems.ProgressiveInstrumentUpgrade.name,
    PlandoItems.Camera.name,
    PlandoItems.Shockwave.name,
}

# This dict only contains names for plando items that don't map 1:1 to Item.
plandoItemNameDict = {
    PlandoItems.ProgressiveSlam: "Progressive Slam",
    PlandoItems.ProgressiveAmmoBelt: "Progressive Ammo Belt",
    PlandoItems.ProgressiveInstrumentUpgrade: "Progressive Instrument Upgrade",
    PlandoItems.DonkeyBlueprint: "Blueprint (Donkey)",
    PlandoItems.DiddyBlueprint: "Blueprint (Diddy)",
    PlandoItems.LankyBlueprint: "Blueprint (Lanky)",
    PlandoItems.TinyBlueprint: "Blueprint (Tiny)",
    PlandoItems.ChunkyBlueprint: "Blueprint (Chunky)",
    PlandoItems.JunkItem: "Junk Item",
    PlandoItems.RandomKong: "Random Kong",
    PlandoItems.RandomMove: "Random Move",
    PlandoItems.RandomKongMove: "Random Kong Move",
    PlandoItems.RandomSharedMove: "Random Shared Move",
    PlandoItems.RandomKey: "Random Key",
    PlandoItems.RandomItem: "Random Collectible",
}


def GetNameFromPlandoItem(plandoItem: PlandoItems) -> str:
    """Obtain a display name for a given PlandoItem enum."""
    if plandoItem in plandoItemNameDict:
        return plandoItemNameDict[plandoItem]
    mappedItem = PlandoItemToItemMap[plandoItem]
    return ItemList[mappedItem].name


# A master dictionary of all possible item locations, mapped to a set of which
# items may not appear in that location. This will be used to filter all the
# dropdowns used in the plandomizer.
ItemRestrictionsPerLocation = {location.name: set() for location in LocationList.keys()}

# Each blueprint item should only appear in locations specific to the Kong who
# can pick up that blueprint. Any "All Kongs" locations may not have any
# blueprints assigned to them. Additionally, any location only accessible by
# one Kong may not have that Kong placed in that location.
blueprintItemSet = {PlandoItems.DonkeyBlueprint.name, PlandoItems.DiddyBlueprint.name, PlandoItems.LankyBlueprint.name, PlandoItems.TinyBlueprint.name, PlandoItems.ChunkyBlueprint.name}
for locEnum, locObj in LocationList.items():
    if locObj.kong == Kongs.donkey:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Donkey.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DiddyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.LankyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.TinyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.ChunkyBlueprint.name)
    elif locObj.kong == Kongs.diddy:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Diddy.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DonkeyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.LankyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.TinyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.ChunkyBlueprint.name)
    elif locObj.kong == Kongs.lanky:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Lanky.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DonkeyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DiddyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.TinyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.ChunkyBlueprint.name)
    elif locObj.kong == Kongs.tiny:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Tiny.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DonkeyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DiddyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.LankyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.ChunkyBlueprint.name)
    elif locObj.kong == Kongs.chunky:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Chunky.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DonkeyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.DiddyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.LankyBlueprint.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.TinyBlueprint.name)
    else:
        ItemRestrictionsPerLocation[locEnum.name].update(blueprintItemSet)

# Banana fairy locations have a handful of limitations.
bananaFairyRestrictedItems = {
    PlandoItems.Camera.name,
    PlandoItems.NintendoCoin.name,
    PlandoItems.RarewareCoin.name,
    PlandoItems.BananaMedal.name,
    PlandoItems.Bean.name,
    PlandoItems.Pearl.name,
    PlandoItems.RainbowCoin.name,
    PlandoItems.JunkItem.name,
    PlandoItems.DonkeyBlueprint.name,
    PlandoItems.DiddyBlueprint.name,
    PlandoItems.LankyBlueprint.name,
    PlandoItems.TinyBlueprint.name,
    PlandoItems.ChunkyBlueprint.name,
}

# For every location in LocationList, if the default reward is a Banana Fairy,
# add all of the restricted items to the restricted set.
for locEnum, locObj in LocationList.items():
    if locObj.default == Items.BananaFairy:
        ItemRestrictionsPerLocation[locEnum.name].update(bananaFairyRestrictedItems)

# Very few items are permitted in Kong locations.
kongRestrictedItemSet = {
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
    PlandoItems.Coconut.name,
    PlandoItems.Peanut.name,
    PlandoItems.Grape.name,
    PlandoItems.Feather.name,
    PlandoItems.Pineapple.name,
    PlandoItems.HomingAmmo.name,
    PlandoItems.SniperSight.name,
    PlandoItems.ProgressiveAmmoBelt.name,
    PlandoItems.Bongos.name,
    PlandoItems.Guitar.name,
    PlandoItems.Trombone.name,
    PlandoItems.Saxophone.name,
    PlandoItems.Triangle.name,
    PlandoItems.ProgressiveInstrumentUpgrade.name,
    PlandoItems.Camera.name,
    PlandoItems.Shockwave.name,
    PlandoItems.NintendoCoin.name,
    PlandoItems.RarewareCoin.name,
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
    PlandoItems.BananaMedal.name,
    PlandoItems.BattleCrown.name,
    PlandoItems.Bean.name,
    PlandoItems.Pearl.name,
    PlandoItems.RainbowCoin.name,
    PlandoItems.FakeItem.name,
    PlandoItems.JunkItem.name,
    PlandoItems.DonkeyBlueprint.name,
    PlandoItems.DiddyBlueprint.name,
    PlandoItems.LankyBlueprint.name,
    PlandoItems.TinyBlueprint.name,
    PlandoItems.ChunkyBlueprint.name,
    PlandoItems.RandomMove.name,
    PlandoItems.RandomKongMove.name,
    PlandoItems.RandomSharedMove.name,
    PlandoItems.RandomKey.name,
    PlandoItems.RandomItem.name,
}

kongLocationList = [Locations.DiddyKong.name, Locations.TinyKong.name, Locations.LankyKong.name, Locations.ChunkyKong.name]

for locationName in kongLocationList:
    ItemRestrictionsPerLocation[locationName].update(kongRestrictedItemSet)

# We need to separate the shops into Kong-specific and shared.
sharedShopsSet = set()
kongSpecificShopSet = set()
for locEnum, locObj in LocationList.items():
    if locObj.type == Types.Shop:
        if locObj.kong == Kongs.any:
            sharedShopsSet.add(locEnum.name)
        else:
            kongSpecificShopSet.add(locEnum.name)

# Shared shops should not have Kong-specific moves.
kongSpecificMoveItemSet = {
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
    PlandoItems.Coconut.name,
    PlandoItems.Peanut.name,
    PlandoItems.Grape.name,
    PlandoItems.Feather.name,
    PlandoItems.Pineapple.name,
    PlandoItems.Bongos.name,
    PlandoItems.Guitar.name,
    PlandoItems.Trombone.name,
    PlandoItems.Saxophone.name,
    PlandoItems.Triangle.name,
    PlandoItems.RandomKongMove.name,
}

# Kong-specific shops have a handful of banned items.
kongSpecificShopRestrictedItemSet = {PlandoItems.Vines.name, PlandoItems.Swim.name, PlandoItems.Oranges.name, PlandoItems.Barrels.name, PlandoItems.Shockwave.name}

# General shops have few restrictions.
shopRestrictedItemSet = {PlandoItems.RainbowCoin.name, PlandoItems.JunkItem.name}

# Add the restricted items for each shop location. (This will also cover the
# blueprint redemptions, which is fine.)
for shop in sharedShopsSet:
    ItemRestrictionsPerLocation[shop].update(kongSpecificMoveItemSet)
    ItemRestrictionsPerLocation[shop].update(shopRestrictedItemSet)

for shop in kongSpecificShopSet:
    ItemRestrictionsPerLocation[shop].update(kongSpecificShopRestrictedItemSet)
    ItemRestrictionsPerLocation[shop].update(shopRestrictedItemSet)

# The Jetpac game has few restrictions.
ItemRestrictionsPerLocation[Locations.RarewareCoin.name].update(shopRestrictedItemSet)

# Crowns are not allowed on Helm Medal locations.
helmMedalLocationList = [Locations.HelmDonkeyMedal.name, Locations.HelmDiddyMedal.name, Locations.HelmLankyMedal.name, Locations.HelmTinyMedal.name, Locations.HelmChunkyMedal.name]
for locationName in helmMedalLocationList:
    ItemRestrictionsPerLocation[locationName].add(PlandoItems.BattleCrown.name)

# Boss fights cannot have junk items or blueprint rewards.
bossFightLocationList = [
    Locations.JapesKey.name,
    Locations.AztecKey.name,
    Locations.FactoryKey.name,
    Locations.GalleonKey.name,
    Locations.ForestKey.name,
    Locations.CavesKey.name,
    Locations.CastleKey.name,
]
for locationName in bossFightLocationList:
    ItemRestrictionsPerLocation[locationName].add(PlandoItems.JunkItem.name)
    ItemRestrictionsPerLocation[locationName].update(blueprintItemSet)

for locEnum, locObj in LocationList.items():
    # Enemies and crates should not have junk item rewards.
    if locObj.type == Types.CrateItem or locObj.type == Types.Enemies:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.JunkItem.name)
    # Battle arenas cannot have junk item or blueprint rewards.
    if locObj.type == Types.Crown:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.JunkItem.name)
        ItemRestrictionsPerLocation[locEnum.name].update(blueprintItemSet)
    # Junk items cannot be placed anywhere in Hideout Helm. Due to technical
    # limitations, neither can Golden Bananas. Due to logic-related reasons,
    # neither can a handful of moves needed to fight bosses.
    if locObj.level == Levels.HideoutHelm:
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.JunkItem.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.GoldenBanana.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.HunkyChunky.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.PonyTailTwirl.name)
        ItemRestrictionsPerLocation[locEnum.name].add(PlandoItems.Barrels.name)

# This one rock can't have Kongs as a reward.
ItemRestrictionsPerLocation[Locations.IslesDonkeyJapesRock.name].update(KongSet)
ItemRestrictionsPerLocation[Locations.IslesDonkeyJapesRock.name].add(PlandoItems.RandomKong.name)

# These specific locations cannot have fake items on them.
badFakeItemLocationList = [
    # Caves Beetle Race causes issues with a blueprint potentially being there
    Locations.CavesLankyBeetleRace.name,
    # Stuff that may be required to access other stuff - Not really fair
    Locations.JapesDonkeyFreeDiddy.name,
    Locations.JapesDonkeyFrontofCage.name,
    Locations.IslesDonkeyJapesRock.name,
    Locations.FactoryDonkeyDKArcade.name,
    Locations.FactoryTinyDartboard.name,
    Locations.JapesLankyFairyCave.name,
    Locations.AztecLankyVulture.name,
    Locations.AztecDiddyRamGongs.name,
    Locations.ForestDiddyRafters.name,
    Locations.CavesTiny5DoorIgloo.name,
    Locations.CavesDiddy5DoorCabinUpper.name,
    Locations.CastleDonkeyTree.name,
    Locations.CastleLankyGreenhouse.name,
    Locations.HelmBananaFairy1.name,
    Locations.HelmBananaFairy2.name,
    # Miscellaneous issues
    Locations.NintendoCoin.name,
    Locations.RarewareCoin.name,
]
for locationName in badFakeItemLocationList:
    ItemRestrictionsPerLocation[locationName].add(PlandoItems.FakeItem.name)

# Rainbow coins cannot be placed on the Banana Fairy's gift.
ItemRestrictionsPerLocation[Locations.CameraAndShockwave.name].add(PlandoItems.RainbowCoin.name)

# Dirt patches cannot have blueprints placed on them.
dirtPatchLocationList = [
    Locations.RainbowCoin_Location00.name,
    Locations.RainbowCoin_Location01.name,
    Locations.RainbowCoin_Location02.name,
    Locations.RainbowCoin_Location03.name,
    Locations.RainbowCoin_Location04.name,
    Locations.RainbowCoin_Location05.name,
    Locations.RainbowCoin_Location06.name,
    Locations.RainbowCoin_Location07.name,
    Locations.RainbowCoin_Location08.name,
    Locations.RainbowCoin_Location09.name,
    Locations.RainbowCoin_Location10.name,
    Locations.RainbowCoin_Location11.name,
    Locations.RainbowCoin_Location12.name,
    Locations.RainbowCoin_Location13.name,
    Locations.RainbowCoin_Location14.name,
    Locations.RainbowCoin_Location15.name,
]
for locationName in dirtPatchLocationList:
    ItemRestrictionsPerLocation[locationName].update(blueprintItemSet)

# These specific locations cannot have blueprints placed on them.
badBlueprintLocationList = [
    Locations.IslesDonkeyJapesRock.name,
    Locations.JapesDonkeyFrontofCage.name,
    Locations.JapesDonkeyFreeDiddy.name,
    Locations.AztecDiddyFreeTiny.name,
    Locations.AztecDonkeyFreeLanky.name,
    Locations.FactoryLankyFreeChunky.name,
]
for locationName in badBlueprintLocationList:
    ItemRestrictionsPerLocation[locationName].update(blueprintItemSet)


def PlandoItemFilter(itemList: list[dict], location: str) -> list[dict]:
    """Return a filtered list of plando items that are permitted at the given location.

    Args:
        itemList (dict[]): The list of possible plando items. Each item
            contains "name" and "value" string fields.
        location (str): The location where we are trying to place items.
            Equal to the string name of the Location enum.
    """
    # Filter out every item that appears in the restricted set for this location.
    return [item for item in itemList if item["value"] not in ItemRestrictionsPerLocation[location["value"]]]


# A dictionary indicating which mini-games are unavailable to certain Kongs.
kongMinigameRestrictions = {
    "Donkey": {Minigames.DiddyRocketbarrel.name, Minigames.TinyPonyTailTwirl.name, Minigames.ChunkyHiddenKremling.name},
    "Diddy": {Minigames.SpeedySwingSortieNormal.name, Minigames.DonkeyTarget.name, Minigames.TinyPonyTailTwirl.name, Minigames.ChunkyHiddenKremling.name},
    "Lanky": {
        Minigames.BusyBarrelBarrageEasy.name,
        Minigames.BusyBarrelBarrageNormal.name,
        Minigames.BusyBarrelBarrageHard.name,
        Minigames.SpeedySwingSortieNormal.name,
        Minigames.DonkeyTarget.name,
        Minigames.TinyPonyTailTwirl.name,
        Minigames.ChunkyHiddenKremling.name,
    },
    "Tiny": {Minigames.DonkeyTarget.name, Minigames.ChunkyHiddenKremling.name},
    "Chunky": {Minigames.SpeedySwingSortieNormal.name, Minigames.DonkeyTarget.name, Minigames.TinyPonyTailTwirl.name},
}


def PlandoMinigameFilter(minigameList: list[str], kong: str) -> list[str]:
    """Return a filtered list of minigames that can be played by each Kong.

    This will prevent the user from placing impossible minigames in locations
    that only certain Kongs can access.

    Args:
        minigameList (str[]): The list of possible minigames.
        kong (str): The Kong who will be playing the minigame.
    """
    if kong == "All Kongs":
        return minigameList
    return [game for game in minigameList if game["value"] not in kongMinigameRestrictions[kong]]


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
    Locations.RarewareCoin.name: 121,  # Jetpac
}


def PlandoShopSortFilter(shopLocationList: list[str]) -> list[str]:
    """Return a sorted list of shop locations. These are sorted by level, then by vendor, then by Kong. This makes the full list easier to browse.

    Args:
        shopLocationList (str[]): The list of all shop locations.
    """

    def shopKey(shopLocation):
        return shopLocationOrderingDict[shopLocation["value"]]

    return sorted(shopLocationList, key=shopKey)


def PlandoOptionClassAnnotation(panel: str, kong: str, location: str, item: str) -> str:
    """Apply certain CSS classes to dropdown menu options.

    This allows for the frontend to quickly disable or enable options if they
    conflict with the existing settings.
    """
    classSet = set()

    # Each key gets its own class.
    if item in KeySet:
        classSet.add(f"plando-{item}-option")

    # Each Kong gets their own class.
    if item in KongSet:
        classSet.add(f"plando-{item}-option")

    # Each move gets its own class.
    if item in MoveSet:
        classSet.add(f"plando-{item}-option")

    # Camera and Shockwave get their own class.
    if item in {PlandoItems.Camera.name, PlandoItems.Shockwave.name}:
        classSet.add("plando-camera-shockwave-option")

    # If there are classes to append, add them in a list and return.
    if len(classSet) > 0:
        return f"class=\"{' '.join(list(classSet))}\""
    else:
        return ""


# A dictionary that maps plando options to enum classes. The key for each enum
# must exactly match that of the associated HTML input.
PlandoEnumMap = {
    "plando_spawn_location": Regions,
    "plando_starting_kongs_selected": Kongs,
    "plando_kong_rescue_donkey": Kongs,
    "plando_kong_rescue_diddy": Kongs,
    "plando_kong_rescue_lanky": Kongs,
    "plando_kong_rescue_tiny": Kongs,
    "plando_kong_rescue_chunky": Kongs,
    "plando_starting_moves_selected": PlandoItems,
    "plando_level_order_0": Levels,
    "plando_level_order_1": Levels,
    "plando_level_order_2": Levels,
    "plando_level_order_3": Levels,
    "plando_level_order_4": Levels,
    "plando_level_order_5": Levels,
    "plando_level_order_6": Levels,
    "plando_krool_order_0": Kongs,
    "plando_krool_order_1": Kongs,
    "plando_krool_order_2": Kongs,
    "plando_krool_order_3": Kongs,
    "plando_krool_order_4": Kongs,
    "plando_helm_order_0": Kongs,
    "plando_helm_order_1": Kongs,
    "plando_helm_order_2": Kongs,
    "plando_helm_order_3": Kongs,
    "plando_helm_order_4": Kongs,
}
