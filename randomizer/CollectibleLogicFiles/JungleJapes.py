# fmt: off
"""Collectible logic file for Jungle Japes."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesMain: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: l.vines, None, 5),  # Starting area
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 6),  # Between Snide's and Diddy's cage
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 2),  # W3
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Tree by Funky's
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Tree by cannon
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # Tree by Diddy's cage
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 1),  # By Troff n Scoff
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Above underground
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Snide's
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5),  # Starting area
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 7),  # Around mountain
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 2),  # Treetops, TB side
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 2),  # Treetops, Painting room side
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 2),  # Underwater
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Above mountain
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5),  # In river
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.handstand, None, 3),  # To painting room
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Treetop by Snide's
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # Next to Snide's
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 5),  # In first tunnel
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 5),  # Around entrance to underground
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 2),  # On Funky's store

        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.vines, None, 3),  # Around BBlast pad
    ],
    Regions.JapesBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: True, None, 2),

    ],
    Regions.JapesBeyondCoconutGate1: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 10),

    ],
    Regions.JapesBeyondCoconutGate2: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: True, None, 9),  # Path to Cranky
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.coconut, None, 1),  # Under Rambi box
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: Events.Rambi in l.Events, None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # In front of Cranky's
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 3),  # By Diddy BP
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: Events.Rambi in l.Events, None, 1),  # In breakable hut
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 1),  # To Lanky BP room
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.handstand, None, 6),  # On slippery slopes
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.handstand, None, 1),  # On top of slippery slope
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 1),  # On treetop in Cranky area
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: Events.Rambi in l.Events, None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # In Lanky BP room
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # By hut
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # On treetop in Cranky area
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: Events.Rambi in l.Events, None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # By hut
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),  # On Cranky's Lab

    ],
    Regions.JapesBeyondFeatherGate: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini, None, 3),  # In hollow trunk to the left
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini, None, 3),  # In hollow trunk to the right
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: True, None, 1),  # By beehive
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 4),

    ],
    Regions.JapesBeyondPeanutGate: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.grape, None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.feather, None, 1),

    ],
    Regions.Mine: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: True, None, 5),  # In stream
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # On mound by peanut switch
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # On box by conveyors
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: True, None, 1),  # In minecart
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # In conveyor room

    ],
    Regions.JapesLankyCave: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 2),  # On steps
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: True, None, 2),  # On pegs
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),

    ],
    Regions.BeyondRambiGate: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: True, None, 5),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 7),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 3),

    ],
    Regions.TinyHive: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: True, None, 8),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),

    ],
    Regions.JapesCatacomb: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: True, None, 2),

    ]
}
