# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, TransitionFront, LocationLogic, Region

LogicRegions = {
    Regions.Treehouse: Region("Treehouse", Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.StartArea, lambda l: True)
    ]),

    Regions.StartArea: Region("Start Area", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.Treehouse, lambda l: True),
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: l.donkey),
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
        TransitionFront(Regions.StartArea, lambda l: True),
        TransitionFront(Regions.Prison, lambda l: True),
        TransitionFront(Regions.BananaFairyRoom, lambda l: l.mini and l.istiny, Transitions.IslesMainToFairy),
        TransitionFront(Regions.JungleJapesLobby, lambda l: True, Transitions.IslesMainToJapesLobby),
        TransitionFront(Regions.AngryAztecLobby, lambda l: True, Transitions.IslesMainToAztecLobby),
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: True),
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True, Transitions.IslesMainToGalleonLobby),
        TransitionFront(Regions.CabinIsle, lambda l: True),
        TransitionFront(Regions.CrystalCavesLobby, lambda l: True, Transitions.IslesMainToCavesLobby),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: True, Transitions.IslesMainToCastleLobby),
        TransitionFront(Regions.HideoutHelmLobby, lambda l: True and l.monkeyport and l.istiny),
        TransitionFront(Regions.KRool, lambda l: Events.KeysTurnIn in l.Events),
    ]),

    Regions.Prison: Region("Prison", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: l.sprint and l.islanky),
    ], [
        Event(Events.KeysTurnIn, lambda l: l.JapesKey and l.AztecKey and l.FactoryKey and l.GalleonKey and l.ForestKey and l.CavesKey and l.CastleKey and l.HelmKey),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", Levels.DKIsles, False, None, [
        LocationLogic(Locations.CameraAndShockwave, lambda l: True),
        LocationLogic(Locations.RarewareBanana, lambda l: l.BananaFairies >= 20 and l.istiny),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesFairyToMain),
    ]),

    # All lobies take you to themselves when you die
    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesJapesLobbyToMain),
        TransitionFront(Regions.JungleJapesMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.JungleJapes - 1], Transitions.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyAztecLobby, lambda l: l.charge and l.diddy and l.twirl and l.istiny, True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesAztecLobbyToMain),
        TransitionFront(Regions.AngryAztecStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.AngryAztec - 1], Transitions.IslesToAztec),
    ]),

    Regions.CrocodileIsleBeyondLift: Region("Crocodile Isle Beyond Lift", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesSnideRoom, lambda l: True, Transitions.IslesMainToSnideRoom),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: True, Transitions.IslesMainToFactoryLobby),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: l.spring and l.isdiddy, True),
        LocationLogic(Locations.IslesBattleArena1, lambda l: l.ischunky),
    ], [], [
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: True, Transitions.IslesSnideRoomToMain),
        TransitionFront(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: l.grab and l.bongos and l.donkey),
        LocationLogic(Locations.IslesTinyKasplat, lambda l: l.punch and l.chunky and l.tiny),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
    ], [], [
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: True, Transitions.IslesFactoryLobbyToMain),
        TransitionFront(Regions.FranticFactoryStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.FranticFactory - 1], Transitions.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: l.chunky and l.superSlam and l.mini and l.tiny),
        LocationLogic(Locations.IslesChunkyKasplat, lambda l: l.chunky),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesGalleonLobbyToMain),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.GloomyGalleon - 1], Transitions.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        LocationLogic(Locations.IslesDiddySummit, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy, True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.IslesMainToForestLobby),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: (l.coconut and l.donkey) and (l.peanut and l.diddy)
                      and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.feather and l.tiny),
    ], [], [
        TransitionFront(Regions.CabinIsle, lambda l: True, Transitions.IslesForestLobbyToMain),
        TransitionFront(Regions.FungiForestStart, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.FungiForest - 1], Transitions.IslesToForest),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: l.punch and l.chunky and l.strongKong and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesLankyKasplat, lambda l: l.punch and l.chunky and l.lanky),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesCavesLobbyToMain),
        TransitionFront(Regions.CrystalCavesMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.CrystalCaves - 1], Transitions.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: l.punch and l.chunky and l.balloon and l.islanky, True),
        LocationLogic(Locations.IslesDiddyKasplat, lambda l: l.coconut and l.donkey and l.diddy),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesCastleLobbyToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.GoldenBananas >= l.settings.EntryGBs[Levels.CreepyCastle - 1], Transitions.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: l.gorillaGone and l.ischunky, True),
        LocationLogic(Locations.IslesDonkeyKasplat, lambda l: l.scope and l.coconut and l.donkey),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.HideoutHelmStart, lambda l: l.gorillaGone and l.chunky and l.GoldenBananas >= l.settings.EntryGBs[Levels.HideoutHelm - 1]),
    ]),

    Regions.KRool: Region("K. Rool", Levels.DKIsles, True, None, [
        LocationLogic(Locations.BananaHoard, lambda l: Events.KRoolDonkey in l.Events and Events.KRoolDiddy in l.Events
                      and Events.KRoolLanky in l.Events and Events.KRoolTiny in l.Events and Events.KRoolChunky in l.Events),
    ], [
        Event(Events.KRoolDonkey, lambda l: not l.settings.krool_donkey or l.donkey),
        Event(Events.KRoolDiddy, lambda l: not l.settings.krool_diddy or (l.jetpack and l.peanut and l.diddy)),
        Event(Events.KRoolLanky, lambda l: not l.settings.krool_lanky or (l.trombone and l.lanky)),
        Event(Events.KRoolTiny, lambda l: not l.settings.krool_tiny or (l.mini and l.feather and l.tiny)),
        Event(Events.KRoolChunky, lambda l: not l.settings.krool_chunky or (l.superSlam and l.gorillaGone and l.hunkyChunky and l.chunky))
    ], []),
}
