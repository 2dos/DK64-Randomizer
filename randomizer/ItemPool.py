"""Contains functions related to setting up the pool of shuffled items."""
import itertools
from random import shuffle
from randomizer.Enums.Events import Events

import randomizer.Enums.Kongs as KongObject
from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemFromKong
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Lists.Location import DonkeyMoveLocations, DiddyMoveLocations, LankyMoveLocations, TinyMoveLocations, ChunkyMoveLocations, SharedMoveLocations, TrainingBarrelLocations, LocationList
from randomizer.Lists.ShufflableExit import ShufflableExits


def PlaceConstants(settings):
    """Place items which are to be put in a hard-coded location."""
    # Handle key placements
    if settings.shuffle_loading_zones == "levels" and settings.shuffle_items == "none":
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
    # Settings-dependent locations
    # Determine what types of locations are being shuffled
    typesOfItemsShuffled = []
    if settings.kong_rando:
        typesOfItemsShuffled.append(Types.Kong)
    if settings.move_rando != "off":
        typesOfItemsShuffled.append(Types.Shop)
    if settings.training_barrels == "shuffled":
        typesOfItemsShuffled.append(Types.TrainingBarrel)
    if settings.shockwave_status != "vanilla":
        typesOfItemsShuffled.append(Types.Shockwave)
    if settings.shuffle_loading_zones == "levels":
        typesOfItemsShuffled.append(Types.Key)
    if settings.shuffle_items == "phase1":
        typesOfItemsShuffled.extend([Types.Banana, Types.Crown, Types.Blueprint, Types.Key, Types.Medal, Types.Coin])
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
    if settings.unlock_all_moves:
        LocationList[Locations.SimianSlam].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.SuperSimianSlam].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.SuperDuperSimianSlam].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.BaboonBlast].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.StrongKong].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.GorillaGrab].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.ChimpyCharge].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.RocketbarrelBoost].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.SimianSpring].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Orangstand].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.BaboonBalloon].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.OrangstandSprint].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.MiniMonkey].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.PonyTailTwirl].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Monkeyport].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.HunkyChunky].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.PrimatePunch].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.GorillaGone].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.CoconutGun].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.PeanutGun].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.GrapeGun].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.FeatherGun].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.PineappleGun].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.AmmoBelt1].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.HomingAmmo].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.AmmoBelt2].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.SniperSight].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Bongos].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Guitar].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Trombone].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Saxophone].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.Triangle].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.MusicUpgrade1].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.ThirdMelon].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.MusicUpgrade2].PlaceConstantItem(Items.NoItem)
    if settings.unlock_fairy_shockwave and settings.shockwave_status == "vanilla":
        LocationList[Locations.CameraAndShockwave].PlaceConstantItem(Items.NoItem)


def AllItems(settings):
    """Return all shuffled items."""
    allItems = []
    if settings.shuffle_items != "none":
        allItems.extend(Blueprints(settings))
        allItems.extend(HighPriorityItems(settings))
        allItems.extend(LowPriorityItems(settings))
        allItems.extend(ExcessItems(settings))
        allItems.extend(Keys(settings))
    elif settings.move_rando != "off":
        allItems.extend(DonkeyMoves)
        allItems.extend(DiddyMoves)
        allItems.extend(LankyMoves)
        allItems.extend(TinyMoves)
        allItems.extend(ChunkyMoves)
        allItems.extend(ImportantSharedMoves)
        if settings.training_barrels == "shuffled":
            allItems.extend(TrainingBarrelAbilities().copy())
        if settings.shockwave_status == "shuffled_decoupled":
            allItems.append(Items.Camera)
            allItems.append(Items.Shockwave)
        else:
            allItems.append(Items.CameraAndShockwave)
    if settings.kong_rando:
        allItems.extend(Kongs(settings))
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
    kongMoves.extend(JunkSharedMoves)
    return kongMoves


def Blueprints(settings):
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


def BlueprintAssumedItems(settings):
    """Items which are assumed to be owned while placing blueprints."""
    return Keys(settings) + LowPriorityItems(settings) + ExcessItems(settings)


def KeyAssumedItems(settings):
    """Items which are assumed to be owned while placing keys."""
    return LowPriorityItems(settings) + ExcessItems(settings)


def Keys(settings):
    """Return all key items."""
    keys = []
    for event in settings.krool_keys_required:
        if event == Events.JapesKeyTurnedIn:
            keys.append(Items.JungleJapesKey)
        elif event == Events.AztecKeyTurnedIn:
            keys.append(Items.AngryAztecKey)
        elif event == Events.FactoryKeyTurnedIn:
            keys.append(Items.FranticFactoryKey)
        elif event == Events.GalleonKeyTurnedIn:
            keys.append(Items.GloomyGalleonKey)
        elif event == Events.ForestKeyTurnedIn:
            keys.append(Items.FungiForestKey)
        elif event == Events.CavesKeyTurnedIn:
            keys.append(Items.CrystalCavesKey)
        elif event == Events.CastleKeyTurnedIn:
            keys.append(Items.CreepyCastleKey)
        elif event == Events.HelmKeyTurnedIn:
            keys.append(Items.HideoutHelmKey)
    keys.sort()
    return keys


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
    guns = []
    if not settings.unlock_all_moves:
        guns.extend([Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple])
    return guns


def Instruments(settings):
    """Return all instrument items."""
    instruments = []
    if not settings.unlock_all_moves:
        instruments.extend([Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle])
    return instruments


def TrainingBarrelAbilities():
    """Return all training barrel abilities."""
    barrelAbilities = [Items.Vines, Items.Swim, Items.Oranges, Items.Barrels]
    return barrelAbilities


def Upgrades(settings):
    """Return all upgrade items."""
    upgrades = []
    # Add training barrel items to item pool if shuffled
    if settings.training_barrels == "shuffled":
        upgrades.extend(TrainingBarrelAbilities())
    # Add either progressive upgrade items or individual ones depending on settings
    if not settings.unlock_all_moves:
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
    if not settings.unlock_fairy_shockwave:
        if settings.shockwave_status == "vanilla" or settings.shockwave_status == "shuffled":
            upgrades.append(Items.CameraAndShockwave)
        else:
            upgrades.append(Items.Camera)
            upgrades.append(Items.Shockwave)

    return upgrades


def HighPriorityItems(settings):
    """Get all items which are of high importance logically.

    Placing these first prevents fill failures.
    """
    itemPool = []
    itemPool.extend(Kongs(settings))
    itemPool.extend(Guns(settings))
    itemPool.extend(Instruments(settings))
    itemPool.extend(Upgrades(settings))
    return itemPool


def HighPriorityAssumedItems(settings):
    """Items which are assumed to be owned while placing high priority items."""
    return Blueprints(settings) + Keys(settings) + LowPriorityItems(settings) + ExcessItems(settings)


def LowPriorityItems(settings):
    """While most of these items still have logical value they are not as important."""
    itemPool = []

    itemPool.extend(itertools.repeat(Items.GoldenBanana, 100))
    itemPool.extend(itertools.repeat(Items.BananaMedal, 15))
    if not settings.crown_door_open:
        itemPool.extend(itertools.repeat(Items.BattleCrown, 4))
    if not settings.coin_door_open:
        itemPool.append(Items.NintendoCoin)
        itemPool.append(Items.RarewareCoin)
    if not settings.unlock_all_moves:
        itemPool.append(Items.SniperSight)
        if not settings.hard_shooting:
            itemPool.append(Items.HomingAmmo)
    return itemPool


def ExcessItems(settings):
    """Items which either have no logical value or are excess copies of those that do."""
    itemPool = []

    if not settings.unlock_all_moves:
        # Weapon upgrades
        if settings.hard_shooting:
            itemPool.append(Items.HomingAmmo)
        itemPool.extend(itertools.repeat(Items.ProgressiveAmmoBelt, 2))

        # Instrument upgrades
        itemPool.extend(itertools.repeat(Items.ProgressiveInstrumentUpgrade, 3))

    # Collectables
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 61))  # Blueprint GBs are already placed
    itemPool.extend(itertools.repeat(Items.BananaMedal, 25))
    itemPool.extend(itertools.repeat(Items.BattleCrown, 6))
    if settings.crown_door_open:
        itemPool.extend(itertools.repeat(Items.BattleCrown, 4))
    if settings.coin_door_open:
        itemPool.append(Items.NintendoCoin)
        itemPool.append(Items.RarewareCoin)

    return itemPool


DonkeyMoves = [Items.Coconut, Items.Bongos, Items.BaboonBlast, Items.StrongKong, Items.GorillaGrab]
DiddyMoves = [Items.Peanut, Items.Guitar, Items.ChimpyCharge, Items.RocketbarrelBoost, Items.SimianSpring]
LankyMoves = [Items.Grape, Items.Trombone, Items.Orangstand, Items.BaboonBalloon, Items.OrangstandSprint]
TinyMoves = [Items.Feather, Items.Saxophone, Items.MiniMonkey, Items.PonyTailTwirl, Items.Monkeyport]
ChunkyMoves = [Items.Pineapple, Items.Triangle, Items.HunkyChunky, Items.PrimatePunch, Items.GorillaGone]
ImportantSharedMoves = [Items.ProgressiveSlam, Items.ProgressiveSlam, Items.SniperSight, Items.HomingAmmo]
JunkSharedMoves = [Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade]
