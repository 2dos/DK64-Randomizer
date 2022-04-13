"""Module to handle randomizing kong free order."""
import random

from randomizer.Lists.KongLocations import KongRequirements
from randomizer.MapsAndExits import Maps


def RemoveKong(kong_index):
    """Remove kong from available kongs in other locations."""
    for location in KongRequirements.values():
        if kong_index in location.free:
            location.free.remove(kong_index)


def AssignLocked(kong_index, key):
    """Assign kong to the locked slot of a location."""
    KongRequirements[key].kong_placed = kong_index
    KongRequirements[key].assigned_locked = True
    RemoveKong(kong_index)


def AssignPuzzle(kong_index, key):
    """Assign kong to the puzzle slot of a location."""
    KongRequirements[key].kong_puzzle = kong_index
    KongRequirements[key].assigned_puzzle = True


def Reset():
    """Reset all kong rando variables."""
    for x in KongRequirements.values():
        x.kong_placed = 0
        x.kong_puzzle = 0
        x.assigned_locked = False
        x.assigned_puzzle = False
        x.free = x.base_free.copy()
        x.puzzle_kong = x.base_puzzle_kong.copy()


def writeDefault():
    """Set kong rando information to default/vanilla."""
    KongRequirements[Maps.TrainingGrounds].kong_placed = 0
    KongRequirements[Maps.JungleJapes].kong_placed = 1
    KongRequirements[Maps.JungleJapes].kong_puzzle = 0
    KongRequirements[Maps.AztecLlamaTemple].kong_placed = 2
    KongRequirements[Maps.AztecLlamaTemple].kong_puzzle = 0
    KongRequirements[Maps.AztecTinyTemple].kong_placed = 3
    KongRequirements[Maps.AztecTinyTemple].kong_puzzle = 1
    KongRequirements[Maps.FranticFactory].kong_placed = 4
    KongRequirements[Maps.FranticFactory].kong_puzzle = 2


def ShuffleKongs(settings):
    """Shuffles Kongs around."""
    # Rules:
    # The kong who is being freed cannot be freed by themselves
    # A loop of kongs cannot be created
    success = False
    whole_generation_attempts = 0
    while not success:
        Reset()
        freed_kongs = []
        locked_locations = list(KongRequirements.keys()).copy()
        if Maps.TrainingGrounds in locked_locations:
            locked_locations.remove(Maps.TrainingGrounds)
        # print("Reset")
        # Determine Starting Kong
        starting_kong = random.choice(KongRequirements[Maps.TrainingGrounds].free)
        freed_kongs.append(starting_kong)
        # print(f"Assigned kong {starting_kong} to be locked in {KongRequirements[Maps.TrainingGrounds].name}")
        AssignLocked(starting_kong, Maps.TrainingGrounds)
        AssignPuzzle(5, Maps.TrainingGrounds)
        random.shuffle(locked_locations)
        shuffle_attempts = 0

        while len(locked_locations) > 0:
            selection_array = []
            for x in freed_kongs:
                if x in KongRequirements[locked_locations[0]].puzzle_kong:
                    selection_array.append(x)
            fail = False
            if len(selection_array) > 0:
                proposed_puzzle_kong = random.choice(selection_array)
                list_without_puzzle_kong = KongRequirements[locked_locations[0]].free.copy()
                if proposed_puzzle_kong in list_without_puzzle_kong:
                    list_without_puzzle_kong.remove(proposed_puzzle_kong)
            else:
                fail = True
            if not fail:
                if proposed_puzzle_kong in KongRequirements[locked_locations[0]].puzzle_kong and len(list_without_puzzle_kong) > 0:
                    shuffle_attempts = 0
                    AssignPuzzle(proposed_puzzle_kong, locked_locations[0])
                    # print(f"Assigned kong {proposed_puzzle_kong} to be solve the {KongRequirements[locked_locations[0]].name} puzzle")
                    added_kong = random.choice(list_without_puzzle_kong)
                    AssignLocked(added_kong, locked_locations[0])
                    freed_kongs.append(added_kong)
                    # print(f"Assigned kong {added_kong} to be locked in {KongRequirements[locked_locations[0]].name}")
                    if locked_locations[0] in locked_locations:
                        locked_locations.remove(locked_locations[0])
                    if len(locked_locations) == 0:
                        success = True
                else:
                    fail = True
            if fail:
                if shuffle_attempts < 5:
                    # if len(selection_array) == 0:
                    #     print(f"Kong Placement failed {shuffle_attempts+1}/5. Doesn't possess any kongs which is in puzzle array for {KongRequirements[locked_locations[0]].name}")
                    # else:
                    #     print(f"Kong Placement failed {shuffle_attempts+1}/5. Could not find kong {proposed_puzzle_kong} in puzzle array for {KongRequirements[locked_locations[0]].name}")
                    random.shuffle(locked_locations)
                    shuffle_attempts += 1
                else:
                    success = False
                    # print(f"Kong Generation failed ({whole_generation_attempts+1}/5). Reshuffling")
                    # print(f"Freed: {freed_kongs}")
                    # for x in KongRequirements.values():
                    #     print("")
                    #     print(f"Name: {x.name}")
                    #     print(f"Unlock: {x.free}")
                    #     print(f"Puzzle: {x.puzzle_kong}")
                    #     if x.assigned_locked:
                    #         print(f"Assigned Unlock: {x.kong_placed}")
                    #     if x.assigned_puzzle:
                    #         print(f"Assigned Puzzle: {x.kong_puzzle}")
                    whole_generation_attempts += 1
                    break

        if whole_generation_attempts > 5:
            # print(f"Kong Generation failed ({whole_generation_attempts+1}/5). Writing default")
            writeDefault()
            break

    settings.shuffled_kong_placement = {
        "Training Grounds": {
            "locked": {
                "kong": KongRequirements[Maps.TrainingGrounds].kong_placed,
                "write": 0x141,
            }
        },
        "Jungle Japes": {
            "locked": {
                "kong": KongRequirements[Maps.JungleJapes].kong_placed,
                "write": 0x142,
            },
            "puzzle": {
                "kong": KongRequirements[Maps.JungleJapes].kong_puzzle,
                "write": 0x143,
            },
        },
        "Llama Temple": {
            "locked": {
                "kong": KongRequirements[Maps.AztecLlamaTemple].kong_placed,
                "write": 0x144,
            },
            "puzzle": {
                "kong": KongRequirements[Maps.AztecLlamaTemple].kong_puzzle,
                "write": 0x145,
            },
        },
        "Tiny Temple": {
            "locked": {
                "kong": KongRequirements[Maps.AztecTinyTemple].kong_placed,
                "write": 0x146,
            },
            "puzzle": {
                "kong": KongRequirements[Maps.AztecTinyTemple].kong_puzzle,
                "write": 0x147,
            },
        },
        "Frantic Factory": {
            "locked": {
                "kong": KongRequirements[Maps.FranticFactory].kong_placed,
                "write": 0x148,
            },
            "puzzle": {
                "kong": KongRequirements[Maps.FranticFactory].kong_puzzle,
                "write": 0x149,
            },
        },
    }
