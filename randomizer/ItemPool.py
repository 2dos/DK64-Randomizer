"""Contains functions related to setting up the pool of shuffled items."""
import itertools
from random import shuffle

import randomizer.Enums.Kongs as KongObject
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import MoveRando, ShockwaveStatus, ShuffleLoadingZones, TrainingBarrels
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemFromKong
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Lists.Location import ChunkyMoveLocations, DiddyMoveLocations, DonkeyMoveLocations, LankyMoveLocations, LocationList, SharedMoveLocations, TinyMoveLocations, TrainingBarrelLocations
from randomizer.Lists.ShufflableExit import ShufflableExits


def PlaceConstants(settings):
    """Place items which are to be put in a hard-coded location."""
    # Handle key placements
    if settings.key_8_helm:
        LocationList[Locations.HelmKey].PlaceItem(Items.HideoutHelmKey)
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels and Types.Key not in settings.shuffled_location_types:
        # Place keys in the lobbies they normally belong in
        # Ex. Whatever level is in the Japes lobby entrance will always have the Japes key
        for level in LevelInfoList.values():
            # If level exit isn't shuffled, use vanilla key
            if not ShufflableExits[level.TransitionTo].shuffled:
                LocationList[level.KeyLocation].PlaceConstantItem(level.KeyItem)
            else:
                # Find the transition this exit is attached to, and use that to get the proper location to place this key
                dest = ShufflableExits[level.TransitionTo].shuffledId
                shuffledTo = [x for x in LevelInfoList.values() if x.TransitionTo == dest][0]
                LocationList[shuffledTo.KeyLocation].PlaceConstantItem(level.KeyItem)
        # The key in Helm is always Key 8 in these settings
        LocationList[Locations.HelmKey].PlaceConstantItem(Items.HideoutHelmKey)
    # Settings-dependent locations
    # Determine what types of locations are being shuffled
    typesOfItemsShuffled = []
    if settings.kong_rando:
        typesOfItemsShuffled.append(Types.Kong)
    if settings.move_rando != MoveRando.off:
        typesOfItemsShuffled.append(Types.Shop)
        if settings.training_barrels == TrainingBarrels.shuffled:
            typesOfItemsShuffled.append(Types.TrainingBarrel)
        if settings.shockwave_status != ShockwaveStatus.vanilla:
            typesOfItemsShuffled.append(Types.Shockwave)
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        typesOfItemsShuffled.append(Types.Key)
    typesOfItemsShuffled.extend(settings.shuffled_location_types)
    # Invert this list because I think it'll be faster
    typesOfItemsNotShuffled = [typ for typ in Types if typ not in typesOfItemsShuffled]
    # Place the default item at every location of a type we're not shuffling
    for location in LocationList:
        if LocationList[location].type in typesOfItemsNotShuffled:
            LocationList[location].PlaceDefaultItem()

    # Empty out some locations based on the settings
    if settings.starting_kongs_count == 5:
        LocationList[Locations.DiddyKong].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.LankyKong].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.TinyKong].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.ChunkyKong].PlaceConstantItem(Items.NoItem)
    if settings.shockwave_status == ShockwaveStatus.start_with:
        LocationList[Locations.CameraAndShockwave].PlaceConstantItem(Items.NoItem)


def AllItems(settings):
    """Return all shuffled items."""
    allItems = []
    if Types.Blueprint in settings.shuffled_location_types:
        allItems.extend(Blueprints())
    if Types.Banana in settings.shuffled_location_types:
        allItems.extend(GoldenBananaItems())
    if Types.ToughBanana in settings.shuffled_location_types:
        allItems.extend(ToughGoldenBananaItems())
    if Types.Coin in settings.shuffled_location_types:
        allItems.extend(CompanyCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems())
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems())
    if Types.Bean in settings.shuffled_location_types:  # Could check for pearls as well
        allItems.extend(MiscItemRandoItems())
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems())
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems())
    if Types.FakeItem in settings.shuffled_location_types:
        allItems.extend(FakeItems())
    if Types.JunkItem in settings.shuffled_location_types:
        allItems.extend(JunkItems())
    if settings.move_rando != MoveRando.off:
        allItems.extend(DonkeyMoves)
        allItems.extend(DiddyMoves)
        allItems.extend(LankyMoves)
        allItems.extend(TinyMoves)
        allItems.extend(ChunkyMoves)
        allItems.extend(ImportantSharedMoves)
        if settings.training_barrels == TrainingBarrels.shuffled:
            allItems.extend(TrainingBarrelAbilities().copy())
        if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
            allItems.append(Items.Camera)
            allItems.append(Items.Shockwave)
        else:
            allItems.append(Items.CameraAndShockwave)
    if settings.kong_rando or Types.Kong in settings.shuffled_location_types:
        allItems.extend(Kongs(settings))
    return allItems


def AllItemsForMovePlacement(settings):
    """Return all shuffled items we need to assume for move placement."""
    allItems = []
    if Types.Blueprint in settings.shuffled_location_types:
        allItems.extend(Blueprints())
    if Types.Banana in settings.shuffled_location_types:
        allItems.extend(GoldenBananaItems())
    if Types.ToughBanana in settings.shuffled_location_types:
        allItems.extend(ToughGoldenBananaItems())
    if Types.Coin in settings.shuffled_location_types:
        allItems.extend(CompanyCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems())
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems())
    if Types.Bean in settings.shuffled_location_types:  # Could check for pearls as well
        allItems.extend(MiscItemRandoItems())
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems())
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems())
    if Types.FakeItem in settings.shuffled_location_types:
        allItems.extend(FakeItems())
    if Types.JunkItem in settings.shuffled_location_types:
        allItems.extend(JunkItems())
    return allItems


def AllKongMoves():
    """Return all moves."""
    allMoves = []
    allMoves.extend(DonkeyMoves)
    allMoves.extend(DiddyMoves)
    allMoves.extend(LankyMoves)
    allMoves.extend(TinyMoves)
    allMoves.extend(ChunkyMoves)
    allMoves.extend(ImportantSharedMoves)
    return allMoves


def AllMovesForOwnedKongs(kongs):
    """Return all moves for the given list of Kongs."""
    kongMoves = []
    if KongObject.Kongs.donkey in kongs:
        kongMoves.extend(DonkeyMoves)
    if KongObject.Kongs.diddy in kongs:
        kongMoves.extend(DiddyMoves)
    if KongObject.Kongs.lanky in kongs:
        kongMoves.extend(LankyMoves)
    if KongObject.Kongs.tiny in kongs:
        kongMoves.extend(TinyMoves)
    if KongObject.Kongs.chunky in kongs:
        kongMoves.extend(ChunkyMoves)
    kongMoves.extend(ImportantSharedMoves)
    return kongMoves


def ShockwaveTypeItems(settings):
    """Return the Shockwave-type items for the given settings."""
    if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
        return [Items.Camera, Items.Shockwave]
    else:
        return [Items.CameraAndShockwave]


def Blueprints():
    """Return all blueprint items."""
    blueprints = [
        Items.DKIslesDonkeyBlueprint,
        Items.DKIslesDiddyBlueprint,
        Items.DKIslesLankyBlueprint,
        Items.DKIslesTinyBlueprint,
        Items.DKIslesChunkyBlueprint,
        Items.JungleJapesDonkeyBlueprint,
        Items.JungleJapesDiddyBlueprint,
        Items.JungleJapesLankyBlueprint,
        Items.JungleJapesTinyBlueprint,
        Items.JungleJapesChunkyBlueprint,
        Items.AngryAztecDonkeyBlueprint,
        Items.AngryAztecDiddyBlueprint,
        Items.AngryAztecLankyBlueprint,
        Items.AngryAztecTinyBlueprint,
        Items.AngryAztecChunkyBlueprint,
        Items.FranticFactoryDonkeyBlueprint,
        Items.FranticFactoryDiddyBlueprint,
        Items.FranticFactoryLankyBlueprint,
        Items.FranticFactoryTinyBlueprint,
        Items.FranticFactoryChunkyBlueprint,
        Items.GloomyGalleonDonkeyBlueprint,
        Items.GloomyGalleonDiddyBlueprint,
        Items.GloomyGalleonLankyBlueprint,
        Items.GloomyGalleonTinyBlueprint,
        Items.GloomyGalleonChunkyBlueprint,
        Items.FungiForestDonkeyBlueprint,
        Items.FungiForestDiddyBlueprint,
        Items.FungiForestLankyBlueprint,
        Items.FungiForestTinyBlueprint,
        Items.FungiForestChunkyBlueprint,
        Items.CrystalCavesDonkeyBlueprint,
        Items.CrystalCavesDiddyBlueprint,
        Items.CrystalCavesLankyBlueprint,
        Items.CrystalCavesTinyBlueprint,
        Items.CrystalCavesChunkyBlueprint,
        Items.CreepyCastleDonkeyBlueprint,
        Items.CreepyCastleDiddyBlueprint,
        Items.CreepyCastleLankyBlueprint,
        Items.CreepyCastleTinyBlueprint,
        Items.CreepyCastleChunkyBlueprint,
    ]
    return blueprints


def Keys():
    """Return all key items."""
    return [Items.JungleJapesKey, Items.AngryAztecKey, Items.FranticFactoryKey, Items.GloomyGalleonKey, Items.FungiForestKey, Items.CrystalCavesKey, Items.CreepyCastleKey, Items.HideoutHelmKey]


def Kongs(settings):
    """Return Kong items depending on settings."""
    kongs = []
    if settings.starting_kongs_count != 5:
        kongs = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
        kongs.remove(ItemFromKong(settings.starting_kong))
    return kongs


def GetKongForItem(item):
    """Return Kong object from kong-type item."""
    if item == Items.Donkey:
        return KongObject.Kongs.donkey
    elif item == Items.Diddy:
        return KongObject.Kongs.diddy
    elif item == Items.Lanky:
        return KongObject.Kongs.lanky
    elif item == Items.Tiny:
        return KongObject.Kongs.tiny
    else:
        return KongObject.Kongs.chunky


def Guns(settings):
    """Return all gun items."""
    return [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]


def Instruments(settings):
    """Return all instrument items."""
    return [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]


def TrainingBarrelAbilities():
    """Return all training barrel abilities."""
    barrelAbilities = [Items.Vines, Items.Swim, Items.Oranges, Items.Barrels]
    return barrelAbilities


def Upgrades(settings):
    """Return all upgrade items."""
    upgrades = []
    # Add training barrel items to item pool if shuffled
    if settings.training_barrels == TrainingBarrels.shuffled:
        upgrades.extend(TrainingBarrelAbilities())
    # Add either progressive upgrade items or individual ones depending on settings
    upgrades.extend(itertools.repeat(Items.ProgressiveSlam, 3 - 1))  # -1 for starting slam
    if settings.progressive_upgrades:
        upgrades.extend(itertools.repeat(Items.ProgressiveDonkeyPotion, 3))
        upgrades.extend(itertools.repeat(Items.ProgressiveDiddyPotion, 3))
        upgrades.extend(itertools.repeat(Items.ProgressiveLankyPotion, 3))
        upgrades.extend(itertools.repeat(Items.ProgressiveTinyPotion, 3))
        upgrades.extend(itertools.repeat(Items.ProgressiveChunkyPotion, 3))
    else:
        upgrades.extend(
            [
                Items.BaboonBlast,
                Items.StrongKong,
                Items.GorillaGrab,
                Items.ChimpyCharge,
                Items.RocketbarrelBoost,
                Items.SimianSpring,
                Items.Orangstand,
                Items.BaboonBalloon,
                Items.OrangstandSprint,
                Items.MiniMonkey,
                Items.PonyTailTwirl,
                Items.Monkeyport,
                Items.HunkyChunky,
                Items.PrimatePunch,
                Items.GorillaGone,
            ]
        )
    upgrades.append(Items.HomingAmmo)
    upgrades.append(Items.SniperSight)
    upgrades.extend(itertools.repeat(Items.ProgressiveAmmoBelt, 2))
    upgrades.extend(itertools.repeat(Items.ProgressiveInstrumentUpgrade, 3))
    if settings.shockwave_status != ShockwaveStatus.start_with:
        if settings.shockwave_status == ShockwaveStatus.vanilla or settings.shockwave_status == ShockwaveStatus.shuffled:
            upgrades.append(Items.CameraAndShockwave)
        else:
            upgrades.append(Items.Camera)
            upgrades.append(Items.Shockwave)

    return upgrades


def HighPriorityItems(settings):
    """Get all items which are of high importance logically."""
    itemPool = []
    itemPool.extend(Kongs(settings))
    itemPool.extend(Guns(settings))
    itemPool.extend(Instruments(settings))
    itemPool.extend(Upgrades(settings))
    return itemPool


def CompanyCoinItems():
    """Return the Company Coin items to be placed."""
    itemPool = []
    itemPool.append(Items.NintendoCoin)
    itemPool.append(Items.RarewareCoin)
    return itemPool


TOUGH_BANANA_COUNT = 13


def GoldenBananaItems():
    """Return a list of GBs to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 161 - TOUGH_BANANA_COUNT))  # 40 Blueprint GBs are always already placed (see Types.BlueprintBanana)
    return itemPool


def ToughGoldenBananaItems():
    """Return a list of GBs to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.GoldenBanana, TOUGH_BANANA_COUNT))
    return itemPool


def BananaMedalItems():
    """Return a list of Banana Medals to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BananaMedal, 40))
    return itemPool


def BattleCrownItems():
    """Return a list of Crowns to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BattleCrown, 10))
    return itemPool


def MiscItemRandoItems():
    """Return a list of Items that are classed as miscellaneous."""
    itemPool = []
    itemPool.append(Items.Bean)
    itemPool.extend(itertools.repeat(Items.Pearl, 5))
    return itemPool


def RainbowCoinItems():
    """Return a list of Rainbow Coins to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.RainbowCoin, 16))
    return itemPool


def FairyItems():
    """Return a list of Fairies to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BananaFairy, 20))
    return itemPool


def FakeItems():
    """Return a list of Fake Items to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.FakeItem, 10))  # Up to 10 fake items
    return itemPool


def JunkItems():
    """Return a list of Junk Items to be placed."""
    itemPool = []
    # items_to_place = (Items.JunkAmmo, Items.JunkCrystal, Items.JunkFilm, Items.JunkMelon, Items.JunkOrange)
    # items_to_place = (Items.JunkAmmo, Items.JunkCrystal, Items.JunkMelon, Items.JunkOrange)
    items_to_place = [Items.JunkMelon]
    lim = int(100 / len(items_to_place))
    for item_type in items_to_place:
        itemPool.extend(itertools.repeat(item_type, lim))
    return itemPool


def GetItemsNeedingToBeAssumed(settings, placed_types):
    """Return a list of all items that will be assumed for immediate item placement."""
    itemPool = []
    unplacedTypes = [typ for typ in settings.shuffled_location_types if typ not in placed_types]
    if Types.Banana in unplacedTypes:
        itemPool.extend(GoldenBananaItems())
    if Types.ToughBanana in unplacedTypes:
        itemPool.extend(ToughGoldenBananaItems())
    if Types.Shop in unplacedTypes:
        itemPool.extend(AllKongMoves())
    if Types.Blueprint in unplacedTypes:
        itemPool.extend(Blueprints())
    if Types.Fairy in unplacedTypes:
        itemPool.extend(FairyItems())
    if Types.Key in unplacedTypes:
        itemPool.extend(Keys())
    if Types.Crown in unplacedTypes:
        itemPool.extend(BattleCrownItems())
    if Types.Coin in unplacedTypes:
        itemPool.extend(CompanyCoinItems())
    if Types.TrainingBarrel in unplacedTypes:
        itemPool.extend(TrainingBarrelAbilities())
    if Types.Kong in unplacedTypes:
        itemPool.extend(Kongs(settings))
    if Types.Medal in unplacedTypes:
        itemPool.extend(BananaMedalItems())
    if Types.Shockwave in unplacedTypes:
        itemPool.extend(ShockwaveTypeItems(settings))
    if Types.Bean in unplacedTypes:
        itemPool.extend(MiscItemRandoItems())  # Covers Bean and Pearls
    if Types.RainbowCoin in unplacedTypes:
        itemPool.extend(RainbowCoinItems())
    if Types.ToughBanana in unplacedTypes:
        itemPool.extend(ToughGoldenBananaItems())
    # Never logic-affecting items
    # if Types.FakeItem in unplacedTypes:
    #     itemPool.extend(FakeItems())
    # if Types.JunkItem in unplacedTypes:
    #     itemPool.extend(JunkItems())
    # if Types.Hint in unplacedTypes: someday???
    #     itemPool.extend(HintItems()) hints in the pool???
    # If shops are not part of the larger item pool and are not placed, we may still need to assume them
    # It is worth noting that TrainingBarrel and Shockwave type items are contingent on Shop type items being in the item rando pool
    if Types.Shop not in settings.shuffled_location_types and Types.Shop not in placed_types and settings.move_rando != MoveRando.off:
        itemPool.extend(AllKongMoves())
        if settings.training_barrels == TrainingBarrels.shuffled:
            itemPool.extend(TrainingBarrelAbilities().copy())
        if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
            itemPool.extend(ShockwaveTypeItems(settings))
    return itemPool


DonkeyMoves = [Items.Coconut, Items.Bongos, Items.BaboonBlast, Items.StrongKong, Items.GorillaGrab]
DiddyMoves = [Items.Peanut, Items.Guitar, Items.ChimpyCharge, Items.RocketbarrelBoost, Items.SimianSpring]
LankyMoves = [Items.Grape, Items.Trombone, Items.Orangstand, Items.BaboonBalloon, Items.OrangstandSprint]
TinyMoves = [Items.Feather, Items.Saxophone, Items.MiniMonkey, Items.PonyTailTwirl, Items.Monkeyport]
ChunkyMoves = [Items.Pineapple, Items.Triangle, Items.HunkyChunky, Items.PrimatePunch, Items.GorillaGone]
ImportantSharedMoves = [Items.ProgressiveSlam, Items.ProgressiveSlam, Items.SniperSight, Items.HomingAmmo]
JunkSharedMoves = [Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade]
ProgressiveSharedMovesSet = {Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveSlam}
