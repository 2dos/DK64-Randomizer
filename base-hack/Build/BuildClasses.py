"""Global classes for the build process."""

from image_converter import convertToRGBA32
from typing import BinaryIO
import subprocess
from BuildEnums import ChangeType, TableNames, TextureFormat
from BuildLib import main_pointer_table_offset
import encoders


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
        use_external_gzip=False,
        use_zlib=False,
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
        do_not_extract=False,
        do_not_compress=False,
        do_not_recompress=False,
    ):
        """Initialize with given parameters."""
        self.name = name
        self.subtype = subtype
        self.start = start
        self.compressed_size = compressed_size
        self.source_file = source_file
        self.use_external_gzip = use_external_gzip
        self.use_zlib = use_zlib
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
    TableInfo(index=TableNames.Unknown22),
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
