"""Module used to handle setting and randomizing bonus barrels."""
import random

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Minigames import Minigames
from randomizer.Lists.Minigame import MinigameAssociations


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
        for minigame in minigamePool:
            MinigameAssociations[location] = minigame
            # If world is still valid, keep minigame associated there
            if Fill.VerifyWorld(settings):
                minigamePool.remove(minigame)
                break
            else:
                MinigameAssociations[location] = Minigames.NoGame


def BarrelShuffle(settings):
    """Facilitate shuffling of barrels."""
    # First make master copies of locations and minigames
    barrelLocations = [x for x in MinigameAssociations.keys()]
    minigamePool = [x for x in MinigameAssociations.values()]
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
                print("Minigame placement failed, out of retries.")
                raise Ex.BarrelAttemptCountExceeded
            else:
                retries += 1
                print("Minigame placement failed. Retrying. Tries: " + str(retries))
