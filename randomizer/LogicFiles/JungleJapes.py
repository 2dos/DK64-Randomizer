from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Jungle Japes Main": Region("Jungle Japes Main", True, [
        Location("Diddy Kong", lambda l: l.coconut),
        Location("Japes Donkey Front of Cage", lambda l: l.isdonkey),
        Location("Japes Donkey Free Diddy", lambda l: l.coconut and l.isdonkey),
        Location("Japes Donkey Caged Banana", lambda l: Events.JapesDonkeySwitch in l.Events and l.isdonkey),
        Location("Japes Donkey Baboon Blast", lambda l: l.blast and l.isdonkey),
        Location("Japes Diddy Caged Banana", lambda l: Events.JapesDiddySwitch1 in l.Events and l.isdiddy),
        Location("Japes Diddy Mountain", lambda l: Events.JapesDiddySwitch2 in l.Events and l.isdiddy),
        Location("Japes Lanky Caged Banana", lambda l: Events.JapesLankySwitch in l.Events and l.islanky),
        Location("Japes Tiny Caged Banana", lambda l: Events.JapesTinySwitch in l.Events and l.istiny),
        Location("Japes Chunky Boulder", lambda l: l.ischunky),
        Location("Japes Chunky Caged Banana", lambda l: Events.JapesChunkySwitch and l.ischunky),
        Location("Japes Battle Arena", lambda l: True),
    ], [], [
        Exit("Jungle Japes Lobby", lambda l: True),
        Exit("Japes Beyond Peanut Gate", lambda l: l.peanut),
        Exit("Japes Beyond Coconut Gate 1", lambda l: l.coconut),
        Exit("Japes Beyond Coconut Gate 2", lambda l: l.coconut),
        Exit("Mine", lambda l: l.peanut and l.isdiddy),
        Exit("Japes Lanky Cave", lambda l: l.peanut and l.handstand and l.islanky),
        Exit("Japes Catacomb", lambda l: l.chunkyAccess and l.Slam),
        Exit("Funky", lambda l: True),
        Exit("Snide", lambda l: True),
        Exit("Japes Boss Lobby", lambda l: True),
    ]),

    "Japes Beyond Peanut Gate": Region("Japes Beyond Peanut Gate", False, [
        Location("Japes Diddy Tunnel", lambda l: l.isdiddy),
        Location("Japes Lanky Mad Maze Maul", lambda l: l.grape and l.islanky),
        Location("Japes Tiny Splish Splash Salvage", lambda l: l.feather and l.istiny),
    ], [], [
        Exit("Japes Boss Lobby", lambda l: True),
    ]),

    "Japes Beyond Coconut Gate 1": Region("Japes Beyond Coconut Gate 1", False, [
        Location("Japes Donkey Kasplat", lambda l: l.isdonkey),
        Location("Japes Tiny Kasplat", lambda l: l.istiny),
    ], [], [
        Exit("Japes Beyond Feather Gate", lambda l: l.feather and l.tinyAccess),
    ]),

    "Japes Beyond Feather Gate": Region("Japes Beyond Feather Gate", True, [
        Location("Japes Tiny Stump", lambda l: l.mini and l.istiny),
        Location("Japes Chunky Minecart Mayhem", lambda l: l.hunkyChunky and l.ischunky),
    ], [], [
        Exit("Tiny Hive", lambda l: l.mini and l.istiny),
    ]),

    "Tiny Hive": Region("Tiny Hive", False, [
        Location("Japes Tiny Beehive", lambda l: l.Slam and l.istiny),
    ], [], [
        Exit("Japes Beyond Feather Gate", lambda l: True),
    ]),

    "Japes Beyond Coconut Gate 2": Region("Japes Beyond Coconut Gate 2", True, [
        Location("Japes Lanky Speedy Swing Sortie", lambda l: l.handstand and l.islanky),
        Location("Japes Diddy Kasplat", lambda l: l.isdiddy),
        Location("Japes Lanky Kasplat", lambda l: l.islanky),
    ], [
        Event(Events.Rambi, lambda l: l.coconut),
        Event(Events.JapesDonkeySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.isdonkey),
        Event(Events.JapesDiddySwitch1, lambda l: Events.Rambi in l.Events and l.Slam and l.isdiddy),
        Event(Events.JapesLankySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.islanky),
        Event(Events.JapesTinySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.istiny),
    ], [
        Exit("Beyond Rambi Gate", lambda l: Events.Rambi in l.Events),
        Exit("Cranky", lambda l: True),
    ]),

    "Beyond Rambi Gate": Region("Beyond Rambi Gate", False, [
        Location("Japes Banana Fairy Rambi Cave", lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.Slam and l.ischunky),
    ], [
        Exit("Japes Boss Lobby", lambda l: True),
    ]),

    "Japes Lanky Cave": Region("Japes Lanky Cave", False, [
        Location("Japes Lanky Fairy Cave", lambda l: l.grape and l.islanky),
        Location("Japes Banana Fairy Lanky Cave", lambda l: l.grape and l.camera and l.islanky),
    ], [], [
        Exit("Jungle Japes Main", lambda l: True),
    ]),

    "Mine": Region("Mine", False, [], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Events(Events.JapesDiddySwitch2, lambda l: l.Slam and l.isdiddy),
    ], [
        Exit("Jungle Japes Main", lambda l: True),
        Exit("Japes Minecarts", lambda l: l.charge and l.Slam and l.isdiddy),
    ]),

    "Japes Minecarts": Region("Japes Minecarts", False, [
        Location("Japes Diddy Minecarts", lambda l: l.isdiddy),
    ], [], []),

    "Japes Catacomb": Region("Japes Catacomb", False, [
        Location("Japes Chunky Underground", lambda l: l.pineapple and l.ischunky),
        Location("Japes Chunky Kasplat", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit("Jungle Japes Main", lambda l: True),
    ]),

    "Japes Boss Lobby": Region("Japes Boss Lobby", True, [], [], [
        # 50 bananas
        Exit("Japes Boss", lambda l: l.isdonkey),
    ]),

    "Japes Boss": Region("Japes Boss", False, [
        Location("Japes Key", lambda l: l.isdonkey),
    ], [], []),
}
