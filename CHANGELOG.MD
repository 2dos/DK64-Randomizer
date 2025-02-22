# Version 4.0 First Dev Push notes
This is the changelog for the initial push of 4.0 into Dev:
- Below is a list of features that are being pushed to the dev site
- If you encounter any Bugs, please post your Spoiler log and [BPS](https://dev.dk64randomizer.com/bps_maker) with an explanation of the bug in the #dev-Bug-Reports [Discord Channel](https://discord.dk64randomizer.com).


## CHANGELOG
### New Randomizers
- Chaos B. Lockers
    - Items other than Golden Bananas will be required to clear the B. Locker. The counts of which are dictated by `Chaos Ratio`
- Added shop owners in the item pool
    - These will need to be obtained to purchase items inside the shops. Hints which indicate the level a shopkeeper is in can be obtained by visiting their shop when they have yet to be obtained.
- Nintendo & Rareware Coins have been split up in the item rando selector
- K Rool phases have been added into the boss pool, meaning they can appear behind boss doors. Consequently, regular bosses can now appear in the final boss sequence, turning it into a boss gauntlet
- Added custom races for Castle Car Race
- Added the ability to collect colored bananas in Isles, which will add 5 extra medals to the game. This is exclusive to CB Rando, and can be changed with the dropdown menu there.
- Changes to LZR:
    - Added option to add Helm and Helm Lobby to the loading zone pool
    - If auto-keys is enabled: K. Lumsy entrances are added to the pool
    - If kongs are in the Item Rando pool: Tiny Temple and Llama Temple entrances are in the pool
    - Better Hints have been written
- Added DK Portal randomizer, which will randomize where the start of the level is. It uses the same pool as custom wrinkly doors and T&S Portals. There's a fair amount of excluded locations to prevent unbeatable scenarios
- Ice Trap Updates:
	- Added the ability to customize how many ice traps are going to be **ATTEMPTED** to be placed. This takes away from the junk allocation, meaning that a seed with a lot of ice traps will not have a lot of junk (inc. Dropsanity).
	- Added two new kinds of Ice Traps:
		- Reverse Controls: Obtaining a "Reverse Controls" ice trap will reverse your controls for about 8 seconds.
		- Slowing: Obtaining a "Slowing" ice trap will slow the player down to about 50% speed for 8 seconds, and place a lot of goop on the player. Our lawyers have told us to inform you that this green goop is not from K. Rool's toes.

### Others
- A statistics screen has been added to the end sequence, which displays:
	- % time played as each of the 5 kongs
	- Amount of tags performed
	- Amount of photos taken
	- Amount of times caught by kops
	- Amount of enemies killed
- Added functionality to make enemies in crowns decrease the timer, depending on what enemies are killed. Shockwave will nullify almost all bonus you receive from killing, so killing them without shockwave is always a better idea.
- Oranges have been enabled in crowns
- You can now specify the exact amount of pearls to spawn Mermaid GB
- Added an option to change the amount of bonus barrels per room that you need to complete in order to defeat a helm room. This comes with the following options:
	- Two: Vanilla behavior
	- One: The right-most barrel in each room will be completed
	- None: Playing the instrument pad will play the room shutdown cutscene
- Added Moontail glitched logic
- Hard Mode changes:
    - Hard bosses has been separated from Hard Mode again, with the ability to select the specific changes you want regarding bosses to be enabled
    - Added `Shuffled Jetpac Enemies`, so that a level will utilize the enemies from a different level
    - Added `Lower Max Refill Amounts`, so that you will have to think harder on using your resources more efficiently
    - Added `Strict Helm Timer`, which will make the base start time of Hideout Helm 0 minutes instead of 10
	- Added `Angry Caves`, which makes Caves rockfall constant, resulting in harder navigation of Caves. This takes priority over the `Calm Caves` QoL option.
    - Added `Donk in the Dark World` and `Donk in the Sky`, which will make traversing the game harder and require you to try and remember how the game looks.
        - `Donk in the Dark World` will apply the challenge of Fungi Dark Attic to the entire game (Excl. Japes Main area, Factory Testing and Factory Production room for performance reasons)
        - `Donk in the Sky` will disable level geometry rendering.
        - Enabling both will enable the secret `Memory Challenge` option, where some maps use Dark World and some maps use Sky.
- Added the ability to start the game in Training Grounds, with the need to complete 4 minigames to unlock the training moves.
- Changes to hints:
    - Added "Freeing Kongs" as a path endpoint which can be hinted.
	- You will no longer see "Troff 'n' Scoff" path hints. Instead, they have been baked into the medal rewards region. The name of the medal rewards region in hints has been altered to make this a bit clearer.

### Quality of life changes
- Dirt patches have been added to item previews
- The "pad rising" cutscene in Castle Lanky Dungeon will now play if Item Rando is enabled to show the reward.
- Bonus Minigames will now display the difficulty of the minigame below it
- The lives mechanic has been removed from DK Arcade
- Removed the troll flame from DK Arcade 75m

### Fixes
- Fairies can now have the bean, pearls, junk, medals and company coins. All of these 3 have been turned into 3D Models when an actor
- Race hoops are now 3D models, making them easier to judge when you have flown through it
- Crowns can now be on Helm Medals and Key 8 checks, as this will no longer crash the game
- Helm Medal checks will no longer be able to be obtained early by clipping into the lazer field
- Cannon Game will now reset to it's default position upon failing the minigame or dispensing 5 shots
- The following enemies will no longer damage the player upon trying to shockwave them:
	- Purple Klaptraps
	- Red Klaptraps
	- Zingers
	- Robo-Zingers
	- Bats
- Spider Boss fight room no longer has the `pickups_respawn` attribute, meaning that bizarre effects will no longer happen
- Kabooms that are placed via enemy rando will now explode within a timely manner (4.67s), rather than potentially taking 18 minutes to do so.
- The slam switch on the K. Rool Ship in Galleon will now respond to `Progressive Switch Strength`
- The wind tower in Castle will now allow you to stay at the top after exiting the bonus barrel.

### Cosmetic-adjacent changes
- Added the ability for multiple kongs to play as Krusha, and added the ability to play as K Rool (both costumes), Cranky (DK only) and Candy (Tiny only). Disco Chunky is still a cosmetic setting, but will only be available to enable if you have Chunky in his default costume.
- Added ability to specify a specific transition spin image, using the transition editor: https://theballaam96.github.io/transition_editor
- In Chunky Phase, chunky will now be translucent during the punch sequence
- Dirt patches have been made easier to distinguish (no item preview)
- "Dark Mode Textboxes" has been changed to "Dark Mode UI", and will also make the D-Pad visual dark
- Added option to display the song name on-screen when it starts playing
- Added big head and small head mode (thanks to GL for help with this)
- Added color swaps to the following objects and sprites:
	- Jetman
	- Golden Bananas (And consequently ice traps, which are a hue shift on the new banana color)
	- Shockwave particles
	- Fireball/Fire Sprites (Disabled with colorblind mode)
- Added color swaps to enemies and other NPCs:
	- Affected by "Random" color swaps:
		- Klobbers *(Also affects some regular barrels)*
		- Kabooms *(Also affects some regular TNT barrels)*
		- Klump (Attire)
		- Kosha (Just the body)
		- Robots
		- K. Rool (Clothes, Gloves, Toes)
		- Ghosts (Kritter-in-a-sheet)
		- Funky and Candy
		- Both beavers
		- Kasplats
	- Affected by just "Extreme" color swaps:
		- Kosha (Club and Helmet)
		- Kremlings
		- Rabbit
		- Snakes (Teetering Turtle Trouble)
		- K. Rool (Skin, Crown, Belt emblem)
		- Klump (Skin)
- Added model swaps to the following objects:
	- The kremlings that burp in the piano minigame in Frantic Factory
	- The spotlight fish in Galleon
- Crowns (excl. "Forest Fracas") will now have random names
- Added "Keep Vanilla Song Locations" option
- The background of the pause menu has been overhauled to remove the blurry background and change it to a simple darkening effect, making it easier on the eyes, more modern and less taxing on system resources
- The numbers in Number Game in Factory will utilize random colors if "Random Misc Cosmetics" is on
- The DK Portal and the transform/tag barrel underside textures have been updated to the updated DK64 Randomizer logo

### Misc
- Irondonk now plays the game over cutscene upon losing all 5 kongs
- Potion icon has been updated
- 3D Melon model has been updated
- Added Snap to the end sequence
- The option for native widescreen has been removed (Too much strain on the game)

### Plandomizer
- Added ability to plando custom locations for objects

### Site Changes
- The spoiler log display on the website has been completely reformatted
- The site has been ported to boostrap 5.3.3 (from 5.1). This will mostly result in changes that you don't recognize. The major change as a result of this is that the sliders on the progression tab have been changed as our old sliders only supported bootstrap 3 and 4, and just so happened to work on 5.1.
- Various events on the site will produce a toast providing the user feedback on what is happening.
- `Complex Level Order` has been merged into the `Entrance Randomizer` selector
- Galleon shipwreck gates remaining open is now in the `Misc Changes` selector rather than the `Removed Barriers` selector.

### Technical Changes
- Lots of internal code cleanup
- Converted all display list modifications to using f3dex2 macros
- `pointer_addresses.json` has been vastly shrunk to be quicker on site loading
- Boss doors which have 0 CBs as the unlock condition will now employ a less hacky way of doing this without crashing the game. This fixes a few bugs which occurred as a result of this.
- More settings have been dumped to the spoiler. A lot of internal changes have been made to best facilitate trackers that aim to support 4.0 during dev.