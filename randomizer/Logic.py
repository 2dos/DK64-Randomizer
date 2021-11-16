from LogicClasses import Kongs
import LogicFiles.DKIsles

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
        
        self.BluePrints = []

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
        self.donkey = "donkey" in ownedItems or self.startkong == Kongs.donkey
        self.diddy = "diddy" in ownedItems or self.startkong == Kongs.diddy
        self.lanky = "lanky" in ownedItems or self.startkong == Kongs.lanky
        self.tiny = "tiny" in ownedItems or self.startkong == Kongs.tiny
        self.chunky = "chunky" in ownedItems or self.startkong == Kongs.chunky

        self.blast = "Baboon Blast" in ownedItems and self.donkey
        self.strongKong = "Strong Kong" in ownedItems and self.donkey
        self.grab = "Gorilla Grab" in ownedItems and self.donkey
        self.charge = "Chimpy Charge" in ownedItems and self.diddy
        self.jetpack = "Rocketbarrel Boost" in ownedItems and self.diddy
        self.spring = "Simian Spring" in ownedItems and self.diddy
        self.handstand = "Orangstand" in ownedItems and self.lanky
        self.balloon = "Baboon Balloon" in ownedItems and self.lanky
        self.sprint = "Orangstand Sprint" in ownedItems and self.lanky
        self.mini = "Mini Monkey" in ownedItems and self.tiny
        self.twirl = "Pony Tail Twirl" in ownedItems and self.tiny
        self.monkeyport = "Monkeyport" in ownedItems and self.tiny
        self.hunkyChunky = "Hunky Chunky" in ownedItems and self.chunky
        self.punch = "Primate Punch" in ownedItems and self.chunky
        self.gorillaGone = "Gorilla Gone" in ownedItems and self.chunky

        self.coconut = "Coconut" in ownedItems and self.donkey
        self.peanut = "Peanut" in ownedItems and self.diddy
        self.grape = "Grape" in ownedItems and self.lanky
        self.feather = "Feather" in ownedItems and self.tiny
        self.pineapple = "Pineapple" in ownedItems and self.chunky

        self.bongos = "Bongos" in ownedItems and self.donkey
        self.guitar = "Guitar" in ownedItems and self.diddy
        self.trombone = "Trombone" in ownedItems and self.lanky
        self.saxophone = "Saxophone" in ownedItems and self.tiny
        self.triangle = "Triangle" in ownedItems and self.chunky

        self.nintendoCoin = "Nintendo Coin" in ownedItems
        self.rarewareCoin = "Rareware Coin" in ownedItems

        self.camera = "Camera and Shockwave" in ownedItems
        self.shockwave = "Camera and Shockwave" in ownedItems

        self.JapesKey = "Jungle Japes Key" in ownedItems
        self.AztecKey = "Angry Aztec Key" in ownedItems
        self.FactoryKey = "Frantic Factory Key" in ownedItems
        self.GalleonKey = "Gloomy Galleon Key" in ownedItems
        self.ForestKey = "Fungi Forest Key" in ownedItems
        self.CavesKey = "Crystal Caves Key" in ownedItems
        self.CastleKey = "Creepy Castle Key" in ownedItems
        self.HelmKey = "Hideout Helm Key" in ownedItems

        self.Slam = len([x for x in ownedItems if x == "Progressive Slam"])
        self.GoldenBananas = len([x for x in ownedItems if x == "Golden Banana"])
        self.BananaFairies = len([x for x in ownedItems if x == "Banana Fairies"])
        self.BananaMedals = len([x for x in ownedItems if x == "Banana Medals"])

        self.BluePrints = [x for x in ownedItems if "Blueprint" in x]

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

# Initialize logic variables, for now assume start with donkey
LogicVariables = LogicVarHolder(Kongs.donkey)

#Import regions from logic files
Regions = {}
Regions.update(LogicFiles.DKIsles.Regions)
