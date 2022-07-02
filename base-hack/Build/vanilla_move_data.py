"""Get vanilla move data."""
from typing import BinaryIO

special_move_prices = [3, 5, 7]
gun_price = 3
ins_price = 3
slam_prices = [5, 7]
gun_upg_prices = [5, 7]
ammo_belt_prices = [3, 5]
ins_upg_prices = [5, 7, 9]

cranky_0 = [0x01, 0x02, 0x03, 0xF0, 0x12, 0xF0, 0x13]
cranky_1 = [0x01, 0xF0, 0x02, 0xF0, 0x12, 0x03, 0x13]
funky = [0x21, 0xF0, 0x31, 0xF0, 0x22, 0x32, 0x23]
candy = [0xF0, 0x41, 0xF0, 0x42, 0xF0, 0x43, 0x44]
cranky_arr = [cranky_0, cranky_0, cranky_0, cranky_1, cranky_1]

move_offset = 0xA8
price_offset = 0x36
space_offset = 0x1FED020


def getWrite(value, kong):
    """Get value of move."""
    type = (value >> 4) & 0xF
    if type == 0xF:
        type = 5
    if type == 5:
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
    fh.seek(space_offset + move_offset)
    for x in range(5):
        for y in range(7):
            fh.write(bytearray([getWrite(cranky_arr[x][y], x)]))
    for x in range(5):
        for y in range(7):
            fh.write(bytearray([getWrite(funky[y], x)]))
    for x in range(5):
        for y in range(7):
            fh.write(bytearray([getWrite(candy[y], x)]))
