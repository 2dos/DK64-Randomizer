# dk64-level-progression-randomizer
Experimental Python script that randomizes the level progression in the DK64 ROM.

Initial release goals:
- Randomizes the level order of DK64 (Hideout Helm always last)
  - The level lobby entrances and exits are randomized and tied together
  - Example: If Creepy Castle is level 1, then it only takes 1 GB to enter and 60 bananas to fight the boss under Vanilla rules
- Option to modify the length of the game (changes the B Locker and Troff n Scoff counts)
  - Vanilla game length is default
  - Shorter: B Locker GB requirements: 1-3-10-20-35-50-65-80, Troff n Scoff banana requirements: 50-75-100-125-150-200-250
- Option to unlock all kongs from the start
- Option to unlock all moves from the start
- Option to enable the Tag Anywhere hack
- Option to shorten hideout helm
  - Start in Blast-o-matic room
  - Open I-II-III-IV-V doors
  - The gates in front of the music pads are gone
  - Open Crown door
  - Open Rareware and Nintendo Coin door
- Option to enable quality of life changes
  - Removes first time text
  - Removes first time boss cutscenes
  - Shorter Snide blueprint turn-in cutscenes
  - Shorter K Lumsy key turn-in cutscenes
  - Remove DK Rap from startup
  - Story skip set to "On" by default (not locked to on)
  - Fast start: Training Barrels complete, start with Simian Slam, spawn in DK Isles
