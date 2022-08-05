"""Get vanilla move data."""
from typing import BinaryIO

special_move_prices = [3, 5, 7]
gun_price = 3
ins_price = 3
slam_prices = [5, 7]
gun_upg_prices = [5, 7]
ammo_belt_prices = [3, 5]
ins_upg_prices = [5, 7, 9]

cranky_0 = [
    {
        "item_type": "special",
        "item_index": 1,
    },
    {
        "item_type": "special",
        "item_index": 2,
    },
    {
        "item_type": "special",
        "item_index": 3,
    },
    {"item_type": "nothing"},
    {
        "item_type": "slam",
        "item_index": 2,
    },
    {"item_type": "nothing"},
    {
        "item_type": "slam",
        "item_index": 3,
    },
    {
        "item_type": "nothing"
    }
]
cranky_1 = [
    {
        "item_type": "special",
        "item_index": 1,
    },
    {
        "item_type": "nothing",
    },
    {
        "item_type": "special",
        "item_index": 2,
    },
    {"item_type": "nothing"},
    {
        "item_type": "slam",
        "item_index": 2,
    },
    {
        "item_type": "special",
        "item_index": 3,
    },
    {
        "item_type": "slam",
        "item_index": 3,
    },
    {
        "item_type": "nothing"
    }
]

funky = [
    {
        "item_type": "gun",
        "item_index": 1,
    },
    {
        "item_type": "nothing"
    },
    {
        "item_type": "ammo_belt",
        "item_index": 1,
    },
    {
        "item_type": "nothing",
    },
    {
        "item_type": "gun",
        "item_index": 2,
    },
    {
        "item_type": "ammo_belt",
        "item_index": 2,
    },
    {
        "item_type": "gun",
        "item_index": 3,
    },
    {
        "item_type": "nothing"
    }
]

candy = [
    {
        "item_type": "nothing"
    },
    {
        "item_type": "instrument",
        "item_index": 1,
    },
    {
        "item_type": "nothing"
    },
    {
        "item_type": "instrument",
        "item_index": 2,
    },
    {
        "item_type": "nothing"
    },
    {
        "item_type": "instrument",
        "item_index": 3,
    },
    {
        "item_type": "instrument",
        "item_index": 4,
    },
    {
        "item_type": "nothing"
    }
]

cranky_moves = {
    "dk": cranky_0.copy(),
    "diddy": cranky_0.copy(),
    "lanky": cranky_1.copy(),
    "tiny": cranky_1.copy(),
    "chunky": cranky_1.copy(),
}

funky_moves = {
    "dk": funky.copy(),
    "diddy": funky.copy(),
    "lanky": funky.copy(),
    "tiny": funky.copy(),
    "chunky": funky.copy(),
}

candy_moves = {
    "dk": candy.copy(),
    "diddy": candy.copy(),
    "lanky": candy.copy(),
    "tiny": candy.copy(),
    "chunky": candy.copy(),
}

training = {
    "dive": {
        "item_type": "flag",
        "flag": 0x182
    },
    "orange": {
        "item_type": "flag",
        "flag": 0x184
    },
    "barrel": {
        "item_type": "flag",
        "flag": 0x185
    },
    "vine": {
        "item_type": "flag",
        "flag": 0x183
    },
}

bfi = {
    "item_type": "flag",
    "flag": -2, # Both BFI Moves
}

def convertItem(item: dict, kong: int) -> int:
    """Convert move item to encoded int."""
    master_info = 0
    text_index = 0
    flag = 0xFFFF # -1
    types = ["special","slam","gun","ammo_belt","instrument","flag","gb"]
    flag_types = ["flag","gb"]
    shared_types = ["slam","ammo_belt"] # Instrument covered by diff
    if item["item_type"] == "nothing":
        master_info = 7 << 5
    elif item["item_type"] in types:
        master_info = (types.index(item["item_type"]) & 7) << 5
        move_kong = kong & 7
        if item["item_type"] in shared_types:
            move_kong = 0
        elif item["item_type"] == "instrument":
            if item["item_index"] > 1:
                move_kong = 0
        move_lvl = 0
        if "item_index" in item:
            move_lvl = (item["item_index"] - 1) & 3
        master_info |= (move_lvl << 3)
        master_info |= move_kong
        if item["item_type"] in flag_types:
            flag = item["flag"]
            if flag < 0:
                flag += 65536
    return (master_info << 24) | (text_index << 16) | flag


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
    fh.seek(space_offset + price_offset)
    for x in range(5):
        fh.write(bytearray(special_move_prices))
    fh.write(bytearray(slam_prices))
    for x in range(5):
        fh.write(bytearray([gun_price]))
    for x in range(5):
        fh.write(bytearray([ins_price]))
    fh.write(bytearray(gun_upg_prices))
    fh.write(bytearray(ammo_belt_prices))
    fh.write(bytearray(ins_upg_prices))
    # Space Data
    fh.seek(move_offset)
    for x in range(int(0x400/4)):
        fh.write((0).to_bytes(4,"big"))
    fh.seek(move_offset)
    move_blocks = [cranky_moves,funky_moves,candy_moves]
    for block in move_blocks:
        for kong_index, kong in enumerate(block):
            for level in block[kong]:
                fh.write(convertItem(level,kong_index).to_bytes(4,"big"))
    for training_barrel in training:
        training_item = training[training_barrel]
        fh.write(convertItem(training_item,0).to_bytes(4,"big"))
    fh.write(convertItem(bfi,0).to_bytes(4,"big"))