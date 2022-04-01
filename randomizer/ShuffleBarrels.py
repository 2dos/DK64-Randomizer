"""Module used to handle setting and randomizing bonus barrels."""
import random
import js

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Minigames import Minigames
from randomizer.Lists.Minigame import MinigameAssociations, MinigameRequirements, BarrelMetaData
from randomizer.MapsAndExits import Maps


def Reset(barrelLocations):
    """Reset bonus barrel associations."""
    for key in barrelLocations:
        MinigameAssociations[key] = Minigames.NoGame


def ShuffleBarrels(settings, barrelLocations, minigamePool):
    """Shuffle minigames to different barrels."""
    random.shuffle(barrelLocations)
    random.shuffle(minigamePool)
    while len(barrelLocations) > 0:
        location = barrelLocations.pop()
        # Check each remaining minigame to see if placing it will produce a valid world
        success = False
        for minigame in minigamePool:
            MinigameAssociations[location] = minigame
            enabled_for_map = True
            if not MinigameRequirements[minigame].assign:
                enabled_for_map = False
                minigamePool.remove(minigame)
            # Check if banned in Helm and attempted to place in Helm
            if not MinigameRequirements[minigame].helm_enabled and BarrelMetaData[location].map == Maps.HideoutHelm:
                enabled_for_map = False
            # If world is still valid, keep minigame associated there
            if Fill.VerifyWorld(settings) and enabled_for_map:
                minigamePool.remove(minigame)
                if MinigameRequirements[minigame].repeat:
                    replacement_index = random.randint(0, len(minigamePool))
                    if replacement_index >= len(minigamePool):
                        minigamePool.append(minigame)
                    else:
                        minigamePool.insert(replacement_index, minigame)
                success = True
                break
            else:
                MinigameAssociations[location] = Minigames.NoGame
        if not success:
            raise Ex.BarrelOutOfMinigames


def BarrelShuffle(settings):
    """Facilitate shuffling of barrels."""
    # First make master copies of locations and minigames
    barrelLocations = [x for x in BarrelMetaData.keys()]
    minigamePool = [x for x in MinigameRequirements.keys()]
    retries = 0
    while True:
        try:
            # Shuffle barrels
            Reset(barrelLocations)
            ShuffleBarrels(settings, barrelLocations.copy(), minigamePool.copy())
            # Verify world by assuring all locations are still reachable
            if not Fill.VerifyWorld(settings):
                raise Ex.BarrelPlacementException
            return
        except Ex.BarrelPlacementException:
            if retries == 5:
                js.postMessage("Minigame placement failed, out of retries.")
                raise Ex.BarrelAttemptCountExceeded
            else:
                retries += 1
                js.postMessage("Minigame placement failed. Retrying. Tries: " + str(retries))
