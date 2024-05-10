"""Build the ROM."""

import gzip
import json
import os
import shutil
import subprocess
import sys
import zlib

import create_helm_geo
import generate_disco_models
import generate_watch_file
import model_fix
from pull_guns_and_instruments import pullHandModels
from model_port import loadNewModels

# Patcher functions for the extracted files
from patch_text import writeNoExpPakMessages
import portal_instance_script
import shop_instance_script
from adjust_exits import adjustExits
from adjust_zones import modifyTriggers
from BuildClasses import File, HashIcon, ModelChange, ROMPointerFile, TextChange
from BuildEnums import ChangeType, CompressionMethods, TableNames, TextureFormat
from BuildLib import BLOCK_COLOR_SIZE, ROMName, music_size, newROMName, barrel_skins, getBonusSkinOffset
from convertPortalImage import convertPortalImage
from convertSetup import convertSetup
from cutscene_builder import buildScripts
from end_seq_writer import createSquishFile, createTextFile
from generate_yellow_wrinkly import generateYellowWrinkly
from helm_doors import getHelmDoorModel
from instance_script_maker import BuildInstanceScripts
from model_shrink import shrinkModel
from enemy_fixes import fixFactoryDiddyPincodeEnemies

# Infrastructure for recomputing DK64 global pointer tables
# from BuildNames import maps
from populateSongData import writeVanillaSongData
from recompute_overlays import isROMAddressOverlay, readOverlayOriginalData, replaceOverlayData, writeModifiedOverlaysToROM, writeUncompressedOverlays
from recompute_pointer_table import clampCompressedTextures, dumpPointerTableDetails, getFileInfo, parsePointerTables, replaceROMFile, writeModifiedPointerTablesToROM
from staticcode import patchStaticCode
from vanilla_move_data import writeVanillaMoveData
from writeWarpData import generateDefaultPadPairing

if os.path.exists(newROMName):
    os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

# pullHandModels()
loadNewModels()
BuildInstanceScripts()

portal_images = []
portal_images.append(convertPortalImage("assets/portals/DK_rando_portal_1.png"))
portal_images.append(convertPortalImage("assets/portals/DK_rando_portal_2.png"))

createTextFile("assets/credits")
createSquishFile("assets/credits")
generateYellowWrinkly()

getHelmDoorModel(6022, 6023, "crown_door.bin")
getHelmDoorModel(6024, 6025, "coin_door.bin")

file_dict = [
    # File(
    #     name="Static ASM Code",
    #     subtype=ChangeType.FixedLocation,
    #     start=0x113F0,
    #     compressed_size=0xB15E4,
    #     source_file="StaticCode.bin",
    #     compression_method=CompressionMethods.ExternalGzip,
    #     patcher=patchStaticCode,
    # ),
    File(name="Dolby Logo", pointer_table_index=TableNames.TexturesHUD, file_index=176, source_file="assets/Dolby/DolbyThin.png", texture_format=TextureFormat.IA4),
    File(name="Thumb Image", pointer_table_index=TableNames.TexturesHUD, file_index=94, source_file="assets/Nintendo Logo/Nintendo5.png", texture_format=TextureFormat.RGBA5551),
    File(name="DKTV Image", pointer_table_index=TableNames.TexturesHUD, file_index=44, source_file="assets/DKTV/logo3.png", texture_format=TextureFormat.RGBA5551),
    File(name="Spin Transition Image", pointer_table_index=TableNames.TexturesHUD, file_index=95, source_file="assets/transition/transition-body.png", texture_format=TextureFormat.IA4),
    # File(name="Moves Image", pointer_table_index=TableNames.TexturesHUD, file_index=115, source_file="assets/file_screen/moves.png", texture_format=TextureFormat.RGBA5551),
    File(name="Medal Image", pointer_table_index=TableNames.TexturesHUD, file_index=116, source_file="assets/displays/medal.png", texture_format=TextureFormat.RGBA5551),
    File(name="Tag Barrel Shell Texture", pointer_table_index=TableNames.TexturesGeometry, file_index=4938, source_file="assets/tagbarrel/shell.png", texture_format=TextureFormat.RGBA5551),
    File(name="Gong Geometry", pointer_table_index=TableNames.ModelTwoGeometry, file_index=195, source_file="assets/Gong/gong_geometry.bin", bps_file="assets/Gong/gong_geometry.bps"),
    File(name="End Sequence Credits", pointer_table_index=TableNames.Unknown19, file_index=7, source_file="assets/credits/credits.bin", do_not_delete_source=True),
    File(
        name="DK Wrinkly Door",
        pointer_table_index=TableNames.ModelTwoGeometry,
        file_index=240,
        source_file="assets/Gong/hint_door.bin",
        do_not_delete_source=True,
        target_compressed_size=0x1420,
        target_uncompressed_size=0x1420,
    ),
    File(name="WXY_Slash", pointer_table_index=TableNames.TexturesHUD, file_index=12, source_file="assets/displays/wxys.png", texture_format=TextureFormat.RGBA5551),
    File(
        name="DK Tie Palette",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6013,
        source_file="assets/hash/dk_tie_palette.png",
        do_not_extract=True,
        texture_format=TextureFormat.RGBA5551,
        target_compressed_size=BLOCK_COLOR_SIZE,
    ),
    File(
        name="Tiny Overalls Palette",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6014,
        source_file="assets/hash/tiny_palette.png",
        do_not_extract=True,
        texture_format=TextureFormat.RGBA5551,
        target_compressed_size=BLOCK_COLOR_SIZE,
    ),
    File(name="Bean Sprite", pointer_table_index=TableNames.TexturesGeometry, file_index=6020, source_file="assets/displays/bean.png", do_not_extract=True, texture_format=TextureFormat.RGBA5551),
    File(name="Pearl Sprite", pointer_table_index=TableNames.TexturesGeometry, file_index=6021, source_file="assets/displays/pearl.png", do_not_extract=True, texture_format=TextureFormat.RGBA5551),
    File(name="Kong (DK) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=599, source_file="kong_dk_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="Kong (Diddy) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=600, source_file="kong_diddy_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="Kong (Lanky) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=601, source_file="kong_lanky_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="Kong (Tiny) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=602, source_file="kong_tiny_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="Kong (Chunky) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=603, source_file="kong_chunky_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="Fairy Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=604, source_file="fairy_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="DPad Image", pointer_table_index=TableNames.TexturesHUD, file_index=187, source_file="assets/displays/dpad.png", texture_format=TextureFormat.RGBA5551),
    File(name="Tracker Image", pointer_table_index=TableNames.TexturesHUD, file_index=161, source_file="assets/file_screen/tracker.png", texture_format=TextureFormat.RGBA5551),
    File(name="Nintendo Coin Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=72, source_file="nintendo_coin_om2.bin", do_not_delete_source=True),
    File(name="Nintendo Coin Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=183, source_file="rainbow_coin_om2.bin", do_not_delete_source=True),
    File(name="Rareware Coin Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=655, source_file="rareware_coin_om2.bin", do_not_delete_source=True),
    File(name="Potion (DK) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=91, source_file="potion_dk_om2.bin", do_not_delete_source=True, bloat_compression=True),
    File(name="Potion (Diddy) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=498, source_file="potion_diddy_om2.bin", do_not_delete_source=True, bloat_compression=True),
    File(name="Potion (Lanky) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=89, source_file="potion_lanky_om2.bin", do_not_delete_source=True, bloat_compression=True),
    File(name="Potion (Tiny) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=499, source_file="potion_tiny_om2.bin", do_not_delete_source=True, bloat_compression=True),
    File(name="Potion (Chunky) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=501, source_file="potion_chunky_om2.bin", do_not_delete_source=True, bloat_compression=True),
    File(name="Potion (Any) Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=502, source_file="potion_any_om2.bin", do_not_delete_source=True, bloat_compression=True),
    # File(name="K. Rool (Cutscenes) Model", pointer_table_index=TableNames.ActorGeometry, file_index=0x48, source_file="k_rool_cutscenes_om1.bin", do_not_delete_source=True),
    File(
        name="Krusha Head",
        subtype=ChangeType.FixedLocation,
        start=0x1FF6000,
        source_file="assets/displays/krusha_head64.png",
        do_not_delete_source=True,
        texture_format=TextureFormat.RGBA5551,
        do_not_compress=True,
    ),
    File(
        name="Snow Texture",
        subtype=ChangeType.FixedLocation,
        start=0x1FF8000,
        source_file="assets/displays/snow32.png",
        do_not_delete_source=True,
        texture_format=TextureFormat.RGBA5551,
        do_not_compress=True,
    ),
    File(name="Crown Door Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=422, source_file="crown_door.bin", do_not_delete_source=True),
    File(name="Coin Door Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=423, source_file="coin_door.bin", do_not_delete_source=True),
    File(
        name="Crown Door Image 1",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6022,
        source_file="assets/displays/door_crown.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
        target_compressed_size=0xF20,
    ),
    File(
        name="Crown Door Image 2",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6023,
        source_file="assets/displays/num_4.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
        target_compressed_size=0xF20,
    ),
    File(
        name="Coin Door Image 1",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6024,
        source_file="assets/displays/door_combocoin.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
        target_compressed_size=0xF20,
    ),
    File(
        name="Coin Door Image 2",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6025,
        source_file="assets/displays/num_2.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
        target_compressed_size=0xF20,
    ),
    File(
        name="Fake GB Shine",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=getBonusSkinOffset(0),
        source_file="assets/displays/gb_shine.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
    ),
    File(
        name="Melon Surface",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=getBonusSkinOffset(4),
        source_file="assets/hash/melon_resized.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
        target_compressed_size=0x800,
    ),
    File(name="Fake Item Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=605, source_file="fake_item.bin", do_not_delete_source=True, do_not_extract=True),
    File(name="Melon Model", pointer_table_index=TableNames.ModelTwoGeometry, file_index=606, source_file="melon_om2.bin", do_not_extract=True, do_not_delete_source=True),
    File(name="21132 Sign", pointer_table_index=TableNames.TexturesGeometry, file_index=0x7CA, source_file="21132_tex.bin", target_size=2 * 64 * 32),
    File(name="Crypt Lever Sign 1", pointer_table_index=TableNames.TexturesGeometry, file_index=0x999, source_file="cryptlev1_tex.bin", target_size=2 * 64 * 32),
    File(name="Crypt Lever Sign 2", pointer_table_index=TableNames.TexturesGeometry, file_index=0x99A, source_file="cryptlev2_tex.bin", target_size=2 * 64 * 32),
    File(name="Base Barrel Skin", pointer_table_index=TableNames.ActorGeometry, file_index=0x75, source_file="barrel_skin_base.bin", do_not_delete_source=True),
    File(
        name="Base Barrel Shell",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=getBonusSkinOffset(5),
        source_file="assets/tagbarrel/plain_shell.png",
        texture_format=TextureFormat.RGBA5551,
        do_not_delete_source=True,
    ),
    File(name="Majoras Mask Moon", pointer_table_index=TableNames.TexturesHUD, file_index=115, source_file="assets/displays/moon_santa.png", texture_format=TextureFormat.IA8),
    File(name="Scoff Head", pointer_table_index=TableNames.TexturesHUD, file_index=114, source_file="assets/hash/scoff_head.png", texture_format=TextureFormat.RGBA5551),
    File(name="Outlined Crosshair", pointer_table_index=TableNames.TexturesHUD, file_index=113, source_file="assets/displays/crosshair.png", texture_format=TextureFormat.IA8),
    File(name="Wrinkly Sprite", pointer_table_index=TableNames.TexturesHUD, file_index=108, source_file="assets/displays/wrinkly_sprite.png", texture_format=TextureFormat.IA8),
]

file_dict = file_dict + buildScripts()

for bell in [692, 693]:
    file_dict.append(
        File(
            name=f"Bell {bell}",
            pointer_table_index=TableNames.ModelTwoGeometry,
            file_index=bell,
            source_file=f"bell{bell}.png",
            target_size=0x35C,
        )
    )

for klap_tex in [0xF31, 0xF32, 0xF33, 0xF35, 0xF37, 0xF38, 0xF39, 0xF3C, 0xF3D, 0xF3E, 0xF3F, 0xF40, 0xF41, 0xF44, 0xF45, 0xF46, 0xF47, 0xF48, 0xF49]:
    file_dict.append(
        File(
            name=f"Klaptrap Texture {hex(klap_tex)}",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=klap_tex,
            source_file=f"klap_tex{klap_tex}.png",
            target_size=0xAB8,
        )
    )

for img in (0x4DD, 0x4E4, 0x6B, 0xF0, 0x8B2, 0x5C2, 0x66E, 0x66F, 0x685, 0x6A1, 0xF8, 0x136, 2007):
    file_dict.append(
        File(
            name=f"Snow Texture {hex(img)}",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=img,
            source_file=f"grass{img}.bin",
            target_compressed_size=0xAA0,
        )
    )

number_game_changes = [
    {"number": 6, "state": "unlit", "texture": 520},
    {"number": 6, "state": "lit", "texture": 521},
    {"number": 9, "state": "unlit", "texture": 526},
    {"number": 9, "state": "lit", "texture": 527},
]
for num in number_game_changes:
    file_dict.append(
        File(
            name=f"Number Game ({num['number']}, {num['state']})",
            pointer_table_index=TableNames.TexturesUncompressed,
            file_index=num["texture"],
            source_file=f"assets/displays/num_{num['number']}_{num['state']}.png",
            texture_format=TextureFormat.RGBA5551,
            do_not_compress=True,
        )
    )
for x in range(5):
    file_dict.append(
        File(
            name=f"Blueprint Model ({x})",
            pointer_table_index=TableNames.ModelTwoGeometry,
            file_index=0xDD + x,
            source_file=f"blueprint{x}.bin",
            do_not_delete_source=True,
            target_size=0x6C4,
        )
    )
for x in range(0x5A, 0x5E):
    file_dict.append(File(name=f"Melon Slice ({hex(x)})", pointer_table_index=TableNames.TexturesHUD, file_index=x, source_file=f"melon{x}.bin", target_compressed_size=48 * 42 * 2))

for item in range(3):
    file_dict.append(
        File(
            name=f"Rainbow Coin ({item})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=getBonusSkinOffset(item + 1),
            source_file=f"assets/hash/rainbow_{item}.png",
            do_not_extract=True,
            texture_format=TextureFormat.RGBA5551,
        )
    )

for ci, coin in enumerate(["nin_coin", "rw_coin"]):
    for item in range(2):
        file_dict.append(
            File(
                name=f"{coin.replace('_',' ').capitalize()} ({item})",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=6015 + item + (2 * ci),
                source_file=f"assets/hash/{coin}_{item}.png",
                do_not_extract=True,
                texture_format=TextureFormat.RGBA5551,
            )
        )
file_dict.append(
    File(
        name="Special Coin Side",
        pointer_table_index=TableNames.TexturesGeometry,
        file_index=6019,
        source_file=f"assets/hash/modified_coin_side.png",
        do_not_extract=True,
        texture_format=TextureFormat.RGBA5551,
    )
)

key_textures = (0xBAB, 0xC6F)
for tx in key_textures:
    dim = 32
    if tx == 0xC6F:
        dim = 4
    file_dict.append(
        File(
            name=f"Key Texture {tx}",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=tx,
            source_file=f"key_tex{tx}.png",
            target_size=2 * dim * dim,
        )
    )

starts = (0x15F8, 0x15E8, 0x158F, 0x1600, 0x15F0)
for si, s in enumerate(starts):
    for x in range(8):
        file_dict.append(
            File(
                name=f"Blueprint Image (Kong {si + 1}, Frame {x})",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=s + x,
                source_file=f"bp{si}_{x}.bin",
                target_size=48 * 42 * 2,
            )
        )

kong_names = ["DK", "Diddy", "Lanky", "Tiny", "Chunky"]
ammo_names = ["standard_crate", "homing_crate"]

switch_faces = [0xB25, 0xB1E, 0xC81, 0xC80, 0xB24]
for face_index, face in enumerate(switch_faces):
    file_dict.append(
        File(
            name=f"Switch Face (Kong {face_index + 1})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=face,
            source_file=f"switch_face_{face}.bin",
            target_size=32 * 32 * 2,
        )
    )

for ammo_index, ammo in enumerate(ammo_names):
    file_dict.append(
        File(
            name=f"{ammo.replace('_',' ')} Image",
            pointer_table_index=TableNames.TexturesHUD,
            file_index=188 + ammo_index,
            source_file=f"assets/displays/{ammo}.png",
            texture_format=TextureFormat.RGBA5551,
        )
    )

for kong_index, kong in enumerate(kong_names):
    file_dict.append(
        File(
            name=f"DPad - {kong} Face",
            pointer_table_index=TableNames.TexturesHUD,
            file_index=190 + kong_index,
            source_file=f"assets/displays/{kong.lower()}_face.png",
            texture_format=TextureFormat.RGBA5551,
            target_compressed_size=32 * 32 * 2,
        )
    )

for start in [4897, 4903, 4712, 4950, 4925]:
    for offset in range(6):
        file_dict.append(
            File(
                name=f"Shockwave Frame {start + offset}",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=start + offset,
                source_file=f"shockwave_{start+offset}.bin",
                target_compressed_size=32 * 32 * 4,
                target_uncompressed_size=32 * 32 * 4,
            )
        )

for start in [0xD60, 0x67F, 0xD64, 0xD62, 0xD66, 0xD61, 0x680, 0xD65, 0xD63, 0xD67]:
    file_dict.append(
        File(
            name=f"Mushroom {start}",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=start,
            source_file=f"Mushroom_{start}.bin",
            target_size=64 * 32 * 2,
        )
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
    "lanky_bp",
    "crown_shop",
    "key",
    "medal",
    "potion32",
    "nin_coin",
    "rw_coin",
    "bean32",
    "pearl32",
    "fairy",
    "rainbow_coin",
    "fake_gb_shop",
]
for x, shop in enumerate(shop_face_array):
    data = File(
        name=f"Shop Indicator ({shop})",
        pointer_table_index=TableNames.TexturesHUD,
        file_index=195 + x,
        source_file=f"assets/displays/{shop}.png",
        texture_format=TextureFormat.RGBA32,
    )
    if "_face" in shop:
        data.target_compressed_size = 32 * 32 * 4
    file_dict.append(data)

base_coin_sfx = "assets/music/Win95_startup.dk64song"
new_coin_sfx = "assets/music/coin_sfx.bin"
if os.path.exists(new_coin_sfx):
    os.remove(new_coin_sfx)
shutil.copyfile(base_coin_sfx, new_coin_sfx)

arcade_rewards = [
    # 0 - Nintendo Coin / No Item
    "bean",  # 1 - Bean
    "blueprint",  # 2 - Blueprint
    "crown",  # 3 - Crown
    "fairy",  # 4 - Fairy
    "gb",  # 5 - GB
    "key",  # 6 - Key
    "medal",  # 7 - Medal
    "pearl",  # 8 - Pearl
    "potion_dk",  # 9 - Potion (DK)
    "potion_diddy",  # 10 - Potion (Diddy)
    "potion_lanky",  # 11 - Potion (Lanky)
    "potion_tiny",  # 12 - Potion (Tiny)
    "potion_chunky",  # 13 - Potion (Chunky)
    "potion_any",  # 14 - Potion (Any)
    "dk",  # 15 - DK
    "diddy",  # 16 - Diddy
    "lanky",  # 17 - Lanky
    "tiny",  # 18 - Tiny
    "chunky",  # 19 - Chunky
    "rainbow",  # 20 - Rainbow Coin
    "rwcoin",  # 21 - RW Coin
    "melon",  # 22 - Melon Slice
]

jetpac_rewards = [
    # 0 - Rareware Coin / No Item
    "bean",  # 1 - Bean
    "blueprint",  # 2 - Blueprint
    "crown",  # 3 - Crown
    "fairy",  # 4 - Fairy
    "gb",  # 5 - GB
    "key",  # 6 - Key
    "medal",  # 7 - Medal
    "pearl",  # 8 - Pearl
    "potion",  # 9 - Potion
    "kong",  # 10 - Kong
    "rainbow",  # 11 - Rainbow Coin
    "nintendo",  # 12 - Nintendo Coin
    "melon",  # 13 - Melon
]

for rwd_index, rwd in enumerate(arcade_rewards):
    file_dict.append(
        File(
            name=f"Arcade Reward - {rwd.capitalize()}",
            pointer_table_index=TableNames.Unknown6,
            file_index=rwd_index,
            source_file=f"assets/arcade_jetpac/arcade/{rwd}.png",
            do_not_compress=True,
            texture_format=TextureFormat.RGBA5551,
            do_not_delete_source=True,
        )
    )
for rwd_index, rwd in enumerate(jetpac_rewards):
    file_dict.append(
        File(
            name=f"Jetpac Reward - {rwd.capitalize()}",
            pointer_table_index=TableNames.Unknown6,
            file_index=rwd_index + len(arcade_rewards),
            source_file=f"assets/arcade_jetpac/jetpac/{rwd}.png",
            do_not_compress=True,
            texture_format=TextureFormat.I8,
            do_not_delete_source=True,
        )
    )


map_replacements = []
song_replacements = [
    {"name": "baboon_balloon", "index": 107, "bps": True},
    {"name": "bonus_minigames", "index": 8, "bps": True},
    {"name": "dk_rap", "index": 75, "bps": True},
    {"name": "failure_races_try_again", "index": 87, "bps": True},
    {"name": "move_get", "index": 114, "bps": True},
    {"name": "nintendo_logo", "index": 174, "bps": True},
    {"name": "success_races", "index": 86, "bps": True},
    # {"name": "klumsy_celebration", "index": 125, "bps": True},
    {"name": "coin_sfx", "index": 7, "bps": False},
    {"name": "intro_story", "index": 122, "bps": True},
]
changed_song_indexes = []

for song in song_replacements:
    item = File(
        name=song["name"].replace("_", " "),
        pointer_table_index=TableNames.MusicMIDI,
        file_index=song["index"],
        source_file=f"assets/music/{song['name']}.bin",
        target_compressed_size=music_size,
    )
    if song["bps"]:
        item.bps_file = f"assets/music/{song['name']}.bps"
    else:
        item.do_not_delete_source = True
        item.do_not_extract = True
    file_dict.append(item)
    changed_song_indexes.append(song["index"])

for door in (0xF2, 0xEF, 0x67, 0xF1):
    file_dict.append(
        File(
            name=f"Wrinkly Door {hex(door)}",
            pointer_table_index=TableNames.ModelTwoGeometry,
            file_index=door,
            source_file=f"door{door}.bin",
            target_size=0x1420,
        )
    )

switches = [
    [0x94, 0x16C, 0x167],
    [0x93, 0x16B, 0x166],
    [0x95, 0x16D, 0x168],
    [0x96, 0x16E, 0x169],
    [0xB8, 0x16A, 0x165],
]
for ki, kong in enumerate(switches):
    for li, lvl in enumerate(kong):
        file_dict.append(
            File(
                name=f"Slam Switch (Kong {ki}, Lvl {li})",
                pointer_table_index=TableNames.ModelTwoGeometry,
                file_index=lvl,
                source_file=f"switch{lvl}.bin",
                target_size=0xC70,
            )
        )

# Instance Scripts
with open("./instance_scripts_data.json", "r") as json_f:
    instance_script_maps = json.load(json_f)
maps_to_expand = list(range(0, 216))
SCRIPT_EXPANSION_SIZE = 0x200
for x in instance_script_maps:
    maps_to_expand.remove(x["map"])
    script_file_name = f"{x['name']}.raw"
    expand_size = 0x2000
    with open(script_file_name, "rb") as script_f:
        data = script_f.read()
        compress = gzip.compress(data, compresslevel=9)
        expand_size = len(data) + SCRIPT_EXPANSION_SIZE
    file_dict.append(
        File(
            name=f"{x['name'].replace('_',' ')} Instance Scripts",
            pointer_table_index=TableNames.InstanceScripts,
            file_index=x["map"],
            source_file=script_file_name,
            target_size=expand_size,
            do_not_recompress=True,
            do_not_delete_source=True,
        )
    )
for x in maps_to_expand:
    with open(ROMName, "rb") as fh:
        instance_f = ROMPointerFile(fh, TableNames.InstanceScripts, x)
        item_size = instance_f.size
        if instance_f.compressed:
            fh.seek(instance_f.start)
            data = fh.read(item_size)
            data = zlib.decompress(data, (15 + 32))
            item_size = len(data)
        file_dict.append(
            File(
                name=f"Script {x}",
                pointer_table_index=TableNames.InstanceScripts,
                file_index=x,
                source_file=f"script{x}.bin",
                target_size=item_size + SCRIPT_EXPANSION_SIZE,
                do_not_recompress=True,
            )
        )

for x in range(175):
    if x > 0:
        if x not in changed_song_indexes:
            file_dict.append(
                File(
                    name=f"Song {x}",
                    pointer_table_index=TableNames.MusicMIDI,
                    file_index=x,
                    source_file=f"song{x}.bin",
                    target_compressed_size=music_size,
                )
            )
for x in range(6):
    file_dict.append(
        File(
            name=f"DKTV Inputs {x}",
            pointer_table_index=TableNames.DKTVInputs,
            file_index=x,
            source_file=f"dktv{x}.bin",
            target_compressed_size=0x718,
        )
    )
for x in range(221):
    file_dict.append(File(name=f"Zones for map {x}", pointer_table_index=TableNames.Triggers, file_index=x, source_file=f"lz{x}.bin", target_compressed_size=0x850, do_not_recompress=True))
# Setup
setup_expansion_size = 0x2580
for x in range(221):
    local_expansion = setup_expansion_size
    if x in (0, 1, 2, 5, 9, 15, 0x19):
        local_expansion = 0
    with open(ROMName, "rb") as fh:
        setup_f = ROMPointerFile(fh, TableNames.Setups, x)
        item_size = setup_f.size
        if setup_f.compressed:
            fh.seek(setup_f.start)
            data = fh.read(setup_f.size)
            data = zlib.decompress(data, (15 + 32))
            item_size = len(data)
        file_dict.append(
            File(
                name=f"Setup for map {x}",
                pointer_table_index=TableNames.Setups,
                file_index=x,
                source_file=f"setup{x}.bin",
                target_size=item_size + local_expansion,
                do_not_recompress=True,
            )
        )
for x in range(221):
    if x != 2:  # DK Arcade path file is massive
        file_dict.append(
            File(
                name=f"Paths for map {x}",
                pointer_table_index=TableNames.Paths,
                file_index=x,
                source_file=f"paths{x}.bin",
                target_size=0x600,
                do_not_recompress=True,
            )
        )
for x in range(221):
    if x == 0x1A:
        file_dict.append(
            File(
                name=f"Character Spawners for map {x}",
                pointer_table_index=TableNames.Spawners,
                file_index=x,
                source_file="factory_spawners.bin",
                target_size=0x1400,
                do_not_recompress=True,
                do_not_delete_source=True,
            )
        )
    else:
        file_dict.append(
            File(
                name=f"Character Spawners for map {x}",
                pointer_table_index=TableNames.Spawners,
                file_index=x,
                source_file=f"charspawners{x}.bin",
                target_size=0x1400,
                do_not_recompress=True,
            )
        )
file_dict.append(
    File(
        name="Dark Cloud",
        pointer_table_index=TableNames.TexturesHUD,
        file_index=107,
        source_file=f"assets/displays/text_bubble_dark.png",
        texture_format=TextureFormat.RGBA5551,
        target_compressed_size=0xC00,
    )
)
for x in range(10):
    file_dict.append(
        File(
            name=f"Tag Barrel Bottom Texture ({x+1})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=4749 + x,
            source_file="assets/tagbarrel/bottom.png",
            texture_format=TextureFormat.RGBA5551,
        )
    )
for x in range(4761, 4768):
    sz = "44"
    if x == 4761:
        sz = "3264"
    file_dict.append(
        File(
            name=f"Portal Ripple Texture ({x})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=x,
            source_file=f"assets/displays/empty{sz}.png",
            texture_format=TextureFormat.RGBA5551,
        )
    )
for x in range(0xB50, 0xB56):
    file_dict.append(
        File(
            name=f"Unused Texture ({x})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=x,
            source_file=f"assets/displays/empty11.png",
            texture_format=TextureFormat.RGBA5551,
        )
    )
for x in range(0xDD1, 0xDD6):
    file_dict.append(
        File(
            name=f"Unused Texture ({x})",
            pointer_table_index=TableNames.TexturesGeometry,
            file_index=x,
            source_file=f"assets/displays/empty11.png",
            texture_format=TextureFormat.RGBA5551,
        )
    )
barrel_faces = ["Dk", "Diddy", "Lanky", "Tiny", "Chunky"]
barrel_offsets = [4817, 4815, 4819, 4769, 4747]
for x in range(5):
    for y in range(2):
        file_dict.append(
            File(
                name=f"{barrel_faces[x]} Transform Barrel Shell ({y+1})",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=barrel_offsets[x] + y,
                source_file=f"assets/tagbarrel/{barrel_faces[x]} barrel {y}a.png",
                texture_format=TextureFormat.RGBA5551,
            )
        )


kong_palettes = {
    0xE8C: [(32, 32), "block"],  # DK Base
    0xE8D: [(43, 32), "checkered"],  # DK Tie Hang
    0xE66: [(32, 32), "block"],  # Diddy Cap/Shirt
    0xE69: [(32, 32), "block"],  # Lanky Overalls
    0xE9A: [(32, 32), "block"],  # Lanky Fur (Front)
    0xE94: [(32, 32), "block"],  # Lanky Fur
    0xEB9: [(43, 32), "checkered"],  # Chunky Checkered Shirt
    0xE67: [(32, 32), "block"],  # Chunky Shirt Front
    0xE68: [(32, 32), "block"],  # Tiny Hair
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
    file_dict.append(File(name=f"Palette Expansion ({hex(x)})", pointer_table_index=TableNames.TexturesGeometry, file_index=x, source_file=f"palette_{x}.bin", target_compressed_size=x_s))

for tex in range(0x273, 0x27D):
    file_dict.append(File(name=f"Head Expansion ({hex(tex)})", pointer_table_index=TableNames.TexturesGeometry, file_index=tex, source_file=f"head_{tex}.bin", target_compressed_size=32 * 64 * 2))

colorblind_changes = [[4120, 4124, 32, 44], [5819, 5858, 32, 64], [0xBB2, 0xBB3, 32, 16], [0xCE0, 0xCEB, 48, 42]]
for change in colorblind_changes:
    for file_index in range(change[0], change[1] + 1):
        file_dict.append(
            File(
                name=f"Colorblind Expansion {file_index}",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=file_index,
                source_file=f"colorblind_exp_{file_index}.bin",
                target_size=2 * change[2] * change[3],
            )
        )

for bi, b in enumerate(barrel_skins):
    for x in range(2):
        file_dict.append(
            File(
                name=f"Barrel Skin ({b.capitalize()} - {x + 1})",
                pointer_table_index=TableNames.TexturesGeometry,
                file_index=6026 + (2 * bi) + x,
                source_file=f"assets/displays/barrel_{b}_{x}.png",
                texture_format=TextureFormat.RGBA5551,
            )
        )

shrinkModel(False, "", 0xAE, 0.15, "shrink_crown.bin", False)  # Battle Crown
shrinkModel(False, "", 0xA4, 0.1, "shrink_key.bin", False)  # Boss Key
shrinkModel(True, "potion_dk_om1.bin", 0, 0.08, "shrink_potion_dk.bin", False)  # Potion (DK)
shrinkModel(True, "potion_diddy_om1.bin", 0, 0.08, "shrink_potion_diddy.bin", False)  # Potion (Diddy)
shrinkModel(True, "potion_lanky_om1.bin", 0, 0.08, "shrink_potion_lanky.bin", False)  # Potion (Lanky)
shrinkModel(True, "potion_tiny_om1.bin", 0, 0.08, "shrink_potion_tiny.bin", False)  # Potion (Tiny)
shrinkModel(True, "potion_chunky_om1.bin", 0, 0.08, "shrink_potion_chunky.bin", False)  # Potion (Chunky)
shrinkModel(True, "potion_any_om1.bin", 0, 0.08, "shrink_potion_any.bin", False)  # Potion (Any)
shrinkModel(False, "", 0x3C, 5, "shrink_fairy.bin", True)  # Fairy
shrinkModel(True, "dk_base.bin", 0, 1 / 0.15, "shrink_dk.bin", True)  # DK
shrinkModel(True, "diddy_base.bin", 0, 1 / 0.15, "shrink_diddy.bin", True)  # Diddy
shrinkModel(True, "lanky_base.bin", 0, 1 / 0.15, "shrink_lanky.bin", True)  # Lanky
shrinkModel(True, "tiny_base.bin", 0, 1 / 0.15, "shrink_tiny.bin", True)  # Tiny
shrinkModel(False, "", 0xB, 1 / 0.15, "shrink_chunky.bin", True)  # Chunky
shrinkModel(True, "fake_item_actor.bin", 0, 0.15, "shrink_ice_trap.bin", False),

model_changes = [
    ModelChange(0, "diddy_base.bin"),
    ModelChange(1, "diddy_ins.bin"),
    ModelChange(5, "lanky_base.bin"),
    ModelChange(6, "lanky_ins.bin"),
    ModelChange(3, "dk_base.bin"),
    ModelChange(8, "tiny_base.bin"),
    ModelChange(9, "tiny_ins.bin"),
    ModelChange(0xEC, "disco_instrument.bin"),
    ModelChange(0xDA, "krusha_base.bin"),
    ModelChange(0xED, "potion_dk_om1.bin", True),
    ModelChange(0xEE, "potion_diddy_om1.bin", True),
    ModelChange(0xEF, "potion_lanky_om1.bin", True),
    ModelChange(0xF0, "potion_tiny_om1.bin", True),
    ModelChange(0xF1, "potion_chunky_om1.bin", True),
    ModelChange(0xF2, "potion_any_om1.bin", True),
    ModelChange(0xF3, "shrink_crown.bin"),
    ModelChange(0xF4, "shrink_key.bin"),
    ModelChange(0xF5, "shrink_potion_dk.bin", True),
    ModelChange(0xF6, "shrink_potion_diddy.bin", True),
    ModelChange(0xF7, "shrink_potion_lanky.bin", True),
    ModelChange(0xF8, "shrink_potion_tiny.bin", True),
    ModelChange(0xF9, "shrink_potion_chunky.bin", True),
    ModelChange(0xFA, "shrink_potion_any.bin", True),
    ModelChange(0xFB, "shrink_fairy.bin"),
    ModelChange(0xFC, "fake_item_actor.bin"),
    ModelChange(0xFD, "shrink_dk.bin"),
    ModelChange(0xFE, "shrink_diddy.bin"),
    ModelChange(0xFF, "shrink_lanky.bin"),
    ModelChange(0x100, "shrink_tiny.bin"),
    ModelChange(0x101, "shrink_chunky.bin"),
    ModelChange(0x102, "shrink_ice_trap.bin"),
    ModelChange(0xA3, "counter.bin"),
    # ModelChange(0xC0, "guitar_om1.bin"),
]
model_changes = sorted(model_changes, key=lambda d: d.model_index)

for x in model_changes:
    data = File(
        name=f"Model {x.model_index}",
        pointer_table_index=TableNames.ActorGeometry,
        file_index=x.model_index,
        source_file=x.model_file,
        do_not_delete_source=True,
    )
    if x.model_index > 0xEB:
        data.do_not_extract = True
    if x.model_index == 0xDA:
        data.target_compressed_size = 0x4740
        data.target_uncompressed_size = 0x4740
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
                File(
                    name=f"Portal Image {x+1} - {segment}",
                    pointer_table_index=TableNames.TexturesUncompressed,
                    file_index=931 + (4 * x) + y,
                    source_file=found_image,
                    texture_format=TextureFormat.RGBA5551,
                    do_not_compress=True,
                )
            )

hash_icons = [
    HashIcon("bongos.png", 48),
    HashIcon("crown.png", 49),
    HashIcon("dkcoin.png", 50),
    HashIcon("fairy.png", 51),
    HashIcon("guitar.png", 55),
    HashIcon("nin_coin.png", 62),
    HashIcon("orange.png", 63),
    HashIcon("rainbow_coin.png", 64),
    HashIcon("rw_coin.png", 65),
    HashIcon("sax.png", 76),
]
for index, icon in enumerate(hash_icons):
    file_dict.append(
        File(
            name=f"Hash Icon {index}",
            pointer_table_index=TableNames.TexturesHUD,
            file_index=icon.file_index,
            source_file=f"assets/hash/{icon.icon_file}",
            texture_format=TextureFormat.RGBA5551,
        )
    )

text_files = (
    TextChange("Bonus Instructions", 0, ""),
    TextChange("Story Level Intro", 0, ""),
    TextChange("Kong Names", 0, "kongname_text.bin"),
    TextChange("Diddy", 0, ""),
    TextChange("Tiny", 0, ""),
    TextChange("Chunky", 0, ""),
    TextChange("Lanky", 0, ""),
    TextChange("Funky", 0, ""),
    TextChange("Cranky", 0x2800, "cranky_text.bin"),
    TextChange("Candy", 0, ""),
    TextChange("Llama", 0, ""),
    TextChange("Snide", 0, ""),
    TextChange("DK TV Screen", 0, ""),
    TextChange("Dolby", 0, "dolby_text.bin"),
    TextChange("Beetle", 0, ""),
    TextChange("Vulture", 0, ""),
    TextChange("Squawks", 0, ""),
    TextChange("Factory Car Race", 0, ""),
    TextChange("Seal Race", 0, ""),
    TextChange("Misc & Microbuffer", 0x1200, "misc_squawks_text.bin"),
    TextChange("Rabbit", 0, ""),
    TextChange("Owl", 0, ""),
    TextChange("Worm", 0, ""),
    TextChange("Mermaid", 0, ""),
    TextChange("DK", 0, "dk_text.bin"),
    TextChange("Training Grounds", 0, ""),
    TextChange("Bonus Encouragement", 0, ""),
    TextChange("K. Lumsy", 0, ""),
    TextChange("Seal Race 2", 0, ""),
    TextChange("B. Locker", 0, ""),
    TextChange("Fairy Queen", 0, ""),
    TextChange("Beanstalk", 0, ""),
    TextChange("Custom", 0, "custom_text.bin"),
    TextChange("Ice Tomato", 0, ""),
    TextChange("Castle Car Race", 0, ""),
    TextChange("Location/Level Names", 0, ""),
    TextChange("Pause Menu", 0, ""),
    TextChange("Main Menu", 0, "menu_text.bin"),
    TextChange("Race Positions", 0, ""),
    TextChange("Move Names", 0x2000, "move_names.bin"),  # Expanded for the Krusha move names feature
    TextChange("Fairy Queen Rareware Door", 0, "fairy_rw_text.bin"),
    TextChange("Wrinkly", 0x2800, ""),
    TextChange("Snide's Bonus Games", 0, ""),
    TextChange("Hint Regions", 0, "hint_region_text.bin"),
    TextChange("Item Locations", 0x2800, "item_locations.bin"),
    TextChange("Wrinkly Short", 0x2800, "short_wrinkly.bin"),
)

for index, text in enumerate(text_files):
    data = File(
        name=f"{text.name} Text",
        pointer_table_index=TableNames.Text,
        file_index=index,
        source_file=f"text{index}.bin" if text.file == "" else text.file,
    )
    if text.change:
        data.do_not_compress = True
        data.do_not_delete_source = True
        data.do_not_extract = True
    else:
        data.do_not_recompress = True
        data.setTargetSize(0x2000)
    if text.change_expansion > 0:
        data.setTargetSize(text.change_expansion)
        data.do_not_recompress = True
    file_dict.append(data)

with open(ROMName, "rb") as fh:
    adjustExits(fh)

for x in range(216):
    if os.path.exists(f"exit{x}.bin"):
        file_dict.append(File(name=f"Map {x} Exits", pointer_table_index=TableNames.Exits, file_index=x, source_file=f"exit{x}.bin", do_not_compress=True, do_not_delete_source=True))

print("\nDK64 Extractor\nBuilt by Isotarge")

with open(ROMName, "rb") as fh:
    print("[1 / 7] - Parsing pointer tables")
    parsePointerTables(fh)
    readOverlayOriginalData(fh)

    print("[2 / 7] - Extracting files from ROM")
    fixFactoryDiddyPincodeEnemies(fh)
    for x in file_dict:
        # N64Tex conversions do not need to be extracted to disk from ROM
        x.generateOutputFile()

        # gzip.exe appends .gz to the filename, we'll do the same
        if x.compression_method == CompressionMethods.ExternalGzip:
            x.output_file += ".gz"

        # If we're not extracting the file to disk, we're using a custom .bin that shoudn't be deleted
        if x.do_not_extract:
            x.do_not_delete_source = True

        # Extract the compressed file from ROM
        if not x.do_not_extract:
            byte_read = bytes()
            if x.subtype == ChangeType.PointerTable:
                file_info = getFileInfo(x.pointer_table_index, x.file_index)
                if file_info:
                    x.start = file_info.new_absolute_address
                    x.compressed_size = len(file_info.data)
            if x.start is None:
                print(vars(x))
            fh.seek(x.start)
            byte_read = fh.read(x.compressed_size)

            if not x.do_not_delete_source:
                if os.path.exists(x.source_file):
                    os.remove(x.source_file)

                with open(x.source_file, "wb") as fg:
                    fh.seek(x.start)
                    if int.from_bytes(fh.read(2), "big") == 0x1F8B:
                        dec = zlib.decompress(byte_read, 15 + 32)
                    else:
                        dec = byte_read
                    fg.write(dec)

print("[3 / 7] - Patching Extracted Files")
for x in file_dict:
    if x.patcher is not None and callable(x.patcher):
        print(" - Running patcher for " + x.source_file)
        x.patcher(x.source_file)

with open(newROMName, "r+b") as fh:
    print("[4 / 7] - Writing patched files to ROM")
    clampCompressedTextures(fh, 6070)
    for x in file_dict:
        if x.bps_file is not None:
            with open(x.source_file, "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            subprocess.Popen(["build\\flips.exe", "--apply", x.bps_file, x.source_file, x.source_file]).wait()
            # shutil.copyfile(x.source_file, x.source_file.replace(".bin", ".raw"))

        x.generateTextureFile()

        if x.target_compressed_size is not None:
            x.do_not_compress = True
            if x.source_file[:5] == "setup":
                convertSetup(x.source_file)
            if x.source_file[:2] == "lz":
                modifyTriggers(x.source_file)
            with open(x.source_file, "rb") as fg:
                byte_read = fg.read()
                uncompressed_size = len(byte_read)
            if x.do_not_recompress:
                compress = bytearray(byte_read)
                if x.target_uncompressed_size is not None:
                    diff = x.target_uncompressed_size - len(byte_read)
                    byte_append = 0
                    if diff > 0:
                        byte_read += byte_append.to_bytes(diff, "big")
                    compress = bytearray(byte_read)
                    uncompressed_size = x.target_uncompressed_size
            else:
                precomp = gzip.compress(byte_read, compresslevel=9)
                byte_append = 0
                diff = x.target_compressed_size - len(precomp)
                if diff > 0:
                    precomp += byte_append.to_bytes(diff, "big")
                compress = bytearray(precomp)
                # Zero out timestamp in gzip header to make builds deterministic
                compress[4] = 0
                compress[5] = 0
                compress[6] = 0
                compress[7] = 0
            with open(x.source_file, "wb") as fg:
                fg.write(compress)
            x.output_file = x.source_file

        if x.compression_method == CompressionMethods.ExternalGzip:
            if os.path.exists(x.source_file):
                result = subprocess.check_output(["./build/gzip.exe", "-f", "-n", "-k", "-q", "-9", x.output_file.replace(".gz", "")])
                if os.path.exists(x.output_file):
                    with open(x.output_file, "r+b") as outputFile:
                        # Chop off gzip footer
                        outputFile.truncate(len(outputFile.read()) - 8)

        if os.path.exists(x.output_file):
            byte_read = bytes()
            if x.target_compressed_size is None:
                uncompressed_size = 0
            with open(x.output_file, "rb") as fg:
                byte_read = fg.read()
                if x.target_compressed_size is None:
                    uncompressed_size = len(byte_read)

            if x.do_not_compress:
                compress = bytearray(byte_read)
            elif x.compression_method == CompressionMethods.ExternalGzip:
                compress = bytearray(byte_read)
            elif x.compression_method == CompressionMethods.Zlib:
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

            print(" - Writing " + x.output_file + " (" + hex(len(compress)) + f") to ROM")
            if x.subtype == ChangeType.PointerTable:
                # More complicated write, update the pointer tables to point to the new data
                replaceROMFile(fh, x.pointer_table_index, x.file_index, compress, uncompressed_size)
            elif x.start is not None:
                if isROMAddressOverlay(x.start):
                    replaceOverlayData(x.start, compress)
                else:
                    # Simply write the bytes at the absolute address in ROM specified by x.start
                    fh.seek(x.start)
                    fh.write(compress)
            else:
                print("  - WARNING: Can't find address information in file_dict entry to write " + x.output_file + " (" + hex(len(compress)) + ") to ROM")
        else:
            print(x.output_file + " does not exist")

        # Cleanup temporary files
        if not x.do_not_delete:
            if not x.do_not_delete_output:
                if os.path.exists(x.output_file) and x.output_file != x.source_file:
                    os.remove(x.output_file)
            if not x.do_not_delete_source:
                if os.path.exists(x.source_file):
                    os.remove(x.source_file)
    writeUncompressedOverlays(fh)

    print("[5 / 7] - Writing recomputed pointer tables to ROM")
    writeModifiedPointerTablesToROM(fh)
    writeModifiedOverlaysToROM(fh)

    print("[6 / 7] - Dumping details of all pointer tables to rom/build.log")
    dumpPointerTableDetails("rom/build.log", fh, False)

    # Change Helm Geometry (Can't use main CL Build System because of forced duplication)
    geo_file = ROMPointerFile(fh, TableNames.MapGeometry, 0x11)
    fh.seek(geo_file.start)
    for by_i in range(geo_file.size):
        fh.write((0).to_bytes(1, "big"))
    fh.seek(geo_file.start)
    with open("helm.bin", "rb") as helm_geo:
        fh.write(gzip.compress(helm_geo.read(), compresslevel=9))

    # Replace Helm Text
    text_file = ROMPointerFile(fh, TableNames.Text, 19)
    fh.seek(text_file.start + 0x7B9)
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

    # Default Menu Settings
    fh.seek(0x1FED020 + 0xC8)
    fh.write((40).to_bytes(1, "big"))
    fh.seek(0x1FED020 + 0xC9)
    fh.write((40).to_bytes(1, "big"))

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
    fh.seek(0x1FF0E00)
    for level_index in range(8):
        for bp_item in (78, 75, 77, 79, 76):
            fh.write(bp_item.to_bytes(2, "big"))
    # Medals
    fh.seek(0x1FF1080)
    for medal_item in range(40):
        fh.write((5).to_bytes(1, "big"))
    # Crown
    fh.seek(0x1FF10C0)
    for crown_item in range(10):
        fh.write((86).to_bytes(2, "big"))
    # Key
    fh.seek(0x1FF1000)
    for crown_item in range(8):
        fh.write((72).to_bytes(2, "big"))
    # Misc Drops
    fh.seek(0x1FED020 + 0xDC)
    for x in range(2):
        fh.write((45).to_bytes(2, "big"))
    # Fairies
    fh.seek(0x1FF1040)
    for x in range(20):
        fh.write((0x3D).to_bytes(2, "big"))
    # Rainbow Coins
    fh.seek(0x1FF10E0)
    for x in range(16):
        fh.write((0x8C).to_bytes(2, "big"))
    # Melon Crates
    fh.seek(0x1FF0E80)
    for x in range(16):
        fh.write((0x2F).to_bytes(2, "big"))
    # Enemies
    fh.seek(0x1FF9000)
    for x in range(426):
        fh.write((0).to_bytes(4, "big"))
    # Shop Hints
    fh.seek(0x1FED020 + 0x14B)
    fh.write((1).to_bytes(1, "big"))

    fh.seek(0x1FFD000)
    for x in range(64):
        fh.write((0).to_bytes(4, "big"))

    # Hint Flags
    fh.seek(0x1FFE000)
    for x in range(35):
        fh.write((0xFFFF).to_bytes(2, "big"))

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

    with open("assets/credits/squish.bin", "rb") as squish:
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
        pth = f"assets/hash/{x.icon_file}"
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
        "bean",
        "pearl",
        "bean32",
        "pearl32",
        "door_combocoin",
        "door_crown",
        "num_2",
        "num_4",
        "bonus_skin",
        "fairy",
        "fake_gb",
        "fake_gb_shop",
        "rainbow_coin",
        "gb_shine",
        "melon_surface",
        "melon_resized",
        "text_bubble_dark",
        "warp_left",
        "warp_right",
        "warp_rim_0",
        "warp_rim_1",
        "crosshair",
        "wrinkly_sprite",
    ]
    for b in barrel_skins:
        displays.extend([f"barrel_{b}_0", f"barrel_{b}_1"])
    for disp in displays:
        for ext in [".png", ".rgba32", ".rgba5551"]:
            other_remove.append(f"displays/{disp}{ext}")
    for x in range(8):
        other_remove.append(f"file_screen/key{x+1}.png")
    other_remove.append("file_screen/tracker.png")
    for x in other_remove:
        pth = f"assets/{x}"
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
        "rainbow_0",
        "rainbow_1",
        "rainbow_2",
        "special_coin_side",
        "fairy_0",
        "bonus_Skin",
        "melon_resized",
        "melon_slice",
        "scoff_head",
    ]
    script_files = [x[0] for x in os.walk("assets/instance_scripts/")]
    shop_files = ["snide.json", "cranky.json", "funky.json", "candy.json"]
    for folder in script_files:
        for file in os.listdir(folder):
            file = f"{folder}/{file}"
            for shop in shop_files:
                if shop in file:
                    if os.path.exists(file):
                        os.remove(file)
    for hash_item in hash_items:
        for f_t in ["rgba5551", "png"]:
            pth = f"assets/hash/{hash_item}.{f_t}"
            if os.path.exists(pth):
                os.remove(pth)
    credits_bins = ["credits", "squish"]
    for x in credits_bins:
        pth = f"assets/credits/{x}.bin"
        if os.path.exists(pth):
            os.remove(pth)
    arcade_images = [
        "blueprint",
        "crown",
        "fairy",
        "gb",
        "key",
        "medal",
        "rainbow",
        "rwcoin",
        "melon",
    ]
    for img in arcade_images:
        pth = f"assets/arcade_jetpac/arcade/{img}.png"
        if os.path.exists(pth):
            os.remove(pth)
    if os.path.exists("assets/Gong/hint_door.bin"):
        os.remove("assets/Gong/hint_door.bin")
    # for x in model_changes:
    #     if os.path.exists(x["model_file"]):
    #         os.remove(x["model_file"])
    if os.path.exists(new_coin_sfx):
        os.remove(new_coin_sfx)
    if os.path.exists("helm.bin"):
        os.remove("helm.bin")
    for x in range(216):
        if os.path.exists(f"exit{x}.bin"):
            os.remove(f"exit{x}.bin")
    # pth = "assets/displays/soldout_bismuth.rgba32"
    # if os.path.exists(pth):
    #     os.remove(pth)
    writeNoExpPakMessages(fh)

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
