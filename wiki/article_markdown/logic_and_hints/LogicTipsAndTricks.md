This page is intended to clarify some knowledge about how the fill places items and notable logic useful for many playthroughs. Tips are provided in no particular order, but are grouped by level. Information relevant (but not necessarily exclusive) to Season 2 will is tagged.  

# Terminology
Some terminology is commonly used in randomizer discussion. Some definitions and examples should help clarify intent in the language used in the tips and tricks below.
- **"The fill"** - This refers to the algorithm that places items in locations randomly. When the fill "expects" something, it means that it is anticipating you have access to that something before further items can be placed. For example, if the fill is "expecting" you to have Coconut Gun, then anything depending on that expectation cannot be placed without you also having access to Coconut Gun.  
Fill expectations are only expectations, NOT requirements. You don't HAVE to get Coconut Gun before anything that "expects" you to have it. Fill expectations have no impact on items required to beat seeds.  
- **"Logic"** - This refers to the various expectations to reach locations and areas. For example, the logic expects you to have Coconut Gun to enter the Lighthouse Area in Galleon. The logic is flexible based on settings and may change those requirements based on activated glitch logic, entrance randomizers, and more.  
Logic requirements, on the other hand, are hard requirements. You will be logically required to have Coconut Gun to enter the Lighthouse Area (barring glitches, etc.) and if something is "logically required to beat the seed," that's where this comes from.
- **"Level order is/isn't important"** - The importance of level order affects several critical fill expectations and logic requirements.  
Level order is important in Vanilla level order and Level Order Rando without Complex Level Order enabled.  
Level order is NOT important in both Coupled and Decoupled Loading Zone Randomizers as well as Complex Level Order seeds.  
In **S2**, level order is important.
- **"LZR"** - Stands for Loading Zone Randomizer. It also includes both Coupled and Decoupled settings unless specified.
- **"FTA"** - Stands for Free Trade Agreement. This is the setting that enables Kongs to pick up other Kongs' major collectibles. Logic does account for this setting being enabled!

# Global
- **(S2)** If level order is important, the fill places items in such a way to guarantee a certain number of Kongs by each level. The fill expects:
  - 2 Kongs before entering level 3
  - 3 Kongs before entering level 4
  - 4 Kongs before entering level 5
  - 5 Kongs before entering level 6  
  
  For example, you cannot find any item that would lock your 4th Kong in level 5 or beyond. Levels 4 and earlier are fair game.
- **(S2)** If level order is important, the fill places Barrels, Vines, and Diving (not Oranges!) expecting you to have them BEFORE entering level 4.  
This can include level 4's lobby in some circumstances.
- **(S2)** The fill expects you to have 1.2 times the number of fairies required, rounded down, to reach the Rareware GB location. Basically, you have a small buffer on fairies that you may choose acquire.
- The fill expects you to have 1.2 times the number of medals required, rounded down, to reach the Rareware Coin location on Jetpac. This functions the same as above.
- The logic does take into account gravity affecting some rewards from automatically completed bonus barrels. Any barrel that drops their item does not require you to have to be able to reach the original barrel's location in the first place.
- **(S2)** The fill chooses completely random starting moves, independent of what Kongs you start with. This may or may not help your early progression, but the fill doesn't care.
- In LZR (mostly), you may be expected to use the Exit Level option on the pause menu. This will take you to the exit that you would normally reach by exiting the level portal. Some maps (notably most races) will only exit you to the entrance you came from.
- In LZR (mostly), you may be expected to die to return to the start of the level. Not all maps allow this (notably Japes Underground) but it is often crucial in 5-Door Temple rooms or the Factory Crusher room.
- **(S2)** **Tag Anywhere is NEVER in logic for anything.** If you tag Kongs somewhere without tag barrel access to compensate for not owning the guns or instruments you otherwise need, you are bypassing logical requirements.
- Some settings (most notably Kasplat location shuffle) can place Kasplats in water shallow enough their heads peek above the surface. These Kasplats are in logic with no additional items if you can reach them, as jumping on their heads kills them.

# Bonus Barrels and Bosses
- **(S2)** The Donkey Blast Helm minigame does not logically require any items, despite using a Baboon Blast barrel.
- **(S2)** The Lanky Sprint Helm minigame can be completed comfortably by any Kong and does not logically require Sprint.
- **(S2)** The Chunky Helm shooting minigame logically requires Homing, Sniper, or the hard shooting setting to deal with potentially troublesome mushrooms that hide behind boxes.
- **(S2)** Some Mad Maze Mauls have logical requirements due to the enemies contained within.
  - The 120 second Mad Maze Maul logically requires the barrel's Kong's gun and either Shockwave or Oranges.
  - The 125 second Mad Maze Maul logically requires the barrel's Kong's gun.
- **(S2)** Dogadon 2 does NOT require Primate Punch. Standard B punches also damage him while you are Hunky Chunky.
- **(S2)** If level order is important, bosses are placed in such a way as to guarantee they are beatable in logic with moves in or before their level. This means you can use boss placement to read the placement of specific items:
  - Hunky Chunky is always placed in or before the level that Dogadon 2 appears.
  - Twirl is always placed in or before the level that Mad Jack appears (in non-hard bosses).
  - Barrels is always placed in or before the level of the first barrels-required boss.
  - If the Aztec T&S is suspiciously cheap, it is likely that Guitar is placed after Aztec and locking the majority of CBs. This one is a little trickier to read as it's not a guarantee unless it's blatant.

# DK Isles
- **(S2)** Diddy's Peanut Cage above the waterfall logically requires the Rocketbarrel barrel to be spawned and used. This makes the location logically require significantly more things than you might expect at first glance. At a minimum, Barrels, Trombone, Rocketbarrel, and Peanut are all required.
- One of Donkey, Chunky, or Tiny + Twirl is logically required to reach the ear of DK Isle to enter lobby 6. This is sometimes relevant in Complex Level Order seeds and LZR.

# Jungle Japes
- **(S2)** In Kong Rando, the fill assigns a Kong to be the Diddy-freeing-Kong for the purposes of assigning a Kong to those locations. This changes what the location's Kong is for the purposes of hints. A "Diddy finds Chunky in Jungle Japes" hint could have Chunky on the item in front of the Kong cage if Diddy is the Diddy-freeing-Kong.
- **(S2)** The back of Japes only opens when you acquire the reward inside the Kong cage atop the hillside. The logic knows what requirements are necessary for this. This includes:
  - Whether or not there is even a Kong in the cage to be freed. This means that the cage is already open and the item can be freely run into.
  - Whether or not FTA is on for the item in the cage. This can mean you would be forced to go find the Diddy-freeing-Kong to pick up the item.
- **(S2)** The dirt patch on the hill to the painting room logically requires one of Lanky + Orangstand OR Tiny + Twirl.
- **(S2)** Entering the Japes minecart logically requires Chimpy Charge to slow down the conveyors and open the gate (despite the potential to jump around it).
- **(S2)** The Tiny Shellhive logically requires one of Saxophone or Oranges due to the strong, very large enemies that can prevent you from slamming the switches.
- **(S2)** Vines is not logically required to reach the Troff 'N' Scoff alcove above the right tunnel. You are expected to be able to jump into the alcove from the upper levels of the hillside.
- In Japes Diddy Mountain, hitting the Peanut Switch is not logically required to reach the slam switch. Diddy can jump across the gap or backflip up. This is generally only relevant in LZR, where you might not already have the gun.

# Angry Aztec
- **(S2)** Similar to the Diddy-freeing-Kong scenario (see Jungle Japes), the Tiny and Lanky cages work the same way.
- **(S2)** The Kasplat past the Coconut gate on the sandy bridge logically requires one of Donkey + Strong Kong OR Tiny + Twirl.
- **(S2)** The Guitar pad to open the back of Aztec logically requires either Rocketbarrel or Vines to reach it. Unlike the abilities needed to enter the level at all, this requirement is NOT assumed by the hints! See the All About Hints page for details on hint assumptions.

# Frantic Factory
- **(S2)** Similar to the Diddy-freeing-Kong scenario (see Jungle Japes), the Chunky cage works the same way.
- **(S2)** Only half of the switches at the bottom of the production room actually do anything. The Diddy and Chunky switches actually spawn their item while the Lanky item and Tiny bonus barrel are always spawned. *Regardless of this,* the ability to slam switches in Factory is logically required for all four.

# Gloomy Galleon
- In LZR, you may exit from an entrance that starts you swimming underwater. This means you then have logical access to everything underwater in that area. "Diving" according to the logic is the ability to press Z to go from surface swimming to underwater swimming. By exiting from an underwater entrance, you can bypass that requirement.
- **(S2)** Troff 'N' Scoff portals in this level are in inconvenient locations. You logically need one of Vines or Diving to reach any.
- **(S2)** For technical reasons the ship always has a green switch on it, regardless of the switch strength of the rest of the level.

# Fungi Forest
- **(S2)** The Day/Night switches logically require guns to activate. You can also use Oranges, but because this is uncommon knowledge it is not part of the logic.
- **(S2)** Climbing the interior of the giant mushroom does NOT logically require Vines. The single-vine gaps can be jumped. Note that the night-locked door does logically require Vines to reach.
- **(S2)** There are no logical requirements to drop down from the exterior top floor of the giant mushroom to the upper platform with the Kasplat or the platform with the Battle Arena, regardless of time of day.
- In LZR, every entrance in the Forest Mills is fair game to be shuffled. This includes every Mini Monkey entrance, including the normally-useless connector between the front of the mill and the back of the mill.
- **(S2)** The Lanky Shooting Attic logically requires Homing or the hard shooting setting.
- **(S2)** The dirt patch discovered beneath the grass in the mills area is a location that can have items. There is a miscellaneous setting (active in S2) that raises it slightly to make it visible.
- **(S2)** Chunky Keg Crushing logically requires you to activate the conveyor belt with Donkey. This makes it require a substantial amount of moves that might not be apparent. At a minimum you need enough slam upgrades, Gorilla Grab, Primate Punch, Triangle, and Barrels.  
  Chunky Keg Crushing only requires the crushing of 2 kegs to account for LZR seeds not being able to simply walk the third keg over.

# Crystal Caves
- **(S2)** There is a Strong Kong barrel added to the Donkey igloo. Because of that barrel, this location now logically requires Strong Kong.
- **(S2)** The Donkey Shooting Cabin logically requires Homing or the hard shooting setting.
- **(S2)** The Diddy Lower Cabin does NOT logically require Rocketbarrel. It is easy to backflip up to a side platform instead.
- **(S2)** The Tiny and Diddy Lower Cabins each logically require Oranges and are two of the very few locations to always logically require Oranges.
- **(S2)** Don't forget about the dirt patch in the Giant Kosha room!
- The Diddy Upper Cabin logically requires Guitar or Oranges. In non-LZR this is trivial, as the room requires Guitar to enter.
- The Battle Arena in Donkey's Cabin requires Donkey because only he can slam the switches to rotate the room. This is only relevant in LZR.

# Creepy Castle
- **(S2)** You are logically required to Monkeyport into the Museum to take the photo of the fairy there. It is possible (but not in logic) to take a photo of that fairy through the glass on Chunky's side of the Museum.
- **(S2)** Logic may require you to do the Lanky Tower with either Sniper or Homing. To hit the grape switches with Homing, you have to stand closer to the targeted switch's wall and let the homing shot carry the grape above your reticle.
- **(S2)** Despite the Sprint barrel inside, Lanky's Greenhouse does not logically require Sprint.
- **(S2)** Chunky's Shed can be completed by killing all the invisible enemies with either Triangle OR (Gorilla Gone + Pineapple). Both of these cases still logically require Primate Punch to open the box.
- **(S2)** The fairy inside the tree logically requires Diving. This is because it could be possible to softlock a seed by completing Donkey Tree Sniping, raising the water, and leaving (for whatever reason). You would then need Diving to get back to the fairy.  
  The exit from that room also requires Diving for a similar reason - when the water is raised you need Diving to access it.

# Hideout Helm and K. Rool
- **(S2)** The Helm Battle Arena (no matter where it is) always logically requires the Blast-O-Matic to be deactivated.
- **(S2)** The fill always fills Helm with valid items. This is to aid the fill in more location-starved settings.
- **(S2)** Donkey's K. Rool phase logically requires no items, despite using Baboon Blast barrels.
- **(S2)** Tiny's K. Rool phase logically requires Feather and Mini Monkey. You can also damage K. Rool's toes with Oranges. but this is not in logic. You do not need Twirl to jump over the shockwaves.