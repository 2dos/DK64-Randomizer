# fmt: off
"""Collectible logic file for Fungi Forest."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.FungiForestStart: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5),  # To Giant Mushroom Area
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5),  # To Mill Area
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 2),  # Bounce
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # Warp 4
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Warp 1
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # Warp 3
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: l.feather, None, 4),  # Behind feather gate only
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Warp 2
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Minecart Entry
    ],
    Regions.ForestMinecarts: [
    ],
    Regions.GiantMushroomArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Lower Warp 5
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 2),  # Rocketbarrel
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Warp 3
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 10),
    ],
    Regions.MushroomLower: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: Events.MushroomCannonsSpawned in l.Events, None, 3),  # Cannon shots pathway
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 1st Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # After 1st Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 2nd Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # After 2nd Ladder
    ],
    Regions.MushroomLowerExterior: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 15),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ForestBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 2),
    ],
    Regions.MushroomUpper: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 7),
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # Top
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 3rd Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # After 3rd Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 4th Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 5th Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 6th Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # 7th Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Top
    ],
    Regions.MushroomNightDoor: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),
    ],
    Regions.MushroomNightExterior: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.MushroomUpperExterior: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Upper Warp 5
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 10),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.handstand, None, 1),  # Top of mushroom
    ],
    Regions.MushroomChunkyRoom: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.MushroomLankyZingersRoom: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 2),
    ],
    Regions.MushroomLankyMushroomsRoom: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),
    ],
    Regions.HollowTreeArea: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 10),  # Around Tree
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # Warp 4
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Top of Tree
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 10),  # Tunnel
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 3),  # To Rabbit
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # To Rabbit
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 8),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.saxophone and l.mini, None, 1),
    ],
    Regions.Anthill: [
    ],
    Regions.MillArea: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Behind Barn
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Snide
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 3),  # Near Rafter Barn
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.spring, None, 1),  # Near Rafter Barn
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 7),  # Mill roof
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Above Balloon pad
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: Events.Night in l.Events, None, 1),  # Attic Entrance
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 17),  # Underwater
    ],
    Regions.MillChunkyArea: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch, None, 1),
    ],
    Regions.MillTinyArea: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 2),  # Near Spider
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: Events.MillBoxBroken in l.Events, None, 1),  # Inside Box
    ],
    Regions.SpiderRoom: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),
    ],
    Regions.GrinderRoom: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.Slam, None, 1),  # In slam box
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.superSlam and l.coconut, None, 1),  # Behind gate
    ],
    Regions.MillRafters: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.guitar, None, 2),
    ],
    Regions.WinchRoom: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
    ],
    Regions.MillAttic: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),
    ],
    Regions.ThornvineArea: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 1),  # Behind on switch
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ThornvineBarn: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.Slam, None, 1),  # In slam box
    ],
    Regions.WormArea: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 3),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 1),  # Last one behind Pineapple gate
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Warp 2
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 9),
    ],
}
