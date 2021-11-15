from enum import Enum

class Kongs(Enum):
    donkey = 1
    diddy = 2
    lanky = 3
    tiny = 4
    chunky = 5

class LogicLocation:
    def __init__(self, name, logic):
        self.name = name
        self.logic = logic
        self.item = None

    def PlaceItem(self, item):
        self.item = item

class Event:
    def __init__(self, name, logic):
        self.name = name
        self.logic = logic

class Exit:
    def __init__(self, dest, logic):
        self.dest = dest
        self.logic = logic

class Region:
    def __init__(self, name, tagbarrel, locations, events, exits):
        self.name = name
        self.tagbarrel = tagbarrel
        self.locations = locations
        self.events = events
        self.exits = exits

        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

    def UpdateAccess(self, kong, logicVariables):
        if self.tagbarrel:
            self.donkeyAccess = logicVariables.donkey
            self.diddyAccess = logicVariables.diddy
            self.lankyAccess = logicVariables.lanky
            self.tinyAccess = logicVariables.tiny
            self.chunkyAccess = logicVariables.chunky
        else:
            if kong == Kongs.donkey:
                self.donkeyAccess = True
            elif kong == Kongs.diddy:
                self.diddyAccess = True
            elif kong == Kongs.lanky:
                self.lankyAccess = True
            elif kong == Kongs.tiny:
                self.tinyAccess = True
            else:
                self.chunkyAccess = True
    
    def HasAccess(self, kong):
        if kong == Kongs.donkey:
            return self.donkeyAccess
        elif kong == Kongs.diddy:
            return self.diddyAccess
        elif kong == Kongs.lanky:
            return self.lankyAccess
        elif kong == Kongs.tiny:
            return self.tinyAccess
        else:
            return self.chunkyAccess
