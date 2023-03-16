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
        tile_image = getFile(7, question_mark_tiles[tile], False, 32, 64, "rgba5551")
        mask = getFile(7, question_mark_tile_masks[(tile % 2)], False, 32, 64, "rgba5551")
        resize = question_mark_resize
        mask = mask.resize((resize[0], resize[1]))
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, question_mark_offsets[(tile % 2)], int(tile / 2), (tile % 2))
        writeColorImageToROM(masked_tile, 7, question_mark_tiles[tile], 32, 64, False, "rgba5551")
    for tile in range(len(face_tiles)):
        face_index = int(tile / 4)
        if face_index < 5:
            width = 32
            height = 64
        else:
            width = 44
            height = 44
        mask = getFile(25, face_tile_masks[int(tile / 2)], True, width, height, "rgba5551")
        resize = face_resize[face_index]
        mask = mask.resize((resize[0], resize[1]))
        tile_image = getFile(7, face_tiles[tile], False, 32, 64, "rgba5551")
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, face_offsets[int(tile / 2)], face_index, (int(tile / 2) % 2))
        writeColorImageToROM(masked_tile, 7, face_tiles[tile], 32, 64, False, "rgba5551")


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


def maskImageWithOutline(im_f, base_index, min_y, type=""):
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
    if base_index == 2 or (base_index == 3 and color_bases[base_index] == "#13C4D8"):  # lanky or (tiny in Tritanopia mode)
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
            if format == "rgba32":
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
    if format == "rgba32":
        bytes_per_px = 4
    if len(data) > (bytes_per_px * width * height):
        print(f"Image too big error: {table_index} > {file_index}")
    if table_index in (14, 25):
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    ROM().writeBytes(data)


def writeKasplatHairColorToROM(color, table_index, file_index, format: str):
    """Write color to ROM for kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color)
    if format == "rgba32":
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
    """Write color to ROM for white kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color1)
    mask2 = getRGBFromHash(color2)
    if format == "rgba32":
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


def maskBlueprintImage(im_f, base_index, monochrome=False):
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
    if monochrome is True:
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
        # Figure out which colors to use and where to put them
        color1_offsets = [1548, 1580, 1612, 1644, 1676, 1708, 1756, 1788, 1804, 1820, 1836, 1852, 1868, 1884, 1900, 1916, 
                          1932, 1948, 1964, 1980, 1996, 2012, 2028, 2044, 2076, 2108, 2124, 2156, 2188, 2220, 2252, 2284, 
                          2316, 2348, 2380, 2396, 2412, 2428, 2444, 2476, 2508, 2540, 2572, 2604, 2636, 2652, 2668, 2684, 
                          2700, 2716, 2732, 2748, 2764, 2780, 2796, 2812, 2828, 2860, 2892, 2924, 2956, 2988, 3020, 3052]
        color2_offsets = [1564, 1596, 1628, 1660, 1692, 1724, 1740, 1772, 2332, 2364, 2460, 2492, 2524, 2556, 2588, 2620]
        new_color1 = getRGBFromHash(color_bases[kong])
        new_color2 = getRGBFromHash(color_bases[kong])
        if kong == 0:
            for channel in range(3):
                new_color2[channel] = max(80, new_color1[channel])  # Too black is bad

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
    """Recolor the Wrinkly hint door doorframes for colorblind mode."""
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
        new_color1 = getRGBFromHash(color_bases[4])
        new_color2 = getRGBFromHash(color_bases[2])
        new_color3 = getRGBFromHash(color_bases[1])

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
                new_color[channel] = max(39, new_color[channel])  # Too black is bad

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


def overwrite_object_colors(spoiler: Spoiler):
    """Overwrite object colors."""
    global color_bases
    mode = spoiler.settings.colorblind_mode
    if mode != ColorblindMode.off:
        if mode == ColorblindMode.prot:
            color_bases = ["#000000", "#0072FF", "#766D5A", "#FFFFFF", "#FDE400"]
        elif mode == ColorblindMode.deut:
            color_bases = ["#000000", "#318DFF", "#7F6D59", "#FFFFFF", "#E3A900"]
        elif mode == ColorblindMode.trit:
            color_bases = ["#000000", "#C72020", "#13C4D8", "#FFFFFF", "#FFA4A4"]
        file = 175
        dk_single = getFile(7, file, False, 44, 44, "rgba5551")
        dk_single = dk_single.resize((21, 21))
        blueprint_lanky = []
        # Preload blueprint images. Lanky's blueprint image is so much easier to mask, because it is blue, and the frame is brown
        for file in range(8):
            blueprint_lanky.append(getFile(25, 5519 + (file), True, 48, 42, "rgba5551"))
        writeWhiteKasplatHairColorToROM("#FFFFFF", "#000000", 25, 4125, "rgba5551")
        recolorWrinklyDoors()
        recolorSlamSwitches()
        recolorRotatingRoomTiles()
        recolorBlueprintModelTwo()
        for kong_index in range(5):
            # file = 4120
            # # Kasplat Hair
            # hair_im = getFile(25, file, True, 32, 44, "rgba5551")
            # hair_im = maskImage(hair_im, kong_index, 0)
            # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False)
            writeKasplatHairColorToROM(color_bases[kong_index], 25, [4124, 4122, 4123, 4120, 4121][kong_index], "rgba5551")
            for file in range(5519, 5527):
                # Blueprint sprite
                blueprint_start = [5624, 5608, 5519, 5632, 5616]
                blueprint_im = blueprint_lanky[(file - 5519)]
                blueprint_im = maskBlueprintImage(blueprint_im, kong_index, True)
                writeColorImageToROM(blueprint_im, 25, blueprint_start[kong_index] + (file - 5519), 48, 42, False, "rgba5551")
            for file in range(4925, 4931):
                # Shockwave
                shockwave_start = [4897, 4903, 4712, 4950, 4925]
                shockwave_im = getFile(25, shockwave_start[kong_index] + (file - 4925), True, 32, 32, "rgba32")
                shockwave_im = maskImage(shockwave_im, kong_index, 0)
                writeColorImageToROM(shockwave_im, 25, shockwave_start[kong_index] + (file - 4925), 32, 32, False, "rgba32")
            if kong_index == 0 or kong_index == 3 or (kong_index == 2 and mode != ColorblindMode.trit):  # Lanky (prot, deut only) or DK or Tiny
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getFile(7, single_start[kong_index] + (file - 152), False, 44, 44, "rgba5551")
                    single_im = maskImageWithOutline(single_im, kong_index, 0, "single")
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, "rgba5551")
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, "rgba5551")
                    coin_im = maskImageWithOutline(coin_im, kong_index, 0)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, "rgba5551")
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, "rgba5551")
                    bunch_im = maskImageWithOutline(bunch_im, kong_index, 0, "bunch")
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, "rgba5551")
                for file in range(5819, 5827):
                    # Balloon
                    balloon_start = [5835, 5827, 5843, 5851, 5819]
                    balloon_im = getFile(25, balloon_start[kong_index] + (file - 5819), True, 32, 64, "rgba5551")
                    balloon_im = maskImageWithOutline(balloon_im, kong_index, 33)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, balloon_start[kong_index] + (file - 5819), 32, 64, False, "rgba5551")
            else:
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getFile(7, single_start[kong_index] + (file - 152), False, 44, 44, "rgba5551")
                    single_im = maskImage(single_im, kong_index, 0)
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, "rgba5551")
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, "rgba5551")
                    coin_im = maskImage(coin_im, kong_index, 0)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, "rgba5551")
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, "rgba5551")
                    bunch_im = maskImage(bunch_im, kong_index, 0, True)
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, "rgba5551")
                for file in range(5819, 5827):
                    # Balloon
                    balloon_start = [5835, 5827, 5843, 5851, 5819]
                    balloon_im = getFile(25, balloon_start[kong_index] + (file - 5819), True, 32, 64, "rgba5551")
                    balloon_im = maskImage(balloon_im, kong_index, 33)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, balloon_start[kong_index] + (file - 5819), 32, 64, False, "rgba5551")


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
