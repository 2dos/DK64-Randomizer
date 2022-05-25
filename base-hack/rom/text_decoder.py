"""Decode text file into arrays of text items."""

with open("1114DD6_ZLib.bin", "rb") as fh:
    fh.seek(0)
    count = int.from_bytes(fh.read(1), "big")
    print(count)
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
                        text_blocks.append(
                            {
                                "type": "unk",
                                "position": _pos,
                                "data": hex(_dat),
                            }
                        )
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
                    text_blocks.append(
                        {
                            "type": "normal",
                            "start": _start,
                            "size": _size,
                        }
                    )
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
                    # print(fh.read(item3["size"]))
            text_block.append(temp)
        text.append(text_block)
    text_idx = 0
    for t in text:
        print(f"[{text_idx}] - {t}")
        text_idx += 1
