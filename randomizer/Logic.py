"""Contains the class which holds logic variables, and the master copy of regions."""
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
from randomizer.Lists.ShufflableExit import GetShuffledLevelIndex
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Time import Time
from randomizer.Lists.Location import Location, LocationList
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Prices import CanBuy, GetPriceOfMoveItem


STARTING_SLAM = 1  # Currently we're assuming you always start with 1 slam


class LogicVarHolder:
    """Used to store variables when checking logic conditions."""

    def __init__(self, settings=None):
        """Initialize with given parameters."""
        if settings is None:
            return
        self.settings = settings
        self.startkong = self.settings.starting_kong
        self.Reset()

    def Reset(self):
        """Reset all logic variables.

        Done between reachability searches and upon initialization.
        """
        self.donkey = Kongs.donkey in self.settings.starting_kong_list
        self.diddy = Kongs.diddy in self.settings.starting_kong_list
        self.lanky = Kongs.lanky in self.settings.starting_kong_list
        self.tiny = Kongs.tiny in self.settings.starting_kong_list
        self.chunky = Kongs.chunky in self.settings.starting_kong_list

        # Right now assuming start with training barrels
        self.vines = True  # self.settings.training_barrels == "startwith"
        self.swim = True  # self.settings.training_barrels == "startwith"
        self.oranges = True  # self.settings.training_barrels == "startwith"
        self.barrels = True  # self.settings.training_barrels == "startwith"

        self.progDonkey = 3 if self.settings.unlock_all_moves else 0
        self.blast = self.settings.unlock_all_moves
        self.strongKong = self.settings.unlock_all_moves
        self.grab = self.settings.unlock_all_moves

        self.progDiddy = 3 if self.settings.unlock_all_moves else 0
        self.charge = self.settings.unlock_all_moves
        self.jetpack = self.settings.unlock_all_moves
        self.spring = self.settings.unlock_all_moves

        self.progLanky = 3 if self.settings.unlock_all_moves else 0
        self.handstand = self.settings.unlock_all_moves
        self.balloon = self.settings.unlock_all_moves
        self.sprint = self.settings.unlock_all_moves

        self.progTiny = 3 if self.settings.unlock_all_moves else 0
        self.mini = self.settings.unlock_all_moves
        self.twirl = self.settings.unlock_all_moves
        self.monkeyport = self.settings.unlock_all_moves

        self.progChunky = 3 if self.settings.unlock_all_moves else 0
        self.hunkyChunky = self.settings.unlock_all_moves
        self.punch = self.settings.unlock_all_moves
        self.gorillaGone = self.settings.unlock_all_moves

        self.coconut = self.settings.unlock_all_moves
        self.peanut = self.settings.unlock_all_moves
        self.grape = self.settings.unlock_all_moves
        self.feather = self.settings.unlock_all_moves
        self.pineapple = self.settings.unlock_all_moves

        self.bongos = self.settings.unlock_all_moves
        self.guitar = self.settings.unlock_all_moves
        self.trombone = self.settings.unlock_all_moves
        self.saxophone = self.settings.unlock_all_moves
        self.triangle = self.settings.unlock_all_moves

        self.nintendoCoin = False
        self.rarewareCoin = False

        self.camera = self.settings.unlock_fairy_shockwave
        self.shockwave = self.settings.unlock_fairy_shockwave

        self.scope = self.settings.unlock_all_moves
        self.homing = self.settings.unlock_all_moves

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

        self.Slam = 3 if self.settings.unlock_all_moves else STARTING_SLAM
        self.AmmoBelts = 2 if self.settings.unlock_all_moves else 0
        self.InstUpgrades = 3 if self.settings.unlock_all_moves else 0

        self.GoldenBananas = 0
        self.BananaFairies = 0
        self.BananaMedals = 0
        self.BattleCrowns = 0

        self.superSlam = self.settings.unlock_all_moves
        self.superDuperSlam = self.settings.unlock_all_moves

        self.Blueprints = []

        self.Events = []

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
                self.Events.append(keyEvent)

        # Colored banana and coin arrays
        # Colored bananas as 7 arrays of 5 (7 levels for 5 kongs)
        self.ColoredBananas = []
        for i in range(7):
            self.ColoredBananas.append([0] * 5)
        self.Coins = [0] * 5

        # These access variables based on current region
        # Shouldn't be checked unless updated directly beforehand
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

        self.kong = self.startkong

        self.UpdateKongs()

    def Update(self, ownedItems):
        """Update logic variables based on owned items."""
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

        self.Slam = 3 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveSlam) + STARTING_SLAM
        self.AmmoBelts = 2 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveAmmoBelt)
        self.InstUpgrades = 3 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveInstrumentUpgrade)

        self.GoldenBananas = sum(1 for x in ownedItems if x == Items.GoldenBanana)
        self.BananaFairies = sum(1 for x in ownedItems if x == Items.BananaFairy)
        self.BananaMedals = sum(1 for x in ownedItems if x == Items.BananaMedal)
        self.BattleCrowns = sum(1 for x in ownedItems if x == Items.BattleCrown)

        self.camera = self.camera or Items.CameraAndShockwave in ownedItems
        self.shockwave = self.shockwave or Items.CameraAndShockwave in ownedItems

        self.scope = self.scope or Items.SniperSight in ownedItems
        self.homing = self.homing or Items.HomingAmmo in ownedItems

        self.superSlam = self.Slam >= 2
        self.superDuperSlam = self.Slam >= 3

        self.Blueprints = [x for x in ownedItems if x >= Items.DKIslesDonkeyBlueprint]

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
        if kong == Kongs.diddy:
            return self.peanut and self.isdiddy
        if kong == Kongs.lanky:
            return self.grape and self.islanky
        if kong == Kongs.tiny:
            return self.feather and self.istiny
        if kong == Kongs.chunky:
            return self.pineapple and self.ischunky
        if kong == Kongs.any:
            return (self.coconut and self.isdonkey) or (self.peanut and self.isdiddy) or (self.grape and self.islanky) or (self.feather and self.istiny) or (self.pineapple and self.ischunky)

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

    def CanFreeDiddy(self):
        """Check if kong at Diddy location can be freed."""
        return self.HasGun(self.settings.diddy_freeing_kong)

    def CanFreeTiny(self):
        """Check if kong at Tiny location can be freed,r equires either chimpy charge or primate punch."""
        if self.settings.tiny_freeing_kong == Kongs.diddy:
            return self.charge and self.isdiddy
        elif self.settings.tiny_freeing_kong == Kongs.chunky:
            return self.punch and self.ischunky
        # Used only as placeholder during fill when kong puzzles are not yet assigned
        elif self.settings.tiny_freeing_kong == Kongs.any:
            return True

    def CanFreeLanky(self):
        """Check if kong at Lanky location can be freed, requires freeing kong to have its gun and instrument."""
        return self.HasGun(self.settings.lanky_freeing_kong) and self.HasInstrument(self.settings.lanky_freeing_kong)

    def CanFreeChunky(self):
        """Check if kong at Chunky location can be freed."""
        return self.Slam and self.IsKong(self.settings.chunky_freeing_kong)

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
        if collectible.type == Collectibles.coin:
            # Rainbow coin, add 5 coins for each kong
            if collectible.kong == Kongs.any:
                for i in range(5):
                    self.Coins[i] += collectible.amount * 5
            # Normal coins, add amount for the kong
            else:
                self.Coins[collectible.kong] += collectible.amount
        # Add bananas for correct level for this kong
        elif collectible.type == Collectibles.banana:
            self.ColoredBananas[level][collectible.kong] += collectible.amount
        # Add 5 times amount of banana bunches
        elif collectible.type == Collectibles.bunch:
            self.ColoredBananas[level][collectible.kong] += collectible.amount * 5
        # Add 10 bananas for a balloon
        elif collectible.type == Collectibles.balloon:
            self.ColoredBananas[level][collectible.kong] += collectible.amount * 10
        collectible.added = True

    def PurchaseShopItem(self, location: Location):
        """Purchase items from shops and subtract price from logical coin counts."""
        if location.item is not None and location.item is not Items.NoItem:
            price = GetPriceOfMoveItem(location.item, self.settings, self.Slam, self.AmmoBelts, self.InstUpgrades)
            # print("BuyShopItem for location: " + location.name)
            # print("Item: " + ItemList[location.item].name + " has Price: " + str(price))
            # If shared move, take the price from all kongs EVEN IF THEY AREN'T FREED YET
            if location.kong == Kongs.any:
                for kong in range(0, 5):
                    self.Coins[kong] -= price
            # If kong specific move, just that kong paid for it
            else:
                self.Coins[location.kong] -= price

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

    def KasplatAccess(self, location):
        """Use the kasplat map to check kasplat logic for blueprint locations."""
        kong = self.kasplat_map[location]
        if location == Locations.GalleonKasplatGoldTower:
            # Water level needs to be raised and you spring up as diddy to get killed by the kasplat
            # Or, any kong having teleporter access works too
            if kong == Kongs.diddy:
                return Events.WaterSwitch in self.Events and self.IsKong(Kongs.diddy)
            else:
                return Events.TreasureRoomTeleporterUnlocked in self.Events and self.HasAccess(randomizer.Enums.Regions.Regions.Shipyard, kong)
        return self.IsKong(kong)

    def CanBuy(self, location):
        """Check if there are enough coins to purchase this location."""
        return CanBuy(location, self.Coins, self.settings, self.Slam, self.AmmoBelts, self.InstUpgrades)

    def CanAccessKRool(self):
        """Make sure that each required key has been turned in."""
        return all(not keyRequired not in self.Events for keyRequired in self.settings.krool_keys_required)

    def IsBossReachable(self, level):
        """Check if the boss banana requirement is met."""
        return self.HasEnoughKongs(level) and sum(self.ColoredBananas[level]) >= self.settings.BossBananas[level]

    def HasEnoughKongs(self, level, forPreviousLevel=False):
        """Check if kongs are required for progression, do we have enough to reach the given level."""
        if self.settings.kongs_for_progression and level != Levels.HideoutHelm:
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
        hasRequiredMoves = True
        if bossFight == Maps.FactoryBoss and requiredKong == Kongs.tiny:
            hasRequiredMoves = self.twirl
        elif bossFight == Maps.FungiBoss:
            hasRequiredMoves = self.hunkyChunky
        return self.IsKong(requiredKong) and hasRequiredMoves

    def IsLevelEnterable(self, level):
        """Check if level entry requirement is met."""
        return self.HasEnoughKongs(level, forPreviousLevel=True) and self.GoldenBananas >= self.settings.EntryGBs[level]


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


def ClearAllLocations():
    """Clear item from every location."""
    for location in LocationList.values():
        location.item = None
