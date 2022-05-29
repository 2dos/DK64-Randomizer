"""Build the ROM."""
import gzip
import os
import shutil
import subprocess
import sys
import zlib

import generate_watch_file

# Patcher functions for the extracted files
import patch_text
from adjust_exits import adjustExits
from convertPortalImage import convertPortalImage
from convertSetup import convertSetup

# Infrastructure for recomputing DK64 global pointer tables
from map_names import maps
from populateSongData import writeVanillaSongData
from recompute_overlays import isROMAddressOverlay, readOverlayOriginalData, replaceOverlayData, writeModifiedOverlaysToROM
from recompute_pointer_table import dumpPointerTableDetails, getFileInfo, make_safe_filename, parsePointerTables, pointer_tables, replaceROMFile, writeModifiedPointerTablesToROM
from replace_simslam_text import replaceSimSlam
from staticcode import patchStaticCode
from vanilla_move_data import writeVanillaMoveData
from image_converter import convertToRGBA32
from end_seq_writer import createTextFile, createSquishFile
from instance_script_maps import instance_script_maps
from generate_yellow_wrinkly import generateYellowWrinkly

ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"

if os.path.exists(newROMName):
    os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

portal_images = []
portal_images.append(convertPortalImage("assets/Non-Code/portals/DK_rando_portal_1.png"))
portal_images.append(convertPortalImage("assets/Non-Code/portals/DK_rando_portal_2.png"))

createTextFile("assets/Non-Code/credits")
createSquishFile("assets/Non-Code/credits")
generateYellowWrinkly()

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
        "name": "Tag Barrel Shell Texture",
        "pointer_table_index": 25,
        "file_index": 4938,
        "source_file": "assets/Non-Code/tagbarrel/shell.png",
        "texture_format": "rgba5551",
    },
    {
        "name": "Gong Geometry",
        "pointer_table_index": 4,
        "file_index": 195,
        "source_file": "assets/Non-Code/Gong/gong_geometry.bin",
        "bps_file": "assets/Non-Code/Gong/gong_geometry.bps",
        "is_diff_patch": True,
    },
    {
        "name": "No Face",
        "pointer_table_index": 14,
        "file_index": 0x21,
        "source_file": "assets/Non-Code/displays/none.png",
        "texture_format": "rgba32",
    },
    {
        "name": "DK Face",
        "pointer_table_index": 14,
        "file_index": 0x22,
        "source_file": "assets/Non-Code/displays/dk_face.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Diddy Face",
        "pointer_table_index": 14,
        "file_index": 0x23,
        "source_file": "assets/Non-Code/displays/diddy_face.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Lanky Face",
        "pointer_table_index": 14,
        "file_index": 0x24,
        "source_file": "assets/Non-Code/displays/lanky_face.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Tiny Face",
        "pointer_table_index": 14,
        "file_index": 0x25,
        "source_file": "assets/Non-Code/displays/tiny_face.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Chunky Face",
        "pointer_table_index": 14,
        "file_index": 0x26,
        "source_file": "assets/Non-Code/displays/chunky_face.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Shared Face",
        "pointer_table_index": 14,
        "file_index": 0x27,
        "source_file": "assets/Non-Code/displays/shared.png",
        "texture_format": "rgba32",
    },
    {
        "name": "Sold Out Face",
        "pointer_table_index": 14,
        "file_index": 0x28,
        "source_file": "assets/Non-Code/displays/soldout32.png",
        "texture_format": "rgba32",
    },
    {
        "name": "End Sequence Credits",
        "pointer_table_index": 19,
        "file_index": 7,
        "source_file": "assets/Non-Code/credits/credits.bin",
        "do_not_delete_source": True,
    },
    {
        "name": "DK Wrinkly Door",
        "pointer_table_index": 4,
        "file_index": 0xF0,
        "source_file": "assets/Non-Code/Gong/hint_door.bin",
        "do_not_delete_source": True,
    },
    {"name": "WXY_Slash", "pointer_table_index": 14, "file_index": 12, "source_file": "assets/Non-Code/displays/wxys.png", "texture_format": "rgba5551"},
]

map_replacements = []
song_replacements = [
    {"name": "baboon_balloon", "index": 107},
    {"name": "bonus_minigames", "index": 8},
    {"name": "dk_rap", "index": 75},
    {"name": "failure_races_try_again", "index": 87},
    {"name": "move_get", "index": 114},
    {"name": "nintendo_logo", "index": 174},
    {"name": "success_races", "index": 86},
]
changed_song_indexes = []

# for song in song_replacements:
#     file_dict.append(
#         {
#             "name": song["name"].replace("_", " "),
#             "pointer_table_index": 0,
#             "file_index": song["index"],
#             "source_file": f"assets/Non-Code/music/{song['name']}.bin",
#             "bps_file": f"assets/Non-Code/music/{song['name']}.bps",
#             "target_compressed_size": 0x2DDE,
#             "is_diff_patch": True,
#         }
#     )
#     changed_song_indexes.append(song["index"])

for x in instance_script_maps:
    file_dict.append(
        {
            "name": f"{x['name'].replace('_',' ')} Instance Scripts",
            "pointer_table_index": 10,
            "file_index": x["map"],
            "source_file": f"assets/Non-Code/instance_scripts/{x['name']}.bin",
            "bps_file": f"assets/Non-Code/instance_scripts/{x['name']}.bps",
            "is_diff_patch": True,
        }
    )

for x in range(175):
    if x > 0:
        if x not in changed_song_indexes:
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
for x in range(221):
    file_dict.append(
        {
            "name": "Character Spawners for map " + str(x),
            "pointer_table_index": 16,
            "file_index": x,
            "source_file": "charspawners" + str(x) + ".bin",
            "target_compressed_size": 0x1000,
            "target_uncompressed_size": 0x1000,
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
        if x != 32:
            if x != 0x18:
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
for x in range(10):
    file_dict.append(
        {
            "name": f"Tag Barrel Bottom Texture ({x+1})",
            "pointer_table_index": 25,
            "file_index": 4749 + x,
            "source_file": "assets/Non-Code/tagbarrel/bottom.png",
            "texture_format": "rgba5551",
        }
    )
barrel_faces = ["Dk", "Diddy", "Lanky", "Tiny", "Chunky"]
barrel_offsets = [4817, 4815, 4819, 4769, 4747]
for x in range(5):
    for y in range(2):
        file_dict.append(
            {
                "name": f"{barrel_faces[x]} Transform Barrel Shell ({y+1})",
                "pointer_table_index": 25,
                "file_index": barrel_offsets[x] + y,
                "source_file": f"assets/Non-Code/tagbarrel/{barrel_faces[x]} barrel {y}a.png",
                "texture_format": "rgba5551",
            }
        )
portal_image_order = [
    ["SE", "NE", "SW", "NW"],
    ["NW", "SW", "NE", "SE"],
]
for x in range(2):
    order = portal_image_order[x]
    image_series = portal_images[x]
    for y in range(4):
        segment = order[y]
        found_image = ""
        for image in image_series:
            if segment in image:
                found_image = image
        if found_image != "":
            file_dict.append(
                {
                    "name": f"Portal Image {x+1} - {segment}",
                    "pointer_table_index": 7,
                    "file_index": 931 + (4 * x) + y,
                    "source_file": found_image,
                    "texture_format": "rgba5551",
                    "do_not_compress": True,
                }
            )

hash_icons = ["bongos.png", "crown.png", "dkcoin.png", "fairy.png", "guitar.png", "nin_coin.png", "orange.png", "rainbow_coin.png", "rw_coin.png", "sax.png"]
hash_indexes = [48, 49, 50, 51, 55, 62, 63, 64, 65, 76]
for x in range(len(hash_indexes)):
    idx = hash_indexes[x]
    file_dict.append({"name": f"Hash Icon {x+1}", "pointer_table_index": 14, "file_index": idx, "source_file": f"assets/Non-Code/hash/{hash_icons[x]}", "texture_format": "rgba5551"})
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
file_dict.append(
    {
        "name": "Custom Text",
        "pointer_table_index": 12,
        "file_index": 32,
        "source_file": "custom_text.bin",
        "do_not_compress": True,
        "do_not_delete_source": True,
    },
)
file_dict.append(
    {
        "name": "DK Text",
        "pointer_table_index": 12,
        "file_index": 0x18,
        "source_file": "dk_text.bin",
        "do_not_compress": True,
        "do_not_delete_source": True,
    }
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
            if "start" not in x:
                print(x)
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
        if "is_diff_patch" in x and x["is_diff_patch"]:
            with open(x["source_file"], "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            subprocess.Popen(["build\\flips.exe", "--apply", x["bps_file"], x["source_file"], x["source_file"]]).wait()
            # shutil.copyfile(x["source_file"],x["source_file"].replace(".bin",".raw"))

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

        if "texture_format" in x:
            if x["texture_format"] in ["rgba5551", "i4", "ia4", "i8", "ia8"]:
                result = subprocess.check_output(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
            elif x["texture_format"] == "rgba32":
                convertToRGBA32(x["source_file"])
                x["source_file"] = x["source_file"].replace(".png", ".rgba32")
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

    # Replace Helm Text
    main_pointer_table_offset = 0x101C50
    fh.seek(main_pointer_table_offset + (12 * 4))
    text_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(text_table + (19 * 4))
    misc_text = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(misc_text + 0x750)
    fh.write(("?").encode("ascii"))
    for i in range(0x15):
        fh.write(("\0").encode("ascii"))
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
    writeVanillaMoveData(fh)
    adjustExits(fh)
    replaceSimSlam(fh)
    writeVanillaSongData(fh)
    for x in portal_images:
        for y in x:
            if os.path.exists(y):
                os.remove(y)
    fh.seek(0x1FED020 + 0x141)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x142)
    fh.write((1).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x143)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x144)
    fh.write((2).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x145)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x146)
    fh.write((3).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x147)
    fh.write((1).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x148)
    fh.write((4).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x149)
    fh.write((2).to_bytes(1, "big"))

    fh.seek(0x1FED020 + 0x13B)
    fh.write((1).to_bytes(1, "big"))

    with open("assets/Non-Code/credits/squish.bin", "rb") as squish:
        fh.seek(0x1FFF800)
        fh.write(squish.read())

    vanilla_coin_reqs = [
        {"offset": 0x12C, "coins": 50},
        {"offset": 0x12D, "coins": 50},
        {"offset": 0x12E, "coins": 10},
        {"offset": 0x12F, "coins": 10},
        {"offset": 0x130, "coins": 10},
        {"offset": 0x131, "coins": 50},
        {"offset": 0x132, "coins": 50},
        {"offset": 0x133, "coins": 25},
    ]
    for coinreq in vanilla_coin_reqs:
        fh.seek(0x1FED020 + coinreq["offset"])
        fh.write(coinreq["coins"].to_bytes(1, "big"))
    for x in hash_icons:
        pth = f"assets/Non-Code/hash/{x}"
        if os.path.exists(pth):
            os.remove(pth)
    other_remove = []
    displays = ["dk_face", "diddy_face", "lanky_face", "tiny_face", "chunky_face", "none", "shared", "soldout32", "wxys", "yellow_qmark_0", "yellow_qmark_1"]
    for disp in displays:
        for ext in [".png", ".rgba32"]:
            other_remove.append(f"displays/{disp}{ext}")
    for x in range(8):
        other_remove.append(f"file_screen/key{x+1}.png")
    for x in other_remove:
        pth = f"assets/Non-Code/{x}"
        if os.path.exists(pth):
            os.remove(pth)
    credits_bins = ["credits", "squish"]
    for x in credits_bins:
        pth = f"assets/Non-Code/credits/{x}.bin"
        if os.path.exists(pth):
            os.remove(pth)
    if os.path.exists("assets/Non-Code/Gong/hint_door.bin"):
        os.remove("assets/Non-Code/Gong/hint_door.bin")
    # pth = "assets/Non-Code/displays/soldout_bismuth.rgba32"
    # if os.path.exists(pth):
    #     os.remove(pth)

print("[7 / 7] - Generating BizHawk RAM watch")

sys.exit()
