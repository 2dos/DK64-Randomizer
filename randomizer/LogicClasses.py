"""Contains classes used in the logic system."""
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Time import Time


class LocationLogic:
    """Logic for a location."""

    def __init__(self, id, logic, bonusBarrel=None):
        """Initialize with given parameters."""
        self.id = id
        self.logic = logic  # Lambda function for accessibility
        self.bonusBarrel = bonusBarrel  # Uses MinigameType enum


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

    def __init__(self, type, kong, logic, coords, amount=1, enabled=True, vanilla=True):
        """Initialize with given parameters."""
        self.type = type
        self.kong = kong
        self.logic = logic
        self.amount = amount
        self.coords = coords  # Null for vanilla collectibles for now. For custom, use (x,y,z) format
        self.added = False
        self.enabled = enabled
        self.vanilla = vanilla


class Region:
    """Region contains shufflable locations, events, and transitions to other regions."""

    def __init__(self, name, hint_name, level, tagbarrel, deathwarp, locations, events, transitionFronts, restart=None):
        """Initialize with given parameters."""
        self.name = name
        self.hint_name = hint_name
        self.level = level
        self.tagbarrel = tagbarrel
        self.deathwarp = None
        self.locations = locations
        self.events = events
        self.exits = transitionFronts  # In the context of a region, exits are how you leave the region
        self.restart = restart

        self.dayAccess = False
        self.nightAccess = False

        # If possible to die in this region, add an exit to where dying will take you
        # deathwarp is also set to none in regions in which a deathwarp would take you to itself
        # Or if there is loading-zone-less free access to the region it would take you to already
        if deathwarp is not None:
            # If deathwarp is itself an exit class (necessary when deathwarp requires custom logic) just add it directly
            if isinstance(deathwarp, TransitionFront):
                self.deathwarp = deathwarp
            else:
                # If deathwarp is -1, indicates to use the default value for it, which is the starting area of the level
                if deathwarp == -1:
                    deathwarp = self.GetDefaultDeathwarp()
                self.deathwarp = TransitionFront(deathwarp, lambda l: True)

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
        else:  # kongs == Kongs.any, just need to check if any kong has access
            return self.donkeyAccess or self.diddyAccess or self.lankyAccess or self.tinyAccess or self.chunkyAccess

    def ResetAccess(self):
        """Clear access variables set during search."""
        # Kong access
        self.donkeyAccess = False
        self.diddyAccess = False
        self.lankyAccess = False
        self.tinyAccess = False
        self.chunkyAccess = False
        # Time access
        self.dayAccess = False
        self.nightAccess = False

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

    def __init__(self, regionId, exitName, spoilerName, reverse=None):
        """Initialize with given parameters."""
        self.regionId = regionId  # Destination region
        self.name = exitName
        self.spoilerName = spoilerName
        self.reverse = reverse  # Indicates a reverse direction transition, if one exists


class TransitionFront:
    """The entered side of a transition between regions."""

    def __init__(self, dest, logic, exitShuffleId=None, assumed=False, time=Time.Both):
        """Initialize with given parameters."""
        self.dest = dest  # Planning to remove this
        self.logic = logic  # Lambda function for accessibility
        self.exitShuffleId = exitShuffleId  # Planning to remove this
        self.time = time
        self.assumed = assumed  # Indicates this is an assumed exit attached to the root


class Sphere:
    """A randomizer concept often used in spoiler logs.

    A 'sphere' is a collection of locations and items that are accessible
    or obtainable with only the items available from earlier, smaller spheres.
    Sphere 0 items are what you start with in a seed, sphere 1 items can be
    obtained with those items, sphere 2 items can be obtained with sphere 0
    and sphere 1 items, and so on.
    """

    def __init__(self):
        """Initialize with given parameters."""
        self.seedBeaten = False
        self.availableGBs = 0
        self.locations = []
