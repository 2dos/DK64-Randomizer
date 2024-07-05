"""Get a series of skeleton images from a model, great for analysis with model work."""

from BuildLib import main_pointer_table_offset, intf_to_float
from BuildEnums import TableNames
import zlib
import os
from PIL import Image, ImageDraw, ImageFont


def getSkeleton(model_index: int, model_file: str = None):
    """Obtain Skeleton."""
    if model_file is None:
        with open("../rom/dk64.z64", "rb") as rom:
            rom.seek(main_pointer_table_offset + (TableNames.ActorGeometry * 4))
            actor_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")

            rom.seek(actor_table + (model_index << 2))
            model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
            model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
            model_size = model_end - model_start
            rom.seek(model_start)
            model_data = zlib.decompress(rom.read(model_size), (15 + 32))
            with open("temp_skeleton.bin", "wb") as fh:
                fh.write(model_data)
    opened_file = "temp_skeleton.bin"
    if model_file is not None:
        opened_file = model_file
    with open(opened_file, "rb") as fh:
        offset = int.from_bytes(fh.read(4), "big")
        fh.seek(8)
        bone_start = (int.from_bytes(fh.read(4), "big") + 0x28) - offset
        fh.seek(0x20)
        bone_count = int.from_bytes(fh.read(1), "big")
        bone_offsets = [None] * bone_count
        bone_master = [0] * bone_count
        bone_bases = []
        for b in range(bone_count):
            bone_offsets.append([0, 0, 0])  # Same ^
            bone_bases.append([0, 0, 0])  # Same ^
        # Grab Bones
        connections = []
        for b in range(bone_count):
            fh.seek(bone_start + (b * 0x10))
            base_bone = int.from_bytes(fh.read(1), "big")
            local_bone = int.from_bytes(fh.read(1), "big")
            master_bone = int.from_bytes(fh.read(1), "big")
            coords = [0, 0, 0]
            if base_bone != 0xFF:
                coords = bone_offsets[base_bone].copy()
            fh.seek(bone_start + (b * 0x10) + 4)
            for c in range(3):
                value = intf_to_float(int.from_bytes(fh.read(4), "big"))
                if base_bone == 8:
                    print(model_index, value)
                coords[c] += value
            bone_offsets[local_bone] = coords.copy()
            bone_bases[master_bone] = coords.copy()
            bone_master[local_bone] = master_bone
            if base_bone != 0xFF and local_bone != 0xFF:
                connections.append([base_bone, local_bone])
        scale = 3
        points = [(x[0] + 250, 250 - x[1]) for x in bone_offsets]
        points = [(x[0] * scale, x[1] * scale) for x in points]

        image = Image.new("RGB", (500 * scale, 500 * scale), "white")
        draw = ImageDraw.Draw(image)

        # Define font and font size
        font = ImageFont.load_default()

        text_draw_positions = []

        # Draw points and numbers
        disable_overlap = True
        for i, (x, y) in enumerate(points, 0):
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill="black")  # Draw point
            text_x = x + 5
            text_y = y - 5
            while True:
                in_range_of_other = False
                for z in text_draw_positions:
                    dx = text_x - z[0]
                    dy = text_y - z[1]
                    d = (dx * dx) + (dy * dy)
                    if d < 100:
                        in_range_of_other = disable_overlap
                if in_range_of_other:
                    text_y -= 10
                else:
                    break
            text_draw_positions.append((text_x, text_y))
            draw.text((text_x, text_y), str(i), font=font, fill="black")  # Draw number
        for i in connections:
            draw.line([points[i[0]], points[i[1]]], fill="black", width=2)

        # Save or display the image
        if not os.path.exists("./skeleton/"):
            os.mkdir("./skeleton/")
        file_name = f"./skeleton/model_{hex(model_index)}.png"
        if model_file is not None:
            file_name = f"./skeleton/model_{model_file.replace('.bin','').replace('../','')}.png"
        image.save(file_name)


getSkeleton(3)
getSkeleton(0x10)
getSkeleton(0x48)
getSkeleton(0x67)
getSkeleton(0xDA)
getSkeleton(8)
getSkeleton(0x12)
getSkeleton(0x11)
