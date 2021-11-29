from Enums.Items import Items
from Enums.Events import Events
from Enums.Levels import Levels
from Enums.Kongs import Kongs
from Enums.Collectibles import Collectibles

import LogicFiles.DKIsles
import LogicFiles.JungleJapes
import LogicFiles.AngryAztec
import LogicFiles.FranticFactory
import LogicFiles.GloomyGalleon
import LogicFiles.FungiForest
import LogicFiles.CrystalCaves
import LogicFiles.CreepyCastle
import LogicFiles.HideoutHelm
import LogicFiles.Shops

import CollectibleLogicFiles.DKIsles
import CollectibleLogicFiles.JungleJapes
import CollectibleLogicFiles.AngryAztec
import CollectibleLogicFiles.FranticFactory
import CollectibleLogicFiles.GloomyGalleon
import CollectibleLogicFiles.FungiForest
import CollectibleLogicFiles.CrystalCaves
import CollectibleLogicFiles.CreepyCastle
from randomizer.LogicClasses import Collectible

class LogicVarHolder:

    def __init__(self, startkong):
        self.startkong = startkong
        self.Reset()

    # Reset all logic variables
    # Done between reachability searches
    def Reset(self):
        self.donkey = self.startkong == Kongs.donkey
        self.diddy = self.startkong == Kongs.diddy
        self.lanky = self.startkong == Kongs.lanky
        self.tiny = self.startkong == Kongs.tiny
        self.chunky = self.startkong == Kongs.chunky

        self.vines = False
        self.swim = False
        self.oranges = False
        self.barrels = False

        self.blast = False
        self.strongKong = False
        self.grab = False
        self.charge = False
        self.jetpack = False
        self.spring = False
        self.handstand = False
        self.balloon = False
        self.sprint = False
        self.mini = False
        self.twirl = False
        self.monkeyport = False
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

        self.camera = False
        self.shockwave = False

        self.JapesKey = False
        self.AztecKey = False
        self.FactoryKey = False
        self.GalleonKey = False
        self.ForestKey = False
        self.CavesKey = False
        self.CastleKey = False
        self.HelmKey = False
        
        self.Slam = 0
        self.GoldenBananas = 0
        self.BananaFairies = 0
        self.BananaMedals = 0
        self.BattleCrowns = 0
        
        self.superSlam = False
        self.superDuperSlam = False

        self.Blueprints = []

        self.Events = []

        # Colored banana and coin arrays 
        # Colored bananas as 8 arrays of 5, only need 7 but leave room for DK Isles since we use the enum
        self.coloredBananas = [[0]*5]*8
        self.Coins = [0]*5

        # These access variables based on current region
        # Shouldn't be checked unless updated directly beforehand
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

        self.kong = self.startkong

        self.UpdateKongs()

    # Update logic variables based on owned items
    def Update(self, ownedItems):
        self.donkey = self.donkey or Items.Donkey in ownedItems or self.startkong == Kongs.donkey
        self.diddy = self.diddy or Items.Diddy in ownedItems or self.startkong == Kongs.diddy
        self.lanky = self.lanky or Items.Lanky in ownedItems or self.startkong == Kongs.lanky
        self.tiny = self.tiny or Items.Tiny in ownedItems or self.startkong == Kongs.tiny
        self.chunky = self.chunky or Items.Chunky in ownedItems or self.startkong == Kongs.chunky

        self.vines = self.vines or Items.Vines in ownedItems
        self.swim = self.swim or Items.Swim in ownedItems
        self.oranges = self.oranges or Items.Oranges in ownedItems
        self.barrels = self.barrels or Items.Barrels in ownedItems

        self.blast = self.blast or Items.BaboonBlast in ownedItems and self.donkey
        self.strongKong = self.strongKong or Items.StrongKong in ownedItems and self.donkey
        self.grab = self.grab or Items.GorillaGrab in ownedItems and self.donkey
        self.charge = self.charge or Items.ChimpyCharge in ownedItems and self.diddy
        self.jetpack = self.jetpack or Items.RocketbarrelBoost in ownedItems and self.diddy
        self.spring = self.spring or Items.SimianSpring in ownedItems and self.diddy
        self.handstand = self.handstand or Items.Orangstand in ownedItems and self.lanky
        self.balloon = self.balloon or Items.BaboonBalloon in ownedItems and self.lanky
        self.sprint = self.sprint or Items.OrangstandSprint in ownedItems and self.lanky
        self.mini = self.mini or Items.MiniMonkey in ownedItems and self.tiny
        self.twirl = self.twirl or Items.PonyTailTwirl in ownedItems and self.tiny
        self.monkeyport = self.monkeyport or Items.Monkeyport in ownedItems and self.tiny
        self.hunkyChunky = self.hunkyChunky or Items.HunkyChunky in ownedItems and self.chunky
        self.punch = self.punch or Items.PrimatePunch in ownedItems and self.chunky
        self.gorillaGone = self.gorillaGone or Items.GorillaGone in ownedItems and self.chunky

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

        self.Slam = sum(1 for x in ownedItems if x == Items.ProgressiveSlam)
        self.GoldenBananas = sum(1 for x in ownedItems if x == Items.GoldenBanana)
        self.BananaFairies = sum(1 for x in ownedItems if x == Items.BananaFairy)
        self.BananaMedals = sum(1 for x in ownedItems if x == Items.BananaMedal)
        self.BattleCrowns = sum(1 for x in ownedItems if x == Items.BattleCrown)

        self.camera = self.camera or Items.CameraAndShockwave in ownedItems
        self.shockwave = self.shockwave or Items.CameraAndShockwave in ownedItems

        self.superSlam = self.Slam >= 2
        self.superDuperSlam = self.Slam >= 3

        self.Blueprints = [x for x in ownedItems if x >= Items.DKIslesDonkeyBlueprint]

    # Add an event to events list so it can be checked for logically
    def AddEvent(self, event):
        self.Events.append(event)

    # Set current kong for logic
    def SetKong(self, kong):
        self.kong = kong
        self.UpdateKongs()

    # Return all owned kongs
    def GetKongs(self):
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

    # Set variables for current kong based on self.kong
    def UpdateKongs(self):
        self.isdonkey = self.kong == Kongs.donkey
        self.isdiddy = self.kong == Kongs.diddy
        self.islanky = self.kong == Kongs.lanky
        self.istiny = self.kong == Kongs.tiny
        self.ischunky = self.kong == Kongs.chunky

    # Check if logic is currently a specific kong
    def IsKong(self, kong):
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
        if kong == Kongs.rainbow:
            return True

    # Set access of current region
    def UpdateCurrentRegionAccess(self, region):
        self.donkeyAccess = region.donkeyAccess
        self.diddyAccess = region.diddyAccess
        self.lankyAccess = region.lankyAccess
        self.tinyAccess = region.tinyAccess
        self.chunkyAccess = region.chunkyAccess

    # Check whether a level, or any level above it, has been entered
    def LevelEntered(self, level):
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

    # Add a collectible
    def AddCollectible(self, collectible, level):
        if collectible.type == Collectibles.coin:
            # Rainbow coin, add 5 coins for each kong
            if collectible.kong == Kongs.rainbow:
                for i in range(5):
                    self.Coins[i] += 5
            # Normal coins, add amount for the kong
            else:
                self.Coins[collectible.kong] += collectible.amount
        # Add bananas for correct level for this kong
        elif collectible.type == Collectibles.banana:
            self.coloredBananas[level][collectible.kong] += collectible.amount
        # Add 10 bananas for a balloon
        elif collectible.type == Collectibles.balloon:
            self.coloredBananas[level][collectible.kong] += 10
        collectible.added = True

# Initialize logic variables, for now assume start with donkey
LogicVariables = LogicVarHolder(Kongs.donkey)

# Import regions from logic files
Regions = {}
Regions.update(LogicFiles.DKIsles.LogicRegions)
Regions.update(LogicFiles.JungleJapes.LogicRegions)
Regions.update(LogicFiles.AngryAztec.LogicRegions)
Regions.update(LogicFiles.FranticFactory.LogicRegions)
Regions.update(LogicFiles.GloomyGalleon.LogicRegions)
Regions.update(LogicFiles.FungiForest.LogicRegions)
Regions.update(LogicFiles.CrystalCaves.LogicRegions)
Regions.update(LogicFiles.CreepyCastle.LogicRegions)
Regions.update(LogicFiles.HideoutHelm.LogicRegions)
Regions.update(LogicFiles.Shops.LogicRegions)

# Auxillary regions for colored bananas and banana coins
CollectibleRegions = {}
CollectibleRegions.update(CollectibleLogicFiles.DKIsles.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.JungleJapes.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.AngryAztec.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.FranticFactory.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.GloomyGalleon.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.FungiForest.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.CrystalCaves.LogicRegions)
CollectibleRegions.update(CollectibleLogicFiles.CreepyCastle.LogicRegions)

# Reset kong access for all regions
def ResetRegionAccess():
    for region in Regions.values():
        region.ResetAccess()

# Reset if each collectible has been added
def ResetCollectiblesRegions():
    for region in CollectibleRegions.values():
        for collectible in region:
            collectible.added = False

# Updates access of master regions list from a temp list of regions
def UpdateAllRegionsAccess(tempRegions):
    for (key, value) in Regions.items():
        value.UpdateAccessFromRegion(tempRegions[key])
