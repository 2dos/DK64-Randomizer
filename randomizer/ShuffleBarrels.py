"""Module used to handle setting and randomizing bonus barrels."""
import random

import js
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Settings import Settings
from randomizer.Enums.Minigames import Minigames
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Lists.MapsAndExits import Maps


def Reset(barrelLocations):
    """Reset bonus barrel associations."""
    for key in barrelLocations:
        BarrelMetaData[key].minigame = Minigames.NoGame


def ShuffleBarrels(settings: Settings, barrelLocations, minigamePool):
    """Shuffle minigames to different barrels."""
    random.shuffle(barrelLocations)
    random.shuffle(minigamePool)
    while len(barrelLocations) > 0:
        location = barrelLocations.pop()
        # Don't bother shuffling or validating barrel locations which are skipped
        if BarrelMetaData[location].map == Maps.HideoutHelm and settings.helm_barrels == "skip":
            continue
        elif BarrelMetaData[location].map != Maps.HideoutHelm and settings.bonus_barrels == "skip":
            continue
        # Check each remaining minigame to see if placing it will produce a valid world
        success = False
        for minigame in minigamePool:
            BarrelMetaData[location].minigame = minigame
            # Check if banned in Helm and attempted to place in Helm
            if settings.bonus_barrels != "all_beaver_bother":
                if not MinigameRequirements[minigame].helm_enabled and BarrelMetaData[location].map == Maps.HideoutHelm:
                    continue
            # If world is still valid, keep minigame associated there
            if settings.bonus_barrels != "all_beaver_bother":
                if Fill.VerifyWorld(settings):
                    minigamePool.remove(minigame)
                    if MinigameRequirements[minigame].repeat:
                        replacement_index = random.randint(20, len(minigamePool))
                        if replacement_index >= len(minigamePool):
                            minigamePool.append(minigame)
                        else:
                            minigamePool.insert(replacement_index, minigame)
                    success = True
                    break
                else:
                    BarrelMetaData[location].minigame = Minigames.NoGame
            else:
                random.shuffle(minigamePool)
                success = True
                break
        if not success:
            raise Ex.BarrelOutOfMinigames


def BarrelShuffle(settings: Settings):
    """Facilitate shuffling of barrels."""
    # First make master copies of locations and minigames
    barrelLocations = list(BarrelMetaData.keys())
    minigamePool = [x for x in MinigameRequirements.keys() if x != Minigames.NoGame]
    if settings.bonus_barrels == "all_beaver_bother":
        minigamePool = [x for x in MinigameRequirements.keys() if x in (Minigames.BeaverBotherEasy, Minigames.BeaverBotherNormal, Minigames.BeaverBotherHard)]
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
            retries += 1
            js.postMessage("Minigame placement failed. Retrying. Tries: " + str(retries))
