"""Convert RGB colors into a kong color palette."""
import gzip
import math

import js
from randomizer.Patching.Patcher import ROM


def convertRGBAToBytearray(rgba_lst):
    """Convert RGBA list with 4 items (r,g,b,a) to a two-byte array in RGBA5551 format."""
    twobyte = (rgba_lst[0] << 11) | (rgba_lst[1] << 6) | (rgba_lst[2] << 1) | rgba_lst[3]
    lower = twobyte % 256
    upper = int(twobyte / 256) % 256
    return [upper, lower]


def convertColors(color_palettes):
    """Convert color into RGBA5551 format."""
    for palette in color_palettes:
        for zone in palette["zones"]:
            rgba_list = []
            if zone["fill_type"] == "checkered" or zone["fill_type"] == "radial":
                lim = 2
            else:
                lim = 1
            for x in range(lim):
                rgba = [0, 0, 0, 1]
                for i in range(3):
                    if zone["fill_type"] == "radial":
                        val = int(int(f"0x{zone['colors'][0][(2*i)+1:(2*i)+3]}", 16) * (1 / 8))
                        if x == 1:
                            val = int(val * 2)
                    else:
                        val = int(int(f"0x{zone['colors'][x][(2*i)+1:(2*i)+3]}", 16) * (1 / 8))
                    if val < 0:
                        val = 0
                    elif val > 31:
                        val = 31
                    rgba[i] = val
                rgba_list.append(rgba)
            bytes_array = []
            if zone["fill_type"] in ("block", "kong"):
                ext = convertRGBAToBytearray(rgba_list[0])
                for x in range(32 * 32):
                    bytes_array.extend(ext)
            elif zone["fill_type"] == "radial":
                cen_x = 15.5
                cen_y = 15.5
                max_dist = (cen_x * cen_x) + (cen_y * cen_y)
                channel_diffs = [0, 0, 0]
                for i in range(3):
                    channel_diffs[i] = rgba_list[1][i] - rgba_list[0][i]
                for y in range(32):
                    for x in range(32):
                        dx = cen_x - x
                        dy = cen_y - y
                        dst = (dx * dx) + (dy * dy)
                        proportion = 1 - (dst / max_dist)
                        prop = [0, 0, 0, 1]
                        for i in range(3):
                            val = int((channel_diffs[i] * proportion) + rgba_list[0][i])
                            if val < 0:
                                val = 0
                            elif val > 31:
                                val = 31
                            prop[i] = val
                        ext = convertRGBAToBytearray(prop)
                        bytes_array.extend(ext)
            elif zone["fill_type"] == "checkered":
                for size_mult in range(3):
                    dim_s = int(32 / math.pow(2, size_mult))
                    pol_s = int(dim_s / 8)
                    for y in range(dim_s):
                        for x in range(dim_s):
                            y_offset = 0
                            if size_mult == 1:
                                y_offset = 1
                            color_polarity_x = int(x / pol_s) % 2
                            color_polarity_y = int((y + y_offset) / pol_s) % 2
                            color_polarity = (color_polarity_x + color_polarity_y) % 2
                            ext = convertRGBAToBytearray(rgba_list[color_polarity])
                            bytes_array.extend(ext)
                for i in range(18):
                    ext = convertRGBAToBytearray(rgba_list[1])
                    bytes_array.extend(ext)
                for i in range(4):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray(rgba_list[1])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
            elif zone["fill_type"] == "patch":
                for size_mult in range(3):
                    patch_start_x = int(6 / math.pow(2, size_mult))
                    patch_start_y = int(8 / math.pow(2, size_mult))
                    # print(f"{patch_start_x} | {patch_start_y}")
                    patch_size = 3 - size_mult
                    if patch_size == 3:
                        patch_size = 5
                    dim_s = int(32 / math.pow(2, size_mult))
                    for y in range(dim_s):
                        for x in range(dim_s):
                            is_block = True  # Set to false to generate patch
                            if x < patch_start_x:
                                is_block = True
                            elif x >= patch_start_x + (4 * patch_size):
                                is_block = True
                            elif y < patch_start_y:
                                is_block = True
                            elif y >= patch_start_y + (3 * patch_size):
                                is_block = True
                            if is_block:
                                ext = convertRGBAToBytearray(rgba_list[0])
                            else:
                                delta_x = x - patch_start_x
                                delta_y = y - patch_start_y
                                color_polarity_x = int(delta_x / patch_size) % 2
                                color_polarity_y = int(delta_y / patch_size) % 2
                                color_polarity = (color_polarity_x + color_polarity_y) % 2
                                patch_rgba = [31, 31, 31, 1]
                                if color_polarity == 1:
                                    patch_rgba = [31, 0, 0, 1]
                                ext = convertRGBAToBytearray(patch_rgba)
                            bytes_array.extend(ext)
                for i in range(18):
                    ext = convertRGBAToBytearray(rgba_list[0])
                    bytes_array.extend(ext)
                for i in range(4):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray(rgba_list[0])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
            elif zone["fill_type"] == "sparkle":
                dim_rgba = []
                for channel_index, channel in enumerate(rgba_list[0]):
                    if channel_index == 3:
                        dim_rgba.append(1)
                    else:
                        dim_channel = 0.8 * channel
                        dim_rgba.append(int(dim_channel))
                for y in range(32):
                    for x in range(32):
                        pix_rgba = []
                        if x == 31:
                            pix_rgba = rgba_list[0].copy()
                        else:
                            for channel_index in range(4):
                                if channel_index == 3:
                                    pix_channel = 1
                                else:
                                    diff = rgba_list[0][channel_index] - dim_rgba[channel_index]
                                    applied_diff = int(diff * (x / 31))
                                    pix_channel = dim_rgba[channel_index] + applied_diff
                                    if pix_channel < 0:
                                        pix_channel = 0
                                    if pix_channel > 31:
                                        pix_channel = 31
                                pix_rgba.append(pix_channel)
                        sparkle_px = [[28, 5], [27, 10], [21, 11], [25, 14], [23, 15], [23, 16], [26, 18], [20, 19], [25, 25]]
                        for px in sparkle_px:
                            if px[0] == x and px[1] == y:
                                pix_rgba = [0xFF, 0xFF, 0xFF, 1]
                        bytes_array.extend(convertRGBAToBytearray(pix_rgba))

            write_point = js.pointer_addresses[25]["entries"][zone["image"]]["pointing_to"]
            ROM().seek(write_point)
            ROM().writeBytes(gzip.compress(bytearray(bytes_array), compresslevel=9))
