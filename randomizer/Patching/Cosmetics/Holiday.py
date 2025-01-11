"""All code associated with temporary holiday-based cosmetic effects."""

import gzip
from PIL import Image, ImageEnhance
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Library.Generic import Holidays, getHoliday
from randomizer.Patching.Library.Image import (
    getImageFile,
    getBonusSkinOffset,
    ExtraTextures,
    TextureFormat,
    maskImageWithColor,
    writeColorImageToROM,
    hueShift,
    hueShiftImageContainer,
)
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Settings import CharacterColors, KongModels


def changeBarrelColor(ROM_COPY: ROM, barrel_color: tuple = None, metal_color: tuple = None, brighten_barrel: bool = False):
    """Change the colors of the various barrels."""
    wood_img = getImageFile(ROM_COPY, 25, getBonusSkinOffset(ExtraTextures.ShellWood), True, 32, 64, TextureFormat.RGBA5551)
    metal_img = getImageFile(ROM_COPY, 25, getBonusSkinOffset(ExtraTextures.ShellMetal), True, 32, 64, TextureFormat.RGBA5551)
    qmark_img = getImageFile(ROM_COPY, 25, getBonusSkinOffset(ExtraTextures.ShellQMark), True, 32, 64, TextureFormat.RGBA5551)
    if barrel_color is not None:
        if brighten_barrel:
            enhancer = ImageEnhance.Brightness(wood_img)
            wood_img = enhancer.enhance(2)
        wood_img = maskImageWithColor(wood_img, barrel_color)
    if metal_color is not None:
        metal_img = maskImageWithColor(metal_img, metal_color)
    wood_img.paste(metal_img, (0, 0), metal_img)
    writeColorImageToROM(wood_img, 25, getBonusSkinOffset(ExtraTextures.BonusShell), 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)  # Bonus Barrel
    tag_img = Image.new(mode="RGBA", size=(32, 64))
    tag_img.paste(wood_img, (0, 0), wood_img)
    tag_img.paste(qmark_img, (0, 0), qmark_img)
    writeColorImageToROM(tag_img, 25, 4938, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)  # Tag Barrel
    # Compose Transform Barrels
    kongs = [
        {"face_left": 0x27C, "face_right": 0x27B, "barrel_tex_start": 4817, "targ_width": 24},  # DK
        {"face_left": 0x279, "face_right": 0x27A, "barrel_tex_start": 4815, "targ_width": 24},  # Diddy
        {"face_left": 0x277, "face_right": 0x278, "barrel_tex_start": 4819, "targ_width": 24},  # Lanky
        {"face_left": 0x276, "face_right": 0x275, "barrel_tex_start": 4769, "targ_width": 24},  # Tiny
        {"face_left": 0x273, "face_right": 0x274, "barrel_tex_start": 4747, "targ_width": 24},  # Chunky
    ]
    for kong in kongs:
        bar_left = Image.new(mode="RGBA", size=(32, 64))
        bar_right = Image.new(mode="RGBA", size=(32, 64))
        face_left = getImageFile(ROM_COPY, 25, kong["face_left"], True, 32, 64, TextureFormat.RGBA5551)
        face_right = getImageFile(ROM_COPY, 25, kong["face_right"], True, 32, 64, TextureFormat.RGBA5551)
        width = kong["targ_width"]
        height = width * 2
        face_left = face_left.resize((width, height))
        face_right = face_right.resize((width, height))
        right_w_offset = 32 - width
        top_h_offset = (64 - height) >> 1
        bar_left.paste(wood_img, (0, 0), wood_img)
        bar_right.paste(wood_img, (0, 0), wood_img)
        bar_left.paste(face_left, (right_w_offset, top_h_offset), face_left)
        bar_right.paste(face_right, (0, top_h_offset), face_right)
        writeColorImageToROM(bar_left, 25, kong["barrel_tex_start"], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
        writeColorImageToROM(bar_right, 25, kong["barrel_tex_start"] + 1, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    # Cannons
    barrel_left = Image.new(mode="RGBA", size=(32, 64))
    barrel_right = Image.new(mode="RGBA", size=(32, 64))
    barrel_left.paste(wood_img, (0, 0), wood_img)
    barrel_right.paste(wood_img, (0, 0), wood_img)
    barrel_left = barrel_left.crop((0, 0, 16, 64))
    barrel_right = barrel_right.crop((16, 0, 32, 64))
    writeColorImageToROM(barrel_left, 25, 0x12B3, 16, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    writeColorImageToROM(barrel_right, 25, 0x12B4, 16, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    if barrel_color is not None:
        tex_data = {
            getBonusSkinOffset(ExtraTextures.RocketTop): (1, 1372),
            0x12B5: (48, 32),
            0x12B8: (44, 44),
        }
        for img in tex_data:
            dim_x = tex_data[img][0]
            dim_y = tex_data[img][1]
            img_output = getImageFile(ROM_COPY, 25, img, True, dim_x, dim_y, TextureFormat.RGBA5551)
            img_output = maskImageWithColor(img_output, barrel_color)
            writeColorImageToROM(img_output, 25, img, dim_x, dim_y, False, TextureFormat.RGBA5551, ROM_COPY)


def applyCelebrationRims(ROM_COPY: ROM, hue_shift: int, enabled_bananas: list[bool] = [False, False, False, False, False]):
    """Retexture the warp pad rims to have a more celebratory tone."""
    banana_textures = []
    vanilla_banana_textures = [0xA8, 0x98, 0xE8, 0xD0, 0xF0]
    for kong_index, ban in enumerate(enabled_bananas):
        if ban:
            banana_textures.append(vanilla_banana_textures[kong_index])
    place_bananas = False
    if len(banana_textures) > 0:
        place_bananas = True
        if len(banana_textures) < 4:
            banana_textures = (banana_textures * 4)[:4]
    if place_bananas:
        bananas = [getImageFile(ROM_COPY, 7, x, False, 44, 44, TextureFormat.RGBA5551).resize((14, 14)) for x in banana_textures]
    banana_placement = [
        # File, x, y
        [0xBB3, 15, 1],  # 3
        [0xBB2, 2, 1],  # 2
        [0xBB3, 0, 1],  # 4
        [0xBB2, 17, 1],  # 1
    ]
    for img in (0xBB2, 0xBB3):
        side_im = getImageFile(ROM_COPY, 25, img, True, 32, 16, TextureFormat.RGBA5551)
        hueShift(side_im, hue_shift)
        if place_bananas:
            for bi, banana in enumerate(bananas):
                if banana_placement[bi][0] == img:
                    b_x = banana_placement[bi][1]
                    b_y = banana_placement[bi][2]
                    side_im.paste(banana, (b_x, b_y), banana)
        side_by = []
        side_px = side_im.load()
        for y in range(16):
            for x in range(32):
                red_short = (side_px[x, y][0] >> 3) & 31
                green_short = (side_px[x, y][1] >> 3) & 31
                blue_short = (side_px[x, y][2] >> 3) & 31
                alpha_short = 1 if side_px[x, y][3] > 128 else 0
                value = (red_short << 11) | (green_short << 6) | (blue_short << 1) | alpha_short
                side_by.extend([(value >> 8) & 0xFF, value & 0xFF])
        px_data = bytearray(side_by)
        px_data = gzip.compress(px_data, compresslevel=9)
        ROM_COPY.seek(getPointerLocation(TableNames.TexturesGeometry, img))
        ROM_COPY.writeBytes(px_data)


def applyHolidayMode(settings, ROM_COPY: ROM):
    """Change grass texture to snow."""
    HOLIDAY = getHoliday(settings)
    if HOLIDAY == Holidays.no_holiday:
        changeBarrelColor(ROM_COPY)  # Fixes some Krusha stuff
        return
    if HOLIDAY == Holidays.Christmas:
        # Set season to Christmas
        ROM_COPY.seek(settings.rom_data + 0xDB)
        ROM_COPY.writeMultipleBytes(2, 1)
        # Grab Snow texture, transplant it
        ROM_COPY.seek(0x1FF8000)
        snow_im = Image.new(mode="RGBA", size=((32, 32)))
        snow_px = snow_im.load()
        snow_by = []
        for y in range(32):
            for x in range(32):
                rgba_px = int.from_bytes(ROM_COPY.readBytes(2), "big")
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
            start = getPointerLocation(TableNames.TexturesGeometry, img)
            ROM_COPY.seek(start)
            ROM_COPY.writeBytes(byte_data)
        # Alter CI4 Palettes
        start = getPointerLocation(TableNames.TexturesGeometry, 2007)
        mags = [140, 181, 156, 181, 222, 206, 173, 230, 255, 255, 255, 189, 206, 255, 181, 255]
        new_ci4_palette = []
        for mag in mags:
            comp_mag = mag >> 3
            data = (comp_mag << 11) | (comp_mag << 6) | (comp_mag << 1) | 1
            new_ci4_palette.extend([(data >> 8), (data & 0xFF)])
        byte_data = gzip.compress(bytearray(new_ci4_palette), compresslevel=9)
        ROM_COPY.seek(start)
        ROM_COPY.writeBytes(byte_data)
        # Alter rims
        applyCelebrationRims(ROM_COPY, 50, [True, True, True, True, False])
        # Change DK's Tie and Tiny's Hair
        if settings.dk_tie_colors != CharacterColors.custom and settings.kong_model_dk == KongModels.default:
            tie_hang = [0xFF] * 0xAB8
            tie_hang_data = gzip.compress(bytearray(tie_hang), compresslevel=9)
            ROM_COPY.seek(getPointerLocation(TableNames.TexturesGeometry, 0xE8D))
            ROM_COPY.writeBytes(tie_hang_data)
            tie_loop = [0xFF] * (32 * 32 * 2)
            tie_loop_data = gzip.compress(bytearray(tie_loop), compresslevel=9)
            ROM_COPY.seek(getPointerLocation(TableNames.TexturesGeometry, 0x177D))
            ROM_COPY.writeBytes(tie_loop_data)
        if settings.tiny_hair_colors != CharacterColors.custom and settings.kong_model_tiny == KongModels.default:
            tiny_hair = []
            for x in range(32 * 32):
                tiny_hair.extend([0xF8, 0x01])
            tiny_hair_data = gzip.compress(bytearray(tiny_hair), compresslevel=9)
            ROM_COPY.seek(getPointerLocation(TableNames.TexturesGeometry, 0xE68))
            ROM_COPY.writeBytes(tiny_hair_data)
        # Tag Barrel, Bonus Barrel & Transform Barrels
        changeBarrelColor(ROM_COPY, None, (0x00, 0xC0, 0x00))
    elif HOLIDAY == Holidays.Halloween:
        ROM_COPY.seek(settings.rom_data + 0xDB)
        ROM_COPY.writeMultipleBytes(1, 1)
        # Pad Rim
        applyCelebrationRims(ROM_COPY, -12)
        # Tag Barrel, Bonus Barrel & Transform Barrels
        changeBarrelColor(ROM_COPY, (0x00, 0xC0, 0x00))
        # Turn Ice Tomato Orange
        sizes = {
            0x1237: 700,
            0x1238: 1404,
            0x1239: 1372,
            0x123A: 1372,
            0x123B: 692,
            0x123C: 1372,
            0x123D: 1372,
            0x123E: 1372,
            0x123F: 1372,
            0x1240: 1372,
            0x1241: 1404,
        }
        for img in range(0x1237, 0x1241 + 1):
            hueShiftImageContainer(25, img, 1, sizes[img], TextureFormat.RGBA5551, 240)
    elif HOLIDAY == Holidays.Anniv25:
        changeBarrelColor(ROM_COPY, (0xFF, 0xFF, 0x00), None, True)
        sticker_im = getImageFile(ROM_COPY, 25, getBonusSkinOffset(ExtraTextures.Anniv25Sticker), True, 1, 1372, TextureFormat.RGBA5551)
        vanilla_sticker_im = getImageFile(ROM_COPY, 25, 0xB7D, True, 1, 1372, TextureFormat.RGBA5551)
        sticker_im_snipped = sticker_im.crop((0, 0, 1, 1360))
        writeColorImageToROM(sticker_im_snipped, 25, 0xB7D, 1, 1360, False, TextureFormat.RGBA5551, ROM_COPY)
        vanilla_sticker_portion = vanilla_sticker_im.crop((0, 1360, 1, 1372))
        new_im = Image.new(mode="RGBA", size=(1, 1372))
        new_im.paste(sticker_im_snipped, (0, 0), sticker_im_snipped)
        new_im.paste(vanilla_sticker_portion, (0, 1360), vanilla_sticker_portion)
        writeColorImageToROM(new_im, 25, 0x1266, 1, 1372, False, TextureFormat.RGBA5551, ROM_COPY)
        applyCelebrationRims(ROM_COPY, 0, [False, True, True, True, True])
