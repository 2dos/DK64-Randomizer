"""Update all the overlays in the ROM."""

from typing import BinaryIO
from BuildClasses import OverlayInfo
from BuildEnums import Overlay
from BuildLib import heap_size
from heap import getHeapData

overlays = [
    OverlayInfo(Overlay.Static, 0x113F0, 0xC29D4, 0x949C, 0x80000776, 0x80000792, 0x8000077A, 0x8000078E, 0x149160, 0x1CBF0),  # 1
    OverlayInfo(Overlay.Menu, 0xCBE70, 0xD4554, 0x5A2, 0x8000083E, 0x8000086A, 0x80000842, 0x80000866, 0xEF50, 0xFC0),  # 10
    OverlayInfo(Overlay.Multiplayer, 0xD4B00, 0xD69F8, 0xFB, 0x8000077E, 0x8000079A, 0x80000782, 0x80000796, 0x2F70, 0x190),  # 2
    OverlayInfo(Overlay.Minecart, 0xD6B00, 0xD98A0, 0x197, 0x800007B6, 0x800007E2, 0x800007BA, 0x800007DE, 0x4B90, 0x280),  # 3
    OverlayInfo(Overlay.Bonus, 0xD9A40, 0xDF346, 0x2BA, 0x800007BE, 0x800007EA, 0x800007C2, 0x800007E6, 0x9860, 0x690),  # 4
    OverlayInfo(Overlay.Race, 0xDF600, 0xE649A, 0x2DB, 0x800007CA, 0x800007EE, 0x800007C6, 0x800007F2, 0xBB10, 0x650),  # 5
    OverlayInfo(Overlay.Critter, 0xE6780, 0xE9D17, 0x38C, 0x800007D2, 0x800007F6, 0x800007CE, 0x800007FA, 0x57F0, 0x9C0),  # 6
    OverlayInfo(Overlay.Boss, 0xEA0B0, 0xF388F, 0x90A, 0x800007DA, 0x800007FE, 0x800007D6, 0x80000802, 0x118B0, 0x1510),  # 7
    OverlayInfo(Overlay.Arcade, 0xF41A0, 0xFB42C, 0x1EC4, 0x80000832, 0x80000856, 0x8000082E, 0x8000085A, 0xE220, 0x189E0),  # 8
    OverlayInfo(Overlay.Jetpac, 0xFD2F0, 0x1010FD, 0x936, 0x8000083A, 0x8000085E, 0x80000836, 0x80000862, 0x7090, 0x3BA0),  # 9
]


def isROMAddressOverlay(absolute_address: int):
    """Check if its an overlay."""
    for x in overlays:
        if x.code_rom == absolute_address:
            return True
        if x.data_rom == absolute_address:
            return True

    return False


def readOverlayOriginalData(fr: BinaryIO):
    """Read the original overlay data."""
    for x in overlays:
        fr.seek(x.code_rom)
        x.setCode(fr.read(x.code_size_compressed - 8), fr.read(8))
        x.setData(fr.read(x.data_size_compressed - 8), fr.read(8))


def replaceOverlayData(absolute_address: int, newCompressedData: bytearray):
    """Replace the overlay."""
    for x in overlays:
        if absolute_address == x.code_rom:
            print(" - Replacing " + x.overlay.name + " .code with modified data")
            x.code = newCompressedData
            return
        if absolute_address == x.data_rom:
            print(" - Replacing " + x.overlay.name + " .data with modified data")
            x.data = newCompressedData
            return


def writeModifiedOverlaysToROM(fr: BinaryIO):
    """Write the data to ROM."""
    # TODO: Make sure they aren't too big
    for x in overlays:
        fr.seek(x.code_rom)
        fr.write(x.code)
        fr.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))  # gzip footer
        fr.write(x.data)
        fr.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))  # gzip footer


def getUpperValue(value: int) -> int:
    """Get upper 2 bytes of a value write for asm changes."""
    upper_2 = value >> 16
    if value & 0x8000:
        return upper_2 + 1
    return upper_2


def getLowerValue(value: int) -> int:
    """Get lower 2 bytes of a value write for asm changes."""
    return value & 0xFFFF


def writeStaticValue(fr: BinaryIO, address: int, static_base: int, value: int, size: int = 2):
    """Write short to the static overlay."""
    offset = address - 0x805FB300
    fr.seek(static_base + offset)
    fr.write(value.to_bytes(size, "big"))


BOOT_START = 0x1050


def writeUncompressedOverlays(fr: BinaryIO):
    """Write uncompressed overlays to ROM."""
    fr.seek(0x2000000 + heap_size)
    static_start = None
    static_end = None
    for x in overlays:
        x.code_start = fr.tell()
        print(f"- Writing decompressed overlay code for {x.overlay.name} to ROM Address {hex(x.code_start)}")
        fr.write(x.code_decompressed)
        x.data_start = fr.tell()
        print(f"- Writing decompressed overlay data for {x.overlay.name} to ROM Address {hex(x.data_start)}")
        fr.write(x.data_decompressed)
        x.data_end = fr.tell()
        if x.overlay == Overlay.Static:
            static_start = x.code_start
            static_end = x.data_end
    # Static load
    fr.seek(BOOT_START + (0x71A - 0x450))
    fr.write(getUpperValue(static_start).to_bytes(2, "big"))
    fr.seek(BOOT_START + (0x71E - 0x450))
    fr.write(getUpperValue(static_end).to_bytes(2, "big"))
    fr.seek(BOOT_START + (0x72A - 0x450))
    fr.write(getLowerValue(static_end).to_bytes(2, "big"))
    fr.seek(BOOT_START + (0x732 - 0x450))
    fr.write(getLowerValue(static_start).to_bytes(2, "big"))

    static_upper = None
    static_data_upper = None
    multi_upper = None
    multi_data_upper = None
    for x in overlays:
        fr.seek(x.code_write_upper + BOOT_START)
        fr.write(getUpperValue(x.code_start).to_bytes(2, "big"))
        fr.seek(x.code_write_lower + BOOT_START)
        fr.write(getLowerValue(x.code_start).to_bytes(2, "big"))
        fr.seek(x.data_write_upper + BOOT_START)
        fr.write(getUpperValue(x.data_end).to_bytes(2, "big"))
        fr.seek(x.data_write_lower + BOOT_START)
        fr.write(getLowerValue(x.data_end).to_bytes(2, "big"))
        if x.overlay == Overlay.Static:
            static_upper = getUpperValue(x.code_start)
            static_data_upper = getUpperValue(x.data_end)
        elif x.overlay == Overlay.Multiplayer:
            multi_upper = getUpperValue(x.code_start)
            multi_data_upper = getUpperValue(x.data_end)
        # Write plain offsets to ROM
        fr.seek(0x1FFB000 + (8 * x.overlay))
        fr.write(x.code_start.to_bytes(4, "big"))
        fr.write(x.data_end.to_bytes(4, "big"))
    # Disable decompression of static
    fr.seek(BOOT_START + (0x720 - 0x450))
    fr.write((0x01403025).to_bytes(4, "big"))
    fr.seek(BOOT_START + (0x738 - 0x450))
    fr.write((0).to_bytes(4, "big"))
    with open("asm/overlay_defs.asm", "w") as fh:
        fh.write("; Automatically written by build/recompute_overlays.py\n\n")
        fh.write(f".definelabel static_code_upper, {hex(static_upper)}\n")
        fh.write(f".definelabel static_data_upper, {hex(static_data_upper)}\n")
        fh.write(f".definelabel multi_code_upper, {hex(multi_upper)}\n")
        fh.write(f".definelabel multi_data_upper, {hex(multi_data_upper)}\n")

    if static_start is not None:
        # Very simple base level changes to get stuff working
        # Decompression
        writeStaticValue(fr, 0x806108FE, static_start, 0)
        writeStaticValue(fr, 0x8061090A, static_start, 0)
        writeStaticValue(fr, 0x8061090E, static_start, 0)
        writeStaticValue(fr, 0x80610926, static_start, 0)
        # Heap Shrink
        writeStaticValue(fr, 0x80610512, static_start, getHeapData()["upper"])
        writeStaticValue(fr, 0x8061051A, static_start, getHeapData()["lower"])
        # Kong Coloring
        writeStaticValue(fr, 0x8068A62F, static_start, 0, 1)
        writeStaticValue(fr, 0x8068A450, static_start, 0, 4)
        writeStaticValue(fr, 0x8068A458, static_start, 0, 4)
        # Nintendo Logo
        dimensions = [256, 132]
        offset = 640 - (2 * dimensions[0])
        writeStaticValue(fr, 0x805FB8BA, static_start, dimensions[0])
        writeStaticValue(fr, 0x805FB8FA, static_start, dimensions[1])
        writeStaticValue(fr, 0x805FB902, static_start, offset)
        writeStaticValue(fr, 0x805FB8AA, static_start, 0x7840)
        # Others
        writeStaticValue(fr, 0x805FC164, static_start, 0x080037A2, 4)
        # Lag Hook
        # fh.seek(0x5374)
        # fh.write(patch_lag_hook)


def getOverlayTotalSize() -> int:
    """Get size of all uncompressed overlays."""
    return sum([x.code_size + x.data_size for x in overlays])
