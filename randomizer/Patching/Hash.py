"""Locate Hash images for displaying on the website."""
import base64
import io
import zlib

from PIL import Image

from randomizer.Patching.Patcher import ROM, LocalROM


def get_hash_images(type="local"):
    """Get and return a list of hash images for the website UI."""
    images = [
        {"name": "bongos", "format": "rgba16", "table": 25, "index": 5548, "w": 40, "h": 40},
        {"name": "crown", "format": "rgba16", "table": 25, "index": 5893, "w": 44, "h": 44},
        {"name": "dk_coin", "format": "rgba16", "table": 7, "index": 500, "w": 48, "h": 44},
        {"name": "fairy", "format": "rgba32", "table": 25, "index": 5869, "w": 32, "h": 32},
        {"name": "guitar", "format": "rgba16", "table": 25, "index": 5547, "w": 40, "h": 40},
        {"name": "nin_coin", "format": "rgba16", "table": 25, "index": 5912, "w": 44, "h": 44},
        {"name": "orange", "format": "rgba16", "table": 7, "index": 309, "w": 32, "h": 32},
        {"name": "rainbow_coin", "format": "rgba16", "table": 25, "index": 5963, "w": 48, "h": 44},
        {"name": "rw_coin", "format": "rgba16", "table": 25, "index": 5905, "w": 44, "h": 44},
        {"name": "saxaphone", "format": "rgba16", "table": 25, "index": 5549, "w": 40, "h": 40},
    ]

    ptr_offset = 0x101C50
    loaded_images = []
    rom_type = None
    if type == "browser":
        rom_type = ROM()
    else:
        rom_type = LocalROM()
    for x in images:
        rom_type.seek(ptr_offset + (x["table"] * 4))
        ptr_table = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        rom_type.seek(ptr_table + (x["index"] * 4))
        img_start = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        rom_type.seek(ptr_table + ((x["index"] + 1) * 4))
        img_end = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        img_size = img_end - img_start
        rom_type.seek(img_start)
        if x["table"] == 25:
            dec = zlib.decompress(rom_type.readBytes(img_size), 15 + 32)
        else:
            dec = rom_type.readBytes(img_size)
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

        in_mem_file = io.BytesIO()
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.save(in_mem_file, format="PNG")
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()

        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode("ascii")
        loaded_images.append(base64_encoded_result_str)

    return loaded_images
