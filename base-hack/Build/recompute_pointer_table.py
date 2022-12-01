"""Recompute all the pointers within the rom."""
from hashlib import sha1
from json import dumps
from typing import BinaryIO

import encoders
from map_names import maps

class TableEntry:
    """Class to store information regarding a pointer table entry."""

    def __init__(self, index, pointer_address, absolute_address, next_absolute_address, bit_set):
        self.index = index
        self.pointer_address = pointer_address
        self.absolute_address = absolute_address
        self.new_absolute_address = absolute_address
        self.next_absolute_address = next_absolute_address
        self.bit_set = bit_set
        self.original_sha1 = ""
        self.new_sha1 = ""
        self.filename = ""

class PointerTable:
    """Class to store information regarding a pointer table."""

    def __init__(self, *, name="", index=0, encoded_filename=None, decoded_filename=None, dont_overwrite_uncompressed_sizes=False, encoder=None, decoder=None, do_not_compress=False, use_external_gzip=False):
        """Initialize with given parameters."""
        self.index = index
        if name == "":
            self.name = f"Unknown {index}"
        else:
            self.name = name
        self.encoded_filename = encoded_filename
        self.decoded_filename = decoded_filename
        self.dont_overwrite_uncompressed_sizes = dont_overwrite_uncompressed_sizes
        self.encoder = encoder
        self.decoder = decoder
        self.do_not_compress = do_not_compress
        self.num_entries = 0
        self.entries = []
        self.original_compressed_size = 0
        self.absolute_address = None
        self.new_absolute_address = None
        self.use_external_gzip = use_external_gzip

    def setAbsoluteAddress(self, value, overwrite_old=False):
        self.new_absolute_address = value
        if overwrite_old:
            self.absolute_address = value

    def initEntries(self, entry_count):
        self.num_entries = entry_count
        self.entries = []
        self.original_compressed_size = 0

    def pushEntry(self, entry: TableEntry):
        self.entries.append(entry)

pointer_tables = [
    PointerTable(name="Music MIDI", index=0),
    PointerTable(name="Map Geometry", index=1, encoded_filename="geometry.bin", decoded_filename="geometry.todo"),
    PointerTable(name="Map Walls", index=2, encoded_filename="walls.bin", decoded_filename="walls.obj", dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Map Floors", index=3, encoded_filename="floors.bin", decoded_filename="floors.obj", dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Object Model 2 Geometry", index=4),
    PointerTable(name="Actor Geometry", index=5),
    PointerTable(index=6, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Textures (Uncompressed)", index=7, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Map Cutscenes", index=8, encoded_filename="cutscenes.bin", decoded_filename="cutscenes.todo"),
    PointerTable(name="Map Object Setups", index=9, encoded_filename="setup.bin", decoded_filename="setup.json", encoder=encoders.encodeSetup, decoder=encoders.decodeSetup),
    PointerTable(name="Map Object Model 2 Behaviour Scripts", index=10, encoded_filename="object_behaviour_scripts.bin", decoded_filename="object_behaviour_scripts.todo"),
    PointerTable(name="Animations", index=11, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Text", index=12),
    PointerTable(index=13),
    PointerTable(name="Textures", index=14),
    PointerTable(name="Map Paths", index=15, encoded_filename="paths.bin", decoded_filename="paths.json", encoder=encoders.encodePaths, decoder=encoders.decodePaths, do_not_compress=True, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Map Character Spawners", index=16, encoded_filename="character_spawners.bin", decoded_filename="character_spawners.json", encoder=encoders.encodeCharacterSpawners, decoder=encoders.decodeCharacterSpawners),
    PointerTable(name="DKTV Inputs", index=17),
    PointerTable(name="Map Loading Zones", index=18, encoded_filename="loading_zones.bin", decoded_filename="loading_zones.json", encoder=encoders.encodeLoadingZones, decoder=encoders.decodeLoadingZones),
    PointerTable(index=19),
    PointerTable(index=20, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Map Autowalk Data", index=21, encoded_filename="autowalk.bin", decoded_filename="autowalk.json", encoder=encoders.encodeAutowalk, decoder=encoders.decodeAutowalk, do_not_compress=True, dont_overwrite_uncompressed_sizes=True),
    PointerTable(index=22),
    PointerTable(name="Map Exits", index=23, encoded_filename="exits.bin", decoded_filename="exits.json", encoder=encoders.encodeExits, decoder=encoders.decodeExits, do_not_compress=True, dont_overwrite_uncompressed_sizes=True),
    PointerTable(name="Map Race Checkpoints", index=24, encoded_filename="race_checkpoints.bin", decoded_filename="race_checkpoints.json", encoder=encoders.encodeCheckpoints, decoder=encoders.decodeCheckpoints),
    PointerTable(name="Textures", index=25),
    PointerTable(name="Uncompressed File Sizes", index=26, dont_overwrite_uncompressed_sizes=True),
    PointerTable(index=27),
    PointerTable(index=28),
    PointerTable(index=29),
    PointerTable(index=30),
    PointerTable(index=31),
]

num_tables = len(pointer_tables)
main_pointer_table_offset = 0x101C50

# The address of the next available byte of free space in ROM
# used when appending files to the end of the ROM
# next_available_free_space = 0x1FED020
# next_available_free_space = 0x2000000
next_available_free_space = 0x2030000  # TODO: Get this calculating automatically

# These will be indexed by pointer table index then by SHA1 hash of the data
pointer_table_files = [{}] * len(pointer_tables)

force_table_rewrite = [
    # 0, # Music MIDI
    # 1, # Map Geometry
    # 2, # Map Walls
    # 3, # Map Floors
    # 4, # Object Model 2 Geometry
    # 5, # Actor Geometry
    # 7, # Textures (Uncompressed)
    # 8, # Map Cutscenes
    # 9, # Map Object Setups
    # 10, # Map Object Model 2 Behaviour Scripts
    # 11, # Animations
    # 12, # Text
    # 14, # Textures
    # 15, # Map Paths
    # 16, # Map Character Spawners
    # 18, # Map Loading Zones
    # 21, # Map Autowalk Data
    # 23, # Map Exits
    # 24, # Map Race Checkpoints
    # 25, # Textures
]


def make_safe_filename(s: str):
    """Make the file name safe without _."""

    def safe_char(c: str):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def getOriginalUncompressedSize(fh: BinaryIO, pointer_table_index: int, file_index: int):
    """Get the orignal uncompressed size."""
    if pointer_tables[pointer_table_index].dont_overwrite_uncompressed_sizes:
        return 0

    ROMAddress = pointer_tables[26].entries[pointer_table_index].absolute_address + file_index * 4

    # print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

    fh.seek(ROMAddress)
    return int.from_bytes(fh.read(4), "big")


# Write the new uncompressed size back to ROM to prevent malloc buffer overruns when decompressing
def writeUncompressedSize(fh: BinaryIO, pointer_table_index: int, file_index: int, uncompressed_size: int):
    """Write to the uncompressed size."""
    if pointer_tables[pointer_table_index].dont_overwrite_uncompressed_sizes:
        return 0

    fh.seek(main_pointer_table_offset + (26 * 4))
    unc_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(unc_table + (pointer_table_index * 4))
    ROMAddress = main_pointer_table_offset + int.from_bytes(fh.read(4), "big") + file_index * 4

    # Game seems to align these mod 2
    if uncompressed_size % 2 == 1:
        uncompressed_size += 1

    print(" - Writing new uncompressed size " + hex(uncompressed_size) + " for file " + str(pointer_table_index) + "->" + str(file_index) + " to ROM address " + hex(ROMAddress))

    fh.seek(ROMAddress)
    fh.write(int.to_bytes(uncompressed_size, 4, "big"))


def getPointerTableCompressedSize(pointer_table_index: int):
    """Get the tables compressed size."""
    total_compressed_size = 0
    if pointer_table_index < len(pointer_tables):
        pointer_table = pointer_tables[pointer_table_index]
        for entry in pointer_table.entries:
            file_info = getFileInfo(pointer_table_index, entry.index)
            if file_info:
                total_compressed_size += len(file_info["data"])
    return total_compressed_size


def parsePointerTables(fh: BinaryIO):
    """Parse the pointer tables."""
    # Read pointer table addresses
    fh.seek(main_pointer_table_offset)
    for x in pointer_tables:
        absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
        x.setAbsoluteAddress(absolute_address, True)

    # Read pointer table lengths
    fh.seek(main_pointer_table_offset + num_tables * 4)
    for x in pointer_tables:
        x.initEntries(int.from_bytes(fh.read(4), "big"))

    # Read pointer table entries
    for x in pointer_tables:
        if x.num_entries > 0:
            for i in range(x.num_entries):
                # Compute address and size information about the pointer
                fh.seek(x.absolute_address + i * 4)
                raw_int = int.from_bytes(fh.read(4), "big")
                absolute_address = (raw_int & 0x7FFFFFFF) + main_pointer_table_offset
                next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
                x.pushEntry(
                    TableEntry(i, hex(x.absolute_address + i * 4), absolute_address, next_absolute_address, (raw_int & 0x80000000) > 0)
                )

    # Read data and original uncompressed size
    # Note: Needs to happen after all entries are read for annoying reasons
    for x in pointer_tables:
        if x.num_entries > 0:
            for y in x.entries:
                if not y.bit_set:
                    absolute_size = y.next_absolute_address - y.absolute_address
                    if absolute_size > 0:
                        file_info = addFileToDatabase(fh, y.absolute_address, absolute_size, x.index, y.index)
                        x.original_compressed_size += absolute_size

    # Go back over and look up SHA1s for the bit_set entries
    # Note: Needs to be last because it's possible earlier entries point to later entries that might not have data yet
    for x in pointer_tables:
        if x.num_entries > 0:
            for y in x.entries:
                if y.bit_set:
                    fh.seek(y.absolute_address)
                    lookup_index = int.from_bytes(fh.read(2), "big")
                    file_info = getFileInfo(x.index, lookup_index)
                    if file_info:
                        y.original_sha1 = file_info["sha1"]
                        y.new_sha1 = file_info["sha1"]
                        # y.bit_set = False # We'll turn this back on later when recomputing pointer tables


def addFileToDatabase(fh: BinaryIO, absolute_address: int, absolute_size: int, pointer_table_index: int, file_index: int):
    """Add the files to the database."""
    # TODO: Get rid of this check
    for x in pointer_tables:
        if x.absolute_address == absolute_address:
            print(f"WARNING: POINTER TABLE {x.index} BEING USED AS FILE!")
            return

    fh.seek(absolute_address)
    data = fh.read(absolute_size)

    dataSHA1Hash = sha1(data).hexdigest()

    pointer_tables[pointer_table_index].entries[file_index].original_sha1 = dataSHA1Hash
    pointer_tables[pointer_table_index].entries[file_index].new_sha1 = dataSHA1Hash

    pointer_table_files[pointer_table_index][dataSHA1Hash] = {
        "new_absolute_address": absolute_address,
        "data": data,
        "sha1": dataSHA1Hash,
        "uncompressed_size": getOriginalUncompressedSize(fh, pointer_table_index, file_index),
    }
    return pointer_table_files[pointer_table_index][dataSHA1Hash]


def getFileInfo(pointer_table_index: int, file_index: int):
    """Get the files info."""
    if pointer_table_index not in range(len(pointer_tables)):
        return

    if file_index not in range(len(pointer_tables[pointer_table_index].entries)):
        return

    if not pointer_tables[pointer_table_index].entries[file_index].new_sha1 in pointer_table_files[pointer_table_index]:
        return

    return pointer_table_files[pointer_table_index][pointer_tables[pointer_table_index].entries[file_index].new_sha1]


def replaceROMFile(rom: BinaryIO, pointer_table_index: int, file_index: int, data: bytes, uncompressed_size: int, filename: str = ""):
    """Replace the ROM file."""
    # TODO: Get this working
    if pointer_table_index == 8 and file_index == 0:
        print(" - WARNING: Tried to replace Test Map cutscenes. This will replace global cutscenes, so it has been disabled for now to prevent crashes.")
        return

    # Align data to 2 byte boundary for DMA
    if len(data) % 2 == 1:
        data_array = bytearray(data)
        data_array.append(0)
        data = bytes(data_array)

    # Insert the new data into the database
    dataSHA1Hash = sha1(data).hexdigest()
    pointer_table_files[pointer_table_index][dataSHA1Hash] = {"data": data, "sha1": dataSHA1Hash, "uncompressed_size": uncompressed_size}

    # Update the entry in the pointer table to point to the new data
    if file_index >= len(pointer_tables[pointer_table_index].entries):
        diff = file_index - len(pointer_tables[pointer_table_index].entries) + 1
        print(f" - Appending {diff} extra entries to {pointer_tables[pointer_table_index].name} ({(file_index+1)-diff}->{file_index+1})")
        for d in range(diff):
            pointer_tables[pointer_table_index].pushEntry(
                TableEntry(file_index, None, None, None, False)
            )
        rom.seek(main_pointer_table_offset + (4 * len(pointer_tables)) + (4 * pointer_table_index))
        rom.write((file_index + 1).to_bytes(4, "big"))
        pointer_tables[pointer_table_index].num_entries = file_index + 1

        # Update uncompressed pointer table entry
        rom.seek(main_pointer_table_offset + (4 * 26))
        uncompressed_table_location = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(uncompressed_table_location + (4 * pointer_table_index))
        uncompressed_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        uncompressed_finish = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        uncompressed_table_size = uncompressed_finish - uncompressed_start
        if uncompressed_table_size > 0:
            print(f" - Expanding pointer table {pointer_table_index} from {uncompressed_table_size} bytes to {4 * (file_index + 1)} bytes")
            rom.seek(uncompressed_start)
            new_uncompressed_data = bytearray(rom.read(uncompressed_table_size))
            for d in range((4 * (file_index + 1)) - uncompressed_table_size):
                new_uncompressed_data.append(0)
            replaceROMFile(rom, 26, pointer_table_index, bytes(new_uncompressed_data), 4 * (file_index + 1))

    pointer_tables[pointer_table_index].entries[file_index].new_sha1 = dataSHA1Hash

    if len(filename) > 0:
        pointer_tables[pointer_table_index].entries[file_index].filename = filename


def clampCompressedTextures(rom: BinaryIO, cap: int):
    """Clamps the size of pointer table 25 to reduce it's size to save space."""
    original_length = len(pointer_tables[25].entries)
    if original_length > cap:
        print(f"- Compressing pointer table 25 to {cap} entries")
        pointer_tables[25].entries = pointer_tables[25].entries[:cap]
        rom.seek(main_pointer_table_offset + (4 * len(pointer_tables)) + (4 * 25))
        rom.write((cap).to_bytes(4, "big"))
        pointer_tables[25].num_entries = cap

        # Update uncompressed pointer table entry
        rom.seek(main_pointer_table_offset + (4 * 26))
        uncompressed_table_location = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(uncompressed_table_location + (4 * 25))
        uncompressed_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        uncompressed_finish = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        uncompressed_table_size = uncompressed_finish - uncompressed_start
        if uncompressed_table_size > 0:
            new_size = 4 * cap
            print(f" - Compressing pointer table 25 from {uncompressed_table_size} bytes to {new_size} bytes")
            rom.seek(uncompressed_start)
            new_uncompressed_data = bytearray(rom.read(new_size))
            replaceROMFile(rom, 26, 25, bytes(new_uncompressed_data), new_size)


def shouldWritePointerTable(index: int):
    """Write to the pointer table."""
    # Table 6 is nonsense.
    # This fixes heap corruption caused by a buffer overrun when decompressing a replaced file into a malloc'd buffer
    if index == 6:
        return False

    # No need to recompute pointer tables with no entries in them
    if pointer_tables[index].num_entries == 0:
        return False

    if index in force_table_rewrite:
        return True

    # TODO: Better logic for this
    if pointer_tables[index]:
        for y in pointer_tables[index].entries:
            if y.original_sha1 != y.new_sha1:
                return True

    return False


def shouldRelocatePointerTable(index: int):
    """Relocate the pointer table."""
    # TODO: Remove this once deduplication is implemented
    # Note: Always relocate map walls, floors, geometry, and model 2 behaviour scripts
    # These tables contain bit_set entries so cannot be rewritten in place until deduplication works properly
    if index in (1, 2, 3, 10):
        return True

    return getPointerTableCompressedSize(index) > pointer_tables[index].original_compressed_size


def writeModifiedPointerTablesToROM(fh: BinaryIO):
    """Write the modified pointer tables to the rom file."""
    global next_available_free_space

    # Reserve pointer table space and write new data
    for x in pointer_tables:
        if not shouldWritePointerTable(x.index):
            continue

        # Reserve free space for the pointer table in ROM
        space_required = x.num_entries * 4 + 4
        should_relocate = shouldRelocatePointerTable(x.index)
        if should_relocate:
            x.new_absolute_address = next_available_free_space

        write_pointer = x.new_absolute_address + space_required
        earliest_file_address = write_pointer

        # Write all files to ROM
        for y in x.entries:
            file_info = getFileInfo(x.index, y.index)
            y.new_absolute_address = write_pointer
            if file_info:
                if len(file_info["data"]) > 0:
                    write_pointer += len(file_info["data"])
                    fh.seek(y.new_absolute_address)
                    fh.write(file_info["data"])

        # If the files have been appended to ROM, we need to move the free space pointer along by the number of bytes written
        if should_relocate:
            next_available_free_space += space_required  # For the pointer table itself
            next_available_free_space += write_pointer - earliest_file_address  # For all of the files

    # Recompute the pointer tables using the new file addresses and write them in the reserved space
    for x in reversed(pointer_tables):
        fh.seek(main_pointer_table_offset + (26 * 4))
        print(f"Pointer Table {x.index}. New Location: {hex(main_pointer_table_offset + int.from_bytes(fh.read(4),'big'))}. Write Location:")
        if not shouldWritePointerTable(x.index):
            continue

        adjusted_pointer = 0
        next_pointer = 0
        for y in x.entries:
            file_info = getFileInfo(x.index, y.index)
            if file_info:
                # Pointers to regular files calculated as normal
                adjusted_pointer = y.new_absolute_address - main_pointer_table_offset
                next_pointer = y.new_absolute_address + len(file_info["data"]) - main_pointer_table_offset

                # Update the uncompressed filesize
                if y.original_sha1 != y.new_sha1:
                    writeUncompressedSize(fh, x.index, y.index, file_info["uncompressed_size"])
            else:
                adjusted_pointer = next_pointer

            # Fix for tables with no entry at slot 0
            if adjusted_pointer == 0:
                adjusted_pointer = earliest_file_address - main_pointer_table_offset
                next_pointer = earliest_file_address - main_pointer_table_offset

            # Update the pointer
            fh.seek(x.new_absolute_address + y.index * 4)
            fh.write(adjusted_pointer.to_bytes(4, "big"))
            fh.write(next_pointer.to_bytes(4, "big"))

        # Redirect the global pointer to the new table
        fh.seek(main_pointer_table_offset + x.index * 4)
        fh.write((x.new_absolute_address - main_pointer_table_offset).to_bytes(4, "big"))


dataset = []


def dumpPointerTableDetails(filename: str, fr: BinaryIO):
    """Dump the pointer table info into a JSON readable pointer table."""
    print("Dumping Pointer Table Details to " + filename)
    for x in pointer_tables:
        entries = []
        for y in x.entries:
            # Seek to the address and read the value
            fr.seek(x.new_absolute_address + y.index * 4)
            # Find the new position
            pointing_to = (int.from_bytes(fr.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
            file_info = getFileInfo(x.index, y.index)
            uncompressed_size = getOriginalUncompressedSize(fr, x.index, y.index)
            filename = y.filename
            if filename == "":
                filename = None
            new_entry = {
                "index": int(len(entries)),
                "new_address": int(x.new_absolute_address + y.index * 4),
                "pointing_to": int(pointing_to),
                "compressed_size": int(len(file_info["data"])) if file_info else None,
                "uncompressed_size": int(uncompressed_size) if uncompressed_size > 0 else None,
                "bit_set": y.bit_set,
                "map_index": maps[y.index] if x.num_entries == 221 else None,
                "file_name": filename,
                "sha": y.new_sha1,
            }
            entries.insert(y.index, new_entry)
        section_data = {
            "name": x.name,
            "address": int(x.new_absolute_address),
            "total_entries": int(x.num_entries),
            "starting_byte": int(x.original_compressed_size),
            "ending_byte": int(getPointerTableCompressedSize(x.index)),
            "entries": entries,
        }
        dataset.insert(x.index, section_data)

    with open("../static/patches/pointer_addresses.json", "w") as fh:
        fh.write(dumps(dataset))


def dumpPointerTableDetailsLegacy(filename: str, fr: BinaryIO):
    """Dump the table details in the legacy log format."""
    with open(filename, "w") as fh:
        for x in pointer_tables:
            fh.write(f"{x.index}: {x.name}: {hex(x.new_absolute_address)} ({x.num_entries} entries, {hex(x.original_compressed_size)} -> {hex(getPointerTableCompressedSize(x.index))} bytes)\n")
            for y in x.entries:
                fh.write(" - " + str(y.index) + ": ")
                fh.write(hex(x.new_absolute_address + y.index * 4) + " -> ")
                fr.seek(x.new_absolute_address + y.index * 4)
                pointing_to = (int.from_bytes(fr.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
                fh.write(hex(pointing_to))

                file_info = getFileInfo(x.index, y.index)
                if file_info:
                    fh.write(" (" + hex(len(file_info["data"])) + ")")
                else:
                    fh.write(" WARNING: File info not found")

                uncompressed_size = getOriginalUncompressedSize(fr, x.index, y.index)
                if uncompressed_size > 0:
                    fh.write(" (" + hex(uncompressed_size) + ")")
                fh.write(" (" + str(y.bit_set) + ")")

                if x.num_entries == 221:
                    fh.write(" (" + maps[y.index] + ")")

                fh.write(" (" + str(y.new_sha1) + ")")

                if y.filename != "":
                    fh.write(" (" + str(y.filename) + ")")

                fh.write("\n")
