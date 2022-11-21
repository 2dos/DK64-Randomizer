"""Randomize puzzles."""
import random

from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def chooseSFX():
    """Choose random SFX from bank of acceptable SFX."""
    banks = [[98, 138], [166, 252], [398, 411], [471, 476], [519, 535], [547, 575], [614, 631], [644, 650]]
    bank = random.choice(banks)
    return random.randint(bank[0], bank[1])


def randomize_puzzles(spoiler: Spoiler):
    """Shuffle elements of puzzles. Currently limited to coin challenge requirements but will be extended in future."""
    sav = spoiler.settings.rom_data
    if spoiler.settings.puzzle_rando:
        race_requirements = {"factory_race": [5, 15], "castle_race": [5, 15], "seal_race": [5, 12]}
        if spoiler.settings.fast_gbs:
            race_requirements["factory_race"] = [3, 8]
            race_requirements["castle_race"] = [5, 12]
            race_requirements["seal_race"] = [5, 10]

        coin_req_info = [
            {"offset": 0x13C, "coins": random.randint(10, 50)},  # Caves Beetle
            {"offset": 0x13D, "coins": random.randint(20, 50)},  # Aztec Beetle
            {"offset": 0x13E, "coins": random.randint(race_requirements["factory_race"][0], race_requirements["factory_race"][1])},  # Factory Car
            {"offset": 0x13F, "coins": random.randint(race_requirements["seal_race"][0], race_requirements["seal_race"][1])},  # Seal Race
            {"offset": 0x140, "coins": random.randint(race_requirements["castle_race"][0], race_requirements["castle_race"][1])},  # Castle Car
            {"offset": 0x141, "coins": random.randint(40, 70)},  # Japes Cart
            {"offset": 0x142, "coins": random.randint(25, 55)},  # Fungi Cart
            {"offset": 0x143, "coins": random.randint(5, 45)},  # Castle Cart
        ]
        for coinreq in coin_req_info:
            ROM().seek(sav + coinreq["offset"])
            ROM().writeMultipleBytes(coinreq["coins"], 1)
        chosen_sounds = []
        for matching_head in range(8):
            ROM().seek(sav + 0x15C + (2 * matching_head))
            sfx = chooseSFX()
            while sfx in chosen_sounds:
                sfx = chooseSFX()
            chosen_sounds.append(sfx)
            ROM().writeMultipleBytes(sfx, 2)
        for piano_item in range(7):
            ROM().seek(sav + 0x16C + piano_item)
            key = random.randint(0, 5)
            ROM().writeMultipleBytes(key, 1)
        for face_puzzle_square in range(9):
            ROM().seek(sav + 0x17E + face_puzzle_square)  # DK Face Puzzle
            if face_puzzle_square == 8:
                ROM().writeMultipleBytes(random.choice([0, 1, 3]), 1)  # Lanky for this square glitches out the puzzle. Nice going Loser kong
            else:
                ROM().writeMultipleBytes(random.randint(0, 3), 1)
            ROM().seek(sav + 0x187 + face_puzzle_square)  # Chunky Face Puzzle
            if face_puzzle_square == 2:
                ROM().writeMultipleBytes(random.choice([0, 1, 3]), 1)  # Lanky for this square glitches out the puzzle. Nice going Loser kong again
            else:
                ROM().writeMultipleBytes(random.randint(0, 3), 1)
