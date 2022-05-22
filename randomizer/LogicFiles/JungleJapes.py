# fmt: off
"""Logic file for Jungle Japes."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.JungleJapesMain: Region("Jungle Japes Main", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesDonkeyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.donkey] >= 75),
        LocationLogic(Locations.JapesDiddyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.diddy] >= 75),
        LocationLogic(Locations.JapesLankyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.lanky] >= 75),
        LocationLogic(Locations.JapesTinyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.tiny] >= 75),
        LocationLogic(Locations.JapesChunkyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.chunky] >= 75),
        LocationLogic(Locations.DiddyKong, lambda l: l.CanFreeDiddy()),
        LocationLogic(Locations.JapesDonkeyFrontofCage, lambda l: l.HasKong(l.settings.diddy_freeing_kong)),
        LocationLogic(Locations.JapesDonkeyFreeDiddy, lambda l: l.CanFreeDiddy()),
        LocationLogic(Locations.JapesDonkeyCagedBanana, lambda l: Events.JapesDonkeySwitch in l.Events and l.donkey),
        LocationLogic(Locations.JapesDiddyCagedBanana, lambda l: Events.JapesDiddySwitch1 in l.Events and l.diddy),
        LocationLogic(Locations.JapesDiddyMountain, lambda l: Events.JapesDiddySwitch2 in l.Events and l.diddy),
        LocationLogic(Locations.JapesLankyCagedBanana, lambda l: Events.JapesLankySwitch in l.Events and l.lanky),
        LocationLogic(Locations.JapesTinyCagedBanana, lambda l: Events.JapesTinySwitch in l.Events and l.tiny),
        LocationLogic(Locations.JapesChunkyBoulder, lambda l: l.chunky),
        LocationLogic(Locations.JapesChunkyCagedBanana, lambda l: Events.JapesChunkySwitch and l.chunky),
        LocationLogic(Locations.JapesBattleArena, lambda l: True),
    ], [
        Event(Events.JapesEntered, lambda l: True),
        Event(Events.JapesSpawnW5, lambda l: Events.JapesDiddySwitch2 in l.Events),
        Event(Events.JapesFreeKongOpenGates, lambda l: l.CanFreeDiddy()),
    ], [
        TransitionFront(Regions.JungleJapesLobby, lambda l: True, Transitions.JapesToIsles),
        TransitionFront(Regions.JapesBeyondPeanutGate, lambda l: l.peanut and l.diddy),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: Events.JapesFreeKongOpenGates in l.Events),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: Events.JapesFreeKongOpenGates in l.Events),
        TransitionFront(Regions.Mine, lambda l: l.peanut and l.isdiddy, Transitions.JapesMainToMine),
        TransitionFront(Regions.JapesLankyCave, lambda l: l.peanut and l.diddy and l.handstand and l.islanky, Transitions.JapesMainToLankyCave),
        TransitionFront(Regions.JapesCatacomb, lambda l: l.Slam and l.chunkyAccess, Transitions.JapesMainToCatacomb),
        TransitionFront(Regions.FunkyJapes, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: l.vines and (l.donkey or l.diddy or l.chunky)),  # Lanky and Tiny have a rough time with the vines and falling from top is not intuitive
        TransitionFront(Regions.JapesBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.JapesMainToBBlast)
    ]),

    Regions.JapesBaboonBlast: Region("Japes Baboon Blast", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyBaboonBlast, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True)
    ]),

    Regions.JapesBeyondPeanutGate: Region("Japes Beyond Peanut Gate", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyTunnel, lambda l: l.isdiddy),
        LocationLogic(Locations.JapesLankyGrapeGate, lambda l: l.grape and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesTinyFeatherGateBarrel, lambda l: l.feather and l.istiny, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: True),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKasplatLeftTunnelNear, lambda l: True),
        LocationLogic(Locations.JapesKasplatLeftTunnelFar, lambda l: True),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.feather and l.tinyAccess),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", Levels.JungleJapes, True, -1, [
        LocationLogic(Locations.JapesTinyStump, lambda l: l.mini and l.tiny),
        LocationLogic(Locations.JapesChunkyGiantBonusBarrel, lambda l: l.hunkyChunky and l.ischunky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: True),
        TransitionFront(Regions.TinyHive, lambda l: l.mini and l.istiny, Transitions.JapesMainToTinyHive),
    ]),

    Regions.TinyHive: Region("Tiny Hive", Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesTinyBeehive, lambda l: l.Slam and l.istiny),
    ], [], [
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: True, Transitions.JapesTinyHiveToMain),
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesLankySlope, lambda l: l.handstand and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesKasplatNearPaintingRoom, lambda l: True),
        LocationLogic(Locations.JapesKasplatNearLab, lambda l: True),
    ], [
        Event(Events.Rambi, lambda l: l.coconut),
        Event(Events.JapesDonkeySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.donkey),
        Event(Events.JapesDiddySwitch1, lambda l: Events.Rambi in l.Events and l.Slam and l.diddy),
        Event(Events.JapesLankySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.lanky),
        Event(Events.JapesTinySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.tiny),
    ], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.BeyondRambiGate, lambda l: Events.Rambi in l.Events),
        TransitionFront(Regions.CrankyJapes, lambda l: True),
    ]),

    Regions.BeyondRambiGate: Region("Beyond Rambi Gate", Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesBananaFairyRambiCave, lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.Slam and l.ischunky),
    ], [
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: True),
    ]),

    # Lanky Cave deathwarp: Requires you to be lanky and have simian slam so you can slam the pegs and summon zingers to kill you
    Regions.JapesLankyCave: Region("Japes Lanky Cave", Levels.JungleJapes, False, TransitionFront(Regions.JungleJapesMain, lambda l: l.Slam and l.islanky), [
        LocationLogic(Locations.JapesLankyFairyCave, lambda l: l.grape and l.Slam and l.islanky),
        LocationLogic(Locations.JapesBananaFairyLankyCave, lambda l: l.grape and l.camera and l.Slam and l.islanky),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesLankyCaveToMain),
    ]),

    Regions.Mine: Region("Mine", Levels.JungleJapes, False, -1, [], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Event(Events.JapesDiddySwitch2, lambda l: l.Slam and l.isdiddy),
    ], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesMineToMain),
        TransitionFront(Regions.JapesMinecarts, lambda l: l.charge and l.Slam and l.isdiddy),
    ]),

    Regions.JapesMinecarts: Region("Japes Minecarts", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMinecarts, lambda l: l.isdiddy),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
    ], Transitions.JapesMineToCarts
    ),

    # Catacomb deaths lead back to itself
    Regions.JapesCatacomb: Region("Japes Catacomb", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesChunkyUnderground, lambda l: l.pineapple and l.ischunky),
        LocationLogic(Locations.JapesKasplatUnderground, lambda l: l.pineapple),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesCatacombToMain),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", Levels.JungleJapes, True, None, [], [], [
        TransitionFront(Regions.JapesBoss, lambda l: l.IsBossReachable(Levels.JungleJapes)),
    ]),

    Regions.JapesBoss: Region("Japes Boss", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKey, lambda l: l.IsBossBeatable(Levels.JungleJapes)),
    ], [], []),
}
