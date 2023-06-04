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
    ], [], [], restart=-1),

    Regions.JungleJapesStart: Region("Jungle Japes Start", "Japes Lowlands", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesDonkeyCagedBanana, lambda l: ((Events.JapesDonkeySwitch in l.Events or l.CanPhaseswim() or l.CanSkew(False)) and l.donkey) or ((l.CanPhaseswim() or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesChunkyBoulder, lambda l: l.chunky and l.barrels),
    ], [
        Event(Events.JapesEntered, lambda l: True),
        Event(Events.JapesW1aTagged, lambda l: True),
        Event(Events.JapesW1bTagged, lambda l: True),
        Event(Events.JapesW2aTagged, lambda l: True),
        Event(Events.JapesW3bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesLobby, lambda l: True, Transitions.JapesToIsles),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.JapesBeyondPeanutGate, lambda l: (l.peanut and l.diddy) or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: l.settings.open_levels or Events.JapesFreeKongOpenGates in l.Events or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: l.settings.open_levels or Events.JapesFreeKongOpenGates in l.Events or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesCatacomb, lambda l: (l.Slam and l.chunky and l.barrels) or l.CanPhaseswim() or l.CanSkew(False), Transitions.JapesMainToCatacomb),
        TransitionFront(Regions.JapesBaboonBlast, lambda l: (l.vines or l.CanMoonkick()) and l.blast and l.isdonkey),  # , Transitions.JapesMainToBBlast)
    ]),

    Regions.JungleJapesMain: Region("Jungle Japes Main", "Japes Hillside", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.DiddyKong, lambda l: l.CanFreeDiddy()),
        LocationLogic(Locations.JapesDonkeyFrontofCage, lambda l: l.HasKong(l.settings.diddy_freeing_kong) or l.settings.free_trade_items),
        LocationLogic(Locations.JapesDonkeyFreeDiddy, lambda l: Events.JapesFreeKongOpenGates in l.Events),
        LocationLogic(Locations.JapesDiddyCagedBanana, lambda l: ((Events.JapesDiddySwitch1 in l.Events or l.phasewalk or l.generalclips or l.CanSkew(False)) and l.diddy) or ((l.phasewalk or l.generalclips or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesLankyCagedBanana, lambda l: ((Events.JapesLankySwitch in l.Events or l.CanSkew(False)) and l.lanky) or (l.CanSkew(False) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesTinyCagedBanana, lambda l: ((Events.JapesTinySwitch in l.Events or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False)) and l.tiny) or ((l.phasewalk or l.CanPhaseswim() or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesChunkyCagedBanana, lambda l: ((Events.JapesChunkySwitch in l.Events or l.phasewalk or l.CanSkew(False)) and l.chunky) or ((l.phasewalk or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesBattleArena, lambda l: not l.settings.crown_placement_rando),
        LocationLogic(Locations.RainbowCoin_Location00, lambda l: l.shockwave and ((l.handstand and l.islanky) or (l.twirl and l.istiny) or l.CanMoonkick() or ((l.phasewalk or l.generalclips) and (l.istiny or l.isdiddy))))
    ], [
        Event(Events.JapesFreeKongOpenGates, lambda l: l.CanOpenJapesGates()),
        Event(Events.JapesW2bTagged, lambda l: True),
        Event(Events.JapesW3aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: l.settings.open_levels or Events.JapesFreeKongOpenGates in l.Events or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.Mine, lambda l: l.peanut and l.isdiddy, Transitions.JapesMainToMine),
        TransitionFront(Regions.JapesTopOfMountain, lambda l: (l.peanut and l.isdiddy) or l.CanMoonkick()),
        TransitionFront(Regions.JapesLankyCave, lambda l: (((l.peanut and l.diddy) or l.CanSkew(False)) and ((l.handstand and l.islanky) or (l.twirl and l.istiny) or l.CanMoonkick())) or (l.CanMoonkick() and (l.phasewalk or l.CanSkew(False))) or ((l.phasewalk or l.generalclips or l.CanSkew(False)) and (l.isdiddy or l.istiny)), Transitions.JapesMainToLankyCave),
        TransitionFront(Regions.FunkyJapes, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),  # Falling from top is not super intuitive but extremely convenient for T&S door rando
        TransitionFront(Regions.BeyondRambiGate, lambda l: l.CanPhaseswim() or l.CanSkew(False) or l.phasewalk or l.generalclips),
    ]),

    Regions.JapesTopOfMountain: Region("Japes Top of Mountain", "Japes Hillside", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMountain, lambda l: Events.JapesDiddySwitch2 in l.Events and (l.isdiddy or l.settings.free_trade_items)),
    ], [
        Event(Events.JapesW5bTagged, lambda l: Locations.JapesDiddyMountain in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.JapesBaboonBlast: Region("Japes Baboon Blast", "Japes Lowlands", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyBaboonBlast, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True)
    ]),

    Regions.JapesBeyondPeanutGate: Region("Japes Beyond Peanut Gate", "Japes Lowlands", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyTunnel, lambda l: l.isdiddy or l.settings.free_trade_items),
        LocationLogic(Locations.JapesLankyGrapeGate, lambda l: (l.grape and l.islanky) or ((l.phasewalk or l.generalclips or l.CanSkew(False)) and (l.islanky or l.settings.free_trade_items)), MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesTinyFeatherGateBarrel, lambda l: (l.feather and l.istiny) or ((l.phasewalk or l.CanSkew(False)) and (l.istiny or l.settings.free_trade_items)), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", "Hive Tunnel Area", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKasplatLeftTunnelNear, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatLeftTunnelFar, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.settings.open_levels or (l.feather and l.tiny) or l.phasewalk or l.CanSkew(False)),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", "Hive Tunnel Area", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesTinyStump, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSkew(False)),
        LocationLogic(Locations.JapesChunkyGiantBonusBarrel, lambda l: l.hunkyChunky and l.ischunky, MinigameType.BonusBarrel),
    ], [
        Event(Events.JapesW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: True),
        TransitionFront(Regions.TinyHive, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSkew(False) or (l.hunkyChunky and l.ischunky and l.generalclips), Transitions.JapesMainToTinyHive),
        TransitionFront(Regions.BeyondRambiGate, lambda l: l.hunkyChunky and l.ischunky and l.generalclips),
    ]),

    Regions.TinyHive: Region("Tiny Hive", "Hive Tunnel Area", Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesTinyBeehive, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.phasewalk or l.generalclips)) or (l.settings.free_trade_items and l.phasewalk)),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.isdiddy or l.istiny or l.islanky or l.phasewalk, Transitions.JapesTinyHiveToMain),  # It is technically possible to leave with DK and Chunky, just tricky
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", "Japes Stormy Tunnel Area", Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesLankySlope, lambda l: l.handstand and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesKasplatNearPaintingRoom, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.Rambi, lambda l: (l.coconut and l.isdonkey) or l.phasewalk),
        Event(Events.JapesDonkeySwitch, lambda l: (Events.Rambi in l.Events or l.phasewalk) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.donkey),
        Event(Events.JapesDiddySwitch1, lambda l: (Events.Rambi in l.Events or l.phasewalk) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.diddy),
        Event(Events.JapesLankySwitch, lambda l: (Events.Rambi in l.Events or l.phasewalk) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.lanky),
        Event(Events.JapesTinySwitch, lambda l: (Events.Rambi in l.Events or l.phasewalk) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.tiny),
        Event(Events.JapesW4aTagged, lambda l: True),
        Event(Events.JapesW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
        TransitionFront(Regions.BeyondRambiGate, lambda l: Events.Rambi in l.Events or l.phasewalk or l.CanSkew(False)),
        TransitionFront(Regions.CrankyJapes, lambda l: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.CanMoonkick()),
    ]),

    Regions.BeyondRambiGate: Region("Beyond Rambi Gate", "Japes Stormy Tunnel Area", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesBananaFairyRambiCave, lambda l: l.camera),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) and l.ischunky and l.barrels),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    # Lanky Cave deathwarp: Requires you to be lanky and have simian slam so you can slam the pegs and summon zingers to kill you
    Regions.JapesLankyCave: Region("Japes Lanky Cave", "Japes Caves and Mines", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesLankyFairyCave, lambda l: (((l.grape or l.trombone) and l.Slam) or l.generalclips) and l.islanky),
        LocationLogic(Locations.JapesBananaFairyLankyCave, lambda l: (((l.grape or l.trombone) and l.Slam) or l.generalclips) and l.islanky and l.camera),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesLankyCaveToMain),
    ]),

    Regions.Mine: Region("Mine", "Japes Caves and Mines", Levels.JungleJapes, False, -1, [], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Event(Events.JapesDiddySwitch2, lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy),
    ], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMain, lambda l: True, Transitions.JapesMineToMain),
        TransitionFront(Regions.JapesMinecarts, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) or l.phasewalk) and ((l.charge and l.isdiddy) or l.phasewalk or (l.advanced_platforming and l.isdiddy))),
    ]),

    Regions.JapesMinecarts: Region("Japes Minecarts", "Japes Caves and Mines", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMinecarts, lambda l: l.isdiddy or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda l: True),
    ], Transitions.JapesMineToCarts
    ),

    # Catacomb deaths lead back to itself
    Regions.JapesCatacomb: Region("Japes Catacomb", "Japes Caves and Mines", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesChunkyUnderground, lambda l: (l.vines and l.pineapple and l.ischunky) or (((l.twirl and l.istiny) or (l.vines and (l.isdiddy or l.istiny)) or (l.isdonkey and l.settings.krusha_kong != Kongs.donkey)) and l.advanced_platforming and l.settings.free_trade_items) or l.phasewalk),
        LocationLogic(Locations.JapesKasplatUnderground, lambda l: not l.settings.kasplat_rando and ((l.vines and l.pineapple and l.ischunky) or (l.vines and (l.isdiddy or l.istiny) and l.advanced_platforming and l.settings.free_trade_items) or l.phasewalk)),
    ], [], [
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesStart, lambda l: True, Transitions.JapesCatacombToMain),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", "Troff 'N' Scoff", Levels.JungleJapes, True, None, [], [], [
        TransitionFront(Regions.JapesBoss, lambda l: l.IsBossReachable(Levels.JungleJapes)),
    ]),

    Regions.JapesBoss: Region("Japes Boss", "Troff 'N' Scoff", Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKey, lambda l: l.IsBossBeatable(Levels.JungleJapes)),
    ], [], []),
}
