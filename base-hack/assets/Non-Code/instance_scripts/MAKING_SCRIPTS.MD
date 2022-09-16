# Object Instance Scripts

This guide serves as a knowledge base document for editing object scripts.
## Getting the Scripts
### Vanilla
To acquire the vanilla script files, including the `.raw` files that will be used by the object script editor introduced later in this guide, you will need to run `objectScriptGrabber.py` in the `instance_scripts` directory (You may want to copy this file to elsewhere on your PC and then run it in that separate location). Upon providing a DK64 US ROM, it will generate all of the object scripts.
### Scripts modified by Randomizer
Upon building the DK64 Randomizer base hack, it will generate all the `.raw` files that are supplied to the ROM in the `instance_scripts` directory. These are ignored by git, so you will not need to worry about deleting these.

## Editing the Scripts
### Operating the Editor
There is an editor for the object scripts which aims to make the process of modifying game object scripts easier. This can be found here: [Object Script Editor](https://theballaam96.github.io/object_script_editor.html)
Upon booting the editor, you can load a `.raw` file through the file prompt. Upon loading a file, it will convert the bytes into human readable-ish code. Since it's loading scripts for a map, there will likely be multiple objects which have a script.
To select a script, click a hex number in the bottom left box. These are a list of IDs for an object instance, each object in a map will have a unique ID. To see what each ID references, either reference the [viewer](https://theballaam96.github.io/object_script_viewer.html) (which has the object IDs provided) or the data extracted from when you ran `objectScriptGrabber.py`. This will display a C-Like representation of the code on the right-hand side, and an editable custom language on the left-hand side.
### Script Structure
Object Scripts are separated into blocks. Each block can contain up to 5 condition statements, followed by up to 4 execution statements. The way these are communicated are with certain statements:
| Statement | Usage | parameters |Syntax|
|-------------|---------|--------|-----|
|COND|Executes some in-game function which returns a true or false value. If it returns true, then the condition is successful. | 4: First parameter is the condition function index, last 3 are arguments | `COND 0 | 1 2 3` |
|CONDINV|Same as COND, but the condition is successful if the function passes as false, and is unsuccessful if the function passes as true | Same as COND | `CONDINV 0 | 1 2 3` |
|EXEC|Executes an in-game function|4: First parameter is the execution function index, last 3 are arguments| `EXEC 0 | 1 2 3` |
|ENDBLOCK|Terminates a block|None|`ENDBLOCK`|
## Saving a script
For Randomizer, due to the frequent nature of collaboration, the "Save Map Scripts to PC" functionality of editor is not used. Instead, we store the scripts that have been modified to be different to vanilla in some way inside the Randomizer repository in a `.script` file. 
### Creating a map directory
**Only do this bit if your script is part of a map which has no other previously modified scripts in it**
To create a map directory that is correctly interpretted by the Randomizer base hack build routine, you need to do some minor formatting.
**1** | Create a directory in `instance_scripts` for your map with a name that is indicative of the map name. For example, if you are modifying a script inside mech fish, call it `mech_fish` or `galleon_fish` or something of that nature.
**2** | Create a file inside that directory named `.map`. Inside this file, list the map index (which can either be stored as hexadecimal or decimal). To get the map index, [use this tool](https://htmlpreview.github.io/?https://github.com/theballaam96/DK64TestScripts/blob/master/Donkey%20Kong%2064/Glitch%20History%20Webpage/maplookup.html#).

Example `.map` file for Mechanical Fish:
```
0x33
```
### Creating a script File
Script files contain the code for your modified script as well as some header information that is used to correctly write your code to the right spot in ROM.

**1** | Create a `.script` file which is named appropriately. For example, if your script modifies the Arcade Round 1 Golden Banana, you would create a file with a name like `arcade_gb.script`
**2** | Create a .data section in your file:
```
.data
id = 0x0
behav_9C = 0
```
The ID is the object ID that you are modifying (can either be hex or decimal). To find the object ID, see either the output from `objectScriptGrabber.py` or the [script viewer](https://theballaam96.github.io/object_script_viewer.html). If you are adding a completely new script, ensure your ID is unique and include `behav_9C = 0` in your .data header
**3** | Create the .code section of your file:
```
.data
id = 0x0
behav_9C = 0
.code
COND 0 | 1 2 3
CONDINV 0 | 1 2 3
EXEC 0 | 1 2 3
ENDBLOCK
(...)
```
The code section is the COND/EXEC/etc code that is from the script editor, which can be copy and pasted over into the document.

## Further Questions
If you have any further questions, please ask inside the [DK64 Randomizer discord](https://discord.dk64randomizer.com) in the #dev-discussion channel