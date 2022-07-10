"""Pull hash images from ROM."""
import os
import zlib

from PIL import Image

images = [
    {
        "name": "bongos",
        "format": "rgba16",
        "table": 25,
        "index": 5548,
        "w": 40,
        "h": 40,
        "resize": True,
        "flip": True,
    },
    {"name": "crown", "format": "rgba16", "table": 25, "index": 5893, "w": 44, "h": 44, "resize": True, "flip": True},
    {"name": "dkcoin", "format": "rgba16", "table": 7, "index": 500, "w": 48, "h": 44, "resize": True, "flip": True},
    {"name": "fairy", "format": "rgba32", "table": 25, "index": 5869, "w": 32, "h": 32, "resize": True, "flip": True},
    {
        "name": "guitar",
        "format": "rgba16",
        "table": 25,
        "index": 5547,
        "w": 40,
        "h": 40,
        "resize": True,
        "flip": True,
    },
    {"name": "nin_coin", "format": "rgba16", "table": 25, "index": 5912, "w": 44, "h": 44, "resize": True, "flip": True},
    {
        "name": "orange",
        "format": "rgba16",
        "table": 7,
        "index": 309,
        "w": 32,
        "h": 32,
        "resize": True,
        "flip": True,
    },
    {"name": "rainbow_coin", "format": "rgba16", "table": 25, "index": 5963, "w": 48, "h": 44, "resize": True, "flip": True},
    {"name": "rw_coin", "format": "rgba16", "table": 25, "index": 5905, "w": 44, "h": 44, "resize": True, "flip": True},
    {
        "name": "sax",
        "format": "rgba16",
        "table": 25,
        "index": 5549,
        "w": 40,
        "h": 40,
        "resize": True,
        "flip": True,
    },
    {
        "name": "boss_key",
        "format": "rgba16",
        "table": 25,
        "index": 5877,
        "w": 44,
        "h": 44,
        "resize": False,
        "flip": True,
    },
    {
        "name": "01234",
        "format": "rgba16",
        "table": 14,
        "index": 15,
        "w": 76,
        "h": 24,
        "resize": False,
        "flip": False,
    },
    {
        "name": "56789",
        "format": "rgba16",
        "table": 14,
        "index": 16,
        "w": 76,
        "h": 24,
        "resize": False,
        "flip": False,
    },
    {
        "name": "WXYL",
        "format": "rgba16",
        "table": 14,
        "index": 12,
        "w": 76,
        "h": 24,
        "resize": False,
        "flip": False,
    },
    {
        "name": "specialchars",
        "format": "rgba16",
        "table": 14,
        "index": 0x1E,
        "w": 64,
        "h": 32,
        "resize": False,
        "flip": False,
    },
    {
        "name": "red_qmark_0",
        "format": "rgba16",
        "table": 7,
        "index": 508,
        "w": 32,
        "h": 64,
        "resize": False,
        "flip": False,
    },
    {
        "name": "red_qmark_1",
        "format": "rgba16",
        "table": 7,
        "index": 509,
        "w": 32,
        "h": 64,
        "resize": False,
        "flip": False,
    },
]

kong_tex = ["chunky", "tiny", "lanky", "diddy", "dk"]
tex_idx = 0x273
for kong in kong_tex:
    for x in range(2):
        images.append(
            {
                "name": f"{kong}_face_{x}",
                "format": "rgba16",
                "table": 25,
                "index": tex_idx + x,
                "w": 32,
                "h": 64,
                "resize": False,
                "flip": True,
            }
        )
    tex_idx += 2

ptr_offset = 0x101C50

if not os.path.exists("assets/Non-Code/hash"):
    os.mkdir("assets/Non-Code/hash")

print("Extracting Images from ROM")
with open("rom/dk64.z64", "rb") as fh:
    for x in images:
        fh.seek(ptr_offset + (x["table"] * 4))
        ptr_table = ptr_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(ptr_table + (x["index"] * 4))
        img_start = ptr_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(ptr_table + ((x["index"] + 1) * 4))
        img_end = ptr_offset + int.from_bytes(fh.read(4), "big")
        img_size = img_end - img_start
        fh.seek(img_start)
        if x["table"] == 7:
            dec = fh.read(img_size)
        else:
            dec = zlib.decompress(fh.read(img_size), 15 + 32)
        img_name = f"assets/Non-Code/hash/{x['name']}.png"
        if os.path.exists(img_name):
            os.remove(img_name)
        with open(img_name, "wb") as fg:
            fg.seek(0)
        im = Image.new(mode="RGBA", size=(x["w"], x["h"]))
        pix = im.load()
        pix_count = x["w"] * x["h"]
        for pixel in range(pix_count):
            if x["format"] == "rgba16":
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
            elif x["format"] == "rgba32":
                start = pixel * 4
                end = start + 4
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 24) & 0xFF
                green = (pixel_data >> 16) & 0xFF
                blue = (pixel_data >> 8) & 0xFF
                alpha = pixel_data & 0xFF
            pix_x = pixel % x["w"]
            pix_y = int(pixel / x["w"])
            pix[pix_x, pix_y] = (red, green, blue, alpha)
        if x["flip"]:
            im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if x["resize"]:
            im = im.resize((32, 32))
        im.save(img_name)
