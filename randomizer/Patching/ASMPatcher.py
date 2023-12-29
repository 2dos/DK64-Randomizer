"""Patches assembly instructions from the overlays rather than doing changes live."""

from randomizer.Patching.Lib import Overlay, float_to_hex
from randomizer.Settings import Settings

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
    if overlay not in list(offset_dict.keys()):
        return None
    overlay_start = offset_dict[overlay]
    rdram_start = 0x805FB300 if overlay == Overlay.Static else 0x80024000
    return overlay_start + (address - rdram_start)


def writeValue(ROM_COPY, address: int, overlay: Overlay, value: int, offset_dict: dict, size: int = 2, signed: bool = False):
    """Write value to ROM based on overlay."""
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        return
    ROM_COPY.seek(rom_start)
    passed_value = value
    if value < 0 and signed:
        passed_value += 1 << (8 * size)
    ROM_COPY.writeMultipleBytes(passed_value, size)


def writeFloat(ROM_COPY, address: int, overlay: Overlay, value: float, offset_dict: dict):
    """Write floating point variable to ROM."""
    rom_start = getROMAddress(address, overlay, offset_dict)
    if rom_start is None:
        return
    ROM_COPY.seek(rom_start)
    passed_value = int(float_to_hex(value), 16)
    ROM_COPY.writeMultipleBytes(passed_value, 4)


def patchAssemblyCosmetic(ROM_COPY, settings: Settings):
    """Patch assembly instructions that pertain to cosmetic changes."""
    offset_dict = populateOverlayOffsets(ROM_COPY)

    if settings.troff_brighten:
        writeFloat(ROM_COPY, 0x8075B8B0, Overlay.Static, 1, offset_dict)


def patchAssembly(ROM_COPY, spoiler):
    """Patch all assembly instructions."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    writeValue(ROM_COPY, 0x8060E04C, Overlay.Static, 0, offset_dict, 4)  # Prevent moves overwrite
    writeValue(ROM_COPY, 0x8060DDAA, Overlay.Static, 0, offset_dict)  # Writes readfile data to moves
    writeValue(ROM_COPY, 0x806C9CDE, Overlay.Static, 7, offset_dict)  # GiveEverything, write to bitfield. Seems to be unused but might as well
    writeValue(ROM_COPY, 0x8074DC84, Overlay.Static, 0x53, offset_dict)  # Increase PAAD size
    writeValue(ROM_COPY, 0x8060EEE0, Overlay.Static, 0x240E0000, offset_dict, 4)  # Disable Graphical Debugger. ADDIU $t6, $r0, 0
    # Mermaid
    writeValue(ROM_COPY, 0x806C3B64, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3BD0, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3C20, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state write
    writeValue(ROM_COPY, 0x806C3C2C, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state progress write

    if spoiler.settings.no_healing:
        writeValue(ROM_COPY, 0x80683A34, Overlay.Static, 0, offset_dict, 4)  # Cancel Tag Health Refill
        writeValue(ROM_COPY, 0x806CB340, Overlay.Static, 0, offset_dict, 4)  # Voiding
        writeValue(ROM_COPY, 0x806DEFE4, Overlay.Static, 0, offset_dict, 4)  # Fairies
        writeValue(ROM_COPY, 0x806A6EA8, Overlay.Static, 0, offset_dict, 4)  # Bonus Barrels
    else:
        writeValue(ROM_COPY, 0x806A6EA8, Overlay.Static, 0x0C1C2519, offset_dict, 4)  # Set Bonus Barrel to refill health

    if spoiler.settings.bonus_barrel_auto_complete:
        writeValue(ROM_COPY, 0x806818DE, Overlay.Static, 0x4248, offset_dict)  # Make Aztec Lobby GB spawn above the trapdoor)
        writeValue(ROM_COPY, 0x80681690, Overlay.Static, 0, offset_dict, 4)  # Make some barrels not play a cutscene
        writeValue(ROM_COPY, 0x8068188C, Overlay.Static, 0, offset_dict, 4)  # Prevent disjoint mechanic for Caves/Fungi BBlast Bonus
        writeValue(ROM_COPY, 0x80681898, Overlay.Static, 0x1000, offset_dict)
        writeValue(ROM_COPY, 0x8068191C, Overlay.Static, 0, offset_dict, 4)  # Remove Oh Banana
        writeValue(ROM_COPY, 0x80680986, Overlay.Static, 0xFFFE, offset_dict)  # Prevent Factory BBBandit Bonus dropping
        writeValue(ROM_COPY, 0x806809C8, Overlay.Static, 0x1000, offset_dict)  # Prevent Fungi TTTrouble Bonus dropping
        writeValue(ROM_COPY, 0x80681962, Overlay.Static, 1, offset_dict)  # Make bonus noclip

    if spoiler.settings.tns_location_rando:
        # Adjust warp code to make camera be behind player, loading portal
        writeValue(ROM_COPY, 0x806C97D0, Overlay.Static, 0xA06E0007, offset_dict, 4)  # SB $t6, 0x7 ($v1)

    if spoiler.settings.cb_rando:
        writeValue(ROM_COPY, 0x8069C2FC, Overlay.Static, 0, offset_dict, 4)

    if spoiler.settings.perma_death:
        writeValue(ROM_COPY, 0x8064EC00, Overlay.Static, 0x24020001, offset_dict, 4)
