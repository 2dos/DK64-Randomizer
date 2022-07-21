"""Randomize puzzles."""
import random
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def chooseSFX():
    """Choose random SFX from bank of acceptable SFX."""
    banks = [
        [98, 138],
        [166, 252],
        [398, 411],
        [471, 476],
        [519, 535],
        [547, 575],
        [614, 631],
        [644, 650],
    ]
    bank = random.choice(banks)
    return random.randint(bank[0], bank[1])


def randomize_puzzles(spoiler: Spoiler):
    """Shuffle elements of puzzles. Currently limited to coin challenge requirements but will be extended in future."""
    if spoiler.settings.puzzle_rando:
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
        chosen_sounds = []
        for matching_head in range(8):
            ROM().seek(0x1FED020 + 0x14C + (2 * matching_head))
            sfx = chooseSFX()
            while sfx in chosen_sounds:
                sfx = chooseSFX()
            chosen_sounds.append(sfx)
            ROM().writeMultipleBytes(sfx, 2)
        for piano_item in range(7):
            ROM().seek(0x1FED0020 + 0x15C + piano_item)
            key = random.randint(0, 5)
            ROM().writeMultipleBytes(key, 1)
