"""Patches assembly instructions from the overlays rather than doing changes live."""

from randomizer.Patching.Lib import Overlay, float_to_hex, IsItemSelected, compatible_background_textures
from randomizer.Settings import Settings
from randomizer.Enums.Settings import FasterChecksSelected, RemovedBarriersSelected, FreeTradeSetting, HardModeSelected, FungiTimeSetting, MiscChangesSelected
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Models import Model
from randomizer.Patching.Patcher import ROM, LocalROM

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
    passed_value = int(value)
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


def patchAssemblyCosmetic(ROM_COPY: ROM, settings: Settings):
    """Patch assembly instructions that pertain to cosmetic changes excluding Widescreen."""
    offset_dict = populateOverlayOffsets(ROM_COPY)

    if settings.troff_brighten:
        writeFloat(ROM_COPY, 0x8075B8B0, Overlay.Static, 1, offset_dict)

    if settings.remove_water_oscillation:
        writeValue(ROM_COPY, 0x80661B54, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 0
        writeValue(ROM_COPY, 0x80661B64, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 1
        writeValue(ROM_COPY, 0x8068BDF4, Overlay.Static, 0, offset_dict, 4)  # Disable rocking in Seasick Ship
        writeValue(ROM_COPY, 0x8068BDFC, Overlay.Static, 0x1000, offset_dict)  # Disable rocking in Mech Fish

    if settings.caves_tomato_model == Model.Tomato:
        writeValue(ROM_COPY, 0x8075F602, Overlay.Static, Model.Tomato + 1, offset_dict)

    if settings.fungi_tomato_model == Model.IceTomato:
        writeValue(ROM_COPY, 0x8075F4E2, Overlay.Static, Model.IceTomato + 1, offset_dict)

    if settings.bother_klaptrap_model:
        writeValue(ROM_COPY, 0x806F0376, Overlay.Static, settings.bother_klaptrap_model + 1, offset_dict)
        writeValue(ROM_COPY, 0x806C8B42, Overlay.Static, settings.bother_klaptrap_model + 1, offset_dict)

    if settings.rabbit_model == Model.Beetle:
        writeValue(ROM_COPY, 0x8075F242, Overlay.Static, Model.Beetle + 1, offset_dict)  # Rabbit Race
        # Animation scale
        writeValue(ROM_COPY, 0x806BE942, Overlay.Static, 0x285, offset_dict)
        writeValue(ROM_COPY, 0x806BEFC2, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF052, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF066, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF0C2, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BF1D2, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BEA8A, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BEB6A, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF1DE, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x8075F244, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BE9B2, Overlay.Static, 0x287, offset_dict)
        writeValue(ROM_COPY, 0x806BED5E, Overlay.Static, 0x288, offset_dict)
        # Chunky 5DI
        writeValue(ROM_COPY, 0x8075F3F2, Overlay.Static, Model.Beetle + 1, offset_dict)
        writeValue(ROM_COPY, 0x806B23C6, Overlay.Static, 0x287, offset_dict)

    if settings.misc_cosmetics:
        writeValue(ROM_COPY, 0x8064F052, Overlay.Static, settings.wrinkly_rgb[0], offset_dict)
        writeValue(ROM_COPY, 0x8064F04A, Overlay.Static, settings.wrinkly_rgb[1], offset_dict)
        writeValue(ROM_COPY, 0x8064F046, Overlay.Static, settings.wrinkly_rgb[2], offset_dict)
        # Menu Background
        if settings.menu_texture_index is not None:
            writeValue(ROM_COPY, 0x8070761A, Overlay.Static, 0, offset_dict)
            if compatible_background_textures[settings.menu_texture_index].is32by32:
                writeValue(ROM_COPY, 0x8070762E, Overlay.Static, 0xFFE0, offset_dict)
                writeValue(ROM_COPY, 0x8070727E, Overlay.Static, 0xC07C, offset_dict)
                writeValue(ROM_COPY, 0x80707222, Overlay.Static, 0x073F, offset_dict)
            writeValue(ROM_COPY, 0x80707126, Overlay.Static, compatible_background_textures[settings.menu_texture_index].table, offset_dict)
            menu_background_rgba = 0x505050FF
            if compatible_background_textures[settings.menu_texture_index].is_color:
                menu_background_rgba = 0x000020FF  # TODO: Get colors working properly
            writeValue(ROM_COPY, 0x8075EAE4, Overlay.Static, menu_background_rgba, offset_dict, 4)
            writeValue(ROM_COPY, 0x80754CEC, Overlay.Static, settings.menu_texture_index, offset_dict)

    if settings.crosshair_outline:
        writeValue(ROM_COPY, 0x806FFAFE, Overlay.Static, 113, offset_dict)
        writeValue(ROM_COPY, 0x806FF116, Overlay.Static, 113, offset_dict)
        writeValue(ROM_COPY, 0x806B78DA, Overlay.Static, 113, offset_dict)


def isFasterCheckEnabled(spoiler, fast_check: FasterChecksSelected):
    """Determine if a faster check setting is enabled."""
    return IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, fast_check)


def isQoLEnabled(spoiler, misc_change: MiscChangesSelected):
    """Determine if a faster check setting is enabled."""
    return IsItemSelected(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, misc_change)


FLAG_ABILITY_CAMERA = 0x2FD


def expandSaveFile(ROM_COPY: LocalROM, static_expansion: int, actor_count: int, offset_dict: dict):
    """Expand Save file."""
    expansion = static_expansion + actor_count
    flag_block_size = 0x320 + expansion
    targ_gb_bits = 7  # Max 127
    added_bits = (targ_gb_bits - 3) * 8
    kong_var_size = 0xA1 + added_bits
    file_info_location = flag_block_size + (5 * kong_var_size)
    file_default_size = file_info_location + 0x72
    # Flag Block Size
    writeValue(ROM_COPY, 0x8060E36A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E31E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E2C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D54A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D4A2, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D45E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D3C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D32E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D23E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CF62, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CC52, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C78A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C352, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BF96, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BA7A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BEC6, Overlay.Static, file_info_location, offset_dict)
    # Increase GB Storage Size
    writeValue(ROM_COPY, 0x8060BE12, Overlay.Static, targ_gb_bits, offset_dict)  # Bit Size
    writeValue(ROM_COPY, 0x8060BE06, Overlay.Static, targ_gb_bits << 3, offset_dict)  # Allocation for all levels
    writeValue(ROM_COPY, 0x8060BE26, Overlay.Static, 0x40C0, offset_dict)  # SLL 2 -> SLL 3
    writeValue(ROM_COPY, 0x8060BCC0, Overlay.Static, 0x24090000 | kong_var_size, offset_dict, 4)  # ADDIU $t1, $r0, kong_var_size
    writeValue(ROM_COPY, 0x8060BCC4, Overlay.Static, 0x01C90019, offset_dict, 4)  # MULTU $t1, $t6
    writeValue(ROM_COPY, 0x8060BCC8, Overlay.Static, 0x00004812, offset_dict, 4)  # MFLO $t1
    writeValue(ROM_COPY, 0x8060BCCC, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Model 2 Start
    writeValue(ROM_COPY, 0x8060C2F2, Overlay.Static, flag_block_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BCDE, Overlay.Static, flag_block_size, offset_dict)
    # Reallocate Balloons + Patches
    writeValue(ROM_COPY, 0x80688BCE, Overlay.Static, 0x320 + static_expansion, offset_dict)  # Reallocated to just before model 2 block


def patchAssembly(ROM_COPY, spoiler):
    """Patch all assembly instructions."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    writeValue(ROM_COPY, 0x8060E04C, Overlay.Static, 0, offset_dict, 4)  # Prevent moves overwrite
    writeValue(ROM_COPY, 0x8060DDAA, Overlay.Static, 0, offset_dict)  # Writes readfile data to moves
    writeValue(ROM_COPY, 0x806C9CDE, Overlay.Static, 7, offset_dict)  # GiveEverything, write to bitfield. Seems to be unused but might as well
    writeValue(ROM_COPY, 0x8074DC84, Overlay.Static, 0x53, offset_dict)  # Increase PAAD size
    writeValue(ROM_COPY, 0x8060EEE0, Overlay.Static, 0x240E0000, offset_dict, 4)  # Disable Graphical Debugger. ADDIU $t6, $r0, 0
    writeValue(ROM_COPY, 0x806416BC, Overlay.Static, 0, offset_dict, 4)  # Prevent parent map check in cross-map object change communications
    writeValue(ROM_COPY, 0x806AF75C, Overlay.Static, 0x1000, offset_dict)  # New Kop Code
    writeValue(ROM_COPY, 0x806CBD78, Overlay.Static, 0x18400005, offset_dict, 4)  # BLEZ $v0, 0x5 - Decrease in health occurs if trap bubble active
    writeValue(ROM_COPY, 0x806A65B8, Overlay.Static, 0x240A0006, offset_dict, 4)  # Always ensure chunky bunch sprite (Rock Bunch)
    writeValue(ROM_COPY, 0x806A64B0, Overlay.Static, 0x240A0004, offset_dict, 4)  # Always ensure lanky coin sprite (Rabbit Race 1 Reward)
    writeValue(ROM_COPY, 0x8060036A, Overlay.Static, 0xFF, offset_dict)  # Fix game crash upon exiting a bonus with no parent
    writeValue(ROM_COPY, 0x806F88A8, Overlay.Static, 0x1000, offset_dict)  # Force disable coin cheat
    writeValue(ROM_COPY, 0x805FEA14, Overlay.Static, 0, offset_dict, 4)  # Prevent Enguarde arena setting kong as Enguarde
    writeValue(ROM_COPY, 0x805FEA08, Overlay.Static, 0, offset_dict, 4)  # Prevent Rambi arena setting kong as Rambi

    # Level Index Fixes
    for map_index in (Maps.OrangeBarrel, Maps.BarrelBarrel, Maps.VineBarrel, Maps.DiveBarrel):
        writeValue(ROM_COPY, 0x807445E0 + map_index, Overlay.Static, 9, offset_dict, 1)  # Write Training level index to LEVEL_BONUS
    # Mermaid
    writeValue(ROM_COPY, 0x806C3B64, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3BD0, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3C20, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state write
    writeValue(ROM_COPY, 0x806C3C2C, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state progress write
    # Silk Memes
    writeValue(ROM_COPY, 0x806ADA6C, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ADA78, Overlay.Static, 0, offset_dict, 4)
    # Fix Spider Crashes
    writeValue(ROM_COPY, 0x8075F46C, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADA26, Overlay.Static, 0x2F5, offset_dict)  # This might fix spawning if set on non-init
    writeValue(ROM_COPY, 0x806ADA2A, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADA32, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADBC6, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADC66, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADD3A, Overlay.Static, 0x2F5, offset_dict)
    # Decouple Camera from Shockwave
    writeValue(ROM_COPY, 0x806E9812, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Usage
    writeValue(ROM_COPY, 0x806AB0F6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Isles Fairies Display
    writeValue(ROM_COPY, 0x806AAFB6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Other Fairies Display
    writeValue(ROM_COPY, 0x806AA762, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Display
    writeValue(ROM_COPY, 0x8060D986, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeValue(ROM_COPY, 0x806F6F76, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeValue(ROM_COPY, 0x806F916A, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film max
    # Disable training pre-checks
    writeValue(ROM_COPY, 0x80698386, Overlay.Static, 0, offset_dict)  # Disable ability to use vines in vine barrel unless you have vines
    writeValue(ROM_COPY, 0x806E426C, Overlay.Static, 0, offset_dict, 4)  # Disable ability to pick up objects in barrel barrel unless you have barrels
    writeValue(ROM_COPY, 0x806E7736, Overlay.Static, 0, offset_dict)  # Disable ability to dive in dive barrel unless you have dive
    writeValue(ROM_COPY, 0x806E2D8A, Overlay.Static, 0, offset_dict)  # Disable ability to throw oranges in orange barrel unless you have oranges
    # Files
    balloon_patch_count = 150
    static_expansion = 0x100
    if spoiler.settings.enemy_drop_rando:
        static_expansion += 426  # Total Enemies
    if False:  # TODO: Check Archipelago
        static_expansion += 400  # Archipelago Flag size
    expandSaveFile(ROM_COPY, static_expansion, balloon_patch_count, offset_dict)
    # 1-File Fixes
    writeValue(ROM_COPY, 0x8060CF34, Overlay.Static, 0x240E0001, offset_dict, 4)  # Slot 1
    writeValue(ROM_COPY, 0x8060CF38, Overlay.Static, 0x240F0002, offset_dict, 4)  # Slot 2
    writeValue(ROM_COPY, 0x8060CF3C, Overlay.Static, 0x24180003, offset_dict, 4)  # Slot 3
    writeValue(ROM_COPY, 0x8060CF40, Overlay.Static, 0x240D0000, offset_dict, 4)  # Slot 0
    writeValue(ROM_COPY, 0x8060D3AC, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060DCE8, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060CD1A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 2
    writeValue(ROM_COPY, 0x8060CE7E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 3
    writeValue(ROM_COPY, 0x8060CE5A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 4
    writeValue(ROM_COPY, 0x8060CF0E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 5
    writeValue(ROM_COPY, 0x8060CF26, Overlay.Static, 1, offset_dict)  # File Loop Cancel 6
    writeValue(ROM_COPY, 0x8060D106, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060D43E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060CD08, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CE48, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CF04, Overlay.Static, 0x26270000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060BFA4, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060E378, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D33C, Overlay.Static, 0x254B0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D470, Overlay.Static, 0x256C0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D4B0, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D558, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060CF74, Overlay.Static, 0x25090000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D24C, Overlay.Static, 0x25AE0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060C84C, Overlay.Static, 0xA02067C8, offset_dict, 4)  # Force file 0
    writeValue(ROM_COPY, 0x8060C654, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C664, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C6C4, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060C6D4, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060D294, Overlay.Static, 0, offset_dict, 4)  # Cartridge EEPROM Wipe cancel

    # Move Decoupling
    # Strong Kong
    writeValue(ROM_COPY, 0x8067ECFC, Overlay.Static, 0x30810002, offset_dict, 4)  # ANDI $at $a0 2
    writeValue(ROM_COPY, 0x8067ED00, Overlay.Static, 0x50200003, offset_dict, 4)  # BEQL $at $r0 3
    # Rocketbarrel
    writeValue(ROM_COPY, 0x80682024, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x80682028, Overlay.Static, 0x50200006, offset_dict, 4)  # BEQL $at $r0 0x6
    # OSprint
    writeValue(ROM_COPY, 0x8067ECE0, Overlay.Static, 0x30810004, offset_dict, 4)  # ANDI $at $a0 4
    writeValue(ROM_COPY, 0x8067ECE4, Overlay.Static, 0x10200002, offset_dict, 4)  # BEQZ $at, 2
    # Mini Monkey
    writeValue(ROM_COPY, 0x8067EC80, Overlay.Static, 0x30830001, offset_dict, 4)  # ANDI $v1 $a0 1
    writeValue(ROM_COPY, 0x8067EC84, Overlay.Static, 0x18600002, offset_dict, 4)  # BLEZ $v1 2
    # Hunky Chunky (Not Dogadon)
    writeValue(ROM_COPY, 0x8067ECA0, Overlay.Static, 0x30810001, offset_dict, 4)  # ANDI $at $a0 1
    writeValue(ROM_COPY, 0x8067ECA4, Overlay.Static, 0x18200002, offset_dict, 4)  # BLEZ $at 2
    # PTT
    writeValue(ROM_COPY, 0x806E20F0, Overlay.Static, 0x31010002, offset_dict, 4)  # ANDI $at $t0 2
    writeValue(ROM_COPY, 0x806E20F4, Overlay.Static, 0x5020000F, offset_dict, 4)  # BEQL $at $r0 0xF
    # PPunch
    writeValue(ROM_COPY, 0x806E48F4, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x806E48F8, Overlay.Static, 0x50200074, offset_dict, 4)  # BEQL $at $r0 0xF

    # Disable Sniper Scope Overlay
    writeValue(ROM_COPY, 0x806FF80C, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF85C, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF8AC, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF8FC, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF940, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF988, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF9D0, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FFA18, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0

    writeValue(ROM_COPY, 0x806A7564, Overlay.Static, 0xC4440080, offset_dict, 4)  # Crown default floor will be it's initial Y spawn position. Fixes a crash on N64

    # Expand Display List
    writeValue(ROM_COPY, 0x805FE56A, Overlay.Static, 8000, offset_dict)
    writeValue(ROM_COPY, 0x805FE592, Overlay.Static, 0x4100, offset_dict)  # SLL 4 (Doubles display list size)
    # Sniper Scope Check
    writeValue(ROM_COPY, 0x806D2988, Overlay.Static, 0x93190002, offset_dict, 4)  # LBU $t9, 0x2 ($t8)
    writeValue(ROM_COPY, 0x806D2990, Overlay.Static, 0x33210004, offset_dict, 4)  # ANDI $at, $t9, 0x4
    writeValue(ROM_COPY, 0x806D299C, Overlay.Static, 0x1020, offset_dict)  # BEQ $at, $r0
    # EEPROM Patch
    writeValue(ROM_COPY, 0x8060D588, Overlay.Static, 0, offset_dict, 4)  # NOP
    # TEMPORARY FIX FOR SAVE BUG
    writeValue(ROM_COPY, 0x8060D790, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Cancel Tamper
    writeValue(ROM_COPY, 0x8060AEFC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x80611788, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Fix HUD if DK not free
    writeValue(ROM_COPY, 0x806FA324, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x807505AE, Overlay.Static, 385, offset_dict)  # Set Flag to DK Flag
    # Fix CB Spawning
    writeValue(ROM_COPY, 0x806A7882, Overlay.Static, 385, offset_dict)  # DK Balloon
    # Fix Boss Doors if DK not free
    writeValue(ROM_COPY, 0x80649358, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Fix Pause Menu
    writeValue(ROM_COPY, 0x806ABFF8, Overlay.Static, 0, offset_dict, 4)  # NOP (Write of first slot to 1)
    writeValue(ROM_COPY, 0x806AC002, Overlay.Static, 0x530, offset_dict)
    writeValue(ROM_COPY, 0x806AC006, Overlay.Static, 0x5B0, offset_dict)
    writeValue(ROM_COPY, 0x8075054D, Overlay.Static, 0xD7, offset_dict, 1)  # Change DK Q Mark to #FFD700
    # Guard Animation Fix
    writeValue(ROM_COPY, 0x806AF8C6, Overlay.Static, 0x2C1, offset_dict)
    # Remove flare effect from guards
    writeValue(ROM_COPY, 0x806AE440, Overlay.Static, 0, offset_dict, 4)
    # Boost Diddy/Tiny's Barrel Speed
    writeFloat(ROM_COPY, 0x807533A0, Overlay.Static, 240, offset_dict)  # Diddy Ground
    writeFloat(ROM_COPY, 0x807533A8, Overlay.Static, 240, offset_dict)  # Tiny Ground
    writeFloat(ROM_COPY, 0x807533DC, Overlay.Static, 260, offset_dict)  # Lanky Air
    writeFloat(ROM_COPY, 0x807533E0, Overlay.Static, 260, offset_dict)  # Tiny Air
    # Bump Model Two Allowance
    writeValue(ROM_COPY, 0x80632026, Overlay.Static, 550, offset_dict)  # Japes
    writeValue(ROM_COPY, 0x80632006, Overlay.Static, 550, offset_dict)  # Aztec
    writeValue(ROM_COPY, 0x80631FF6, Overlay.Static, 550, offset_dict)  # Factory
    writeValue(ROM_COPY, 0x80632016, Overlay.Static, 550, offset_dict)  # Galleon
    writeValue(ROM_COPY, 0x80631FE6, Overlay.Static, 550, offset_dict)  # Fungi
    writeValue(ROM_COPY, 0x80632036, Overlay.Static, 550, offset_dict)  # Others

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

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.factory_toy_monster_fight):
        writeValue(ROM_COPY, 0x806BBB22, Overlay.Static, 5, offset_dict)  # Chunky toy box speedup

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.forest_owl_race):
        writeValue(ROM_COPY, 0x806C58D6, Overlay.Static, 8, offset_dict)  # Owl ring amount
        writeValue(ROM_COPY, 0x806C5B16, Overlay.Static, 8, offset_dict)  # Owl ring amount

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.forest_rabbit_race):
        writeValue(ROM_COPY, 0x806BEDFC, Overlay.Static, 0, offset_dict, 4)  # Spawn banana coins on beating rabbit 2 (Beating round 2 branches to banana coin spawning label before continuing)

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.caves_ice_tomato_minigame):
        writeValue(ROM_COPY, 0x806BC582, Overlay.Static, 30, offset_dict)  # Ice Tomato Timer

    if spoiler.settings.free_trade_setting != FreeTradeSetting.none:
        # Non-BP Items
        writeValue(ROM_COPY, 0x807319C0, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make all reward spots think no kong
        # writeValue(ROM_COPY, 0x80632E94, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make flag mapping think no kong
        if spoiler.settings.free_trade_setting == FreeTradeSetting.major_collectibles:
            writeValue(ROM_COPY, 0x806F56F8, Overlay.Static, 0, offset_dict, 4)  # Disable Flag Set for blueprints
            writeValue(ROM_COPY, 0x806A606C, Overlay.Static, 0, offset_dict, 4)  # Disable translucency for blueprints

    if IsItemSelected(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardModeSelected.hard_enemies):
        writeValue(ROM_COPY, 0x806B12DA, Overlay.Static, 0x3A9, offset_dict)  # Kasplat Shockwave Chance
        writeValue(ROM_COPY, 0x806B12FE, Overlay.Static, 0x3B3, offset_dict)  # Kasplat Shockwave Chance

    if spoiler.settings.medal_cb_req > 0:
        writeValue(ROM_COPY, 0x806F934E, Overlay.Static, spoiler.settings.medal_cb_req, offset_dict)  # Acquisition
        writeValue(ROM_COPY, 0x806F935A, Overlay.Static, spoiler.settings.medal_cb_req, offset_dict)  # Acquisition
        writeValue(ROM_COPY, 0x806AA942, Overlay.Static, spoiler.settings.medal_cb_req, offset_dict)  # Pause Menu Tick

    if spoiler.settings.fungi_time_internal == FungiTimeSetting.dusk:
        writeValue(ROM_COPY, 0x806C5614, Overlay.Static, 0x50000006, offset_dict, 4)
        writeValue(ROM_COPY, 0x806BE8F8, Overlay.Static, 0x50000008, offset_dict, 4)

    if spoiler.settings.enable_tag_anywhere:
        writeValue(ROM_COPY, 0x806F6D94, Overlay.Static, 0, offset_dict, 4)  # Prevent delayed collection
        writeValue(ROM_COPY, 0x806F5B68, Overlay.Static, 0x1000, offset_dict)  # Standard Ammo
        writeValue(ROM_COPY, 0x806F59A8, Overlay.Static, 0x1000, offset_dict)  # Bunch
        writeValue(ROM_COPY, 0x806F6CAC, Overlay.Static, 0x9204001A, offset_dict, 4)  # LBU $a0, 0x1A ($s0)
        writeValue(ROM_COPY, 0x806F6CB0, Overlay.Static, 0x86060002, offset_dict, 4)  # LH $a2, 0x2 ($s0)
        writeValue(ROM_COPY, 0x806F53AC, Overlay.Static, 0, offset_dict, 4)  # Prevent LZ case
        writeValue(ROM_COPY, 0x806C7088, Overlay.Static, 0x1000, offset_dict)  # Mech fish dying

    if spoiler.settings.puzzle_rando:
        # Alter diddy R&D
        diddy_rnd_code_writes = [
            # Code 0: 4231
            0x8064E06A,
            0x8064E066,
            0x8064E062,
            0x8064E05E,
            # Code 1: 3124
            0x8064E046,
            0x8064E042,
            0x8064E03E,
            0x8064E00E,
            # Code 2: 1342
            0x8064E026,
            0x8064E022,
            0x8064E01E,
            0x8064E01A,
        ]
        for code_index, code in enumerate(spoiler.settings.diddy_rnd_doors):
            for sub_index, item in enumerate(code):
                writeValue(ROM_COPY, diddy_rnd_code_writes[(4 * code_index) + sub_index], Overlay.Static, item + 1, offset_dict)

        # DK Face Puzzle
        dk_face_puzzle_register_values = [0x80, 0x95, 0x83, 0x82]  # 0 = r0, 1 = s5, 2 = v1, 3 = v0
        dk_face_puzzle_addresses = [
            0x8064AD11,
            0x8064AD15,
            0x8064AD01,
            0x8064AD19,
            0x8064AD1D,
            0x8064AD05,
            0x8064AD21,
            0x8064AD09,
            0x8064AD29,
        ]
        for index, address in enumerate(dk_face_puzzle_addresses):
            if spoiler.dk_face_puzzle[index] is not None:
                reg_value = dk_face_puzzle_register_values[spoiler.dk_face_puzzle[index]]
                writeValue(ROM_COPY, address, Overlay.Static, reg_value, offset_dict, 1)

        # Chunky Face Puzzle
        chunky_face_puzzle_register_values = [0x40, 0x54, 0x48, 0x44]  # 0 = r0, 1 = s4, 2 = t0, 3 = a0
        chunky_face_puzzle_addresses = [
            0x8064A2ED,
            0x8064A2F1,
            0x8064A2D5,
            0x8064A2F5,
            0x8064A2F9,
            0x8064A2FD,
            0x8064A2DD,
            0x8064A301,
            0x8064A305,
        ]
        for index, address in enumerate(chunky_face_puzzle_addresses):
            if spoiler.chunky_face_puzzle[index] is not None:
                reg_value = chunky_face_puzzle_register_values[spoiler.chunky_face_puzzle[index]]
                writeValue(ROM_COPY, address, Overlay.Static, reg_value, offset_dict, 1)

    if isQoLEnabled(spoiler, MiscChangesSelected.fast_picture_taking):
        # Fast Camera Photo
        writeValue(ROM_COPY, 0x80699454, Overlay.Static, 0x5000, offset_dict)  # Fast tick/no mega-slowdown on Biz
        writeValue(ROM_COPY, 0x806992B6, Overlay.Static, 0x14, offset_dict)  # No wait for camera film development
        writeValue(ROM_COPY, 0x8069932A, Overlay.Static, 0x14, offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.lowered_aztec_lobby_bonus):
        # Lower Aztec Lobby Bonus
        writeValue(ROM_COPY, 0x80680D56, Overlay.Static, 0x7C, offset_dict)  # 0x89 if this needs to be unreachable without PTT
    if isQoLEnabled(spoiler, MiscChangesSelected.small_bananas_always_visible):
        writeValue(ROM_COPY, 0x806324D4, Overlay.Static, 0x24020001, offset_dict, 4)  # ADDIU $v0, $r0, 1. Disable kong flag check
        writeValue(ROM_COPY, 0x806A78C4, Overlay.Static, 0, offset_dict, 4)  # NOP. Disable kong flag check
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_hints):
        writeValue(ROM_COPY, 0x8069E0F6, Overlay.Static, 1, offset_dict)
        writeValue(ROM_COPY, 0x8069E112, Overlay.Static, 1, offset_dict)
        writeValue(ROM_COPY, 0x80758BC9, Overlay.Static, 0xAE, offset_dict, 1)  # Quadruple Growth Speed (8E -> AE)
        writeValue(ROM_COPY, 0x80758BD1, Overlay.Static, 0xAE, offset_dict, 1)  # Quadruple Shrink Speed (8E -> AE)
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_boot):
        # Remove DKTV - Game Over
        writeValue(ROM_COPY, 0x8071319E, Overlay.Static, 0x50, offset_dict)
        writeValue(ROM_COPY, 0x807131AA, Overlay.Static, 5, offset_dict)
        # Remove DKTV - End Seq
        writeValue(ROM_COPY, 0x8071401E, Overlay.Static, 0x50, offset_dict)
        writeValue(ROM_COPY, 0x8071404E, Overlay.Static, 5, offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_transform_animation):
        writeValue(ROM_COPY, 0x8067EAB2, Overlay.Static, 1, offset_dict)  # OSprint
        writeValue(ROM_COPY, 0x8067EAC6, Overlay.Static, 1, offset_dict)  # HC Dogadon 2
        writeValue(ROM_COPY, 0x8067EACA, Overlay.Static, 1, offset_dict)  # Others
        writeValue(ROM_COPY, 0x8067EA92, Overlay.Static, 1, offset_dict)  # Others 2
    if isQoLEnabled(spoiler, MiscChangesSelected.animal_buddies_grab_items):
        # Transformations can pick up other's collectables
        writeValue(ROM_COPY, 0x806F6330, Overlay.Static, 0x96AC036E, offset_dict, 4)  # Collection
        # Collection
        writeValue(ROM_COPY, 0x806F68A0, Overlay.Static, 0x95B8036E, offset_dict, 4)  # DK Collection
        writeValue(ROM_COPY, 0x806F68DC, Overlay.Static, 0x952C036E, offset_dict, 4)  # Diddy Collection
        writeValue(ROM_COPY, 0x806F6914, Overlay.Static, 0x95F9036E, offset_dict, 4)  # Tiny Collection
        writeValue(ROM_COPY, 0x806F694C, Overlay.Static, 0x95AE036E, offset_dict, 4)  # Lanky Collection
        writeValue(ROM_COPY, 0x806F6984, Overlay.Static, 0x952B036E, offset_dict, 4)  # Chunky Collection
        # Opacity
        writeValue(ROM_COPY, 0x80637998, Overlay.Static, 0x95B9036E, offset_dict, 4)  # DK Opacity
        writeValue(ROM_COPY, 0x806379E8, Overlay.Static, 0x95CF036E, offset_dict, 4)  # Diddy Opacity
        writeValue(ROM_COPY, 0x80637A28, Overlay.Static, 0x9589036E, offset_dict, 4)  # Tiny Opacity
        writeValue(ROM_COPY, 0x80637A68, Overlay.Static, 0x954B036E, offset_dict, 4)  # Chunky Opacity
        writeValue(ROM_COPY, 0x80637AA8, Overlay.Static, 0x9708036E, offset_dict, 4)  # Lanky Opacity
        # CB/Coin rendering
        writeValue(ROM_COPY, 0x806394FC, Overlay.Static, 0x958B036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639540, Overlay.Static, 0x9728036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639584, Overlay.Static, 0x95AE036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639430, Overlay.Static, 0x95CD036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806393EC, Overlay.Static, 0x9519036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806395C8, Overlay.Static, 0x952A036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x8063960C, Overlay.Static, 0x95F8036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639474, Overlay.Static, 0x9549036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806393A8, Overlay.Static, 0x956C036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806394B8, Overlay.Static, 0x970F036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639650, Overlay.Static, 0x956C036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639710, Overlay.Static, 0x9549036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639750, Overlay.Static, 0x970F036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806396D0, Overlay.Static, 0x95CD036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639690, Overlay.Static, 0x9519036E, offset_dict, 4)  # Rendering
    if isQoLEnabled(spoiler, MiscChangesSelected.reduced_lag):
        writeValue(ROM_COPY, 0x80748010, Overlay.Static, 0x8064F2F0, offset_dict, 4)  # Cancel Sandstorm
        # No Rain
        writeFloat(ROM_COPY, 0x8075E3E0, Overlay.Static, 0, offset_dict)  # Set Isles Rain Radius to 0
        writeValue(ROM_COPY, 0x8068AF90, Overlay.Static, 0, offset_dict, 4)  # Disable weather
    if isQoLEnabled(spoiler, MiscChangesSelected.homing_balloons):
        writeValue(ROM_COPY, 0x80694F6A, Overlay.Static, 10, offset_dict)  # Coconut
        writeValue(ROM_COPY, 0x80692B82, Overlay.Static, 10, offset_dict)  # Peanuts
        writeValue(ROM_COPY, 0x8069309A, Overlay.Static, 10, offset_dict)  # Grape
        writeValue(ROM_COPY, 0x80695406, Overlay.Static, 10, offset_dict)  # Feather
        writeValue(ROM_COPY, 0x80694706, Overlay.Static, 10, offset_dict)  # Pineapple
    if isQoLEnabled(spoiler, MiscChangesSelected.better_fairy_camera):
        # Increased range for fairy shots
        screen_x_center = 160
        screen_y_center = 120
        screen_x_dist = 24  # Usually 16
        screen_y_dist = 24  # Usually 16
        fairy_range = 1000
        writeValue(ROM_COPY, 0x806C5DB6, Overlay.Static, screen_x_center - screen_x_dist, offset_dict)  # X Minimum
        writeValue(ROM_COPY, 0x806C5DC6, Overlay.Static, screen_x_center + screen_x_dist, offset_dict)  # X Maximum
        writeValue(ROM_COPY, 0x806C5DD6, Overlay.Static, screen_y_center - screen_y_dist, offset_dict)  # Y Minimum
        writeValue(ROM_COPY, 0x806C5DDE, Overlay.Static, screen_y_center + screen_y_dist, offset_dict)  # Y Maximum
        writeValue(ROM_COPY, 0x806C5DE8, Overlay.Static, 0x240B0000 | fairy_range, offset_dict, 4)  # Force max acceptable dist to 1000
    writeValue(ROM_COPY, 0x80032096, Overlay.Arcade, 0, offset_dict)  # Disable Nin 1981 flicker
    writeValue(ROM_COPY, 0x8002672A, Overlay.Arcade, 0xFFFF, offset_dict)  # Disable Donkey Kong logo title flicker
