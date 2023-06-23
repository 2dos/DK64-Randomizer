"""Write new Disco Chunky models."""
import os
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames
from BuildLib import ROMName


class Vert:
    """Vertex Information."""

    def __init__(self, coords, rgba, other=[0, 0, 0]):
        """Initialize with given data."""
        offset = [-10, 0, -10]
        new_coords = [0, 0, 0]
        for c_i, c in enumerate(coords):
            new_coords[c_i] = c + offset[c_i]
        self.coords = new_coords
        self.rgba = rgba
        self.other = other


temp_file = "temp.bin"
ins_file = "disco_instrument.bin"

ins_new_verts = [
    Vert([89, -5, -25], 0x128300FF),
    Vert([89, -5, 24], 0x008100FF),
    Vert([85, -1, 24], 0x810000FF),
    Vert([85, -1, -25], 0xC1006DFF),
    Vert([93, -1, -25], 0x7C00E5FF),
    Vert([93, -1, 24], 0x7F0000FF),
    Vert([89, 3, -25], 0x127D00FF),
    Vert([89, 3, 24], 0x007F00FF),
    Vert([81, -5, 28], 0x008100FF),
    Vert([39, -5, 4], 0xED840DFF),
    Vert([41, -1, 0], 0x7F0000FF),
    Vert([83, -1, 24], 0x3F0093FF),
    Vert([79, -1, 32], 0xC1006DFF),
    Vert([37, -1, 7], 0xA40056FF),
    Vert([81, 3, 28], 0x007F00FF),
    Vert([39, 3, 4], 0xED7C0DFF),
    Vert([83, -5, -29], 0xF983F1FF),
    Vert([39, -5, -4], 0xED84F3FF),
    Vert([37, -1, -7], 0xA400AAFF),
    Vert([81, -1, -32], 0xDF0086FF),
    Vert([83, 3, -29], 0xF97DF1FF),
    Vert([39, 3, -4], 0xED7CF3FF),
    Vert([39, 3, 0], 0xDB7900FF),
    Vert([39, -5, 0], 0xDB8700FF),
    Vert([35, -1, 4], 0x85001EFF),
    Vert([90, -1, -33], 0x420094FF),
    Vert([81, -5, 28], 0x6C0041FF),
    Vert([83, -1, 24], 0x6C0041FF),
    Vert([81, 3, 28], 0x6C0041FF),
    Vert([79, -1, 32], 0x6C0041FF),
    Vert([89, -5, 24], 0x00007FFF),
    Vert([93, -1, 24], 0x00007FFF),
    Vert([89, 3, 24], 0x00007FFF),
    Vert([85, -1, 24], 0x00007FFF),
    Vert([39, -5, -4], 0xED84F3FF),
    Vert([35, -1, -4], 0x8500E2FF),
    Vert([37, -1, -7], 0xA400AAFF),
    Vert([90, -1, -33], 0x420094FF),
    Vert([83, 3, -29], 0xF97DF1FF),
    Vert([89, 3, -25], 0x127D00FF),
    Vert([39, 3, -4], 0xED7CF3FF),
    Vert([35, -1, 4], 0x85001EFF),
    Vert([39, 3, 4], 0xED7C0DFF),
    Vert([39, 3, 0], 0xDB7900FF),
    Vert([39, -5, 0], 0xDB8700FF),
    Vert([6, -2, -11], 0x34098DFF),
    Vert([15, -12, -10], 0x42EB97FF),
    Vert([13, -20, -9], 0x46D1A2FF),
    Vert([-8, -2, 0], 0x8BED2BFF),
    Vert([-12, -18, -8], 0x8C09D0FF),
    Vert([-8, -17, 3], 0xB4F764FF),
    Vert([15, -12, 0], 0x66F149FF),
    Vert([10, -2, 0], 0x6C1040FF),
    Vert([9, -19, 6], 0x39E46DFF),
    Vert([0, -19, 6], 0xECCE72FF),
    Vert([0, -2, 11], 0xF0E57AFF),
    Vert([-7, -2, -10], 0xA6EFA9FF),
    Vert([15, -3, -6], 0x4569F2FF),
    Vert([58, -11, -12], 0x6A4500FF),
    Vert([58, -16, -7], 0x611D4BFF),
    Vert([58, -20, -12], 0xCD8C00FF),
    Vert([58, -16, -16], 0x611DB5FF),
    Vert([-3, -16, -16], 0x9FE3B5FF),
    Vert([-3, -20, -12], 0x96BB00FF),
    Vert([-3, -16, -7], 0x9FE34BFF),
    Vert([-3, -11, -12], 0x337400FF),
    Vert([35, -1, 4], 0x00007EFF, [0, 1023, 195]),
    Vert([39, 3, 0], 0xCC7300FF, [0, 1536, 65342]),
    Vert([39, -5, 0], 0x348D00FF, [0, 512, 65339]),
    Vert([35, -1, -4], 0x000082FF, [0, 2049, 196]),
    Vert([39, -5, 0], 0x348D00FF, [0, 2560, 65339]),
    Vert([13, -15, -1], 0xCC7300FF, [0, 1536, 2500]),
    Vert([11, -19, 2], 0x00007EFF, [0, 1024, 2612]),
    Vert([10, -23, -1], 0x348D00FF, [0, 512, 2711]),
    Vert([11, -19, -5], 0x000082FF, [0, 2048, 2612]),
    Vert([10, -23, -1], 0x348D00FF, [0, 2560, 2711]),
]

ins_new_dl = [
    """
        E7 00 00 00 00 00 00 00
        E2 00 00 1C 00 55 20 78
        D7 00 00 02 08 00 08 00
        FD 10 00 00 00 00 0E BF
        E6 00 00 00 00 00 00 00
        F3 00 00 00 07 3F F1 00
        E7 00 00 00 00 00 00 00
        E3 00 10 01 00 00 00 00
        F5 10 10 00 00 01 40 50
        DE 00 00 00 05 00 00 00
        D9 FF FF FF 00 06 00 00
        DA 38 00 03 04 00 01 C0
        01 01 E0 3C 03 00 38 C0
        06 00 02 04 00 00 04 06
        06 02 00 08 00 02 08 0A
        06 0A 08 0C 00 0A 0C 0E
        06 06 04 0E 00 06 0E 0C
        06 10 12 14 00 10 14 16
        06 12 10 18 00 12 18 1A
        06 1A 18 1C 00 1A 1C 1E
        06 16 14 1E 00 16 1E 1C
        06 20 22 24 00 20 24 26
        06 22 20 06 00 22 06 14
        06 14 06 28 00 14 28 2A
        06 26 24 2A 00 26 2A 28
        06 2A 2C 1E 00 2A 1E 14
        06 14 12 2E 00 14 2E 22
        06 30 1A 1E 00 12 1A 30
        06 00 06 20 00 28 06 0C
        06 32 08 00 00 32 26 28
        06 32 20 26 00 32 00 20
        06 12 30 2E 00 08 32 0C
        06 34 36 38 00 34 38 3A
        01 00 F0 1E 03 00 3A A0
        06 00 02 04 00 00 04 06
        06 08 0A 0C 00 0E 10 12
        06 14 0C 0A 00 16 18 1A
        06 1A 14 0A 00 1C 0A 08
    """,
    """
        E7 00 00 00 00 00 00 00
        E3 00 0A 01 00 10 00 00
        E2 00 00 1C 0C 19 20 78
        FC 26 A0 04 1F 10 93 FF
        E3 00 0F 00 00 01 00 00
        D7 00 28 02 FF FF FF FF
        FD 10 00 00 00 00 0D 09
        E6 00 00 00 00 00 00 00
        F3 00 00 00 07 55 B0 00
        E7 00 00 00 00 00 00 00
        E3 00 10 01 00 00 00 00
        F2 00 20 02 00 07 E0 7E
        F5 10 09 00 01 01 04 41
        F5 10 05 40 02 00 C8 32
        F5 10 03 50 03 00 8C 23
        F5 10 03 54 04 00 50 14
        F5 10 03 56 05 00 14 05
        D9 FB FF FF 00 00 00 00
        DA 38 00 03 04 00 01 80
        01 00 50 16 03 00 3D 30
        DA 38 00 03 04 00 01 C0
        01 00 50 0A 03 00 3C E0
        06 00 02 0C 00 00 0C 0E
        06 04 00 0E 00 04 0E 10
        06 02 06 12 00 02 12 0C
        06 06 08 14 00 06 14 12
        D9 FD FF FF 00 00 00 00
        DF 00 00 00 00 00 00 00
    """,
]

beater_new_dl = """
    01 01 50 2A 03 00 3B 90
    FD 10 00 00 00 00 0E BF
    06 1A 1C 1E 00 1A 1E 20
    06 22 24 26 00 22 26 28
    06 1A 20 22 00 1A 22 28
    06 20 1E 24 00 20 24 22
    06 1E 1C 26 00 1E 26 24
    06 1C 1A 28 00 1C 28 26
"""

# beater_new_dl = """
#     E7 00 00 00 00 00 00 00
#     01 01 50 2A 03 00 3B 90
#     FD 10 00 00 00 00 0E BF
#     E6 00 00 00 00 00 00 00
#     F3 00 00 00 07 3F F1 00
#     E7 00 00 00 00 00 00 00
#     E3 00 10 01 00 00 00 00
#     06 1A 1C 1E 00 1A 1E 20
#     06 22 24 26 00 22 26 28
#     06 1A 20 22 00 1A 22 28
#     06 20 1E 24 00 20 24 22
#     06 1E 1C 26 00 1E 26 24
#     06 1C 1A 28 00 1C 28 26
# """

with open(ROMName, "rb") as rom:
    disco_f = ROMPointerFile(rom, TableNames.ActorGeometry, 0xD)
    rom.seek(disco_f.start)
    disco_data = zlib.decompress(rom.read(disco_f.size), (15 + 32))
    vert_end = 0x38E8
    dl_end = 0x58B8
    # Disco Chunky + Instrument
    with open(ins_file, "wb") as fh:
        fh.write(disco_data)
    with open(ins_file, "rb") as fh:
        # Verts
        fh.seek(0x28)
        vert_data = fh.read(vert_end - 0x28)
        with open(temp_file, "wb") as fg:
            fg.write(vert_data)
            for vert_block in ins_new_verts:
                # Vert Blocks:
                # 0x38C0 - 0x1E
                # 0x3AA0 - 0x0F
                # 0x3B90 - 0x15
                # 0x3CE0 - 0x05
                for c in vert_block.coords:
                    if c < 0:
                        c += 65536
                    fg.write(c.to_bytes(2, "big"))
                for o in vert_block.other:
                    fg.write(o.to_bytes(2, "big"))
                fg.write(vert_block.rgba.to_bytes(4, "big"))
        with open(temp_file, "rb") as fg:
            vert_data = fg.read()
        # Display Lists
        fh.seek(vert_end)
        dl_mid = 0x4800
        dl_data = b""
        dl_data_0 = fh.read(dl_mid - vert_end)
        dl_data_1 = fh.read(dl_end - dl_mid)
        with open(temp_file, "wb") as fg:
            fg.write(dl_data_0)
            # for dl_block in beater_new_dl:
            #     fix_arr = dl_block.split("\n")
            #     fix_lst = []
            #     for f in fix_arr:
            #         if not f == "":
            #             for x in f.strip().split(" "):
            #                 if x.strip() != "":
            #                     fix_lst.append(int(f"0x{x}", 16))
            #     fg.write(bytearray(fix_lst))
            fg.write(dl_data_1)
            pos = fg.tell()
            fg.seek(pos - 8)
            for dl_block in ins_new_dl:
                fix_arr = dl_block.split("\n")
                fix_lst = []
                for f in fix_arr:
                    if not f == "":
                        for x in f.strip().split(" "):
                            if x.strip() != "":
                                fix_lst.append(int(f"0x{x}", 16))
                fg.write(bytearray(fix_lst))
        with open(temp_file, "rb") as fg:
            dl_data = fg.read()
        fh.seek(dl_end + 4)
        other_data = fh.read()
        fh.seek(0x14)
        header_data = fh.read(0x28 - 0x14)
        with open(temp_file, "wb") as fg:
            base = 0x10001080
            fg.write(base.to_bytes(4, "big"))
            fg.write((base + len(vert_data) + len(dl_data)).to_bytes(4, "big"))
            fg.write((base + len(vert_data) + len(dl_data) + 4).to_bytes(4, "big"))
            fg.write((base + len(vert_data) + len(dl_data) + 0x174).to_bytes(4, "big"))
            fg.write((base + len(vert_data) + len(dl_data) + 0x32C).to_bytes(4, "big"))
            fg.write(header_data)
            fg.write(vert_data)
            fg.write(dl_data)
            fg.write((base + len(vert_data)).to_bytes(4, "big"))
            fg.write(other_data)
    with open(temp_file, "rb") as fg:
        with open(ins_file, "wb") as fh:
            fh.write(fg.read())
    if os.path.exists(temp_file):
        os.remove(temp_file)
