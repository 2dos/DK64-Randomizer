"""Encode text file to ROM."""


def writeText(file_name, text):
    """Write the text to ROM."""
    with open(file_name, "wb") as fh:
        fh.write(bytearray([len(text)]))
        position = 0
        for textbox in text:
            fh.write(bytearray([1, 1, len(textbox)]))
            for string in textbox:
                fh.write(bytearray([0, 0]))
                fh.write(position.to_bytes(2, "big"))
                fh.write(len(string).to_bytes(2, "big"))
                fh.write(bytearray([0, 0]))
                position += len(string)
                # fh.write(position.to_bytes(2,"big"))
            fh.write(bytearray([0, 0, 0, 0]))
        fh.write(bytearray([0xA, 0xC3]))
        for textbox in text:
            for string in textbox:
                fh.write(string.encode("ascii"))
