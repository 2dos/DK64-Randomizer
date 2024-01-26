"""Get vanilla move data."""

from typing import BinaryIO

special_move_prices = [3, 5, 7]
gun_price = 3
ins_price = 3
slam_prices = [5, 7]
gun_upg_prices = [5, 7]
ammo_belt_prices = [3, 5]
ins_upg_prices = [5, 7, 9]

DEFAULT_SLAM_PURCHASE = 1


class MoveType:
    """Class which stores info about move types."""

    def __init__(self, type, index=1, price=0):
        """Initialize with given data."""
        self.type = type
        self.index = index
        self.price = price


cranky_0 = [
    MoveType("special", 1, 3),
    MoveType("special", 2, 5),
    MoveType("special", 3, 7),
    MoveType("nothing"),
    MoveType("slam", DEFAULT_SLAM_PURCHASE, 5),
    MoveType("nothing"),
    MoveType("slam", DEFAULT_SLAM_PURCHASE, 7),
    MoveType("nothing"),
]
cranky_1 = [
    MoveType("special", 1, 3),
    MoveType("nothing"),
    MoveType("special", 2, 5),
    MoveType("nothing"),
    MoveType("slam", DEFAULT_SLAM_PURCHASE, 5),
    MoveType("special", 3, 7),
    MoveType("slam", DEFAULT_SLAM_PURCHASE, 7),
    MoveType("nothing"),
]

funky = [MoveType("gun", 1, 3), MoveType("nothing"), MoveType("ammo_belt", 1, 3), MoveType("nothing"), MoveType("gun", 2, 5), MoveType("ammo_belt", 2, 5), MoveType("gun", 3, 7), MoveType("nothing")]

candy = [
    MoveType("nothing"),
    MoveType("instrument", 1, 3),
    MoveType("nothing"),
    MoveType("instrument", 2, 5),
    MoveType("nothing"),
    MoveType("instrument", 3, 7),
    MoveType("instrument", 3, 9),
    MoveType("nothing"),
]

cranky_moves = {"dk": cranky_0.copy(), "diddy": cranky_0.copy(), "lanky": cranky_1.copy(), "tiny": cranky_1.copy(), "chunky": cranky_1.copy()}

funky_moves = {"dk": funky.copy(), "diddy": funky.copy(), "lanky": funky.copy(), "tiny": funky.copy(), "chunky": funky.copy()}

candy_moves = {"dk": candy.copy(), "diddy": candy.copy(), "lanky": candy.copy(), "tiny": candy.copy(), "chunky": candy.copy()}

training = {"dive": MoveType("flag", 0x182), "orange": MoveType("flag", 0x184), "barrel": MoveType("flag", 0x185), "vine": MoveType("flag", 0x183)}

bfi = {"bfi": MoveType("flag", -2)}

first_move = {"base_slam": MoveType("nothing")}


def convertItem(item: dict, kong: int) -> int:
    """Convert move item to encoded int."""
    master_info = 0
    flag = 0xFFFF  # -1
    types = ["special", "slam", "gun", "ammo_belt", "instrument", "flag", "gb"]
    flag_types = ["flag", "gb"]
    shared_types = ["slam", "ammo_belt"]  # Instrument covered by diff
    if item.type == "nothing":
        master_info = 7 << 5
    elif item.type in types:
        master_info = (types.index(item.type) & 7) << 5
        move_kong = kong & 7
        if item.type in shared_types:
            move_kong = 0
        elif item.type == "instrument":
            if item.index > 1:
                move_kong = 0
        move_lvl = (item.index - 1) & 3
        master_info |= move_lvl << 3
        master_info |= move_kong
        if item.type in flag_types:
            flag = item.index
            if flag < 0:
                flag += 65536
    return (master_info << 24) | (item.price << 16) | flag


price_offset = 0x36
space_offset = 0x1FED020
move_offset = 0x1FEF000


def getWrite(value, kong):
    """Get value of move."""
    type = (value >> 4) & 0xF
    if type == 0xF:
        type = 7
    if type == 7:
        move_v = 0
    else:
        move_v = (value & 0xF) - 1

    ret = ((type & 7) << 5) | ((move_v & 3) << 3) | (kong & 7)
    # print(f"{hex(ret)}: {type} | {move_v} | {kong}")
    return ret


def writeVanillaMoveData(fh):
    """Write vanilla move data."""
    print("Writing vanilla move data")
    # Prices
    fh.seek(space_offset + 0x45)
    fh.write(bytearray(slam_prices))
    fh.seek(space_offset + 0x53)
    fh.write(bytearray(ammo_belt_prices))
    fh.write(bytearray(ins_upg_prices))
    # Space Data
    fh.seek(move_offset)
    for x in range(int(0x400 / 4)):
        fh.write((0).to_bytes(4, "big"))
    fh.seek(move_offset)
    move_blocks = [cranky_moves, funky_moves, candy_moves]
    for block in move_blocks:
        for kong_index, kong in enumerate(block):
            for level in block[kong]:
                fh.write(convertItem(level, kong_index).to_bytes(4, "big"))
    for training_barrel in training:
        training_item = training[training_barrel]
        fh.write(convertItem(training_item, 0).to_bytes(4, "big"))
    fh.write(convertItem(bfi["bfi"], 0).to_bytes(4, "big"))
    fh.write(convertItem(first_move["base_slam"], 0).to_bytes(4, "big"))
