"""Stores the requirements for each minigame."""

from randomizer.Enums.Minigames import Minigames

minigameRequirements = {
    # Misc. Barrels
    Minigames.BattyBarrelBandit: lambda l: True,
    Minigames.BigBugBash: lambda l: True,
    Minigames.KremlingKosh: lambda l: True,
    Minigames.PerilPathPanic: lambda l: True,
    Minigames.SearchlightSeek: lambda l: True,
    Minigames.TeeteringTurtleTrouble: lambda l: True,
    Minigames.BeaverBother: lambda l: True,
    Minigames.KrazyKongKlamour: lambda l: True,
    Minigames.StashSnatch: lambda l: True,
    Minigames.MinecartMayhem: lambda l: True,
    Minigames.MadMazeMaul: lambda l: True,
    Minigames.StealthySnoop: lambda l: True,
    Minigames.SpeedySwingSortie: lambda l: l.vines,
    Minigames.SpeedySwingSortieTwirl: lambda l: l.vines and l.twirl and l.istiny,
    Minigames.SplishSplashSalvage: lambda l: l.swim,
    Minigames.SplishSplashSalvageVines: lambda l: l.swim and l.vines,
    # Lanky excluded from this game because his gun is too long
    Minigames.BusyBarrelBarrage: lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or
                                           (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    # Helm barrels
    Minigames.DKRambi: lambda l: True,
    Minigames.DKTarget: lambda l: l.isdonkey,
    Minigames.DiddyKremling: lambda l: l.Slam,
    Minigames.DiddyRocketbarrel: lambda l: l.Slam and l.jetpack and l.peanut and l.isdiddy,
    # Supposed to use sprint but can make it without, even with Chunky
    Minigames.LankyMaze: lambda l: True,
    Minigames.LankyShooting: lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape)
                                       (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    Minigames.TinyMushroom: lambda l: True,
    Minigames.TinyPonyTailTwirl: lambda l: l.twirl and l.istiny,
    Minigames.ChunkyHiddenKremling: lambda l: l.hunkyChunky and l.punch and l.ischunky,
    Minigames.ChunkyShooting: lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape)
                                        (l.istiny and l.feather) or (l.ischunky and l.pineapple),
}
