from LogicClasses import Kongs
from Enums.Items import Items
from Enums.Events import Events
from Enums.Levels import Levels
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
        self.donkey = Items.Donkey in ownedItems or self.startkong == Kongs.donkey
        self.diddy = Items.Diddy in ownedItems or self.startkong == Kongs.diddy
        self.lanky = Items.Lanky in ownedItems or self.startkong == Kongs.lanky
        self.tiny = Items.Tiny in ownedItems or self.startkong == Kongs.tiny
        self.chunky = Items.Chunky in ownedItems or self.startkong == Kongs.chunky

        self.blast = Items.BaboonBlast in ownedItems and self.donkey
        self.strongKong = Items.StrongKong in ownedItems and self.donkey
        self.grab = Items.GorillaGrab in ownedItems and self.donkey
        self.charge = Items.ChimpyCharge in ownedItems and self.diddy
        self.jetpack = Items.RocketbarrelBoost in ownedItems and self.diddy
        self.spring = Items.SimianSpring in ownedItems and self.diddy
        self.handstand = Items.Orangstand in ownedItems and self.lanky
        self.balloon = Items.BaboonBalloon in ownedItems and self.lanky
        self.sprint = Items.OrangstandSprint in ownedItems and self.lanky
        self.mini = Items.MiniMonkey in ownedItems and self.tiny
        self.twirl = Items.PonyTailTwirl in ownedItems and self.tiny
        self.monkeyport = Items.Monkeyport in ownedItems and self.tiny
        self.hunkyChunky = Items.HunkyChunky in ownedItems and self.chunky
        self.punch = Items.PrimatePunch in ownedItems and self.chunky
        self.gorillaGone = Items.GorillaGone in ownedItems and self.chunky

        self.coconut = Items.Coconut in ownedItems and self.donkey
        self.peanut = Items.Peanut in ownedItems and self.diddy
        self.grape = Items.Grape in ownedItems and self.lanky
        self.feather = Items.Feather in ownedItems and self.tiny
        self.pineapple = Items.Pineapple in ownedItems and self.chunky

        self.bongos = Items.Bongos in ownedItems and self.donkey
        self.guitar = Items.Guitar in ownedItems and self.diddy
        self.trombone = Items.Trombone in ownedItems and self.lanky
        self.saxophone = Items.Saxophone in ownedItems and self.tiny
        self.triangle = Items.Triangle in ownedItems and self.chunky

        self.nintendoCoin = Items.NintendoCoin in ownedItems
        self.rarewareCoin = Items.RarewareCoin in ownedItems

        self.camera = Items.CameraAndShockwave in ownedItems
        self.shockwave = Items.CameraAndShockwave in ownedItems

        self.JapesKey = Items.JungleJapesKey in ownedItems
        self.AztecKey = Items.AngryAztecKey in ownedItems
        self.FactoryKey = Items.FranticFactoryKey in ownedItems
        self.GalleonKey = Items.GloomyGalleonKey in ownedItems
        self.ForestKey = Items.FungiForestKey in ownedItems
        self.CavesKey = Items.CrystalCavesKey in ownedItems
        self.CastleKey = Items.CreepyCastleKey in ownedItems
        self.HelmKey = Items.HideoutHelmKey in ownedItems

        self.Slam = len([x for x in ownedItems if x == Items.ProgressiveSlam])
        self.GoldenBananas = len([x for x in ownedItems if x == Items.GoldenBanana])
        self.BananaFairies = len([x for x in ownedItems if x == Items.BananaFairy])
        self.BananaMedals = len([x for x in ownedItems if x == Items.BananaMedal])
        self.BattleCrowns = len([x for x in ownedItems if x == Items.BattleCrown])

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

# Initialize logic variables, for now assume start with donkey
LogicVariables = LogicVarHolder(Kongs.donkey)

#Import regions from logic files
Regions = {}
Regions.update(LogicFiles.DKIsles.Regions)
Regions.update(LogicFiles.JungleJapes.Regions)
Regions.update(LogicFiles.AngryAztec.Regions)
Regions.update(LogicFiles.FranticFactory.Regions)
Regions.update(LogicFiles.GloomyGalleon.Regions)
Regions.update(LogicFiles.FungiForest.Regions)
Regions.update(LogicFiles.CrystalCaves.Regions)
Regions.update(LogicFiles.CreepyCastle.Regions)
Regions.update(LogicFiles.HideoutHelm.Regions)
Regions.update(LogicFiles.Shops.Regions)
