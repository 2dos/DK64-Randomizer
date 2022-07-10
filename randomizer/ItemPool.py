"""Contains functions related to setting up the pool of shuffled items."""
import itertools
from random import shuffle

from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Transitions import Transitions
from randomizer.Lists.Item import ItemFromKong
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Lists.Location import LocationList
from randomizer.Lists.ShufflableExit import ShufflableExits


def PlaceConstants(settings):
    """Place items which are to be put in a hard-coded location."""
    # Handle key placements
    if settings.shuffle_loading_zones == "levels":
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
    if settings.shuffle_items != "all":
        shuffledLocations = []
        if settings.shuffle_items == "moves":
            shuffledLocations.extend(DonkeyMoveLocations)
            shuffledLocations.extend(DiddyMoveLocations)
            shuffledLocations.extend(LankyMoveLocations)
            shuffledLocations.extend(TinyMoveLocations)
            shuffledLocations.extend(ChunkyMoveLocations)
            shuffledLocations.extend(SharedMoveLocations)
        if settings.kong_rando:
            shuffledLocations.append(Locations.DiddyKong)
            shuffledLocations.append(Locations.LankyKong)
            shuffledLocations.append(Locations.TinyKong)
            shuffledLocations.append(Locations.ChunkyKong)
        if settings.shuffle_loading_zones == "levels":
            shuffledLocations.append(Locations.JapesKey)
            shuffledLocations.append(Locations.AztecKey)
            shuffledLocations.append(Locations.FactoryKey)
            shuffledLocations.append(Locations.GalleonKey)
            shuffledLocations.append(Locations.ForestKey)
            shuffledLocations.append(Locations.CavesKey)
            shuffledLocations.append(Locations.CastleKey)
        locations = [x for x in LocationList if x not in shuffledLocations]
        # All locations NOT shuffled will place their default item here
        for location in locations:
            LocationList[location].PlaceDefaultItem()
    if settings.training_barrels == "normal":
        LocationList[Locations.IslesVinesTrainingBarrel].PlaceConstantItem(Items.Vines)
        LocationList[Locations.IslesSwimTrainingBarrel].PlaceConstantItem(Items.Swim)
        LocationList[Locations.IslesOrangesTrainingBarrel].PlaceConstantItem(Items.Oranges)
        LocationList[Locations.IslesBarrelsTrainingBarrel].PlaceConstantItem(Items.Barrels)
    elif settings.training_barrels == "startwith":
        LocationList[Locations.IslesVinesTrainingBarrel].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.IslesSwimTrainingBarrel].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.IslesOrangesTrainingBarrel].PlaceConstantItem(Items.NoItem)
        LocationList[Locations.IslesBarrelsTrainingBarrel].PlaceConstantItem(Items.NoItem)
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
    if settings.unlock_fairy_shockwave:
        LocationList[Locations.CameraAndShockwave].PlaceConstantItem(Items.NoItem)


def AllItems(settings):
    """Return all shuffled items."""
    allItems = []
    if settings.shuffle_items == "all":
        allItems.extend(Blueprints(settings))
        allItems.extend(HighPriorityItems(settings))
        allItems.extend(LowPriorityItems(settings))
        allItems.extend(ExcessItems(settings))
    elif settings.shuffle_items == "moves":
        allItems.extend(DonkeyMoves)
        allItems.extend(DiddyMoves)
        allItems.extend(LankyMoves)
        allItems.extend(TinyMoves)
        allItems.extend(ChunkyMoves)
        allItems.extend(ImportantSharedMoves)
    if settings.kong_rando:
        allItems.extend(Kongs(settings))
    return allItems


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
    return LowPriorityItems(settings) + ExcessItems(settings)


def Keys():
    """Return all key items."""
    keys = [Items.JungleJapesKey, Items.AngryAztecKey, Items.FranticFactoryKey, Items.GloomyGalleonKey, Items.FungiForestKey, Items.CrystalCavesKey, Items.CreepyCastleKey, Items.HideoutHelmKey]
    return keys


def Kongs(settings):
    """Return Kong items depending on settings."""
    kongs = []
    if settings.starting_kongs_count != 5:
        kongs = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
        kongs.remove(ItemFromKong(settings.starting_kong))
    return kongs


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
        upgrades.append(Items.CameraAndShockwave)

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
    return Blueprints(settings) + LowPriorityItems(settings) + ExcessItems(settings)


def LowPriorityItems(settings):
    """While most of these items still have logical value they are not as important."""
    itemPool = []

    itemPool.extend(itertools.repeat(Items.GoldenBanana, 100))
    itemPool.extend(itertools.repeat(Items.BananaFairy, 20))
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
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 101))
    itemPool.extend(itertools.repeat(Items.BananaMedal, 25))
    itemPool.extend(itertools.repeat(Items.BattleCrown, 6))
    if settings.crown_door_open:
        itemPool.extend(itertools.repeat(Items.BattleCrown, 4))
    if settings.coin_door_open:
        itemPool.append(Items.NintendoCoin)
        itemPool.append(Items.RarewareCoin)

    return itemPool


def GetMoveLocationsToRemove(sharedMoveShops: set):
    """Determine locations to remove from the move pool based on where shared moves got placed."""
    locationsToRemove = []
    for sharedMoveShop in sharedMoveShops:
        # Japes Shops
        if sharedMoveShop == Locations.SharedJapesPotion:
            locationsToRemove.append(Locations.BaboonBlast)
            locationsToRemove.append(Locations.ChimpyCharge)
            locationsToRemove.append(Locations.Orangstand)
            locationsToRemove.append(Locations.MiniMonkey)
            locationsToRemove.append(Locations.HunkyChunky)
        elif sharedMoveShop == Locations.SharedJapesGun:
            locationsToRemove.append(Locations.CoconutGun)
            locationsToRemove.append(Locations.PeanutGun)
            locationsToRemove.append(Locations.GrapeGun)
            locationsToRemove.append(Locations.FeatherGun)
            locationsToRemove.append(Locations.PineappleGun)
        # Aztec Shops
        elif sharedMoveShop == Locations.SharedAztecPotion:
            locationsToRemove.append(Locations.StrongKong)
            locationsToRemove.append(Locations.RocketbarrelBoost)
            locationsToRemove.append(Locations.LankyAztecPotion)
            locationsToRemove.append(Locations.TinyAztecPotion)
            locationsToRemove.append(Locations.ChunkyAztecPotion)
        elif sharedMoveShop == Locations.SharedAztecGun:
            locationsToRemove.append(Locations.DonkeyAztecGun)
            locationsToRemove.append(Locations.DiddyAztecGun)
            locationsToRemove.append(Locations.LankyAztecGun)
            locationsToRemove.append(Locations.TinyAztecGun)
            locationsToRemove.append(Locations.ChunkyAztecGun)
        elif sharedMoveShop == Locations.SharedAztecInstrument:
            locationsToRemove.append(Locations.Bongos)
            locationsToRemove.append(Locations.Guitar)
            locationsToRemove.append(Locations.Trombone)
            locationsToRemove.append(Locations.Saxophone)
            locationsToRemove.append(Locations.Triangle)
        # Factory Shops
        elif sharedMoveShop == Locations.SharedFactoryPotion:
            locationsToRemove.append(Locations.GorillaGrab)
            locationsToRemove.append(Locations.SimianSpring)
            locationsToRemove.append(Locations.BaboonBalloon)
            locationsToRemove.append(Locations.PonyTailTwirl)
            locationsToRemove.append(Locations.PrimatePunch)
        elif sharedMoveShop == Locations.AmmoBelt1:
            locationsToRemove.append(Locations.DonkeyFactoryGun)
            locationsToRemove.append(Locations.DiddyFactoryGun)
            locationsToRemove.append(Locations.LankyFactoryGun)
            locationsToRemove.append(Locations.TinyFactoryGun)
            locationsToRemove.append(Locations.ChunkyFactoryGun)
        elif sharedMoveShop == Locations.SharedFactoryInstrument:
            locationsToRemove.append(Locations.DonkeyFactoryInstrument)
            locationsToRemove.append(Locations.DiddyFactoryInstrument)
            locationsToRemove.append(Locations.LankyFactoryInstrument)
            locationsToRemove.append(Locations.TinyFactoryInstrument)
            locationsToRemove.append(Locations.ChunkyFactoryInstrument)
        # Galleon Shops
        elif sharedMoveShop == Locations.SharedGalleonPotion:
            locationsToRemove.append(Locations.DonkeyGalleonPotion)
            locationsToRemove.append(Locations.DiddyGalleonPotion)
            locationsToRemove.append(Locations.LankyGalleonPotion)
            locationsToRemove.append(Locations.TinyGalleonPotion)
            locationsToRemove.append(Locations.ChunkyGalleonPotion)
        elif sharedMoveShop == Locations.SharedGalleonGun:
            locationsToRemove.append(Locations.DonkeyGalleonGun)
            locationsToRemove.append(Locations.DiddyGalleonGun)
            locationsToRemove.append(Locations.LankyGalleonGun)
            locationsToRemove.append(Locations.TinyGalleonGun)
            locationsToRemove.append(Locations.ChunkyGalleonGun)
        elif sharedMoveShop == Locations.MusicUpgrade1:
            locationsToRemove.append(Locations.DonkeyGalleonInstrument)
            locationsToRemove.append(Locations.DiddyGalleonInstrument)
            locationsToRemove.append(Locations.LankyGalleonInstrument)
            locationsToRemove.append(Locations.TinyGalleonInstrument)
            locationsToRemove.append(Locations.ChunkyGalleonInstrument)
        # Forest Shops
        elif sharedMoveShop == Locations.SuperSimianSlam:
            locationsToRemove.append(Locations.DonkeyForestPotion)
            locationsToRemove.append(Locations.DiddyForestPotion)
            locationsToRemove.append(Locations.LankyForestPotion)
            locationsToRemove.append(Locations.TinyForestPotion)
            locationsToRemove.append(Locations.ChunkyForestPotion)
        elif sharedMoveShop == Locations.HomingAmmo:
            locationsToRemove.append(Locations.DonkeyForestGun)
            locationsToRemove.append(Locations.DiddyForestGun)
            locationsToRemove.append(Locations.LankyForestGun)
            locationsToRemove.append(Locations.TinyForestGun)
            locationsToRemove.append(Locations.ChunkyForestGun)
        # Caves Shops
        elif sharedMoveShop == Locations.SharedCavesPotion:
            locationsToRemove.append(Locations.DonkeyCavesPotion)
            locationsToRemove.append(Locations.DiddyCavesPotion)
            locationsToRemove.append(Locations.OrangstandSprint)
            locationsToRemove.append(Locations.Monkeyport)
            locationsToRemove.append(Locations.GorillaGone)
        elif sharedMoveShop == Locations.AmmoBelt2:
            locationsToRemove.append(Locations.DonkeyCavesGun)
            locationsToRemove.append(Locations.DiddyCavesGun)
            locationsToRemove.append(Locations.LankyCavesGun)
            locationsToRemove.append(Locations.TinyCavesGun)
            locationsToRemove.append(Locations.ChunkyCavesGun)
        elif sharedMoveShop == Locations.ThirdMelon:
            locationsToRemove.append(Locations.DonkeyCavesInstrument)
            locationsToRemove.append(Locations.DiddyCavesInstrument)
            locationsToRemove.append(Locations.LankyCavesInstrument)
            locationsToRemove.append(Locations.TinyCavesInstrument)
            locationsToRemove.append(Locations.ChunkyCavesInstrument)
        # Castle Shops
        elif sharedMoveShop == Locations.SuperDuperSimianSlam:
            locationsToRemove.append(Locations.DonkeyCastlePotion)
            locationsToRemove.append(Locations.DiddyCastlePotion)
            locationsToRemove.append(Locations.LankyCastlePotion)
            locationsToRemove.append(Locations.TinyCastlePotion)
            locationsToRemove.append(Locations.ChunkyCastlePotion)
        elif sharedMoveShop == Locations.SniperSight:
            locationsToRemove.append(Locations.DonkeyCastleGun)
            locationsToRemove.append(Locations.DiddyCastleGun)
            locationsToRemove.append(Locations.LankyCastleGun)
            locationsToRemove.append(Locations.TinyCastleGun)
            locationsToRemove.append(Locations.ChunkyCastleGun)
        elif sharedMoveShop == Locations.MusicUpgrade2:
            locationsToRemove.append(Locations.DonkeyCastleInstrument)
            locationsToRemove.append(Locations.DiddyCastleInstrument)
            locationsToRemove.append(Locations.LankyCastleInstrument)
            locationsToRemove.append(Locations.TinyCastleInstrument)
            locationsToRemove.append(Locations.ChunkyCastleInstrument)
    return set(locationsToRemove)


DonkeyMoveLocations = {
    Locations.BaboonBlast,
    Locations.StrongKong,
    Locations.GorillaGrab,
    Locations.CoconutGun,
    Locations.Bongos,
    Locations.DonkeyGalleonPotion,
    Locations.DonkeyForestPotion,
    Locations.DonkeyCavesPotion,
    Locations.DonkeyCastlePotion,
    Locations.DonkeyAztecGun,
    Locations.DonkeyFactoryGun,
    Locations.DonkeyGalleonGun,
    Locations.DonkeyForestGun,
    Locations.DonkeyCavesGun,
    Locations.DonkeyCastleGun,
    Locations.DonkeyFactoryInstrument,
    Locations.DonkeyGalleonInstrument,
    Locations.DonkeyCavesInstrument,
    Locations.DonkeyCastleInstrument,
}
DiddyMoveLocations = {
    Locations.ChimpyCharge,
    Locations.RocketbarrelBoost,
    Locations.SimianSpring,
    Locations.PeanutGun,
    Locations.Guitar,
    Locations.DiddyGalleonPotion,
    Locations.DiddyForestPotion,
    Locations.DiddyCavesPotion,
    Locations.DiddyCastlePotion,
    Locations.DiddyAztecGun,
    Locations.DiddyFactoryGun,
    Locations.DiddyGalleonGun,
    Locations.DiddyForestGun,
    Locations.DiddyCavesGun,
    Locations.DiddyCastleGun,
    Locations.DiddyFactoryInstrument,
    Locations.DiddyGalleonInstrument,
    Locations.DiddyCavesInstrument,
    Locations.DiddyCastleInstrument,
}
LankyMoveLocations = {
    Locations.Orangstand,
    Locations.BaboonBalloon,
    Locations.OrangstandSprint,
    Locations.GrapeGun,
    Locations.Trombone,
    Locations.LankyAztecPotion,
    Locations.LankyGalleonPotion,
    Locations.LankyForestPotion,
    Locations.LankyCastlePotion,
    Locations.LankyAztecGun,
    Locations.LankyFactoryGun,
    Locations.LankyGalleonGun,
    Locations.LankyForestGun,
    Locations.LankyCavesGun,
    Locations.LankyCastleGun,
    Locations.LankyFactoryInstrument,
    Locations.LankyGalleonInstrument,
    Locations.LankyCavesInstrument,
    Locations.LankyCastleInstrument,
}
TinyMoveLocations = {
    Locations.MiniMonkey,
    Locations.PonyTailTwirl,
    Locations.Monkeyport,
    Locations.FeatherGun,
    Locations.Saxophone,
    Locations.TinyAztecPotion,
    Locations.TinyGalleonPotion,
    Locations.TinyForestPotion,
    Locations.TinyCastlePotion,
    Locations.TinyAztecGun,
    Locations.TinyFactoryGun,
    Locations.TinyGalleonGun,
    Locations.TinyForestGun,
    Locations.TinyCavesGun,
    Locations.TinyCastleGun,
    Locations.TinyFactoryInstrument,
    Locations.TinyGalleonInstrument,
    Locations.TinyCavesInstrument,
    Locations.TinyCastleInstrument,
}
ChunkyMoveLocations = {
    Locations.HunkyChunky,
    Locations.PrimatePunch,
    Locations.GorillaGone,
    Locations.PineappleGun,
    Locations.Triangle,
    Locations.ChunkyAztecPotion,
    Locations.ChunkyGalleonPotion,
    Locations.ChunkyForestPotion,
    Locations.ChunkyCastlePotion,
    Locations.ChunkyAztecGun,
    Locations.ChunkyFactoryGun,
    Locations.ChunkyGalleonGun,
    Locations.ChunkyForestGun,
    Locations.ChunkyCavesGun,
    Locations.ChunkyCastleGun,
    Locations.ChunkyFactoryInstrument,
    Locations.ChunkyGalleonInstrument,
    Locations.ChunkyCavesInstrument,
    Locations.ChunkyCastleInstrument,
}
SharedMoveLocations = {
    Locations.SuperSimianSlam,
    Locations.SuperDuperSimianSlam,
    Locations.SniperSight,
    Locations.HomingAmmo,
    Locations.AmmoBelt1,
    Locations.AmmoBelt2,
    Locations.MusicUpgrade1,
    Locations.ThirdMelon,
    Locations.MusicUpgrade2,
    Locations.SharedJapesPotion,
    Locations.SharedJapesGun,
    Locations.SharedAztecPotion,
    Locations.SharedAztecGun,
    Locations.SharedAztecInstrument,
    Locations.SharedFactoryPotion,
    Locations.SharedFactoryInstrument,
    Locations.SharedGalleonPotion,
    Locations.SharedGalleonGun,
    Locations.SharedCavesPotion,
}
DonkeyMoves = [Items.Coconut, Items.Bongos, Items.BaboonBlast, Items.StrongKong, Items.GorillaGrab]
DiddyMoves = [Items.Peanut, Items.Guitar, Items.ChimpyCharge, Items.RocketbarrelBoost, Items.SimianSpring]
LankyMoves = [Items.Grape, Items.Trombone, Items.Orangstand, Items.BaboonBalloon, Items.OrangstandSprint]
TinyMoves = [Items.Feather, Items.Saxophone, Items.MiniMonkey, Items.PonyTailTwirl, Items.Monkeyport]
ChunkyMoves = [Items.Pineapple, Items.Triangle, Items.HunkyChunky, Items.PrimatePunch, Items.GorillaGone]
ImportantSharedMoves = [Items.ProgressiveSlam, Items.ProgressiveSlam, Items.SniperSight, Items.HomingAmmo]
JunkSharedMoves = [Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade]
