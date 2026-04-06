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
    fh.write(f"extern const sprite_data_struct_single balloon_sprites[{len(barrel_skins)}];\n")

with open("src/lib_balloon.c", "w") as fh:
    fh.write("/*\n")
    for line in disclaimer:
        fh.write(f"\t{line}\n")
    fh.write("*/\n")
    fh.write("\n")
    fh.write("#include \"../include/common.h\"\n\n")
    fh.write("ROM_RODATA_NUM const sprite_data_struct_single balloon_sprites[" + str(len(barrel_skins)) + "] = {\n")
    for skin_index, skin in enumerate(barrel_skins):
        fh.write("\t{ // " + skin + "\n")
        fh.write(f"\t\t.unk0 = {hex(0xD0 + skin_index)},\n")
        fh.write("\t\t.images_per_frame_horizontal = 1,\n")
        fh.write("\t\t.images_per_frame_vertical = 1,\n")
        fh.write("\t\t.codec = RGBA16,\n")
        fh.write("\t\t.unk8 = -1,\n")
        fh.write("\t\t.table = TABLE_25,\n")
        fh.write("\t\t.width = 32,\n")
        fh.write("\t\t.height = 64,\n")
        fh.write("\t\t.image_count = 1,\n")
        fh.write(f"\t\t.image = {6026 + (3 * len(barrel_skins)) + skin_index},\n")
        fh.write("\t},\n")
    fh.write("};\n")