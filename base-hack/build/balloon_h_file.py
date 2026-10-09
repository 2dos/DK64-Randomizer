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
    fh.write(f"#define BALLOON_IMAGE_START {6026 + (3 * len(barrel_skins))}\n")