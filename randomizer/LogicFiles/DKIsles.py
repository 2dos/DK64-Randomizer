# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.GameStart: Region("Game Start", "Training Grounds", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
    ], [], [
        TransitionFront(Regions.Credits, lambda l: True),
        # Replace these with the actual starting region if we choose to randomize it
        TransitionFront(Regions.IslesMain, lambda l: l.settings.fast_start_beginning_of_game),
        TransitionFront(Regions.Treehouse, lambda l: not l.settings.fast_start_beginning_of_game)
    ]),

    Regions.Credits: Region("Credits", "Credits", Levels.DKIsles, False, None, [
        LocationLogic(Locations.BananaHoard, lambda l: l.WinConditionMet())
    ], [], []),

    Regions.Treehouse: Region("Treehouse", "Training Grounds", Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.TrainingGrounds, lambda l: True, Transitions.IslesTreehouseToStart)
    ]),

    Regions.TrainingGrounds: Region("Training Grounds", "Training Grounds", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesStartToMain),
        TransitionFront(Regions.Treehouse, lambda l: True, Transitions.IslesStartToTreehouse),
        TransitionFront(Regions.CrankyIsles, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", "DK Isle", Levels.DKIsles, True, None, [
        # Don't check for donkey for rock- If lobbies are closed and first B.Locker is not 0, this banana must be grabbable by
        # the starting kong, so for logic we assume any kong can grab it since that's practically true.
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: (l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events)),
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: l.feather and l.tiny),
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.tiny),
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: l.grape and l.lanky),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: l.pineapple and l.chunky),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera and l.monkeyport and l.tiny),
    ], [
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.monkeyport and l.saxophone and l.tiny),
    ], [
        TransitionFront(Regions.TrainingGrounds, lambda l: True, Transitions.IslesMainToStart),
        TransitionFront(Regions.Prison, lambda l: True),
        TransitionFront(Regions.BananaFairyRoom, lambda l: l.mini and l.istiny, Transitions.IslesMainToFairy),
        TransitionFront(Regions.JungleJapesLobby, lambda l: l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events, Transitions.IslesMainToJapesLobby),
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.vines or l.pathMode),
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events) and (l.swim or l.pathMode), Transitions.IslesMainToGalleonLobby),
        TransitionFront(Regions.CabinIsle, lambda l: l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events, Transitions.IslesMainToCastleLobby),
        TransitionFront(Regions.HideoutHelmLobby, lambda l: l.monkeyport and l.istiny
                        and (l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events))),
        # If you have monkeyport, you can warp up to the hideout helm entrance and drop down to the upper part of Crocodile Isle
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: l.monkeyport and l.istiny),
        TransitionFront(Regions.KRool, lambda l: l.CanAccessKRool()),
    ]),

    Regions.IslesMainUpper: Region("Isles Main Upper", "DK Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.chunky and l.barrels),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
    ], [
        TransitionFront(Regions.AngryAztecLobby, lambda l: l.settings.open_lobbies or Events.JapesKeyTurnedIn in l.Events, Transitions.IslesMainToAztecLobby),
        TransitionFront(Regions.CrystalCavesLobby, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events) and (l.isdonkey or l.ischunky or (l.istiny and l.twirl)), Transitions.IslesMainToCavesLobby),
    ]),

    Regions.Prison: Region("Prison", "Krem Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: l.sprint and l.islanky),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: True),
        Event(Events.JapesKeyTurnedIn, lambda l: l.JapesKey),
        Event(Events.AztecKeyTurnedIn, lambda l: l.AztecKey),
        Event(Events.FactoryKeyTurnedIn, lambda l: l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.GalleonKey),
        Event(Events.ForestKeyTurnedIn, lambda l: l.ForestKey),
        Event(Events.CavesKeyTurnedIn, lambda l: l.CavesKey),
        Event(Events.CastleKeyTurnedIn, lambda l: l.CastleKey),
        Event(Events.HelmKeyTurnedIn, lambda l: l.HelmKey),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", "Banana Fairy Room", Levels.DKIsles, False, None, [
        LocationLogic(Locations.CameraAndShockwave, lambda l: True),
        LocationLogic(Locations.RarewareBanana, lambda l: l.BananaFairies >= l.settings.rareware_gb_fairies and (l.istiny or l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesFairyToMain),
    ]),

    # All lobies take you to themselves when you die
    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesJapesLobbyToMain),
        TransitionFront(Regions.JungleJapesMain, lambda l: l.IsLevelEnterable(Levels.JungleJapes), Transitions.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyAztecLobby, lambda l: (((l.charge and l.diddy and l.twirl) or l.settings.bonus_barrels == "skip") and l.istiny) or (l.settings.bonus_barrels == "skip" and l.settings.free_trade_items), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True, Transitions.IslesAztecLobbyToMain),
        TransitionFront(Regions.AngryAztecStart, lambda l: l.IsLevelEnterable(Levels.AngryAztec), Transitions.IslesToAztec),
    ]),

    Regions.CrocodileIsleBeyondLift: Region("Crocodile Isle Beyond Lift", "Krem Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesSnideRoom, lambda l: True, Transitions.IslesMainToSnideRoom),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events, Transitions.IslesMainToFactoryLobby),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", "Krem Isle", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: ((l.settings.bonus_barrels == "skip" or l.spring) and l.isdiddy) or (l.settings.bonus_barrels == "skip" and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesBattleArena1, lambda l: not l.settings.crown_placement_rando and l.chunky and l.barrels),
    ], [], [
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: True, Transitions.IslesSnideRoomToMain),
        TransitionFront(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: l.grab and l.bongos and l.donkey),
        LocationLogic(Locations.IslesKasplatFactoryLobby, lambda l: not l.settings.kasplat_rando and l.punch and l.chunky),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
    ], [], [
        TransitionFront(Regions.CrocodileIsleBeyondLift, lambda l: True, Transitions.IslesFactoryLobbyToMain),
        TransitionFront(Regions.FranticFactoryStart, lambda l: l.IsLevelEnterable(Levels.FranticFactory), Transitions.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobbyEntrance: Region("Gloomy Galleon Lobby Entrance", "Level Lobbies", Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesGalleonLobbyToMain),
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True, Transitions.IslesToGalleon),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: l.chunky and l.superSlam and l.mini and l.twirl and l.swim and l.tiny),
        LocationLogic(Locations.IslesKasplatGalleonLobby, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: l.swim),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.IsLevelEnterable(Levels.GloomyGalleon), Transitions.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", "DK Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy),
        LocationLogic(Locations.IslesDiddySummit, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.IslesMainToForestLobby),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: not l.settings.crown_placement_rando and (l.coconut and l.donkey) and (l.peanut and l.diddy)
                      and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.feather and l.tiny),
    ], [], [
        TransitionFront(Regions.CabinIsle, lambda l: True, Transitions.IslesForestLobbyToMain),
        TransitionFront(Regions.FungiForestStart, lambda l: l.IsLevelEnterable(Levels.FungiForest), Transitions.IslesToForest),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: l.punch and l.chunky and l.strongKong and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesKasplatCavesLobby, lambda l: not l.settings.kasplat_rando and l.punch and l.chunky),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True, Transitions.IslesCavesLobbyToMain),  # TODO: Possibly add a region for the outside of CrystalCavesLobby
        TransitionFront(Regions.CrystalCavesMain, lambda l: l.IsLevelEnterable(Levels.CrystalCaves), Transitions.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: l.chunky and l.balloon and l.islanky and l.barrels, MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatCastleLobby, lambda l: not l.settings.kasplat_rando and l.coconut and l.donkey),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesCastleLobbyToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.IsLevelEnterable(Levels.CreepyCastle), Transitions.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", "Level Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: l.gorillaGone and l.ischunky and l.vines, MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatHelmLobby, lambda l: not l.settings.kasplat_rando and l.scope and l.coconut and l.donkey),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.HideoutHelmStart, lambda l: l.gorillaGone and l.chunky and l.vines and l.IsLevelEnterable(Levels.HideoutHelm)),
    ]),

    Regions.KRool: Region("K. Rool", "K. Rool Arena", Levels.DKIsles, True, None, [], [
        Event(Events.KRoolDonkey, lambda l: not l.settings.krool_donkey or l.donkey),
        Event(Events.KRoolDiddy, lambda l: not l.settings.krool_diddy or (l.jetpack and l.peanut and l.diddy)),
        Event(Events.KRoolLanky, lambda l: not l.settings.krool_lanky or (l.trombone and l.lanky)),
        Event(Events.KRoolTiny, lambda l: not l.settings.krool_tiny or (l.mini and l.feather and l.tiny)),
        Event(Events.KRoolChunky, lambda l: not l.settings.krool_chunky or (l.superSlam and l.gorillaGone and l.hunkyChunky and l.punch and l.chunky)),
        Event(Events.KRoolDefeated, lambda l: Events.KRoolDonkey in l.Events and Events.KRoolDiddy in l.Events and Events.KRoolLanky in l.Events and Events.KRoolTiny in l.Events and Events.KRoolChunky in l.Events)
    ], []),
}
