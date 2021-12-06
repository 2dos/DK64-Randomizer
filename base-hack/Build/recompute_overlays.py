from typing import BinaryIO

overlays = [
    {
        "name": "global_asm",
        "codeROMAddress": 0x113F0,
        "dataROMAddress": 0xC29D4,
        "dataCompressedSize": 0x949C, # - 8 for length without gzip footer
        # Note: These byte arrays should not contain the gzip footer
        # codeCompressedData: [], // Will be written to ROM
        # dataCompressedData: [], // Will be written to ROM directly after .code, regardless of the original .data address
    },
    {
        "name": "menu",
        "codeROMAddress": 0xCBE70,
        "dataROMAddress": 0xD4554,
        "dataCompressedSize": 0x5A2, # - 8 for length without gzip footer
    },
    {
        "name": "multiplayer",
        "codeROMAddress": 0xD4B00,
        "dataROMAddress": 0xD69F8,
        "dataCompressedSize": 0xFB, # - 8 for length without gzip footer
    },
    {
        "name": "minecart",
        "codeROMAddress": 0xD6B00,
        "dataROMAddress": 0xD98A0,
        "dataCompressedSize": 0x197, # - 8 for length without gzip footer
    },
    {
        "name": "bonus",
        "codeROMAddress": 0xD9A40,
        "dataROMAddress": 0xDF346,
        "dataCompressedSize": 0x2AA, # - 8 for length without gzip footer
    },
    {
        "name": "race",
        "codeROMAddress": 0xDF600,
        "dataROMAddress": 0xE649A,
        "dataCompressedSize": 0x2DB, # - 8 for length without gzip footer
    },
    {
        "name": "?",
        "codeROMAddress": 0xE6780,
        "dataROMAddress": 0xE9D17,
        "dataCompressedSize": 0x38C, # - 8 for length without gzip footer
    },
    {
        "name": "boss",
        "codeROMAddress": 0xEA0B0,
        "dataROMAddress": 0xF388F,
        "dataCompressedSize": 0x90A, # - 8 for length without gzip footer
    },
    {
        "name": "arcade",
        "codeROMAddress": 0xF41A0,
        "dataROMAddress": 0xFB42C,
        "dataCompressedSize": 0x1EC4, # - 8 for length without gzip footer
    },
    {
        "name": "jetpac",
        "codeROMAddress": 0xFD2F0,
        "dataROMAddress": 0x1010FD,
        "dataCompressedSize": 0x936, # - 8 for length without gzip footer
    },
]

def isROMAddressOverlay(absolute_address : int):
    for x in overlays:
        if x["codeROMAddress"] == absolute_address:
            return True
        if x["dataROMAddress"] == absolute_address:
            return True
    
    return False

def readOverlayOriginalData(fr : BinaryIO):
    for x in overlays:
        x["codeCompressedSize"] = x["dataROMAddress"] - x["codeROMAddress"]
        fr.seek(x["codeROMAddress"])
        x["codeCompressedData"] = fr.read(x["codeCompressedSize"] - 8)
        fr.read(8) # skip gzip footer
        x["dataCompressedData"] = fr.read(x["dataCompressedSize"] - 8)
        fr.read(8) # skip gzip footer

def replaceOverlayData(absolute_address : int, newCompressedData : bytearray):
    for x in overlays:
        if absolute_address == x["codeROMAddress"]:
            print(" - Replacing " + x["name"] + " .code with modified data")
            x["codeCompressedData"] = newCompressedData
            return
        if absolute_address == x["dataROMAddress"]:
            print(" - Replacing " + x["name"] + " .data with modified data")
            x["dataCompressedData"] = newCompressedData
            return

def writeModifiedOverlaysToROM(fr : BinaryIO):
    # TODO: Make sure they aren't too big
    for x in overlays:
        fr.seek(x["codeROMAddress"])
        fr.write(x["codeCompressedData"])
        fr.write(bytes([0,0,0,0,0,0,0,0])) # gzip footer
        fr.write(x["dataCompressedData"])
        fr.write(bytes([0,0,0,0,0,0,0,0])) # gzip footer