"""Module used to distribute items randomly."""
from json import dumps
from random import shuffle, choice, uniform, randint

import js
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.ShuffleDoors import ShuffleDoors
import randomizer.ShuffleExits as ShuffleExits
import randomizer.LogicFiles.DKIsles as IslesLogic
from randomizer.CompileHints import compileHints
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Enums.Warps import Warps
from randomizer.Lists.Item import ItemList, KongFromItem
from randomizer.Lists.Location import LocationList, TrainingBarrelLocations, DonkeyMoveLocations, DiddyMoveLocations, LankyMoveLocations, TinyMoveLocations, ChunkyMoveLocations, SharedMoveLocations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Lists.ShufflableExit import GetLevelShuffledToIndex, GetShuffledLevelIndex
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Logic import LogicVarHolder, LogicVariables
from randomizer.Logic import Regions as RegionList
from randomizer.LogicClasses import Sphere, TransitionFront
from randomizer.Prices import GetMaxForKong
from randomizer.Settings import Settings
from randomizer.ShuffleBarrels import BarrelShuffle
from randomizer.ShuffleBosses import ShuffleBossesBasedOnOwnedItems
from randomizer.ShuffleKasplats import InitKasplatMap, KasplatShuffle
from randomizer.ShufflePatches import ShufflePatches
from randomizer.ShuffleShopLocations import ShuffleShopLocations
from randomizer.ShuffleWarps import ShuffleWarps, ShuffleWarpsCrossMap
from randomizer.ShuffleCBs import ShuffleCBs
from randomizer.ShuffleCrowns import ShuffleCrowns
from randomizer.ShuffleItems import ShuffleItems


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


def GetAccessibleLocations(settings, startingOwnedItems, searchType=SearchMode.GetReachable, purchaseList=None, targetItemId=None):
    """Search to find all reachable locations given owned items."""
    # No logic? Calls to this method that are checking things just return True
    if settings.no_logic and searchType in [SearchMode.CheckAllReachable, SearchMode.CheckBeatable, SearchMode.CheckSpecificItemReachable]:
        return True
    if purchaseList is None:
        purchaseList = []
    accessible = set()
    newLocations = set()
    ownedItems = startingOwnedItems.copy()
    newItems = []  # debug code utility
    playthroughLocations = []
    eventAdded = True
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or eventAdded:
        # Add items and events from the last search iteration
        sphere = Sphere()
        if playthroughLocations:
            sphere.availableGBs = playthroughLocations[-1].availableGBs
        for locationId in newLocations:
            accessible.add(locationId)
            location = LocationList[locationId]
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                # In search mode GetReachableWithControlledPurchases, only allowed to purchase items as prescribed by purchaseOrder
                if location.type == Types.Shop and searchType == SearchMode.GetReachableWithControlledPurchases and locationId not in purchaseList:
                    continue
                ownedItems.append(location.item)
                newItems.append(location.item)
                # If we want to generate the playthrough and the item is a playthrough item, add it to the sphere
                if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
                    if location.item == Items.GoldenBanana:
                        sphere.availableGBs += 1
                        sphere.locations.append(locationId)
                        continue
                    # Banana hoard in a sphere by itself
                    elif location.item == Items.BananaHoard:
                        sphere.locations = [locationId]
                        break
                    sphere.locations.append(locationId)
                # If we're looking for one item and we find it, we're done
                elif searchType == SearchMode.CheckSpecificItemReachable and location.item == targetItemId:
                    return True
        eventAdded = False
        # Reset new lists
        newLocations = set()
        # Update based on new items
        LogicVariables.Update(ownedItems)
        newItems = []
        if len(sphere.locations) > 0:
            if searchType == SearchMode.GeneratePlaythrough:
                sphere.seedBeaten = LogicVariables.bananaHoard
            playthroughLocations.append(sphere)

        # If we're checking beatability, check for the Banana Hoard after updating the last set of locations
        if searchType == SearchMode.CheckBeatable and LogicVariables.bananaHoard:
            return True

        # Do a search for each owned kong
        for kong in set(LogicVariables.GetKongs()):
            LogicVariables.SetKong(kong)

            startRegion = Logic.Regions[Regions.GameStart]
            startRegion.id = Regions.GameStart
            startRegion.dayAccess = True
            startRegion.nightAccess = Events.Night in LogicVariables.Events
            regionPool = set()
            regionPool.add(startRegion)
            addedRegions = set()
            addedRegions.add(Regions.GameStart)

            tagAccess = [(key, value) for (key, value) in Logic.Regions.items() if value.HasAccess(kong) and key not in addedRegions]
            addedRegions.update([x[0] for x in tagAccess])  # first value is the region key
            regionPool.update([x[1] for x in tagAccess])  # second value is the region itself

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
                        if not collectible.added and collectible.kong in (kong, Kongs.any) and collectible.enabled and collectible.logic(LogicVariables):
                            LogicVariables.AddCollectible(collectible, region.level)
                # Check accessibility for each location in this region
                for location in region.locations:
                    if location.id not in newLocations and location.id not in accessible and location.logic(LogicVariables):
                        location_obj = LocationList[location.id]
                        # If this location is a bonus barrel, must make sure its logic is met as well
                        if (
                            (location.bonusBarrel is MinigameType.BonusBarrel and settings.bonus_barrels != "skip")
                            or (location.bonusBarrel is MinigameType.HelmBarrel and settings.helm_barrels != "skip")
                        ) and (not MinigameRequirements[BarrelMetaData[location.id].minigame].logic(LogicVariables)):
                            continue
                        # If this location has a blueprint, then make sure this is the correct kong
                        elif (location_obj.item is not None and ItemList[LocationList[location.id].item].type == Types.Blueprint) and (
                            not LogicVariables.BlueprintAccess(ItemList[LocationList[location.id].item])
                        ):
                            continue
                        # If this location is a Kasplat but doesn't have a blueprint, still make sure this is the correct kong to be accessible at all
                        elif (location_obj.type == Types.Blueprint) and (not LogicVariables.IsKong(location_obj.kong) and not settings.free_trade_items):
                            continue
                        # Every shop has a price
                        elif (location_obj.type == Types.Shop and location_obj.item is not None and location_obj.item != Items.NoItem) and (
                            searchType != SearchMode.GetReachableWithControlledPurchases or location.id in purchaseList
                        ):
                            # In search mode GetReachableWithControlledPurchases, only allowed to purchase at locations from what is passed in as "purchaseList"
                            LogicVariables.PurchaseShopItem(location.id)
                        elif location.id == Locations.NintendoCoin:
                            LogicVariables.Coins[Kongs.donkey] -= 2  # Subtract 2 coins for arcade lever
                        newLocations.add(location.id)
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
                            addedRegions.add(destination)
                            newRegion = Logic.Regions[destination]
                            newRegion.id = destination
                            regionPool.add(newRegion)
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
                        addedRegions.add(destination)
                        newRegion = Logic.Regions[destination]
                        newRegion.id = destination
                        regionPool.add(newRegion)

    if searchType in (SearchMode.GetReachable, SearchMode.GetReachableWithControlledPurchases):
        return accessible
    elif searchType == SearchMode.CheckBeatable or searchType == SearchMode.CheckSpecificItemReachable:
        # If the search has completed and the target item has not been found, then we failed to find it
        # settings.debug_accessible = accessible
        return False
    elif searchType == SearchMode.GeneratePlaythrough:
        return playthroughLocations
    elif searchType == SearchMode.CheckAllReachable:
        # settings.debug_accessible = accessible
        # settings.debug_accessible_2 = []
        # if len(accessible) > 300:
        #     settings.debug_accessible_2 = accessible[300:]
        # settings.debug_accessible_not = [location for location in LocationList if location not in accessible]
        # settings.debug_accessible_not_2 = []
        # if len(settings.debug_accessible_not) > 300:
        #     settings.debug_accessible_not_2 = settings.debug_accessible_not[300:]
        # settings.debug_enormous_pain_1 = [LocationList[location] for location in settings.debug_accessible]
        # settings.debug_enormous_pain_2 = [LocationList[location] for location in settings.debug_accessible_2]
        # settings.debug_enormous_pain_3 = [LocationList[location] for location in settings.debug_accessible_not]
        # settings.debug_enormous_pain_4 = [LocationList[location] for location in settings.debug_accessible_not_2]
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
    while 1:
        Reset()
        reachable = GetAccessibleLocations(settings, [], SearchMode.GetReachableWithControlledPurchases, locationsToPurchase)
        # Subtract the price of the chosen location from maxCoinsNeeded
        itemsToPurchase = [LocationList[x].item for x in locationsToPurchase]
        coinsSpent = GetMaxCoinsSpent(settings, locationsToPurchase)
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
        # If we found the Banana Hoard, world is valid!
        if LogicVariables.bananaHoard:
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
    for i in range(len(PlaythroughLocations) - 1, -1, -1):
        # We can immediately ignore spheres past the first sphere that is beaten
        if i > 0 and PlaythroughLocations[i - 1].seedBeaten:
            PlaythroughLocations.remove(PlaythroughLocations[i])
            continue
        sphere = PlaythroughLocations[i]
        # We want to track specific GBs in each sphere of the spoiler log up to and including the sphere where the last B. Locker becomes openable
        if i > 0 and PlaythroughLocations[i - 1].availableGBs > mostExpensiveBLocker:
            sphere.locations = [locationId for locationId in sphere.locations if LocationList[locationId].item != Items.GoldenBanana]
        for locationId in sphere.locations.copy():
            location = LocationList[locationId]
            # All GBs that make it here are logically required
            if location.item == Items.GoldenBanana:
                continue
            # Items that are part of the win condition are always part of the Playthrough but are never part of it otherwise
            if location.item == Items.BananaFairy:
                if settings.win_condition != "all_fairies":
                    sphere.locations.remove(locationId)
                continue
            if location.item == Items.BananaMedal:
                if settings.win_condition != "all_medals":
                    sphere.locations.remove(locationId)
                continue
            if location.item is not None and ItemList[location.item].type == Types.Blueprint:
                if settings.win_condition != "all_blueprints":
                    sphere.locations.remove(locationId)
                continue
            # Copy out item from location
            item = location.item
            location.item = None
            # Check if the game is still beatable
            Reset()
            if GetAccessibleLocations(settings, [], SearchMode.CheckBeatable):
                # If the game is still beatable this is an unnecessary location, so remove it.
                sphere.locations.remove(locationId)
                # We delay the item to ensure future locations which may rely on this one
                # do not give a false positive for beatability.
                location.SetDelayedItem(item)
                locationsToAddBack.append(locationId)
            else:
                # Else it is essential, don't remove it from the playthrough and add the item back.
                location.PlaceItem(item)

    # Check if there are any empty spheres, if so remove them
    for i in range(len(PlaythroughLocations) - 1, -1, -1):
        sphere = PlaythroughLocations[i]
        if len(sphere.locations) == 0:
            PlaythroughLocations.remove(sphere)

    # Re-place those items which were delayed earlier.
    for locationId in locationsToAddBack:
        LocationList[locationId].PlaceDelayedItem()


def PareWoth(spoiler, PlaythroughLocations):
    """Pare playthrough to locations which are Way of the Hoard (hard required by logic)."""
    # The functionality is similar to ParePlaythrough, but we want to see if individual locations are
    # hard required, so items are added back after checking regardless of the outcome.
    WothLocations = []
    for sphere in PlaythroughLocations:
        # Don't want constant locations in woth and we can filter out some types of items as not being essential to the woth
        for loc in [
            loc
            for loc in sphere.locations
            if not LocationList[loc].constant and ItemList[LocationList[loc].item].type not in (Types.Banana, Types.BlueprintBanana, Types.Crown, Types.Medal, Types.Blueprint)
        ]:
            WothLocations.append(loc)
    WothLocations.append(Locations.BananaHoard)  # The Banana Hoard is the endpoint of the Way of the Hoard
    # Check every item location to see if removing it by itself makes the game unbeatable
    for i in range(len(WothLocations) - 1, -1, -1):
        locationId = WothLocations[i]
        location = LocationList[locationId]
        item = location.item
        location.item = None
        # Check if game is still beatable
        Reset()
        if GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
            # If game is still beatable, this location is not hard required
            WothLocations.remove(locationId)
        # Either way, add location back
        location.PlaceItem(item)
    # Only need to build paths for item rando
    if spoiler.settings.shuffle_items:
        CalculateWothPaths(spoiler, WothLocations)
        CalculateFoolish(spoiler, WothLocations)
    return WothLocations


def CalculateWothPaths(spoiler, WothLocations):
    """Calculate the Paths (dependencies) for each Way of the Hoard item."""
    # Helps get more accurate paths by removing important obstacles to level entry
    # Removes the following:
    # - The need for vines to progress in Aztec
    # - The need for swim to get into level 4
    # - The need for keys to open lobbies (this is done with open_lobbies)
    LogicVariables.pathMode = True
    old_open_lobbies_temp = spoiler.settings.open_lobbies
    spoiler.settings.open_lobbies = True
    falseWothLocations = []
    # Prep the dictionary that will contain the path for the key item
    for locationId in WothLocations:
        spoiler.woth_paths[locationId] = [locationId]  # The endpoint is on its own path
    for locationId in WothLocations:
        # Remove the item from the location
        location = LocationList[locationId]
        item_id = location.item
        location.item = None
        # We also need to assume Kongs in order to get a "pure" path instead of Kong paths being a subset of most later paths.
        # Anything locked behind a a Kong will then require everything that Kong requires.
        # This sort of defeats the purpose of paths, as it would put everything in a Kong's path into the path of many, many items.
        assumedItems = ItemPool.Kongs(spoiler.settings)
        # Find all accessible locations without this item placed
        Reset()
        # At this point we know there is no breaking purchase order
        # Therefore moves required to get coins for shop purchases are not dependencies
        # So give the logic infinite coins so it can purchase anything it needs
        LogicVariables.GainInfiniteCoins()
        # Also assume max GBs so no B. Lockers can get in your way, leading to items that are only needed for GBs to be on paths
        LogicVariables.GoldenBananas = 201
        accessible = GetAccessibleLocations(spoiler.settings, assumedItems, SearchMode.GetReachable)
        isOnAnotherPath = False
        # Then check every other WotH location for accessibility
        for other_location in WothLocations:
            # If it is no longer accessible, then this location is on the path of that other location
            if other_location not in accessible:
                spoiler.woth_paths[other_location].append(locationId)
                isOnAnotherPath = True
        # Put the item back for future calculations
        location.PlaceItem(item_id)
        # If this item doesn't show up on any other paths, it's not actually WotH
        # This is rare, but could happen if the item at the location is needed for coins or B. Lockers - it's usually required, but not helpful to hint at all
        if item_id not in assumedItems and item_id != Items.BananaHoard and not isOnAnotherPath:
            falseWothLocations.append(locationId)
    # After everything is calculated, get rid of paths for false WotH locations
    for locationId in falseWothLocations:
        WothLocations.remove(locationId)
        del spoiler.woth_paths[locationId]
    LogicVariables.pathMode = False  # Don't carry this pathMode flag beyond this method ever
    spoiler.settings.open_lobbies = old_open_lobbies_temp  # Undo the open lobbies setting change too


def CalculateFoolish(spoiler, WothLocations):
    """Calculate the items and regions that are foolish (blocking no major items)."""
    wothItems = [LocationList[loc].item for loc in WothLocations]
    # First we need to determine what Major Items are foolish
    foolishItems = []
    # Determine which of our major items we need to check
    majorItems = ItemPool.AllKongMoves()
    if spoiler.settings.training_barrels != "normal":
        # I don't trust oranges quite yet - you can put an item in Diddy's upper cabin and it might think oranges is foolish still
        majorItems.extend([Items.Vines, Items.Swim, Items.Barrels])
    if spoiler.settings.shockwave_status == "shuffled":
        majorItems.append(Items.CameraAndShockwave)
    if spoiler.settings.shockwave_status == "shuffled_decoupled":
        majorItems.append(Items.Camera)
        majorItems.append(Items.Shockwave)
    for item in majorItems:
        # If this item is in the WotH, it can't possibly be foolish so we can skip it
        if item in wothItems:
            continue
        # Check the item to see if it locks *any* progression (even non-critical)
        Reset()
        LogicVariables.BanItem(item)  # Ban this item from being picked up
        GetAccessibleLocations(spoiler.settings, [], SearchMode.GetReachable)  # Check what's reachable
        if LogicVariables.HasAllItems():  # If you still have all the items, this one blocks no progression and is foolish
            foolishItems.append(item)
    spoiler.foolish_moves = foolishItems

    # Use the settings to determine non-progression Major Items
    majorItems = [item for item in majorItems if item not in foolishItems]
    majorItems.extend(ItemPool.Keys())
    majorItems.extend(ItemPool.Kongs(spoiler.settings))
    majorItems.append(Items.Oranges)  # Again, not comfortable foolishing oranges yet
    if Types.Coin in spoiler.settings.shuffled_location_types and spoiler.settings.coin_door_open in ["need_both", "need_rw"]:
        majorItems.append(Items.RarewareCoin)
    if Types.Coin in spoiler.settings.shuffled_location_types and spoiler.settings.coin_door_open in ["need_both", "need_nin"]:
        majorItems.append(Items.NintendoCoin)
    if Types.Blueprint in spoiler.settings.shuffled_location_types and spoiler.settings.win_condition == "all_blueprints":
        majorItems.extend(ItemPool.Blueprints(spoiler.settings))
    if Types.Medal in spoiler.settings.shuffled_location_types and spoiler.settings.win_condition == "all_medals":
        majorItems.append(Items.BananaMedal)
    if Types.Crown in spoiler.settings.shuffled_location_types and not spoiler.settings.crown_door_open:
        majorItems.append(Items.BattleCrown)
    # ***if fairy locations are shuffled*** and there's a major item on Rareware GB or fairies are the win con
    # then we'd majorItems.append(Items.BananaFairy)

    nonHintableNames = {"K. Rool Arena", "Snide", "Candy Generic", "Funky Generic", "Credits"}  # These regions never have anything useful so shouldn't be hinted
    if Types.Coin not in spoiler.settings.shuffled_location_types:
        nonHintableNames.add("Jetpac Game")  # If this is vanilla, it's never useful to hint
    # In order for a region to be foolish, it can contain none of these Major Items
    for id, region in RegionList.items():
        locations = [loc for loc in region.locations if loc.id in LocationList.keys()]
        # If this region DOES contain a major item, add it the name to the set of non-hintable hint regions
        if any([loc for loc in locations if LocationList[loc.id].item in majorItems]):
            nonHintableNames.add(region.hint_name)
    # The regions that are foolish are all regions not in this list (that have locations in them!)
    spoiler.foolish_region_names = list(set([region.hint_name for id, region in RegionList.items() if any(region.locations) and region.hint_name not in nonHintableNames]))


def RandomFill(settings, itemsToPlace, inOrder=False):
    """Randomly place given items in any location disregarding logic."""
    if not inOrder:
        shuffle(itemsToPlace)
    # Get all remaining empty locations
    empty = []
    for (id, location) in LocationList.items():
        if location.item is None:
            empty.append(id)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        item = itemsToPlace.pop()
        validLocations = settings.GetValidLocationsForItem(item)
        itemEmpty = [x for x in empty if x in validLocations]
        if len(itemEmpty) == 0:
            return len(itemsToPlace)
        shuffle(itemEmpty)
        locationId = itemEmpty.pop()
        LocationList[locationId].PlaceItem(item)
        empty.remove(locationId)
    return 0


def ForwardFill(settings, itemsToPlace, ownedItems=None, inOrder=False):
    """Forward fill algorithm for item placement."""
    if ownedItems is None:
        ownedItems = []
    if not inOrder:
        shuffle(itemsToPlace)
    ownedItems = ownedItems.copy()
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Get a random item
        item = itemsToPlace.pop(0)
        # Find a random empty location which is reachable with current items
        Reset()
        reachable = GetAccessibleLocations(settings, ownedItems.copy())
        validLocations = settings.GetValidLocationsForItem(item)
        reachable = [x for x in reachable if LocationList[x].item is None and x in validLocations]
        if len(reachable) == 0:  # If there are no empty reachable locations, reached a dead end
            return len(itemsToPlace)
        shuffle(reachable)
        locationId = reachable.pop()
        # Place the item
        ownedItems.append(item)
        LocationList[locationId].PlaceItem(item)
        # Debug code utility for very important items
        if item in ItemPool.HighPriorityItems(settings):
            settings.debug_fill[locationId] = item
        if item in ItemPool.Keys():
            settings.debug_fill[locationId] = item
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


def AssumedFill(settings, itemsToPlace, ownedItems=None, inOrder=False):
    """Assumed fill algorithm for item placement."""
    if ownedItems is None:
        ownedItems = []
    # While there are items to place
    if not inOrder:
        shuffle(itemsToPlace)
    while len(itemsToPlace) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemsToPlace.pop(0)
        itemShuffled = False
        owned = itemsToPlace.copy()
        owned.extend(ownedItems)

        itemValidLocations = settings.GetValidLocationsForItem(item)
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
        shuffle(validReachable)
        if ItemList[item].type == Types.Kong:
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
                    settings.diddy_freeing_kong = choice(ownedKongs)
                elif locationId == Locations.LankyKong:
                    settings.lanky_freeing_kong = choice(ownedKongs)
                elif locationId == Locations.TinyKong:
                    eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
                    if len(eligibleFreers) == 0:
                        js.postMessage("Failed placing item " + ItemList[item].name + " in location " + LocationList[locationId].name + ", due to no kongs being able to free them")
                        valid = False
                        break
                    settings.tiny_freeing_kong = choice(eligibleFreers)
                elif locationId == Locations.ChunkyKong:
                    settings.chunky_freeing_kong = choice(ownedKongs)
            # Check valid reachable after placing to see if it is broken
            # Need to re-assign owned items since the search adds a bunch of extras
            owned = itemsToPlace.copy()
            owned.extend(ownedItems)
            Reset()
            reachable = GetAccessibleLocations(settings, owned)
            valid = True
            # For each remaining item, ensure that it has a valid location reachable after placing this item
            for checkItem in itemsToPlace:
                itemValid = settings.GetValidLocationsForItem(checkItem)
                validReachable = [x for x in reachable if x in itemValid and x != locationId]
                if len(validReachable) == 0:
                    js.postMessage("Failed placing item " + ItemList[item].name + " in location " + LocationList[locationId].name + ", due to too few remaining locations in play")
                    valid = False
                    break
                reachable.remove(validReachable[0])  # Remove one so same location can't be "used" twice
            # If world is not valid, undo item placement and try next location
            if not valid:
                LocationList[locationId].item = None
                itemShuffled = False
                continue
            # Debug code utility for very important items
            if item in ItemPool.HighPriorityItems(settings):
                settings.debug_fill[locationId] = item
            if item in ItemPool.Keys():
                settings.debug_fill[locationId] = item
            itemShuffled = True
            break
        if not itemShuffled:
            js.postMessage("Failed placing item " + ItemList[item].name + " in any of remaining " + str(ItemList[item].type) + " type possible locations")
            return len(itemsToPlace) + 1
    return 0


def GetMaxCoinsSpent(settings, purchasedShops):
    """Calculate the max number of coins each kong could have spent given the ownedItems and the price settings."""
    MaxCoinsSpent = [0, 0, 0, 0, 0, 0]
    slamLevel = 0
    ammoBelts = 0
    instUpgrades = 0
    for location_id in purchasedShops:
        location = LocationList[location_id]
        if location.item == Items.ProgressiveSlam:
            movePrice = settings.prices[location.item][slamLevel]
            slamLevel += 1
        elif location.item == Items.ProgressiveAmmoBelt:
            movePrice = settings.prices[location.item][ammoBelts]
            ammoBelts += 1
        elif location.item == Items.ProgressiveInstrumentUpgrade:
            movePrice = settings.prices[location.item][instUpgrades]
            instUpgrades += 1
        elif settings.random_prices == "vanilla":
            movePrice = settings.prices[location.item]
        else:
            movePrice = settings.prices[location_id]
        if movePrice is not None:
            MaxCoinsSpent[location.kong] += movePrice
    # All shared moves add to the cost of each Kong
    for kong_index in range(5):
        MaxCoinsSpent[kong_index] += MaxCoinsSpent[int(Kongs.any)]
    MaxCoinsSpent.pop()  # Remove the shared total, as it was just for numbers keeping
    return MaxCoinsSpent


# @pp.profile_by_line()
def GetUnplacedItemPrerequisites(spoiler, targetItemId, placedMoves, ownedKongs=[]):
    """Given the target item and the current world state, find a valid, minimal, unplaced set of items required to reach the location it is in."""
    # Settings-required moves are always owned in order to complete this method based on the settings
    settingsRequiredMoves = []
    if Types.Key in spoiler.settings.shuffled_location_types:  # If keys are to be shuffled, they won't be shuffled yet
        settingsRequiredMoves = ItemPool.BlueprintAssumedItems().copy()  # We want Keys/Company Coins/Crowns here and this is a convenient collection
    # The most likely case - if no moves are needed, get out of here quickly
    Reset()
    if GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
        return []
    requiredMoves = []
    if ownedKongs == []:
        ownedKongs = GetKongs()
    # Some locations can be accessed by multiple items, so we'll shuffle the order we check the items to randomly pick one of them first
    # We should have just placed this item, so it should be available with the provided list of owned kongs
    # We don't want to find requirements for Kongs we don't own, as we shouldn't need them
    #   e.g. You own DK, Diddy, and Tiny but want to find the prerequisites for an item found in the Llama temple
    #     You intentionally only look at DK/Diddy/Tiny moves so you don't find Grape as a prerequisite because you don't have Lanky
    #     In this example (with no other shuffles), there are two possible return values depending on the shuffle order.
    #     Either [Items.Guitar, Items.Coconut] OR [Items.Guitar, Items.Feather]
    moveList = [move for move in ItemPool.AllMovesForOwnedKongs(ownedKongs)]
    # Sometimes a move requires shockwave as a prerequisite
    if spoiler.settings.shockwave_status != "vanilla":
        moveList.append(Items.Shockwave)
    # Often moves require training barrels as prerequisites
    if spoiler.settings.training_barrels != "normal":
        moveList.extend(ItemPool.TrainingBarrelAbilities())
    moveList = [move for move in moveList if move not in placedMoves]
    if targetItemId in moveList:
        moveList.remove(targetItemId)
    # You can get dangerously circular logic when one slam is placed here. Assume no slams when searching for accessibility and then add one later
    if Items.ProgressiveSlam in placedMoves:
        while Items.ProgressiveSlam in moveList:
            moveList.remove(Items.ProgressiveSlam)
    shuffle(moveList)
    lastRequiredMove = None
    for move in moveList:
        # For each move, see if adding it to the list of required moves gives us access to the location
        requiredMoves.append(move)
        Reset()
        if GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy() + requiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
            # If it does give us access, then we don't need any more moves
            # Note the last required move for later
            lastRequiredMove = move
            break
    # If we haven't found it yet but have a slam placed, it might be super duper locked so let's try that
    if lastRequiredMove is None and placedMoves.count(Items.ProgressiveSlam) == 1:
        requiredMoves.append(Items.ProgressiveSlam)
        Reset()
        if GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy() + requiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
            lastRequiredMove = move
    # If we didn't find a required move, the item was placed improperly somehow (this shouldn't happen)
    if lastRequiredMove is None:
        # DEBUG CODE - This helps find where items are being placed
        mysteryLocation = None
        itemobj = ItemList[targetItemId]
        if type(spoiler.settings.valid_locations[itemobj.type]) is dict:
            for possibleLocationThisItemGotPlaced in spoiler.settings.valid_locations[itemobj.type][itemobj.kong]:
                if LocationList[possibleLocationThisItemGotPlaced].item == targetItemId:
                    mysteryLocation = LocationList[possibleLocationThisItemGotPlaced]
                    break
        else:
            for possibleLocationThisItemGotPlaced in spoiler.settings.valid_locations[itemobj.type]:
                if LocationList[possibleLocationThisItemGotPlaced].item == targetItemId:
                    mysteryLocation = LocationList[possibleLocationThisItemGotPlaced]
                    break
        if mysteryLocation is None:
            raise Ex.ItemPlacementException("Target item not placed??")
        print("Item placed in an inaccessible location: " + str(mysteryLocation.name))
        raise Ex.ItemPlacementException("Item placed in an inaccessible location: " + str(mysteryLocation.name))
    # requiredMoves now contains all items that are required, but probably a bunch of useless stuff too
    # Time to cull moves until we get to only exactly what we need
    while requiredMoves != [] and requiredMoves[0] != lastRequiredMove:
        # Remove the first item and see if we can still access the target
        possiblyUnnecessaryItem = requiredMoves.pop(0)
        Reset()
        if not GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy() + requiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
            # If it's no longer accessible, then re-add it to the end of the list
            requiredMoves.append(possiblyUnnecessaryItem)
        # Repeat until we find the last required move
    spoiler.settings.debug_prerequisites[targetItemId] = requiredMoves
    return requiredMoves


def PlaceItems(settings, algorithm, itemsToPlace, ownedItems=None, inOrder=False):
    """Places items using given algorithm."""
    if ownedItems is None:
        ownedItems = []
    # Always use random fill with no logic
    if settings.no_logic:
        algorithm = "random"
    if algorithm == "assumed":
        return AssumedFill(settings, itemsToPlace, ownedItems, inOrder)
    elif algorithm == "forward":
        return ForwardFill(settings, itemsToPlace, ownedItems, inOrder)
    elif algorithm == "random":
        return RandomFill(settings, itemsToPlace, inOrder)


def FillShuffledKeys(spoiler):
    """Fill Keys in shuffled locations based on the settings."""
    keysToPlace = ItemPool.Keys().copy()
    if spoiler.settings.key_8_helm:
        keysToPlace.remove(Items.HideoutHelmKey)
    # Level-agnostic key placement settings include...
    # - No logic (totally random)
    # - Loading Zone randomizer (key unlocks are typically of lesser importance)
    # - Complex level progression (key order is non-linear)
    if spoiler.settings.no_logic or spoiler.settings.shuffle_loading_zones == "all" or spoiler.settings.hard_level_progression:
        # Place keys in a random order except...
        shuffle(keysToPlace)
        # Keys 3 and 8 should be placed last to give them higher location potential
        if Items.FranticFactoryKey in keysToPlace:
            keysToPlace.remove(Items.FranticFactoryKey)
            keysToPlace.append(Items.FranticFactoryKey)
        if Items.HideoutHelmKey in keysToPlace:
            keysToPlace.remove(Items.HideoutHelmKey)
            keysToPlace.append(Items.HideoutHelmKey)
        keysUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, keysToPlace, ItemPool.KeyAssumedItems(), inOrder=True)
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")
    # Simple linear level order progression leads to straightforward key placement
    elif spoiler.settings.kongs_for_progression:  # This check is so we don't accidentally wipe progression on settings we don't want to
        assumedItems = ItemPool.KeyAssumedItems()
        # Key 1 must be before level 2
        BlockAccessToLevel(spoiler.settings, 2)
        keysUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.JungleJapesKey], assumedItems)
        # Key 2 must be before level 3
        BlockAccessToLevel(spoiler.settings, 3)
        keysUnplaced += PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.AngryAztecKey], assumedItems)
        # Keys 3 and 4 must be before level 5
        BlockAccessToLevel(spoiler.settings, 5)
        keysUnplaced += PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.FranticFactoryKey, Items.GloomyGalleonKey], assumedItems)
        # Key 5 must be before level 6
        BlockAccessToLevel(spoiler.settings, 6)
        keysUnplaced += PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.FungiForestKey], assumedItems)
        # Keys 6 and 7 must be before level 8
        BlockAccessToLevel(spoiler.settings, 8)
        keysUnplaced += PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.CrystalCavesKey, Items.CreepyCastleKey], assumedItems)
        # Key 8 can be anywhere
        BlockAccessToLevel(spoiler.settings, 100)
        if Items.HideoutHelmKey in keysToPlace:
            keysUnplaced += PlaceItems(spoiler.settings, spoiler.settings.algorithm, [Items.HideoutHelmKey], assumedItems)
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")
    # Not entirely sure what settings these are but being careful doesn't hurt
    else:
        # Place the keys in order
        keysUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, keysToPlace, ItemPool.KeyAssumedItems(), inOrder=True)
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")


def Fill(spoiler):
    """Fully randomizes and places all items."""
    spoiler.settings.debug_fill = {}
    spoiler.settings.debug_prerequisites = {}
    spoiler.settings.debug_fill_blueprints = {}
    # First place constant items
    ItemPool.PlaceConstants(spoiler.settings)
    # Then fill Kongs and Moves
    FillKongsAndMoves(spoiler)
    # Then place Blueprints
    if Types.Blueprint in spoiler.settings.shuffled_location_types:
        Reset()
        # Blueprints can be placed randomly - there's no location that can cause blueprints to lock themselves
        blueprintsUnplaced = PlaceItems(spoiler.settings, "random", ItemPool.Blueprints(spoiler.settings).copy(), ItemPool.BlueprintAssumedItems())
        if blueprintsUnplaced > 0:
            raise Ex.ItemPlacementException(str(blueprintsUnplaced) + " unplaced blueprints.")
    # Then place keys
    if Types.Key in spoiler.settings.shuffled_location_types:
        FillShuffledKeys(spoiler)
    # Then place Nintendo & Rareware Coins
    if Types.Coin in spoiler.settings.shuffled_location_types:
        Reset()
        coinsUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.CompanyCoinItems(), ItemPool.CoinAssumedItems())
        if coinsUnplaced > 0:
            raise Ex.ItemPlacementException(str(coinsUnplaced) + " unplaced company coins.")
    # Then place Battle Crowns
    if Types.Crown in spoiler.settings.shuffled_location_types:
        Reset()
        # Crowns can be placed randomly if the crown door is open
        algo = "random"
        if not spoiler.settings.crown_door_open:
            algo = spoiler.settings.algorithm
        crownsUnplaced = PlaceItems(spoiler.settings, algo, ItemPool.BattleCrownItems(), ItemPool.CrownAssumedItems())
        if crownsUnplaced > 0:
            raise Ex.ItemPlacementException(str(crownsUnplaced) + " unplaced crowns.")
    # Then place Banana Medals
    if Types.Medal in spoiler.settings.shuffled_location_types:
        Reset()
        # Medals can also be placed randomly
        algo = "random"
        # Unless it could have put something important on the Rareware Coin
        # If it did, placing them randomly could fail to fill (it's likely to fail to fill anyway)
        if Types.Coin in spoiler.settings.shuffled_location_types or spoiler.settings.medal_requirement > 39:
            algo = spoiler.settings.algorithm
        medalsUnplaced = PlaceItems(spoiler.settings, algo, ItemPool.BananaMedalItems(), ItemPool.MedalAssumedItems())
        if medalsUnplaced > 0:
            raise Ex.ItemPlacementException(str(medalsUnplaced) + " unplaced medals.")
    # Then fill remaining locations with GBs
    if Types.Banana in spoiler.settings.shuffled_location_types:
        Reset()
        gbsUnplaced = PlaceItems(spoiler.settings, "random", ItemPool.GoldenBananaItems(), [])
        if gbsUnplaced > 0:
            raise Ex.ItemPlacementException(str(gbsUnplaced) + " unplaced GBs.")
    # Some locations require special care to make logic work correctly
    # This is the only location that cares about None vs NoItem - it needs to be None so it fills correctly but NoItem for logic to generate progression correctly
    if LocationList[Locations.JapesDonkeyFreeDiddy].item is None:
        LocationList[Locations.JapesDonkeyFreeDiddy].PlaceItem(Items.NoItem)
    # Finally, check if game is beatable
    Reset()
    if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckAllReachable):
        raise Ex.GameNotBeatableException("Game not able to complete 101% after placing all items.")
    return


def ShuffleSharedMoves(spoiler, placedMoves):
    """Shuffles shared kong moves into shops and then returns the remaining ones and their valid locations."""
    # First place constant items
    ItemPool.PlaceConstants(spoiler.settings)

    # Confirm there are enough locations available for each remaining shared move
    availableSharedShops = [location for location in SharedMoveLocations if LocationList[location].item is None]
    placedSharedMoves = [move for move in placedMoves if move in ItemPool.ImportantSharedMoves or move in ItemPool.JunkSharedMoves]
    if len(availableSharedShops) < len(ItemPool.ImportantSharedMoves) + len(ItemPool.JunkSharedMoves) - len(placedSharedMoves):
        raise Ex.ItemPlacementException(
            "Too many kong moves placed before shared moves. Only "
            + str(len(availableSharedShops))
            + " available for "
            + str(len(ItemPool.ImportantSharedMoves))
            + str(len(ItemPool.JunkSharedMoves))
            + str(len(placedSharedMoves))
            + " remaining shared moves."
        )

    # When a shared move is assigned to a shop in any particular level, that shop cannot also hold any kong-specific moves.
    # To avoid conflicts, first determine which level shops will have shared moves then remove these shops from each kong's valid locations list
    if spoiler.settings.training_barrels != "normal" and Items.Oranges not in placedMoves:
        # First place training moves that are not placed. By this point, only Oranges need to be placed here as the others are important to place even earlier than this
        trainingMovesUnplaced = PlaceItems(spoiler.settings, "assumed", [Items.Oranges], [x for x in ItemPool.AllItems(spoiler.settings) if x != Items.Oranges and x not in placedMoves])
        if trainingMovesUnplaced > 0:
            raise Ex.ItemPlacementException("Failed to place Orange training barrel move.")
        placedMoves.append(Items.Oranges)
    importantSharedToPlace = ItemPool.ImportantSharedMoves.copy()
    # Next place any fairy moves that need placing, settings dependent
    if spoiler.settings.shockwave_status == "shuffled" and Items.CameraAndShockwave not in placedMoves:
        importantSharedToPlace.append(Items.CameraAndShockwave)
    elif spoiler.settings.shockwave_status == "shuffled_decoupled" and (Items.Camera not in placedMoves or Items.Shockwave not in placedMoves):
        importantSharedToPlace.append(Items.Camera)
        importantSharedToPlace.append(Items.Shockwave)
    for item in placedMoves:
        if item in importantSharedToPlace:
            importantSharedToPlace.remove(item)
    importantSharedUnplaced = PlaceItems(
        spoiler.settings, "assumed", importantSharedToPlace, [x for x in ItemPool.AllItems(spoiler.settings) if x not in importantSharedToPlace and x not in placedMoves]
    )
    if importantSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(importantSharedUnplaced) + " unplaced shared important items.")
    junkSharedToPlace = ItemPool.JunkSharedMoves.copy()
    for item in placedMoves:
        if item in junkSharedToPlace:
            junkSharedToPlace.remove(item)
    junkSharedUnplaced = PlaceItems(spoiler.settings, "random", junkSharedToPlace, [x for x in ItemPool.AllItems(spoiler.settings) if x not in junkSharedToPlace])
    if junkSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(junkSharedUnplaced) + " unplaced shared junk items.")


def FillKongsAndMovesGeneric(spoiler):
    """Facilitate shuffling individual pools of items in lieu of full item rando."""
    retries = 0
    while 1:
        try:
            Fill(spoiler)
            # Check if game is beatable
            Reset()
            if not VerifyWorldWithWorstCoinUsage(spoiler.settings):
                raise Ex.GameNotBeatableException("Game potentially unbeatable after placing all items.")
            return
        except Ex.FillException as ex:
            if retries == 20:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            retries += 1
            if retries % 5 == 0:
                js.postMessage("Retrying fill really hard. Tries: " + str(retries))
                # Handle Loading Zones - does not work right now but is something I want here eventually
                # if spoiler.settings.shuffle_loading_zones != "none":
                #     ShuffleExits.Reset()
                #     ShuffleExits.ExitShuffle(spoiler.settings)
                #     spoiler.UpdateExits()
                spoiler.settings.shuffle_prices()
            else:
                js.postMessage("Retrying fill. Tries: " + str(retries))
            Reset()
            Logic.ClearAllLocations()


def GeneratePlaythrough(spoiler):
    """Generate playthrough and way of the hoard and update spoiler."""
    js.postMessage("Seed generated! Finalizing spoiler...")
    # Generate and display the playthrough
    Reset()
    PlaythroughLocations = GetAccessibleLocations(spoiler.settings, [], SearchMode.GeneratePlaythrough)  # identify in the spheres where the win condition is met
    ParePlaythrough(spoiler.settings, PlaythroughLocations)
    # Generate and display woth
    WothLocations = PareWoth(spoiler, PlaythroughLocations)
    # Write data to spoiler and return
    spoiler.UpdateLocations(LocationList)
    if any(spoiler.settings.shuffled_location_types):
        ShuffleItems(spoiler)
    spoiler.UpdatePlaythrough(LocationList, PlaythroughLocations)
    spoiler.UpdateWoth(LocationList, WothLocations)


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
            # Must be able to bypass Guitar door - the active bananaports condition is in case your only Llama Temple access is through the quicksand cave
            and (Kongs.diddy in ownedKongs or spoiler.settings.open_levels or (Kongs.donkey in ownedKongs and spoiler.settings.activate_all_bananaports == "all"))
            and (Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs)
        ):  # Must be able to open Llama Temple
            logicallyAccessibleKongLocations.append(Locations.LankyKong)
    return logicallyAccessibleKongLocations


def PlacePriorityItems(spoiler, itemsToPlace, beforePlacedItems, levelBlock=None):
    """Place the given items with priority, also placing all dependencies depending on where they got placed. Returns a list of all items newly placed by this function."""
    if itemsToPlace == []:  # Base case of recursion - when priority items no longer have dependencies, they'll hit this method placing zero items
        return []
    # Prevent reference shenanigans because I'm too lazy to do it properly
    priorityItemsToPlace = itemsToPlace.copy()
    placedItems = beforePlacedItems.copy()
    # If we're blocking past a certain level, ban keys that would unlock anything beyond those levels
    bannedKeys = []
    if levelBlock is not None:
        bannedKeys = [key for key in ItemPool.Keys() if ItemList[key].index >= levelBlock]
    allOtherItems = ItemPool.AllKongMoves().copy()
    if Types.Key in spoiler.settings.shuffled_location_types:  # If keys are to be shuffled, they won't be shuffled yet
        allOtherItems.extend(ItemPool.BlueprintAssumedItems().copy())  # We want Keys/Company Coins/Crowns here and this is a convenient collection
        # However we don't want all keys - don't assume keys for or beyond the latest logically allowed level's key
        for key in bannedKeys:
            allOtherItems.remove(key)
    if spoiler.settings.training_barrels != "normal":
        allOtherItems.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.shockwave_status != "vanilla":
        allOtherItems.append(Items.Shockwave)  # Shockwave is rarely needed
    # Two exceptions: we don't assume we have the items to be placed, as then they could lock themselves
    for item in priorityItemsToPlace:
        allOtherItems.remove(item)
    # We also don't assume we have any placed items. If these unlock locations we should find them as we go.
    # This should prevent circular logic (e.g. the diddy-unlocking-gun being locked behind guitar which is already priority placed in Japes Cranky)
    for item in placedItems:
        allOtherItems.remove(item)
    # At last, place all the items
    failedToPlace = PlaceItems(spoiler.settings, "assumed", priorityItemsToPlace.copy(), ownedItems=allOtherItems)
    if failedToPlace > 0:
        item_names = ", ".join([ItemList[item].name for item in priorityItemsToPlace])
        raise Ex.ItemPlacementException(f"Failed to priority place {item_names}")
    # Note down the latest known list of owned kongs - I don't think this is necessary, but if it is less than 5 it is accurate and should speed up GetUnplacedItemPrerequisites
    ownedKongs = LogicVariables.GetKongs()
    # The items we just placed can now be treated as such
    placedItems.extend(priorityItemsToPlace)
    numberOfSlamsPlaced = placedItems.count(Items.ProgressiveSlam)
    unplacedDependencies = []
    for item in priorityItemsToPlace:
        # Find what items are needed to get this item
        unplacedItems = GetUnplacedItemPrerequisites(spoiler, item, placedItems, ownedKongs)
        slamsRequired = unplacedItems.count(Items.ProgressiveSlam)
        # Add each unplaced item to the list of items that now need to be placed, making sure not to add duplicates or third slams
        for item in unplacedItems:
            if item not in unplacedDependencies or (item == Items.ProgressiveSlam and slamsRequired > 1 and unplacedDependencies.count(Items.ProgressiveSlam) < 2):
                unplacedDependencies.append(item)
    # Recursively place priority items with the dependencies - anything this method places will also need to be returned by the outermost call
    priorityItemsToPlace.extend(PlacePriorityItems(spoiler, unplacedDependencies, placedItems, levelBlock))
    return priorityItemsToPlace


def PlaceKongsInKongLocations(spoiler, kongItems, kongLocations):
    """For these settings, Kongs to place, and locations to place them in, place the Kongs in such a way the generation will never error here."""
    ownedKongs = [kong for kong in spoiler.settings.starting_kong_list]
    # In entrance randomizer, it's too complicated to quickly determine kong accessibility.
    # Instead, we place Kongs in a specific order to guarantee we'll at least have an eligible freer.
    # To be at least somewhat nice to no logic users, we also use this section here so kongs don't lock each other.
    if spoiler.settings.shuffle_loading_zones == "all" or spoiler.settings.no_logic:
        shuffle(kongItems)
        if Locations.ChunkyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.ChunkyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.chunky_freeing_kong = choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        if Locations.DiddyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.DiddyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.diddy_freeing_kong = choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # The Lanky location can't be your first in cases where the Lanky freeing Kong can't get into the llama temple and you need a second Kong
        if Locations.LankyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.LankyKong].PlaceItem(kongItemToBeFreed)
            spoiler.settings.lanky_freeing_kong = choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # Placing the Tiny location last guarantees we have one of Diddy or Chunky
        if Locations.TinyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            LocationList[Locations.TinyKong].PlaceItem(kongItemToBeFreed)
            eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
            spoiler.settings.tiny_freeing_kong = choice(eligibleFreers)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
    # In level order shuffling, we need to be very particular about who we unlock and in what order so as to guarantee completion
    # Vanilla levels can be treated as if the level shuffler randomly placed all the levels in the same order
    elif spoiler.settings.shuffle_loading_zones in ("levels", "none"):
        latestLogicallyAllowedLevel = len(ownedKongs) + 1
        # Logically we can always enter any level on hard level progression
        if spoiler.settings.hard_level_progression:
            latestLogicallyAllowedLevel = 7
        logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
        while len(ownedKongs) != 5:
            # If there aren't any accessible Kong locations, then the level order shuffler has a bug (this shouldn't happen)
            if not any(logicallyAccessibleKongLocations):
                raise Ex.EntrancePlacementException(
                    "Levels shuffled in a way that makes Kong unlocks impossible. SEND THIS TO THE DEVS! " + dumps(spoiler.settings.__dict__) + " SEND THIS TO THE DEVS!"
                )
            # Begin by finding the currently accessible Kong locations
            # Randomly pick an accessible location
            progressionLocation = choice(logicallyAccessibleKongLocations)
            logicallyAccessibleKongLocations.remove(progressionLocation)
            # Pick a Kong to free this location from the Kongs we currently have
            if progressionLocation == Locations.DiddyKong:
                spoiler.settings.diddy_freeing_kong = choice(ownedKongs)
            elif progressionLocation == Locations.LankyKong:
                spoiler.settings.lanky_freeing_kong = choice(ownedKongs)
            elif progressionLocation == Locations.TinyKong:
                eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
                spoiler.settings.tiny_freeing_kong = choice(eligibleFreers)
            elif progressionLocation == Locations.ChunkyKong:
                spoiler.settings.chunky_freeing_kong = choice(ownedKongs)
            # Remove this location from any considerations
            kongLocations.remove(progressionLocation)
            # Pick a Kong to unlock from the locked Kongs
            kongToBeFreed = choice(kongItems)
            # With this kong, we can progress one level further (if we care about this logic)
            if not spoiler.settings.hard_level_progression:
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
                    if len(progressionKongItems) == 0:
                        raise Ex.FillException("Kongs placed in a way that is impossible to unlock everyone. SEND THIS TO THE DEVS! " + dumps(spoiler.settings.__dict__) + " SEND THIS TO THE DEVS!")
                    # Pick a random Kong from the Kongs that guarantee progression
                    kongToBeFreed = choice(progressionKongItems)
            # Now that we have a combination guaranteed to not break the seed or logic, lock it in
            LocationList[progressionLocation].PlaceItem(kongToBeFreed)
            kongItems.remove(kongToBeFreed)
            ownedKongs.append(ItemPool.GetKongForItem(kongToBeFreed))
            # Refresh the location list and repeat until all Kongs are free
            logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
    # Pick freeing kongs for any that are still "any" with no restrictions.
    if spoiler.settings.diddy_freeing_kong == Kongs.any:
        spoiler.settings.diddy_freeing_kong = choice(GetKongs())
    if spoiler.settings.lanky_freeing_kong == Kongs.any:
        spoiler.settings.lanky_freeing_kong = choice(GetKongs())
    if spoiler.settings.tiny_freeing_kong == Kongs.any:
        spoiler.settings.tiny_freeing_kong = choice([Kongs.diddy, Kongs.chunky])
    if spoiler.settings.chunky_freeing_kong == Kongs.any:
        spoiler.settings.chunky_freeing_kong = choice(GetKongs())
    # Update the locations' assigned kong with the set freeing kong list
    LocationList[Locations.JapesDonkeyFrontofCage].kong = spoiler.settings.diddy_freeing_kong
    LocationList[Locations.JapesDonkeyFreeDiddy].kong = spoiler.settings.diddy_freeing_kong
    LocationList[Locations.AztecDonkeyFreeLanky].kong = spoiler.settings.lanky_freeing_kong
    LocationList[Locations.AztecDiddyFreeTiny].kong = spoiler.settings.tiny_freeing_kong
    LocationList[Locations.FactoryLankyFreeChunky].kong = spoiler.settings.chunky_freeing_kong
    spoiler.settings.update_valid_locations()


def FillKongs(spoiler):
    """Place Kongs in valid locations."""
    # Determine what kong items need to be placed
    startingKongItems = [ItemPool.ItemFromKong(kong) for kong in spoiler.settings.starting_kong_list]
    kongItems = [item for item in ItemPool.Kongs(spoiler.settings) if item not in startingKongItems]
    # If Kongs can be placed anywhere, we don't need anything special
    if spoiler.settings.shuffle_items and Types.Kong in spoiler.settings.shuffled_location_types:
        assumedItems = ItemPool.AllKongMoves().copy()
        if spoiler.settings.training_barrels != "normal":
            assumedItems.extend(ItemPool.TrainingBarrelAbilities())
        if spoiler.settings.shockwave_status != "vanilla":
            assumedItems.append(Items.Shockwave)
        Reset()
        PlaceItems(spoiler.settings, spoiler.settings.algorithm, kongItems, assumedItems)
        # We don't care who gets the GBs for these locations anymore, just random it up
        spoiler.settings.diddy_freeing_kong = choice(GetKongs())
        spoiler.settings.lanky_freeing_kong = choice(GetKongs())
        spoiler.settings.tiny_freeing_kong = choice([Kongs.diddy, Kongs.chunky])
        spoiler.settings.chunky_freeing_kong = choice(GetKongs())
        # Update the locations' assigned kong with the set freeing kong list
        LocationList[Locations.JapesDonkeyFrontofCage].kong = spoiler.settings.diddy_freeing_kong
        LocationList[Locations.JapesDonkeyFreeDiddy].kong = spoiler.settings.diddy_freeing_kong
        LocationList[Locations.AztecDonkeyFreeLanky].kong = spoiler.settings.lanky_freeing_kong
        LocationList[Locations.AztecDiddyFreeTiny].kong = spoiler.settings.tiny_freeing_kong
        LocationList[Locations.FactoryLankyFreeChunky].kong = spoiler.settings.chunky_freeing_kong
        # If we didn't put an item in a kong location, then it gets a NoItem
        # This matters specifically so the logic around Diddy's cage behaves properly
        if LocationList[Locations.DiddyKong].item is None:
            LocationList[Locations.DiddyKong].PlaceItem(Items.NoItem)
        spoiler.settings.update_valid_locations()
    # If kongs must be in Kong cages, we need to be more careful
    else:
        # Determine what locations the kong items need to be placed in
        if any(spoiler.settings.kong_locations):
            emptyKongLocations = [location for location in [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong] if location not in spoiler.settings.kong_locations]
            for locationId in emptyKongLocations:
                LocationList[locationId].PlaceItem(Items.NoItem)
        Reset()
        # Specialized Kong placement function that will never fail to find a beatable combination of Kong unlocks for the vanilla locations
        PlaceKongsInKongLocations(spoiler, kongItems, spoiler.settings.kong_locations.copy())


def FillKongsAndMoves(spoiler):
    """Fill kongs, then progression moves, then shared moves, then rest of moves."""
    itemsToPlace = []
    preplacedPriorityMoves = []

    # Handle kong rando first so we know what moves are most important to place
    if spoiler.settings.kong_rando:
        FillKongs(spoiler)

    levelBlockInPlace = False
    # Once Kongs are placed, the top priority is placing training barrel moves first. These (mostly) need to be very early because they block access to whole levels.
    if not spoiler.settings.unlock_all_moves and spoiler.settings.move_rando != "off" and spoiler.settings.training_barrels == "shuffled":
        # First place barrels - needed for most bosses
        needBarrelsByThisLevel = None
        if not spoiler.settings.no_logic and spoiler.settings.shuffle_loading_zones != "all" and not spoiler.settings.hard_level_progression:
            # In standard level order, place barrels very early to prevent same-y boss orders
            needBarrelsByThisLevel = 2
            BlockAccessToLevel(spoiler.settings, needBarrelsByThisLevel)
            levelBlockInPlace = True
        itemsPlacedForBarrels = PlacePriorityItems(spoiler, [Items.Barrels], preplacedPriorityMoves, levelBlock=needBarrelsByThisLevel)
        preplacedPriorityMoves.extend(itemsPlacedForBarrels)
        # Next place vines - needed to beat Aztec and maybe get to upper DK Isle
        if Items.Vines not in preplacedPriorityMoves:
            needVinesByThisLevel = None
            if not spoiler.settings.no_logic and spoiler.settings.shuffle_loading_zones != "all" and not spoiler.settings.hard_level_progression:
                needVinesByThisLevel = 2
                # In a standard level order seed, we need to place vines before Aztec (or else it isn't beatable)
                for i in range(1, 8):
                    if spoiler.settings.level_order[i] == Levels.AngryAztec:
                        needVinesByThisLevel = i
                        break
                # If we don't have at least Isles warps on, we also need it to access level 2 (and 6)
                if spoiler.settings.activate_all_bananaports == "off":
                    # The vine level is whatever comes first: Aztec or level 2
                    needVinesByThisLevel = min(2, needVinesByThisLevel)
                BlockAccessToLevel(spoiler.settings, needVinesByThisLevel)
                levelBlockInPlace = True
            itemsPlacedForVines = PlacePriorityItems(spoiler, [Items.Vines], preplacedPriorityMoves, levelBlock=needVinesByThisLevel)
            preplacedPriorityMoves.extend(itemsPlacedForVines)
        # Next place swim - needed to get into level 4
        if Items.Swim not in preplacedPriorityMoves:
            needSwimByThisLevel = None
            if not spoiler.settings.no_logic and spoiler.settings.shuffle_loading_zones != "all" and not spoiler.settings.hard_level_progression:
                # In a standard level order seed, we need swim to access level 4 (whatever it is)
                needSwimByThisLevel = 4
                BlockAccessToLevel(spoiler.settings, needSwimByThisLevel)
                levelBlockInPlace = True
            itemsPlacedForSwim = PlacePriorityItems(spoiler, [Items.Swim], preplacedPriorityMoves, levelBlock=needSwimByThisLevel)
            preplacedPriorityMoves.extend(itemsPlacedForSwim)
    # If we had to put in a level block, undo it now - only settings that need progression fixed later will do this so this is fine
    if levelBlockInPlace:
        BlockAccessToLevel(spoiler.settings, 100)

    if spoiler.settings.kong_rando:
        # If kongs are our progression, then place moves that unlock those kongs before anything else
        # This logic only matters if the level order is critical to progression (i.e. not loading zone shuffled)
        if spoiler.settings.kongs_for_progression and spoiler.settings.shuffle_loading_zones != "all" and spoiler.settings.move_rando != "start_with":
            lockedKongs = [kong for kong in GetKongs() if kong not in spoiler.settings.starting_kong_list]
            for kong in lockedKongs:
                # We need the item representation of the kong
                kongItem = ItemPool.ItemFromKong(kong)
                # To save some cost on the coming method, we know none of the locked kong's moves can be prerequisites
                otherKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
                otherKongs.remove(kong)
                # Get the unplaced prerequisites to this Kong's location - this could indirectly include other Kongs' locations
                directPrerequisiteMoves = GetUnplacedItemPrerequisites(spoiler, kongItem, preplacedPriorityMoves, otherKongs)
                newlyPlacedItems = PlacePriorityItems(spoiler, directPrerequisiteMoves, preplacedPriorityMoves)
                preplacedPriorityMoves.extend(newlyPlacedItems)

    # Handle shared moves before other moves in move rando
    if not spoiler.settings.unlock_all_moves and spoiler.settings.move_rando != "off":
        # Shuffle the shared move locations since they must be done first
        ShuffleSharedMoves(spoiler, preplacedPriorityMoves.copy())
        # Set up remaining kong moves to be shuffled
        itemsToPlace.extend(ItemPool.DonkeyMoves)
        itemsToPlace.extend(ItemPool.DiddyMoves)
        itemsToPlace.extend(ItemPool.LankyMoves)
        itemsToPlace.extend(ItemPool.TinyMoves)
        itemsToPlace.extend(ItemPool.ChunkyMoves)

    # Handle remaining moves/items
    Reset()
    itemsToPlace = [item for item in itemsToPlace if item not in preplacedPriorityMoves]
    settingsRequiredMoves = []
    if Types.Key in spoiler.settings.shuffled_location_types:  # If keys are to be shuffled, they won't be shuffled yet
        settingsRequiredMoves = ItemPool.BlueprintAssumedItems().copy()  # We want Keys/Company Coins/Crowns here and this is a convenient collection
    unplaced = PlaceItems(spoiler.settings, "assumed", itemsToPlace, settingsRequiredMoves)
    if unplaced > 0:
        # debug code - outputs all preplaced and shared items in an attempt to find where things are going wrong
        locationsAndMoves = {}
        emptyShops = []
        emptySharedShops = []
        for locationId in LocationList:
            location = LocationList[locationId]
            if location.item is not None and location.item != Items.NoItem and location.item <= Items.CameraAndShockwave:
                locationsAndMoves[locationId] = location.item
            if location.type == Types.Shop and location.item is None:
                emptyShops.append(location)
                if locationId in SharedMoveLocations:
                    emptySharedShops.append(location)
        raise Ex.ItemPlacementException(str(unplaced) + " unplaced items.")

    # Final touches to item placement, some locations need special treatment
    if not spoiler.settings.unlock_all_moves and spoiler.settings.move_rando != "off":
        # If we're shuffling training moves, always put a move in each training barrel
        if spoiler.settings.training_barrels == "shuffled":
            emptyTrainingBarrels = [loc for loc in TrainingBarrelLocations if LocationList[loc].item is None]
            if len(emptyTrainingBarrels) > 0:
                # Find the list of shops that have a kong move in them
                kongMoveLocationsList = []
                for location in DonkeyMoveLocations:
                    item_at_location = LocationList[location].item
                    if item_at_location is not None and item_at_location != Items.NoItem:
                        kongMoveLocationsList.append(location)
                for location in DiddyMoveLocations:
                    item_at_location = LocationList[location].item
                    if item_at_location is not None and item_at_location != Items.NoItem:
                        kongMoveLocationsList.append(location)
                for location in LankyMoveLocations:
                    item_at_location = LocationList[location].item
                    if item_at_location is not None and item_at_location != Items.NoItem:
                        kongMoveLocationsList.append(location)
                for location in TinyMoveLocations:
                    item_at_location = LocationList[location].item
                    if item_at_location is not None and item_at_location != Items.NoItem:
                        kongMoveLocationsList.append(location)
                for location in ChunkyMoveLocations:
                    item_at_location = LocationList[location].item
                    if item_at_location is not None and item_at_location != Items.NoItem:
                        kongMoveLocationsList.append(location)
                # If no shops have a kong move (can happen in item rando), then we gotta dig deeper for moves - this can place some shared moves earlier but that's cool too
                if len(kongMoveLocationsList) == 0:
                    for location_id, location in LocationList.items():
                        if location.item in ItemPool.AllKongMoves():
                            kongMoveLocationsList.append(location_id)
                # Worth noting that moving a move to the training barrels will always make it more accessible, and thus doesn't need any additional logic
                for emptyBarrel in emptyTrainingBarrels:
                    # Pick a random Kong move to put in the training barrel. This should be both more interesting than a shared move and lead to fewer empty shops.
                    locationToVacate = choice(kongMoveLocationsList)
                    itemToBeMoved = LocationList[locationToVacate].item
                    LocationList[emptyBarrel].PlaceItem(itemToBeMoved)
                    LocationList[locationToVacate].PlaceItem(Items.NoItem)
                    kongMoveLocationsList.remove(locationToVacate)
                    if locationToVacate in spoiler.settings.debug_fill.keys():  # Should only fail in no logic
                        del spoiler.settings.debug_fill[locationToVacate]
                        spoiler.settings.debug_fill[emptyBarrel] = itemToBeMoved
    spoiler.settings.debug_preplaced_priority_moves = preplacedPriorityMoves
    if preplacedPriorityMoves.count(Items.ProgressiveSlam) > 2:
        raise Ex.FillException("Somehow managed to place 3 slams? This shouldn't happen.")


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
    retries = 0
    while 1:
        try:
            # Need to place constants to update boss key items after shuffling levels
            ItemPool.PlaceConstants(spoiler.settings)
            # Assume we can progress through the levels so long as we have enough kongs
            WipeProgressionRequirements(spoiler.settings)
            spoiler.settings.kongs_for_progression = True
            # Fill locations
            Fill(spoiler)
            # Update progression requirements based on what is now accessible after all shuffles are done
            if spoiler.settings.hard_level_progression:
                SetNewProgressionRequirementsUnordered(spoiler.settings)
            else:
                SetNewProgressionRequirements(spoiler.settings)
            # Once progression requirements updated, no longer assume we need kongs freed for level progression
            spoiler.settings.kongs_for_progression = False
            # Check if game is beatable
            if not VerifyWorldWithWorstCoinUsage(spoiler.settings):
                raise Ex.GameNotBeatableException("Game potentially unbeatable after placing all items.")
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
        settings.boss_maps[i] = Maps.JapesBoss  # This requires barrels, forcing it to be placed very early, reducing (removing?) boss fill fail possiblities
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
    # Get sphere 0 GB count
    BlockAccessToLevel(settings, 0)
    Reset()
    accessible = GetAccessibleLocations(settings, [])
    goldenBananaTotals.append(LogicVariables.GoldenBananas)
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
            accessibleMoves = [
                LocationList[x].item
                for x in accessible
                if LocationList[x].item != Items.NoItem and LocationList[x].item is not None and ItemList[LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
            ]
            ownedMoves[previousLevel] = accessibleMoves
    # Cap the B. Locker amounts based on a random fraction of accessible bananas & GBs
    BLOCKER_MIN = 0.4
    BLOCKER_MAX = 0.7
    if settings.hard_blockers:
        BLOCKER_MIN = 0.6
        BLOCKER_MAX = 0.95
    firstBlocker = min(settings.blocker_0, 1, goldenBananaTotals[0])  # First B. Locker shouldn't be more than 1 GB but could be 0 in full item rando
    settings.EntryGBs = [
        firstBlocker,
        min(settings.blocker_1, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[1]))),
        min(settings.blocker_2, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[2]))),
        min(settings.blocker_3, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[3]))),
        min(settings.blocker_4, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[4]))),
        min(settings.blocker_5, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[5]))),
        min(settings.blocker_6, max(firstBlocker, round(uniform(BLOCKER_MIN, BLOCKER_MAX) * goldenBananaTotals[6]))),
        settings.blocker_7,  # Last B. Locker shouldn't be affected
    ]
    # Prevent scenario where B. Lockers randomize to not-always-increasing values
    if settings.randomize_blocker_required_amounts:
        for i in range(1, 7):
            # If this level is more expensive than the next level, swap the B. Lockers
            # This will never break logic - if you could get into a more expensive level 3, you could get into an equally expensive level 4
            if settings.EntryGBs[i] > settings.EntryGBs[i + 1]:
                temp = settings.EntryGBs[i]
                settings.EntryGBs[i] = settings.EntryGBs[i + 1]
                settings.EntryGBs[i + 1] = temp
    settings.BossBananas = [
        min(settings.troff_0, sum(coloredBananaCounts[0]), round(settings.troff_0 / (settings.troff_max * settings.troff_weight_0) * sum(coloredBananaCounts[0]))),
        min(settings.troff_1, sum(coloredBananaCounts[1]), round(settings.troff_1 / (settings.troff_max * settings.troff_weight_1) * sum(coloredBananaCounts[1]))),
        min(settings.troff_2, sum(coloredBananaCounts[2]), round(settings.troff_2 / (settings.troff_max * settings.troff_weight_2) * sum(coloredBananaCounts[2]))),
        min(settings.troff_3, sum(coloredBananaCounts[3]), round(settings.troff_3 / (settings.troff_max * settings.troff_weight_3) * sum(coloredBananaCounts[3]))),
        min(settings.troff_4, sum(coloredBananaCounts[4]), round(settings.troff_4 / (settings.troff_max * settings.troff_weight_4) * sum(coloredBananaCounts[4]))),
        min(settings.troff_5, sum(coloredBananaCounts[5]), round(settings.troff_5 / (settings.troff_max * settings.troff_weight_5) * sum(coloredBananaCounts[5]))),
        min(settings.troff_6, sum(coloredBananaCounts[6]), round(settings.troff_6 / (settings.troff_max * settings.troff_weight_6) * sum(coloredBananaCounts[6]))),
    ]
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)
    ShuffleBossesBasedOnOwnedItems(settings, ownedKongs, ownedMoves)
    settings.owned_kongs_by_level = ownedKongs
    settings.owned_moves_by_level = ownedMoves


def SetNewProgressionRequirementsUnordered(settings: Settings):
    """Set level progression requirements based on a random path of accessible levels."""
    isKeyItemRando = settings.shuffle_items and Types.Key in settings.shuffled_location_types
    ownedKongs = {}
    ownedMoves = {}
    allMoves = ItemPool.DonkeyMoves.copy()
    allMoves.extend(ItemPool.DiddyMoves)
    allMoves.extend(ItemPool.LankyMoves)
    allMoves.extend(ItemPool.TinyMoves)
    allMoves.extend(ItemPool.ChunkyMoves)
    allMoves.extend(ItemPool.ImportantSharedMoves)
    allMoves.extend(ItemPool.TrainingBarrelAbilities())
    KeyEvents = [
        Events.JapesKeyTurnedIn,
        Events.AztecKeyTurnedIn,
        Events.FactoryKeyTurnedIn,
        Events.GalleonKeyTurnedIn,
        Events.ForestKeyTurnedIn,
        Events.CavesKeyTurnedIn,
        Events.CastleKeyTurnedIn,
        Events.HelmKeyTurnedIn,
    ]

    # Before doing anything else, determine how many GBs we can access without entering any levels
    # This is likely to be 1, but depending on the settings there are pretty good odds more are available
    BlockAccessToLevel(settings, 0)
    Reset()
    accessible = GetAccessibleLocations(settings, [])
    runningGBTotal = LogicVariables.GoldenBananas
    minimumBLockerGBs = 0

    # Reset B. Lockers and T&S to initial values
    settings.EntryGBs = [settings.blocker_0, settings.blocker_1, settings.blocker_2, settings.blocker_3, settings.blocker_4, settings.blocker_5, settings.blocker_6, settings.blocker_7]
    settings.BossBananas = [settings.troff_0, settings.troff_1, settings.troff_2, settings.troff_3, settings.troff_4, settings.troff_5, settings.troff_6]
    # We also need to remember T&S values in an array as we'll overwrite the settings value in the process of determining location availability
    initialTNS = [settings.troff_0, settings.troff_1, settings.troff_2, settings.troff_3, settings.troff_4, settings.troff_5, settings.troff_6]

    # Cap the B. Locker amounts based on a random fraction of accessible GBs
    BLOCKER_MIN = 0.4
    BLOCKER_MAX = 0.7
    if settings.hard_blockers:
        BLOCKER_MIN = 0.6
        BLOCKER_MAX = 0.95

    levelsProgressed = []
    foundProgressionKeyEvents = []

    # Until we've completed every level...
    while len(levelsProgressed) < 7:
        openLevels = GetAccessibleOpenLevels(settings, accessible)
        # Pick a random accessible B. Locker
        accessibleIncompleteLevels = [level for level in openLevels if level not in levelsProgressed and settings.EntryGBs[level] <= round(runningGBTotal * BLOCKER_MAX)]
        # If we have no levels accessible, we need to lower a B. Locker count to make one accessible
        if len(accessibleIncompleteLevels) == 0:
            openUnprogressedLevels = [level for level in openLevels if level not in levelsProgressed]
            if len(openUnprogressedLevels) == 0:
                raise Ex.FillException("E1: Hard level order shuffler failed to progress through levels.")
            # Next level chosen randomly (possible room for improvement here?) from accessible levels
            nextLevelToBeat = choice(openUnprogressedLevels)
            # If we are allowed to randomize B. Lockers as we please, try to swap a lower random B. Locker value with this level's
            if settings.randomize_blocker_required_amounts:
                # Find the lowest GB B. Locker
                incompleteLevelWithLowestBLocker = nextLevelToBeat
                for level in range(0, len(settings.EntryGBs)):
                    if level not in levelsProgressed and settings.EntryGBs[level] < settings.EntryGBs[incompleteLevelWithLowestBLocker]:
                        incompleteLevelWithLowestBLocker = level
                # Swap B. Locker values with the randomly chosen accessible level
                temp = settings.EntryGBs[incompleteLevelWithLowestBLocker]
                settings.EntryGBs[incompleteLevelWithLowestBLocker] = settings.EntryGBs[nextLevelToBeat]
                settings.EntryGBs[nextLevelToBeat] = temp
            # If the level still isn't accessible, we have to truncate the required amount
            if settings.EntryGBs[nextLevelToBeat] > round(runningGBTotal * BLOCKER_MAX):
                # Each B. Locker must be greater than the previous one and at least a specified percentage of availalbe GBs
                highroll = round(runningGBTotal * BLOCKER_MAX)
                lowroll = max(minimumBLockerGBs, round(runningGBTotal * BLOCKER_MIN))
                if lowroll > highroll:
                    print("this shouldn't happen but here we are")
                    lowroll = highroll
                settings.EntryGBs[nextLevelToBeat] = randint(lowroll, highroll)
            accessibleIncompleteLevels = [nextLevelToBeat]
        else:
            nextLevelToBeat = choice(accessibleIncompleteLevels)
            # Our last few lobbies could have very low B. Lockers, this condition makes sure B. Lockers always increase in value
            if settings.randomize_blocker_required_amounts and runningGBTotal > settings.blocker_max and settings.EntryGBs[nextLevelToBeat] < minimumBLockerGBs:
                settings.EntryGBs[nextLevelToBeat] = randint(minimumBLockerGBs, settings.blocker_max)
        minimumBLockerGBs = settings.EntryGBs[nextLevelToBeat]  # This B. Locker is now the minimum for the next one
        levelsProgressed.append(nextLevelToBeat)

        # Determine the Kong, GB, and Move accessibility from this level
        # If we get keys (and thus level progression) from the boss...
        if not isKeyItemRando:
            # Block the ability to complete the boss of every level we could complete but haven't yet (including this one)
            # This allows logic to get items from any other accessible level to beat this one
            BlockCompletionOfLevelSet(settings, accessibleIncompleteLevels)
        Reset()
        accessible = GetAccessibleLocations(settings, [])
        runningGBTotal = LogicVariables.GoldenBananas

        # If at any moment we can get keys, let's see if we found any here
        if isKeyItemRando:
            # Until we know a new level is accessible...
            while 1:
                openLevels = GetAccessibleOpenLevels(settings, accessible)
                # If we haven't found all the levels and have progressed through all open levels, we need to lower the CB requirement of one or more bosses for progression
                if len(openLevels) < 7 and len(openLevels) == len(levelsProgressed):
                    bossLocations = [location for id, location in LocationList.items() if location.type == Types.Key and location.level in levelsProgressed]
                    shuffle(bossLocations)
                    priorityBossLocation = None
                    priorityStrength = -1
                    # Loop through the boss locations, looking for the most likely progression candidate
                    for bossLocation in bossLocations:
                        # If this location has nothing, don't even pretend to consider it
                        if bossLocation.item is None or bossLocation.item == Items.NoItem:
                            continue
                        # If this one is already reachable, skip
                        availableCBs = sum(LogicVariables.ColoredBananas[bossLocation.level])
                        if availableCBs < settings.BossBananas[bossLocation.level]:  # Note we track against current values so we take into account already-lowered ones
                            # Absolute top priority for boss rewards is barrels - this can lock other bosses
                            if bossLocation.item == Items.Barrels:
                                priorityBossLocation = bossLocation
                                priorityStrength = 1000
                            # Next up is Keys - these can directly lock lobbies
                            itemOnBoss = ItemList[bossLocation.item]
                            if itemOnBoss.type == Types.Key and priorityStrength < 100:
                                priorityBossLocation = bossLocation
                                priorityStrength = 100
                            # Next up is Swim - if this is shuffled it locks a lobby
                            if bossLocation.item == Items.Swim and priorityStrength < 99:
                                priorityBossLocation = bossLocation
                                priorityStrength = 99
                            # Next up is Vines - if this is shuffled it sometimes locks a lobby but is also often locking a lot of things
                            if bossLocation.item == Items.Vines and priorityStrength < 98:
                                priorityBossLocation = bossLocation
                                priorityStrength = 98
                            # Next up is Guns/Instruments - these are more likely to lock Kongs which unlock Keys
                            if bossLocation.item in ItemPool.Guns(settings) or bossLocation.item in ItemPool.Instruments(settings):
                                priorityBossLocation = bossLocation
                                priorityStrength = 50
                            # Other boss rewards of interest would be moves with no particular priority
                            elif itemOnBoss.type == Types.Shop and priorityStrength < 10:
                                priorityBossLocation = bossLocation
                                priorityStrength = 10
                            # Very low priority reward moves are Oranges and Shockwave/Camera
                            elif itemOnBoss.type in (Types.TrainingBarrel, Types.Shockwave) and priorityStrength < 9:
                                priorityBossLocation = bossLocation
                                priorityStrength = 9
                            # Zero priority rewards is basically everything else
                            elif priorityStrength < 0:
                                priorityBossLocation = bossLocation
                                priorityStrength = 0
                            # The rest won't be locking progression so don't need to be lowered
                    if priorityBossLocation is None:
                        # If we've already lowered all the T&S we can, then that's a fill error
                        raise Ex.FillException("E2: Hard level order shuffler failed to progress through levels.")
                    randomlyRolledRatio = initialTNS[priorityBossLocation.level] / settings.troff_max
                    settings.BossBananas[priorityBossLocation.level] = round(availableCBs * randomlyRolledRatio)
                    accessibleMoves = [
                        LocationList[x].item
                        for x in accessible
                        if LocationList[x].item != Items.NoItem and LocationList[x].item is not None and ItemList[LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
                    ]
                    if priorityBossLocation.item in accessibleMoves:
                        accessibleMoves.remove(priorityBossLocation.item)
                    ownedMoves[priorityBossLocation.level] = accessibleMoves
                    ownedKongs[priorityBossLocation.level] = LogicVariables.GetKongs()
                    # Now that this boss location is accessible, let's see what's new and then repeat this loop in case we didn't find a new key
                    Reset()
                    accessible = GetAccessibleLocations(settings, [])
                else:
                    # To break out of this loop, we either have a level we can progress to or we've just found all the levels
                    break
        # If we acquire keys in the traditional way, we go get this level's boss key
        else:
            # Determine if the level we picked was a level progression key
            if not settings.open_lobbies:
                lobbyIndex = -1
                for key in settings.level_order.keys():
                    if settings.level_order[key] == nextLevelToBeat:
                        lobbyIndex = key - 1
                        break
                foundKeyEvent = KeyEvents[lobbyIndex]
                # If we need this key to open new lobbies, it's a progression key
                if foundKeyEvent in settings.krool_keys_required and foundKeyEvent not in [Events.FactoryKeyTurnedIn, Events.CavesKeyTurnedIn, Events.CastleKeyTurnedIn]:
                    foundProgressionKeyEvents.append(foundKeyEvent)

            # If we've progressed through all open levels, then we need to pick a progression key we've found to acquire and set that level's Troff n Scoff
            if len(openLevels) == len(levelsProgressed) and any(foundProgressionKeyEvents):
                chosenKeyEvent = choice(foundProgressionKeyEvents)
                foundProgressionKeyEvents.remove(chosenKeyEvent)
                # Determine what level needs to be completed
                # Assume levels that could be locked by moves are locked - this will be fixed at the end of this loop
                if chosenKeyEvent == Events.JapesKeyTurnedIn:
                    LogicVariables.Events.append(Events.JapesKeyTurnedIn)
                    bossCompletedLevel = settings.level_order[1]
                elif chosenKeyEvent == Events.AztecKeyTurnedIn:
                    LogicVariables.Events.append(Events.AztecKeyTurnedIn)
                    bossCompletedLevel = settings.level_order[2]
                elif chosenKeyEvent == Events.GalleonKeyTurnedIn:
                    LogicVariables.Events.append(Events.GalleonKeyTurnedIn)
                    bossCompletedLevel = settings.level_order[4]
                elif chosenKeyEvent == Events.ForestKeyTurnedIn:
                    LogicVariables.Events.append(Events.ForestKeyTurnedIn)
                    bossCompletedLevel = settings.level_order[5]
                availableCBs = sum(LogicVariables.ColoredBananas[bossCompletedLevel])
                # If we don't have enough CBs to beat the boss per the settings-determined value
                if availableCBs < initialTNS[bossCompletedLevel]:
                    # Reduce the requirement to an amount guaranteed to be available, based on the ratio of the initial T&S roll
                    randomlyRolledRatio = initialTNS[bossCompletedLevel] / settings.troff_max
                    settings.BossBananas[bossCompletedLevel] = round(availableCBs * randomlyRolledRatio)
                else:
                    settings.BossBananas[bossCompletedLevel] = initialTNS[bossCompletedLevel]
                ownedKongs[bossCompletedLevel] = LogicVariables.GetKongs()
                if settings.unlock_all_moves:
                    ownedMoves[bossCompletedLevel] = allMoves
                else:
                    accessibleMoves = [
                        LocationList[x].item
                        for x in accessible
                        if LocationList[x].item != Items.NoItem and LocationList[x].item is not None and ItemList[LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
                    ]
                    ownedMoves[bossCompletedLevel] = accessibleMoves

    # For any boss location behind a T&S we didn't lower...
    bossLocations = [
        location for id, location in LocationList.items() if location.type == Types.Key and location.level in levelsProgressed and settings.BossBananas[location.level] >= initialTNS[location.level]
    ]
    for bossLocation in bossLocations:
        # For any level we explicitly blocked, undo the blocking
        if settings.BossBananas[bossLocation.level] > 500:
            # We should have access to everything by this point
            settings.BossBananas[bossLocation.level] = initialTNS[bossLocation.level]
        # For any level we haven't lowered yet, assume we own everything
        if bossLocation.level not in ownedKongs.keys():
            ownedKongs[bossLocation.level] = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
            ownedMoves[bossLocation.level] = allMoves
        # If boss rewards could be anything, we have to make sure they're accessible independent of all else
        if isKeyItemRando:
            bossReward = bossLocation.item
            # If the boss reward doesn't contain progression, it's fine
            if bossReward is None or ItemList[bossReward].type not in (Types.TrainingBarrel, Types.Shop, Types.Shockwave, Types.Key):
                continue
            # You never have the boss reward when fighting it, so remove it from consideration for boss placement
            if bossReward in ownedMoves[bossLocation.level]:
                ownedMoves[bossLocation.level].remove(bossReward)
            # If it could contain progression, place a dummy item there and see if we can reach it
            bossLocation.PlaceItem(Items.TestItem)
            Reset()
            accessible = GetAccessibleLocations(settings, [])
            if not LogicVariables.found_test_item:
                # If we can't reach it eventually in this world state, then we need to lower this T&S
                randomlyRolledRatio = initialTNS[bossLocation.level] / settings.troff_max
                availableCBs = sum(LogicVariables.ColoredBananas[bossLocation.level])
                settings.BossBananas[bossLocation.level] = round(availableCBs * randomlyRolledRatio)
                accessibleMoves = [
                    LocationList[x].item
                    for x in accessible
                    if LocationList[x].item != Items.NoItem and LocationList[x].item is not None and ItemList[LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
                ]
                ownedMoves[bossLocation.level] = accessibleMoves
                ownedKongs[bossLocation.level] = LogicVariables.GetKongs()
            # Put it back so we don't accidentally an item
            bossLocation.PlaceItem(bossReward)

    # Because we might not have sorted the B. Lockers when they're randomly generated, Helm might be a surprisingly low number if it's not maximized
    if settings.randomize_blocker_required_amounts and not settings.maximize_helm_blocker and settings.EntryGBs[7] < minimumBLockerGBs:
        # Ensure that Helm is the most expensive B. Locker
        settings.EntryGBs[7] = randint(minimumBLockerGBs, settings.blocker_max)
    # Place boss locations based on kongs and moves found for each level
    ShuffleBossesBasedOnOwnedItems(settings, ownedKongs, ownedMoves)
    settings.owned_kongs_by_level = ownedKongs
    settings.owned_moves_by_level = ownedMoves

    # After setting all the progression, make sure we did it right
    # Technically the coin logic check after this will cover it, but this will help identify issues better
    Reset()
    if not GetAccessibleLocations(settings, [], SearchMode.CheckAllReachable):
        raise Ex.GameNotBeatableException("Complex progression generation prevented 101%.")


def GetAccessibleOpenLevels(settings, accessible):
    """Return the list of levels (not lobbies) you have access to after running GetAccessibleLocations()."""
    KeyEvents = [
        Events.JapesKeyTurnedIn,
        Events.AztecKeyTurnedIn,
        Events.FactoryKeyTurnedIn,
        Events.GalleonKeyTurnedIn,
        Events.ForestKeyTurnedIn,
        Events.CavesKeyTurnedIn,
        Events.CastleKeyTurnedIn,
        Events.HelmKeyTurnedIn,
    ]
    # Determine what keys we have
    keysTurnedIn = [event for event in LogicVariables.Events if event in KeyEvents]
    openLobbyIndexes = [1]
    if not settings.open_lobbies:
        # For the keys we have, determine what lobbies are open
        for key in keysTurnedIn:
            if key == Events.JapesKeyTurnedIn:
                openLobbyIndexes.append(2)
            elif key == Events.AztecKeyTurnedIn:
                openLobbyIndexes.append(3)
                openLobbyIndexes.append(4)
            elif key == Events.GalleonKeyTurnedIn:
                openLobbyIndexes.append(5)
            elif key == Events.ForestKeyTurnedIn:
                openLobbyIndexes.append(6)
                openLobbyIndexes.append(7)
    else:
        # If the setting is on, then all lobbies are open
        openLobbyIndexes = [1, 2, 3, 4, 5, 6, 7]
    # We need a kong who can enter the Caves Lobby logically
    if 6 in openLobbyIndexes and not LogicVariables.donkey and not LogicVariables.chunky and not (LogicVariables.tiny and LogicVariables.twirl):
        openLobbyIndexes.remove(6)
    # We may need training moves for access to some lobbies
    if settings.training_barrels != "normal":
        # Vines only matter if we don't have Isles warps activated
        if settings.activate_all_bananaports == "off" and not LogicVariables.vines:
            # Aztec lobby requires vines to get to
            if 2 in openLobbyIndexes:
                openLobbyIndexes.remove(2)
            # Caves lobby requires vines to get to
            if 6 in openLobbyIndexes:
                openLobbyIndexes.remove(6)
        # Galleon lobby requires swim
        if 4 in openLobbyIndexes and not LogicVariables.swim:
            openLobbyIndexes.remove(4)
    # Convert indexes to the shuffled levels
    accessibleOpenLevels = [settings.level_order[index] for index in openLobbyIndexes]
    # After converting to levels, double check that we can actually do anything in Aztec
    if Levels.AngryAztec in accessibleOpenLevels:
        if not LogicVariables.vines and not (LogicVariables.tiny and LogicVariables.twirl):  # Need vines or (tiny + twirl)
            accessibleOpenLevels.remove(Levels.AngryAztec)
    return accessibleOpenLevels


def BlockAccessToLevel(settings: Settings, level):
    """Assume the level index passed in is the furthest level you have access to in the level order."""
    for i in range(0, 8):
        if i >= level:
            # This level and those after it are locked out
            settings.EntryGBs[i] = 1000
            if i < 7:
                settings.BossBananas[i] = 1000
        else:
            # Previous levels assumed accessible
            settings.EntryGBs[i] = 0
            if i < 7:
                settings.BossBananas[i] = 0
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)


def BlockCompletionOfLevelSet(settings: Settings, lockedLevels):
    """Prevent acquiring the keys of the levels provided."""
    for i in range(0, 7):
        if i in lockedLevels:
            # This level is incompletable
            settings.BossBananas[i] = 1000


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
        if (spoiler.settings.move_rando != "off" and not spoiler.settings.unlock_all_moves) or spoiler.settings.kong_rando or any(spoiler.settings.shuffled_location_types):
            FillKongsAndMovesGeneric(spoiler)
        else:
            # Just check if normal item locations are beatable with given settings
            ItemPool.PlaceConstants(spoiler.settings)
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.VanillaItemsGameNotBeatableException("Game unbeatable.")
    GeneratePlaythrough(spoiler)
    if spoiler.settings.wrinkly_hints in ["standard", "cryptic"]:
        compileHints(spoiler)
    Reset()
    ShuffleExits.Reset()
    spoiler.createJson()
    js.postMessage("Patching ROM...")
    return spoiler


def ShuffleMisc(spoiler):
    """Shuffle miscellaneous objects outside of main fill algorithm, including Kasplats, Bonus barrels, and bananaport warps."""
    # T&S and Wrinkly Door Shuffle
    if (
        spoiler.settings.wrinkly_location_rando
        or spoiler.settings.tns_location_rando
        or ("remove_wrinkly_puzzles" in spoiler.settings.misc_changes_selected or len(spoiler.settings.misc_changes_selected) == 0)
    ):
        ShuffleDoors(spoiler)
    # Handle Crown Placement
    if spoiler.settings.crown_placement_rando:
        crown_replacements = {}
        crown_human_replacements = {}
        ShuffleCrowns(crown_replacements, crown_human_replacements)
        spoiler.crown_locations = crown_replacements
        spoiler.human_crowns = dict(sorted(crown_human_replacements.items()))
    # Handle kasplats - this is the first VerifyWorld check, all shuffles affecting Locations must be before this one
    KasplatShuffle(spoiler, LogicVariables)
    spoiler.human_kasplats = {}
    spoiler.UpdateKasplats(LogicVariables.kasplat_map)
    # Handle bonus barrels
    if spoiler.settings.bonus_barrels in ("random", "selected"):
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # CB Shuffle
    if spoiler.settings.cb_rando:
        ShuffleCBs(spoiler)
    # Handle Bananaports
    if spoiler.settings.bananaport_rando == "in_level":
        replacements = []
        human_replacements = {}
        ShuffleWarps(replacements, human_replacements)
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    elif spoiler.settings.bananaport_rando in ("crossmap_coupled", "crossmap_decoupled"):
        replacements = []
        human_replacements = {}
        ShuffleWarpsCrossMap(replacements, human_replacements, spoiler.settings.bananaport_rando == "crossmap_coupled")
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    # Random Patches
    if spoiler.settings.random_patches:
        human_patches = []
        spoiler.human_patches = ShufflePatches(spoiler, human_patches).copy()
    if spoiler.settings.shuffle_shops:
        ShuffleShopLocations(spoiler)
    # Item Rando
    spoiler.human_item_assignment = {}
    if spoiler.settings.activate_all_bananaports in ["all", "isles"]:
        # In simpler bananaport shuffling, we can rely on the map id and warp number to find pairs
        if spoiler.settings.bananaport_rando in ("in_level", "off"):
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
        # In complex cross-map shuffling, we have to rely on saved destination regions to generate transitions
        else:
            for warp in BananaportVanilla.values():
                warpRegion = Logic.Regions[warp.region_id]
                if spoiler.settings.activate_all_bananaports != "isles" or (warp.region_id in IslesLogic.LogicRegions.keys() and warp.destination_region_id in IslesLogic.LogicRegions.keys()):
                    bananaportExit = TransitionFront(warp.destination_region_id, lambda l: True)
                    warpRegion.exits.append(bananaportExit)
    spoiler.settings.update_valid_locations()
