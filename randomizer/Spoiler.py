"""Spoiler class and functions."""

from randomizer.Location import LocationList
from randomizer.Item import ItemList


class Spoiler:
    """Class which contains all spoiler data passed into and out of randomizer."""

    def __init__(self, settings):
        """Initialize spoiler just with settings."""
        self.settings = settings
        self.locations = {}
        self.playthrough = []

    def UpdateLocations(self, locations):
        """Update location list for what was produced by the fill."""
        self.locations = locations.copy()

    def UpdatePlaythrough(self, playthroughLocations):
        """Write playthrough as a list of dicts of location/item pairs."""
        self.playthrough = []
        for sphere in playthroughLocations:
            newSphere = {}
            for locationId in sphere:
                location = self.locations[locationId]
                newSphere[location.name] = ItemList[location.item].name
            self.playthrough.append(newSphere)
