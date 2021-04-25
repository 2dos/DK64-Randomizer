"""Gui and main program for rando DK64."""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import seed
from random import shuffle
import tkinter as tk
import shutil
import random
import sys
import os


def randomize():
    # Prevent users from generating seeds with non-numeric/invalid values
    if str(textboxSeed.get()).isdecimal() is False:
        messagebox.showwarning(
            "DK64 Randomizer",
            "The seed must be a number with 6 digits maximum.",
        )
        return

    for x in vanillaBLocker:
        if (
            str(labels["textboxBL" + str(vanillaBLocker.index(x))].get()).isdecimal() is False
            or int(labels["textboxBL" + str(vanillaBLocker.index(x))].get()) > 200
        ):
            messagebox.showwarning(
                "DK64 Randomizer",
                "B Locker fields must have a value between 0 and 200.",
            )
            return

    for x in vanillaTNS:
        if (
            str(labels["textboxTNS" + str(vanillaTNS.index(x))].get()).isdecimal() is False
            or int(labels["textboxTNS" + str(vanillaTNS.index(x))].get()) < 1
            or int(labels["textboxTNS" + str(vanillaTNS.index(x))].get()) > 500
        ):
            messagebox.showwarning(
                "DK64 Randomizer",
                "Troff n Scoff fields must have a value between 1 and 500.",
            )
            return

    # Arrays for Finalized Setting Values
    finalBLocker = []
    finalTNS = []
    finalNumerical = [0, 1, 2, 3, 4, 5, 6]
    finalKeyFlags = ["0x001A", "0x004A", "0x008A", "0x00A8", "0x00EC", "0x0124", "0x013D"]
    finalLevels = levelEntrances[:]

    # Start Spoiler Log and ASM Generation
    shutil.copy2(os.path.join(sys.path[0], "asmFunctions.asm"), os.path.join(sys.path[0], "settings.asm"))
    log = open(os.path.join(sys.path[0], "spoilerlog.txt"), "w+")
    asm = open(os.path.join(sys.path[0], "settings.asm"), "a+")

    # Write Settings
    log.write("Randomizer Settings" + "\n")
    log.write("-------------------" + "\n")
    log.write("Level Progression Randomized: " + str(varLevelProgression.get()) + "\n")
    if str(varLevelProgression.get()) == "True":
        log.write("Seed: " + str(textboxSeed.get()) + "\n")
    log.write("All Kongs Unlocked: " + str(varKongs.get()) + "\n")
    log.write("All Moves Unlocked: " + str(varMoves.get()) + "\n")
    log.write("Fairy Queen Camera + Shockwave: " + str(varFairyQueen.get()) + "\n")
    log.write("Tag Anywhere Enabled: " + str(varTagAnywhere.get()) + "\n")
    log.write("Shorter Hideout Helm: " + str(varShorterHelm.get()) + "\n")
    log.write("Quality of Life Changes: " + str(varQOL.get()) + "\n")
    log.write("\n")

    # Fill Arrays with chosen game length values
    for x in vanillaBLocker:
        finalBLocker.append(labels["textboxBL" + str(vanillaBLocker.index(x))].get())

    for x in vanillaTNS:
        finalTNS.append(labels["textboxTNS" + str(vanillaTNS.index(x))].get())

    # Shuffle Level Progression
    if str(varLevelProgression.get()) == "True":
        asm.write(".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 1" + "\n" + "\n")  # Run Randomizer in ASM
        seed(textboxSeed.get())
        shuffle(finalLevels)
        log.write("Level Order: " + "\n")
        asm.write(".align" + "\n" + "LevelOrder:" + "\n")

        # Set Level Order in ASM and Spoiler Log
        for x in finalLevels:
            if str(x) == "Jungle Japes":
                finalNumerical[finalLevels.index(x)] = 0
            elif str(x) == "Angry Aztec":
                finalNumerical[finalLevels.index(x)] = 1
            elif str(x) == "Frantic Factory":
                finalNumerical[finalLevels.index(x)] = 2
            elif str(x) == "Gloomy Galleon":
                finalNumerical[finalLevels.index(x)] = 3
            elif str(x) == "Fungi Forest":
                finalNumerical[finalLevels.index(x)] = 4
            elif str(x) == "Crystal Caves":
                finalNumerical[finalLevels.index(x)] = 5
            elif str(x) == "Creepy Castle":
                finalNumerical[finalLevels.index(x)] = 6
            log.write(str(finalLevels.index(x) + 1) + ". " + x + " ")
            log.write("(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, ")
            log.write("Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)")
            log.write("\n")
            asm.write("\t" + ".byte " + str(finalNumerical[finalLevels.index(x)]))
            asm.write("\n")
        log.write("8. Hideout Helm ")
        log.write("(B Locker: " + str(finalBLocker[7]) + " GB)")
        asm.write("\t" + ".byte 7")  # Helm should always be set to position 8 in the array
        asm.write("\n" + "\n")
    else:
        asm.write(".align" + "\n" + "RandoOn:" + "\n" + "\t" + ".byte 0" + "\n" + "\n")  # Dont run Randomizer in ASM

    # Set B Lockers in ASM
    asm.write(".align" + "\n" + "BLockerDefaultAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[7]))  # Helm B Locker always uses last value in level array
    asm.write("\n" + "\n")

    # ANTI CHEAT (set GB amounts to the B Locker post in-game cheat code)
    asm.write(".align" + "\n" + "BLockerCheatAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half " + str(finalBLocker[7]))  # Helm B Locker always uses last value in level array
    asm.write("\n" + "\n")

    # Set Troff n Scoffs in ASM
    asm.write(".align" + "\n" + "TroffNScoffAmounts:" + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalTNS[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\t" + ".half 1")  # Isles TNS should always be set to 1
    asm.write("\n" + "\n")

    # Set Keys
    asm.write(".align" + "\n" + "KeyFlags:" + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Jungle Japes")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Angry Aztec")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Frantic Factory")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Gloomy Galleon")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Fungi Forest")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Crystal Caves")]) + "\n")
    asm.write("\t" + ".half " + str(finalKeyFlags[finalLevels.index("Creepy Castle")]) + "\n")
    asm.write("\n" + "\n")

    # Unlock All Kongs
    asm.write(".align" + "\n" + "KongFlags:" + "\n")
    if str(varKongs.get()) == "True":
        asm.write("\t" + ".half 385" + "\n")  # DK
        asm.write("\t" + ".half 6" + "\n")  # Diddy
        asm.write("\t" + ".half 70" + "\n")  # Lanky
        asm.write("\t" + ".half 66" + "\n")  # Tiny
        asm.write("\t" + ".half 117" + "\n")  # Chunky
    asm.write("\t" + ".half 0" + "\n" + "\n")  # Null Terminator (required)

    # Unlock All Moves
    asm.write(".align" + "\n" + "UnlockAllMoves:" + "\n")
    if str(varMoves.get()) == "True":
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")
    asm.write(
        ".align" + "\n" + "SniperValue:" + "\n" + "\t" + ".byte 0x3" + "\n" + "\n"
    )  # Sniper Scope: 3 = off, 7 = on

    # Unlock Camera + Shockwave
    asm.write(".align" + "\n" + "FairyQueenRewards:" + "\n")
    if str(varFairyQueen.get()) == "True":
        asm.write("\t" + ".half 377" + "\n")  # BFI Camera/Shockwave
    asm.write("\t" + ".half 0" + "\n" + "\n")  # Null Terminator (required)

    # Enable Tag Anywhere
    asm.write(".align" + "\n" + "TagAnywhereOn:" + "\n")
    if str(varTagAnywhere.get()) == "True":
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Shorter Hideout Helm
    asm.write(".align" + "\n" + "ShorterHelmOn:" + "\n")
    if str(varShorterHelm.get()) == "True":
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Quality of Life Changes
    asm.write(".align" + "\n" + "QualityChangesOn:" + "\n")
    if str(varQOL.get()) == "True":
        asm.write("\t" + ".byte 1" + "\n" + "\n")
    else:
        asm.write("\t" + ".byte 0" + "\n" + "\n")

    # Fast Start
    asm.write(".align" + "\n" + "FastStartFlags:" + "\n")
    if str(varQOL.get()) == "True":
        asm.write("\t" + ".half 386" + "\n")  # Dive Barrel
        asm.write("\t" + ".half 387" + "\n")  # Vine Barrel
        asm.write("\t" + ".half 388" + "\n")  # Orange Barrel
        asm.write("\t" + ".half 389" + "\n")  # Barrel Barrel
        asm.write("\t" + ".half 0x1BB" + "\n")  # Japes Boulder Smashed
        asm.write("\t" + ".half 0x186" + "\n")  # Isles Escape CS
        asm.write("\t" + ".half 0x17F" + "\n")  # Training Barrels Spawned
        asm.write("\t" + ".half 0x180" + "\n")  # Cranky has given Sim Slam
        asm.write("\t" + ".half 385" + "\n")  # DK Free
    asm.write("\t" + ".half 0" + "\n")  # Null Terminator (required)

    log.close()
    asm.close()

    messagebox.showinfo(
        "DK64 Randomizer",
        "Game generated successfully!",
    )

    root.destroy()


def randoEnable():
    """Disable the randomizer sub-options if the Level Progression Randomizer is not selected."""
    textboxSeed.config(state=NORMAL if varLevelProgression.get() else DISABLED)
    buttonSeed.config(state=NORMAL if varLevelProgression.get() else DISABLED)
    # Force all kongs for level progression randomizer until logic can be implemented
    checkKongs.select()
    checkKongs.config(state=DISABLED if varLevelProgression.get() else NORMAL)


def randomSeed():
    """Generate a random 6 digit number for a seed ID."""
    genNum = random.randrange(1, 10 ** 6)
    genSixDigits = str(genNum).zfill(6)
    textboxSeed.insert(0, genSixDigits)


def lengthPresetsBL(event):
    """Autofill B Locker options with presets."""
    if str(dropdownLengthBL.get()) == "Vanilla":
        for x in vanillaBLocker:
            labels["textboxBL" + str(vanillaBLocker.index(x))].set(str(vanillaBLocker[vanillaBLocker.index(x)]))
    elif str(dropdownLengthBL.get()) == "Steady":
        for x in steadyBLocker:
            labels["textboxBL" + str(steadyBLocker.index(x))].set(str(steadyBLocker[steadyBLocker.index(x)]))
    elif str(dropdownLengthBL.get()) == "Half":
        for x in halfBLocker:
            labels["textboxBL" + str(halfBLocker.index(x))].set(str(halfBLocker[halfBLocker.index(x)]))
    elif str(dropdownLengthBL.get()) == "Hell":
        for x in hellBLocker:
            labels["textboxBL" + str(hellBLocker.index(x))].set(str(hellBLocker[hellBLocker.index(x)]))


def lengthPresetsTNS(event):
    """Autofill Troff N Scoff options with presets."""
    if str(dropdownLengthTNS.get()) == "Vanilla":
        for x in vanillaTNS:
            labels["textboxTNS" + str(vanillaTNS.index(x))].set(str(vanillaTNS[vanillaTNS.index(x)]))
    elif str(dropdownLengthTNS.get()) == "Steady":
        for x in vanillaTNS:  # Doesn't loop properly if multiple fields are the same value
            labels["textboxTNS" + str(vanillaTNS.index(x))].set(str(steadyTNS[vanillaTNS.index(x)]))
    elif str(dropdownLengthTNS.get()) == "Half":
        for x in halfTNS:
            labels["textboxTNS" + str(halfTNS.index(x))].set(str(halfTNS[halfTNS.index(x)]))
    elif str(dropdownLengthTNS.get()) == "Hell":
        for x in hellTNS:
            labels["textboxTNS" + str(hellTNS.index(x))].set(str(hellTNS[hellTNS.index(x)]))


# Generate the window
root = tk.Tk()
root.title("DK64 Randomizer")
root.geometry("250x450")
root.resizable(False, False)
root.wm_attributes("-topmost", "true")
root.wm_attributes("-toolwindow", "true")
mainTabs = ttk.Notebook(root)

levelsTab = ttk.Frame(mainTabs)
miscellaneousTab = ttk.Frame(mainTabs)
mainTabs.add(levelsTab, text="Level Progression")
mainTabs.add(miscellaneousTab, text="Miscellaneous")
mainTabs.pack(expand=1, fill="both")

rootFrame = Frame(root)
rootFrame.pack()
levelsFrame = Frame(levelsTab)
levelsFrame.pack()
levelsOptionsGrid = Frame(levelsTab)
levelsOptionsGrid.pack()
levelsProgressionGrid = Frame(levelsTab)
levelsProgressionGrid.pack()


class CreateToolTip(object):
    """Create a ToolTip function since TKinter doesn't do this natively.

    Source: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

    Args:
        object (widget): Widget info text.
    """

    def __init__(self, widget, text="widget info"):
        """Create the widget object.

        Args:
            widget (widget): Widget to update.
            text (str, optional): Text of the tool tip. Defaults to "widget info".
        """
        self.waittime = 500  # miliseconds
        self.wraplength = 250  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):  # dead: disable
        """View the tooltip.

        Args:
            event (Event, optional): Event object. Defaults to None.
        """
        self.schedule()

    def leave(self, event=None):  # dead: disable
        """No longer viewing the tooltip.

        Args:
            event (Event, optional): Event object. Defaults to None.
        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """Tie the tooptip to a widget."""
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        """Remove the tooltip from a widget."""
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        """Show the tooltip."""
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_attributes("-topmost", "true")
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        """Hide the tooltip."""
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class SeedEntry(ttk.Entry):
    """Create an Entry function for 6 digit numbers only."""

    def __init__(self, master=None, **kwargs):
        """Create the 6 digit number.

        Args:
            master (Frame, optional): Frame object. Defaults to None.
        """
        self.var = tk.StringVar(master)
        self.var.trace("w", self.validate)
        ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set

    def validate(self, *args):  # dead: disable
        """Validate that the string we have is a valid seed id."""
        value = self.get()
        if not value.isdigit():
            self.set("".join(x for x in value if x.isdigit()))
        if len(value) > 6:
            self.set(value[:6])


class BLEntry(ttk.Entry):
    """Create an Entry function for 3 digit numbers only."""

    def __init__(self, master=None, **kwargs):
        """Create the 6 digit number.

        Args:
            master (Frame, optional): Frame object. Defaults to None.
        """
        self.var = tk.StringVar(master)
        self.var.trace("w", self.validate)
        ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set

    def validate(self, *args):  # dead: disable
        """Validate that the string we have is a valid seed id."""
        value = self.get()
        if not value.isdigit():
            self.set("".join(x for x in value if x.isdigit()))
        if len(value) > 3:
            self.set(value[:3])


class TNSEntry(ttk.Entry):
    """Create an Entry function for 3 digit numbers only."""

    def __init__(self, master=None, **kwargs):
        """Create the 6 digit number.

        Args:
            master (Frame, optional): Frame object. Defaults to None.
        """
        self.var = tk.StringVar(master)
        self.var.trace("w", self.validate)
        ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set

    def validate(self, *args):  # dead: disable
        """Validate that the string we have is a valid seed id."""
        value = self.get()
        if not value.isdigit():
            self.set("".join(x for x in value if x.isdigit()))
        if len(value) > 3:
            self.set(value[:3])


# Interaction Variables
varLevelProgression = BooleanVar()
varKongs = BooleanVar()
varMoves = BooleanVar()
varFairyQueen = BooleanVar()
varTagAnywhere = BooleanVar()
varShorterHelm = BooleanVar()
varQOL = BooleanVar()

# Option Arrays
levelEntrances = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
]

gameLengthOptionsBL = ["Vanilla", "Steady", "Half", "Hell"]
gameLengthOptionsTNS = ["Vanilla", "Steady", "Half", "Hell"]

vanillaBLocker = [1, 5, 15, 30, 50, 65, 80, 100]
steadyBLocker = [1, 10, 20, 30, 40, 50, 60, 75]
halfBLocker = [1, 5, 10, 15, 20, 30, 40, 50]
hellBLocker = [1, 10, 25, 50, 75, 100, 125, 150]

vanillaTNS = [60, 120, 200, 250, 300, 350, 400]
steadyTNS = [150, 150, 150, 150, 150, 150, 150]
halfTNS = [50, 75, 100, 125, 150, 175, 200]
hellTNS = [150, 200, 250, 300, 350, 400, 450]

# Randomize Level Progression Checkbox
checkLevelProgression = Checkbutton(
    levelsFrame,
    text="Randomize Level Progression",
    variable=varLevelProgression,
    command=randoEnable,
)
checkLevelProgression.pack(padx=5, pady=5)
checkLevelProgression.select()
CreateToolTip(
    checkLevelProgression,
    "This option will randomize the level lobby entrances. "
    + "\n"
    + "The level will match the B Locker and Troff n Scoff requirements of the slot that it falls in. "
    + "\n"
    + "Hideout Helm will always be the final level. ",
)

# Seed Textbox
textboxSeed = SeedEntry(levelsOptionsGrid, width=8, justify="center")
textboxSeed.insert(0, str(random.randrange(1, 10 ** 6)).zfill(6))
textboxSeed.grid(row=0, column=0, padx=5, sticky=W)
CreateToolTip(
    textboxSeed,
    "You can either manually enter a 6 digit number or click the button to the right to pick one for you. "
    "This program will generate the game based off the number entered. ",
)

# Pick a Random Seed Number Button
buttonSeed = Button(levelsOptionsGrid, text="Random Seed", command=randomSeed)
buttonSeed.grid(row=0, column=1, padx=5, pady=5)
CreateToolTip(
    buttonSeed,
    "Click this button to randomly generate a 6 digit number to base the seed on.",
)

# Level Progression Textboxes
labelProgression = Label(levelsProgressionGrid, text="Progression")
labelProgression.grid(row=0, column=0, padx=5, pady=5)
labelColumnBL = Label(levelsProgressionGrid, text="B Locker")
labelColumnBL.grid(row=0, column=1, padx=5, pady=5)
labelColumnTNS = Label(levelsProgressionGrid, text="Troff N Scoff")
labelColumnTNS.grid(row=0, column=2, padx=5, pady=5)

labelPresets = Label(levelsProgressionGrid, text="Presets")
labelPresets.grid(row=1, column=0, padx=5, pady=5)
dropdownLengthBL = ttk.Combobox(levelsProgressionGrid, values=gameLengthOptionsBL, width=6, state="readonly")
dropdownLengthBL.grid(row=1, column=1, padx=5, pady=5)
dropdownLengthBL.current(0)
dropdownLengthBL.bind("<<ComboboxSelected>>", lengthPresetsBL)
CreateToolTip(
    dropdownLengthBL,
    "Select the B Locker progression of the game generated. "
    + "\n"
    + "\n"
    + "Vanilla: 1-5-15-30-50-65-80-100 "
    + "\n"
    + "Steady: 1-10-20-30-40-50-60-75 "
    + "\n"
    + "Half: 1-5-10-15-20-30-40-50 "
    + "\n"
    + "Hell: 1-10-25-50-75-100-125-150 ",
)
dropdownLengthTNS = ttk.Combobox(levelsProgressionGrid, values=gameLengthOptionsTNS, width=6, state="readonly")
dropdownLengthTNS.grid(row=1, column=2, padx=5, pady=5)
dropdownLengthTNS.current(0)
dropdownLengthTNS.bind("<<ComboboxSelected>>", lengthPresetsTNS)
CreateToolTip(
    dropdownLengthTNS,
    "Select the Troff n Scoff progression of the game generated. "
    + "\n"
    + "\n"
    + "Vanilla: 60-120-200-250-300-350-400 "
    + "\n"
    + "Steady: All doors set to 150 "
    + "\n"
    + "Half: 50-75-100-125-150-175-200 "
    + "\n"
    + "Hell: 150-200-250-300-350-400-450 ",
)

# Generate B Locker/TNS Input Grid
labels = {}
for x in vanillaBLocker:
    labels["label" + str(vanillaBLocker.index(x))] = Label(
        levelsProgressionGrid, text="Level " + str(vanillaBLocker.index(x) + 1)
    )
    labels["label" + str(vanillaBLocker.index(x))].grid(row=vanillaBLocker.index(x) + 2, column=0, padx=5, pady=5)
    labels["textboxBL" + str(vanillaBLocker.index(x))] = BLEntry(levelsProgressionGrid, width=4, justify="center")
    labels["textboxBL" + str(vanillaBLocker.index(x))].grid(row=vanillaBLocker.index(x) + 2, column=1, padx=5)
    labels["textboxBL" + str(vanillaBLocker.index(x))].insert(0, str(vanillaBLocker[vanillaBLocker.index(x)]))
    CreateToolTip(
        labels["textboxBL" + str(vanillaBLocker.index(x))],
        "You can adjust each individual B Locker amount to any number between 0-200. "
        "Note that you could make it impossible to beat the game glitchless if certain levels are set too high, "
        "as the program does not validate if a game is beatable glitchless with adjusted B Locker settings. "
        "If you are unsure what to adjust the level values to, use the presets dropdown instead.",
    )
    if vanillaBLocker.index(x) < len(vanillaTNS):
        labels["textboxTNS" + str(vanillaBLocker.index(x))] = TNSEntry(levelsProgressionGrid, width=4, justify="center")
        labels["textboxTNS" + str(vanillaBLocker.index(x))].grid(row=vanillaBLocker.index(x) + 2, column=2, padx=5)
        labels["textboxTNS" + str(vanillaBLocker.index(x))].insert(0, str(vanillaTNS[vanillaBLocker.index(x)]))
        CreateToolTip(
            labels["textboxTNS" + str(vanillaBLocker.index(x))],
            "You can adjust each individual Troff n Scoff amount to any number between 1-500. "
            "Note that you could make it impossible to beat the game glitchless if early levels are set too high, "
            "as the program does not validate if a game is beatable glitchless with adjusted Troff n Scoff settings. "
            "If you are unsure what to adjust the level values to, use the presets dropdown instead.",
        )

# Unlock All Kongs Checkbox
checkKongs = Checkbutton(miscellaneousTab, text="Unlock All Kongs", variable=varKongs, state=DISABLED)
checkKongs.pack(padx=5, pady=5)
checkKongs.select()
CreateToolTip(
    checkKongs,
    "This option will make all 5 kongs available from the start without freeing them. "
    + "\n"
    + "The golden bananas awarded when freeing specific kongs still must be collected even with this option on. "
    + "\n"
    + "If using Level Progression Randomizer and playing through glitchless, this option is forced on. ",
)

# Unlock All Moves Checkbox
checkMoves = Checkbutton(miscellaneousTab, text="Unlock All Purchasable Moves", variable=varMoves)
checkMoves.pack(padx=5, pady=5)
CreateToolTip(
    checkMoves,
    "This option will make all moves available from the start without purchasing them. "
    + "\n"
    + "Includes all Cranky, all Candy, and almost all Funky purchasables. "
    + "\n"
    + "Does not include access to JetPac in Cranky; you will still need 15 banana medals. "
    + "\n"
    + "Does not include snipe scope to reduce 1st person camera lag. Is still purchasable. "
    + "\n"
    + "Does not include the shockwave attack from the banana fairy queen. ",
)

# Unlock Fairy Camera and Shockwave Attack
checkFairy = Checkbutton(miscellaneousTab, text="Fairy Camera and Shockwave Attack", variable=varFairyQueen)
checkFairy.pack(padx=5, pady=5)
CreateToolTip(
    checkFairy,
    "This option makes the fairy camera and shockwave attack available from the start. "
    + "\n"
    + "Normally obtainable by visiting the Banana Fairy Queen with Tiny as Mini Monkey. ",
)

# Enable Tag Anywhere Checkbox
checkTagAnywhere = Checkbutton(miscellaneousTab, text="Enable Tag Anywhere", variable=varTagAnywhere)
checkTagAnywhere.pack(padx=5, pady=5)
CreateToolTip(
    checkTagAnywhere,
    "This option will allow you to switch kongs almost anywhere using DPad left or DPad right. "
    + "\n"
    + "You will still need to unlock the kong you want if Unlock All Kongs isn't enabled. "
    + "\n"
    + "You cannot switch kongs in rooms or areas that would otherwise break the puzzle. ",
)

# Shorter Hideout Helm Checkbox
checkShorterHelm = Checkbutton(miscellaneousTab, text="Shorter Hideout Helm", variable=varShorterHelm)
checkShorterHelm.pack(padx=5, pady=5)
checkShorterHelm.select()
CreateToolTip(
    checkShorterHelm,
    "This option will shorten the time it takes to beat Hideout Helm with the following changes: "
    + "\n"
    + "- You will spawn in the Blast o Matic room. "
    + "\n"
    + "- Opens the roman numeral doors to each Kong's room. "
    + "\n"
    + "- The gates in front of the music pads are gone. "
    + "\n"
    + "- The 4 crown door is open. "
    + "\n"
    + "- The Rareware/Nintendo Coin door is open. ",
)

# Quality of Life Changes Checkbox
checkQOL = Checkbutton(miscellaneousTab, text="Quality of Life Changes", variable=varQOL)
checkQOL.pack(padx=5, pady=5)
checkQOL.select()
CreateToolTip(
    checkQOL,
    "This option enables the following quality of life changes to the game: "
    + "\n"
    + "- Removes first time text. "
    + "\n"
    + "- Removes first time boss cutscenes. "
    + "\n"
    + "- Remove cutscenes from the startup sequence. "
    + "\n"
    + "- Story Skip option in the main menu set to On by default. "
    + "\n"
    + "- Fast start: Training Barrels complete, start with Simian Slam, spawn in DK Isles, Japes lobby open. ",
)

# Generate Button
buttonGenerate = Button(rootFrame, text="Generate Game", command=randomize)
buttonGenerate.pack(padx=5, pady=5)

# Initialize the GUI
root.mainloop()
