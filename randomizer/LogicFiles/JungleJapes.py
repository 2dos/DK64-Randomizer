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
    Regions.JungleJapesMedals: Region("Jungle Japes Medals", "Jungle Japes Medal Rewards", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.JapesDiddyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.JapesLankyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.JapesTinyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.JapesChunkyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], []),

    Regions.JungleJapesMain: Region("Jungle Japes Main", "Japes Outdoors", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.DiddyKong, lambda l: l.CanFreeDiddy()),
        LocationLogic(Locations.JapesDonkeyFrontofCage, lambda l: l.HasKong(l.settings.diddy_freeing_kong) or l.settings.free_trade_items),
        LocationLogic(Locations.JapesDonkeyFreeDiddy, lambda l: Events.JapesFreeKongOpenGates in l.Events),
        LocationLogic(Locations.JapesDonkeyCagedBanana, lambda l: Events.JapesDonkeySwitch in l.Events and l.donkey),
        LocationLogic(Locations.JapesDiddyCagedBanana, lambda l: Events.JapesDiddySwitch1 in l.Events and l.diddy),
        LocationLogic(Locations.JapesLankyCagedBanana, lambda l: Events.JapesLankySwitch in l.Events and l.lanky),
        LocationLogic(Locations.JapesTinyCagedBanana, lambda l: Events.JapesTinySwitch in l.Events and l.tiny),
        LocationLogic(Locations.JapesChunkyBoulder, lambda l: l.chunky and l.barrels),
        LocationLogic(Locations.JapesChunkyCagedBanana, lambda l: Events.JapesChunkySwitch in l.Events and l.chunky),
        LocationLogic(Locations.JapesBattleArena, lambda l: not l.settings.crown_placement_rando),
    ], [
        Event(Events.JapesEntered, lambda l: True),
        Event(Events.JapesSpawnW5, lambda l: Events.JapesMountainTopGB in l.Events or l.settings.activate_all_bananaports),
        Event(Events.JapesFreeKongOpenGates, lambda l: l.CanOpenJapesGates()),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesLobby, lambda l: True, Transitions.JapesToIsles),
        TransitionFront(Regions.JapesBeyondPeanutGate, lambda l: l.peanut and l.diddy),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: l.settings.open_levels or Events.JapesFreeKongOpenGates in l.Events),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: l.settings.open_levels or Events.JapesFreeKongOpenGates in l.Events),
        TransitionFront(Regions.Mine, lambda l: l.peanut and l.isdiddy, Transitions.JapesMainToMine),
        TransitionFront(Regions.JapesTopOfMountain, lambda l: l.peanut and l.isdiddy),
        TransitionFront(Regions.JapesLankyCave, lambda l: l.peanut and l.diddy and ((l.handstand and l.islanky) or (l.twirl and l.istiny)), Transitions.JapesMainToLankyCave),
        TransitionFront(Regions.JapesCatacomb, lambda l: l.Slam and l.chunky and l.barrels, Transitions.JapesMainToCatacomb),
        TransitionFront(Regions.FunkyJapes, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),  # Falling from top is not super intuitive but extremely convenient for T&S door rando
        TransitionFront(Regions.JapesBaboonBlast, lambda l: l.vines and l.blast and l.isdonkey)  # , Transitions.JapesMainToBBlast)
    ]),

    Regions.JapesTopOfMountain: Region("Japes Top of Mountain", "Japes Outdoors", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMountain, lambda l: Events.JapesDiddySwitch2 in l.Events and (l.isdiddy or l.settings.free_trade_items)),
    ], [
        Event(Events.JapesMountainTopGB, lambda l: Events.JapesDiddySwitch2 in l.Events and (l.isdiddy or l.settings.free_trade_items)),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.JapesBaboonBlast: Region("Japes Baboon Blast", "Japes Outdoors", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyBaboonBlast, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True)
    ]),

    Regions.JapesBeyondPeanutGate: Region("Japes Beyond Peanut Gate", "Japes Tunnels", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyTunnel, lambda l: l.isdiddy or l.settings.free_trade_items),
        LocationLogic(Locations.JapesLankyGrapeGate, lambda l: l.grape and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesTinyFeatherGateBarrel, lambda l: l.feather and l.istiny, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", "Japes Tunnels", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKasplatLeftTunnelNear, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatLeftTunnelFar, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.settings.open_levels or (l.feather and l.tiny)),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", "Hive Area", Levels.JungleJapes, True, -1, [
        LocationLogic(Locations.JapesTinyStump, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.JapesChunkyGiantBonusBarrel, lambda l: l.hunkyChunky and l.ischunky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: True),
        TransitionFront(Regions.TinyHive, lambda l: l.mini and l.istiny, Transitions.JapesMainToTinyHive),
        TransitionFront(Regions.JapesTopOfMountain, lambda l: Events.JapesSpawnW5 in l.Events)
    ]),

    Regions.TinyHive: Region("Tiny Hive", "Hive Area", Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesTinyBeehive, lambda l: l.Slam and l.istiny and (l.saxophone or l.oranges)),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.isdiddy or l.istiny or l.islanky, Transitions.JapesTinyHiveToMain),  # It is technically possible to leave with DK and Chunky, just tricky
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", "Japes Tunnels", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesLankySlope, lambda l: l.handstand and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesKasplatNearPaintingRoom, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.Rambi, lambda l: l.coconut),
        Event(Events.JapesDonkeySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.donkey),
        Event(Events.JapesDiddySwitch1, lambda l: Events.Rambi in l.Events and l.Slam and l.diddy),
        Event(Events.JapesLankySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.lanky),
        Event(Events.JapesTinySwitch, lambda l: Events.Rambi in l.Events and l.Slam and l.tiny),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.BeyondRambiGate, lambda l: Events.Rambi in l.Events),
        TransitionFront(Regions.CrankyJapes, lambda l: True),
    ]),

    Regions.BeyondRambiGate: Region("Beyond Rambi Gate", "Japes Tunnels", Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesBananaFairyRambiCave, lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.Slam and l.ischunky and l.barrels),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    # Lanky Cave deathwarp: Requires you to be lanky and have simian slam so you can slam the pegs and summon zingers to kill you
    Regions.JapesLankyCave: Region("Japes Lanky Cave", "Japes Underground", Levels.JungleJapes, False, TransitionFront(Regions.JungleJapesMain, lambda l: l.Slam and l.islanky), [
        LocationLogic(Locations.JapesLankyFairyCave, lambda l: l.grape and l.Slam and l.islanky),
        LocationLogic(Locations.JapesBananaFairyLankyCave, lambda l: l.grape and l.camera and l.Slam and l.islanky),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesLankyCaveToMain),
    ]),

    Regions.Mine: Region("Mine", "Japes Underground", Levels.JungleJapes, False, -1, [], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Event(Events.JapesDiddySwitch2, lambda l: l.Slam and l.isdiddy),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesMineToMain),
        TransitionFront(Regions.JapesMinecarts, lambda l: l.charge and l.Slam and l.isdiddy),
    ]),

    Regions.JapesMinecarts: Region("Japes Minecarts", "Japes Underground", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMinecarts, lambda l: l.isdiddy or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
    ], Transitions.JapesMineToCarts
    ),

    # Catacomb deaths lead back to itself
    Regions.JapesCatacomb: Region("Japes Catacomb", "Japes Underground", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesChunkyUnderground, lambda l: l.vines and l.pineapple and l.ischunky),
        LocationLogic(Locations.JapesKasplatUnderground, lambda l: not l.settings.kasplat_rando and l.pineapple and l.vines),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesCatacombToMain),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", "Troff 'N' Scoff", Levels.JungleJapes, True, None, [], [], [
        TransitionFront(Regions.JapesBoss, lambda l: l.IsBossReachable(Levels.JungleJapes)),
    ]),

    Regions.JapesBoss: Region("Japes Boss", "Troff 'N' Scoff", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKey, lambda l: l.IsBossBeatable(Levels.JungleJapes)),
    ], [], []),
}
