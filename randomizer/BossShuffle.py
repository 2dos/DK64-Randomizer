"""Randomize Boss Locations."""
from array import array
import random
from randomizer.Enums.Kongs import Kongs
from randomizer.MapsAndExits import Maps

def ShuffleBosses(boss_location_rando:bool):
    boss_maps = [
        Maps.JapesBoss,
        Maps.AztecBoss,
        Maps.FactoryBoss,
        Maps.GalleonBoss,
        Maps.FungiBoss,
        Maps.CavesBoss,
        Maps.CastleBoss
    ]
    if boss_location_rando:
        random.shuffle(boss_maps)
    return boss_maps

def ShuffleBossKongs(boss_maps:array, boss_kong_rando:bool):
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

def SelectRandomKongForBoss(boss_map:Maps):
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
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.CastleBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    return random.choice(possibleKongs)