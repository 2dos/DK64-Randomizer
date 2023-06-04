# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import MinigameBarrels
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.GameStart: Region("Game Start", "Training Grounds", Levels.DKIsles, False, None, [
        # The locations in this region should *only* be training barrels and starting moves - if you need to put something here, make another region (e.g. Credits)
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        # Starting Moves
        LocationLogic(Locations.PreGiven_Location00, lambda l: True),
        LocationLogic(Locations.PreGiven_Location01, lambda l: True),
        LocationLogic(Locations.PreGiven_Location02, lambda l: True),
        LocationLogic(Locations.PreGiven_Location03, lambda l: True),
        LocationLogic(Locations.PreGiven_Location04, lambda l: True),
        LocationLogic(Locations.PreGiven_Location05, lambda l: True),
        LocationLogic(Locations.PreGiven_Location06, lambda l: True),
        LocationLogic(Locations.PreGiven_Location07, lambda l: True),
        LocationLogic(Locations.PreGiven_Location08, lambda l: True),
        LocationLogic(Locations.PreGiven_Location09, lambda l: True),
        LocationLogic(Locations.PreGiven_Location10, lambda l: True),
        LocationLogic(Locations.PreGiven_Location11, lambda l: True),
        LocationLogic(Locations.PreGiven_Location12, lambda l: True),
        LocationLogic(Locations.PreGiven_Location13, lambda l: True),
        LocationLogic(Locations.PreGiven_Location14, lambda l: True),
        LocationLogic(Locations.PreGiven_Location15, lambda l: True),
        LocationLogic(Locations.PreGiven_Location16, lambda l: True),
        LocationLogic(Locations.PreGiven_Location17, lambda l: True),
        LocationLogic(Locations.PreGiven_Location18, lambda l: True),
        LocationLogic(Locations.PreGiven_Location19, lambda l: True),
        LocationLogic(Locations.PreGiven_Location20, lambda l: True),
        LocationLogic(Locations.PreGiven_Location21, lambda l: True),
        LocationLogic(Locations.PreGiven_Location22, lambda l: True),
        LocationLogic(Locations.PreGiven_Location23, lambda l: True),
        LocationLogic(Locations.PreGiven_Location24, lambda l: True),
        LocationLogic(Locations.PreGiven_Location25, lambda l: True),
        LocationLogic(Locations.PreGiven_Location26, lambda l: True),
        LocationLogic(Locations.PreGiven_Location27, lambda l: True),
        LocationLogic(Locations.PreGiven_Location28, lambda l: True),
        LocationLogic(Locations.PreGiven_Location29, lambda l: True),
        LocationLogic(Locations.PreGiven_Location30, lambda l: True),
        LocationLogic(Locations.PreGiven_Location31, lambda l: True),
        LocationLogic(Locations.PreGiven_Location32, lambda l: True),
        LocationLogic(Locations.PreGiven_Location33, lambda l: True),
        LocationLogic(Locations.PreGiven_Location34, lambda l: True),
        LocationLogic(Locations.PreGiven_Location35, lambda l: True),
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
        LocationLogic(Locations.RainbowCoin_Location13, lambda l: l.shockwave),
        LocationLogic(Locations.RainbowCoin_Location14, lambda l: l.shockwave and (l.vines or l.CanMoonkick())),  # Banana Hoard patch
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesStartToMain),
        TransitionFront(Regions.Treehouse, lambda l: True, Transitions.IslesStartToTreehouse),
        TransitionFront(Regions.CrankyIsles, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", "DK Isle", Levels.DKIsles, True, None, [
        # Don't check for donkey for rock- If lobbies are closed and first B.Locker is not 0, this banana must be grabbable by
        # the starting kong, so for logic we assume any kong can grab it since that's practically true.
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: (l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events)),
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: (l.feather and l.tiny) or ((l.phasewalk or l.CanSTS()) and (l.istiny or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: ((l.grape or l.CanPhaseswim() or l.phasewalk) and l.lanky) or (l.phasewalk and l.settings.free_trade_items)),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: (l.pineapple and l.chunky) or ((l.CanSTS() or l.phasewalk) and (l.ischunky or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
        LocationLogic(Locations.RainbowCoin_Location04, lambda l: l.shockwave),
    ], [
        Event(Events.IslesW1aTagged, lambda l: True),
        Event(Events.IslesW1bTagged, lambda l: True),
        Event(Events.IslesW2aTagged, lambda l: True),
        Event(Events.IslesW3aTagged, lambda l: True),
        Event(Events.IslesW3bTagged, lambda l: True),
        Event(Events.IslesW4aTagged, lambda l: True),
        Event(Events.IslesW5aTagged, lambda l: True),
        Event(Events.IslesW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.TrainingGrounds, lambda l: True, Transitions.IslesMainToStart),
        TransitionFront(Regions.Prison, lambda l: True),
        TransitionFront(Regions.BananaFairyRoom, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSTS(), Transitions.IslesMainToFairy),
        TransitionFront(Regions.JungleJapesLobby, lambda l: l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events or l.phasewalk or l.CanSTS(), Transitions.IslesMainToJapesLobby),
        TransitionFront(Regions.KremIsle, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.vines or l.CanMoonkick() or l.assumeUpperIslesAccess),
        TransitionFront(Regions.CabinIsle, lambda l: l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events or l.CanMoonkick()),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events, Transitions.IslesMainToCastleLobby),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.tbs),
        TransitionFront(Regions.KRool, lambda l: l.CanAccessKRool() or l.assumeKRoolAccess),
    ]),

    Regions.IslesMainUpper: Region("Isles Main Upper", "DK Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.chunky and l.barrels),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
        Event(Events.IslesW2bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.AngryAztecLobby, lambda l: l.settings.open_lobbies or Events.JapesKeyTurnedIn in l.Events or l.phasewalk, Transitions.IslesMainToAztecLobby),
        TransitionFront(Regions.CrystalCavesLobby, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events) and (l.isdonkey or l.ischunky or (l.istiny and l.twirl) or ((l.isdiddy or l.islanky) and l.advanced_platforming) or l.CanMoonkick()), Transitions.IslesMainToCavesLobby),
    ]),

    Regions.Prison: Region("Prison", "Krem Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: (l.sprint and l.islanky) or (l.phasewalk and (l.islanky or l.settings.free_trade_items))),
        LocationLogic(Locations.RainbowCoin_Location12, lambda l: l.shockwave),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: True),
        Event(Events.JapesKeyTurnedIn, lambda l: l.JapesKey and l.HasFillRequirementsForLevel(l.settings.level_order[2])),  # To be able to turn a key in, you must have the *fill moves* required to enter the next level
        Event(Events.AztecKeyTurnedIn, lambda l: l.AztecKey and l.HasFillRequirementsForLevel(l.settings.level_order[3])),  # Only the kongs and moves, not the GBs
        Event(Events.FactoryKeyTurnedIn, lambda l: l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.GalleonKey and l.HasFillRequirementsForLevel(l.settings.level_order[5])),  # This helps prevent weird fill issues in simple level order
        Event(Events.ForestKeyTurnedIn, lambda l: l.ForestKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),  # For example, if a Kong were in lobby 7, this could wreak havoc on key placement
        Event(Events.CavesKeyTurnedIn, lambda l: l.CavesKey and l.HasFillRequirementsForLevel(Levels.HideoutHelm)),
        Event(Events.CastleKeyTurnedIn, lambda l: l.CastleKey and l.HasFillRequirementsForLevel(Levels.HideoutHelm)),
        Event(Events.HelmKeyTurnedIn, lambda l: l.HelmKey),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", "Banana Fairy Room", Levels.DKIsles, False, None, [
        LocationLogic(Locations.CameraAndShockwave, lambda l: True),
        LocationLogic(Locations.RarewareBanana, lambda l: l.CanGetRarewareGB()),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesFairyToMain),
    ]),

    # All lobies take you to themselves when you die
    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", "Japes-Forest Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
        LocationLogic(Locations.JapesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),

    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesJapesLobbyToMain),
        TransitionFront(Regions.JungleJapesStart, lambda l: l.IsLevelEnterable(Levels.JungleJapes), Transitions.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", "Japes-Forest Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyAztecLobby, lambda l: (((l.charge and l.diddy and l.twirl) or l.settings.bonus_barrels == MinigameBarrels.skip) and l.istiny) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and l.tiny and l.feather and ((l.chunky and l.hunkyChunky) or l.settings.remove_wrinkly_puzzles)),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True, Transitions.IslesAztecLobbyToMain),
        TransitionFront(Regions.AngryAztecStart, lambda l: l.IsLevelEnterable(Levels.AngryAztec), Transitions.IslesToAztec),
    ]),

    Regions.KremIsle: Region("Krem Isle Base", "Krem Isle", Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanPhaseswim()) and (l.swim or l.assumeLevel4Entry), Transitions.IslesMainToGalleonLobby),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanMoonkick() or l.tbs),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.monkeyport and l.istiny),
    ]),

    Regions.KremIsleBeyondLift: Region("Krem Isle Beyond Lift", "Krem Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: (l.coconut and l.isdonkey) or ((l.CanSkew(True) and l.CanSTS()) and (l.isdonkey or l.settings.free_trade_items))),
    ], [
        Event(Events.IslesW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.KremIsle, lambda l: True),
        TransitionFront(Regions.IslesSnideRoom, lambda l: True, Transitions.IslesMainToSnideRoom),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or (l.CanSkew(True) and l.CanSTS()), Transitions.IslesMainToFactoryLobby),
    ]),

    Regions.KremIsleTopLevel: Region("Krem Isle Top Level", "Krem Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.tiny),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera),
    ], [
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.saxophone and l.tiny),
    ], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: (l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events) or (l.generalclips and l.twirl)) or l.tbs),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", "Krem Isle", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: ((l.settings.bonus_barrels == MinigameBarrels.skip or l.spring) and l.isdiddy) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesBattleArena1, lambda l: not l.settings.crown_placement_rando and l.chunky and l.barrels),
    ], [], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True, Transitions.IslesSnideRoomToMain),
        TransitionFront(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", "Japes-Forest Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: (l.grab or l.CanMoonkick()) and l.bongos and l.donkey),
        LocationLogic(Locations.IslesKasplatFactoryLobby, lambda l: not l.settings.kasplat_rando and l.punch and l.chunky),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
        LocationLogic(Locations.FactoryDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.FactoryDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy or l.ischunky)))),
        LocationLogic(Locations.FactoryLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy or l.ischunky)))),
        LocationLogic(Locations.FactoryTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy or l.ischunky)))),
        LocationLogic(Locations.FactoryChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True, Transitions.IslesFactoryLobbyToMain),
        TransitionFront(Regions.FranticFactoryStart, lambda l: l.IsLevelEnterable(Levels.FranticFactory), Transitions.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobbyEntrance: Region("Gloomy Galleon Lobby Entrance", "Level Lobbies", Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesGalleonLobbyToMain),
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", "Japes-Forest Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: ((l.chunky and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.mini and l.twirl and l.swim and l.tiny) or (l.CanPhaseswim() and (l.istiny or l.settings.free_trade_items)))),
        LocationLogic(Locations.IslesKasplatGalleonLobby, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.GalleonDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [], [
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: l.swim),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.IsLevelEnterable(Levels.GloomyGalleon), Transitions.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", "DK Isle", Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: ((Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack) or (l.advanced_platforming and (l.isdiddy or (l.isdonkey and l.settings.krusha_kong != Kongs.donkey) or (l.istiny and l.twirl) or l.ischunky))) and ((l.peanut and l.isdiddy) or l.phasewalk and l.settings.free_trade_items)),
        LocationLogic(Locations.IslesDiddySummit, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.RainbowCoin_Location03, lambda l: l.shockwave),
        LocationLogic(Locations.RainbowCoin_Location05, lambda l: ((Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy) or (l.twirl and l.istiny and l.advanced_platforming)) and l.shockwave),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.IslesMainToForestLobby),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", "Japes-Forest Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: not l.settings.crown_placement_rando and (((l.coconut and l.donkey) and (l.peanut and l.diddy)
                      and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky)) or l.phasewalk) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.feather and l.tiny),
        LocationLogic(Locations.ForestDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),  # These might look strange
        LocationLogic(Locations.ForestDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),  # But they're all covered
        LocationLogic(Locations.ForestLankyDoor, lambda l: not l.settings.wrinkly_location_rando),  # Check HintAccess() in Logic.py
        LocationLogic(Locations.ForestTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.ForestChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [], [
        TransitionFront(Regions.CabinIsle, lambda l: True, Transitions.IslesForestLobbyToMain),
        TransitionFront(Regions.FungiForestStart, lambda l: l.IsLevelEnterable(Levels.FungiForest), Transitions.IslesToForest),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", "Caves-Helm Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: ((l.punch and l.chunky and l.strongKong) or l.phasewalk) and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesKasplatCavesLobby, lambda l: not l.settings.kasplat_rando and ((l.punch and l.chunky) or l.phasewalk or l.ledgeclip)),
        LocationLogic(Locations.CavesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles) and l.isdiddy and l.jetpack),
        LocationLogic(Locations.CavesLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True, Transitions.IslesCavesLobbyToMain),  # TODO: Possibly add a region for the outside of CrystalCavesLobby
        TransitionFront(Regions.CrystalCavesMain, lambda l: l.IsLevelEnterable(Levels.CrystalCaves), Transitions.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", "Caves-Helm Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: (l.chunky and l.balloon and l.islanky and l.barrels) or ((l.CanMoonkick() or (l.advanced_platforming and l.istiny and l.twirl and l.settings.krusha_kong != Kongs.tiny)) and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatCastleLobby, lambda l: not l.settings.kasplat_rando and ((l.coconut and l.donkey) or l.phasewalk)),
        LocationLogic(Locations.CastleDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.RainbowCoin_Location15, lambda l: l.shockwave and ((l.chunky and l.balloon and l.islanky and l.barrels) or l.CanMoonkick() or (l.advanced_platforming and l.istiny and l.twirl and l.settings.krusha_kong != Kongs.tiny))),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesCastleLobbyToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.IsLevelEnterable(Levels.CreepyCastle), Transitions.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", "Caves-Helm Lobbies", Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: (l.gorillaGone and l.ischunky and l.vines) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.advanced_platforming and l.istiny and l.twirl and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatHelmLobby, lambda l: not l.settings.kasplat_rando and ((l.scope and l.coconut) or (l.twirl and l.tiny and l.advanced_platforming))),
    ], [], [
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events)),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True),  # You fall through the mouth if the lobby hasn't been opened (if you used a glitch to get in)
        TransitionFront(Regions.HideoutHelmStart, lambda l: ((l.gorillaGone and l.chunky and l.vines) or (l.CanMoonkick() and l.donkey)) and l.IsLevelEnterable(Levels.HideoutHelm)),
    ]),

    Regions.KRool: Region("K. Rool", "K. Rool Arena", Levels.DKIsles, True, None, [], [
        Event(Events.KRoolDonkey, lambda l: not l.settings.krool_donkey or l.donkey),
        Event(Events.KRoolDiddy, lambda l: not l.settings.krool_diddy or (l.jetpack and l.peanut and l.diddy)),
        Event(Events.KRoolLanky, lambda l: not l.settings.krool_lanky or (l.trombone and l.lanky and l.barrels)),
        Event(Events.KRoolTiny, lambda l: not l.settings.krool_tiny or (l.mini and l.feather and l.tiny)),
        Event(Events.KRoolChunky, lambda l: not l.settings.krool_chunky or (l.superSlam and l.gorillaGone and l.hunkyChunky and l.punch and l.chunky)),
        Event(Events.KRoolDefeated, lambda l: Events.KRoolDonkey in l.Events and Events.KRoolDiddy in l.Events and Events.KRoolLanky in l.Events and Events.KRoolTiny in l.Events and Events.KRoolChunky in l.Events)
    ], []),
}
