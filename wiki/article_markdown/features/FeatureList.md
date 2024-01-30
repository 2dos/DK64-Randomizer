# V3.0
*(In Progress)*

# V2.0
## Item Randomizer
- **Added Items / Locations**:
	-	Moves / Shops
	-	Golden Bananas (Including separation between tougher challenges and easier challenges to enable the user to avoid tougher, longer challenges like Caves Beetle Race)
	-	Battle Crowns / Crown Pads
	-	Blueprints / Kasplats
	-	Keys / Bosses
	-	Banana Medals / Medal Reward
	-	Company Coins / 8bit Minigame Rewards
	-	Kongs
	-	Fairies
	-	Rainbow Coins / Dirt Patches
	-	Bean / 2nd Anthill Reward
	-	Pearls / Galleon Pearl Chest
	-	Ice Traps (Slightly green Golden Bananas which rotate the opposite way. Picking them up will put you in a trap bubble and deal 1 damage).
	-	Junk Items (Melons which refills a melon slice-worth of health)
- **Related Changes**:
	- Bonus Barrel skin will now show the reward inside
	- The reward for defeating a boss will show above the boss door when you open it up
	- The reward for completing a crown will show in the background
	- The baboon blast courses in Fungi Forest and Crystal Caves will show a brief cutscene upon entrance which shows the bonus barrel, enabling the user to determine whether the course is worth completing.
	- Various lengthy tasks will now hint the item that you will obtain for beating the task
	- A cutscene will play upon talking to the Banana Fairy Queen (after obtaining the first reward) which will show what is behind the door that is opened by obtaining a certain amount of fairies

## More Randomizers
- **Location Randomizers**:
	- Wrinkly Doors
	- Troff 'n' Scoff Portals
	- Battle Crowns
	- Fairies
	- Colored Bananas
	- Coins
- **More Moves Added**: Training Moves (Diving, Vine Swinging, Oranges and Barrel Throwing), Camera and Shockwave have been added to Move Randomizer.'
- **Cross-Map Warps**: Additional modes for `Bananaport Randomizer`. Warps can now be paired with warps in other levels.
- **Arcade Level Order Rando**: The four stages in DK Arcade are now in a random order.
- **Random Starting Location**: You can now start almost anywhere in the game.

## Server and UI Updates
- **Server**: Huge revamp means that seeds will generate significantly faster than 1.5.
- **Patches**: Now works across version, meaning that patches generated on 2.0 will work on future versions.
- **Settings String Revamp**: Settings Strings have been overhauled to be more condensed and more adaptable to site updates.
- **Minor UI Updates**: Replaced randomization toggles with a dice icon.
- **More Selectors**:
	- Starting Keys: You can now select the exact keys you want to start with in your seed
	- Quality of Life (Misc Changes): You can now select which quality of life options you want to enable or disable that is part of the `Misc Changes` setting.
	- Enemy Rando: You can now select which enemies you want to add into the pool for enemy and crown randomizer.
	- Starting move count: The user can now pick how many moves they want to be given at the start of the seed. This can range from 0 to 40. As a result, the "unlock all moves" setting as this can be replicated by setting the starting move count to 40.
	- Colored Bananas: The user can now set the amount of colored bananas required to obtain the medal reward
	- Fairy Requirement: The user can now set the amount of fairies required to open the door inside Banana Fairy Island
	- Bananaport Randomization: The user can now select which levels will have the bananaport randomization setting applied
- **Advanced ROM Header**: Enables DK64 Randomizer to work and save on more emulators and platforms than before.
- **Greater Music Capabilities**: Custom Music can now be as large as 32kb instead of 16,512 bytes
- **Presets**: Presets have been altered to accommodate all of the new changes. This includes removing Season 1 settings, and replacing it with Season 2 settings.

## New Settings
- **Glitch Logic**: For glitch enthusiasts, you can now generate seeds which expect you to do particular glitches in certain locations to access locations and/or items earlier than you would be able to with glitchless scenarios. Additionally, you can select which glitches you would like to be in logic.
- **Helm Hurry Mode**: DK64, but we added a timer. You can customize the bonuses that are provided for obtaining certain items as well as the starting time. Try to beat as much of the game as you can.
- **File Screen Tracker**: The file progress screen will now display a whole host of information about the file, including the moves that you have.
- **Progressive Slam Switches**: Slam switches  can be tied to level order, so that red slam switches will always be in level 7 regardless of what level is occupied in that slot.
- **Extra Hints**:
	- Extra Hints have been added to hint the locations of very important items in the very late stages of the seed
	- The following extra hints have been added under the scenario of the player not having the move:
		- **Monkeyport**: Accessible by touching the lower monkeyport pad in DK Isles upon obtaining enough Golden Bananas to enter all of the first 7 levels.
		- **Gorilla Gone**: Accessible by touching the pad in Helm Lobby upon obtaining enough Golden Bananas to enter all levels.
		- **Simian Slam Upgrades**: Accessible by entering Chunky Phase without any slam upgrades.
		- **All Instruments**: Accessible by touching the pads in Hideout Helm, as long as the pad is spawned. These hints are only applied if the extra hint setting is set to "all"
- **Complex Level Progression**: A level order randomizer mode which disables a lot of measures that simple level order randomization uses to generate fair seeds.
- **Changes to existing settings**:
	- Faster Checks:
		- Mill Lever Puzzle is shortened from 5 levers to 3 levers
		- Jetpac will require only 2500 points to obtain the reward instead of 5000
	- Random Puzzle Solutions:
		- Mill Lever Puzzle will be randomized
		- Crypt Lever Puzzle will be randomized
- **Helm Doors**: The required item and amount of that item to open the two doors before getting Key 8 (or whatever item is placed there) can be changed or randomized, depending on the user's preferences.
- **Win Condition**: The user can change the trigger that will pull up the game's credits from the following list:
	- Beat K. Rool
	- Acquire Key 8
	- Obtain All Keys
	- Obtain All Fairies
	- Obtain All Blueprints
	- Obtain All Medals
	- Kremling Kapture: Take a photo of all enemies in the game. A checklist can be found [here](https://docs.google.com/spreadsheets/d/1nTZYi36dFaTB1XCgB7dJJffMsaKz-wOFmP5nDo8l3Uo/edit#gid=0).

## Difficulty
- **Tiny Phase**: Toe sequence is now randomized with hard bosses.
- **Smaller Shops**: Shops will have, at most, 3 items in them. This makes shops a little less overpowered in settings such as Item Rando
- **Hard Enemies**:
	- Kasplats will now have a 6% chance of shockwaving
	- Guards will have triple health
	- Spider Projectiles unfortunately needed to be removed because of the strange and bizarre crashes that they would end up causing, including corruption of the game's memory management systems.

## Cosmetics
- **Disco Chunky**: Optional cosmetic modifier for Chunky Kong
- **Krusha**: Now playable in Adventure mode by replacing a random kong or a kong of your choice. Pressing Z+B will allow Krusha to skate. In order to perform moves that normally require Z+B (Chimpy Charge, Orangstand, Primate Punch), you'll have to be below a certain speed. Krusha will fire out explosive limes instead of the replacement kong's ammo type.
- **Various cosmetic options randomized**: Klaptraps in Minigames, skybox colors and many more minor things have some cosmetic modifier applied.

### Pause Menu Overhaul
- **Level In-Game Time**: The game now stores and displays the in-game time played in a level.
- **Checks**: Added a screen which displays the checks that have been completed in game. For example, if you kill a kasplat which drops a key, acquiring the key will complete a kasplat check.
- **Hints**: Hints that have been read will now be added to the pause menu, which can be quickly re-read through the pause menu.
- **Moves Tracker**: The tracker from the file screen has been ported to the pause menu.

## Quality of life changes
### Optional Changes
- **Remove Cutscenes**: Removed over 250 cutscenes from gameplay, greatly speeding up the flow of the game for experienced players.
- **Vanilla Fixes Additions**:
	- The second race with the Fungi Forest Rabbit will now provide infinite crystals.
	- The Hideout Helm timer will now correctly pause when selecting an option in the pause menu that isn't "unpause"
	- A softlock will no longer occur upon entering a battle crown with Strong Kong
	- "Squawks with a spotlight" will behave slightly better
	- Fixes a bug where Tiny throwing a TNT Barrel from a pad would occasionally result in the TNT Pad moving along with the barrel.
- **Reduced Lag Additions**:
	- Anti-aliasing is disabled, improving the game's fps by as much as 4fps.
	- More weather effects have been removed.
- **Homing Balloons**: Homing Ammo will now home in on Balloons
- **Raise Fungi Dirt Patch**: The dirt patch hidden under some grass in Fungi Forest that was famously hidden until 2017 has been slightly raised to make it more obvious that it is there.
- **Kongless Hint Doors**: Kongless hint doors will remove the kong unlock requirement in order to read a hint
- **Fast Hints**: Wrinkly will now appear faster to enable quicker reading of hints.
- **Save K. Rool Progress**: K. Rool will now save the progress that is made during the fight. In other words, if you die in Tiny Phase (where Tiny Phase is the 2nd phase of the fight), re-entering the fight will put you back in Tiny Phase instead of the 1st phase.
- **Small Bananas always visible**: Makes colored bananas and banana coins always visible regardless of whether you have the kong unlocked
- **Brighten Mad Maze Maul Enemies**: Forces the enemies inside Mad Maze Maul to be full brightness regardless of their positional lighting conditions, making them easier to spot.
- **Remove Wrinkly Puzzles**: Makes all doors accessible in Fungi Lobby without spinning the wheel, removes the crystals in Caves Lobby, and places Chunky's wrinkly door behind feather door in Aztec Lobby.
### Non-Optional Changes
- The Tag Barrel near the mermaid palace has been shifted.
- The Lanky and Chunky balloons in Galleon have been shifted to fix some bugged loading.
- Guards will no longer spot players who are in a gorilla gone/strong kong/orangstand sprint state
- The bean is now permanently saved to your file upon collection
- Vines will now render as red and translucent if you have not obtained vine swinging
- More lives are given at the start of DK Arcade, meaning that you won't get a game over as often.
- The fairy that is behind the bars in the 5-Door Ship in Galleon has been relocated to not be behind the bars. Not only does this make this fairy easier to obtain, but it also makes it possible on some PC/Emulator configurations.
- Hints will now have text that is highlighted in various colors allowing the player to parse the hint quicker
- The lever puzzle in the Creepy Castle crypt will now have the numbers on the signs denoting the order which you are intended to pull the levers.
- Shop indicator will now display both the kong and the item that will be obtained from that kong

## Accessibility Changes
- **Remove Water Oscillation**: Removes water oscillation and the oscillation in the Seasickness ship and the Mech fish to reduce potential motion sickness
		- Additionally, the underwater items in Caves have been raised in accordance with this setting.
- **Inverted Camera Controls**: Option has been added to the options menu in-game to invert the direction the camera moves when moving the analog stick up or down.
- **Dark Mode Textboxes**: Textboxes can be optionally changed to dark mode for all dark mode enthusiasts
- **Kong Heads on Balloons**: Kong heads will be placed on balloons, making it easier to distinguish the kong assigned to a balloon in troubling lighting conditions.
- **Colorblind Mode**: Item colors and various other color-based elements will be altered to make them more distinguishable to users with various types of colorblindness. The user can input their type of colorblindness, which will affect what the altered colors are.

## Miscellaneous Changes	
- Autocomplete bonus barrels: Behavior has been modified so that it will only autocomplete once the barrel is visible.
- The boot messages which are shown during fast boot are randomized.
- Chunky Phase is not always the last phase in K. Rool. Likewise, DK Room is not always the first room in Helm.
- Kop Changes:
	- They will now drop crystals.
	- Kops will be momentarily distracted whenever they are playing with their walkie talkie. When distracted, the kop will have reduced visibility.
- The block elevators in Block Tower room in Factory now go up and down faster, and more randomly
- In Irondonk, the monkeyport pad to get to Helm Lobby is useable by every kong. Additionally, the Helm B. Locker will respond to all kongs.
- Cranky will now refill crystal coconuts, if you have a crystal coconut move.
- Item Collision has been overhauled to be significantly better with varied item sizes (notably the Golden Bananas in Galleon 2-Door Ship and the one hidden by the large rock in DK Isles) and items placed in specific locations which expose flaws with the vanilla game's collision system.
- Oranges will now be translucent if you do not have the orange throwing ability
- Tag Anywhere now buffers the input. In other words, if you pause, and hold either D-Pad left or right, upon unpausing, you will change kong instantly
- Shockwave & Camera can now be decoupled to be separate moves.
- The default value for the settings that can be set on the in-game main menu can be set on the randomizer website.
- Logo has been updated.

## Bug Fixes and other dev-related minutiae
- Fixed GetOut enemies in battle crowns occasionally crashing the game
- Many other crashes and bugs fixed.
- The stack trace screen (only visible when the game has crashed from an invalid operation) has been overhauled to yield more information. Hopefully you never see this change, but it helps us (the developers) debug and fix sources of crashes faster. Unfortunately, Wii U still doesn't render this.

# V1.5
## Fresh Website
- **New Presets**: Season 1 Level Order Race Settings (aka Spike's settings) preset has been added, as well as a preset with just the quality of life changes offered by the randomizer.
- **New Website UI**: Revamped UI scales better on various screen sizes. The spoiler log has also had a revamp to be easier to interpret for everyone.
- **Getting Started**: New Getting Started tab dedicated to applying presets and providing resources.
- **Setting Strings**: Settings Strings for exporting and importing settings.
- **Caching**: Your ROM will be cached by the website after uploading it. No more choosing your ROM file every time you enter the site. Additionally, the past 10 seeds generated will also be cached.
- **Cosmetics**: You can now select your own cosmetics after applying a patch file.
- **Code Alert**: If the randomizer code has been updated since you loaded the site, the website will produce an alert to let you know of this.
- **Performance Updates**: Generally improved performance, load times, and responsiveness.

## New Randomizers
- **Dirt Patch Location Shuffling**: This shuffles dirt patch locations across the seed while keeping the distribution between levels consistent.
- **Shop Location Shuffling**: Candy's shop in Factory might be at Snide's instead. Shops are only shuffled within levels so you don't get multiple of one shop.
- **Cross Kong Purchases**: Any Kong can buy any other Kong's moves. For example, you might have Chunky purchasing Rocketbarrel.
- **Kasplat Location Shuffling**: Kasplats locations are picked from a large set of hand-picked location. Each Kong still has one per level, but where was the Kasplat?
- **No Logic**: For those feeling brave. I hope you know what you're doing.
- **Shuffled Helm**: The order and number of rooms required for Helm can be randomized.
- **Crown Randomizer**: Crown enemies have been decoupled from the enemy randomizer and have multiple difficulties to pick from.
- **Randomize Pickups**: Pickups (ammo, crystal coconuts, oranges, etc.) are randomized. There is a weighting to it so not everything ends up as film.

## New Options
- **Activate Bananaports**: Either the Isles warps or all warps are activated from the start of the seed. The logic does take this into account.
- **Shuffle Puzzle Solutions**: Various puzzles throughout the game have been randomized. See [the wiki](https://github.com/2dos/DK64-Randomizer/wiki/Feature-Explanations#puzzle-solution-randomizer) for a full list.
- **Extreme Prices**: Prices so high you must start with shockwave!
- **Open Levels**: Some levels with annoying gates can have those gates pre-opened. The logic does take this into account.
- **Remove High Requirements**: Some areas that have prohibitively high and/or specific requirements to enter have skipped a step or two in the process of entry. For example the switches to enter Aztec's 5-Door Temple start spawned.
- **Fast GBs**: Particularly slow GBs have been sped up significantly. This includes things like making races 1 lap or doing more damage to the Mechanical Fish. A full list can be found on [the wiki](https://github.com/2dos/DK64-Randomizer/wiki/Feature-Explanations#fast-golden-bananas).
- **Randomize Medal Requirement**: Instead of having a set medal count, you can randomize the amount of medals needed to play Jetpac.
- **Bonus Barrel Customization**: You can now pick and choose the minigames that will appear in a seed.
- **Key 8 Door Requirements**: You can now require the door to Key 8 require one, both, or none of the coins typically required in vanilla.
- **Maximize Helm B. Locker**: Force the Helm B. Locker to be the maximum amount specified while still being able to randomize the rest.
- **Hard Bosses**: Some bosses will get a little bit harder or require you to fight them with unusual Kongs.
- **Shorter Bosses**: Ever feel like the boss fights are annoyingly long? With this option, you can shorten the boss fights to be roughly a minute shorter. Changes to the boss fights with this setting can be found on [the wiki](https://github.com/2dos/DK64-Randomizer/wiki/Feature-Explanations#shorter-bosses).

## Quality of Life Upgrades
- **Troff 'n' Scoff Indicator**: An audio indicator is added for when you reach the required colored banana count for Troff N' Scoff in a level
- **Auto Key Turn Ins**: Keys are automatically turned in without having to return to K. Lumsy, opening lobbies instantly.
- **Fast Warps**: The bananaport animation is sped up significantly.
- **D-Pad Display**: Icons will appear on your HUD showing who you can tag to, what ammo you currently have toggled, or functionality to show your current blueprint & total colored banana count.
- **Tag Anywhere Improvements**: Tag Anywhere has been optimized to speed up the delay between tags after item collection.
- **Misc Changes update**: The weather in various levels has been removed to reduce lag and improve stability. Extreme lag when taking a photo on some emulators has been removed as well. A full list of what "Misc Changes" does can be found on [the wiki](https://github.com/2dos/DK64-Randomizer/wiki/Feature-Explanations#misc-changes).
- **Strong Kong in Ice Maze**: This difficult banana is easier should you have Strong Kong. A strong kong barrel has been placed next to the entrance.
- **Emulator Warning**: If you have an incorrectly set-up emulator, a warning will appear on the main menu informing you of this, suggesting you look up [the wiki guide](https://github.com/2dos/DK64-Randomizer/wiki/Consoles-and-Emulators).

## Improved Cosmetics
- **Kong Coloring**: Kongs, Rambi and Enguarde can now be any RGB color, whether random or user-selected.
- **Beaver Bother Klaptrap**: The Klaptrap model you play as in Beaver Bother can be swapped with some other interesting models

## Other Changes
- **Boot Sequence**: Boot sequence has been shortened by about 60% with a nostalgic callback to your favorite 1990s operating system whilst you wait.
- **Improved Hints**: The hints system has undergone a major rework and should now be significantly more useful. This includes a hint inside Hideout Helm which provides the kongs used to fight King K. Rool.
- **Guards!**: K. Rool has sent out his police force. Watch out for Kops when enemies are randomized.
- **Beaver Bother**: Golden beavers have been added to Beaver Bother. They move faster but are worth 2 points.
- **Minigame Changes**: Enemy Rando has been extended to work with some minigames. Additionally, oranges are now enabled in minigames, allowing you to beat *that* Mad Maze Maul without shockwave.
- **Bonus Barrels**: Two Bonus Barrels have been slightly moved to improve the consistency of entry: Tiny's in Aztec Lobby and Diddy's in Factory Storage Room
- **Kong Buffs**: Barrel throw speeds have been improved for Kongs previously terrible at it, and DK's boat speed in Pufftoss has been buffed. This now allows some Kongs to fight bosses they could not before.
- **Fast Transform**: The transformation animation upon entering a barrel has been sped up significantly.
- **Extra Enemy Rando Changes**: Purple and Red Klaptraps will now be shuffled in with the harder enemies. Koshas have been removed from the pool for the Enemy Gauntlet Cabin in Caves. Enemy Speed Rando, Crown Rando and General Enemy Rando have been split into separate options.
- **Item Pickup as Transformations**: Rambi and Enguarde will now be able to pick up DK and Lanky's items respectively.
- **Isles Cranky**: This shop tucked away inside DK Isles can now sell you moves.
- **Caves Troff 'n' Scoff**: An extra Troff 'n' Scoff has been placed inside Crystal Caves which doesn't require any moves to access. This vastly improves seed generation success rates for Level Order Randomizer.
- **In-Game Time**: The ingame timer that is displayed on the file progress screen has been restored to vanilla behavior.
- **Ammo Swap Remap**: The ammo type swap funcitonality has been changed from "Hold L" to "Press D-Down to toggle".

## Bug Fixes
- **Vanilla Bug Fixes**:
	- Vine sequences have been recalculated to prevent situations where a kong misses a vine.
	- Tag Barrels now properly update all background variables
	- Rocketbarrel slow-turn glitch has been fixed
	- Falling off Mad Jack in a particular way will no longer make you fall off the elevator ride up.
	- The banana bunch inside the rock in Japes and the coins spawned by beating the first rabbit race in Fungi will always spawn as a Chunky bunch and Lanky coins respectively.
	- The phase reset plane in Mad Jack has been lowered.
	- The ice maze in Crystal Caves now responds to all kongs. No more cheating!
	- Guards no longer produce solar flare effects from their torches.
	- Diddy & Chunky's medals in Helm now are mapped correctly to their respective flags.
	- DK will no longer show up in the statistics portion of the pause menu if he isn't freed.
	- Fixed [Fake Production Room](https://clips.twitch.tv/SuperPlayfulMomRaccAttack-XIGy4D-zhChQe0EN)
	- The door to Frantic Factory Lobby has been solidified.
- **Text**: Textboxes will now auto-close (vanilla behavior) if the textbox has been produced outside of a lobby or shop. This fixes some bugs and crashes.
- **Music Rando**: Some songs in v1.0 when placed in certain slots would incorrectly loop or not loop. This has been fixed in 1.5.
- **Move Use Text**: The textbox that shows up after purchasing a move that instructs you on how to use the move now informs you about the correct move.

# V1.0

## Loading Zone Randomizer
- Two extra types
	- **Coupled (Formerly known as DKoupled)**: Going back through the loading zone where you entered brings you to the place you came from. Example: Entering the portal in Japes Lobby brings you to DK’s Ice Maze room. Exiting the Ice Maze Room brings you to Japes Lobby (from the DK Portal).
	- **Decoupled (Formerly known as DKhaos)**: No loading zone linking occurs

## Kong Randomizer
- **Shuffle Kongs**: Your starting kong may be different and all the other 4 kongs will be randomly placed amongst the 4 vanilla cage locations. Additionally, a random kong will be required to free them (for instance, Tiny could free Lanky in Japes)
- **Starting Kong Amount**: If you want a little bit of a head-start, you can change the amount of kongs you are initially provided, from 1 to 5.

## Move & Shop Price Randomizer

- **Move Randomizer**: Shuffle moves within the 19 available shops. Moves aren’t restricted to only being purchasable from the intended shop (eg. An instrument may be sold by Cranky).
- **Price Randomizer**: Randomize the prices of moves within a few presets:
	- **Vanilla**: All moves will be their vanilla price
	- **Free**: All moves will cost 0 coins
	- **Low**: Moves will mostly cost fewer than 5 coins
	- **Medium**: Moves will be a little more expensive
	- **High**: Moves will be pretty expensive. Coin hunting will be required

## Bonus Barrel Randomizer

- Bonus Barrels will have random minigames placed inside them, including the Snide’s Minigames and some unused ones. There are currently two modes:
	- **Regular**: All minigames will be considered. Some minigames will be banned in Helm due to difficulty
	- **Oops All Beaver Bother**: As the name suggests, every minigame will be beaver bother

## Boss Randomizer
- **Boss Kong Randomizer**: Hate always fighting Army Dillo as DK? With Boss Kong Randomizer, the game may want you to fight Army Dillo as Lanky. This also changes the order of kongs in the King Kut Out boss fight.
- **Boss Location Randomizer**: Bosses will be in different levels to where they normally are in vanilla. For example: Mad Jack (normally the boss of Factory) could be the boss of Crystal Caves

## Bananaport Randomizer
- Shuffles bananaports around their vanilla locations. This may yield useful results (such as a bananaport pair that takes you between the start of Aztec and the back of Aztec) or very useless results (such as a bananaport pair that takes you between two warps at the start of Isles).

## K. Rool Phases
- **Shuffle**: K. Rool Phases will be swapped around. For example, the order could go: Diddy, Tiny, Lanky, DK, Chunky. Chunky will always be the final phase
- **Length modifier**: Change the amount of phases you will need to complete to beat K. Rool

## Enemy Randomizer
- **Enemies types**: All of the enemies in the game can now be almost anywhere.
- **Enemy speed**: Each enemy spawner will now have a random speed assigned to it. You could get a very slow enemy, or you could get a very speedy enemy.

## Kasplat Randomizer
- Kasplats will be shuffled in amongst their vanilla locations. For example, in Helm Lobby, you could get a Chunky Kasplat (In the vanilla game, it’s a DK Kasplat)

## B. Locker and Troff ‘n’ Scoff requirement randomizer
- In the demo, you had to set the requirements for all 8 B. Lockers and all 7 Troff ‘n’ Scoffs. In V1, you will be able to randomize it and set a maximum value that the randomization is capped to.

## Difficulty Modifiers:
- **Damage Multiplier**: Choose between normal damage, double damage, quad damage and one-hit KO (12x damage).
- **No Heals**: Various in-game elements which normally fully refill health will not heal you anymore if this setting is enabled.
- **No Melon Slice Drops**: Enemies will no longer drop melon slices. The only chance you have of refilling health is limited to the melon crates if you have this setting and no heals on.
- **Kong Perma Death**: DK Isles has been afflicted with a terrible curse. If a kong dies, you will lose that kong forever. Lose all of your kongs and you will game over. You may be temporarily given a kong back to beat a boss, but that is all the grace you will get. To remove this curse, you must reach Hideout Helm and turn off the Blast-o-Matic. Do be careful though, turning on this setting and losing too many kongs may make your playthrough unbeatable.
- **Disable Tag Barrel Spawning**: If you have Tag Anywhere on, you can now disable Tag Barrels spawning

## Random Medal Requirement
- The vanilla game normally requires you to have 15 banana medals to play Jetpac. In randomizer, you can randomize this requirement.

## Random Race Coin Requirement
- Each race will have a random amount of coins you will need to collect. The amount of coins required can be seen with the HUD.

## Key Modifier
- Change the amount of keys required to spawn the K. Rool boss fight from 0 to 8. You can also toggle whether Key 8 will be required or not within your pool of mandatory keys.

## Cosmetics
- **Music Rando**: Randomizes the music within the game within 3 categories. Those categories being Background Music, Fanfares, and Events.
- **Kong Colors**: Randomizes the color of each kong within a shortlist of available colors.

## Miscellaneous Settings
- **Auto-complete Bonus Barrels**: If this setting is enabled, Bonus Minigames will instantly produce their golden banana as soon as you load the bonus barrel.
- **Open Lobbies**: Opens all lobbies in the game. This doesn’t turn in any additional keys
- **Wrinkly Hints**: If this setting is enabled, Wrinkly will provide exhilarating hints which may help you beat your seed. Then again, she may just tell you some useless knowledge.
- **Shop Hints**: If this setting is enabled, shop owners will provide a hint to what move you are being offered before you buy it
- **FPS Display**: Displays an FPS display at the bottom left of the screen
- **Warp to Isles Menu Option**: If enabled, on the pause menu, you will occasionally be provided an option to warp directly to DK Isles, therefore saving you a console reset in situations where you want to just head back to the start of Isles.
- **Helm Start Location**: There are three options on where you want to start Helm from:
	- **Vanilla**: You will start Helm from the beginning of the level
	- **Skip Start**: You will start Helm next to the lever in the Blast-o-Matic room with all of the roman numeral doors open.
	- **Skip All**: You will start Helm next to the Coin door with the Blast-o-Matic off.
- **Troff ‘n’ Scoff Portal Numbers**: Shows a number on the Troff ‘n’ Scoff portal with the amount of bananas left to turn into Troff ‘n’ Scoff in that level.
- **Shop Indicator**: Displays a series of faces of all the kongs who have a move purchasable in that shop. A “SOLD OUT” sign will appear if there are no moves left to purchase in that shop.

## Miscellaneous Changes
    
- **Shop owners**: They will now only sell you 1 move at a time
- **Moves**: They have been decoupled from their vanilla order. Therefore you can purchase Cranky’s special moves out of sequence should the seed dictate so
- **Vanilla bugs fixed**: “Fake Key” and “Helm Medals glitch” have been fixed as these two glitches are heavily detrimental to casual play.
- **Aztec Sandstorm & Castle Rain**: Both have been disabled to heavily reduce lag. Additionally, turning off the castle rain/lightning effects helps improve playability of Castle for those who have photosensitivity.
- **Speedy T&S Turn-ins**: Colored Banana turn-ins in Troff ‘n’ Scoff are now 4x faster.
- **In-Game Time**: Now displayed in H:M:S.ms format, and it removes all lag from IGT calculation to provide some additional balance between cross-console races
- **File Screen**: Displays some extra statistics including seed hash, moves obtained, keys obtained and blueprints obtained.
- **K. Lumsy Keys**: All keys you possess will be turned in at the same time and will skip their associated cutscene in Isles.
- **Homing Ammo**: If you have homing ammo, and you want to use standard ammo instead, you can hold L to use standard ammo instead
- **Krazy Kong Klamour**: No longer affected by lag, which should make playing this minigame on Wii U VC and some emulators a lot easier without pause buffering.
- **Sniper Scope**: No longer shows overlay, improving FPS from 20fps to 30fps. The crosshair for Sniper has been changed to yellow to better indicate when you have Sniper Scope.
- **Lowered requirements for freeing Aztec Kongs**: Llama Temple gun switches are pre-spawned (you no longer have to do the Baboon Blast course) and the Ice is already melted in Tiny Temple
- **Textboxes**: Will no longer close until you press B, making it easier to read important text.
- **Stack Trace**: If the game crashes (which we have done everything to prevent), the game will show a stack trace which is useful for debugging. (N64/Emu only. Wii U is weird)
- **Exit Softlocks**: Some exit locations have been slightly modified so that you are no longer softlocked if you come out of certain exits with insufficient progression
- **Dance Skips**: No longer occur in races, fixing some oddities surrounding dance skipping race golden bananas
- **Tag Anywhere**: Bunch of bug fixes surrounding this to make it a better experience
- **End Sequence**: Shows credits of all those who helped make V1 of DK64 Randomizer possible

# V0.1 Beta
## Level Order Randomizer
- Randomizes the order of levels. Hideout Helm will always be the last level (Unlock all kongs is forced on if this setting is enabled)
## Gameplay length Modifiers
- **B. Locker and Troff ‘n’ Scoff Requirement**: Change the requirements for each B. Locker and Troff ‘n’ Scoff in the game
- **Presets**: There are 4 presets which you can select which will change the requirements:
	- **Vanilla**: B. Lockers and Troff ‘n’ Scoffs are their vanilla amount
	- **Steady**: Gradual and consistent increments from one level to the next
	- **Half**: B. Lockers and Troff ‘n’ Scoffs are roughly half their vanilla amount
	- **Hell**: B. Lockers and Troff ‘n’ Scoff requirements are vastly increased.
## Miscellaneous settings
- **Unlock all Kongs**: Unlocks all kongs from the start of a new file
- **Unlock all Moves**: Unlocks all moves (excluding Sniper Scope) from the start of a new file
- **Unlock fairy camera/shockwave**: Unlocks the Banana Fairy’s reward (fairy camera and shockwave attack) from the start of the game
- **Fast Helm Start**: Starts Hideout Helm in the Blast-O-Matic Room with the roman numeral doors opened
- **Crown Door Open**: Opens the crown door in Helm by default
- **Coin Door Open**: Opens the coin door in Helm by default
## Quality of life features
- **Tag Anywhere**: Pressing D-Pad Left or D-Pad Right will change kongs between what kongs you have unlocked
- **First Time Text**: Most of the annoying first time text has been removed
- **Cutscenes**: Some of the unnecessary cutscenes are auto-skipped
- **Fast Boot**: The game skips the rap and DK TV upon boot
- **Story Skip**: Set to “on” by default