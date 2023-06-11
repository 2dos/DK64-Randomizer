"""Apply cosmetic skins to kongs."""
import gzip
import random
import zlib
from random import randint

from PIL import Image, ImageDraw, ImageEnhance

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, ColorblindMode, HelmDoorItem, KlaptrapModel
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Lib import TextureFormat, float_to_hex, getObjectAddressBrowser, int_to_list, intf_to_float
from randomizer.Patching.Patcher import ROM, LocalROM


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

    def __init__(self, setting: HelmDoorItem, image_indexes: list, flip=False, table=25, dimensions=(44, 44), format=TextureFormat.RGBA5551):
        """Initialize with given parameters."""
        self.setting = setting
        self.image_indexes = image_indexes
        self.flip = flip
        self.table = table
        self.dimensions = dimensions
        self.format = format


def apply_cosmetic_colors(settings):
    """Apply cosmetic skins to kongs."""
    model_index = 0
    sav = settings.rom_data
    if js.document.getElementById("override_cosmetics").checked or True:
        model_setting = KlaptrapModel[js.document.getElementById("klaptrap_model").value]
    else:
        model_setting = settings.klaptrap_model
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
    settings.klaptrap_model_index = model_index
    if settings.misc_cosmetics:
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

    if js.document.getElementById("override_cosmetics").checked or True:
        if js.document.getElementById("random_colors").checked:
            settings.dk_colors = CharacterColors.randomized
            settings.diddy_colors = CharacterColors.randomized
            settings.lanky_colors = CharacterColors.randomized
            settings.tiny_colors = CharacterColors.randomized
            settings.chunky_colors = CharacterColors.randomized
            settings.rambi_colors = CharacterColors.randomized
            settings.enguarde_colors = CharacterColors.randomized
        else:
            settings.dk_colors = CharacterColors[js.document.getElementById("dk_colors").value]
            settings.dk_custom_color = js.document.getElementById("dk_custom_color").value
            settings.diddy_colors = CharacterColors[js.document.getElementById("diddy_colors").value]
            settings.diddy_custom_color = js.document.getElementById("diddy_custom_color").value
            settings.lanky_colors = CharacterColors[js.document.getElementById("lanky_colors").value]
            settings.lanky_custom_color = js.document.getElementById("lanky_custom_color").value
            settings.tiny_colors = CharacterColors[js.document.getElementById("tiny_colors").value]
            settings.tiny_custom_color = js.document.getElementById("tiny_custom_color").value
            settings.chunky_colors = CharacterColors[js.document.getElementById("chunky_colors").value]
            settings.chunky_custom_color = js.document.getElementById("chunky_custom_color").value
            settings.rambi_colors = CharacterColors[js.document.getElementById("rambi_colors").value]
            settings.rambi_custom_color = js.document.getElementById("rambi_custom_color").value
            settings.enguarde_colors = CharacterColors[js.document.getElementById("enguarde_colors").value]
            settings.enguarde_custom_color = js.document.getElementById("enguarde_custom_color").value
    else:
        if settings.random_colors:
            settings.dk_colors = CharacterColors.randomized
            settings.diddy_colors = CharacterColors.randomized
            settings.lanky_colors = CharacterColors.randomized
            settings.tiny_colors = CharacterColors.randomized
            settings.chunky_colors = CharacterColors.randomized
            settings.rambi_colors = CharacterColors.randomized
            settings.enguarde_colors = CharacterColors.randomized

    colors_dict = {
        "dk_colors": settings.dk_colors,
        "dk_custom_color": settings.dk_custom_color,
        "diddy_colors": settings.diddy_colors,
        "diddy_custom_color": settings.diddy_custom_color,
        "lanky_colors": settings.lanky_colors,
        "lanky_custom_color": settings.lanky_custom_color,
        "tiny_colors": settings.tiny_colors,
        "tiny_custom_color": settings.tiny_custom_color,
        "chunky_colors": settings.chunky_colors,
        "chunky_custom_color": settings.chunky_custom_color,
        "rambi_colors": settings.rambi_colors,
        "rambi_custom_color": settings.rambi_custom_color,
        "enguarde_colors": settings.enguarde_colors,
        "enguarde_custom_color": settings.enguarde_custom_color,
    }
    for kong in kong_settings:
        process = True
        if kong["kong_index"] == 4:  # Chunky
            is_disco = settings.disco_chunky
            if settings.krusha_kong == Kongs.chunky:
                is_disco = False
            if is_disco and kong["kong"] == "chunky":
                process = False
            elif not is_disco and kong["kong"] == "disco_chunky":
                process = False
        is_krusha = False
        if settings.krusha_kong is not None:
            if settings.krusha_kong == kong["kong_index"]:
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
                    mode = settings.colorblind_mode
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
                        if settings.disco_chunky:
                            base_obj["zones"][1]["colors"][0] = opp_color
                        else:
                            base_obj["zones"][0]["colors"][1] = opp_color
                color_palettes.append(base_obj)
                color_obj[f"{kong['kong']}"] = color
            elif is_krusha:
                del base_obj["zones"][0]
                color_palettes.append(base_obj)
    settings.colors = color_obj
    if len(color_palettes) > 0:
        convertColors(color_palettes)


color_bases = []
balloon_single_frames = [(4, 38), (5, 38), (5, 38), (5, 38), (5, 38), (5, 38), (4, 38), (4, 38)]


def getFile(table_index: int, file_index: int, compressed: bool, width: int, height: int, format: str):
    """Grab image from file."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    try:
        LocalROM().seek(file_start)
        data = LocalROM().readBytes(file_size)
    except Exception:
        ROM().seek(file_start)
        data = ROM().readBytes(file_size)
    if compressed:
        data = zlib.decompress(data, (15 + 32))
    im_f = Image.new(mode="RGBA", size=(width, height))
    pix = im_f.load()
    for y in range(height):
        for x in range(width):
            if format == TextureFormat.RGBA32:
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


def maskImageWithColor(im_f: Image, mask: tuple):
    """Apply rgb mask to image using a rgb color tuple."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.copy()
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def maskImage(im_f, base_index, min_y, keep_dark=False):
    """Apply RGB mask to image."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if keep_dark is False:
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


def maskMushroomImage(im_f, reference_image, color, side_2=False):
    """Apply RGB mask to mushroom image."""
    w, h = im_f.size
    pixels_to_mask = []
    pix_ref = reference_image.load()
    for x in range(w):
        for y in range(h):
            base_ref = list(pix_ref[x, y])
            # Filter out the white dots that won't get filtered out correctly with the below conditions
            if not (max(abs(base_ref[0] - base_ref[2]), abs(base_ref[1] - base_ref[2])) < 41 and abs(base_ref[0] - base_ref[1]) < 11):
                # Filter out that one lone pixel that is technically blue AND gets through the above filter, but should REALLY not be blue
                if not (side_2 is True and x == 51 and y == 21):
                    # Select the exact pixels to mask, which is all the "blue" pixels, filtering out the white spots
                    if base_ref[2] > base_ref[0] and base_ref[2] > base_ref[1] and int(base_ref[0] + base_ref[1]) < 200:
                        pixels_to_mask.append([x, y])
                    # Select the darker blue pixels as well
                    elif base_ref[2] > int(base_ref[0] + base_ref[1]):
                        pixels_to_mask.append([x, y])
    pix = im_f.load()
    mask = getRGBFromHash(color)
    for channel in range(3):
        mask[channel] = max(1, mask[channel])  # Absolute black is bad
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0 and [x, y] in pixels_to_mask:
                average_light = int((base[0] + base[1] + base[2]) / 3)
                for channel in range(3):
                    base[channel] = int(mask[channel] * (average_light / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorRotatingRoomTiles():
    """Determine how to recolor the tiles rom the memory game in Donkey's Rotating Room in Caves."""
    question_mark_tiles = [900, 901, 892, 893, 896, 897, 890, 891, 898, 899, 894, 895]
    face_tiles = [874, 878, 875, 879, 876, 886, 877, 885, 880, 887, 881, 888, 870, 872, 871, 873, 866, 882, 867, 883, 868, 889, 869, 884]
    question_mark_tile_masks = [508, 509]
    face_tile_masks = [636, 635, 633, 634, 631, 632, 630, 629, 627, 628, 5478, 5478]
    question_mark_resize = [17, 37]
    face_resize = [[32, 64], [32, 64], [32, 64], [32, 64], [32, 64], [71, 66]]
    question_mark_offsets = [[16, 14], [0, 14]]
    face_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [-5, -1], [-38, -1]]

    for tile in range(len(question_mark_tiles)):
        tile_image = getFile(7, question_mark_tiles[tile], False, 32, 64, TextureFormat.RGBA5551)
        mask = getFile(7, question_mark_tile_masks[(tile % 2)], False, 32, 64, TextureFormat.RGBA5551)
        resize = question_mark_resize
        mask = mask.resize((resize[0], resize[1]))
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, question_mark_offsets[(tile % 2)], int(tile / 2), (tile % 2))
        writeColorImageToROM(masked_tile, 7, question_mark_tiles[tile], 32, 64, False, TextureFormat.RGBA5551)
    for tile in range(len(face_tiles)):
        face_index = int(tile / 4)
        if face_index < 5:
            width = 32
            height = 64
        else:
            width = 44
            height = 44
        mask = getFile(25, face_tile_masks[int(tile / 2)], True, width, height, TextureFormat.RGBA5551)
        resize = face_resize[face_index]
        mask = mask.resize((resize[0], resize[1]))
        tile_image = getFile(7, face_tiles[tile], False, 32, 64, TextureFormat.RGBA5551)
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, face_offsets[int(tile / 2)], face_index, (int(tile / 2) % 2))
        writeColorImageToROM(masked_tile, 7, face_tiles[tile], 32, 64, False, TextureFormat.RGBA5551)


def maskImageRotatingRoomTile(im_f, im_mask, paste_coords, image_color_index, tile_side):
    """Apply RGB mask to image of a Rotating Room Memory Tile."""
    w, h = im_f.size
    im_original = im_f
    pix_original = im_original.load()
    pixels_original = []
    for x in range(w):
        pixels_original.append([])
        for y in range(h):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    brightener = ImageEnhance.Brightness(im_f)
    im_f = brightener.enhance(2)
    pix = im_f.load()
    pix_mask = im_mask.load()
    w2, h2 = im_mask.size
    mask_coords = []
    for x in range(w2):
        for y in range(h2):
            coord = list(pix_mask[x, y])
            if coord[3] > 0:
                mask_coords.append([(x + paste_coords[0]), (y + paste_coords[1])])
    if image_color_index < 5:
        mask = getRGBFromHash(color_bases[image_color_index])
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too dark looks bad
    else:
        mask = getRGBFromHash(color_bases[2])
    mask2 = getRGBFromHash("#000000")
    if image_color_index == 0:
        mask2 = getRGBFromHash("#FFFFFF")
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base_original = list(pixels_original[x][y])
            if [x, y] not in mask_coords:
                if image_color_index in [1, 2, 4]:  # Diddy, Lanky and Chunky don't get any special features
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                elif image_color_index in [0, 3]:  # Donkey and Tiny get a diamond-shape frame
                    side = w
                    if tile_side == 1:
                        side = 0
                    if abs(abs(side - x) - y) < 2 or abs(abs(side - x) - abs(h - y)) < 2:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                else:  # Golden Banana gets a block-pattern
                    if (int(x / 8) + int(y / 8)) % 2 == 0:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
            else:
                for channel in range(3):
                    base[channel] = base_original[channel]
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


def maskImageWithOutline(im_f, base_index, min_y, colorblind_mode, type=""):
    """Apply RGB mask to image with an Outline in a different color."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if type != "bunch" or base_index == 4:
        brightener = ImageEnhance.Brightness(im_dupe)
        im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getRGBFromHash(color_bases[base_index])
    if base_index == 2 or (base_index == 0 and colorblind_mode == ColorblindMode.trit):  # lanky or (DK in tritanopia mode)
        border_color = color_bases[4]
    else:
        border_color = color_bases[1]
    mask2 = getRGBFromHash(border_color)
    contrast = False
    if base_index == 0:
        contrast = True
    for channel in range(3):
        mask[channel] = max(39, mask[channel])  # Too black is bad for these items
        if base_index == 0 and type == "single":  # Donkey's single
            mask[channel] += 20
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                    if contrast is True:
                        if base[channel] > 30:
                            base[channel] = int(base[channel] / 2)
                        else:
                            base[channel] = int(base[channel] / 4)
                pix[x, y] = (base[0], base[1], base[2], base[3])
    for t in range(3):
        for x in range(w):
            for y in range(min_y, h):
                base = list(pix[x, y])
                if base[3] > 0:
                    if (
                        (x + t < w and list(pix[x + t, y])[3] == 0)
                        or (y + t < h and list(pix[x, y + t])[3] == 0)
                        or (x - t > -1 and list(pix[x - t, y])[3] == 0)
                        or (y - t > min_y - 1 and list(pix[x, y - t])[3] == 0)
                    ):
                        pix[x, y] = (mask2[0], mask2[1], mask2[2], base[3])
    return im_f


def writeColorImageToROM(im_f, table_index, file_index, width, height, transparent_border: bool, format: str):
    """Write texture to ROM."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    try:
        LocalROM().seek(file_start)
    except Exception:
        ROM().seek(file_start)
    pix = im_f.load()
    width, height = im_f.size
    bytes_array = []
    border = 1
    right_border = 3
    for y in range(height):
        for x in range(width):
            if transparent_border and ((x < border) or (y < border) or (x >= (width - border)) or (y >= (height - border))) or (x == (width - right_border)):
                pix_data = [0, 0, 0, 0]
            else:
                pix_data = list(pix[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            else:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    data = bytearray(bytes_array)
    bytes_per_px = 2
    if format == TextureFormat.RGBA32:
        bytes_per_px = 4
    if len(data) > (bytes_per_px * width * height):
        print(f"Image too big error: {table_index} > {file_index}")
    if table_index in (14, 25):
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    try:
        LocalROM().writeBytes(data)
    except Exception:
        ROM().writeBytes(data)


def writeKasplatHairColorToROM(color, table_index, file_index, format: str):
    """Write color to ROM for kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color)
    if format == TextureFormat.RGBA32:
        color_lst = mask.copy()
        color_lst.append(255)  # Alpha
        null_color = [0] * 4
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        color_lst = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            bytes_array.extend(color_lst)
    for i in range(18):
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeWhiteKasplatHairColorToROM(color1, color2, table_index, file_index, format: str):
    """Write color to ROM for white kasplats, giving them a black-white block pattern."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color1)
    mask2 = getRGBFromHash(color2)
    if format == TextureFormat.RGBA32:
        color_lst_0 = mask.copy()
        color_lst_0.append(255)
        color_lst_1 = mask2.copy()
        color_lst_1.append(255)
        null_color = [0] * 4
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        val_r2 = int((mask2[0] >> 3) << 11)
        val_g2 = int((mask2[1] >> 3) << 6)
        val_b2 = int((mask2[2] >> 3) << 1)
        rgba_val2 = val_r2 | val_g2 | val_b2 | 1
        color_lst_0 = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
        color_lst_1 = [(rgba_val2 >> 8) & 0xFF, rgba_val2 & 0xFF]
        null_color = [0] * 2
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if (int(y / 7) + int(x / 8)) % 2 == 0:
                bytes_array.extend(color_lst_0)
            else:
                bytes_array.extend(color_lst_1)
    for i in range(18):
        bytes_array.extend(color_lst_0)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst_0)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeKlaptrapSkinColorToROM(color_index, table_index, file_index, format: str):
    """Write color to ROM for klaptraps."""
    im_f = getFile(table_index, file_index, True, 32, 43, format)
    im_f = maskImage(im_f, color_index, 0, (color_index != 3))
    pix = im_f.load()
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeSpecialKlaptrapTextureToROM(color_index, table_index, file_index, format: str, pixels_to_ignore: list):
    """Write color to ROM for klaptraps special texture(s)."""
    im_f = getFile(table_index, file_index, True, 32, 43, format)
    pix_original = im_f.load()
    pixels_original = []
    for x in range(32):
        pixels_original.append([])
        for y in range(43):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    im_f_masked = maskImage(im_f, color_index, 0, (color_index != 3))
    pix = im_f_masked.load()
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if [x, y] not in pixels_to_ignore:
                color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            else:
                color_lst = calculateKlaptrapPixel(list(pixels_original[x][y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        if [i, 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[i][42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        if [(22 + i), 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[(22 + i)][42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def calculateKlaptrapPixel(mask: list, format: str):
    """Calculate the new color for the given pixel."""
    if format == TextureFormat.RGBA32:
        color_lst = mask.copy()
        color_lst.append(255)  # Alpha
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        color_lst = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
    return color_lst


def maskBlueprintImage(im_f, base_index):
    """Apply RGB mask to blueprint image."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getRGBFromHash(color_bases[base_index])
    if max(mask[0], max(mask[1], mask[2])) < 39:
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too black is bad for these items
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the wooden frame
                # brown is orange, is red and (red+green), is very little blue
                # but, if the color is light, we can't rely on the blue value alone.
                if base2[2] > 20 and (base2[2] > base2[1] or base2[1] - base2[2] < 20):
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskLaserImage(im_f, base_index):
    """Apply RGB mask to laser texture."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getRGBFromHash(color_bases[base_index])
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the white center of the laser
                if min(base2[0], min(base2[1], base2[2])) <= 210:
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskPotionImage(im_f, primary_color, secondary_color=None):
    """Apply RGB mask to DK arcade potion reward preview texture."""
    w, h = im_f.size
    pix = im_f.load()
    mask = getRGBFromHash(primary_color)
    if secondary_color is not None:
        mask2 = secondary_color
    for channel in range(3):
        mask[channel] = max(1, mask[channel])
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            # Filter out transparent pixels and the cork
            if base[3] > 0 and y > 2 and [x, y] not in [[9, 4], [10, 4]]:
                # Filter out the bottle's contents
                if base[0] == base[1] and base[1] == base[2]:
                    if secondary_color is not None:
                        # Color the bottle itself
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                else:
                    # Color the bottle's contents
                    average_light = int((base[0] + base[1] + base[2]) / 3)
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (average_light / 255))
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorWrinklyDoors():
    """Recolor the Wrinkly hint door doorframes for colorblind mode."""
    file = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
    for kong in range(5):
        wrinkly_door_start = js.pointer_addresses[4]["entries"][file[kong]]["pointing_to"]
        wrinkly_door_finish = js.pointer_addresses[4]["entries"][file[kong] + 1]["pointing_to"]
        wrinkly_door_size = wrinkly_door_finish - wrinkly_door_start
        ROM().seek(wrinkly_door_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(wrinkly_door_start)
        data = ROM().readBytes(wrinkly_door_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them (list extensions to mitigate the linter's "artistic freedom" putting 1 value per line)
        color1_offsets = [1548, 1580, 1612, 1644, 1676, 1708, 1756, 1788, 1804, 1820, 1836, 1852, 1868, 1884, 1900, 1916]
        color1_offsets = color1_offsets + [1932, 1948, 1964, 1980, 1996, 2012, 2028, 2044, 2076, 2108, 2124, 2156, 2188, 2220, 2252, 2284]
        color1_offsets = color1_offsets + [2316, 2348, 2380, 2396, 2412, 2428, 2444, 2476, 2508, 2540, 2572, 2604, 2636, 2652, 2668, 2684]
        color1_offsets = color1_offsets + [2700, 2716, 2732, 2748, 2764, 2780, 2796, 2812, 2828, 2860, 2892, 2924, 2956, 2988, 3020, 3052]
        color2_offsets = [1564, 1596, 1628, 1660, 1692, 1724, 1740, 1772, 2332, 2364, 2460, 2492, 2524, 2556, 2588, 2620]
        new_color1 = getRGBFromHash(color_bases[kong])
        new_color2 = getRGBFromHash(color_bases[kong])
        if kong == 0:
            for channel in range(3):
                new_color2[channel] = max(80, new_color1[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the doorframe
        for offset in color1_offsets:
            for i in range(3):
                num_data[offset + i] = new_color1[i]
        for offset in color2_offsets:
            for i in range(3):
                num_data[offset + i] = new_color2[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(wrinkly_door_start)
        ROM().writeBytes(data)


def recolorSlamSwitches():
    """Recolor the Simian Slam switches for colorblind mode."""
    file = [0x94, 0x93, 0x95, 0x96, 0xB8, 0x16C, 0x16B, 0x16D, 0x16E, 0x16A, 0x167, 0x166, 0x168, 0x169, 0x165]
    for switch in range(15):
        slam_switch_start = js.pointer_addresses[4]["entries"][file[switch]]["pointing_to"]
        slam_switch_finish = js.pointer_addresses[4]["entries"][file[switch] + 1]["pointing_to"]
        slam_switch_size = slam_switch_finish - slam_switch_start
        ROM().seek(slam_switch_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(slam_switch_start)
        data = ROM().readBytes(slam_switch_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color_offsets = [1828, 1844, 1860, 1876, 1892, 1908]
        new_color1 = getRGBFromHash(color_bases[4])  # chunky's color
        new_color2 = getRGBFromHash(color_bases[2])  # lanky's color
        new_color3 = getRGBFromHash(color_bases[1])  # diddy's color

        # Green switches
        if switch < 5:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color1[i]
        # Blue switches
        elif switch < 10:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color2[i]
        # Red switches
        else:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color3[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(slam_switch_start)
        ROM().writeBytes(data)


def recolorBlueprintModelTwo():
    """Recolor the Blueprint Model2 items for colorblind mode."""
    file = [0xDE, 0xE0, 0xE1, 0xDD, 0xDF]
    for kong in range(5):
        blueprint_model2_start = js.pointer_addresses[4]["entries"][file[kong]]["pointing_to"]
        blueprint_model2_finish = js.pointer_addresses[4]["entries"][file[kong] + 1]["pointing_to"]
        blueprint_model2_size = blueprint_model2_finish - blueprint_model2_start
        ROM().seek(blueprint_model2_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(blueprint_model2_start)
        data = ROM().readBytes(blueprint_model2_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x52C, 0x54C, 0x57C, 0x58C, 0x5AC, 0x5CC, 0x5FC, 0x61C]
        color2_offsets = [0x53C, 0x55C, 0x5EC, 0x60C]
        color3_offsets = [0x56C, 0x59C, 0x5BC, 0x5DC]
        new_color = getRGBFromHash(color_bases[kong])
        if kong == 0:
            for channel in range(3):
                new_color[channel] = max(39, new_color[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the model2 item
        for offset in color1_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color2_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color3_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(blueprint_model2_start)
        ROM().writeBytes(data)


def recolorBells():
    """Recolor the Chunky Minecart bells for colorblind mode (prot/deut)."""
    file = 693
    minecart_bell_start = js.pointer_addresses[4]["entries"][file]["pointing_to"]
    minecart_bell_finish = js.pointer_addresses[4]["entries"][file + 1]["pointing_to"]
    minecart_bell_size = minecart_bell_finish - minecart_bell_start
    ROM().seek(minecart_bell_start)
    indicator = int.from_bytes(ROM().readBytes(2), "big")
    ROM().seek(minecart_bell_start)
    data = ROM().readBytes(minecart_bell_size)
    if indicator == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    num_data = []  # data, but represented as nums rather than b strings
    for d in data:
        num_data.append(d)
    # Figure out which colors to use and where to put them
    color1_offsets = [0x214, 0x244, 0x264, 0x274, 0x284]
    color2_offsets = [0x224, 0x234, 0x254]
    new_color1 = getRGBFromHash("#0066FF")
    new_color2 = getRGBFromHash("#0000FF")

    # Recolor the bell
    for offset in color1_offsets:
        for i in range(3):
            num_data[offset + i] = new_color1[i]
    for offset in color2_offsets:
        for i in range(3):
            num_data[offset + i] = new_color2[i]

    data = bytearray(num_data)  # convert num_data back to binary string
    if indicator == 0x1F8B:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(minecart_bell_start)
    ROM().writeBytes(data)


def recolorKlaptraps():
    """Recolor the klaptrap models for colorblind mode."""
    green_files = [0xF31, 0xF32, 0xF33, 0xF35, 0xF37, 0xF39]  # 0xF2F collar? 0xF30 feet?
    red_files = [0xF44, 0xF45, 0xF46, 0xF47, 0xF48, 0xF49]  # , 0xF42 collar? 0xF43 feet?
    purple_files = [0xF3C, 0xF3D, 0xF3E, 0xF3F, 0xF40, 0xF41]  # 0xF3B feet?, 0xF3A collar?

    # Regular textures
    for file in range(6):
        writeKlaptrapSkinColorToROM(4, 25, green_files[file], TextureFormat.RGBA5551)
        writeKlaptrapSkinColorToROM(1, 25, red_files[file], TextureFormat.RGBA5551)
        writeKlaptrapSkinColorToROM(3, 25, purple_files[file], TextureFormat.RGBA5551)

    belly_pixels_to_ignore = []
    for x in range(32):
        for y in range(43):
            if y < 29 or (y > 31 and y < 39) or y == 40 or y == 42:
                belly_pixels_to_ignore.append([x, y])
            elif (y == 39 and x < 16) or (y == 41 and x < 24):
                belly_pixels_to_ignore.append([x, y])

    # Special texture that requires only partial recoloring, in this case file 0xF38 which is the belly, and only the few green pixels
    writeSpecialKlaptrapTextureToROM(4, 25, 0xF38, TextureFormat.RGBA5551, belly_pixels_to_ignore)


def recolorPotions(colorblind_mode):
    """Overwrite potion colors."""
    secondary_color = [color_bases[1], None, color_bases[4], color_bases[1], None, None]
    if colorblind_mode == ColorblindMode.trit:
        secondary_color[0] = color_bases[4]
        secondary_color[2] = None
    for color in range(len(secondary_color)):
        if secondary_color[color] is not None:
            secondary_color[color] = getRGBFromHash(secondary_color[color])

    # Actor:
    file = [[0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF2], [0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA]]
    for type in range(2):
        for potion_color in range(6):
            potion_actor_start = js.pointer_addresses[5]["entries"][file[type][potion_color]]["pointing_to"]
            potion_actor_finish = js.pointer_addresses[5]["entries"][file[type][potion_color] + 1]["pointing_to"]
            potion_actor_size = potion_actor_finish - potion_actor_start
            ROM().seek(potion_actor_start)
            indicator = int.from_bytes(ROM().readBytes(2), "big")
            ROM().seek(potion_actor_start)
            data = ROM().readBytes(potion_actor_size)
            if indicator == 0x1F8B:
                data = zlib.decompress(data, (15 + 32))
            num_data = []  # data, but represented as nums rather than b strings
            for d in data:
                num_data.append(d)
            # Figure out which colors to use and where to put them
            color1_offsets = [0x34]
            color2_offsets = [0x44, 0x54, 0xA4]
            color3_offsets = [0x64, 0x74, 0x84, 0xE4]
            color4_offsets = [0x94]
            color5_offsets = [0xB4, 0xC4, 0xD4]
            # color6_offsets = [0xF4, 0x104, 0x114, 0x124, 0x134, 0x144, 0x154, 0x164]
            if potion_color < 5:
                new_color = getRGBFromHash(color_bases[potion_color])
            else:
                new_color = getRGBFromHash("#FFFFFF")

            # Recolor the actor item
            for offset in color1_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    if secondary_color[potion_color] is not None and potion_color == 3:  # tiny
                        num_data[offset + i] = int(num_data[offset + i] * (secondary_color[potion_color][i] / 255))
                    elif secondary_color[potion_color] is not None:  # donkey gets an even darker shade
                        num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 8) / 255))
                    elif secondary_color[potion_color] is not None:  # other kongs with a secondary color get a darker shade
                        num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 4) / 255))
                    else:
                        num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color2_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color3_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color4_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color5_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

            data = bytearray(num_data)  # convert num_data back to binary string
            if indicator == 0x1F8B:
                data = gzip.compress(data, compresslevel=9)
            ROM().seek(potion_actor_start)
            ROM().writeBytes(data)

    # Model2:
    file = [91, 498, 89, 499, 501, 502]
    for potion_color in range(6):
        potion_model2_start = js.pointer_addresses[4]["entries"][file[potion_color]]["pointing_to"]
        potion_model2_finish = js.pointer_addresses[4]["entries"][file[potion_color] + 1]["pointing_to"]
        potion_model2_size = potion_model2_finish - potion_model2_start
        ROM().seek(potion_model2_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(potion_model2_start)
        data = ROM().readBytes(potion_model2_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x144]
        color2_offsets = [0x154, 0x164, 0x1B4]
        color3_offsets = [0x174, 0x184, 0x194, 0x1F4]
        color4_offsets = [0x1A4]
        color5_offsets = [0x1C4, 0x1D4, 0x1E4]
        # color6_offsets = [0x204, 0x214, 0x224, 0x234, 0x244, 0x254, 0x264, 0x274]
        if potion_color < 5:
            new_color = getRGBFromHash(color_bases[potion_color])
        else:
            new_color = getRGBFromHash("#FFFFFF")

        # Recolor the model2 item
        for offset in color1_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                if secondary_color[potion_color] is not None and potion_color == 3:  # tiny
                    num_data[offset + i] = int(num_data[offset + i] * (secondary_color[potion_color][i] / 255))
                elif secondary_color[potion_color] is not None:  # donkey gets an even darker shade
                    num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 8) / 255))
                elif secondary_color[potion_color] is not None:  # other kongs with a secondary color get a darker shade
                    num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 4) / 255))
                else:
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color2_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color3_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color4_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color5_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(potion_model2_start)
        ROM().writeBytes(data)

    # DK Arcade sprites
    for file in range(8, 14):
        index = file - 8
        if index < 5:
            color = color_bases[index]
        else:
            color = "#FFFFFF"
        potion_image = getFile(6, file, False, 20, 20, TextureFormat.RGBA5551)
        potion_image = maskPotionImage(potion_image, color, secondary_color[index])
        writeColorImageToROM(potion_image, 6, file, 20, 20, False, TextureFormat.RGBA5551)


def recolorMushrooms():
    """Recolor the various colored mushrooms in the game for colorblind mode."""
    reference_mushroom_image = getFile(7, 297, False, 32, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side1 = getFile(25, 0xD64, True, 64, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side2 = getFile(25, 0xD65, True, 64, 32, TextureFormat.RGBA5551)
    files_table_7 = [296, 295, 297, 299, 298]
    files_table_25_side_1 = [0xD60, 0x67F, 0xD64, 0xD62, 0xD66]
    files_table_25_side_2 = [0xD61, 0x680, 0xD65, 0xD63, 0xD67]
    for file in range(5):
        # Mushroom on the ceiling inside Fungi Forest Lobby
        mushroom_image = getFile(7, files_table_7[file], False, 32, 32, TextureFormat.RGBA5551)
        mushroom_image = maskMushroomImage(mushroom_image, reference_mushroom_image, color_bases[file])
        writeColorImageToROM(mushroom_image, 7, files_table_7[file], 32, 32, False, TextureFormat.RGBA5551)
        # Mushrooms in Lanky's colored mushroom puzzle (and possibly also the bouncy mushrooms)
        mushroom_image_side_1 = getFile(25, files_table_25_side_1[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_1 = maskMushroomImage(mushroom_image_side_1, reference_mushroom_image_side1, color_bases[file])
        writeColorImageToROM(mushroom_image_side_1, 25, files_table_25_side_1[file], 64, 32, False, TextureFormat.RGBA5551)
        mushroom_image_side_2 = getFile(25, files_table_25_side_2[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_2 = maskMushroomImage(mushroom_image_side_2, reference_mushroom_image_side2, color_bases[file], True)
        writeColorImageToROM(mushroom_image_side_2, 25, files_table_25_side_2[file], 64, 32, False, TextureFormat.RGBA5551)


BALLOON_START = [5835, 5827, 5843, 5851, 5819]


def overwrite_object_colors(settings):
    """Overwrite object colors."""
    global color_bases
    mode = settings.colorblind_mode
    if mode != ColorblindMode.off:
        if mode == ColorblindMode.prot:
            color_bases = ["#000000", "#0072FF", "#766D5A", "#FFFFFF", "#FDE400"]
        elif mode == ColorblindMode.deut:
            color_bases = ["#000000", "#318DFF", "#7F6D59", "#FFFFFF", "#E3A900"]
        elif mode == ColorblindMode.trit:
            color_bases = ["#000000", "#C72020", "#13C4D8", "#FFFFFF", "#FFA4A4"]
        if mode in (ColorblindMode.prot, ColorblindMode.deut):
            recolorBells()
        # Preload DK single cb image to paste onto balloons
        file = 175
        dk_single = getFile(7, file, False, 44, 44, TextureFormat.RGBA5551)
        dk_single = dk_single.resize((21, 21))
        blueprint_lanky = []
        # Preload blueprint images. Lanky's blueprint image is so much easier to mask, because it is blue, and the frame is brown
        for file in range(8):
            blueprint_lanky.append(getFile(25, 5519 + (file), True, 48, 42, TextureFormat.RGBA5551))
        writeWhiteKasplatHairColorToROM("#FFFFFF", "#000000", 25, 4125, TextureFormat.RGBA5551)
        recolorWrinklyDoors()
        recolorSlamSwitches()
        recolorRotatingRoomTiles()
        recolorBlueprintModelTwo()
        recolorKlaptraps()
        recolorPotions(mode)
        recolorMushrooms()
        for kong_index in range(5):
            # file = 4120
            # # Kasplat Hair
            # hair_im = getFile(25, file, True, 32, 44, TextureFormat.RGBA5551)
            # hair_im = maskImage(hair_im, kong_index, 0)
            # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False)
            writeKasplatHairColorToROM(color_bases[kong_index], 25, [4124, 4122, 4123, 4120, 4121][kong_index], TextureFormat.RGBA5551)
            for file in range(5519, 5527):
                # Blueprint sprite
                blueprint_start = [5624, 5608, 5519, 5632, 5616]
                blueprint_im = blueprint_lanky[(file - 5519)]
                blueprint_im = maskBlueprintImage(blueprint_im, kong_index)
                writeColorImageToROM(blueprint_im, 25, blueprint_start[kong_index] + (file - 5519), 48, 42, False, TextureFormat.RGBA5551)
            for file in range(4925, 4931):
                # Shockwave
                shockwave_start = [4897, 4903, 4712, 4950, 4925]
                shockwave_im = getFile(25, shockwave_start[kong_index] + (file - 4925), True, 32, 32, TextureFormat.RGBA32)
                shockwave_im = maskImage(shockwave_im, kong_index, 0)
                writeColorImageToROM(shockwave_im, 25, shockwave_start[kong_index] + (file - 4925), 32, 32, False, TextureFormat.RGBA32)
            for file in range(784, 796):
                # Helm Laser (will probably also affect the Pufftoss laser and the Game Over laser)
                laser_start = [784, 748, 363, 760, 772]
                laser_im = getFile(7, laser_start[kong_index] + (file - 784), False, 32, 32, TextureFormat.RGBA32)
                laser_im = maskLaserImage(laser_im, kong_index)
                writeColorImageToROM(laser_im, 7, laser_start[kong_index] + (file - 784), 32, 32, False, TextureFormat.RGBA32)
            if kong_index == 0 or kong_index == 3 or (kong_index == 2 and mode != ColorblindMode.trit):  # Lanky (prot, deut only) or DK or Tiny
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getFile(7, single_start[kong_index] + (file - 152), False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImageWithOutline(single_im, kong_index, 0, mode, "single")
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImageWithOutline(coin_im, kong_index, 0, mode)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, TextureFormat.RGBA5551)
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImageWithOutline(bunch_im, kong_index, 0, mode, "bunch")
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getFile(25, BALLOON_START[kong_index] + (file - 5819), True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImageWithOutline(balloon_im, kong_index, 33, mode)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + (file - 5819), 32, 64, False, TextureFormat.RGBA5551)
            else:
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getFile(7, single_start[kong_index] + (file - 152), False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImage(single_im, kong_index, 0)
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImage(coin_im, kong_index, 0)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, TextureFormat.RGBA5551)
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImage(bunch_im, kong_index, 0, True)
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getFile(25, BALLOON_START[kong_index] + (file - 5819), True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImage(balloon_im, kong_index, 33)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + (file - 5819), 32, 64, False, TextureFormat.RGBA5551)
    if settings.head_balloons:
        for kong in range(5):
            for offset in range(8):
                balloon_im = getFile(25, BALLOON_START[kong] + offset, True, 32, 64, TextureFormat.RGBA5551)
                kong_im = getFile(14, 190 + kong, True, 32, 32, TextureFormat.RGBA5551)
                kong_im = kong_im.transpose(Image.FLIP_TOP_BOTTOM).resize((20, 20))
                balloon_im.paste(kong_im, (5, 39), kong_im)
                writeColorImageToROM(balloon_im, 25, BALLOON_START[kong] + offset, 32, 64, False, TextureFormat.RGBA5551)


ORANGE_SCALING = 0.7


def applyKrushaKong(settings):
    """Apply Krusha Kong setting."""
    ROM().seek(settings.rom_data + 0x11C)
    if settings.krusha_kong is None:
        ROM().write(255)
    elif settings.krusha_kong < 5:
        ROM().write(settings.krusha_kong)
        placeKrushaHead(settings.krusha_kong)
        changeKrushaModel(settings.krusha_kong)
        if settings.krusha_kong == Kongs.donkey:
            fixBaboonBlasts()
        # Orange Switches
        switch_faces = [0xB25, 0xB1E, 0xC81, 0xC80, 0xB24]
        base_im = getFile(25, 0xC20, True, 32, 32, TextureFormat.RGBA5551)
        orange_im = getFile(7, 0x136, False, 32, 32, TextureFormat.RGBA5551)
        if settings.colorblind_mode == ColorblindMode.off:
            orange_im = maskImageWithColor(orange_im, (0, 150, 0))
        else:
            orange_im = maskImageWithColor(orange_im, (0, 255, 0))  # Brighter green makes this more distinguishable for colorblindness
        dim_length = int(32 * ORANGE_SCALING)
        dim_offset = int((32 - dim_length) / 2)
        orange_im = orange_im.resize((dim_length, dim_length))
        base_im.paste(orange_im, (dim_offset, dim_offset), orange_im)
        writeColorImageToROM(base_im, 25, switch_faces[settings.krusha_kong], 32, 32, False, TextureFormat.RGBA5551)


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
        item_start = getObjectAddressBrowser(0xBC, id, "actor")
        if item_start is not None:
            ROM().seek(item_start + 0x14)
            ROM().writeMultipleBytes(0xFFFFFFEC, 4)
            ROM().seek(item_start + 0x1B)
            ROM().writeMultipleBytes(0, 1)
    # Caves Baboon Blast
    item_start = getObjectAddressBrowser(0xBA, 4, "actor")
    if item_start is not None:
        ROM().seek(item_start + 0x4)
        ROM().writeMultipleBytes(int(float_to_hex(510), 16), 4)
    item_start = getObjectAddressBrowser(0xBA, 12, "actor")
    if item_start is not None:
        ROM().seek(item_start + 0x4)
        ROM().writeMultipleBytes(int(float_to_hex(333), 16), 4)
    # Castle Baboon Blast
    item_start = getObjectAddressBrowser(0xBB, 4, "actor")
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


def writeMiscCosmeticChanges(settings):
    """Write miscellaneous changes to the cosmetic colors."""
    if settings.misc_cosmetics:
        # Melon HUD
        data = {7: [0x13C, 0x147], 14: [0x5A, 0x5D], 25: [0x17B2, 0x17B2]}
        shift = random.randint(-359, 359)
        for table in data:
            table_data = data[table]
            for img in range(table_data[0], table_data[1] + 1):
                if table == 25 and img == 0x17B2:
                    dims = (32, 32)
                else:
                    dims = (48, 42)
                melon_im = getFile(table, img, table != 7, dims[0], dims[1], TextureFormat.RGBA5551)
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
        return getFile(14, 15, True, 76, 24, TextureFormat.RGBA5551).crop((num_0_bounds[x], 0, num_0_bounds[x + 1], 24))
    num_1_bounds = [0, 15, 28, 43, 58, 76]
    x = number - 5
    return getFile(14, 16, True, 76, 24, TextureFormat.RGBA5551).crop((num_1_bounds[x], 0, num_1_bounds[x + 1], 24))


def numberToImage(number: int, dim: tuple):
    """Convert multi-digit number to image."""
    digits = 1
    if number < 10:
        digits = 1
    elif number < 100:
        digits = 2
    else:
        digits = 3
    current = number
    nums = []
    total_width = 0
    max_height = 0
    sep_dist = 1
    for _ in range(digits):
        base = getNumberImage(current % 10)
        bbox = base.getbbox()
        base = base.crop(bbox)
        nums.append(base)
        base_w, base_h = base.size
        max_height = max(max_height, base_h)
        total_width += base_w
        current = int(current / 10)
    nums.reverse()
    total_width += (digits - 1) * sep_dist
    base = Image.new(mode="RGBA", size=(total_width, max_height))
    pos = 0
    for num in nums:
        base.paste(num, (pos, 0), num)
        num_w, num_h = num.size
        pos += num_w + sep_dist
    output = Image.new(mode="RGBA", size=dim)
    xScale = dim[0] / total_width
    yScale = dim[1] / max_height
    scale = xScale
    if yScale < xScale:
        scale = yScale
    new_w = int(total_width * scale)
    new_h = int(max_height * scale)
    x_offset = int((dim[0] - new_w) / 2)
    y_offset = int((dim[1] - new_h) / 2)
    new_dim = (new_w, new_h)
    base = base.resize(new_dim)
    output.paste(base, (x_offset, y_offset), base)
    return output


def applyHelmDoorCosmetics(settings):
    """Apply Helm Door Cosmetic Changes."""
    crown_door_required_item = settings.crown_door_item
    if crown_door_required_item == HelmDoorItem.vanilla and settings.crown_door_item_count != 4:
        crown_door_required_item = HelmDoorItem.req_crown
    coin_door_required_item = settings.coin_door_item
    if coin_door_required_item == HelmDoorItem.vanilla and settings.coin_door_item_count != 2:
        coin_door_required_item = HelmDoorItem.req_companycoins
    Doors = [
        HelmDoorSetting(crown_door_required_item, settings.crown_door_item_count, 6022, 6023),
        HelmDoorSetting(coin_door_required_item, settings.coin_door_item_count, 6024, 6025),
    ]
    Images = [
        HelmDoorImages(HelmDoorItem.req_gb, [0x155C]),
        HelmDoorImages(HelmDoorItem.req_bp, [x + 4 for x in (0x15F8, 0x15E8, 0x158F, 0x1600, 0x15F0)], False, 25, (48, 42)),
        HelmDoorImages(HelmDoorItem.req_bean, [0], True, 6, (20, 20)),
        HelmDoorImages(HelmDoorItem.req_pearl, [0xD5F], False, 25, (32, 32)),
        HelmDoorImages(HelmDoorItem.req_fairy, [0x16ED], False, 25, (32, 32), TextureFormat.RGBA32),
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
                writeColorImageToROM(base, 25, door.item_image, 44, 44, True, TextureFormat.RGBA5551)
                writeColorImageToROM(numberToImage(door.count, (44, 44)).transpose(Image.FLIP_TOP_BOTTOM), 25, door.number_image, 44, 44, True, TextureFormat.RGBA5551)


def applyHolidayMode(settings):
    """Change grass texture to snow."""
    if settings.holiday_setting:
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


def updateMillLeverTexture(settings):
    """Update the 21132 texture."""
    if settings.mill_levers[0] > 0:
        # Get Number bounds
        base_num_texture = getFile(table_index=25, file_index=0x7CA, compressed=True, width=64, height=32, format=TextureFormat.RGBA5551)
        number_textures = [None, None, None]
        number_x_bounds = (
            (18, 25),
            (5, 16),
            (36, 47),
        )
        modified_tex = getFile(table_index=25, file_index=0x7CA, compressed=True, width=64, height=32, format=TextureFormat.RGBA5551)
        for tex in range(3):
            number_textures[tex] = base_num_texture.crop((number_x_bounds[tex][0], 7, number_x_bounds[tex][1], 25))
        total_width = 0
        for x in range(5):
            if settings.mill_levers[x] > 0:
                idx = settings.mill_levers[x] - 1
                total_width += number_x_bounds[idx][1] - number_x_bounds[idx][0]
        # Overwrite old panel
        overwrite_panel = Image.new(mode="RGBA", size=(58, 26), color=(131, 65, 24))
        modified_tex.paste(overwrite_panel, (3, 3), overwrite_panel)
        # Generate new number texture
        new_num_texture = Image.new(mode="RGBA", size=(total_width, 18))
        x_pos = 0
        for num in range(5):
            if settings.mill_levers[num] > 0:
                num_val = settings.mill_levers[num] - 1
                new_num_texture.paste(number_textures[num_val], (x_pos, 0), number_textures[num_val])
                x_pos += number_x_bounds[num_val][1] - number_x_bounds[num_val][0]
        scale_x = 58 / total_width
        scale_y = 26 / 18
        scale = min(scale_x, scale_y)
        x_size = int(total_width * scale)
        y_size = int(18 * scale)
        new_num_texture = new_num_texture.resize((x_size, y_size))
        x_offset = int((58 - x_size) / 2)
        modified_tex.paste(new_num_texture, (3 + x_offset, 3), new_num_texture)
        writeColorImageToROM(modified_tex, 25, 0x7CA, 64, 32, False, TextureFormat.RGBA5551)


def updateCryptLeverTexture(settings):
    """Update the two textures for Donkey Minecart entry."""
    if settings.crypt_levers[0] > 0:
        # Get a blank texture
        texture_0 = getFile(table_index=25, file_index=0x999, compressed=True, width=32, height=64, format=TextureFormat.RGBA5551)
        blank = texture_0.crop((8, 5, 23, 22))
        texture_0.paste(blank, (8, 42), blank)
        texture_1 = texture_0.copy()
        for xi, x in enumerate(settings.crypt_levers):
            corrected = x - 1
            y_slot = corrected % 3
            num = getNumberImage(xi + 1)
            num = num.transpose(Image.FLIP_TOP_BOTTOM)
            w, h = num.size
            scale = 2 / 3
            y_offset = int((h * scale) / 2)
            x_offset = int((w * scale) / 2)
            num = num.resize((int(w * scale), int(h * scale)))
            y_pos = (51, 33, 14)
            tl_y = y_pos[y_slot] - y_offset
            tl_x = 16 - x_offset
            if corrected < 3:
                texture_0.paste(num, (tl_x, tl_y), num)
            else:
                texture_1.paste(num, (tl_x, tl_y), num)
        writeColorImageToROM(texture_0, 25, 0x99A, 32, 64, False, TextureFormat.RGBA5551)
        writeColorImageToROM(texture_1, 25, 0x999, 32, 64, False, TextureFormat.RGBA5551)


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
    "Telling Killi to eventually play DK64",
    "Crediting Grant Kirkhope",
    "Dropping Crayons",
    "Saying Hello when others wont",
)


def writeBootMessages():
    """Write boot messages into ROM."""
    placed_messages = random.sample(boot_phrases, 4)
    for message_index, message in enumerate(placed_messages):
        LocalROM().seek(0x1FFD000 + (0x40 * message_index))
        LocalROM().writeBytes(message.upper().encode("ascii"))
