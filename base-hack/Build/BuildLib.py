"""Library functions for the build procedure."""

import struct
from PIL import Image

main_pointer_table_offset = 0x101C50
BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something
ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"
finalROM = "rom/dk64-randomizer-base-dev.z64"
music_size = 24000
heap_size = 0x34000 + music_size
flut_size = 0
MODEL_DIRECTORY = "assets/models/"

INSTRUMENT_PADS = {
    168: "bongo",
    169: "guitar",
    170: "sax",
    171: "triangle",
    172: "trombone",
}

barrel_skins = (
    "gb",
    "dk",
    "diddy",
    "lanky",
    "tiny",
    "chunky",
    "bp",
    "nin_coin",
    "rw_coin",
    "key",
    "crown",
    "medal",
    "potion",
    "bean",
    "pearl",
    "fairy",
    "rainbow",
    "fakegb",
    "melon",
    "cranky",
    "funky",
    "candy",
    "snide",
    "hint",
)


def getBonusSkinOffset(offset: int):
    """Get texture index after the barrel skins."""
    return 6026 + (3 * len(barrel_skins)) + offset


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def hueShift(im: Image, amount: int):
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


def convertToRGBA32(png_file):
    """Convert PNG to RGBA32 binary."""
    im = Image.open(png_file)
    width, height = im.size
    pix = im.load()
    new_file = png_file.replace(".png", ".rgba32")
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                fh.write((r & 0xFF).to_bytes(1, "big"))
                fh.write((g & 0xFF).to_bytes(1, "big"))
                fh.write((b & 0xFF).to_bytes(1, "big"))
                fh.write((a & 0xFF).to_bytes(1, "big"))
