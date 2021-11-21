import random

import Logic
from Logic import LogicVariables
from Enums.Regions import Regions
from Enums.Items import Items
from Item import ItemList

# Search to find all reachable locations given owned items
def GetAccessibleLocations(ownedItems, searchType=0):
    accessible = []
    accessibleIds = []
    newLocations = []
    playthroughLocations = []
    eventAdded = True
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or eventAdded:
        # Add items and events from the last search iteration
        sphere = []
        for location in newLocations:
            accessible.append(location)
            accessibleIds.append(location.name)
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                ownedItems.append(location.item)
            if searchType == 1 and ItemList[location.item].playthrough:
                if location.item == Items.BananaHoard:
                    sphere = [location]
                    break
                sphere.append(location)
        if len(sphere) > 0:
            playthroughLocations.append(sphere)
            if sphere[0].item == Items.BananaHoard:
                break
        eventAdded = False
        # Reset new lists
        newLocations = []
        newLocationIds = []
        # Update based on new items
        LogicVariables.Update(ownedItems)

        # Do a search for each owned kong
        for kong in LogicVariables.GetKongs():
            LogicVariables.SetKong(kong)

            regionPool = [Logic.Regions[Regions.Start]]
            addedRegions = [Regions.Start]  

            tagAccess = [(key, value) for (key, value) in Logic.Regions.items() if value.HasAccess(kong) and key not in addedRegions]
            addedRegions.extend([x[0] for x in tagAccess]) # first value is the region key
            regionPool.extend([x[1] for x in tagAccess]) # second value is the region itself

            # Loop for each region until no more accessible regions found
            while len(regionPool) > 0:
                region = regionPool.pop()

                region.UpdateAccess(kong, LogicVariables) # Set that this kong has access to this region
                LogicVariables.UpdateCurrentRegionAccess(region) # Set in logic as well

                # Check accessibility for each location in this region
                for location in region.locations:
                    if location.logic(LogicVariables) and location.name not in newLocationIds and location.name not in accessibleIds:
                        newLocations.append(location)
                        newLocationIds.append(location.name)
                # Check accessibility for each event in this region
                for event in region.events:
                    if event.name not in LogicVariables.Events and event.logic(LogicVariables):
                        eventAdded = True
                        LogicVariables.Events.append(event.name)
                # Check accessibility for each exit in this region
                for exit in region.exits:
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if exit.dest not in addedRegions and exit.logic(LogicVariables):
                        addedRegions.append(exit.dest)
                        regionPool.append(Logic.Regions[exit.dest])

    if searchType == 0:
        return accessible
    elif searchType == 1:
        return playthroughLocations

# Reset kong access for all regions
def ResetRegionAccess():
    for region in Logic.Regions.values():
        region.ResetAccess()

# Assumed fill algorithm for item placement
def AssumedFill(itemPool):
    random.shuffle(itemPool)
    # While there are items to place
    while len(itemPool) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemPool.pop()
        LogicVariables.Reset()
        ResetRegionAccess()
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
    LogicVariables.Reset()
    ResetRegionAccess()
    PlaythroughLocations = GetAccessibleLocations([], 1)
    i = 0
    for sphere in PlaythroughLocations:
        print("\nSphere " + str(i))
        i += 1
        for location in sphere:
            print(location.name + ": " + ItemList[location.item].name)
