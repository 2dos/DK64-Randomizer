If you wish to play the exact same seed with others, there are a few ways that we support you sharing seeds.

# .lanky File
## Creating and Patching
Upon loading up the generator, there is an option to "Generate a patch file". If this is enabled, and then you generate your seed, the generator will spit out two files. The `.z64` ROM and the `.lanky` patch file. If you wish to play the same seed with others, but want to allow others to change only the cosmetic features, send the `.lanky` file over.

If you have received a `.lanky` file and wish to generate a ROM from that `.lanky` file, then you will need to visit the generator, click on `Generate from Patch File`, and then upload your patch file to the generator to produce a patched Randomizer ROM. You can also modify the cosmetic attributes before you generate to allow your seed to visually look a little different to others.

## Benefits
- Fits within Discord's file size limit
- Allows others to modify cosmetic features whilst racing the exact same seed functionality-wise

## Drawbacks
- Files only work for the same version of the site that they were generated. If the site base code changes between the making of the `.lanky` file and the usage of it, it will fail to work.

# Settings String
## Creating and Patching
After picking your settings, click "Export" in the lower section of the generator page. This will fill a textbox to the left of the button with a settings string that you can copy and paste to others.
To import a settings string, paste the desired settings string into the textbox on the left of the aforementioned buttons, and then click "Import". This will change all the settings on the website to match those which were set when the setting string was exported.

## Benefits
- Allows others to modify settings to make tweaks to their own preferences. Can also be used as a way to race the same seed if you both use the exact same seed without modifying any settings.
- Settings string is just text, should your setup have restrictions on uploading files or if you have a lower quality internet connection.

## Drawbacks
- Any settings changes, including the seed, will change the assortments in the randomizer. As such, accidental changes can result in an unfair playing field

# BPS File
## Creating and Patching
After you have patched your ROM, create a BPS file that goes from the vanilla ROM to your patched Randomizer ROM. You can use any BPS patcher you have on hand. If you do not have any BPS Patcher program, we would advise our [tailored BPS Patcher](https://dev.dk64randomizer.com/bps_maker) as it prevents any issues arising from others having different ROM endianness.
To patch from a BPS, we would advise using [ROMPatcher.js](https://www.marcrobledo.com/RomPatcher.js/)

## Benefits
- Others will not have to go through the generator to make their seed
- Everyone will have the exact same byte-patching ROM no matter what.
- Works regardless of when the patch was made or when the patch is used.

## Drawbacks
- Unless you're using our tailored BPS patcher, problems can arise if not everyone has the same ROM endianness
- No cosmetic changes can be made to a seed from a BPS file
