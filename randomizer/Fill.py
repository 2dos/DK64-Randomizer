"""Module used to distribute items randomly."""
import copy
import random

import randomizer.ItemPool as ItemPool
import randomizer.Logic as Logic
from randomizer.Enums.Items import Items
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Item import ItemList
from randomizer.Logic import LogicVariables


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
            # If we want to generate the playthrough and the item is a playthrough item, add it to the sphere
            if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
                # Banana hoard in a sphere by itself
                if location.item == Items.BananaHoard:
                    sphere = [location]
                    break
                sphere.append(location)
            # If we're checking beatability, just want to know if we have access to the banana hoard
            if searchType == SearchMode.CheckBeatable and location.item == Items.BananaHoard:
                return True
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

            startRegion = Logic.Regions[Regions.Start]
            startRegion.id = Regions.Start
            regionPool = [startRegion]
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
                        newRegion = Logic.Regions[exit.dest]
                        newRegion.id = exit.dest
                        regionPool.append(newRegion)
                # Finally check accessibility for collectibles
                if region.id in Logic.CollectibleRegions.keys():
                    for collectible in Logic.CollectibleRegions[region.id]:
                        if not collectible.added and kong == collectible.kong and collectible.logic(LogicVariables):
                            LogicVariables.AddCollectible(collectible, region.level)

    if searchType == SearchMode.GetReachable:
        return accessible
    elif searchType == SearchMode.CheckBeatable:
        # If the search has completed and banana hoard has not been found, game is unbeatable
        return False
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
    return 0


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
    return 0


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
    return 0


def PlaceItems(algorithm, itemsToPlace, ownedItems=[]):
    """Places items using given algorithm."""
    if algorithm == "assumed":
        return AssumedFill(itemsToPlace, ownedItems)
    elif algorithm == "forward":
        return ForwardFill(itemsToPlace, ownedItems)


def Fill(algorithm):
    """Place all items."""
    retries = 0
    while retries < 5:
        try:
            # First place win condition item at K Rool
            Logic.Regions[Regions.KRool].GetLocation("Banana Hoard").PlaceItem(Items.BananaHoard)
            # Then place priority (logically very important) items
            highPriorityUnplaced = PlaceItems(algorithm, ItemPool.HighPriorityItems(), ItemPool.HighPriorityAssumedItems())
            if highPriorityUnplaced > 0:
                raise Exception(str(highPriorityUnplaced) + " unplaced high priority items.")
            # Then place blueprints
            Reset()
            blueprintsUnplaced = PlaceItems(algorithm, ItemPool.Blueprints(), ItemPool.BlueprintAssumedItems())
            if blueprintsUnplaced > 0:
                raise Exception(str(blueprintsUnplaced) + " unplaced blueprints.")
            # Then place the rest of items
            Reset()
            lowPriorityUnplaced = PlaceItems(algorithm, ItemPool.LowPriorityItems(), ItemPool.ExcessItems())
            if lowPriorityUnplaced > 0:
                raise Exception(str(lowPriorityUnplaced) + " unplaced low priority items.")
            # Finally place excess items fully randomly
            excessUnplaced = RandomFill(ItemPool.ExcessItems())
            if excessUnplaced > 0:
                raise Exception(str(excessUnplaced) + " unplaced excess items.")
            # Check if game is beatable
            Reset()
            if not GetAccessibleLocations([], SearchMode.CheckBeatable):
                raise Exception("Game unbeatable after placing all items.")
            # Generate and display the playthrough
            Reset()
            PlaythroughLocations = GetAccessibleLocations([], SearchMode.GeneratePlaythrough)
            i = 0
            spoiler_log = []
            for sphere in PlaythroughLocations:
                spoiler_log.append("\nSphere " + str(i))
                i += 1
                for location in sphere:
                    spoiler_log.append(location.name + ": " + ItemList[location.item].name)
            return spoiler_log
        except Exception as ex:
            if retries == 4:
                print("Fill failed, out of retries.")
                raise ex
            else:
                retries += 1
                print(ex)
                print("Fill failed. Retrying. Tries: " + str(retries))
