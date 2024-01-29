# Pack Formats

If you want to create your own cosmetic pack you need to adhere to the following format.

Within a zip file, eg: Pack.zip
```
bgm/
    - file1.bin
majoritems/
    - file2.bin
minoritems/
    - file3.bin
events/
    - file4.bin
```

You can name the files whatever you want they just need to have been converted with the n64 midi tool and saved as a .bin file.
Currently we just randomly select from the whole list of files and will eventually allow specific song placement.

# Creating Custom music

## Video Tutorial

It's worth noting that some information that this tutorial talks about is out of date, including (but not limited to):
- File Size Restrictions
- Using the desktop N64 Midi Tool (which is now outdated and bugged)

It's recommended that you visit [the discord](https://discord.dk64randomizer.com) for any information until a more up-to-date tutorial is available.

<ytvideo yt-id="gvPjUqf4ju4"></ytvideo>

## Acquiring the DK64 Soundfont
1. Open `N64 SoundBank Tool` (Note "Soundbank" not "Sound"), which can be found [here](https://github.com/jombo23/N64-Tools/tree/master)
2. Select `Donkey Kong 64 (U)` in the dropdown and load your DK64 US ROM
3. Select "Write all DLS Soundfont Banks", and select a folder. It should write a file called `ExtractedSoundbank_00.dls` in there
4. Visit the [online version of N64 Midi Tool](https://theballaam96.github.io/music_converter) and click `"Fix Soundfont"`.
5. Load `ExtractedSoundbank_00.dls` as your DLS Soundfont
6. Select either `DLS` or `SF2` as the output format. Different pieces of software will support either one or both of these, so feel free to download both the `DLS` version and the `SF2` version if you're unsure.
7. Click `Download`.
8. Happy Donkin'

### Acquire other soundfonts

1. Open N64 SoundBank Tool (Note "Soundbank" not "Sound"), which can be found [here](https://github.com/jombo23/N64-Tools/tree/master)
2. Select the game of your choice in the dropdown and load the relevant ROM
3. Select `"Write all DLS Soundfont Banks"`, and select a folder. It should write a file called `ExtractedSoundbank_00.dls` in there
4. Go to this page and [download the installation package for Viena64](http://www.synthfont.com/Downloads.html)
5. Do all the installation setup. You will only need this program for the next 5-10 minutes.
6. `File > Import Soundfonts > Click "Ok" > Files > Select the ExtractedSoundbank_00.dls file > Open`
7. In the prompt that has popped up: `Select all in all Soundfonts > Ok`
8. `File > Save as > Save as a .sf2 file`
9. The SF2 file you just saved should now be the relevant soundfont you can work from. Feel free to uninstall Viena64 as you will no longer need it.

## Common Problems

**Important changes between vanilla DK64 and Randomizer**
> From 2.0 onwards, DK64 Randomizer can support files as big as 32768 bytes instead of 16512 for main BGM tracks. 
> Compressed file sizes aren't a concern with regard to DK64 Randomizer.

**An instrument is looping out of sync of other instruments when playing back my song in-game**
> Before importing your MIDI into `N64 Midi Tool`, check **BOTH** `No Repeaters` and `Extend Short Tracks`

# Custom Music Categorization
Music in DK64 is classed into 5 categories: BGM (Background Music), Major Items, Minor Items, Events, Other.

## Background Music
*Will play in the background in levels when walking around.*
- Jungle Japes
	- Jungle Japes (Starting Area)
	- Jungle Japes (Minecart)
	- Jungle Japes (Army Dillo)
	- Jungle Japes (Caves/Underground) (NOTE: Also plays in the seasick ship in Galleon)
	- Jungle Japes (Lobby)
	- Jungle Japes (Tunnels)
	- Jungle Japes (Baboon Blast)
	- Jungle Japes
	- Jungle Japes (Cranky Area)
- Angry Aztec
	- Angry Aztec
	- Angry Aztec (Beetle Slide)
	- Angry Aztec (Temple)
	- Angry Aztec (Dogadon)
	- Angry Aztec (5-Door Temple/5DT)
	- Angry Aztec (Lobby)
	- Angry Aztec (Tunnels)
	- Angry Aztec (Chunky Klaptraps)
	- Angry Aztec (Baboon Blast)
- Frantic Factory
	- Frantic Factory (Car Race)
	- Frantic Factory
	- Frantic Factory (Lobby)
	- Frantic Factory (Mad Jack)
	- Frantic Factory (Crusher Room)
	- Frantic Factory (R&D)
	- Frantic Factory (Production Room)
- Gloomy Galleon
	- Gloomy Galleon (Pufftoss)
	- Gloomy Galleon (Seal Race)
	- Gloomy Galleon (Tunnels)
	- Gloomy Galleon (Lighthouse)
	- Gloomy Galleon (2DS)
	- Gloomy Galleon (5DS/Submarine)
	- Gloomy Galleon (Treasure Chest)
	- Gloomy Galleon (Mermaid Palace)
	- Gloomy Galleon (Mechanical Fish)
	- Gloomy Galleon (Baboon Blast)
	- Gloomy Galleon (Lobby)
	- Gloomy Galleon (Outside)
- Fungi Forest
	- Fungi Forest (Anthill)
	- Fungi Forest (Barn)
	- Fungi Forest (Mill)
	- Fungi Forest (Spider)
	- Fungi Forest (Mushroom Top Rooms)
	- Fungi Forest (Giant Mushroom)
	- Fungi Forest (Day)
	- Fungi Forest (Night)
	- Fungi Forest (Minecart)
	- Fungi Forest (Dogadon)
	- Fungi Forest (Winch Room)
	- Fungi Forest (Lobby)
	- Fungi Forest (Baboon Blast)
	- Fungi Forest (Rabbit Race)
- Crystal Caves
	- Crystal Caves (Army Dillo)
	- Crystal Caves (Cabins)
	- Crystal Caves (Rotating Room)
	- Crystal Caves (Tile Flipping)
	- Crystal Caves (Tunnels)
	- Crystal Caves
	- Crystal Caves (Tantrum)
	- Crystal Caves (Beetle Race)
	- Crystal Caves (Igloos)
	- Crystal Caves (Lobby)
	- Crystal Caves (Baboon Blast)
- Creepy Castle
	- Creepy Castle (Wind Tower)
	- Creepy Castle (Tree)
	- Creepy Castle (Museum)
	- Creepy Castle (Kut Out)
	- Creepy Castle (Dungeon Without Chains)
	- Creepy Castle (Inner Crypts)
	- Creepy Castle (Ballroom)
	- Creepy Castle (Greenhouse)
	- Creepy Castle
	- Creepy Castle (Minecart)
	- Creepy Castle (Crypt)
	- Creepy Castle (Dungeon with Chains)
	- Creepy Castle (Lobby)
	- Creepy Castle (Trash Can)
	- Creepy Castle (Baboon Blast)
- Hideout Helm
	- Hideout Helm (Blast-o-Matic on)
	- Hideout Helm (Blast-o-Matic off)
	- Hideout Helm (Bonus Barrels)
	- Hideout Helm (Lobby)
- DK Isles
	- DK Isles
	- DK Isles (K. Rool's Ship)
	- DK Isles (Banana Fairy Island)
	- DK Isles (K. Lumsy's Prison)
	- Training Grounds
	- DK Isles (Snide's Room)
	- K. Lumsy Celebration
	- K. Rool Takeoff
- Miscellaneous
	- Cranky's Lab
	- Funky's Hut
	- Bonus Minigames
	- Mini Monkey
	- Hunky Chunky
	- Snide's HQ
	- Candy's Music Shop
	- Pause Menu
	- Rambi
	- Troff 'n' Scoff
	- Awaiting to enter boss
	- Battle Arena
	- Strong Kong
	- Rocketbarrel Boost
	- Orangstand Sprint
	- DK Rap
	- Mad Maze Maul
	- Stealthy Snoop
	- Minecart Mayhem
	- Boss Introduction
	- Mini Boss
	- Gorilla Gone
	- Intro Story Medley
	- Enguarde
	- Main Menu
	- K. Rool's Theme
	- K. Rool's Battle
	- End Sequence
	- K. Lumsy Ending
	- K. Rool's Entrance
	- Monkey Smash
	- Wrinkly Kong
	- Nintendo Logo

## Major Items
*The song will play whenever a major item is spawned or collected.*
- Golden Banana (GB) / Key Get
- Company Coin Get
- Blueprint Get
- Blueprint Drop
- Move Get
- Gun Get
- Headphones Get
- Pearl Get
- Drop Rainbow Coin
- Rainbow Coin Get
- Bean Get
- Banana Medal Get

## Minor Items
*The song will play whenever a minor item is spawned or collected.*
- Banana Coin Get
- Minecart Coin Get
- Melon Slice Get
- Crystal Coconut Get
- Fairy Tick
- Melon Slice Drop
- Drop Coins (Minecart)
- Checkpoint
- Normal Star

## Events
*The song will play sometimes when triggering an event.*
- Triangle Trample
- Guitar Gazump
- Bongo Blast
- Trombone Tremor
- Saxophone Slam
- Transformation
- Success
- Failure
- Boss Defeat
- Boss Unlock
- Success (Races)
- Failure (Races & Try Again)
- Baboon Balloon
- Oh Banana
- 100th CB Get
- Going Through Vulture Ring
- BBlast final star

## Other
*(There is no way to randomize these tracks by design. These are purely listed to prevent confusion)*
- Silence
- Unused Coin Pickup (In rando, this is changed to the windows 95 theme that plays on fast boot)
- Water Droplets
- DK Transition (Opening)
- DK Transition (Closing)
- Generic Twinkly sounds
- Fairy Nearby
- Nintendo Logo (Old?)
- Generic Seaside Sounds
- Tag Barrel
- K. Rool Defeat
- Start (To Pause Game)
- Unused High-Pitched Japes
- Bonus Barrel Introduction
- Game Over