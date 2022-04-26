"""Module used to distribute items randomly."""
import random

import js
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Settings import Settings
import randomizer.ShuffleExits as ShuffleExits
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList, KongFromItem
from randomizer.Lists.Location import Location, LocationList
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Logic import LogicVarHolder, LogicVariables, STARTING_SLAM
from randomizer.LogicClasses import TransitionFront
from randomizer.Prices import GetPriceOfMoveItem
from randomizer.ShuffleBarrels import BarrelShuffle
from randomizer.ShuffleKasplats import KasplatShuffle
from randomizer.ShuffleWarps import ShuffleWarps


def GetExitLevelExit(settings, region):
    """Get the exit that using the "Exit Level" button will take you to."""
    level = region.level
    # For now, restarts will not be randomized
    # if settings.shuffle_loading_zones == "all" and region.restart is not None:
    #     return ShuffleExits.ShufflableExits[region.restart].shuffledId
    if level == Levels.JungleJapes:
        return ShuffleExits.ShufflableExits[Transitions.JapesToIsles].shuffledId
    elif level == Levels.AngryAztec:
        return ShuffleExits.ShufflableExits[Transitions.AztecToIsles].shuffledId
    elif level == Levels.FranticFactory:
        return ShuffleExits.ShufflableExits[Transitions.FactoryToIsles].shuffledId
    elif level == Levels.GloomyGalleon:
        return ShuffleExits.ShufflableExits[Transitions.GalleonToIsles].shuffledId
    elif level == Levels.FungiForest:
        return ShuffleExits.ShufflableExits[Transitions.ForestToIsles].shuffledId
    elif level == Levels.CrystalCaves:
        return ShuffleExits.ShufflableExits[Transitions.CavesToIsles].shuffledId
    elif level == Levels.CreepyCastle:
        return ShuffleExits.ShufflableExits[Transitions.CastleToIsles].shuffledId


def GetAccessibleLocations(settings, ownedItems, searchType=SearchMode.GetReachable):
    """Search to find all reachable locations given owned items."""
    accessible = []
    newLocations = []
    playthroughLocations = []
    eventAdded = True
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or eventAdded:
        # Add items and events from the last search iteration
        sphere = []
        for locationId in newLocations:
            accessible.append(locationId)
            location = LocationList[locationId]
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                ownedItems.append(location.item)
                # If we want to generate the playthrough and the item is a playthrough item, add it to the sphere
                if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
                    # Banana hoard in a sphere by itself
                    if location.item == Items.BananaHoard:
                        sphere = [locationId]
                        break
                    sphere.append(locationId)
                # If we're checking beatability, just want to know if we have access to the banana hoard
                if searchType == SearchMode.CheckBeatable and location.item == Items.BananaHoard:
                    return True
        if len(sphere) > 0:
            playthroughLocations.append(sphere)
            if LocationList[sphere[0]].item == Items.BananaHoard:
                break
        eventAdded = False
        # Reset new lists
        newLocations = []
        # Update based on new items
        LogicVariables.Update(ownedItems)

        # Do a search for each owned kong
        for kong in LogicVariables.GetKongs():
            LogicVariables.SetKong(kong)

            startRegion = Logic.Regions[Regions.IslesMain]
            startRegion.id = Regions.IslesMain
            regionPool = [startRegion]
            addedRegions = [Regions.IslesMain]

            tagAccess = [(key, value) for (key, value) in Logic.Regions.items() if value.HasAccess(kong) and key not in addedRegions]
            addedRegions.extend([x[0] for x in tagAccess])  # first value is the region key
            regionPool.extend([x[1] for x in tagAccess])  # second value is the region itself

            # Loop for each region until no more accessible regions found
            while len(regionPool) > 0:
                region = regionPool.pop()
                region.UpdateAccess(kong, LogicVariables)  # Set that this kong has access to this region
                LogicVariables.UpdateCurrentRegionAccess(region)  # Set in logic as well

                # Check accessibility for each event in this region
                for event in region.events:
                    if event.name not in LogicVariables.Events and event.logic(LogicVariables):
                        eventAdded = True
                        LogicVariables.Events.append(event.name)
                # Check accessibility for collectibles
                if region.id in Logic.CollectibleRegions.keys():
                    for collectible in Logic.CollectibleRegions[region.id]:
                        if not collectible.added and (kong == collectible.kong or collectible.kong == Kongs.any) and collectible.logic(LogicVariables):
                            LogicVariables.AddCollectible(collectible, region.level)
                # Check accessibility for each location in this region
                for location in region.locations:
                    if location.logic(LogicVariables) and location.id not in newLocations and location.id not in accessible:
                        # If this location is a bonus barrel, must make sure its logic is met as well
                        if location.bonusBarrel and settings.bonus_barrels != "skip":
                            minigame = BarrelMetaData[location.id].minigame
                            if not MinigameRequirements[minigame].logic(LogicVariables):
                                continue
                        # If this location is a blueprint, then make sure this is the correct kong
                        elif LocationList[location.id].type == Types.Blueprint:
                            if not LogicVariables.KasplatAccess(location.id):
                                continue
                        # Any shop item with exception of simian slam has a price
                        elif LocationList[location.id].type == Types.Shop and location.id != Locations.SimianSlam:
                            LogicVariables.PurchaseShopItem(LocationList[location.id])
                        newLocations.append(location.id)
                # Check accessibility for each exit in this region
                exits = region.exits.copy()
                # If loading zones are shuffled, the "Exit Level" button in the pause menu could potentially take you somewhere new
                if settings.shuffle_loading_zones and region.level != Levels.DKIsles and region.level != Levels.Shops:
                    levelExit = GetExitLevelExit(settings, region)
                    # When shuffling levels, unplaced level entrances will have no destination yet
                    if levelExit is not None:
                        dest = ShuffleExits.ShufflableExits[levelExit].back.regionId
                        exits.append(TransitionFront(dest, lambda l: True))
                for exit in exits:
                    destination = exit.dest
                    # If this exit has an entrance shuffle id and the shufflable exits list has it marked as shuffled,
                    # use the entrance it was shuffled to by getting the region of the destination exit.
                    # If the exit is assumed from root, do not look for a shuffled exit - just explore the destination
                    if exit.exitShuffleId is not None and not exit.assumed:
                        shuffledExit = ShuffleExits.ShufflableExits[exit.exitShuffleId]
                        if shuffledExit.shuffled:
                            destination = ShuffleExits.ShufflableExits[shuffledExit.shuffledId].back.regionId
                        elif shuffledExit.toBeShuffled and not exit.assumed:
                            continue
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if destination not in addedRegions and exit.logic(LogicVariables):
                        addedRegions.append(destination)
                        newRegion = Logic.Regions[destination]
                        newRegion.id = destination
                        regionPool.append(newRegion)
                # Deathwarps currently send to the vanilla destination
                if region.deathwarp is not None:
                    destination = region.deathwarp.dest
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if destination not in addedRegions and region.deathwarp.logic(LogicVariables):
                        addedRegions.append(destination)
                        newRegion = Logic.Regions[destination]
                        newRegion.id = destination
                        regionPool.append(newRegion)

    if searchType == SearchMode.GetReachable:
        return accessible
    elif searchType == SearchMode.CheckBeatable:
        # If the search has completed and banana hoard has not been found, game is unbeatable
        return False
    elif searchType == SearchMode.GeneratePlaythrough:
        return playthroughLocations
    elif searchType == SearchMode.CheckAllReachable:
        return len(accessible) == len(LocationList)
    elif searchType == SearchMode.GetUnreachable:
        return [x for x in LocationList if x not in accessible]


def VerifyWorld(settings):
    """Make sure all item locations are reachable on current world graph with constant items placed and all other items owned."""
    ItemPool.PlaceConstants(settings)
    unreachables = GetAccessibleLocations(settings, ItemPool.AllItems(settings), SearchMode.GetUnreachable)
    isValid = len(unreachables) == 0
    Reset()
    return isValid


def Reset():
    """Reset logic variables and region info that should be reset before a search."""
    LogicVariables.Reset()
    Logic.ResetRegionAccess()
    Logic.ResetCollectibleRegions()


def ParePlaythrough(settings, PlaythroughLocations):
    """Pare playthrough down to only the essential elements."""
    locationsToAddBack = []
    # Check every location in the list of spheres.
    for i in range(len(PlaythroughLocations) - 2, -1, -1):
        sphere = PlaythroughLocations[i]
        for locationId in sphere.copy():
            location = LocationList[locationId]
            # Copy out item from location
            item = location.item
            location.item = None
            # Check if the game is still beatable
            Reset()
            if GetAccessibleLocations(settings, [], SearchMode.CheckBeatable):
                # If the game is still beatable, this is an unnecessary location, remove it.
                sphere.remove(locationId)
                # We delay the item to ensure future locations which may rely on this one
                # do not give a false positive for beatability.
                location.SetDelayedItem(item)
                locationsToAddBack.append(locationId)
            else:
                # Else it is essential, don't remove it from the playthrough and add the item back.
                location.PlaceItem(item)

    # Check if there are any empty spheres, if so remove them
    for i in range(len(PlaythroughLocations) - 2, -1, -1):
        sphere = PlaythroughLocations[i]
        if len(sphere) == 0:
            PlaythroughLocations.remove(sphere)

    # Re-place those items which were delayed earlier.
    for locationId in locationsToAddBack:
        LocationList[locationId].PlaceDelayedItem()


def PareWoth(settings, PlaythroughLocations):
    """Pare playthrough to locations which are Way of the Hoard (hard required by logic)."""
    # The functionality is similar to ParePlaythrough, but we want to see if individual locations are
    # hard required, so items are added back after checking regardless of the outcome.
    WothLocations = []
    for sphere in PlaythroughLocations:
        # Don't want constant locations in woth
        for loc in [x for x in sphere if not LocationList[x].constant]:
            WothLocations.append(loc)
    # Check every item location to see if removing it by itself makes the game unbeatable
    for i in range(len(WothLocations) - 2, -1, -1):
        locationId = WothLocations[i]
        location = LocationList[locationId]
        item = location.item
        location.item = None
        # Check if game is still beatable
        Reset()
        if GetAccessibleLocations(settings, [], SearchMode.CheckBeatable):
            # If game is still beatable, this location is not hard required
            WothLocations.remove(locationId)
        # Either way, add location back
        location.PlaceItem(item)
    return WothLocations


def RandomFill(itemsToPlace, validLocations):
    """Randomly place given items in any location disregarding logic."""
    random.shuffle(itemsToPlace)
    # Get all remaining empty locations
    empty = []
    for (id, location) in LocationList.items():
        if location.item is None and id in validLocations:
            empty.append(id)
    random.shuffle(empty)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        if len(empty) == 0:
            return len(itemsToPlace)
        item = itemsToPlace.pop()
        locationId = empty.pop()
        LocationList[locationId].PlaceItem(item)
    return 0


def ForwardFill(settings, itemsToPlace, validLocations, ownedItems=[]):
    """Forward fill algorithm for item placement."""
    random.shuffle(itemsToPlace)
    ownedItems = ownedItems.copy()
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Find a random empty location which is reachable with current items
        reachable = GetAccessibleLocations(settings, ownedItems.copy())
        reachable = [x for x in reachable if LocationList[x].item is None and x in validLocations]
        if len(reachable) == 0:  # If there are no empty reachable locations, reached a dead end
            return len(itemsToPlace)
        random.shuffle(reachable)
        locationId = reachable.pop()
        # Get a random item and place it there, also adding to owned items
        item = itemsToPlace.pop()
        ownedItems.append(item)
        LocationList[locationId].PlaceItem(item)
    return 0


def GetItemValidLocations(validLocations, item):
    """Get the list of valid locations for this item."""
    # If validLocations is a dictionary, check for this item's value
    itemValidLocations = validLocations
    if isinstance(validLocations, dict):
        for itemKey in validLocations.keys():
            if item == itemKey:
                itemValidLocations = validLocations[itemKey]
                break
            # Valid locations entry wasn't found
            itemValidLocations = [x for x in LocationList]
    return itemValidLocations


def AssumedFill(settings, itemsToPlace, validLocations, ownedItems=[]):
    """Assumed fill algorithm for item placement."""
    # Calculate total cost of moves
    maxCoinsSpent = GetMaxCoinsSpent(settings, itemsToPlace + ownedItems)
    # While there are items to place
    random.shuffle(itemsToPlace)
    while len(itemsToPlace) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemsToPlace.pop(0)
        itemShuffled = False
        owned = itemsToPlace.copy()
        owned.extend(ownedItems)
        # Check current level of each progressive move
        slamLevel = sum(1 for x in owned if x == Items.ProgressiveSlam) + STARTING_SLAM
        ammoBelts = sum(1 for x in owned if x == Items.ProgressiveAmmoBelt)
        instUpgrades = sum(1 for x in owned if x == Items.ProgressiveInstrumentUpgrade)
        # print("slamLevel: " + str(slamLevel) + ", ammoBelts: " + str(ammoBelts) + ", instUpgrades: " + str(instUpgrades))
        itemValidLocations = GetItemValidLocations(validLocations, item)
        # Find all valid reachable locations for this item
        Reset()
        reachable = GetAccessibleLocations(settings, owned)
        validReachable = [x for x in reachable if LocationList[x].item is None and x in itemValidLocations]
        # If there are no empty reachable locations, reached a dead end
        if len(validReachable) == 0:
            print("Failed placing item " + ItemList[item].name + ", no valid reachable locations without this item.")
            currentKongsFreed = [ItemList[x].name for x in owned if ItemList[x].type == Types.Kong]
            currentKongsFreed.insert(0, settings.starting_kong.name)
            currentMovesOwned = [ItemList[x].name for x in owned if ItemList[x].type == Types.Shop]
            currentGbCount = len([x for x in owned if ItemList[x].type == Types.Banana])
            js.postMessage("Current Moves owned at failure: " + str(currentMovesOwned) + " with GB count: " + str(currentGbCount) + " and kongs freed: " + str(currentKongsFreed))
            return len(itemsToPlace) + 1
        # Shop items need coin logic
        if ItemList[item].type == Types.Shop:
            moveKong = ItemList[item].kong
            movePrice = GetPriceOfMoveItem(item, settings, slamLevel, ammoBelts, instUpgrades)
            movePriceArray = [0, 0, 0, 0, 0]
            if movePrice is not None:
                if moveKong == Kongs.any:
                    for anyKong in range(5):
                        maxCoinsSpent[anyKong] -= movePrice
                        movePriceArray[anyKong] = movePrice
                else:
                    maxCoinsSpent[moveKong] -= movePrice
                    movePriceArray[moveKong] = movePrice
        elif ItemList[item].type == Types.Kong:
            ownedKongs = [KongFromItem(x) for x in owned if ItemList[x].type == Types.Kong]
            ownedKongs.insert(0, settings.starting_kong)
            kongBeingPlaced = KongFromItem(item)
            if kongBeingPlaced in ownedKongs:
                ownedKongs.remove(kongBeingPlaced)  # Cannot free with the kong being placed
        random.shuffle(validReachable)
        # Get a random, empty, reachable location
        for locationId in validReachable:
            # Atempt to place the item here
            LocationList[locationId].PlaceItem(item)
            # When placing a kong, also decide who among the owned kongs can free them
            if ItemList[item].type == Types.Kong:
                # Choose the puzzle solver
                if locationId == Locations.DiddyKong or locationId == Locations.ChunkyKong:
                    settings.diddy_freeing_kong = random.choice(ownedKongs)
                elif locationId == Locations.LankyKong:
                    # TODO: see if we can open this to all kongs
                    settings.lanky_freeing_kong = random.choice(list(set(ownedKongs).intersection([Kongs.donkey, Kongs.lanky, Kongs.tiny])))
                elif locationId == Locations.TinyKong:
                    settings.tiny_freeing_kong = random.choice(list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky])))
            # Check valid reachable after placing to see if it is broken
            # Need to re-assign owned items since the search adds a bunch of extras
            owned = itemsToPlace.copy()
            owned.extend(ownedItems)
            Reset()
            reachable = GetAccessibleLocations(settings, owned)
            valid = True
            # For each remaining item, ensure that it has a valid location reachable after placing this item
            for checkItem in itemsToPlace:
                itemValid = GetItemValidLocations(validLocations, checkItem)
                validReachable = [x for x in reachable if x in itemValid]
                if len(validReachable) == 0:
                    js.postMessage("Failed placing item " + ItemList[item].name + " in location " + LocationList[locationId].name + ", due to too few remaining locations in play")
                    valid = False
                    break
                reachable.remove(validReachable[0])  # Remove one so same location can't be "used" twice
            # Attempt to verify coins
            if valid and ItemList[item].type == Types.Shop:
                currentCoins = [0, 0, 0, 0, 0]
                for kong in range(5):
                    currentCoins[kong] = LogicVariables.Coins[kong] - maxCoinsSpent[kong]
                # Breaking condition where we don't have access to enough coins
                for kong in range(5):
                    if currentCoins[kong] < movePriceArray[kong]:
                        # if currentCoins[kong] < 0:
                        # print("Failed placing item: " + ItemList[item].name)
                        # print("movePriceArray: " + str(movePriceArray))
                        # print("Total Coins Accessible: " + str(LogicVariables.Coins))
                        # print("maxCoinsSpent: " + str(maxCoinsSpent))
                        # print("currentCoins: " + str(currentCoins))
                        # print("items left to place: " + str(len(itemsToPlace)))
                        valid = False
            # If world is not valid, undo item placement and try next location
            if not valid:
                LocationList[locationId].item = None
                itemShuffled = False
                continue
            else:
                itemShuffled = True
                break
        if not itemShuffled:
            js.postMessage("Failed placing item " + ItemList[item].name + " in any of remaining " + str(len(validLocations)) + " possible locations")
            return len(itemsToPlace) + 1
    return 0


def GetMaxCoinsSpent(settings, ownedItems):
    """Calculate the max number of coins each kong could have spent given the ownedItems and the price settings."""
    MaxCoinsSpent = [0, 0, 0, 0, 0]
    slamLevel = sum(1 for x in ownedItems if x == Items.ProgressiveSlam) + STARTING_SLAM
    ammoBelts = sum(1 for x in ownedItems if x == Items.ProgressiveAmmoBelt)
    instUpgrades = sum(1 for x in ownedItems if x == Items.ProgressiveInstrumentUpgrade)
    for ownedItem in ownedItems:
        if ItemList[ownedItem].type == Types.Shop:
            moveKong = ItemList[ownedItem].kong
            if ownedItem == Items.ProgressiveSlam:
                slamLevel -= 1
            elif ownedItem == Items.ProgressiveAmmoBelt:
                ammoBelts -= 1
            elif ownedItem == Items.ProgressiveInstrumentUpgrade:
                instUpgrades -= 1
            movePrice = GetPriceOfMoveItem(ownedItem, settings, slamLevel, ammoBelts, instUpgrades)
            if movePrice is not None:
                if moveKong == Kongs.any:
                    # Shared moves could have been bought by any kong
                    for anyKong in range(5):
                        MaxCoinsSpent[anyKong] += movePrice
                else:
                    MaxCoinsSpent[moveKong] += movePrice
            # print("Move Kong: " + moveKong.name)
            # print("Move Price : " + str(movePrice))
            # print("MaxCoinsSpent: " + str(MaxCoinsSpent))
    return MaxCoinsSpent


def PlaceItems(settings, algorithm, itemsToPlace, ownedItems=[], validLocations=[]):
    """Places items using given algorithm."""
    # If list of valid locations not provided, just use all valid locations
    if len(validLocations) == 0:
        validLocations = [x for x in LocationList]
    if algorithm == "assumed":
        return AssumedFill(settings, itemsToPlace, validLocations, ownedItems)
    elif algorithm == "forward":
        return ForwardFill(settings, itemsToPlace, validLocations, ownedItems)
    elif algorithm == "random":
        return RandomFill(itemsToPlace, validLocations)


def Fill(spoiler):
    """Fully randomizes and places all items. Currently theoretical."""
    retries = 0
    while True:
        try:
            # First place constant items
            ItemPool.PlaceConstants(spoiler.settings)
            # Then place priority (logically very important) items
            highPriorityUnplaced = PlaceItems(
                spoiler.settings,
                spoiler.settings.algorithm,
                ItemPool.HighPriorityItems(spoiler.settings),
                ItemPool.HighPriorityAssumedItems(spoiler.settings),
            )
            if highPriorityUnplaced > 0:
                raise Ex.ItemPlacementException(str(highPriorityUnplaced) + " unplaced high priority items.")
            # Then place blueprints
            Reset()
            blueprintsUnplaced = PlaceItems(
                spoiler.settings,
                spoiler.settings.algorithm,
                ItemPool.Blueprints(spoiler.settings),
                ItemPool.BlueprintAssumedItems(spoiler.settings),
            )
            if blueprintsUnplaced > 0:
                raise Ex.ItemPlacementException(str(blueprintsUnplaced) + " unplaced blueprints.")
            # Then place the rest of items
            Reset()
            lowPriorityUnplaced = PlaceItems(
                spoiler.settings,
                spoiler.settings.algorithm,
                ItemPool.LowPriorityItems(spoiler.settings),
                ItemPool.ExcessItems(spoiler.settings),
            )
            if lowPriorityUnplaced > 0:
                raise Ex.ItemPlacementException(str(lowPriorityUnplaced) + " unplaced low priority items.")
            # Finally place excess items fully randomly
            hi = ItemPool.ExcessItems(spoiler.settings)
            excessUnplaced = PlaceItems(spoiler.settings, "random", ItemPool.ExcessItems(spoiler.settings))
            if excessUnplaced > 0:
                raise Ex.ItemPlacementException(str(excessUnplaced) + " unplaced excess items.")
            # Check if game is beatable
            Reset()
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.GameNotBeatableException("Game unbeatable after placing all items.")
            # Generate and display the playthrough
            Reset()
            PlaythroughLocations = GetAccessibleLocations(spoiler.settings, [], SearchMode.GeneratePlaythrough)
            ParePlaythrough(spoiler.settings, PlaythroughLocations)
            # Generate and display woth
            WothLocations = PareWoth(spoiler.settings, PlaythroughLocations)
            # Write data to spoiler and return
            spoiler.UpdateLocations(LocationList)
            spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
            spoiler.UpdateWoth(LocationList, WothLocations)
            return spoiler
        except Ex.FillException as ex:
            if retries == 4:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            else:
                retries += 1
                js.postMessage("Fill failed. Retrying. Tries: " + str(retries))
                Reset()
                Logic.ClearAllLocations()


def ShuffleMoves(spoiler):
    """Shuffles shared kong moves and then returns the remaining ones and their valid locations."""
    # First place constant items
    ItemPool.PlaceConstants(spoiler.settings)
    # Set up owned items
    kongMoves = []
    kongMoves.extend(ItemPool.DonkeyMoves)
    kongMoves.extend(ItemPool.DiddyMoves)
    kongMoves.extend(ItemPool.LankyMoves)
    kongMoves.extend(ItemPool.TinyMoves)
    kongMoves.extend(ItemPool.ChunkyMoves)

    # When a shared move is assigned to a shop in any particular level, that shop cannot also hold any kong-specific moves.
    # To avoid conflicts, first determine which level shops will have shared moves then remove these shops from each kong's valid locations list
    importantSharedUnplaced = PlaceItems(
        spoiler.settings, "assumed", ItemPool.ImportantSharedMoves.copy(), [x for x in ItemPool.AllItems(spoiler.settings) if x not in ItemPool.ImportantSharedMoves], ItemPool.SharedMoveLocations
    )
    if importantSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(importantSharedUnplaced) + " unplaced shared important items.")
    junkSharedUnplaced = PlaceItems(spoiler.settings, "random", ItemPool.JunkSharedMoves.copy(), validLocations=ItemPool.SharedMoveLocations)
    if junkSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(junkSharedUnplaced) + " unplaced shared junk items.")
    sharedMoveShops = []
    for sharedLocation in ItemPool.SharedMoveLocations:
        if LocationList[sharedLocation].item is not None:
            sharedMoveShops.append(sharedLocation)
    locationsToRemove = ItemPool.GetMoveLocationsToRemove(sharedMoveShops)
    # Now we need to set up the valid locations dictionary
    validLocations = {}
    kongMoveArrays = [ItemPool.DonkeyMoves, ItemPool.DiddyMoves, ItemPool.LankyMoves, ItemPool.TinyMoves, ItemPool.ChunkyMoves]
    kongLocationArrays = [ItemPool.DonkeyMoveLocations, ItemPool.DiddyMoveLocations, ItemPool.LankyMoveLocations, ItemPool.TinyMoveLocations, ItemPool.ChunkyMoveLocations]
    for i in range(5):
        for item in kongMoveArrays[i]:
            validLocations[item] = kongLocationArrays[i] - locationsToRemove
    return (kongMoves, validLocations)


def ShuffleMisc(spoiler):
    """Facilitate shuffling individual pools of items in lieu of full item rando."""
    retries = 0
    while True:
        try:
            itemsToPlace = []
            validLocations = {}
            # Handle move rando
            if spoiler.settings.shuffle_items == "moves":
                # Shuffle the shared move locations since they must be done first,
                # and return the kong moves and their locations
                (moveItems, moveLocations) = ShuffleMoves(spoiler)
                itemsToPlace.extend(moveItems)
                validLocations.update(moveLocations)
            # Handle kong rando
            if spoiler.settings.kong_rando:
                kongItems = ItemPool.Kongs(spoiler.settings)
                kongValidLocations = {}
                kongLocations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
                for item in kongItems:
                    kongValidLocations[item] = kongLocations
                # Kongs could be shuffled in the following generic shuffle, but since they're so restrictive,
                # a few failures are almost certain if they are, unfortunately.
                Reset()
                unplaced = PlaceItems(spoiler.settings, "assumed", kongItems, ownedItems=itemsToPlace, validLocations=kongValidLocations)
                if unplaced > 0:
                    raise Ex.ItemPlacementException(str(unplaced) + " unplaced kongs.")
            # Perform the shuffle
            Reset()
            unplaced = PlaceItems(spoiler.settings, "assumed", itemsToPlace, validLocations=validLocations)
            if unplaced > 0:
                raise Ex.ItemPlacementException(str(unplaced) + " unplaced items.")
            # Check if game is beatable
            Reset()
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.GameNotBeatableException("Game unbeatable after placing all items.")
            # Generate and display the playthrough
            Reset()
            PlaythroughLocations = GetAccessibleLocations(spoiler.settings, [], SearchMode.GeneratePlaythrough)
            ParePlaythrough(spoiler.settings, PlaythroughLocations)
            # Generate and display woth
            WothLocations = PareWoth(spoiler.settings, PlaythroughLocations)
            # Write data to spoiler and return
            spoiler.UpdateLocations(LocationList)
            spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
            spoiler.UpdateWoth(LocationList, WothLocations)
            return spoiler
        except Ex.FillException as ex:
            if retries == 20:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            else:
                retries += 1
                js.postMessage("Fill failed. Retrying. Tries: " + str(retries))
                Reset()
                Logic.ClearAllLocations()


def ShuffleKongsAndLevels(spoiler):
    """Shuffle Kongs and Levels simultaneously accounting for restrictions."""
    # All methods here follow this Kongs vs level progression rule:
    # Must be able to have 2 kongs no later than level 2
    # Must be able to have 3 kongs no later than level 3
    # Must be able to have 4 kongs no later than level 4
    # Must be able to have 5 kongs no later than level 5
    # Valid Example:
    #   1. Caves - No kongs found
    #   2. Aztec - Can free 2nd kong here, other kong is move locked
    #   3. Japes - Can free 3rd kong here
    #   4. Galleon - Find move to free other kong from aztec
    #   5. Factory - Find last kong
    #   6. Castle
    #   7. Fungi
    # ALGORITHM START
    # 1. Determine Starting Kong (done previously in Settings.resolve_settings)
    # 2. Determine where Japes, Aztec, and Factory fit in level order, with some restrictions
    # 3. Determine the rest of the levels randomly
    newLevelOrder = ShuffleLevelOrderWithRestrictions(spoiler.settings)
    ShuffleExits.ShuffleLevelExits(newLevelOrder)
    spoiler.UpdateExits()
    # 4. TODO: Change level access logic to require a number of kongs to be free

    # Assume all T&S and B.Lockers are zero for now
    WipeProgressionTotals(spoiler.settings)
    # 5. Fill the kongs

    # 6. Fill the moves

    # 7. Perform Boss Location & Boss Kong rando, ensuring the first boss can be beaten with an unlocked kong and so on.

    # 8. Determine upper limits for the B. Locker and T&S amounts based on accessible bananas & GBs, and pick random values capped by these.


def ShuffleLevelOrderWithRestrictions(settings: Settings):
    """Determine level order given starting kong and the need to find more kongs along the way."""
    levelIndexChoices = {1, 2, 3, 4, 5, 6, 7}

    # Decide where Aztec will go
    # Diddy can reasonably make progress if Aztec is first level
    if settings.starting_kong == Kongs.diddy:
        aztecIndex = random.randint(1, 4)
    else:
        aztecIndex = random.randint(2, 4)
    levelIndexChoices.remove(aztecIndex)

    # Decide where Japes will go
    japesOptions = []
    # If Aztec is level 4, both of Japes/Factory need to be in level 1-3
    if aztecIndex == 4:
        japesOptions = list(levelIndexChoices.intersection({1, 3}))
    else:
        japesOptions = list(levelIndexChoices.intersection({1, 5}))
    japesIndex = random.choice(japesOptions)
    levelIndexChoices.remove(japesIndex)

    # Decide where Factory will go
    factoryOptions = []
    # If starting kong is Chunky, one of Japes/Factory needs to be in level 1-2 (until we can get Chunky to Free kong in Tiny Temple)
    if settings.starting_kong == Kongs.chunky and japesIndex > 2:
        factoryOptions = list(levelIndexChoices.intersection({1, 2}))
    # If Aztec is level 4, both of Japes/Factory need to be in level 1-3
    elif aztecIndex == 4:
        factoryOptions = list(levelIndexChoices.intersection({1, 3}))
    # If Aztec is level 3, one of Japes/Factory needs to be in level 1-2 and other in level 1-5
    elif aztecIndex == 3:
        if japesIndex < 3:
            factoryOptions = list(levelIndexChoices.intersection({1, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1, 2}))
    # If Aztec is level 1 or 2, one of Japes/Factory needs to be in level 1-4 and other in level 1-5
    else:
        if japesIndex < 5:
            factoryOptions = list(levelIndexChoices.intersection({1, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1, 4}))
    factoryIndex = random.choice(factoryOptions)
    levelIndexChoices.remove(factoryIndex)

    # Decide the remaining level order randomly
    remainingLevels = list(levelIndexChoices)
    random.shuffle(remainingLevels)
    galleonIndex = remainingLevels.pop()
    forestIndex = remainingLevels.pop()
    cavesIndex = remainingLevels.pop()
    castleIndex = remainingLevels.pop()
    newLevelOrder = {
        japesIndex: Levels.JungleJapes,
        aztecIndex: Levels.AngryAztec,
        factoryIndex: Levels.FranticFactory,
        galleonIndex: Levels.GloomyGalleon,
        forestIndex: Levels.FungiForest,
        cavesIndex: Levels.CrystalCaves,
        castleIndex: Levels.CreepyCastle,
    }
    return newLevelOrder


def GetAccessibleKongLocations(levels: list, ownedKongs: list):
    """Get all kong locations within the provided levels which are reachable by owned kongs."""
    kongLocations = []
    for level in levels:
        if level == Levels.JungleJapes:
            kongLocations.append(Locations.DiddyKong)
        elif level == Levels.AngryAztec:
            if Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs:
                kongLocations.append(Locations.LankyKong)
            if Kongs.diddy in ownedKongs:
                kongLocations.append(Locations.TinyKong)
        elif level == Levels.FranticFactory:
            if Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs:
                kongLocations.append(Locations.ChunkyKong)
    return kongLocations


def WipeProgressionTotals(settings: Settings):
    """Wipe out progression totals to assume access through main 7 levels."""
    for i in range(0, 6):
        settings.EntryGBs[i] = 0
        settings.BossBananas[i] = 0


def Generate_Spoiler(spoiler):
    """Generate a complete spoiler based on input settings."""
    # Init logic vars with settings
    global LogicVariables
    LogicVariables = LogicVarHolder(spoiler.settings)
    # Handle kasplats
    KasplatShuffle(LogicVariables)
    spoiler.human_kasplats = {}
    spoiler.UpdateKasplats(LogicVariables.kasplat_map)
    # Handle bonus barrels
    if spoiler.settings.bonus_barrels == "random":
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # Handle Bananaports
    if spoiler.settings.bananaport_rando:
        replacements = []
        human_replacements = {}
        ShuffleWarps(replacements, human_replacements)
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    # Handle Kong Rando + Level Rando combination separately since it is more restricted
    if spoiler.settings.shuffle_loading_zones == "levels" and spoiler.settings.kong_rando:
        # Force move rando on if not starting will all moves
        if not spoiler.settings.unlock_all_moves:
            spoiler.settings.shuffle_items = "moves"
        ShuffleKongsAndLevels(spoiler)
    else:
        # Handle ER
        if spoiler.settings.shuffle_loading_zones != "none":
            ShuffleExits.ExitShuffle(spoiler.settings)
            spoiler.UpdateExits()
        # Handle Item Fill
        if spoiler.settings.shuffle_items == "all":
            Fill(spoiler)
        elif spoiler.settings.shuffle_items == "moves" or spoiler.settings.kong_rando:
            ShuffleMisc(spoiler)
        else:
            # Just check if normal item locations are beatable with given settings
            ItemPool.PlaceConstants(spoiler.settings)
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.VanillaItemsGameNotBeatableException("Game unbeatable.")
            # Playthrough and location list probably unnecessary with vanilla items
            # Reset()
            # PlaythroughLocations = GetAccessibleLocations([], SearchMode.GeneratePlaythrough)
            # ParePlaythrough(PlaythroughLocations)
            # # Write data to spoiler and return
            # spoiler.UpdateLocations(LocationList)
            # spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
    Reset()
    ShuffleExits.Reset()
    return spoiler
