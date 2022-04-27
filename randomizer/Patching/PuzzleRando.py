"""Randomize puzzles."""
import random
from randomizer.Patching.Patcher import ROM


def randomize_puzzles():
    """Shuffle elements of puzzles. Currently limited to coin challenge requirements but will be extended in future."""
    coin_req_info = [
        {"offset": 0x12C, "coins": random.randint(10, 50)},  # Caves Beetle
        {"offset": 0x12D, "coins": random.randint(20, 50)},  # Aztec Beetle
        {"offset": 0x12E, "coins": random.randint(5, 15)},  # Factory Car
        {"offset": 0x12F, "coins": random.randint(5, 12)},  # Seal Race
        {"offset": 0x130, "coins": random.randint(5, 15)},  # Castle Car
        {"offset": 0x131, "coins": random.randint(40, 70)},  # Japes Cart
        {"offset": 0x132, "coins": random.randint(25, 55)},  # Fungi Cart
        {"offset": 0x133, "coins": random.randint(5, 45)},  # Castle Cart
    ]
    for coinreq in coin_req_info:
        ROM().seek(0x1FED020 + coinreq["offset"])
        ROM().writeMultipleBytes(coinreq["coins"], 1)
