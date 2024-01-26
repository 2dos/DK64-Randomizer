The DK64 Randomizer is able to be played on many different consoles and emulators. We will list more emulators in here as we test them; both ones that are recommended and ones to avoid.

# Supported

## N64

### Everdrive

The DK64 Randomizer is confirmed to work with any Everdrive version 2.5 and above. This includes 2.5, 3, X5 and X7. Just simply drop the ROM into its SD card and load it as normal. We recommend that any players looking to play on N64 purchase one of these (note that only the X5 and X7 are currently sold as new).

Everdrive versions lower than 2.49 (including the Everdrive plus spinoff) does work, but may have saving issues. 

**For Everdrive 2.5 and 3.0 users, do NOT use the version 3 OS! The current recommended OS are as follows:**

| Everdrive      | OS to Use |
| -------------- | --------- |
| 2.5, 3.0       | [2.13](https://krikzz.com/pub/support/everdrive-64/v2x-v3x/os-bin/OS-V2.13.zip)      |
| X5, X7         | [3.06](https://krikzz.com/pub/support/everdrive-64/x-series/OS/OS-V3.06.zip)      |

Simply format your SD card then extract the contents of the downloaded folder to your SD card to install the OS.

### 64drive

The 64drive has not been tested, but likely works.

## Wii U VC

The DK64 randomizer works via inject on Wii U VC. Instructions on how to set up a Wii U VC inject can be found [on Ballaam's DK64 Practice ROM website](https://dk64practicerom.com/install?guide=wii_inject).

**THE WII U OS VERSION MUST BE AT LEAST 5.5.6**

## Bizhawk (DK64 Edition)

**NOTE**: BizHawk tries to emulate the lag of the N64 and is more PC intensive. If this doesn't sound like something you'd be happy with using, use a different platform.

[Bizhawk (DK64 Edition)](https://github.com/theballaam96/BizHawk-dk64Edition/releases/tag/DK64-1.0) is a special build of Bizhawk specifically for DK64 randomizer. The game otherwise doesn't save on normal Bizhawk builds.

In order to run BizHawk, you may need to install the [pre-requisites](https://github.com/TASEmulators/BizHawk-Prereqs/releases/tag/1.4).

## Project 64 3.0

[Project 64 3.0](https://www.pj64-emu.com/public-releases) introduced several changes that fixed several problems with DK64 emulation that older versions had. By default, Project 64 should detect that Donkey Kong 64 is the game being played when a DK64 Randomizer ROM is loaded. However, there are still adjustments that need to be made to make it fully playable with DK64 Randomizer. 

1. Go to Options -> Configurations to access the settings menu.
2. **Uncheck** "Pause emulation when window is not active" and **uncheck** "Hide advanced settings."
3. Click "Plugins." Ensure "GLideN64" is the selected video plugin.
4. Close Project64.
5. Navigate to the Project64 3.0 directory on your computer (usually in the C drive in the Program Files x86 folder). Go to the Config directory and open _Project64.rdb_ in the [RDB Editor Webpage](https://dev.dk64randomizer.com/rdb_editor). Save the output file as _Project64.rdb_. Once you downloaded the new version of the file, delete the old one in the PJ64 directory before placing the downloaded file here.

For transparency purposes, the editor adds the following text to the bottom of the file and saves it to the right format:
```
[DONKEY KONG 64-C:45]
Alt Identifier=69696969-69696969-C:45
RDRAM Size=8

[69696969-69696969-C:45]
Internal Name=DONKEY KONG 64
Status=Compatible
Counter Factor=1
Culling=1
Emulate Clear=1
Primary Frame Buffer=1
Save Type=16kbit Eeprom
Linking=Off
```

# Do not use

## Project 64 versions 0, 1 or 2

Old versions of PJ64 have game breaking bugs such as random void outs and warping across the map. Please use 3.0 or above.

## Retroarch

Retroarch cannot save DK64 save files and therefore is not recommended for use with DK64 randomizer. In addition, the cores have various issues with the way the game is rendered:
- The Mupen core has the usual ugly graphical spiking bugs that exist in basically every other Mupen-based emulator.
- The ParaLLEI core does not have the graphical spiking bugs, but instead has various graphics that don't properly load when you are far away (objects are just black shapes) or simply dont load at all.

## BizHawk

Use the specific DK64 build of Bizhawk instead; you will not be able to save the game otherwise and will likely experience game-affecting graphical glitches.

## Anything Else Not Listed

Anything listed under **Do Not Use** or anything else that isn't listed on this page will not be officially supported by DK64 Randomizer.

# Troubleshooting

## BizHawk (DK64 Edition)
**The game is too laggy**
> BizHawk tries to emulate the lag of the Nintendo 64 due to being primarily intended as an emulator to make [Tool Assisted Speedruns](https://www.youtube.com/watch?v=Ietk1-Wb7oY). As such, in-game lag is expected. Additionally, for similar reasons, the emulator is more intensive on your computer than other emulators which don't strive for similar goals. If this is something you do not want, use another platform instead (except N64)

**I'm getting an expansion pak message on boot/emulator setup message on the main menu**
> You've almost certainly downloaded regular BizHawk. Please download the DK64 Edition instead

**I'm getting errors regarding Microsoft C++ Redistributable 2015 before even getting to the emulator**
> You've most likely not fully installed the pre-requisites for BizHawk. Please run the [pre-requisites](https://github.com/TASEmulators/BizHawk-Prereqs/releases/tag/1.4) program. If you are still getting the error, Microsoft should have a download somewhere. Google is your friend.

## Project64 3.0
**Jittery Camera**
> Make sure `Emulate frame buffer` is on in `Options > Graphics Settings > Frame buffer`

**Getting a fatal error or some form of other error upon booting ROM**
> This is most likely a symptom of `Project64.rdb` being incorrectly set up. I would advise re-performing those steps, ensuring that you are overwriting the existing `Project64.rdb` file located in the config folder, and that your file is named **EXACTLY** `Project64.rdb`

**I'm getting an emulator setup error on the main menu**
> This is a symptom of an incorrectly set up emulator, generally `Project64.rdb` not being created correctly. See "Getting a fatal error or some form of other error upon booting ROM" above.