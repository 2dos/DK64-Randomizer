# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Exits import Exits
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.Start: Region("Start", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: True),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesStartToMain),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: Events.KLumsyTalkedTo in l.Events and l.donkey),
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: l.feather and l.tiny),
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.tiny),
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: l.grape and l.lanky),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: l.pineapple and l.chunky),
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.chunky),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera and l.monkeyport and l.tiny),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunky and l.trombone and l.lanky),
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.monkeyport and l.saxophone and l.tiny),
    ], [
        Exit(Regions.Start, lambda l: True, Exits.IslesStartToMain),
        Exit(Regions.Prison, lambda l: True, Exits.IslesMainToPrison),
        Exit(Regions.BananaFairyRoom, lambda l: l.mini and l.istiny, Exits.IslesMainToFairy),
        Exit(Regions.JungleJapesLobby, lambda l: Events.KLumsyTalkedTo in l.Events, Exits.IslesMainToJapesLobby),
        Exit(Regions.AngryAztecLobby, lambda l: True, Exits.IslesMainToAztecLobby),
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.GloomyGalleonLobby, lambda l: True, Exits.IslesMainToGalleonLobby),
        Exit(Regions.CabinIsle, lambda l: True),
        Exit(Regions.CrystalCavesLobby, lambda l: True, Exits.IslesMainToCavesLobby),
        Exit(Regions.CreepyCastleLobby, lambda l: True, Exits.IslesMainToCastleLobby),
        Exit(Regions.HideoutHelmLobby, lambda l: True and l.monkeyport and l.istiny, Exits.IslesMainToHelmLobby),
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
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesPrisonToMain),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", Levels.DKIsles, False, [
        LocationLogic(Locations.CameraAndShockwave, lambda l: True),
        LocationLogic(Locations.RarewareBanana, lambda l: l.BananaFairies >= 20 and l.istiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesFairyToMain),
    ]),

    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesJapesLobbyToMain),
        Exit(Regions.JungleJapesMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.JungleJapes - 1], Exits.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesTinyBigBugBash, lambda l: l.charge and l.diddy and l.twirl and l.tiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesAztecLobbyToMain),
        Exit(Regions.AngryAztecStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.AngryAztec - 1], Exits.IslesToAztec),
    ]),

    Regions.CrocodileIsleBeyondLift: Region("Crocodile Isle Beyond Lift", Levels.DKIsles, False, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.IslesSnideRoom, lambda l: True, Exits.IslesMainToSnideRoom),
        Exit(Regions.FranticFactoryLobby, lambda l: True, Exits.IslesMainToFactoryLobby),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: l.spring and l.isdiddy),
        LocationLogic(Locations.IslesBattleArena1, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True, Exits.IslesSnideRoomToMain),
        Exit(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: l.grab and l.bongos and l.donkey),
        LocationLogic(Locations.IslesTinyKasplat, lambda l: l.punch and l.chunky and l.tiny),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True, Exits.IslesFactoryLobbyToMain),
        Exit(Regions.FranticFactoryStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.FranticFactory - 1], Exits.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: l.chunky and l.superSlam and l.mini and l.tiny),
        LocationLogic(Locations.IslesChunkyKasplat, lambda l: l.chunky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesGalleonLobbyToMain),
        Exit(Regions.GloomyGalleonStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.GloomyGalleon - 1], Exits.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", Levels.DKIsles, False, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        LocationLogic(Locations.IslesDiddySummit, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy),
    ], [], [
        Exit(Regions.FungiForestLobby, lambda l: True, Exits.IslesMainToForestLobby),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: (l.coconut and l.donkey) and (l.peanut and l.diddy) 
            and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.feather and l.tiny),
    ], [], [
        Exit(Regions.CabinIsle, lambda l: True, Exits.IslesFactoryLobbyToMain),
        Exit(Regions.FungiForestStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.FungiForest - 1], Exits.IslesToFactory),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: l.punch and l.chunky and l.strongKong and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesLankyKasplat, lambda l: l.punch and l.chunky and l.lanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesCavesLobbyToMain),
        Exit(Regions.CrystalCavesMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.CrystalCaves - 1], Exits.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: l.punch and l.chunky and l.balloon and l.lanky),
        LocationLogic(Locations.IslesDiddyKasplat, lambda l: l.coconut and l.donkey and l.diddy),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesCastleLobbyToMain),
        Exit(Regions.CreepyCastleMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.CreepyCastle - 1], Exits.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", Levels.DKIsles, True, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: l.gorillaGone and l.chunky),
        LocationLogic(Locations.IslesDonkeyKasplat, lambda l: l.coconut and l.donkey),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True, Exits.IslesHelmLobbyToMain),
        Exit(Regions.HideoutHelmStart, lambda l: l.gorillaGone and l.chunky and l.GoldenBananas >= l.settings.EntryGBs[Levels.HideoutHelm - 1], Exits.IslesToHelm),
    ]),

    Regions.KRool: Region("K. Rool", Levels.DKIsles, True, [
        LocationLogic(Locations.BananaHoard, lambda l: l.donkey and l.jetpack and l.peanut and l.diddy and l.trombone and l.lanky
                      and l.mini and l.feather and l.tiny and l.superSlam and l.gorillaGone and l.hunkyChunky and l.chunky),
    ], [], []),
}
