"""Apply cosmetic skins to kongs."""
import random
from random import randint

import js
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Lib import intf_to_float, float_to_hex, int_to_list, getObjectAddress
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, ColorblindMode, HelmDoorItem, KlaptrapModel
from PIL import Image, ImageEnhance, ImageDraw
import zlib
import gzip


class HelmDoorSetting:
    """Class to store information regarding helm doors."""

    def __init__(self, item_setting: HelmDoorItem, count: int, item_image: int, number_image: int):
        """Initialize with given parameters."""
        self.item_setting = item_setting
        self.count = count
        self.item_image = item_image
        self.number_image = number_image


class HelmDoorImages:
    """Class to store information regarding helm door item images."""

    def __init__(self, setting: HelmDoorItem, image_indexes: list, flip=False, table=25, dimensions=(44, 44), format="rgba5551"):
        """Initialize with given parameters."""
        self.setting = setting
        self.image_indexes = image_indexes
        self.flip = flip
        self.table = table
        self.dimensions = dimensions
        self.format = format


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    model_index = 0
    sav = spoiler.settings.rom_data
    if js.document.getElementById("override_cosmetics").checked:
        model_setting = KlaptrapModel[js.document.getElementById("klaptrap_model").value]
    else:
        model_setting = spoiler.settings.klaptrap_model
    if model_setting == KlaptrapModel.green:
        model_index = 0x21
    elif model_setting == KlaptrapModel.purple:
        model_index = 0x22
    elif model_setting == KlaptrapModel.red:
        model_index = 0x23
    elif model_setting == KlaptrapModel.random_klap:
        model_index = random.randint(0x21, 0x23)
    elif model_setting == KlaptrapModel.random_model:
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
    if spoiler.settings.misc_cosmetics:
        ROM().seek(sav + 0x196)
        ROM().write(1)
        # Skybox RGBA
        ROM().seek(sav + 0x197)
        for channel in range(24):
            ROM().writeMultipleBytes(random.randint(0, 255), 1)
        # Klaptrap Colors
        ROM().seek(sav + 0x1AF)
        for klaptrap in range(2):
            ROM().writeMultipleBytes(random.randint(0, 2), 1)
        # Wrinkly Color
        ROM().seek(sav + 0x1B1)
        for channel in range(3):
            ROM().writeMultipleBytes(random.randint(0, 255), 1)
    ROM().seek(sav + 0x136)
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
            spoiler.settings.dk_colors = CharacterColors.randomized
            spoiler.settings.diddy_colors = CharacterColors.randomized
            spoiler.settings.lanky_colors = CharacterColors.randomized
            spoiler.settings.tiny_colors = CharacterColors.randomized
            spoiler.settings.chunky_colors = CharacterColors.randomized
            spoiler.settings.rambi_colors = CharacterColors.randomized
            spoiler.settings.enguarde_colors = CharacterColors.randomized
        else:
            spoiler.settings.dk_colors = CharacterColors[js.document.getElementById("dk_colors").value]
            spoiler.settings.dk_custom_color = js.document.getElementById("dk_custom_color").value
            spoiler.settings.diddy_colors = CharacterColors[js.document.getElementById("diddy_colors").value]
            spoiler.settings.diddy_custom_color = js.document.getElementById("diddy_custom_color").value
            spoiler.settings.lanky_colors = CharacterColors[js.document.getElementById("lanky_colors").value]
            spoiler.settings.lanky_custom_color = js.document.getElementById("lanky_custom_color").value
            spoiler.settings.tiny_colors = CharacterColors[js.document.getElementById("tiny_colors").value]
            spoiler.settings.tiny_custom_color = js.document.getElementById("tiny_custom_color").value
            spoiler.settings.chunky_colors = CharacterColors[js.document.getElementById("chunky_colors").value]
            spoiler.settings.chunky_custom_color = js.document.getElementById("chunky_custom_color").value
            spoiler.settings.rambi_colors = CharacterColors[js.document.getElementById("rambi_colors").value]
            spoiler.settings.rambi_custom_color = js.document.getElementById("rambi_custom_color").value
            spoiler.settings.enguarde_colors = CharacterColors[js.document.getElementById("enguarde_colors").value]
            spoiler.settings.enguarde_custom_color = js.document.getElementById("enguarde_custom_color").value
    else:
        if spoiler.settings.random_colors:
            spoiler.settings.dk_colors = CharacterColors.randomized
            spoiler.settings.diddy_colors = CharacterColors.randomized
            spoiler.settings.lanky_colors = CharacterColors.randomized
            spoiler.settings.tiny_colors = CharacterColors.randomized
            spoiler.settings.chunky_colors = CharacterColors.randomized
            spoiler.settings.rambi_colors = CharacterColors.randomized
            spoiler.settings.enguarde_colors = CharacterColors.randomized

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
            if spoiler.settings.krusha_kong == Kongs.chunky:
                is_disco = False
            if is_disco and kong["kong"] == "chunky":
                process = False
            elif not is_disco and kong["kong"] == "disco_chunky":
                process = False
        is_krusha = False
        if spoiler.settings.krusha_kong is not None:
            if spoiler.settings.krusha_kong == kong["kong_index"]:
                is_krusha = True
                kong["palettes"] = [{"name": "krusha_skin", "image": 4971, "fill_type": "block"}, {"name": "krusha_indicator", "image": 4966, "fill_type": "kong"}]
                process = True
        if process:
            base_obj = {"kong": kong["kong"], "zones": []}
            for palette in kong["palettes"]:
                arr = ["#000000"]
                if palette["fill_type"] == "checkered":
                    arr = ["#000000", "#000000"]
                elif palette["fill_type"] == "kong":
                    kong_colors = ["#ffd700", "#ff0000", "#1699ff", "#B045ff", "#41ff25"]
                    mode = spoiler.settings.colorblind_mode
                    if mode != ColorblindMode.off:
                        if mode == ColorblindMode.prot:
                            kong_colors = ["#FDE400", "#0072FF", "#766D5A", "#FFFFFF", "#000000"]
                        elif mode == ColorblindMode.deut:
                            kong_colors = ["#E3A900", "#318DFF", "#7F6D59", "#FFFFFF", "#000000"]
                        elif mode == ColorblindMode.trit:
                            kong_colors = ["#FFA4A4", "#C72020", "#13C4D8", "#FFFFFF", "#000000"]
                    arr = [kong_colors[kong["kong_index"]]]
                base_obj["zones"].append({"zone": palette["name"], "image": palette["image"], "fill_type": palette["fill_type"], "colors": arr})
            if colors_dict[kong["base_setting"]] != CharacterColors.vanilla:
                if colors_dict[kong["base_setting"]] == CharacterColors.randomized:
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
            elif is_krusha:
                del base_obj["zones"][0]
                color_palettes.append(base_obj)
    spoiler.settings.colors = color_obj
    if len(color_palettes) > 0:
        convertColors(color_palettes)


color_bases = []
balloon_single_frames = [(4, 38), (5, 38), (5, 38), (5, 38), (5, 38), (5, 38), (4, 38), (4, 38)]


def getFile(table_index: int, file_index: int, compressed: bool, width: int, height: int, format: str):
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
            if format == "rgba32":
                offset = ((y * width) + x) * 4
                pix_data = int.from_bytes(data[offset : offset + 4], "big")
                red = (pix_data >> 24) & 0xFF
                green = (pix_data >> 16) & 0xFF
                blue = (pix_data >> 8) & 0xFF
                alpha = pix_data & 0xFF
            else:
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
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def hueShift(im, amount):
    """Apply a hue shift on an image."""
    hsv_im = im.convert("HSV")
    im_px = im.load()
    w, h = hsv_im.size
    hsv_px = hsv_im.load()
    for y in range(h):
        for x in range(w):
            old = list(hsv_px[x, y]).copy()
            old[0] = (old[0] + amount) % 360
            hsv_px[x, y] = (old[0], old[1], old[2])
    rgb_im = hsv_im.convert("RGB")
    rgb_px = rgb_im.load()
    for y in range(h):
        for x in range(w):
            new = list(rgb_px[x, y])
            new.append(list(im_px[x, y])[3])
            im_px[x, y] = (new[0], new[1], new[2], new[3])
    return im


def maskImageMonochrome(im_f, base_index, min_y):
    """Apply RGB mask to image in Black and White."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getRGBFromHash("#FFFFFF")
    mask2 = mask.copy()
    previous_pixel_opaque = False
    invert = False
    if color_bases[base_index] == "#000000":
        invert = True
    for channel in range(3):
        mask2[channel] = int(255 - mask2[channel])
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                if not previous_pixel_opaque or (x < (w - 1) and list(pix[(x + 1), y])[3] == 0):
                    # create an outline that contrasts the main color (black if white, white if black)
                    for channel in range(3):
                        base[channel] = int(mask2[channel])
                else:
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                if invert:
                    for channel in range(3):
                        base[channel] = int(255 - base[channel])
                pix[x, y] = (base[0], base[1], base[2], base[3])
                previous_pixel_opaque = True
            else:
                previous_pixel_opaque = False
    return im_f


def writeColorImageToROM(im_f, table_index, file_index, width, height, transparent_border: bool):
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
            if transparent_border and ((x == 0) or (y == 0) or (x >= (width - 1)) or (y >= (height - 1))):
                pix_data = [0, 0, 0, 0]
            else:
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
    if table_index in (14, 25):
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    ROM().writeBytes(data)


def writeColorToROM(color, table_index, file_index):
    """Write color to ROM for kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color)
    val_r = int((mask[0] >> 3) << 11)
    val_g = int((mask[1] >> 3) << 6)
    val_b = int((mask[2] >> 3) << 1)
    rgba_val = val_r | val_g | val_b | 1
    bytes_array = []
    for y in range(42):
        for x in range(32):
            bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
    for i in range(18):
        bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
    for i in range(4):
        bytes_array.extend([0, 0])
    for i in range(3):
        bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeWhiteKasplatColorToROM(color1, color2, table_index, file_index):
    """Write color to ROM for white kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color1)
    val_r = int((mask[0] >> 3) << 11)
    val_g = int((mask[1] >> 3) << 6)
    val_b = int((mask[2] >> 3) << 1)
    rgba_val = val_r | val_g | val_b | 1
    mask2 = getRGBFromHash(color2)
    val_r2 = int((mask2[0] >> 3) << 11)
    val_g2 = int((mask2[1] >> 3) << 6)
    val_b2 = int((mask2[2] >> 3) << 1)
    rgba_val2 = val_r2 | val_g2 | val_b2 | 1
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if y % 10 > 1:
                bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
            else:
                bytes_array.extend([(rgba_val2 >> 8) & 0xFF, rgba_val2 & 0xFF])
    for i in range(18):
        bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
    for i in range(4):
        bytes_array.extend([0, 0])
    for i in range(3):
        bytes_array.extend([(rgba_val >> 8) & 0xFF, rgba_val & 0xFF])
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def overwrite_object_colors(spoiler: Spoiler):
    """Overwrite object colors."""
    global color_bases
    mode = spoiler.settings.colorblind_mode
    if mode != ColorblindMode.off:
        if mode == ColorblindMode.prot:
            color_bases = ["#FDE400", "#0072FF", "#766D5A", "#FFFFFF", "#000000"]
        elif mode == ColorblindMode.deut:
            color_bases = ["#E3A900", "#318DFF", "#7F6D59", "#FFFFFF", "#000000"]
        elif mode == ColorblindMode.trit:
            color_bases = ["#FFA4A4", "#C72020", "#13C4D8", "#FFFFFF", "#000000"]
        file = 175
        dk_single = getFile(7, file, False, 44, 44, "rgba5551")
        dk_single = dk_single.resize((21, 21))
        for kong_index in range(5):
            if kong_index == 3 or kong_index == 4:
                if color_bases[kong_index] == "#FFFFFF":
                    writeWhiteKasplatColorToROM(color_bases[kong_index], "#000000", 25, [4124, 4122, 4123, 4120, 4121][kong_index])
                else:
                    writeColorToROM(color_bases[kong_index], 25, [4124, 4122, 4123, 4120, 4121][kong_index])
                for file in range(152, 160):
                    # Single
                    single_im = getFile(7, file, False, 44, 44, "rgba5551")
                    single_im = maskImageMonochrome(single_im, kong_index, 0)
                    single_start = [168, 152, 232, 208, 240]
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False)
                for file in range(216, 224):
                    # Coin
                    coin_im = getFile(7, file, False, 48, 42, "rgba5551")
                    coin_im = maskImageMonochrome(coin_im, kong_index, 0)
                    coin_start = [224, 256, 248, 216, 264]
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False)
                for file in range(274, 286):
                    # Bunch
                    bunch_im = getFile(7, file, False, 44, 44, "rgba5551")
                    bunch_im = maskImageMonochrome(bunch_im, kong_index, 0)
                    bunch_start = [274, 854, 818, 842, 830]
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getFile(25, file, True, 32, 64, "rgba5551")
                    balloon_im = maskImageMonochrome(balloon_im, kong_index, 33)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    balloon_start = [5835, 5827, 5843, 5851, 5819]
                    writeColorImageToROM(balloon_im, 25, balloon_start[kong_index] + (file - 5819), 32, 64, False)
            else:
                # file = 4120
                # # Kasplat Hair
                # hair_im = getFile(25, file, True, 32, 44, "rgba5551")
                # hair_im = maskImage(hair_im, kong_index, 0)
                writeColorToROM(color_bases[kong_index], 25, [4124, 4122, 4123, 4120, 4121][kong_index])
                # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False)
                for file in range(152, 160):
                    # Single
                    single_im = getFile(7, file, False, 44, 44, "rgba5551")
                    single_im = maskImage(single_im, kong_index, 0)
                    single_start = [168, 152, 232, 208, 240]
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False)
                for file in range(216, 224):
                    # Coin
                    coin_im = getFile(7, file, False, 48, 42, "rgba5551")
                    coin_im = maskImage(coin_im, kong_index, 0)
                    coin_start = [224, 256, 248, 216, 264]
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False)
                for file in range(274, 286):
                    # Bunch
                    bunch_im = getFile(7, file, False, 44, 44, "rgba5551")
                    bunch_im = maskImage(bunch_im, kong_index, 0)
                    bunch_start = [274, 854, 818, 842, 830]
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getFile(25, file, True, 32, 64, "rgba5551")
                    balloon_im = maskImage(balloon_im, kong_index, 33)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    balloon_start = [5835, 5827, 5843, 5851, 5819]
                    writeColorImageToROM(balloon_im, 25, balloon_start[kong_index] + (file - 5819), 32, 64, False)


def applyKrushaKong(spoiler: Spoiler):
    """Apply Krusha Kong setting."""
    ROM().seek(spoiler.settings.rom_data + 0x11C)
    if spoiler.settings.krusha_kong is None:
        ROM().write(255)
    elif spoiler.settings.krusha_kong < 5:
        ROM().write(spoiler.settings.krusha_kong)
        placeKrushaHead(spoiler.settings.krusha_kong)
        changeKrushaModel(spoiler.settings.krusha_kong)
        if spoiler.settings.krusha_kong == Kongs.donkey:
            fixBaboonBlasts()


DK_SCALE = 0.75
GENERIC_SCALE = 0.49
krusha_scaling = [
    # [x, y, z, xz, y]
    # DK
    [lambda x: x * DK_SCALE, lambda x: x * DK_SCALE, lambda x: x * GENERIC_SCALE, lambda x: x * DK_SCALE, lambda x: x * DK_SCALE],
    # Diddy
    [lambda x: (x * 1.043) - 41.146, lambda x: (x * 9.893) - 8.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.103) - 14.759, lambda x: (x * 0.823) + 35.220],
    # Lanky
    [lambda x: (x * 0.841) - 17.231, lambda x: (x * 6.925) - 2.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 0.680) - 18.412, lambda x: (x * 0.789) + 42.138],
    # Tiny
    [lambda x: (x * 0.632) + 7.590, lambda x: (x * 6.925) + 0.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.567) - 21.676, lambda x: (x * 0.792) + 41.509],
    # Chunky
    [lambda x: x, lambda x: x, lambda x: x, lambda x: x, lambda x: x],
]


def readListAsInt(arr: list, start: int, size: int) -> int:
    """Read list and convert to int."""
    val = 0
    for i in range(size):
        val = (val * 256) + arr[start + i]
    return val


def changeKrushaModel(krusha_kong: int):
    """Modify Krusha Model to be smaller to enable him to fit through smaller gaps."""
    krusha_model_start = js.pointer_addresses[5]["entries"][0xDA]["pointing_to"]
    krusha_model_finish = js.pointer_addresses[5]["entries"][0xDB]["pointing_to"]
    krusha_model_size = krusha_model_finish - krusha_model_start
    ROM().seek(krusha_model_start)
    indicator = int.from_bytes(ROM().readBytes(2), "big")
    ROM().seek(krusha_model_start)
    data = ROM().readBytes(krusha_model_size)
    if indicator == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    num_data = []  # data, but represented as nums rather than b strings
    for d in data:
        num_data.append(d)
    base = 0x450C
    count_0 = readListAsInt(num_data, base, 4)
    changes = krusha_scaling[krusha_kong][:3]
    changes_0 = [
        krusha_scaling[krusha_kong][3],
        krusha_scaling[krusha_kong][4],
        krusha_scaling[krusha_kong][3],
    ]
    for i in range(count_0):
        i_start = base + 4 + (i * 0x14)
        for coord_index, change in enumerate(changes):
            val_i = readListAsInt(num_data, i_start + (4 * coord_index) + 4, 4)
            val_f = change(intf_to_float(val_i))
            val_i = int(float_to_hex(val_f), 16)
            for di, d in enumerate(int_to_list(val_i, 4)):
                num_data[i_start + (4 * coord_index) + 4 + di] = d
    section_2_start = base + 4 + (count_0 * 0x14)
    count_1 = readListAsInt(num_data, section_2_start, 4)
    for i in range(count_1):
        i_start = section_2_start + 4 + (i * 0x10)
        for coord_index, change in enumerate(changes_0):
            val_i = readListAsInt(num_data, i_start + (4 * coord_index), 4)
            val_f = change(intf_to_float(val_i))
            val_i = int(float_to_hex(val_f), 16)
            for di, d in enumerate(int_to_list(val_i, 4)):
                num_data[i_start + (4 * coord_index) + di] = d
    data = bytearray(num_data)  # convert num_data back to binary string
    if indicator == 0x1F8B:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(krusha_model_start)
    ROM().writeBytes(data)


def fixBaboonBlasts():
    """Fix various baboon blasts to work for Krusha."""
    # Fungi Baboon Blast
    for id in (2, 5):
        item_start = getObjectAddress(0xBC, id, "actor")
        if item_start is not None:
            ROM().seek(item_start + 0x14)
            ROM().writeMultipleBytes(0xFFFFFFEC, 4)
            ROM().seek(item_start + 0x1B)
            ROM().writeMultipleBytes(0, 1)
    # Caves Baboon Blast
    item_start = getObjectAddress(0xBA, 4, "actor")
    if item_start is not None:
        ROM().seek(item_start + 0x4)
        ROM().writeMultipleBytes(int(float_to_hex(510), 16), 4)
    item_start = getObjectAddress(0xBA, 12, "actor")
    if item_start is not None:
        ROM().seek(item_start + 0x4)
        ROM().writeMultipleBytes(int(float_to_hex(333), 16), 4)
    # Castle Baboon Blast
    item_start = getObjectAddress(0xBB, 4, "actor")
    if item_start is not None:
        ROM().seek(item_start + 0x0)
        ROM().writeMultipleBytes(int(float_to_hex(2472), 16), 4)
        ROM().seek(item_start + 0x8)
        ROM().writeMultipleBytes(int(float_to_hex(1980), 16), 4)


def placeKrushaHead(slot):
    """Replace a kong's face with the Krusha face."""
    kong_face_textures = [[0x27C, 0x27B], [0x279, 0x27A], [0x277, 0x278], [0x276, 0x275], [0x273, 0x274]]
    unc_face_textures = [[579, 586], [580, 587], [581, 588], [582, 589], [577, 578]]
    ROM().seek(0x1FF6000)
    left = []
    right = []
    img32 = []
    img32_rgba32 = []
    y32 = []
    y32_rgba32 = []
    for y in range(64):
        x32 = []
        x32_rgba32 = []
        for x in range(64):
            data_hi = int.from_bytes(ROM().readBytes(1), "big")
            data_lo = int.from_bytes(ROM().readBytes(1), "big")
            val = (data_hi << 8) | data_lo
            val_r = ((val >> 11) & 0x1F) << 3
            val_g = ((val >> 6) & 0x1F) << 3
            val_b = ((val >> 1) & 0x1F) << 3
            val_a = 0
            if val & 1:
                val_a = 255
            data_rgba32 = [val_r, val_g, val_b, val_a]
            if x < 32:
                right.extend([data_hi, data_lo])
            else:
                left.extend([data_hi, data_lo])
            if ((x % 2) + (y % 2)) == 0:
                x32.extend([data_hi, data_lo])
                x32_rgba32.extend(data_rgba32)
        if len(x32) > 0 and len(x32_rgba32):
            y32.append(x32)
            y32_rgba32.append(x32_rgba32)
    y32.reverse()
    for y in y32:
        img32.extend(y)
    y32_rgba32.reverse()
    for y in y32_rgba32:
        img32_rgba32.extend(y)
    for x in range(2):
        img_data = [right, left][x]
        texture_index = kong_face_textures[slot][x]
        unc_index = unc_face_textures[slot][x]
        texture_addr = js.pointer_addresses[25]["entries"][texture_index]["pointing_to"]
        unc_addr = js.pointer_addresses[7]["entries"][unc_index]["pointing_to"]
        data = gzip.compress(bytearray(img_data), compresslevel=9)
        ROM().seek(texture_addr)
        ROM().writeBytes(data)
        ROM().seek(unc_addr)
        ROM().writeBytes(bytearray(img_data))
    rgba32_addr32 = js.pointer_addresses[14]["entries"][196 + slot]["pointing_to"]
    rgba16_addr32 = js.pointer_addresses[14]["entries"][190 + slot]["pointing_to"]
    data32 = gzip.compress(bytearray(img32), compresslevel=9)
    data32_rgba32 = gzip.compress(bytearray(img32_rgba32), compresslevel=9)
    ROM().seek(rgba32_addr32)
    ROM().writeBytes(bytearray(data32_rgba32))
    ROM().seek(rgba16_addr32)
    ROM().writeBytes(bytearray(data32))


def writeMiscCosmeticChanges(spoiler: Spoiler):
    """Write miscellaneous changes to the cosmetic colors."""
    if spoiler.settings.misc_cosmetics:
        # Melon HUD
        data = {7: [0x13C, 0x147], 14: [0x5A, 0x5D], 25: [0x17B2, 0x17B2]}
        shift = random.randint(0, 359)
        for table in data:
            table_data = data[table]
            for img in range(table_data[0], table_data[1] + 1):
                if table == 25 and img == 0x17B2:
                    dims = (32, 32)
                else:
                    dims = (48, 42)
                melon_im = getFile(table, img, table != 7, dims[0], dims[1], "rgba5551")
                melon_im = hueShift(melon_im, shift)
                melon_px = melon_im.load()
                bytes_array = []
                for y in range(dims[1]):
                    for x in range(dims[0]):
                        pix_data = list(melon_px[x, y])
                        red = int((pix_data[0] >> 3) << 11)
                        green = int((pix_data[1] >> 3) << 6)
                        blue = int((pix_data[2] >> 3) << 1)
                        alpha = int(pix_data[3] != 0)
                        value = red | green | blue | alpha
                        bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
                px_data = bytearray(bytes_array)
                if table != 7:
                    px_data = gzip.compress(px_data, compresslevel=9)
                ROM().seek(js.pointer_addresses[table]["entries"][img]["pointing_to"])
                ROM().writeBytes(px_data)


def getNumberImage(number: int):
    """Get Number Image from number."""
    if number < 5:
        num_0_bounds = [0, 20, 30, 45, 58, 76]
        x = number
        return getFile(14, 15, True, 76, 24, "rgba5551").crop((num_0_bounds[x], 0, num_0_bounds[x + 1], 24))
    num_1_bounds = [0, 15, 28, 43, 58, 76]
    x = number - 5
    return getFile(14, 16, True, 76, 24, "rgba5551").crop((num_1_bounds[x], 0, num_1_bounds[x + 1], 24))


def numberToImage(number: int, dim: tuple):
    """Convert multi-digit number to image."""
    digits = 1
    if number < 10:
        digits = 1
    elif number < 100:
        digits = 2
    else:
        digits = 3
    allocation_per_digit = (dim[0] / digits, dim[1])
    base = Image.new(mode="RGBA", size=dim)
    current = number
    for d in range(digits):
        num_im = getNumberImage(current % 10)
        current = int(current / 10)
        num_w, num_h = num_im.size
        xscale = allocation_per_digit[0] / num_w
        yscale = allocation_per_digit[1] / num_h
        scale = min(xscale, yscale)
        num_im = num_im.resize((int(num_w * scale), int(num_h * scale)))
        slot_start = (dim[0] / digits) * ((digits - 1) - d)
        slot_middle = slot_start + ((dim[0] / digits) / 2)
        base.paste(num_im, (int(slot_middle - ((num_w * scale) / 2)), 0), num_im)
    return base


def applyHelmDoorCosmetics(spoiler: Spoiler):
    """Apply Helm Door Cosmetic Changes."""
    Doors = [
        HelmDoorSetting(spoiler.settings.crown_door_item, spoiler.settings.crown_door_item_count, 6022, 6023),
        HelmDoorSetting(spoiler.settings.coin_door_item, spoiler.settings.coin_door_item_count, 6024, 6025),
    ]
    Images = [
        HelmDoorImages(HelmDoorItem.req_gb, [0x155C]),
        HelmDoorImages(HelmDoorItem.req_bp, [x + 4 for x in (0x15F8, 0x15E8, 0x158F, 0x1600, 0x15F0)], False, 25, (48, 42)),
        HelmDoorImages(HelmDoorItem.req_bean, [0], True, 6, (20, 20)),
        HelmDoorImages(HelmDoorItem.req_pearl, [0xD5F], False, 25, (32, 32)),
        HelmDoorImages(HelmDoorItem.req_fairy, [0x16ED], False, 25, (32, 32), "rgba32"),
        HelmDoorImages(HelmDoorItem.req_key, [5877]),
        HelmDoorImages(HelmDoorItem.req_medal, [0x156C]),
        HelmDoorImages(HelmDoorItem.req_rainbowcoin, [5963], False, 25, (48, 42)),
        HelmDoorImages(HelmDoorItem.req_crown, [5893]),
        HelmDoorImages(HelmDoorItem.req_companycoins, [5905, 5912]),
    ]
    for door in Doors:
        for image_data in Images:
            if image_data.setting == door.item_setting:
                base = Image.new(mode="RGBA", size=(44, 44))
                base_overlay = Image.new(mode="RGBA", size=image_data.dimensions)
                for image_slot, image in enumerate(image_data.image_indexes):
                    item_im = getFile(image_data.table, image, image_data.table in (14, 25), image_data.dimensions[0], image_data.dimensions[1], image_data.format)
                    start_x = 0
                    finish_x = image_data.dimensions[0]
                    if len(image_data.image_indexes) > 1:
                        start_x = int(image_slot * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        finish_x = int((image_slot + 1) * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        item_im = item_im.crop((start_x, 0, finish_x, image_data.dimensions[1]))
                    base_overlay.paste(item_im, (start_x, 0), item_im)
                if image_data.flip:
                    base_overlay = base_overlay.transpose(Image.FLIP_TOP_BOTTOM)
                if image_data.dimensions[0] > image_data.dimensions[1]:
                    # Width shrinked to 44
                    new_height = image_data.dimensions[1] * (44 / image_data.dimensions[0])
                    base_overlay = base_overlay.resize((44, int(new_height)))
                    base.paste(base_overlay, (0, int(22 - (new_height / 2))), base_overlay)
                else:
                    # Height shrinked to 44
                    new_width = image_data.dimensions[0] * (44 / image_data.dimensions[1])
                    base_overlay = base_overlay.resize((int(new_width), 44))
                    base.paste(base_overlay, (int(22 - (new_width / 2)), 0), base_overlay)
                if door.item_setting == HelmDoorItem.req_pearl:
                    pearl_mask_im = Image.new("RGBA", (44, 44), (0, 0, 0, 255))
                    draw = ImageDraw.Draw(pearl_mask_im)
                    draw.ellipse((0, 0, 43, 43), fill=(0, 0, 0, 0), outline=(0, 0, 0, 0))
                    pix_pearl = base.load()
                    for y in range(44):
                        for x in range(44):
                            r, g, b, a = pearl_mask_im.getpixel((x, y))
                            if a > 128:
                                pix_pearl[x, y] = (0, 0, 0, 0)
                writeColorImageToROM(base, 25, door.item_image, 44, 44, True)
                writeColorImageToROM(numberToImage(door.count, (44, 44)).transpose(Image.FLIP_TOP_BOTTOM), 25, door.number_image, 44, 44, True)


def applyHolidayMode(spoiler: Spoiler):
    """Change grass texture to snow."""
    enable_holiday_override = False
    if spoiler.settings.holiday_mode and enable_holiday_override:
        ROM().seek(0x1FF8000)
        snow_im = Image.new(mode="RGBA", size=((32, 32)))
        snow_px = snow_im.load()
        snow_by = []
        for y in range(32):
            for x in range(32):
                rgba_px = int.from_bytes(ROM().readBytes(2), "big")
                red = ((rgba_px >> 11) & 31) << 3
                green = ((rgba_px >> 6) & 31) << 3
                blue = ((rgba_px >> 1) & 31) << 3
                alpha = (rgba_px & 1) * 255
                snow_px[x, y] = (red, green, blue, alpha)
        for dim in (32, 16, 8, 4):
            snow_im = snow_im.resize((dim, dim))
            px = snow_im.load()
            for y in range(dim):
                for x in range(dim):
                    rgba_data = list(px[x, y])
                    data = 0
                    for c in range(3):
                        data |= (rgba_data[c] >> 3) << (1 + (5 * c))
                    if rgba_data[3] != 0:
                        data |= 1
                    snow_by.extend([(data >> 8), (data & 0xFF)])
        byte_data = gzip.compress(bytearray(snow_by), compresslevel=9)
        for img in (0x4DD, 0x4E4, 0x6B, 0xF0, 0x8B2, 0x5C2, 0x66E, 0x66F, 0x685, 0x6A1, 0xF8, 0x136):
            start = js.pointer_addresses[25]["entries"][img]["pointing_to"]
            ROM().seek(start)
            ROM().writeBytes(byte_data)


boot_phrases = (
    "Removing Lanky Kong",
    "Telling 2dos to play DK64",
    "Locking K. Lumsy in a cage",
    "Stealing the Banana Hoard",
    "Finishing the game in a cave",
    "Becoming the peak of randomizers",
    "Giving kops better eyesight",
    "Patching in the glitches",
    "Enhancing Cfox Luck",
    "Finding Rareware GB in Galleon",
    "Resurrecting Chunky Kong",
    "Shouting out Grant Kirkhope",
    "Crediting L. Godfrey",
    "Removing Stop n Swop",
    "Assembling the scraps",
    "Blowing in the cartridge",
    "Backflipping in Chunky Phase",
    "Hiding 20 fairies",
    "Randomizing collision normals",
    "Removing hit detection",
    "Compressing K Rools Voice Lines",
    "Checking divide by 0 doesnt work",
    "Adding every move to Isles",
    "Segueing in dk64randomizer.com",
    "Removing lag. Or am I?",
    "Hiding a dirt patch under grass",
    "Giving Wrinkly the spoiler log",
    "Questioning sub 2:30 in LUA Rando",
    "Chasing Lanky in Fungi Forest",
    "Banning Potions from Candys Shop",
    "Finding someone who can help you",
    "Messing up your seed",
    "Crashing Krem Isle",
    "Increasing Robot Punch Resistance",
    "Caffeinating banana fairies",
    "Bothering Beavers",
    "Inflating Banana Balloons",
    "Counting to 16",
    "Removing Walls",
    "Taking it to the fridge",
    "Brewing potions",
    "Reticulating Splines",  # SimCity 2000
    "Ironing Donks",
    "Replacing mentions of Hero with Hoard",
    "Suggesting you also try BK Randomizer",
    "Scattering 3500 Bananas",
    "Stealing ideas from other randomizers",
    "Fixing Krushas Collision",
    "Falling on 75m",
    "Summoning Salt",
    "Combing Chunkys Afro",
    "Asking what you gonna do",
    "Thinking with portals",
    "Reminding you to hydrate",
    "Injecting lag",
    "Turning Sentient",
    "Performing for you",
    "Charging 2 coins per save",
    "Loading in Beavers",
    "Lifting Boulders with Relative Ease",
    "Doing Monkey Science Probably",
    "Telling Killklli to eventually play DK64",
)


def writeBootMessages(spoiler: Spoiler):
    """Write boot messages into ROM."""
    placed_messages = random.sample(boot_phrases, 4)
    print(placed_messages)
    for message_index, message in enumerate(placed_messages):
        ROM().seek(0x1FFD000 + (0x40 * message_index))
        ROM().writeBytes(message.upper().encode("ascii"))
