"""Convert 63x63 Portal image into 4 32x32 segments."""

import os

from PIL import Image


def convertPortalImage(image_name):
    """Split image into 4 segments for the portal."""
    im = Image.open(image_name)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    pix = im.load()

    caps = {"NW": [[0, 0], [32, 32]], "SW": [[0, 31], [32, 63]], "SE": [[31, 31], [63, 63]], "NE": [[31, 0], [63, 32]]}
    split_list = []
    for sub in caps.keys():
        x_min = caps[sub][0][0]
        x_max = caps[sub][1][0]
        x_diff = x_max - x_min
        y_min = caps[sub][0][1]
        y_max = caps[sub][1][1]
        y_diff = y_max - y_min
        im2 = Image.new("RGBA", size=(x_diff, y_diff))
        pix2 = im2.load()
        for x_offset in range(x_diff):
            x = x_min + x_offset
            for y_offset in range(y_diff):
                y = y_min + y_offset
                pix_rgba = pix[x, y]
                pix2[x_offset, y_offset] = pix_rgba
        new_name = image_name.replace(".png", f"_{sub}.png")
        split_list.append(new_name)
        im2.save(new_name)
    return split_list
