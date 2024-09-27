"""Pull hash images from ROM."""

import os
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, TextureFormat
from BuildLib import ROMName
from PIL import Image


class ImageData:
    """Class to store information regarding images."""

    def __init__(self, name: str, format: str, table: int, index: int, width: int, height: int, resize: bool, flip: bool):
        """Initialize with given data."""
        self.name = name
        self.format = format
        self.table = table
        self.index = index
        self.width = width
        self.height = height
        self.resize = resize
        self.flip = flip


crate_frame_l = 7
crate_frame_r = 9
images = [
    ImageData("bongos", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5548, 40, 40, True, True),
    ImageData("crown", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5893, 44, 44, True, True),
    ImageData("dkcoin", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 500, 48, 44, True, True),
    ImageData("fairy", TextureFormat.RGBA32, TableNames.TexturesGeometry, 5869, 32, 32, True, True),
    ImageData("fairy_0", TextureFormat.RGBA32, TableNames.TexturesGeometry, 0x16ED, 32, 32, True, True),
    ImageData("guitar", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5547, 40, 40, True, True),
    ImageData("triangle", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5550, 40, 40, True, True),
    ImageData("trombone", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5551, 40, 40, True, True),
    ImageData("peanut", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 424, 32, 32, True, True),
    ImageData("peanut", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 424, 32, 32, True, True),
    ImageData("feather", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 642, 32, 32, True, True),
    ImageData("grape", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 650, 32, 32, True, True),
    ImageData("pineapple", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 666, 32, 48, True, True),
    ImageData("coconut", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 675, 40, 51, True, True),
    ImageData("nin_coin", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5912, 44, 44, True, True),
    ImageData("orange", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 309, 32, 32, True, True),
    ImageData("rainbow_coin", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5963, 48, 44, True, True),
    ImageData("rw_coin", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5905, 44, 44, True, True),
    ImageData("sax", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5549, 40, 40, True, True),
    ImageData("boss_key", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5877, 44, 44, False, True),
    ImageData("01234", TextureFormat.RGBA5551, TableNames.TexturesHUD, 15, 76, 24, False, False),
    ImageData("56789", TextureFormat.RGBA5551, TableNames.TexturesHUD, 16, 76, 24, False, False),
    ImageData("MNO", TextureFormat.RGBA5551, TableNames.TexturesHUD, 9, 76, 24, False, False),
    ImageData("PQRS", TextureFormat.RGBA5551, TableNames.TexturesHUD, 10, 76, 24, False, False),
    ImageData("WXYL", TextureFormat.RGBA5551, TableNames.TexturesHUD, 12, 76, 24, False, False),
    ImageData("specialchars", TextureFormat.RGBA5551, TableNames.TexturesHUD, 30, 64, 32, False, False),
    ImageData("red_qmark_0", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 508, 32, 64, False, False),
    ImageData("red_qmark_1", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 509, 32, 64, False, False),
    ImageData("dk_tie_palette", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 3686, 32, 32, False, False),
    ImageData("tiny_palette", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 3689, 32, 32, False, False),
    ImageData("homing_crate_0", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 185, 32, 64, False, True),
    ImageData("homing_crate_1", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 200, 32, 64, False, True),
    ImageData("standard_crate_0", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 392, 32, 64, False, True),
    ImageData("standard_crate_1", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 407, 32, 64, False, True),
    ImageData("num_1_unlit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 510, 32, 32, False, False),
    ImageData("num_1_lit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 511, 32, 32, False, False),
    ImageData("num_6_unlit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 520, 32, 32, False, False),
    ImageData("num_6_lit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 521, 32, 32, False, False),
    ImageData("num_7_unlit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 522, 32, 32, False, False),
    ImageData("num_7_lit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 523, 32, 32, False, False),
    ImageData("num_9_unlit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 526, 32, 32, False, False),
    ImageData("num_9_lit", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 527, 32, 32, False, False),
    ImageData("film", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 439, 48, 42, False, True),
    ImageData("melon", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 544, 48, 42, False, True),
    ImageData("headphones", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 979, 40, 40, False, True),
    ImageData("special_coin_side", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5901, 44, 44, False, True),
    ImageData("gb", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5468, 44, 44, False, True),
    ImageData("medal", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x156C, 44, 44, False, True),
    ImageData("dk_bp", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x15FC, 48, 42, False, True),
    ImageData("lanky_bp", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x1593, 48, 42, False, True),
    ImageData("key", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x16F5, 44, 44, False, True),
    ImageData("crown_shop", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x1705, 44, 44, False, True),
    ImageData("pearl", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xD5F, 32, 32, False, True),
    ImageData("bean", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xD3C, 64, 32, False, True),
    ImageData("rw_coin_noresize", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5905, 44, 44, False, True),
    ImageData("nin_coin_noresize", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5912, 44, 44, False, True),
    ImageData("crown_noresize", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5893, 44, 44, False, True),
    ImageData("bonus_skin", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x128A, 16, 64, False, False),
    ImageData("gb_shine", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xB7B, 32, 32, False, False),
    ImageData("rainbow_coin_noflip", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 5963, 48, 44, False, False),
    ImageData("melon_resized", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 544, 48, 42, False, False),
    ImageData("melon_slice", TextureFormat.RGBA5551, TableNames.TexturesUncompressed, 0x142, 48, 42, False, True),
    ImageData("text_bubble", TextureFormat.IA8, TableNames.TexturesHUD, 0x52, 96, 64, False, False),
    ImageData("warp_top_0", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xDF9, 32, 64, False, False),
    ImageData("warp_top_1", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xDFA, 32, 64, False, False),
    ImageData("warp_rim_0", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xBB2, 32, 16, False, False),
    ImageData("warp_rim_1", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xBB3, 32, 16, False, False),
    ImageData("gun_crosshair", TextureFormat.IA8, TableNames.TexturesHUD, 0x38, 64, 64, False, False),
    ImageData("scoff_head", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xC9D, 48, 42, False, True),
    ImageData("wrinkly", TextureFormat.IA8, TableNames.TexturesGeometry, 0x1773, 64, 64, False, True),
    ImageData("diddy_balloon", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x16C3, 32, 64, False, False),
    ImageData("dirt_face", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x1379, 32, 32, False, False),
    ImageData("snide_face", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x172E, 64, 32, False, False),
    ImageData("white_font_early", TextureFormat.IA8, TableNames.TexturesHUD, 3, 176, 16, False, False),
    ImageData("white_font_late", TextureFormat.IA8, TableNames.TexturesHUD, 4, 176, 16, False, False),
    ImageData("question_mark", TextureFormat.IA8, TableNames.TexturesGeometry, 5923, 16, 32, False, True),
    ImageData("k_rool_head_left", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x383, 32, 64, False, True),
    ImageData("k_rool_head_right", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x384, 32, 64, False, True),
    ImageData("medal_rim", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xBAB, 32, 32, False, False),
    ImageData("mush_top_0", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x67F, 64, 32, False, False),
    ImageData("mush_top_1", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x680, 64, 32, False, False),
    ImageData("cannon_support", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x12B5, 48, 32, False, False),
    ImageData("cannon_base", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0x12B8, 44, 44, False, False),
    ImageData("barrel_bottom", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xF14, 1, 1372, False, False),
]

shop_owners = {
    "candy": 0x172A,
    "cranky": 0x1387,
    "funky": 0x172F,
}

for owner in shop_owners:
    for x in range(4):
        images.append(ImageData(f"{owner}_face_{x}", TextureFormat.RGBA5551, TableNames.TexturesGeometry, shop_owners[owner] + x, 32, 32, False, False))

kong_tex = ["chunky", "tiny", "lanky", "diddy", "dk"]
tex_idx = 0x273
for kong in kong_tex:
    for x in range(2):
        images.append(ImageData(f"{kong}_face_{x}", TextureFormat.RGBA5551, TableNames.TexturesGeometry, tex_idx + x, 32, 64, False, True))
    tex_idx += 2

for x in range(7):
    size = 0xAB8
    if x == 2:
        size = 0xAF8
    elif x == 6:
        size = 0x560
    images.append(ImageData(f"beetle_img_{0xFC3 + x}", TextureFormat.RGBA5551, TableNames.TexturesGeometry, 0xFC3 + x, size >> 1, 1, False, False))

if not os.path.exists("assets/hash"):
    os.mkdir("assets/hash")

print("Extracting Images from ROM")
with open(ROMName, "rb") as fh:
    for x in images:
        image_file = ROMPointerFile(fh, x.table, x.index)
        fh.seek(image_file.start)
        if x.table == 7:
            dec = fh.read(image_file.size)
        else:
            dec = zlib.decompress(fh.read(image_file.size), 15 + 32)
        img_name = f"assets/hash/{x.name}.png"
        if os.path.exists(img_name):
            os.remove(img_name)
        with open(img_name, "wb") as fg:
            fg.seek(0)
        im = Image.new(mode="RGBA", size=(x.width, x.height))
        pix = im.load()
        pix_count = x.width * x.height
        for pixel in range(pix_count):
            if x.format == TextureFormat.RGBA5551:
                start = pixel * 2
                end = start + 2
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 11) & 0x1F
                green = (pixel_data >> 6) & 0x1F
                blue = (pixel_data >> 1) & 0x1F
                alpha = pixel_data & 1
                red = int((red / 0x1F) * 0xFF)
                green = int((green / 0x1F) * 0xFF)
                blue = int((blue / 0x1F) * 0xFF)
                alpha = alpha * 255
            elif x.format == TextureFormat.RGBA32:
                start = pixel * 4
                end = start + 4
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 24) & 0xFF
                green = (pixel_data >> 16) & 0xFF
                blue = (pixel_data >> 8) & 0xFF
                alpha = pixel_data & 0xFF
            elif x.format == TextureFormat.IA8:
                start = pixel
                end = pixel + 1
                pixel_data = int.from_bytes(dec[start:end], "big")
                intensity = int(((pixel_data >> 4) / 0xF) * 255)
                alpha = int(((pixel_data & 0xF) / 0xF) * 255)
                red = intensity
                green = intensity
                blue = intensity
            pix_x = pixel % x.width
            pix_y = int(pixel / x.width)
            pix[pix_x, pix_y] = (red, green, blue, alpha)
        if x.flip:
            im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if x.resize:
            im = im.resize((32, 32))
        im.save(img_name)
