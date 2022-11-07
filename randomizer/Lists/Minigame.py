"""Stores the requirements for each minigame."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Lists.MapsAndExits import Maps


class Minigame:
    """Class which stores name and logic for a minigame."""

    def __init__(self, *, name="No Game", group="No Group", map_id=0, helm_enabled=True, can_repeat=True, difficulty_lvl=0, logic=0):
        """Initialize with given parameters."""
        self.name = name
        self.map = map_id
        self.helm_enabled = helm_enabled
        self.repeat = can_repeat
        self.difficulty = difficulty_lvl
        self.logic = logic
        self.group = group


HelmMinigameLocations = [
    Locations.HelmDonkey1,
    Locations.HelmDonkey2,
    Locations.HelmDiddy1,
    Locations.HelmDiddy2,
    Locations.HelmLanky1,
    Locations.HelmLanky2,
    Locations.HelmTiny1,
    Locations.HelmTiny2,
    Locations.HelmChunky1,
    Locations.HelmChunky2,
]

MinigameRequirements = {
    Minigames.NoGame: Minigame(name="No Game", group="No Group", helm_enabled=False, logic=lambda l: True),
    # Batty Barrel Bandit
    Minigames.BattyBarrelBanditVEasy: Minigame(name="Batty Barrel Bandit (Slow)", group="Batty Barrel Bandit", map_id=Maps.BattyBarrelBanditVEasy, logic=lambda l: True),
    Minigames.BattyBarrelBanditEasy: Minigame(name="Batty Barrel Bandit (Progressive Speed)", group="Batty Barrel Bandit", map_id=Maps.BattyBarrelBanditEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.BattyBarrelBanditNormal: Minigame(
        name="Batty Barrel Bandit (Medium)", group="Batty Barrel Bandit", map_id=Maps.BattyBarrelBanditNormal, helm_enabled=False, difficulty_lvl=2, logic=lambda l: True
    ),
    Minigames.BattyBarrelBanditHard: Minigame(
        name="Batty Barrel Bandit (Fast)", group="Batty Barrel Bandit", map_id=Maps.BattyBarrelBanditHard, helm_enabled=False, difficulty_lvl=3, logic=lambda l: True
    ),
    # Big Bug Bash
    Minigames.BigBugBashVEasy: Minigame(name="Big Bug Bash (4 Bugs)", group="Big Bug Bash", map_id=Maps.BigBugBashVEasy, logic=lambda l: True),
    Minigames.BigBugBashEasy: Minigame(name="Big Bug Bash (6 Bugs)", group="Big Bug Bash", map_id=Maps.BigBugBashEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.BigBugBashNormal: Minigame(name="Big Bug Bash (8 Bugs)", group="Big Bug Bash", map_id=Maps.BigBugBashNormal, difficulty_lvl=2, logic=lambda l: True),
    Minigames.BigBugBashHard: Minigame(name="Big Bug Bash (10 Bugs)", group="Big Bug Bash", map_id=Maps.BigBugBashHard, difficulty_lvl=3, logic=lambda l: True),
    # Busy Barrel Barrage - Lanky excluded because gun is too long
    Minigames.BusyBarrelBarrageEasy: Minigame(
        name="Busy Barrel Barrage (45 seconds, Slow Respawn)",
        group="Busy Barrel Barrage",
        map_id=Maps.BusyBarrelBarrageEasy,
        logic=lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    ),
    Minigames.BusyBarrelBarrageNormal: Minigame(
        name="Busy Barrel Barrage (45 seconds, Medium Respawn)",
        group="Busy Barrel Barrage",
        map_id=Maps.BusyBarrelBarrageNormal,
        difficulty_lvl=1,
        logic=lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    ),
    Minigames.BusyBarrelBarrageHard: Minigame(
        name="Busy Barrel Barrage (60 seconds, Random Spawns)",
        group="Busy Barrel Barrage",
        map_id=Maps.BusyBarrelBarrageHard,
        difficulty_lvl=2,
        logic=lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    ),
    # Mad Maze Maul - 120/11 requires shockwave to beat, as such, banned from Helm
    Minigames.MadMazeMaulEasy: Minigame(name="Mad Maze Maul (60 seconds, 5 enemies)", group="Mad Maze Maul", map_id=Maps.MadMazeMaulEasy, logic=lambda l: True),
    Minigames.MadMazeMaulNormal: Minigame(name="Mad Maze Maul (60 seconds, 7 enemies)", group="Mad Maze Maul", map_id=Maps.MadMazeMaulNormal, difficulty_lvl=1, logic=lambda l: True),
    Minigames.MadMazeMaulHard: Minigame(
        name="Mad Maze Maul (120 seconds, 11 enemies)",
        group="Mad Maze Maul",
        map_id=Maps.MadMazeMaulHard,
        helm_enabled=False,
        difficulty_lvl=2,
        logic=lambda l: (l.shockwave or l.oranges) and l.HasGun(Kongs.any),
    ),
    Minigames.MadMazeMaulInsane: Minigame(name="Mad Maze Maul (125 seconds, 10 enemies)", group="Mad Maze Maul", map_id=Maps.MadMazeMaulInsane, difficulty_lvl=3, logic=lambda l: l.HasGun(Kongs.any)),
    # Minecart Mayhem - Higher two difficulties are too hard for those who don't have a guide to do in Helm
    Minigames.MinecartMayhemEasy: Minigame(name="Minecart Mayhem (30 seconds, 1 TNT)", group="Minecart Mayhem", map_id=Maps.MinecartMayhemEasy, logic=lambda l: True),
    Minigames.MinecartMayhemNormal: Minigame(
        name="Minecart Mayhem (45 seconds, 2 TNT)", group="Minecart Mayhem", map_id=Maps.MinecartMayhemNormal, helm_enabled=False, difficulty_lvl=1, logic=lambda l: True
    ),
    Minigames.MinecartMayhemHard: Minigame(
        name="Minecart Mayhem (60 seconds, 2 TNT)", group="Minecart Mayhem", map_id=Maps.MinecartMayhemHard, helm_enabled=False, difficulty_lvl=2, logic=lambda l: True
    ),
    # Beaver Bother - Banned from Helm due to widespread difficulty
    Minigames.BeaverBotherEasy: Minigame(name="Beaver Bother (12 Beavers)", group="Beaver Bother", map_id=Maps.BeaverBotherEasy, helm_enabled=False, logic=lambda l: True),
    Minigames.BeaverBotherNormal: Minigame(name="Beaver Bother (15 Slow Beavers)", group="Beaver Bother", map_id=Maps.BeaverBotherNormal, helm_enabled=False, difficulty_lvl=1, logic=lambda l: True),
    Minigames.BeaverBotherHard: Minigame(name="Beaver Bother (15 Fast Beavers)", group="Beaver Bother", map_id=Maps.BeaverBotherHard, helm_enabled=False, difficulty_lvl=2, logic=lambda l: True),
    # Teetering Turtle Trouble
    Minigames.TeeteringTurtleTroubleVEasy: Minigame(
        name="Teetering Turtle Trouble (45 seconds, 2.5% help chance)", group="Teetering Turtle Trouble", map_id=Maps.TeeteringTurtleTroubleVEasy, logic=lambda l: True
    ),
    Minigames.TeeteringTurtleTroubleEasy: Minigame(
        name="Teetering Turtle Trouble (45 seconds, 4% help chance)", group="Teetering Turtle Trouble", map_id=Maps.TeeteringTurtleTroubleEasy, difficulty_lvl=1, logic=lambda l: True
    ),
    Minigames.TeeteringTurtleTroubleNormal: Minigame(
        name="Teetering Turtle Trouble (60 seconds, 5% help chance)", group="Teetering Turtle Trouble", map_id=Maps.TeeteringTurtleTroubleNormal, difficulty_lvl=2, logic=lambda l: True
    ),
    Minigames.TeeteringTurtleTroubleHard: Minigame(
        name="Teetering Turtle Trouble (60 seconds, 7.5% help chance)", group="Teetering Turtle Trouble", map_id=Maps.TeeteringTurtleTroubleHard, difficulty_lvl=3, logic=lambda l: True
    ),
    # Stealthy Snoop
    Minigames.StealthySnoopVEasy: Minigame(name="Stealthy Snoop (50 seconds)", group="Stealthy Snoop", map_id=Maps.StealthySnoopVEasy, logic=lambda l: True),
    Minigames.StealthySnoopEasy: Minigame(name="Stealthy Snoop (60 seconds)", group="Stealthy Snoop", map_id=Maps.StealthySnoopEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.StealthySnoopNormal: Minigame(name="Stealthy Snoop (70 seconds)", group="Stealthy Snoop", map_id=Maps.StealthySnoopNormal, difficulty_lvl=2, logic=lambda l: True),
    Minigames.StealthySnoopHard: Minigame(name="Stealthy Snoop (90 seconds)", group="Stealthy Snoop", map_id=Maps.StealthySnoopHard, difficulty_lvl=3, logic=lambda l: True),
    # Stash Snatch - SSnatch Hybrid determined too difficulty for Helm
    Minigames.StashSnatchEasy: Minigame(name="Stash Snatch (60 seconds, 6 coins)", group="Stash Snatch", map_id=Maps.StashSnatchEasy, logic=lambda l: True),
    Minigames.StashSnatchNormal: Minigame(name="Stash Snatch (60 seconds, 16 coins)", group="Stash Snatch", map_id=Maps.StashSnatchNormal, difficulty_lvl=1, logic=lambda l: True),
    Minigames.StashSnatchHard: Minigame(
        name="Stash Snatch (120 seconds, 4 coins, Stash Snatch Hybrid)", group="Stash Snatch", map_id=Maps.StashSnatchHard, helm_enabled=False, difficulty_lvl=2, logic=lambda l: True
    ),
    Minigames.StashSnatchInsane: Minigame(name="Stash Snatch (120 seconds, 33 coins)", group="Stash Snatch", map_id=Maps.StashSnatchInsane, difficulty_lvl=3, logic=lambda l: True),
    # Splish Splash Salvage
    Minigames.SplishSplashSalvageEasy: Minigame(name="Splish Splash Salvage (8 coins)", group="Splish Splash Salvage", map_id=Maps.SplishSplashSalvageEasy, logic=lambda l: l.swim and l.vines),
    Minigames.SplishSplashSalvageNormal: Minigame(
        name="Splish Splash Salvage (10 coins)", group="Splish Splash Salvage", map_id=Maps.SplishSplashSalvageNormal, difficulty_lvl=1, logic=lambda l: l.swim
    ),
    Minigames.SplishSplashSalvageHard: Minigame(name="Splish Splash Salvage (15 coins)", group="Splish Splash Salvage", map_id=Maps.SplishSplashSalvageHard, difficulty_lvl=2, logic=lambda l: l.swim),
    # Speedy Swing Sortie
    Minigames.SpeedySwingSortieEasy: Minigame(name="Speedy Swing Sortie (40 seconds, 9 coins)", group="Speedy Swing Sortie", map_id=Maps.SpeedySwingSortieEasy, logic=lambda l: l.vines),
    Minigames.SpeedySwingSortieNormal: Minigame(
        name="Speedy Swing Sortie (45 seconds, 14 coins)", group="Speedy Swing Sortie", map_id=Maps.SpeedySwingSortieNormal, difficulty_lvl=1, logic=lambda l: l.vines and l.twirl and l.istiny
    ),
    Minigames.SpeedySwingSortieHard: Minigame(
        name="Speedy Swing Sortie (60 seconds, 6 coins)", group="Speedy Swing Sortie", map_id=Maps.SpeedySwingSortieHard, helm_enabled=False, difficulty_lvl=2, logic=lambda l: l.vines
    ),
    # Krazy Kong Klamour - Fast flicker games banned from Helm because Wii U semi-requires pause buffer to hit Bananas. Not expecting users to know this trick
    Minigames.KrazyKongKlamourEasy: Minigame(name="Krazy Kong Klamour (10 Bananas, Slow Flicker)", group="Krazy Kong Klamour", map_id=Maps.KrazyKongKlamourEasy, logic=lambda l: True),
    Minigames.KrazyKongKlamourNormal: Minigame(
        name="Krazy Kong Klamour (15 Bananas, Slow Flicker)", group="Krazy Kong Klamour", map_id=Maps.KrazyKongKlamourNormal, difficulty_lvl=1, logic=lambda l: True
    ),
    Minigames.KrazyKongKlamourHard: Minigame(
        name="Krazy Kong Klamour (5 Bananas, Fast Flicker)", group="Krazy Kong Klamour", map_id=Maps.KrazyKongKlamourHard, helm_enabled=False, difficulty_lvl=2, logic=lambda l: True
    ),
    Minigames.KrazyKongKlamourInsane: Minigame(
        name="Krazy Kong Klamour (10 Bananas, Fast Flicker)", group="Krazy Kong Klamour", map_id=Maps.KrazyKongKlamourInsane, helm_enabled=False, difficulty_lvl=3, logic=lambda l: True
    ),
    # Searchlight Seek
    Minigames.SearchlightSeekVEasy: Minigame(name="Searchlight Seek (4 Klaptraps)", group="Searchlight Seek", map_id=Maps.SearchlightSeekVEasy, logic=lambda l: True),
    Minigames.SearchlightSeekEasy: Minigame(name="Searchlight Seek (6 Klaptraps)", group="Searchlight Seek", map_id=Maps.SearchlightSeekEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.SearchlightSeekNormal: Minigame(name="Searchlight Seek (8 Klaptraps)", group="Searchlight Seek", map_id=Maps.SearchlightSeekNormal, difficulty_lvl=2, logic=lambda l: True),
    Minigames.SearchlightSeekHard: Minigame(name="Searchlight Seek (10 Klaptraps)", group="Searchlight Seek", map_id=Maps.SearchlightSeekHard, difficulty_lvl=3, logic=lambda l: True),
    # Kremling Kosh
    Minigames.KremlingKoshVEasy: Minigame(name="Kremling Kosh (18 points)", group="Kremling Kosh", map_id=Maps.KremlingKoshVEasy, logic=lambda l: True),
    Minigames.KremlingKoshEasy: Minigame(name="Kremling Kosh (22 points)", group="Kremling Kosh", map_id=Maps.KremlingKoshEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.KremlingKoshNormal: Minigame(name="Kremling Kosh (25 points)", group="Kremling Kosh", map_id=Maps.KremlingKoshNormal, difficulty_lvl=2, logic=lambda l: True),
    Minigames.KremlingKoshHard: Minigame(name="Kremling Kosh (28 points)", group="Kremling Kosh", map_id=Maps.KremlingKoshHard, difficulty_lvl=3, logic=lambda l: True),
    # Peril Path Panic
    Minigames.PerilPathPanicVEasy: Minigame(name="Peril Path Panic (6 points)", group="Peril Path Panic", map_id=Maps.PerilPathPanicVEasy, logic=lambda l: True),
    Minigames.PerilPathPanicEasy: Minigame(name="Peril Path Panic (8 points)", group="Peril Path Panic", map_id=Maps.PerilPathPanicEasy, difficulty_lvl=1, logic=lambda l: True),
    Minigames.PerilPathPanicNormal: Minigame(name="Peril Path Panic (10 points)", group="Peril Path Panic", map_id=Maps.PerilPathPanicNormal, difficulty_lvl=2, logic=lambda l: True),
    Minigames.PerilPathPanicHard: Minigame(name="Peril Path Panic (12 points)", group="Peril Path Panic", map_id=Maps.PerilPathPanicHard, difficulty_lvl=3, logic=lambda l: True),
    # Helm barrels
    Minigames.DonkeyRambi: Minigame(name="Hideout Helm: DK Rambi", group="Helm Minigames", map_id=Maps.HelmBarrelDKRambi, can_repeat=True, logic=lambda l: True),
    Minigames.DonkeyTarget: Minigame(name="Hideout Helm: DK Targets", group="Helm Minigames", map_id=Maps.HelmBarrelDKTarget, can_repeat=True, logic=lambda l: l.isdonkey),
    Minigames.DiddyKremling: Minigame(name="Hideout Helm: Diddy Kremlings", group="Helm Minigames", map_id=Maps.HelmBarrelDiddyKremling, can_repeat=True, logic=lambda l: l.Slam),
    Minigames.DiddyRocketbarrel: Minigame(
        name="Hideout Helm: Diddy Rocketbarrel", group="Helm Minigames", map_id=Maps.HelmBarrelDiddyRocketbarrel, can_repeat=True, logic=lambda l: l.Slam and l.jetpack and l.peanut and l.isdiddy
    ),
    # Supposed to use sprint but can make it without), even with Chunky
    Minigames.LankyMaze: Minigame(name="Hideout Helm: Lanky Maze", group="Helm Minigames", map_id=Maps.HelmBarrelLankyMaze, can_repeat=True, logic=lambda l: True),
    Minigames.LankyShooting: Minigame(
        name="Hideout Helm: Lanky Shooting",
        group="Helm Minigames",
        map_id=Maps.HelmBarrelLankyShooting,
        can_repeat=True,
        logic=lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    ),
    Minigames.TinyMushroom: Minigame(name="Hideout Helm: Tiny Mushroom", group="Helm Minigames", map_id=Maps.HelmBarrelTinyMush, helm_enabled=True, can_repeat=True, logic=lambda l: True),
    Minigames.TinyPonyTailTwirl: Minigame(
        name="Hideout Helm: Tiny Ponytail Twirl", group="Helm Minigames", map_id=Maps.HelmBarrelTinyPTT, helm_enabled=True, can_repeat=True, logic=lambda l: l.twirl and l.istiny
    ),
    Minigames.ChunkyHiddenKremling: Minigame(
        name="Hideout Helm: Chunky Hidden Kremling",
        group="Helm Minigames",
        map_id=Maps.HelmBarrelChunkyHidden,
        helm_enabled=True,
        can_repeat=True,
        logic=lambda l: l.hunkyChunky and l.punch and l.ischunky,
    ),
    Minigames.ChunkyShooting: Minigame(
        name="Hideout Helm: Chunky Shooting",
        group="Helm Minigames",
        map_id=Maps.HelmBarrelChunkyShooting,
        can_repeat=True,
        logic=lambda l: (l.scope or l.homing or l.settings.hard_shooting)
        and ((l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    ),
}

MinigameSelector = []
result = []
for minigame in MinigameRequirements.values():
    name = minigame.group
    if name not in result and name != "No Group":
        MinigameSelector.append({"name": name, "value": name.lower().replace(" ", "_"), "tooltip": ""})
        result.append(name)


class MinigameLocationData:
    """Class which stores container map and barrel id for a minigame barrel."""

    def __init__(self, map_id, barrel_id, minigame):
        """Initialize with given parameters."""
        self.map = map_id
        self.barrel_id = barrel_id
        self.minigame = minigame


BarrelMetaData = {
    Locations.IslesDiddySnidesLobby: MinigameLocationData(Maps.IslesSnideRoom, 2, Minigames.BattyBarrelBanditNormal),
    Locations.IslesTinyAztecLobby: MinigameLocationData(Maps.AngryAztecLobby, 1, Minigames.BigBugBashNormal),
    Locations.IslesChunkyHelmLobby: MinigameLocationData(Maps.HideoutHelmLobby, 10, Minigames.KremlingKoshHard),
    Locations.IslesDiddySummit: MinigameLocationData(Maps.Isles, 11, Minigames.PerilPathPanicNormal),
    Locations.IslesLankyCastleLobby: MinigameLocationData(Maps.CreepyCastleLobby, 2, Minigames.SearchlightSeekHard),
    Locations.JapesLankyGrapeGate: MinigameLocationData(Maps.JungleJapes, 32, Minigames.MadMazeMaulEasy),
    Locations.JapesChunkyGiantBonusBarrel: MinigameLocationData(Maps.JungleJapes, 33, Minigames.MinecartMayhemEasy),
    Locations.JapesLankySlope: MinigameLocationData(Maps.JungleJapes, 34, Minigames.SpeedySwingSortieEasy),
    Locations.JapesTinyFeatherGateBarrel: MinigameLocationData(Maps.JungleJapes, 31, Minigames.SplishSplashSalvageNormal),
    Locations.AztecLanky5DoorTemple: MinigameLocationData(Maps.AztecLanky5DTemple, 0, Minigames.BigBugBashVEasy),
    Locations.AztecChunkyCagedBarrel: MinigameLocationData(Maps.AngryAztec, 35, Minigames.BusyBarrelBarrageEasy),
    Locations.AztecChunky5DoorTemple: MinigameLocationData(Maps.AztecChunky5DTemple, 0, Minigames.KremlingKoshVEasy),
    Locations.AztecDonkeyQuicksandCave: MinigameLocationData(Maps.AngryAztec, 33, Minigames.StealthySnoopVEasy),
    Locations.AztecLankyLlamaTempleBarrel: MinigameLocationData(Maps.AztecLlamaTemple, 2, Minigames.TeeteringTurtleTroubleVEasy),
    Locations.FactoryLankyTestingRoomBarrel: MinigameLocationData(Maps.FranticFactory, 15, Minigames.BattyBarrelBanditEasy),
    Locations.FactoryDiddyChunkyRoomBarrel: MinigameLocationData(Maps.FranticFactory, 13, Minigames.BeaverBotherEasy),
    Locations.FactoryTinyProductionRoom: MinigameLocationData(Maps.FranticFactory, 16, Minigames.KrazyKongKlamourEasy),
    Locations.FactoryDiddyBlockTower: MinigameLocationData(Maps.FranticFactory, 0, Minigames.PerilPathPanicVEasy),
    Locations.FactoryChunkybyArcade: MinigameLocationData(Maps.FranticFactory, 14, Minigames.StashSnatchEasy),
    Locations.GalleonChunky5DoorShip: MinigameLocationData(Maps.Galleon5DShipDiddyLankyChunky, 1, Minigames.BattyBarrelBanditVEasy),
    Locations.GalleonTinySubmarine: MinigameLocationData(Maps.GalleonSubmarine, 3, Minigames.BigBugBashEasy),
    Locations.GalleonDonkey5DoorShip: MinigameLocationData(Maps.Galleon5DShipDKTiny, 0, Minigames.KrazyKongKlamourEasy),
    Locations.GalleonTiny2DoorShip: MinigameLocationData(Maps.Galleon2DShip, 0, Minigames.KremlingKoshEasy),
    Locations.GalleonLankyGoldTower: MinigameLocationData(Maps.GloomyGalleon, 7, Minigames.SearchlightSeekVEasy),
    Locations.GalleonDiddy5DoorShip: MinigameLocationData(Maps.Galleon5DShipDiddyLankyChunky, 0, Minigames.SplishSplashSalvageEasy),
    Locations.GalleonDiddyGoldTower: MinigameLocationData(Maps.GloomyGalleon, 6, Minigames.StealthySnoopNormal),
    Locations.ForestDiddyOwlRace: MinigameLocationData(Maps.FungiForest, 21, Minigames.BusyBarrelBarrageNormal),
    Locations.ForestLankyColoredMushrooms: MinigameLocationData(Maps.ForestLankyMushroomsRoom, 0, Minigames.KrazyKongKlamourHard),
    Locations.ForestDonkeyBarn: MinigameLocationData(Maps.ForestThornvineBarn, 3, Minigames.MinecartMayhemNormal),
    Locations.ForestDonkeyBaboonBlast: MinigameLocationData(Maps.ForestBaboonBlast, 22, Minigames.PerilPathPanicEasy),
    Locations.ForestTinyMushroomBarrel: MinigameLocationData(Maps.ForestGiantMushroom, 8, Minigames.SpeedySwingSortieNormal),
    Locations.ForestDiddyTopofMushroom: MinigameLocationData(Maps.FungiForest, 18, Minigames.TeeteringTurtleTroubleEasy),
    Locations.CavesDonkeyBaboonBlast: MinigameLocationData(Maps.CavesBaboonBlast, 19, Minigames.BusyBarrelBarrageHard),
    Locations.CavesTinyCaveBarrel: MinigameLocationData(Maps.CrystalCaves, 7, Minigames.KrazyKongKlamourHard),
    Locations.CavesDiddyJetpackBarrel: MinigameLocationData(Maps.CrystalCaves, 6, Minigames.MadMazeMaulNormal),
    Locations.CavesChunky5DoorCabin: MinigameLocationData(Maps.CavesChunkyCabin, 0, Minigames.SearchlightSeekNormal),
    Locations.CastleLankyTower: MinigameLocationData(Maps.CastleTower, 0, Minigames.BeaverBotherNormal),
    Locations.CastleChunkyTree: MinigameLocationData(Maps.CastleTree, 0, Minigames.BeaverBotherNormal),
    Locations.CastleDiddyAboveCastle: MinigameLocationData(Maps.CreepyCastle, 9, Minigames.BigBugBashHard),
    Locations.CastleLankyDungeon: MinigameLocationData(Maps.CastleDungeon, 0, Minigames.KremlingKoshNormal),
    Locations.CastleDiddyBallroom: MinigameLocationData(Maps.CastleBallroom, 1, Minigames.MinecartMayhemHard),
    Locations.CastleChunkyCrypt: MinigameLocationData(Maps.CastleCrypt, 0, Minigames.SearchlightSeekHard),
    Locations.CastleTinyOverChasm: MinigameLocationData(Maps.CastleUpperCave, 0, Minigames.TeeteringTurtleTroubleNormal),
    Locations.HelmDonkey1: MinigameLocationData(Maps.HideoutHelm, 16, Minigames.DonkeyRambi),
    Locations.HelmDonkey2: MinigameLocationData(Maps.HideoutHelm, 15, Minigames.DonkeyTarget),
    Locations.HelmDiddy1: MinigameLocationData(Maps.HideoutHelm, 8, Minigames.DiddyKremling),
    Locations.HelmDiddy2: MinigameLocationData(Maps.HideoutHelm, 9, Minigames.DiddyRocketbarrel),
    Locations.HelmLanky1: MinigameLocationData(Maps.HideoutHelm, 10, Minigames.LankyMaze),
    Locations.HelmLanky2: MinigameLocationData(Maps.HideoutHelm, 11, Minigames.LankyShooting),
    Locations.HelmTiny1: MinigameLocationData(Maps.HideoutHelm, 13, Minigames.TinyMushroom),
    Locations.HelmTiny2: MinigameLocationData(Maps.HideoutHelm, 12, Minigames.TinyPonyTailTwirl),
    Locations.HelmChunky1: MinigameLocationData(Maps.HideoutHelm, 14, Minigames.ChunkyHiddenKremling),
    Locations.HelmChunky2: MinigameLocationData(Maps.HideoutHelm, 7, Minigames.ChunkyShooting),
}
