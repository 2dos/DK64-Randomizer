"""Instance Script library functions and classes."""

from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Settings import SwitchsanityGone
from randomizer.Enums.Songs import Songs
from randomizer.Patching.Library.DataTypes import short_to_ushort
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ScriptsLib import *

def getCScript(index: int, item_id: int):
    """Get the generic c script caller."""
    return compileInstanceScript(item_id, [ScriptBlock([], [FunctionData(7, [125, short_to_ushort(index), item_id])])])


level_map_mapping = {
    Levels.DKIsles: [
        Maps.Isles,
        Maps.BananaFairyRoom,
        Maps.JungleJapesLobby,
        Maps.AngryAztecLobby,
        Maps.IslesSnideRoom,
        Maps.FranticFactoryLobby,
        Maps.GloomyGalleonLobby,
        Maps.FungiForestLobby,
        Maps.CrystalCavesLobby,
        Maps.CreepyCastleLobby,
        Maps.HideoutHelmLobby,
        Maps.TrainingGrounds,
        Maps.Treehouse,
        Maps.KLumsy,
    ],
    Levels.JungleJapes: [
        Maps.JungleJapes,
        Maps.JapesTinyHive,
        Maps.JapesLankyCave,
        Maps.JapesMountain,
        Maps.JapesMinecarts,
        Maps.JapesUnderGround,
        Maps.JapesBaboonBlast,
    ],
    Levels.AngryAztec: [
        Maps.AngryAztec,
        Maps.AztecTinyTemple,
        Maps.AztecDonkey5DTemple,
        Maps.AztecDiddy5DTemple,
        Maps.AztecLanky5DTemple,
        Maps.AztecTiny5DTemple,
        Maps.AztecChunky5DTemple,
        Maps.AztecTinyRace,
        Maps.AztecLlamaTemple,
        Maps.AztecBaboonBlast,
    ],
    Levels.FranticFactory: [
        Maps.FranticFactory,
        Maps.FactoryTinyRace,
        Maps.FactoryPowerHut,
        Maps.FactoryCrusher,
        Maps.FactoryBaboonBlast,
    ],
    Levels.GloomyGalleon: [
        Maps.GloomyGalleon,
        Maps.GalleonLighthouse,
        Maps.GalleonMermaidRoom,
        Maps.GalleonSickBay,
        Maps.GalleonSealRace,
        Maps.GalleonTreasureChest,
        Maps.GalleonSubmarine,
        Maps.GalleonMechafish,
        Maps.Galleon5DShipDKTiny,
        Maps.Galleon5DShipDiddyLankyChunky,
        Maps.Galleon2DShip,
        Maps.GalleonBaboonBlast,
    ],
    Levels.FungiForest: [
        Maps.FungiForest,
        Maps.ForestMinecarts,
        Maps.ForestGiantMushroom,
        Maps.ForestChunkyFaceRoom,
        Maps.ForestLankyZingersRoom,
        Maps.ForestLankyMushroomsRoom,
        Maps.ForestAnthill,
        Maps.ForestMillFront,
        Maps.ForestMillBack,
        Maps.ForestSpider,
        Maps.ForestRafters,
        Maps.ForestWinchRoom,
        Maps.ForestMillAttic,
        Maps.ForestThornvineBarn,
        Maps.ForestBaboonBlast,
    ],
    Levels.CrystalCaves: [
        Maps.CrystalCaves,
        Maps.CavesLankyRace,
        Maps.CavesFrozenCastle,
        Maps.CavesDonkeyIgloo,
        Maps.CavesDiddyIgloo,
        Maps.CavesLankyIgloo,
        Maps.CavesTinyIgloo,
        Maps.CavesChunkyIgloo,
        Maps.CavesRotatingCabin,
        Maps.CavesDonkeyCabin,
        Maps.CavesDiddyLowerCabin,
        Maps.CavesDiddyUpperCabin,
        Maps.CavesLankyCabin,
        Maps.CavesTinyCabin,
        Maps.CavesChunkyCabin,
        Maps.CavesBaboonBlast,
    ],
    Levels.CreepyCastle: [
        Maps.CreepyCastle,
        Maps.CastleTree,
        Maps.CastleLibrary,
        Maps.CastleBallroom,
        Maps.CastleMuseum,
        Maps.CastleTinyRace,
        Maps.CastleTower,
        Maps.CastleGreenhouse,
        Maps.CastleTrashCan,
        Maps.CastleShed,
        Maps.CastleLowerCave,
        Maps.CastleCrypt,
        Maps.CastleMinecarts,
        Maps.CastleMausoleum,
        Maps.CastleUpperCave,
        Maps.CastleDungeon,
        Maps.CastleBaboonBlast,
    ],
    Levels.HideoutHelm: [
        Maps.HideoutHelm,
    ],
}
level_key_flag_mapping = {
    Levels.JungleJapes: 0x1A,
    Levels.AngryAztec: 0x4A,
    Levels.FranticFactory: 0x8A,
    Levels.GloomyGalleon: 0xA8,
    Levels.FungiForest: 0xEC,
    Levels.CrystalCaves: 0x124,
    Levels.CreepyCastle: 0x13D,
}
level_portal_flag_mapping = {
    Levels.JungleJapes: 0x2E,
    Levels.AngryAztec: 0x6C,
    Levels.FranticFactory: 0x98,
    Levels.GloomyGalleon: 0xCB,
    Levels.FungiForest: 0x102,
    Levels.CrystalCaves: 0x12E,
    Levels.CreepyCastle: 0x160,
}


def getLevel(map_id: Maps, source: str, lobby_is_isles: bool = True) -> Levels:
    """Get the level associated with a map."""
    if not lobby_is_isles:
        lobby_mapping = {
            Maps.JungleJapesLobby: Levels.JungleJapes,
            Maps.AngryAztecLobby: Levels.AngryAztec,
            Maps.FranticFactoryLobby: Levels.FranticFactory,
            Maps.GloomyGalleonLobby: Levels.GloomyGalleon,
            Maps.FungiForestLobby: Levels.FungiForest,
            Maps.CrystalCavesLobby: Levels.CrystalCaves,
            Maps.CreepyCastleLobby: Levels.CreepyCastle,
            Maps.HideoutHelmLobby: Levels.HideoutHelm,
        }
        if map_id in lobby_mapping:
            return lobby_mapping[map_id]
    for lvl, map_ids in level_map_mapping.items():
        if map_id in map_ids:
            return lvl
    raise Exception(f"Invalid level for {source}")


def getTroffPortalScript(map_id: Maps, item_id: int, exit_id: int) -> list[int]:
    """Get the instance script for a troff and scoff portal."""
    level_id: Levels = None
    boss_flag = level_key_flag_mapping[Levels.JungleJapes]
    portal_flag = level_portal_flag_mapping[Levels.JungleJapes]
    portal_range = 90
    if map_id != Maps.TroffNScoff:
        portal_range = 60
        level_id = getLevel(map_id, "portal")
        portal_flag = level_portal_flag_mapping[level_id]
        boss_flag = level_key_flag_mapping[level_id]
    return compileInstanceScript(
        item_id,
        [
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(22, [1, 0, 0]),
                    FunctionData(20, [1, 160, 0]),
                    FunctionData(22, [3, 0, 0]),
                    FunctionData(20, [3, 115, 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    IScript_IsFlagSet(portal_flag),
                ],
                [
                    IScript_SetOpacity(True, 0, 255),
                    IScript_SetTangibility(False),
                    IScript_SetState(20),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    IScript_IsFlagSet(boss_flag, FlagType.permanent, True, lambda m: m != Maps.TroffNScoff),
                ],
                [
                    FunctionData(17, [1, 65535, 0]),
                    FunctionData(17, [3, 65535, 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    IScript_IsFlagSet(portal_flag, FlagType.permanent, True, lambda m: m != Maps.TroffNScoff),
                ],
                [
                    IScript_SetTimer(45),
                    IScript_SetState(1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InRange(portal_range),
                    IScript_IsCutsceneActive(True, lambda m: m == Maps.TroffNScoff),
                ],
                [
                    FunctionData(3, [60, 0, 0], inclusion_lambda=lambda m: m != Maps.TroffNScoff),
                    FunctionData(3, [0, 60, 0], inclusion_lambda=lambda m: m == Maps.TroffNScoff),
                    FunctionData(7, [116, 0, 1]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InRange(portal_range),
                    IScript_IsCutsceneActive(True, lambda m: m == Maps.TroffNScoff),
                ],
                [
                    FunctionData(110, [1, 0, 0]),
                    IScript_PlayCutscene(29, 0, 15),
                    IScript_SetAction(90),
                    IScript_SetState(100),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(100),
                    IScript_IsTimer(0),
                    IScript_IsFlagSet(boss_flag),
                ],
                [
                    IScript_SetTimer(60),
                    IScript_SetFlag(portal_flag),
                    IScript_SetState(40),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(100),
                    IScript_IsTimer(0),
                    IScript_IsFlagSet(boss_flag, FlagType.permanent, True, lambda m: m != Maps.TroffNScoff),
                ],
                [
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(40),
                    IScript_IsTimer(0),
                ],
                [
                    IScript_SetOpacity(True, 0, 4),
                    IScript_SetTangibility(False),
                    IScript_PlaySFX(994, pitch_variance=20, volume_unk_mult=10),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(40),
                    IScript_IsTimer(0),
                ],
                [
                    IScript_SetState(41),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(41),
                    FunctionData(21, [2, 0, 0]),
                ],
                [
                    FunctionData(7, [116, 0, 2]),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(41),
                    FunctionData(21, [2, 0, 0], True),
                ],
                [
                    IScript_SetState(20),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InRange(60, True),
                ],
                [
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_IsCutsceneActive(),
                ],
                [
                    IScript_SetState(2),
                ],
                lambda m: m == Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(2),
                    IScript_IsTimer(0),
                ],
                [
                    FunctionData(90, [60, 60, 60]),
                    FunctionData(61, [3, 0, 0]),
                    IScript_SetState(3),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(3),
                    IScript_IsFlagSet(portal_flag),
                ],
                [
                    IScript_SetOpacity(True, 0, 255),
                    IScript_SetTangibility(False),
                    IScript_SetState(20),
                ],
                lambda m: m != Maps.TroffNScoff,
            ),
            ScriptBlock(
                [
                    IScript_IsState(3),
                    FunctionData(16, [1, 1, 0]),
                ],
                [
                    IScript_SetTimer(5),
                    FunctionData(7, [116, 0, 0]),
                    FunctionData(110, [1, 0, 0]),
                    FunctionData(37, [28, 0, 15]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(3),
                    FunctionData(16, [1, 1, 0]),
                ],
                [
                    IScript_SetAction(89),
                    IScript_SetState(4),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(4),
                    IScript_IsTimer(0),
                ],
                [
                    FunctionData(134, [short_to_ushort(exit_id), 0, 0], inclusion_lambda=lambda m: m != Maps.TroffNScoff),
                    FunctionData(135, [0, 0, 0], inclusion_lambda=lambda m: m == Maps.TroffNScoff),
                    IScript_SetState(5),
                ],
            ),
            ScriptBlock(
                [
                    IScript_True(),
                ],
                [
                    FunctionData(7, [125, short_to_ushort(-3), item_id]),
                ],
            ),
        ],
        map_id,
    )


level_crown_map_mapping = {
    Levels.JungleJapes: [Maps.JapesCrown],
    Levels.AngryAztec: [Maps.AztecCrown],
    Levels.FranticFactory: [Maps.FactoryCrown],
    Levels.GloomyGalleon: [Maps.GalleonCrown],
    Levels.FungiForest: [Maps.ForestCrown],
    Levels.CrystalCaves: [Maps.CavesCrown],
    Levels.CreepyCastle: [Maps.CastleCrown],
    Levels.HideoutHelm: [Maps.HelmCrown],
    Levels.DKIsles: [Maps.LobbyCrown, Maps.SnidesCrown],
}
level_crown_flag_mapping = {
    Levels.JungleJapes: [0x261],
    Levels.AngryAztec: [0x262],
    Levels.FranticFactory: [0x263],
    Levels.GloomyGalleon: [0x264],
    Levels.FungiForest: [0x265],
    Levels.CrystalCaves: [0x268],
    Levels.CreepyCastle: [0x269],
    Levels.HideoutHelm: [0x26A],
    Levels.DKIsles: [0x266, 0x267],
}


def getCrownScript(container_map_id: Maps, item_id: int, isIsles2: bool = False) -> list[int]:
    """Get the instance script for the battle crown pad."""
    level_id = getLevel(container_map_id, "crown pad")
    map_list = level_crown_map_mapping[level_id]
    flag_list = level_crown_flag_mapping[level_id]
    crown_target_map = Maps.JapesCrown
    flag_id = 0
    if isIsles2:
        crown_target_map = map_list[1]
        flag_id = flag_list[1]
    else:
        crown_target_map = map_list[0]
        flag_id = flag_list[0]
    return compileInstanceScript(
        item_id,
        [
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    IScript_SetScriptRunState(RunState.distance, 900),
                    IScript_SetState(1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsFlagSet(flag_id),
                ],
                [
                    FunctionData(71, [0, 0, 0]),
                    IScript_SetOpacity(True, 0, 255),
                    IScript_SetScriptRunState(RunState.pause),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(18, [4, 2, 0]),
                    FunctionData(29, [1, 0, 0]),
                ],
                [
                    FunctionData(73, [7, crown_target_map, 2]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(18, [3, 2, 0]),
                    FunctionData(29, [1, 0, 0]),
                ],
                [
                    FunctionData(73, [7, crown_target_map, 2]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(18, [2, 2, 0]),
                    FunctionData(29, [1, 0, 0]),
                ],
                [
                    FunctionData(73, [7, crown_target_map, 2]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(18, [5, 2, 0]),
                    FunctionData(29, [1, 0, 0]),
                ],
                [
                    FunctionData(73, [7, crown_target_map, 2]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(18, [6, 2, 0]),
                    FunctionData(29, [1, 0, 0]),
                ],
                [
                    FunctionData(73, [7, crown_target_map, 2]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    FunctionData(13, [2, 0, 0]),
                    IScript_IsFlagSet(358, FlagType.permanent, True),
                ],
                [
                    IScript_SetFlag(358),
                    FunctionData(110, [1, 0, 0]),
                    FunctionData(37, [24, 1, 0]),
                    IScript_SetState(2),
                ],
            ),
        ],
    )


def getCrateScript(item_id: int) -> list[int]:
    """Get the instance script for a melon crate."""
    return compileInstanceScript(
        item_id,
        [
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(90, [50, 50, 50]),
                    FunctionData(61, [4, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(20, [1, 255, 0]),
                    FunctionData(17, [1, 65535, 0]),
                    IScript_SetScriptRunState(RunState.distance, 500),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(24, [1, 1, 0]),
                    IScript_SetState(1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_IsState(0, 1),
                    FunctionData(55, [1, 18, 0]),
                ],
                [
                    IScript_PlaySFX(757, 100, 0, 80, 20),
                    IScript_SetState(1, 1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_IsState(0, 1),
                    FunctionData(55, [1, 19, 0]),
                ],
                [
                    IScript_PlaySFX(757, 100, 0, 70, 20),
                    IScript_SetState(1, 1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_IsState(1, 1),
                    FunctionData(55, [1, 18, 0], True),
                    FunctionData(55, [1, 19, 0], True),
                ],
                [
                    IScript_SetState(0, 1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    FunctionData(16, [4, 1, 0]),
                ],
                [
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InControlState(28),
                    IScript_IsStandingOnObject(),
                ],
                [
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    FunctionData(16, [1, 1, 0]),
                    FunctionData(57, [2040, 0, 0]),
                ],
                [
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(2),
                ],
                [
                    IScript_PlaySong(Songs.MelonSliceDrop),
                    IScript_PlaySFX(35),
                    FunctionData(7, [16, 0, 0]),
                    FunctionData(79, [65534, 0, 0]),
                ],
            ),
        ],
    )


def getFiveTwoDoorShipGateScript(item_id: int, flag_id: int, timer: int, timer_2: int, tied_pad: int) -> list[int]:
    is_slam_switch = flag_id in (0x2FE, 0x2FF)
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsState(0),
            IScript_IsFlagSet(flag_id),
        ], [
            IScript_SetState(10),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_IsFlagSet(flag_id, FlagType.permanent, True),
        ], [
            FunctionData(20, [1 if is_slam_switch else 2, 2, 0], False, lambda f: f != 0x2FC),  # Not Chunky
            FunctionData(22, [1 if is_slam_switch else 2, 1, 0], False, lambda f: f != 0x2FC),  # Not Chunky
            IScript_SetScriptRunState(RunState.pause),
        ]),
        ScriptBlock([
            IScript_IsState(10),
        ], [
            FunctionData(20, [2, 2, 0], False, lambda f: f == 0x2FC),  # Chunky
            FunctionData(22, [2, 1, 0], False, lambda f: f == 0x2FC),  # Chunky
            IScript_SetTimer(300 if flag_id == 0x2FF else 250),
            IScript_SetState(11),
            IScript_SetFlag(flag_id),
        ]),
        ScriptBlock([
            IScript_IsState(11),
            IScript_IsTimer(timer),
        ], [
            FunctionData(17, [1 if is_slam_switch else 2, 1, 0]),
            FunctionData(14, [288, 0, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(11),
            IScript_IsTimer(timer_2),
        ], [
            FunctionData(16, [0, 0, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(11),
            IScript_IsTimer(0),
        ], [
            IScript_SetScriptRunState(RunState.pause),
        ]),
        ScriptBlock([
            IScript_IsState(20),
            IScript_InRange(200 if is_slam_switch else 100, True),
        ], [
            FunctionData(17, [1 if is_slam_switch else 2, 1, 0]),
            FunctionData(14, [288, 0, 0]),
            IScript_SetTimer(70 if is_slam_switch else 75),
            IScript_SetState(21),
        ]),
        ScriptBlock([
            IScript_IsState(21),
            IScript_IsTimer(0),
        ], [
            FunctionData(16, [0, 0, 0]),
            IScript_SetExternalState(tied_pad, 20 if is_slam_switch else 0),
            IScript_SetExternalScriptRunState(tied_pad, RunState.run),
            IScript_SetScriptRunState(RunState.pause),
        ]),
    ], flag_id)

def getFactoryBlastControllerScript(item_id) -> list[int]:
    """Get the instance script for the controller within Factory blast."""
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_True(),
        ], [
            FunctionData(7, [15, 0, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            FunctionData(45, [129, 1, 0], True),
            FunctionData(45, [130, 1, 0]),
        ], [
            FunctionData(88, [Maps.FranticFactory, 45, 10]),
            FunctionData(93, [0, 0, 0]),
            FunctionData(49, [Maps.FranticFactory, 15, 0x100]),
            IScript_SetState(1),
        ]),
    ])

def getKRoolShipScript(item_id: int) -> list[int]:
    """Get the instance script associated with the crashed ship."""
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsState(0),
        ], [
            IScript_SetOpacity(True, 0, 255),
            IScript_SetTangibility(False),
            FunctionData(71, [0, 0, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            FunctionData(6, [7, short_to_ushort(-9), 0]),
        ], [
            IScript_SetOpacity(True, 255, 255),
            IScript_SetTangibility(True),
            FunctionData(71, [1, 0, 0]),
            IScript_SetState(1),
        ]),
        ScriptBlock([
            IScript_IsState(1),
        ], [
            IScript_SetScriptRunState(RunState.pause),
            IScript_SetState(2),
        ]),
    ])

def getKRoolShipControllerScript(item_id: int, radius: int) -> list[int]:
    """Get the instance script associated with the controller object for a custom ship."""
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsState(0),
            FunctionData(6, [7, short_to_ushort(-9), 0]),
            IScript_InRange(radius),
        ], [
            FunctionData(7, [125, short_to_ushort(-10), 0]),
            IScript_SetState(1),
        ])
    ])

def getHelmLobbyActivatorScript(item_id: int, activator: SwitchsanityGone, bonus_map: int, microhint: bool) -> list[int]:
    """Get the instance script for the Helm Lobby activator if it is a lever."""
    # Gone
    return compileInstanceScript(item_id, [
        # Regive Gone upon exiting bonus
        ScriptBlock([
            FunctionData(50, [bonus_map, 0, 0]),
            IScript_IsState(0),
        ], [
            FunctionData(115, [65535, 0, 0]),
            IScript_SetAction(58),
            IScript_SetState(1, 1),
        ], lambda d: d["activator"] == SwitchsanityGone.gone_pad),
        # Gong Init
        ScriptBlock([
            IScript_IsState(0),
        ], [
            FunctionData(62, [1, 0, 0]),
            IScript_SetScriptRunState(RunState.distance, 400),
            FunctionData(39, [1, 0, 0]),
            FunctionData(39, [2, 0, 0]),
            FunctionData(39, [3, 0, 0]), 
            FunctionData(39, [4, 0, 0]), 
        ], lambda d: d["activator"] == SwitchsanityGone.gong),
        # Lever Init
        ScriptBlock([
            IScript_IsState(0),
        ], [
            FunctionData(24, [1, 1, 0]),
            FunctionData(39, [1, 0, 0]),
            FunctionData(62, [0, 0, 0]),
            FunctionData(20, [1, 85, 0]),
            FunctionData(22, [1, 1, 0]),
            FunctionData(40, [1, 0, 0]),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
        # Hide/Show pad with move
        ScriptBlock([
            IScript_IsState(0),
            IScript_HasSpecialMove(Kongs.chunky, 3, True, lambda d: d["activator"] == SwitchsanityGone.gone_pad),  # Doesn't have gone
            IScript_HasSpecialMove(Kongs.diddy, 1, True, lambda d: d["activator"] == SwitchsanityGone.gong),  # Doesn't have charge
            IScript_HasSpecialMove(Kongs.donkey, 3, True, lambda d: d["activator"] == SwitchsanityGone.lever),  # Doesn't have grab
            FunctionData(6, [7, short_to_ushort(-8), activator - SwitchsanityGone.bongos], True, lambda d: d["is_instrument"]),  # Doesn't have instrument
        ], [
            IScript_SetOpacity(True, 70, 255, lambda d: d["activator"] not in (SwitchsanityGone.gong, SwitchsanityGone.lever)),  # Make pad translucent
            FunctionData(7, [125, short_to_ushort(-4), 0]),
            IScript_SetState(5, 0, lambda d: d["microhint"]),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_HasSpecialMove(Kongs.chunky, 3, False, lambda d: d["activator"] == SwitchsanityGone.gone_pad),  # Has Gone
            IScript_HasSpecialMove(Kongs.diddy, 1, False, lambda d: d["activator"] == SwitchsanityGone.gong),  # Has charge
            IScript_HasSpecialMove(Kongs.donkey, 3, False, lambda d: d["activator"] == SwitchsanityGone.lever),  # Has grab
            FunctionData(6, [7, short_to_ushort(-8), activator - SwitchsanityGone.bongos], False, lambda d: d["is_instrument"]),  # Has Instrument
        ], [
            IScript_SetScriptRunState(RunState.distance, 300, lambda d: d["activator"] != SwitchsanityGone.gong),
            FunctionData(7, [125, short_to_ushort(-4), 0]),
            IScript_SetState(1),
        ]),
        # Activator script
        ScriptBlock([
            IScript_IsKongStandingOnObject(Kongs.chunky),
            IScript_HasSpecialMove(Kongs.chunky, 3),
        ], [
            FunctionData(73, [4, 65535, 0]),
        ], lambda d: d["activator"] == SwitchsanityGone.gone_pad),
        ScriptBlock([
            IScript_IsKongStandingOnObject(activator - SwitchsanityGone.bongos),
            FunctionData(6, [7, short_to_ushort(-8), activator - SwitchsanityGone.bongos]),
            IScript_InControlState(103),
        ], [
            IScript_SetScriptRunState(RunState.run),
            IScript_SetState(7),
        ], lambda d: d["is_instrument"]),
        ScriptBlock([
            IScript_IsState(1),
            FunctionData(24, [3, 1, 0]),
            IScript_InControlStateAndProgress(46, 1),
        ], [
            FunctionData(20, [1, 200, 0]),
            FunctionData(26, [1, 0, 0]),
            FunctionData(17, [1, 1, 0]),
            IScript_SetTimer(50),
            FunctionData(39, [1, 1, 0]),
            FunctionData(39, [2, 1, 0]),
            FunctionData(39, [3, 1, 0]),
            FunctionData(39, [4, 1, 0]),
            FunctionData(22, [1, 0, 0]),
            IScript_PlaySFX(165, 0, 95, 60, 5),
            IScript_SetScriptRunState(RunState.run),
            IScript_SetState(8),
        ], lambda d: d["activator"] == SwitchsanityGone.gong),
        ScriptBlock([
            IScript_IsState(1),
            FunctionData(18, [2, 2, 0]),
            FunctionData(6, [3, 0, 0]),
            IScript_HasSpecialMove(Kongs.donkey, 3),
        ], [
            FunctionData(120, [1, 0, 0]),
            FunctionData(73, [8, 0, 0]),
            IScript_SetState(1, 1),
            IScript_SetTimer(5),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
        ScriptBlock([
            IScript_IsState(1, 1),
            FunctionData(4, [0, 0, 0]),
        ], [
            IScript_SetState(0, 1),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
        ScriptBlock([
            IScript_IsState(1, 1),
            IScript_IsTimer(0, 0, True),
            IScript_InControlState(120),
        ], [
            IScript_SetScriptRunState(RunState.run),
            IScript_SetState(0, 1),
            IScript_SetState(9),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
        # Is gone active - Then progress to cutscene
        ScriptBlock([
            IScript_IsState(1),
            FunctionData(38, [0, 64, 0]),
        ], [
            IScript_SetTimer(15),
            IScript_SetState(2),
        ], lambda d: d["activator"] == SwitchsanityGone.gone_pad),
        ScriptBlock([
            IScript_IsState(2),
            IScript_IsTimer(0),
            IScript_IsState(0, 1),
        ], [
            IScript_PlayCutscene(1),
            IScript_SetTimer(200),
            IScript_SetState(1, 1),
            IScript_SetState(3),
        ]),
        ScriptBlock([
            IScript_IsState(2),
            IScript_IsTimer(0),
            IScript_IsState(1, 1),
        ], [
            IScript_SetTimer(20),
            IScript_SetState(3),
        ]),
        ScriptBlock([
            IScript_IsState(3),
            IScript_IsTimer(0),
        ], [
            IScript_SetState(4),
        ]),
        # Hide the gong
        ScriptBlock([
            IScript_IsState(4),
            FunctionData(21, [2, 0, 0], True),
        ], [
            FunctionData(16, [0, 0, 0]),
            IScript_SetOpacity(True, 0, 255),
            IScript_SetTangibility(False),
            IScript_SetScriptRunState(RunState.pause),
        ], lambda d: d["activator"] == SwitchsanityGone.gong),
        # Microhint
        ScriptBlock([
            IScript_IsState(5),
            IScript_HasSpecialMove(Kongs.chunky, 3, False, lambda d: d["activator"] == SwitchsanityGone.gone_pad),  # Has Gone
            IScript_HasSpecialMove(Kongs.diddy, 1, False, lambda d: d["activator"] == SwitchsanityGone.gong),  # Has charge
            IScript_HasSpecialMove(Kongs.donkey, 3, False, lambda d: d["activator"] == SwitchsanityGone.lever),  # Has grab
            FunctionData(6, [7, short_to_ushort(-8), activator - SwitchsanityGone.bongos], False, lambda d: d["is_instrument"]),  # Has Instrument
        ], [
            IScript_SetOpacity(True, 255, 255),
            IScript_SetScriptRunState(RunState.distance, 300),
            IScript_SetState(1),
        ]),
        ScriptBlock([
            IScript_IsState(5),
            IScript_HasSpecialMove(Kongs.chunky, 3, True, lambda d: d["activator"] == SwitchsanityGone.gone_pad),  # Doesn't have Gone
            IScript_HasSpecialMove(Kongs.diddy, 1, True, lambda d: d["activator"] == SwitchsanityGone.gong),  # Doesn't have charge
            IScript_HasSpecialMove(Kongs.donkey, 3, True, lambda d: d["activator"] == SwitchsanityGone.lever),  # Doesn't have grab
            FunctionData(6, [7, short_to_ushort(-8), activator - SwitchsanityGone.bongos], True, lambda d: d["is_instrument"]),  # Doesn't have Instrument
            FunctionData(6, [7, short_to_ushort(-5), 0]),
            IScript_IsStandingOnObject(False, lambda d: d["activator"] != SwitchsanityGone.gong),  # Standing on object
            IScript_InRange(20, False, lambda d: d["activator"] == SwitchsanityGone.gong),  # Close to object
        ], [
            IScript_PlayCutscene(3),
            IScript_SetState(6),
        ]),
        ScriptBlock([
            IScript_IsState(6),
            IScript_IsStandingOnObject(True, lambda d: d["activator"] != SwitchsanityGone.gong),  # Not standing on object
            IScript_InRange(20, True, lambda d: d["activator"] == SwitchsanityGone.gong),  # Not close to object
            IScript_IsCutsceneActive(True),
        ], [
            IScript_SetState(5),
        ]),
        # Instrument Handler
        ScriptBlock([
            IScript_IsState(7),
            IScript_IsCutsceneActive(True),
        ], [
            FunctionData(7, [125, short_to_ushort(-6), 0]),
            IScript_SetTimer(15),
            IScript_SetState(2),
        ], lambda d: d["is_instrument"]),
        # Gong Handler
        ScriptBlock([
            IScript_IsState(8),
            IScript_IsTimer(10),
        ], [
            FunctionData(14, [282, 0, 12800]),
            FunctionData(20, [2, 3, 0]),
            FunctionData(17, [2, 1, 0]),
        ], lambda d: d["activator"] == SwitchsanityGone.gong),
        ScriptBlock([
            IScript_IsState(8),
            IScript_IsTimer(0),
        ], [
            FunctionData(39, [1, 0, 0]),
            FunctionData(39, [2, 0, 0]),
            FunctionData(39, [3, 0, 0]),
            FunctionData(39, [4, 0, 0]),
            FunctionData(7, [125, short_to_ushort(-6), 0]),
            IScript_SetState(2),
        ], lambda d: d["activator"] == SwitchsanityGone.gong),
        # Lever Handler
        ScriptBlock([
            IScript_IsState(9),
            FunctionData(51, [0, 114, 0]),
        ], [
            FunctionData(40, [1, 1, 0]),
            FunctionData(17, [1, 1, 0]),
            IScript_PlaySFX(459),
            IScript_SetState(10),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
        ScriptBlock([
            IScript_IsState(10),
            FunctionData(51, [0, 155, 0]),
        ], [
            FunctionData(7, [125, short_to_ushort(-6), 0]),
            IScript_SetState(2),
        ], lambda d: d["activator"] == SwitchsanityGone.lever),
    ], {
        "activator": activator,
        "is_instrument": activator >= SwitchsanityGone.bongos and activator <= SwitchsanityGone.triangle,
        "microhint": microhint
    })


def getObjectHideScript(item_id: int) -> list[int]:
    """Get the instance script associated with instantly hiding an object."""
    return compileInstanceScript(
        item_id,
        [
            ScriptBlock(
                [],
                [
                    IScript_SetOpacity(True, 0, 255),
                    IScript_SetTangibility(False),
                    FunctionData(71, [0, 0, 0]),
                    IScript_SetScriptRunState(RunState.pause),
                ],
            ),
        ],
    )


def getWrinklyScript(map_id: Maps, kong: Kongs, item_id: int) -> list[int]:
    """Get the instance script associated with a wrinkly door."""
    level_id = getLevel(map_id, "wrinkly", False)
    view_flag = 0x384 + (level_id * 5) + kong
    return compileInstanceScript(
        item_id,
        [
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(39, [1, 0, 0]),
                    FunctionData(39, [2, 0, 0]),
                    FunctionData(40, [1, 1, 0]),
                    FunctionData(40, [2, 1, 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                ],
                [
                    FunctionData(22, [1, 1, 0]),
                    FunctionData(20, [1, 10, 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    FunctionData(6, [7, short_to_ushort(-7), 0], True),
                ],
                [
                    IScript_SetState(20),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    FunctionData(6, [7, short_to_ushort(-7), 0]),
                    IScript_IsFlagSet(view_flag),
                ],
                [
                    FunctionData(40, [1, 2, 0]),
                    FunctionData(40, [2, 2, 0]),
                    IScript_SetState(1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(0),
                    FunctionData(6, [7, short_to_ushort(-7), 0]),
                    IScript_IsFlagSet(view_flag, FlagType.permanent, True),
                ],
                [
                    FunctionData(40, [1, 0, 0]),
                    FunctionData(40, [2, 0, 0]),
                    IScript_SetState(1),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InRange(40),
                    FunctionData(6, [18, 0, 0]),
                ],
                [
                    FunctionData(17, [1, 1, 0]),
                    FunctionData(7, [105, kong, 0]),
                    IScript_PlaySFX(19, pitch_variance=20),
                    IScript_SetState(2),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(1),
                    IScript_InRange(40),
                    FunctionData(6, [18, 0, 0]),
                ],
                [
                    FunctionData(7, [125, short_to_ushort(-16), 1]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(2),
                    FunctionData(6, [12, 0, 0]),
                ],
                [
                    FunctionData(17, [1, 1, 0]),
                    IScript_PlaySFX(19, pitch_variance=20),
                    IScript_SetState(3),
                    FunctionData(7, [125, short_to_ushort(-16), 0]),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(3),
                    FunctionData(21, [1, 0, 0], True),
                ],
                [
                    IScript_PlaySFX(50, volume_unk_mult=60),
                    IScript_SetState(4),
                ],
            ),
            ScriptBlock(
                [
                    IScript_IsState(4),
                    IScript_InRange(60, True),
                ],
                [
                    IScript_SetState(1),
                ],
            ),
        ],
    )


def getHelmPadScript(item_id: int, temp_flags: list, kong_id: Kongs, glass_panel: int, hint_cs: int, helm_micro_enabled: bool, req_helm_minigames: int, helm_order: list) -> list[int]:
    """Get the instance script for the Helm music pads."""
    helm_order = helm_order.copy()
    if len(helm_order) < 5:
        delta = 5 - len(helm_order)
        for _ in range(delta):
            helm_order.append(None)
    slots = {
        Kongs.donkey: 0,
        Kongs.chunky: 1,
        Kongs.tiny: 2,
        Kongs.lanky: 3,
        Kongs.diddy: 4,
    }
    power_beams = [11, 8, 12, 10, 9]
    power_beams_0 = [16, 14, 13, 15, 17]
    power_beams_1 = [30, 32, 34, 36, 38]
    current_slot = None
    next_slot = None
    previous_slot = None
    for x in range(5):
        if helm_order[x] == slots[kong_id]:
            current_slot = x
            if x > 0:
                previous_slot = helm_order[x - 1]
            if x < 4:
                next_slot = helm_order[x + 1]
    in_helm_sequence = slots[kong_id] in helm_order
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsFlagSet(temp_flags[0], FlagType.temporary),
            IScript_IsFlagSet(temp_flags[1], FlagType.temporary),
            IScript_IsFlagSet(temp_flags[2], FlagType.temporary, True),
        ], [
            # Turn off power beams instantly - fixes the 2f quirk of cs skips
            IScript_SetExternalState(power_beams[slots[kong_id]], 10),
            IScript_SetExternalState(power_beams_0[slots[kong_id]], 10),
            IScript_SetExternalState(power_beams_1[slots[kong_id]], 10),
            # Helm Complete stuff
            IScript_PlayCutscene(8, 1, 0, lambda m: m["next_slot"] is None and m["current_slot"] is not None),  # Play CS
            IScript_SetFlag(0x302, FlagType.permanent, True, lambda m: m["next_slot"] is None and m["current_slot"] is not None),  # Turn off BoM
            IScript_SetFlag(0x50, FlagType.temporary, True, lambda m: m["next_slot"] is None and m["current_slot"] is not None),  # Helm temp flag
            # Go to next stuff
            IScript_PlayCutscene(8 if current_slot is None else 4 + current_slot, 1, 0, lambda m: m["next_slot"] is not None),  # Play CS
            IScript_SetFlag(temp_flags[2], FlagType.temporary, True),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            FunctionData(6, [7, short_to_ushort(-8), kong_id], True),  # Does not have instrument
        ], [
            IScript_SetState(20),
        ], inclusion_lambda=lambda m: m["micro"]),
        ScriptBlock([
            IScript_IsState(0),
        ], [
            FunctionData(116, [2, 0, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_IsFlagSet(770),
        ], [
            IScript_SetOpacity(False, 0, 20),
            IScript_SetScriptRunState(RunState.distance, 500),
            IScript_SetState(11),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_IsFlagSet(0 if previous_slot is None else 0x4B + previous_slot, FlagType.temporary, False, lambda m: m["previous_slot"] is not None),
        ], [
            IScript_SetOpacity(False, 0, 20),
            IScript_SetScriptRunState(RunState.distance, 500),
            IScript_SetState(11),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_IsFlagSet(0 if previous_slot is None else 0x4B + previous_slot, FlagType.temporary, True),
            IScript_IsFlagSet(770, FlagType.permanent, True),
        ], [
            IScript_SetScriptRunState(RunState.distance, 300),
            IScript_SetOpacity(True, 0, 255),
            FunctionData(71, [0, 0, 0]),
            FunctionData(1 if kong_id == Kongs.diddy else 38, [99 if kong_id == Kongs.diddy else 2, 0, 0]),  # Diddy has a separate call for this?
        ], lambda m: m["previous_slot"] is not None),
        ScriptBlock([
            IScript_IsState(10),
        ], [
            IScript_SetOpacity(False, 0, 20),
            FunctionData(71, [1, 0, 0]),
            IScript_SetState(11),
        ]),
        ScriptBlock([
            IScript_IsState(11),
            FunctionData(6, [7, short_to_ushort(-8), kong_id], True),  # Does not have instrument
        ], [
            IScript_SetState(20),
        ], inclusion_lambda=lambda m: m["micro"]),
        ScriptBlock([
            IScript_IsState(11),
            FunctionData(13, [2, 0, 0]),
            IScript_IsKong(kong_id),
            IScript_InControlState(103),
        ], [
            IScript_SetState(12),
        ]),
        ScriptBlock([
            IScript_IsState(12),
            IScript_IsCutsceneActive(True),
        ], [
            # Set minigame flags
            IScript_SetFlag(temp_flags[0], FlagType.temporary),
            IScript_SetFlag(temp_flags[1], FlagType.temporary),
            IScript_PlayCutscene(9 + (item_id - 0x2C), 1, 0, inclusion_lambda=lambda m: not m["in_helm_sequence"]),
        ], inclusion_lambda=lambda m: m["minis"] == 0),
        ScriptBlock([
            IScript_IsState(12),
            IScript_IsCutsceneActive(True),
        ], [
            IScript_PlayCutscene(9 + (item_id - 0x2C), 1, 0, inclusion_lambda=lambda m: m["minis"] > 0),
            IScript_SetExternalScriptRunState(glass_panel, RunState.run),
            IScript_SetExternalState(glass_panel, 10),
            IScript_SetState(13),
        ]),
        ScriptBlock([
            IScript_IsState(13),
            IScript_IsCutsceneActive(True),
        ], [
            IScript_SetState(11),
        ]),
        ScriptBlock([
            IScript_IsState(20),
            FunctionData(6, [7, short_to_ushort(-8), kong_id]),  # Has instrument
        ], [
            IScript_SetState(0),
        ], inclusion_lambda=lambda m: m["micro"]),
        ScriptBlock([
            IScript_IsState(20),
            IScript_IsStandingOnObject(),
        ], [
            IScript_PlayCutscene(hint_cs),
            IScript_SetState(21),
        ], inclusion_lambda=lambda m: m["micro"]),
        ScriptBlock([
            IScript_IsState(21),
            IScript_IsStandingOnObject(True),
            IScript_IsCutsceneActive(True),
        ], [
            IScript_SetState(20),
        ], inclusion_lambda=lambda m: m["micro"]),
    ], {
        "micro": helm_micro_enabled,
        "minis": req_helm_minigames,
        "in_helm_sequence": in_helm_sequence,
        "previous_slot": previous_slot,
        "next_slot": next_slot,
        "current_slot": current_slot,
    })

def getHelmMonkeyport(item_id: int, kong: Kongs, microhint: bool):
    """Get the script associated with getting to the top of Krem Isle."""
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsState(0),
            IScript_HasSpecialMove(Kongs.tiny, 3, True, lambda d: d["kong"] == Kongs.tiny),  # Doesn't have mport
            IScript_HasSpecialMove(Kongs.donkey, 1, True, lambda d: d["kong"] == Kongs.donkey),  # Doesn't have blast
            IScript_HasSpecialMove(Kongs.lanky, 2, True, lambda d: d["kong"] == Kongs.lanky),  # Doesn't have balloon
        ], [
            IScript_SetOpacity(True, 70, 255),
            IScript_SetState(5, 0, lambda d: d["microhint"]),
        ]),
        ScriptBlock([
            IScript_IsState(0),
            IScript_HasSpecialMove(Kongs.tiny, 3, False, lambda d: d["kong"] == Kongs.tiny),  # Has mport
            IScript_HasSpecialMove(Kongs.donkey, 1, False, lambda d: d["kong"] == Kongs.donkey),  # Has blast
            IScript_HasSpecialMove(Kongs.lanky, 2, False, lambda d: d["kong"] == Kongs.lanky),  # Has balloon
        ], [
            IScript_SetOpacity(True, 255, 255),
            IScript_SetScriptRunState(RunState.distance, 300),
            IScript_SetState(1),
        ]),
        ScriptBlock([
            IScript_IsState(1),
            IScript_IsKongStandingOnObject(kong),
        ], [
            IScript_SetExternalState(55, 20, 0, lambda d: d["kong"] == Kongs.tiny),  # Activate other pad (mport)
            IScript_SetExternalScriptRunState(55, RunState.run, 0, lambda d: d["kong"] == Kongs.tiny),  # Activate other pad (mport)
            FunctionData(73, [0, Maps.Isles, 0], False, lambda d: d["kong"] == Kongs.donkey),  # Activate blast pad (dk)
            FunctionData(73, [6, 15, 0], False, lambda d: d["kong"] == Kongs.lanky),  # Activate balloon (lanky)
        ]),
        ScriptBlock([
            IScript_IsState(20),
        ], [
            FunctionData(73, [3, 0, 0]),
            IScript_SetState(0),
        ], lambda d: d["kong"] == Kongs.tiny),
        # Microhint handling
        ScriptBlock([
            IScript_IsState(5),
            IScript_HasSpecialMove(Kongs.tiny, 3, True, lambda d: d["kong"] == Kongs.tiny),  # Doesn't have mport
            IScript_HasSpecialMove(Kongs.donkey, 1, True, lambda d: d["kong"] == Kongs.donkey),  # Doesn't have blast
            IScript_HasSpecialMove(Kongs.lanky, 2, True, lambda d: d["kong"] == Kongs.lanky),  # Doesn't have balloon
            FunctionData(6, [7, short_to_ushort(-11), 7]),  # Can open 7 B Lockers
            IScript_IsStandingOnObject(),  # Standing on object
        ], [
            IScript_PlayCutscene(24),  # Play CS
            IScript_SetState(6),
        ], lambda d: d["microhint"]),
        ScriptBlock([
            IScript_IsState(5),
            IScript_HasSpecialMove(Kongs.tiny, 3, False, lambda d: d["kong"] == Kongs.tiny),  # Has mport
            IScript_HasSpecialMove(Kongs.donkey, 1, False, lambda d: d["kong"] == Kongs.donkey),  # Has blast
            IScript_HasSpecialMove(Kongs.lanky, 2, False, lambda d: d["kong"] == Kongs.lanky),  # Has balloon
        ], [
            IScript_SetState(0),
        ], lambda d: d["microhint"]),
        ScriptBlock([
            IScript_IsState(6),
            IScript_IsStandingOnObject(True),  # Not standing on object
            IScript_IsCutsceneActive(True),  # CS not playing
        ], [
            IScript_SetState(5),
        ], lambda d: d["microhint"]),
    ], {
        "kong": kong,
        "microhint": microhint
    })

def getPianoScript(item_id: int, piano_order: list[int], fast_piano: bool):
    # A = 0, B = 1, C = 2, D = 3, E = 4, F = 5
    cutscenes = {
        # Key: Seq Length
        3: {
            "cutscene_index": 16,
            "delta": 60,
            "length": 160,
        },
        4: {
            "cutscene_index": 17,
            "delta": 20,
            "length": 140,
        },
        5: {
            "cutscene_index": 18,
            "delta": 20,
            "length": 170,
        },
        6: {
            "cutscene_index": 19,
            "delta": 20,
            "length": 200,
        },
        7: {
            "cutscene_index": 20,
            "delta": 20,
            "length": 230,
        },
    }
    script = [
        # Starting section
        ScriptBlock([
            IScript_IsState(0),
        ], [
            FunctionData(22, [1, 1, 0]),
            FunctionData(22, [2, 1, 0]),
            FunctionData(22, [3, 1, 0]),
            FunctionData(22, [4, 1, 0]),
            FunctionData(22, [5, 1, 0]),
            FunctionData(22, [6, 1, 0]),
            IScript_SetScriptRunState(RunState.pause),
        ]),
    ]
    state_start = 10
    failure_state = 250
    for x in range(5):  # 5 repetitions of the sequence
        if fast_piano and x in (1, 3):
            continue
        sequence_count = 3 + x
        local_sequence = piano_order[:sequence_count]
        delta = cutscenes[sequence_count]["delta"]
        timer_total = cutscenes[sequence_count]["length"]
        # Timer setup
        burp_state = state_start
        script.append(
            ScriptBlock([
                IScript_IsState(state_start),
                IScript_IsTimer(0),
            ], [
                IScript_PlayCutscene(cutscenes[sequence_count]["cutscene_index"]),
                IScript_SetTimer(timer_total),
                IScript_SetState(state_start + 1),
            ])
        )
        for y in range(sequence_count):
            # Play Kremling
            script.append(
                ScriptBlock([
                    IScript_IsState(state_start + 1),
                    IScript_IsTimer(timer_total - (delta + (30 * y))),
                ], [
                    FunctionData(94, [local_sequence[y] + 5, 0, 0]),  # Spawn Kremling
                ]),
            )
        script.append(
            ScriptBlock([
                IScript_IsState(state_start + 1),
                IScript_IsTimer(0),
            ], [
                IScript_SetState(state_start + 2),
            ]),
        )
        state_start += 2
        for y in range(sequence_count):
            successful_kremling = [
                FunctionData(94, [local_sequence[y] + 5, 0, 0]),  # Spawn Kremling
                IScript_SetTimer(50),
                FunctionData(17, [local_sequence[y] + 1, 2, 0]),
                IScript_SetState(state_start + 2),
            ]
            if y == (sequence_count - 1):
                successful_kremling.append(
                    IScript_PlaySFX(673),  # Play Ding
                )
            script.extend([
                ScriptBlock([
                    IScript_IsState(state_start),
                    IScript_IsTimer(0),
                ], [
                    IScript_SetState(state_start + 1),
                ]),
                ScriptBlock([
                    IScript_IsState(state_start),
                    IScript_IsStandingOnObject(True),  # Not on piano
                ], [
                    IScript_SetTimer(0),  # Set timer to 0
                    IScript_SetState(state_start + 1),
                ]),
                ScriptBlock([
                    IScript_IsState(state_start + 1),
                    FunctionData(13, [local_sequence[y] + 1, 0, 0]),  # Is pressing right key
                    IScript_InControlState(28),  # Is slamming
                ], successful_kremling),
                ScriptBlock([
                    IScript_IsState(state_start + 1),
                    IScript_InControlState(28),  # Is slamming
                    FunctionData(6, [1, local_sequence[y] + 1, 0]),  # Is pressing wrong key
                ], [
                    IScript_SetState(burp_state),
                    IScript_SetTimer(50),
                    IScript_PlaySFX(0x98),  # Error Sound
                ]),
            ])
            state_start += 2
    script.extend([
        ScriptBlock([
            IScript_IsState(state_start),
            IScript_IsTimer(20),
        ], [
            IScript_SetExternalState(62, 10),
            IScript_SetExternalScriptRunState(62, RunState.run),
        ]),
        ScriptBlock([
            IScript_IsState(state_start),
            IScript_IsTimer(0),
        ], [
            IScript_SetScriptRunState(RunState.pause),
        ]),
        ScriptBlock([
            IScript_IsState(failure_state),
        ], [
            IScript_SetTimer(10),
            IScript_SetState(failure_state + 1),
        ]),
        ScriptBlock([
            IScript_IsState(failure_state + 1),
            IScript_IsTimer(0),
        ], [
            IScript_PlaySong(Songs.Failure),
            IScript_SetTimer(90),
            IScript_SetState(failure_state + 2),
        ]),
        ScriptBlock([
            IScript_IsState(failure_state + 2),
            IScript_IsTimer(0),
        ], [
            IScript_SetExternalState(61, 10),
            IScript_SetExternalScriptRunState(61, RunState.run),
            IScript_SetScriptRunState(RunState.pause),
        ]),
    ])
    return compileInstanceScript(item_id, script)

def getDiddyRNDDoorScript(item_id: int, fast_rnd: bool, cutscene_id: int, pen_id: int, enemy_ids: list[int]) -> list[int]:
    """Get the script associated with the Diddy R&D Doors."""
    door_ids = [63, 64, 65]
    remaining_door_ids = [x for x in door_ids if x != item_id]
    
    return compileInstanceScript(item_id, [
        ScriptBlock([
            FunctionData(29, [1, 0, 0]),
            FunctionData(29, [0, 5, 0]),
        ], [
            IScript_SetState(0),
        ]),
        ScriptBlock([
            IScript_IsState(1),
            FunctionData(58, [0, 0, 0], True),
        ], [
            FunctionData(7, [67, 1, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(2),
            FunctionData(58, [0, 0, 0], True),
        ], [
            FunctionData(7, [67, 2, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(3),
            FunctionData(58, [0, 0, 0], True),
        ], [
            FunctionData(7, [67, 3, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(4),
            FunctionData(58, [0, 0, 0], True),
        ], [
            FunctionData(7, [67, 4, 0]),
        ]),
        ScriptBlock([
            IScript_IsState(5),
            IScript_IsExternalState(96, 0),
        ], [
            IScript_SetState(6),
        ]),
        ScriptBlock([
            IScript_IsState(5),
            IScript_IsExternalState(96, 1),
        ], [
            IScript_SetState(6),
        ]),
        ScriptBlock([
            IScript_IsState(5),
            IScript_IsExternalState(96, 2),
        ], [
            IScript_SetState(6),
        ]),
        ScriptBlock([
            IScript_IsState(6),
        ], [
            FunctionData(129, [0, 0, 0]),
            IScript_SetExternalState(remaining_door_ids[0], 50),
            IScript_SetExternalState(remaining_door_ids[1], 50),
            IScript_SetScriptRunState(RunState.run),
            IScript_SetTimer(120),
            IScript_SetState(7),
        ]),
        ScriptBlock([
            IScript_IsState(7),
            IScript_IsTimer(100),
        ], [
            IScript_PlayCutscene(cutscene_id),
        ]),
        ScriptBlock([
            IScript_IsState(7),
            IScript_IsTimer(90),
        ], [
            IScript_SetExternalState(319, 10),
            IScript_SetExternalScriptRunState(319, RunState.run),
        ]),
        ScriptBlock([
            IScript_IsState(7),
            IScript_IsTimer(0),
        ], [
            IScript_SetState(8),
        ]),
        ScriptBlock([
            IScript_IsState(8),
        ], [
            FunctionData(22, [1, 1, 0]),
            FunctionData(20, [1, 20, 0]),
            FunctionData(17, [1, 1, 0]),
            IScript_SetTimer(100),
            IScript_PlaySFX(385, pitch_variance=20),
            FunctionData(92, [pen_id, 0, 1]),
            IScript_SetState(9),
        ]),
        ScriptBlock([
            IScript_IsState(9),
            IScript_IsTimer(90),
        ], [IScript_SpawnEnemy(x) for x in enemy_ids] + [
            IScript_PlaySong(Songs.MiniBoss),
        ]),
        ScriptBlock([
            IScript_IsState(9),
            IScript_IsTimer(0),
        ], [
            IScript_PlaySFX(415, pitch_variance=20),
            FunctionData(17, [1, 1, 0]),
            IScript_SetState(10),
        ]),
        ScriptBlock([
            IScript_IsState(10),
            FunctionData(21, [1, 0, 0], True),
        ], [
            FunctionData(92, [pen_id, 0, 0]),
            IScript_PlaySFX(151, pitch_variance=20),
            IScript_SetScriptRunState(RunState.init),
            IScript_SetState(11),
        ]),
        ScriptBlock([
            IScript_IsState(11),
        ] + [FunctionData(30, [x, 0, 0], True) for x in enemy_ids], [
            FunctionData(130, [0, 0, 0]),
            FunctionData(111, [104, 0, 0]),
            IScript_SetExternalState(319, 20),
            IScript_SetExternalScriptRunState(319, RunState.run),
            FunctionData(28, [96, 0, 3 if fast_rnd else 1]),
            IScript_SetExternalScriptRunState(96, RunState.run),
            FunctionData(83, [49, 0, 0]),
        ] + [
            IScript_SetExternalScriptRunState(x, RunState.pause, 0, lambda d: d["fast"])  # Disable other doors
            for x in remaining_door_ids
        ] + [
            IScript_SetScriptRunState(RunState.pause),  # Disable this door
        ]),
        ScriptBlock([
            IScript_IsState(50),
        ], [
            FunctionData(7, [67, 65535, 0]),
            IScript_SetState(51),
        ]),
    ], {
        "fast": fast_rnd
    })

def getIntangibleObjectPreview(item_id) -> list[int]:
    """Get the instance script associated with intangible item previews."""
    return compileInstanceScript(item_id, [
        ScriptBlock([
            IScript_IsState(0),
        ], [
            IScript_SetTangibility(False),
            IScript_SetOpacity(True, 255, 255),
            IScript_SetState(1),
        ]),
    ])

def replaceScriptLines(ROM_COPY: LocalROM, cont_map_id: int, item_ids: list[int], replacement_mapping: dict) -> None:
    """Replace a script line with another."""
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    # Construct good pre-existing scripts
    file_offset = 2
    for _ in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for _ in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2
            for _ in range(cond_count):
                func = int.from_bytes(ROM_COPY.readBytes(2), "big")
                params = []
                for _ in range(3):
                    params.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                if script_id in item_ids:
                    constructed = f"{'CONDINV' if func & 0x8000 else 'COND'} {func & 0x7FFF} | {params[0]} {params[1]} {params[2]}"
                    if constructed in replacement_mapping:
                        new_output = replacement_mapping[constructed]
                        segs = new_output.split(" ")
                        func = 0x8000 if "CONDINV" in new_output else 0
                        func |= int(segs[1])
                        params = [
                            int(segs[3]),
                            int(segs[4]),
                            int(segs[5]),
                        ]
                        ROM_COPY.seek(script_table + file_offset)
                        ROM_COPY.writeMultipleBytes(func, 2)
                        for p in params:
                            ROM_COPY.writeMultipleBytes(p, 2)
                file_offset += 8
            ROM_COPY.seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2
            for _ in range(exec_count):
                func = int.from_bytes(ROM_COPY.readBytes(2), "big")
                params = []
                for _ in range(3):
                    params.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                if script_id in item_ids:
                    constructed = f"EXEC {func} | {params[0]} {params[1]} {params[2]}"
                    if constructed in replacement_mapping:
                        new_output = replacement_mapping[constructed]
                        segs = new_output.split(" ")
                        func = int(segs[1])
                        params = [
                            int(segs[3]),
                            int(segs[4]),
                            int(segs[5]),
                        ]
                        ROM_COPY.seek(script_table + file_offset)
                        ROM_COPY.writeMultipleBytes(func, 2)
                        for p in params:
                            ROM_COPY.writeMultipleBytes(p, 2)
                file_offset += 8


def addNewScript(ROM_COPY: LocalROM, cont_map_id: int, item_ids: list[int], stype: ScriptTypes, extra_data: dict = {}) -> None:
    """Append a new script to the script database. Has to be just 1 execution and 1 endblock."""
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for _ in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for _ in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            ROM_COPY.seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id not in item_ids:
            script_data = []
            ROM_COPY.seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            good_scripts.append(script_data)
    # Get new script data
    for item_id in item_ids:
        subscript = None
        if stype == ScriptTypes.Bananaport:
            subscript = getCScript(-1, item_id)
        elif stype == ScriptTypes.Wrinkly:
            subscript = getWrinklyScript(cont_map_id, extra_data[item_id]["kong_id"], item_id)
        elif stype == ScriptTypes.TnsPortal:
            subscript = getTroffPortalScript(cont_map_id, item_id, extra_data[item_id]["exit_id"])
        elif stype in (ScriptTypes.CrownMain, ScriptTypes.CrownIsles2):
            subscript = getCrownScript(cont_map_id, item_id, stype == ScriptTypes.CrownIsles2)
        elif stype == ScriptTypes.MelonCrate:
            subscript = getCrateScript(item_id)
        elif stype == ScriptTypes.DeleteItem:
            subscript = getObjectHideScript(item_id)
        elif stype == ScriptTypes.HelmLobbyPadGrab:
            subscript = getHelmLobbyActivatorScript(item_id, extra_data["activator"], extra_data["bonus_map"], extra_data["microhint"])
        elif stype == ScriptTypes.GalleonShipwreckDoor:
            subscript = getFiveTwoDoorShipGateScript(item_id, extra_data[item_id]["flag_id"], extra_data[item_id]["timer"], extra_data[item_id]["timer_2"], extra_data[item_id]["tied_pad"])
        elif stype == ScriptTypes.FactoryBlastController:
            subscript = getFactoryBlastControllerScript(item_id)
        elif stype == ScriptTypes.KRoolShip:
            subscript = getKRoolShipScript(item_id)
        elif stype == ScriptTypes.KRoolShipController:
            subscript = getKRoolShipControllerScript(item_id, extra_data[item_id]["radius"])
        elif stype == ScriptTypes.HelmInstrumentPad:
            subscript = getHelmPadScript(item_id, extra_data[item_id]["temp_flags"], extra_data[item_id]["kong_id"], extra_data[item_id]["glass_panel"], extra_data[item_id]["hint_cs"], extra_data[item_id]["microhint"], extra_data[item_id]["req_minigames"], extra_data[item_id]["helm_order"])
        elif stype == ScriptTypes.KrocIslePort:
            subscript = getHelmMonkeyport(item_id, extra_data["kong"], extra_data["microhint"])
        elif stype == ScriptTypes.Piano:
            subscript = getPianoScript(item_id, extra_data["piano_order"], extra_data["fast_piano"])
        elif stype == ScriptTypes.DiddyRNDDoors:
            subscript = getDiddyRNDDoorScript(item_id, extra_data[item_id]["fast_rnd"], extra_data[item_id]["cutscene_id"], extra_data[item_id]["pen_id"], extra_data[item_id]["enemy_ids"])
        elif stype == ScriptTypes.IntangibleObject:
            subscript = getIntangibleObjectPreview(item_id)
        if subscript is not None:
            good_scripts.append(subscript)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)


slammable_switches = {
    Maps.JungleJapes: [0x1A, 0x40, 0x41, 0x3F, 0x3E, 0x3D],
    Maps.JapesMountain: [0xB, 0xA, 0x6],
    Maps.JapesTinyHive: [0x2, 0x3],
    Maps.AngryAztec: [0x28],
    Maps.AztecLlamaTemple: [0x69, 0x29, 0xE, 0xF, 0x10],
    Maps.AztecTinyTemple: [0x0, 0x1A],
    Maps.FranticFactory: [0x79, 0x31, 0x7A, 0x24, 0x30, 0x3D, 0x2F, 0x80, 0x2E, 0x61],
    Maps.GloomyGalleon: [0x2A, 0x1D, 0x1C, 0x27],
    Maps.GloomyGalleonLobby: [0xA],
    Maps.FungiForest: [0xEC, 0x10, 0xF, 0xEB],
    Maps.ForestThornvineBarn: [0x0],
    Maps.ForestMillFront: [0x1, 0x2],
    Maps.ForestGiantMushroom: [0x1, 0x0],
    Maps.ForestMillAttic: [0x0],
    Maps.ForestChunkyFaceRoom: [0x1],
    Maps.CrystalCaves: [0xD, 0x144],
    Maps.CreepyCastle: [0x12, 0x17, 0x16, 0xF, 0x19],
    Maps.CastleDungeon: [0x5, 0x4, 0x6],
    Maps.CastleMausoleum: [0x4],
    Maps.CastleLibrary: [0x4],
}


def setProgSlamStrength(ROM_COPY: LocalROM, settings):
    """Update the instance scripts for all slam switches impacted by prog slam strength."""
    for map_id, obj_ids in slammable_switches.items():
        level_id = getLevel(map_id, "slam switches", False)
        slam_strength = settings.switch_allocation[level_id]
        if slam_strength > 0:
            for x in range(4):
                replaceScriptLines(
                    ROM_COPY,
                    map_id,
                    obj_ids,
                    {
                        f"COND 37 | {x} 0 0": f"COND 37 | {slam_strength} 0 0",
                    },
                )
        else:
            for x in range(4):
                replaceScriptLines(
                    ROM_COPY,
                    map_id,
                    obj_ids,
                    {
                        f"COND 37 | {x} 0 0": "COND 0 | 0 0 0",
                    },
                )
            replaceScriptLines(
                ROM_COPY,
                map_id,
                obj_ids,
                {
                    "COND 23 | 28 0 0": "COND 0 | 0 0 0",
                },
            )
