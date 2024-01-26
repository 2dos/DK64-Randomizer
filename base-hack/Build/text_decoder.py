"""Decode text file into arrays of text items."""

import os
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import Icons, TableNames
from BuildLib import ROMName

temp_file = "decodedtext.bin"


def grabText(file_index: int) -> list:
    """Pull text from ROM with a particular file index."""
    with open(ROMName, "rb") as fh:
        text_file = ROMPointerFile(fh, TableNames.Text, file_index)
        fh.seek(text_file.start)
        with open(temp_file, "wb") as fg:
            if text_file.compressed:
                fg.write(zlib.decompress(fh.read(text_file.size), (15 + 32)))
            else:
                fg.write(fh.read(text_file.size))

    with open(temp_file, "rb") as fh:
        fh.seek(0)
        count = int.from_bytes(fh.read(1), "big")
        text = []
        text_data = []
        text_start = (count * 0xF) + 3
        data_start = 1
        for i in range(count):
            fh.seek(data_start)
            section_1_count = int.from_bytes(fh.read(1), "big")
            section_2_count = int.from_bytes(fh.read(1), "big")
            section_3_count = int.from_bytes(fh.read(1), "big")
            # print(str(section_1_count) + " > " + str(section_2_count) + " > " + str(section_3_count))
            fh.seek(data_start + 5)
            start = int.from_bytes(fh.read(2), "big")
            size = int.from_bytes(fh.read(2), "big")
            block_start = 1
            blocks = []
            for k in range(section_1_count):
                fh.seek(data_start + block_start)
                sec2ct = int.from_bytes(fh.read(1), "big")
                offset = 0
                if (sec2ct & 4) != 0:
                    # print("Adding offset")
                    offset += 4
                text_blocks = []
                if (sec2ct & 1) == 0:
                    if (sec2ct & 2) != 0:
                        fh.seek(data_start + block_start + offset + 1)
                        sec3ct = int.from_bytes(fh.read(1), "big")
                        for j in range(sec3ct):
                            _block = block_start + 2 + offset + (4 * j) - 1
                            fh.seek(data_start + _block)
                            _pos = int.from_bytes(fh.read(2), "big")
                            fh.seek(data_start + _block)
                            _dat = int.from_bytes(fh.read(4), "big")
                            text_blocks.append({"type": "sprite", "position": _pos, "data": hex(_dat), "sprite": Icons((_dat >> 8) & 0xFF)})
                        added = block_start + 2 + offset + (4 * sec3ct) + 4
                else:
                    fh.seek(data_start + block_start + offset + 1)
                    sec3ct = int.from_bytes(fh.read(1), "big")
                    for j in range(sec3ct):
                        _block = block_start + 2 + offset + (8 * j) - 1
                        fh.seek(data_start + _block + 3)
                        _start = int.from_bytes(fh.read(2), "big")
                        fh.seek(data_start + _block + 5)
                        _size = int.from_bytes(fh.read(2), "big")
                        text_blocks.append({"type": "normal", "start": _start, "size": _size})
                    added = block_start + 2 + offset + (8 * sec3ct) + 4
                blocks.append({"block_start": hex(block_start + data_start), "section2count": sec2ct, "section3count": sec3ct, "offset": offset, "text": text_blocks})
                block_start = added
            fh.seek(data_start)
            if added < data_start:
                info = b""
            else:
                info = fh.read(added - data_start)
            text_data.append({"arr": info, "text": blocks, "section1count": section_1_count, "section2count": section_2_count, "section3count": section_3_count, "data_start": hex(data_start)})
            text_start += added - data_start
            data_start += block_start
        for item in text_data:
            text_block = []
            # print(item)
            for item2 in item["text"]:
                # print(item2)
                temp = []
                for item3 in item2["text"]:
                    if item3["type"] == "normal":
                        start = item3["start"] + data_start + 2
                        # print(hex(start))
                        end = start + item3["size"]
                        fh.seek(start)
                        temp.append(fh.read(item3["size"]).decode())
                    elif item3["type"] == "sprite":
                        temp.append(item3["sprite"])
                        # print(fh.read(item3["size"]))
                text_block.append(temp)
            text.append(text_block)
    if os.path.exists(temp_file):
        os.remove(temp_file)
    formatted_text = []
    for t in text:
        y = []
        for x in t:
            y.append({"text": x})
        formatted_text.append(y)
    return formatted_text
