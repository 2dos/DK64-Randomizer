"""Build the ROM."""
import gzip
import json
import os
import shutil
import subprocess
import sys
import zlib

import create_helm_geo
import generate_watch_file
import shop_instance_script  # HAS TO BE BEFORE `instance_script_maker`
from writeWarpData import generateDefaultPadPairing  # HAS TO BE BEFORE `instance_script_maker`
import portal_instance_script  # HAS TO BE BEFORE `instance_script_maker`
import instance_script_maker
import model_fix
import generate_disco_models
import model_port

# Patcher functions for the extracted files
import patch_text
from adjust_exits import adjustExits
from convertPortalImage import convertPortalImage
from convertSetup import convertSetup
from end_seq_writer import createSquishFile, createTextFile
from generate_yellow_wrinkly import generateYellowWrinkly
from image_converter import convertToRGBA32

# Infrastructure for recomputing DK64 global pointer tables
from map_names import maps
from populateSongData import writeVanillaSongData
from recompute_overlays import isROMAddressOverlay, readOverlayOriginalData, replaceOverlayData, writeModifiedOverlaysToROM
from recompute_pointer_table import (
    dumpPointerTableDetails,
    getFileInfo,
    make_safe_filename,
    parsePointerTables,
    pointer_tables,
    replaceROMFile,
    writeModifiedPointerTablesToROM,
    clampCompressedTextures,
)
from staticcode import patchStaticCode
from vanilla_move_data import writeVanillaMoveData

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

BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something

file_dict = [
    {"name": "Static ASM Code", "start": 0x113F0, "compressed_size": 0xB15E4, "source_file": "StaticCode.bin", "use_external_gzip": True, "patcher": patchStaticCode},
    {"name": "Dolby Logo", "pointer_table_index": 14, "file_index": 176, "source_file": "assets/Non-Code/Dolby/DolbyThin.png", "texture_format": "ia4"},
    {"name": "Thumb Image", "pointer_table_index": 14, "file_index": 94, "source_file": "assets/Non-Code/Nintendo Logo/Nintendo4.png", "texture_format": "rgba5551"},
    {"name": "DKTV Image", "pointer_table_index": 14, "file_index": 44, "source_file": "assets/Non-Code/DKTV/logo3.png", "texture_format": "rgba5551"},
    {"name": "Spin Transition Image", "pointer_table_index": 14, "file_index": 95, "source_file": "assets/Non-Code/transition/transition-body.png", "texture_format": "ia4"},
    {"name": "Moves Image", "pointer_table_index": 14, "file_index": 115, "source_file": "assets/Non-Code/file_screen/moves.png", "texture_format": "rgba5551"},
    {"name": "Medal Image", "pointer_table_index": 14, "file_index": 116, "source_file": "assets/Non-Code/displays/medal.png", "texture_format": "rgba5551"},
    {"name": "Tag Barrel Shell Texture", "pointer_table_index": 25, "file_index": 4938, "source_file": "assets/Non-Code/tagbarrel/shell.png", "texture_format": "rgba5551"},
    {
        "name": "Gong Geometry",
        "pointer_table_index": 4,
        "file_index": 195,
        "source_file": "assets/Non-Code/Gong/gong_geometry.bin",
        "bps_file": "assets/Non-Code/Gong/gong_geometry.bps",
        "is_diff_patch": True,
    },
    {"name": "End Sequence Credits", "pointer_table_index": 19, "file_index": 7, "source_file": "assets/Non-Code/credits/credits.bin", "do_not_delete_source": True},
    {"name": "DK Wrinkly Door", "pointer_table_index": 4, "file_index": 0xF0, "source_file": "assets/Non-Code/Gong/hint_door.bin", "do_not_delete_source": True},
    {"name": "WXY_Slash", "pointer_table_index": 14, "file_index": 12, "source_file": "assets/Non-Code/displays/wxys.png", "texture_format": "rgba5551"},
    {
        "name": "DK Tie Palette",
        "pointer_table_index": 25,
        "file_index": 6013,
        "source_file": "assets/Non-Code/hash/dk_tie_palette.png",
        "do_not_extract": True,
        "texture_format": "rgba5551",
        "target_compressed_size": BLOCK_COLOR_SIZE,
    },
    {
        "name": "Tiny Overalls Palette",
        "pointer_table_index": 25,
        "file_index": 6014,
        "source_file": "assets/Non-Code/hash/tiny_palette.png",
        "do_not_extract": True,
        "texture_format": "rgba5551",
        "target_compressed_size": BLOCK_COLOR_SIZE,
    },
    {"name": "DPad Image", "pointer_table_index": 14, "file_index": 187, "source_file": "assets/Non-Code/displays/dpad.png", "texture_format": "rgba5551"},
    {"name": "Tracker Image", "pointer_table_index": 14, "file_index": 0xA1, "source_file": "assets/Non-Code/file_screen/tracker.png", "texture_format": "rgba5551"},
    {"name": "Nintendo Coin Model", "pointer_table_index": 4, "file_index": 0x48, "source_file": "nintendo_coin_om2.bin", "do_not_delete_source": True},
    {"name": "Rareware Coin Model", "pointer_table_index": 4, "file_index": 0x28F, "source_file": "rareware_coin_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (DK) Model", "pointer_table_index": 4, "file_index": 0x5B, "source_file": "potion_dk_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (Diddy) Model", "pointer_table_index": 4, "file_index": 0x1F2, "source_file": "potion_diddy_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (Lanky) Model", "pointer_table_index": 4, "file_index": 0x59, "source_file": "potion_lanky_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (Tiny) Model", "pointer_table_index": 4, "file_index": 0x1F3, "source_file": "potion_tiny_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (Chunky) Model", "pointer_table_index": 4, "file_index": 0x1F5, "source_file": "potion_chunky_om2.bin", "do_not_delete_source": True},
    {"name": "Potion (Any) Model", "pointer_table_index": 4, "file_index": 0x1F6, "source_file": "potion_any_om2.bin", "do_not_delete_source": True},
    {"name": "Krusha Head", "start": 0x1FF6000, "source_file": "assets/Non-Code/displays/krusha_head64.png", "do_not_delete_source": True, "texture_format": "rgba5551", "do_not_compress": True},
]

number_game_changes = [
    {"number": 6, "state": "unlit", "texture": 520},
    {"number": 6, "state": "lit", "texture": 521},
    {"number": 9, "state": "unlit", "texture": 526},
    {"number": 9, "state": "lit", "texture": 527},
]
for num in number_game_changes:
    file_dict.append(
        {
            "name": f"Number Game ({num['number']}, {num['state']})",
            "pointer_table_index": 7,
            "file_index": num["texture"],
            "source_file": f"assets/Non-Code/displays/num_{num['number']}_{num['state']}.png",
            "texture_format": "rgba5551",
            "do_not_compress": True,
        }
    )
for x in range(5):
    file_dict.append(
        {
            "name": f"Blueprint Model ({x})",
            "pointer_table_index": 4,
            "file_index": 0xDD + x,
            "source_file": f"blueprint{x}.bin",
            "do_not_delete_source": True,
        }
    )
for x in range(0x5A, 0x5E):
    file_dict.append({"name": f"Melon Slice ({hex(x)})", "pointer_table_index": 14, "file_index": x, "source_file": f"melon{x}.bin", "target_compressed_size": 48 * 42 * 2})

for ci, coin in enumerate(["nin_coin", "rw_coin"]):
    for item in range(2):
        file_dict.append(
            {
                "name": f"{coin.replace('_',' ').capitalize()} ({item})",
                "pointer_table_index": 25,
                "file_index": 6015 + item + (2 * ci),
                "source_file": f"assets/Non-Code/hash/{coin}_{item}.png",
                "do_not_extract": True,
                "texture_format": "rgba5551",
            }
        )
file_dict.append(
    {"name": "Special Coin Side", "pointer_table_index": 25, "file_index": 6019, "source_file": f"assets/Non-Code/hash/modified_coin_side.png", "do_not_extract": True, "texture_format": "rgba5551"}
)

kong_names = ["DK", "Diddy", "Lanky", "Tiny", "Chunky"]
ammo_names = ["standard_crate", "homing_crate"]

for ammo_index, ammo in enumerate(ammo_names):
    file_dict.append(
        {"name": f"{ammo.replace('_',' ')} Image", "pointer_table_index": 14, "file_index": 188 + ammo_index, "source_file": f"assets/Non-Code/displays/{ammo}.png", "texture_format": "rgba5551"}
    )

for kong_index, kong in enumerate(kong_names):
    file_dict.append(
        {
            "name": f"DPad - {kong} Face",
            "pointer_table_index": 14,
            "file_index": 190 + kong_index,
            "source_file": f"assets/Non-Code/displays/{kong.lower()}_face.png",
            "texture_format": "rgba5551",
            "target_compressed_size": 32 * 32 * 2,
        }
    )

shop_face_array = [
    "none",  # No Face
    "dk_face",
    "diddy_face",
    "lanky_face",
    "tiny_face",
    "chunky_face",
    "shared",  # Shared Move
    "soldout32",  # Sold Out
    "gb",
    "dk_bp",
    "crown_shop",
    "key",
    "medal",
    "potion32",
    "nin_coin",
    "rw_coin",
]
for x, shop in enumerate(shop_face_array):
    data = {"name": f"Shop Indicator ({shop})", "pointer_table_index": 14, "file_index": 195 + x, "source_file": f"assets/Non-Code/displays/{shop}.png", "texture_format": "rgba32"}
    if "_face" in shop:
        data["target_compressed_size"] = 32 * 32 * 4
    file_dict.append(data)

base_coin_sfx = "assets/Non-Code/music/Win95_startup.dk64song"
new_coin_sfx = "assets/Non-Code/music/coin_sfx.bin"
if os.path.exists(new_coin_sfx):
    os.remove(new_coin_sfx)
shutil.copyfile(base_coin_sfx, new_coin_sfx)

map_replacements = []
song_replacements = [
    {"name": "baboon_balloon", "index": 107, "bps": True},
    {"name": "bonus_minigames", "index": 8, "bps": True},
    {"name": "dk_rap", "index": 75, "bps": True},
    {"name": "failure_races_try_again", "index": 87, "bps": True},
    {"name": "move_get", "index": 114, "bps": True},
    {"name": "nintendo_logo", "index": 174, "bps": True},
    {"name": "success_races", "index": 86, "bps": True},
    {"name": "klumsy_celebration", "index": 125, "bps": True},
    {"name": "coin_sfx", "index": 7, "bps": False},
]
changed_song_indexes = []

for song in song_replacements:
    item = {"name": song["name"].replace("_", " "), "pointer_table_index": 0, "file_index": song["index"], "source_file": f"assets/Non-Code/music/{song['name']}.bin", "target_compressed_size": 0x2DDE}
    if song["bps"]:
        item["is_diff_patch"] = True
        item["bps_file"] = f"assets/Non-Code/music/{song['name']}.bps"
    else:
        item["do_not_delete_source"] = True
        item["do_not_extract"] = True
    file_dict.append(item)
    changed_song_indexes.append(song["index"])

# Instance Scripts
with open("./instance_scripts_data.json", "r") as json_f:
    instance_script_maps = json.load(json_f)
maps_to_expand = list(range(0, 216))
script_expansion_size = 0x200
for x in instance_script_maps:
    maps_to_expand.remove(x["map"])
    script_file_name = f"{x['name']}.raw"
    expand_size = 0x2000
    with open(script_file_name, "rb") as script_f:
        data = script_f.read()
        compress = gzip.compress(data, compresslevel=9)
        expand_size = len(data) + script_expansion_size
    file_dict.append(
        {
            "name": f"{x['name'].replace('_',' ')} Instance Scripts",
            "pointer_table_index": 10,
            "file_index": x["map"],
            "source_file": script_file_name,
            "target_compressed_size": expand_size,
            "target_uncompressed_size": expand_size,
            "do_not_recompress": True,
            "do_not_delete_source": True,
        }
    )
for x in maps_to_expand:
    with open(ROMName, "rb") as fh:
        fh.seek(0x101C50 + (10 * 4))
        script_table = 0x101C50 + int.from_bytes(fh.read(4), "big")
        fh.seek(script_table + (x * 4))
        item_start = 0x101C50 + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        item_end = 0x101C50 + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        fh.seek(item_start)
        is_compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
        item_size = item_end - item_start
        if is_compressed:
            fh.seek(item_start)
            data = fh.read(item_size)
            data = zlib.decompress(data, (15 + 32))
            item_size = len(data)
        file_dict.append(
            {
                "name": f"Script {x}",
                "pointer_table_index": 10,
                "file_index": x,
                "source_file": f"script{x}.bin",
                "target_compressed_size": item_size + script_expansion_size,
                "target_uncompressed_size": item_size + script_expansion_size,
                "do_not_recompress": True,
            }
        )

for x in range(175):
    if x > 0:
        if x not in changed_song_indexes:
            file_dict.append({"name": "Song " + str(x), "pointer_table_index": 0, "file_index": x, "source_file": "song" + str(x) + ".bin", "target_compressed_size": 0x2DDE})
for x in range(6):
    file_dict.append({"name": "DKTV Inputs " + str(x), "pointer_table_index": 17, "file_index": x, "source_file": "dktv" + str(x) + ".bin", "target_compressed_size": 0x718})
for x in range(221):
    file_dict.append({"name": "Zones for map " + str(x), "pointer_table_index": 18, "file_index": x, "source_file": "lz" + str(x) + ".bin", "target_compressed_size": 0x850, "do_not_recompress": True})
# Setup
setup_expansion_size = 0x12C0
for x in range(221):
    local_expansion = setup_expansion_size
    if x in (0, 1, 2, 5, 9, 15, 0x19):
        local_expansion = 0
    with open(ROMName, "rb") as fh:
        setup_tbl_index = 9
        fh.seek(0x101C50 + (setup_tbl_index * 4))
        script_table = 0x101C50 + int.from_bytes(fh.read(4), "big")
        fh.seek(script_table + (x * 4))
        item_start = 0x101C50 + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        item_end = 0x101C50 + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
        fh.seek(item_start)
        is_compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
        item_size = item_end - item_start
        if is_compressed:
            fh.seek(item_start)
            data = fh.read(item_size)
            data = zlib.decompress(data, (15 + 32))
            item_size = len(data)
        file_dict.append(
            {
                "name": "Setup for map " + str(x),
                "pointer_table_index": 9,
                "file_index": x,
                "source_file": "setup" + str(x) + ".bin",
                "target_compressed_size": item_size + local_expansion,
                "target_uncompressed_size": item_size + local_expansion,
                "do_not_recompress": True,
            }
        )
for x in range(221):
    if x != 2:  # DK Arcade path file is massive
        file_dict.append(
            {
                "name": "Paths for map " + str(x),
                "pointer_table_index": 15,
                "file_index": x,
                "source_file": "paths" + str(x) + ".bin",
                "target_uncompressed_size": 0x600,
                "target_compressed_size": 0x600,
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
            "target_compressed_size": 0x1400,
            "target_uncompressed_size": 0x1400,
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
    if x not in (13, 32, 0x18, 0x27, 8, 37, 2):
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
        {"name": f"Tag Barrel Bottom Texture ({x+1})", "pointer_table_index": 25, "file_index": 4749 + x, "source_file": "assets/Non-Code/tagbarrel/bottom.png", "texture_format": "rgba5551"}
    )
for x in range(4761, 4768):
    file_dict.append({"name": f"Portal Ripple Texture ({x})", "pointer_table_index": 25, "file_index": x, "source_file": f"assets/Non-Code/displays/empty11.png", "texture_format": "rgba5551"})
for x in range(0xB50, 0xB56):
    file_dict.append({"name": f"Unused Texture ({x})", "pointer_table_index": 25, "file_index": x, "source_file": f"assets/Non-Code/displays/empty11.png", "texture_format": "rgba5551"})
for x in range(0xDD1, 0xDD6):
    file_dict.append({"name": f"Unused Texture ({x})", "pointer_table_index": 25, "file_index": x, "source_file": f"assets/Non-Code/displays/empty11.png", "texture_format": "rgba5551"})
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


kong_palettes = {
    0xE8C: [(32, 32), "block"],  # DK Base
    0xE66: [(32, 32), "block"],  # Diddy Cap/Shirt
    0xE69: [(32, 32), "block"],  # Lanky Overalls
    0xEB9: [(43, 32), "checkered"],  # Chunky Checkered Shirt
    0xE67: [(32, 32), "block"],  # Chunky Shirt Front
    3826: [(32, 32), "block"],  # Rambi
    3847: [(32, 32), "block"],  # Enguarde
    3734: [(43, 32), "checkered"],  # Lanky Patch
    3777: [(32, 32), "sparkle"],  # Disco Shirt
    3778: [(32, 32), "sparkle"],  # Disco Gloves
    4971: [(32, 32), "block"],  # Krusha Skin
    4966: [(32, 32), "block"],  # Krusha Belt
}
for x in kong_palettes:
    x_s = kong_palettes[x][0][0] * kong_palettes[x][0][1] * 2
    if kong_palettes[x][0][0] == 32 and kong_palettes[x][0][1] == 32 and kong_palettes[x][1] == "block":
        x_s = BLOCK_COLOR_SIZE
    file_dict.append({"name": f"Palette Expansion ({hex(x)})", "pointer_table_index": 25, "file_index": x, "source_file": f"palette_{x}.bin", "target_compressed_size": x_s})

for tex in range(0x273, 0x27D):
    file_dict.append({"name": f"Head Expansion ({hex(tex)})", "pointer_table_index": 25, "file_index": tex, "source_file": f"head_{tex}.bin", "target_compressed_size": 32 * 64 * 2})

colorblind_changes = [[4120, 4124, 32, 44], [5819, 5858, 32, 64]]
for change in colorblind_changes:
    for file_index in range(change[0], change[1] + 1):
        file_dict.append(
            {
                "name": f"Colorblind Expansion {file_index}",
                "pointer_table_index": 25,
                "file_index": file_index,
                "source_file": f"colorblind_exp_{file_index}.bin",
                "target_compressed_size": 2 * change[2] * change[3],
            }
        )


model_changes = [
    {"model_index": 0, "model_file": "diddy_base.bin"},
    {"model_index": 1, "model_file": "diddy_ins.bin"},
    {"model_index": 5, "model_file": "lanky_base.bin"},
    {"model_index": 6, "model_file": "lanky_ins.bin"},
    {"model_index": 3, "model_file": "dk_base.bin"},
    {"model_index": 8, "model_file": "tiny_base.bin"},
    {"model_index": 9, "model_file": "tiny_ins.bin"},
    {"model_index": 0xEC, "model_file": "disco_instrument.bin"},
    {"model_index": 0xDA, "model_file": "krusha_base.bin"},
    {"model_index": 0xED, "model_file": "potion_dk_om1.bin"},
    {"model_index": 0xEE, "model_file": "potion_diddy_om1.bin"},
    {"model_index": 0xEF, "model_file": "potion_lanky_om1.bin"},
    {"model_index": 0xF0, "model_file": "potion_tiny_om1.bin"},
    {"model_index": 0xF1, "model_file": "potion_chunky_om1.bin"},
    {"model_index": 0xF2, "model_file": "potion_any_om1.bin"},
    {"model_index": 0xA3, "model_file": "counter.bin"},
]
for x in model_changes:
    data = {"name": f"Model {x['model_index']}", "pointer_table_index": 5, "file_index": x["model_index"], "source_file": x["model_file"], "do_not_delete_source": True}
    if x["model_index"] > 0xEB:
        data["do_not_extract"] = True
    file_dict.append(data)

portal_image_order = [["SE", "NE", "SW", "NW"], ["NW", "SW", "NE", "SE"]]
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
file_dict.append({"name": "Dolby Text", "pointer_table_index": 12, "file_index": 13, "source_file": "dolby_text.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "Custom Text", "pointer_table_index": 12, "file_index": 32, "source_file": "custom_text.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "DK Text", "pointer_table_index": 12, "file_index": 0x18, "source_file": "dk_text.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "Move Names Text", "pointer_table_index": 12, "file_index": 0x27, "source_file": "move_names.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "Cranky Text", "pointer_table_index": 12, "file_index": 8, "source_file": "cranky_text.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "Menu Text", "pointer_table_index": 12, "file_index": 37, "source_file": "menu_text.bin", "do_not_compress": True, "do_not_delete_source": True})
file_dict.append({"name": "Kong Name Text", "pointer_table_index": 12, "file_index": 2, "source_file": "kongname_text.bin", "do_not_compress": True, "do_not_delete_source": True})

with open(ROMName, "rb") as fh:
    adjustExits(fh)

for x in range(216):
    if os.path.exists(f"exit{x}.bin"):
        file_dict.append({"name": f"Map {x} Exits", "pointer_table_index": 23, "file_index": x, "source_file": f"exit{x}.bin", "do_not_compress": True, "do_not_delete_source": True})

print("\nDK64 Extractor\nBuilt by Isotarge")

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
                    fh.seek(x["start"])
                    if int.from_bytes(fh.read(2), "big") == 0x1F8B:
                        dec = zlib.decompress(byte_read, 15 + 32)
                    else:
                        dec = byte_read
                    fg.write(dec)

print("[3 / 7] - Patching Extracted Files")
for x in file_dict:
    if "patcher" in x and callable(x["patcher"]):
        print(" - Running patcher for " + x["source_file"])
        x["patcher"](x["source_file"])

with open(newROMName, "r+b") as fh:
    print("[4 / 7] - Writing patched files to ROM")
    clampCompressedTextures(fh, 6030)
    for x in file_dict:
        if "is_diff_patch" in x and x["is_diff_patch"]:
            with open(x["source_file"], "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            subprocess.Popen(["build\\flips.exe", "--apply", x["bps_file"], x["source_file"], x["source_file"]]).wait()
            # shutil.copyfile(x["source_file"], x["source_file"].replace(".bin", ".raw"))

        if "texture_format" in x:
            if x["texture_format"] in ["rgba5551", "i4", "ia4", "i8", "ia8"]:
                result = subprocess.check_output(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
                if "target_compressed_size" in x:
                    x["source_file"] = x["source_file"].replace(".png", f".{x['texture_format']}")
            elif x["texture_format"] == "rgba32":
                convertToRGBA32(x["source_file"])
                x["source_file"] = x["source_file"].replace(".png", ".rgba32")
            else:
                print(" - ERROR: Unsupported texture format " + x["texture_format"])

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
                replaceROMFile(fh, x["pointer_table_index"], x["file_index"], compress, uncompressed_size)
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

    # Change Helm Geometry (Can't use main CL Build System because of forced duplication)
    main_pointer_table_offset = 0x101C50
    fh.seek(main_pointer_table_offset + 4)
    geo_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(geo_table + (0x11 * 4))
    helm_geo = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    helm_geo_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
    helm_geo_size = helm_geo_end - helm_geo
    fh.seek(helm_geo)
    for by_i in range(helm_geo_size):
        fh.write((0).to_bytes(1, "big"))
    fh.seek(helm_geo)
    with open("helm.bin", "rb") as helm_geo:
        fh.write(gzip.compress(helm_geo.read(), compresslevel=9))

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
    generateDefaultPadPairing(fh)
    writeVanillaSongData(fh)
    fh.seek(0x1FED020 + 0x11E)
    fh.write((1).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x11C)
    fh.write((0xFF).to_bytes(1, "big"))
    for x in portal_images:
        for y in x:
            if os.path.exists(y):
                os.remove(y)

    # Kong Order
    fh.seek(0x1FED020 + 0x151)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x152)
    fh.write((1).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x153)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x154)
    fh.write((2).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x155)
    fh.write((0).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x156)
    fh.write((3).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x157)
    fh.write((1).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x158)
    fh.write((4).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x159)
    fh.write((2).to_bytes(1, "big"))

    # Pkmn Snap Default Enemies
    pkmn_snap_enemies = [
        True,  # Kaboom
        True,  # Blue Beaver
        True,  # Book
        True,  # Klobber
        True,  # Zinger (Charger)
        True,  # Klump
        True,  # Klaptrap (Green)
        True,  # Zinger (Bomber)
        True,  # Klaptrap (Purple)
        False,  # Klaptrap (Red)
        False,  # Gold Beaver
        True,  # Mushroom Man
        True,  # Ruler
        True,  # Robo-Kremling
        True,  # Kremling
        True,  # Kasplat (DK)
        True,  # Kasplat (Diddy)
        True,  # Kasplat (Lanky)
        True,  # Kasplat (Tiny)
        True,  # Kasplat (Chunky)
        False,  # Kop
        True,  # Robo-Zinger
        True,  # Krossbones
        True,  # Shuri
        True,  # Gimpfish
        True,  # Mr. Dice (Green)
        True,  # Sir Domino
        True,  # Mr. Dice (Red)
        True,  # Fireball w/ Glasses
        True,  # Small Spider
        True,  # Bat
        True,  # Tomato
        True,  # Ghost
        True,  # Pufftup
        True,  # Kosha
    ]
    values = [0, 0, 0, 0, 0]
    for pi, p in enumerate(pkmn_snap_enemies):
        if p is True:
            offset = pi >> 3
            shift = pi & 7
            values[offset] |= 1 << shift
    fh.seek(0x1FED020 + 0x117)
    for x in range(5):
        fh.write(values[x].to_bytes(1, "big"))

    # Item Rando defaults
    # Blueprints
    fh.seek(0x1FF1000)
    for level_index in range(8):
        for bp_item in (78, 75, 77, 79, 76):
            fh.write(bp_item.to_bytes(1, "big"))
    # Medals
    fh.seek(0x1FF1080)
    for medal_item in range(40):
        fh.write((5).to_bytes(1, "big"))
    # Crown
    fh.seek(0x1FF10C0)
    for crown_item in range(10):
        fh.write((86).to_bytes(1, "big"))
    # Key
    fh.seek(0x1FF10D0)
    for crown_item in range(8):
        fh.write((72).to_bytes(1, "big"))
    # Misc Drops
    fh.seek(0x1FED020 + 0x114)
    for x in range(2):
        fh.write((45).to_bytes(1, "big"))
    # Shop Hints
    fh.seek(0x1FED020 + 0x14B)
    fh.write((1).to_bytes(1, "big"))

    piano_vanilla = [2, 1, 2, 3, 4, 2, 0]
    for piano_index, piano_key in enumerate(piano_vanilla):
        fh.seek(0x1FED020 + 0x16C + piano_index)
        fh.write(piano_key.to_bytes(1, "big"))

    dk_face_puzzle_vanilla = [0, 3, 2, 0, 1, 2, 3, 2, 1]
    chunky_face_puzzle_vanilla = [0, 1, 3, 1, 2, 1, 3, 0, 1]
    for face_index in range(9):
        fh.seek(0x1FED020 + 0x17E + face_index)
        fh.write(dk_face_puzzle_vanilla[face_index].to_bytes(1, "big"))
        fh.seek(0x1FED020 + 0x187 + face_index)
        fh.write(chunky_face_puzzle_vanilla[face_index].to_bytes(1, "big"))

    with open("assets/Non-Code/credits/squish.bin", "rb") as squish:
        fh.seek(0x1FFF800)
        fh.write(squish.read())

    vanilla_coin_reqs = [
        {"offset": 0x13C, "coins": 50},
        {"offset": 0x13D, "coins": 50},
        {"offset": 0x13E, "coins": 10},
        {"offset": 0x13F, "coins": 10},
        {"offset": 0x140, "coins": 10},
        {"offset": 0x141, "coins": 50},
        {"offset": 0x142, "coins": 50},
        {"offset": 0x143, "coins": 25},
    ]
    for coinreq in vanilla_coin_reqs:
        fh.seek(0x1FED020 + coinreq["offset"])
        fh.write(coinreq["coins"].to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0x48)
    for lvl in (1, 4, 3, 2):  # Arcade Order
        fh.write(lvl.to_bytes(1, "big"))
    for x in range(5):
        # Write default Helm Order
        fh.seek(0x1FED020 + x)
        fh.write(x.to_bytes(1, "big"))
    for x in hash_icons:
        pth = f"assets/Non-Code/hash/{x}"
        if os.path.exists(pth):
            os.remove(pth)
    other_remove = []
    displays = [
        "dk_face",
        "diddy_face",
        "lanky_face",
        "tiny_face",
        "chunky_face",
        "none",
        "shared",
        "soldout32",
        "wxys",
        "yellow_qmark_0",
        "yellow_qmark_1",
        "empty44",
        "empty3264",
        "homing_crate",
        "num_6_lit",
        "num_6_unlit",
        "num_9_lit",
        "num_9_unlit",
        "standard_crate",
        "crown",
        "crown_shop",
        "dk_bp",
        "gb",
        "key",
        "krusha_head64",
        "lanky_bp",
        "medal",
        "nin_coin",
        "potion32",
        "rw_coin",
    ]
    for disp in displays:
        for ext in [".png", ".rgba32", ".rgba5551"]:
            other_remove.append(f"displays/{disp}{ext}")
    for x in range(8):
        other_remove.append(f"file_screen/key{x+1}.png")
    other_remove.append("file_screen/tracker.png")
    for x in other_remove:
        pth = f"assets/Non-Code/{x}"
        if os.path.exists(pth):
            os.remove(pth)
    hash_items = [
        "dk_tie_palette",
        "homing_crate_0",
        "homing_crate_1",
        "num_1_lit",
        "num_1_unlit",
        "num_6_lit",
        "num_6_unlit",
        "num_7_lit",
        "num_7_unlit",
        "num_9_lit",
        "num_9_unlit",
        "standard_crate_0",
        "standard_crate_1",
        "tiny_palette",
        "coconut",
        "feather",
        "grape",
        "peanut",
        "pineapple",
        "triangle",
        "trombone",
        "modified_coin_side",
        "nin_coin_0",
        "nin_coin_1",
        "rw_coin_0",
        "rw_coin_1",
        "special_coin_side",
    ]
    script_files = [x[0] for x in os.walk("assets/Non-Code/instance_scripts/")]
    shop_files = ["snide.script", "cranky.script", "funky.script", "candy.script"]
    for folder in script_files:
        for file in os.listdir(folder):
            file = f"{folder}/{file}"
            for shop in shop_files:
                if shop in file:
                    if os.path.exists(file):
                        os.remove(file)
    for hash_item in hash_items:
        for f_t in ["rgba5551", "png"]:
            pth = f"assets/Non-Code/hash/{hash_item}.{f_t}"
            if os.path.exists(pth):
                os.remove(pth)
    credits_bins = ["credits", "squish"]
    for x in credits_bins:
        pth = f"assets/Non-Code/credits/{x}.bin"
        if os.path.exists(pth):
            os.remove(pth)
    if os.path.exists("assets/Non-Code/Gong/hint_door.bin"):
        os.remove("assets/Non-Code/Gong/hint_door.bin")
    for x in model_changes:
        if os.path.exists(x["model_file"]):
            os.remove(x["model_file"])
    if os.path.exists(new_coin_sfx):
        os.remove(new_coin_sfx)
    if os.path.exists("helm.bin"):
        os.remove("helm.bin")
    for x in range(216):
        if os.path.exists(f"exit{x}.bin"):
            os.remove(f"exit{x}.bin")
    # pth = "assets/Non-Code/displays/soldout_bismuth.rgba32"
    # if os.path.exists(pth):
    #     os.remove(pth)

# Get BPS Data
with open(newROMName, "r+b") as fh:
    size = len(fh.read())
    add = 0x10 - (size % 0x10)
    if add != 0x10:
        size += add
    fh.seek(0x1FF4000)
    fh.write(size.to_bytes(4, "big"))

print("[7 / 7] - Generating BizHawk RAM watch")

sys.exit()
