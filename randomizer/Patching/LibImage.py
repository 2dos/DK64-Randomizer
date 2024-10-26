"""Image modification library functions."""

import js
import zlib
import random
import gzip
from enum import IntEnum, auto
from PIL import Image
from randomizer.Patching.Patcher import ROM, LocalROM


class TextureFormat(IntEnum):
    """Texture Format Enum."""

    Null = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    I8 = auto()
    I4 = auto()
    IA8 = auto()
    IA4 = auto()


class ExtraTextures(IntEnum):
    """Extra Textures in Table 25 after the bonus skins."""

    FakeGBShine = 0
    RainbowCoin0 = auto()
    RainbowCoin1 = auto()
    RainbowCoin2 = auto()
    MelonSurface = auto()
    BonusShell = auto()
    OSprintLogoLeft = auto()
    OSprintLogoRight = auto()
    BLockerItemMove = auto()
    BLockerItemBlueprint = auto()
    BLockerItemFairy = auto()
    BLockerItemBean = auto()
    BLockerItemPearl = auto()
    BLockerItemRainbowCoin = auto()
    BLockerItemIceTrap = auto()
    BLockerItemPercentage = auto()
    BLockerItemBalloon = auto()
    BLockerItemCompanyCoin = auto()
    BLockerItemKong = auto()
    BeetleTex0 = auto()
    BeetleTex1 = auto()
    BeetleTex2 = auto()
    BeetleTex3 = auto()
    BeetleTex4 = auto()
    BeetleTex5 = auto()
    BeetleTex6 = auto()
    Feather0 = auto()
    Feather1 = auto()
    Feather2 = auto()
    Feather3 = auto()
    Feather4 = auto()
    Feather5 = auto()
    Feather6 = auto()
    Feather7 = auto()
    FoolOverlay = auto()
    MedalRim = auto()
    MushTop0 = auto()
    MushTop1 = auto()
    ShellWood = auto()
    ShellMetal = auto()
    ShellQMark = auto()
    RocketTop = auto()
    BlastTop = auto()


def getImageFromAddress(rom_address: int, width: int, height: int, compressed: bool, file_size: int, format: TextureFormat):
    """Get image from a ROM address."""
    try:
        LocalROM().seek(rom_address)
        data = LocalROM().readBytes(file_size)
    except Exception:
        ROM().seek(rom_address)
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


def getImageFile(table_index: int, file_index: int, compressed: bool, width: int, height: int, format: TextureFormat):
    """Grab image from file."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    return getImageFromAddress(file_start, width, height, compressed, file_size, format)


def getRandomHueShift(min: int = -359, max: int = 359) -> int:
    """Get random hue shift."""
    return random.randint(min, max)


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


def imageToCI(ROM_COPY: ROM, im_f, ci_index: int, tex_index: int, pal_index: int):
    """Change image to a CI texture."""
    if ci_index not in (4, 8):
        return
    color_count = 1 << ci_index
    if color_count < 32:
        im_f = im_f.quantize(colors=color_count, method=Image.MAXCOVERAGE)
    else:
        im_f = im_f.convert("P", palette=Image.ADAPTIVE, colors=color_count)
    palette_indexes = list(im_f.getdata())
    palette = im_f.getpalette()
    palette_colors = [tuple(palette[i : i + 3]) for i in range(0, len(palette), 3)]
    rgba5551_values = []
    for color in palette_colors:
        colv = 0
        for channel_value in color:
            val = channel_value & 0x1F
            colv <<= 5
            colv |= val
        colv |= 1
        rgba5551_values.append(colv)
    tex_bin = []
    if ci_index == 8:
        tex_bin = palette_indexes.copy()
    else:
        output_value = 0
        for index, value in enumerate(palette_indexes):
            if (index & 1) == 0:
                output_value = (value & 0xF) << 4
            else:
                output_value |= value & 0xF
                tex_bin.append(output_value)
    pal_bin = []
    for half in rgba5551_values:
        upper = (half >> 8) & 0xFF
        lower = half & 0xFF
        pal_bin.extend([upper, lower])
    tex_bin_file = gzip.compress(bytearray(tex_bin), compresslevel=9)
    pal_bin_file = gzip.compress(bytearray(pal_bin), compresslevel=9)
    tex_start = js.pointer_addresses[25]["entries"][tex_index]["pointing_to"]
    tex_end = js.pointer_addresses[25]["entries"][tex_index + 1]["pointing_to"]
    pal_start = js.pointer_addresses[25]["entries"][pal_index]["pointing_to"]
    pal_end = js.pointer_addresses[25]["entries"][pal_index + 1]["pointing_to"]
    if (tex_end - tex_start) < len(tex_bin_file):
        return
    if (pal_end - pal_start) < len(pal_bin_file):
        return
    ROM_COPY.seek(tex_start)
    ROM_COPY.write(tex_bin_file)
    ROM_COPY.seek(pal_start)
    ROM_COPY.write(pal_bin_file)
