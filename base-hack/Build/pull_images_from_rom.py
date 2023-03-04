"""Pull hash images from ROM."""
import os
import zlib

from PIL import Image
from BuildLib import main_pointer_table_offset


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
    ImageData("bongos", "rgba16", 25, 5548, 40, 40, True, True),
    ImageData("crown", "rgba16", 25, 5893, 44, 44, True, True),
    ImageData("dkcoin", "rgba16", 7, 500, 48, 44, True, True),
    ImageData("fairy", "rgba32", 25, 5869, 32, 32, True, True),
    ImageData("fairy_0", "rgba32", 25, 0x16ED, 32, 32, True, True),
    ImageData("guitar", "rgba16", 25, 5547, 40, 40, True, True),
    ImageData("triangle", "rgba16", 25, 5550, 40, 40, True, True),
    ImageData("trombone", "rgba16", 25, 5551, 40, 40, True, True),
    ImageData("peanut", "rgba16", 7, 424, 32, 32, True, True),
    ImageData("peanut", "rgba16", 7, 424, 32, 32, True, True),
    ImageData("feather", "rgba16", 7, 642, 32, 32, True, True),
    ImageData("grape", "rgba16", 7, 650, 32, 32, True, True),
    ImageData("pineapple", "rgba16", 7, 666, 32, 48, True, True),
    ImageData("coconut", "rgba16", 7, 675, 40, 51, True, True),
    ImageData("nin_coin", "rgba16", 25, 5912, 44, 44, True, True),
    ImageData("orange", "rgba16", 7, 309, 32, 32, True, True),
    ImageData("rainbow_coin", "rgba16", 25, 5963, 48, 44, True, True),
    ImageData("rw_coin", "rgba16", 25, 5905, 44, 44, True, True),
    ImageData("sax", "rgba16", 25, 5549, 40, 40, True, True),
    ImageData("boss_key", "rgba16", 25, 5877, 44, 44, False, True),
    ImageData("01234", "rgba16", 14, 15, 76, 24, False, False),
    ImageData("56789", "rgba16", 14, 16, 76, 24, False, False),
    ImageData("MNO", "rgba16", 14, 9, 76, 24, False, False),
    ImageData("PQRS", "rgba16", 14, 10, 76, 24, False, False),
    ImageData("WXYL", "rgba16", 14, 12, 76, 24, False, False),
    ImageData("specialchars", "rgba16", 14, 30, 64, 32, False, False),
    ImageData("red_qmark_0", "rgba16", 7, 508, 32, 64, False, False),
    ImageData("red_qmark_1", "rgba16", 7, 509, 32, 64, False, False),
    ImageData("dk_tie_palette", "rgba16", 25, 3686, 32, 32, False, False),
    ImageData("tiny_palette", "rgba16", 25, 3689, 32, 32, False, False),
    ImageData("homing_crate_0", "rgba16", 7, 185, 32, 64, False, True),
    ImageData("homing_crate_1", "rgba16", 7, 200, 32, 64, False, True),
    ImageData("standard_crate_0", "rgba16", 7, 392, 32, 64, False, True),
    ImageData("standard_crate_1", "rgba16", 7, 407, 32, 64, False, True),
    ImageData("num_1_unlit", "rgba16", 7, 510, 32, 32, False, False),
    ImageData("num_1_lit", "rgba16", 7, 511, 32, 32, False, False),
    ImageData("num_6_unlit", "rgba16", 7, 520, 32, 32, False, False),
    ImageData("num_6_lit", "rgba16", 7, 521, 32, 32, False, False),
    ImageData("num_7_unlit", "rgba16", 7, 522, 32, 32, False, False),
    ImageData("num_7_lit", "rgba16", 7, 523, 32, 32, False, False),
    ImageData("num_9_unlit", "rgba16", 7, 526, 32, 32, False, False),
    ImageData("num_9_lit", "rgba16", 7, 527, 32, 32, False, False),
    ImageData("film", "rgba16", 7, 439, 48, 42, False, True),
    ImageData("melon", "rgba16", 7, 544, 48, 42, False, True),
    ImageData("headphones", "rgba16", 7, 979, 40, 40, False, True),
    ImageData("special_coin_side", "rgba16", 25, 5901, 44, 44, False, True),
    ImageData("gb", "rgba16", 25, 5468, 44, 44, False, True),
    ImageData("medal", "rgba16", 25, 0x156C, 44, 44, False, True),
    ImageData("dk_bp", "rgba16", 25, 0x15FC, 48, 42, False, True),
    ImageData("lanky_bp", "rgba16", 25, 0x1593, 48, 42, False, True),
    ImageData("key", "rgba16", 25, 0x16F5, 44, 44, False, True),
    ImageData("crown_shop", "rgba16", 25, 0x1705, 44, 44, False, True),
    ImageData("pearl", "rgba16", 25, 0xD5F, 32, 32, False, True),
    ImageData("bean", "rgba16", 25, 0xD3C, 64, 32, False, True),
    ImageData("rw_coin_noresize", "rgba16", 25, 5905, 44, 44, False, True),
    ImageData("nin_coin_noresize", "rgba16", 25, 5912, 44, 44, False, True),
    ImageData("crown_noresize", "rgba16", 25, 5893, 44, 44, False, True),
    ImageData("bonus_skin", "rgba16", 25, 0x128A, 16, 64, False, False),
    ImageData("gb_shine", "rgba16", 25, 0xB7B, 32, 32, False, False),
    ImageData("rainbow_coin_noflip", "rgba16", 25, 5963, 48, 44, False, False),
    ImageData("melon_resized", "rgba16", 7, 544, 48, 42, False, False),
    ImageData("melon_slice", "rgba16", 7, 0x142, 48, 42, False, True),
    ImageData("text_bubble", "ia8", 14, 0x52, 96, 64, False, False),
]

kong_tex = ["chunky", "tiny", "lanky", "diddy", "dk"]
tex_idx = 0x273
for kong in kong_tex:
    for x in range(2):
        images.append(ImageData(f"{kong}_face_{x}", "rgba16", 25, tex_idx + x, 32, 64, False, True))
    tex_idx += 2


if not os.path.exists("assets/hash"):
    os.mkdir("assets/hash")

print("Extracting Images from ROM")
with open("rom/dk64.z64", "rb") as fh:
    for x in images:
        fh.seek(main_pointer_table_offset + (x.table * 4))
        ptr_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(ptr_table + (x.index * 4))
        img_start = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(ptr_table + ((x.index + 1) * 4))
        img_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        img_size = img_end - img_start
        fh.seek(img_start)
        if x.table == 7:
            dec = fh.read(img_size)
        else:
            dec = zlib.decompress(fh.read(img_size), 15 + 32)
        img_name = f"assets/hash/{x.name}.png"
        if os.path.exists(img_name):
            os.remove(img_name)
        with open(img_name, "wb") as fg:
            fg.seek(0)
        im = Image.new(mode="RGBA", size=(x.width, x.height))
        pix = im.load()
        pix_count = x.width * x.height
        for pixel in range(pix_count):
            if x.format == "rgba16":
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
            elif x.format == "rgba32":
                start = pixel * 4
                end = start + 4
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 24) & 0xFF
                green = (pixel_data >> 16) & 0xFF
                blue = (pixel_data >> 8) & 0xFF
                alpha = pixel_data & 0xFF
            elif x.format == "ia8":
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
