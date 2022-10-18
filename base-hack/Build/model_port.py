"""Port models to actors and model two objects, based on inputs of vertices and a display list."""

import zlib
import os

rom_file = "rom/dk64.z64"
temp_file = "temp.bin"
ptr_offset = 0x101C50
m2_table = 4
ac_table = 5

# Conversions:
# Load vertices Seg Start:
# - Actor: 0x3
# - M2: 0x8
# G_MTX:
# - Actor: 0x4
# - M2: 0x9


def portalModel_M2(vtx_file, dl_file, overlay_dl_file, model_name, base):
    """Convert model two model file from various source files."""
    with open(rom_file, "rb") as rom:
        rom.seek(ptr_offset + (m2_table * 4))
        table = ptr_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        size = finish - start
        rom.seek(start)
        data = rom.read(size)
        rom.seek(start)
        indic = int.from_bytes(rom.read(2), "big")
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(temp_file, "wb") as fh:
            fh.write(data)
    with open(temp_file, "rb") as fh:
        with open(f"{model_name}_om2.bin", "wb") as fg:
            fh.seek(0x40)
            dl_start = int.from_bytes(fh.read(4), "big")
            fh.seek(0)
            head = fh.read(dl_start)
            fg.write(head)
            dl_data_length = 0
            with open(dl_file, "rb") as dl:
                dl_data = dl.read()
                dl_data_length = len(dl_data)
                fg.write(dl_data)
            dl_addon_length = 0
            if overlay_dl_file != 0:
                with open(overlay_dl_file, "rb") as dl:
                    dl_addon = dl.read()
                    dl_addon_length = len(dl_addon)
                    fg.write(dl_addon)
            else:
                dl_addon_length = 8
                fg.write((0xDF << 56).to_bytes(8, "big"))
            vtx_data_length = 0
            with open(vtx_file, "rb") as vtx:
                vtx_data = vtx.read()
                vtx_data_length = len(vtx_data)
                fg.write(vtx_data)
            fh.seek(0x4C)
            file_extra_data_start = int.from_bytes(fh.read(4), "big")
            fh.seek(file_extra_data_start)
            file_extra_data = fh.read()
            fg.write(file_extra_data)
            fg.seek(0x44)
            pointer = dl_start + dl_data_length
            fg.write(pointer.to_bytes(4, "big"))
            pointer += dl_addon_length
            fg.write(pointer.to_bytes(4, "big"))
            pointer += vtx_data_length
            fh.seek(0x4C)
            old = int.from_bytes(fh.read(4), "big")
            fg.write(pointer.to_bytes(4, "big"))
            diff = pointer - old
            iterations = int(((dl_start - 1) - 0x50) / 4)
            for i in range(iterations):
                old = int.from_bytes(fh.read(4), "big")
                fg.write((old + diff).to_bytes(4, "big"))
    if os.path.exists(temp_file):
        os.remove(temp_file)


def portalModel_Actor(vtx_file, dl_file, model_name, base):
    """Create actor file from various source files."""
    with open(rom_file, "rb") as rom:
        rom.seek(ptr_offset + (ac_table * 4))
        table = ptr_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        size = finish - start
        rom.seek(start)
        data = rom.read(size)
        rom.seek(start)
        indic = int.from_bytes(rom.read(2), "big")
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(temp_file, "wb") as fh:
            fh.write(data)
    with open(temp_file, "rb") as fh:
        with open(f"{model_name}_om1.bin", "wb") as fg:
            fg.write(fh.read(0x28))  # Head
            vtx_len = 0
            with open(vtx_file, "rb") as vtx:
                vtx_data = vtx.read()
                vtx_len = len(vtx_data)
                fg.write(vtx_data)
            dl_len = 0
            with open(dl_file, "rb") as dl:
                dl_data = dl.read()[0x30:]
                dl_len = len(dl_data)
                fg.write(dl_data)
            fh.seek(0)
            init_ptr = int.from_bytes(fh.read(4), "big")
            init_dl_end_ptr = int.from_bytes(fh.read(4), "big")
            dl_end = fg.tell()
            fg.seek(4)
            dl_end_ptr = dl_end + init_ptr - 0x28
            fg.write(dl_end_ptr.to_bytes(4, "big"))
            diff = dl_end_ptr - init_dl_end_ptr
            for i in range(3):
                old = int.from_bytes(fh.read(4), "big")
                fg.write((old + diff).to_bytes(4, "big"))
            fg.seek(dl_end)
            fg.write((init_ptr + vtx_len).to_bytes(4, "big"))
            fh.seek(init_dl_end_ptr + 0x2C - init_ptr)
            fg.write(fh.read())
    if os.path.exists(temp_file):
        os.remove(temp_file)


model_dir = "assets/Non-Code/models/"
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}nin_coin.dl", f"{model_dir}coin_overlay.dl", "nintendo_coin", 0x90)
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}rw_coin.dl", f"{model_dir}coin_overlay.dl", "rareware_coin", 0x90)
portalModel_M2(f"{model_dir}potion_dk.vtx", f"{model_dir}potion.dl", 0, "potion_dk", 0x90)
portalModel_M2(f"{model_dir}potion_diddy.vtx", f"{model_dir}potion.dl", 0, "potion_diddy", 0x90)
portalModel_M2(f"{model_dir}potion_lanky.vtx", f"{model_dir}potion.dl", 0, "potion_lanky", 0x90)
portalModel_M2(f"{model_dir}potion_tiny.vtx", f"{model_dir}potion.dl", 0, "potion_tiny", 0x90)
portalModel_M2(f"{model_dir}potion_chunky.vtx", f"{model_dir}potion.dl", 0, "potion_chunky", 0x90)
portalModel_M2(f"{model_dir}potion_any.vtx", f"{model_dir}potion.dl", 0, "potion_any", 0x90)
# portalModel_Actor(f"{model_dir}coin.vtx", f"{model_dir}nin_coin.dl", "nintendo_coin", 0x66)
