import os
from typing import BinaryIO

"""
	ROM TESTER
	Displays all values in the variable space in an easier-to-read format rather than a hex editor
	***PURELY*** for debugging purposes
	To use:
		- Place your modified Rando ROM in /rom_tester
		- Run this script
		- This script will spit out details for ALL .z64 files in /rom_tester, so if you only want data for a specific rom, make sure that's the only one in /rom_tester
"""

levels = ["Japes","Aztec","Factory","Galleon","Fungi","Caves","Castle","Helm"]
keys = [0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D]
special_moves = [
	"Baboon Blast","Strong Kong","Gorilla Grab",
	"Chimpy Charge","Rocketbarrel","Simian Spring",
	"Orangstand","Baboon Balloon","Orangstand Sprint",
	"Mini Monkey","Pony Tail Twirl","Monkeyport",
	"Hunky Chunky","Primate Punch","Gorilla Gone",
	"Super Simian Slam","Super Duper Simian Slam",
	"Coconut Gun","Peanut Popguns","Grape Shooter","Feather Bow","Pineapple Launcher",
	"Bongo Blast","Guitar Gazump","Trombone Tremor","Saxaphone Slam","Triangle Trample",
	"Homing Ammo","Sniper Scope",
	"Ammo Belt 1","Ammo Belt 2",
	"Instrument Upgrade 1","3rd Melon","Instrument Upgrade 2"
]
kongs = ["DK","Diddy","Lanky","Tiny","Chunky","Krusha","Rambi","Enguarde"]
shops = ["Cranky","Funky","Candy"]
bosses = [
	{"name":"Army Dillo 1","map":0x8},
	{"name":"Dogadon 1","map":0xC5},
	{"name":"Mad Jack","map":0x9A},
	{"name":"Pufftoss","map":0x6F},
	{"name":"Dogadon 2","map":0x53},
	{"name":"Army Dillo 2","map":0xC4},
	{"name":"King Kut Out","map":0xC7},
]
move_types = ["Special Move","Slam","Gun","Ammo Belt","Instrument"]

def getValue(fh,offset,size):
	fh.seek(0x1FED020 + offset)
	return int.from_bytes(fh.read(size),"big")

def getTrueFalse(fh,offset,size):
	val = getValue(fh,offset,size)
	if val != 0:
		return True
	return False

def getMapExit(fh,offset):
	val = getValue(fh,offset,2);
	return f"Map {(val>>16)&0xFF}, Exit {val & 0xFF}"

def getKong(fh,offset):
	val = getValue(fh,offset,1)
	if val >= 0:
		if val < 8:
			return kongs[val]
	return f"Kong {hex(val)}"

def getMove(fh,offset):
	val = getValue(fh,offset,1)
	move_type = (val >> 4) & 0xF;
	move_lvl = val & 0xF;
	if move_type == 0xF:
		return "No Upgrade"
	return f"{move_types[move_type]} level {str(move_lvl)}"

files = [f for f in os.listdir(".") if os.path.isfile(f)]
for f in files:
	if ".z64" in f:
		print(f"Analyzing {f}")
		with open(f,"rb") as fh:
			print(f"\tLevel Order Rando: {str(getTrueFalse(fh,0,1))}")
			print(f"\tLevel Order:")
			for x in range(7):
				idx_val = getValue(fh,1 + x,1)
				print(f"\t\t[{x}] - {levels[idx_val]} ({idx_val})")
			print(f"\tTroff 'n' Scoff Count:")
			for x in range(7):
				print(f"\t\t{levels[x]}: {getValue(fh,8+(2*x),2)}")
			print(f"\tB. Locker Requirement:")
			for x in range(8):
				print(f"\t\t{levels[x]} Lobby: {getValue(fh,0x16+x,1)}")
			print(f"\tKey Flags:")
			for x in range(7):
				key_str = ""
				flag_val = getValue(fh,0x1E+(2*x),2)
				if flag_val in keys:
					key_str = f" (Key {keys.index(flag_val)+1})"
				print(f"\t\t{levels[x]} Boss: {hex(flag_val)}{key_str}")
			print(f"\tUnlock Kongs: {str(getTrueFalse(fh,0x2C,1))}")
			print(f"\tUnlock Moves: {str(getTrueFalse(fh,0x2D,1))}")
			print(f"\tFast Start (Beginning): {str(getTrueFalse(fh,0x2E,1))}")
			print(f"\tCamera Unlocked: {str(getTrueFalse(fh,0x2F,1))}")
			print(f"\tTag Anywhere: {str(getTrueFalse(fh,0x30,1))}")
			print(f"\tFast Start (Helm): {str(getTrueFalse(fh,0x31,1))}")
			print(f"\tCrown Door Open: {str(getTrueFalse(fh,0x32,1))}")
			print(f"\tCoin Door Open: {str(getTrueFalse(fh,0x33,1))}")
			print(f"\tQuality of Life changes: {str(getTrueFalse(fh,0x34,1))}")
			print(f"\tPrice Rando On: {str(getTrueFalse(fh,0x35,1))}")
			for x in range(34):
				print(f"\t\t{special_moves[x]}: {getValue(fh,0x36+x,1)}")
			print(f"\tK Rool Order:")
			for x in range(5):
				print(f"\t\t[{x}] - {getKong(fh,0x58+x)} Phase")
			print(f"\tRandomize More Loading Zones: {str(getTrueFalse(fh,0x5D,1))}")
			print(f"\t\tAztec Beetle Enter: {getMapExit(fh,0x5E)}")
			print(f"\t\tAztec Beetle Exit: {getMapExit(fh,0x60)}")
			print(f"\t\tCaves Beetle Exit: {getMapExit(fh,0x62)}")
			print(f"\t\tSeal Race Exit: {getMapExit(fh,0x64)}")
			print(f"\t\tFactory Car Exit: {getMapExit(fh,0x66)}")
			print(f"\t\tCastle Car Exit: {getMapExit(fh,0x68)}")
			print(f"\t\tSeasick Ship Enter: {getMapExit(fh,0x6A)}")
			print(f"\t\tFungi Minecart Enter: {getMapExit(fh,0x6C)}")
			print(f"\t\tFungi Minecart Exit: {getMapExit(fh,0x6E)}")
			print(f"\t\tJapes Minecart Exit: {getMapExit(fh,0x70)}")
			print(f"\t\tCastle Minecart Exit: {getMapExit(fh,0x72)}")
			print(f"\t\tCastle Lobby Entrance: {getMapExit(fh,0x74)}")
			print(f"\t\tK. Rool Exit: {getMapExit(fh,0x76)}")
			for x in range(8):
				print(f"\t\t{levels[x]} Exit: {getMapExit(fh,0x78+(2*x))}")
			for x in range(7):
				print(f"\t\t{levels[x]} Entrance: {getMapExit(fh,0x88+(2*x))}")
			print(f"\tFPS Display On: {str(getTrueFalse(fh,0x96,1))}")	
			print(f"\tBoss Kongs:")
			for x in range(7):
				print(f"\t\t{levels[x]} Boss: {getKong(fh,0x97+x)}")
			print(f"\tBoss Locations:")
			for x in range(7):
				boss_val = getValue(fh,0x9E+x,1)
				boss_str = hex(boss_val)
				for y in bosses:
					if y["map"] == boss_val:
						boss_str = y["name"]
				print(f"\t\t{levels[x]} Boss: {boss_str}")
			print(f"\tDamage Multiplier: {getValue(fh,0xA5,1)}")
			print(f"\tNo Health Refills: {str(getTrueFalse(fh,0xA6,1))}")
			print(f"\tMove Rando On: {str(getTrueFalse(fh,0xA7,1))}")
			for shop in range(3):
				for kong in range(5):
					for level in range(7):
						print(f"\t\t{kongs[kong]} {shops[shop]} {levels[level]}: {getMove(fh,0xA8 + level + (7 * kong) + (35 * shop))}")
			print(f"\tKut Out Kong Order:")
			for x in range(5):
				print(f"\t\t[{x}] - {getKong(fh,0x111+x)}")
			print(f"\tRemove B. Lockers:")
			for x in range(8):
				print(f"\t\t{levels[x]} Lobby: {str(((getValue(fh,0x116,1) >> x) & 1) != 0)}")
			print(f"\tRemove Minigame Barrels:")
			print(f"\t\tBonus Barrels: {str((getValue(fh,0x117,1) & 1) != 0)}")
			print(f"\t\tHelm Barrels: {str((getValue(fh,0x117,1) & 2) != 0)}")
			print(f"\tKeys Pre-Turned:")
			for x in range(8):
				print(f"\t\tKey {x+1}: {str(((getValue(fh,0x118,1) >> x) & 1) != 0)}")
			print(f"\tDisable Drops: {str(getTrueFalse(fh,0x119,1))}")
			print(f"\tHash:")
			for x in range(5):
				print(f"\t\t[{x}] - {str(getValue(fh,0x11A + x,1))}")