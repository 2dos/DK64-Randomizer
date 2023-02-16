"""Encode text file to ROM."""
from BuildLib import float_to_hex, icon_db


def writeText(file_name, text):
    """Write the text to ROM."""
    print(f"Writing Text File: {file_name}")
    with open(file_name, "wb") as fh:
        fh.write(bytearray([len(text)]))
        position = 0
        for textbox in text:
            fh.write(len(textbox).to_bytes(1, "big"))
            for block in textbox:
                # Get Icon State
                icon_id = -1
                for string in block["text"]:
                    if string in icon_db.values():
                        for icon in icon_db:
                            if icon_db[icon] == string:
                                icon_id = icon
                if icon_id > -1:
                    fh.write(bytearray([2, 1]))
                    fh.write(icon_id.to_bytes(2, "big"))
                    fh.write(bytearray([0, 0]))
                else:
                    fh.write(bytearray([1, len(block["text"])]))
                    for string in block["text"]:
                        fh.write(position.to_bytes(4, "big"))
                        fh.write(len(string).to_bytes(2, "big"))
                        fh.write(bytearray([0, 0]))
                        position += len(string)
                unk0 = 0
                if "unk0" in block:
                    unk0 = block["unk0"]
                fh.write(int(float_to_hex(unk0), 16).to_bytes(4, "big"))
        fh.write(bytearray(position.to_bytes(2, "big")))
        for textbox in text:
            for block in textbox:
                is_icon = False
                for string in block["text"]:
                    if string in icon_db.values():
                        is_icon = True
                if not is_icon:
                    for string in block["text"]:
                        fh.write(string.encode("ascii"))
