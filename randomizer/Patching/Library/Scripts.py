"""Instance Script library functions and classes."""

from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Patching.Library.DataTypes import short_to_ushort
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM

class FunctionData:
    """Function Data Class."""

    def __init__(
        self,
        function: int,
        parameters: list,
        inverted: bool = False,
        inclusion_lambda = None
    ):
        """Initialize with given parameters."""
        self.function = function
        self.parameters = parameters.copy()
        self.inverted = inverted
        self.include = inclusion_lambda
        if inclusion_lambda is None:
            self.include = lambda _: True

    def compile(self, allow_inversion: bool, val: int) -> list[int]:
        """Compile into a line for a script."""
        if not self.include(val):
            return []
        func = self.function
        if allow_inversion and self.inverted:
            func |= 0x8000
        if len(self.parameters) < 3:
            self.parameters = self.parameters + [0, 0, 0]
            self.parameters = self.parameters[:3]
        return [func] + self.parameters[:3]


class ScriptBlock:
    """Script Block Class."""

    def __init__(
        self,
        conditions: list[FunctionData],
        executions: list[FunctionData],
        inclusion_lambda = None
    ):
        """Initialize with given parameters."""
        self.conditions = conditions.copy()
        self.executions = executions.copy()
        self.include = inclusion_lambda
        if inclusion_lambda is None:
            self.include = lambda _: True

    def getActiveConditions(self, val: int):
        """Get the active conditions for a block."""
        return [x for x in self.conditions if x.include(val)]
    
    def getActiveExecutions(self, val: int):
        """Get the active executions for a block."""
        return [x for x in self.executions if x.include(val)]

    def compile(self, val: int) -> list[int]:
        """Compile into a block for a script."""
        active_conds = self.getActiveConditions(val)
        active_execs = self.getActiveExecutions(val)
        output_bin = [len(active_conds)]
        if len(active_conds) > 5:
            raise Exception("Too many conditions to compile script.")
        if len(active_execs) > 4:
            raise Exception("Too many executions to compile script.")
        for cond in active_conds:
            output_bin.extend(cond.compile(True, val))
        output_bin.append(len(active_execs))
        for exec in active_execs:
            output_bin.extend(exec.compile(False, val))
        return output_bin

def compileInstanceScript(item_id, script: list[ScriptBlock], val: int = None) -> list[int]:
    """Compile instance script into a binary format."""
    output_bin = [item_id, 0, 0]
    block_count = 0
    for block in script:
        if len(block.getActiveConditions(val)) > 0 or len(block.getActiveExecutions(val)) > 0:
            block_count += 1
            output_bin.extend(block.compile(val))
    output_bin[1] = block_count
    return output_bin

def getCScript(index: int, item_id: int):
    """Get the generic c script caller."""
    return compileInstanceScript(item_id, [
        ScriptBlock([], [
            FunctionData(7, [125, short_to_ushort(index), item_id])
        ])
    ])

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
    ]
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

def getTroffPortalScript(map_id: Maps, item_id: int) -> list[int]:
    """Get the instance script for a troff and scoff portal."""
    level_id: Levels = None
    boss_flag = level_key_flag_mapping[Levels.JungleJapes]
    portal_flag = level_portal_flag_mapping[Levels.JungleJapes]
    portal_range = 90
    exit_id = 3  # TODO: Configure this
    if map_id != Maps.TroffNScoff:
        portal_range = 60
        for lvl, map_ids in level_map_mapping.items():
            if map_id in map_ids:
                level_id = lvl
        if level_id is None:
            raise Exception("Invalid level for portal")
        portal_flag = level_portal_flag_mapping[level_id]
        boss_flag = level_key_flag_mapping[level_id]
    return compileInstanceScript(item_id, [
        ScriptBlock([
            FunctionData(1, [0, 0, 0]),
        ], [
            FunctionData(22, [1, 0, 0]),
            FunctionData(20, [1, 160, 0]),
            FunctionData(22, [3, 0, 0]),
            FunctionData(20, [3, 115, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [0, 0, 0]),
            FunctionData(45, [portal_flag, 0, 0]),
        ], [
            FunctionData(69, [1, 0, 255]),
            FunctionData(70, [0, 0, 0]),
            FunctionData(1, [20, 0, 0]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [0, 0, 0]),
            FunctionData(45, [boss_flag, 0, 0], True, lambda m: m != Maps.TroffNScoff),
        ], [
            FunctionData(17, [1, 65535, 0]),
            FunctionData(17, [3, 65535, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [0, 0, 0]),
            FunctionData(45, [portal_flag, 0, 0], True, lambda m: m != Maps.TroffNScoff),
        ], [
            FunctionData(3, [0, 45, 0]),
            FunctionData(1, [1, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [1, 0, 0]),
            FunctionData(19, [portal_range, 0, 0]),
            FunctionData(35, [0, 0, 0], True, lambda m: m == Maps.TroffNScoff),
        ], [
            FunctionData(3, [60, 0, 0], inclusion_lambda = lambda m: m != Maps.TroffNScoff),
            FunctionData(3, [0, 60, 0], inclusion_lambda = lambda m: m == Maps.TroffNScoff),
            FunctionData(7, [116, 0, 1]),
            FunctionData(110, [1, 0, 0]),
            FunctionData(37, [29, 0, 15]),
        ]),
        ScriptBlock([
            FunctionData(1, [1, 0, 0]),
            FunctionData(19, [portal_range, 0, 0]),
            FunctionData(35, [0, 0, 0], True, lambda m: m == Maps.TroffNScoff),
        ], [
            FunctionData(25, [90, 0, 0]),
            FunctionData(1, [100, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [100, 0, 0]),
            FunctionData(4, [0, 0, 0]),
            FunctionData(45, [boss_flag, 0, 0]),
        ], [
            FunctionData(3, [0, 60, 0]),
            FunctionData(107, [portal_flag, 1, 0]),
            FunctionData(1, [40, 0, 0]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [100, 0, 0]),
            FunctionData(4, [0, 0, 0]),
            FunctionData(45, [boss_flag, 0, 0], True, lambda m: m != Maps.TroffNScoff),
        ], [
            FunctionData(1, [2, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [40, 0, 0]),
            FunctionData(4, [0, 0, 0]),
        ], [
            FunctionData(69, [1, 0, 4]),
            FunctionData(70, [0, 0, 0]),
            FunctionData(15, [994, 20, 10]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [40, 0, 0]),
            FunctionData(4, [0, 0, 0]),
        ], [
            FunctionData(1, [41, 0, 0]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [41, 0, 0]),
            FunctionData(21, [2, 0, 0]),
        ], [
            FunctionData(7, [116, 0, 2]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [41, 0, 0]),
            FunctionData(21, [2, 0, 0], True),
        ], [
            FunctionData(1, [20, 0, 0]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [1, 0, 0]),
            FunctionData(19, [portal_range, 0, 0], True),
        ], [
            FunctionData(1, [2, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [1, 0, 0]),
            FunctionData(35, [0, 0, 0]),
        ],
        [
            FunctionData(1, [2, 0, 0]),
        ], lambda m: m == Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [2, 0, 0]),
            FunctionData(4, [0, 0, 0]),
        ], [
            FunctionData(90, [60, 60, 60]),
            FunctionData(61, [3, 0, 0]),
            FunctionData(1, [3, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [3, 0, 0]),
            FunctionData(45, [portal_flag, 0, 0]),
        ], [
            FunctionData(69, [1, 0, 255]),
            FunctionData(70, [0, 0, 0]),
            FunctionData(1, [20, 0, 0]),
        ], lambda m: m != Maps.TroffNScoff),
        ScriptBlock([
            FunctionData(1, [3, 0, 0]),
            FunctionData(16, [1, 1, 0]),
        ], [
            FunctionData(3, [0, 5, 0]),
            FunctionData(7, [116, 0, 0]),
            FunctionData(110, [1, 0, 0]),
            FunctionData(37, [28, 0, 15]),
        ]),
        ScriptBlock([
            FunctionData(1, [3, 0, 0]),
            FunctionData(16, [1, 1, 0]),
        ], [
            FunctionData(25, [89, 0, 0]),
            FunctionData(1, [4, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(1, [4, 0, 0]),
            FunctionData(4, [0, 0, 0]),
        ], [
            FunctionData(134, [short_to_ushort(exit_id), 0, 0], inclusion_lambda=lambda m: m != Maps.TroffNScoff),
            FunctionData(135, [0, 0, 0], inclusion_lambda=lambda m: m == Maps.TroffNScoff),
            FunctionData(1, [5, 0, 0]),
        ]),
        ScriptBlock([
            FunctionData(0, [0, 0, 0]),
        ], [
            FunctionData(7, [125, short_to_ushort(-3), item_id]),  # Must be last for item id appending
        ]),
    ], map_id)

def replaceScriptLines(ROM_COPY: LocalROM, cont_map_id: int, item_ids: list[int], replacement_mapping: dict) -> None:
    """Replace a script line with another."""
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2
            for cond in range(cond_count):
                func = int.from_bytes(ROM_COPY.readBytes(2), "big")
                params = []
                for _ in range(3):
                    params.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                if script_id in item_ids:
                    constructed = f"COND{'INV' if func & 0x8000 else ''} {func & 0x7FFF} | {params[0]} {params[1]} {params[2]}"
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
            for exec in range(exec_count):
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

def addNewScript(ROM_COPY: LocalROM, cont_map_id: int, item_ids: list[int], type: ScriptTypes) -> None:
    """Append a new script to the script database. Has to be just 1 execution and 1 endblock."""
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
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
        if type == ScriptTypes.Bananaport:
            subscript = getCScript(-1, item_id)
        elif type == ScriptTypes.Wrinkly:
            subscript = getCScript(-2, item_id)
        elif type == ScriptTypes.TnsPortal:
            subscript = getTroffPortalScript(cont_map_id, item_id)
        elif type == ScriptTypes.CrownMain:
            subscript = getCScript(-5, item_id)
        elif type == ScriptTypes.CrownIsles2:
            subscript = getCScript(-6, item_id)
        elif type == ScriptTypes.MelonCrate:
            subscript = getCScript(-13, item_id)
        elif type == ScriptTypes.DeleteItem:
            subscript = getCScript(-16, item_id)
        if subscript is not None:
            good_scripts.append(subscript)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)