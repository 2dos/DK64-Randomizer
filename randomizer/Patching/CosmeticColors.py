"""Apply cosmetic skins to kongs."""
import random
from random import randint

import js
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from PIL import Image, ImageEnhance
import zlib
import gzip


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    model_index = 0
    if js.document.getElementById("override_cosmetics").checked:
        model_setting = js.document.getElementById("klaptrap_model").value
    else:
        model_setting = spoiler.settings.klaptrap_model
    if model_setting == "green":
        model_index = 0x21
    elif model_setting == "purple":
        model_index = 0x22
    elif model_setting == "red":
        model_index = 0x23
    elif model_setting == "random_klap":
        model_index = random.randint(0x21, 0x23)
    elif model_setting == "random_model":
        permitted_models = [
            0x19,  # Beaver
            0x1E,  # Klobber
            0x20,  # Kaboom
            0x21,  # Green Klap
            0x22,  # Purple Klap
            0x23,  # Red Klap
            0x24,  # Klap Teeth
            0x26,  # Krash
            0x27,  # Troff
            0x30,  # N64 Logo
            0x34,  # Mech Fish
            0x42,  # Krossbones
            0x47,  # Rabbit
            0x4B,  # Minecart Skeleton Head
            0x51,  # Tomato
            0x62,  # Ice Tomato
            0x69,  # Golden Banana
            0x70,  # Microbuffer
            0x72,  # Bell
            0x96,  # Missile (Car Race)
            0xB0,  # Red Buoy
            0xB1,  # Green Buoy
            0xBD,  # Rareware Logo
        ]
        model_index = random.choice(permitted_models)
    spoiler.settings.klaptrap_model_index = model_index
    ROM().seek(spoiler.settings.rom_data + 0x136)
    ROM().writeMultipleBytes(model_index, 1)
    color_palettes = []
    color_obj = {}
    colors_dict = {}
    kong_settings = [
        {"kong": "dk", "palettes": [{"name": "base", "image": 3724, "fill_type": "block"}], "base_setting": "dk_colors", "custom_setting": "dk_custom_color", "kong_index": 0},
        {"kong": "diddy", "palettes": [{"name": "cap_shirt", "image": 3686, "fill_type": "block"}], "base_setting": "diddy_colors", "custom_setting": "diddy_custom_color", "kong_index": 1},
        {
            "kong": "lanky",
            "palettes": [{"name": "overalls", "image": 3689, "fill_type": "block"}, {"name": "patch", "image": 3734, "fill_type": "patch"}],
            "base_setting": "lanky_colors",
            "custom_setting": "lanky_custom_color",
            "kong_index": 2,
        },
        {"kong": "tiny", "palettes": [{"name": "overalls", "image": 6014, "fill_type": "block"}], "base_setting": "tiny_colors", "custom_setting": "tiny_custom_color", "kong_index": 3},
        {
            "kong": "chunky",
            "palettes": [{"name": "shirt_back", "image": 3769, "fill_type": "checkered"}, {"name": "shirt_front", "image": 3687, "fill_type": "block"}],
            "base_setting": "chunky_colors",
            "custom_setting": "chunky_custom_color",
            "kong_index": 4,
        },
        {
            "kong": "disco_chunky",
            "palettes": [{"name": "shirt", "image": 3777, "fill_type": "sparkle"}, {"name": "gloves", "image": 3778, "fill_type": "sparkle"}],
            "base_setting": "chunky_colors",
            "custom_setting": "chunky_custom_color",
            "kong_index": 4,
        },
        {"kong": "rambi", "palettes": [{"name": "base", "image": 3826, "fill_type": "block"}], "base_setting": "rambi_colors", "custom_setting": "rambi_custom_color", "kong_index": 5},
        {"kong": "enguarde", "palettes": [{"name": "base", "image": 3847, "fill_type": "block"}], "base_setting": "enguarde_colors", "custom_setting": "enguarde_custom_color", "kong_index": 6},
    ]

    if js.document.getElementById("override_cosmetics").checked:
        if js.document.getElementById("random_colors").checked:
            spoiler.settings.dk_colors = "randomized"
            spoiler.settings.diddy_colors = "randomized"
            spoiler.settings.lanky_colors = "randomized"
            spoiler.settings.tiny_colors = "randomized"
            spoiler.settings.chunky_colors = "randomized"
            spoiler.settings.rambi_colors = "randomized"
            spoiler.settings.enguarde_colors = "randomized"
        else:
            spoiler.settings.dk_colors = js.document.getElementById("dk_colors").value
            spoiler.settings.dk_custom_color = js.document.getElementById("dk_custom_color").value
            spoiler.settings.diddy_colors = js.document.getElementById("diddy_colors").value
            spoiler.settings.diddy_custom_color = js.document.getElementById("diddy_custom_color").value
            spoiler.settings.lanky_colors = js.document.getElementById("lanky_colors").value
            spoiler.settings.lanky_custom_color = js.document.getElementById("lanky_custom_color").value
            spoiler.settings.tiny_colors = js.document.getElementById("tiny_colors").value
            spoiler.settings.tiny_custom_color = js.document.getElementById("tiny_custom_color").value
            spoiler.settings.chunky_colors = js.document.getElementById("chunky_colors").value
            spoiler.settings.chunky_custom_color = js.document.getElementById("chunky_custom_color").value
            spoiler.settings.rambi_colors = js.document.getElementById("rambi_colors").value
            spoiler.settings.rambi_custom_color = js.document.getElementById("rambi_custom_color").value
            spoiler.settings.enguarde_colors = js.document.getElementById("enguarde_colors").value
            spoiler.settings.enguarde_custom_color = js.document.getElementById("enguarde_custom_color").value
    else:
        if spoiler.settings.random_colors:
            spoiler.settings.dk_colors = "randomized"
            spoiler.settings.diddy_colors = "randomized"
            spoiler.settings.lanky_colors = "randomized"
            spoiler.settings.tiny_colors = "randomized"
            spoiler.settings.chunky_colors = "randomized"
            spoiler.settings.rambi_colors = "randomized"
            spoiler.settings.enguarde_colors = "randomized"

    colors_dict = {
        "dk_colors": spoiler.settings.dk_colors,
        "dk_custom_color": spoiler.settings.dk_custom_color,
        "diddy_colors": spoiler.settings.diddy_colors,
        "diddy_custom_color": spoiler.settings.diddy_custom_color,
        "lanky_colors": spoiler.settings.lanky_colors,
        "lanky_custom_color": spoiler.settings.lanky_custom_color,
        "tiny_colors": spoiler.settings.tiny_colors,
        "tiny_custom_color": spoiler.settings.tiny_custom_color,
        "chunky_colors": spoiler.settings.chunky_colors,
        "chunky_custom_color": spoiler.settings.chunky_custom_color,
        "rambi_colors": spoiler.settings.rambi_colors,
        "rambi_custom_color": spoiler.settings.rambi_custom_color,
        "enguarde_colors": spoiler.settings.enguarde_colors,
        "enguarde_custom_color": spoiler.settings.enguarde_custom_color,
    }
    for kong in kong_settings:
        process = True
        if kong["kong_index"] == 4:  # Chunky
            is_disco = spoiler.settings.disco_chunky
            if spoiler.settings.krusha_slot == "chunky":
                is_disco = False
            if is_disco and kong["kong"] == "chunky":
                process = False
            elif not is_disco and kong["kong"] == "disco_chunky":
                process = False
        kong_names = ["dk", "diddy", "lanky", "tiny", "chunky"]
        is_krusha = False
        if spoiler.settings.krusha_slot in kong_names:
            if kong_names.index(spoiler.settings.krusha_slot) == kong["kong_index"]:
                is_krusha = True
                kong["palettes"] = [
                    {"name": "krusha_skin", "image": 4971, "fill_type": "block"},
                    {"name": "krusha_indicator", "image": 4966, "fill_type": "kong"},
                ]
        if process:
            base_obj = {"kong": kong["kong"], "zones": []}
            for palette in kong["palettes"]:
                arr = ["#000000"]
                if palette["fill_type"] == "checkered":
                    arr = ["#000000", "#000000"]
                elif palette["fill_type"] == "kong":
                    kong_colors = ["#ffd700", "#ff0000", "#1699ff", "#B045ff", "#41ff25"]
                    arr = [kong_colors[kong["kong_index"]]]
                base_obj["zones"].append({"zone": palette["name"], "image": palette["image"], "fill_type": palette["fill_type"], "colors": arr})
            if colors_dict[kong["base_setting"]] != "vanilla":
                if colors_dict[kong["base_setting"]] == "randomized":
                    color = f"#{format(randint(0, 0xFFFFFF), '06x')}"
                else:
                    color = colors_dict[kong["custom_setting"]]
                    if not color:
                        color = "#000000"
                base_obj["zones"][0]["colors"][0] = color
                if kong["kong_index"] in (2, 4) and not is_krusha:
                    base_obj["zones"][1]["colors"][0] = color
                    if kong["kong_index"] == 4:
                        red = int(f"0x{color[1:3]}", 16)
                        green = int(f"0x{color[3:5]}", 16)
                        blue = int(f"0x{color[5:7]}", 16)
                        opp_color = f"#{format(255-red,'02x')}{format(255-green,'02x')}{format(255-blue,'02x')}"
                        if spoiler.settings.disco_chunky:
                            base_obj["zones"][1]["colors"][0] = opp_color
                        else:
                            base_obj["zones"][0]["colors"][1] = opp_color
                color_palettes.append(base_obj)
                color_obj[f"{kong['kong']}"] = color
    spoiler.settings.colors = color_obj
    if len(color_palettes) > 0:
        print(color_palettes)
        convertColors(color_palettes)


color_bases = [
    "#1D439E",
    "#FF0000",
    "#66C7FF",
    "#FFC302",
    "#000000",
]
balloon_single_frames = [
    (4, 38),
    (5, 38),
    (5, 38),
    (5, 38),
    (5, 38),
    (5, 38),
    (4, 38),
    (4, 38),
]


def getFile(table_index: int, file_index: int, compressed: bool, width: int, height: int):
    """Grab image from file."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    ROM().seek(file_start)
    data = ROM().readBytes(file_size)
    if compressed:
        data = zlib.decompress(data, (15 + 32))
    im_f = Image.new(mode="RGBA", size=(width, height))
    pix = im_f.load()
    for y in range(height):
        for x in range(width):
            offset = ((y * width) + x) * 2
            pix_data = int.from_bytes(data[offset : offset + 2], "big")
            red = ((pix_data >> 11) & 31) << 3
            green = ((pix_data >> 6) & 31) << 3
            blue = ((pix_data >> 1) & 31) << 3
            alpha = (pix_data & 1) * 255
            pix[x, y] = (red, green, blue, alpha)
    return im_f


def getRGBFromHash(hash: str):
    """Convert hash RGB code to rgb array."""
    red = int(hash[1:3], 16)
    green = int(hash[3:5], 16)
    blue = int(hash[5:7], 16)
    return [red, green, blue]


def maskImage(im_f, base_index, min_y):
    """Apply RGB mask to image."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getRGBFromHash(color_bases[base_index])
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            for channel in range(3):
                base[channel] = int(mask[channel] * (base[channel] / 255))
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def writeColorImageToROM(im_f, table_index, file_index, width, height):
    """Write texture to ROM."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    ROM().seek(file_start)
    pix = im_f.load()
    width, height = im_f.size
    bytes_array = []
    for y in range(height):
        for x in range(width):
            pix_data = list(pix[x, y])
            red = int((pix_data[0] >> 3) << 11)
            green = int((pix_data[1] >> 3) << 6)
            blue = int((pix_data[2] >> 3) << 1)
            alpha = int(pix_data[3] != 0)
            value = red | green | blue | alpha
            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    data = bytearray(bytes_array)
    if len(data) > (2 * width * height):
        print(f"Image too big error: {table_index} > {file_index}")
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    ROM().writeBytes(data)


def overwrite_object_colors():
    """Overwrite object colors."""
    file = 175
    dk_single = getFile(7, file, False, 44, 44)
    dk_single = dk_single.resize((21, 21))
    for kong_index in range(5):
        file = 4120
        # Kasplat Hair
        hair_im = getFile(25, file, True, 32, 44)
        hair_im = maskImage(hair_im, kong_index, 0)
        writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44)
        for file in range(152, 160):
            # Single
            single_im = getFile(7, file, False, 44, 44)
            single_im = maskImage(single_im, kong_index, 0)
            single_start = [168, 152, 232, 208, 240]
            writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44)
        for file in range(216, 224):
            # Coin
            coin_im = getFile(7, file, False, 48, 42)
            coin_im = maskImage(coin_im, kong_index, 0)
            coin_start = [224, 256, 248, 216, 264]
            writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42)
        for file in range(274, 286):
            # Bunch
            bunch_im = getFile(7, file, False, 44, 44)
            bunch_im = maskImage(bunch_im, kong_index, 0)
            bunch_start = [274, 854, 818, 842, 830]
            writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44)
        for file in range(5819, 5827):
            # Balloon
            balloon_im = getFile(25, file, True, 32, 64)
            balloon_im = maskImage(balloon_im, kong_index, 33)
            balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
            balloon_start = [5835, 5827, 5843, 5851, 5819]
            writeColorImageToROM(balloon_im, 25, balloon_start[kong_index] + (file - 5819), 32, 64)
