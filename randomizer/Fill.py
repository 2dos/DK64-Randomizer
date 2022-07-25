"""Module used to distribute items randomly."""
import random

import js
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Warps import Warps
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
from randomizer.Lists.ShufflableExit import GetLevelShuffledToIndex, GetShuffledLevelIndex
from randomizer.Lists.Warps import BananaportVanilla
import randomizer.Logic as Logic
from randomizer.Settings import Settings
import randomizer.ShuffleExits as ShuffleExits
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs, GetKongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList, KongFromItem
from randomizer.Lists.Location import LocationList
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Logic import LogicVarHolder, LogicVariables, STARTING_SLAM
from randomizer.LogicClasses import Sphere, TransitionFront
from randomizer.Prices import GetMaxForKong, GetPriceOfMoveItem
from randomizer.ShuffleBarrels import BarrelShuffle
from randomizer.ShuffleKasplats import InitKasplatMap, KasplatShuffle
from randomizer.ShuffleWarps import ShuffleWarps
from randomizer.ShuffleBosses import ShuffleBossesBasedOnOwnedItems
from randomizer.ShufflePatches import ShufflePatches


def GetExitLevelExit(region):
    """Get the exit that using the "Exit Level" button will take you to."""
    level = region.level
    # If you have option to restart, means there is no Exit Level option
    if region.restart is not None:
        return None
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


def GetAccessibleLocations(settings, ownedItems, searchType=SearchMode.GetReachable, purchaseList=None):
    """Search to find all reachable locations given owned items."""
    if purchaseList is None:
        purchaseList = []
    accessible = []
    newLocations = []
    playthroughLocations = []
    eventAdded = True
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or eventAdded:
        # Add items and events from the last search iteration
        sphere = Sphere()
        if playthroughLocations:
            sphere.availableGBs = playthroughLocations[-1].availableGBs
        for locationId in newLocations:
            accessible.append(locationId)
            location = LocationList[locationId]
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                # In search mode GetReachableWithControlledPurchases, only allowed to purchase items as prescribed by purchaseOrder
                if location.type == Types.Shop and locationId != Locations.SimianSlam and searchType == SearchMode.GetReachableWithControlledPurchases and locationId not in purchaseList:
                    continue
                ownedItems.append(location.item)
                # If we want to generate the playthrough and the item is a playthrough item, add it to the sphere
                if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
                    # Banana hoard in a sphere by itself
                    if location.item == Items.BananaHoard:
                        sphere.locations = [locationId]
                        break
                    if location.item == Items.GoldenBanana:
                        sphere.availableGBs += 1
                    sphere.locations.append(locationId)
                # If we're checking beatability, just want to know if we have access to the banana hoard
                if searchType == SearchMode.CheckBeatable and location.item == Items.BananaHoard:
                    return True
        if len(sphere.locations) > 0:
            playthroughLocations.append(sphere)
            if LocationList[sphere.locations[0]].item == Items.BananaHoard:
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
            startRegion.dayAccess = True
            startRegion.nightAccess = Events.Night in LogicVariables.Events
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
                    # Can start searching with night access
                    # Check this even if Night's already been added, because you could
                    # lose night access from start to Forest main, then regain it here
                    if event.name == Events.Night and event.logic(LogicVariables):
                        region.nightAccess = True
                # Check accessibility for collectibles
                if region.id in Logic.CollectibleRegions.keys():
                    for collectible in Logic.CollectibleRegions[region.id]:
                        if not collectible.added and collectible.kong in (kong, Kongs.any) and collectible.logic(LogicVariables) and collectible.enabled:
                            LogicVariables.AddCollectible(collectible, region.level)
                # Check accessibility for each location in this region
                for location in region.locations:
                    if location.logic(LogicVariables) and location.id not in newLocations and location.id not in accessible:
                        # If this location is a bonus barrel, must make sure its logic is met as well
                        if (location.bonusBarrel is MinigameType.BonusBarrel and settings.bonus_barrels != "skip") or (
                            location.bonusBarrel is MinigameType.HelmBarrel and settings.helm_barrels != "skip"
                        ):
                            minigame = BarrelMetaData[location.id].minigame
                            if not MinigameRequirements[minigame].logic(LogicVariables):
                                continue
                        # If this location is a blueprint, then make sure this is the correct kong
                        elif LocationList[location.id].type == Types.Blueprint:
                            if not LogicVariables.KasplatAccess(location.id):
                                continue
                        # Any shop item with exception of simian slam has a price
                        elif LocationList[location.id].type == Types.Shop and location.id != Locations.SimianSlam:
                            # In search mode GetReachableWithControlledPurchases, only allowed to purchase what is passed in as "ownedItems"
                            if searchType != SearchMode.GetReachableWithControlledPurchases or location.id in purchaseList:
                                LogicVariables.PurchaseShopItem(LocationList[location.id])
                        elif location.id == Locations.NintendoCoin:
                            LogicVariables.Coins[Kongs.donkey] -= 2  # Subtract 2 coins for arcade lever
                        newLocations.append(location.id)
                # Check accessibility for each exit in this region
                exits = region.exits.copy()
                # If loading zones are shuffled, the "Exit Level" button in the pause menu could potentially take you somewhere new
                if settings.shuffle_loading_zones and region.level != Levels.DKIsles and region.level != Levels.Shops:
                    levelExit = GetExitLevelExit(region)
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
                        # Check time of day
                        timeAccess = True
                        if exit.time == Time.Night and not region.nightAccess:
                            timeAccess = False
                        elif exit.time == Time.Day and not region.dayAccess:
                            timeAccess = False
                        if timeAccess:
                            addedRegions.append(destination)
                            newRegion = Logic.Regions[destination]
                            newRegion.id = destination
                            regionPool.append(newRegion)
                    # If it's accessible, update time of day access whether already added or not
                    # This way if a region has access from 2 different regions, one time-restricted and one not,
                    # it will be known that it can be accessed during either time of day
                    if exit.logic(LogicVariables):
                        # If this region has day access and the exit isn't restricted to night-only, then the destination has day access
                        if region.dayAccess and exit.time != Time.Night and not Logic.Regions[destination].dayAccess:
                            Logic.Regions[destination].dayAccess = True
                            # Count as event added so search doesn't get stuck if region is searched,
                            # then later a new time of day access is found so it should be re-visited
                            eventAdded = True
                        # And vice versa
                        if region.nightAccess and exit.time != Time.Day and not Logic.Regions[destination].nightAccess:
                            Logic.Regions[destination].nightAccess = True
                            eventAdded = True
                # Deathwarps currently send to the vanilla destination
                if region.deathwarp is not None:
                    destination = region.deathwarp.dest
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if destination not in addedRegions and region.deathwarp.logic(LogicVariables):
                        addedRegions.append(destination)
                        newRegion = Logic.Regions[destination]
                        newRegion.id = destination
                        regionPool.append(newRegion)

    if searchType in (SearchMode.GetReachable, SearchMode.GetReachableWithControlledPurchases):
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
    if settings.no_logic:
        return True  # Don't verify world in no logic
    ItemPool.PlaceConstants(settings)
    unreachables = GetAccessibleLocations(settings, ItemPool.AllItems(settings), SearchMode.GetUnreachable)
    isValid = len(unreachables) == 0
    Reset()
    return isValid


def VerifyWorldWithWorstCoinUsage(settings):
    """Make sure the game is beatable without it being possible to run out of coins for required moves."""
    if settings.no_logic:
        return True  # Don't verify world in no logic
    locationsToPurchase = []
    reachable = []
    maxCoins = [
        GetMaxForKong(settings, Kongs.donkey),
        GetMaxForKong(settings, Kongs.diddy),
        GetMaxForKong(settings, Kongs.lanky),
        GetMaxForKong(settings, Kongs.tiny),
        GetMaxForKong(settings, Kongs.chunky),
    ]
    while True:
        Reset()
        reachable = GetAccessibleLocations(settings, [], SearchMode.GetReachableWithControlledPurchases, locationsToPurchase)
        # Subtract the price of the chosen location from maxCoinsNeeded
        itemsToPurchase = [LocationList[x].item for x in locationsToPurchase]
        coinsSpent = GetMaxCoinsSpent(settings, itemsToPurchase)
        coinsNeeded = [maxCoins[kong] - coinsSpent[kong] for kong in range(0, 5)]
        coinsBefore = LogicVariables.Coins.copy()
        # print("Coins owned during search: " + str(coinsBefore))
        # print("Coins needed during search: " + str(coinsNeeded))
        # If we found enough coins that every kong can buy all their moves, world is valid!
        if (
            coinsBefore[Kongs.donkey] >= coinsNeeded[Kongs.donkey]
            and coinsBefore[Kongs.diddy] >= coinsNeeded[Kongs.diddy]
            and coinsBefore[Kongs.lanky] >= coinsNeeded[Kongs.lanky]
            and coinsBefore[Kongs.tiny] >= coinsNeeded[Kongs.tiny]
            and coinsBefore[Kongs.chunky] >= coinsNeeded[Kongs.chunky]
        ):
            # print("Seed is valid, found enough coins with worst purchase order: " + str([LocationList[x].name + ": " + LocationList[x].item.name + ", " for x in locationsToPurchase]))
            Reset()
            return True
        # If we found the BananaHoard, world is valid!
        if len([x for x in reachable if LocationList[x].item == Items.BananaHoard]) > 0:
            # print("Seed is valid, found banana hoard with worst purchase order: " + str([LocationList[x].name + ": " + LocationList[x].item.name + ", " for x in locationsToPurchase]))
            Reset()
            return True
        # For each accessible shop location
        newReachableShops = [
            x
            for x in reachable
            if LocationList[x].type == Types.Shop and LocationList[x].item is not None and LocationList[x].item != Items.NoItem and x not in locationsToPurchase and LogicVariables.CanBuy(x)
        ]
        shopDifferentials = {}
        shopUnlocksItems = {}
        # If no accessible shop locations found, means you got coin locked and the seed is not valid
        if len(newReachableShops) == 0:
            print("Seed is invalid, coin locked with purchase order: " + str([LocationList[x].name + ": " + LocationList[x].item.name + ", " for x in locationsToPurchase]))
            Reset()
            return False
        locationToBuy = None
        # print("Accessible Shops: " + str([LocationList[x].name for x in newReachableShops]))
        for shopLocation in newReachableShops:
            # print("Check buying " + LocationList[shopLocation].item.name + " from location " + LocationList[shopLocation].name)
            # Recheck accessible to see how many coins will be available afterward
            tempLocationsToPurchase = locationsToPurchase.copy()
            tempLocationsToPurchase.append(shopLocation)
            Reset()
            reachableAfter: list = GetAccessibleLocations(settings, [], SearchMode.GetReachableWithControlledPurchases, tempLocationsToPurchase)
            coinsAfter = LogicVariables.Coins.copy()
            # Calculate the coin differential
            coinDifferential = [0, 0, 0, 0, 0]
            for kong in LogicVariables.GetKongs():
                coinDifferential[kong] = coinsAfter[kong] - coinsBefore[kong]
            # print("Coin differential: " + str(coinDifferential))
            shopDifferentials[shopLocation] = coinDifferential
            shopUnlocksItems[shopLocation] = [LocationList[x].item for x in reachableAfter if x not in reachable and LocationList[x].item is not None]
            # Determine if this is the new worst move
            if locationToBuy is None:
                locationToBuy = shopLocation
                continue
            # Coin differential must be negative for at least one kong to be considered new worst
            if len([x for x in shopDifferentials[shopLocation] if x < 0]) == 0:
                continue
            # If a move unlocks new kongs it is more useful than others, even if it has a worse coin differential
            existingMoveKongsUnlocked = len([x for x in shopUnlocksItems[locationToBuy] if ItemList[x].type == Types.Kong])
            currentMoveKongsUnlocked = len([x for x in shopUnlocksItems[shopLocation] if ItemList[x].type == Types.Kong])
            if currentMoveKongsUnlocked > existingMoveKongsUnlocked:
                continue
            # If a move unlocks a new boss key it is more useful than others, even if it has a worse coin differential
            existingMoveKeysUnlocked = len([x for x in shopUnlocksItems[locationToBuy] if ItemList[x].type == Types.Key])
            currentMoveKeysUnlocked = len([x for x in shopUnlocksItems[shopLocation] if ItemList[x].type == Types.Key])
            if currentMoveKeysUnlocked > existingMoveKeysUnlocked:
                continue
            # All else equal, pick the move with the lowest overall coin differential
            existingMoveCoinDiff = sum(list(shopDifferentials[locationToBuy]))
            currentMoveCoinDiff = sum(list(shopDifferentials[shopLocation]))
            if currentMoveCoinDiff < existingMoveCoinDiff:
                locationToBuy = shopLocation
        # Purchase the "least helpful" move & add to owned Items
        # print("Choosing to buy " + LocationList[locationToBuy].item.name + " from " + LocationList[locationToBuy].name)
        locationsToPurchase.append(locationToBuy)


def Reset():
    """Reset logic variables and region info that should be reset before a search."""
    LogicVariables.Reset()
    Logic.ResetRegionAccess()
    Logic.ResetCollectibleRegions()


def ParePlaythrough(settings, PlaythroughLocations):
    """Pare playthrough down to only the essential elements."""
    locationsToAddBack = []
    mostExpensiveBLocker = max([settings.blocker_0, settings.blocker_1, settings.blocker_2, settings.blocker_3, settings.blocker_4, settings.blocker_5, settings.blocker_6, settings.blocker_7])
    # Check every location in the list of spheres.
    for i in range(len(PlaythroughLocations) - 2, -1, -1):
        sphere = PlaythroughLocations[i]
        # If there are more available GBs than the most expensive B. Locker needs, none of them are logically required
        # If there are fewer available GBs than the most expensive B. Locker requires, all of them are logically required
        if sphere.availableGBs > mostExpensiveBLocker:
            sphere.locations = [locationId for locationId in sphere.locations if LocationList[locationId].item != Items.GoldenBanana]
            continue
        for locationId in sphere.locations.copy():
            location = LocationList[locationId]
            # All GBs that make it here are logically required
            if location.item == Items.GoldenBanana:
                continue
            # Copy out item from location
            item = location.item
            location.item = None
            # Check if the game is still beatable
            Reset()
            if GetAccessibleLocations(settings, [], SearchMode.CheckBeatable):
                # If the game is still beatable, this is an unnecessary location, remove it.
                sphere.locations.remove(locationId)
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
        if len(sphere.locations) == 0:
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
        for loc in [x for x in sphere.locations if not LocationList[x].constant]:
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
        if location.item is None:
            empty.append(id)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        item = itemsToPlace.pop()
        itemEmpty = [x for x in empty if x in GetItemValidLocations(validLocations, item)]
        if len(itemEmpty) == 0:
            return len(itemsToPlace)
        random.shuffle(itemEmpty)
        locationId = itemEmpty.pop()
        LocationList[locationId].PlaceItem(item)
        empty.remove(locationId)
    return 0


def ForwardFill(settings, itemsToPlace, validLocations, ownedItems=None):
    """Forward fill algorithm for item placement."""
    if ownedItems is None:
        ownedItems = []
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
            itemValidLocations = list(LocationList)
    return itemValidLocations


def AssumedFill(settings, itemsToPlace, validLocations, ownedItems=None, isPriorityMove=False):
    """Assumed fill algorithm for item placement."""
    if ownedItems is None:
        ownedItems = []
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
            startKongList = []
            for x in settings.starting_kong_list:
                startKongList.append(x.name.capitalize())
            for i, kong in enumerate(startKongList):
                currentKongsFreed.insert(i, kong)
            currentMovesOwned = [ItemList[x].name for x in owned if ItemList[x].type == Types.Shop]
            currentGbCount = len([x for x in owned if ItemList[x].type == Types.Banana])
            js.postMessage("Current Moves owned at failure: " + str(currentMovesOwned) + " with GB count: " + str(currentGbCount) + " and kongs freed: " + str(currentKongsFreed))
            return len(itemsToPlace) + 1
        random.shuffle(validReachable)
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
            for i, kong in enumerate(settings.starting_kong_list):
                ownedKongs.insert(i, kong)
            kongBeingPlaced = KongFromItem(item)
            if kongBeingPlaced in ownedKongs:
                ownedKongs.remove(kongBeingPlaced)  # Cannot free with the kong being placed
            # If kongs are needed for level progression
            if settings.kongs_for_progression:
                # To lower failure rate, place kongs from later to earlier levels
                japesIndex = GetShuffledLevelIndex(Levels.JungleJapes)
                aztecIndex = GetShuffledLevelIndex(Levels.AngryAztec)
                factoryIndex = GetShuffledLevelIndex(Levels.FranticFactory)
                kongPriority = {}
                for i in range(0, 7):
                    if i == japesIndex:
                        if Locations.DiddyKong in settings.kong_locations:
                            kongPriority[Locations.DiddyKong] = i
                        else:
                            kongPriority[Locations.DiddyKong] = -1
                    elif i == aztecIndex:
                        if Locations.LankyKong in settings.kong_locations:
                            kongPriority[Locations.LankyKong] = i
                        else:
                            kongPriority[Locations.LankyKong] = -1
                        if Locations.TinyKong in settings.kong_locations:
                            kongPriority[Locations.TinyKong] = i
                        else:
                            kongPriority[Locations.TinyKong] = -1
                    elif i == factoryIndex:
                        if Locations.ChunkyKong in settings.kong_locations:
                            kongPriority[Locations.ChunkyKong] = i
                        else:
                            kongPriority[Locations.ChunkyKong] = -1
                validReachable.sort(key=lambda x: kongPriority[x], reverse=True)
        # Get a random, empty, reachable location
        for locationId in validReachable:
            # Atempt to place the item here
            LocationList[locationId].PlaceItem(item)
            # When placing a kong, also decide who among the owned kongs can free them
            if ItemList[item].type == Types.Kong:
                # If this is meant to be an empty cage, place no item here
                if locationId not in settings.kong_locations:
                    LocationList[locationId].PlaceItem(Items.NoItem)
                # Choose the puzzle solver, even if it's an empty cage
                if locationId == Locations.DiddyKong:
                    settings.diddy_freeing_kong = random.choice(ownedKongs)
                elif locationId == Locations.LankyKong:
                    settings.lanky_freeing_kong = random.choice(ownedKongs)
                elif locationId == Locations.TinyKong:
                    eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
                    if len(eligibleFreers) == 0:
                        js.postMessage("Failed placing item " + ItemList[item].name + " in location " + LocationList[locationId].name + ", due to no kongs being able to free them")
                        valid = False
                        break
                    settings.tiny_freeing_kong = random.choice(eligibleFreers)
                elif locationId == Locations.ChunkyKong:
                    settings.chunky_freeing_kong = random.choice(ownedKongs)
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
                validReachable = [x for x in reachable if x in itemValid and x != locationId]
                if len(validReachable) == 0:
                    js.postMessage("Failed placing item " + ItemList[item].name + " in location " + LocationList[locationId].name + ", due to too few remaining locations in play")
                    valid = False
                    break
                reachable.remove(validReachable[0])  # Remove one so same location can't be "used" twice
            # Attempt to verify coins
            # This check is skipped for priority items for the following reasons:
            # - We place only a handful of priority items and they must be bought anyway, so other expensive moves should be shifted instead
            # - We arbitrarily limit level (and therefore coin) access while placing priority moves, so this isn't an accurate check anyway
            if valid and ItemList[item].type == Types.Shop and not isPriorityMove:
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


def PlaceItems(settings, algorithm, itemsToPlace, ownedItems=None, validLocations=None, isPriorityMove=False):
    """Places items using given algorithm."""
    if ownedItems is None:
        ownedItems = []
    if validLocations is None:
        validLocations = []
    # Always use random fill with no logic
    if settings.no_logic:
        algorithm = "random"
    # If list of valid locations not provided, just use all valid locations
    if len(validLocations) == 0:
        validLocations = list(LocationList)
    if algorithm == "assumed":
        return AssumedFill(settings, itemsToPlace, validLocations, ownedItems, isPriorityMove)
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
            highPriorityUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.HighPriorityItems(spoiler.settings), ItemPool.HighPriorityAssumedItems(spoiler.settings))
            if highPriorityUnplaced > 0:
                raise Ex.ItemPlacementException(str(highPriorityUnplaced) + " unplaced high priority items.")
            # Then place blueprints
            Reset()
            blueprintsUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.Blueprints(spoiler.settings), ItemPool.BlueprintAssumedItems(spoiler.settings))
            if blueprintsUnplaced > 0:
                raise Ex.ItemPlacementException(str(blueprintsUnplaced) + " unplaced blueprints.")
            # Then place the rest of items
            Reset()
            lowPriorityUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.LowPriorityItems(spoiler.settings), ItemPool.ExcessItems(spoiler.settings))
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
            return
        except Ex.FillException as ex:
            if retries == 4:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            retries += 1
            js.postMessage("Retrying fill. Tries: " + str(retries))
            Reset()
            Logic.ClearAllLocations()


def ShuffleSharedMoves(spoiler):
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

    # If any shops have a kong's move placed, remove the shop from the pool for shared moves
    availableSharedShops = ItemPool.SharedMoveLocations.copy()
    kongMoveOccupiedShops = ItemPool.GetKongMoveOccupiedShops()
    for location in kongMoveOccupiedShops:
        availableSharedShops.remove(location)
    if len(availableSharedShops) < len(ItemPool.ImportantSharedMoves) + len(ItemPool.JunkSharedMoves):
        raise Ex.ItemPlacementException("Too many kong moves placed before shared moves. Only " + len(availableSharedShops) + " available for all shared moves.")

    # When a shared move is assigned to a shop in any particular level, that shop cannot also hold any kong-specific moves.
    # To avoid conflicts, first determine which level shops will have shared moves then remove these shops from each kong's valid locations list
    importantSharedUnplaced = PlaceItems(
        spoiler.settings, "assumed", ItemPool.ImportantSharedMoves.copy(), [x for x in ItemPool.AllItems(spoiler.settings) if x not in ItemPool.ImportantSharedMoves], availableSharedShops
    )
    if importantSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(importantSharedUnplaced) + " unplaced shared important items.")
    junkSharedUnplaced = PlaceItems(
        spoiler.settings, "random", ItemPool.JunkSharedMoves.copy(), [x for x in ItemPool.AllItems(spoiler.settings) if x not in ItemPool.JunkSharedMoves], validLocations=availableSharedShops
    )
    if junkSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(junkSharedUnplaced) + " unplaced shared junk items.")
    sharedMoveShops = []
    for sharedLocation in availableSharedShops:
        if LocationList[sharedLocation].item is not None:
            sharedMoveShops.append(sharedLocation)
    locationsToRemove = ItemPool.GetMoveLocationsToRemove(sharedMoveShops)
    # Now we need to set up the valid locations dictionary
    validLocations = {}
    kongMoveArrays = [ItemPool.DonkeyMoves, ItemPool.DiddyMoves, ItemPool.LankyMoves, ItemPool.TinyMoves, ItemPool.ChunkyMoves]
    kongLocationArrays = [ItemPool.DonkeyMoveLocations, ItemPool.DiddyMoveLocations, ItemPool.LankyMoveLocations, ItemPool.TinyMoveLocations, ItemPool.ChunkyMoveLocations]
    mergedLocationArrays = ItemPool.DonkeyMoveLocations.copy()
    mergedLocationArrays.update(ItemPool.DiddyMoveLocations.copy())
    mergedLocationArrays.update(ItemPool.LankyMoveLocations.copy())
    mergedLocationArrays.update(ItemPool.TinyMoveLocations.copy())
    mergedLocationArrays.update(ItemPool.ChunkyMoveLocations.copy())
    for i in range(5):
        for item in kongMoveArrays[i]:
            if spoiler.settings.move_rando == "on_cross_purchase":
                validLocations[item] = mergedLocationArrays - locationsToRemove
            else:
                validLocations[item] = kongLocationArrays[i] - locationsToRemove
    return (kongMoves, validLocations)


def FillKongsAndMovesGeneric(spoiler):
    """Facilitate shuffling individual pools of items in lieu of full item rando."""
    retries = 0
    while True:
        try:
            FillKongsAndMoves(spoiler)
            # Check if game is beatable
            Reset()
            if not VerifyWorldWithWorstCoinUsage(spoiler.settings):
                raise Ex.GameNotBeatableException("Game unbeatable after placing all items.")
            return
        except Ex.FillException as ex:
            if retries == 20:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            retries += 1
            js.postMessage("Retrying fill. Tries: " + str(retries))
            Reset()
            Logic.ClearAllLocations()


def GeneratePlaythrough(spoiler):
    """Generate playthrough and way of the hoard and update spoiler."""
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


def GetKongUnlockingMovesAndValidLocations(spoiler, location, ownedKongs=[]):
    """Given the settings and a locked Kong's location, determine the moves needed to unlock them in preparation for PlaceItems. Note that `ownedKongs` is only needed for Locations.LankyKong."""
    kongUnlockingItemsDict = {}
    if location == Locations.DiddyKong:
        # We need the Diddy freeing Kong's gun
        gun = Items.Coconut
        validLocations = ItemPool.DonkeyMoveLocations.copy()
        if spoiler.settings.diddy_freeing_kong == Kongs.diddy:
            gun = Items.Peanut
            validLocations = ItemPool.DiddyMoveLocations.copy()
        elif spoiler.settings.diddy_freeing_kong == Kongs.lanky:
            gun = Items.Grape
            validLocations = ItemPool.LankyMoveLocations.copy()
        elif spoiler.settings.diddy_freeing_kong == Kongs.tiny:
            gun = Items.Feather
            validLocations = ItemPool.TinyMoveLocations.copy()
        elif spoiler.settings.diddy_freeing_kong == Kongs.chunky:
            gun = Items.Pineapple
            validLocations = ItemPool.ChunkyMoveLocations.copy()
        kongUnlockingItemsDict[gun] = validLocations
    elif location == Locations.LankyKong:
        # We always need the guitar to get to the Llama Temple - make extra double triple sure it doesn't lock itself
        kongUnlockingItemsDict[Items.Guitar] = ItemPool.DiddyMoveLocations.copy()
        kongUnlockingItemsDict[Items.Guitar].remove(Locations.DiddyAztecGun)
        kongUnlockingItemsDict[Items.Guitar].remove(Locations.RocketbarrelBoost)
        # We also need a different Kong's gun to get into the Llama Temple
        llamaTempleOpeningKong = random.choice([kong for kong in ownedKongs if kong in (Kongs.donkey, Kongs.lanky, Kongs.tiny)])
        llamaTempleOpeningGun = Items.Coconut
        llamaTempleOpeningGunLocations = ItemPool.DonkeyMoveLocations
        if llamaTempleOpeningKong == Kongs.lanky:
            llamaTempleOpeningGun = Items.Grape
            llamaTempleOpeningGunLocations = ItemPool.LankyMoveLocations
        elif llamaTempleOpeningKong == Kongs.tiny:
            llamaTempleOpeningGun = Items.Feather
            llamaTempleOpeningGunLocations = ItemPool.TinyMoveLocations
        kongUnlockingItemsDict[llamaTempleOpeningGun] = llamaTempleOpeningGunLocations
        # We need the gun and instrument of the Lanky freeing Kong
        gun = Items.Coconut
        instrument = Items.Bongos
        validLocations = ItemPool.DonkeyMoveLocations
        if spoiler.settings.lanky_freeing_kong == Kongs.diddy:
            gun = Items.Peanut
            instrument = Items.Guitar
            validLocations = ItemPool.DiddyMoveLocations
        elif spoiler.settings.lanky_freeing_kong == Kongs.lanky:
            gun = Items.Grape
            instrument = Items.Trombone
            validLocations = ItemPool.LankyMoveLocations
        elif spoiler.settings.lanky_freeing_kong == Kongs.tiny:
            gun = Items.Feather
            instrument = Items.Saxophone
            validLocations = ItemPool.TinyMoveLocations
        elif spoiler.settings.lanky_freeing_kong == Kongs.chunky:
            gun = Items.Pineapple
            instrument = Items.Triangle
            validLocations = ItemPool.ChunkyMoveLocations
        kongUnlockingItemsDict[gun] = validLocations
        kongUnlockingItemsDict[instrument] = validLocations
    elif location == Locations.TinyKong:
        # We need Peanut & Charge or Pineapple & Punch to open Tiny's cage
        gun = Items.Peanut
        move = Items.ChimpyCharge
        validLocations = ItemPool.DiddyMoveLocations
        if spoiler.settings.tiny_freeing_kong == Kongs.chunky:
            gun = Items.Pineapple
            move = Items.PrimatePunch
            validLocations = ItemPool.ChunkyMoveLocations
        kongUnlockingItemsDict[gun] = validLocations
        kongUnlockingItemsDict[move] = validLocations
    # Locations.ChunkyKong has no prerequisites yet

    # If cross Kong purchases are enabled, then expand the valid item location lists
    if spoiler.settings.move_rando == "on_cross_purchase":
        allKongMoveLocations = ItemPool.DonkeyMoveLocations.copy()
        allKongMoveLocations.update(ItemPool.DiddyMoveLocations.copy())
        allKongMoveLocations.update(ItemPool.LankyMoveLocations.copy())
        allKongMoveLocations.update(ItemPool.TinyMoveLocations.copy())
        allKongMoveLocations.update(ItemPool.ChunkyMoveLocations.copy())
        allKongMoveLocations = list(allKongMoveLocations)
        for item in kongUnlockingItemsDict:
            kongUnlockingItemsDict[item] = allKongMoveLocations
    return kongUnlockingItemsDict


def GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLevel):
    """Find the logically accessible Kong Locations given the current state of Kong unlocking."""
    logicallyAccessibleKongLocations = []
    for level in range(1, latestLevel + 1):
        if spoiler.settings.level_order[level] == Levels.JungleJapes and Locations.DiddyKong in kongLocations:
            logicallyAccessibleKongLocations.append(Locations.DiddyKong)
        if spoiler.settings.level_order[level] == Levels.FranticFactory and Locations.ChunkyKong in kongLocations:
            logicallyAccessibleKongLocations.append(Locations.ChunkyKong)
        if spoiler.settings.level_order[level] == Levels.AngryAztec and Locations.TinyKong in kongLocations and (Kongs.diddy in ownedKongs or Kongs.chunky in ownedKongs):
            logicallyAccessibleKongLocations.append(Locations.TinyKong)
        if (
            spoiler.settings.level_order[level] == Levels.AngryAztec
            and Locations.LankyKong in kongLocations
            and (Kongs.diddy in ownedKongs or spoiler.settings.open_levels)  # Must be able to open Guitar door
            and (Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs)
        ):  # Must be able to open Llama Temple
            logicallyAccessibleKongLocations.append(Locations.LankyKong)
    return logicallyAccessibleKongLocations


def PlaceKongs(spoiler, kongItems, kongLocations):
    """For these settings, Kongs to place, and locations to place them in, place the Kongs in such a way the generation will never error here."""
    ownedKongs = [kong for kong in spoiler.settings.starting_kong_list]
    # In entrance randomizer, it's too complicated to quickly determine kong accessibility.
    # Instead, we place Kongs in a specific order to guarantee we'll at least have an eligible freer.
    # To be at least somewhat nice to no logic users, we also use this section here so kongs don't lock each other.
    if spoiler.settings.shuffle_loading_zones == "all" or spoiler.settings.no_logic:
        random.shuffle(kongItems)
        if Locations.ChunkyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.ChunkyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.chunky_freeing_kong = random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        if Locations.DiddyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.DiddyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.diddy_freeing_kong = random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # The Lanky location can't be your first in cases where the Lanky freeing Kong can't get into the llama temple and you need a second Kong
        if Locations.LankyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.LankyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.lanky_freeing_kong = random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # Placing the Tiny location last guarantees we have one of Diddy or Chunky
        if Locations.TinyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.TinyKong].PlaceItem(kongItemToBeFreed)
            eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
            spoiler.settings.tiny_freeing_kong = random.choice(eligibleFreers)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
    # In level order shuffling, we need to be very particular about who we unlock and in what order so as to guarantee completion
    # Vanilla levels can be treated as if the level shuffler randomly placed all the levels in the same order
    elif spoiler.settings.shuffle_loading_zones in ("levels", "none"):
        latestLogicallyAllowedLevel = len(ownedKongs) + 1
        logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
        while len(ownedKongs) != 5:
            # If there aren't any accessible Kong locations, then the level order shuffler has a bug (this shouldn't happen)
            if not any(logicallyAccessibleKongLocations):
                raise Ex.EntrancePlacementException("Levels shuffled in a way that makes Kong unlocks impossible. SEND THIS TO THE DEVS!")
            # Begin by finding the currently accessible Kong locations
            # Randomly pick an accessible location
            progressionLocation = random.choice(logicallyAccessibleKongLocations)
            logicallyAccessibleKongLocations.remove(progressionLocation)
            # Pick a Kong to free this location from the Kongs we currently have
            if progressionLocation == Locations.DiddyKong:
                spoiler.settings.diddy_freeing_kong = random.choice(ownedKongs)
            elif progressionLocation == Locations.LankyKong:
                spoiler.settings.lanky_freeing_kong = random.choice(ownedKongs)
            elif progressionLocation == Locations.TinyKong:
                eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
                spoiler.settings.tiny_freeing_kong = random.choice(eligibleFreers)
            elif progressionLocation == Locations.ChunkyKong:
                spoiler.settings.chunky_freeing_kong = random.choice(ownedKongs)
            # Remove this location from any considerations
            kongLocations.remove(progressionLocation)
            # Pick a Kong to unlock from the locked Kongs
            kongToBeFreed = random.choice(kongItems)
            # With this kong, we can progress one level further
            latestLogicallyAllowedLevel += 1
            # If this Kong must unlock more locked Kong locations, we have to be more careful
            # The second condition here because we don't need to worry about the last placed Kong
            if len(logicallyAccessibleKongLocations) == 0 and len(kongItems) > 1:
                # First check if that newly accessible level adds a location. If it does, then it doesn't matter who we free here
                logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
                if not any(logicallyAccessibleKongLocations):
                    # If it doesn't, then we need to see which Kongs will open more Kongs
                    progressionKongItems = []
                    for kongItem in kongItems:
                        # Test each Kong by temporarily owning them and seeing what we can now reach
                        tempOwnedKongs = [x for x in ownedKongs]
                        tempOwnedKongs.append(ItemPool.GetKongForItem(kongItem))
                        newlyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, tempOwnedKongs, latestLogicallyAllowedLevel)
                        if any(newlyAccessibleKongLocations):
                            progressionKongItems.append(kongItem)
                    # Pick a random Kong from the Kongs that guarantee progression
                    kongToBeFreed = random.choice(progressionKongItems)
            # Now that we have a combination guaranteed to not break the seed or logic, lock it in
            LocationList[progressionLocation].PlaceItem(kongToBeFreed)
            kongItems.remove(kongToBeFreed)
            ownedKongs.append(ItemPool.GetKongForItem(kongToBeFreed))
            # Refresh the location list and repeat until all Kongs are free
            logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
    # Pick freeing kongs for any that are still "any" with no restrictions.
    if spoiler.settings.diddy_freeing_kong == Kongs.any:
        spoiler.settings.diddy_freeing_kong = random.choice(GetKongs())
    if spoiler.settings.lanky_freeing_kong == Kongs.any:
        spoiler.settings.lanky_freeing_kong = random.choice(GetKongs())
    if spoiler.settings.tiny_freeing_kong == Kongs.any:
        spoiler.settings.tiny_freeing_kong = random.choice(GetKongs())
    if spoiler.settings.chunky_freeing_kong == Kongs.any:
        spoiler.settings.chunky_freeing_kong = random.choice(GetKongs())


def FillKongsAndMoves(spoiler):
    """Fill kongs, then progression moves, then shared moves, then rest of moves."""
    itemsToPlace = []
    validLocations = {}
    preplacedPriorityMoves = []

    # Handle kong rando
    if spoiler.settings.kong_rando:
        # Determine what kong items need to be placed
        kongItems = ItemPool.Kongs(spoiler.settings)
        for kongItem in kongItems:
            if ItemPool.GetKongForItem(kongItem) in spoiler.settings.starting_kong_list:
                kongItems.remove(kongItem)
        # Determine what locations the kong items need to be placed in
        kongValidLocations = {}
        kongLocations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
        if any(spoiler.settings.kong_locations):
            emptyKongLocations = [location for location in kongLocations if location not in spoiler.settings.kong_locations]
            for locationId in emptyKongLocations:
                LocationList[locationId].PlaceItem(Items.NoItem)
                kongLocations.remove(locationId)
        for item in kongItems:
            kongValidLocations[item] = kongLocations
        # We place Kongs first so we know what Kong moves are most important to place next
        Reset()
        # Specialized Kong placement function that will never fail to find a beatable combination of Kong unlocks
        PlaceKongs(spoiler, kongItems, [x for x in kongLocations])

        # If kongs are our progression, then place moves that unlock those kongs before anything else
        # This logic only matters if the level order is critical to progression (i.e. not loading zone shuffled)
        if spoiler.settings.kongs_for_progression and spoiler.settings.shuffle_loading_zones != "all" and spoiler.settings.move_rando != "start_with":
            locationsLockingKongs = [location for location in kongLocations]
            ownedKongs = [kong for kong in spoiler.settings.starting_kong_list]
            latestLogicallyAllowedLevel = spoiler.settings.starting_kongs_count + 1
            levelIndex = 1
            checkedAllLogicallyAvailableLevels = False
            # Loop until we've logically unlocked all the kongs
            # It may take multiple loops through available levels before we unlock all kongs
            while len(ownedKongs) != 5:
                latestLogicallyAllowedLevel = len(ownedKongs) + 1
                priorityItemsDict = {}
                kongToBeGained = None
                # For each level that has a locked kong, identify the items needed to unlock them
                # We're about to place these items in accessible locations, so assume can we now own the kong
                if spoiler.settings.level_order[levelIndex] == Levels.FranticFactory and Locations.ChunkyKong in locationsLockingKongs and spoiler.settings.chunky_freeing_kong in ownedKongs:
                    locationsLockingKongs.remove(Locations.ChunkyKong)
                    kongToBeGained = ItemPool.GetKongForItem(LocationList[Locations.ChunkyKong].item)
                if spoiler.settings.level_order[levelIndex] == Levels.JungleJapes and Locations.DiddyKong in locationsLockingKongs and spoiler.settings.diddy_freeing_kong in ownedKongs:
                    locationsLockingKongs.remove(Locations.DiddyKong)
                    priorityItemsDict = GetKongUnlockingMovesAndValidLocations(spoiler, Locations.DiddyKong)
                    for alreadyPriorityPlacedMove in preplacedPriorityMoves:
                        priorityItemsDict.pop(alreadyPriorityPlacedMove, None)
                    kongToBeGained = ItemPool.GetKongForItem(LocationList[Locations.DiddyKong].item)
                if spoiler.settings.level_order[levelIndex] == Levels.AngryAztec and Locations.TinyKong in locationsLockingKongs and spoiler.settings.tiny_freeing_kong in ownedKongs:
                    locationsLockingKongs.remove(Locations.TinyKong)
                    priorityItemsDict = GetKongUnlockingMovesAndValidLocations(spoiler, Locations.TinyKong)
                    for alreadyPriorityPlacedMove in preplacedPriorityMoves:
                        priorityItemsDict.pop(alreadyPriorityPlacedMove, None)
                    kongToBeGained = ItemPool.GetKongForItem(LocationList[Locations.TinyKong].item)
                elif (
                    spoiler.settings.level_order[levelIndex] == Levels.AngryAztec
                    and Locations.LankyKong in locationsLockingKongs
                    and spoiler.settings.lanky_freeing_kong in ownedKongs
                    and (Kongs.diddy in ownedKongs or spoiler.settings.open_levels)
                    and (Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs)
                ):
                    locationsLockingKongs.remove(Locations.LankyKong)
                    priorityItemsDict = GetKongUnlockingMovesAndValidLocations(spoiler, Locations.LankyKong, ownedKongs)
                    for alreadyPriorityPlacedMove in preplacedPriorityMoves:
                        priorityItemsDict.pop(alreadyPriorityPlacedMove, None)
                    kongToBeGained = ItemPool.GetKongForItem(LocationList[Locations.LankyKong].item)

                # Place the priority items and any items they may depend on
                while any(priorityItemsDict):
                    # Do not allow anything here to be placed in levels that would break the level order kong logic
                    # The -1 is because we just added 1 earlier and there isn't a convenient way to do it later
                    BlockAccessToLevel(spoiler.settings, latestLogicallyAllowedLevel)
                    Reset()
                    priorityItems = list(priorityItemsDict.keys())
                    # Assume we have all other moves as we place items. This increases the potential number of locations items can be shuffled into
                    allOtherItems = ItemPool.AllKongMoves().copy()
                    # Two exceptions: we don't assume we have the items to be placed, as then they could lock themselves
                    for item in priorityItemsDict.keys():
                        allOtherItems.remove(item)
                    # We also don't assume we have any preplaced priority moves. If these unlock locations we should find them as we go.
                    # This should prevent circular logic (e.g. the diddy-unlocking-gun being locked behind guitar which is already priority placed in Japes Cranky)
                    for item in preplacedPriorityMoves:
                        allOtherItems.remove(item)
                    unplaced = PlaceItems(spoiler.settings, "assumed", priorityItems, ownedItems=allOtherItems, validLocations=priorityItemsDict, isPriorityMove=True)
                    if unplaced > 0:
                        raise Ex.ItemPlacementException("Failed to place items that would unlock Kong number " + str(len(ownedKongs) + 1) + ", " + kongToBeGained.name)
                    preplacedPriorityMoves.extend(list(priorityItemsDict.keys()))
                    # After placing these priority items, the new locations may require some of those items we assumed we had
                    priorityItemDependencyDict = {}
                    # However, the open levels setting removes all of the possible dependencies
                    if not spoiler.settings.open_levels:
                        for item in list(priorityItemsDict.keys()):
                            # Get the location of these priority items
                            location = None
                            for possibleLocationThisItemGotPlaced in priorityItemsDict[item]:
                                if LocationList[possibleLocationThisItemGotPlaced].item == item:
                                    location = possibleLocationThisItemGotPlaced
                                    break
                            # Check all the shops that are locked by items
                            # Aztec Cranky and Funky are locked by Guitar
                            if (location in ItemPool.AztecCrankyMoveLocations or location in ItemPool.AztecFunkyMoveLocations) and Items.Guitar not in preplacedPriorityMoves:
                                guitarLocations = ItemPool.DiddyMoveLocations.copy()
                                priorityItemDependencyDict[Items.Guitar] = guitarLocations
                            # Forest Funky is locked by Feather and Pineapple
                            if location in ItemPool.ForestFunkyMoveLocations:
                                # There's no way a kong locked behind Forest Funky can be your second kong
                                # This _should_ be covered by the ownedItems=OwnedKongMoves preventing you from having the guns to get to it, which in turn prevents access to that shop unless you have both Chunky and Tiny
                                if len(ownedKongs) == 1:
                                    raise Ex.ItemPlacementException("Fungi Funky logic issue - SEND THIS TO A DEV!")
                                if Items.Feather not in preplacedPriorityMoves:
                                    featherLocations = ItemPool.TinyMoveLocations.copy()
                                    priorityItemDependencyDict[Items.Feather] = featherLocations
                                if Items.Pineapple not in preplacedPriorityMoves:
                                    pineappleLocations = ItemPool.ChunkyMoveLocations.copy()
                                    priorityItemDependencyDict[Items.Pineapple] = pineappleLocations
                                # Japes Cranky is locked by the diddy_freeing_kong's gun, but that's covered by the Locations.DiddyKong dependencies by this logic:
                                # A: There's a kong there and either...
                                #   We'll have already placed the dependencies for it because it's in an earlier level
                                #   Or it won't be an option logically
                                # B: There isn't a kong there and the gates are already open
                    # If we found any dependencies, we have to check for further dependencies
                    priorityItemsDict = priorityItemDependencyDict
                # Update progression with any newly acquired Kongs
                if kongToBeGained is not None:
                    ownedKongs.append(kongToBeGained)
                    checkedAllLogicallyAvailableLevels = False
                # If we didn't find progression here, check the next logically available level
                else:
                    # If we checked all the levels and don't have all the kongs, then we're logic-locked (somehow)
                    if levelIndex == latestLogicallyAllowedLevel and checkedAllLogicallyAvailableLevels:
                        raise Ex.ItemPlacementException("Kongs logically locked behind themselves. Only " + str(len(ownedKongs)) + " kongs logically accessible.")
                    elif levelIndex == latestLogicallyAllowedLevel:
                        checkedAllLogicallyAvailableLevels = True
                    # Wrap back to level 1 if we hit the end - it's logically possible we've now unlocked a kong that frees an earlier kong
                    levelIndex = (levelIndex % latestLogicallyAllowedLevel) + 1
            # Undo any level blocking that may have been performed
            BlockAccessToLevel(spoiler.settings, 100)

    # Handle shared moves before other moves in move rando
    if spoiler.settings.shuffle_items == "moves":
        # Shuffle the shared move locations since they must be done first,
        # and return the kong moves and their locations
        (moveItems, moveLocations) = ShuffleSharedMoves(spoiler)
        itemsToPlace.extend(moveItems)
        validLocations.update(moveLocations)

    # Handle remaining moves/items
    Reset()
    itemsToPlace = [item for item in itemsToPlace if item not in preplacedPriorityMoves]
    unplaced = PlaceItems(spoiler.settings, "assumed", itemsToPlace, [], validLocations=validLocations)
    if unplaced > 0:
        raise Ex.ItemPlacementException(str(unplaced) + " unplaced items.")


def FillKongsAndMovesForLevelOrder(spoiler):
    """Shuffle Kongs and Moves accounting for level order restrictions."""
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
    # print("Starting Kongs: " + str([kong.name + " " for kong in spoiler.settings.starting_kong_list]))
    # Need to place constants to update boss key items after shuffling levels
    ItemPool.PlaceConstants(spoiler.settings)
    retries = 0
    while True:
        try:
            # Assume we can progress through the levels so long as we have enough kongs
            WipeProgressionRequirements(spoiler.settings)
            spoiler.settings.kongs_for_progression = True
            # Fill the kongs and the moves
            FillKongsAndMoves(spoiler)
            # Update progression requirements based on what is now accessible after all shuffles are done
            SetNewProgressionRequirements(spoiler.settings)
            # Once progression requirements updated, no longer assume we need kongs freed for level progression
            spoiler.settings.kongs_for_progression = False
            # Check if game is beatable
            if not VerifyWorldWithWorstCoinUsage(spoiler.settings):
                raise Ex.GameNotBeatableException("Game unbeatable after placing all items.")
            return
        except Ex.FillException as ex:
            Reset()
            Logic.ClearAllLocations()
            retries += 1
            if retries == 20:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            # Every 5th fill, retry more aggressively by reshuffling level order and move prices
            if retries % 5 == 0:
                js.postMessage("Retrying fill really hard. Tries: " + str(retries))
                spoiler.settings.shuffle_prices()
                if spoiler.settings.shuffle_loading_zones == "levels":
                    ShuffleExits.ShuffleExits(spoiler.settings)
                    spoiler.UpdateExits()
            else:
                js.postMessage("Retrying fill. Tries: " + str(retries))


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


def WipeProgressionRequirements(settings: Settings):
    """Wipe out progression requirements to assume access through main 7 levels."""
    for i in range(0, 7):
        # Assume T&S and B.Locker amounts will be attainable for now
        settings.EntryGBs[i] = 0
        settings.BossBananas[i] = 0
        # Assume starting kong can beat all the bosses for now
        settings.boss_kongs[i] = settings.starting_kong
        settings.boss_maps[i] = Maps.JapesBoss
    # Also for now consider any kong can free any other kong, to avoid false failures in fill
    if settings.kong_rando:
        settings.diddy_freeing_kong = Kongs.any
        settings.lanky_freeing_kong = Kongs.any
        settings.tiny_freeing_kong = Kongs.any
        settings.chunky_freeing_kong = Kongs.any


def SetNewProgressionRequirements(settings: Settings):
    """Set new progression requirements based on what is owned or accessible heading into each level."""
    # Find for each level: # of accessible bananas, total GBs, owned kongs & owned moves
    coloredBananaCounts = []
    goldenBananaTotals = []
    ownedKongs = {}
    ownedMoves = {}
    if settings.unlock_all_moves:
        allMoves = ItemPool.DonkeyMoves.copy()
        allMoves.extend(ItemPool.DiddyMoves)
        allMoves.extend(ItemPool.LankyMoves)
        allMoves.extend(ItemPool.TinyMoves)
        allMoves.extend(ItemPool.ChunkyMoves)
        allMoves.extend(ItemPool.ImportantSharedMoves)
    for level in range(1, 8):
        BlockAccessToLevel(settings, level)
        Reset()
        accessible = GetAccessibleLocations(settings, [])
        previousLevel = GetLevelShuffledToIndex(level - 1)
        coloredBananaCounts.append(LogicVariables.ColoredBananas[previousLevel])
        goldenBananaTotals.append(LogicVariables.GoldenBananas)
        ownedKongs[previousLevel] = LogicVariables.GetKongs()
        if settings.unlock_all_moves:
            ownedMoves[previousLevel] = allMoves
        else:
            accessibleMoves = [LocationList[x].item for x in accessible if LocationList[x].type == Types.Shop and LocationList[x].item != Items.NoItem and LocationList[x].item is not None]
            ownedMoves[previousLevel] = accessibleMoves
    # Cap the B. Locker and T&S amounts based on a random fraction of accessible bananas & GBs
    BLOCKER_MIN = 0.4
    BLOCKER_MAX = 0.7
    settings.EntryGBs = [
        min(settings.blocker_0, 1),  # First B. Locker shouldn't be more than 1 GB
        min(settings.blocker_1, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[0]))),
        min(settings.blocker_2, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[1]))),
        min(settings.blocker_3, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[2]))),
        min(settings.blocker_4, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[3]))),
        min(settings.blocker_5, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[4]))),
        min(settings.blocker_6, max(1, round(random.uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[5]))),
        settings.blocker_7,  # Last B. Locker shouldn't be affected
    ]
    settings.BossBananas = [
        min(settings.troff_0, round(settings.troff_0 / (settings.troff_max * settings.troff_weight_0) * sum(coloredBananaCounts[0]))),
        min(settings.troff_1, round(settings.troff_1 / (settings.troff_max * settings.troff_weight_1) * sum(coloredBananaCounts[1]))),
        min(settings.troff_2, round(settings.troff_2 / (settings.troff_max * settings.troff_weight_2) * sum(coloredBananaCounts[2]))),
        min(settings.troff_3, round(settings.troff_3 / (settings.troff_max * settings.troff_weight_3) * sum(coloredBananaCounts[3]))),
        min(settings.troff_4, round(settings.troff_4 / (settings.troff_max * settings.troff_weight_4) * sum(coloredBananaCounts[4]))),
        min(settings.troff_5, round(settings.troff_5 / (settings.troff_max * settings.troff_weight_5) * sum(coloredBananaCounts[5]))),
        min(settings.troff_6, round(settings.troff_6 / (settings.troff_max * settings.troff_weight_6) * sum(coloredBananaCounts[6]))),
    ]
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)
    ShuffleBossesBasedOnOwnedItems(settings, ownedKongs, ownedMoves)


def BlockAccessToLevel(settings: Settings, level):
    """Assume the level index passed in is the furthest level you have access to in the level order."""
    for i in range(0, 7):
        if i >= level:
            # This level and those after it are locked out
            settings.EntryGBs[i] = 1000
            settings.BossBananas[i] = 1000
        else:
            # Previous levels assumed accessible
            settings.EntryGBs[i] = 0
            settings.BossBananas[i] = 0
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)


def Generate_Spoiler(spoiler):
    """Generate a complete spoiler based on input settings."""
    # Init logic vars with settings
    global LogicVariables
    LogicVariables = LogicVarHolder(spoiler.settings)
    # Initiate kasplat map with default
    InitKasplatMap(LogicVariables)
    # Handle Kong Rando + Level Rando combination separately since it is more restricted
    if spoiler.settings.kongs_for_progression:
        # Handle Level Order if randomized
        if spoiler.settings.shuffle_loading_zones == "levels":
            ShuffleExits.ShuffleExits(spoiler.settings)
            spoiler.UpdateExits()
        # Assume we can progress through the levels, since these will be adjusted within FillKongsAndMovesForLevelRando
        WipeProgressionRequirements(spoiler.settings)
        # Handle misc randomizations
        ShuffleMisc(spoiler)
        # Handle Item Fill
        FillKongsAndMovesForLevelOrder(spoiler)
    else:
        # Handle misc randomizations
        ShuffleMisc(spoiler)
        # Handle Loading Zones
        if spoiler.settings.shuffle_loading_zones != "none":
            ShuffleExits.ExitShuffle(spoiler.settings)
            spoiler.UpdateExits()
        # Handle Item Fill
        if spoiler.settings.shuffle_items == "all":
            Fill(spoiler)
        elif spoiler.settings.shuffle_items == "moves" or spoiler.settings.kong_rando:
            FillKongsAndMovesGeneric(spoiler)
        else:
            # Just check if normal item locations are beatable with given settings
            ItemPool.PlaceConstants(spoiler.settings)
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.VanillaItemsGameNotBeatableException("Game unbeatable.")
    GeneratePlaythrough(spoiler)
    Reset()
    ShuffleExits.Reset()
    return spoiler


def ShuffleMisc(spoiler):
    """Shuffle miscellaneous objects outside of main fill algorithm, including Kasplats, Bonus barrels, and bananaport warps."""
    # Handle kasplats
    KasplatShuffle(spoiler, LogicVariables)
    spoiler.human_kasplats = {}
    spoiler.UpdateKasplats(LogicVariables.kasplat_map)
    # Handle bonus barrels
    if spoiler.settings.bonus_barrels in ("random", "all_beaver_bother"):
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # Handle Bananaports
    if spoiler.settings.bananaport_rando:
        replacements = []
        human_replacements = {}
        ShuffleWarps(replacements, human_replacements)
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    if spoiler.settings.random_patches:
        human_patches = []
        spoiler.human_patches = ShufflePatches(spoiler, human_patches).copy()

    if spoiler.settings.activate_all_bananaports in ["all", "isles"]:
        warpMapIds = set([BananaportVanilla[warp].map_id for warp in Warps])
        for map_id in warpMapIds:
            mapWarps = [BananaportVanilla[warp] for warp in Warps if BananaportVanilla[warp].map_id == map_id]
            for warpData in mapWarps:
                pairedWarpData = [
                    BananaportVanilla[pair]
                    for pair in Warps
                    if BananaportVanilla[pair].map_id == map_id and BananaportVanilla[pair].new_warp == warpData.new_warp and BananaportVanilla[pair].name != warpData.name
                ][0]
                # Add an exit to each warp's region to the paired warp's region unless it's the same region
                if warpData.region_id != pairedWarpData.region_id and (spoiler.settings.activate_all_bananaports == "all" or (warpData.map_id == Maps.Isles)):
                    warpRegion = Logic.Regions[warpData.region_id]
                    bananaportExit = TransitionFront(pairedWarpData.region_id, lambda l: True)
                    warpRegion.exits.append(bananaportExit)
