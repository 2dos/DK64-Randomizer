# fmt: off
"""Logic file for Jungle Japes."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.JungleJapesMain: Region("Jungle Japes Main", Levels.JungleJapes, True, [
        LocationLogic(Locations.JapesDonkeyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.donkey] >= 75),
        LocationLogic(Locations.JapesDiddyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.diddy] >= 75),
        LocationLogic(Locations.JapesLankyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.lanky] >= 75),
        LocationLogic(Locations.JapesTinyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.tiny] >= 75),
        LocationLogic(Locations.JapesChunkyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.chunky] >= 75),
        LocationLogic(Locations.DiddyKong, lambda l: l.coconut),
        LocationLogic(Locations.JapesDonkeyFrontofCage, lambda l: l.isdonkey),
        LocationLogic(Locations.JapesDonkeyFreeDiddy, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.JapesDonkeyCagedBanana, lambda l: Events.JapesDonkeySwitch in l.Events and l.isdonkey),
        LocationLogic(Locations.JapesDonkeyBaboonBlast, lambda l: l.blast and l.isdonkey),
        LocationLogic(Locations.JapesDiddyCagedBanana, lambda l: Events.JapesDiddySwitch1 in l.Events and l.isdiddy),
        LocationLogic(Locations.JapesDiddyMountain, lambda l: Events.JapesDiddySwitch2 in l.Events and l.isdiddy),
        LocationLogic(Locations.JapesLankyCagedBanana, lambda l: Events.JapesLankySwitch in l.Events and l.islanky),
        LocationLogic(Locations.JapesTinyCagedBanana, lambda l: Events.JapesTinySwitch in l.Events and l.istiny),
        LocationLogic(Locations.JapesChunkyBoulder, lambda l: l.ischunky),
        LocationLogic(Locations.JapesChunkyCagedBanana, lambda l: Events.JapesChunkySwitch and l.ischunky),
        LocationLogic(Locations.JapesBattleArena, lambda l: True),
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
        LocationLogic(Locations.JapesDiddyTunnel, lambda l: l.isdiddy),
        LocationLogic(Locations.JapesLankyMadMazeMaul, lambda l: l.grape and l.islanky),
        LocationLogic(Locations.JapesTinySplishSplashSalvage, lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", Levels.JungleJapes, False, [
        LocationLogic(Locations.JapesDonkeyKasplat, lambda l: l.isdonkey),
        LocationLogic(Locations.JapesTinyKasplat, lambda l: l.istiny),
    ], [], [
        Exit(Regions.JapesBeyondFeatherGate, lambda l: l.feather and l.tinyAccess),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", Levels.JungleJapes, True, [
        LocationLogic(Locations.JapesTinyStump, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.JapesChunkyMinecartMayhem, lambda l: l.hunkyChunky and l.ischunky),
    ], [], [
        Exit(Regions.TinyHive, lambda l: l.mini and l.istiny),
    ]),

    Regions.TinyHive: Region("Tiny Hive", Levels.JungleJapes, False, [
        LocationLogic(Locations.JapesTinyBeehive, lambda l: l.Slam and l.istiny),
    ], [], [
        Exit(Regions.JapesBeyondFeatherGate, lambda l: True),
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", Levels.JungleJapes, True, [
        LocationLogic(Locations.JapesLankySpeedySwingSortie, lambda l: l.handstand and l.islanky),
        LocationLogic(Locations.JapesDiddyKasplat, lambda l: l.isdiddy),
        LocationLogic(Locations.JapesLankyKasplat, lambda l: l.islanky),
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
        LocationLogic(Locations.JapesBananaFairyRambiCave, lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.Slam and l.ischunky),
    ], [
        Exit(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesLankyCave: Region("Japes Lanky Cave", Levels.JungleJapes, False, [
        LocationLogic(Locations.JapesLankyFairyCave, lambda l: l.grape and l.islanky),
        LocationLogic(Locations.JapesBananaFairyLankyCave, lambda l: l.grape and l.camera and l.islanky),
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
        LocationLogic(Locations.JapesDiddyMinecarts, lambda l: l.isdiddy),
    ], [], []),

    Regions.JapesCatacomb: Region("Japes Catacomb", Levels.JungleJapes, False, [
        LocationLogic(Locations.JapesChunkyUnderground, lambda l: l.pineapple and l.ischunky),
        LocationLogic(Locations.JapesChunkyKasplat, lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", Levels.JungleJapes, True, [], [], [
        Exit(Regions.JapesBoss, lambda l: l.isdonkey and sum(l.ColoredBananas[Levels.JungleJapes]) >= 50),
    ]),

    Regions.JapesBoss: Region("Japes Boss", Levels.JungleJapes, False, [
        LocationLogic(Locations.JapesKey, lambda l: l.isdonkey),
    ], [], []),
}
