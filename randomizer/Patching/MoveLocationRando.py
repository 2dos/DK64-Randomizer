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


def writeMoveDataToROM(arr: list):
    """Write move data to ROM."""
    for x in arr:
        if x["move_type"] == "flag":
            flag_dict = {"dive": 0x182, "orange": 0x184, "barrel": 0x185, "vine": 0x183, "camera": 0x2FD, "shockwave": 0x179, "camera_shockwave": 0xFFFE}
            flag_index = 0xFFFF
            if x["flag"] in flag_dict:
                flag_index = flag_dict[x["flag"]]
            ROM().writeMultipleBytes(5 << 5, 1)
            ROM().writeMultipleBytes(x["price"], 1)
            ROM().writeMultipleBytes(flag_index, 2)
        elif x["move_type"] is None:
            ROM().writeMultipleBytes(7 << 5, 1)
            ROM().writeMultipleBytes(0, 1)
            ROM().writeMultipleBytes(0xFFFF, 2)
        else:
            move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
            data = move_types.index(x["move_type"]) << 5 | (x["move_lvl"] << 3) | x["move_kong"]
            ROM().writeMultipleBytes(data, 1)
            ROM().writeMultipleBytes(x["price"], 1)
            ROM().writeMultipleBytes(0xFFFF, 2)


def randomize_moves(spoiler: Spoiler):
    """Randomize Move locations based on move_data from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    movespaceOffset = spoiler.settings.move_location_data
    if spoiler.settings.move_rando not in ("off", "starts_with") and spoiler.move_data is not None:
        # Take a copy of move_data before modifying
        move_arrays = spoiler.move_data.copy()

        dk_crankymoves = move_arrays[0][0][0]
        diddy_crankymoves = move_arrays[0][0][1]
        lanky_crankymoves = move_arrays[0][0][2]
        tiny_crankymoves = move_arrays[0][0][3]
        chunky_crankymoves = move_arrays[0][0][4]
        dk_funkymoves = move_arrays[0][1][0]
        diddy_funkymoves = move_arrays[0][1][1]
        lanky_funkymoves = move_arrays[0][1][2]
        tiny_funkymoves = move_arrays[0][1][3]
        chunky_funkymoves = move_arrays[0][1][4]
        dk_candymoves = move_arrays[0][2][0]
        diddy_candymoves = move_arrays[0][2][1]
        lanky_candymoves = move_arrays[0][2][2]
        tiny_candymoves = move_arrays[0][2][3]
        chunky_candymoves = move_arrays[0][2][4]

        training_moves = move_arrays[1]
        bfi_move = move_arrays[2]

        ROM().seek(varspaceOffset + moveRandoOffset)
        ROM().write(0x1)
        ROM().seek(movespaceOffset)
        writeMoveDataToROM(dk_crankymoves)
        writeMoveDataToROM(diddy_crankymoves)
        writeMoveDataToROM(lanky_crankymoves)
        writeMoveDataToROM(tiny_crankymoves)
        writeMoveDataToROM(chunky_crankymoves)
        writeMoveDataToROM(dk_funkymoves)
        writeMoveDataToROM(diddy_funkymoves)
        writeMoveDataToROM(lanky_funkymoves)
        writeMoveDataToROM(tiny_funkymoves)
        writeMoveDataToROM(chunky_funkymoves)
        writeMoveDataToROM(dk_candymoves)
        writeMoveDataToROM(diddy_candymoves)
        writeMoveDataToROM(lanky_candymoves)
        writeMoveDataToROM(tiny_candymoves)
        writeMoveDataToROM(chunky_candymoves)
        writeMoveDataToROM(training_moves)
        writeMoveDataToROM(bfi_move)
