
# 2.0 Initial Push to Dev Branch
This is the changelog for the initial push of 2.0 into dev:
- There will be more changes to come, which will be posted in `#dev-branch-changes` when they are made.
- Whilst we have made a lot of effort to make dev branch stable and bug fix when we find things, we would like to remind that **dev branch is not a stable branch. Playing on dev means you may experience crashes or seeds being unbeatable**. Please post in `#dev-bug-reports` if you find anything. 
- Additionally, if you come across something you don't like that isn't a bug, please post in `#dev-discussion`. We're always looking for feedback and ways to improve the randomizer.

## NOTES FOR DEVS BEFORE PUBLISHING (AMEND CHANGELOG AS APPROPRIATE TO REMOVE ENTRIES)
- Wrinkly Door/T&S Rando is still pending locations from Seagull, and logic.
- Battle Crown Rando is still pending logic
- Item Rando doesn't have any hints (yet)

## CHANGELOG
### New Randomizers
- **Battle Crown Rando**: Battle Crown Pads will be in new, interesting locations.
- **Wrinkly Door & T&S Door Rando**: These doors will be in random locations. There will be 5 wrinkly doors scattered around a level including the lobby, and some amount of T&S Doors.
- **Move Rando**: Gloriously expanded. Now (optionally) includes the camera and shockwave (can be decoupled) as well as the four training moves.
- **Colored Banana Rando**: Bismuth (Speedruns Explained) has placed over 8,000 new colored banana locations. They can be anywhere and everywhere.
- **Item Rando**: Golden Bananas, Medals, Blueprints, Company Coins, Crowns and Keys. They have been shuffled amongst eachother. 
	- Note: This has only recently been completed. This does not have any hints included
	- Note 2: We are going to expand this to include kongs and moves into the pool. It's just gonna take some time. 
- **Cross-Level Warps**: Warps can now be paired with warps from other maps. You can choose between coupled and decoupled cross-level warps.
- **Enemy Randomizer Multiselector**: Enemy Rando has been expanded to include a selector where you can specify what enemies will appear in the pool. Yes, this includes "Oops All Kops".
### End Game & New Gamemodes
- **K. Rool Improvements**: Chunky Phase is no longer guaranteed to appear in the K. Rool Sequence.
- **Helm improvements**: If DK is in the Helm room sequence, he will no longer always be first.
- **Win Condition Editor**: Getting bored of fighting K. Rool? Change the win condition to one of the following:
	- **Beat K. Rool**: Self-explanatory. Smack that crocodile into DK: King of Swing.
	- **Get Key 8**: All of what you love, minus the crocodile guy.
	- **All Fairies**: Capture them all and give the most useless item in the game some love.
	- **All Blueprints**: Show exactly how OP Blueprints are by getting these as quickly as you can.
	- **All Banana Medals**: For the small banana enthusiasts.
	- **Pokemon Snap**: Take a picture of every enemy in the game. Wonderful!
- **Helm Hurry Mode**: Start with 15 minutes, get time added for collecting certain items. The official Twitter review is "Stressful".
	- Golden Bananas add 30 seconds.
	- Blueprints add 2 minutes.
	- Freeing a kong adds 5 minutes.
- **Free Trade Agreement**: Items are no longer bound by the annoyances of being locked to certain kongs. Any kong can pick up any item. There's multiple options with this to go into finer granularity.
### Cosmetics
- **'Cause this is thriller.**: Chunky is in the mood for the spooky season. If you ask me, perhaps a little *too* in the mood. He's grown his hair and ditched his normal clothing.
- **He's the 6th Member of the DK Crew**: Krusha feels like he's been left out, so he might kidnap one of the kongs and take their place (and their moveset).
	- For kongs who have a Z+B special move (Diddy Charge, Lanky OStand, Chunky Punch), you need to be under a certain speed in order to execute these moves if that kong is swapped out.
	- This will override the new Chunky cosmetic if Chunky is replaced.
- **File Screen Tracker**: The file screen has been revamped to show a tracker for which items you have.
- **Visible Bananas**: If colored banana rando is on, the colored bananas of the kongs you don't own will be visible.
- **Colorblind Mode**: If you are colorblind, there is a setting which modifies the colors of the kong-specific items in the game to be more distinguishable.
### Improvements and miscellaneous changes
- **Galleon Water Balloons**: The galleon balloons above the water on the shipwreck side have been adjusted to spawn more easily without unintuitive camera movement.
- **Uninverted Camera Controls**: Toggleable in the options menu of the game.
- **Guards are afraid of a ghost**: Guards have gone a little blind and will no longer spot a kong if they are in Gorilla Gone.
- **Rabbit Race 2**: Will now provide infinite crystals for the duration of the race.
- **Bonus Barrel Autocomplete**: Now will only explode if the bonus barrel is visible.
- **Cutscenes**: Hate them? Good! We've removed over 250 extra cutscenes as part of the "Remove Cutscenes" Miscellaneous change.
- **Misc Changes**: Has been segmented into various different options which you can customize to your hearts content.
### Bug Fixes
- **Fast Warps**: Now change music as expected
- **Fungi Bean**: In the vanilla game, this would only stay in your inventory as long until you exit your file. The bean will now permanently save to your file.
- **Flying TNT Pad**: In the vanilla game, if you throw the TNT Barrel with Tiny, under certain situations, the TNT Pad will latch onto the barrel and move with it. This has been fixed. Unfortunately, a side effect of this fix is that the TNT pad will not respond to the ground ripple effect that AD does.

## Other notes
- **Presets**: We haven't updated any presets yet with any of the new features. Season 1 settings will likely not change, likewise with the `Vanilla but Better` preset. Other presets will be changed after we see how each thing plays. A season 2 preset will be made in the future to include some of the 2.0 changes with the aim of seeds being roughly the same length as season 1.