"""Assembly patching for the widescreen hack."""

from randomizer.Settings import Settings
from randomizer.Patching.Lib import Overlay, float_to_hex, IsItemSelected
from randomizer.Patching.ASMPatcher import writeValue, writeFloat, populateOverlayOffsets
from randomizer.Enums.Settings import MiscChangesSelected
from randomizer.Patching.Patcher import ROM

SCREEN_WD = 366
SCREEN_HD = 208
GFX_START = 0x101A40
BOOT_OFFSET = 0xFB20 - 0xEF20


def patchAssemblyCosmeticWS(ROM_COPY: ROM, settings: Settings):
    """Write Widescreen changes to ROM."""
    if not settings.true_widescreen:
        return
    offset_dict = populateOverlayOffsets(ROM_COPY)

    ROM_COPY.seek(settings.rom_data + 0x1B4)
    ROM_COPY.write(1)

    ROM_COPY.seek(GFX_START + 0x00)
    ROM_COPY.writeMultipleBytes(SCREEN_WD * 2, 2)  # 2D Viewport Width
    ROM_COPY.seek(GFX_START + 0x02)
    ROM_COPY.writeMultipleBytes(SCREEN_HD * 2, 2)  # 2D Viewport Height
    ROM_COPY.seek(GFX_START + 0x08)
    ROM_COPY.writeMultipleBytes(SCREEN_WD * 2, 2)  # 2D Viewport X Position
    ROM_COPY.seek(GFX_START + 0x0A)
    ROM_COPY.writeMultipleBytes(SCREEN_HD * 2, 2)  # 2D Viewport Y Position
    ROM_COPY.seek(GFX_START + 0x9C)
    ROM_COPY.writeMultipleBytes((SCREEN_WD << 14) | (SCREEN_HD << 2), 4)  # Default Scissor for 2D
    data_offsets = [0xEF20, 0xF7E0]
    internal_size = 0x50
    internal_offsets = [0, 2]
    for tv_offset in data_offsets:
        for int_offset in internal_offsets:
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x08)
            ROM_COPY.writeMultipleBytes(SCREEN_WD, 4)  # VI Width
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x20)
            ROM_COPY.writeMultipleBytes(int((SCREEN_WD * 512) / 320), 4)  # VI X Scale
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x28)
            ROM_COPY.writeMultipleBytes((SCREEN_WD * 2), 4)  # VI Field 1 Framebuffer Offset
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x3C)
            ROM_COPY.writeMultipleBytes((SCREEN_WD * 2), 4)  # VI Field 2 Framebuffer Offset
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x2C)
            ROM_COPY.writeMultipleBytes(int((SCREEN_HD * 1024) / 240), 4)  # VI Field 1 Y Scale
            ROM_COPY.seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x40)
            ROM_COPY.writeMultipleBytes(int((SCREEN_HD * 1024) / 240), 4)  # VI Field 2 Y Scale
    ROM_COPY.seek(BOOT_OFFSET + 0xBC4 + 2)
    ROM_COPY.writeMultipleBytes(SCREEN_WD * 2, 2)  # Row Offset of No Expansion Pak Image
    ROM_COPY.seek(BOOT_OFFSET + 0xBC8 + 2)
    ROM_COPY.writeMultipleBytes(SCREEN_WD * SCREEN_HD * 2, 2)  # Invalidation Size for Framebuffer 1
    ROM_COPY.seek(BOOT_OFFSET + 0xE08)
    ROM_COPY.writeMultipleBytes(0x24180000 | SCREEN_WD, 4)  # Row Pitch for No Expansion Pak Screen Text
    ROM_COPY.seek(BOOT_OFFSET + 0xE0C)
    ROM_COPY.writeMultipleBytes(0x03060019, 4)  # Calculate Row Pixel Number for No Expansion Pak Screen Text
    ROM_COPY.seek(BOOT_OFFSET + 0xE10)
    ROM_COPY.writeMultipleBytes(0x0000C012, 4)  # Get Row Pixel Number for No Expansion Pak Screen Text
    ROM_COPY.seek(BOOT_OFFSET + 0x1020 + 2)
    ROM_COPY.writeMultipleBytes((SCREEN_WD - 8) * 2, 2)  # Text Framebuffer Pitch

    # Sand Effect
    writeValue(ROM_COPY, 0x80750240, Overlay.Static, SCREEN_WD, offset_dict)  # Sand Effect Vertex 2 X
    writeValue(ROM_COPY, 0x80750248, Overlay.Static, ((SCREEN_WD * 2016) / 320), offset_dict)  # Sand Effect Vertex 2 X Texcoord
    writeValue(ROM_COPY, 0x80750250, Overlay.Static, SCREEN_WD, offset_dict)  # Sand Effect Vertex 3 X
    writeValue(ROM_COPY, 0x80750252, Overlay.Static, SCREEN_HD, offset_dict)  # Sand Effect Vertex 3 Y
    writeValue(ROM_COPY, 0x80750258, Overlay.Static, ((SCREEN_WD * 2016) / 320), offset_dict)  # Sand Effect Vertex 3 X Texcoord
    writeValue(ROM_COPY, 0x8075025A, Overlay.Static, ((SCREEN_HD * 2016) / 240), offset_dict)  # Sand Effect Vertex 3 Y Texcoord
    writeValue(ROM_COPY, 0x80750262, Overlay.Static, SCREEN_HD, offset_dict)  # Sand Effect Vertex 4 Y
    writeValue(ROM_COPY, 0x8075026A, Overlay.Static, ((SCREEN_HD * 2016) / 240), offset_dict)  # Sand Effect Vertex 3 4 Texcoord

    writeValue(ROM_COPY, 0x80750848, Overlay.Static, (SCREEN_WD - 1), offset_dict)  # Right Edge of Blackness in Border 1
    writeValue(ROM_COPY, 0x80750856, Overlay.Static, (SCREEN_HD - 1), offset_dict)  # Bottom Edge of Blackness in Border 2
    writeValue(ROM_COPY, 0x8075085C, Overlay.Static, (SCREEN_WD - 11), offset_dict)  # Left Edge of Blackness in Border 3
    writeValue(ROM_COPY, 0x80750860, Overlay.Static, (SCREEN_WD - 1), offset_dict)  # Right Edge of Blackness in Border 3
    writeValue(ROM_COPY, 0x80750862, Overlay.Static, (SCREEN_HD - 1), offset_dict)  # Bottom Edge of Blackness in Border 3
    writeValue(ROM_COPY, 0x8075086A, Overlay.Static, (SCREEN_HD - 11), offset_dict)  # Top Edge of Blackness in Border 4
    writeValue(ROM_COPY, 0x8075086C, Overlay.Static, (SCREEN_WD - 11), offset_dict)  # Right Edge of Blackness in Border 4
    writeValue(ROM_COPY, 0x8075086E, Overlay.Static, (SCREEN_HD - 1), offset_dict)  # Bottom Edge of Blackness in Border 4

    writeValue(ROM_COPY, 0x80750950, Overlay.Static, SCREEN_WD - 11, offset_dict)  # Right Edge of Viewport Setup 1
    writeValue(ROM_COPY, 0x80750952, Overlay.Static, SCREEN_HD - 11, offset_dict)  # Bottom Edge of Viewport Setup 1
    writeValue(ROM_COPY, 0x8075095C, Overlay.Static, SCREEN_WD - 11, offset_dict)  # Right Edge of Viewport Setup 2
    writeValue(ROM_COPY, 0x8075095E, Overlay.Static, SCREEN_HD - 11, offset_dict)  # Bottom Edge of Viewport Setup 1

    writeValue(ROM_COPY, 0x80754C58, Overlay.Static, SCREEN_WD, offset_dict)  # X Position of Vertex 2 of UI Layer 1
    writeValue(ROM_COPY, 0x80754C68, Overlay.Static, SCREEN_WD, offset_dict)  # X Position of Vertex 3 of UI Layer 1
    writeValue(ROM_COPY, 0x80754C6A, Overlay.Static, SCREEN_HD, offset_dict)  # Y Position of Vertex 3 of UI Layer 1
    writeValue(ROM_COPY, 0x80754C7A, Overlay.Static, SCREEN_HD, offset_dict)  # Y Position of Vertex 4 of UI Layer 1
    writeValue(ROM_COPY, 0x80754C98, Overlay.Static, SCREEN_WD, offset_dict)  # X Position of Vertex 2 of UI Layer 2
    writeValue(ROM_COPY, 0x80754CA8, Overlay.Static, SCREEN_WD, offset_dict)  # X Position of Vertex 3 of UI Layer 2
    writeValue(ROM_COPY, 0x80754CAA, Overlay.Static, SCREEN_HD, offset_dict)  # Y Position of Vertex 3 of UI Layer 2
    writeValue(ROM_COPY, 0x80754CBA, Overlay.Static, SCREEN_HD, offset_dict)  # Y Position of Vertex 4 of UI Layer 2

    writeValue(ROM_COPY, 0x80027396, Overlay.Bonus, SCREEN_WD - 40, offset_dict)  # X Position of Melons
    writeValue(ROM_COPY, 0x8002D1B2, Overlay.Bonus, SCREEN_WD << 1, offset_dict)  # X Position of HIT and Combo Text

    writeFloat(ROM_COPY, 0x80758140, Overlay.Static, SCREEN_WD - 1, offset_dict)  # X Size of Pause Menu Background Texture 1
    writeFloat(ROM_COPY, 0x80758144, Overlay.Static, SCREEN_WD - 1, offset_dict)  # X Size of Pause Menu Background Texture 1
    writeFloat(ROM_COPY, 0x80758148, Overlay.Static, SCREEN_WD - 1, offset_dict)  # X Size of Pause Menu Background Texture 1
    writeFloat(ROM_COPY, 0x8075814C, Overlay.Static, SCREEN_WD - 1, offset_dict)  # X Size of Pause Menu Background Texture 1

    writeValue(ROM_COPY, 0x800330E0, Overlay.Menu, (SCREEN_WD * 2) - 520, offset_dict)  # X Position of Vertex 1 of Chart Border
    writeValue(ROM_COPY, 0x800330F0, Overlay.Menu, (SCREEN_WD * 2) + 520, offset_dict)  # X Position of Vertex 2 of Chart Border
    writeValue(ROM_COPY, 0x80033100, Overlay.Menu, (SCREEN_WD * 2) + 480, offset_dict)  # X Position of Vertex 3 of Chart Border
    writeValue(ROM_COPY, 0x80033110, Overlay.Menu, (SCREEN_WD * 2) - 480, offset_dict)  # X Position of Vertex 4 of Chart Border
    writeValue(ROM_COPY, 0x80033120, Overlay.Menu, (SCREEN_WD * 2) - 520, offset_dict)  # X Position of Vertex 5 of Chart Border
    writeValue(ROM_COPY, 0x80033130, Overlay.Menu, (SCREEN_WD * 2) + 520, offset_dict)  # X Position of Vertex 6 of Chart Border
    writeValue(ROM_COPY, 0x80033140, Overlay.Menu, (SCREEN_WD * 2) + 480, offset_dict)  # X Position of Vertex 7 of Chart Border
    writeValue(ROM_COPY, 0x80033150, Overlay.Menu, (SCREEN_WD * 2) - 480, offset_dict)  # X Position of Vertex 8 of Chart Border
    writeValue(ROM_COPY, 0x80033160, Overlay.Menu, (SCREEN_WD * 2) + 520, offset_dict)  # X Position of Vertex 9 of Chart Border
    writeValue(ROM_COPY, 0x80033170, Overlay.Menu, (SCREEN_WD * 2) + 520, offset_dict)  # X Position of Vertex 10 of Chart Border
    writeValue(ROM_COPY, 0x80033180, Overlay.Menu, (SCREEN_WD * 2) + 480, offset_dict)  # X Position of Vertex 11 of Chart Border
    writeValue(ROM_COPY, 0x80033190, Overlay.Menu, (SCREEN_WD * 2) + 480, offset_dict)  # X Position of Vertex 12 of Chart Border
    writeValue(ROM_COPY, 0x800331A0, Overlay.Menu, (SCREEN_WD * 2) - 520, offset_dict)  # X Position of Vertex 13 of Chart Border
    writeValue(ROM_COPY, 0x800331B0, Overlay.Menu, (SCREEN_WD * 2) - 520, offset_dict)  # X Position of Vertex 14 of Chart Border
    writeValue(ROM_COPY, 0x800331C0, Overlay.Menu, (SCREEN_WD * 2) - 480, offset_dict)  # X Position of Vertex 15 of Chart Border
    writeValue(ROM_COPY, 0x800331D0, Overlay.Menu, (SCREEN_WD * 2) - 480, offset_dict)  # X Position of Vertex 16 of Chart Border
    writeValue(ROM_COPY, 0x800331E0, Overlay.Menu, (SCREEN_WD * 2) - 320, offset_dict)  # X Position of Vertex 17 of Chart Border
    writeValue(ROM_COPY, 0x800331F0, Overlay.Menu, (SCREEN_WD * 2) + 320, offset_dict)  # X Position of Vertex 18 of Chart Border
    writeValue(ROM_COPY, 0x80033200, Overlay.Menu, (SCREEN_WD * 2) + 320, offset_dict)  # X Position of Vertex 19 of Chart Border
    writeValue(ROM_COPY, 0x80033210, Overlay.Menu, (SCREEN_WD * 2) - 320, offset_dict)  # X Position of Vertex 20 of Chart Border

    writeFloat(ROM_COPY, 0x80033894, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Player 1 in Player Setup
    writeFloat(ROM_COPY, 0x8003389C, Overlay.Menu, (SCREEN_WD / 2) + 50, offset_dict)  # X Position of Player 2 in Player Setup
    writeFloat(ROM_COPY, 0x800338A4, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Player 3 in Player Setup
    writeFloat(ROM_COPY, 0x800338AC, Overlay.Menu, (SCREEN_WD / 2) - 50, offset_dict)  # X Position of Player 4 in Player Setup

    upper_barrels = -75 + (65 * (SCREEN_HD / 240))
    lower_barrels = -75 + (135 * (SCREEN_HD / 240))
    writeFloat(ROM_COPY, 0x80033790, Overlay.Menu, upper_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x8003379C, Overlay.Menu, upper_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337A0, Overlay.Menu, lower_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337AC, Overlay.Menu, lower_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337B0, Overlay.Menu, lower_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337BC, Overlay.Menu, lower_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337C0, Overlay.Menu, upper_barrels, offset_dict)
    writeFloat(ROM_COPY, 0x800337CC, Overlay.Menu, upper_barrels, offset_dict)

    writeValue(ROM_COPY, 0x8002C26E, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x8002C2CE, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x8002C2FE, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of C-Up
    writeValue(ROM_COPY, 0x8002C326, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Start
    writeValue(ROM_COPY, 0x8002C3EA, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x8002C43A, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x8002C472, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of C-Down
    writeValue(ROM_COPY, 0x8002C4A2, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of C-Up
    writeValue(ROM_COPY, 0x8002C4CA, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x8002C51A, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of C-Down
    writeValue(ROM_COPY, 0x8002C54A, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of C-Down
    writeValue(ROM_COPY, 0x8002A312, Overlay.Menu, SCREEN_WD << 2, offset_dict)  # X Offset of Yes Text
    writeValue(ROM_COPY, 0x8002A3AE, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x8002A3B2, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    writeValue(ROM_COPY, 0x8002A3E2, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    writeValue(ROM_COPY, 0x8002A416, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Orange
    writeValue(ROM_COPY, 0x8002A41A, Overlay.Menu, (SCREEN_HD / 2) + 8, offset_dict)  # Y Position of Orange
    writeValue(ROM_COPY, 0x8002A442, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x8002A446, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of Analog Stick
    writeValue(ROM_COPY, 0x80029D6A, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x80029EA6, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Bouncing Orange
    writeValue(ROM_COPY, 0x80029ED2, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x80029D6E, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    writeValue(ROM_COPY, 0x80029D9E, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    writeValue(ROM_COPY, 0x80028EEE, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x80028EF2, Overlay.Menu, SCREEN_HD / 2, offset_dict)  # Y Position of Analog Stick
    writeValue(ROM_COPY, 0x80029026, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x8002902A, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    writeValue(ROM_COPY, 0x8002905A, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of B Button
    writeValue(ROM_COPY, 0x8002C736, Overlay.Menu, (SCREEN_WD * 2) - 570, offset_dict)  # X Position of Player Win/Lose Status
    writeValue(ROM_COPY, 0x8002C8DE, Overlay.Menu, SCREEN_WD * 2, offset_dict)  # X Position of Score Text
    writeValue(ROM_COPY, 0x8002CADA, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x800288C6, Overlay.Menu, SCREEN_WD / 2, offset_dict)  # X Position of Analog Stick
    writeValue(ROM_COPY, 0x800288CA, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of Analog Stick
    writeValue(ROM_COPY, 0x80028B1E, Overlay.Menu, SCREEN_WD - 30, offset_dict)  # X Position of A Button
    writeValue(ROM_COPY, 0x80028B22, Overlay.Menu, SCREEN_HD - 30, offset_dict)  # Y Position of A Button
    # Snide Menu
    writeValue(ROM_COPY, 0x80024632, Overlay.Menu, SCREEN_WD * 2, offset_dict)  # X Position of Blueprint Names
    writeValue(ROM_COPY, 0x800246AA, Overlay.Menu, (SCREEN_WD * 2) - 290, offset_dict)  # X Position of Blueprints Text
    writeValue(ROM_COPY, 0x800246F2, Overlay.Menu, (SCREEN_WD * 2) - 290, offset_dict)  # X Position of Exit Text
    writeValue(ROM_COPY, 0x80024742, Overlay.Menu, (SCREEN_WD * 2) - 290, offset_dict)  # X Position of Bonus Text
    writeValue(ROM_COPY, 0x80024FF2, Overlay.Menu, (SCREEN_WD / 2) - 120, offset_dict)  # X Position of Left Edge of Chart Blackness
    writeValue(ROM_COPY, 0x80024FF6, Overlay.Menu, (SCREEN_WD / 2) - 90, offset_dict)  # X Position of Right Edge of Chart Blackness
    writeValue(ROM_COPY, 0x80025CA2, Overlay.Menu, (SCREEN_WD * 2) - 140, offset_dict)  # X Position of Yes Text for DK Arcade
    writeValue(ROM_COPY, 0x80025CEA, Overlay.Menu, (SCREEN_WD * 2) - 140, offset_dict)  # X Position of No Text for DK Arcade
    # Pause Menu
    writeValue(ROM_COPY, 0x80629626, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width
    writeValue(ROM_COPY, 0x8062960A, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height
    writeValue(ROM_COPY, 0x806296F6, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 2
    writeValue(ROM_COPY, 0x806296D6, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 2
    writeValue(ROM_COPY, 0x806297E6, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 3
    writeValue(ROM_COPY, 0x806297C2, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 3
    writeValue(ROM_COPY, 0x806298BA, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 4
    writeValue(ROM_COPY, 0x80629872, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 4
    writeValue(ROM_COPY, 0x8062999E, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 5
    writeValue(ROM_COPY, 0x8062997E, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 5
    writeValue(ROM_COPY, 0x80629A5A, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 6
    writeValue(ROM_COPY, 0x80629A12, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 6
    writeValue(ROM_COPY, 0x80629B4A, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 7
    writeValue(ROM_COPY, 0x80629B26, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 7
    writeValue(ROM_COPY, 0x80629BAA, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 8
    writeValue(ROM_COPY, 0x80629B82, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 8
    writeValue(ROM_COPY, 0x80629C6A, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 9
    writeValue(ROM_COPY, 0x80629C22, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 9
    writeValue(ROM_COPY, 0x80629D06, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 10
    writeValue(ROM_COPY, 0x80629CC2, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 10
    writeValue(ROM_COPY, 0x80629E46, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 10
    writeValue(ROM_COPY, 0x80629DEA, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 10
    writeValue(ROM_COPY, 0x80629F6E, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 11
    writeValue(ROM_COPY, 0x80629F12, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 11
    writeValue(ROM_COPY, 0x8062A07E, Overlay.Static, SCREEN_WD, offset_dict)  # Pause Menu Texture Width 12
    writeValue(ROM_COPY, 0x8062A03E, Overlay.Static, SCREEN_HD, offset_dict)  # Pause Menu Texture Height 12
    writeValue(ROM_COPY, 0x806ACF76, Overlay.Static, SCREEN_WD << 1, offset_dict)  # X Position of Multiplayer Pause Menu Return
    writeValue(ROM_COPY, 0x806ACF82, Overlay.Static, (SCREEN_HD << 1) - 40, offset_dict)  # Y Position of Multiplayer Pause Menu Return
    writeValue(ROM_COPY, 0x806ACFDE, Overlay.Static, SCREEN_WD << 1, offset_dict)  # X Position of Multiplayer Pause Menu Quit Game
    writeValue(ROM_COPY, 0x806ACFE2, Overlay.Static, (SCREEN_HD << 1) + 40, offset_dict)  # Y Position of Multiplayer Pause Menu Quit Game
    # Screen 0
    writeValue(ROM_COPY, 0x806AA546, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Oranges)
    writeValue(ROM_COPY, 0x806AA512, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Oranges Counter)
    writeValue(ROM_COPY, 0x806AA5B6, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Ammo)
    writeValue(ROM_COPY, 0x806AA562, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Ammo Counter)
    writeValue(ROM_COPY, 0x806AA66E, Overlay.Static, (SCREEN_HD >> 1) + 0x28, offset_dict)  # Y Position (Crystals)
    writeValue(ROM_COPY, 0x806AA63A, Overlay.Static, (SCREEN_HD >> 1) + 0x28, offset_dict)  # Y Position (Crystals Counter)
    writeValue(ROM_COPY, 0x806AA6E2, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Coins)
    writeValue(ROM_COPY, 0x806AA6AE, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Coins Counter)
    writeValue(ROM_COPY, 0x806AA756, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Instrument)
    writeValue(ROM_COPY, 0x806AA6FE, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Instrument Counter)
    writeValue(ROM_COPY, 0x806AA7CE, Overlay.Static, (SCREEN_HD >> 1) + 0x28, offset_dict)  # Y Position (Film)
    writeValue(ROM_COPY, 0x806AA79A, Overlay.Static, (SCREEN_HD >> 1) + 0x28, offset_dict)  # Y Position (Film Counter)
    writeValue(ROM_COPY, 0x806AA836, Overlay.Static, SCREEN_HD - 32, offset_dict)  # Y Position (GB)
    writeValue(ROM_COPY, 0x806AA7EE, Overlay.Static, SCREEN_HD - 32, offset_dict)  # Y Position (GB Counter)
    # Screen 1
    writeValue(ROM_COPY, 0x806AA996, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Medal)
    writeValue(ROM_COPY, 0x806AA9E6, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (Medal Tick)
    writeValue(ROM_COPY, 0x806AAAD2, Overlay.Static, SCREEN_HD - 0x25, offset_dict)  # Y Position (GB)
    writeValue(ROM_COPY, 0x806AAB72, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (BP)
    writeValue(ROM_COPY, 0x806AABD2, Overlay.Static, (SCREEN_HD >> 1) + 5, offset_dict)  # Y Position (BP Tick)
    writeValue(ROM_COPY, 0x806AAC22, Overlay.Static, SCREEN_HD >> 1, offset_dict)  # Y Position (Stick)
    # Screen 2
    writeValue(ROM_COPY, 0x806AB0A2, Overlay.Static, (SCREEN_HD >> 1) - 35, offset_dict)  # Y Position (Crown 1)
    writeValue(ROM_COPY, 0x806AB0EA, Overlay.Static, (SCREEN_HD >> 1) + 25, offset_dict)  # Y Position (Crown 2)
    writeValue(ROM_COPY, 0x806AB13E, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Fairy 1)
    writeValue(ROM_COPY, 0x806AB17A, Overlay.Static, (SCREEN_HD >> 1) + 30, offset_dict)  # Y Position (Fairy 2)
    writeValue(ROM_COPY, 0x806AB1B6, Overlay.Static, (SCREEN_HD >> 1) - 30, offset_dict)  # Y Position (Fairy 3)
    writeValue(ROM_COPY, 0x806AB1F2, Overlay.Static, (SCREEN_HD >> 1) + 30, offset_dict)  # Y Position (Fairy 4)
    writeValue(ROM_COPY, 0x806AAFAA, Overlay.Static, SCREEN_HD >> 1, offset_dict)  # Y Position (Crown)
    writeValue(ROM_COPY, 0x806AAFFE, Overlay.Static, SCREEN_HD >> 1, offset_dict)  # Y Position (Fairy 1)
    writeValue(ROM_COPY, 0x806AB03A, Overlay.Static, SCREEN_HD >> 1, offset_dict)  # Y Position (Fairy 2)
    writeValue(ROM_COPY, 0x806AB22E, Overlay.Static, SCREEN_HD - 0x25, offset_dict)  # Y Position (GB)
    # Generic
    writeValue(ROM_COPY, 0x806AB48E, Overlay.Static, SCREEN_HD - 0x28, offset_dict)  # Y Position (Z)
    writeValue(ROM_COPY, 0x806AB4C2, Overlay.Static, SCREEN_HD - 0x28, offset_dict)  # Y Position (R)

    # Cancel Transitions
    writeValue(ROM_COPY, 0x80628508, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x80683A2C, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806A84F8, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806AD090, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806DB540, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806DB92C, Overlay.Static, 0, offset_dict, 4)
    # HUD
    writeValue(ROM_COPY, 0x806FF0F2, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of Cannon Cursor
    writeValue(ROM_COPY, 0x806FF0F6, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of Cannon Cursor
    writeValue(ROM_COPY, 0x806FF3AA, Overlay.Static, (SCREEN_WD / 2) - 80, offset_dict)  # X Position of Upper-Left of Capture Marker
    writeValue(ROM_COPY, 0x806FF3AE, Overlay.Static, (SCREEN_HD / 2) - 80, offset_dict)  # Y Position of Upper-Left of Capture Marker
    writeValue(ROM_COPY, 0x806FF3EE, Overlay.Static, (SCREEN_WD / 2) + 80, offset_dict)  # X Position of Upper-Right of Capture Marker
    writeValue(ROM_COPY, 0x806FF3F2, Overlay.Static, (SCREEN_HD / 2) - 80, offset_dict)  # Y Position of Upper-Right of Capture Marker
    writeValue(ROM_COPY, 0x806FF436, Overlay.Static, (SCREEN_WD / 2) + 80, offset_dict)  # X Position of Lower-Right of Capture Marker
    writeValue(ROM_COPY, 0x806FF43A, Overlay.Static, (SCREEN_HD / 2) + 80, offset_dict)  # Y Position of Lower-Right of Capture Marker
    writeValue(ROM_COPY, 0x806FF47E, Overlay.Static, (SCREEN_WD / 2) - 80, offset_dict)  # X Position of Lower-Left of Capture Marker
    writeValue(ROM_COPY, 0x806FF482, Overlay.Static, (SCREEN_HD / 2) + 80, offset_dict)  # Y Position of Lower-Left of Capture Marker
    writeValue(ROM_COPY, 0x806FF4CE, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of Capture Center
    writeValue(ROM_COPY, 0x806FF4D2, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of Capture Center
    writeValue(ROM_COPY, 0x806FF566, Overlay.Static, SCREEN_WD - 40, offset_dict)  # X Position of Sad Face
    writeValue(ROM_COPY, 0x806FF5D2, Overlay.Static, SCREEN_WD - 40, offset_dict)  # X Position of Happy Face
    writeValue(ROM_COPY, 0x806FF692, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of Picture X Sign
    writeValue(ROM_COPY, 0x806FF696, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of Picture X Sign
    writeValue(ROM_COPY, 0x806FF70A, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of Picture Check Sign
    writeValue(ROM_COPY, 0x806FF70E, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of Picture Check Sign
    writeValue(ROM_COPY, 0x806FFAD6, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of Scope Cursor
    writeValue(ROM_COPY, 0x806FFADA, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of Scope Cursor
    writeValue(ROM_COPY, 0x806F8536, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (CBs)
    y_offset = 0x24 * (SCREEN_HD / 240)
    writeValue(ROM_COPY, 0x806F858E, Overlay.Static, 0x24 + y_offset, offset_dict)  # Y Position of HUD (GB Character)
    writeValue(ROM_COPY, 0x806F85CA, Overlay.Static, (SCREEN_WD / 2) + 34, offset_dict)  # X Position of HUD (Blueprints)
    writeValue(ROM_COPY, 0x806F85CE, Overlay.Static, SCREEN_HD - 30, offset_dict)  # Y Position of HUD (Blueprints)
    writeValue(ROM_COPY, 0x806F8606, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Medal - Multibunch)
    if not IsItemSelected(settings.quality_of_life, settings.misc_changes_selected, MiscChangesSelected.hud_hotkey):
        writeValue(ROM_COPY, 0x806F860A, Overlay.Static, SCREEN_HD - 30, offset_dict)  # Y Position of HUD (Medal - Multibunch)
    writeValue(ROM_COPY, 0x806F8642, Overlay.Static, (SCREEN_WD / 2) - 38, offset_dict)  # X Position of HUD (GB Bottom)
    writeValue(ROM_COPY, 0x806F8646, Overlay.Static, SCREEN_HD - 30, offset_dict)  # Y Position of HUD (GB Bottom)
    writeValue(ROM_COPY, 0x806F868E, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Crystals)
    writeValue(ROM_COPY, 0x806F86C6, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Standard Ammo)
    writeValue(ROM_COPY, 0x806F873A, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Homing Ammo)
    writeValue(ROM_COPY, 0x806F87A6, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Oranges)
    writeValue(ROM_COPY, 0x806F8812, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Film)
    writeValue(ROM_COPY, 0x806F8816, Overlay.Static, SCREEN_HD - 30, offset_dict)  # Y Position of HUD (Film)
    writeValue(ROM_COPY, 0x806F8852, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Race Coin)
    writeValue(ROM_COPY, 0x806F88CA, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Banana Coins)
    writeValue(ROM_COPY, 0x806F893A, Overlay.Static, SCREEN_WD - 30, offset_dict)  # X Position of HUD (Instrument)
    writeValue(ROM_COPY, 0x806FEFD2, Overlay.Static, SCREEN_WD / 2, offset_dict)  # X Position of cannon game reticle
    writeValue(ROM_COPY, 0x806FEFD6, Overlay.Static, SCREEN_HD / 2, offset_dict)  # Y Position of cannon game reticle
    writeValue(ROM_COPY, 0x80708906, Overlay.Static, SCREEN_WD << 1, offset_dict)  # X Position of Melons in UI
    writeValue(ROM_COPY, 0x8068D98E, Overlay.Static, SCREEN_WD - 40, offset_dict)  # X Position of Camera Icon
    writeValue(ROM_COPY, 0x8068D98A, Overlay.Static, SCREEN_HD - 30, offset_dict)  # Y Position of Camera Icon
    writeValue(ROM_COPY, 0x806ACB4E, Overlay.Static, (SCREEN_WD * 2) - 280, offset_dict)  # X Position of Try Again Text
    writeValue(ROM_COPY, 0x806ACB5A, Overlay.Static, (SCREEN_HD * 2) - 220, offset_dict)  # Y Position of Try Again Text
    writeValue(ROM_COPY, 0x806ACB9E, Overlay.Static, (SCREEN_WD * 2) - 120, offset_dict)  # X Position of Yes Text
    writeValue(ROM_COPY, 0x806ACBA6, Overlay.Static, (SCREEN_HD * 2) - 80, offset_dict)  # Y Position of Yes Text
    writeValue(ROM_COPY, 0x806ACBE2, Overlay.Static, (SCREEN_WD * 2) - 120, offset_dict)  # X Position of No Text
    writeValue(ROM_COPY, 0x806ACBEA, Overlay.Static, (SCREEN_HD * 2) + 60, offset_dict)  # Y Position of No Text
    # Scissor
    writeValue(ROM_COPY, 0x805FB9F8, Overlay.Static, 0x24190000 | (SCREEN_WD - 1), offset_dict, 4)  # Scissor Width for Jetpac and DK Arcade
    writeValue(ROM_COPY, 0x805FBA0C, Overlay.Static, 0x24090000 | (SCREEN_HD - 1), offset_dict, 4)  # Scissor Height for Jetpac and Arcade
    writeValue(ROM_COPY, 0x805FBB04, Overlay.Static, 0x24090000 | (SCREEN_WD - 11), offset_dict, 4)  # Scissor Right Edge for Game
    writeValue(ROM_COPY, 0x805FBB18, Overlay.Static, 0x240B0000 | (SCREEN_HD - 11), offset_dict, 4)  # Scissor Bottom Edge for Game
    writeValue(ROM_COPY, 0x805FBBF4, Overlay.Static, 0x24180000 | SCREEN_WD, offset_dict, 4)  # Screen Width for Framebuffer
    writeValue(ROM_COPY, 0x805FBC0C, Overlay.Static, 0x240F0000 | SCREEN_HD, offset_dict, 4)  # Screen Height for Framebuffer
    writeValue(ROM_COPY, 0x805FBC24, Overlay.Static, 0x24040000, offset_dict, 4)  # Remove Black Bars
    noise_scissor = ((SCREEN_WD - 11) << 14) | ((SCREEN_HD - 11) << 2)
    writeValue(ROM_COPY, 0x8070368A, Overlay.Static, (noise_scissor >> 16) & 0xFFFF, offset_dict)  # Upper Part of Noise Scissor
    writeValue(ROM_COPY, 0x8070369A, Overlay.Static, noise_scissor & 0xFFFF, offset_dict)  # Lower Part of Noise Scissor
    noise_scissor_gfx = 0xF6000000 | ((SCREEN_WD - 11) << 14)
    writeValue(ROM_COPY, 0x807036AE, Overlay.Static, (noise_scissor_gfx >> 16) & 0xFFFF, offset_dict)  # Upper Part of Noise Rectangle
    writeValue(ROM_COPY, 0x807036B2, Overlay.Static, noise_scissor_gfx & 0xFFFF, offset_dict)  # Lower Part of Noise Rectangle
    # Change fairy picture viewport target
    writeValue(ROM_COPY, 0x806C5DB6, Overlay.Static, (SCREEN_WD >> 1) - 22, offset_dict)  # X Minimum
    writeValue(ROM_COPY, 0x806C5DC6, Overlay.Static, (SCREEN_WD >> 1) + 22, offset_dict)  # X Maximum
    writeValue(ROM_COPY, 0x806C5DD6, Overlay.Static, (SCREEN_HD >> 1) - 22, offset_dict)  # Y Minimum
    writeValue(ROM_COPY, 0x806C5DDE, Overlay.Static, (SCREEN_HD >> 1) + 22, offset_dict)  # Y Maximum
