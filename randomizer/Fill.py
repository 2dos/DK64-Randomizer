import random

import Logic
from Logic import LogicVariables
from Enums.Regions import Regions
from Enums.Items import Items

# Search to find all reachable locations given owned items
def GetAccessibleLocations(ownedItems):
    accessible = []
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
                ownedItems.append(location.item)
        LogicVariables.Events.extend(newEvents)
        # Reset new lists
        newLocations = []
        newEvents = []
        # Update based on new items
        LogicVariables.Update(ownedItems)

        # Do a search for each owned kong
        for kong in LogicVariables.GetKongs():
            LogicVariables.SetKong(kong)

            # Starting point
            regionPool = [Logic.Regions[Regions.Start]]
            addedRegions = [Regions.Start]

            # Loop for each region until no more accessible regions found
            while len(regionPool) > 0:
                region = regionPool.pop()

                region.UpdateAccess(kong, LogicVariables) # Set that this kong has access to this region
                LogicVariables.UpdateCurrentRegionAccess(region) # Set in logic as well

                # Check accessibility for each location in this region
                for location in region.locations:
                    if location not in accessible and location not in newLocations and location.logic(LogicVariables):
                        newLocations.append(location)
                # Check accessibility for each event in this region
                for event in region.events:
                    if event.name not in LogicVariables.Events and event.name not in newEvents and event.logic(LogicVariables):
                        newEvents.append(event.name)
                # Check accessibility for each exit in this region
                for exit in region.exits:
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if exit.dest not in addedRegions and exit.logic(LogicVariables):
                        addedRegions.append(exit.dest)
                        regionPool.append(Logic.Regions[exit.dest])

                # No regions left, check if there are any this kong has access to
                # through a tag barrel but has not yet visited.
                if len(regionPool) == 0:
                    # tagAccess is a list of tuples of keys and values for applicable regions
                    tagAccess = [(key, value) for (key, value) in Logic.Regions.items() if key not in addedRegions and value.HasAccess(kong)]
                    addedRegions.extend([x[0] for x in tagAccess]) # first value is the region key
                    regionPool = [x[1] for x in tagAccess] # second value is the region itself

    return accessible

# Assumed fill algorithm for item placement
def AssumedFill(itemPool):
    random.shuffle(itemPool)
    # While there are items to place
    while len(itemPool) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemPool.pop()
        LogicVariables.Reset()
        reachable = GetAccessibleLocations(itemPool.copy())
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

def Fill(itemPool):
    Logic.Regions[Regions.KRool].GetLocation("Banana Hoard").PlaceItem(Items.BananaHoard)
    AssumedFill(itemPool)
