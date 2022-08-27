"""Module used to handle setting and randomizing bonus barrels."""
import random

import js
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Minigames import Minigames
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Settings import Settings


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
        helm = False
        for minigame in minigamePool:
            # Check if any minigames can be placed in helm
            if MinigameRequirements[minigame].helm_enabled:
                helm = True
        for minigame in minigamePool:
            BarrelMetaData[location].minigame = minigame
            # If there is a minigame that can be placed in Helm, skip banned minigames, otherwise continue as normal
            if not MinigameRequirements[minigame].helm_enabled and BarrelMetaData[location].map == Maps.HideoutHelm and helm is True:
                continue
            # If world is still valid, keep minigame associated there
            if settings.bonus_barrels != "selected":
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
                if Fill.VerifyWorld(settings):
                    minigamePool.remove(minigame)
                    if MinigameRequirements[minigame].repeat:
                        replacement_index = random.randint(int(len(minigamePool) / 2), len(minigamePool))
                        if replacement_index >= len(minigamePool):
                            minigamePool.append(minigame)
                        else:
                            minigamePool.insert(replacement_index, minigame)
                    success = True
                    break
                else:
                    BarrelMetaData[location].minigame = Minigames.NoGame
        if not success:
            raise Ex.BarrelOutOfMinigames


def BarrelShuffle(settings: Settings):
    """Facilitate shuffling of barrels."""
    # First make master copies of locations and minigames
    barrelLocations = list(BarrelMetaData.keys())
    if settings.bonus_barrels == "selected":
        minigame_dict = {
            "batty_barrel_bandit": [Minigames.BattyBarrelBanditVEasy, Minigames.BattyBarrelBanditEasy, Minigames.BattyBarrelBanditNormal, Minigames.BattyBarrelBanditHard],
            "big_bug_bash": [Minigames.BigBugBashVEasy, Minigames.BigBugBashEasy, Minigames.BigBugBashNormal, Minigames.BigBugBashHard],
            "busy_barrel_barrage": [Minigames.BusyBarrelBarrageEasy, Minigames.BusyBarrelBarrageNormal, Minigames.BusyBarrelBarrageHard],
            "mad_maze_maul": [Minigames.MadMazeMaulEasy, Minigames.MadMazeMaulNormal, Minigames.MadMazeMaulHard, Minigames.MadMazeMaulInsane],
            "minecart_mayhem": [Minigames.MinecartMayhemEasy, Minigames.MinecartMayhemNormal, Minigames.MinecartMayhemHard],
            "beaver_bother": [Minigames.BeaverBotherEasy, Minigames.BeaverBotherNormal, Minigames.BeaverBotherHard],
            "teetering_turtle_trouble": [Minigames.TeeteringTurtleTroubleVEasy, Minigames.TeeteringTurtleTroubleEasy, Minigames.TeeteringTurtleTroubleNormal, Minigames.TeeteringTurtleTroubleHard],
            "stealthy_snoop": [Minigames.StealthySnoopVEasy, Minigames.StealthySnoopEasy, Minigames.StealthySnoopNormal, Minigames.StealthySnoopHard],
            "stash_snatch": [Minigames.StashSnatchEasy, Minigames.StashSnatchNormal, Minigames.StashSnatchHard, Minigames.StashSnatchInsane],
            "splish_splash_salvage": [Minigames.SplishSplashSalvageEasy, Minigames.SplishSplashSalvageNormal, Minigames.SplishSplashSalvageHard],
            "speedy_swing_sortie": [Minigames.SpeedySwingSortieEasy, Minigames.SpeedySwingSortieNormal, Minigames.SpeedySwingSortieHard],
            "krazy_kong_klamour": [Minigames.KrazyKongKlamourEasy, Minigames.KrazyKongKlamourNormal, Minigames.KrazyKongKlamourHard, Minigames.KrazyKongKlamourInsane],
            "searchlight_seek": [Minigames.SearchlightSeekVEasy, Minigames.SearchlightSeekEasy, Minigames.SearchlightSeekNormal, Minigames.SearchlightSeekHard],
            "kremling_kosh": [Minigames.KremlingKoshVEasy, Minigames.KremlingKoshEasy, Minigames.KremlingKoshNormal, Minigames.KremlingKoshHard],
            "peril_path_panic": [Minigames.PerilPathPanicVEasy, Minigames.PerilPathPanicEasy, Minigames.PerilPathPanicNormal, Minigames.PerilPathPanicHard],
            "helm_minigames": [
                Minigames.DonkeyRambi,
                Minigames.DonkeyTarget,
                Minigames.DiddyKremling,
                Minigames.DiddyRocketbarrel,
                Minigames.LankyMaze,
                Minigames.LankyShooting,
                Minigames.TinyMushroom,
                Minigames.TinyPonyTailTwirl,
                Minigames.ChunkyHiddenKremling,
                Minigames.ChunkyShooting,
            ],
        }
        minigamePool = []
    else:
        minigamePool = [x for x in MinigameRequirements.keys() if x != Minigames.NoGame]
    if settings.bonus_barrels == "selected":
        for name, value in minigame_dict.items():
            if name in settings.minigames_list_selected:
                minigamePool.extend([x for x in MinigameRequirements.keys() if x in value])
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
