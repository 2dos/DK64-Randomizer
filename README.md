# DK64 Randomizer
Python script that randomizes various options in the DK64 ROM. See the Wiki section on how to set up and use the script.

- Website: https://dk64randomizer.com/ (or https://dk64r.com for a shorthand redirect)
- Dev Branch: https://dev.dk64randomizer.com
- Discord: https://discord.dk64randomizer.com

Randomizer by 2dos and Ballaam | Web Interface by Killklli

## Current Features
- Randomizes the level order of DK64 (Hideout Helm always last)
  - The level lobby entrances and exits are randomized and tied together
  - Example: If Creepy Castle is level 1, then it only takes 1 GB to enter and 60 bananas to fight the boss under Vanilla rules
  - Validation to ensure the seed is able to be beaten glitchless
  - Unlock All Kongs must be turned on 
  - For logic purposes, in Galleon, the Peanut Popgun door that opens the sunken ship area is already opened
- Options to modify the length of the game (changes the B Locker and Troff n Scoff counts)
  - Fully customizable B Locker and Troff n Scoff requirements per level
  - Four presets for each: Vanilla, Steady, Half and Hell
- Option to unlock all kongs from the start
- Option to unlock all moves from the start
- Option to unlock the fairy camera and shockwave attack (fairy queen rewards) from the start
- Option to enable the Tag Anywhere hack
- Option for a fast Hideout Helm start
  - Start in Blast-o-matic room in front of Gorilla Grab lever
  - I-II-III-IV-V doors opened
  - The gates in front of the music pads are gone
- Option to open the Crown door in Helm
- Option to open the Nintendo and Rareware Coin door
  - Note that you cannot collect the DK Arcade GB with this option enabled, as the program simply adds the coins to your inventory
- Option to enable quality-of-life changes
  - Removes first time text
  - Removes most cutscenes (including GB dances)
  - Removes first time boss cutscenes
  - Remove DK Rap and extra cutscenes from startup
  - Story skip set to "On" by default (not locked to on)
- Option for Fast Start
  - Training Barrels complete
  - Start with Simian Slam
  - Spawn in DK Isles
  - Japes Lobby entrance open

## Contributing
Anyone is welcome to contribute. If you are wanting to make changes to be eventually implemeted into the master branch, please create a pull request from the dev branch. Any master branch changes are reflected on https://dk64randomizer.com/ while the dev branch changes are reflected on https://dev.dk64randomizer.com. Any merges into dev must be approved by either 2dos, Ballaam or Killklli. Only the dev branch can be merged into the master branch.
