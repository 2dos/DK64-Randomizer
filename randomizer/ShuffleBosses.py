"""Randomize Boss Locations."""
import random
from array import array
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.MapsAndExits import Maps

BossMapList = [Maps.JapesBoss, Maps.AztecBoss, Maps.FactoryBoss, Maps.GalleonBoss, Maps.FungiBoss, Maps.CavesBoss, Maps.CastleBoss]


def ShuffleBosses(boss_location_rando: bool):
    """Shuffle boss locations."""
    boss_maps = BossMapList.copy()
    if boss_location_rando:
        random.shuffle(boss_maps)
    return boss_maps


def ShuffleBossKongs(boss_maps: array, boss_kong_rando: bool):
    """Shuffle the kongs required for the bosses."""
    vanillaBossKongs = {}
    vanillaBossKongs[Maps.JapesBoss] = Kongs.donkey
    vanillaBossKongs[Maps.AztecBoss] = Kongs.diddy
    vanillaBossKongs[Maps.FactoryBoss] = Kongs.tiny
    vanillaBossKongs[Maps.GalleonBoss] = Kongs.lanky
    vanillaBossKongs[Maps.FungiBoss] = Kongs.chunky
    vanillaBossKongs[Maps.CavesBoss] = Kongs.donkey
    vanillaBossKongs[Maps.CastleBoss] = Kongs.lanky

    boss_kongs = []
    for level in range(7):
        boss_map = boss_maps[level]
        if boss_kong_rando:
            kong = SelectRandomKongForBoss(boss_map)
        else:
            kong = vanillaBossKongs[boss_map]
        boss_kongs.append(kong)

    return boss_kongs


def SelectRandomKongForBoss(boss_map: Maps):
    """Randomly choses from the allowed list for the boss."""
    if boss_map == Maps.JapesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.AztecBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FactoryBoss:
        possibleKongs = [Kongs.donkey, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.GalleonBoss:
        possibleKongs = [Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FungiBoss:
        possibleKongs = [Kongs.chunky]
    elif boss_map == Maps.CavesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.chunky]
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


def ShuffleBossesBasedOnOwnedItems(settings, ownedKongs: dict, ownedMoves: dict):
    """Perform Boss Location & Boss Kong rando, ensuring each first boss can be beaten with an unlocked kong and owned moves."""
    bossLevelOptions = {0, 1, 2, 3, 4, 5, 6}
    # First place dogadon 2 (most restrictive)
    forestBossOptions = [x for x in bossLevelOptions if Kongs.chunky in ownedKongs[x] and Items.HunkyChunky in ownedMoves[x]]
    forestBossIndex = random.choice(forestBossOptions)
    forestBossKong = Kongs.chunky
    bossLevelOptions.remove(forestBossIndex)
    # Then place Mad jack (next most restrictive)
    factoryBossOptions = [x for x in bossLevelOptions if Kongs.donkey in ownedKongs[x] or Kongs.chunky in ownedKongs[x] or (Kongs.tiny in ownedKongs[x] and Items.PonyTailTwirl in ownedMoves[x])]
    factoryBossIndex = random.choice(factoryBossOptions)
    factoryBossKongOptions = set(ownedKongs[factoryBossIndex]).intersection({Kongs.donkey, Kongs.chunky})
    if Kongs.tiny in ownedKongs[factoryBossIndex] and Items.PonyTailTwirl in ownedMoves[factoryBossIndex]:
        factoryBossKongOptions.add(Kongs.tiny)
    factoryBossKong = random.choice(list(factoryBossKongOptions))
    bossLevelOptions.remove(factoryBossIndex)
    # Then place Pufftoss (next most restrictive)
    galleonBossOptions = [x for x in bossLevelOptions if Kongs.diddy in ownedKongs[x] or Kongs.lanky in ownedKongs[x] or Kongs.tiny in ownedKongs[x] or Kongs.chunky in ownedKongs[x]]
    galleonBossIndex = random.choice(galleonBossOptions)
    galleonBossKongOptions = set(ownedKongs[galleonBossIndex]).intersection({Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky})
    galleonBossKong = random.choice(list(galleonBossKongOptions))
    bossLevelOptions.remove(galleonBossIndex)
    # Place the rest randomly
    remainingBosses = list(bossLevelOptions)
    random.shuffle(remainingBosses)
    japesBossIndex = remainingBosses.pop()
    japesBossKong = random.choice(ownedKongs[japesBossIndex])
    aztecBossIndex = remainingBosses.pop()
    aztecBossKong = random.choice(ownedKongs[aztecBossIndex])
    cavesBossIndex = remainingBosses.pop()
    cavesBossKong = random.choice(ownedKongs[cavesBossIndex])
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
    print("New Boss Order: " + str(newBossMaps))
    print("New Boss Kongs: " + str(newBossKongs))
    if len(newBossMaps) < 7:
        raise Exception("Invalid boss order with fewer than the 7 required main levels.")
    settings.boss_maps = newBossMaps
    settings.boss_kongs = newBossKongs
    settings.kutout_kongs = ShuffleKutoutKongs(settings.boss_maps, settings.boss_kongs, True)
