from typing import BinaryIO

kong_colors = {
    "dk": (0xFF, 0xD7, 0x00),
    "diddy": (0xFF, 0x00, 0x00),
    "lanky": (0x16, 0x99, 0xFF),
    "tiny": (0xB0, 0x45, 0xFF),
    "chunky": (0x41, 0xFF, 0x25),
    "any": (0xFF, 0xFF, 0xFF),
}

POT_Y_BOTTOM = 0
POT_Y_MIDDLE = 73
POT_Y_TOP = 128
POT_H_FAR = 54
POT_H_NEAR = 19
POT_COLOR_STRENGTHS = (
    0x70,  # Vanilla: 0x47
    0x9F,
    0xDE,
    0xEB,
)


class Vtx:
    def __init__(self, x: int, y: int, z: int, color_strength: int, alpha: int = 0xFF, forced_color: tuple = None):
        self.x = x
        self.y = y
        self.z = z
        self.color_strength = color_strength
        self.alpha = alpha
        self.forced_color = forced_color

    def writeVtx(self, fh: BinaryIO, color: tuple):
        output_color = None
        if self.forced_color is not None:
            output_color = self.forced_color
        else:
            strength = self.color_strength / POT_COLOR_STRENGTHS[3]  # Max strength
            output_color = []
            for x in range(3):
                channel = int(color[x] * strength)
                output_color.append(channel)
        if len(output_color) != 3:
            raise Exception("Invalid color channel count")
        ux = self.x if self.x >= 0 else 65536 + self.x
        uy = self.y if self.y >= 0 else 65536 + self.y
        uz = self.z if self.z >= 0 else 65536 + self.z
        fh.write(ux.to_bytes(2, "big"))
        fh.write(uy.to_bytes(2, "big"))
        fh.write(uz.to_bytes(2, "big"))
        for _ in range(3):
            fh.write((0).to_bytes(2, "big"))
        for channel in output_color:
            fh.write(channel.to_bytes(1, "big"))
        fh.write(self.alpha.to_bytes(1, "big"))


vertex_information = [
    Vtx(0, POT_Y_BOTTOM, -POT_H_FAR, POT_COLOR_STRENGTHS[2]),
    Vtx(POT_H_FAR, POT_Y_BOTTOM, 0, POT_COLOR_STRENGTHS[0]),
    Vtx(0, POT_Y_BOTTOM, POT_H_FAR, POT_COLOR_STRENGTHS[0]),
    Vtx(0, POT_Y_MIDDLE, -POT_H_NEAR, POT_COLOR_STRENGTHS[3]),
    Vtx(-POT_H_NEAR, POT_Y_MIDDLE, 0, POT_COLOR_STRENGTHS[3]),
    Vtx(0, POT_Y_MIDDLE, POT_H_NEAR, POT_COLOR_STRENGTHS[3]),
    Vtx(0, POT_Y_MIDDLE, -POT_H_NEAR, POT_COLOR_STRENGTHS[2]),
    Vtx(-POT_H_FAR, POT_Y_BOTTOM, 0, POT_COLOR_STRENGTHS[0]),
    Vtx(-POT_H_NEAR, POT_Y_MIDDLE, 0, POT_COLOR_STRENGTHS[1]),
    Vtx(0, POT_Y_MIDDLE, POT_H_NEAR, POT_COLOR_STRENGTHS[1]),
    Vtx(POT_H_NEAR, POT_Y_MIDDLE, 0, POT_COLOR_STRENGTHS[1]),
    Vtx(POT_H_NEAR, POT_Y_MIDDLE, 0, POT_COLOR_STRENGTHS[3]),
    Vtx(0, POT_Y_TOP, -POT_H_NEAR, 0xFF, 0x66, (0xFF, 0xFF, 0xFF)),
    Vtx(0, POT_Y_MIDDLE, -POT_H_NEAR, 0xFF, 0x66, (0x97, 0xCD, 0xCD)),
    Vtx(-POT_H_NEAR, POT_Y_MIDDLE, 0, 0xFF, 0x66, (0x78, 0xB9, 0xAF)),
    Vtx(POT_H_NEAR, POT_Y_TOP, 0, 0xFF, 0x66, (0x78, 0xB9, 0xAF)),
    Vtx(POT_H_NEAR, POT_Y_MIDDLE, 0, 0xFF, 0x66, (0x78, 0xB9, 0xAF)),
    Vtx(0, POT_Y_TOP, POT_H_NEAR, 0xFF, 0x66, (0x49, 0x71, 0x6B)),
    Vtx(0, POT_Y_MIDDLE, POT_H_NEAR, 0xFF, 0x66, (0x49, 0x71, 0x6B)),
    Vtx(-POT_H_NEAR, POT_Y_TOP, 0, 0xFF, 0x66, (0x78, 0xB9, 0xAF)),
]

for kong_name, color in kong_colors.items():
    with open(f"../assets/models/potion_{kong_name}.vtx", "wb") as fh:
        for v in vertex_information:
            v.writeVtx(fh, color)
