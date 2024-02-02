"""Pull instruments and guns from kong models."""

import zlib
from BuildLib import ROMName, MODEL_DIRECTORY
from BuildEnums import TableNames
from BuildClasses import PointerFile, ROMPointerFile, TableEntry, pointer_tables
from model_port import portalModel_Actor

TEMP_FILE = "temp.bin"
BASE_ACTOR = [
    0xE7,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0xE3,
    0x00,
    0x0A,
    0x01,
    0x00,
    0x00,
    0x00,
    0x00,
    0xE2,
    0x00,
    0x00,
    0x1C,
    0x00,
    0x55,
    0x20,
    0x78,
    0xFC,
    0x11,
    0x96,
    0x23,
    0xFF,
    0x2F,
    0xFF,
    0xFF,
    0xE3,
    0x00,
    0x0F,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0xD7,
    0x00,
    0x00,
    0x02,
    0x08,
    0x00,
    0x08,
    0x00,
]


def getSubmodel(model_index: int, dl_info: list, model_name: str):
    """Get submodel from actor model."""
    with open(ROMName, "rb") as rom:
        kong_model = ROMPointerFile(rom, TableNames.ActorGeometry, model_index)
        rom.seek(kong_model.start)
        data = zlib.decompress(rom.read(kong_model.size), (15 + 32))
        with open(TEMP_FILE, "wb") as fh:
            fh.write(data)
        with open(TEMP_FILE, "r+b") as fh:
            with open(f"{MODEL_DIRECTORY}{model_name}.vtx", "wb") as vtx:
                with open(f"{MODEL_DIRECTORY}{model_name}.dl", "wb") as dl:
                    # for x in BASE_ACTOR:
                    #     dl.write(x.to_bytes(1, "big"))
                    vert_transplant = []
                    vert_loc = 0
                    DL_COPY_SIZE = 8
                    VERT_COPY_SIZE = 2
                    SCALE_FACTOR = 10
                    for x in dl_info:
                        diff = x[1] - x[0]
                        for y in range(int((diff) / 8)):
                            instruction_start = x[0] + (y * 8)
                            fh.seek(instruction_start)
                            command = int.from_bytes(fh.read(1), "big")
                            if command == 1:
                                fh.seek(instruction_start + 1)
                                loaded_vert_count = int.from_bytes(fh.read(2), "big") >> 4
                                loaded_vert_count = 32
                                fh.seek(instruction_start + 6)
                                loaded_vert_start = int(int.from_bytes(fh.read(2), "big") / 0x10)
                                fh.seek(instruction_start + 6)
                                fh.write((vert_loc * 0x10).to_bytes(2, "big"))
                                vert_transplant.append([loaded_vert_start, loaded_vert_count])
                                vert_loc += loaded_vert_count
                        for y in range(int(diff / DL_COPY_SIZE)):
                            fh.seek(x[0] + (y * DL_COPY_SIZE))
                            command = int.from_bytes(fh.read(1), "big")
                            if command != 0xDA:
                                fh.seek(x[0] + (y * DL_COPY_SIZE))
                                dl.write(fh.read(DL_COPY_SIZE))
                        dl.write((0xDF << 24).to_bytes(4, "big"))
                        dl.write((0).to_bytes(4, "big"))
                    for x in vert_transplant:
                        fh.seek(0x28 + (x[0] * 0x10))
                        for y in range(int((x[1] * 0x10) / VERT_COPY_SIZE)):
                            in_vert = y % 8
                            read = fh.read(VERT_COPY_SIZE)
                            if in_vert < 3:
                                coord = int.from_bytes(read, "big")
                                if coord & 0x8000:
                                    coord -= 65536
                                coord *= SCALE_FACTOR
                                if coord < 0:
                                    coord += 65536
                                read = coord.to_bytes(2, "big")
                            vtx.write(read)
    portalModel_Actor(f"{MODEL_DIRECTORY}{model_name}.vtx", f"{MODEL_DIRECTORY}{model_name}.dl", model_name, 0xB8)


def pullHandModels():
    """Get hand model."""
    getSubmodel(1, [[0x3A98, 0x3E28]], "guitar")
