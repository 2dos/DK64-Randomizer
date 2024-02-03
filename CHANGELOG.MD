
#  Version 3.0 Release Notes
This is the changelog for the initial push of 3.0 into Master:
- Below is a list of features that are being pushed to the Main site
- If you encounter any Bugs, please post your Spoiler log and [BPS](https://dev.dk64randomizer.com/bps_maker) with an explanation of the bug in the #3.0-Bug-Reports [Discord Channel](https://discord.dk64randomizer.com).

## CHANGELOG
### New Hints
- **Multipath**: A whole new rework to the hint system from 2.0 where a region check can hint multiple path items. Example below:
	- "Something in the Outer Isles is on the path to Keys 7 and 8 and K. Rool vs. Chunky and Diddy."
	- ONE item in the Outer Isles will be on the path to Key 7, Key 8, Chunky's K. Rool Phase, and Diddy's K. Rool Phase
	- That one item will ONLY be on the path to those Keys/Phases meaning that it will not lead to Key 4 or Tiny's K. Rool Phase
- **Direct Item Hinting**: Instead of your standard hints with paths and Way of the Hoard, this new hint system will directly tell you where your moves and keys are. This hint system will also tell you some other important hints such as Helm and Krool Phases. This hint system will prioritize which moves you need, but it can give you useless moves. It is up to you to figure out which moves you need. For Example: Looking for Simian Spring? Try looking in Forest with Chunky
- **Advanced Item Hinting**: Same functionality as above, but instead of telling you the specific move, it will instead hint the Item type. For Example: Looking for kong pad moves? Try looking in the Giant Mushroom Insides.
- **Spoiler Hints**: This is an independent hint system from the Wrinkly doors. Your spoiler log will contain a "Spoiler Hints" section that will reveal some information about the seed that may help you as you explore. This "Spoiler Hints" section will be in the spoiler log regardless of whether or not you checked the Generate Spoiler Log option. This makes these hints viable for racing, if you were wondering. One small quirk: training moves count as Isles! Spoiler Hints come in two forms. Vials, and Points
	- **Vials**: The levels of Keys, Kongs, and vials are hinted. Vials include their color.
	- **Points**: Inspired by other randomizers, each world is assigned a point value based on its contents. The value of each category of items provides can be customized on the website.
	- **Tracker**: This Hint system works with OnlySpaghettiCode's Track-o-Matic Tracker which can be found [here](https://github.com/Brian0255/Track-O-Matic/releases/latest)
- **Progressive Hints**: You can now unlock your hints with Golden Bananas instead of going through each lobby. You can select how many GBs it costs to unlock your last hint.
- **Dim Solved Hints**: This option will dim any hints that you have acquired the item to. (This won't be enabled in any Racing Preset)
- **New Hint Type Changes**: There are now a few changes made to the types of hints you can see:
	- **Region Potion Counts**: You can now get hints that tell you how many potions are in a region. These potions can very from very important to bait potions
	- B. Locker and Troff & Scoff hints are now removed from filler hints
	- You can no longer find more than 1 K. Rool/Helm Order Hint in a seed.

### **NEW** Major Features
- **Melon Crate Randomization**: With popular demand, Melon Crates are now added into the Item Pool! You can now find all your favorite items such as a suspiciously looking Gloden Banane in one of these boxes!
- **Melon Crate Shuffler**: In addition to above, you can now find Melon Crates in Wacky Places such as Underwater.
- **Hard Mode**: Spice up your DK64 Randomizer experience with new difficulty toggles, such as lower fall damage threshold and all water is lava!
- **Start without Simian Slam**: You can now start a DK64 Seed without a single Slam Move
- **Dropsanity**: Ever wanted to shoot a Zinger and it drop Key 4? Well now you can with Dropsanity! Most enemies that can respawn have been added to the item pool. You can tell if they have an item if they have a sparkling effect on them. This adds 289 checks into the game.
- **Switchsanity**: Various pads and switches across the game have been randomized, resulting in different requirements to reach certain areas. For example, the pad on top of the llama cage can be any instrument pad, not just guitar. You can also pick between having all switches enabled or just the Monkeyport/Gorilla Gone pads randomized. A full list of switches can be found [here](https://dev.dk64randomizer.com/wiki/SwitchsanitySwitches)
- **Random Settings**: Ever wanted to play a seed without knowing what settings you choose? Well, now you can with this new feature. There are 4 options to choose from:
	- [Easy](https://dev.dk64randomizer.com/wiki/RandomSettingsEasy.html)
	- [Standard](https://dev.dk64randomizer.com/wiki/RandomSettingsStandard.html)
	- [Difficult](https://dev.dk64randomizer.com/wiki/RandomSettingsDifficult.html)
	- [Difficult with Quality of Life Shuffle](https://dev.dk64randomizer.com/wiki/RandomSettingsDifficultWithQolShuffle.html)
- **Fungi Forest Day/Night Rando**: Tired of always starting Fungi Forest at Day time? Worry no more, because with this feature, you can now customize how you want to start Fungi Forest. Five new options have been added:
	- Day Time Start (Vanilla)
	- Night Time Start
	- Random Start
	- Dusk: All Time based gates are now open irregardless of whether its day or night
	- Progressive Time: Time will now advance progressively. Each cycle is around 5 minutes long and only progressives when you're in Forest Outdoors.
- **Galleon Tides**: You can now choose what Tide level you want to start Galleon with. You can pick from High, Low, or even Random.
- **Pincode Number Rando**: The Door Combinations for Diddy's R&D Room will now be randomized with Puzzle Rando Enabled.
- **Music Overhaul**: Cosmetic Packs now accept a new type of file `.candy`. This file contains the song binaries and a bunch of other data for filtering. This means the songs you pick will only show up in appropriate places. Additionally, you can now pick a percentage of Vanilla Music that can appear in your seeds.
- **Rambi and Enguarde Bonus Barrels**: The Rambi and Enguarde Arena has been added to the minigame pool. Rambi Arena requires 100 points, Enguarde Arena requires 125. Enguarde Arena logically requires diving to complete
- **Training Barrels**: The Four Training Barrels you see at the start of a Vanilla Game are now added to the Bonus Barrels Pool. Try not to get 2%ed with Oranges 😉
 
 ## Minor Features
 - **Custom Location Update**: Arenas, Dirt Patches, and Melon Crates now share the same list of possible location (With a few exceptions). A full list of all available locations can be found [here](https://dev.dk64randomizer.com/wiki/Custom-Location-Lists.html)
 - **Starting Move Selector**: You can now pick what moves you want to start with.
 - **Starting Kong Selector**: You can now also pick what Kong you what to start your seed with.
 - **Quick Fungi Transition**: Fungi Forest's Time of Day transitions have been heavily reduced
 - **Global Instrument**: All Kongs now share the same amount of Instrument Energy rather than it being separate based on the Kong
 - **Fast Pause Transition**: Pause Transition no longer take 5-10 Business days to Transition between Screens. This has been sped up by a factor of 10
 - **Item Acquisition**: You can now see where you have obtained items in the Pause Menu.
- **Delayed Spoiler Log Release**: You can now choose to release your spoiler log after a certain period of time if you wanna race or just not look at the log until after you finish the seed.
- **Hint Region Pause Screen**: No longer will you be confused on what hint region you are in. When you pause the game, you can see what Hint Region you are in. Example: [Region Hint](https://discord.com/channels/463917049782075395/559837132428935170/1203096476239134770)
- **Junk Bosses Begone**:  Every boss is now guaranteed to have an item on it.
- **Mystery Menu is back**: The Cheats toggle from the mystery menu is now always available.
- **No Hard Minigames**: A new toggle has been added to remove Hard Variations of minigames in the Minigame Pool.
- **New Multiselectors**: Remove Barriers and Faster Checks now have Multiselectors so you can pick and choose what Barriers/Checks you want turned on.
- **Random Helm Door Improvements**: Random Helm Door requirements have been split into 3 separate random options:
	- [Easy]( https://dev.dk64randomizer.com/wiki/Random-Helm-Door-Changes.html#easy)
	- [Medium](https://dev.dk64randomizer.com/wiki/Random-Helm-Door-Changes.html#medium)
	- [Hard](https://dev.dk64randomizer.com/wiki/Random-Helm-Door-Changes.html#hard)

### Cosmetics
- **Music Selection**: Users can now choose which songs they want to appear in specific locations, using the UI in the new Music tab.
- **Music Exclusion**: A new setting to make certain music not play
	- Transformation Songs such as Mini Monkey or Hunky Chunky
	- **Sub Areas**: Going through sub areas will not change the song being played, It will, however, be played if you go through a Loading Zone and enter back
	- Pause Menu
	- Wrinkly Doors
- **Crosshairs**: Crosshair for guns/cannon barrels (etc) now has a black outline to aid visibility. Additionally, the color of the crosshair is now impacted by colorblind mode. 
- **Random Menu Background**: The Background on the Main Menu now has Random Textures applied to it Example: [Region Hint](https://discord.com/channels/463917049782075395/559837132428935170/1203096476239134770)
- **Krusha now Exists**: Krusha's moves will have a Krusha twist to them, and the kong name will in most cases be replaced with Krusha's name
- **New Cosmetic Options**: All random model-related settings have been merged into one "Random Model Swaps". It has 3 options to choose from:
	- **Off**
	- **Random**
		- 50% chance that the tomato in Caves looks like the regular one
		- 50% chance that the tomato in Fungi looks like the ice one
		- Peril Path Panic fairy/Teetering Turtles Turtle model rando. The model chosen for the Peril Path Panic fairies will also be reflected with the fairies that you see in the End Sequence.
		- Random Klaptrap colors in Beaver Bother, Searchlight Seek and Peril Path Panic
	- **Extreme**:
		- All things from "Random", plus all that is below
		- 50% chance the Aztec/Caves races are against the rabbit
		- 50% chance that the Fungi race is against the beetle (will also change the NPC in Chunky 5DI)
		- Random model for the Klaptrap in Beaver Bother
- **T&S Visual Indicator**: Added a Visual Indicator for when you have enough Colored Bananas to fight the Boss
- **Additional Color Options**: Added the ability to customize the Color of DK's Tie, Tiny's Hair, and Lanky's Fur.
- **Cosmetic Restoration**: Thanks to JXJacob, The Patch on Lanky's overalls and the "DK" on Donkey's Tie are now restored and work with custom colors.
- **Cannon Game Speed**: Holding A while in the Galleon Cannon will slow down the rotation speed, making it easier to control.
- **Vanilla K. Rool Requirements**: You can now only require Key 3, and Key 8 to spawn K. Rools Ship.
- **Press Start to Skip Cutscene**: There is now an option to press start to skip the cutscene if you wish to see the cutscene.

### Bug Fixes/Improvements
- **Bonus Barrel Fixes**: Bonus Barrels are now truly Random and the chance of a Barrel being rolled twice are no longer higher than inteded.
- **Starting Key Slider**: The Starting Key Slider has been updated to be more intuitive at a glance.
- **Japes Alcove Logic**: The Troff & Scoff portal alcove now requires Vines to reach if you don't have Advanced Platforming turned on
- **Chunky Phase Slam Hint**: Fixed a bug where Chunky Phase Slam hint wouldnt work 50% of the time.
- **Helm Hurry fix**: Fixed a bug where the bean would give the Helm Hurry bonus of Pearls.
- **Fake GB Restriction**: Added Aztec Diddy Gongs and Lanky Vulture to list of banned Ice Trap Locations.
- **Mushroom Interior CB Fix**: The Coordinates of the Colored Bananas on the ladders are now fixed so you do not need to jump off to grab them with Diddy or Tiny.
- **Helm Hurry Timer Increase**: Helm Hurry start time can now go as high as 65,535 seconds.
- **Japes Mountain Cutscene**: The "No Chimpy Charge" Cutscene has now been removed if you have Remove Cutscenes turned on.
- **Helm Fairies Ban**: The 2 fairies behind the second Helm door are now banned to have anything that is required for the Helm doors to unlock if you have Fairies in the Item Pool.
- **Stash Patch**: The Stash Snatch/Stealthy Snoop hybrid Minigame will only appear in seeds where both Stash Snatch and Stealthy Snoop are enabled.
- **Bounce Fix**: For the longest time, Ice Traps and Kong Items would have excessively high gravity applied to their bounce to fix a bug with their bounce function. This bug has now been fixed and those items will no longer bounce weirdly.
- **"Jacob Rolling Patch"**: [Jacob Rolling](https://clips.twitch.tv/VibrantBoredLasagnaKAPOW-HEe8AmUtB9dTtUsg) has been patched by resetting the speed back to walking speed if the player was previously moving than that.

## Other notes
- **New Presets**: Some new Presets have been added:
	- **Beginner Preset**: A new preset tailors to beginners of DK64 Randomizer. For logic tips and tricks, [Click Here](https://dev.dk64randomizer.com/wiki/Logic-Tips-and-Tricks.html)
	- **Hitlist**: A Kingdom Hearts II Style preset focused on completing the worst checks in the game. This preset uses OnlySpaghettiCode's Tracker: [Track-o-Matic](https://github.com/Brian0255/Track-O-Matic/releases/latest)
	- **KEVIN**: A preset created by KeiperDontCare. This preset has an All Keys Wincon with Key 8 **NOT** Locked in Helm. Also uses the same Tracker mentioned above.
	- **Treasure Hurry**: A preset created by Kamerson. This preset has Helm Hurry enabled where collecting items lowers the time. The goal is to either get the timer to zero, or to beat K. Rool.
- **Modified Presets**: Some presets have also been modified from the Master Branch:
	- **NSAK**: Full list of changes are mentioned [Here](https://dev.dk64randomizer.com/wiki/NSAK-Racing-Rules.html)
	- **Balanced LZR**: Added Fungi Dusk, Removed Custom Colored Bananas, and Added Progressive Hints.

## Changes that didnt get updated
- **Plandomizer**: This is not getting pushed to the Main Branch and is still staying on Dev Site until it's ready
- **Widescreen Hack**: This is also staying in dev as it is still being fixed. 