"""Shuffle the final boss location within the game."""

from randomizer.Lists.ShipLocations import ship_locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import TransitionFront


def ShuffleShip(spoiler):
    """Shuffle ship function based on settings."""
    spoiler.ship_location_index = None
    spoiler.ship_name = ""
    if not spoiler.settings.ship_location_rando:
        return
    loc_count = len(ship_locations)
    index = spoiler.settings.random.randrange(loc_count)
    loc = ship_locations[index]
    spoiler.ship_name = loc.name
    if loc.is_vanilla:
        return
    spoiler.ship_location_index = index
    # Remove the existing link between IslesMain and KRool
    for reg in spoiler.RegionList:
        spoiler.RegionList[reg].exits = [x for x in spoiler.RegionList[reg].exits if x.dest != Regions.KRool]
    # Add the new link
    spoiler.RegionList[loc.region].exits.append(TransitionFront(Regions.KRool, lambda l: (l.CanAccessKRool() and loc.logic(l)) or l.assumeKRoolAccess))
