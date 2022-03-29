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

move_offset = 0xA8
price_offset = 0x36
space_offset = 0x1FED020


def writeVanillaMoveData(fh):
    """Write vanilla move data."""
    print("Writing vanilla move data")
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
    fh.seek(space_offset + move_offset)
    for x in range(2):
        fh.write(bytearray(cranky_0))
    for x in range(3):
        fh.write(bytearray(cranky_1))
    for x in range(5):
        fh.write(bytearray(funky))
    for x in range(5):
        fh.write(bytearray(candy))
