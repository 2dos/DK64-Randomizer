# Developing the base hack of DK64 Randomizer
## Initial Setup
1. [Fork the DK64 Randomizer Repo](https://github.com/2dos/DK64-Randomizer/fork)
2. Create a branch based off the dev branch, and load that new branch up using GitHub desktop or the git client of your choice.
3. In a command prompt, navigate to the base directory of the repo. Run the following: ```python -m pip install -r requirements-dev.txt```
4. Place a DK64 US ROM called `dk64.z64` in `./base-hack/rom/`. If you have a `.n64`, you can use [this](https://hack64.net/tools/swapper.php) tool to swap the endianness of the ROM so that it'll work with the build procedure.
5. Go to the base-hack directory in the command prompt and run ```./build.bat --test python``` in command prompt. This will start the build process of the base hack of DK64 Randomizer and produce a ROM in the `./base-hack/rom` directory called `dk64-randomizer-base-dev.z64` which you can open in your emulator of choice. This is a way to generate a ROM to test scenarios without having to go through the generator. The first run of this will take a while as there's a lot of initial setup that the build procedure has to do.

## If you wish to update display lists
1. Get [Ubuntu for windows](https://ubuntu.com/desktop/wsl)
2. Get [the N64 toolchain](https://github.com/glankk/n64) by running the `sudo sh`(...) command stated in the README
3. In your Ubuntu for Windows console, run `nano ~/.bashrc` to edit the `.bashrc` file with nano, and add the following entry at the bottom:
```
# GFXDIS
g() {
    gfxdis.f3dex2 -x -d -g dl++ "$1"
}
```
4. Save the file and exit, then restart Ubuntu for Windows.
5. To convert dl bytecode to Gfx, run the following command:
```
g FA000000FFFFFFFF
```
Where the argument is the bytecode. If you set it up correctly, gfxdis should output the following:
```
gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
```

## Final necessities before pushing your changes
1. Once you are happy with your changes and it's behaving as you would expect, run `Lint Repo` in the VSCode tasks.
2. Run ```./build.bat - python``` in a the command prompt in the `./base-hack` directory. This is necessary as the last step because it creates the patch file used by the generator.