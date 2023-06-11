"""Contains the class which holds logic variables, and the master copy of regions."""
from math import ceil

import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.DKIsles
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes
import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.HideoutHelm
import randomizer.LogicFiles.JungleJapes
import randomizer.LogicFiles.Shops
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions as RegionEnum
from randomizer.Enums.Settings import ActivateAllBananaports, GlitchesSelected, HelmDoorItem, LogicType, ShockwaveStatus, ShuffleLoadingZones, TrainingBarrels, WinCondition
from randomizer.Enums.Time import Time
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import LocationList
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.ShufflableExit import GetShuffledLevelIndex
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Prices import CanBuy, GetPriceAtLocation

STARTING_SLAM = 1  # Currently we're assuming you always start with 1 slam


def IsGlitchEnabled(settings, glitch_enum):
    """Check if glitch is enabled in the settings."""
    return len(settings.glitches_selected) == 0 or glitch_enum in settings.glitches_selected


class LogicVarHolder:
    """Used to store variables when checking logic conditions."""

    def __init__(self, settings=None):
        """Initialize with given parameters."""
        if settings is None:
            return
        self.settings = settings

        # Some restrictions are added to the item placement fill for the sake of reducing indirect errors. We can overlook these restrictions once we know the fill is valid.
        self.assumeFillSuccess = False
        # See CalculateWothPaths method for details on these assumptions
        self.assumeInfiniteGBs = False
        self.assumeInfiniteCoins = False
        self.assumeAztecEntry = False
        self.assumeLevel4Entry = False
        self.assumeUpperIslesAccess = False
        self.assumeKRoolAccess = False

        self.startkong = self.settings.starting_kong
        # Glitch Logic
        enable_glitch_logic = self.settings.logic_type == LogicType.glitch
        self.phasewalk = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.phase_walking)
        self.phaseswim = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.phase_swimming)
        self.moonkicks = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.moonkicks)
        self.ledgeclip = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.ledge_clips)
        self.generalclips = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.general_clips)  # General clips which have no real category
        self.lanky_blocker_skip = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.b_locker_skips)  # Also includes ppunch skip
        self.dk_blocker_skip = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.b_locker_skips)
        self.troff_skip = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.troff_n_scoff_skips)
        self.spawn_snags = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.spawn_snags)
        self.advanced_platforming = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.advanced_platforming)
        self.tbs = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.tag_barrel_storage) and not self.settings.disable_tag_barrels
        self.swim_through_shores = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.swim_through_shores)
        self.boulder_clip = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.boulder_clips) and False  # Temporarily disabled
        self.skew = enable_glitch_logic and IsGlitchEnabled(settings, GlitchesSelected.skew)
        # Reset
        self.Reset()

    def Reset(self):
        """Reset all logic variables.

        Done between reachability searches and upon initialization.
        """
        self.latest_owned_items = []
        self.found_test_item = False
        self.banned_items = []

        self.donkey = Kongs.donkey in self.settings.starting_kong_list
        self.diddy = Kongs.diddy in self.settings.starting_kong_list
        self.lanky = Kongs.lanky in self.settings.starting_kong_list
        self.tiny = Kongs.tiny in self.settings.starting_kong_list
        self.chunky = Kongs.chunky in self.settings.starting_kong_list

        # Right now assuming start with training barrels
        self.vines = self.settings.training_barrels == TrainingBarrels.normal
        self.swim = self.settings.training_barrels == TrainingBarrels.normal
        self.oranges = self.settings.training_barrels == TrainingBarrels.normal
        self.barrels = self.settings.training_barrels == TrainingBarrels.normal

        self.progDonkey = 0
        self.blast = False
        self.strongKong = False
        self.grab = False

        self.progDiddy = 0
        self.charge = False
        self.jetpack = False
        self.spring = False

        self.progLanky = 0
        self.handstand = False
        self.balloon = False
        self.sprint = False

        self.progTiny = 0
        self.mini = False
        self.twirl = False
        self.monkeyport = False

        self.progChunky = 0
        self.hunkyChunky = False
        self.punch = False
        self.gorillaGone = False

        self.coconut = False
        self.peanut = False
        self.grape = False
        self.feather = False
        self.pineapple = False

        self.bongos = False
        self.guitar = False
        self.trombone = False
        self.saxophone = False
        self.triangle = False

        self.nintendoCoin = False
        self.rarewareCoin = False

        self.camera = self.settings.shockwave_status == ShockwaveStatus.start_with
        self.shockwave = self.settings.shockwave_status == ShockwaveStatus.start_with

        self.scope = False
        self.homing = False

        self.JapesKey = False
        self.AztecKey = False
        self.FactoryKey = False
        self.GalleonKey = False
        self.ForestKey = False
        self.CavesKey = False
        self.CastleKey = False
        self.HelmKey = False

        self.HelmDonkey1 = False
        self.HelmDonkey2 = False
        self.HelmDiddy1 = False
        self.HelmDiddy2 = False
        self.HelmLanky1 = False
        self.HelmLanky2 = False
        self.HelmTiny1 = False
        self.HelmTiny2 = False
        self.HelmChunky1 = False
        self.HelmChunky2 = False

        self.Slam = STARTING_SLAM
        self.AmmoBelts = 0
        self.InstUpgrades = 0

        self.GoldenBananas = 0
        self.BananaFairies = 0
        self.BananaMedals = 0
        self.BattleCrowns = 0

        self.superSlam = False
        self.superDuperSlam = False

        self.Blueprints = []

        self.Events = []

        self.Hints = []

        self.SpecialLocationsReached = []

        # Set key events for keys which are given to the player at start of game
        keyEvents = [
            Events.JapesKeyTurnedIn,
            Events.AztecKeyTurnedIn,
            Events.FactoryKeyTurnedIn,
            Events.GalleonKeyTurnedIn,
            Events.ForestKeyTurnedIn,
            Events.CavesKeyTurnedIn,
            Events.CastleKeyTurnedIn,
            Events.HelmKeyTurnedIn,
        ]
        for keyEvent in keyEvents:
            if keyEvent not in self.settings.krool_keys_required:
                # This is horrifyingly bad to go keys -> events -> keys but the patcher is expecting events in krool_keys_required and I'm not touching the math there to fix it
                if keyEvent == Events.JapesKeyTurnedIn:
                    self.JapesKey = True
                elif keyEvent == Events.AztecKeyTurnedIn:
                    self.AztecKey = True
                elif keyEvent == Events.FactoryKeyTurnedIn:
                    self.FactoryKey = True
                elif keyEvent == Events.GalleonKeyTurnedIn:
                    self.GalleonKey = True
                elif keyEvent == Events.ForestKeyTurnedIn:
                    self.ForestKey = True
                elif keyEvent == Events.CavesKeyTurnedIn:
                    self.CavesKey = True
                elif keyEvent == Events.CastleKeyTurnedIn:
                    self.CastleKey = True
                elif keyEvent == Events.HelmKeyTurnedIn:
                    self.HelmKey = True

        activated_warp_maps = []
        if self.settings.activate_all_bananaports == ActivateAllBananaports.all:
            activated_warp_maps = [
                Maps.JungleJapes,
                Maps.AngryAztec,
                Maps.AztecLlamaTemple,
                Maps.FranticFactory,
                Maps.GloomyGalleon,
                Maps.FungiForest,
                Maps.CrystalCaves,
                Maps.CreepyCastle,
                Maps.CastleCrypt,
                Maps.Isles,
            ]
        elif self.settings.activate_all_bananaports == ActivateAllBananaports.isles:
            activated_warp_maps = [Maps.Isles]
        if any(activated_warp_maps):
            for warp_data in BananaportVanilla.values():
                if warp_data.map_id in activated_warp_maps:
                    self.Events.append(warp_data.event)

        # Colored banana and coin arrays
        # Colored bananas as 7 arrays of 5 (7 levels for 5 kongs)
        self.ColoredBananas = []
        for i in range(7):
            self.ColoredBananas.append([0] * 5)

        self.Coins = [0] * 5
        self.RegularCoins = [0] * 5
        self.RainbowCoins = 0
        self.SpentCoins = [0] * 5

        # These access variables based on current region
        # Shouldn't be checked unless updated directly beforehand
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

        self.kong = self.startkong

        self.bananaHoard = False

        self.UpdateKongs()

    def isPriorHelmComplete(self, kong: Kongs):
        """Determine if there is access to the kong's helm room."""
        room_seq = (Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy)
        kong_evt = (Events.HelmDonkeyDone, Events.HelmDiddyDone, Events.HelmLankyDone, Events.HelmTinyDone, Events.HelmChunkyDone)
        desired_index = room_seq.index(kong)
        helm_order = self.settings.helm_order
        if desired_index in helm_order:
            sequence_slot = helm_order.index(desired_index)
            if sequence_slot > 0:
                prior_kong = room_seq[helm_order[sequence_slot - 1]]
                return kong_evt[prior_kong] in self.Events
        return Events.HelmDoorsOpened in self.Events

    def UpdateCoins(self):
        """Update coin total."""
        for x in range(5):
            self.Coins[x] = (self.RegularCoins[x] + (5 * self.RainbowCoins)) - self.SpentCoins[x]

    def Update(self, ownedItems):
        """Update logic variables based on owned items."""
        # Except for banned items - these items aren't allowed to be used by the logic
        ownedItems = [item for item in ownedItems if item not in self.banned_items]

        self.latest_owned_items = ownedItems
        self.found_test_item = self.found_test_item or Items.TestItem in ownedItems

        self.donkey = self.donkey or Items.Donkey in ownedItems or self.startkong == Kongs.donkey
        self.diddy = self.diddy or Items.Diddy in ownedItems or self.startkong == Kongs.diddy
        self.lanky = self.lanky or Items.Lanky in ownedItems or self.startkong == Kongs.lanky
        self.tiny = self.tiny or Items.Tiny in ownedItems or self.startkong == Kongs.tiny
        self.chunky = self.chunky or Items.Chunky in ownedItems or self.startkong == Kongs.chunky

        self.vines = self.vines or Items.Vines in ownedItems
        self.swim = self.swim or Items.Swim in ownedItems
        self.oranges = self.oranges or Items.Oranges in ownedItems
        self.barrels = self.barrels or Items.Barrels in ownedItems

        self.progDonkey = sum(1 for x in ownedItems if x == Items.ProgressiveDonkeyPotion)
        self.blast = self.blast or (Items.BaboonBlast in ownedItems or self.progDonkey >= 1) and self.donkey
        self.strongKong = self.strongKong or (Items.StrongKong in ownedItems or self.progDonkey >= 2) and self.donkey
        self.grab = self.grab or (Items.GorillaGrab in ownedItems or self.progDonkey >= 3) and self.donkey

        self.progDiddy = sum(1 for x in ownedItems if x == Items.ProgressiveDiddyPotion)
        self.charge = self.charge or (Items.ChimpyCharge in ownedItems or self.progDiddy >= 1) and self.diddy
        self.jetpack = self.jetpack or (Items.RocketbarrelBoost in ownedItems or self.progDiddy >= 2) and self.diddy
        self.spring = self.spring or (Items.SimianSpring in ownedItems or self.progDiddy >= 3) and self.diddy

        self.progLanky = sum(1 for x in ownedItems if x == Items.ProgressiveLankyPotion)
        self.handstand = self.handstand or (Items.Orangstand in ownedItems or self.progLanky >= 1) and self.lanky
        self.balloon = self.balloon or (Items.BaboonBalloon in ownedItems or self.progLanky >= 2) and self.lanky
        self.sprint = self.sprint or (Items.OrangstandSprint in ownedItems or self.progLanky >= 3) and self.lanky

        self.progTiny = sum(1 for x in ownedItems if x == Items.ProgressiveTinyPotion)
        self.mini = self.mini or (Items.MiniMonkey in ownedItems or self.progTiny >= 1) and self.tiny
        self.twirl = self.twirl or (Items.PonyTailTwirl in ownedItems or self.progTiny >= 2) and self.tiny
        self.monkeyport = self.monkeyport or (Items.Monkeyport in ownedItems or self.progTiny >= 3) and self.tiny

        self.progChunky = sum(1 for x in ownedItems if x == Items.ProgressiveChunkyPotion)
        self.hunkyChunky = self.hunkyChunky or (Items.HunkyChunky in ownedItems or self.progChunky >= 1) and self.chunky
        self.punch = self.punch or (Items.PrimatePunch in ownedItems or self.progChunky >= 2) and self.chunky
        self.gorillaGone = self.gorillaGone or (Items.GorillaGone in ownedItems or self.progChunky >= 3) and self.chunky

        self.coconut = self.coconut or Items.Coconut in ownedItems and self.donkey
        self.peanut = self.peanut or Items.Peanut in ownedItems and self.diddy
        self.grape = self.grape or Items.Grape in ownedItems and self.lanky
        self.feather = self.feather or Items.Feather in ownedItems and self.tiny
        self.pineapple = self.pineapple or Items.Pineapple in ownedItems and self.chunky

        self.bongos = self.bongos or Items.Bongos in ownedItems and self.donkey
        self.guitar = self.guitar or Items.Guitar in ownedItems and self.diddy
        self.trombone = self.trombone or Items.Trombone in ownedItems and self.lanky
        self.saxophone = self.saxophone or Items.Saxophone in ownedItems and self.tiny
        self.triangle = self.triangle or Items.Triangle in ownedItems and self.chunky

        self.nintendoCoin = self.nintendoCoin or Items.NintendoCoin in ownedItems
        self.rarewareCoin = self.rarewareCoin or Items.RarewareCoin in ownedItems

        self.JapesKey = self.JapesKey or Items.JungleJapesKey in ownedItems
        self.AztecKey = self.AztecKey or Items.AngryAztecKey in ownedItems
        self.FactoryKey = self.FactoryKey or Items.FranticFactoryKey in ownedItems
        self.GalleonKey = self.GalleonKey or Items.GloomyGalleonKey in ownedItems
        self.ForestKey = self.ForestKey or Items.FungiForestKey in ownedItems
        self.CavesKey = self.CavesKey or Items.CrystalCavesKey in ownedItems
        self.CastleKey = self.CastleKey or Items.CreepyCastleKey in ownedItems
        self.HelmKey = self.HelmKey or Items.HideoutHelmKey in ownedItems

        self.HelmDonkey1 = self.HelmDonkey1 or Items.HelmDonkey1 in ownedItems
        self.HelmDonkey2 = self.HelmDonkey2 or Items.HelmDonkey2 in ownedItems
        self.HelmDiddy1 = self.HelmDiddy1 or Items.HelmDiddy1 in ownedItems
        self.HelmDiddy2 = self.HelmDiddy2 or Items.HelmDiddy2 in ownedItems
        self.HelmLanky1 = self.HelmLanky1 or Items.HelmLanky1 in ownedItems
        self.HelmLanky2 = self.HelmLanky2 or Items.HelmLanky2 in ownedItems
        self.HelmTiny1 = self.HelmTiny1 or Items.HelmTiny1 in ownedItems
        self.HelmTiny2 = self.HelmTiny2 or Items.HelmTiny2 in ownedItems
        self.HelmChunky1 = self.HelmChunky1 or Items.HelmChunky1 in ownedItems
        self.HelmChunky2 = self.HelmChunky2 or Items.HelmChunky2 in ownedItems

        self.Slam = sum(1 for x in ownedItems if x == Items.ProgressiveSlam) + STARTING_SLAM
        if Items.ProgressiveSlam in self.banned_items:  # If slam is banned, prevent logic from owning a better slam
            self.Slam = STARTING_SLAM
        self.AmmoBelts = sum(1 for x in ownedItems if x == Items.ProgressiveAmmoBelt)
        self.InstUpgrades = sum(1 for x in ownedItems if x == Items.ProgressiveInstrumentUpgrade)

        self.GoldenBananas = sum(1 for x in ownedItems if x == Items.GoldenBanana)
        self.BananaFairies = sum(1 for x in ownedItems if x == Items.BananaFairy)
        self.BananaMedals = sum(1 for x in ownedItems if x == Items.BananaMedal)
        self.BattleCrowns = sum(1 for x in ownedItems if x == Items.BattleCrown)
        self.RainbowCoins = sum(1 for x in ownedItems if x == Items.RainbowCoin)

        self.camera = self.camera or Items.CameraAndShockwave in ownedItems or Items.Camera in ownedItems
        self.shockwave = self.shockwave or Items.CameraAndShockwave in ownedItems or Items.Shockwave in ownedItems

        self.scope = self.scope or Items.SniperSight in ownedItems
        self.homing = self.homing or Items.HomingAmmo in ownedItems

        self.superSlam = self.Slam >= 2
        self.superDuperSlam = self.Slam >= 3

        self.Blueprints = [x for x in ownedItems if x >= Items.JungleJapesDonkeyBlueprint and x <= Items.DKIslesChunkyBlueprint]
        self.Hints = [x for x in ownedItems if x >= Items.JapesDonkeyHint and x <= Items.CastleChunkyHint]
        self.Beans = sum(1 for x in ownedItems if x == Items.Bean)
        self.Pearls = sum(1 for x in ownedItems if x == Items.Pearl)

        self.UpdateCoins()

        self.bananaHoard = self.bananaHoard or Items.BananaHoard in ownedItems

    def GetCoins(self, kong):
        """Get Coin Total for a kong."""
        self.UpdateCoins()
        return self.Coins[kong]

    def CanSlamSwitch(self, level: Levels, default_requirement_level: int):
        """Determine whether the player can operate the necessary slam operation.

        Keyword arguments:
        level -- level which the switch takes place
        default_requirement_level -- Default requirement for the switch without randomization. 1 - Base slam, 2 - Super, 3 - Super Duper.
        """
        slam_req = default_requirement_level
        if self.settings.alter_switch_allocation:
            slam_req = self.settings.switch_allocation[level]
        if slam_req == 2:
            return self.superSlam
        elif slam_req == 3:
            return self.superDuperSlam
        return self.Slam

    def CanPhaseswim(self):
        """Determine whether the player can perform phase swim."""
        return self.phaseswim and self.swim

    def CanSTS(self):
        """Determine whether the player can perform swim through shores."""
        return self.swim_through_shores and self.swim

    def CanMoonkick(self):
        """Determine whether the player can perform a moonkick."""
        return self.moonkicks and self.isdonkey and self.settings.krusha_kong != Kongs.donkey

    def CanOStandTBSNoclip(self):
        """Determine whether the player can perform Orangstand TBS Noclip."""
        return self.tbs and self.handstand and self.islanky

    def CanAccessRNDRoom(self):
        """Determine whether the player can enter an R&D Room with glitches."""
        return self.phasewalk or self.generalclips or self.CanOStandTBSNoclip()

    def CanGetOnCannonGamePlatform(self):
        """Determine whether the player can get on the platform in Cannon Game Room in Gloomy Galleon."""
        return Events.WaterSwitch in self.Events or (self.advanced_platforming and (self.ischunky or (self.islanky and self.settings.krusha_kong != Kongs.lanky)))

    def CanSkew(self, swim, kong_req=Kongs.any):
        """Determine whether the player can skew."""
        if swim:
            return self.skew and self.swim and self.HasGun(kong_req) and self.CanPhaseswim()
        return self.skew

    def AddEvent(self, event):
        """Add an event to events list so it can be checked for logically."""
        self.Events.append(event)

    def SetKong(self, kong):
        """Set current kong for logic."""
        self.kong = kong
        self.UpdateKongs()

    def GetKongs(self):
        """Return all owned kongs."""
        ownedKongs = []
        if self.donkey:
            ownedKongs.append(Kongs.donkey)
        if self.diddy:
            ownedKongs.append(Kongs.diddy)
        if self.lanky:
            ownedKongs.append(Kongs.lanky)
        if self.tiny:
            ownedKongs.append(Kongs.tiny)
        if self.chunky:
            ownedKongs.append(Kongs.chunky)
        return ownedKongs

    def UpdateKongs(self):
        """Set variables for current kong based on self.kong."""
        self.isdonkey = self.kong == Kongs.donkey
        self.isdiddy = self.kong == Kongs.diddy
        self.islanky = self.kong == Kongs.lanky
        self.istiny = self.kong == Kongs.tiny
        self.ischunky = self.kong == Kongs.chunky

    def IsKong(self, kong):
        """Check if logic is currently a specific kong."""
        if kong == Kongs.donkey:
            return self.isdonkey
        if kong == Kongs.diddy:
            return self.isdiddy
        if kong == Kongs.lanky:
            return self.islanky
        if kong == Kongs.tiny:
            return self.istiny
        if kong == Kongs.chunky:
            return self.ischunky
        if kong == Kongs.any:
            return True

    def HasKong(self, kong):
        """Check if logic currently owns a specific kong."""
        if kong == Kongs.donkey:
            return self.donkey
        if kong == Kongs.diddy:
            return self.diddy
        if kong == Kongs.lanky:
            return self.lanky
        if kong == Kongs.tiny:
            return self.tiny
        if kong == Kongs.chunky:
            return self.chunky
        if kong == Kongs.any:
            return True

    def HasGun(self, kong):
        """Check if logic currently is currently the specified kong and owns a gun for them."""
        if kong == Kongs.donkey:
            return self.coconut and self.isdonkey
        elif kong == Kongs.diddy:
            return self.peanut and self.isdiddy
        elif kong == Kongs.lanky:
            return self.grape and self.islanky
        elif kong == Kongs.tiny:
            return self.feather and self.istiny
        elif kong == Kongs.chunky:
            return self.pineapple and self.ischunky
        elif kong == Kongs.any:
            return (self.coconut and self.isdonkey) or (self.peanut and self.isdiddy) or (self.grape and self.islanky) or (self.feather and self.istiny) or (self.pineapple and self.ischunky)
        return False

    def HasInstrument(self, kong):
        """Check if logic currently is currently the specified kong and owns an instrument for them."""
        if kong == Kongs.donkey:
            return self.bongos and self.isdonkey
        if kong == Kongs.diddy:
            return self.guitar and self.isdiddy
        if kong == Kongs.lanky:
            return self.trombone and self.islanky
        if kong == Kongs.tiny:
            return self.saxophone and self.istiny
        if kong == Kongs.chunky:
            return self.triangle and self.ischunky
        if kong == Kongs.any:
            return (self.bongos and self.isdonkey) or (self.guitar and self.isdiddy) or (self.trombone and self.islanky) or (self.saxophone and self.istiny) or (self.triangle and self.ischunky)

    def DoorItemCheck(self, item, count):
        """Check if item requirement has been fulfilled with regards to a Helm door item."""
        helmdoor_vars = {
            HelmDoorItem.req_gb: self.GoldenBananas,
            HelmDoorItem.req_bp: len(self.Blueprints),
            HelmDoorItem.req_companycoins: sum([self.nintendoCoin, self.rarewareCoin]),
            HelmDoorItem.req_key: sum([self.JapesKey, self.AztecKey, self.FactoryKey, self.GalleonKey, self.ForestKey, self.CavesKey, self.CastleKey, self.HelmKey]),
            HelmDoorItem.req_medal: self.BananaMedals,
            HelmDoorItem.req_crown: self.BattleCrowns,
            HelmDoorItem.req_fairy: self.BananaFairies,
            HelmDoorItem.req_rainbowcoin: self.RainbowCoins,
            HelmDoorItem.req_bean: self.Beans,
            HelmDoorItem.req_pearl: self.Pearls,
        }
        if item in helmdoor_vars.keys():
            return helmdoor_vars[item] >= count
        return True

    def CrownDoorOpened(self):
        """Check if Crown Door is opened."""
        if self.settings.crown_door_item == HelmDoorItem.opened:
            return True
        elif self.settings.crown_door_item == HelmDoorItem.vanilla:
            return self.DoorItemCheck(HelmDoorItem.req_crown, self.settings.crown_door_item_count)
        return self.DoorItemCheck(self.settings.crown_door_item, self.settings.crown_door_item_count)

    def CoinDoorOpened(self):
        """Check if Coin Door is opened."""
        if self.settings.coin_door_item == HelmDoorItem.opened:
            return True
        elif self.settings.coin_door_item == HelmDoorItem.vanilla:
            return self.DoorItemCheck(HelmDoorItem.req_companycoins, self.settings.coin_door_item_count)
        return self.DoorItemCheck(self.settings.coin_door_item, self.settings.coin_door_item_count)

    def CanFreeDiddy(self):
        """Check if the cage locking Diddy's vanilla location can be opened."""
        return LocationList[Locations.DiddyKong].item == Items.NoItem or self.HasGun(self.settings.diddy_freeing_kong)

    def CanOpenJapesGates(self):
        """Check if we can pick up the item inside Diddy's cage, thus opening the gates in Japes."""
        caged_item_id = LocationList[Locations.JapesDonkeyFreeDiddy].item
        # If it's NoItem, then the gates are already open
        if caged_item_id == Items.NoItem:
            return True
        # If we can't free Diddy, then we can't access the item so we can't reach the item
        if not self.CanFreeDiddy():
            return False
        # If we are the right kong, then we can always get the item
        if self.IsKong(self.settings.diddy_freeing_kong):
            return True
        # If we aren't the right kong, we need free trade to be on
        elif self.settings.free_trade_items:
            # During the fill we can't assume this item is accessible quite yet - this could cause errors with placing items in the back of Japes
            if caged_item_id is None:
                return False
            # If it's not a blueprint, free trade gets us the item
            if ItemList[caged_item_id].type != Types.Blueprint:
                return True
            # But if it is a blueprint, we need to check blueprint access (which checks blueprint free trade)
            else:
                return self.BlueprintAccess(ItemList[caged_item_id])
        # If we failed to hit a successful condition, we failed to reach the caged item
        return False

    def CanFreeTiny(self):
        """Check if kong at Tiny location can be freed, requires either chimpy charge or primate punch."""
        if LocationList[Locations.TinyKong].item == Items.NoItem:
            return self.IsKong(self.settings.tiny_freeing_kong) or self.settings.free_trade_items
        elif self.settings.tiny_freeing_kong == Kongs.diddy:
            return self.charge and self.isdiddy
        elif self.settings.tiny_freeing_kong == Kongs.chunky:
            return self.punch and self.ischunky
        # Used only as placeholder during fill when kong puzzles are not yet assigned
        elif self.settings.tiny_freeing_kong == Kongs.any:
            return True

    def CanLlamaSpit(self):
        """Check if the Llama spit can be triggered."""
        return self.HasInstrument(self.settings.lanky_freeing_kong)

    def CanFreeLanky(self):
        """Check if kong at Lanky location can be freed, requires freeing kong to have its gun and instrument."""
        return (self.HasGun(self.settings.lanky_freeing_kong) or LocationList[Locations.LankyKong].item == Items.NoItem) and (
            (self.swim and self.HasInstrument(self.settings.lanky_freeing_kong)) or self.phasewalk or self.CanPhaseswim()
        )

    def CanFreeChunky(self):
        """Check if kong at Chunky location can be freed."""
        # If the cage is empty, the item is just lying on the ground
        if LocationList[Locations.ChunkyKong].item == Items.NoItem:
            return self.IsKong(self.settings.chunky_freeing_kong) or self.settings.free_trade_items
        # Otherwise you need the right slam level (usually 1)
        else:
            return self.CanSlamSwitch(Levels.FranticFactory, 1) and self.IsKong(self.settings.chunky_freeing_kong)

    def UpdateCurrentRegionAccess(self, region):
        """Set access of current region."""
        self.donkeyAccess = region.donkeyAccess
        self.diddyAccess = region.diddyAccess
        self.lankyAccess = region.lankyAccess
        self.tinyAccess = region.tinyAccess
        self.chunkyAccess = region.chunkyAccess

    def LevelEntered(self, level):
        """Check whether a level, or any level above it, has been entered."""
        if Events.CastleEntered in self.Events:
            return True
        elif Events.CavesEntered in self.Events and level <= Levels.CrystalCaves:
            return True
        elif Events.ForestEntered in self.Events and level <= Levels.FungiForest:
            return True
        elif Events.GalleonEntered in self.Events and level <= Levels.GloomyGalleon:
            return True
        elif Events.FactoryEntered in self.Events and level <= Levels.FranticFactory:
            return True
        elif Events.AztecEntered in self.Events and level <= Levels.AngryAztec:
            return True
        elif Events.JapesEntered in self.Events and level <= Levels.JungleJapes:
            return True
        return False

    def AddCollectible(self, collectible, level):
        """Add a collectible."""
        if collectible.enabled:
            missingGun = False
            if collectible.type == Collectibles.coin:
                # Normal coins, add amount for the kong
                self.Coins[collectible.kong] += collectible.amount
                self.RegularCoins[collectible.kong] += collectible.amount
            # Add bananas for correct level for this kong
            elif collectible.type == Collectibles.banana:
                self.ColoredBananas[level][collectible.kong] += collectible.amount
            # Add 5 times amount of banana bunches
            elif collectible.type == Collectibles.bunch:
                self.ColoredBananas[level][collectible.kong] += collectible.amount * 5
            # Add 10 bananas for a balloon
            elif collectible.type == Collectibles.balloon:
                if self.HasGun(collectible.kong):
                    self.ColoredBananas[level][collectible.kong] += collectible.amount * 10
                    collectible.added = True
                missingGun = True
            if not missingGun:
                collectible.added = True

    def PurchaseShopItem(self, location_id):
        """Purchase from this location and subtract price from logical coin counts."""
        location = LocationList[location_id]
        price = GetPriceAtLocation(self.settings, location_id, location, self.Slam, self.AmmoBelts, self.InstUpgrades)
        if price is None:  # This shouldn't happen but it's probably harmless
            return  # TODO: solve this
        # If shared move, take the price from all kongs EVEN IF THEY AREN'T FREED YET
        if location.kong == Kongs.any:
            for kong in range(0, 5):
                self.Coins[kong] -= price
                self.SpentCoins[kong] += price
            return
        # If kong specific move, just that kong paid for it
        else:
            self.Coins[location.kong] -= price
            self.SpentCoins[location.kong] += price
            return

    @staticmethod
    def HasAccess(region, kong):
        """Check if a certain kong has access to a certain region.

        Usually the region's own HasAccess function is used, but this is necessary for checking access for other regions in logic files.
        """
        return Regions[region].HasAccess(kong)

    @staticmethod
    def TimeAccess(region, time):
        """Check if a certain region has the given time of day access."""
        if time == Time.Day:
            return Regions[region].dayAccess
        elif time == Time.Night:
            return Regions[region].nightAccess
        # Not sure when this'd be used
        else:  # if time == Time.Both
            return Regions[region].dayAccess or Regions[region].nightAccess

    def BlueprintAccess(self, item):
        """Check if we are the correct kong for this blueprint item."""
        if item is None or item.type != Types.Blueprint:
            return False
        return self.settings.free_trade_blueprints or self.IsKong(item.kong)

    def HintAccess(self, location, region_id):
        """Check if we are the right kong for this hint door."""
        if location.item is None:
            return False
        # The only weird exception: vanilla Fungi Lobby hint doors only check for Chunky, not the current Kong, and all besides Chunky's needs grab
        if not self.settings.wrinkly_location_rando and not self.settings.remove_wrinkly_puzzles and region_id == RegionEnum.FungiForestLobby:
            return self.chunky and (location.kong == Kongs.chunky or (self.donkey and self.grab))
        return self.HasKong(location.kong)

    def CanBuy(self, location):
        """Check if there are enough coins to purchase this location."""
        return CanBuy(location, self)

    def CanAccessKRool(self):
        """Make sure that each required key has been turned in."""
        return all(not keyRequired not in self.Events for keyRequired in self.settings.krool_keys_required)

    def IsBossReachable(self, level):
        """Check if the boss banana requirement is met."""
        return self.HasEnoughKongs(level) and ((sum(self.ColoredBananas[level]) >= self.settings.BossBananas[level]) or self.troff_skip)

    def HasEnoughKongs(self, level, forPreviousLevel=False):
        """Check if kongs are required for progression, do we have enough to reach the given level."""
        # If your kongs are not progression (LZR, no logic, etc.) or it's *complex* level order, these requirements don't apply
        if self.settings.kongs_for_progression and not self.settings.hard_level_progression:
            levelIndex = 8
            if level != Levels.HideoutHelm:
                # Figure out where this level fits in the progression
                levelIndex = GetShuffledLevelIndex(level)
                if forPreviousLevel:
                    levelIndex = levelIndex - 1
            # Must have sufficient kongs freed to make forward progress for first 5 levels
            if levelIndex < 5:
                return len(self.GetKongs()) > levelIndex
            else:
                # Expect to have all the kongs by level 6
                return len(self.GetKongs()) == 5
        else:
            return True

    def IsBossBeatable(self, level):
        """Return true if the boss for a given level is beatable according to boss location rando and boss kong rando."""
        requiredKong = self.settings.boss_kongs[level]
        bossFight = self.settings.boss_maps[level]
        # Ensure we have the required moves for the boss fight itself
        hasRequiredMoves = True
        if bossFight == Maps.FactoryBoss and requiredKong == Kongs.tiny and not (self.settings.hard_bosses and self.settings.krusha_kong != Kongs.tiny):
            hasRequiredMoves = self.twirl
        elif bossFight == Maps.FungiBoss:
            hasRequiredMoves = self.hunkyChunky and self.barrels
        elif bossFight == Maps.JapesBoss or bossFight == Maps.AztecBoss or bossFight == Maps.CavesBoss:
            hasRequiredMoves = self.barrels
        # In simple level order, there are a couple very specific cases we have to account for in order to prevent boss fill failures
        level_order_matters = not self.settings.hard_level_progression and self.settings.shuffle_loading_zones in (ShuffleLoadingZones.none, ShuffleLoadingZones.levels)
        if level_order_matters and not self.assumeFillSuccess:  # These conditions only matter on fill, not on playthrough
            order_of_level = 7  # Guaranteed to be 1-7 here
            for level_order in self.settings.level_order:
                if self.settings.level_order[level_order] == level:
                    order_of_level = level_order
            if order_of_level == 4 and not self.barrels:  # Prevent Barrels on boss 3
                return False
            if order_of_level == 7 and (not self.hunkyChunky or (not self.twirl and not self.settings.hard_bosses)):  # Prevent Hunky on boss 7, and also Twirl on non-hard bosses
                return False
        return self.IsKong(requiredKong) and hasRequiredMoves

    def HasFillRequirementsForLevel(self, level):
        """Check if we meet the fill's move requirements for the given level."""
        # These requirements are only relevant for fill purposes - once we know the fill is valid, we can ignore these requirements
        if self.assumeFillSuccess:
            return True
        # Additionally, these restrictions only apply to simple level order, as these are the only seeds progressing levels in 1-7 order
        level_order_matters = not self.settings.hard_level_progression and self.settings.shuffle_loading_zones in (ShuffleLoadingZones.none, ShuffleLoadingZones.levels)
        if level_order_matters:
            # Levels have some special requirements depending on where they fall in the level order
            order_of_level = 8  # If order_of_level remains unchanged in the coming loop, then the level is Helm which is always 8th
            order_of_aztec = 0
            for level_order in self.settings.level_order:
                if self.settings.level_order[level_order] == level:
                    order_of_level = level_order
                if self.settings.level_order[level_order] == Levels.AngryAztec:
                    order_of_aztec = level_order
            # You need to have vines or twirl before you can enter Aztec or any level beyond it
            if order_of_level >= order_of_aztec and not (self.vines or (self.istiny and self.twirl)):
                return False
            if order_of_level >= 4:
                # Require the following moves by level 4:
                # - Swim so you can get into Lobby 4. This prevents logic from skipping this level for T&S requirements, preventing 0'd T&S.
                # - Barrels so there will always be an eligible boss fill given the available moves at any level.
                # - Vines for gameplay reasons. Needing vines for Helm is a frequent bottleneck and this eases the hunt for it.
                if not self.swim or not self.barrels or not self.vines:
                    return False
                # Require one of twirl or hunky chunky by level 7 to prevent non-hard-boss fill failures
                if not self.settings.hard_bosses and order_of_level >= 7 and not (self.twirl or self.hunkyChunky):
                    return False
                # Require both hunky chunky and twirl (or hard bosses) before Helm to prevent boss fill failures
                if order_of_level > 7 and not self.hunkyChunky or (not self.twirl and not self.settings.hard_bosses):
                    return False
            # Make sure we have access to all prior required keys before entering the next level - this prevents keys from being placed in levels beyond what they unlock
            if order_of_level > 1 and not self.JapesKey:
                return False
            elif order_of_level > 2 and not self.AztecKey:
                return False
            elif order_of_level > 4 and (not self.FactoryKey or not self.GalleonKey):
                return False
            elif order_of_level > 5 and not self.ForestKey:
                return False
            elif order_of_level > 7 and (not self.CavesKey or not self.CastleKey):
                return False

        # If we have the moves, ensure we have enough kongs as well
        return self.HasEnoughKongs(level, forPreviousLevel=True)

    def IsLevelEnterable(self, level):
        """Check if level entry requirement is met."""
        # We must meet the fill's kong and move requirements to enter this level
        if not self.HasFillRequirementsForLevel(level):
            return False
        # Calculate what levels we can glitch into
        dk_skip_levels = [Levels.AngryAztec, Levels.GloomyGalleon, Levels.FungiForest, Levels.CrystalCaves, Levels.CreepyCastle]
        if self.CanMoonkick():
            dk_skip_levels.append(Levels.HideoutHelm)
        can_dk_skip = self.isdonkey and self.dk_blocker_skip and level in dk_skip_levels
        can_diddy_skip = self.isdiddy and self.lanky_blocker_skip and level == Levels.HideoutHelm and self.generalclips
        can_lanky_skip = self.islanky and self.lanky_blocker_skip and level != Levels.HideoutHelm
        can_tiny_skip = self.istiny and self.lanky_blocker_skip and level == Levels.HideoutHelm and self.generalclips
        can_chunky_skip = self.ischunky and self.lanky_blocker_skip and self.punch and level not in (Levels.FranticFactory, Levels.HideoutHelm)
        # To enter a level, we either need (or assume) enough GBs to get rid of B. Locker or a glitch way to bypass it
        return self.assumeInfiniteGBs or self.GoldenBananas >= self.settings.EntryGBs[level] or can_dk_skip or can_diddy_skip or can_lanky_skip or can_tiny_skip or can_chunky_skip

    def WinConditionMet(self):
        """Check if the current game state has met the win condition."""
        if self.settings.win_condition == WinCondition.beat_krool:
            return Events.KRoolDefeated in self.Events
        # Photo taking doesn't have a perfect wincon so this'll do until something better is concocted
        if self.settings.win_condition == WinCondition.poke_snap:
            return Events.KRoolDefeated in self.Events and self.camera
        elif self.settings.win_condition == WinCondition.get_key8:
            return self.HelmKey
        elif self.settings.win_condition == WinCondition.all_fairies:
            return self.BananaFairies >= 20
        elif self.settings.win_condition == WinCondition.all_blueprints:
            return len(self.Blueprints) >= 40
        elif self.settings.win_condition == WinCondition.all_medals:
            return self.BananaMedals >= 40
        elif self.settings.win_condition == WinCondition.all_keys:
            return (
                Events.JapesKeyTurnedIn in self.Events
                and Events.AztecKeyTurnedIn in self.Events
                and Events.FactoryKeyTurnedIn in self.Events
                and Events.GalleonKeyTurnedIn in self.Events
                and Events.ForestKeyTurnedIn in self.Events
                and Events.CavesKeyTurnedIn in self.Events
                and Events.CastleKeyTurnedIn in self.Events
                and Events.HelmKeyTurnedIn in self.Events
            )
        else:
            return False

    def CanGetRarewareCoin(self):
        """Check if you meet the logical requirements to obtain the Rareware Coin."""
        have_enough_medals = self.BananaMedals >= self.settings.medal_requirement
        # Make sure you have access to enough levels to fit the locations in. This isn't super precise and doesn't need to be.
        required_level_order = max(2, min(ceil(self.settings.medal_requirement / 4), 6))  # At least level 2 to give space for medal placements, at most level 6 to allow shenanigans
        return have_enough_medals and self.HasFillRequirementsForLevel(self.settings.level_order[required_level_order])

    def CanGetRarewareGB(self):
        """Check if you meet the logical requirements to obtain the Rareware GB."""
        have_enough_fairies = self.BananaFairies >= self.settings.rareware_gb_fairies
        is_correct_kong = self.istiny or self.settings.free_trade_items
        required_level_order = max(2, min(ceil(self.settings.rareware_gb_fairies / 2), 5))  # At least level 2 to give space for fairy placements, at most level 5 to allow shenanigans
        return have_enough_fairies and is_correct_kong and self.HasFillRequirementsForLevel(self.settings.level_order[required_level_order])

    def BanItems(self, items):
        """Prevent an item from being picked up by the logic."""
        self.banned_items = items
        # Also remove logical ownership of each item - this covers cases where you start with the move flag (not the training barrels, just raw start with like the camera/shockwave setting)
        for item in items:
            if item == Items.Vines:
                self.vines = False
            elif item == Items.Swim:
                self.swim = False
            elif item == Items.Barrels:
                self.barrels = False
            elif item == Items.Oranges:
                self.oranges = False
            elif item == Items.BaboonBlast:
                self.blast = False
            elif item == Items.StrongKong:
                self.strongKong = False
            elif item == Items.GorillaGrab:
                self.grab = False
            elif item == Items.ChimpyCharge:
                self.charge = False
            elif item == Items.RocketbarrelBoost:
                self.jetpack = False
            elif item == Items.SimianSpring:
                self.spring = False
            elif item == Items.Orangstand:
                self.handstand = False
            elif item == Items.BaboonBalloon:
                self.balloon = False
            elif item == Items.OrangstandSprint:
                self.sprint = False
            elif item == Items.MiniMonkey:
                self.mini = False
            elif item == Items.PonyTailTwirl:
                self.twirl = False
            elif item == Items.Monkeyport:
                self.monkeyport = False
            elif item == Items.HunkyChunky:
                self.hunkyChunky = False
            elif item == Items.PrimatePunch:
                self.punch = False
            elif item == Items.GorillaGone:
                self.gorillaGone = False
            elif item == Items.Coconut:
                self.coconut = False
            elif item == Items.Peanut:
                self.peanut = False
            elif item == Items.Grape:
                self.grape = False
            elif item == Items.Feather:
                self.feather = False
            elif item == Items.Pineapple:
                self.pineapple = False
            elif item == Items.HomingAmmo:
                self.homing = False
            elif item == Items.SniperSight:
                self.scope = False
            elif item == Items.Bongos:
                self.bongos = False
            elif item == Items.Guitar:
                self.guitar = False
            elif item == Items.Trombone:
                self.trombone = False
            elif item == Items.Saxophone:
                self.saxophone = False
            elif item == Items.Triangle:
                self.triangle = False
            elif item == Items.CameraAndShockwave:
                self.camera = False
                self.shockwave = False
            elif item == Items.Camera:
                self.camera = False
            elif item == Items.Shockwave:
                self.shockwave = False
            elif item == Items.ProgressiveSlam:
                self.Slam = STARTING_SLAM
                # Banned slams are also handled with care in Update() specially

    def HasAllItems(self):
        """Return if you have all progression items."""
        # You may now own the banned item
        self.latest_owned_items.extend(self.banned_items)
        self.banned_items = []
        self.Update(self.latest_owned_items)
        # If you didn't beat the game, you obviously don't have all the progression items - this covers the possible need for camera and each key
        if not self.WinConditionMet():
            return False
        # Otherwise return true if you have all major moves
        return (
            self.donkey
            and self.diddy
            and self.lanky
            and self.tiny
            and self.chunky
            and self.vines
            and self.swim
            and self.barrels
            and self.oranges
            and self.blast
            and self.strongKong
            and self.grab
            and self.charge
            and self.jetpack
            and self.spring
            and self.handstand
            and self.balloon
            and self.sprint
            and self.mini
            and self.twirl
            and self.monkeyport
            and self.hunkyChunky
            and self.punch
            and self.gorillaGone
            and self.superDuperSlam
            and self.coconut
            and self.peanut
            and self.grape
            and self.feather
            and self.pineapple
            and self.homing
            and self.scope
            and self.shockwave
            and self.bongos
            and self.guitar
            and self.trombone
            and self.saxophone
            and self.triangle
        )


LogicVariables = LogicVarHolder()

# Import regions from logic files
Regions = {}
Regions.update(randomizer.LogicFiles.DKIsles.LogicRegions)
Regions.update(randomizer.LogicFiles.JungleJapes.LogicRegions)
Regions.update(randomizer.LogicFiles.AngryAztec.LogicRegions)
Regions.update(randomizer.LogicFiles.FranticFactory.LogicRegions)
Regions.update(randomizer.LogicFiles.GloomyGalleon.LogicRegions)
Regions.update(randomizer.LogicFiles.FungiForest.LogicRegions)
Regions.update(randomizer.LogicFiles.CrystalCaves.LogicRegions)
Regions.update(randomizer.LogicFiles.CreepyCastle.LogicRegions)
Regions.update(randomizer.LogicFiles.HideoutHelm.LogicRegions)
Regions.update(randomizer.LogicFiles.Shops.LogicRegions)

# Auxillary regions for colored bananas and banana coins
CollectibleRegions = {}
CollectibleRegions.update(randomizer.CollectibleLogicFiles.DKIsles.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.FungiForest.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions)
CollectibleRegions.update(randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions)


def ResetRegionAccess():
    """Reset kong access for all regions."""
    for region in Regions.values():
        region.ResetAccess()


def ResetCollectibleRegions():
    """Reset if each collectible has been added."""
    for region in CollectibleRegions.values():
        for collectible in region:
            collectible.added = False
            # collectible.enabled = collectible.vanilla


def ClearAllLocations():
    """Clear item from every location."""
    for location in LocationList.values():
        location.item = None
