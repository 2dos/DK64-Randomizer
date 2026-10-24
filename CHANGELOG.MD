# Version 6.0 First Dev Push notes
This is the changelog for the initial push of 6.0 into Dev:
- Below is a list of features that are being pushed to the dev site
- If you encounter any Bugs, please post your Spoiler log and [BPS](https://dev.dk64randomizer.com/bps_maker) with an explanation of the bug in the #dev-Bug-Reports [Discord Channel](https://discord.dk64randomizer.com).


## CHANGELOG
## IMPORTANT PSA
6.0 Includes a huge rework in the Fill and Patching process. Previously, Fill and Patching were intertwined, but with the addition of a new fancy tool called Protobuf (Proto), we can now separate the Fill and Patching process. Why you ask? This will be explained later in the changelog. The biggest risk with this is by separating the Fill from the patching, **there can be a mismatch between the Spoiler log and the actual seed**, meaning you might find say Kremling Kosh in your seed when it was actually supposed to be Stealthy Snoop. A lot of dev testing has gone into making sure everything matches with the Spoiler log. In addition, this made a huge change to setting strings since they have been moved from an API to a proto. Please double check the string on import to see if everything matches up. **IF YOU FIND ANY MISMATCHES BETWEEN YOUR GENNED SEED AND THE SPOILER LOG. REPORT IT! DONT BE A KEIPER**
### New Randomizers
- New items added into the pool
  - Time of Day:
    - The Fungi Day/Night switches are now added into the pool. Collecting a day/night item will open the corresponding time of day items. Adding this into the pool will overwrite your `Fungi Time` setting
  - Cannons:
    - All cannons such as the Castle Lobby and Fungi Isle cannon are locked behind the cannon move. This doesnt affect Blast courses and DK Phase.
- New Checks added into the pool
  - Balloons:
    - All kong balloons can now be checks, a preview of the item will be shown on the balloon and will drop to the ground on pop. This also affects custom CBs. No this does not add the corresponding balloons into the item pool, popping will still add 10 CBs to your inventory.
  - Breakables:
    - Any chest or box such as the underwater checks in Galleon or the Fungi Boxes can now be checks
- White Slam:
  - You can now make a level not require a slam in the `Progressive Switch Strength`. Walking on a switch will acivate said switch.
- Free Trade Agreement CBs
  - Colored Bananas can now be collected by any Kong if the `Free Trade Agreement` setting is set to `All + CBs`.
- Custom Minigames:
  - DK Arcade and Jetpac can now be customized. Play your favorite games such as Wordle and 2048.
    - Turn on `Custom Arcade Minigames` in the Bonus Barrels section of the Overworld tab, then use its cog to choose which minigames each machine can become. One is picked at random for each machine. Leaving a list empty allows every custom minigame, and ticking Vanilla allows the original game.
    - If you're interested in making a custom minigame to be added for everyone to play, inquire in [#dev-discussion](https://discord.com/channels/463917049782075395/559837132428935170)
- Custom Kong models:
  - Cranky, Candy, Funky, and K. Rool are now playable. Simply choose which model you want to replace a Kong in the `Kong Models` setting
- New Switchsanity options:
  - Primate Punch and Chimpy Charge gates can now be added in switchsanity, meaning you can now be expected to Primate Punch a Gong or Chimpy Charge a Punch gate
- Added a bunch of new wincons including a tasks wincon:
  - List of new Wincons:
    - Shoot the Mechanical Fish's heart
    - Complete the second round of DK Arcade
    - Complete the Jetpac Check
    - Defeat the Toy Monster
    - Obtain the secret fairy reward
    - Blast Courses
  - The Tasks wincon allows you to mix and match between 8 different tasks to create a wincon jamboree
- Irondonk revision:
  - Irondonk is now revised to be a lives based challenge instead of a 1 life per kong challenge. Running out of lives will permanently delete your save file.
- Random Face Puzzle Pictures:
  - You can now replace the face puzzle images. This will change the tiles to include the Kong color.
    - This also means that Chunky Face Puzzle no longer has 2 solutions

### Misc
- Added Random Kong and Boot SFX:
  - The boot sfx that plays when you load a seed and the initial kong on the
- The remaining items in Arcade and Jetpac have been readded
- Fixed some jank with piano game with animation cancels
- Fixed the music bug that would cause parts of the audio engine to become unusable without a restart (it now fixes itself upon going through a spinning DK transition)
- Fixed notes unintentionally playing indefinitely (if they play longer than intended, going through a spinning DK transition will fix it)
- Fixed some jank with T&S Portals
- Fixed a bug when colliding with many items simultaneously
- Did some cleanup with Tag Anywhere limitations
- Bunch of base-hack cleanup
- Moved the Selector info from an API to protobuf for quicker site loads


### AP Changes
- Hey! Remember when I said why we wanted to separate the whole Fill from the Patching process? Well... Separating the Fill from Patching allows us to get rid of the Pillow and pyxdelta dependencies meaning the apworld has now gone from **37.2 Mb** down to only **1.9 Mb**. In addition the `.chunky` patch files have gone from 9.1 Mb down to only ~233.5 kB. The biggest and most important change however, is we now have **ROMless host generation for AP** 🎉🎉🎉🎉🎉🎉🎉🎉
- Site yaml exporter:
  - You can now use dk64randomizer.com to create a yaml. Simply choose the settings you want and in the `export` dropdown, click Export as yaml and enter the AP name you want. Double check the settings you picked though.
- In addition to the above, a bunch of new settings have been added to match up with the site
  - Fully revamped item pool:
    - You can now add more things to the pool such as:
      - Crowns
      - Blueprints
      - Banana Medals
      - Company Coins
      - Fairies
      - Rainbow Coins
      - DA BEAN
      - Pearls
      - Crates
      - Hints
      - Shopkeepers
      - Half Medals
      - Snide Turn-ins
      - Time of Day
      - Boulders
      - Balloons
      - Breakables
      - Dropsanity
  - A fully customizable starting moves pool which mirrors how the site does it. (You're welcome Bethany)
  - Progressive Switch Strength (you can change the Simian Slam switch strengths in each level, choosing between white, green, blue, and red)
  - We now have Krusha and Co. added as playable characters in the krusha_model_mode and kong_models settings
  - Troff n Scoff CB customization
  - Random DK Portal Locations
  - Random Starting Location
  - Half-Medal percentage
    - Instead of half-medals being at 50% of a full CB, you can now customize it to any percentage you wish
  - Custom Arcade Games
  - Free Trade Colored Bananas
- Note that not all new settings in the 6.0 changelog is in AP yet such as the new wincons but will be added in a future update
- Added damagelink
- UT now has a built in, fully accurate map and item tracker. To use this, download the latest poptracker pack from [here](https://github.com/UmedMuzl/dk64pt/releases/tag/rip) and put the zip into the `ut_pack_path` option under `dk64_options`. Poptracker will no longer receive any updates except to add new items and locations.
- I am speed:
  - The client now processes and sends items at Mcqueen speed. Text notifications also now go through a batching process and takes advantage of the countstruct system meaning if someone releases, instead of getting 5 separate banana medals, the client batches and send it as 5x Banana Medals