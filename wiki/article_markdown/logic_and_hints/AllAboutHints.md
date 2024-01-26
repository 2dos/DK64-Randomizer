This page is designed to explain the ins and outs of the hint system in DK64 Randomizer. This is a complex system that is of very high importance to quickly beat seeds, particularly when item randomizer is enabled. Each type of hint works a little differently so each will be covered separately and some common features will be listed at the end.  

# A quick note on hint systems
- The "Standard" hint system is recommended for most settings. This system is flexible and accounts for all kinds of win conditions, seed length, predicted fill difficulty, and many other settings.  
- The "Cryptic" setting is identical to "Standard" with some light riddling in names.
- The "Fixed" setting is optimized for Season 2 racing. See Season 2 Hints below for details.

# Path Hints
Path hints are critical to finding very important items across your seed. They come in the basic form of: `"An item in the {hint region} is on the path to {path endpoint}."`
## How do they work?
The goal with path hints is to pare down to the bare essentials (within reason) for the end item on the path. So if Key 8 is locked by Coconut, Key 8 will have Coconut on its path. This then applies to all other prerequisites, so all items needed to get Coconut will be on the path to Key 8. This repeats until the moves needed have no prerequisites. At this point you have created the path. Here's an example.
```
"Key 7": {
    "Factory Dirt Patch (Dark Room)": "Key 7",
    "Isles Dirt Patch (Under Caves Lobby)": "Bongos",
    "Japes Diddy Medal": "Coconut",
    "Caves Donkey 5 Door Cabin": "Peanut",
    "Castle Diddy Medal": "Primate Punch"
}
```
The goal of the path is on the top of the path listed, and then items are generally acquired in order. Bongos + Coconut will get you Peanut out of Donkey's 5 Door Cabin. Then Peanut will get Punch from Diddy's Castle Medal. Finally you get Key 7 from the dirt patch in the Factory Dark Room.
## Assumptions
Some assumptions are made to improve the quality of the paths. This is important to more efficiently hint more relevant things. These assumptions are ***critical*** to maximizing your understanding of how path hints will direct you. Assumptions made vary by settings.  
For path generation it is assumed that:
- You have infinite coins. No moves will be hinted strictly for acquiring coins. This would be absolutely awful to get hinted, as it would intuitively point you in the wrong direction entirely.
- You have infinite GBs. Similarly to coins, a move needed strictly for GBs would point you in the wrong direction, making it an actively detrimental hint.
- You have access to K. Rool. This is essential to K. Rool paths. More on that later.
- You have access to all Kongs. This is to prevent significant retreading or duplication on paths. If Peanut is used to unlock Tiny, we don't want Peanut to be on the path to every Tiny check in the game. This is often stated as "Kongs are assumed," meaning that **a path hint will never point at a Kong's location directly!**
- You have access to all levels. Similarly to Kongs, Everything on the path to Key 5 should be aimed directly at that item to be as straightforward as possible. We don't want Key prerequisites to be on the path to Keys via another Key. This is often stated as "Keys are assumed" meaning that **in S2, a path hint will never point at a different key's location directly!**  
*Note for Loading Zone Randomizer: This assumption does not apply in LZR! This is because the impact of adding any given loading zone is significantly reduced.*
- You can dive to get into level 4. This is to prevent a heavily-locked Diving from impacting every location in level 4. It would be unintuitive for Diving to be on the path to Forest Chunky Minecart purely because Forest was level 4.  
*Note for Loading Zone Randomizer: This assumption does not apply in LZR! This is for similar reasons as the previous, as gaining access to a single random entrance is less impactful.*
- You can get past the quicksand at the start of Aztec. Vines or Tiny + Twirl is always available before Aztec, but we don't want that to overload or misdirect paths for anything in Aztec. *However*, Vines often ends up on the path to things in the back of Aztec because you may need Vines (or Rocketbarrel) to get to the Guitar pad that opens it up.  
*Note for Loading Zone Randomizer: This assumption does not apply in LZR! Much of the time you have access to Aztec via exiting the 5-Door Temple, and when you don't it is notable.*
- You have access to upper Isles. Again, another Vines constraint to possibly save some headaches. This is far more niche and not relevant to S2 because with activated Isles warps you immediately have access to upper Isles.  
*Note for Loading Zone Randomizer: This assumption does not apply in LZR! This is because it is again loading-zone-based in settings where these specific loading zones likely matter significantly less.*
### Hint Regions
One half of your path hint is comprised of a region of DK64. These regions are arbitrarily created by us and utilize natural divisions in levels to help intuit reasonably-sized chunks of the game. **All locations are in exactly one region.**  
The full list of regions is here: https://docs.google.com/spreadsheets/d/1V8E9CzuS0SfXl9vVpm4oMn2ddJVNrwXDOKlIL109tOE/edit#gid=0  
A full list of location-region pairs for all S2 locations is here: https://docs.google.com/spreadsheets/d/1V8E9CzuS0SfXl9vVpm4oMn2ddJVNrwXDOKlIL109tOE/edit#gid=510482791  
If the location that is being hinted is a starting move, it will directy hint the move itself instead of the location. e.g. `"Your training with Rocketbarrel Boost in on the path to..."`
## Path Endpoints
There are a couple different path endpoints and they largely behave literally with some nuance:
- Keys can be an endpoint to hinted paths. e.g. `"path to Key 4."`  
The number of hints you will get for a Key depends on the length of the path. Longer paths get more hints. Fixed hints has a specialized algorithm to distribute the fixed number of hints *(see Season 2 section)* while in Standard settings the number of hints correlates to path length as follows:  
  - Length 1-2: 1 Hint
  - Length 3-6: 2 Hints
  - Length 7-10: 3 Hints
  - Length 11+: 4 Hints  

  *The path length to Key 8 does not include Monkeyport, Gorilla Gone, or Vines if you start with them and Key 8 is guaranteed to be in Helm.*
- K. Rool phases can be an endpoint if your win condition is to defeat K. Rool. e.g. `"path to aiding Diddy's fight against K. Rool."`  
  - The Donkey phase requires nothing and will never be hinted
  - The Diddy phase requires Peanut and Rocketbarrel
  - The Lanky phase requires Trombone and Barrels
  - The Tiny phase requires Feather and Mini Monkey
  - The Chunky phase requires one Slam upgrade, Primate Punch, Hunky Chunky, and Gorilla Gone  

  Similarly to Key paths, in Standard hints the number of K. Rool path hints seen is based on the number of items on the path to defeating K. Rool. Season 2 has a corner case regarding this. *(see Season 2 section)*  
*Starting moves that are used for K. Rool phases do not count towards this path length!*  
  - Length 0: No Hints (you started with all the moves you need)
  - Length 1-2: 1 Hint
  - Length 3-4: 2 Hints
  - Length 5-7: 3 Hints
  - Length 8-10: 4 Hints
  - Length 11+: 5 Hints
- The camera can be an endpoint if you don't start with it and your win condition is All Fairies or Kremling Kapture. This is to assist in your search for the Camera as needed. The number of hints you get is identical to the path length of Keys.
## Duplicate Path Hints
If you see two path hints with **exactly** identical phrasing, *they refer to different locations in that region!*  
If you see `"An item in the Japes Hillside is on the path to Key 5."` on two different hint doors, then two different items in Japes Hillside are on the path to Key 5.  
If you see these two hints  
`"An item in the Japes Hillside is on the path to Key 4."`  
`"An item in the Japes Hillside is on the path to Key 5."`  
They could be referring to the same location (see Duplicate Aversion).  
**NOTE: The K. Rool path is treated as one path, regardless of phase!** This means that you can see these two hints:  
`"An item in the Giant Mushroom Exterior is on the path aiding Diddy's fight against K. Rool."`  
`"An item in the Giant Mushroom Exterior is on the path to aiding Chunky's fight against K. Rool."`  
and know they always refer to different locations!  

# Way of the Hoard Hints
These are hints that point to distinct individual locations that are strictly logically required to beat the seed. Whatever item you find at that location will be helpful in achieving your win condition. This is a riff on ZOOTR's Way of the Hero and functions identically.
## "Strictly Required"
A "strictly required" item means that every sequence of events that can logically complete the seed will always use that location. This means that either/or situations are often neither Way of the Hoard.  
The most notable example of this is with Progressive Slams. Often you need one slam upgrade for Chunky phase. In many of those worlds, you could logically acquire either slam upgrade to beat the seed. This means that neither is "strictly required" because there exists a world where you did not go to one of the slams' locations and still beat the seed. If one slam locks the other slam, then all worlds will route through the first slam's location, making that location Way of the Hoard.
## Interaction with Path Hints
While Way of the Hoard hints are *always* unique from each other, there can be some overlap with path hints. Two of your hints may be:  
`"An item in the Giant Mushroom Insides is on the path to Key 5."`  
`"Forest Tiny Mushroom Barrel is on the Way of the Hoard"`  
It is possible for these to both be referring to the same location, but you cannot be certain until you have full cleared the region. It could be that Key 5 is on Forest Donkey Mushroom Cannons while Gorilla Gone is in that bonus barrel.
## Duplication Aversion
Both Path hints and Way of the Hoard hints are aimed at specific locations. These two categories of hints are generated independently of each other with one exception. There is a mechanism which attempts to reduce the number of times a location is hinted.  
Each hint is looking at a specific location. If a location is randomly chosen to be hinted but is already hinted elsewhere, it will reroll that choice exactly once. If the reroll is an already hinted location, tough luck.

# Helm Order Hints
You may find these hints if your Helm requires fewer than 5 Kongs. You are *guaranteed* to find one somewhere in your seed if eligible.

# K. Rool Order Hints
You may find these hints if your goal is K. Rool and you have fewer than 5 phases. In addition to these hints you may find on doors, you can find the K. Rool fight order on the wall in K. Rool's throne room in Helm. Because of this, you are not guaranteed to find one of these hints if your seed is expected to route through Helm (required Key 8 in Helm).

# Kong Location Hints
You may find these hints if you unlock your Kongs throughout your seed. 
- If Kongs are in cages, you will find hints that tell you which Kong frees another in a level. This will not distinguish between cages in Aztec.
- If Kongs are not in cages (e.g. on GBs, in shops, etc.), you will find hints that tell you who finds each Kong and in what level. e.g. `"Tiny can find Diddy in Jungle Japes."`  
Sometimes they will not hint the Kong but instead hint the item type they are on (e.g. "A fairy holds Diddy in Jungle Japes"). You will always get one hint per locked Kong.  
In some rare scenarios, you may see `"{kong name} can find {him/her}self in {level}? How odd..."` This means that the kong is on a check flagged for themself but is still available for other kongs, usually through the Free Trade Agreement used in S2.

# Direct Item Hints
You may find these if you have early randomized keys to find. These constitute Keys 1 and 2 in simple level order. This is relevant to S2 specifically for Key 2.  
These hints are identically formatted to the Kong location hints when Kongs are out of cages: `"Key 2 can be found by {kong} in {level}."`
- Note that if the item is on a boss, your hint will point to the Kong the boss is for, but it will not tell you it's a boss!

# Foolish Hints
A region is "foolish" if you need no items inside that region.
- Collectibles are NOT considered when calculating foolish regions. You may need to enter foolish regions for coins, colored bananas, or GBs.
- Foolish hints are specific to major item locations. They only care about the locations contained in the specific region, not any events. If the Lighthouse is foolish, that does not kill every location that needs the water raised, nor does it mean that all entrances in the region are foolish in LZR.
- You may find a hint that says "It would be foolish to collect colored bananas in {level}." This means that your medal rewards AND the boss in that level contain nothing useful.
- These hints do take into account items locking other items. For example if you find a crown in a foolish region, you know that neither Helm door requires crowns.
- The only vials that can be in foolish regions are Ammo Belts and Instrument Upgrades. No vials that have logic implications can be found in foolish regions.
 
# Entrance Hints
You may find these hints if you are in coupled or decoupled loading zone randomizer seeds.
- You are prioritized one hint that points you to Japes, Aztec, and Factory each.
- The remaining entrance hints will usually point to important locations, prioritizing useful connectors like Castle tunnels or Training Grounds.

# Microhints
Most microhints follow the Direct Item Hint format:  
`"You would be better off looking in {level} with {kong} for this."`  
If the location is not tied to a kong, it will instead state the type of location:  
`"You would be better off looking for {item type} with in {level} for this"`
## Some
- Monkeyport: Touching the Monkeyport pad at the back of Krem Isle while holding enough GBs to enter the most expensive non-Helm B. Locker (usually level 7) will give you a hint to its location.
- Gorilla Gone: Touching the Gorilla Gone pad in Helm Lobby while holding enough GBs to enter Helm will give you a hint to its location.
- Slam: Entering the Chunky phase of K. Rool without a slam upgrade will have the announcer tell you what levels you can find both slam upgrades in. If they are in the same level, he tells you a single level.  
Note that K. Rool progress is saved. You can progress up to this phase, get the hint, get a slam, and return straight to Chunky phase.
## All
- Helm Instruments: Touching an instrument pad in Helm while not in possession of that instrument will give you a hint to its location.

# Season 2 Hints
The "Fixed" option uses a fixed distribution of hint types and is optimized for the S2 racing preset. It is best used in conjunction with exactly the S2 racing preset.  
The distribution is as follows:
- Helm Order: 1
- Kong Location: 3 (one for each locked kong)
- Key Path: 10
- K. Rool Path: 5
- Way of the Hoard: 9
- Foolish Region: 7  

These numbers were taken from the rough average of the "Standard" system's outputs for S2 settings while also culling worse hint categories.  
A notable absence is a K. Rool order hint. You are expected to piece this together from K. Rool path hints as well as the wall in Helm.

## When to use this Fixed setting
This option does not have anything specific enabling or disabling it, but you are ***VERY*** likely to encounter errors if the settings deviate significantly from the S2 preset.  
Breaking deviations can include (but are not limited to):
- Changing the win condition
- Starting with more/fewer keys
- Starting with too many moves
- Removing Shops from the item pool
- Starting with more/fewer kongs
- Probably some other things I'm forgetting because it's complicated  

If you're not sure, the "Standard" settings are more likely to give your custom settings a suitable (or better) experience.

## Fixed Number of Key Path Hints
With a fixed number of key path hints, the fixed number of hints are distributed to give more hints to keys with longer paths. This can lead to an arbitrary number of hints for a key, possibly up to 6 if one key is WAY more locked than the others.  
It is possible to deduce the relative lengths of paths for each key depending on how many hints you get. If you get more hints for Key 5 than Key 7, you know that Key 5 has more items on its path and could be harder to find.  
***Every key is guaranteed to have a hint!***

## Fixed Number of K. Rool Hints
There exists a niche corner case for K. Rool path hints in the Fixed setting:  
`"Very little is on the path to K. Rool."`  
This means that there are fewer than 5 hintable things on the path to K. Rool. This usually manifests through some combination of Donkey phase being required, a number of K. Rool moves in your starting move set, and/or other moves being lightly locked.

# Dev Hints (coming in 3.0)
## Multipath
Multipath hints are a natural extension of path generation. Instead of one move hinted to one path, it is **one move** hinted to **every path** it is on.
- These share the same hint regions, endpoints, and assumptions as the old single-path hints.
- Hints can point to key and win condition paths at the same time. e.g. `Something in the Lighthouse Area is on the path to Key 8 and K. Rool vs. Lanky`
- Every endpoint in your seed is guaranteed to be on at least one multipath hint unless hinting it would be useless. This might look like: `Your training with Mini Monkey is on the path to K. Rool vs Tiny` (and nothing else!)
- Keys 1 and 2 in simple level order are no longer given direct item hints, and are instead given paths and folded into the multipath hints. You may see things on the path to Key 2 now.
- Same hint availability rules apply: if you're missing a Key 2 hint, it should be available without Key 2.
- All multipath hints will always point to different items. Identically worded multipath hints still point to different items (as path hints do).
- You can get a LOT of paths hinted for a single item. Fear not! This is usually a very important item with broad uses and your path hints that point to single paths usually help home in on your goals.
- The number of multipath hints you get is tied to the overall length of your paths by a similar formula as before. It calculates how many hints you would get in the old version (see Path Endpoints section above) and then gives you about that many Multipath hints. To simplify, you should be getting a comparable amount of multipath hints as you got path hints. Given that they generally give more info, this is a buff!
### Negative Information from Multipath
Because ALL paths are hinted for the chosen item, you can use that information to deduce what an item is NOT on the path to. This may assist you as you track down your last items - remember what they cannot be behind!
- e.g. `Something in the Main Isle is on the path to Key 4 and K. Rool vs Diddy` (and NOT on the path to any other Keys or K. Rool phases!)   

## Foreseen Pathless
An item is "foreseen pathless" if it is not on the path to anything. This essentially means the item is not "strictly required" and is not Way of the Hoard.
- The hint will look something like: `I have foreseen that there are no paths to the Hoard which contain Baboon Blast.`
- You may need a pathless item to satisfy an either/or, but it will still not be on any paths. e.g. Japes Painting Hill Dirt can be acquired with either Orangstand or Pony Tail Twirl. If both are available, then an item in that dirt patch would not prevent either from being hinted pathless.
- Only moves can be hinted pathless. You're welcome beanlievers.
- Progressive Slams cannot be hinted pathless.
- Certain moves are obviously more important than others, and the hints are biased to hint those moves pathless more than others. The moves are: every gun, every instrument, Vines, Diving, Barrels, Camera, Shockwave, Rocketbarrel, Mini Monkey, and Primate Punch.

## Region Potion Counts
These hints tell you how many potions are contained in a hint region.
- The hint will look something like: `Scouring the Forest Mills will yield you 2 potions.`
- The hints have nothing to do with the quality of the potion. Instrument Upgrades and Ammo Belts are included in the count!
- Eligible hint regions are regions that *are not shops* and contain at least one potion.
- There is no bias to what eligible regions it will select.
- *This only counts potions!* You may find Kongs or Keys in that region that do not contribute to the count.

## Other Hint Changes
- You can only receive a maximum of 1 a Helm Order hint and 1 K. Rool Order hint. I will not apologize for Rocketbarrel locked Helm orders.
- B. Locker and Troff 'N' Scoff value hints have been disabled for item rando. These hints are so bad they aren't even mentioned anywhere in this document.
- The Fixed hint preset has changed to account for the new hint types. It is now the following:
  - Helm Order: 1
  - Kong Location: 3 (one for each locked kong)
  - Multipath: 14
  - Way of the Hoard: 9
  - Foolish Region: 4
  - Forseen Pathless: 2
  - Region Potion Count: 2

# Item Hinting Hints (Dev)
This is an entirely separate hint system designed to be a streamlined experience. It is intended to be more approachable than learning paths while still maintaining complexity and depth in analysis. It is entirely separate from the standard hint system, as none of the above hint types will appear.

## Hint Structure
The hints have a 50/50 chance to be either:
- A: `Looking for {item}? Try looking in the {hint region}.`
  - Hint regions are the same ones used in path hints.
- B: `Looking for {item}? Try looking in {level} with {kong}.`
  - This style follows the same general hint structure as the microhints (see above), meaning it could also be: `Looking for {item}? Seek {location type} in {level} for this.`
    - Location types include Kasplats, dirt patches, fairies, and battle arenas.

## What things get a hint?
- The items that can be hinted are Kongs, Keys, and non-junk moves.
- The priority of what gets hinted is the following:
  - Keys
  - Kongs that are on the Way of the Hoard
  - Moves that are on the Way of the Hoard
  - A slam if you have not received a slam hint from the above priority and you don't start with Slam 2
  - Moves/Kongs that are not on the Way of the Hoard
- This priority means that if a move is hinted, it is more likely to be required.
- If a move is not hinted, it is NOT required unless your seed has so many required items that not everything could get a hint (this is rare unless you're actively trying to make a seed awful).

## Hint Placement
- Every hint door available will be taken by these item hinting hints.
- Hints to _required_ things will try very hard to not lock themselves. 
  - e.g. A Rocketbarrel hint will not be on the Rocketbarrel-locked door in Caves lobby unless it is not Way of the Hoard.
  - e.g. A Key 2 hint will not be in lobby 3 or lobby 4.
- There are a few hints that will be placed before item hinting hints:
  - A Helm Order hint will be placed if Helm is random and required.
  - A K. Rool Order hint will be placed if K. Rool is random and required.
  - A hint will be placed for each random Helm door.

## Advanced Item Hinting
All the same rules apply to Advanced Item Hinting except that the item to-be-hinted is instead hinted as a category of that item.
- For example, a kong would be hinted as `Looking for kongs? Try looking...` (the rest of the hint is the same as described above)
- Kong moves can be hinted as either `Looking for {kong} moves?` or `Looking for {move type}?`.
  - The move types are: `Guns`, `Instruments`, `active kong moves` (Punch, Grab, etc.), `kong barrel moves` (Mini, Rocketbarrel, etc.), `kong pad moves` (Blast, Balloon, etc.)
  - Even though you can now hint items in two different ways, ***there will only ever be one hint per item! All hints point to unique items!*** You can use this fact to crunch the numbers on whether or not an item is hinted or if an ambiguous hint points to a desired item.
- Barrels, Diving, Oranges, and Vines are always hinted as `Looking for training moves?`
- Other shared moves (slams, sniper. homing) are always hinted as `Looking for shared moves?`
- Camera and Shockwave are hinted as `Looking for fairy moves?`
- A hint to the Bean will be unchanged.
- The category is plural for grammatical purposes - *each hint always refers to a single item.*
