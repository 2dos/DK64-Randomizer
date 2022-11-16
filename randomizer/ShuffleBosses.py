"""Randomize Boss Locations."""
import random
from array import array

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.Exceptions import BossOutOfLocationsException, FillException, ItemPlacementException
from randomizer.Lists.MapsAndExits import Maps

BossMapList = [Maps.JapesBoss, Maps.AztecBoss, Maps.FactoryBoss, Maps.GalleonBoss, Maps.FungiBoss, Maps.CavesBoss, Maps.CastleBoss]


def ShuffleBosses(boss_location_rando: bool):
    """Shuffle boss locations."""
    boss_maps = BossMapList.copy()
    if boss_location_rando:
        random.shuffle(boss_maps)
    return boss_maps


def ShuffleBossKongs(settings):
    """Shuffle the kongs required for the bosses."""
    vanillaBossKongs = {
        Maps.JapesBoss: Kongs.donkey,
        Maps.AztecBoss: Kongs.diddy,
        Maps.FactoryBoss: Kongs.tiny,
        Maps.GalleonBoss: Kongs.lanky,
        Maps.FungiBoss: Kongs.chunky,
        Maps.CavesBoss: Kongs.donkey,
        Maps.CastleBoss: Kongs.lanky,
    }

    boss_kongs = []
    for level in range(7):
        boss_map = settings.boss_maps[level]
        if settings.boss_kong_rando:
            kong = SelectRandomKongForBoss(boss_map, settings.hard_bosses)
        else:
            kong = vanillaBossKongs[boss_map]
        boss_kongs.append(kong)

    return boss_kongs


def SelectRandomKongForBoss(boss_map: Maps, hard_bosses: bool):
    """Randomly choses from the allowed list for the boss."""
    possibleKongs = []
    if boss_map == Maps.JapesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.AztecBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FactoryBoss:
        if hard_bosses:
            possibleKongs = [Kongs.donkey, Kongs.tiny, Kongs.chunky]
        else:
            possibleKongs = [Kongs.tiny]
    elif boss_map == Maps.GalleonBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FungiBoss:
        possibleKongs = [Kongs.chunky]
    elif boss_map == Maps.CavesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.CastleBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    return random.choice(possibleKongs)


def ShuffleKutoutKongs(boss_maps: array, boss_kongs: array, boss_kong_rando: bool):
    """Shuffle the Kutout kong order."""
    vanillaKutoutKongs = [Kongs.lanky, Kongs.tiny, Kongs.chunky, Kongs.donkey, Kongs.diddy]
    kutout_kongs = []
    if boss_kong_rando:
        kutoutLocation = boss_maps.index(Maps.CastleBoss)
        starting_kong = boss_kongs[kutoutLocation]
        kongPool = vanillaKutoutKongs.copy()
        kongPool.remove(starting_kong)
        random.shuffle(kongPool)

        kutout_kongs.append(starting_kong)
        kutout_kongs.extend(kongPool)
    else:
        kutout_kongs = vanillaKutoutKongs
    return kutout_kongs


def ShuffleKKOPhaseOrder(settings):
    """Shuffle the phase order in King Kut Out."""
    kko_phases = [0, 1, 2, 3]
    random.shuffle(kko_phases)
    kko_phase_subset = []
    for phase_slot in range(3):
        kko_phase_subset.append(kko_phases[phase_slot])
    return kko_phase_subset.copy()


def ShuffleBossesBasedOnOwnedItems(settings, ownedKongs: dict, ownedMoves: dict):
    """Perform Boss Location & Boss Kong rando, ensuring each first boss can be beaten with an unlocked kong and owned moves."""
    try:
        bossLevelOptions = {0, 1, 2, 3, 4, 5, 6}
        # Find levels we can place Dogadon 2 (most restrictive)
        forestBossOptions = [x for x in bossLevelOptions if Kongs.chunky in ownedKongs[x] and Items.HunkyChunky in ownedMoves[x] and Items.Barrels in ownedMoves[x]]
        if not settings.kong_rando and not settings.boss_location_rando and 4 not in forestBossOptions:
            raise ItemPlacementException("Items not placed to allow vanilla Dogadon 2.")
        # Then find levels we can place Mad jack (next most restrictive)
        if settings.hard_bosses:
            factoryBossOptions = [
                x for x in bossLevelOptions if Kongs.donkey in ownedKongs[x] or Kongs.chunky in ownedKongs[x] or (Kongs.tiny in ownedKongs[x] and Items.PonyTailTwirl in ownedMoves[x])
            ]
        else:
            factoryBossOptions = [x for x in bossLevelOptions if Kongs.tiny in ownedKongs[x] and Items.PonyTailTwirl in ownedMoves[x]]
        # This sequence of placing Dogadon 2 and Mad Jack will only fail if both Hunky Chunky and Twirl are placed in level 7
        # If we have fewer options for Dogadon 2, place that first
        forestBossKong = None
        bossTryingToBePlaced = "Dogadon 2"
        if len(forestBossOptions) < len(factoryBossOptions):
            forestBossIndex = random.choice(forestBossOptions)
            forestBossKong = Kongs.chunky
            if forestBossIndex in factoryBossOptions:
                factoryBossOptions.remove(forestBossIndex)
        # Otherwise place Factory first
        bossTryingToBePlaced = "Mad Jack"
        if settings.hard_bosses:
            factoryBossIndex = random.choice(factoryBossOptions)
            factoryBossKongOptions = set(ownedKongs[factoryBossIndex]).intersection({Kongs.donkey, Kongs.chunky})
            if Kongs.tiny in ownedKongs[factoryBossIndex] and Items.PonyTailTwirl in ownedMoves[factoryBossIndex]:
                factoryBossKongOptions.add(Kongs.tiny)
            factoryBossKong = random.choice(list(factoryBossKongOptions))
        else:
            factoryBossIndex = random.choice(factoryBossOptions)
            factoryBossKong = Kongs.tiny
        if factoryBossIndex in forestBossOptions:
            forestBossOptions.remove(factoryBossIndex)
        # Then place Dogadon 2 (if Mad Jack was placed first)
        if forestBossKong is None:
            bossTryingToBePlaced = "Dogadon 2"
            forestBossIndex = random.choice(forestBossOptions)
            forestBossKong = Kongs.chunky

        bossLevelOptions.remove(forestBossIndex)
        bossLevelOptions.remove(factoryBossIndex)

        # Place the barrels-required bosses
        bossTryingToBePlaced = "barrels-locked bosses"
        barrelsBossOptions = [x for x in bossLevelOptions if Items.Barrels in ownedMoves[x]]
        random.shuffle(barrelsBossOptions)
        cavesBossIndex = barrelsBossOptions.pop()
        cavesBossKong = random.choice(ownedKongs[cavesBossIndex])
        bossLevelOptions.remove(cavesBossIndex)
        japesBossIndex = barrelsBossOptions.pop()
        japesBossKong = random.choice(ownedKongs[japesBossIndex])
        bossLevelOptions.remove(japesBossIndex)
        aztecBossIndex = barrelsBossOptions.pop()
        aztecBossKong = random.choice(ownedKongs[aztecBossIndex])
        bossLevelOptions.remove(aztecBossIndex)

        # Place the last 2 freely
        bossTryingToBePlaced = "the easy bosses to place (if this breaks here something REALLY strange happened)"
        remainingBosses = list(bossLevelOptions)
        random.shuffle(remainingBosses)
        galleonBossIndex = remainingBosses.pop()
        galleonBossKong = random.choice(ownedKongs[galleonBossIndex])
        castleBossIndex = remainingBosses.pop()
        castleBossKong = random.choice(ownedKongs[castleBossIndex])
        newBossMaps = []
        newBossKongs = []
        for level in range(0, 7):
            if level == japesBossIndex:
                newBossMaps.append(Maps.JapesBoss)
                newBossKongs.append(japesBossKong)
            elif level == aztecBossIndex:
                newBossMaps.append(Maps.AztecBoss)
                newBossKongs.append(aztecBossKong)
            elif level == factoryBossIndex:
                newBossMaps.append(Maps.FactoryBoss)
                newBossKongs.append(factoryBossKong)
            elif level == galleonBossIndex:
                newBossMaps.append(Maps.GalleonBoss)
                newBossKongs.append(galleonBossKong)
            elif level == forestBossIndex:
                newBossMaps.append(Maps.FungiBoss)
                newBossKongs.append(forestBossKong)
            elif level == cavesBossIndex:
                newBossMaps.append(Maps.CavesBoss)
                newBossKongs.append(cavesBossKong)
            elif level == castleBossIndex:
                newBossMaps.append(Maps.CastleBoss)
                newBossKongs.append(castleBossKong)
        # print("New Boss Order: " + str(newBossMaps))
        # print("New Boss Kongs: " + str(newBossKongs))
        if len(newBossMaps) < 7:
            raise FillException("Invalid boss order with fewer than the 7 required main levels.")
    except Exception as ex:
        if isinstance(ex.args[0], str) and "index out of range" in ex.args[0]:
            print("Unlucky move placement fill :(")
            raise BossOutOfLocationsException("No valid locations to place " + bossTryingToBePlaced)
        if isinstance(ex.args[0], str) and "pop from empty list" in ex.args[0]:
            print("Barrels bad.")
            raise BossOutOfLocationsException("No valid locations to place " + bossTryingToBePlaced)
        raise ex

    # Only apply this shuffle if the settings permit it
    # If kongs are random we have to shuffle bosses and locations or else we might break logic
    if settings.kong_rando or settings.boss_location_rando:
        settings.boss_maps = newBossMaps
    else:
        settings.boss_maps = BossMapList.copy()
    if settings.kong_rando or settings.boss_kong_rando:
        # If we shuffle kongs but not locations, we must forcibly sort the array with the known valid kongs
        if not settings.boss_location_rando:
            settings.boss_kongs = [japesBossKong, aztecBossKong, factoryBossKong, galleonBossKong, forestBossKong, cavesBossKong, castleBossKong]
        else:
            settings.boss_kongs = newBossKongs
    else:
        settings.boss_kongs = ShuffleBossKongs(settings)
    settings.kutout_kongs = ShuffleKutoutKongs(settings.boss_maps, settings.boss_kongs, settings.boss_kong_rando)
