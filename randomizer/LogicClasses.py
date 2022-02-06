"""Contains classes used in the logic system."""
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions


class LocationLogic:
    """Logic for a location."""

    def __init__(self, id, logic):
        """Initialize with given parameters."""
        self.id = id
        self.logic = logic  # Lambda function for accessibility


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

class Collectible:
    """Class used for colored bananas and banana coins."""

    def __init__(self, type, kong, logic, coords, amount=1):
        """Initialize with given parameters."""
        self.type = type
        self.kong = kong
        self.logic = logic
        self.amount = amount
        self.coords = coords
        self.added = False


class Region:
    """Region contains shufflable locations, events, and transitions to other regions."""

    def __init__(self, name, level, tagbarrel, deathwarp, locations, events, transitionFronts):
        """Initialize with given parameters."""
        self.name = name
        self.level = level
        self.tagbarrel = tagbarrel
        self.locations = locations
        self.events = events
        self.exits = transitionFronts # In the context of a region, exits are how you leave the region

        # If possible to die in this region, add an exit to where dying will take you
        # deathwarp is also set to none in regions in which a deathwarp would take you to itself
        # Or if there is loading-zone-less free access to the region it would take you to already
        if deathwarp is not None:
            # If deathwarp is itself an exit class (necessary when deathwarp requires custom logic) just add it directly
            if isinstance(deathwarp, TransitionFront):
                self.exits.append(deathwarp)
            else:
                # If deathwarp is -1, indicates to use the default value for it, which is the starting area of the level
                if deathwarp == -1:
                    deathwarp = self.GetDefaultDeathwarp()
                self.exits.append(TransitionFront(deathwarp, lambda l: True))

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
        elif kong == Kongs.chunky:
            return self.chunkyAccess
        else:  # kongs == Kongs.rainbow, just need to check if any kong has access
            return self.donkeyAccess or self.diddyAccess or self.lankyAccess or self.tinyAccess or self.chunkyAccess

    def ResetAccess(self):
        """Clear access for all kongs."""
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False

    def GetDefaultDeathwarp(self):
        """Get the default deathwarp depending on the region's level."""
        if self.level == Levels.DKIsles:
            return Regions.IslesMain
        elif self.level == Levels.JungleJapes:
            return Regions.JungleJapesMain
        elif self.level == Levels.AngryAztec:
            return Regions.AngryAztecStart
        elif self.level == Levels.FranticFactory:
            return Regions.FranticFactoryStart
        elif self.level == Levels.GloomyGalleon:
            return Regions.GloomyGalleonStart
        elif self.level == Levels.FungiForest:
            return Regions.FungiForestStart
        elif self.level == Levels.CrystalCaves:
            return Regions.CrystalCavesMain
        elif self.level == Levels.CreepyCastle:
            return Regions.CreepyCastleMain
        elif self.level == Levels.HideoutHelm:
            return Regions.HideoutHelmStart

class TransitionBack:
    """The exited side of a transition between regions."""

    def __init__(self, regionId, exitName):
        """Initialize with given parameters."""
        self.regionId = regionId
        self.name = exitName

class TransitionFront:
    """The entered side of a transition between regions."""

    def __init__(self, dest, logic, exitShuffleId=None, assumed=False):
        """Initialize with given parameters."""
        self.dest = dest # Planning to remove this
        # self.back = back
        self.logic = logic  # Lambda function for accessibility
        # self.shufflable = shufflable
        self.exitShuffleId = exitShuffleId # Planning to remove this
        self.assumed = assumed  # Indicates this is an assumed exit attached to the root
