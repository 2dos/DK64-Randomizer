"""Randomize Boss Locations."""
import random
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