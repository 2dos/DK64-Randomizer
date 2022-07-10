"""ROM TESTER.

Displays all values in the variable space in an easier-to-read format rather than a hex editor
***PURELY*** for debugging purposes
To use:
    - Place your modified Rando ROM in /rom_tester
    - Run this script
    - This script will spit out details for ALL .z64 files in /rom_tester, so if you only want data for a specific rom, make sure that's the only one in /rom_tester
"""
import os
from typing import BinaryIO

levels = ["Japes", "Aztec", "Factory", "Galleon", "Fungi", "Caves", "Castle", "Helm"]
keys = [0x1A, 0x4A, 0x8A, 0xA8, 0xEC, 0x124, 0x13D]
special_moves = [
    "Baboon Blast",
    "Strong Kong",
    "Gorilla Grab",
    "Chimpy Charge",
    "Rocketbarrel",
    "Simian Spring",
    "Orangstand",
    "Baboon Balloon",
    "Orangstand Sprint",
    "Mini Monkey",
    "Pony Tail Twirl",
    "Monkeyport",
    "Hunky Chunky",
    "Primate Punch",
    "Gorilla Gone",
    "Super Simian Slam",
    "Super Duper Simian Slam",
    "Coconut Gun",
    "Peanut Popguns",
    "Grape Shooter",
    "Feather Bow",
    "Pineapple Launcher",
    "Bongo Blast",
    "Guitar Gazump",
    "Trombone Tremor",
    "Saxaphone Slam",
    "Triangle Trample",
    "Homing Ammo",
    "Sniper Scope",
    "Ammo Belt 1",
    "Ammo Belt 2",
    "Instrument Upgrade 1",
    "3rd Melon",
    "Instrument Upgrade 2",
]
kongs = ["DK", "Diddy", "Lanky", "Tiny", "Chunky", "Krusha", "Rambi", "Enguarde"]
shops = ["Cranky", "Funky", "Candy"]
bosses = [
    {"name": "Army Dillo 1", "map": 0x8},
    {"name": "Dogadon 1", "map": 0xC5},
    {"name": "Mad Jack", "map": 0x9A},
    {"name": "Pufftoss", "map": 0x6F},
    {"name": "Dogadon 2", "map": 0x53},
    {"name": "Army Dillo 2", "map": 0xC4},
    {"name": "King Kut Out", "map": 0xC7},
]
move_types = ["Special Move", "Slam", "Gun", "Ammo Belt", "Instrument"]
key_goals = ["Angry Aztec", "Factory & Galleon", "K. Rool Part 1", "Fungi", "Caves & Castle", "Helm Part 1", "Helm Part 2"]


def getValue(fh, offset, size):
    """Get the value of the object."""
    fh.seek(0x1FED020 + offset)
    return int.from_bytes(fh.read(size), "big")


def getTrueFalse(fh, offset, size):
    """Get if the value is true or false."""
    val = getValue(fh, offset, size)
    if val != 0:
        return True
    return False


def getMapExit(fh, offset):
    """Get the current map exit."""
    val_m = getValue(fh, offset, 1)
    val_e = getValue(fh, offset + 1, 1)
    return f"Map {val_m}, Exit {val_e}"


def getKong(fh, offset):
    """Get the current kong."""
    val = getValue(fh, offset, 1)
    if val >= 0:
        if val < 8:
            return kongs[val]
    return f"Kong {hex(val)}"


def getMove(fh, offset):
    """Get the current move."""
    val = getValue(fh, offset, 1)
    move_type = (val >> 4) & 0xF
    move_lvl = val & 0xF
    if move_type == 0xF:
        return "No Upgrade"
    return f"{move_types[move_type]} level {str(move_lvl)}"


output_file = "output.txt"
if os.path.exists(output_file):
    os.remove(output_file)
with open(output_file, "w") as fh:
    print("Created File")


def output(string):
    """Write the output."""
    with open(output_file, "a") as fh:
        fh.write(string + "\n")


files = [f for f in os.listdir(".") if os.path.isfile(f)]
for f in files:
    if ".z64" in f:
        output(f"Analyzing {f}")
        with open(f, "rb") as fh:
            output(f"\tLevel Order Rando: {str(getTrueFalse(fh,0,1))}")
            output(f"\tLevel Order:")
            for x in range(7):
                idx_val = getValue(fh, 1 + x, 1)
                output(f"\t\t[{x}] - {levels[idx_val]} ({idx_val})")
            output(f"\tTroff 'n' Scoff Count:")
            for x in range(7):
                output(f"\t\t{levels[x]}: {getValue(fh,8+(2*x),2)}")
            output(f"\tB. Locker Requirement:")
            for x in range(8):
                output(f"\t\t{levels[x]} Lobby: {getValue(fh,0x16+x,1)}")
            output(f"\tKey Flags:")
            for x in range(7):
                key_str = ""
                flag_val = getValue(fh, 0x1E + (2 * x), 2)
                if flag_val in keys:
                    key_str = f" (Key {keys.index(flag_val)+1})"
                output(f"\t\tOpens {key_goals[x]}: {hex(flag_val)}{key_str}")
            output(f"\tUnlock Kongs: {str(getTrueFalse(fh,0x2C,1))}")
            output(f"\tUnlock Moves: {str(getTrueFalse(fh,0x2D,1))}")
            output(f"\tFast Start (Beginning): {str(getTrueFalse(fh,0x2E,1))}")
            output(f"\tCamera Unlocked: {str(getTrueFalse(fh,0x2F,1))}")
            output(f"\tTag Anywhere: {str(getTrueFalse(fh,0x30,1))}")
            output(f"\tFast Start (Helm): {str(getTrueFalse(fh,0x31,1))}")
            output(f"\tCrown Door Open: {str(getTrueFalse(fh,0x32,1))}")
            output(f"\tCoin Door Open: {str(getTrueFalse(fh,0x33,1))}")
            output(f"\tQuality of Life changes: {str(getTrueFalse(fh,0x34,1))}")
            output(f"\tPrice Rando On: {str(getTrueFalse(fh,0x35,1))}")
            for x in range(34):
                output(f"\t\t{special_moves[x]}: {getValue(fh,0x36+x,1)}")
            output(f"\tK Rool Order:")
            for x in range(5):
                output(f"\t\t[{x}] - {getKong(fh,0x58+x)} Phase")
            output(f"\tRandomize More Loading Zones: {str(getTrueFalse(fh,0x5D,1))}")
            output(f"\t\tAztec Beetle Enter: {getMapExit(fh,0x5E)}")
            output(f"\t\tAztec Beetle Exit: {getMapExit(fh,0x60)}")
            output(f"\t\tCaves Beetle Exit: {getMapExit(fh,0x62)}")
            output(f"\t\tSeal Race Exit: {getMapExit(fh,0x64)}")
            output(f"\t\tFactory Car Exit: {getMapExit(fh,0x66)}")
            output(f"\t\tCastle Car Exit: {getMapExit(fh,0x68)}")
            output(f"\t\tSeasick Ship Enter: {getMapExit(fh,0x6A)}")
            output(f"\t\tFungi Minecart Enter: {getMapExit(fh,0x6C)}")
            output(f"\t\tFungi Minecart Exit: {getMapExit(fh,0x6E)}")
            output(f"\t\tJapes Minecart Exit: {getMapExit(fh,0x70)}")
            output(f"\t\tCastle Minecart Exit: {getMapExit(fh,0x72)}")
            output(f"\t\tCastle Lobby Entrance: {getMapExit(fh,0x74)}")
            output(f"\t\tK. Rool Exit: {getMapExit(fh,0x76)}")
            output(f"\t\tBallroom to Museum (Monkeyport): {getMapExit(fh,0x120)}")
            output(f"\t\tMuseum to Ballroom (Monkeyport): {getMapExit(fh,0x122)}")
            for x in range(8):
                output(f"\t\t{levels[x]} Exit: {getMapExit(fh,0x78+(2*x))}")
            for x in range(7):
                output(f"\t\t{levels[x]} Entrance: {getMapExit(fh,0x88+(2*x))}")
            output(f"\tFPS Display On: {str(getTrueFalse(fh,0x96,1))}")
            output(f"\tBoss Kongs:")
            for x in range(7):
                output(f"\t\t{levels[x]} Boss: {getKong(fh,0x97+x)}")
            output(f"\tBoss Locations:")
            for x in range(7):
                boss_val = getValue(fh, 0x9E + x, 1)
                boss_str = hex(boss_val)
                for y in bosses:
                    if y["map"] == boss_val:
                        boss_str = y["name"]
                output(f"\t\t{levels[x]} Boss: {boss_str}")
            output(f"\tDamage Multiplier: {getValue(fh,0xA5,1)}")
            output(f"\tNo Health Refills: {str(getTrueFalse(fh,0xA6,1))}")
            output(f"\tMove Rando On: {str(getTrueFalse(fh,0xA7,1))}")
            for shop in range(3):
                for kong in range(5):
                    for level in range(7):
                        output(f"\t\t{kongs[kong]} {shops[shop]} {levels[level]}: {getMove(fh,0xA8 + level + (7 * kong) + (35 * shop))}")
            output(f"\tKut Out Kong Order:")
            for x in range(5):
                output(f"\t\t[{x}] - {getKong(fh,0x111+x)}")
            output(f"\tRemove B. Lockers:")
            for x in range(8):
                output(f"\t\t{levels[x]} Lobby: {str(((getValue(fh,0x116,1) >> x) & 1) != 0)}")
            output(f"\tRemove Minigame Barrels:")
            output(f"\t\tBonus Barrels: {str((getValue(fh,0x117,1) & 1) != 0)}")
            output(f"\t\tHelm Barrels: {str((getValue(fh,0x117,1) & 2) != 0)}")
            output(f"\tKeys Pre-Turned:")
            for x in range(8):
                output(f"\t\tKey {x+1}: {str(((getValue(fh,0x118,1) >> x) & 1) != 0)}")
            output(f"\tDisable Drops: {str(getTrueFalse(fh,0x119,1))}")
            output(f"\tHash:")
            for x in range(5):
                output(f"\t\t[{x}] - {str(getValue(fh,0x11A + x,1))}")
            output(f"\tMusic Rando On: {str(getTrueFalse(fh,0x11F,1))}")
            output(f"\tShop Indicator On: {str(getTrueFalse(fh,0x124,1))}")
            output(f"\tWarp to Isles Enabled: {str(getTrueFalse(fh,0x125,1))}")
            output(f"\tColor Kongs: {str(getTrueFalse(fh,0x126,1))}")
            rgb_offset = 0x127
            for x in range(8):
                if x != 5:
                    output(f"\t\t{kongs[x]} RGB: {hex(getValue(fh,rgb_offset,3))}")
                    rgb_offset += 3
            output(f"\tLobbies Auto-opened:")
            for x in range(8):
                output(f"\t\t{levels[x]} Lobby Entrance: {str(((getValue(fh,0x13C,1) >> x) & 1) != 0)}")
            output(f"\tPerma-Lose Kongs: {str(getTrueFalse(fh,0x13D,1))}")
            output(f"\tDisable Boss Kong Check: {str(getTrueFalse(fh,0x13E,1))}")
            output(f"\tPrevent Tag Spawn: {str(getTrueFalse(fh,0x13F,1))}")
            jetpac_req = getValue(fh, 0x140, 1)
            if jetpac_req == 0:
                output(f"\tJetpac Requirement: Vanilla")
            else:
                output(f"\tJetpac Requirement: {jetpac_req} Medals")
