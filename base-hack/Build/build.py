"""Build the ROM."""
import gzip
import os
import shutil
import subprocess
import zlib

import generate_watch_file

# Patcher functions for the extracted files
import patch_text
from convertSetup import convertSetup

# Infrastructure for recomputing DK64 global pointer tables
from map_names import maps
from recompute_overlays import (
    isROMAddressOverlay,
    readOverlayOriginalData,
    replaceOverlayData,
    writeModifiedOverlaysToROM,
)
from recompute_pointer_table import (
    dumpPointerTableDetails,
    getFileInfo,
    make_safe_filename,
    parsePointerTables,
    pointer_tables,
    replaceROMFile,
    writeModifiedPointerTablesToROM,
)
from staticcode import patchStaticCode

ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"

if os.path.exists(newROMName):
    os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

file_dict = [
    {
        "name": "Static ASM Code",
        "start": 0x113F0,
        "compressed_size": 0xB15E4,
        "source_file": "StaticCode.bin",
        "use_external_gzip": True,
        "patcher": patchStaticCode,
    },
    {
        "name": "Dolby Logo",
        "pointer_table_index": 14,
        "file_index": 176,
        "source_file": "assets/Non-Code/Dolby/DolbyThin.png",
        "texture_format": "ia4",
    },
    {
        "name": "Thumb Image",
        "pointer_table_index": 14,
        "file_index": 94,
        "source_file": "assets/Non-Code/Nintendo Logo/Nintendo.png",
        "texture_format": "rgba5551",
    },
    {
        "name": "DKTV Image",
        "pointer_table_index": 14,
        "file_index": 44,
        "source_file": "assets/Non-Code/DKTV/logo3.png",
        "texture_format": "rgba5551",
    },
    {
        "name": "Spin Transition Image",
        "pointer_table_index": 14,
        "file_index": 95,
        "source_file": "assets/Non-Code/transition/transition-body.png",
        "texture_format": "ia4",
    },
    {
        "name": "Moves Image",
        "pointer_table_index": 14,
        "file_index": 115,
        "source_file": "assets/Non-Code/file_screen/moves.png",
        "texture_format": "rgba5551",
    },
    {
        "name": "Blueprint Image",
        "pointer_table_index": 14,
        "file_index": 116,
        "source_file": "assets/Non-Code/file_screen/blueprint.png",
        "texture_format": "rgba5551",
    },
    {
        "name": "Isles Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 34,
        "source_file": "assets/Non-Code/instance_scripts/isles.bin",
        "bps_file": "assets/Non-Code/instance_scripts/isles.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Helm Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 17,
        "source_file": "assets/Non-Code/instance_scripts/helm.bin",
        "bps_file": "assets/Non-Code/instance_scripts/helm.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Galleon Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 0x1E,
        "source_file": "assets/Non-Code/instance_scripts/galleon.bin",
        "bps_file": "assets/Non-Code/instance_scripts/galleon.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Aztec Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 0x26,
        "source_file": "assets/Non-Code/instance_scripts/aztec.bin",
        "bps_file": "assets/Non-Code/instance_scripts/aztec.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Fungi Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 0x30,
        "source_file": "assets/Non-Code/instance_scripts/fungi.bin",
        "bps_file": "assets/Non-Code/instance_scripts/fungi.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Chunky Phase Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 207,
        "source_file": "assets/Non-Code/instance_scripts/chunky_phase.bin",
        "bps_file": "assets/Non-Code/instance_scripts/chunky_phase.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Diddy 5DC Upper Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 200,
        "source_file": "assets/Non-Code/instance_scripts/diddy_5dc_upper.bin",
        "bps_file": "assets/Non-Code/instance_scripts/diddy_5dc_upper.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Dungeon Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 163,
        "source_file": "assets/Non-Code/instance_scripts/dungeon.bin",
        "bps_file": "assets/Non-Code/instance_scripts/dungeon.bps",
        "is_diff_patch": True,
    },
    {
        "name": "Wind Tower Object Instance Scripts",
        "pointer_table_index": 10,
        "file_index": 105,
        "source_file": "assets/Non-Code/instance_scripts/wind_tower.bin",
        "bps_file": "assets/Non-Code/instance_scripts/wind_tower.bps",
        "is_diff_patch": True,
    },
]

map_replacements = []

for x in range(175):
    if x > 0:
        file_dict.append(
            {
                "name": "Song " + str(x),
                "pointer_table_index": 0,
                "file_index": x,
                "source_file": "song" + str(x) + ".bin",
                "target_compressed_size": 0x2DDE,
            }
        )
for x in range(6):
    file_dict.append(
        {
            "name": "DKTV Inputs " + str(x),
            "pointer_table_index": 17,
            "file_index": x,
            "source_file": "dktv" + str(x) + ".bin",
            "target_compressed_size": 0x718,
        }
    )
for x in range(221):
    file_dict.append(
        {
            "name": "Zones for map " + str(x),
            "pointer_table_index": 18,
            "file_index": x,
            "source_file": "lz" + str(x) + ".bin",
            "target_compressed_size": 0x850,
            "do_not_recompress": True,
        }
    )
for x in range(221):
    file_dict.append(
        {
            "name": "Setup for map " + str(x),
            "pointer_table_index": 9,
            "file_index": x,
            "source_file": "setup" + str(x) + ".bin",
            "target_compressed_size": 0x8000,
            "target_uncompressed_size": 0x8000,
            "do_not_recompress": True,
        }
    )
for x in range(8):
    file_dict.append(
        {
            "name": "Key " + str(x + 1) + " file screen",
            "pointer_table_index": 14,
            "file_index": 107 + x,
            "source_file": "assets/Non-Code/file_screen/key" + str(x + 1) + ".png",
            "texture_format": "rgba5551",
        }
    )
for x in range(43):
    if x != 13:
        file_dict.append(
            {
                "name": "Text " + str(x),
                "pointer_table_index": 12,
                "file_index": x,
                "source_file": "text" + str(x) + ".bin",
                "target_compressed_size": 0x2000,
                "target_uncompressed_size": 0x2000,
                "do_not_recompress": True,
            }
        )
file_dict.append(
    {
        "name": "Dolby Text",
        "pointer_table_index": 12,
        "file_index": 13,
        "source_file": "dolby_text.bin",
        "do_not_compress": True,
        "do_not_delete_source": True,
    },
)


print("DK64 Extractor")

with open(ROMName, "rb") as fh:
    print("[1 / 7] - Parsing pointer tables")
    parsePointerTables(fh)
    readOverlayOriginalData(fh)

    for x in map_replacements:
        print(" - Processing map replacement " + x["name"])
        if os.path.exists(x["map_folder"]):
            found_geometry = False
            found_floors = False
            found_walls = False
            should_compress_walls = True
            should_compress_floors = True
            for y in pointer_tables:
                if "encoded_filename" not in y:
                    continue

                # Convert decoded_filename to encoded_filename using the encoder function
                # Eg. exits.json to exits.bin
                if "encoder" in y and callable(y["encoder"]):
                    if "decoded_filename" in y and os.path.exists(x["map_folder"] + y["decoded_filename"]):
                        y["encoder"](x["map_folder"] + y["decoded_filename"], x["map_folder"] + y["encoded_filename"])

                if os.path.exists(x["map_folder"] + y["encoded_filename"]):
                    if y["index"] == 1:
                        with open(x["map_folder"] + y["encoded_filename"], "rb") as fg:
                            byte_read = fg.read(10)
                            should_compress_walls = (byte_read[9] & 0x1) != 0
                            should_compress_floors = (byte_read[9] & 0x2) != 0
                        found_geometry = True
                    elif y["index"] == 2:
                        found_walls = True
                    elif y["index"] == 3:
                        found_floors = True

            # Check that all walls|floors|geometry files exist on disk, or that none of them do
            walls_floors_geometry_valid = (found_geometry == found_walls) and (found_geometry == found_floors)

            if not walls_floors_geometry_valid:
                print("  - WARNING: In map replacement: " + x["name"])
                print("    - Need all 3 files present to replace walls, floors, and geometry.")
                print("    - Only found 1 or 2 of them out of 3. Make sure all 3 exist on disk.")
                print("    - Will skip replacing walls, floors, and geometry to prevent crashes.")

            for y in pointer_tables:
                if "encoded_filename" not in y:
                    continue

                if os.path.exists(x["map_folder"] + y["encoded_filename"]):
                    # Special case to prevent crashes with custom level geometry, walls, and floors
                    # Some of the files are compressed in ROM, some are not
                    if y["index"] in [1, 2, 3] and not walls_floors_geometry_valid:
                        continue

                    do_not_compress = "do_not_compress" in y and y["do_not_compress"]
                    if y["index"] == 2:
                        do_not_compress = not should_compress_walls
                    elif y["index"] == 3:
                        do_not_compress = not should_compress_floors

                    print("  - Found " + x["map_folder"] + y["encoded_filename"])
                    file_dict.append(
                        {
                            "name": x["name"] + y["name"],
                            "pointer_table_index": y["index"],
                            "file_index": x["map_index"],
                            "source_file": x["map_folder"] + y["encoded_filename"],
                            "do_not_extract": True,
                            "do_not_compress": do_not_compress,
                            "use_external_gzip": "use_external_gzip" in y and y["use_external_gzip"],
                        }
                    )

    print("[2 / 7] - Extracting files from ROM")
    for x in file_dict:
        # N64Tex conversions do not need to be extracted to disk from ROM
        if "texture_format" in x:
            x["do_not_extract"] = True
            x["output_file"] = x["source_file"].replace(".png", "." + x["texture_format"])

        if "output_file" not in x:
            x["output_file"] = x["source_file"]

        # gzip.exe appends .gz to the filename, we'll do the same
        if "use_external_gzip" in x and x["use_external_gzip"]:
            x["output_file"] = x["output_file"] + ".gz"

        # If we're not extracting the file to disk, we're using a custom .bin that shoudn't be deleted
        if "do_not_extract" in x and x["do_not_extract"]:
            x["do_not_delete_source"] = True

        # Extract the compressed file from ROM
        if not ("do_not_extract" in x and x["do_not_extract"]):
            byte_read = bytes()
            if "pointer_table_index" in x and "file_index" in x:
                file_info = getFileInfo(x["pointer_table_index"], x["file_index"])
                if file_info:
                    x["start"] = file_info["new_absolute_address"]
                    x["compressed_size"] = len(file_info["data"])

            fh.seek(x["start"])
            byte_read = fh.read(x["compressed_size"])

            if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
                if os.path.exists(x["source_file"]):
                    os.remove(x["source_file"])

                with open(x["source_file"], "wb") as fg:
                    dec = zlib.decompress(byte_read, 15 + 32)
                    fg.write(dec)

print("[3 / 7] - Patching Extracted Files")
for x in file_dict:
    if "patcher" in x and callable(x["patcher"]):
        print(" - Running patcher for " + x["source_file"])
        x["patcher"](x["source_file"])

with open(newROMName, "r+b") as fh:
    print("[4 / 7] - Writing patched files to ROM")
    for x in file_dict:
        if "target_compressed_size" in x:
            x["do_not_compress"] = True
            if x["source_file"][:5] == "setup":
                convertSetup(x["source_file"])
            with open(x["source_file"], "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            if "do_not_recompress" in x and x["do_not_recompress"]:
                compress = bytearray(byte_read)
                if "target_uncompressed_size" in x:
                    diff = x["target_uncompressed_size"] - len(byte_read)
                    byte_append = 0
                    if diff > 0:
                        byte_read += byte_append.to_bytes(diff, "big")
                    compress = bytearray(byte_read)
                    uncompressed_size = x["target_uncompressed_size"]
            else:
                precomp = gzip.compress(byte_read, compresslevel=9)
                byte_append = 0
                diff = x["target_compressed_size"] - len(precomp)
                if diff > 0:
                    precomp += byte_append.to_bytes(diff, "big")
                compress = bytearray(precomp)
                # Zero out timestamp in gzip header to make builds deterministic
                compress[4] = 0
                compress[5] = 0
                compress[6] = 0
                compress[7] = 0
            with open(x["source_file"], "wb") as fg:
                fg.write(compress)
            x["output_file"] = x["source_file"]

        if "is_diff_patch" in x and x["is_diff_patch"]:
            with open(x["source_file"], "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            subprocess.Popen(["build\\flips.exe", "--apply", x["bps_file"], x["source_file"], x["source_file"]]).wait()

        if "texture_format" in x:
            if x["texture_format"] in ["rgba5551", "i4", "ia4", "i8", "ia8"]:
                result = subprocess.check_output(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
            else:
                print(" - ERROR: Unsupported texture format " + x["texture_format"])

        if "use_external_gzip" in x and x["use_external_gzip"]:
            if os.path.exists(x["source_file"]):
                result = subprocess.check_output(["./build/gzip.exe", "-f", "-n", "-k", "-q", "-9", x["output_file"].replace(".gz", "")])
                if os.path.exists(x["output_file"]):
                    with open(x["output_file"], "r+b") as outputFile:
                        # Chop off gzip footer
                        outputFile.truncate(len(outputFile.read()) - 8)

        if os.path.exists(x["output_file"]):
            byte_read = bytes()
            if "target_compressed_size" not in x:
                uncompressed_size = 0
            with open(x["output_file"], "rb") as fg:
                byte_read = fg.read()
                if "target_compressed_size" not in x:
                    uncompressed_size = len(byte_read)

            if "do_not_compress" in x and x["do_not_compress"]:
                compress = bytearray(byte_read)
            elif "use_external_gzip" in x and x["use_external_gzip"]:
                compress = bytearray(byte_read)
            elif "use_zlib" in x and x["use_zlib"]:
                compressor = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, 25)
                compress = compressor.compress(byte_read)
                compress += compressor.flush()
                compress = bytearray(compress)
                # Zero out timestamp in gzip header to make builds deterministic
                compress[4] = 0
                compress[5] = 0
                compress[6] = 0
                compress[7] = 0
            else:
                compress = bytearray(gzip.compress(byte_read, compresslevel=9))
                # Zero out timestamp in gzip header to make builds deterministic
                compress[4] = 0
                compress[5] = 0
                compress[6] = 0
                compress[7] = 0

            print(" - Writing " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
            if "pointer_table_index" in x and "file_index" in x:
                # More complicated write, update the pointer tables to point to the new data
                replaceROMFile(x["pointer_table_index"], x["file_index"], compress, uncompressed_size)
            elif "start" in x:
                if isROMAddressOverlay(x["start"]):
                    replaceOverlayData(x["start"], compress)
                else:
                    # Simply write the bytes at the absolute address in ROM specified by x["start"]
                    fh.seek(x["start"])
                    fh.write(compress)
            else:
                print("  - WARNING: Can't find address information in file_dict entry to write " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
        else:
            print(x["output_file"] + " does not exist")

        # Cleanup temporary files
        if not ("do_not_delete" in x and x["do_not_delete"]):
            if not ("do_not_delete_output" in x and x["do_not_delete_output"]):
                if os.path.exists(x["output_file"]) and x["output_file"] != x["source_file"]:
                    os.remove(x["output_file"])
            if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
                if os.path.exists(x["source_file"]):
                    os.remove(x["source_file"])

    print("[5 / 7] - Writing recomputed pointer tables to ROM")
    writeModifiedPointerTablesToROM(fh)
    writeModifiedOverlaysToROM(fh)

    print("[6 / 7] - Dumping details of all pointer tables to rom/build.log")
    dumpPointerTableDetails("rom/build.log", fh)

    # for x in file_dict:
    #     if "is_diff_patch" in x and x["is_diff_patch"]:
    #         if os.path.exists(x["source_file"]):
    #             os.remove(x["source_file"])

    # Wipe Space
    fh.seek(0x1FED020)
    arr = []
    for x in range(0x200):
        arr.append(0)
    fh.write(bytearray(arr))

print("[7 / 7] - Generating BizHawk RAM watch")

exit()
