"""Module used to distribute items randomly."""
import random
import copy

from randomizer.Enums.Regions import Regions
from randomizer.Enums.Items import Items
from randomizer.Enums.SearchMode import SearchMode
import randomizer.Logic as Logic
from randomizer.Logic import LogicVariables
from randomizer.Item import ItemList
import randomizer.ItemPool as ItemPool


def KongSearch(kong, logicVariables, accessibleIds, start, Regions, collectibleRegions, newLocations, newLocationIds):
    """Find all locations accessible by this kong with current logic variables."""
    logicVariables.SetKong(kong)
    newEvents = []

    startRegion = Regions[start]
    startRegion.id = start
    regionPool = [startRegion]
    addedRegions = [start]

    tagAccess = [(key, value) for (key, value) in Regions.items() if value.HasAccess(kong) and key not in addedRegions]
    addedRegions.extend([x[0] for x in tagAccess])  # first value is the region key
    regionPool.extend([x[1] for x in tagAccess])  # second value is the region itself

    # Loop for each region until no more accessible regions found
    while len(regionPool) > 0:
        region = regionPool.pop()

        region.UpdateAccess(kong, logicVariables)  # Set that this kong has access to this region
        logicVariables.UpdateCurrentRegionAccess(region)  # Set in logic as well

        # Check accessibility for each location in this region
        for location in region.locations:
            if (
                location.logic(logicVariables)
                and location.name not in newLocationIds
                and location.name not in accessibleIds
            ):
                newLocations.append(location)
                newLocationIds.append(location.name)
        # Check accessibility for each event in this region
        for event in region.events:
            if event.name not in logicVariables.Events and event.logic(logicVariables):
                newEvents.append(event.name)
                logicVariables.Events.append(event.name)
        # Check accessibility for each exit in this region
        for exit in region.exits:
            # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
            if exit.dest not in addedRegions and exit.logic(logicVariables):
                addedRegions.append(exit.dest)
                newRegion = Regions[exit.dest]
                newRegion.id = exit.dest
                regionPool.append(newRegion)
        # Finally check accessibility for collectibles
        if region.id in collectibleRegions.keys():
            for collectible in collectibleRegions[region.id]:
                if (
                    not collectible.added
                    and logicVariables.IsKong(collectible.kong)
                    and collectible.logic(logicVariables)
                ):
                    logicVariables.AddCollectible(collectible, region.level)

    return Regions, collectibleRegions, newLocations, newLocationIds, newEvents


def GetAccessibleLocations(ownedItems, searchType=SearchMode.GetReachable):
    """Search to find all reachable locations given owned items."""
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
            if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
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
            tempRegions, tempCollectibleRegions, tempNew, tempNewIds, newEvents = KongSearch(
                kong,
                copy.deepcopy(LogicVariables),
                accessibleIds.copy(),
                Regions.Start,
                Logic.Regions.copy(),
                Logic.CollectibleRegions.copy(),
                newLocations.copy(),
                newLocationIds.copy(),
            )
            # Update regional access from search
            Logic.UpdateAllRegionsAccess(tempRegions)
            Logic.UpdateCollectiblesAdded(tempCollectibleRegions)
            # Add new things found in search
            # list(set()) removes redundancies
            newLocations.extend(tempNew)
            newLocations = list(set(newLocations))
            newLocationIds.extend(tempNewIds)
            newLocationIds = list(set(newLocationIds))
            if len(newEvents) > 0:
                eventAdded = True
                LogicVariables.Events.extend(newEvents)
                LogicVariables.Events = list(set(LogicVariables.Events))

    if searchType == SearchMode.GetReachable:
        return accessible
    elif searchType == SearchMode.GeneratePlaythrough:
        return playthroughLocations


def RandomFill(itemsToPlace):
    """Randomly place given items in any location disregarding logic."""
    random.shuffle(itemsToPlace)
    # Get all remaining empty locations
    empty = []
    for region in Logic.Regions.values():
        for location in region.locations:
            if location.item is None:
                empty.append(location)
    random.shuffle(empty)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        if len(empty) == 0:
            return len(itemsToPlace)
        item = itemsToPlace.pop()
        location = empty.pop()
        location.PlaceItem(item)


def Reset():
    """Reset logic variables and region info that should be reset before a search."""
    LogicVariables.Reset()
    Logic.ResetRegionAccess()
    Logic.ResetCollectibleRegions()


def ForwardFill(itemsToPlace, ownedItems=[]):
    """Forward fill algorithm for item placement."""
    random.shuffle(itemsToPlace)
    ownedItems = ownedItems.copy()
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Find a random empty location which is reachable with current items
        reachable = GetAccessibleLocations(ownedItems.copy())
        reachable = [x for x in reachable if x.item is None]
        if len(reachable) == 0:  # If there are no empty reachable locations, reached a dead end
            return len(itemsToPlace)
        random.shuffle(reachable)
        location = reachable.pop()
        # Get a random item and place it there, also adding to owned items
        item = itemsToPlace.pop()
        ownedItems.append(item)
        location.PlaceItem(item)


def AssumedFill(itemsToPlace, ownedItems=[]):
    """Assumed fill algorithm for item placement."""
    random.shuffle(itemsToPlace)
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemsToPlace.pop()
        ownedItems = itemsToPlace.copy()
        ownedItems.extend(ownedItems)
        Reset()
        reachable = GetAccessibleLocations(ownedItems.copy())
        reachable = [x for x in reachable if x.item is None]
        # If there are no empty reachable locations, reached a dead end
        if len(reachable) == 0:
            return len(itemsToPlace)
        # Get a random, empty, reachable location and place the item there
        random.shuffle(reachable)
        location = reachable.pop()
        location.PlaceItem(item)


def PlaceItems(algorithm, itemsToPlace, ownedItems=[]):
    """Places items using given algorithm."""
    if algorithm == "assumed":
        AssumedFill(itemsToPlace, ownedItems)
    elif algorithm == "forward":
        ForwardFill(itemsToPlace, ownedItems)


def Fill(algorithm):
    """Place all items."""
    # First place win condition item at K Rool
    Logic.Regions[Regions.KRool].GetLocation("Banana Hoard").PlaceItem(Items.BananaHoard)
    # Then place priority (logically very important) items
    highPriorityUnplaced = PlaceItems(algorithm, ItemPool.HighPriorityItems(), ItemPool.HighPriorityAssumedItems())
    # Then place blueprints
    Reset()
    blueprintsUnplaced = PlaceItems(algorithm, ItemPool.Blueprints(), ItemPool.BlueprintAssumedItems())
    # Then place the rest of items
    Reset()
    lowPriorityUnplaced = PlaceItems(algorithm, ItemPool.LowPriorityItems(), ItemPool.ExcessItems())
    # Finally place excess items fully randomly
    excessUnplaced = RandomFill(ItemPool.ExcessItems())
    # Generate and display the playthrough
    Reset()
    PlaythroughLocations = GetAccessibleLocations([], SearchMode.GeneratePlaythrough)
    i = 0
    for sphere in PlaythroughLocations:
        print("\nSphere " + str(i))
        i += 1
        for location in sphere:
            print(location.name + ": " + ItemList[location.item].name)
