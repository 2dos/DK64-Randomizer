"""Randomize Move Locations."""
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler

# /* 0x0A7 */ char move_rando_on; // O = No Move Randomization. 1 = On.
# /* 0x0A8 */ unsigned char dk_crankymoves[7]; // First 4 bits indicates the moves type, 0 = Moves, 1 = Slam, 2 = Guns, 3 = Ammo Belt, 4 = Instrument, 0xF = No Upgrade. Last 4 bits indicate move level (eg. 1 = Baboon Blast, 2 = Strong Kong, 3 = Gorilla Grab). Each item in the array indicates the level it is given (eg. 1st slot is purchased in Japes, 2nd for Aztec etc.)
# /* 0x0AF */ unsigned char diddy_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0B6 */ unsigned char lanky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0BD */ unsigned char tiny_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0C4 */ unsigned char chunky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0CB */ unsigned char dk_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D2 */ unsigned char diddy_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D9 */ unsigned char lanky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E0 */ unsigned char tiny_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E7 */ unsigned char chunky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0EE */ unsigned char dk_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0F5 */ unsigned char diddy_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0FC */ unsigned char lanky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x103 */ unsigned char tiny_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x10A */ unsigned char chunky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi

varspaceOffset = 0x1FED020  # TODO: Define this as constant in a more global place
moveRandoOffset = 0x0A7

dk_crankymoves = []
diddy_crankymoves = []
lanky_crankymoves = []
tiny_crankymoves = []
chunky_crankymoves = []
dk_funkymoves = []
diddy_funkymoves = []
lanky_funkymoves = []
tiny_funkymoves = []
chunky_funkymoves = []
dk_candymoves = []
diddy_candymoves = []
lanky_candymoves = []
tiny_candymoves = []
chunky_candymoves = []


def randomize_moves(spoiler: Spoiler):
    """Randomize Move locations based on move_data from spoiler."""
    if spoiler.settings.shuffle_items == "moves" and spoiler.move_data is not None:
        # Take a copy of move_data before modifying
        move_arrays = spoiler.move_data.copy()
        for shop in range(3):
            for kong in range(5):
                for level in range(7):
                    if move_arrays[shop][kong][level] == 0:
                        move_arrays[shop][kong][level] = 0xFF

        dk_crankymoves = move_arrays[0][0]
        diddy_crankymoves = move_arrays[0][1]
        lanky_crankymoves = move_arrays[0][2]
        tiny_crankymoves = move_arrays[0][3]
        chunky_crankymoves = move_arrays[0][4]
        dk_funkymoves = move_arrays[1][0]
        diddy_funkymoves = move_arrays[1][1]
        lanky_funkymoves = move_arrays[1][2]
        tiny_funkymoves = move_arrays[1][3]
        chunky_funkymoves = move_arrays[1][4]
        dk_candymoves = move_arrays[2][0]
        diddy_candymoves = move_arrays[2][1]
        lanky_candymoves = move_arrays[2][2]
        tiny_candymoves = move_arrays[2][3]
        chunky_candymoves = move_arrays[2][4]

        ROM().seek(varspaceOffset + moveRandoOffset)
        ROM().write(0x1)
        ROM().writeBytes(bytearray(dk_crankymoves))
        ROM().writeBytes(bytearray(diddy_crankymoves))
        ROM().writeBytes(bytearray(lanky_crankymoves))
        ROM().writeBytes(bytearray(tiny_crankymoves))
        ROM().writeBytes(bytearray(chunky_crankymoves))
        ROM().writeBytes(bytearray(dk_funkymoves))
        ROM().writeBytes(bytearray(diddy_funkymoves))
        ROM().writeBytes(bytearray(lanky_funkymoves))
        ROM().writeBytes(bytearray(tiny_funkymoves))
        ROM().writeBytes(bytearray(chunky_funkymoves))
        ROM().writeBytes(bytearray(dk_candymoves))
        ROM().writeBytes(bytearray(diddy_candymoves))
        ROM().writeBytes(bytearray(lanky_candymoves))
        ROM().writeBytes(bytearray(tiny_candymoves))
        ROM().writeBytes(bytearray(chunky_candymoves))
