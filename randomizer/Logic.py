from LogicClasses import Kongs
import LogicFiles.DKIsles

class LogicVarHolder:

    def __init__(self, startkong):
        self.startkong = startkong
        self.Reset()

    def Reset(self):
        self.donkey = self.startkong == Kongs.donkey
        self.diddy = self.startkong == Kongs.diddy
        self.lanky = self.startkong == Kongs.lanky
        self.tiny = self.startkong == Kongs.tiny
        self.chunky = self.startkong == Kongs.chunky
        self.GoldenBananas = 0

        self.a = False
        self.b = False

        self.Events = []
        self.kong = self.startkong

    def Update(self, ownedItems):
        self.donkey = "donkey" in ownedItems or self.startkong == Kongs.donkey
        self.diddy = "diddy" in ownedItems or self.startkong == Kongs.diddy
        self.lanky = "lanky" in ownedItems or self.startkong == Kongs.lanky
        self.tiny = "tiny" in ownedItems or self.startkong == Kongs.tiny
        self.chunky = "chunky" in ownedItems or self.startkong == Kongs.chunky
        self.GoldenBananas = len([x for x in ownedItems if x == "Golden Banana"])

        self.a = "a" in ownedItems
        self.b = "b" in ownedItems

    def AddEvent(self, event):
        self.Events.append(event)

    # Maps kong name strings to the enum
    kongDict = {
        Kongs.donkey: "donkey",
        Kongs.diddy: "diddy",
        Kongs.lanky: "lanky",
        Kongs.tiny: "tiny",
        Kongs.chunky: "chunky",
    }

    def SetKong(self, kong):
        self.kong = kong

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

LogicVariables = LogicVarHolder(Kongs.donkey)

#Import regions from logic files
Regions = {}
Regions.update(LogicFiles.DKIsles.Regions)
