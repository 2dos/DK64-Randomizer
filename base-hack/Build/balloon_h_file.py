from BuildLib import barrel_skins

disclaimer = [
    "This file is automatically written by base-hack/build/balloon_h_file.py",
    "Please don't alter this c/h file directly as it will get overwritten at next build.",
    "Instead, make changes to the python file.",
    "Thanks,",
    "Ballaam"
]

with open("include/balloon.h", "w") as fh:
    fh.write("/*\n")
    for line in disclaimer:
        fh.write(f"\t{line}\n")
    fh.write("*/\n")
    fh.write("\n")
    for skin in barrel_skins:
        fh.write(f"extern sprite_data_struct balloon_{skin}_sprite;\n")

with open("src/lib_balloon.c", "w") as fh:
    fh.write("/*\n")
    for line in disclaimer:
        fh.write(f"\t{line}\n")
    fh.write("*/\n")
    fh.write("\n")
    fh.write("#include \"../include/common.h\"\n\n")
    for skin_index, skin in enumerate(barrel_skins):
        fh.write(f"sprite_data_struct balloon_{skin}_sprite = {{\n")
        fh.write(f"\t.unk0 = {hex(0xCB + skin_index)},\n")
        fh.write("\t.images_per_frame_horizontal = 1,\n")
        fh.write("\t.images_per_frame_vertical = 1,\n")
        fh.write("\t.codec = RGBA16,\n")
        fh.write("\t.unk8 = -1,\n")
        fh.write("\t.table = TABLE_25,\n")
        fh.write("\t.width = 32,\n")
        fh.write("\t.height = 64,\n")
        fh.write("\t.image_count = 1,\n")
        fh.write(f"\t.images = {{{6026 + (3 * len(barrel_skins)) + skin_index},}}\n")
        fh.write("};\n")