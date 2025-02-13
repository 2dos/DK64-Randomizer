import js
from randomizer.Patching.Library.Generic import Overlay
from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Patcher import ROM

HANDLED_OVERLAYS = (
    Overlay.Static,
    Overlay.Menu,
    Overlay.Multiplayer,
    Overlay.Minecart,
    Overlay.Bonus,
    Overlay.Race,
    Overlay.Critter,
    Overlay.Boss,
    Overlay.Arcade,
    Overlay.Jetpac,
)
BANNED_OFFSETS = (0, 0xFFFFFFFF)
OVERLAY_ENDS = {
    Overlay.Static: 0x80761050,
    Overlay.Menu: 0x80033F10,
    Overlay.Multiplayer: 0x80027100,
    Overlay.Minecart: 0x80028E10,
    Overlay.Bonus: 0x8002DEF0,
    Overlay.Race: 0x80030160,
    Overlay.Critter: 0x8002A1B0,
    Overlay.Boss: 0x80036DC0,
    Overlay.Arcade: 0x8004AC00,
    Overlay.Jetpac: 0x8002EC30,
    Overlay.Custom: 0x805FAE00,
}
CUSTOM_ACTORS_START = 345

def populateOverlayOffsets(ROM_COPY) -> dict:
    """Populate the overlay offset database."""
    result = {}
    for ovl in HANDLED_OVERLAYS:
        ROM_COPY.seek(0x1FFB000 + (8 * ovl))
        code = int.from_bytes(ROM_COPY.readBytes(4), "big")
        if code not in BANNED_OFFSETS:
            result[ovl] = code
    return result


def getROMAddress(address: int, overlay: Overlay, offset_dict: dict) -> int:
    """Get ROM Address corresponding to a specific RDRAM Address in an overlay."""
    if overlay == Overlay.Custom:
        rdram_start = 0x805FAE00 - 0x39DC0
        overlay_start = 0x2000000
    elif overlay == Overlay.Boot:
        rdram_start = 0x80000450
        overlay_start = 0x1050
    else:
        if overlay not in list(offset_dict.keys()):
            return None
        overlay_start = offset_dict[overlay]
        rdram_start = 0x80024000
        if overlay == Overlay.Static:
            rdram_start = 0x805FB300
        elif overlay == Overlay.Boot:
            rdram_start = 0x80000450
    if overlay in OVERLAY_ENDS:
        if address >= OVERLAY_ENDS[overlay]:
            raise Exception(f"Seeking out of bounds for this overlay. Attempted to seek to {hex(address)} in overlay {overlay.name}")
    if address < rdram_start:
        raise Exception(f"Seeking out of bounds for this overlay. Attempted to seek to {hex(address)} in overlay {overlay.name}")
    return overlay_start + (address - rdram_start)


def writeValue(ROM_COPY, address: int, overlay: Overlay, value: int, offset_dict: dict, size: int = 2, signed: bool = False):
    """Write value to ROM based on overlay."""
    if isinstance(ROM_COPY, ROM) and overlay == Overlay.Custom:
        raise Exception("Cosmetics write to the custom code overlay.")
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    ROM_COPY.seek(rom_start)
    passed_value = int(value)
    if value < 0 and signed:
        passed_value += 1 << (8 * size)
    ROM_COPY.writeMultipleBytes(passed_value, size)


def writeFloat(ROM_COPY, address: int, overlay: Overlay, value: float, offset_dict: dict):
    """Write floating point variable to ROM."""
    if isinstance(ROM_COPY, ROM) and overlay == Overlay.Custom:
        raise Exception("Cosmetics write to the custom code overlay.")
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    ROM_COPY.seek(rom_start)
    passed_value = int(float_to_hex(value), 16)
    ROM_COPY.writeMultipleBytes(passed_value, 4)


def writeFloatUpper(ROM_COPY, address: int, overlay: Overlay, value: float, offset_dict: dict):
    """Write upper 16 bit portion of floating point variable to ROM."""
    if isinstance(ROM_COPY, ROM) and overlay == Overlay.Custom:
        raise Exception("Cosmetics write to the custom code overlay.")
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    ROM_COPY.seek(rom_start)
    passed_value = int(float_to_hex(value), 16)
    passed_value = (passed_value >> 16) & 0xFFFF
    ROM_COPY.writeMultipleBytes(passed_value, 2)


def writeFunction(ROM_COPY, address: int, overlay: Overlay, func_name: str, offset_dict: dict):
    """Write function JAL to ROM."""
    if isinstance(ROM_COPY, ROM):
        raise Exception("Cosmetics cannot utilize writeFunction.")
    # NOTE: This **CANNOT** be used for cosmetic changes
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    function_address = js.rom_symbols["symbols"].get(func_name.lower(), None)
    if function_address is None:
        raise Exception(f"Couldn't find function {func_name}.")
    ROM_COPY.seek(rom_start)
    value = 0x0C000000 | ((function_address & 0xFFFFFF) >> 2)
    ROM_COPY.writeMultipleBytes(value, 4)


def writeHook(ROM_COPY, address: int, overlay: Overlay, hook_location: str, offset_dict):
    """Write hook to ROM."""
    if isinstance(ROM_COPY, ROM):
        raise Exception("Cosmetics cannot utilize writeHook.")
    # NOTE: This **CANNOT** be used for cosmetic changes
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    hook_address = js.rom_symbols["symbols"].get(hook_location.lower(), None)
    if hook_address is None:
        raise Exception(f"Couldn't find hook {hook_location}.")
    ROM_COPY.seek(rom_start)
    value = 0x08000000 | ((hook_address & 0xFFFFFF) >> 2)
    ROM_COPY.writeMultipleBytes(value, 4)
    ROM_COPY.writeMultipleBytes(0, 4)


def writeLabelValue(ROM_COPY, address: int, overlay: Overlay, label_name: str, offset_dict) -> int:
    """Write value of label to ROM."""
    if isinstance(ROM_COPY, ROM):
        raise Exception("Cosmetics cannot utilize writeLabelValue.")
    # NOTE: This **CANNOT** be used for cosmetic changes
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        raise Exception(f"Couldn't ascertain a ROM start for address {hex(address)} and Overlay {overlay.name}.")
    label_address = js.rom_symbols["symbols"].get(label_name.lower(), None)
    if label_address is None:
        raise Exception(f"Couldn't find hook {label_name}.")
    ROM_COPY.seek(rom_start)
    ROM_COPY.writeMultipleBytes(label_address, 4)


def getLo(value: int) -> int:
    """Get the lower 16 bits for a 32-bit value that can be loaded into an addiu instruction."""
    return value & 0xFFFF


def getHi(value: int) -> int:
    """Get the upper 16 bits for a 32-bit value that can be loaded into a lui instruction."""
    hi = (value >> 16) & 0xFFFF
    lo = getLo(value)
    if lo & 0x8000:
        return hi + 1
    return hi


def getHiSym(ref: str) -> int:
    """Run getHi, but relative to a symbol rather than a value."""
    label_address = js.rom_symbols["symbols"].get(ref.lower(), None)
    if label_address is None:
        raise Exception(f"Couldn't find symbol {ref}.")
    return getHi(label_address)


def getLoSym(ref: str) -> int:
    """Run getLo, but relative to a symbol rather than a value."""
    label_address = js.rom_symbols["symbols"].get(ref.lower(), None)
    if label_address is None:
        raise Exception(f"Couldn't find symbol {ref}.")
    return getLo(label_address)


def getSym(ref: str) -> int:
    """Get symbol value."""
    sym_value = js.rom_symbols["symbols"].get(ref.lower(), None)
    if sym_value is None:
        raise Exception(f"Couldn't find symbol {ref}.")
    return sym_value


def getVar(ref: str) -> int:
    """Get variable value."""
    label_value = js.rom_symbols["vars"].get(ref.lower(), None)
    if label_value is None:
        raise Exception(f"Couldn't find variable {ref}.")
    return label_value

def getActorIndex(input: int) -> int:
    """Get actor index from provided value."""
    if input & 0x8000:
        return CUSTOM_ACTORS_START + (input & 0x7FFF)
    return input