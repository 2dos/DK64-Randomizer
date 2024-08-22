"""Global classes for the build process."""

import subprocess
from typing import BinaryIO
import zlib
import math

import encoders
from BuildEnums import ChangeType, CompressionMethods, TableNames, TextureFormat, Overlay
from BuildLib import float_to_hex, main_pointer_table_offset, convertToRGBA32


class File:
    """Class to store information regarding file changes."""

    def __init__(
        self,
        *,
        name="",
        subtype: ChangeType = ChangeType.PointerTable,
        start=None,
        compressed_size=0,
        source_file="",
        compression_method=CompressionMethods.PythonGzip,
        patcher=None,
        pointer_table_index: TableNames = TableNames.MusicMIDI,
        file_index=0,
        texture_format: TextureFormat = TextureFormat.Null,
        bps_file=None,
        do_not_delete_source=False,
        do_not_delete_output=False,
        do_not_delete=False,
        target_compressed_size=None,
        target_uncompressed_size=None,
        target_size=None,
        do_not_extract=False,
        do_not_compress=False,
        do_not_recompress=False,
        bloat_compression=False,
    ):
        """Initialize with given parameters."""
        self.name = name
        self.subtype = subtype
        self.start = start
        self.compressed_size = compressed_size
        self.source_file = source_file
        self.compression_method = compression_method
        self.patcher = patcher
        self.pointer_table_index = pointer_table_index
        self.file_index = file_index
        self.texture_format = texture_format
        self.bps_file = bps_file
        self.do_not_delete_source = do_not_delete_source
        self.do_not_delete_output = do_not_delete_output
        self.do_not_delete = do_not_delete
        self.target_compressed_size = target_compressed_size
        self.target_uncompressed_size = target_uncompressed_size
        if target_size is not None:
            self.target_compressed_size = target_size
            self.target_uncompressed_size = target_size
        elif bloat_compression and self.source_file != "":
            with open(self.source_file, "rb") as sf:
                size = len(sf.read())
                self.target_compressed_size = size
                self.target_uncompressed_size = size
        self.do_not_extract = do_not_extract
        self.do_not_compress = do_not_compress
        self.do_not_recompress = do_not_recompress
        # Static files
        self.output_file = None

    def getTextureFormatName(self) -> int:
        """Get name of texture format used for n64tex."""
        return self.texture_format.name.lower()

    def generateOutputFile(self):
        """Generate output file name."""
        if self.texture_format != TextureFormat.Null:
            self.do_not_extract = True
            extension = f".{self.getTextureFormatName()}"
            self.output_file = self.source_file.replace(".png", extension)

        if self.output_file is None:
            self.output_file = self.source_file

    def generateTextureFile(self):
        """Generate Texture File."""
        if self.texture_format != TextureFormat.Null:
            if self.texture_format in [TextureFormat.RGBA5551, TextureFormat.I4, TextureFormat.I8, TextureFormat.IA4, TextureFormat.IA8]:
                result = subprocess.check_output(["./build/n64tex.exe", self.getTextureFormatName(), self.source_file])
                if self.target_compressed_size is not None:
                    self.source_file = self.source_file.replace(".png", f".{self.getTextureFormatName()}")
            elif self.texture_format == TextureFormat.RGBA32:
                convertToRGBA32(self.source_file)
                self.source_file = self.source_file.replace(".png", ".rgba32")
            else:
                print(" - ERROR: Unsupported texture format " + self.getTextureFormatName())

    def setTargetSize(self, size):
        """Set compressed and uncompressed size."""
        self.target_compressed_size = size
        self.target_uncompressed_size = size


class TableEntry:
    """Class to store information regarding a Table Entry."""

    def __init__(self, index: int):
        """Initialize with given parameters."""
        self.index = index
        self.pointer_address = None
        self.absolute_address = None
        self.new_absolute_address = None
        self.next_absolute_address = None
        self.bit_set = False
        self.original_sha1 = ""
        self.new_sha1 = None
        self.filename = None

    def initVanillaFile(self, index: int, base_address: int, raw_address: int, next_address: int):
        """Initialize with given parameters."""
        self.index = index
        self.pointer_address = base_address + (index * 4)
        self.absolute_address = (raw_address & 0x7FFFFFFF) + main_pointer_table_offset
        self.new_absolute_address = (raw_address & 0x7FFFFFFF) + main_pointer_table_offset
        self.next_absolute_address = next_address
        self.bit_set = (raw_address & 0x80000000) > 0
        self.original_sha1 = ""
        self.new_sha1 = ""

    def initVanillaSHA(self, target_sha: str):
        """Initialize SHA attributes for a vanilla file."""
        self.original_sha1 = target_sha
        self.new_sha1 = target_sha

    def hasChanged(self):
        """Check if the file has changed at all."""
        return self.original_sha1 != self.new_sha1


class TableInfo:
    """Class to store information regarding a pointer table."""

    def __init__(
        self,
        *,
        name="",
        index: TableNames,
        encoded_filename=None,
        decoded_filename=None,
        dont_overwrite_uncompressed_sizes=None,
        encoder=None,
        decoder=None,
        do_not_compress=None,
        force_rewrite=False,
        force_relocate=False,
    ):
        """Initialize with given parameters."""
        if name == "":
            self.name = f"Unknown {index.value}"
        else:
            self.name = name
        self.index = index
        self.encoded_filename = encoded_filename
        self.decoded_filename = decoded_filename
        self.dont_overwrite_uncompressed_sizes = dont_overwrite_uncompressed_sizes
        self.encoder = encoder
        self.decoder = decoder
        self.do_not_compress = do_not_compress
        self.force_rewrite = force_rewrite
        self.force_relocate = force_relocate
        # Static
        self.entries: list[TableEntry] = []
        self.num_entries = 0
        self.absolute_address = None
        self.new_absolute_address = None
        self.original_compressed_size = 0

    def initAddress(self, address: int):
        """Set absolute address attributes to the address parameter."""
        self.absolute_address = address
        self.new_absolute_address = address

    def initEntries(self, fh: BinaryIO):
        """Initialize entry data."""
        fh.seek(main_pointer_table_offset + ((num_tables + self.index) * 4))
        self.num_entries = int.from_bytes(fh.read(4), "big")
        self.original_compressed_size = 0
        self.entries = []
        for i in range(self.num_entries):
            # Compute address and size information about the pointer
            fh.seek(self.absolute_address + (i * 4))
            raw_int = int.from_bytes(fh.read(4), "big")
            next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
            new_entry = TableEntry(i)
            new_entry.initVanillaFile(i, self.absolute_address, raw_int, next_absolute_address)
            self.entries.append(new_entry)


pointer_tables = [
    TableInfo(
        name="Music MIDI",
        index=TableNames.MusicMIDI,
    ),
    TableInfo(
        name="Map Geometry",
        index=TableNames.MapGeometry,
        encoded_filename="geometry.bin",
        decoded_filename="geometry.todo",
        force_relocate=True,
    ),
    TableInfo(
        name="Map Walls",
        index=TableNames.MapWalls,
        encoded_filename="walls.bin",
        decoded_filename="walls.obj",
        dont_overwrite_uncompressed_sizes=True,
        force_relocate=True,
    ),
    TableInfo(
        name="Map Floors",
        index=TableNames.MapFloors,
        encoded_filename="floors.bin",
        decoded_filename="floors.obj",
        dont_overwrite_uncompressed_sizes=True,
        force_relocate=True,
    ),
    TableInfo(
        name="Object Model 2 Geometry",
        index=TableNames.ModelTwoGeometry,
    ),
    TableInfo(
        name="Actor Geometry",
        index=TableNames.ActorGeometry,
    ),
    TableInfo(
        index=TableNames.Unknown6,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(
        name="Textures (Uncompressed)",
        index=TableNames.TexturesUncompressed,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(
        name="Map Cutscenes",
        index=TableNames.Cutscenes,
        encoded_filename="cutscenes.bin",
        decoded_filename="cutscenes.todo",
    ),
    TableInfo(
        name="Map Object Setups",
        index=TableNames.Setups,
        encoded_filename="setup.bin",
        decoded_filename="setup.json",
        encoder=encoders.encodeSetup,
        decoder=encoders.decodeSetup,
    ),
    TableInfo(
        name="Map Object Model 2 Behaviour Scripts",
        index=TableNames.InstanceScripts,
        encoded_filename="object_behaviour_scripts.bin",
        decoded_filename="object_behaviour_scripts.todo",
        force_relocate=True,
    ),
    TableInfo(
        name="Animations",
        index=TableNames.Animations,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(
        name="Text",
        index=TableNames.Text,
    ),
    TableInfo(index=TableNames.Unknown13),
    TableInfo(
        name="Textures",
        index=TableNames.TexturesHUD,
    ),
    TableInfo(
        name="Map Paths",
        index=TableNames.Paths,
        encoded_filename="paths.bin",
        decoded_filename="paths.json",
        encoder=encoders.encodePaths,
        decoder=encoders.decodePaths,
        dont_overwrite_uncompressed_sizes=True,
        do_not_compress=True,
    ),
    TableInfo(
        name="Map Character Spawners",
        index=TableNames.Spawners,
        encoded_filename="character_spawners.bin",
        decoded_filename="character_spawners.json",
        encoder=encoders.encodeCharacterSpawners,
        decoder=encoders.decodeCharacterSpawners,
    ),
    TableInfo(
        name="DKTV Inputs",
        index=TableNames.DKTVInputs,
    ),
    TableInfo(
        name="Map Loading Zones",
        index=TableNames.Triggers,
        encoded_filename="loading_zones.bin",
        decoded_filename="loading_zones.json",
        encoder=encoders.encodeLoadingZones,
        decoder=encoders.decodeLoadingZones,
    ),
    TableInfo(index=TableNames.Unknown19),
    TableInfo(
        index=TableNames.Unknown20,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(
        name="Map Autowalk Data",
        index=TableNames.Autowalks,
        encoded_filename="autowalk.bin",
        decoded_filename="autowalk.json",
        encoder=encoders.encodeAutowalk,
        decoder=encoders.decodeAutowalk,
        do_not_compress=True,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(index=TableNames.Critters),
    TableInfo(
        name="Map Exits",
        index=TableNames.Exits,
        encoded_filename="exits.bin",
        decoded_filename="exits.json",
        encoder=encoders.encodeExits,
        decoder=encoders.decodeExits,
        do_not_compress=True,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(
        name="Map Race Checkpoints",
        index=TableNames.RaceCheckpoints,
        encoded_filename="race_checkpoints.bin",
        decoded_filename="race_checkpoints.json",
        encoder=encoders.encodeCheckpoints,
        decoder=encoders.decodeCheckpoints,
    ),
    TableInfo(
        name="Textures",
        index=TableNames.TexturesGeometry,
    ),
    TableInfo(
        name="Uncompressed File Sizes",
        index=TableNames.UncompressedFileSizes,
        dont_overwrite_uncompressed_sizes=True,
    ),
    TableInfo(index=TableNames.Unknown27),
    TableInfo(index=TableNames.Unknown28),
    TableInfo(index=TableNames.Unknown29),
    TableInfo(index=TableNames.Unknown30),
    TableInfo(index=TableNames.Unknown31),
]
num_tables = len(pointer_tables)


class PointerFile:
    """Class to store information regarding a pointer table file."""

    def __init__(self, address: int, data: bytes, sha1: str, uncompressed_size: int):
        """Initialize with given parameters."""
        self.new_absolute_address = address
        self.data = data
        self.sha1 = sha1
        self.uncompressed_size = uncompressed_size


class HashIcon:
    """Class to store information regarding a hash icon."""

    def __init__(self, icon_file: str, file_index: int):
        """Initialize with given parameters."""
        self.icon_file = icon_file
        self.file_index = file_index


class ModelChange:
    """Class to store information regarding a model change."""

    def __init__(self, model_index: int, model_file: str, bloat: bool = False):
        """Initialize with given parameters."""
        self.model_index = model_index
        self.model_file = model_file
        self.bloat = bloat


class TextChange:
    """Class to store information regarding a text change."""

    def __init__(self, name: str, change_expansion: int, file: str):
        """Initialize with given parameters."""
        self.name = name
        self.change = False
        if file is not None:
            if file != "":
                self.change = True
        self.change_expansion = change_expansion
        self.file = file


class SetupRequirement:
    """Class to store information regarding requirements for a setup action to."""

    def __init__(self, *, map_id=None, obj_type: int = None, obj_id: int = None, banned_maps: list = []):
        """Initialize with given parameters."""
        self.map_id = map_id
        self.obj_type = obj_type
        self.obj_id = obj_id
        self.banned_maps = banned_maps.copy()

    def allow(self, map_id: int, obj_type: int, obj_id: int) -> bool:
        """Will input conditions fulfill the requirements."""
        if map_id in self.banned_maps:
            return False
        if self.map_id is None or self.map_id == -1 or self.map_id == map_id:
            if self.obj_type is None or self.obj_type == -1 or self.obj_type == obj_type:
                return self.obj_id is None or self.obj_id == -1 or self.obj_id == obj_id
        return False


class SetupActionModelTwo:
    """Class to store information regarding an added model two item to the setup."""

    def __init__(self, *, requirement: SetupRequirement = None, base_byte_stream=None, type=None, x=None, y=None, z=None, rx=None, ry=None, rz=None, id=None, scale=None, spawn_limit=1):
        """Initialize with given parameters."""
        self.requirement = requirement
        self.base_byte_stream = base_byte_stream
        self.type = type
        # Defaults
        self.x = None
        self.y = None
        self.z = None
        self.rx = None
        self.ry = None
        self.rz = None
        self.scale = None
        if x is not None:
            self.x = int(float_to_hex(x), 16)
        if y is not None:
            self.y = int(float_to_hex(y), 16)
        if z is not None:
            self.z = int(float_to_hex(z), 16)
        if rx is not None:
            self.rx = int(float_to_hex(rx), 16)
        if ry is not None:
            self.ry = int(float_to_hex(ry), 16)
        if rz is not None:
            self.rz = int(float_to_hex(rz), 16)
        if scale is not None:
            self.scale = int(float_to_hex(scale), 16)
        self.id = id
        self.spawn_limit = spawn_limit

    def spawn(self):
        """Spawn item."""
        if self.spawn_limit > 1:
            self.spawn_limit -= 1

    def canSpawn(self) -> bool:
        """Determine whether a spawn can occur with this change."""
        return self.spawn_limit >= 1 and self.requirement.allow()


class ROMPointerFile:
    """Class to store information about a ROM Pointer table file."""

    def __init__(self, rom: BinaryIO, table_index: int, file_index: int):
        """Initialize with given data."""
        rom.seek(main_pointer_table_offset + (table_index * 4))
        table_address = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table_address + (file_index * 4))
        self.start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        self.end = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        self.size = self.end - self.start
        rom.seek(self.start)
        self.compressed = int.from_bytes(rom.read(2), "big") == 0x1F8B


BOOT_OVERLAY_RDRAM = 0x80000450


class OverlayInfo:
    """Class to store information about an overlay."""

    def __init__(
        self,
        overlay: Overlay,
        code_rom: int,
        data_rom: int,
        data_size_compressed: int,
        code_write_upper: int,
        code_write_lower: int,
        data_write_upper: int,
        data_write_lower: int,
        default_code_size: int,
        default_data_size: int,
    ):
        """Initialize with given data."""
        self.overlay = overlay
        self.code_rom = code_rom
        self.data_rom = data_rom
        self.code_size_compressed = self.data_rom - self.code_rom
        self.data_size_compressed = data_size_compressed
        self.no_gzip_footer_length = self.data_size_compressed - 8

        self.code_write_upper = code_write_upper - BOOT_OVERLAY_RDRAM
        self.code_write_lower = code_write_lower - BOOT_OVERLAY_RDRAM
        self.data_write_upper = data_write_upper - BOOT_OVERLAY_RDRAM
        self.data_write_lower = data_write_lower - BOOT_OVERLAY_RDRAM

        self.code = None
        self.data = None
        self.code_decompressed = None
        self.data_decompressed = None
        self.code_size = default_code_size
        self.data_size = default_data_size
        self.code_start = None
        self.data_start = None
        self.data_end = None

    def setCode(self, bytestream: bytes, footer: bytes):
        """Set code values."""
        self.code = bytestream
        self.code_decompressed = zlib.decompress(bytestream + footer, (15 + 32))
        self.code_size = len(self.code_decompressed)

    def setData(self, bytestream: bytes, footer: bytes):
        """Set data values."""
        self.data = bytestream
        self.data_decompressed = zlib.decompress(bytestream + footer, (15 + 32))
        self.data_size = len(self.data_decompressed)


class HintRegion:
    """Class to store information regarding a hint region."""

    def __init__(self, region_name: str, enum_name: str):
        """Initialize with given data."""
        self.region_name = region_name
        self.enum_name = enum_name


hint_region_list = [
    HintRegion("???", "NullRegion"),
    # Shops
    HintRegion("Isles Shops", "ShopIsles"),
    HintRegion("Japes Shops", "ShopJapes"),
    HintRegion("Aztec Shops", "ShopAztec"),
    HintRegion("Factory Shops", "ShopFactory"),
    HintRegion("Galleon Shops", "ShopGalleon"),
    HintRegion("Forest Shops", "ShopFungi"),
    HintRegion("Caves Shops", "ShopCaves"),
    HintRegion("Castle Shops", "ShopCastle"),
    HintRegion("Jetpac Game", "Jetpac"),  # Shouldn't really be accessible
    # Medals
    HintRegion("Isles Medal Rewards", "MedalsIsles"),  # Shouldn't be accessible
    HintRegion("Japes Medal Rewards", "MedalsJapes"),  # Shouldn't be accessible
    HintRegion("Aztec Medal Rewards", "MedalsAztec"),  # Shouldn't be accessible
    HintRegion("Factory Medal Rewards", "MedalsFactory"),  # Shouldn't be accessible
    HintRegion("Galleon Medal Rewards", "MedalsGalleon"),  # Shouldn't be accessible
    HintRegion("Forest Medal Rewards", "MedalsFungi"),  # Shouldn't be accessible
    HintRegion("Caves Medal Rewards", "MedalsCaves"),  # Shouldn't be accessible
    HintRegion("Castle Medal Rewards", "MedalsCastle"),  # Shouldn't be accessible
    # Isles
    HintRegion("Game Start", "GameStart"),
    HintRegion("Credits", "Credits"),
    HintRegion("Main Isle", "IslesMain"),
    HintRegion("Outer Isles", "IslesOuter"),
    HintRegion("Krem Isle", "IslesKrem"),
    HintRegion("Rareware Banana Room", "IslesRareware"),
    HintRegion("Japes - Forest Lobbies", "IslesLobbies0"),
    HintRegion("Caves - Helm Lobbies", "IslesLobbies1"),
    HintRegion("K Rool Arena", "IslesKRool"),  # No checks here right now
    # Japes
    HintRegion("Japes Lowlands", "JapesLow"),
    HintRegion("Japes Hillside", "JapesHigh"),
    HintRegion("Stormy Tunnel Area", "JapesStorm"),
    HintRegion("Hive Tunnel Area", "JapesHive"),
    HintRegion("Japes Caves and Mines", "JapesCaverns"),
    # Aztec
    HintRegion("Aztec Oasis and Totem Area", "AztecOasisTotem"),
    HintRegion("Tiny Temple", "AztecTiny"),
    HintRegion("5 Door Temple", "AztecGetOut"),
    HintRegion("Llama Temple", "AztecLlama"),
    HintRegion("Various Aztec Tunnels", "AztecTunnels"),
    # Factory
    HintRegion("Frantic Factory Start", "FactoryStart"),
    HintRegion("Testing Area", "FactoryTesting"),
    HintRegion("Research and Development Area", "FactoryResearch"),
    HintRegion("Storage and Arcade", "FactoryStorage"),
    HintRegion("Production Room", "FactoryProd"),
    # Galleon
    HintRegion("Galleon Caverns", "GalleonCaverns"),
    HintRegion("Lighthouse Area", "GalleonLighthouse"),
    HintRegion("Shipyard Outskirts", "GalleonShipyard"),
    HintRegion("Treasure Room", "GalleonTreasure"),
    HintRegion("5 Door Ship", "GalleonShip"),
    # Forest
    HintRegion("Forest Center and Beanstalk", "ForestStart"),
    HintRegion("Giant Mushroom Exterior", "ForestGMExt"),
    HintRegion("Giant Mushroom Insides", "ForestGMInt"),
    HintRegion("Owl Tree", "ForestOwl"),
    HintRegion("Forest Mills", "ForestMills"),
    # Caves
    HintRegion("Main Caves Area", "CavesMain"),
    HintRegion("Igloo Area", "CavesIgloo"),
    HintRegion("Cabins Area", "CavesCabins"),
    # Castle
    HintRegion("Castle Surroundings", "CastleExt"),
    HintRegion("Castle Rooms", "CastleRooms"),
    HintRegion("Castle Underground", "CastleUnderground"),
    # Other
    HintRegion("Hideout Helm", "OtherHelm"),
    HintRegion("Troff n Scoff", "OtherTnS"),
    HintRegion("This should not be hinted", "Error"),
]


class Coordinate:
    """Class to store information regarding a coordinate."""

    def __init__(self, x: float, y: float, z: float):
        """Initialize with given parameters."""
        self.x = x
        self.y = y
        self.z = z


class VineSequence:
    """Class to store information regarding a vine sequence."""

    def __init__(self, map_index: int, point_start: Coordinate, point_end: Coordinate, ids: list[int]):
        """Initialize with given parameters."""
        self.map_index = map_index
        self.point_start = point_start
        self.point_end = point_end
        self.ids = ids.copy()

    def getSequenceDistance(self) -> float:
        """Get the distance between point_start and point_end."""
        dx = self.point_end.x - self.point_start.x
        dy = self.point_end.y - self.point_start.y
        dz = self.point_end.z - self.point_start.z
        return math.sqrt((dx * dx) + (dy * dy) + (dz * dz))

    def getSequencePoint(self, index: int, count: int) -> Coordinate:
        """Get a coordinate from the sequence based on the index and total amount of vines that are to be placed."""
        dx = self.point_end.x - self.point_start.x
        dy = self.point_end.y - self.point_start.y
        dz = self.point_end.z - self.point_start.z
        px = self.point_start.x + (((index + 1) / count) * dx)
        py = self.point_start.y + (((index + 1) / count) * dy)
        pz = self.point_start.z + (((index + 1) / count) * dz)
        return Coordinate(px, py, pz)


class MoveName:
    """Class to store the text for a move_name."""

    def __init__(self, name: str, move_type: int, latin: str = None):
        """Initialize with given parameters."""
        self.name = name
        self.move_type = move_type
        self.latin = latin
