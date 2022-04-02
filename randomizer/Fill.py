"""Module used to distribute items randomly."""
import random
from re import search

import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Prices import GetPriceOfMoveItem
import randomizer.ShuffleExits as ShuffleExits
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import Location, LocationList
from randomizer.Lists.Minigame import MinigameAssociations, MinigameRequirements, BarrelMetaData
from randomizer.ShuffleKasplats import KasplatShuffle
from randomizer.Logic import LogicVarHolder, LogicVariables
from randomizer.LogicClasses import TransitionFront
from randomizer.ShuffleBarrels import BarrelShuffle, ShuffleBarrels


def GetExitLevelExit(settings, region):
    """Get the exit that using the "Exit Level" button will take you to."""
    level = region.level
    if settings.shuffle_loading_zones == "all" and region.restart is not None:
        return ShuffleExits.ShufflableExits[region.restart].shuffledId
    elif level == Levels.JungleJapes:
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
            # If searching for access without spending coins, don't add any shop locations (unless it's Simian Slam which is always free)
            if searchType == SearchMode.GetReachableWithoutSpending and location.type == Types.Shop and locationId != Locations.SimianSlam:
                continue
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
                # Check accessibility for each location in this region
                for location in region.locations:
                    if location.logic(LogicVariables) and location.id not in newLocations and location.id not in accessible:
                        # If this location is a bonus barrel, must make sure its logic is met as well
                        if location.bonusBarrel and settings.bonus_barrels != "skip":
                            minigame = MinigameAssociations[location.id]
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
                # Finally check accessibility for collectibles
                if region.id in Logic.CollectibleRegions.keys():
                    for collectible in Logic.CollectibleRegions[region.id]:
                        if not collectible.added and (kong == collectible.kong or collectible.kong == Kongs.any) and collectible.logic(LogicVariables):
                            LogicVariables.AddCollectible(collectible, region.level)

    if searchType == SearchMode.GetReachable or searchType == SearchMode.GetReachableWithoutSpending:
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
    """Pares playthrough down to only the essential elements."""
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


def AssumedFill(settings, itemsToPlace, validLocations, ownedItems=[]):
    """Assumed fill algorithm for item placement."""
    # Calculate total cost of moves
    maxCoinsSpent = GetMaxCoinsSpent(settings, itemsToPlace + ownedItems)

    # While there are items to place
    random.shuffle(itemsToPlace)
    while len(itemsToPlace) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemsToPlace.pop(0)
        owned = itemsToPlace.copy()
        owned.extend(ownedItems)

        # Check current level of each progressive move
        slamLevel = sum(1 for x in owned if x == Items.ProgressiveSlam)
        ammoBelts = sum(1 for x in owned if x == Items.ProgressiveAmmoBelt)
        instUpgrades = sum(1 for x in owned if x == Items.ProgressiveInstrumentUpgrade)
        # print("slamLevel: " + str(slamLevel) + ", ammoBelts: " + str(ammoBelts) + ", instUpgrades: " + str(instUpgrades))

        Reset()
        reachable = GetAccessibleLocations(settings, owned)
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
            currentCoins = [0, 0, 0, 0, 0]
            for kong in range(5):
                currentCoins[kong] = LogicVariables.Coins[kong] - maxCoinsSpent[kong]
            # Breaking condition where we don't have access to enough coins
            for kong in range(5):
                if currentCoins[kong] < movePriceArray[kong]:
                    print("Failed placing item: " + ItemList[item].name)
                    print("movePriceArray: " + str(movePriceArray))
                    print("Total Coins Accessible: " + str(LogicVariables.Coins))
                    print("maxCoinsSpent: " + str(maxCoinsSpent))
                    print("currentCoins: " + str(currentCoins))
                    return len(itemsToPlace) + 1

        validReachable = [x for x in reachable if LocationList[x].item is None and x in validLocations]
        # If there are no empty reachable locations, reached a dead end
        if len(validReachable) == 0:
            return len(itemsToPlace) + 1
        # Get a random, empty, reachable location and place the item there
        random.shuffle(validReachable)
        locationId = validReachable.pop()
        LocationList[locationId].PlaceItem(item)
    return 0


def GetMaxCoinsSpent(settings, ownedItems):
    """Calculate the max number of coins each kong could have spent given the ownedItems and the price settings."""
    MaxCoinsSpent = [0, 0, 0, 0, 0]
    slamLevel = sum(1 for x in ownedItems if x == Items.ProgressiveSlam)
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
            # Write data to spoiler and return
            spoiler.UpdateLocations(LocationList)
            spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
            return spoiler
        except Ex.FillException as ex:
            if retries == 4:
                print("Fill failed, out of retries.")
                raise ex
            else:
                retries += 1
                print("Fill failed. Retrying. Tries: " + str(retries))
                Reset()
                Logic.ClearAllLocations()


def ShuffleMoves(spoiler):
    """Just shuffles moves per kong to other move locations of same kong."""
    retries = 0
    while True:
        try:
            # First place constant items
            ItemPool.PlaceConstants(spoiler.settings)
            # Set up owned items
            ownedItems = []
            ownedItems.extend(ItemPool.DonkeyMoves)
            ownedItems.extend(ItemPool.DiddyMoves)
            ownedItems.extend(ItemPool.LankyMoves)
            ownedItems.extend(ItemPool.TinyMoves)
            ownedItems.extend(ItemPool.ChunkyMoves)
            ownedItems.extend(ItemPool.JunkSharedMoves)
            ownedItems.append(Items.ProgressiveSlam)  # Always start with simian slam

            # For each kong, place their items in their valid locations, removing owneditems before each placement as they're placed
            # Force assumed for move rando since it's so restrictive

            # When a shared move is assigned to a shop in any particular level, that shop cannot also hold any kong-specific moves.
            # To avoid conflicts, first determine which level shops will have shared moves then remove these shops from each kong's valid locations list
            importantSharedUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.ImportantSharedMoves.copy(),
                ownedItems,
                ItemPool.SharedMoveLocations,
            )
            if importantSharedUnplaced > 0:
                raise Ex.ItemPlacementException(str(importantSharedUnplaced) + " unplaced shared important items.")

            ownedItems = [x for x in ownedItems if x not in ItemPool.JunkSharedMoves]
            junkSharedUnplaced = PlaceItems(spoiler.settings, "assumed", ItemPool.JunkSharedMoves.copy(), ownedItems, ItemPool.SharedMoveLocations)
            if junkSharedUnplaced > 0:
                raise Ex.ItemPlacementException(str(junkSharedUnplaced) + " unplaced shared junk items.")

            sharedMoveShops = []
            for sharedLocation in ItemPool.SharedMoveLocations:
                if LocationList[sharedLocation].item is not None:
                    sharedMoveShops.append(sharedLocation)

            locationsToRemove = ItemPool.GetMoveLocationsToRemove(sharedMoveShops)
            Reset()
            ownedItems = [x for x in ownedItems if x not in ItemPool.DonkeyMoves]
            donkeyUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.DonkeyMoves.copy(),
                ownedItems,
                ItemPool.DonkeyMoveLocations - locationsToRemove,
            )
            if donkeyUnplaced > 0:
                raise Ex.ItemPlacementException(str(donkeyUnplaced) + " unplaced donkey items.")
            Reset()
            ownedItems = [x for x in ownedItems if x not in ItemPool.DiddyMoves]
            diddyUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.DiddyMoves.copy(),
                ownedItems,
                ItemPool.DiddyMoveLocations - locationsToRemove,
            )
            if diddyUnplaced > 0:
                raise Ex.ItemPlacementException(str(diddyUnplaced) + " unplaced diddy items.")
            Reset()
            ownedItems = [x for x in ownedItems if x not in ItemPool.LankyMoves]
            lankyUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.LankyMoves.copy(),
                ownedItems,
                ItemPool.LankyMoveLocations - locationsToRemove,
            )
            if lankyUnplaced > 0:
                raise Ex.ItemPlacementException(str(lankyUnplaced) + " unplaced lanky items.")
            Reset()
            ownedItems = [x for x in ownedItems if x not in ItemPool.TinyMoves]
            tinyUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.TinyMoves.copy(),
                ownedItems,
                ItemPool.TinyMoveLocations - locationsToRemove,
            )
            if tinyUnplaced > 0:
                raise Ex.ItemPlacementException(str(tinyUnplaced) + " unplaced tiny items.")
            Reset()
            ownedItems = [x for x in ownedItems if x not in ItemPool.ChunkyMoves]
            chunkyUnplaced = PlaceItems(
                spoiler.settings,
                "assumed",
                ItemPool.ChunkyMoves.copy(),
                ownedItems,
                ItemPool.ChunkyMoveLocations - locationsToRemove,
            )
            if chunkyUnplaced > 0:
                raise Ex.ItemPlacementException(str(chunkyUnplaced) + " unplaced chunky items.")
            # Check if game is beatable
            Reset()
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.GameNotBeatableException("Game unbeatable after placing all items.")
            # Generate and display the playthrough
            Reset()
            PlaythroughLocations = GetAccessibleLocations(spoiler.settings, [], SearchMode.GeneratePlaythrough)
            ParePlaythrough(spoiler.settings, PlaythroughLocations)
            # Write data to spoiler and return
            spoiler.UpdateLocations(LocationList)
            spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
            return spoiler
        except Ex.FillException as ex:
            if retries == 20:
                print("Fill failed, out of retries.")
                raise ex
            else:
                retries += 1
                print("Fill failed. Retrying. Tries: " + str(retries))
                Reset()
                Logic.ClearAllLocations()


def Generate_Spoiler(spoiler):
    """Generate a complete spoiler based on input settings."""
    # Init logic vars with settings
    global LogicVariables
    LogicVariables = LogicVarHolder(spoiler.settings)
    # Handle kasplats
    KasplatShuffle(LogicVariables)
    spoiler.UpdateKasplats(LogicVariables.kasplat_map)
    # Handle bonus barrels
    if spoiler.settings.bonus_barrels == "random":
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # Handle ER
    if spoiler.settings.shuffle_loading_zones != "none":
        ShuffleExits.ExitShuffle(spoiler.settings)
        spoiler.UpdateExits()
    # Place items
    if spoiler.settings.shuffle_items == "all":
        Fill(spoiler)
    elif spoiler.settings.shuffle_items == "moves":
        ShuffleMoves(spoiler)
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
