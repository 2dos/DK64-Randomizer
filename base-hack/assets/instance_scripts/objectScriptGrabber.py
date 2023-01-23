"""Grab object scripts."""
import gzip
import math
import os
import shutil
import tkinter as tk
import zlib
from tkinter import filedialog
from typing import BinaryIO

root = tk.Tk()
root.withdraw()

maps = [
    "Test Map",  # 0
    "Funky's Store",
    "DK Arcade",
    "K. Rool Barrel: Lanky's Maze",
    "Jungle Japes: Mountain",
    "Cranky's Lab",
    "Jungle Japes: Minecart",
    "Jungle Japes",
    "Jungle Japes: Army Dillo",
    "Jetpac",
    "Kremling Kosh! (very easy)",  # 10
    "Stealthy Snoop! (normal, no logo)",
    "Jungle Japes: Shell",
    "Jungle Japes: Lanky's Cave",
    "Angry Aztec: Beetle Race",
    "Snide's H.Q.",
    "Angry Aztec: Tiny's Temple",
    "Hideout Helm",
    "Teetering Turtle Trouble! (very easy)",
    "Angry Aztec: Five Door Temple (DK)",
    "Angry Aztec: Llama Temple",  # 20
    "Angry Aztec: Five Door Temple (Diddy)",
    "Angry Aztec: Five Door Temple (Tiny)",
    "Angry Aztec: Five Door Temple (Lanky)",
    "Angry Aztec: Five Door Temple (Chunky)",
    "Candy's Music Shop",
    "Frantic Factory",
    "Frantic Factory: Car Race",
    "Hideout Helm (Level Intros, Game Over)",
    "Frantic Factory: Power Shed",
    "Gloomy Galleon",  # 30
    "Gloomy Galleon: K. Rool's Ship",
    "Batty Barrel Bandit! (easy)",
    "Jungle Japes: Chunky's Cave",
    "DK Isles Overworld",
    "K. Rool Barrel: DK's Target Game",
    "Frantic Factory: Crusher Room",
    "Jungle Japes: Barrel Blast",
    "Angry Aztec",
    "Gloomy Galleon: Seal Race",
    "Nintendo Logo",  # 40
    "Angry Aztec: Barrel Blast",
    "Troff 'n' Scoff",  # 42
    "Gloomy Galleon: Shipwreck (Diddy, Lanky, Chunky)",
    "Gloomy Galleon: Treasure Chest",
    "Gloomy Galleon: Mermaid",
    "Gloomy Galleon: Shipwreck (DK, Tiny)",
    "Gloomy Galleon: Shipwreck (Lanky, Tiny)",
    "Fungi Forest",
    "Gloomy Galleon: Lighthouse",
    "K. Rool Barrel: Tiny's Mushroom Game",  # 50
    "Gloomy Galleon: Mechanical Fish",
    "Fungi Forest: Ant Hill",
    "Battle Arena: Beaver Brawl!",
    "Gloomy Galleon: Barrel Blast",
    "Fungi Forest: Minecart",
    "Fungi Forest: Diddy's Barn",
    "Fungi Forest: Diddy's Attic",
    "Fungi Forest: Lanky's Attic",
    "Fungi Forest: DK's Barn",
    "Fungi Forest: Spider",  # 60
    "Fungi Forest: Front Part of Mill",
    "Fungi Forest: Rear Part of Mill",
    "Fungi Forest: Mushroom Puzzle",
    "Fungi Forest: Giant Mushroom",
    "Stealthy Snoop! (normal)",
    "Mad Maze Maul! (hard)",
    "Stash Snatch! (normal)",
    "Mad Maze Maul! (easy)",
    "Mad Maze Maul! (normal)",  # 69
    "Fungi Forest: Mushroom Leap",  # 70
    "Fungi Forest: Shooting Game",
    "Crystal Caves",
    "Battle Arena: Kritter Karnage!",
    "Stash Snatch! (easy)",
    "Stash Snatch! (hard)",
    "DK Rap",
    "Minecart Mayhem! (easy)",  # 77
    "Busy Barrel Barrage! (easy)",
    "Busy Barrel Barrage! (normal)",
    "Main Menu",  # 80
    "Title Screen (Not For Resale Version)",
    "Crystal Caves: Beetle Race",
    "Fungi Forest: Dogadon",
    "Crystal Caves: Igloo (Tiny)",
    "Crystal Caves: Igloo (Lanky)",
    "Crystal Caves: Igloo (DK)",
    "Creepy Castle",
    "Creepy Castle: Ballroom",
    "Crystal Caves: Rotating Room",
    "Crystal Caves: Shack (Chunky)",  # 90
    "Crystal Caves: Shack (DK)",
    "Crystal Caves: Shack (Diddy, middle part)",
    "Crystal Caves: Shack (Tiny)",
    "Crystal Caves: Lanky's Hut",
    "Crystal Caves: Igloo (Chunky)",
    "Splish-Splash Salvage! (normal)",
    "K. Lumsy",
    "Crystal Caves: Ice Castle",
    "Speedy Swing Sortie! (easy)",
    "Crystal Caves: Igloo (Diddy)",  # 100
    "Krazy Kong Klamour! (easy)",
    "Big Bug Bash! (very easy)",
    "Searchlight Seek! (very easy)",
    "Beaver Bother! (easy)",
    "Creepy Castle: Tower",
    "Creepy Castle: Minecart",
    "Kong Battle: Battle Arena",
    "Creepy Castle: Crypt (Lanky, Tiny)",
    "Kong Battle: Arena 1",
    "Frantic Factory: Barrel Blast",  # 110
    "Gloomy Galleon: Pufftoss",
    "Creepy Castle: Crypt (DK, Diddy, Chunky)",
    "Creepy Castle: Museum",
    "Creepy Castle: Library",
    "Kremling Kosh! (easy)",
    "Kremling Kosh! (normal)",
    "Kremling Kosh! (hard)",
    "Teetering Turtle Trouble! (easy)",
    "Teetering Turtle Trouble! (normal)",
    "Teetering Turtle Trouble! (hard)",  # 120
    "Batty Barrel Bandit! (easy)",
    "Batty Barrel Bandit! (normal)",
    "Batty Barrel Bandit! (hard)",
    "Mad Maze Maul! (insane)",
    "Stash Snatch! (insane)",
    "Stealthy Snoop! (very easy)",
    "Stealthy Snoop! (easy)",
    "Stealthy Snoop! (hard)",
    "Minecart Mayhem! (normal)",
    "Minecart Mayhem! (hard)",  # 130
    "Busy Barrel Barrage! (hard)",
    "Splish-Splash Salvage! (hard)",
    "Splish-Splash Salvage! (easy)",
    "Speedy Swing Sortie! (normal)",
    "Speedy Swing Sortie! (hard)",
    "Beaver Bother! (normal)",
    "Beaver Bother! (hard)",
    "Searchlight Seek! (easy)",
    "Searchlight Seek! (normal)",
    "Searchlight Seek! (hard)",  # 140
    "Krazy Kong Klamour! (normal)",
    "Krazy Kong Klamour! (hard)",
    "Krazy Kong Klamour! (insane)",
    "Peril Path Panic! (very easy)",
    "Peril Path Panic! (easy)",
    "Peril Path Panic! (normal)",
    "Peril Path Panic! (hard)",
    "Big Bug Bash! (easy)",
    "Big Bug Bash! (normal)",
    "Big Bug Bash! (hard)",  # 150
    "Creepy Castle: Dungeon",
    "Hideout Helm (Intro Story)",
    "DK Isles (DK Theatre)",
    "Frantic Factory: Mad Jack",
    "Battle Arena: Arena Ambush!",
    "Battle Arena: More Kritter Karnage!",
    "Battle Arena: Forest Fracas!",
    "Battle Arena: Bish Bash Brawl!",
    "Battle Arena: Kamikaze Kremlings!",
    "Battle Arena: Plinth Panic!",  # 160
    "Battle Arena: Pinnacle Palaver!",
    "Battle Arena: Shockwave Showdown!",
    "Creepy Castle: Basement",
    "Creepy Castle: Tree",
    "K. Rool Barrel: Diddy's Kremling Game",
    "Creepy Castle: Chunky's Toolshed",
    "Creepy Castle: Trash Can",
    "Creepy Castle: Greenhouse",
    "Jungle Japes Lobby",
    "Hideout Helm Lobby",  # 170
    "DK's House",
    "Rock (Intro Story)",
    "Angry Aztec Lobby",
    "Gloomy Galleon Lobby",
    "Frantic Factory Lobby",
    "Training Grounds",
    "Dive Barrel",
    "Fungi Forest Lobby",
    "Gloomy Galleon: Submarine",
    "Orange Barrel",  # 180
    "Barrel Barrel",
    "Vine Barrel",
    "Creepy Castle: Crypt",
    "Enguarde Arena",
    "Creepy Castle: Car Race",
    "Crystal Caves: Barrel Blast",
    "Creepy Castle: Barrel Blast",
    "Fungi Forest: Barrel Blast",
    "Fairy Island",
    "Kong Battle: Arena 2",  # 190
    "Rambi Arena",
    "Kong Battle: Arena 3",
    "Creepy Castle Lobby",
    "Crystal Caves Lobby",
    "DK Isles: Snide's Room",
    "Crystal Caves: Army Dillo",
    "Angry Aztec: Dogadon",
    "Training Grounds (End Sequence)",
    "Creepy Castle: King Kut Out",
    "Crystal Caves: Shack (Diddy, upper part)",  # 200
    "K. Rool Barrel: Diddy's Rocketbarrel Game",
    "K. Rool Barrel: Lanky's Shooting Game",
    "K. Rool Fight: DK Phase",
    "K. Rool Fight: Diddy Phase",
    "K. Rool Fight: Lanky Phase",
    "K. Rool Fight: Tiny Phase",
    "K. Rool Fight: Chunky Phase",
    "Bloopers Ending",
    "K. Rool Barrel: Chunky's Hidden Kremling Game",
    "K. Rool Barrel: Tiny's Pony Tail Twirl Game",  # 210
    "K. Rool Barrel: Chunky's Shooting Game",
    "K. Rool Barrel: DK's Rambi Game",
    "K. Lumsy Ending",
    "K. Rool's Shoe",
    "K. Rool's Arena",  # 215
    "UNKNOWN 216",
    "UNKNOWN 217",
    "UNKNOWN 218",
    "UNKNOWN 219",
    "UNKNOWN 220",
    "UNKNOWN 221",
]

hud_items = [
    "Coloured banana",
    "Banana coin",
    "Ammo",
    "Homing ammo",
    "Orange",
    "Crystal",
    "Film",
    "Instrument",
    "GB Count?(Left)",
    "GB Count (Bottom)",
    "Banana Medal",
    "Minecart/Minigame Coin",
    "Blueprint",
    "Coloured Bananas (???)",
    "Banana coins (???)",
]

songs = [
    "Silence",
    "Jungle Japes (Starting Area)",
    "Cranky's Lab",
    "Jungle Japes (Minecart)",
    "Jungle Japes (Army Dillo)",
    "Jungle Japes (Caves/Underground)",
    "Funky's Hut",
    "Unused Coin Pickup",
    "Bonus Minigames",
    "Triangle Trample",
    "Guitar Gazump",
    "Bongo Blast",
    "Trombone Tremor",
    "Saxaphone Slam",
    "Angry Aztec",
    "Transformation",
    "Mini Monkey",
    "Hunky Chunky",
    "GB/Key Get",
    "Angry Aztec (Beetle Slide)",
    "Oh Banana",
    "Angry Aztec (Temple)",
    "Company Coin Get",
    "Banana Coin Get",
    "Going through Vulture Ring",
    "Angry Aztec (Dogadon)",
    "Angry Aztec (5DT)",
    "Frantic Factory (Car Race)",
    "Frantic Factory",
    "Snide's HQ",
    "Jungle Japes (Tunnels)",
    "Candy's Music Shop",
    "Minecart Coin Get",
    "Melon Slice Get",
    "Pause Menu",
    "Crystal Coconut Get",
    "Rambi",
    "Angry Aztec (Tunnels)",
    "Water Droplets",
    "Frantic Factory (Mad Jack)",
    "Success",
    "Start (To pause game)",
    "Failure",
    "DK Transition (Opening)",
    "DK Transition (Closing)",
    "Unused High-Pitched Japes",
    "Fairy Tick",
    "Melon Slice Drop",
    "Angry Aztec (Chunky Klaptraps)",
    "Frantic Factory (Crusher Room)",
    "Jungle Japes (Baboon Blast)",
    "Frantic Factory (R&D)",
    "Frantic Factory (Production Room)",
    "Troff 'n' Scoff",
    "Boss Defeat",
    "Angry Aztec (Baboon Blast)",
    "Gloomy Galleon (Outside)",
    "Boss Unlock",
    "Awaiting Entering the Boss",
    "Generic Twinkly Sounds",
    "Gloomy Galleon (Pufftoss)",
    "Gloomy Galleon (Seal Race)",
    "Gloomy Galleon (Tunnels)",
    "Gloomy Galleon (Lighthouse)",
    "Battle Arena",
    "Drop Coins (Minecart)",
    "Fairy Nearby",
    "Checkpoint",
    "Fungi Forest (Day)",
    "Blueprint Get",
    "Fungi Forest (Night)",
    "Strong Kong",
    "Rocketbarrel Boost",
    "Orangstand Sprint",
    "Fungi Forest (Minecart)",
    "DK Rap",
    "Blueprint Drop",
    "Gloomy Galleon (2DS)",
    "Gloomy Galleon (5DS/Submarine)",
    "Gloomy Galleon (Pearls Chest)",
    "Gloomy Galleon (Mermaid Palace)",
    "Fungi Forest (Dogadon)",
    "Mad Maze Maul",
    "Crystal Caves",
    "Crystal Caves (Giant Kosha Tantrum)",
    "Nintendo Logo (Old?)",
    "Success (Races)",
    "Failure (Races & Try Again)",
    "Bonus Barrel Introduction",
    "Stealthy Snoop",
    "Minecart Mayhem",
    "Gloomy Galleon (Mechanical Fish)",
    "Gloomy Galleon (Baboon Blast)",
    "Fungi Forest (Anthill)",
    "Fungi Forest (Barn)",
    "Fungi Forest (Mill)",
    "Generic Seaside Sounds",
    "Fungi Forest (Spider)",
    "Fungi Forest (Mushroom Top Rooms)",
    "Fungi Forest (Giant Mushroom)",
    "Boss Introduction",
    "Tag Barrel (All of them)",
    "Crystal Caves (Beetle Race)",
    "Crystal Caves (Igloos)",
    "Mini Boss",
    "Creepy Castle",
    "Creepy Castle (Minecart)",
    "Baboon Balloon",
    "Gorilla Gone",
    "DK Isles",
    "DK Isles (K Rool's Ship)",
    "DK Isles (Banana Fairy Island)",
    "DK Isles (K-Lumsy's Prison)",
    "Hideout Helm (Blast-O-Matic On)",
    "Move Get",
    "Gun Get",
    "Hideout Helm (Blast-O-Matic Off)",
    "Hideout Helm (Bonus Barrels)",
    "Crystal Caves (Cabins)",
    "Crystal Caves (Rotating Room)",
    "Crystal Caves (Tile Flipping)",
    "Creepy Castle (Tunnels)",
    "Intro Story Medley",
    "Training Grounds",
    "Enguarde",
    "K-Lumsy Celebration",
    "Creepy Castle (Crypt)",
    "Headphones Get",
    "Pearl Get",
    "Creepy Castle (Dungeon w/ Chains)",
    "Angry Aztec (Lobby)",
    "Jungle Japes (Lobby)",
    "Frantic Factory (Lobby)",
    "Gloomy Galleon (Lobby)",
    "Main Menu",
    "Creepy Castle (Inner Crypts)",
    "Creepy Castle (Ballroom)",
    "Creepy Castle (Greenhouse)",
    "K Rool's Theme",
    "Fungi Forest (Winch)",
    "Creepy Castle (Wind Tower)",
    "Creepy Castle (Tree)",
    "Creepy Castle (Museum)",
    "BBlast Final Star",
    "Drop Rainbow Coin",
    "Rainbow Coin Get",
    "Normal Star",
    "Bean Get",
    "Crystal Caves (Army Dillo)",
    "Creepy Castle (Kut Out)",
    "Creepy Castle (Dungeon w/out Chains)",
    "Banana Medal Get",
    "K Rool's Battle",
    "Fungi Forest (Lobby)",
    "Crystal Caves (Lobby)",
    "Creepy Castle (Lobby)",
    "Hideout Helm (Lobby)",
    "Creepy Castle (Trash Can)",
    "End Sequence",
    "K-Lumsy Ending",
    "Jungle Japes",
    "Jungle Japes (Cranky's Area)",
    "K Rool Takeoff",
    "Crystal Caves (Baboon Blast)",
    "Fungi Forest (Baboon Blast)",
    "Creepy Castle (Baboon Blast)",
    "DK Isles (Snide's Room)",
    "K Rool's Entrance",
    "Monkey Smash",
    "Fungi Forest (Rabbit Race)",
    "Game Over",
    "Wrinkly Kong",
    "100th CB Get",
    "K Rool's Defeat",
    "Nintendo Logo",
]

object_modeltwo_types = [
    "Nothing",  # "test" internal name
    "Thin Flame?",  # 2D
    "-",
    "Tree",  # 2D
    "-",
    "Yellow Flowers",  # 2D
    "-",
    "-",
    "Xmas Holly?",  # 2D
    "-",
    "CB Single (Diddy)",
    "Large Wooden Panel",  # 2D
    "Flames",  # 2D
    "CB Single (DK)",
    "Large Iron Bars Panel",  # 2D
    "Goo Hand",  # Castle
    "Flame",  # 2D
    "Homing Ammo Crate",
    "Coffin Door",
    "Coffin Lid",
    "Skull",  # Castle, it has a boulder in it
    "Wooden Crate",
    "CB Single (Tiny)",
    "Shield",  # Castle
    "Metal thing",
    "Coffin",
    "Metal Panel",
    "Rock Panel",
    "Banana Coin (Tiny)",
    "Banana Coin (DK)",
    "CB Single (Lanky)",
    "CB Single (Chunky)",
    "Tree",  # Japes?
    "-",
    "Metal Panel",
    "Banana Coin (Lanky)",
    "Banana Coin (Diddy)",
    "Metal Panel",
    "Metal Panel Red",
    "Banana Coin (Chunky)",
    "Metal Panel Grey",
    "Tree",  # Japes?
    "-",
    "CB Bunch (DK)",
    "Hammock",
    "Small jungle bush plant",
    "-",
    "Small plant",
    "Bush",  # Japes
    "-",
    "-",
    "-",  # Fungi Lobby, Unknown
    "Metal Bridge",  # Helm Lobby
    "Large Blue Crystal",  # Crystal Caves Lobby
    "Plant",
    "Plant",
    "-",
    "White Flowers",
    "Stem 4 Leaves",
    "-",
    "-",
    "Small plant",
    "-",
    "-",
    "-",
    "-",
    "-",
    "Yellow Flower",
    "Blade of Grass Large",
    "Lilypad?",
    "Plant",
    "Iron Bars",  # Castle Lobby Coconut Switch
    "Nintendo Coin",  # Not sure if this is collectable
    "Metal Floor",
    "-",
    "-",
    "Bull Rush",
    "-",
    "-",
    "Metal box/platform",
    "K Crate",  # DK Helm Target Barrel
    "-",
    "Wooden panel",
    "-",
    "-",
    "-",
    "Orange",
    "Watermelon Slice",
    "Tree",  # Unused?
    "Tree",  # Unused
    "Tree",
    "Tree (Black)",  # Unused
    "-",
    "Light Green platform",
    "-",
    "-",
    "-",
    "-",
    "Brick Wall",
    "-",
    "-",
    "-",
    "-",
    "Wrinkly Door (Tiny)",
    "-",
    "-",
    "-",
    "Conveyor Belt",
    "Tree",  # Japes?
    "Tree",
    "Tree",
    "-",
    "Primate Punch Switch",  # Factory
    "Hi-Lo toggle machine",
    "Breakable Metal Grate",  # Factory
    "Cranky's Lab",
    "Golden Banana",
    "Metal Platform",
    "Metal Bars",
    "-",
    "Metal fence",
    "Snide's HQ",
    "Funky's Armory",
    "-",
    "Blue lazer field",
    "-",
    "Bamboo Gate",
    "-",
    "Tree Stump",
    "Breakable Hut",  # Japes
    "Mountain Bridge",  # Japes
    "Tree Stump",  # Japes
    "Bamboo Gate",
    "-",
    "Blue/green tree",
    "-",
    "Mushroom",
    "-",
    "Disco Ball",
    "2 Door (5DS)",  # Galleon
    "3 Door (5DS)",  # Galleon
    "Map of DK island",
    "Crystal Coconut",
    "Ammo Crate",
    "Banana Medal",
    "Peanut",
    "Simian Slam Switch (Chunky, Green)",
    "Simian Slam Switch (Diddy, Green)",
    "Simian Slam Switch (DK, Green)",
    "Simian Slam Switch (Lanky, Green)",
    "Simian Slam Switch (Tiny, Green)",
    "Baboon Blast Pad",
    "Film",
    "Chunky Rotating Room",  # Aztec, Tiny Temple
    "Stone Monkey Face",
    "Stone Monkey Face",
    "Aztec Panel blue",
    "-",  # templestuff, in Tiny Temple
    "Ice Floor",
    "Ice Pole",  # I think this is a spotlight
    "Big Blue wall panel",
    "Big Blue wall panel",
    "Big Blue wall panel",
    "Big Blue wall panel",
    "KONG Letter (K)",
    "KONG Letter (O)",
    "KONG Letter (N)",
    "KONG Letter (G)",
    "Bongo Pad",  # DK
    "Guitar Pad",  # Diddy
    "Saxaphone Pad",  # Tiny
    "Triangle Pad",  # Chunky
    "Trombone Pad",  # Lanky
    "Wood panel small",
    "Wood panel small",
    "Wood panel small",
    "Wood Panel small",
    "Wall Panel",  # Aztec
    "Wall Panel",  # Caves?
    "Stone Monkey Face (Not Solid)",
    "Feed Me Totem",  # Aztec
    "Melon Crate",
    "Lava Platform",  # Aztec, Llama temple
    "Rainbow Coin",
    "Green Switch",
    "Coconut Indicator",  # Free Diddy
    "Snake Head",  # Aztec, Llama temple
    "Matching Game Board",  # Aztec, Llama temple
    "Stone Monkey Head",  # Aztec
    "Large metal section",
    "Production Room Crusher",  # Factory
    "Metal Platform",
    "Metal Object",
    "Metal Object",
    "Metal Object",
    "Gong",  # Diddy Kong
    "Platform",  # Aztec
    "Bamboo together",
    "Metal Bars",
    "Target",  # Minigames
    "Wooden object",
    "Ladder",
    "Ladder",
    "Wooden pole",
    "Blue panel",
    "Ladder",
    "Grey Switch",
    "D Block for toy world",
    "Hatch (Factory)",
    "Metal Bars",
    "Raisable Metal Platform",
    "Metal Cage",
    "Simian Spring Pad",
    "Power Shed",  # Factory
    "Metal platform",
    "Sun Lighting effect panel",
    "Wooden Pole",
    "Wooden Pole",
    "Wooden Pole",
    "-",
    "Question Mark Box",
    "Blueprint (Tiny)",
    "Blueprint (DK)",
    "Blueprint (Chunky)",
    "Blueprint (Diddy)",
    "Blueprint (Lanky)",
    "Tree Dark",
    "Rope",
    "-",
    "-",
    "Lever",
    "Green Croc Head (Minecart)",
    "Metal Gate with red/white stripes",
    "-",
    "Purple Croc Head (Minecart)",
    "Wood panel",
    "DK coin",
    "Wooden leg",
    "-",
    "Wrinkly Door (Lanky)",
    "Wrinkly Door (DK)",
    "Wrinkly Door (Chunky)",
    "Wrinkly Door (Diddy)",
    "Torch",
    "Number Game (1)",  # Factory
    "Number Game (2)",  # Factory
    "Number Game (3)",  # Factory
    "Number Game (4)",  # Factory
    "Number Game (5)",  # Factory
    "Number Game (6)",  # Factory
    "Number Game (7)",  # Factory
    "Number Game (8)",  # Factory
    "Number Game (9)",  # Factory
    "Number Game (10)",  # Factory
    "Number Game (11)",  # Factory
    "Number Game (12)",  # Factory
    "Number Game (13)",  # Factory
    "Number Game (14)",  # Factory
    "Number Game (15)",  # Factory
    "Number Game (16)",  # Factory
    "Bad Hit Detection Wheel",  # Factory
    "Breakable Gate",  # Galleon Primate Punch
    "-",
    "Picture of DK island",
    "White flashing thing",
    "Barrel",  # Galleon Ship
    "Gorilla Gone Pad",
    "Monkeyport Pad",
    "Baboon Balloon Pad",
    "Light",  # Factory?
    "Light",  # Factory?
    "Barrel",  # Galleon Ship
    "Barrel",  # Galleon Ship
    "Barrel",  # Galleon Ship
    "Barrel",  # Galleon Ship
    "Pad",  # TODO: Empty blue pad? Where is this used?
    "Red Light",  # Factory?
    "Breakable X Panel",  # To enter Japes underground
    "Power Shed Screen",  # Factory
    "Crusher",  # Factory
    "Floor Panel",
    "Metal floor panel mesh",
    "Metal Door",  # Factory or Car Race
    "Metal Door",  # Factory or Car Race
    "Metal Door",  # Factory or Car Race
    "Metal Door",  # Factory or Car Race
    "Metal Door",  # Factory or Car Race
    "Metal Door",  # Factory or Car Race
    "Toyz Box",
    "O Pad",  # Aztec Chunky Puzzle
    "Bonus Barrel Trap",  # Aztec
    "Sun Idol",  # Aztec, top of "feed me" totem
    "Candy's Shop",
    "Pineapple Switch",
    "Peanut Switch",
    "Feather Switch",
    "Grape Switch",
    "Coconut Switch",
    "-",
    "Kong Pad",
    "Boss Door",  # Troff'n'Scoff
    "Troff n Scoff Feed Pad",
    "Metal Bars horizontal",
    "Metal Bars",
    "Harbour Gate",  # Galleon
    "K. Rool's Ship",  # Galleon
    "Metal Platform",
    "-",
    "Flame",
    "Flame",
    "Scoff n Troff platform",
    "Troff n Scoff Banana Count Pad (DK)",
    "Torch",
    "-",
    "-",
    "-",
    "Boss Key",
    "Machine",
    "Metal Door",  # Factory or Car Race - Production Room & Lobby - Unused?
    "Metal Door",  # Factory or Car Race - Testing Dept. & Krem Storage
    "Metal Door",  # Factory or Car Race - R&D
    "Metal Door",  # Factory or Car Race - Testing Dept.
    "Piano Game",  # Factory, Lanky
    "Troff n Scoff Banana Count Pad (Diddy)",
    "Troff n Scoff Banana Count Pad (Lanky)",
    "Troff n Scoff Banana Count Pad (Chunky)",
    "Troff n Scoff Banana Count Pad (Tiny)",
    "Door 1342",
    "Door 3142",
    "Door 4231",
    "1 Switch (Red)",
    "2 Switch (Blue)",
    "3 Switch (Orange)",
    "4 Switch (Green)",
    "-",
    "Metal Archway",
    "Green Crystal thing",
    "Red Crystal thing",
    "Propeller",
    "Large Metal Bar",
    "Ray Sheild?",
    "-",
    "-",
    "-",
    "-",
    "Light",
    "Target",  # Fungi/Castle minigames
    "Ladder",
    "Metal Bars",
    "Red Feather",
    "Grape",
    "Pinapple",
    "Coconut",
    "Rope",
    "On Button",
    "Up Button",
    "Metal barrel or lid",
    "Simian Slam Switch (Chunky, Red)",
    "Simian Slam Switch (Diddy, Red)",
    "Simian Slam Switch (DK, Red)",
    "Simian Slam Switch (Lanky, Red)",
    "Simian Slam Switch (Tiny, Red)",
    "Simian Slam Switch (Chunky, Blue)",
    "Simian Slam Switch (Diddy, Blue)",
    "Simian Slam Switch (DK, Blue)",
    "Simian Slam Switch (Lanky, Blue)",
    "Simian Slam Switch (Tiny, Blue)",
    "Metal Grate",  # Lanky Attic
    "Pendulum",  # Fungi Clock
    "Weight",  # Fungi Clock
    "Door",  # Fungi Clock
    "Day Switch",  # Fungi Clock
    "Night Switch",  # Fungi Clock
    "Hands",  # Fungi Clock
    "Bell",  # (Minecart?)
    "Grate",  # (Minecart?)
    "Crystal",  # Red - No Hitbox (Minecart)
    "Crystal",  # Blue - No Hitbox (Minecart)
    "Crystal",  # Green - No Hitbox (Minecart)
    "Door",  # Fungi
    "Gate",  # Fungi, angled
    "Breakable Door",  # Fungi
    "Night Gate",  # Fungi, angled
    "Night Grate",  # Fungi
    "Unknown",  # Internal name is "minecart"
    "Metal Grate",  # Fungi, breakable, well
    "Mill Pulley Mechanism",  # Fungi
    "Metal Bar",  # No Hitbox (Unknown Location)
    "Water Wheel",  # Fungi
    "Crusher",  # Fungi Mill
    "Coveyor Belt",
    "Night Gate",
    "Question Mark Box",  # Factory Lobby, probably other places too
    "Spider Web",  # Door
    "Grey Croc Head",  # Minecart?
    "Caution Sign (Falling Rocks)",  # Minecart
    "Door",  # Minecart
    "Battle Crown",
    "-",
    "-",
    "Dogadon Arena Background",
    "Skull Door (Small)",  # Minecart
    "Skull Door (Big)",  # Minecart
    "-",
    "Tombstone",  # RIP, Minecart
    "-",
    "DK Star",  # Baboon Blast
    "K. Rool's Throne",
    "Bean",  # Fungi
    "Power Beam",  # Helm (Lanky - BoM)
    "Power Beam",  # Helm (Diddy - BoM)
    "Power Beam",  # Helm (Tiny - Medal Room)
    "Power Beam",  # Helm (Tiny - BoM)
    "Power Beam",  # Helm (Chunky - Medal Room)
    "Power Beam",  # Helm (Chunky - BoM)
    "Power Beam",  # Helm (Lanky - Medal Room)
    "Power Beam",  # Helm (DK - Medal Room)
    "Power Beam",  # Helm (DK - BoM)
    "Power Beam",  # Helm (Diddy - Medal Room)
    "Warning Lights",  # Helm Wheel Room
    "K. Rool Door",  # Helm
    "Metal Grate",
    "Crown Door",  # Helm
    "Coin Door",  # Helm
    "Medal Barrier (DK)",  # Helm
    "Medal Barrier (Diddy)",  # Helm
    "Medal Barrier (Tiny)",  # Helm
    "Medal Barrier (Chunky)",  # Helm
    "Medal Barrier (Lanky)",  # Helm
    "I Door (Helm, DK)",
    "V Door (Helm, Diddy)",
    "III Door (Helm, Tiny)",
    "II Door (Helm, Chunky)",
    "IV Door (Helm, Lanky)",
    "Metal Door",  # Helm CS
    "Stone Wall",  # Helm
    "Pearl",  # Galleon
    "Small Door",  # Fungi
    "-",
    "Cloud",  # Castle, Fungi?
    "Warning Lights",  # Crusher/Grinder
    "Door",  # Fungi
    "Mushroom (Yellow)",
    "Mushroom (Purple)",
    "Mushroom (Blue)",
    "Mushroom (Green)",
    "Mushroom (Red)",
    "Mushroom Puzzle Instructions",
    "Face Puzzle Board",  # Fungi
    "Mushroom",  # Climbable, Fungi
    "Small Torch",  # Internal name "test", interestingly
    "DK Arcade Machine",
    "Simian Slam Switch (Any Kong?)",  # Mad Jack fight
    "Spotlight (Crown Arena?)",
    "Battle Crown Pad",
    "Seaweed",
    "Light",  # Galleon Lighthouse
    "Dust?",
    "Moon Trapdoor",  # Fungi
    "Ladder",  # Fungi
    "Mushroom Board",  # 5 gunswitches, Fungi
    "DK Star",
    "Wooden Box",  # Galleon?
    "Yellow CB Powerup",  # Multiplayer
    "Blue CB Powerup",  # Multiplayer
    "Coin Powerup?",  # Multiplayer, causes burp
    "DK Coin",  # Multiplayer?
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Snide's Mechanism",
    "Blue Flowers",  # 2D
    "Plant (Green)",  # 2D
    "Plant (Brown)",  # 2D
    "Plant",  # 2D
    "Pink Flowers",  # 2D
    "Pink Flowers",  # 2D
    "Plant",  # 2D
    "Yellow Flowers",  # 2D
    "Yellow Flowers",  # 2D
    "Plant",  # 2D
    "Blue Flowers",  # 2D
    "Blue Flower",  # 2D
    "Plant",  # 2D
    "Plant",  # 2D
    "Red Flowers",  # 2D
    "Red Flower",  # 2D
    "Mushrooms (Small)",  # 2D
    "Mushrooms (Small)",  # 2D
    "Purple Flowers",  # 2D
    "Tree",  # Castle?
    "Cactus",  # Unused
    "Cactus",  # Unused
    "Ramp",  # Car Race?
    "Submerged Pot",  # Unused
    "Submerged Pot",  # Unused
    "Ladder",  # Fungi
    "Ladder",  # Fungi
    "Floor Texture?",  # Fungi
    "Iron Gate",  # Fungi
    "Day Gate",  # Fungi
    "Night Gate",  # Fungi
    "Cabin Door",  # Caves
    "Ice Wall (Breakable)",  # Caves
    "Igloo Door",  # Caves
    "Castle Top",  # Caves
    "Ice Dome",  # Caves
    "Boulder Pad",  # Caves
    "Target",  # Caves, Tiny 5DI
    "Metal Gate",
    "CB Bunch (Lanky)",
    "CB Bunch (Chunky)",
    "CB Bunch (Tiny)",
    "CB Bunch (Diddy)",
    "Blue Aura",
    "Ice Maze",  # Caves
    "Rotating Room",  # Caves
    "Light + Barrier",  # Caves
    "Light",  # Caves
    "Trapdoor",  # Caves
    "Large Wooden Door",  # Aztec, Llama Temple?
    "Warp 5 Pad",
    "Warp 3 Pad",
    "Warp 4 Pad",
    "Warp 2 Pad",
    "Warp 1 Pad",
    "Large Door",  # Castle
    "Library Door (Revolving?)",  # Castle
    "Blue Platform",  # Factory / K. Rool, Unused?
    "White Platform",  # Factory / K. Rool, Unused?
    "Wooden Platform",  # Castle
    "Wooden Bridge",  # Castle
    "Wooden Door",  # Castle
    "Metal Grate",  # Castle Pipe
    "Metal Door",  # Castle Greenhouse
    "Large Metal Door",  # Castle?
    "Rotating Chair",  # Castle
    "Baboon Balloon Pad (with platform)",
    "Large Aztec Door",
    "Large Aztec Door",
    "Large Wooden Door",  # Castle Tree
    "Large Breakable Wooden Door",  # Castle Tree
    "Pineapple Switch (Rotating)",  # Castle Tree
    ": Pad",  # Aztec Chunky Puzzle
    "Triangle Pad",  # Aztec Chunky Puzzle
    "+ Pad",  # Aztec Chunky Puzzle
    "Stone Monkey Head",  # Aztec
    "Stone Monkey Head",  # Aztec
    "Stone Monkey Head",  # Aztec
    "Door",  # Caves Beetle Race
    "Broken Ship Piece",  # Galleon
    "Broken Ship Piece",  # Galleon
    "Broken Ship Piece",  # Galleon
    "Flotsam",  # Galleon
    "Metal Grate",  # Factory, above crown pad
    "Treasure Chest",  # Galleon
    "Up Switch",  # Galleon
    "Down Switch",
    "DK Star",  # Caves
    "Enguarde Door",  # Galleon
    "Trash Can",  # Castle
    "Fluorescent Tube",  # Castle Toolshed?
    "Wooden Door Half",  # Castle
    "Stone Platform",  # Aztec Lobby?
    "Stone Panel",  # Aztec Lobby?
    "Stone Panel (Rotating)",  # Aztec Lobby
    "Wrinkly Door Wheel",  # Fungi Lobby
    "Wooden Door",  # Fungi Lobby
    "Wooden Panel",  # Fungi? Lobby?
    "Electricity Shields?",  # One for each kong, roughly in shape of Wrinkly Door wheel # TODO: Unused?
    "Unknown",  # Internal name is "torches"
    "Boulder Pad (Red)",  # Caves
    "Candelabra",  # Castle?
    "Banana Peel",  # Slippery
    "Skull+Candle",  # Castle?
    "Metal Box",
    "1 Switch",
    "2 Switch",
    "3 Switch",
    "4 Switch",
    "Metal Grate (Breakable?)",
    "Pound The X Platform",  # DK Isles
    "Wooden Door",  # Castle Shed
    "Chandelier",  # Castle
    "Bone Door",  # Castle
    "Metal Bars",  # Galleon
    "4 Door (5DS)",
    "5 Door (5DS)",
    "Door (Llama Temple)",  # Aztec
    "Coffin Door",  # Breakable?
    "Metal Bars",
    "Metal Grate",  # Galleon
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "Boulder",  # DK Isles, covering cannon to Fungi
    "Boulder",  # DK Isles
    "K. Rool Ship Jaw Bottom",  # DK Isles
    "Blast-O-Matic Cover?",  # DK Isles
    "Blast-O-Matic Cover",  # DK Isles
    "Door",  # DK Isles, covering factory lobby, not solid
    "Platform",  # DK Isles, up to Factory Lobby
    "Propeller",  # K. Rool's Ship
    "K. Rool's Ship",  # DK Isles, Intro Story
    "Mad Jack Platform (White)",
    "Mad Jack Platform (White)",  # Factory
    "Mad Jack Platform (Blue)",  # Factory
    "Mad Jack Platform (Blue)",  # Factory
    "Skull Gate (Minecart)",  # 2D
    "Dogadon Arena Outer",
    "Boxing Ring Corner (Red)",
    "Boxing Ring Corner (Green)",
    "Boxing Ring Corner (Blue)",
    "Boxing Ring Corner (Yellow)",
    "Lightning Rod",  # Pufftoss Fight, DK Isles for some reason
    "Green Electricity",  # Helm? Chunky BoM stuff?
    "Blast-O-Matic",
    "Target",  # K. Rool Fight (Diddy Phase)
    "Spotlight",  # K. Rool Fight
    "-",
    "Vine",  # Unused?
    "Director's Chair",  # Blooper Ending
    "Spotlight",  # Blooper Ending
    "Spotlight",  # Blooper Ending
    "Boom Microphone",  # Blooper Ending
    "Auditions Sign",  # Blooper Ending
    "Banana Hoard",
    "Boulder",  # DK Isles, covering Caves lobby
    "Boulder",  # DK Isles, covering Japes lobby
    "Rareware GB",
    "-",
    "-",
    "-",
    "-",
    "Platform (Crystal Caves Minigame)",  # Tomato game
    "King Kut Out Arm (Bloopers)",
    "Rareware Coin",  # Not collectable?
    "Golden Banana",  # Not collectable?
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "Rock",  # DK Isles, Covering Castle Cannon?
    "K. Rool's Ship",  # DK Isles, Entrance to final fight
    "-",
    "-",
    "-",
    "Wooden Door",  # BFI Guarding Rareware GB
    "-",
    "-",
    "-",
    "Nothing?",
    "Troff n Scoff Portal",
    "Level Entry/Exit",
    "K. Lumsy Key Indicator?",
    "-",
    "-",
    "-",
    "-",
    "-",
    "Red Bell",  # 2D, Minecart
    "Green Bell",  # 2D, Minecart
    "Race Checkpoint",
    # Tested up to 0x2CF inclusive, all crashes so far
]

trigger_types = [
    "Unknown 0x00",
    "Unknown 0x01",
    "Unknown 0x02",
    "Boss Door Trigger",  # Also sets boss fadeout type as fade instead of spin. In toolshed too??
    "Unknown 0x04",
    "Cutscene Trigger",
    "Unknown 0x06",
    "Unknown 0x07",
    "Unknown 0x08",
    "Loading Zone (0x9)",
    "Cutscene Trigger (0xA)",
    "Unknown 0x0B",
    "Loading Zone + Objects",  # Allows objects through
    "Loading Zone (0xD)",
    "Unknown 0x0E",
    "Warp Trigger",  # Factory Poles
    "Loading Zone (0x10)",
    "Loading Zone (0x11)",  # Snide's, Return to Parent Map?
    "Coin Shower Trigger",
    "Detransform Trigger (0x13)",
    "Boss Loading Zone",  # Takes you to the boss of that level
    "Autowalk Trigger",
    "Sound Trigger",
    "Cutscene Trigger (0x17)",
    "Unknown 0x18",
    "Unknown 0x19",
    "Gravity Trigger",
    "Slide Trigger",  # Beetle Slides
    "Unslide Trigger",
    "Loading Zone (Zipper)",
    "Song Trigger",
    "Unknown 0x1F",
    "Cutscene Trigger (0x20)",
    "Unknown 0x21",
    "Unknown 0x22",
    "Unknown 0x23",
    "Detransform Trigger (0x24)",
    "Chunk Texture Load Trigger",
    "K. Lumsy Code Activator",  # In BFI too, but seems like functionality in BFI has been stripped from final
]

relevant_pointer_tables = [
    {"index": 1, "name": "Map Geometry", "output_filename": "geometry.bin"},
    {"index": 2, "name": "Map Walls", "output_filename": "walls.bin"},
    {"index": 3, "name": "Map Floors", "output_filename": "floors.bin"},
    {"index": 8, "name": "Map Cutscenes", "output_filename": "cutscenes.bin"},
    {"index": 9, "name": "Map Setups", "output_filename": "setup.bin"},
    {"index": 10, "name": "Map Data 0xA", "output_filename": "map_0x0a.bin"},
    {"index": 15, "name": "Map Paths", "output_filename": "paths.bin"},
    {"index": 16, "name": "Map Paths", "output_filename": "character_spawners.bin"},
    {"index": 18, "name": "Map Loading Zones", "output_filename": "loading_zones.bin"},
    {"index": 21, "name": "Map Data 0x15", "output_filename": "map_0x15.bin"},
    {"index": 23, "name": "Map Exits", "output_filename": "exits.bin"},
]

num_tables = 32
pointer_tables = []
pointer_table_offsets = [0x101C50, 0x1038D0, 0x1039C0, 0x1A7C20]
main_pointer_table_offset = pointer_table_offsets[0]
folder_append = ["_us", "_pal", "_jp", "_kiosk"]
setup_table_index = 9
script_table_index = 10
files = {}
tab_indentation = 0
folder_removal = []
version = 0


def getTriggerTypeName(index):
    """Convert Trigger type into a name string."""
    if index < (len(trigger_types) - 1):
        return trigger_types[index]
    return "Type %s" % (hex(index))


def getSongName(index):
    """Convert song index into name."""
    if index < (len(songs) - 1):
        return songs[index]
    return "Song %s" % (hex(index))


def getTOrF(value):
    """Get truthiness from value."""
    if value == 0:
        return "False"
    return "True"


def getSetOrNot(value):
    """Get set or unset from value."""
    if value == 0:
        return "Don't Set"
    return "Set"


def display(file, string):
    """Display function upon being passed a string."""
    global tab_indentation

    if string[-1:] != "{":
        if string[-1:] != "}":
            string += ";"
    for x in range(tab_indentation):
        string = "\t" + string
    if string[-1:] == "{":
        tab_indentation += 1
    elif string[-1:] == "}":
        tab_indentation -= 1
    file.write(string + "\n")


def grabConditional(param_1, ScriptCommand, params, behaviour, param_3, file):
    """Convert conditional into series of C-like Functions."""
    functionType = ScriptCommand & 0x7FFF
    inverseFlag = ScriptCommand & 0x8000
    inverseFlagChar = ""
    inverseFlagInvertedChar = "!"
    if inverseFlag != 0:
        inverseFlag = 1
        inverseFlagChar = "!"
        inverseFlagInvertedChar = ""
    else:
        inverseFlagChar = ""
        inverseFlagInvertedChar = "!"
    if functionType == 0:
        display(file, "if (%strue) {" % (inverseFlagChar))
    elif functionType == 1:
        display(file, "if (*(byte *)(behaviour + %s) %s== %s) {" % (hex(params[1] + 0x48), inverseFlagChar, str(params[0])))
    elif functionType == 2:
        display(file, "x2_successful = 0")
        display(file, "x2_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "x2_focusedPlayerNumber_ = x2_focusedPlayerNumber")
        display(file, "x2_focusedPlayerNumber = (x2_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[x2_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "x2_focusedPlayerPointer = *(int *)(character_change_pointer[x2_focusedPlayerNumber_)]->character_pointer)")
        display(file, "if (*(byte *)(x2_focusedPlayerPointer->locked_to_pad) == 1) {")
        display(file, "if (this->id == *(short *)(x2_focusedPlayerPointer->standingOnObjectM2Index)) {")
        display(file, "x2_successful = 1")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "} while (x2_focusedPlayerNumber < player_count)")
        display(file, "}")
        display(file, "if (x2_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 3:
        display(file, "if (1 == 0) {")
    elif functionType == 4:
        display(file, "if (*(ushort *)(behaviour + %s) %s== %s) {" % (hex((params[1] * 2) + 0x44), inverseFlagChar, str(params[0])))
    elif functionType == 5:
        display(file, "if (FUN_806425FC(%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), inverseFlagInvertedChar))
    elif functionType == 6:
        display(file, "if (*(code *)(%s)(behaviour,this->id,%s,%s) %s== 0) {" % (hex(0x80748048 + (params[0] * 4)), str(params[1]), str(params[2]), inverseFlagInvertedChar))
    elif functionType == 7:
        display(file, "if (FUN_80642500(behaviour + 0x14,%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), inverseFlagInvertedChar))
    elif functionType == 8:
        display(file, "if (*(byte *)(behaviour + 0x51) %s== 0) {" % (inverseFlagInvertedChar))
    elif functionType == 9:
        display(file, "if (*(byte *)(behaviour + 0x52) %s== 0) {" % (inverseFlagInvertedChar))
    elif functionType == 10:
        display(file, "xA_successful = 0")
        display(file, "xA_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "xA_focusedPlayerNumber_ = xA_focusedPlayerNumber")
        display(file, "xA_focusedPlayerNumber = (xA_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[xA_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "xA_focusedPlayerPointer = *(int *)(character_change_pointer[xA_focusedPlayerNumber_]->character_pointer)")
        display(file, "xA_successful = 0")
        display(file, "if (*(byte *)(xA_focusedPlayerPointer->locked_to_pad) == 2) {")
        display(file, "if (this->id == *(short *)(xA_focusedPlayerPointer->standingOnObjectM2Index)) {")
        display(file, "xA_successful = 1")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "} while (xA_focusedPlayerNumber < player_count)")
        display(file, "}")
        display(file, "if (xA_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 11:
        display(file, "xB_successful = 0")
        display(file, "xB_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "xB_focusedPlayerNumber_ = xB_focusedPlayerNumber")
        display(file, "xB_focusedPlayerNumber = (xB_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[xB_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "xB_focusedPlayerPointer = *(int *)(character_change_pointer[xB_focusedPlayerNumber_]->character_pointer)")
        display(file, "if (*(byte *)(xB_focusedPlayerPointer->locked_to_pad) == 3) {")
        display(file, "if (*(byte *)(xB_focusedPlayerPointer->unk0x12F == %s)) {" % (str(params[0])))
        display(file, "if (this->id == *(short *)(xB_focusedPlayerPointer->standingOnObjectM2Index)) {")
        display(file, "xB_successful = 1")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "} while (xB_focusedPlayerNumber < player_count)")
        display(file, "}")
        display(file, "if (xB_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 12:
        display(
            file,
            "if (%s(((((FLOAT_807F621C == FLOAT_807F61FC) && (FLOAT_807F6220 == 1729.11706543)) && ((FLOAT_807F6224 == 3433.54956055 && ((FLOAT_807F6228 == 330 && (FLOAT_807F622C == 170)))))) && (FLOAT_807F6230 == 0)) && (FLOAT_807F6234 == 1))) {"
            % (inverseFlagInvertedChar),
        )
    elif functionType == 13:
        display(file, "xC_successful = 0")
        display(file, "xC_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "xC_focusedPlayerNumber_ = xC_focusedPlayerNumber")
        display(file, "xC_focusedPlayerNumber = (xC_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[xC_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "xC_focusedPlayerPointer = *(int *)(character_change_pointer[xC_focusedPlayerNumber_]->character_pointer)")
        display(file, "if (*(byte *)(xC_focusedPlayerPointer->locked_to_pad) == 1) {")
        display(file, "if (this->id == *(short *)(xC_focusedPlayerPointer->standingOnObjectM2Index)) {")
        display(file, "if (this->id == *(byte *)(xC_focusedPlayerPointer->unk0x10E == %s)) {" % (str(params[0])))
        display(file, "xC_successful = 1")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "} while (xC_focusedPlayerNumber < player_count)")
        display(file, "}")
        display(file, "if (xC_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 14:
        display(file, "if (FUN_80641F70(param_1,%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 15:
        display(file, "if (FUN_80723C98(*(word *) (behaviour + 0x38)) %s== 0) {" % (inverseFlagInvertedChar))
    elif functionType == 16:
        x10_conditional = ""
        x10_conditional_2 = ""
        if params[1] != -1:
            x10_conditional = "(*(byte *)(behaviour + 0x5C) != %s) || " % (str(params[1]))
        if params[0] != 0:
            x10_conditional_2 = "(FUN_8067ACC0(*(ushort *)(behaviour + 0x5E)) & %s)" % (str(params[0]))
            display(file, "if ((((*(byte *)(behaviour + 0x5C) == 0) || %s%s)) || (canHitSwitch() == 0)) {" % (x10_conditional, x10_conditional_2))
            display(file, "x10_uvar9 = 0")
            display(file, "} else {")
            display(file, "FUN_80641724(ObjectModel2ArrayPointer[id2index(this->id)].object_type)")
            display(file, "x10_uvar9 = 1")
            display(file, "}")
            display(file, "if (x10_uvar9 %s== 1) {" % (inverseFlagChar))
        else:
            if inverseFlag == 1:
                display(file, "if (true) {")
            else:
                display(file, "if (1 == 0) {")
    elif functionType == 17:
        display(file, "x11_successful = false")
        display(file, "if (loadedActorCount != 0) {")
        display(file, "x11_focusedArraySlot = &loadedActorArray")
        display(file, "x11_focusedActor = loadedActorArray")
        display(file, "while (true) {")
        display(file, "x11_focusedArraySlot = x11_focusedArraySlot + 8")
        display(file, "if ((*(uint *)(x11_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
        display(file, "if (*(int *)(x11_focusedActor->actor_type) == %s) {" % (str(params[0])))
        display(file, "if (x11_focusedActor->locked_to_pad == 1) {")
        display(file, "if (this->id == *(short *)(x11_focusedActor->standingOnObjectM2Index)) {")
        display(file, "x11_successful = true")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x11_focusedArraySlot) || (x11_successful)) break;")
        display(file, "}")
        display(file, "}")
        display(file, "if (%sx11_successful) {" % (inverseFlagChar))
    elif functionType == 18:
        display(file, "x12_successful = false")
        display(file, "if (loadedActorCount != 0) {")
        display(file, "x12_focusedArraySlot = &loadedActorArray")
        display(file, "x12_focusedActor = loadedActorArray")
        display(file, "while (true) {")
        display(file, "x12_focusedArraySlot = x12_focusedArraySlot + 8")
        display(file, "if ((*(uint *)(x12_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
        display(file, "if (*(int *)(x12_focusedActor->actor_type) == %s) {" % (str(params[0])))
        display(file, "if (x12_focusedActor->locked_to_pad == 1) {")
        display(file, "if (this->id == *(short *)(x12_focusedActor->standingOnObjectM2Index)) {")
        display(file, "if (*(short *)(x12_focusedActor->unk10E) == %s) {" % (str(params[1])))
        display(file, "x12_successful = true")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x12_focusedArraySlot) || (x12_successful)) break;")
        display(file, "x12_focusedActor = *x12_focusedArraySlot")
        display(file, "}")
        display(file, "}")
        display(file, "if (%sx12_successful) {" % (inverseFlagChar))
    elif functionType == 19:
        display(file, "if (isPlayerWithinDistanceOfObject(%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 20:
        display(file, "x14_successful_count = 0")
        display(file, "x14_focusedArraySlot = &loadedActorArray")
        display(file, "if (loadedActorCount != 0) {")
        display(file, "x14_focusedActor = loadedActorArray")
        display(file, "while (true) {")
        display(file, "x14_focusedArraySlot = x14_focusedArraySlot + 8")
        display(file, "if ((*(uint *)(x14_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
        display(file, "if (*(int *)(x14_focusedActor->actor_type) == %s) {" % (str(params[0])))
        display(file, "if (x14_focusedActor->locked_to_pad == 1) {")
        display(file, "if (this->id == *(short *)(x14_focusedActor->standingOnObjectM2Index)) {")
        display(file, "if (*(short *)(x14_focusedActor->unk10E) == %s) {" % (str(params[1])))
        display(file, "x14_successful_count = true")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x14_focusedArraySlot)) break;")
        display(file, "x14_focusedActor = *x14_focusedArraySlot")
        display(file, "}")
        display(file, "}")
        display(file, "if (x14_successful_count %s== %s) {" % (inverseFlagChar, str(params[2])))
    elif functionType == 21:
        display(file, "if (FUN_80650D04(this->id,%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 22:
        display(file, "if ((LevelStateBitfield & %s) != 0) {" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 23:
        display(file, "x17_successful = 0")
        display(file, "x17_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "x17_focusedPlayerNumber_ = x17_focusedPlayerNumber")
        display(file, "x17_focusedPlayerNumber = (x17_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[x17_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "x17_focusedPlayerPointer = *(int *)(character_change_pointer[x17_focusedPlayerNumber_]->character_pointer)")
        display(file, "if (*(byte *)(x17_focusedPlayerPointer->control_state) == %s) {" % (str(params[0])))
        if params[1] == 0:
            display(file, "x17_successful = 1")
        else:
            display(file, "if (x17_focusedPlayerPointer->control_state_progress == %s) {" % (str(params[1])))
            display(file, "x17_successful = 1")
            display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "} while (x17_focusedPlayerNumber < player_count)")
        display(file, "}")
        display(file, "if (x17_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 24:
        display(file, "x18_successful = 0")
        display(file, "if (*(byte *)(behaviour + 0x5C) != 0) {")
        if params[1] != -1:
            display(file, "if (*(byte *)(behaviour + 0x5C) == %s){" % (str(params[1])))
        display(file, "if ((*(ushort *)(behaviour + 0x5E) == %s) && canHitSwitch() != 0) {" % (str(params[0])))
        display(file, "FUN_80641724(ObjectModel2Array[id2index(this->id)].object_type)")
        display(file, "x18_successful = 1")
        display(file, "}")
        if params[1] != -1:
            display(file, "}")
        display(file, "}")
        display(file, "if (x18_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 25:
        display(file, "if (*(int *)(PlayerPointer->ActorType) %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 26:
        display(file, "if (*(byte *)(character_change_pointer->unk0x2C0) %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 27:
        display(file, "if (*(byte *)(character_change_pointer->unk0x2C1) %s== 0){" % (inverseFlagInvertedChar))
    elif functionType == 28:
        display(file, "x1C_svar6 = 80650a70()")
        if params[1] == 0:
            if inverseFlag == 0:
                display(file, "if (x1C_svar6 < %s) {" % (str(params[2])))
            else:
                display(file, "if (x1C_svar6 >= %s) {" % (str(params[2])))
        elif params[1] == 1:
            if inverseFlag == 0:
                display(file, "if (x1C_svar6 >= %s) {" % (str(params[2])))
            else:
                display(file, "if (x1C_svar6 < %s) {" % (str(params[2])))
        else:
            display(file, "if (1 == 0) {")
    elif functionType == 29:
        if params[0] == 0:
            if inverseFlag == 0:
                display(file, "if (*(byte *)(behaviour + %s) < %s) {" % (hex(0x48 + params[2]), str(params[1])))
            else:
                display(file, "if (*(byte *)(behaviour + %s) >= %s) {" % (hex(0x48 + params[2]), str(params[1])))
        elif params[0] == 1:
            if inverseFlag == 0:
                display(file, "if (*(byte *)(behaviour + %s) >= %s) {" % (hex(0x48 + params[2]), str(params[1])))
            else:
                display(file, "if (*(byte *)(behaviour + %s) < %s) {" % (hex(0x48 + params[2]), str(params[1])))
        else:
            display(file, "if (1 == 0) {")
    elif functionType == 30:
        display(file, "if ((FUN_80726D7C() & 0xFF) %s== 0){" % (inverseFlagInvertedChar))
    elif functionType == 31:
        if inverseFlag == 0:
            display(file, "if (1 == 0) {")
        else:
            display(file, "if (true) {")
    elif functionType == 32:
        display(file, "if ((FUN_806422D8() & 0xFF) %s== 0){" % (inverseFlagInvertedChar))
    elif functionType == 33:
        display(file, "x21_successful = 0")
        display(file, "x21_focusedPlayerNumber = 0")
        display(file, "if (player_count != 0) {")
        display(file, "do {")
        display(file, "x21_focusedPlayerNumber_ = x21_focusedPlayerNumber")
        display(file, "x21_focusedPlayerNumber = (x21_focusedPlayerNumber_ + 1) & 0xFF")
        display(file, "if (*(byte *)(character_change_pointer[x21_focusedPlayerNumber_]->does_player_exist) != 0) {")
        display(file, "x21_focusedPlayerPointer = *(int *)(character_change_pointer[x21_focusedPlayerNumber_]->character_pointer)")
        display(file, "if (*(byte *)(x21_focusedPlayerPointer->control_state_progress) == %s) {" % (str(params[0])))
        display(file, "x21_successful = 1")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "if (x21_successful %s== 1) {" % (inverseFlagChar))
    elif functionType == 34:
        display(file, "if (touchingModelTwoById(%s) %s== 0) {" % (hex(params[0]), inverseFlagInvertedChar))
    elif functionType == 35:
        display(file, "if (CutsceneActive %s== 1) {" % (inverseFlagChar))
    elif functionType == 36:
        display(file, "x24_focusedActor = getSpawnerTiedActor(%s,0)" % (str(params[0])))
        display(file, "if (*(byte *)(x24_focusedActor->control_state) %s== %s) {" % (inverseFlagChar, str(params[1])))
    elif functionType == 37:
        display(file, "if (%s(*(byte *)CurrentCollectableBase->SlamLvl => %s)) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 38:
        display(file, "if ((*(uint *)(PlayerPointer->unk0x368) & %s) %s== 0) {" % (hex((params[0] * 0x10000) + params[1]), inverseFlagInvertedChar))
    elif functionType == 39:
        display(file, "if ((*(uint *)(PlayerPointer->effectBitfield) & %s) %s== 0) {" % (hex((params[0] * 0x10000) + params[1]), inverseFlagInvertedChar))
    elif functionType == 40:
        display(file, "if ((*(byte *)(behaviour + 0x9A) & 1) %s== 0) {" % (inverseFlagChar))
    elif functionType == 41:
        display(file, "if (notTouchingActorSpawnerWithinRan(%s,%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), str(params[2]), inverseFlagInvertedChar))
    elif functionType == 42:
        if inverseFlag == 0:
            display(file, "if (BYTE_807F61F8 != 0 || *(byte *)(PTR_0x807F61F0->control_state) == 5) {")
        else:
            display(file, "if (BYTE_807F61F8 == 0 && *(byte *)(PTR_0x807F61F0->control_state) != 5) {")
    elif functionType == 43:
        display(file, "if (BYTE_807F61F8 %s== 0) {" % (inverseFlagInvertedChar))
    elif functionType == 44:
        display(file, "if (FUN_80689BAC(%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 45:
        display(file, "if (checkFlag(%s>%s,'Permanent') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
    elif functionType == 46:
        display(file, "if (getAndSetActorSpawnerControlStateFromActorSpawnerID(%s,0,'%s') %s== %s) {" % (str(params[0]), getSetOrNot(0), inverseFlagChar, str(params[1])))
    elif functionType == 47:
        display(file, "if ((isCharacterSpawnerInState7(%s) & 0xFF) %s== 0) {" % (str(params[0] & 0xFF), inverseFlagInvertedChar))
    elif functionType == 48:
        display(file, "if (*(byte *)(PlayerPointer->unk0xD1) %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 49:
        display(file, "x31_ivar10_4 = id2index(&WORD_807F6240[%s])" % (str(params[0])))
        display(file, "if (ObjectModel2ArrayPointer[x31_ivar10_4]->behaviour_pointer[%s] %s== %s) {" % (hex(0x48 + params[2]), inverseFlagChar, str(params[1])))
    elif functionType == 50:
        display(file, "if (*(ushort *)PreviousMap %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 51:
        if params[0] == 0:
            if inverseFlag == 0:
                display(file, "if (%s < FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
            else:
                display(file, "if (%s >= FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
        elif params[0] == 1:
            if inverseFlag == 0:
                display(file, "if (%s >= FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
            else:
                display(file, "if (%s < FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
        else:
            display(file, "if (1 == 0) {")
    elif functionType == 52:
        display(file, "x34_uvar4 == FUN_806C8D2C(%s)" % (str(params[0])))
        if inverseFlag == 0:
            display(file, "if (%s <= &character_collectable_base[(BYTE_807FC929 * 0x5E) + (0x306 * x34_uvar4)] {" % (str(params[1])))
        else:
            display(file, "if (%s > &character_collectable_base[(BYTE_807FC929 * 0x5E) + (0x306 * x34_uvar4)] {" % (str(params[1])))
    elif functionType == 53:
        display(file, "if (*(byte *)PlayerPointer->0xD0 %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 54:
        display(file, "if (checkFlag(%s>%s,'Temporary') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
    elif functionType == 55:
        display(file, "FUN_80650D8C(this->id,%s,austack30,austack36)" % (str(params[0])))
        display(file, "if (austack30[0] %s== %s) {" % (inverseFlagChar, str(params[1])))
    elif functionType == 56:
        display(file, "if (%s(*(byte *)Character < 5)) {" % (inverseFlagChar))
    elif functionType == 57:
        display(file, "if ((%s& *(ushort *)PlayerPointer->CollisionQueue->TypeBitfield) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 58:
        display(file, "if (((1 << %s) & BYTE_807F693E) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
    elif functionType == 59:
        display(file, "if (checkFlag(%s>%s,'Global') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
    elif functionType == 60:
        display(file, "if (PlayerPointer->chunk %s== %s) {" % (inverseFlagChar, str(params[0])))
    elif functionType == 61:
        display(file, "if (BYTE_807F6903 %s== 0) {" % (inverseFlagInvertedChar))
    else:
        display(file, "if ([%s,%s,%s,%s]) {" % (str(functionType), str(params[0]), str(params[1]), str(params[2])))


def grabExecution(param_1, ScriptCommand, params, behaviour, param_3, file):
    """Convert execution into a series of C-Like lines."""
    functionType = ScriptCommand
    if functionType == 0:
        display(file, "FUN_80642748(%s,%s,%s)" % (str(params[0]), str(params[1]), str(behaviour)))
    elif functionType == 1:
        display(file, "*(byte *)(behaviour + %s) = %s" % (hex(params[1] + 0x4B), str(params[0])))
    elif functionType == 2:
        display(file, "FUN_80723284(*(int*)(behaviour + 0x38),%s)" % (str(params[0])))
    elif functionType == 3:
        if params[0] == 0:
            display(file, "*(short *)(behaviour + %s) = %s" % (hex((params[2] * 2) + 0x44), str(params[1])))
        else:
            display(file, "*(short *)(behaviour + %s) = *(short *)(behaviour + %s)" % (hex((params[2] * 2) + 0x44), hex((params[1] * 4) + 0x14)))
    elif functionType == 4:
        display(file, "FUN_80723484(*(int *)(behaviour + 0x38))")
        display(file, "FUN_807238D4(*(int *)(behaviour + 0x38),0x807F621C,0x807F6220,0x807F6224)")
    elif functionType == 5:
        display(file, "FUN_806418E8(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
    elif functionType == 6:
        display(file, "*(float *)(behaviour + %s) = %s" % (hex((params[0] * 4) + 0x14), str(params[1] / 10)))
    elif functionType == 7:
        display(file, "*(code *)(%s)(behaviour,this->id,%s,%s)" % (hex(0x80747E70 + (params[0] * 4)), str(params[1]), str(params[2])))
    elif functionType == 8:
        display(file, "FUN_80642844(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
    elif functionType == 9:
        display(file, "if ((FLOAT_807F621C != FLOAT_807F61FC) || (FLOAT_807F6224 != 3433.54956055)) {")
        display(file, "FUN_80642480(%s)" % (str(params[0])))
        display(file, "}")
    elif functionType == 0xA:
        display(file, "*(byte *)(behaviour + 0x50) = %s" % (str(params[0])))
        display(file, "*(float *)(behaviour + 0x78) = %s" % (str(params[1] / 100)))
        display(file, "*(float *)(behaviour + 0x7C) = %s" % (str(params[2] / 100)))
    elif functionType == 0xB:
        display(file, "*(short *)(behaviour + 0x80) = %s" % (str(params[0])))
        display(file, "*(short *)(behaviour + 0x82) = %s" % (str(params[1])))
    elif functionType == 0xC:
        display(file, "*(short *)(behaviour + 0x84) = %s" % (str(params[0])))
        display(file, "*(short *)(behaviour + 0x86) = %s" % (str(params[1])))
    elif functionType == 0xD:
        display(file, "*(short *)(behaviour + 0x88) = %s" % (str(params[0])))
        display(file, "*(short *)(behaviour + 0x8A) = %s" % (str(params[1])))
    elif functionType == 0xE:
        display(file, "if (*(short *)(behaviour + %s) < 0) {" % (hex(((params[0] & 1) * 2) + 0x10)))
        display(file, "*(short *)(behaviour + %s) = FUN_80605044(this->id,%s,%s,%s)" % (hex(((params[0] & 1) * 2) + 0x10), str(params[0]), str(params[2] & 0x7F), str(params[1] & 2)))
        display(file, "}")
    elif functionType == 0xF:
        xF_ivar5 = params[1]
        if params[1] < 0:
            xF_ivar5 = xF_ivar5 + 0x7F
        xF_uvar9 = (xF_ivar5 >> 7) & 0xFF
        xF_bvar15 = xF_uvar9
        xF_ivar5 = params[2]
        if params[2] < 0:
            xF_ivar5 = xF_ivar5 + 0x7F
        xF_uvar14 = (xF_ivar5 >> 7) & 0xFF
        if xF_uvar9 == 0:
            xF_bvar15 = 0x7F
        if xF_uvar14 == 0:
            xF_uvar14 = 0xFF
        display(file, "FUN_806085DC(this->id,%s,%s,%s)" % (str(params[0]), str(xF_uvar14), str(xF_bvar15)))
    elif functionType == 0x10:
        display(file, "x10_temp = *(short *)(behaviour + %s)" % (hex((params[1] * 2) + 0x10)))
        display(file, "if (-1 < x10_temp) {")
        display(file, "FUN_80605380(x10_temp)")
        display(file, "*(short *)(behaviour + %s) = 0xFFFF" % (hex((params[1] * 2) + 0x10)))
        display(file, "}")
    elif functionType == 0x11:
        display(file, "FUN_806508B4(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x12:
        display(file, "FUN_8065092C(this->id,%s)" % (str(params[0])))
    elif functionType == 0x13:
        display(file, "FUN_80650998(this->id,%s)" % (str(params[0])))
    elif functionType == 0x14:
        display(file, "FUN_80650A04(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x15:
        display(file, "FUN_80650b50(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x16:
        display(file, "FUN_80650BBC(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x17:
        display(file, "FUN_80650C28(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x18:
        display(file, "FUN_80650C98(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x19:
        display(file, "setCharacterChangeParameters(%s,0,0)" % (str(params[0])))
    elif functionType == 0x1A:
        display(file, "FUN_80650AD8(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
    elif functionType == 0x1B:
        display(file, "if ((&WORD_807F6240)[%s] != -1) {" % (str(params[0])))
        display(file, "FUN_806335B0((&WORD_807F6240)[%s],1,%s)" % (str(params[0]), str(params[1])))
        display(file, "}")
    elif functionType == 0x1C:
        display(file, "if ((&WORD_807F6240)[id2index(%s)] != -1) {" % (str(params[0])))
        display(file, "x1C_ivar7 = (&WORD_807F6240)[%s]" % (str(params[0])))
        display(file, "if ((x1C_ivar7 != -1) && (ObjectModel2ArrayPointer[x1C_ivar7].behaviour != 0)) {")
        display(file, "x1C_puvar10 = ObjectModel2ArrayPointer[x1C_ivar7].behaviour + %s" % (str(params[1])))
        display(file, "x1C_puvar10[0x48] = x1C_puvar10[0x48] + %s" % str(params[2]))
        display(file, "}")
        display(file, "}")
    elif functionType == 0x1D:
        display(file, "FUN_80642844(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
    elif functionType == 0x1E:
        display(file, "FUN_80642748(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
    elif functionType == 0x1F:
        display(file, "FUN_807232EC(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
    elif functionType == 0x20:
        display(file, "FUN_80723380(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
    elif functionType == 0x21:
        display(file, "FUN_80723320(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
    elif functionType == 0x22:
        display(file, "*(int *)(behaviour + 0x38) = FUN_80723020(FLOAT_807F6220,FLOAT_807F6224,%s)" % (str(params[2])))
    elif functionType == 0x23:
        display(file, "FUN_80723428(*(int *)(behaviour + 0x38))")
        display(file, "*(int *)(behaviour + 0x38) = 0xFFFFFFFF")
    elif functionType == 0x24:
        display(file, "FUN_8072334C(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
    elif functionType == 0x25:
        display(file, "playCutsceneFromModelTwoScript(behaviour,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x26:
        display(file, "FUN_8064199C(behaviour,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x27:
        display(file, "FUN_80634EA4(this->id,%s,%s)" % (str(params[0]), str(params[1] & 0xFF)))
    elif functionType == 0x28:
        display(file, "FUN_80635018(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x29:
        display(file, "FUN_8061EF4C(0x29,PlayerPointer->unk0x27C,%s,%s,FLOAT_807F621C)" % (str(params[0] & 0xFF), str(params[1])))
    elif functionType == 0x2A:
        display(file, "ObjectModel2ArrayPointer[id2Index(this->id)]->unk0x3C = %s" % (str(params[0])))
    elif functionType == 0x2B:
        display(file, "FUN_80636014(this->id,1)")
    elif functionType == 0x2C:
        display(file, "FUN_806335B0(this->id,1,%s") % (str(params[0]))
        display(file, "FUN_8067A9F0(0,PlayerPointer)")
    elif functionType == 0x2D:
        display(file, "x2d_counter = 0")
        display(file, "x2d_PTR_focusedLoadedActor = &PTR_DAT_807FB930")
        display(file, "if (loadedActorCount != 0) {")
        display(file, "do {")
        display(file, "x2d_ADDR_focusedLoadedActor = *x2d_PTR_focusedLoadedActor")
        display(file, "x2d_counter = x2d_counter + 1")
        display(file, "if ((*(uint *)(x2d_ADDR_focusedLoadedActor->object_properties_bitfield_1) & 0x2000) == 0) {")
        display(file, "if (x2d_ADDR_focusedLoadedActor->locked_to_pad == 0x1) {")
        display(file, "if (this->id == *(word *)(x2d_ADDR_focusedLoadedActor->unk0x10C)) {")
        if params[0] == 0:
            display(file, "*(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) = *(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) & 0xFFFB")
        else:
            display(file, "*(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) = *(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) | 4")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "x2d_PTR_focusedLoadedActor = x2d_PTR_focusedLoadedActor + 8")
        display(file, "x2d_finishedArray = x2d_counter < loadedActorCount")
        display(file, "} while(x2d_finishedArray)")
        display(file, "}")
    elif functionType == 0x2E:
        display(file, "FUN_80651BC0(%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x2F:
        display(file, "FUN_8060B49C(PlayerPointer,%s)" % (str(params[0])))
    elif functionType == 0x30:
        display(file, "InitMapChange(%s,0)" % (str(params[0])))
    elif functionType == 0x31:
        if (params[2] & 0x100) != 0:
            display(file, "SetIntroStoryPlaying(2)")
            display(file, "setNextTransitionType('Fade (Wrong Cutscene)')")
        if (params[2] & 0xFF) == 0:
            display(file, "InitMapChange_TransferredActor(%s,%s,0,0)" % (str(params[0]), str(params[1])))
        else:
            if (params[2] & 0xFF) == 1:
                display(file, "InitMapChange_TransferredActor(%s,%s,0,1)" % (str(params[0]), str(params[1])))
            elif (params[2] & 0xFF) == 2:
                display(file, "InitMapChange_TransferredActor(%s,%s,0,3)" % (str(params[0]), str(params[1])))
            else:
                display(file, "InitMapChange_TransferredActor(%s,%s,0,0)" % (str(params[0]), str(params[1])))
    elif functionType == 0x32:
        display(file, "InitMapChange_ParentMap(%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x33:
        display(file, "FUN_8062B86C(%s,(float)%s,(float)%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
    elif functionType == 0x34:
        display(file, "FUN_8062B8A4(%s,(float)%s,(float)%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
    elif functionType == 0x35:
        display(file, "FUN_80641C98(%s,%s,this->id)" % (str(params[0]), str(params[1])))
    elif functionType == 0x36:
        display(file, "FUN_80641BCC(%s,%s,this->id)" % (str(params[0]), str(params[1])))
    elif functionType == 0x37:
        display(file, "FUN_80679200(PlayerPointer,0,0x400000,%s)" % (str(params[0] & 0xFF)))
    elif functionType == 0x38:
        display(file, "FUN_80651be0(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x39:
        display(file, "*(byte *)(behaviour + 0x4F) = %s" % (str(params[0])))
    elif functionType == 0x3A:
        display(file, "// Execution Type 0x3A stripped from final. Parameters: %s, %s, %s" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x3B:
        display(file, "*(uint *)(PlayerPointer->unk0x368) = *(uint *)(PlayerPointer->unk0x368) & ~%s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x3C:
        display(file, "if (*(int *)(behaviour + 0x94) != 0) {")
        display(file, "FUN_806782C0(*(int *)(behaviour + 0x94))")
        display(file, "*(int *)(behaviour + 0x94) = 0")
        display(file, "}")
    elif functionType == 0x3D:
        display(file, "*(byte *)(behaviour + 0x67) = %s" % (str(params[0])))
    elif functionType == 0x3E:
        display(file, "*(byte *)(behaviour + 0x6F) = %s" % (str(params[0])))
    elif functionType == 0x3F:
        display(file, "*(byte *)(behaviour + 0x6E) = %s" % (str(params[0])))
    elif functionType == 0x40:
        display(file, "*(int *)LevelStateBitfield = *(int *)LevelStateBitfield | %s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x41:
        display(file, "WORD_807F6904 = 1")
    elif functionType == 0x42:
        display(file, "FUN_80634CC8(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x43:
        display(file, "if (%s == 1) {" % (str(params[0])))
        display(file, "*(int *)(behaviour + 0x8) = *(int *)(behaviour + %s)" % (hex((params[1] * 4) + 0x14)))
        display(file, "*(int *)(behaviour + 0xC) = *(int *)(behaviour + %s)" % (hex((params[2] * 4) + 0x14)))
        display(file, "}")
        display(file, "else {")
        display(file, "*(float *)(behaviour + 0x8) = %s" % (str(params[1] / 10)))
        display(file, "*(float *)(behaviour + 0xC) = %s" % (str(params[2] / 10)))
        display(file, "}")
    elif functionType == 0x44:
        display(file, "WORD_807F6906 = %s" % (str(params[0])))
        display(file, "WORD_807F6908 = %s" % (str(params[1])))
    elif functionType == 0x45:
        display(file, "*(byte *)(behaviour + 0x60) = %s" % (str(params[0])))
        display(file, "*(ushort *)(behaviour + 0x62) = %s" % (str(params[1])))
        display(file, "*(byte *)(behaviour + 0x66) = %s" % (str(params[2])))
    elif functionType == 0x46:
        display(file, "*(byte *)(behaviour + 0x70) = %s" % (str(params[0])))
    elif functionType == 0x47:
        display(file, "*(byte *)(behaviour + 0x71) = %s" % (str(params[0])))
    elif functionType == 0x48:
        display(file, "FUN_80604BE8(*(byte *)(behaviour + %s,%s,%s)" % (hex((params[0] * 2) + 0x11), str(params[1] / 100), str(params[2])))
    elif functionType == 0x49:
        display(file, "FUN_8067ABC0(%s,FLOAT_807F621C,FLOAT_807F6220,FLOAT_807F6224)" % (str(params[2])))
    elif functionType == 0x4A:
        display(file, "FUN_8063393C(this->id,1,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x4B:
        display(file, "FUN_8072ED9C(this->id,%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x4C:
        display(file, "x4C_temp = FUN_80650A70()")
        display(file, "x4C_temp = (x4C_temp + %s)" % (hex(params[1])))
        display(file, "if (x4C_temp < 0) {")
        display(file, "x4C_temp = 0")
        display(file, "}")
        display(file, "FUN_80650A04(this->id,%s,x4C_temp)" % (str(params[0])))
    elif functionType == 0x4D:
        display(file, "x4D_svar12 = SpawnModelTwoObject(0,%s,FLOAT_807F690C,FLOAT_807F6910,FLOAT_807F6914)" % (str(params[0])))
        if params[1] == 0:
            display(file, "FUN_80641B00(x4D_svar12,this->id,%s)" % (str(params[2])))
        end
    elif functionType == 0x4E:
        display(file, "FUN_807146A4(%s)" % (str(params[0])))
        display(file, "FUN_807149B8(1)")
        display(file, "FUN_80714B84(0)")
    elif functionType == 0x4F:
        display(file, "if (BYTE_807F6938 != 0x10) {")
        if params[0] == -2:
            display(file, "(&WORD_807F6918)[BYTE_807F6938] = ObjectModel2ArrayPointer[id2index(this->id)]->id")
        else:
            display(file, "(&WORD_807F6918)[BYTE_807F6938] = %s" % (str(params[0])))
        display(file, "BYTE_807F6938 = BYTE_807F6938 + 1")
    elif functionType == 0x50:
        display(file, "if ((&WORD_807F6240)[%s] != -1) {" % (str(params[0])))
        display(file, "FUN_806335B0((&WORD_807F6240)[%s],1,%s)" % (str(params[0]), str(params[1])))
        display(file, "}")
    elif functionType == 0x51:
        display(file, "FUN_806F4F50(this->id,FLOAT_807F621C,FLOAT_807F6220,FLOAT_807F6224)")
    elif functionType == 0x52:
        display(file, "// Execution Type 0x52 stripped from final. Parameters: %s,%s,%s" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x53:
        display(file, "// Execution Type 0x53 stripped from final. Parameters: %s,%s,%s" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x54:
        display(file, "x54_ivar7 = id2index((&WORD_807F6240)[%s])" % (str(params[0])))
        display(file, "if (x54_ivar7 != -1) {")
        display(file, "FUN_8064199C(ObjectModel2ArrayPointer[x54_ivar7].behaviour,%s,%s)" % (str(params[1]), str(params[2])))
        display(file, "}")
    elif functionType == 0x55:
        display(file, "FUN_8062B630(%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x56:
        display(file, "FUN_80724994(1,%s,0,0)" % (str(params[0])))
    elif functionType == 0x57:
        display(file, "FUN_80659620(&uStack52,&uStack56,&uStack60,WORD_807F693A)")
        display(file, "FUN_80659670(%s + fStack32, %s + fStack56,extraout_a0,extraout_a1, %s + fStack60, WORD_807F693A)" % (str(params[0] / 1000), str(params[1] / 1000), str(params[0] / 1000)))
    elif functionType == 0x58:
        display(file, "x58_temp = FUN_805FFE50(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
        display(file, "if (x58_temp == 0) {")
        display(file, "FUN_8063DB3C(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
        display(file, "}")
    elif functionType == 0x59:
        display(file, "FUN_80724994(3,%s,%s,0)" % (str(params[0]), str(params[1])))
    elif functionType == 0x5A:
        display(file, "*(ushort *)(behaviour + 0x68) = %s" % (str(params[0])))
        display(file, "*(ushort *)(behaviour + 0x6A) = %s" % (str(params[1])))
        display(file, "*(ushort *)(behaviour + 0x6C) = %s" % (str(params[2])))
    elif functionType == 0x5B:
        display(file, "FUN_806C92C4(%s)" % (str(params[0])))
    elif functionType == 0x5C:
        display(file, "FUN_80724A9C(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x5D:
        display(file, "setNextTransitionType(%s)" % (str(params[0])))
    elif functionType == 0x5E:
        display(file, "FUN_80641874()")
    elif functionType == 0x5F:
        display(file, "*(uint *)(PlayerPointer->ExtraInfo->unk0x1F0) = *(uint *)(PlayerPointer->ExtraInfo->unk0x1F0 | %s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x60:
        display(file, "FUN_8065F134()")
    elif functionType == 0x61:
        if params[2] == 0:
            display(file, "playSong('%s', 1)" % (getSongName(params[0])))
        else:
            display(file, "playSong('%s', %s)" % (getSongName(params[0]), str(params[2] / 255)))
    elif functionType == 0x62:
        display(file, "WORD_807F693A = %s" % (str(params[0])))
    elif functionType == 0x63:
        display(file, "FUN_8068B830()")
    elif functionType == 0x64:
        display(file, "FUN_8068B8FC()")
    elif functionType == 0x65:
        display(file, "*(byte *)(behaviour + %s) = (byte *)(behaviour + %s) + %s" % (hex(params[1] + 0x4B), hex(params[1] + 0x4B), str(params[0])))
    elif functionType == 0x66:
        display(file, "if (BYTE_807F61F8 == 0) {")
        display(file, "spawnActor(TimerController)")
        display(file, "temp = CurrentActorPointer")
        display(file, "WORD_807F61F4 = PTR_PTR_807FBB44")
        display(file, "CurrentActorPointer = mainmemory.read_u32_be(0x7FBB44)")
        display(file, "spawnTimer(0xDC,0x2A,%s)" % (str(params[0])))
        display(file, "BYTE_807F61F8 = 1")
        display(file, "WORD_807F61F0 = PTR_PTR_807FBB44")
        display(file, "CurrentActorPointer = temp")
        display(file, "}")
    elif functionType == 0x67:
        display(file, "if (BYTE_807F61F8 != 0) {")
        display(file, "FUN_806A2B08()")
        display(file, "}")
    elif functionType == 0x68:
        display(file, "if (BYTE_807F61F8 != 0) {")
        display(file, "FUN_806782C0(DWORD_807F61F0)")
        display(file, "FUN_806782C0(DWORD_807F61F4)")
        display(file, "}")
    elif functionType == 0x69:
        display(file, "FUN_80661398()")
    elif functionType == 0x6A:
        display(file, "FUN_806613E8(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
    elif functionType == 0x6B:
        display(file, "setFlag(%s>%s,%s,'Permanent')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
    elif functionType == 0x6C:
        display(file, "FUN_80631B8C(%s)" % (str(params[0])))
    elif functionType == 0x6D:
        display(file, "FUN_8063A8C4(this->id,1,%s)" % (str(params[0] / 100)))
    elif functionType == 0x6E:
        display(file, "BYTE_807F693F = %s" % (str(params[0])))
    elif functionType == 0x6F:
        display(file, "?playMusic(%s,%s)" % (str(params[0]), str(params[1] & 0xFF)))
    elif functionType == 0x70:
        display(file, "FUN_80602C6C(%s,%s)" % (str(params[0]), str(params[1] / 255)))
    elif functionType == 0x71:
        display(file, "FUN_80602DC4()")
    elif functionType == 0x72:
        display(file, "getAndSetActorSpawnerControlStateFromActorSpawnerID(%s,%s,'%s')" % (str(params[0]), str(params[1] & 0xFF), getSetOrNot(1)))
    elif functionType == 0x73:
        display(file, "FUN_806EB178(0,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
    elif functionType == 0x74:
        display(file, "*(byte *)(behaviour + 0x9B) = *(byte *)(behaviour + 0x9B) | %s" % (hex(params[0])))
    elif functionType == 0x75:
        display(file, "changeTriggerActiveStateOfFirstInstanceOfType('%s',%s)" % (getTriggerTypeName(params[0]), str(params[1])))
    elif functionType == 0x76:
        display(file, "x76_counter = 0")
        display(file, "x76_focusedLoadedActorSlot = &loadedActorArray")
        display(file, "if (loadedActorCount != 0) {")
        display(file, "do {")
        display(file, "x76_focusedLoadedActor = *x76_focusedLoadedActorSlot")
        display(file, "if ((*(uint *)(x76_focusedLoadedActor->object_properties_bitfield) & 0x2000) == 0) {")
        display(file, "if (x76_focusedLoadedActor->locked_to_pad == 1) {")
        display(file, "if (this->id == *(short *)(x76_focusedLoadedActor->unk0x10c)) {")
        display(file, "FUN_80679200(x76_focusedLoadedActor,0,8,0)")
        display(file, "}")
        display(file, "}")
        display(file, "}")
        display(file, "x76_counter = x76_counter + 1")
        display(file, "x76_focusedLoadedActorSlot = x76_focusedLoadedActorSlot + 8")
        display(file, "} while (x76_counter < loadedActorCount)")
        display(file, "}")
    elif functionType == 0x77:
        display(file, "FUN_80650794(this->id,%s,%s,%s)" % (str(params[0]), str(params[1] & 0xFF), str(params[2] / 1000)))
    elif functionType == 0x78:
        display(file, "FUN_806335B0(this->id,1,%s)" % (str(params[0])))
        display(file, "PlayerPointer->unk0x3A4 = uStack40")
        display(file, "PlayerPointer->unk0x3A8 = uStack44")
        display(file, "PlayerPointer->unk0x3AC = uStack48")
    elif functionType == 0x79:
        display(file, "setFlag(%s>%s,%s,'Temporary')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
    elif functionType == 0x7A:
        display(file, "FUN_80661264(%s,%s)" % (str(params[0] & 0xFF), str(params[0] & 0xFF)))
    elif functionType == 0x7B:
        display(file, "FUN_806335B0(this->id,%s)" % (str(params[1])))
        display(file, "FUN_8072ECFC(%s)" % (str(params[0])))
    elif functionType == 0x7C:
        display(file, "BYTE_80748094 = %s" % (str(params[0])))
    elif functionType == 0x7D:
        display(file, "if (*(short *)(behaviour + %s) < 0) {" % (hex((2 * params[1]) + 0x10)))
        display(file, "*(short *)(behaviour + %s) = FUN_80605044(this->id,%s,%s,%s)" % (hex((2 * params[1]) + 0x10), str(params[0]), str(params[2] & 0x7F), str(params[1] & 2)))
        display(file, "}")
    elif functionType == 0x7E:
        x7e_ivar5 = params[1]
        if params[1] < 0:
            x7e_ivar5 = x7e_ivar5 + 0x7F
        x7e_uvar9 = (x7e_ivar5 >> 7) & 0xFF
        x7e_ivar5 = params[2]
        if params[2] < 0:
            x7e_ivar5 = x7e_ivar5 + 0x7F
        x7e_uvar14 = (x7e_ivar5 >> 7) & 0xFF
        x7e_bvar15 = x7e_uvar14
        if x7e_uvar9 == 0:
            x7e_uvar9 = 0x7F
        if x7e_uvar14 == 0:
            x7e_bvar15 = 0xFF
        display(file, "if (BYTE_80748094 < 1) {")
        display(file, "playSFX(%s,0x7FFF,0x427C0000,%s)" % (str(params[0]), str(x7e_uvar9 / 127)))
        display(file, "}")
        display(file, "else {")
        display(file, "FUN_806335B0(this->id,1,BYTE_80748094)")
        display(file, "FUN_806086CC(%s,%s,%s,%s,0.3,0)" % (str(x7e_bvar15), str(x7e_uvar9), str(params[1] & 0x7F), str(params[2] & 0x7F)))
        display(file, "}")
    elif functionType == 0x7F:
        if params[1] == 0:
            x7f_temp = 0
        elif params[1] == 1:
            x7f_temp = 1
        elif params[1] == 2:
            x7f_temp = 2
        elif params[1] == 3:
            x7f_temp = 3
        else:
            x7f_temp = 0
        display(file, "FUN_8072EE0C(this->id,%s,%s)" % (str(params[0]), str(x7f_temp)))
    elif functionType == 0x80:
        display(file, "save()")
    elif functionType == 0x81:
        display(file, "BYTE_807F693E = BYTE_807F693E | (1 << %s)" % (str(params[0])))
    elif functionType == 0x82:
        display(file, "BYTE_807F693E = BYTE_807F693E & ~(1 << %s)" % (str(params[0])))
    elif functionType == 0x83:
        _item = "Unknown %s" % (hex(params[0]))
        if params[0] in hud_items:
            _item = hud_items[params[0]]
        display(file, "setHUDItemAsInfinite(%s,%s,%s)" % (_item, str(params[1]), getTOrF(params[2])))
    elif functionType == 0x84:
        display(file, "setFlag(%s>%s,%s,'Global')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
    elif functionType == 0x85:
        display(file, "FUN_8062D1A8()")
    elif functionType == 0x86:
        display(file, "FUN_806CF398(PlayerPointer)")
        display(file, "InitMapChange_TransferredActor(0x2A,0,%s,2)" % (str(params[0])))
    elif functionType == 0x87:
        display(file, "warpOutOfBonusGame()")
    elif functionType == 0x88:
        display(file, "DWORD_807FBB68 = DWORD_807FBB68 | %s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x89:
        display(file, "DWORD_807FBB68 = DWORD_807FBB68 & ~%s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x8A:
        display(file, "FUN_806417BC(%s,%s)" % (str(params[0]), str(params[1])))
    elif functionType == 0x8B:
        display(file, "*(uint *)(PlayerPointer->unk0x36C) = *(uint *)(PlayerPointer->unk0x36C) & ~%s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x8C:
        display(file, "*(uint *)(PlayerPointer->unk0x36C) = *(uint *)(PlayerPointer->unk0x36C) | %s" % (hex((params[0] * 0x10000) + params[1])))
    elif functionType == 0x8D:
        display(file, "next_transition_type = 'Fade'")
        display(file, "FUN_806CF398(PlayerPointer)")
        display(file, "x8d_uvar5 = getWorld(CurrentMap,0)")
        display(file, "x8d_ivar6 = isLobby(CurrentMap)")
        display(file, "x8d_ivar7 = x8d_uvar5")
        display(file, "if (x8d_ivar6 == 0) {")
        display(file, "warpOutOfLevel(x8d_ivar7)")
        display(file, "}")
        display(file, "else {")
        display(file, "x8d_svar12 = *(short *)(&DAT_8074809C + (x8d_ivar7 * 2))")
        display(file, "x8d_dstack88 = (short)(&WORD_807480AC)[x8d_ivar7]")
        display(file, "x8d_uvar9 = isFlagSet(*(short *)(&DAT_807480BC + (x8d_ivar7 * 2)),'Permanent')")
        display(file, "if ((x8d_uvar9 == 0) && (x8d_svar12 == 0x57)) {")
        display(file, "x8d_dstack88 = 0x15")
        display(file, "}")
        display(file, "x8d_ivar6 = DetermineLevel_NewLevel()")
        display(file, "if (x8d_ivar6 == 0) {")
        display(file, "InitMapChange(x8d_svar12,x8d_dstack88)")
        display(file, "}")
    elif functionType == 0x8E:
        display(file, "FUN_8066C904(&ObjectModel2ArrayPointer[id2index(this->id)]->unk0x28)")
    elif functionType == 0x8F:
        display(file, "FUN_806348B4(&ObjectModel2ArrayPointer[id2index(this->id)]->unk0x48)")
    elif functionType == 0x90:
        display(file, "BYTE_807F6902 = %s" % (str(params[0])))
    elif functionType == 0x91:
        display(file, "*(float *)(PlayerPointer->velocity) = %s" % (str(params[0])))
    elif functionType == 0x92:
        display(file, "*(uint *)(PlayerPointer->unk0x368) = *(uint *)(PlayerPointer->unk0x368) | 0x40000800")
    elif functionType == 0x93:
        display(file, "FUN_8061F510(%s,%s)" % (str(params[0] & 0xFF), str(params[1] & 0xFF)))
    elif functionType == 0x94:
        display(file, "FUN_80724994(2,%s,0,0)" % (str(params[0])))
    elif functionType == 0x95:
        display(file, "WORD_807F693C = 0x80")
    elif functionType == 0x96:
        display(file, "BYTE_807F6903 = %s" % (str(params[0])))
    else:
        display(file, "[%s,%s,%s,%s]" % (str(functionType), str(params[0]), str(params[1]), str(params[2])))


def readData(data, size, read_location):
    """Read data from a file."""
    return bytereadToInt(data[read_location : read_location + size])


def grabScripts(data, file_path):
    """Grab Scripts from file."""
    global tab_indentation
    global folder_removal

    read_location = 0
    script_count = readData(data, 2, read_location)
    if script_count == 0:
        folder_removal.append(file_path)
    elif script_count > 0:
        complete_setup = []
        with open(f"{file_path}/scripts.raw", "wb") as fh:
            fh.write(data)
        with open(file_path + "/setup.bin", "rb") as setupFile:
            with open(file_path + "/setup.json", "w") as setupJson:
                setupFile.seek(0)
                modeltwo_count = bytereadToInt(setupFile.read(4))
                setup_read = 4
                for item in range(modeltwo_count):
                    setupFile.seek(setup_read + 0x2A)
                    _id = bytereadToInt(setupFile.read(2))
                    setupFile.seek(setup_read + 0x28)
                    _type = bytereadToInt(setupFile.read(2))
                    setupFile.seek(setup_read)
                    _x = bytereadToInt(setupFile.read(4))
                    setupFile.seek(setup_read + 4)
                    _y = bytereadToInt(setupFile.read(4))
                    setupFile.seek(setup_read + 8)
                    _z = bytereadToInt(setupFile.read(4))
                    complete_setup.append({"_id": _id, "_type": _type, "_x": _x, "_y": _y, "_z": _z})
                    setup_read += 0x30
                    setupJson.write(str(complete_setup))
        print(file_path + ": " + str(script_count))
        read_location += 2
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for x in range(script_count):
            tab_indentation = 0
            object_id = readData(data, 2, read_location)
            object_type = 0
            object_x = 0
            object_y = 0
            object_z = 0
            for y in complete_setup:
                if y["_id"] == object_id:
                    object_type = y["_type"]
                    object_x = y["_x"]
                    object_y = y["_y"]
                    object_z = y["_z"]
            object_name = "Unknown " + hex(object_type)
            if object_type < (len(object_modeltwo_types) - 1):
                object_name = object_modeltwo_types[object_type]
            object_name = make_safe_filename(object_name).replace("?", "")
            with open(file_path + "/" + object_name + "_" + str(hex(object_id)) + ".json", "w") as jsonFile:
                jsonFile.write("{\n")
                jsonFile.write('\t"_id": ' + hex(object_id) + ",\n")
                jsonFile.write('\t"_type": ' + hex(object_type) + ",\n")
                jsonFile.write('\t"coordinates": {\n')
                jsonFile.write('\t\t"x": ' + hex(object_x) + ",\n")
                jsonFile.write('\t\t"x": ' + hex(object_y) + ",\n")
                jsonFile.write('\t\t"x": ' + hex(object_z))
                jsonFile.write("\t}\n")
                jsonFile.write("\t}\n")

            with open(file_path + "/" + object_name + "_" + str(hex(object_id)) + ".code", "w") as scriptFile:
                block_count = readData(data, 2, read_location + 2)
                behav_9C = readData(data, 2, read_location + 4)
                read_location += 6
                for y in range(block_count):
                    tab_indentation = 0
                    conditional_count = readData(data, 2, read_location)
                    read_location += 2
                    x = {}
                    if conditional_count > 0:
                        for z in range(conditional_count):
                            func = readData(data, 2, read_location)
                            read_location += 2
                            p = []
                            for a in range(3):
                                p.append(readData(data, 2, read_location))
                                read_location += 2
                            grabConditional(0, func, p, 0, 0, scriptFile)
                    execution_count = readData(data, 2, read_location)
                    read_location += 2
                    if execution_count > 0:
                        for z in range(execution_count):
                            func = readData(data, 2, read_location)
                            read_location += 2
                            p = []
                            for a in range(3):
                                p.append(readData(data, 2, read_location))
                                read_location += 2
                            grabExecution(0, func, p, 0, 0, scriptFile)
                    for z in range(tab_indentation):
                        term_string = "}"
                        for a in range(tab_indentation - z - 1):
                            term_string = "\t" + term_string
                        scriptFile.write(term_string + "\n")
                    # blocks.append(x)


# Cheeky Stuff stolen from Iso
def getFileInfo(absolute_address: int):
    """Get file information."""
    if hex(absolute_address) in files:
        return files[hex(absolute_address)]


def getOriginalUncompressedSize(fh: BinaryIO, pointer_table_index: int, file_index: int):
    """Get original uncompressed size."""
    global pointer_tables

    ROMAddress = pointer_tables[26]["entries"][pointer_table_index]["absolute_address"] + file_index * 4

    # print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

    fh.seek(ROMAddress)
    return int.from_bytes(fh.read(4), "big")


def addFileToDatabase(absolute_address: int, data: bytes, uncompressed_size: int):
    """Add file to database."""
    global files
    global pointer_tables

    has_been_written_to_rom = False
    for x in pointer_tables:
        if x["absolute_address"] == absolute_address:
            has_been_written_to_rom = True
            # print("WARNING: POINTER TABLE " + str(x["index"]) + " BEING USED AS FILE!")
            break

    files[hex(absolute_address)] = {
        "new_absolute_address": absolute_address,
        "has_been_modified": False,
        "is_bigger_than_original": False,
        "has_been_written_to_rom": has_been_written_to_rom,
        "data": data,
        "uncompressed_size": uncompressed_size,
    }


def parsePointerTables(fh: BinaryIO):
    """Parse pointer tables."""
    global pointer_tables
    global main_pointer_table_offset
    global maps
    global num_tables

    # Read pointer table addresses
    fh.seek(main_pointer_table_offset)
    i = 0
    while i < num_tables:
        absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
        pointer_tables.append({"index": i, "absolute_address": absolute_address, "new_absolute_address": absolute_address, "num_entries": 0, "entries": []})
        i += 1

    # Read pointer table lengths
    fh.seek(main_pointer_table_offset + num_tables * 4)
    for x in pointer_tables:
        x["num_entries"] = int.from_bytes(fh.read(4), "big")

    # Read pointer table entries
    for x in pointer_tables:
        if x["num_entries"] > 0:
            i = 0
            while i < x["num_entries"]:
                # Compute address and size information about the pointer
                fh.seek(x["absolute_address"] + i * 4)
                raw_int = int.from_bytes(fh.read(4), "big")
                absolute_address = (raw_int & 0x7FFFFFFF) + main_pointer_table_offset
                next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
                x["entries"].append({"index": i, "absolute_address": absolute_address, "next_absolute_address": next_absolute_address, "bit_set": (raw_int & 0x80000000) > 0})
                i += 1

    # Read data and original uncompressed size
    for x in pointer_tables:
        if x["index"] == script_table_index - (version == 3) or x["index"] == setup_table_index - (version == 3):
            for y in x["entries"]:
                absolute_size = y["next_absolute_address"] - y["absolute_address"]

                if absolute_size > 0:
                    fh.seek(y["absolute_address"])
                    data = fh.read(absolute_size)
                    addFileToDatabase(y["absolute_address"], data, getOriginalUncompressedSize(fh, x["index"], y["index"]))


def make_safe_filename(s):
    """Generate safe filename."""

    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def extractMaps(src_file: str):
    """Extract Map Data."""
    global maps

    for mapIndex, mapName in enumerate(maps):
        mapPath = f"map_scripts{folder_append[version]}/" + str(mapIndex) + " - " + make_safe_filename(mapName)
        os.mkdir(mapPath)
        extractMap(src_file, mapIndex, mapPath)


def extractMap(src_file: str, mapIndex: int, mapPath: str):
    """Extract one map data."""
    global pointer_tables
    global files
    global num_tables
    global relevant_pointer_tables
    global folder_removal

    setup_tbl = setup_table_index - (version == 3)
    script_tbl = script_table_index - (version == 3)

    tbls = [setup_tbl, script_tbl]
    sizes = [0, 0]

    idx = 0
    with open(src_file, "rb") as fl:
        for tbl in tbls:
            fl.seek(main_pointer_table_offset + (num_tables * 4) + (4 * tbl))
            tbl_size = int.from_bytes(fl.read(4), "big")
            if tbl_size > mapIndex:
                fl.seek(main_pointer_table_offset + (4 * tbl))
                tbl_ptr = main_pointer_table_offset + int.from_bytes(fl.read(4), "big")
                fl.seek(tbl_ptr + (4 * mapIndex))
                entry_start = main_pointer_table_offset + (int.from_bytes(fl.read(4), "big") & 0x7FFFFFFF)
                entry_finish = main_pointer_table_offset + (int.from_bytes(fl.read(4), "big") & 0x7FFFFFFF)
                entry_size = entry_finish - entry_start
                sizes[idx] = entry_size
                if entry_size > 0:
                    fl.seek(entry_start)
                    compress = fl.read(entry_size)
                    with open("temp.bin", "wb") as fh:
                        fh.write(compress)
                    if int.from_bytes(compress[0:1], "big") == 0x1F and int.from_bytes(compress[1:2], "big") == 0x8B:
                        data = zlib.decompress(compress, 15 + 32)
                    else:
                        data = compress
                    if idx == 0:
                        # Setup
                        built_setup = mapPath + "/setup.bin"
                        with open(built_setup, "wb") as fh:
                            fh.write(data)
                    elif idx == 1:
                        # Scripts
                        built_script = mapPath + "/scripts.bin"
                        with open(built_script, "wb") as fh:
                            fh.write(data)
                        grabScripts(data, mapPath)
            idx += 1
    if sizes[0] + sizes[1] == 0:
        folder_removal.append(mapPath)


def bytereadToInt(read):
    """Convert bytes to an int."""
    total = 0
    for x in list(read):
        total = (total * 256) + x
    return total


def extractScripts():
    """Extract scripts from ROM."""
    global folder_removal
    global pointer_table_offsets
    global main_pointer_table_offset
    global folder_append
    global version

    append = folder_append[0]

    file_path = filedialog.askopenfilename()
    with open(file_path, "rb") as fh:
        endianness = int.from_bytes(fh.read(1), "big")
        if endianness != 0x80:
            print("File is little endian. Convert to big endian and re-run")
            exit()
        else:
            fh.seek(0x3D)
            release_or_kiosk = int.from_bytes(fh.read(1), "big")
            region = int.from_bytes(fh.read(1), "big")
            version = -1
            if release_or_kiosk == 0x50:
                version = 3  # Kiosk
            else:
                if region == 0x45:
                    version = 0  # US
                elif region == 0x4A:
                    version = 2  # JP
                elif region == 0x50:
                    version = 1  # PAL
                else:
                    print("Invalid version")
                    exit()
            main_pointer_table_offset = pointer_table_offsets[version]
            append = folder_append[version]
    if version < 0 or version > 3:
        print("Invalid version")
        exit()

    folder_removal = []
    dump_path = f"./map_scripts{append}"
    if os.path.exists(dump_path):
        shutil.rmtree(dump_path)
    os.mkdir(f"./map_scripts{append}")
    extractMaps(file_path)
    for x in folder_removal:
        if os.path.exists(x):
            for filename in os.listdir(x):
                file_path = os.path.join(x, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))
            os.rmdir(x)


extractScripts()
