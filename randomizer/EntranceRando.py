"""Randomize Entrances based on shuffled_exit_instructions"""
from ast import Not
from randomizer.Patcher import ROM
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


def randomize_entrances(spoiler:Spoiler):
    if spoiler.shuffled_exit_instructions != None:
        for instruction in spoiler.shuffled_exit_instructions:
            # Update the loading zone data in ROM somehow
            print("Container map: " + instruction.container_map)
            print("Destination map: " + instruction.destination_map)
            print("Destination Exit: " + instruction.destination_exit)
            print("New Map: " + instruction.new_map)
            print("New Exit: " + instruction.new_exit)
