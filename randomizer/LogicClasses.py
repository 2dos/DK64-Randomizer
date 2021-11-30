"""Contains classes used in the logic system."""
from Enums.Kongs import Kongs


class Location:
    """A shufflable location at which a random item can be placed."""

    def __init__(self, name, logic):
        """Initialize with given parameters."""
        self.name = name
        self.logic = logic  # Lambda function for accessibility
        self.item = None

    def PlaceItem(self, item):
        """Place item at this location."""
        self.item = item


class Event:
    """Event within a region.

    Events act as statically placed items
    For example, if Lanky must press a button in region x to open something in region y,
    that can be represented as a button press event in region x which is checked for in region y.
    """

    def __init__(self, name, logic):
        """Initialize with given parameters."""
        self.name = name
        self.logic = logic  # Lambda function for accessibility


class Exit:
    """Exit from one region to another."""

    def __init__(self, dest, logic):
        """Initialize with given parameters."""
        self.dest = dest
        self.logic = logic  # Lambda function for accessibility


class Collectible:
    """Class used for colored bananas and banana coins."""

    def __init__(self, type, kong, logic, amount=1):
        """Initialize with given parameters."""
        self.type = type
        self.kong = kong
        self.logic = logic
        self.amount = amount
        self.added = False


class Region:
    """Region contains shufflable locations, events, and exits to other regions."""

    def __init__(self, name, level, tagbarrel, locations, events, exits):
        """Initialize with given parameters."""
        self.name = name
        self.level = level
        self.tagbarrel = tagbarrel
        self.locations = locations
        self.events = events
        self.exits = exits

        # Initially assume no access from any kong
        self.ResetAccess()

    def UpdateAccess(self, kong, logicVariables):
        """Set that given kong has access to this region."""
        # If this region contains a tag barrel, all owned kongs also have access
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

    def UpdateAccessFromRegion(self, region):
        """Set access to region from another region."""
        self.donkeyAccess = self.donkeyAccess or region.donkeyAccess
        self.diddyAccess = self.diddyAccess or region.diddyAccess
        self.lankyAccess = self.lankyAccess or region.lankyAccess
        self.tinyAccess = self.tinyAccess or region.tinyAccess
        self.chunkyAccess = self.chunkyAccess or region.chunkyAccess

    def HasAccess(self, kong):
        """Check if given kong has access through this area.

        Used if a kong has access through a tag barrel only.
        """
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

    def ResetAccess(self):
        """Clear access for all kongs."""
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

    def GetLocation(self, location):
        """Get a specific location from this region given its name."""
        return [x for x in self.locations if x.name == location][0]
