# fmt: off
"""Logic file for Jungle Japes."""

from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Levels import Levels

LogicRegions = {
    Regions.JungleJapesMain: Region("Jungle Japes Main", Levels.JungleJapes, True, [
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
    ], [
        Event(Events.JapesEntered, lambda l: True),
    ], [
        Exit(Regions.JungleJapesLobby, lambda l: True),
        Exit(Regions.JapesBeyondPeanutGate, lambda l: l.peanut),
        Exit(Regions.JapesBeyondCoconutGate1, lambda l: l.coconut),
        Exit(Regions.JapesBeyondCoconutGate2, lambda l: l.coconut),
        Exit(Regions.Mine, lambda l: l.peanut and l.isdiddy),
        Exit(Regions.JapesLankyCave, lambda l: l.peanut and l.handstand and l.islanky),
        Exit(Regions.JapesCatacomb, lambda l: l.Slam and l.chunkyAccess),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesBeyondPeanutGate: Region("Japes Beyond Peanut Gate", Levels.JungleJapes, False, [
        Location("Japes Diddy Tunnel", lambda l: l.isdiddy),
        Location("Japes Lanky Mad Maze Maul", lambda l: l.grape and l.islanky),
        Location("Japes Tiny Splish Splash Salvage", lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", Levels.JungleJapes, False, [
        Location("Japes Donkey Kasplat", lambda l: l.isdonkey),
        Location("Japes Tiny Kasplat", lambda l: l.istiny),
    ], [], [
        Exit(Regions.JapesBeyondFeatherGate, lambda l: l.feather and l.tinyAccess),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", Levels.JungleJapes, True, [
        Location("Japes Tiny Stump", lambda l: l.mini and l.istiny),
        Location("Japes Chunky Minecart Mayhem", lambda l: l.hunkyChunky and l.ischunky),
    ], [], [
        Exit(Regions.TinyHive, lambda l: l.mini and l.istiny),
    ]),

    Regions.TinyHive: Region("Tiny Hive", Levels.JungleJapes, False, [
        Location("Japes Tiny Beehive", lambda l: l.Slam and l.istiny),
    ], [], [
        Exit(Regions.JapesBeyondFeatherGate, lambda l: True),
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", Levels.JungleJapes, True, [
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
        Exit(Regions.BeyondRambiGate, lambda l: Events.Rambi in l.Events),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.BeyondRambiGate: Region("Beyond Rambi Gate", Levels.JungleJapes, False, [
        Location("Japes Banana Fairy Rambi Cave", lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.Slam and l.ischunky),
    ], [
        Exit(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesLankyCave: Region("Japes Lanky Cave", Levels.JungleJapes, False, [
        Location("Japes Lanky Fairy Cave", lambda l: l.grape and l.islanky),
        Location("Japes Banana Fairy Lanky Cave", lambda l: l.grape and l.camera and l.islanky),
    ], [], [
        Exit(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.Mine: Region("Mine", Levels.JungleJapes, False, [], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Event(Events.JapesDiddySwitch2, lambda l: l.Slam and l.isdiddy),
    ], [
        Exit(Regions.JungleJapesMain, lambda l: True),
        Exit(Regions.JapesMinecarts, lambda l: l.charge and l.Slam and l.isdiddy),
    ]),

    Regions.JapesMinecarts: Region("Japes Minecarts", Levels.JungleJapes, False, [
        Location("Japes Diddy Minecarts", lambda l: l.isdiddy),
    ], [], []),

    Regions.JapesCatacomb: Region("Japes Catacomb", Levels.JungleJapes, False, [
        Location("Japes Chunky Underground", lambda l: l.pineapple and l.ischunky),
        Location("Japes Chunky Kasplat", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", Levels.JungleJapes, True, [], [], [
        # 50 bananas
        Exit(Regions.JapesBoss, lambda l: l.isdonkey),
    ]),

    Regions.JapesBoss: Region("Japes Boss", Levels.JungleJapes, False, [
        Location("Japes Key", lambda l: l.isdonkey),
    ], [], []),
}
