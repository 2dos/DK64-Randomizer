"""Library functions for the build procedure."""

import struct
from PIL import Image
import math

main_pointer_table_offset = 0x101C50
BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something
ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"
finalROM = "rom/dk64-randomizer-base-dev.z64"
music_size = 24000
heap_size = 0x34000 + music_size
flut_size = 0
MODEL_DIRECTORY = "assets/models/"
KONG_MODEL_EXP_SIZE = 0x5000

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


def imageToMinMap(img_path: str):
    """Convert an image to a min map rgba5551 texture."""
    mode = 3
    out_name = img_path.replace(".png", "_mipped.png")

    with open(img_path, "rb") as file:
        pi = Image.open(file)
        pi = pi.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((32, 32))
        dims = pi.size

        # mipmapping occurs for every 8-byte block, so this is 8 divided by bytesPerPixel.
        # for RGBA5551, bPP is 2
        pixelsPerBlock = 4

        match mode:
            case 0:
                # scramble/unscramble
                out = Image.new(mode="RGBA", size=dims)
                for y in range(dims[1]):
                    for x in range(dims[0]):
                        curpx = pi.getpixel((x, y))
                        newX = x
                        if y % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newX = x - floor(pixelsPerBlock / 2)
                            else:
                                newX = x + floor(pixelsPerBlock / 2)
                        out.putpixel((newX, y), curpx)
                out.save(f"unmipped_{file.name}")
            case 1:
                # break mipmapped textures into parts (parts are also unscrambled for good measure)
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, targetWidth))
                for y in range(dims[1]):
                    for x in range(dims[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {targetWidth}^2")
                            out.save(f"{targetWidth}_{file.name}")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            out = Image.new(mode="RGBA", size=(targetWidth, targetWidth))
                            pixelsWrittenSoFar = 0
                        curpx = pi.getpixel((x, y))
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newX = newX - floor(pixelsPerBlock / 2)
                            else:
                                newX = newX + floor(pixelsPerBlock / 2)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        out.putpixel((newX, newY), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break
            case 2:
                # assembles mipped texture from a series of images, READY TO PLACE INTO ROM
                # if in.png is the input file at 32x32, it stitches 32_in.png, 16_in.png, 8_in.png and 4_in.png together
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                # also theres like a 99 percent chance that this formula breaks with images that arent 32x32
                outY = int(targetWidth + targetWidth / 4 + targetWidth / 8)
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, outY))
                current_in = Image.open(open(f"{targetWidth}_in.png", "rb"))
                for y in range(out.size[1]):
                    for x in range(out.size[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {targetWidth}^2 image")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            current_in = Image.open(open(f"{targetWidth}_in.png", "rb"))
                            pixelsWrittenSoFar = 0
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        curpx = current_in.getpixel((newX, newY))
                        newerX = x
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newerX = x - floor(pixelsPerBlock / 2)
                            else:
                                newerX = x + floor(pixelsPerBlock / 2)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        out.putpixel((newerX, y), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break
                out.save(f"assembled_{file.name}")
            case 3:
                # take a 32x32 and mipmap it 4 times, READY TO PLACE INTO ROM
                # might work with other dimensions, not sure yet tbh
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                # also theres like a 99 percent chance that this formula breaks with images that arent 32x32
                outY = int(targetWidth + targetWidth / 4 + targetWidth / 8)
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, outY))
                for y in range(out.size[1]):
                    for x in range(out.size[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {tar}^2, shrinking")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            pi.thumbnail((targetWidth, targetWidth))
                            pixelsWrittenSoFar = 0
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        curpx = pi.getpixel((newX, newY))
                        newerX = x
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newerX = x - math.floor(pixelsPerBlock / 2)
                            else:
                                newerX = x + math.floor(pixelsPerBlock / 2)
                        out.putpixel((newerX, y), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break

                out.save(out_name)
            case _:
                print("unknown mode")
