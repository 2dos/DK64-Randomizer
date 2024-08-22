"""Recompute all the pointers within the rom."""

import hashlib
import json
from typing import BinaryIO

from BuildClasses import PointerFile, ROMPointerFile, TableEntry, pointer_tables
from BuildEnums import TableNames
from BuildLib import heap_size, main_pointer_table_offset
from BuildNames import maps
from recompute_overlays import getOverlayTotalSize

# The address of the next available byte of free space in ROM
# used when appending files to the end of the ROM

available_writes = [[0x2000000 + heap_size + getOverlayTotalSize(), 0x3FFFFFF]]

# These will be indexed by pointer table index then by SHA1 hash of the data
pointer_table_files = []
for x in pointer_tables:
    pointer_table_files.append({})


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

    ROMAddress = pointer_tables[TableNames.UncompressedFileSizes].entries[pointer_table_index].absolute_address + file_index * 4

    # print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

    fh.seek(ROMAddress)
    return int.from_bytes(fh.read(4), "big")


# Write the new uncompressed size back to ROM to prevent malloc buffer overruns when decompressing
def writeUncompressedSize(fh: BinaryIO, pointer_table_index: int, file_index: int, uncompressed_size: int):
    """Write to the uncompressed size."""
    if pointer_tables[pointer_table_index].dont_overwrite_uncompressed_sizes:
        return 0

    fh.seek(main_pointer_table_offset + (TableNames.UncompressedFileSizes * 4))
    unc_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(unc_table + (pointer_table_index * 4))
    ROMAddress = main_pointer_table_offset + int.from_bytes(fh.read(4), "big") + file_index * 4

    # Game seems to align these mod 2
    uncompressed_size += uncompressed_size % 2

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
                total_compressed_size += len(file_info.data)
    return total_compressed_size


def parsePointerTables(fh: BinaryIO):
    """Parse the pointer tables."""
    # Read pointer table addresses
    fh.seek(main_pointer_table_offset)
    for x in pointer_tables:
        absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
        x.initAddress(absolute_address)

    # Read pointer table entries
    for x in pointer_tables:
        x.initEntries(fh)

    # Read data and original uncompressed size
    # Note: Needs to happen after all entries are read for annoying reasons
    for x in pointer_tables:
        if x.num_entries > 0:
            for yi, y in enumerate(x.entries):
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
                        y.initVanillaSHA(file_info.sha1)
                        # y.bit_set = False # We'll turn this back on later when recomputing pointer tables


def addFileToDatabase(fh: BinaryIO, absolute_address: int, absolute_size: int, pointer_table_index: int, file_index: int) -> PointerFile:
    """Add the files to the database."""
    # TODO: Get rid of this check
    for x in pointer_tables:
        if x.absolute_address == absolute_address:
            print("WARNING: POINTER TABLE " + str(x.index) + " BEING USED AS FILE!")
            return

    fh.seek(absolute_address)
    data = fh.read(absolute_size)

    dataSHA1Hash = hashlib.sha1(data).hexdigest()

    pointer_tables[pointer_table_index].entries[file_index].initVanillaSHA(dataSHA1Hash)

    pointer_table_files[pointer_table_index][dataSHA1Hash] = PointerFile(absolute_address, data, dataSHA1Hash, getOriginalUncompressedSize(fh, pointer_table_index, file_index))

    return pointer_table_files[pointer_table_index][dataSHA1Hash]


def getFileInfo(pointer_table_index: int, file_index: int) -> PointerFile:
    """Get the files info."""
    if pointer_table_index not in range(len(pointer_tables)):
        return

    if file_index < 0 or file_index >= len(pointer_tables[pointer_table_index].entries):
        return

    if not pointer_tables[pointer_table_index].entries[file_index].new_sha1 in pointer_table_files[pointer_table_index]:
        return

    return pointer_table_files[pointer_table_index][pointer_tables[pointer_table_index].entries[file_index].new_sha1]


def replaceROMFile(rom: BinaryIO, pointer_table_index: int, file_index: int, data: bytes, uncompressed_size: int, filename: str = ""):
    """Replace the ROM file."""
    # TODO: Get this working
    # if pointer_table_index == TableNames.Cutscenes and file_index == 0:
    #     print(" - WARNING: Tried to replace Test Map cutscenes. This will replace global cutscenes, so it has been disabled for now to prevent crashes.")
    #     return

    # Align data to 2 byte boundary for DMA
    if len(data) % 2 == 1:
        data_array = bytearray(data)
        data_array.append(0)
        data = bytes(data_array)

    # Insert the new data into the database
    dataSHA1Hash = hashlib.sha1(data).hexdigest()
    pointer_table_files[pointer_table_index][dataSHA1Hash] = PointerFile(None, data, dataSHA1Hash, uncompressed_size)

    # Update the entry in the pointer table to point to the new data
    if file_index >= len(pointer_tables[pointer_table_index].entries):
        diff = file_index - len(pointer_tables[pointer_table_index].entries) + 1
        print(f" - Appending {diff} extra entries to {pointer_tables[pointer_table_index].name} ({(file_index+1)-diff}->{file_index+1})")
        for _ in range(diff):
            pointer_tables[pointer_table_index].entries.append(TableEntry(file_index))
        rom.seek(main_pointer_table_offset + (4 * len(pointer_tables)) + (4 * pointer_table_index))
        rom.write((file_index + 1).to_bytes(4, "big"))
        pointer_tables[pointer_table_index].num_entries = file_index + 1

        # Update uncompressed pointer table entry
        size_file = ROMPointerFile(rom, TableNames.UncompressedFileSizes, pointer_table_index)
        if size_file.size > 0:
            print(f" - Expanding pointer table {pointer_table_index} from {size_file.size} bytes to {4 * (file_index + 1)} bytes")
            rom.seek(size_file.start)
            new_uncompressed_data = bytearray(rom.read(size_file.size))
            for d in range((4 * (file_index + 1)) - size_file.size):
                new_uncompressed_data.append(0)
            replaceROMFile(rom, TableNames.UncompressedFileSizes, pointer_table_index, bytes(new_uncompressed_data), 4 * (file_index + 1))

    pointer_tables[pointer_table_index].entries[file_index].new_sha1 = dataSHA1Hash

    if len(filename) > 0:
        pointer_tables[pointer_table_index].entries[file_index].filename = filename


def clampCompressedTextures(rom: BinaryIO, cap: int):
    """Clamps the size of pointer table 25 to reduce it's size to save space."""
    original_length = len(pointer_tables[TableNames.TexturesGeometry].entries)
    if original_length > cap:
        print(f"- Compressing pointer table 25 to {cap} entries")
        pointer_tables[TableNames.TexturesGeometry].entries = pointer_tables[TableNames.TexturesGeometry].entries[:cap]
        rom.seek(main_pointer_table_offset + (4 * len(pointer_tables)) + (4 * TableNames.TexturesGeometry))
        rom.write((cap).to_bytes(4, "big"))
        pointer_tables[TableNames.TexturesGeometry].num_entries = cap

        # Update uncompressed pointer table entry
        size_file = ROMPointerFile(rom, TableNames.UncompressedFileSizes, TableNames.TexturesGeometry)
        if size_file.size > 0:
            new_size = 4 * cap
            print(f" - Compressing pointer table 25 from {size_file.size} bytes to {new_size} bytes")
            rom.seek(size_file.start)
            new_uncompressed_data = bytearray(rom.read(new_size))
            replaceROMFile(rom, TableNames.UncompressedFileSizes, 25, bytes(new_uncompressed_data), new_size)


def shouldWritePointerTable(index: int):
    """Write to the pointer table."""
    # Table 6 is nonsense.
    # This fixes heap corruption caused by a buffer overrun when decompressing a replaced file into a malloc'd buffer
    # if index == 6:
    #     return False

    # No need to recompute pointer tables with no entries in them
    if pointer_tables[index].num_entries == 0:
        return False

    if pointer_tables[index].force_rewrite:
        return True

    # TODO: Better logic for this
    if pointer_tables[index]:
        for y in pointer_tables[index].entries:
            if y.hasChanged():
                return True

    return False


def shouldRelocatePointerTable(index: int):
    """Relocate the pointer table."""
    # TODO: Remove this once deduplication is implemented
    # Note: Always relocate tables which contain bit_set entries, so cannot be rewritten in place until deduplication works properly
    if pointer_tables[index].force_relocate:
        return True

    return getPointerTableCompressedSize(index) > pointer_tables[index].original_compressed_size


def allocateSpace(size: int) -> int:
    """Allocate space for pointer table in ROM. Aim for location with least slack."""
    free_location = None
    slack = 0x4000000
    for index, location in enumerate(available_writes):
        available_space = location[1] - location[0]
        if available_space > size:
            proposed_slack = available_space - size
            if proposed_slack < slack:
                slack = proposed_slack
                free_location = index
    return free_location


def writeModifiedPointerTablesToROM(fh: BinaryIO):
    """Write the modified pointer tables to the rom file."""
    global available_writes

    # Reserve pointer table space and write new data
    for x in pointer_tables[::-1]:  # Enumerate backwards since ptr 25 is the biggest table. Makes for smaller ROM. TODO: Calculate order dynamically
        if not shouldWritePointerTable(x.index):
            continue

        # Get new size of entire table
        data_size = 0
        for y in x.entries:
            file_info = getFileInfo(x.index, y.index)
            if file_info:
                if len(file_info.data) > 0:
                    data_size += len(file_info.data)

        # Reserve free space for the pointer table in ROM
        space_required = x.num_entries * 4 + 4
        should_relocate = shouldRelocatePointerTable(x.index)
        write_allocation = None
        start_location = x.new_absolute_address
        if should_relocate:
            write_allocation = allocateSpace(space_required + data_size)
            x.new_absolute_address = available_writes[write_allocation][0]

        write_pointer = x.new_absolute_address + space_required
        earliest_file_address = write_pointer

        # Write all files to ROM
        for y in x.entries:
            file_info = getFileInfo(x.index, y.index)
            y.new_absolute_address = write_pointer
            if file_info:
                if len(file_info.data) > 0:
                    write_pointer += len(file_info.data)
                    fh.seek(y.new_absolute_address)
                    fh.write(file_info.data)

        # If the files have been appended to ROM, we need to move the free space pointer along by the number of bytes written
        if should_relocate:
            available_writes[write_allocation][0] += space_required  # For the pointer table itself
            available_writes[write_allocation][0] += write_pointer - earliest_file_address  # For all of the files
            # Add old pointer table location to available write locations
            available_writes.append([start_location, start_location + pointer_tables[x.index].original_compressed_size])

    # Recompute the pointer tables using the new file addresses and write them in the reserved space
    for x in reversed(pointer_tables):
        fh.seek(main_pointer_table_offset + (TableNames.UncompressedFileSizes * 4))
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
                next_pointer = y.new_absolute_address + len(file_info.data) - main_pointer_table_offset

                # Update the uncompressed filesize
                if y.hasChanged():
                    writeUncompressedSize(fh, x.index, y.index, file_info.uncompressed_size)
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


def dumpPointerTableDetails(filename: str, fr: BinaryIO, generate_json: bool):
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
            new_entry = {
                "index": int(len(entries)),
                "new_address": int(x.new_absolute_address + y.index * 4),
                "pointing_to": int(pointing_to),
                "compressed_size": int(len(file_info.data)) if file_info else None,
                "uncompressed_size": int(uncompressed_size) if uncompressed_size > 0 else None,
                "bit_set": y.bit_set,
                "map_index": maps[y.index] if x.num_entries == 221 else None,
                "file_name": y.filename,
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

    if generate_json:
        with open("../static/patches/pointer_addresses.json", "w") as fh:
            unneeded_table_keys = ["starting_byte", "ending_byte", "total_entries", "address", "name"]
            unneeded_file_keys = ["sha", "bit_set", "file_name", "map_index", "uncompressed_size", "new_address"]
            for table_index, table in enumerate(dataset):
                for k in unneeded_table_keys:
                    del table[k]
                for file in table["entries"]:
                    for k in unneeded_file_keys:
                        del file[k]
                    if table_index != 0:
                        del file["compressed_size"]
                        del file["index"]
            fh.write(json.dumps(dataset))


def dumpPointerTableDetailsLegacy(filename: str, fr: BinaryIO):
    """Dump the table details in the legacy log format."""
    with open(filename, "w") as fh:
        for x in pointer_tables:
            fh.write(
                str(x.index)
                + ": "
                + x.name
                + ": "
                + hex(x.new_absolute_address)
                + " ("
                + str(x.num_entries)
                + " entries, "
                + hex(x.original_compressed_size)
                + " -> "
                + hex(getPointerTableCompressedSize(x.index))
                + " bytes)"
            )
            fh.write("\n")
            for y in x.entries:
                fh.write(" - " + str(y.index) + ": ")
                fh.write(hex(x.new_absolute_address + y.index * 4) + " -> ")
                fr.seek(x.new_absolute_address + y.index * 4)
                pointing_to = (int.from_bytes(fr.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
                fh.write(hex(pointing_to))

                file_info = getFileInfo(x.index, y.index)
                if file_info:
                    fh.write(" (" + hex(len(file_info.data)) + ")")
                else:
                    fh.write(" WARNING: File info not found")

                uncompressed_size = getOriginalUncompressedSize(fr, x.index, y.index)
                if uncompressed_size > 0:
                    fh.write(" (" + hex(uncompressed_size) + ")")
                fh.write(" (" + str(y.bit_set) + ")")

                if x.num_entries == 221:
                    fh.write(" (" + maps[y.index] + ")")

                fh.write(" (" + str(y.new_sha1) + ")")

                if y.filename is not None:
                    fh.write(" (" + str(y.filename) + ")")

                fh.write("\n")
