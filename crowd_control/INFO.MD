# Crowd Control Effects
This document goes over all effects available in DK64 Randomizer: Crowd Control

## General information
- Only 4.0 and above is supported for Crowd Control. 3.0 will not work as it does not have the necessary code changes to handle all of the Crowd Control effects

## Player
### Drunk Kong
Enables a timed effect equivalent to the one you see upon grabbing the reward in Chunky's seasick ship. Controls are reversed. Will enable the warping screen effect if the "Remove Water Oscillation" cosmetic option is disabled.

### Disable Tag Anywhere
A timed effect that disables the ability to use Tag Anywhere throughout it's duration. The disabling will be reflected with the D-Pad OSD with the kong heads being translucent

### Ice Trap the Player
Ice traps the player (will only use the ice trap bubble effect, not the reverse controls or slow sludge effect) which the player will need to break out of.

### Spawn Rocks
Spawns a series of rocks every second just like the Giant Kosha tantrum throughout the duration of this timed effect.

### Instant Balloon
Instantly makes the player inflate as if they pressed Z on a Baboon Balloon pad, which will make them float for 2-3 seconds in the air. If you redeem this whilst the player is in Baboon Balloon, it will extend the duration of that balloon.

### High Gravity
Makes all gravitational values in the game 4x bigger throughout the duration of the effect

### Low Gravity
Makes all gravitational values in the game 4x smaller throughout the duration of the effect. Yes, this also applies to moonkicks.

### Slip
Instantly slips the player up as if they stepped on a banana in DK's house

### Change Kong
Changes the player's kong to a random one that they have and disables tag anywhere throughout the duration of the effect. You will not change to a kong you have yet to acquire, or one you have lost if you have Irondonk enabled.

### Do a backflip
Makes the player do a backflip.

### Ice Floor
Reduces the player's traction to 5% of it's normal value, this makes accelerating to top speed slower and also makes the player carry on moving after stopping for a lot longer.

## Inventory
### Give Coins
Gives 2 coins to each kong (even ones you do not own yet). This caps at 255 coins

### Remove Coins
Removes 2 coins from each kong (even ones you do not own yet).

### Give Consumables
Slightly restocks the consumable inventory of the player. This includes film, crystals, ammo, oranges and instrument energy.

### Remove all consumables
All consumable items are taken from the player. Same types as `Give Consumables`

### Give a Golden Banana
This gives a golden banana to the player. Due to technical reasons, the golden banana is given to the kong in the level where their count is the least. This allows for the player to receive about 5100 golden bananas.

### Remove a Golden Banana
Removes a Golden banana from the player.

## Health
### Refill Health
Resets the player's health to it's fullest capacity

### One Hit KO
Sets the player's damage multiplier so that any damage will kill the player throughout the duration of this effect.

### Double Damage
Sets the player's damage multiplier to 2x. Any damage inflicted will be twice as much as usual. For example: Touching a beaver will do 2 quarter-melons worth of damage instead of 1. Like `One Hit KO`, this is a timed effect.

## Misc
### Get Kaught
Instantly spawns a kop in front of the player. It is hardcoded for this kop to instantly catch you, so evasion is impossible and you will be warped back to the start of the level upon getting caught.

### Get Out
Spawns Krosshair and gives the player 10 seconds to leave the map. If they do so, Krosshair will go away. If they do not leave the map in 10 seconds, they will be killed by a fireball. Pressing start to pause the game is disabled so you can't cheat your way into just pause exiting the level.

### Flip Screen
Flips the screen horizontally and vertically throughout the duration of the effect.

### Warp to the DK Rap
Warps the player to the DK Rap. If the streamer does not want the rap to play in it's entirety, they can set the duration to lower than 188 seconds. **DO NOT SET THIS HIGHER THAN 188 SECONDS**. Pressing start to cancel the rap is disabled.