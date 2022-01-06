# fmt: off
"""Logic file for Frantic Factory."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.FranticFactoryStart: Region("Frantic Factory Start", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryDonkeyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.donkey] >= 75),
        LocationLogic(Locations.FactoryDiddyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.diddy] >= 75),
        LocationLogic(Locations.FactoryLankyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.lanky] >= 75),
        LocationLogic(Locations.FactoryTinyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.tiny] >= 75),
        LocationLogic(Locations.FactoryChunkyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.chunky] >= 75),
    ], [
        Event(Events.FactoryEntered, lambda l: True),
    ], [
        Exit(Regions.FranticFactoryLobby, lambda l: True),
        Exit(Regions.Testing, lambda l: Events.TestingGateOpened in l.Events),
        Exit(Regions.BeyondHatch, lambda l: l.Slam),
    ]),

    Regions.Testing: Region("Testing", Levels.FranticFactory, True, [
        LocationLogic(Locations.FactoryDonkeyNumberGame, lambda l: l.Slam and l.isdonkey),
        LocationLogic(Locations.FactoryDiddyBlockTower, lambda l: l.spring and l.isdiddy),
        LocationLogic(Locations.FactoryLankyBattyBarrelBandit, lambda l: l.balloon and l.islanky),
        LocationLogic(Locations.FactoryTinyDartboard, lambda l: Events.DartsPlayed in l.Events and l.istiny),
        LocationLogic(Locations.FactoryChunkyKasplat, lambda l: l.ischunky),
        LocationLogic(Locations.FactoryBananaFairybyCounting, lambda l: l.camera),
        LocationLogic(Locations.FactoryBananaFairybyFunky, lambda l: l.camera and Events.DartsPlayed in l.Events),
    ], [
        Event(Events.DartsPlayed, lambda l: l.Slam and l.mini and l.feather),
    ], [
        Exit(Regions.FranticFactoryStart, lambda l: True),
        Exit(Regions.RandD, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.Funky, lambda l: Events.DartsPlayed in l.Events),
        Exit(Regions.FactoryBossLobby, lambda l: True),
    ]),

    Regions.RandD: Region("R&D", Levels.FranticFactory, True, [
        LocationLogic(Locations.FactoryDiddyRandD, lambda l: l.guitar and l.charge and l.isdiddy),
        LocationLogic(Locations.FactoryLankyRandD, lambda l: l.trombone and l.Slam and l.islanky),
        LocationLogic(Locations.FactoryChunkyRandD, lambda l: l.triangle and l.punch and l.hunkyChunky and l.ischunky),
        LocationLogic(Locations.FactoryLankyKasplat, lambda l: l.islanky),
        LocationLogic(Locations.FactoryBattleArena, lambda l: l.grab),
    ], [], [
        Exit(Regions.Testing, lambda l: True),
        Exit(Regions.FactoryTinyRace, lambda l: l.mini and l.istiny),
        Exit(Regions.ChunkyRoomPlatform, lambda l: True),
        Exit(Regions.FactoryBossLobby, lambda l: True),
    ]),

    Regions.FactoryTinyRace: Region("Factory Tiny Race", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryTinyCarRace, lambda l: l.istiny),
    ], [], []),

    Regions.ChunkyRoomPlatform: Region("Chunky Room Platform", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryDiddyBeaverBother, lambda l: l.Slam and l.isdiddy),
    ], [], [
        Exit(Regions.PowerHut, lambda l: True),
        Exit(Regions.BeyondHatch, lambda l: True),
    ]),

    Regions.PowerHut: Region("Power Hut", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryDonkeyPowerHut, lambda l: Events.MainCoreActivated in l.Events and l.isdonkey),
    ], [
        Event(Events.MainCoreActivated, lambda l: l.coconut and l.grab and l.isdonkey),
    ], [
        Exit(Regions.ChunkyRoomPlatform, lambda l: True),
    ]),

    Regions.BeyondHatch: Region("Beyond Hatch", Levels.FranticFactory, True, [
        LocationLogic(Locations.ChunkyKong, lambda l: l.handstand and l.Slam and l.islanky),
        LocationLogic(Locations.NintendoCoin, lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab),
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab),
        LocationLogic(Locations.FactoryLankyFreeChunky, lambda l: l.handstand and l.Slam and l.islanky),
        LocationLogic(Locations.FactoryTinybyArcade, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.FactoryChunkyDarkRoom, lambda l: l.punch and l.Slam and l.ischunky),
        LocationLogic(Locations.FactoryChunkyStashSnatch, lambda l: l.punch and l.ischunky),
        LocationLogic(Locations.FactoryDiddyKasplat, lambda l: l.isdiddy),
        LocationLogic(Locations.FactoryTinyKasplat, lambda l: l.istiny),
    ], [
        Event(Events.ArcadeLeverSpawned, lambda l: l.blast and l.isdonkey),
        Event(Events.TestingGateOpened, lambda l: l.Slam),
        Event(Events.DiddyCoreSwitch, lambda l: l.Slam and l.isdiddy),
        Event(Events.LankyCoreSwitch, lambda l: l.Slam and l.islanky),
        Event(Events.TinyCoreSwitch, lambda l: l.Slam and l.istiny),
        Event(Events.ChunkyCoreSwitch, lambda l: l.Slam and l.ischunky),
    ], [
        Exit(Regions.FranticFactoryStart, lambda l: True),
        Exit(Regions.InsideCore, lambda l: Events.MainCoreActivated in l.Events),
        Exit(Regions.MainCore, lambda l: Events.MainCoreActivated in l.Events),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.FactoryBossLobby, lambda l: True),
    ]),

    Regions.InsideCore: Region("Inside Core", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryDonkeyCrusherRoom, lambda l: l.strongKong and l.isdonkey),
    ], [], [
        Exit(Regions.BeyondHatch, lambda l: True),
    ]),

    Regions.MainCore: Region("Main Core", Levels.FranticFactory, True, [
        LocationLogic(Locations.FactoryDiddyProductionRoom, lambda l: Events.DiddyCoreSwitch in l.Events and l.spring and l.isdiddy),
        LocationLogic(Locations.FactoryLankyProductionRoom, lambda l: Events.LankyCoreSwitch in l.Events and l.handstand and l.islanky),
        LocationLogic(Locations.FactoryTinyProductionRoom, lambda l: Events.TinyCoreSwitch in l.Events and l.twirl and l.istiny),
        LocationLogic(Locations.FactoryChunkyProductionRoom, lambda l: Events.ChunkyCoreSwitch in l.Events and l.ischunky),
        LocationLogic(Locations.FactoryDonkeyKasplat, lambda l: l.isdonkey)
    ], [], [
        Exit(Regions.BeyondHatch, lambda l: True),
    ]),

    Regions.FactoryBossLobby: Region("Factory Boss Lobby", Levels.FranticFactory, False, [], [], [
        Exit(Regions.FactoryBoss, lambda l: l.istiny and sum(l.ColoredBananas[Levels.FranticFactory]) >= l.settings.BossBananas[Levels.FranticFactory - 1]),
    ]),

    Regions.FactoryBoss: Region("Factory Boss", Levels.FranticFactory, False, [
        LocationLogic(Locations.FactoryKey, lambda l: l.twirl and l.istiny),
    ], [], []),
}
