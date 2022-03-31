# fmt: off
"""Collectible logic file for Crystal Caves."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.CrystalCavesMain: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Warp 1
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5),  # Near BBlast
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.punch and l.chunky and l.coconut, None, 1),  # Warp 1

        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5),  # Near Funky
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Near Bonus
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Warp 4 pillar
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Near Warp 4 pillar
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.mini and l.twirl and l.tiny and l.jetpack, None, 1),  # Warp 4 cave
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: l.mini and l.twirl and l.tiny and l.jetpack, None, 5),  # Warp 4 cave

        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5),  # Level Start
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.balloon and l.superSlam, None, 1),  # Beetle Race entry
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.jetpack and l.diddy, None, 4),  # Warp 5 platform
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.balloon, None, 3),  # Near Cranky

        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 10),  # River To Igloo
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini, None, 1),  # Warp 3 cave
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.mini and l.twirl and l.feather, None, 1),  # Warp 4 cave

        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch, None, 1),  # Gorilla Gone room
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: l.punch, None, 3),  # Gorilla Gone room
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Warp 2
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 2),  # Small Boulder and switch
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 3),  # Small Boulder and switch
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: l.punch, None, 3),  # Near Snide
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.punch and l.pineapple, None, 1),  # Near Snide
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.mini and l.twirl and l.tiny and l.pineapple, None, 1),  # Warp 3 cave
    ],
    Regions.CavesBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 4),
    ],
    Regions.BoulderCave: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 3),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),

        Collectible(Collectibles.banana, Kongs.chunky, lambda l: Events.CavesSmallBoulderButton in l.Events, None, 6),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky, None, 1),
    ],
    Regions.CavesLankyRace: [
    ],
    Regions.FrozenCastle: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
    ],
    Regions.IglooArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Warp 1
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 5),  # Around Igloo

        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 4),  # Above igloos

        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # Warp 3
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.monkeyport and l.mini and l.twirl, None, 1),  # Monkeyport Ice Shield

        Collectible(Collectibles.banana, Kongs.chunky, lambda l: Events.CavesLargeBoulderButton in l.Events, None, 5),  # Ice Shield
    ],
    Regions.GiantKosha: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 4),
    ],
    Regions.DonkeyIgloo: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 7),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
    ],
    Regions.DiddyIgloo: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
    ],
    Regions.LankyIgloo: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 1),  # First single
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.balloon, None, 4),  # Upper singles
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
    ],
    Regions.TinyIgloo: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ChunkyIgloo: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.CabinArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 10),  # River
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.balloon, None, 1),  # Top of Lanky cabin
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # Warp 2
    ],
    Regions.RotatingCabin: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),
    ],
    Regions.DonkeyCabin: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),
    ],
    Regions.DiddyLowerCabin: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5),
    ],
    Regions.DiddyUpperCabin: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack and l.spring, None, 3),
    ],
    Regions.LankyCabin: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),
    ],
    Regions.TinyCabin: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 2),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ChunkyCabin: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.gorillaGone and l.Slam, None, 4),
    ],
}
