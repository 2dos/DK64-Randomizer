# fmt: off
"""Collectible logic file for Frantic Factory."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.FranticFactoryStart: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5), # First tunnel
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1), # W2
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1), # W1
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1), # Around hatch


    ],
    Regions.Testing: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5), # Path to Numbers game
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1), # Numbers game
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 3), # Path to Funky
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1), # W5
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.spring, None, 5), # Block Tower
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 10), # Path to testing room
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1), # Block tower side of Mini Monkey tunnel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini, None, 1), # Spinning wheel
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1), # By Snide's HQ
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1), # By Funky's
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1), # W3
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1), # Above Snide's room
        
        
    ],
    Regions.RandD: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut and l.guitar, None, 3),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 10), # Around R&D
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1), # W2
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1), # Piano game
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 10), # To car race
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 10), # Toy Monster room
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1), # Toy Monster room
        
        
    ],
    Regions.FactoryTinyRaceLobby: [
        
        
    ],
    Regions.ChunkyRoomPlatform: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch, None, 3),
        

    ],
    Regions.PowerHut: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 3),
        
        
    ],
    Regions.BeyondHatch: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 6), # Tunnel to production room
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 4), # Tunnel between production room and Chunky room
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1), # By shops
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5), # Path to DK Arcade
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 12), # Around bottom of production room
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1), # W5
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5), # Path to shops
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.handstand, None, 5), # Pipe to free Chunky switch
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1), # In arcade room
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 2), # Halfway down the hatch
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 10), # On pole down the hatch
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1), # W1
        
        
    ],
    Regions.FactoryBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 4),
        
        
    ],
    Regions.InsideCore: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 3),
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
        
        
    ],
    Regions.MainCore: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 3), # On cylinders and Simian Spring pad
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 3), # On steps on middle level
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.handstand, None, 5), # On pipe to production room GB
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1), # By T&S portal
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 4), # On conveyors to Bonus Barrel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.twirl, None, 1), # On platform past Bonus Barrel
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1), # On middle level
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 4), # on rotating arms
        
        
    ],
}
