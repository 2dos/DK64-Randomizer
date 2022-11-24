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
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
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
from randomizer.Enums.Time import Time
from randomizer.Lists.Location import LocationList
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.ShufflableExit import GetShuffledLevelIndex
from randomizer.Prices import CanBuy, GetPriceAtLocation

STARTING_SLAM = 1  # Currently we're assuming you always start with 1 slam


class LogicVarHolder:
    """Used to store variables when checking logic conditions."""

    def __init__(self, settings=None):
        """Initialize with given parameters."""
        if settings is None:
            return
        self.settings = settings
        self.pathMode = False  # See CalculateWothPaths method for details
        self.startkong = self.settings.starting_kong
        self.Reset()

    def Reset(self):
        """Reset all logic variables.

        Done between reachability searches and upon initialization.
        """
        self.latest_owned_items = []
        self.found_test_item = False
        self.banned_item = None

        self.donkey = Kongs.donkey in self.settings.starting_kong_list
        self.diddy = Kongs.diddy in self.settings.starting_kong_list
        self.lanky = Kongs.lanky in self.settings.starting_kong_list
        self.tiny = Kongs.tiny in self.settings.starting_kong_list
        self.chunky = Kongs.chunky in self.settings.starting_kong_list

        # Right now assuming start with training barrels
        self.vines = self.settings.training_barrels == "normal"
        self.swim = self.settings.training_barrels == "normal"
        self.oranges = self.settings.training_barrels == "normal"
        self.barrels = self.settings.training_barrels == "normal"

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

        self.camera = self.settings.shockwave_status == "start_with"
        self.shockwave = self.settings.shockwave_status == "start_with"

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

    def Update(self, ownedItems):
        """Update logic variables based on owned items."""
        # Except for the banned item - this item isn't allowed to be used by the logic
        while self.banned_item in ownedItems:
            ownedItems.remove(self.banned_item)
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

        self.Slam = 3 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveSlam) + STARTING_SLAM
        self.AmmoBelts = 2 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveAmmoBelt)
        self.InstUpgrades = 3 if self.settings.unlock_all_moves else sum(1 for x in ownedItems if x == Items.ProgressiveInstrumentUpgrade)

        self.GoldenBananas = sum(1 for x in ownedItems if x == Items.GoldenBanana)
        self.BananaFairies = sum(1 for x in ownedItems if x == Items.BananaFairy)
        self.BananaMedals = sum(1 for x in ownedItems if x == Items.BananaMedal)
        self.BattleCrowns = sum(1 for x in ownedItems if x == Items.BattleCrown)

        self.camera = self.camera or Items.CameraAndShockwave in ownedItems or Items.Camera in ownedItems
        self.shockwave = self.shockwave or Items.CameraAndShockwave in ownedItems or Items.Shockwave in ownedItems

        self.scope = self.scope or Items.SniperSight in ownedItems
        self.homing = self.homing or Items.HomingAmmo in ownedItems

        self.superSlam = self.Slam >= 2
        self.superDuperSlam = self.Slam >= 3

        self.Blueprints = [x for x in ownedItems if x >= Items.JungleJapesDonkeyBlueprint]

        self.bananaHoard = self.bananaHoard or Items.BananaHoard in ownedItems

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
        """Check if kong at Tiny location can be freed,r equires either chimpy charge or primate punch."""
        if self.settings.tiny_freeing_kong == Kongs.diddy:
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
        return self.swim and self.HasGun(self.settings.lanky_freeing_kong) and self.HasInstrument(self.settings.lanky_freeing_kong)

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
        if collectible.enabled:
            added = False
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
                if self.HasGun(collectible.kong):
                    self.ColoredBananas[level][collectible.kong] += collectible.amount * 10
                    collectible.added = True
                added = True
            if not added:
                collectible.added = True

    def PurchaseShopItem(self, location_id):
        """Purchase items from shops and subtract price from logical coin counts."""
        location = LocationList[location_id]
        if location.item is not None and location.item is not Items.NoItem:
            price = GetPriceAtLocation(self.settings, location_id, location, self.Slam, self.AmmoBelts, self.InstUpgrades)
            if price is None:  # This probably shouldn't happen but I think it's harmless
                return  # TODO: solve this
            # print("BuyShopItem for location: " + location.name)
            # print("Item: " + ItemList[location.item].name + " has Price: " + str(price))
            # If shared move, take the price from all kongs EVEN IF THEY AREN'T FREED YET
            if location.kong == Kongs.any:
                for kong in range(0, 5):
                    self.Coins[kong] -= price
            # If kong specific move, just that kong paid for it
            else:
                self.Coins[location.kong] -= price

    def GainInfiniteCoins(self):
        """Add an arbitrarily large amount of coins to the current game state so as to effectively ignore any coin requirements."""
        for i in range(len(self.Coins)):
            self.Coins[i] += 10000

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

    def CanBuy(self, location):
        """Check if there are enough coins to purchase this location."""
        return CanBuy(location, self)

    def CanAccessKRool(self):
        """Make sure that each required key has been turned in."""
        return all(not keyRequired not in self.Events for keyRequired in self.settings.krool_keys_required)

    def IsBossReachable(self, level):
        """Check if the boss banana requirement is met."""
        return self.HasEnoughKongs(level) and sum(self.ColoredBananas[level]) >= self.settings.BossBananas[level]

    def HasEnoughKongs(self, level, forPreviousLevel=False):
        """Check if kongs are required for progression, do we have enough to reach the given level."""
        if self.settings.kongs_for_progression and level != Levels.HideoutHelm and not self.settings.hard_level_progression:
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
            hasRequiredMoves = self.hunkyChunky and self.barrels
        elif bossFight == Maps.JapesBoss or bossFight == Maps.AztecBoss or bossFight == Maps.CavesBoss:
            hasRequiredMoves = self.barrels
        return self.IsKong(requiredKong) and hasRequiredMoves

    def IsLevelEnterable(self, level):
        """Check if level entry requirement is met."""
        # Later levels can have some special requirements
        # "pathMode" is so WotH paths can always enter levels regardless of owned items
        if not self.pathMode and level >= 3:
            level_order_matters = not self.settings.hard_level_progression and self.settings.shuffle_loading_zones in ("none", "levels")
            # If level order matters...
            if level_order_matters:
                # Require barrels by level 3 to prevent boss barrel fill failures
                if not self.barrels:
                    return False
                # Require one of twirl or hunky chunky by level 7 to prevent non-hard-boss fill failures
                if not self.settings.hard_bosses and level >= 7 and not (self.twirl or self.hunkyChunky):
                    return False
        return self.HasEnoughKongs(level, forPreviousLevel=True) and self.GoldenBananas >= self.settings.EntryGBs[level]

    def WinConditionMet(self):
        """Check if the current game state has met the win condition."""
        if self.settings.win_condition == "beat_krool" or self.settings.win_condition == "poke_snap":  # Photo taking doesn't have a clear wincon so this'll do until something better is concocted
            return Events.KRoolDefeated in self.Events
        elif self.settings.win_condition == "get_key8":
            return self.HelmKey
        elif self.settings.win_condition == "all_fairies":
            return self.BananaFairies >= 20
        elif self.settings.win_condition == "all_blueprints":
            return len(self.Blueprints) >= 40
        elif self.settings.win_condition == "all_medals":
            return self.BananaMedals >= 40
        elif self.settings.win_condition == "all_keys":
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
        required_level = min(ceil(self.settings.medal_requirement / 4), 6)
        return have_enough_medals and self.IsLevelEnterable(required_level)

    def BanItem(self, item):
        """Prevent an item from being picked up by the logic."""
        self.banned_item = item

    def HasAllItems(self):
        """Return if you have all progression items."""
        # You may now own the banned item
        self.latest_owned_items.append(self.banned_item)
        self.banned_item = None
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
