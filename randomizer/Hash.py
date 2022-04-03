import zlib
from randomizer.Patcher import ROM
import base64


def get_hash_images():
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
    for x in images:
        ROM().seek(ptr_offset + (x["table"] * 4))
        ptr_table = ptr_offset + int.from_bytes(ROM().readBytes(4), "big")
        ROM().seek(ptr_table + (x["index"] * 4))
        img_start = ptr_offset + int.from_bytes(ROM().readBytes(4), "big")
        ROM().seek(ptr_table + ((x["index"] + 1) * 4))
        img_end = ptr_offset + int.from_bytes(ROM().readBytes(4), "big")
        img_size = img_end - img_start
        ROM().seek(img_start)
        if x["table"] == 25:
            dec = zlib.decompress(ROM().readBytes(img_size), 15 + 32)
        else:
            dec = ROM().readBytes(img_size)
        loaded_images.append(base64.b64encode(dec).decode("ascii"))

    print(loaded_images[0])
    return loaded_images
