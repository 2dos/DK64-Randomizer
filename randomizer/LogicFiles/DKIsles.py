# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.Start: Region("Start", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: True),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: Events.KLumsyTalkedTo in l.Events and l.isdonkey),
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: l.feather and l.istiny),
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.istiny),
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: l.grape and l.islanky),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: l.pineapple and l.ischunky),
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.ischunky),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera and l.monkeyport and l.istiny),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunkyAccess and l.trombone and l.islanky),
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.monkeyport and l.saxophone and l.istiny),
    ], [
        Exit(Regions.Prison, lambda l: True),
        Exit(Regions.BananaFairyRoom, lambda l: l.mini and l.istiny),
        Exit(Regions.JungleJapesLobby, lambda l: Events.KLumsyTalkedTo in l.Events),
        Exit(Regions.AngryAztecLobby, lambda l: True),
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.GloomyGalleonLobby, lambda l: True),
        Exit(Regions.CabinIsle, lambda l: True),
        Exit(Regions.CrystalCavesLobby, lambda l: True),
        Exit(Regions.CreepyCastleLobby, lambda l: True),
        Exit(Regions.HideoutHelmLobby, lambda l: True and l.monkeyport and l.istiny),
        Exit(Regions.KRool, lambda l: Events.EigthKey in l.Events),
    ]),

    Regions.Prison: Region("Prison", Levels.DKIsles, False, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: l.sprint and l.islanky),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: True),
        Event(Events.FirstKey, lambda l: True),
        Event(Events.SecondKey, lambda l: True),
        Event(Events.FourthKey, lambda l: True),
        Event(Events.FifthKey, lambda l: True),
        Event(Events.SeventhKey, lambda l: True),
        Event(Events.EigthKey, lambda l: l.JapesKey and l.AztecKey and l.FactoryKey and l.GalleonKey and l.ForestKey and l.CavesKey and l.CastleKey and l.HelmKey),
    ], [
        Exit(Regions.IslesMain, lambda l: True),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", Levels.DKIsles, False, [
        LocationLogic(Locations.CameraandShockwave, lambda l: True),
        LocationLogic(Locations.RarewareBanana, lambda l: l.BananaFairies >= 20 and l.istiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
    ]),

    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunkyAccess and l.trombone and l.islanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesTinyBigBugBash, lambda l: l.charge and l.twirl and l.istiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.AngryAztecStart, lambda l: True),
    ]),

    Regions.CrocodileIsleBeyondLift: Region("Crocodile Isle Beyond Lift", Levels.DKIsles, False, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.IslesSnideRoom, lambda l: True),
        Exit(Regions.FranticFactoryLobby, lambda l: True),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: l.spring and l.isdiddy),
        LocationLogic(Locations.IslesBattleArena1, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: l.grab and l.bongos and l.isdonkey),
        LocationLogic(Locations.IslesTinyKasplat, lambda l: l.punch and l.istiny),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.FranticFactoryStart, lambda l: True),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: l.chunkyAccess and l.superSlam and l.mini and l.istiny),
        LocationLogic(Locations.IslesChunkyKasplat, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.GloomyGalleonStart, lambda l: True),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", Levels.DKIsles, False, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        LocationLogic(Locations.IslesDiddySummit, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy),
    ], [], [
        Exit(Regions.FungiForestLobby, lambda l: True),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple and l.gorillaGone),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.feather),
    ], [], [
        Exit(Regions.CabinIsle, lambda l: True),
        Exit(Regions.FungiForestStart, lambda l: True),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: l.punch and l.strongKong and l.isdonkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.isdiddy),
        LocationLogic(Locations.IslesLankyKasplat, lambda l: l.punch and l.islanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: l.punch and l.balloon and l.islanky),
        LocationLogic(Locations.IslesDiddyKasplat, lambda l: l.coconut and l.diddy),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: l.gorillaGone),
        LocationLogic(Locations.IslesDonkeyKasplat, lambda l: l.coconut),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.HideoutHelmStart, lambda l: l.gorillaGone and l.GoldenBananas >= 100),
    ]),

    Regions.KRool: Region("K. Rool", Levels.DKIsles, True, [
        LocationLogic(Locations.BananaHoard, lambda l: l.donkeyAccess and l.jetpack and l.peanut and l.diddyAccess and l.trombone and l.lankyAccess
                 and l.mini and l.feather and l.tinyAccess and l.superSlam and l.gorillaGone and l.hunkyChunky and l.chunkyAccess),
    ], [], []),
}
