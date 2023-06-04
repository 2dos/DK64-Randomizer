# fmt: off
"""Logic file for Frantic Factory."""

from re import L

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import MinigameBarrels, ShuffleLoadingZones
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.FranticFactoryMedals: Region("Frantic Factory Medals", "Frantic Factory Medal Rewards", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.FactoryDiddyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.FactoryLankyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.FactoryTinyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.FactoryChunkyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], [], restart=-1),

    Regions.FranticFactoryStart: Region("Frantic Factory Start", "Frantic Factory Start", Levels.FranticFactory, False, None, [], [
        Event(Events.FactoryEntered, lambda l: True),
        Event(Events.HatchOpened, lambda l: l.Slam),
        Event(Events.FactoryW1aTagged, lambda l: True),
        Event(Events.FactoryW2aTagged, lambda l: True),
        Event(Events.FactoryW3aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: True, Transitions.FactoryToIsles),
        TransitionFront(Regions.Testing, lambda l: l.settings.open_levels or Events.TestingGateOpened in l.Events or l.phasewalk or l.generalclips),
        # Hatch opened already in rando if loading zones randomized
        TransitionFront(Regions.BeyondHatch, lambda l: l.settings.shuffle_loading_zones == ShuffleLoadingZones.all or Events.HatchOpened in l.Events or l.phasewalk),
    ]),

    Regions.Testing: Region("Testing", "Testing Area", Levels.FranticFactory, True, -1, [
        LocationLogic(Locations.FactoryDonkeyNumberGame, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.isdonkey),
        LocationLogic(Locations.FactoryDiddyBlockTower, lambda l: l.spring and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryLankyTestingRoomBarrel, lambda l: (l.balloon or l.advanced_platforming) and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryTinyDartboard, lambda l: Events.DartsPlayed in l.Events and l.tiny),
        LocationLogic(Locations.FactoryKasplatBlocks, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.FactoryBananaFairybyCounting, lambda l: l.camera),
        LocationLogic(Locations.FactoryBananaFairybyFunky, lambda l: l.camera and Events.DartsPlayed in l.Events),
    ], [
        Event(Events.DartsPlayed, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and (l.mini or l.phasewalk) and l.feather and l.istiny),
        Event(Events.FactoryW3bTagged, lambda l: True),
        Event(Events.FactoryW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.FranticFactoryStart, lambda l: Events.TestingGateOpened in l.Events or l.phasewalk),
        TransitionFront(Regions.RandD, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.FunkyFactory, lambda l: True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.RandD: Region("R&D", "Research and Development Area", Levels.FranticFactory, True, None, [
        LocationLogic(Locations.FactoryDiddyRandD, lambda l: (l.guitar or l.CanAccessRNDRoom()) and l.charge and l.isdiddy),
        LocationLogic(Locations.FactoryLankyRandD, lambda l: (((l.trombone or l.CanAccessRNDRoom()) and l.CanSlamSwitch(Levels.FranticFactory, 1)) or (l.handstand and l.tbs and l.spawn_snags)) and l.islanky),
        LocationLogic(Locations.FactoryChunkyRandD, lambda l: (l.triangle or l.CanAccessRNDRoom()) and l.punch and l.hunkyChunky and l.ischunky),
        LocationLogic(Locations.FactoryKasplatRandD, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.FactoryBattleArena, lambda l: not l.settings.crown_placement_rando and ((l.grab and l.donkey) or l.CanAccessRNDRoom())),
    ], [
        Event(Events.FactoryW2bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.Testing, lambda l: True),
        TransitionFront(Regions.FactoryTinyRaceLobby, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanOStandTBSNoclip()),
        TransitionFront(Regions.FactoryTinyRace, lambda l: l.phasewalk or l.CanOStandTBSNoclip(), Transitions.FactoryRandDToRace, isGlitchTransition=True),
        TransitionFront(Regions.ChunkyRoomPlatform, lambda l: True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.FactoryTinyRaceLobby: Region("Factory Tiny Race Lobby", "Research and Development Area", Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.RandD, lambda l: (l.mini and l.istiny) or l.phasewalk),
        TransitionFront(Regions.FactoryTinyRace, lambda l: (l.mini and l.istiny) or l.phasewalk, Transitions.FactoryRandDToRace)
    ]),

    Regions.FactoryTinyRace: Region("Factory Tiny Race", "Research and Development Area", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryTinyCarRace, lambda l: l.istiny or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.FactoryTinyRaceLobby, lambda l: True, Transitions.FactoryRaceToRandD),
    ], Transitions.FactoryRandDToRace
    ),

    Regions.ChunkyRoomPlatform: Region("Chunky Room Platform", "Storage and Arcade Area", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDiddyChunkyRoomBarrel, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.isdiddy and (l.vines or l.settings.bonus_barrels == MinigameBarrels.skip), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.PowerHut, lambda l: (l.coconut and l.isdonkey) or l.phasewalk or l.CanMoonkick(), Transitions.FactoryChunkyRoomToPower),
        TransitionFront(Regions.BeyondHatch, lambda l: True),
    ]),

    Regions.PowerHut: Region("Power Hut", "Storage and Arcade Area", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyPowerHut, lambda l: Events.MainCoreActivated in l.Events and (l.isdonkey or l.settings.free_trade_items)),
    ], [
        Event(Events.MainCoreActivated, lambda l: l.grab and l.isdonkey),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.ChunkyRoomPlatform, lambda l: True, Transitions.FactoryPowerToChunkyRoom),
    ]),

    Regions.BeyondHatch: Region("Beyond Hatch", "Storage and Arcade Area", Levels.FranticFactory, True, -1, [
        LocationLogic(Locations.ChunkyKong, lambda l: l.CanFreeChunky()),
        LocationLogic(Locations.NintendoCoin, lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab and l.isdonkey and (l.GetCoins(Kongs.donkey) >= 2)),
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: (not l.settings.fast_gbs and (Events.ArcadeLeverSpawned in l.Events and l.grab and l.isdonkey)) or (l.CanOStandTBSNoclip() and l.spawn_snags)),
        LocationLogic(Locations.FactoryLankyFreeChunky, lambda l: l.CanFreeChunky()),
        LocationLogic(Locations.FactoryTinybyArcade, lambda l: (l.mini and l.tiny) or l.phasewalk),
        LocationLogic(Locations.FactoryChunkyDarkRoom, lambda l: ((l.punch and l.chunky) or l.phasewalk) and ((l.punch and l.CanSlamSwitch(Levels.FranticFactory, 1)) or l.generalclips) and l.ischunky),
        LocationLogic(Locations.RainbowCoin_Location02, lambda l: ((l.punch and l.chunky) or l.phasewalk) and l.shockwave),
        LocationLogic(Locations.FactoryChunkybyArcade, lambda l: ((l.punch or l.phasewalk) and l.ischunky) or (l.phasewalk and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryKasplatStorage, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.TestingGateOpened, lambda l: l.Slam),
        Event(Events.FactoryW1bTagged, lambda l: True),
        Event(Events.FactoryW4aTagged, lambda l: True),
        Event(Events.FactoryW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.FranticFactoryStart, lambda l: l.settings.shuffle_loading_zones == ShuffleLoadingZones.all or Events.HatchOpened in l.Events),
        TransitionFront(Regions.LowerCore, lambda l: True),
        TransitionFront(Regions.CrankyFactory, lambda l: True),
        TransitionFront(Regions.CandyFactory, lambda l: True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
        TransitionFront(Regions.FactoryBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.FactoryMainToBBlast)
    ]),

    Regions.FactoryBaboonBlast: Region("Factory Baboon Blast", "Storage and Arcade Area", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: l.settings.fast_gbs and l.isdonkey),  # The GB is moved here on fast GBs
    ], [
        Event(Events.ArcadeLeverSpawned, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.BeyondHatch, lambda l: True)
    ]),

    Regions.LowerCore: Region("Lower Core", "Production Room", Levels.FranticFactory, False, -1, [
        LocationLogic(Locations.FactoryKasplatProductionBottom, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.MainCoreActivated, lambda l: l.settings.high_req),
        Event(Events.DiddyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.diddy),
        Event(Events.LankyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.lanky),
        Event(Events.TinyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.tiny),
        Event(Events.ChunkyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.chunky),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.BeyondHatch, lambda l: True),
        TransitionFront(Regions.InsideCore, lambda l: Events.MainCoreActivated in l.Events or l.phasewalk, Transitions.FactoryBeyondHatchToInsideCore),
        TransitionFront(Regions.MiddleCore, lambda l: Events.MainCoreActivated in l.Events),
    ]),

    Regions.InsideCore: Region("Inside Core", "Production Room", Levels.FranticFactory, False, -1, [
        LocationLogic(Locations.FactoryDonkeyCrusherRoom, lambda l: (l.strongKong and l.isdonkey) or l.generalclips or l.phasewalk),
    ], [], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.LowerCore, lambda l: True, Transitions.FactoryInsideCoreToBeyondHatch),
    ]),

    Regions.MiddleCore: Region("Middle Core", "Production Room", Levels.FranticFactory, True, None, [
        LocationLogic(Locations.FactoryChunkyProductionRoom, lambda l: Events.ChunkyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.chunky),
    ], [
        Event(Events.FactoryW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.LowerCore, lambda l: True),
        TransitionFront(Regions.UpperCore, lambda l: Events.MainCoreActivated in l.Events),
        TransitionFront(Regions.InsideCore, lambda l: l.ledgeclip, Transitions.FactoryBeyondHatchToInsideCore, isGlitchTransition=True),
    ]),

    Regions.UpperCore: Region("Upper Core", "Production Room", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDiddyProductionRoom, lambda l: Events.DiddyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.spring and l.diddy),
        LocationLogic(Locations.FactoryLankyProductionRoom, lambda l: Events.LankyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.handstand and l.lanky),
        LocationLogic(Locations.FactoryTinyProductionRoom, lambda l: Events.TinyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.twirl and l.istiny, MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryKasplatProductionTop, lambda l: not l.settings.kasplat_rando)
    ], [], [
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.LowerCore, lambda l: True),
        TransitionFront(Regions.MiddleCore, lambda l: True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.FactoryBossLobby: Region("Factory Boss Lobby", "Troff 'N' Scoff", Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.FactoryBoss, lambda l: l.IsBossReachable(Levels.FranticFactory)),
    ]),

    Regions.FactoryBoss: Region("Factory Boss", "Troff 'N' Scoff", Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryKey, lambda l: l.IsBossBeatable(Levels.FranticFactory)),
    ], [], []),
}
