# Website

It is highly recommended you [use the website](https://dk64randomizer.com/) to generate your DK64 randomizer ROMs. The vast majority of players should have no need to run this locally. If you are interested with messing around with the code and starting your own build of DK64 randomizer, see the bottom of this article for instructions.

The website requires your DK64 ROM to be the US version (NTSC-U).

The Japanese (NTSC-J), European/Australian (PAL), Kiosk and Lodgenet versions do not work with the Randomizer.

**DK64randomizer.com does not contain or host any copyrighted material. You MUST provide your own DK64 ROM.**

# Running DK64 Randomizer Locally

[Python 3.10 or above](https://www.python.org/downloads/) is needed to run DK64 Randomizer locally. It does not matter which version you install.

Once Python is installed, you can download the program from the [main code page](https://github.com/2dos/DK64-Randomizer) on GitHub, click the green "Code" button and then download the ZIP (or open one of the other listed methods if preferred). 

1. Open a CMD window or your favorite code editor.
2. Set the CMD folder to the DK64 Randomizer base folder by typing `cd "directory"`
> Example: `cd "C:\Users\2dos\Programs\DK64 Level Progression Randomizer\dk64-randomizer"`

3. Place your US ROM in that directory
4. Copy `python ./runner.py` (or `python3 ./runner.py` depending on what Python version you installed) into the window and hit enter. This will run an HTTPS server off your local machine.
5. Open a web browser and navigate to `https://localhost:8000/`, which will be your downloaded version of DK64 Randomizer.