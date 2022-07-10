"""Encode text file to ROM."""


def writeText(file_name, text):
    """Write the text to ROM."""
    with open(file_name, "wb") as fh:
        fh.write(bytearray([len(text)]))
        position = 0
        for textbox in text:
            fh.write(bytearray([1, 1, len(textbox)]))
            for string in textbox:
                fh.write(position.to_bytes(4, "big"))
                fh.write(len(string).to_bytes(2, "big"))
                fh.write(bytearray([0, 0]))
                position += len(string)
            fh.write(bytearray([0, 0, 0, 0]))
        fh.write(bytearray(position.to_bytes(2, "big")))
        for textbox in text:
            for string in textbox:
                fh.write(string.encode("ascii"))
