"""Replace Wrinkly text in ROM."""

text = [
    ["WRINKLY FTT"],
    ["JAPES DK TEXT"],
    ["JAPES DIDDY TEXT", "SECOND LINE"],
    ["JAPES LANKY TEXT"],
    ["JAPES TINY TEXT"],
    ["JAPES CHUNKY TEXT"],
    ["AZTEC DK TEXT"],
    ["AZTEC DIDDY TEXT"],
    ["AZTEC LANKY TEXT"],
    ["AZTEC TINY TEXT"],
    ["AZTEC CHUNKY TEXT"],
    ["FACTORY DK TEXT"],
    ["FACTORY DIDDY TEXT"],
    ["FACTORY LANKY TEXT"],
    ["FACTORY TINY TEXT"],
    ["FACTORY CHUNKY TEXT"],
    ["GALLEON DK TEXT"],
    ["GALLEON DIDDY TEXT"],
    ["GALLEON LANKY TEXT"],
    ["GALLEON TINY TEXT"],
    ["GALLEON CHUNKY TEXT"],
    ["FUNGI DK TEXT"],
    ["FUNGI DIDDY TEXT"],
    ["FUNGI LANKY TEXT"],
    ["FUNGI TINY TEXT"],
    ["FUNGI CHUNKY TEXT"],
    ["CAVES DK TEXT"],
    ["CAVES DIDDY TEXT"],
    ["CAVES LANKY TEXT"],
    ["CAVES TINY TEXT"],
    ["CAVES CHUNKY TEXT"],
    ["CASTLE DK TEXT"],
    ["CASTLE DIDDY TEXT"],
    ["CASTLE LANKY TEXT"],
    ["CASTLE TINY TEXT"],
    ["CASTLE CHUNKY TEXT"],
]
with open("dk64-randomizer-base-dev.z64", "r+b") as fh:
    fh.seek(0x296FD42)  # Pointer Table 12, Index 41
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
