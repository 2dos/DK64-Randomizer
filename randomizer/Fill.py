import random

import Logic
from Logic import LogicVariables

# Search to find all reachable locations given owned items
def GetAccessibleLocations(ownedItems):
    accessible = []
    items = ownedItems.copy()

    newLocations = []
    newEvents = []
    firstIteration = True
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or len(newEvents) > 0 or firstIteration:
        firstIteration = False
        # Add items and events from the last search iteration
        for location in newLocations:
            accessible.append(location)
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                items.append(location.item)
        LogicVariables.Events.extend(newEvents)
        # Reset new lists
        newLocations = []
        newEvents = []
        # Update based on new items
        LogicVariables.Update(items)

        # Do a search for each owned kong
        for kong in LogicVariables.GetKongs():
            LogicVariables.SetKong(kong)

            # Starting point
            regionPool = [Logic.Regions["Start"]]
            addedRegions = ["Start"]

            # Loop for each region until no more accessible regions found
            while len(regionPool) > 0:
                region = regionPool.pop()

                region.UpdateAccess(kong, LogicVariables) # Set that this kong has access to this region

                # Check accessibility for each location in this region
                for location in region.locations:
                    if location not in accessible and location.logic(LogicVariables, region):
                        newLocations.append(location)
                # Check accessibility for each event in this region
                for event in region.events:
                    if event.name not in LogicVariables.Events and event.logic(LogicVariables, region):
                        newEvents.append(event.name)
                # Check accessibility for each exit in this region
                for exit in region.exits:
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if exit.dest not in addedRegions and exit.logic(LogicVariables, region):
                        addedRegions.append(exit.dest)
                        regionPool.append(Logic.Regions[exit.dest])

                # No regions left, check if there are any this kong has access to
                # through a tag barrel but has not yet visited.
                if len(regionPool) == 0:
                    tagAccess = [x for x in Logic.Regions.values() if x.name not in addedRegions and x.HasAccess(kong)]
                    addedRegions.extend([x.name for x in tagAccess])
                    regionPool = tagAccess


    return accessible

# Assumed fill algorithm for item placement
def AssumedFill():
    # Initialize item pool
    itemPool = ["a", "b", "Golden Banana", "Golden Banana", "Golden Banana"]
    random.shuffle(itemPool)

    # While there are items to place
    while len(itemPool) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemPool.pop()
        LogicVariables.Reset()
        reachable = GetAccessibleLocations(itemPool)
        # for location in reachable:
        #     itemName = "None" if location.item == None else location.item
        #     print(location.name + " " + itemName)
        reachable = [x for x in reachable if x.item == None]
        # If there are no empty reachable locations, reached a dead end
        if len(reachable) == 0:
            break
        # Get a random, empty, reachable location and place the item there
        random.shuffle(reachable)
        location = reachable.pop()
        location.PlaceItem(item)
