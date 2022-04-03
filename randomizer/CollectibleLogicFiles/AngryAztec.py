# fmt: off
"""Collectible logic file for Angry Aztec."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.AngryAztecStart: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.coconut and l.strongKong, None, 2),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 3),
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 3),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.pineapple, None, 4),
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 5),

        # Testing Coin access
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: True, None, 15),
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: True, None, 15),
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: True, None, 15),
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: True, None, 15),
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: True, None, 15),
    ],
    Regions.TempleStart: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.Slam, None, 3),
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: l.Slam, None, 3),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 5),
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 4),
    ],
    Regions.TempleUnderwater: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 7),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 9),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: l.mini, None, 5),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 2),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.AngryAztecMain: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 2),  # Cranky
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Behind Llama Temple
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong, None, 4),
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 3),  # Near Snide
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 4),  # Near Llama Temple

        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5),  # Behind Guitar Door
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 3),  # Near Rocketbarrel
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 3),  # Gongs steps
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 3),  # Gongs Trees
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # Sun Ring
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # On top llama temple
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 4),  # 5DTemple Steps
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.peanut, None, 1),

        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5),  # Snake Road
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Cranky
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 5),  # Treetops

        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 10),  # Tunnel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # Beetle Slide
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # Warp 5
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 5),  # Treetops around 5DTemple
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 5),  # 5DTemple path

        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 10),  # Around Totem
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 6),  # Snide
    ],
    Regions.AztecBaboonBlast: [
    ],
    Regions.DonkeyTemple: [
    ],
    Regions.DiddyTemple: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
    ],
    Regions.LankyTemple: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
    ],
    Regions.TinyTemple: [
    ],
    Regions.ChunkyTemple: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 2),
    ],
    Regions.AztecTinyRace: [
    ],
    Regions.LlamaTemple: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 15),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 6),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: lambda l: True, None, 1),  # Warp 1
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: lambda l: Events.AztecLlamaSpit in l.Events and l.grape, None, 2),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: lambda l: l.grape, None, 1),  # Matching game

        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 3),
    ],
    Regions.LlamaTempleBack: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 2),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.Slam or l.twirl, None, 2),  # Behind Mini tunnel
    ],
}
