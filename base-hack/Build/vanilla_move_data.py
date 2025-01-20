"""Get vanilla move data."""

from typing import BinaryIO
from enum import IntEnum, auto

special_move_prices = [3, 5, 7]
gun_price = 3
ins_price = 3
slam_prices = [5, 7]
gun_upg_prices = [5, 7]
ammo_belt_prices = [3, 5]
ins_upg_prices = [5, 7, 9]

DEFAULT_SLAM_PURCHASE = 1


class MoveIndexes(IntEnum):
    """Enum for move indexes."""

    special = 0
    slam = auto()
    gun = auto()
    ammo_belt = auto()
    instrument = auto()
    flag = auto()
    gb = auto()
    nothing = auto()


class MoveType:
    """Class which stores info about move types."""

    def __init__(self, type: MoveIndexes, index=1, price=0):
        """Initialize with given data."""
        self.type = type
        self.index = index
        self.price = price


cranky_0 = [
    MoveType(MoveIndexes.special, 1, 3),
    MoveType(MoveIndexes.special, 2, 5),
    MoveType(MoveIndexes.special, 3, 7),
    MoveType(MoveIndexes.special, 3, 7),
    MoveType(MoveIndexes.slam, DEFAULT_SLAM_PURCHASE, 5),
    MoveType(MoveIndexes.nothing),
    MoveType(MoveIndexes.slam, DEFAULT_SLAM_PURCHASE, 7),
    MoveType(MoveIndexes.nothing),
]
cranky_1 = [
    MoveType(MoveIndexes.special, 1, 3),
    MoveType(MoveIndexes.special, 1, 3),
    MoveType(MoveIndexes.special, 2, 5),
    MoveType(MoveIndexes.special, 2, 5),
    MoveType(MoveIndexes.slam, DEFAULT_SLAM_PURCHASE, 5),
    MoveType(MoveIndexes.special, 3, 7),
    MoveType(MoveIndexes.slam, DEFAULT_SLAM_PURCHASE, 7),
    MoveType(MoveIndexes.nothing),
]

funky = [
    MoveType(MoveIndexes.gun, 1, 3),
    MoveType(MoveIndexes.gun, 1, 3),
    MoveType(MoveIndexes.ammo_belt, 1, 3),
    MoveType(MoveIndexes.nothing),
    MoveType(MoveIndexes.gun, 2, 5),
    MoveType(MoveIndexes.ammo_belt, 2, 5),
    MoveType(MoveIndexes.gun, 3, 7),
    MoveType(MoveIndexes.nothing),
]

candy = [
    MoveType(MoveIndexes.instrument, 1, 3),
    MoveType(MoveIndexes.instrument, 1, 3),
    MoveType(MoveIndexes.instrument, 1, 3),
    MoveType(MoveIndexes.instrument, 2, 5),
    MoveType(MoveIndexes.nothing),
    MoveType(MoveIndexes.instrument, 3, 7),
    MoveType(MoveIndexes.instrument, 3, 9),
    MoveType(MoveIndexes.nothing),
]

cranky_moves = {"dk": cranky_0.copy(), "diddy": cranky_0.copy(), "lanky": cranky_1.copy(), "tiny": cranky_1.copy(), "chunky": cranky_1.copy()}

funky_moves = {"dk": funky.copy(), "diddy": funky.copy(), "lanky": funky.copy(), "tiny": funky.copy(), "chunky": funky.copy()}

candy_moves = {"dk": candy.copy(), "diddy": candy.copy(), "lanky": candy.copy(), "tiny": candy.copy(), "chunky": candy.copy()}

training = {
    "dive": MoveType(MoveIndexes.flag, 0x182),
    "orange": MoveType(MoveIndexes.flag, 0x184),
    "barrel": MoveType(MoveIndexes.flag, 0x185),
    "vine": MoveType(MoveIndexes.flag, 0x183),
}

bfi = {"bfi": MoveType(MoveIndexes.flag, -2)}

first_move = {"base_slam": MoveType(MoveIndexes.nothing)}


def convertItem(fh: BinaryIO, item: dict, kong: int) -> int:
    """Convert move item to encoded int."""
    flag_types = [MoveIndexes.flag, MoveIndexes.gb]
    shared_types = [MoveIndexes.slam, MoveIndexes.ammo_belt]  # Instrument covered by diff
    # Item Type
    fh.write(int(item.type).to_bytes(2, "big"))
    # Flag/Item Level
    index = item.index
    if item.type in flag_types:
        if index < 0:
            index += 65536
    else:
        if index > 0:
            index -= 1
    fh.write((index).to_bytes(2, "big"))
    # Move Kong
    move_kong = kong
    if item.type in shared_types:
        move_kong = 0
    elif item.type == MoveIndexes.instrument:
        if item.index > 1:
            move_kong = 0
    fh.write((move_kong).to_bytes(1, "big"))
    # Price
    fh.write((item.price).to_bytes(1, "big"))
    return


price_offset = 0x36
space_offset = 0x1FED020
move_offset = 0x1FEF000


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
                convertItem(fh, level, kong_index)
    for training_barrel in training:
        training_item = training[training_barrel]
        convertItem(fh, training_item, 0)
    convertItem(fh, bfi["bfi"], 0)
    convertItem(fh, first_move["base_slam"], 0)
