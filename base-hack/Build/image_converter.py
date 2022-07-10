"""Convert PNG to RGBA32 binary."""
from PIL import Image


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
