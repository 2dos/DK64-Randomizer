from tkinter import *
from tkinter import ttk
import tkinter as tk
import random

#Command to run when clicking the Randomize Button
def randomize():
    #Arrays for Finalized Setting Values
    finalBLocker = []
    finalTNS = []
    finalLevels = levelEntrances[:]

    #Start Spoiler Log Generation
    log = open("spoilerlog.txt","w+")

    #Write Settings to Spoiler Log
    log.write("Randomizer Settings" + "\n")
    log.write("-------------------" + "\n")
    log.write("Level Progression Randomized: " + str(varLevelProgression.get()) + "\n")
    if str(varLevelProgression.get()) == "True":
        log.write("Game Length: " + str(dropdownLength.get()) + "\n")
    log.write("All Kongs Unlocked: " + str(varKongs.get()) + "\n")
    log.write("All Moves Unlocked: " + str(varMoves.get()) + "\n")
    log.write("Tag Anywhere Enabled: " + str(varTagAnywhere.get()) + "\n")
    log.write("Shorter Hideout Helm: " + str(varShorterHelm.get()) + "\n")
    log.write("Quality of Life Changes: " + str(varQOL.get()) + "\n")
    log.write("\n")

    #Fill Arrays with chosen game length values
    if str(dropdownLength.get()) == "Vanilla":
        finalBLocker = vanillaBLocker[:]
        finalTNS = vanillaTNS[:]
    elif str(dropdownLength.get()) == "Shorter":
        finalBLocker = shorterBLocker[:]
        finalTNS = shorterTNS[:]

    #Shuffle Level Progression and Write to Spoiler Log
    if str(varLevelProgression.get()) == "True":
        random.shuffle(finalLevels)
        log.write("Level Order: " + "\n")
        for x in finalLevels:
            log.write(str(finalLevels.index(x) + 1) + ". " + x + " ")
            log.write("(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, ")
            log.write("Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)")
            log.write("\n")
        log.write("8. Hideout Helm ")
        log.write("(B Locker: " + str(finalBLocker[7]) + " GB)")
    log.close()
    root.destroy()

#Command to disable the randomizer length options if the Level Progression Randomizer is not selected
def randoEnable():
    dropdownLength.config(state="readonly" if varLevelProgression.get() else DISABLED)

#Generate the window
root = tk.Tk()
root.title("DK64 Level Progression Randomizer")
root.geometry("250x280")
root.resizable(False, False)
root.wm_attributes('-topmost', 'true')
root.wm_attributes('-toolwindow', 'true')
frame = Frame(root)
frame.pack()
 
#Interaction Variables
varLevelProgression = BooleanVar()
varKongs = BooleanVar()
varMoves = BooleanVar()
varTagAnywhere = BooleanVar()
varShorterHelm = BooleanVar()
varQOL = BooleanVar()

#Option Arrays
gameLengthOptions = ["Vanilla", "Shorter"]

levelEntrances = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle"]

vanillaBLocker= [1, 5, 15, 30, 50, 65, 80, 100]
vanillaTNS = [60, 120, 200, 250, 300, 350, 400]

shorterBLocker = [1, 3, 10, 20, 35, 50, 65, 80]
shorterTNS = [50, 75, 100, 125, 150, 200, 250]
 
#Randomize Level Progression Checkbox
checkLevelProgression = Checkbutton(frame, text = "Randomize Level Progression", variable = varLevelProgression, command = randoEnable)
checkLevelProgression.pack(padx = 5, pady = 5)
checkLevelProgression.select()

#Game Length Dropdown
dropdownLength = ttk.Combobox(frame, values = gameLengthOptions, width = 10, state = "readonly")
dropdownLength.pack(padx = 5, pady = 5)
dropdownLength.current(0)
 
#Unlock All Kongs Checkbox
checkKongs = Checkbutton(frame, text = "Unlock All Kongs", variable = varKongs)
checkKongs.pack(padx = 5, pady = 5)
checkKongs.select()

#Unlock All Moves Checkbox
checkMoves = Checkbutton(frame, text = "Unlock All Moves", variable = varMoves)
checkMoves.pack(padx = 5, pady = 5)

#Enable Tag Anywhere Checkbox
checkTagAnywhere = Checkbutton(frame, text = "Enable Tag Anywhere", variable = varTagAnywhere)
checkTagAnywhere.pack(padx = 5, pady = 5)

#Shorter Hideout Helm Checkbox
checkShorterHelm = Checkbutton(frame, text = "Shorter Hideout Helm", variable = varShorterHelm)
checkShorterHelm.pack(padx = 5, pady = 5)

#Quality of Life Changes Checkbox
checkQOL = Checkbutton(frame, text = "Quality of Life Changes", variable = varQOL)
checkQOL.pack(padx = 5, pady = 5)
 
#Randomize Button
buttonRandomize = Button(frame, text = "Randomize", command = randomize)
buttonRandomize.pack(padx = 5, pady = 5)

#Initialize the GUI
root.mainloop()
