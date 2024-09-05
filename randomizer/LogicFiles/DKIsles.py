# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import FungiTimeSetting, MinigameBarrels, CBRando, RemovedBarriersSelected
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Switches import Switches
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.GameStart: Region("Game Start", HintRegion.GameStart, Levels.DKIsles, False, None, [
        # The locations in this region should *only* be training barrels and starting moves - if you need to put something here, make another region (e.g. Credits)
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        # Starting Shop Owners
        LocationLogic(Locations.ShopOwner_Location00, lambda l: True),
        LocationLogic(Locations.ShopOwner_Location01, lambda l: True),
        LocationLogic(Locations.ShopOwner_Location02, lambda l: True),
        LocationLogic(Locations.ShopOwner_Location03, lambda l: True),
        # Starting Moves
        LocationLogic(Locations.IslesFirstMove, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesClimbing, lambda l: True),
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
        LocationLogic(Locations.PreGiven_Location36, lambda l: True),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: l.settings.fast_start_beginning_of_game or l.settings.auto_keys),
        # Everything you can do in the prison is autocompleted with auto_keys - just copy-paste the logic from the Prison region events here
        Event(Events.JapesKeyTurnedIn, lambda l: l.settings.auto_keys and l.JapesKey and l.HasFillRequirementsForLevel(l.settings.level_order[2])),
        Event(Events.AztecKeyTurnedIn, lambda l: l.settings.auto_keys and l.AztecKey and l.HasFillRequirementsForLevel(l.settings.level_order[3])),
        Event(Events.FactoryKeyTurnedIn, lambda l: l.settings.auto_keys and l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.settings.auto_keys and l.GalleonKey and l.HasFillRequirementsForLevel(l.settings.level_order[5])),
        Event(Events.ForestKeyTurnedIn, lambda l: l.settings.auto_keys and l.ForestKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.CavesKeyTurnedIn, lambda l: l.settings.auto_keys and l.CavesKey and l.HasFillRequirementsForLevel(l.settings.level_order[7])),
        Event(Events.CastleKeyTurnedIn, lambda l: l.settings.auto_keys and l.CastleKey and l.HasFillRequirementsForLevel(l.settings.level_order[7])),
        Event(Events.HelmKeyTurnedIn, lambda l: l.settings.auto_keys and l.HelmKey),
        Event(Events.Night, lambda l: l.settings.fungi_time_internal in (FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.Day, lambda l: l.settings.fungi_time_internal in (FungiTimeSetting.day, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.AztecIceMelted, lambda l: l.checkBarrier(RemovedBarriersSelected.aztec_tiny_temple_ice)),
        Event(Events.TestingGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.factory_testing_gate)),
        Event(Events.LighthouseGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_lighthouse_gate)),
        Event(Events.ShipyardGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_shipyard_area_gate)),
        Event(Events.ActivatedLighthouse, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_seasick_ship)),
        Event(Events.ShipyardTreasureRoomOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_treasure_room)),
        Event(Events.WormGatesOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel)),
        Event(Events.HollowTreeGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_yellow_tunnel)),
    ], [
        # These first 3 Transitions NEED to be in this order, due to Random Starting Location!
        TransitionFront(Regions.Credits, lambda l: True),
        # Replace these with the actual starting region if we choose to randomize it
        TransitionFront(Regions.IslesMain, lambda l: l.settings.fast_start_beginning_of_game),
        TransitionFront(Regions.Treehouse, lambda l: not l.settings.fast_start_beginning_of_game),
        # Medal regions
        TransitionFront(Regions.DKIslesMedals, lambda l: True),
        TransitionFront(Regions.JungleJapesMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.FranticFactoryMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
    ]),

    Regions.DKIslesMedals: Region("DK Isles Medals", HintRegion.IslesCBs, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.IslesDiddyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.IslesLankyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.IslesTinyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.IslesChunkyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], [], restart=-1),

    Regions.Credits: Region("Credits", HintRegion.Credits, Levels.DKIsles, False, None, [
        LocationLogic(Locations.BananaHoard, lambda l: l.WinConditionMet())
    ], [], []),

    Regions.Treehouse: Region("Treehouse", HintRegion.MainIsles, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.TrainingGrounds, lambda l: True, Transitions.IslesTreehouseToStart),
    ]),

    Regions.TrainingGrounds: Region("Training Grounds", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesFirstMove, lambda l: (l.allTrainingChecks and l.crankyAccess) or l.settings.fast_start_beginning_of_game, isAuxiliary=True),
        LocationLogic(Locations.RainbowCoin_Location13, lambda l: True),
        LocationLogic(Locations.RainbowCoin_Location14, lambda l: (l.can_use_vines or l.CanMoonkick()) and l.climbing),  # Banana Hoard patch
    ], [
        Event(Events.TrainingBarrelsSpawned, lambda l: l.crankyAccess or l.settings.fast_start_beginning_of_game),  # Requires Cranky to spawn the training barrels
    ], [
        TransitionFront(Regions.IslesMain, lambda l: l.Slam or l.settings.fast_start_beginning_of_game, Transitions.IslesStartToMain),
        TransitionFront(Regions.Treehouse, lambda l: l.climbing, Transitions.IslesStartToTreehouse),
        TransitionFront(Regions.CrankyIsles, lambda l: l.crankyAccess),
    ]),

    Regions.IslesMain: Region("Isles Main", HintRegion.MainIsles, Levels.DKIsles, True, None, [
        # Don't check for donkey for rock- If lobbies are closed and first B.Locker is not 0, this banana must be grabbable by
        # the starting kong, so for logic we assume any kong can grab it since that's practically true.
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: (l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events)),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: (l.pineapple and l.chunky) or ((l.CanSTS() or l.phasewalk) and (l.ischunky or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesMainEnemy_PineappleCage0, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_FungiCannon0, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_JapesEntrance, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_FungiCannon1, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_PineappleCage1, lambda l: True),
    ], [
        Event(Events.IslesW1aTagged, lambda l: True),
        Event(Events.IslesW1bTagged, lambda l: True),
        Event(Events.IslesW2aTagged, lambda l: True),
        Event(Events.IslesW3aTagged, lambda l: True),
        Event(Events.IslesW3bTagged, lambda l: True),
        Event(Events.IslesW4aTagged, lambda l: True),
        Event(Events.IslesW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.TrainingGrounds, lambda l: True, Transitions.IslesMainToStart),
        TransitionFront(Regions.OuterIsles, lambda l: True),
        TransitionFront(Regions.JungleJapesLobby, lambda l: l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events or l.phasewalk or l.CanSTS(), Transitions.IslesMainToJapesLobby),
        TransitionFront(Regions.KremIsle, lambda l: True),
        TransitionFront(Regions.IslesHill, lambda l: l.climbing or l.assumeUpperIslesAccess),
        TransitionFront(Regions.CabinIsle, lambda l: l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events, Transitions.IslesMainToCastleLobby),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.tbs),
        TransitionFront(Regions.KRool, lambda l: l.CanAccessKRool() or l.assumeKRoolAccess),
    ]),

    Regions.OuterIsles: Region("Outer Isles", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: (l.feather and l.tiny) or ((l.phasewalk or l.CanSTS()) and (l.istiny or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
    ], [
        Event(Events.IslesW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.BananaFairyRoom, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSTS(), Transitions.IslesMainToFairy),
    ]),

    Regions.IslesHill: Region("Isles Hill", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location04, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.can_use_vines or l.CanMoonkick() or l.assumeUpperIslesAccess),
    ]),

    Regions.IslesMainUpper: Region("Isles Main Upper", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.chunky and l.barrels),
        LocationLogic(Locations.IslesMainEnemy_NearAztec, lambda l: True),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunky and l.hasMoveSwitchsanity(Switches.IslesSpawnRocketbarrel, False) and l.barrels),
        Event(Events.IslesW2bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesHill, lambda l: True),
        TransitionFront(Regions.AztecLobbyRoof, lambda l: l.CanMoonkick()),
        TransitionFront(Regions.AngryAztecLobby, lambda l: l.settings.open_lobbies or Events.JapesKeyTurnedIn in l.Events or l.phasewalk, Transitions.IslesMainToAztecLobby),
        TransitionFront(Regions.IslesEar, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events) and ((l.istiny and l.twirl) or (l.isdonkey or l.ischunky or ((l.isdiddy or l.islanky) and l.advanced_platforming) and not l.isKrushaAdjacent(l.kong)) or l.CanMoonkick())),
    ]),

    Regions.IslesEar: Region("Isles Ear", HintRegion.MainIsles, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.CrystalCavesLobby, lambda l: True, Transitions.IslesMainToCavesLobby),
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: (l.istiny and l.twirl) or (l.isdonkey or l.ischunky or ((l.isdiddy or l.islanky) and l.advanced_platforming) and not l.isKrushaAdjacent(l.kong))),
    ]),

    Regions.Prison: Region("Prison", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: (l.sprint and l.islanky) or (l.phasewalk and (l.islanky or l.settings.free_trade_items))),
        LocationLogic(Locations.RainbowCoin_Location12, lambda l: True),
    ], [
        # Changes should match GameStart region for auto_keys considerations
        Event(Events.KLumsyTalkedTo, lambda l: True),
        Event(Events.JapesKeyTurnedIn, lambda l: l.JapesKey and l.HasFillRequirementsForLevel(l.settings.level_order[2])),  # To be able to turn a key in, you must have the *fill moves* required to enter the next level
        Event(Events.AztecKeyTurnedIn, lambda l: l.AztecKey and l.HasFillRequirementsForLevel(l.settings.level_order[3])),  # Only the kongs and moves, not the GBs
        Event(Events.FactoryKeyTurnedIn, lambda l: l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.GalleonKey and l.HasFillRequirementsForLevel(l.settings.level_order[5])),  # This helps prevent weird fill issues in simple level order
        Event(Events.ForestKeyTurnedIn, lambda l: l.ForestKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),  # For example, if a Kong were in lobby 7, this could wreak havoc on key placement
        Event(Events.CavesKeyTurnedIn, lambda l: l.CavesKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.CastleKeyTurnedIn, lambda l: l.CastleKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.HelmKeyTurnedIn, lambda l: l.HelmKey),
    ], [
        TransitionFront(Regions.KremIsle, lambda l: True, Transitions.IslesPrisonToMain),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.CameraAndShockwave, lambda l: True),
    ], [], [
        TransitionFront(Regions.OuterIsles, lambda l: True, Transitions.IslesFairyToMain),
        TransitionFront(Regions.RarewareGBRoom, lambda l: l.CanGetRarewareGB()),
    ]),

    Regions.RarewareGBRoom: Region("Rareware GB Room", HintRegion.RarewareRoom, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RarewareBanana, lambda l: True),
    ], [], [
        TransitionFront(Regions.BananaFairyRoom, lambda l: True),
    ]),

    # All lobies take you to themselves when you die
    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
        LocationLogic(Locations.JapesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesLobbyEnemy_Enemy0, lambda l: True),
        LocationLogic(Locations.JapesLobbyEnemy_Enemy1, lambda l: True),
    ], [
        Event(Events.JapesLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesJapesLobbyToMain),
        TransitionFront(Regions.JungleJapesEntryHandler, lambda l: l.IsLevelEnterable(Levels.JungleJapes), Transitions.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyAztecLobby, lambda l: (((l.charge and l.diddy and l.twirl) or l.settings.bonus_barrels == MinigameBarrels.skip) and l.istiny) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and (l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.phasewalk) and ((l.chunky and l.hunkyChunky) or l.settings.remove_wrinkly_puzzles)),
    ], [
        Event(Events.AztecLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True, Transitions.IslesAztecLobbyToMain),
        TransitionFront(Regions.AngryAztecEntryHandler, lambda l: l.IsLevelEnterable(Levels.AngryAztec), Transitions.IslesToAztec),
    ]),

    Regions.KremIsle: Region("Krem Isle Base", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: ((l.grape or l.CanPhaseswim() or l.phasewalk) and l.lanky) or (l.phasewalk and l.settings.free_trade_items)),
        LocationLogic(Locations.IslesMainEnemy_MonkeyportPad, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.Prison, lambda l: True, Transitions.IslesMainToPrison),
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanPhaseswim()) and (l.swim or l.assumeLevel4Entry), Transitions.IslesMainToGalleonLobby),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanMoonkick() or l.tbs or l.CanMoontail()),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.hasMoveSwitchsanity(Switches.IslesMonkeyport)),
    ]),

    Regions.KremIsleBeyondLift: Region("Krem Isle Beyond Lift", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: (l.coconut and l.isdonkey)),
        LocationLogic(Locations.IslesMainEnemy_UpperFactoryPath, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_LowerFactoryPath0, lambda l: True),
        LocationLogic(Locations.IslesMainEnemy_LowerFactoryPath1, lambda l: True),
    ], [
        Event(Events.IslesW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.KremIsle, lambda l: True),
        TransitionFront(Regions.IslesSnideRoom, lambda l: True, Transitions.IslesMainToSnideRoom),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events, Transitions.IslesMainToFactoryLobby),
    ]),

    Regions.KremIsleTopLevel: Region("Krem Isle Top Level", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.istiny),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera),
    ], [
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.saxophone and l.istiny),
    ], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: (l.generalclips and l.twirl) or l.tbs, Transitions.IslesMainToHelmLobby, isGlitchTransition=True),
        TransitionFront(Regions.KremIsleMouth, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events)),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True),
    ]),

    Regions.KremIsleMouth: Region("Krem Isle Mouth", HintRegion.KremIsles, Levels.DKIsles, False, None, [], [], [
        # You fall through the mouth if the lobby hasn't been opened (if you used a glitch to get in or LZR)
        TransitionFront(Regions.HideoutHelmLobby, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events), Transitions.IslesMainToHelmLobby),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events)),
        # This fall could be a logical point of progression, but you have to surive the drop
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: l.CanSurviveFallDamage()),
        # If you were to die to fall damage here, you'd be sent to the Isles spawn. This is effectively a one-off deathwarp consideration.
        TransitionFront(Regions.IslesMain, lambda l: True),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", HintRegion.KremIsles, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: ((l.settings.bonus_barrels == MinigameBarrels.skip or l.spring) and l.isdiddy) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesBattleArena1, lambda l: not l.settings.crown_placement_rando and l.chunky and l.barrels),
    ], [], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True, Transitions.IslesSnideRoomToMain),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: (l.grab or l.CanMoonkick()) and l.bongos and l.donkey),
        LocationLogic(Locations.IslesKasplatFactoryLobby, lambda l: not l.settings.kasplat_rando and l.punch and l.chunky),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
        LocationLogic(Locations.FactoryDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.FactoryDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy)))),
        LocationLogic(Locations.FactoryLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or l.advanced_platforming)),
        LocationLogic(Locations.FactoryTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy)))),
        LocationLogic(Locations.FactoryChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.FactoryLobbyEnemy_Enemy0, lambda l: True),
    ], [
        Event(Events.FactoryLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: True, Transitions.IslesFactoryLobbyToMain),
        TransitionFront(Regions.FranticFactoryEntryHandler, lambda l: l.IsLevelEnterable(Levels.FranticFactory), Transitions.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobbyEntrance: Region("Gloomy Galleon Lobby Entrance", HintRegion.EarlyLobbies, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesGalleonLobbyToMain),
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: ((l.chunky and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.mini and l.twirl and l.swim and l.tiny) or (l.CanPhaseswim() and (l.istiny or l.settings.free_trade_items))) and (not l.IsLavaWater() or l.Melons >= 3)),
        LocationLogic(Locations.IslesKasplatGalleonLobby, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.GalleonDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [
        Event(Events.GalleonLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: l.swim),
        TransitionFront(Regions.GloomyGalleonEntryHandler, lambda l: l.IsLevelEnterable(Levels.GloomyGalleon), Transitions.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location03, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.twirl and l.istiny and l.advanced_platforming),
        TransitionFront(Regions.IslesAboveWaterfall, lambda l: l.advanced_platforming and (((l.isdiddy or l.isdonkey or l.ischunky) and not l.isKrushaAdjacent(l.kong)) or (l.istiny and l.twirl))),
        TransitionFront(Regions.IslesAirspace, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.IslesMainToForestLobby),
    ]),

    Regions.IslesAboveWaterfall: Region("Isles Above Waterfall", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: (l.peanut and l.isdiddy) or (l.phasewalk and l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.advanced_platforming),
        TransitionFront(Regions.CabinIsle, lambda l: l.CanMoonkick() or (l.advanced_platforming and (((l.isdiddy or l.isdonkey or l.ischunky) and not l.isKrushaAdjacent(l.kong)) or (l.istiny and l.twirl)))),
        TransitionFront(Regions.AztecLobbyRoof, lambda l: l.advanced_platforming and l.istiny and l.twirl),
    ]),

    Regions.IslesAirspace: Region("Isles Airspace", HintRegion.MainIsles, Levels.DKIsles, False, None, [  # You are assumed to be on Rocketbarrel in this region
        LocationLogic(Locations.IslesDiddySummit, lambda l: True, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda l: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: True),
        TransitionFront(Regions.CabinIsle, lambda l: True),
        TransitionFront(Regions.AztecLobbyRoof, lambda l: True),
        TransitionFront(Regions.IslesAboveWaterfall, lambda l: True),
        TransitionFront(Regions.IslesEar, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events)),  # This is likely never relevant because it takes Chunky to spawn the Rocketbarrel
    ]),

    Regions.AztecLobbyRoof: Region("Aztec Lobby Roof", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location05, lambda l: True),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda l: True),
        TransitionFront(Regions.IslesAboveWaterfall, lambda l: l.CanMoonkick()),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: not l.settings.crown_placement_rando and (((l.coconut and l.donkey) and (l.peanut and l.diddy)
                      and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky)) or l.phasewalk) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.hasMoveSwitchsanity(Switches.IslesFungiLobbyFeather, False)),
        LocationLogic(Locations.ForestDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),  # These might look strange
        LocationLogic(Locations.ForestDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),  # But they're all covered
        LocationLogic(Locations.ForestLankyDoor, lambda l: not l.settings.wrinkly_location_rando),  # Check HintAccess() in Logic.py
        LocationLogic(Locations.ForestTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.ForestChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [
        Event(Events.ForestLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.CabinIsle, lambda l: True, Transitions.IslesForestLobbyToMain),
        TransitionFront(Regions.FungiForestEntryHandler, lambda l: l.IsLevelEnterable(Levels.FungiForest), Transitions.IslesToForest),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: ((l.punch and l.chunky and l.strongKong) or l.phasewalk) and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesKasplatCavesLobby, lambda l: not l.settings.kasplat_rando and ((l.punch and l.chunky) or l.phasewalk or l.ledgeclip)),
        LocationLogic(Locations.CavesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles) and ((l.isdiddy and l.jetpack) or l.CanMoonkick())),
        LocationLogic(Locations.CavesLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
    ], [
        Event(Events.CavesLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.IslesEar, lambda l: True, Transitions.IslesCavesLobbyToMain),
        TransitionFront(Regions.CrystalCavesEntryHandler, lambda l: l.IsLevelEnterable(Levels.CrystalCaves), Transitions.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: (l.chunky and l.balloon and l.islanky and l.barrels) or ((l.CanMoonkick() or (l.advanced_platforming and l.istiny and l.twirl and (not l.isKrushaAdjacent(Kongs.tiny)))) and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatCastleLobby, lambda l: not l.settings.kasplat_rando and ((l.coconut and l.donkey) or l.phasewalk)),
        LocationLogic(Locations.CastleDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.RainbowCoin_Location15, lambda l: (l.chunky and l.balloon and l.islanky and l.barrels) or l.CanMoonkick() or (l.advanced_platforming and l.istiny and l.twirl and (not l.isKrushaAdjacent(Kongs.tiny)))),
        LocationLogic(Locations.CastleLobbyEnemy_Left, lambda l: True),
        LocationLogic(Locations.CastleLobbyEnemy_FarRight, lambda l: True),
        LocationLogic(Locations.CastleLobbyEnemy_NearRight, lambda l: True),
    ], [
        Event(Events.CastleLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda l: True, Transitions.IslesCastleLobbyToMain),
        TransitionFront(Regions.CreepyCastleEntryHandler, lambda l: l.IsLevelEnterable(Levels.CreepyCastle), Transitions.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: (l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone, False) and l.ischunky and l.can_use_vines) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.advanced_platforming and l.istiny and l.twirl and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatHelmLobby, lambda l: not l.settings.kasplat_rando and ((l.scope and l.coconut) or (l.twirl and l.tiny and l.advanced_platforming))),
    ], [
        Event(Events.HelmLobbyAccessed, lambda l: True),
    ], [
        TransitionFront(Regions.KremIsleMouth, lambda l: True, Transitions.IslesHelmLobbyToMain),
        TransitionFront(Regions.HideoutHelmEntry, lambda l: ((l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone) and l.can_use_vines) or (l.CanMoonkick() and l.donkey)) and l.IsLevelEnterable(Levels.HideoutHelm), Transitions.IslesToHelm),
    ]),

    Regions.KRool: Region("K. Rool", HintRegion.KRool, Levels.DKIsles, True, None, [], [
        Event(Events.KRoolDonkey, lambda l: not l.settings.krool_donkey or ((l.blast or not l.settings.cannons_require_blast) and l.donkey and l.climbing)),
        Event(Events.KRoolDiddy, lambda l: not l.settings.krool_diddy or (l.jetpack and l.peanut and l.diddy)),
        Event(Events.KRoolLanky, lambda l: not l.settings.krool_lanky or (l.trombone and l.lanky and l.barrels)),
        Event(Events.KRoolTiny, lambda l: not l.settings.krool_tiny or (l.mini and l.feather and l.tiny and (l.climbing or l.twirl))),
        Event(Events.KRoolChunky, lambda l: not l.settings.krool_chunky or (l.CanSlamChunkyPhaseSwitch() and l.gorillaGone and l.hunkyChunky and l.punch and l.chunky)),
        Event(Events.KRoolDillo1, lambda l: not l.settings.krool_dillo1 or l.barrels),
        Event(Events.KRoolDog1, lambda l: not l.settings.krool_dog1 or l.barrels),
        Event(Events.KRoolJack, lambda l: not l.settings.krool_madjack or (l.Slam and l.twirl and l.tiny)),
        Event(Events.KRoolPufftoss, lambda l: not l.settings.krool_pufftoss or True),
        Event(Events.KRoolDog2, lambda l: not l.settings.krool_dog2 or (l.barrels and l.hunkyChunky and l.chunky)),
        Event(Events.KRoolDillo2, lambda l: not l.settings.krool_dillo2 or l.barrels),
        Event(Events.KRoolKKO, lambda l: not l.settings.krool_kutout or True),
        Event(Events.KRoolDefeated, lambda l: Events.KRoolDonkey in l.Events and Events.KRoolDiddy in l.Events and Events.KRoolLanky in l.Events and Events.KRoolTiny in l.Events and Events.KRoolChunky in l.Events and Events.KRoolDillo1 in l.Events and Events.KRoolDillo2 in l.Events and Events.KRoolDog1 in l.Events and Events.KRoolDog2 in l.Events and Events.KRoolJack in l.Events and Events.KRoolPufftoss in l.Events and Events.KRoolKKO in l.Events)
    ], []),
}
