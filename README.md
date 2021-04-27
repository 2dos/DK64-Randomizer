# DK64 Randomizer
Python script that randomizes various options in the DK64 ROM. See the Wiki section on how to set up and use the script.

## Current Features
- Randomizes the level order of DK64 (Hideout Helm always last)
  - The level lobby entrances and exits are randomized and tied together
  - Example: If Creepy Castle is level 1, then it only takes 1 GB to enter and 60 bananas to fight the boss under Vanilla rules
  - Validation to ensure the seed is able to be beaten glitchless
  - Unlock All Kongs must be turned on 
  - For logic purposes, in Galleon, the Peanut Popgun door that opens the sunken ship area is already opened
- Options to modify the length of the game (changes the B Locker and Troff n Scoff counts)
  - Fully customizable B Locker and Troff n Scoff requirements per level
  - Four presets: Vanilla, Steady, Half and Hell
- Option to unlock all kongs from the start
- Option to unlock all moves from the start
- Option to unlock the fairy camera and shockwave attack (fairy queen rewards) from the start
- Option to enable the Tag Anywhere hack
- Option to shorten hideout helm
  - Start in Blast-o-matic room in front of Gorilla Grab lever
  - I-II-III-IV-V doors opened
  - The gates in front of the music pads are gone
  - Open Crown door
  - Open Rareware and Nintendo Coin door (the coins are already given to you)
- Option to enable quality of life changes
  - Removes first time text
  - Removes first time boss cutscenes
  - Remove DK Rap from startup
  - Story skip set to "On" by default (not locked to on)
  - Fast start: Training Barrels complete, start with Simian Slam, spawn in DK Isles
