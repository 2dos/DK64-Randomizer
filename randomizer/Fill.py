"""Module used to distribute items randomly."""
from json import dumps
from math import floor
from random import choice, randint, shuffle, uniform

import js
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
import randomizer.LogicFiles.DKIsles as IslesLogic
import randomizer.ShuffleExits as ShuffleExits
from randomizer.CompileHints import compileHints, compileMicrohints
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Settings import (
    ActivateAllBananaports,
    BananaportRando,
    FillAlgorithm,
    HelmDoorItem,
    LogicType,
    MinigameBarrels,
    MoveRando,
    RandomPrices,
    ShockwaveStatus,
    ShuffleLoadingZones,
    TrainingBarrels,
    WinCondition,
    WrinklyHints,
)
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Enums.Warps import Warps
from randomizer.Lists.Item import ItemList, KongFromItem
from randomizer.Lists.Location import LocationList, PreGivenLocations, SharedMoveLocations, TrainingBarrelLocations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Lists.ShufflableExit import GetLevelShuffledToIndex, GetShuffledLevelIndex
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Logic import LogicVarHolder, LogicVariables
from randomizer.Logic import Regions as RegionList
from randomizer.LogicClasses import Sphere, TransitionFront
from randomizer.Patching import ApplyRandomizer
from randomizer.Prices import GetMaxForKong
from randomizer.Settings import Settings
from randomizer.ShuffleBarrels import BarrelShuffle
from randomizer.ShuffleBosses import CorrectBossKongLocations, ShuffleBossesBasedOnOwnedItems
from randomizer.ShuffleCBs import ShuffleCBs
from randomizer.ShuffleCoins import ShuffleCoins
from randomizer.ShuffleCrowns import ShuffleCrowns
from randomizer.ShuffleDoors import ShuffleDoors, ShuffleVanillaDoors
from randomizer.ShuffleFairies import ShuffleFairyLocations
from randomizer.ShuffleItems import ShuffleItems
from randomizer.ShuffleKasplats import InitKasplatMap, KasplatShuffle
from randomizer.ShufflePatches import ShufflePatches
from randomizer.ShuffleShopLocations import ShuffleShopLocations
from randomizer.ShuffleWarps import LinkWarps, ShuffleWarps, ShuffleWarpsCrossMap


def GetExitLevelExit(region):
    """Get the exit that using the "Exit Level" button will take you to."""
    level = region.level

    # If you have option to restart, means there is no Exit Level option
    if region.restart is not None:
        return None
    # For now, restarts will not be randomized
    # if settings.shuffle_loading_zones == ShuffleLoadingZones.all and region.restart is not None:
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


def GetAccessibleLocations(settings, startingOwnedItems, searchType, purchaseList=None, targetItemId=None):
    """Search to find all reachable locations given owned items."""
    # No logic? Calls to this method that are checking things just return True
    if settings.logic_type == LogicType.nologic and searchType in [SearchMode.CheckAllReachable, SearchMode.CheckBeatable, SearchMode.CheckSpecificItemReachable]:
        return True
    if purchaseList is None:
        purchaseList = []
    accessible = set()
    newLocations = set()
    ownedItems = startingOwnedItems.copy()
    newItems = []  # debug code utility
    playthroughLocations = []
    unpurchasedEmptyShopLocationIds = []
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
            if location.logically_relevant:
                LogicVariables.SpecialLocationsReached.append(locationId)
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
                        # If this location is flagged as inaccessible, ignore it
                        if location_obj.inaccessible:
                            continue
                        # If this location is a bonus barrel, must make sure its logic is met as well
                        elif (
                            (location.bonusBarrel is MinigameType.BonusBarrel and settings.bonus_barrels != MinigameBarrels.skip)
                            or (location.bonusBarrel is MinigameType.HelmBarrel and settings.helm_barrels != MinigameBarrels.skip)
                        ) and (not MinigameRequirements[BarrelMetaData[location.id].minigame].logic(LogicVariables)):
                            continue
                        # If this location is a hint door, then make sure we're the right Kong
                        elif location_obj.item is not None and location_obj.type == Types.Hint and not LogicVariables.HintAccess(location_obj, region.id):
                            continue
                        # If this location has a blueprint, then make sure this is the correct kong
                        elif (location_obj.item is not None and ItemList[location_obj.item].type == Types.Blueprint) and (not LogicVariables.BlueprintAccess(ItemList[location_obj.item])):
                            continue
                        # If this location is a Kasplat but doesn't have a blueprint, still make sure this is the correct kong to be accessible at all
                        elif (location_obj.type == Types.Blueprint) and (not LogicVariables.IsKong(location_obj.kong) and not settings.free_trade_items):
                            continue
                        # If this location is a shop then we know it's reachable and that we have the money for it, but we may want to purchase the location
                        elif location_obj.type == Types.Shop:
                            # The handling of shop locations is a bit complicated so it's broken up for readability
                            # Empty locations are notable because we don't want to buy empty shops (and waste coins) if the fill is complete
                            shopIsEmpty = location_obj.item is None or location_obj.item == Items.NoItem
                            # When handling coin logic we want to buy specific moves, so we may not be allowed to purchase every location
                            locationCanBeBought = searchType != SearchMode.GetReachableWithControlledPurchases or location.id in purchaseList
                            # We always buy non-empty locations if we are not prevented from buying this location
                            if not shopIsEmpty and locationCanBeBought:
                                LogicVariables.PurchaseShopItem(location.id)
                            # Empty locations are accessible, but we need to note them down and possibly purchase them later depending on the search type
                            elif shopIsEmpty:
                                unpurchasedEmptyShopLocationIds.append(location.id)
                        elif location.id == Locations.NintendoCoin:
                            # Spend Two Coins for arcade lever
                            LogicVariables.Coins[Kongs.donkey] -= 2
                            LogicVariables.SpentCoins[Kongs.donkey] += 2
                        newLocations.add(location.id)
                # Check accessibility for each exit in this region
                exits = region.exits.copy()
                # If loading zones are shuffled or your respawn is in a random location, the "Exit Level" button in the pause menu could potentially take you somewhere new
                if (settings.shuffle_loading_zones or settings.random_starting_region) and region.level != Levels.DKIsles and region.level != Levels.Shops:
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
                if region.deathwarp is not None and settings.perma_death is False:
                    destination = region.deathwarp.dest
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if destination not in addedRegions and region.deathwarp.logic(LogicVariables):
                        addedRegions.add(destination)
                        newRegion = Logic.Regions[destination]
                        newRegion.id = destination
                        regionPool.add(newRegion)
                        # If this region has day access, the deathwarp will occur on the same time of day
                        # Note that no deathwarps are dependent on time of day
                        if region.dayAccess:
                            Logic.Regions[destination].dayAccess = True
                            # Count as event added so search doesn't get stuck if region is searched,
                            # then later a new time of day access is found so it should be re-visited
                            eventAdded = True
                        # And vice versa
                        if region.nightAccess:
                            Logic.Regions[destination].nightAccess = True
                            eventAdded = True
    # If we're here to get accessible locations for fill purposes, we need to take a harder look at all the empty shops we didn't buy
    if searchType == SearchMode.GetReachableForFilling:
        shuffle(unpurchasedEmptyShopLocationIds)  # This shuffle is to not bias fills towards earlier shops
        # For each location...
        for location_id in unpurchasedEmptyShopLocationIds:
            # If we can, buy it. This will affect our ability to buy future locations. It's not a guarantee we'll be able to buy all of these locations.
            if LogicVariables.CanBuy(location_id):
                LogicVariables.PurchaseShopItem(location_id)
            # If we can't, treat the location as inaccessible
            else:
                accessible.remove(location_id)
    if searchType in (SearchMode.GetReachable, SearchMode.GetReachableForFilling, SearchMode.GetReachableWithControlledPurchases):
        return accessible
    elif searchType == SearchMode.CheckBeatable or searchType == SearchMode.CheckSpecificItemReachable:
        # If the search has completed and the target item has not been found, then we failed to find it
        # settings.debug_accessible = accessible
        return False
    elif searchType == SearchMode.GeneratePlaythrough:
        return playthroughLocations
    elif searchType == SearchMode.CheckAllReachable:
        expected_accessible_locations = [x for x in LocationList if not LocationList[x].inaccessible]
        # incorrectly_accessible = [x for x in accessible if x not in expected_accessible_locations]
        # incorrectly_inaccessible = [x for x in expected_accessible_locations if x not in accessible]
        # always_inaccessible_locations = [x for x in LocationList if LocationList[x].inaccessible]
        # settings.debug_accessible = accessible
        # settings.debug_accessible_not = [location for location in LocationList if location not in accessible]
        # settings.debug_enormous_pain_1 = [LocationList[location] for location in settings.debug_accessible]
        # settings.debug_enormous_pain_3 = [LocationList[location] for location in settings.debug_accessible_not]
        # if len(accessible) != len(expected_accessible_locations):
        #     return False
        # return True
        return len(accessible) == len(expected_accessible_locations)
    elif searchType == SearchMode.GetUnreachable:
        return [x for x in LocationList if x not in accessible and not LocationList[x].inaccessible]


def VerifyWorld(settings):
    """Make sure all item locations are reachable on current world graph with constant items placed and all other items owned."""
    if settings.logic_type == LogicType.nologic:
        return True  # Don't verify world in no logic
    ItemPool.PlaceConstants(settings)
    unreachables = GetAccessibleLocations(settings, ItemPool.AllItems(settings), SearchMode.GetUnreachable)
    allLocationsReached = len(unreachables) == 0
    allCBsFound = True
    for level_index in range(7):
        if sum(LogicVariables.ColoredBananas[level_index]) != 500:
            # missingCBs = []
            # for region_collectible_list in Logic.CollectibleRegions.values():
            #     for collectible in region_collectible_list:
            #         if collectible.enabled and not collectible.added:
            #             missingCBs.append(collectible)
            allCBsFound = False
    Reset()
    return allLocationsReached and allCBsFound


def VerifyWorldWithWorstCoinUsage(settings):
    """Make sure the game is beatable without it being possible to run out of coins for required moves."""
    if settings.logic_type == LogicType.nologic:
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
    # Set up some thresholds for speeding this method up
    medalThreshold = settings.medal_requirement
    fairyThreshold = settings.rareware_gb_fairies
    pearlThreshold = 5
    if settings.fast_gbs:
        pearlThreshold = 1
    while 1:
        Reset()
        reachable = GetAccessibleLocations(settings, [], SearchMode.GetReachableWithControlledPurchases, locationsToPurchase)
        # Subtract the price of the chosen location from maxCoinsNeeded
        itemsToPurchase = [LocationList[x].item for x in locationsToPurchase]
        coinsSpent = GetMaxCoinsSpent(settings, locationsToPurchase)
        coinsNeeded = [maxCoins[kong] - coinsSpent[kong] for kong in range(0, 5)]
        LogicVariables.UpdateCoins()
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
        # We can cheat some - here we calculate things we know we can add to the purchase order for free
        # All we have to do is ensure that these items are not progressive in ANY way
        # If we manage to add anything to the purchase order, we cut N GetAccessibleLocation calls where N is the length of newReachableShops
        anythingAddedToPurchaseOrder = False
        # Thresholds are the values that would cause the next item of that type to give you access to more locations
        # The GB threshold is the next B. Locker from what we've previously found - opening a B. Locker likely gives you access to more coins
        currentGBCount = LogicVariables.GoldenBananas
        gbThreshold = 1000
        for blocker in range(0, 8):
            if settings.EntryGBs[blocker] > currentGBCount and settings.EntryGBs[blocker] < gbThreshold:
                gbThreshold = settings.EntryGBs[blocker]
        currentMedalCount = LogicVariables.BananaMedals  # Jetpac access might give you another item that gives you access to more coins
        currentFairyCount = LogicVariables.BananaFairies  # Rareware GB access might do the same
        currentPearlCount = LogicVariables.Pearls  # Mermaid GB access might do the same
        for shopLocationId in newReachableShops:
            # Check all of the newly reachable shops' items
            shopItem = LocationList[shopLocationId].item
            # If the item is not going to exactly meet that item type's threshold, we can freely purchase it knowing it will never be progression
            if shopItem == Items.Pearl and (currentPearlCount < (pearlThreshold - 1) or currentPearlCount >= pearlThreshold):
                currentPearlCount += 1  # Treat the item as collected for future calculations, we might approach the threshold during this process
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            if shopItem == Items.BananaMedal and (currentMedalCount < (medalThreshold - 1) or currentMedalCount >= medalThreshold):
                currentMedalCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            if shopItem == Items.BananaFairy and (currentFairyCount < (fairyThreshold - 1) or currentFairyCount >= fairyThreshold):
                currentFairyCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            # Treat GBs and Blueprints as identical
            if (shopItem == Items.GoldenBanana or shopItem in ItemPool.Blueprints()) and (currentGBCount < (gbThreshold - 1) or currentGBCount > gbThreshold):
                currentGBCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            # These items will never practically give progression. Helm doors are not really relevant here, as any theoretical coin lock will happen WELL before this point.
            if shopItem in (Items.BattleCrown, Items.FakeItem, Items.RarewareCoin, Items.NintendoCoin):
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
        # If we added anything to the purchase order, short-circuit back to the top of the loop and keep going with a (hopefully) greatly expanded purchase list
        if anythingAddedToPurchaseOrder:
            continue
        # Now that we know our next item has to give us progression in some form, we can consolidate our "worst location candidates" into the worst options among each type
        # Find the most expensive location of each type (it may not exist)
        mostExpensivePearl = None
        pearlShops = [location for location in newReachableShops if LocationList[location].item == Items.Pearl]
        if settings.random_prices == RandomPrices.vanilla and len(pearlShops) > 0:  # In vanilla prices, prices are by item so we know all these locations have the same price (0)
            mostExpensivePearl = pearlShops[0]
        else:
            for shop in pearlShops:
                if mostExpensivePearl is None or settings.prices[shop] > settings.prices[mostExpensivePearl]:
                    mostExpensivePearl = shop
        mostExpensiveMedal = None
        medalShops = [location for location in newReachableShops if LocationList[location].item == Items.BananaMedal]
        if settings.random_prices == RandomPrices.vanilla and len(medalShops) > 0:  # Same vanilla price logic applies to all of the threshold types (they all cost 0)
            mostExpensiveMedal = medalShops[0]
        else:
            for shop in medalShops:
                if mostExpensiveMedal is None or settings.prices[shop] > settings.prices[mostExpensiveMedal]:
                    mostExpensiveMedal = shop
        mostExpensiveFairy = None
        fairyShops = [location for location in newReachableShops if LocationList[location].item == Items.BananaFairy]
        if settings.random_prices == RandomPrices.vanilla and len(fairyShops) > 0:
            mostExpensiveFairy = fairyShops[0]
        else:
            for shop in fairyShops:
                if mostExpensiveFairy is None or settings.prices[shop] > settings.prices[mostExpensiveFairy]:
                    mostExpensiveFairy = shop
        mostExpensiveGB = None
        gbShops = [location for location in newReachableShops if (LocationList[location].item == Items.GoldenBanana or LocationList[location].item in ItemPool.Blueprints())]
        if settings.random_prices == RandomPrices.vanilla and len(gbShops) > 0:  # While GBs and Blueprints aren't the same item, they both always cost 0 in vanilla
            mostExpensiveGB = gbShops[0]
        else:
            for shop in gbShops:
                if mostExpensiveGB is None or settings.prices[shop] > settings.prices[mostExpensiveGB]:
                    mostExpensiveGB = shop
        # Prepare the candidates for "worst location" - exclude any of the threshold items that we know the worst of
        thresholdItems = ItemPool.Blueprints().copy()
        thresholdItems.extend([Items.Pearl, Items.BananaMedal, Items.BananaFairy, Items.GoldenBanana])
        worstLocationCandidates = [shop for shop in newReachableShops if LocationList[shop].item not in thresholdItems]
        # If there exists a spot of this type, then we add the worst of this type to our list of candidates
        if mostExpensivePearl is not None:
            worstLocationCandidates.append(mostExpensivePearl)
        if mostExpensiveMedal is not None:
            worstLocationCandidates.append(mostExpensiveMedal)
        if mostExpensiveFairy is not None:
            worstLocationCandidates.append(mostExpensiveFairy)
        if mostExpensiveGB is not None:
            worstLocationCandidates.append(mostExpensiveGB)
        locationToBuy = worstLocationCandidates[0]
        if len(worstLocationCandidates) > 1:  # Things can be sped up if there's only one option (this tends to happen)
            for shopLocation in worstLocationCandidates:
                # Recheck accessible to see how many coins will be available afterward
                tempLocationsToPurchase = locationsToPurchase.copy()
                tempLocationsToPurchase.append(shopLocation)
                Reset()
                reachableAfter: list = GetAccessibleLocations(settings, [], SearchMode.GetReachableWithControlledPurchases, tempLocationsToPurchase)
                LogicVariables.UpdateCoins()
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
                if settings.win_condition != WinCondition.all_fairies:
                    sphere.locations.remove(locationId)
                continue
            if location.item == Items.BananaMedal:
                if settings.win_condition != WinCondition.all_medals:
                    sphere.locations.remove(locationId)
                continue
            if location.item is not None and ItemList[location.item].type == Types.Blueprint:
                if settings.win_condition != WinCondition.all_blueprints:
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
    AccessibleHintsForLocation = {}
    for sphere in PlaythroughLocations:
        # Don't want constant locations in woth and we can filter out some types of items as not being essential to the woth
        for loc in [
            loc
            for loc in sphere.locations  # If Keys are constant, we may still want path hints for them.
            if (not LocationList[loc].constant or ItemList[LocationList[loc].item].type == Types.Key)
            and ItemList[LocationList[loc].item].type not in (Types.Banana, Types.BlueprintBanana, Types.Crown, Types.Medal, Types.Blueprint)
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
        # If this is a WotH candidate, take note of what hints are available without this location
        else:
            AccessibleHintsForLocation[locationId] = LogicVariables.Hints.copy()
        # Either way, add location back
        location.PlaceItem(item)
    # Only need to build paths for item rando
    if spoiler.settings.shuffle_items:
        CalculateWothPaths(spoiler, WothLocations)
        CalculateFoolish(spoiler, WothLocations)
    spoiler.accessible_hints_for_location = AccessibleHintsForLocation
    # We kept Keys around to generate paths better, but we don't need them in the spoiler log or being hinted (except for the Helm Key if it's there and also keep the Banana Hoard path)
    WothLocations = [loc for loc in WothLocations if not LocationList[loc].constant or loc == Locations.HelmKey or loc == Locations.BananaHoard]
    if spoiler.settings.shuffle_items:
        # The non-key 8 paths are a bit misleading, so it's best not to show them
        for path_loc in [key for key in spoiler.woth_paths.keys()]:
            if path_loc not in WothLocations:
                del spoiler.woth_paths[path_loc]
    return WothLocations


def CalculateWothPaths(spoiler, WothLocations):
    """Calculate the Paths (dependencies) for each Way of the Hoard item."""
    # Helps get more accurate paths by removing important obstacles to level entry
    # Removes the following:
    # - The need for GBs and coins to reach locations
    # - The need for vines to progress in Aztec
    # - The need for swim to get into level 4
    # - The need for vines to get to upper Isles
    # - The need for all keys to access K. Rool
    # - The need for keys to open lobbies (this is done with open_lobbies)
    old_open_lobbies_temp = spoiler.settings.open_lobbies  # It's far less likely for a key to be a prerequisite
    LogicVariables.assumeInfiniteGBs = True  # This means we don't have to worry about moves required to get GBs to enter B. Lockers - we already know we can clear all B. Lockers
    LogicVariables.assumeInfiniteCoins = True  # This means we don't have to worry about moves required to get coins - we already know there is no breaking purchase order
    LogicVariables.assumeKRoolAccess = True  # This makes the K. Rool path better if we need it
    if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all:
        # These assumptions are only good in level order because entrances can matter more in LZR
        LogicVariables.assumeAztecEntry = True
        LogicVariables.assumeLevel4Entry = True
        LogicVariables.assumeUpperIslesAccess = True
        spoiler.settings.open_lobbies = True

    # Prep the dictionary that will contain the path for the key item
    for locationId in WothLocations:
        spoiler.woth_paths[locationId] = [locationId]  # The endpoint is on its own path
    # If K. Rool is the win condition, prepare phase-specific paths as well
    if spoiler.settings.win_condition == WinCondition.beat_krool:
        for phase in spoiler.settings.krool_order:
            spoiler.krool_paths[phase] = []
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
        accessible = GetAccessibleLocations(spoiler.settings, assumedItems, SearchMode.GetReachable)
        # Then check every other WotH location for accessibility
        for other_location in WothLocations:
            # If it is no longer accessible, then this location is on the path of that other location
            if other_location not in accessible:
                spoiler.woth_paths[other_location].append(locationId)
        # If the win condition is K. Rool, also add this location to those paths as applicable
        if spoiler.settings.win_condition == WinCondition.beat_krool:
            if Kongs.donkey in spoiler.settings.krool_order and Events.KRoolDonkey not in LogicVariables.Events:
                spoiler.krool_paths[Kongs.donkey].append(locationId)
            if Kongs.diddy in spoiler.settings.krool_order and Events.KRoolDiddy not in LogicVariables.Events:
                spoiler.krool_paths[Kongs.diddy].append(locationId)
            if Kongs.lanky in spoiler.settings.krool_order and Events.KRoolLanky not in LogicVariables.Events:
                spoiler.krool_paths[Kongs.lanky].append(locationId)
            if Kongs.tiny in spoiler.settings.krool_order and Events.KRoolTiny not in LogicVariables.Events:
                spoiler.krool_paths[Kongs.tiny].append(locationId)
            if Kongs.chunky in spoiler.settings.krool_order and Events.KRoolChunky not in LogicVariables.Events:
                spoiler.krool_paths[Kongs.chunky].append(locationId)
        # Put the item back for future calculations
        location.PlaceItem(item_id)
    # After everything is calculated, get rid of paths for false WotH locations
    # If an item doesn't show up on any other paths, it's not actually WotH
    # This is rare, but could happen if the item at the location is needed for coins or B. Lockers - it's often required, but not helpful to hint at all
    anything_removed = True
    while anything_removed:
        anything_removed = False
        # Check every WotH location
        for locationId in WothLocations:
            location = LocationList[locationId]
            # If this item doesn't normally show up on paths but is definitely needed, no need to calculate it, it's definitely WotH
            if location.item in assumedItems or location.item == Items.BananaHoard:
                continue
            # Check every other path to see if this location is on any other path
            inAnotherPath = False
            for otherLocationId in [loc for loc in WothLocations if loc != locationId]:
                if locationId in spoiler.woth_paths[otherLocationId]:
                    inAnotherPath = True
                    break
            # If it's not on any other path, it's not WotH
            if not inAnotherPath:
                # Never pare out these moves - the assumptions might overlook their need to enter levels with
                # This is a bit of a compromise, as you *might* see these moves WotH purely for coins/GBs but they won't be on paths
                if location.item in (Items.Swim, Items.Vines, Items.PonyTailTwirl):
                    continue
                # Keys that make it here are also always WotH
                if location.item in ItemPool.Keys():
                    continue
                WothLocations.remove(locationId)
                del spoiler.woth_paths[locationId]
                # If we remove anything, we have to check the whole list again
                anything_removed = True
                break
    # None of these assumptions should ever make it out of this method
    LogicVariables.assumeInfiniteGBs = False
    LogicVariables.assumeInfiniteCoins = False
    LogicVariables.assumeAztecEntry = False
    LogicVariables.assumeLevel4Entry = False
    LogicVariables.assumeUpperIslesAccess = False
    LogicVariables.assumeKRoolAccess = False
    spoiler.settings.open_lobbies = old_open_lobbies_temp  # Undo the open lobbies setting change as needed


def CalculateFoolish(spoiler, WothLocations):
    """Calculate the items and regions that are foolish (blocking no major items)."""
    # FOOLISH MOVES - unable to verify the accuracy of foolish moves, so these have to go :(
    # The problem that needs to be solved: How do you guarantee neither part of a required either/or is foolish?
    # The cases you have to handle in order to solve this:
    # - Both are WotH: this should be straightforward, neither is foolish
    # - Neither is WotH: you have to check that items are individually foolish (the code below) and all individually foolish items are collectively foolish
    # - ONE is WotH: this is hard, as you don't know what of your WotH items could be part of the either/or with an individually foolish move
    # The current state of affairs could guarantee that you couldn't get both parts of an either/or as foolish, but I don't think either should be
    # Until this problem is solved, foolish moves will remain dormant

    # wothItems = [LocationList[loc].item for loc in WothLocations]
    # # First we need to determine what Major Items are foolish
    # foolishItems = []
    # # Determine which of our major items we need to check
    # majorItems = ItemPool.AllKongMoves()
    # if spoiler.settings.training_barrels != TrainingBarrels.normal:
    #     # I don't trust oranges quite yet - you can put an item in Diddy's upper cabin and it might think oranges is foolish still
    #     majorItems.extend([Items.Vines, Items.Swim, Items.Barrels, Items.Oranges])
    # if spoiler.settings.shockwave_status != ShockwaveStatus.shuffled_decoupled:
    #     majorItems.append(Items.CameraAndShockwave)
    # if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
    #     majorItems.append(Items.Camera)
    #     if spoiler.settings.shuffle_items and Types.RainbowCoin in spoiler.settings.shuffled_location_types:
    #         majorItems.append(Items.Shockwave)  # Shockwave foolish is virtually useless to hint as foolish unless rainbow coins are in the pool
    # # We want to know if the bean and pearls are foolish so we can use them in the regional foolish checks later
    # if Types.Bean in spoiler.settings.shuffled_location_types:
    #     majorItems.append(Items.Bean)
    # if Types.Pearl in spoiler.settings.shuffled_location_types:
    #     majorItems.append(Items.Pearl)
    # for item in majorItems:
    #     # If this item is in the WotH, it can't possibly be foolish so we can skip it
    #     if item in wothItems:
    #         continue
    #     # Check the item to see if it locks *any* progression (even non-critical)
    #     Reset()
    #     # Because of how much overlap there is between these two, either they're both foolish or neither is
    #     # if item in (Items.HomingAmmo, Items.SniperSight):
    #     #     LogicVariables.BanItems([Items.HomingAmmo, Items.SniperSight])
    #     # else:
    #     LogicVariables.BanItems([item])  # Ban this item from being picked up
    #     GetAccessibleLocations(spoiler.settings, [], SearchMode.GetReachable)  # Check what's reachable
    #     if LogicVariables.HasAllItems():  # If you still have all the items, this one blocks no progression and is foolish
    #         foolishItems.append(item)
    # spoiler.foolish_moves = [item for item in foolishItems if item not in (Items.Bean, Items.Pearl)]  # Don't hint Bean and Pearl as foolish

    # Use the settings to determine non-progression Major Items
    # majorItems = [item for item in majorItems if item not in foolishItems]
    majorItems = ItemPool.AllKongMoves()
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        majorItems.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.shockwave_status != ShockwaveStatus.shuffled_decoupled:
        majorItems.append(Items.CameraAndShockwave)
    if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
        majorItems.append(Items.Shockwave)
        majorItems.append(Items.Camera)
    majorItems.extend(ItemPool.Keys())
    majorItems.extend(ItemPool.Kongs(spoiler.settings))
    requires_rareware = spoiler.settings.coin_door_item == HelmDoorItem.vanilla
    requires_nintendo = spoiler.settings.coin_door_item == HelmDoorItem.vanilla
    requires_crowns = spoiler.settings.crown_door_item in (HelmDoorItem.vanilla, HelmDoorItem.req_crown) or spoiler.settings.coin_door_item == HelmDoorItem.req_crown
    for x in (spoiler.settings.crown_door_item, spoiler.settings.coin_door_item):
        if x == HelmDoorItem.req_companycoins:
            requires_rareware = True
            requires_nintendo = True

    if Types.Coin in spoiler.settings.shuffled_location_types and requires_rareware:
        majorItems.append(Items.RarewareCoin)
    if Types.Coin in spoiler.settings.shuffled_location_types and requires_nintendo:
        majorItems.append(Items.NintendoCoin)
    if Types.Blueprint in spoiler.settings.shuffled_location_types and (
        spoiler.settings.win_condition == WinCondition.all_blueprints or spoiler.settings.coin_door_item == HelmDoorItem.req_bp or spoiler.settings.crown_door_item == HelmDoorItem.req_bp
    ):
        majorItems.extend(ItemPool.Blueprints())
    if Types.Medal in spoiler.settings.shuffled_location_types and (
        spoiler.settings.win_condition == WinCondition.all_medals or spoiler.settings.coin_door_item == HelmDoorItem.req_medal or spoiler.settings.crown_door_item == HelmDoorItem.req_medal
    ):
        majorItems.append(Items.BananaMedal)
    if Types.Fairy in spoiler.settings.shuffled_location_types and (
        spoiler.settings.win_condition == WinCondition.all_fairies or spoiler.settings.coin_door_item == HelmDoorItem.req_fairy or spoiler.settings.crown_door_item == HelmDoorItem.req_fairy
    ):
        majorItems.append(Items.BananaFairy)
    if Types.Crown in spoiler.settings.shuffled_location_types and requires_crowns:
        majorItems.append(Items.BattleCrown)
    if Types.Pearl in spoiler.settings.shuffled_location_types and (spoiler.settings.coin_door_item == HelmDoorItem.req_pearl or spoiler.settings.crown_door_item == HelmDoorItem.req_pearl):
        majorItems.append(Items.Pearl)
    if Types.Bean in spoiler.settings.shuffled_location_types and (spoiler.settings.coin_door_item == HelmDoorItem.req_bean or spoiler.settings.crown_door_item == HelmDoorItem.req_bean):
        majorItems.append(Items.Bean)
    if Types.RainbowCoin in spoiler.settings.shuffled_location_types and (
        spoiler.settings.coin_door_item == HelmDoorItem.req_rainbowcoin or spoiler.settings.crown_door_item == HelmDoorItem.req_rainbowcoin
    ):
        majorItems.append(Items.RainbowCoin)
    # The contents of some locations can make entire classes of items not foolish
    # Loop through these locations until no new items are added to the list of major items
    newFoolishItems = True
    while newFoolishItems:
        newFoolishItems = False
        if Types.Medal in spoiler.settings.shuffled_location_types and LocationList[Locations.RarewareCoin].item in majorItems and Items.BananaMedal not in majorItems:
            majorItems.append(Items.BananaMedal)
            newFoolishItems = True
        if Types.Fairy in spoiler.settings.shuffled_location_types and LocationList[Locations.RarewareBanana].item in majorItems and Items.BananaFairy not in majorItems:
            majorItems.append(Items.BananaFairy)
            newFoolishItems = True
        if Types.Pearl in spoiler.settings.shuffled_location_types and LocationList[Locations.GalleonTinyPearls].item in majorItems and Items.Pearl not in majorItems:
            majorItems.append(Items.Pearl)
            newFoolishItems = True
        if Types.Bean in spoiler.settings.shuffled_location_types and LocationList[Locations.ForestTinyBeanstalk].item in majorItems and Items.Bean not in majorItems:
            majorItems.append(Items.Bean)
            newFoolishItems = True

    nonHintableNames = {"K. Rool Arena", "Snide", "Candy Generic", "Funky Generic", "Credits"}  # These regions never have anything useful so shouldn't be hinted
    if Types.Coin not in spoiler.settings.shuffled_location_types:
        nonHintableNames.add("Jetpac Game")  # If this is vanilla, it's never useful to hint
    bossLocations = [location for id, location in LocationList.items() if location.type == Types.Key]
    # In order for a region to be foolish, it can contain none of these Major Items
    for id, region in RegionList.items():
        locations = [loc for loc in region.locations if loc.id in LocationList.keys()]
        # If this region DOES contain a major item, add it the name to the set of non-hintable hint regions
        if any([loc for loc in locations if LocationList[loc.id].item in majorItems]):
            nonHintableNames.add(region.hint_name)
        # In addition to being empty, medal regions need the corresponding boss location to be empty to be hinted foolish - this lets us say "CBs are foolish" which is more helpful
        elif "Medal Rewards" in region.hint_name:
            bossLocation = [location for location in bossLocations if location.level == region.level][0]  # Matches only one
            if bossLocation.item in majorItems:
                nonHintableNames.add(region.hint_name)
    # The regions that are foolish are all regions not in this list (that have locations in them!)
    spoiler.foolish_region_names = list(set([region.hint_name for id, region in RegionList.items() if any(region.locations) and region.hint_name not in nonHintableNames]))


def RandomFill(settings, itemsToPlace, inOrder=False):
    """Randomly place given items in any location disregarding logic."""
    if not inOrder:
        shuffle(itemsToPlace)
    # Get all remaining empty locations
    empty = []
    for id, location in LocationList.items():
        if location.item is None:
            empty.append(id)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        item = itemsToPlace.pop()
        validLocations = settings.GetValidLocationsForItem(item)
        itemEmpty = [x for x in empty if x in validLocations and LocationList[x].item is None and not LocationList[x].inaccessible]
        if len(itemEmpty) == 0:
            # invalid_empty_reachable = [x for x in itemEmpty if x not in validLocations]
            # empty_locations = [x for x in LocationList.values() if x.item is None]
            # noitem_locations = [x for x in LocationList.values() if x.type != Types.Shop and x.item is Items.NoItem]
            return len(itemsToPlace)
        shuffle(itemEmpty)
        locationId = itemEmpty.pop()
        LocationList[locationId].PlaceItem(item)
        empty.remove(locationId)
    return 0


def ForwardFill(settings, itemsToPlace, ownedItems=None, inOrder=False, doubleTime=False):
    """Forward fill algorithm for item placement."""
    if ownedItems is None:
        ownedItems = []
    if not inOrder:
        shuffle(itemsToPlace)
    ownedItems = ownedItems.copy()
    needToRefreshReachable = True
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Get a random item
        item = itemsToPlace.pop(0)
        # In "doubleTime", only refresh the list of reachable locations every other item to reduce calls to this method - this should have minimal impact on randomization depending on the item filling here
        if not doubleTime or needToRefreshReachable:
            # Find a random empty location which is reachable with current items
            Reset()
            reachable = GetAccessibleLocations(settings, ownedItems.copy(), SearchMode.GetReachableForFilling)
        validLocations = settings.GetValidLocationsForItem(item)
        validReachable = [x for x in reachable if LocationList[x].item is None and x in validLocations]
        if len(validReachable) == 0:  # If there are no empty reachable locations, reached a dead end
            # invalid_empty_reachable = [x for x in reachable if LocationList[x].item is None and x not in validLocations]
            # valid_empty = [x for x in LocationList.keys() if LocationList[x].item is None and x in validLocations]
            return len(itemsToPlace)
        shuffle(validReachable)
        locationId = validReachable.pop()
        # Place the item
        ownedItems.append(item)
        LocationList[locationId].PlaceItem(item)
        # Debug code utility for very important items
        if item in ItemPool.HighPriorityItems(settings):
            settings.debug_fill[locationId] = item
        if item in ItemPool.Keys():
            settings.debug_fill[locationId] = item
        needToRefreshReachable = not needToRefreshReachable  # Alternate this variable every item for doubleTime
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
        reachable = GetAccessibleLocations(settings, owned, SearchMode.GetReachableForFilling)
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
        # Get a random, empty, reachable location
        for locationId in validReachable:
            # Atempt to place the item here
            LocationList[locationId].PlaceItem(item)
            if len(itemsToPlace) > 0:
                # If we have more items to placed, check valid reachable after placing to see if placing it here causes problems
                # Need to re-assign owned items since the search adds a bunch of extras
                owned = itemsToPlace.copy()
                owned.extend(ownedItems)
                Reset()
                reachable = GetAccessibleLocations(settings, owned, SearchMode.GetReachableForFilling)
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
                    LocationList[locationId].UnplaceItem()
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
        elif settings.random_prices == RandomPrices.vanilla:
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
    settingsRequiredMoves = ItemPool.AllItemsForMovePlacement(spoiler.settings)
    # The most likely case - if no moves are needed, get out of here quickly
    Reset()
    if GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
        return []
    requiredMoves = []
    # Some locations can be accessed by multiple items, so we'll shuffle the order we check the items to randomly pick one of them first
    # We should have just placed this item, so it should be available with the provided list of owned kongs
    # We don't want to find requirements for Kongs we don't own, as we shouldn't need them
    #   e.g. You own DK, Diddy, and Tiny but want to find the prerequisites for an item found in the Llama temple
    #     You intentionally only look at DK/Diddy/Tiny moves so you don't find Grape as a prerequisite because you don't have Lanky
    #     In this example (with no other shuffles), there are two possible return values depending on the shuffle order.
    #     Either [Items.Guitar, Items.Coconut] OR [Items.Guitar, Items.Feather]
    moveList = [move for move in ItemPool.AllKongMoves()]  # I really want to pare this down quickly with ownedKongs, but it hurts the fill to do so
    # Sometimes a move requires camera or shockwave as a prerequisite
    if spoiler.settings.shockwave_status != ShockwaveStatus.vanilla:
        if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
            moveList.append(Items.Camera)
            moveList.append(Items.Shockwave)
        else:
            moveList.append(Items.CameraAndShockwave)
    # Often moves require training barrels as prerequisites
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        moveList.extend(ItemPool.TrainingBarrelAbilities())
    # We only want *unplaced* prerequisites, cull all placed moves from the move list
    for move in placedMoves:
        if move in moveList:
            moveList.remove(move)
    shuffle(moveList)
    itemWasFound = False
    # Every item in moveList could be a required item
    for i in range(0, len(moveList)):
        # Remove one item from the moveList
        possiblyUnnecessaryItem = moveList[i]
        moveList[i] = Items.NoItem
        # Check if the target is still accessible without this item
        Reset()
        if not GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy() + moveList.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
            # If it's no longer accessible, then this item is required
            requiredMoves.append(possiblyUnnecessaryItem)
            # Restore the item to the move list ONLY if it's required - this will cover either/or items
            moveList[i] = possiblyUnnecessaryItem
        else:
            itemWasFound = True
    # If we didn't find a required move, the item was placed improperly somehow (this shouldn't happen)
    if not itemWasFound:
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
        # debug_reachable = GetAccessibleLocations(spoiler.settings, settingsRequiredMoves.copy() + moveList.copy(), SearchMode.GetReachable)
        print("Item placed in an inaccessible location: " + str(mysteryLocation.name))
        raise Ex.ItemPlacementException("Item placed in an inaccessible location: " + str(mysteryLocation.name))

    spoiler.settings.debug_prerequisites[targetItemId] = requiredMoves
    return requiredMoves


def PlaceItems(settings, algorithm, itemsToPlace, ownedItems=None, inOrder=False, doubleTime=False):
    """Places items using given algorithm."""
    if ownedItems is None:
        ownedItems = []
    # Always use random fill with no logic
    if settings.logic_type == LogicType.nologic:
        algorithm = FillAlgorithm.random
    if algorithm == FillAlgorithm.assumed:
        return AssumedFill(settings, itemsToPlace, ownedItems, inOrder)
    elif algorithm == FillAlgorithm.forward:
        return ForwardFill(settings, itemsToPlace, ownedItems, inOrder, doubleTime)
    elif algorithm == FillAlgorithm.random:
        return RandomFill(settings, itemsToPlace, inOrder)


def FillShuffledKeys(spoiler, placed_types):
    """Fill Keys in shuffled locations based on the settings."""
    keysToPlace = []
    for keyEvent in spoiler.settings.krool_keys_required:
        if keyEvent == Events.JapesKeyTurnedIn:
            keysToPlace.append(Items.JungleJapesKey)
        elif keyEvent == Events.AztecKeyTurnedIn:
            keysToPlace.append(Items.AngryAztecKey)
        elif keyEvent == Events.FactoryKeyTurnedIn:
            keysToPlace.append(Items.FranticFactoryKey)
        elif keyEvent == Events.GalleonKeyTurnedIn:
            keysToPlace.append(Items.GloomyGalleonKey)
        elif keyEvent == Events.ForestKeyTurnedIn:
            keysToPlace.append(Items.FungiForestKey)
        elif keyEvent == Events.CavesKeyTurnedIn:
            keysToPlace.append(Items.CrystalCavesKey)
        elif keyEvent == Events.CastleKeyTurnedIn:
            keysToPlace.append(Items.CreepyCastleKey)
        elif keyEvent == Events.HelmKeyTurnedIn:
            keysToPlace.append(Items.HideoutHelmKey)
    if spoiler.settings.key_8_helm and Items.HideoutHelmKey in keysToPlace:
        keysToPlace.remove(Items.HideoutHelmKey)
    # Level-agnostic key placement settings include...
    # - No logic (totally random)
    # - Loading Zone randomizer (key unlocks are typically of lesser importance)
    # - Complex level progression (key order is non-linear)
    if spoiler.settings.logic_type == LogicType.nologic or spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all or spoiler.settings.hard_level_progression:
        # Assumed fills tend to place multiple keys at once better
        keyAlgorithm = FillAlgorithm.assumed
        if spoiler.settings.logic_type == LogicType.nologic:  # Obviously no logic gets random fills
            keyAlgorithm = FillAlgorithm.random
        # Place all the keys
        keysUnplaced = PlaceItems(spoiler.settings, keyAlgorithm, keysToPlace, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types))
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")
    # # Simple linear level order progression leads to straightforward key placement
    else:
        # Place the keys in order
        keysToPlace.sort()
        keysUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, keysToPlace, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types), inOrder=True)
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")


def Fill(spoiler):
    """Fully randomizes and places all items."""
    placed_types = []
    spoiler.settings.debug_fill = {}
    spoiler.settings.debug_prerequisites = {}
    spoiler.settings.debug_fill_blueprints = {}
    # First place constant items - these will never vary and need to be in place for all other fills to know that
    ItemPool.PlaceConstants(spoiler.settings)

    # Place rainbow coins before all randomly placed items so that we have coins set in stone for the other fills
    # It's possible that shops could overload if we continue assuming rainbow coins for too many fills
    if Types.RainbowCoin in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.RainbowCoin)
        Reset()
        rcoinUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.RainbowCoinItems(), ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types))
        if rcoinUnplaced > 0:
            raise Ex.ItemPlacementException(str(rcoinUnplaced) + " unplaced Rainbow Coins.")

    # Then fill Kongs and Moves - this should be a very early fill type for hopefully obvious reasons
    FillKongsAndMoves(spoiler, placed_types)

    # Then place Blueprints - these are moderately restrictive in their placement
    if Types.Blueprint in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Blueprint)
        Reset()
        # Blueprints can be placed randomly - there's no location (yet) that can cause blueprints to lock themselves
        blueprintsUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.Blueprints().copy(), ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types))
        if blueprintsUnplaced > 0:
            raise Ex.ItemPlacementException(str(blueprintsUnplaced) + " unplaced blueprints.")
    # Then place keys
    if Types.Key in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Key)
        FillShuffledKeys(spoiler, placed_types)
    # Then place Nintendo & Rareware Coins
    if Types.Coin in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Coin)
        Reset()
        coinsUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.CompanyCoinItems(), ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types), doubleTime=True)
        if coinsUnplaced > 0:
            raise Ex.ItemPlacementException(str(coinsUnplaced) + " unplaced company coins.")
    # Then place Battle Crowns
    if Types.Crown in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Crown)
        Reset()
        # Crowns can be placed randomly, but only if the helm doors don't need any
        algo = FillAlgorithm.random
        if spoiler.settings.coin_door_item == HelmDoorItem.req_crown or spoiler.settings.crown_door_item in (HelmDoorItem.vanilla, HelmDoorItem.req_crown):
            algo = spoiler.settings.algorithm
        crownsUnplaced = PlaceItems(spoiler.settings, algo, ItemPool.BattleCrownItems(), ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types), doubleTime=True)
        if crownsUnplaced > 0:
            raise Ex.ItemPlacementException(str(crownsUnplaced) + " unplaced crowns.")
    # Then place Banana Medals
    if Types.Medal in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Medal)
        Reset()
        medalsToBePlaced = ItemPool.BananaMedalItems()
        medalAssumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types)
        # Medals up to the Jetpac requirement must be placed carefully
        logicallyPlacedMedals = min(floor(spoiler.settings.medal_requirement * 1.2), 40)
        jetpacRequiredMedals = medalsToBePlaced[:logicallyPlacedMedals]
        medalsUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, jetpacRequiredMedals, medalAssumedItems, doubleTime=True)
        if logicallyPlacedMedals > 0 and medalsUnplaced > 0:
            raise Ex.ItemPlacementException(str(medalsUnplaced) + " unplaced logical medals.")
        # The remaining medals can be placed randomly
        medalsUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, medalsToBePlaced[logicallyPlacedMedals:], medalAssumedItems)
        if logicallyPlacedMedals < 40 and medalsUnplaced > 0:
            raise Ex.ItemPlacementException(str(medalsUnplaced) + " unplaced random medals.")
    # Then place Fairies
    if Types.Fairy in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Fairy)
        Reset()
        fairiesToBePlaced = ItemPool.FairyItems()
        fairyAssumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types)
        # Fairies up to the Rareware GB requirement must be placed carefully
        logicallyPlacedFairies = min(floor(spoiler.settings.rareware_gb_fairies * 1.2), 20)  # Place more fairies in logic than you may need
        rarewareRequiredFairies = fairiesToBePlaced[:logicallyPlacedFairies]
        fairyUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, rarewareRequiredFairies, fairyAssumedItems, doubleTime=True)
        if logicallyPlacedFairies > 0 and fairyUnplaced > 0:
            raise Ex.ItemPlacementException(str(fairyUnplaced) + " unplaced logical fairies.")
        # The remaining fairies can be placed randomly
        fairyUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, fairiesToBePlaced[logicallyPlacedFairies:], fairyAssumedItems)
        if logicallyPlacedFairies < 20 and fairyUnplaced > 0:
            raise Ex.ItemPlacementException(str(fairyUnplaced) + " unplaced random Fairies.")
    # Then place misc progression items
    if Types.Bean in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Bean)
        placed_types.append(Types.Pearl)
        Reset()
        miscUnplaced = PlaceItems(spoiler.settings, spoiler.settings.algorithm, ItemPool.MiscItemRandoItems(), ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types))
        if miscUnplaced > 0:
            raise Ex.ItemPlacementException(str(miscUnplaced) + " unplaced Miscellaneous Items.")
    # Then fill remaining locations with GBs
    if Types.Banana in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Banana)
        Reset()
        gbsUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.GoldenBananaItems(), [])
        if gbsUnplaced > 0:
            raise Ex.ItemPlacementException(str(gbsUnplaced) + " unplaced GBs.")
    if Types.ToughBanana in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.ToughBanana)
        Reset()
        gbsUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.ToughGoldenBananaItems(), [])
        if gbsUnplaced > 0:
            raise Ex.ItemPlacementException(str(gbsUnplaced) + " unplaced tough GBs.")
    # Fill in fake items
    if Types.FakeItem in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.FakeItem)
        Reset()
        fakeUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.FakeItems(), [])
        # Don't raise exception if unplaced fake items
    # Fill in junk items
    if Types.JunkItem in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.JunkItem)
        Reset()
        junkUnplaced = PlaceItems(spoiler.settings, FillAlgorithm.random, ItemPool.JunkItems(), [])
        # Don't raise exception if unplaced junk items

    # Some locations require special care to make logic work correctly
    # This is the only location that cares about None vs NoItem - it needs to be None so it fills correctly but NoItem for logic to generate progression correctly
    if LocationList[Locations.JapesDonkeyFreeDiddy].item is None:
        LocationList[Locations.JapesDonkeyFreeDiddy].PlaceItem(Items.NoItem)
    # Finally, check if game is beatable
    Reset()
    if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckAllReachable):
        print("Failed 101% check")
        raise Ex.GameNotBeatableException("Game not able to complete 101% after placing all items.")
    return


def ShuffleSharedMoves(spoiler, placedMoves, placedTypes):
    """Shuffles shared kong moves into shops and then returns the remaining ones and their valid locations."""
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
    if spoiler.settings.training_barrels != TrainingBarrels.normal and Items.Oranges not in placedMoves:
        # First place training moves that are not placed. By this point, only Oranges need to be placed here as the others are important to place even earlier than this
        trainingMovesUnplaced = PlaceItems(
            spoiler.settings, FillAlgorithm.assumed, [Items.Oranges], [x for x in ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes) if x != Items.Oranges and x not in placedMoves]
        )
        if trainingMovesUnplaced > 0:
            raise Ex.ItemPlacementException("Failed to place Orange training barrel move.")
        placedMoves.append(Items.Oranges)
    importantSharedToPlace = ItemPool.ImportantSharedMoves.copy()
    # Next place any fairy moves that need placing, settings dependent
    if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled and Items.CameraAndShockwave not in placedMoves:
        importantSharedToPlace.append(Items.CameraAndShockwave)
    elif spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled and (Items.Camera not in placedMoves or Items.Shockwave not in placedMoves):
        importantSharedToPlace.append(Items.Camera)
        importantSharedToPlace.append(Items.Shockwave)
    for item in placedMoves:
        if item in importantSharedToPlace:
            importantSharedToPlace.remove(item)
    importantSharedUnplaced = PlaceItems(
        spoiler.settings,
        FillAlgorithm.assumed,
        importantSharedToPlace,
        [x for x in ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes) if x not in importantSharedToPlace and x not in placedMoves],
    )
    if importantSharedUnplaced > 0:
        raise Ex.ItemPlacementException(str(importantSharedUnplaced) + " unplaced shared important items.")
    junkSharedToPlace = ItemPool.JunkSharedMoves.copy()
    for item in placedMoves:
        if item in junkSharedToPlace:
            junkSharedToPlace.remove(item)
    junkSharedUnplaced = PlaceItems(
        spoiler.settings, FillAlgorithm.random, junkSharedToPlace, [x for x in ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes) if x not in junkSharedToPlace]
    )
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
                # TODO: Handle Loading Zones - does not work right now but is something I want here eventually
                # if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
                #     ShuffleExits.Reset()
                #     ShuffleExits.ExitShuffle(spoiler.settings)
                #     spoiler.UpdateExits()
                spoiler.settings.shuffle_prices()
                if spoiler.settings.random_starting_region:
                    spoiler.settings.RandomizeStartingLocation()
            else:
                js.postMessage("Retrying fill. Tries: " + str(retries))
            Reset()
            Logic.ClearAllLocations()


def GeneratePlaythrough(spoiler):
    """Generate playthrough and way of the hoard and update spoiler."""
    js.postMessage("Seed generated! Finalizing spoiler...")
    LogicVariables.assumeFillSuccess = True  # Now that we know the seed is valid, we can assume fill success for the sake of generating the playthrough and WotH
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
            and (Kongs.diddy in ownedKongs or spoiler.settings.open_levels or (Kongs.donkey in ownedKongs and spoiler.settings.activate_all_bananaports == ActivateAllBananaports.all))
            and (Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs)
        ):  # Must be able to open Llama Temple
            logicallyAccessibleKongLocations.append(Locations.LankyKong)
    return logicallyAccessibleKongLocations


def PlacePriorityItems(spoiler, itemsToPlace, beforePlacedItems, placedTypes, levelBlock=None):
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
    allOtherItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes)
    if Types.Key in spoiler.settings.shuffled_location_types:
        # However we don't want all keys - don't assume keys for or beyond the latest logically allowed level's key
        for key in bannedKeys:
            allOtherItems.remove(key)
    # Other exceptions: we don't assume we have the items to be placed, as then they could lock themselves
    for item in priorityItemsToPlace:
        allOtherItems.remove(item)
    # We also don't assume we have any placed items. If these unlock locations we should find them as we go.
    # This should prevent circular logic (e.g. the diddy-unlocking-gun being locked behind guitar which is already priority placed in Japes Cranky)
    for item in placedItems:
        if item in allOtherItems:
            allOtherItems.remove(item)
    # At last, place all the items
    failedToPlace = PlaceItems(spoiler.settings, FillAlgorithm.assumed, priorityItemsToPlace.copy(), ownedItems=allOtherItems)
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
    priorityItemsToPlace.extend(PlacePriorityItems(spoiler, unplacedDependencies, placedItems, placedTypes, levelBlock))
    return priorityItemsToPlace


def PlaceKongsInKongLocations(spoiler, kongItems, kongLocations):
    """For these settings, Kongs to place, and locations to place them in, place the Kongs in such a way the generation will never error here."""
    ownedKongs = [kong for kong in spoiler.settings.starting_kong_list]
    # In entrance randomizer, it's too complicated to quickly determine kong accessibility.
    # Instead, we place Kongs in a specific order to guarantee we'll at least have an eligible freer.
    # To be at least somewhat nice to no logic users, we also use this section here so kongs don't lock each other.
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all or spoiler.settings.logic_type == LogicType.nologic:
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
    elif spoiler.settings.shuffle_loading_zones in (ShuffleLoadingZones.levels, ShuffleLoadingZones.none):
        latestLogicallyAllowedLevel = len(ownedKongs) + 1
        # Logically we can always enter any level on hard level progression
        if spoiler.settings.hard_level_progression:
            latestLogicallyAllowedLevel = 7
        logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
        while len(ownedKongs) != 5:
            # If there aren't any accessible Kong locations, then the level order shuffler has a bug (this shouldn't happen)
            if not any(logicallyAccessibleKongLocations):
                raise Ex.EntrancePlacementException("Levels shuffled in a way that makes Kong unlocks impossible. SEND THIS TO THE DEVS!")
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
                        raise Ex.FillException("Kongs placed in a way that is impossible to unlock everyone. SEND THIS TO THE DEVS!")
                    # Pick a random Kong from the Kongs that guarantee progression
                    kongToBeFreed = choice(progressionKongItems)
            # Now that we have a combination guaranteed to not break the seed or logic, lock it in
            LocationList[progressionLocation].PlaceItem(kongToBeFreed)
            spoiler.settings.debug_fill[progressionLocation] = kongToBeFreed
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


def FillKongs(spoiler, placedTypes):
    """Place Kongs in valid locations."""
    placedTypes.append(Types.Kong)
    # Determine what kong items need to be placed
    startingKongItems = [ItemPool.ItemFromKong(kong) for kong in spoiler.settings.starting_kong_list]
    kongItems = [item for item in ItemPool.Kongs(spoiler.settings) if item not in startingKongItems]
    # If Kongs can be placed anywhere, we don't need anything special
    if spoiler.settings.shuffle_items and Types.Kong in spoiler.settings.shuffled_location_types:
        # First, randomly pick who opens what cage - this prevents cases where a Kong locks themselves
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
        assumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes)
        Reset()
        PlaceItems(spoiler.settings, FillAlgorithm.assumed, kongItems, assumedItems)
        # If we didn't put an item in a kong location, then it gets a NoItem
        # This matters specifically so the logic around items inside Kong cages (VERY important for Diddy's cage) behaves properly
        if LocationList[Locations.DiddyKong].item is None:
            LocationList[Locations.DiddyKong].PlaceItem(Items.NoItem)
        else:
            LocationList[Locations.DiddyKong].kong = spoiler.settings.diddy_freeing_kong  # If any Kong cage DOES have a kong, update the location's assigned Kong
        if LocationList[Locations.TinyKong].item is None:
            LocationList[Locations.TinyKong].PlaceItem(Items.NoItem)
        else:
            LocationList[Locations.TinyKong].kong = spoiler.settings.tiny_freeing_kong
        if LocationList[Locations.LankyKong].item is None:
            LocationList[Locations.LankyKong].PlaceItem(Items.NoItem)
        else:
            LocationList[Locations.LankyKong].kong = spoiler.settings.lanky_freeing_kong
        if LocationList[Locations.ChunkyKong].item is None:
            LocationList[Locations.ChunkyKong].PlaceItem(Items.NoItem)
        else:
            LocationList[Locations.ChunkyKong].kong = spoiler.settings.chunky_freeing_kong
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


def FillKongsAndMoves(spoiler, placedTypes):
    """Fill kongs, then progression moves, then shared moves, then rest of moves."""
    itemsToPlace = []

    # Handle kong rando first so we know what moves are most important to place
    if spoiler.settings.kong_rando:
        FillKongs(spoiler, placedTypes)
    preplacedPriorityMoves = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]  # Kongs are now placed, either in the above method or by default

    # First place our starting moves randomly
    startingMoves = []
    locationsNeedingMoves = []
    # We can expect that all locations in this region are starting move locations or Training Barrels
    for locationLogic in RegionList[Regions.GameStart].locations:
        location = LocationList[locationLogic.id]
        if location.item is None and not location.inaccessible:
            locationsNeedingMoves.append(locationLogic.id)
        elif location.item not in (None, Items.NoItem):
            startingMoves.append(location.item)
    # Fill the empty starting locations
    if any(locationsNeedingMoves):
        newlyPlacedItems = []
        toBeUnplaced = []
        possibleStartingMoves = ItemPool.AllKongMoves().copy()
        if len(locationsNeedingMoves) < 10:
            # Generally only include one copy of the useless progressive moves to bias against picking them when you only have a few starting moves
            possibleStartingMoves.append(Items.ProgressiveAmmoBelt)
            possibleStartingMoves.append(Items.ProgressiveInstrumentUpgrade)
        else:
            # If we have lots of starting moves, we'll need to include all copies so we have enough stuff to fill all locations
            possibleStartingMoves.extend(ItemPool.JunkSharedMoves)
        if spoiler.settings.training_barrels == TrainingBarrels.shuffled:
            possibleStartingMoves.extend(ItemPool.TrainingBarrelAbilities())
        if spoiler.settings.shockwave_status in (ShockwaveStatus.shuffled, ShockwaveStatus.shuffled_decoupled):
            possibleStartingMoves.extend(ItemPool.ShockwaveTypeItems(spoiler.settings))
        shuffle(possibleStartingMoves)
        # For each location needing a move, put in a random valid move
        for locationId in locationsNeedingMoves:
            startingMove = possibleStartingMoves.pop()
            # If we picked a move to place that we already placed, we have to go Unplace it later
            if startingMove in preplacedPriorityMoves:
                toBeUnplaced.append(startingMove)
            # Else it's a newly placed move, note it down as being placed
            else:
                newlyPlacedItems.append(startingMove)
            LocationList[locationId].PlaceItem(startingMove)
            # Helpful debug code to keep track of where all major items are placed - do not rely on this variable anywhere
            if locationId in spoiler.settings.debug_fill.keys():
                del spoiler.settings.debug_fill[locationId]
            spoiler.settings.debug_fill[locationId] = startingMove
        # For any move that we've now placed twice, Unplace it from the non-starting-move location
        if any(toBeUnplaced):
            for location in LocationList.values():
                if location.item in (toBeUnplaced) and location.type not in (Types.TrainingBarrel, Types.PreGivenMove):
                    toBeUnplaced.remove(location.item)
                    location.UnplaceItem()
        # Compile all the moves we now know are placed
        preplacedPriorityMoves.extend(newlyPlacedItems)

    levelBlockInPlace = False
    # Once Kongs are placed, the top priority is placing training barrel moves first. These (mostly) need to be very early because they block access to whole levels.
    if spoiler.settings.move_rando != MoveRando.off and spoiler.settings.training_barrels == TrainingBarrels.shuffled:
        # First place barrels - needed for most bosses
        if Items.Barrels not in preplacedPriorityMoves:
            itemsPlacedForBarrels = PlacePriorityItems(spoiler, [Items.Barrels], preplacedPriorityMoves, placedTypes)  # , levelBlock=needBarrelsByThisLevel)
            preplacedPriorityMoves.extend(itemsPlacedForBarrels)
        # Next place vines - needed to beat Aztec and maybe get to upper DK Isle
        if Items.Vines not in preplacedPriorityMoves:
            itemsPlacedForVines = PlacePriorityItems(spoiler, [Items.Vines], preplacedPriorityMoves, placedTypes)  # , levelBlock=needVinesByThisLevel)
            preplacedPriorityMoves.extend(itemsPlacedForVines)
        # Next place swim - needed to get into level 4
        if Items.Swim not in preplacedPriorityMoves:
            itemsPlacedForSwim = PlacePriorityItems(spoiler, [Items.Swim], preplacedPriorityMoves, placedTypes)  # , levelBlock=needSwimByThisLevel)
            preplacedPriorityMoves.extend(itemsPlacedForSwim)
    # If we had to put in a level block, undo it now - only settings that need progression fixed later will do this so this is fine
    if levelBlockInPlace:
        BlockAccessToLevel(spoiler.settings, 100)

    if spoiler.settings.kong_rando:
        # If kongs are our progression, then place moves that unlock those kongs before anything else
        # This logic only matters if the level order is critical to progression (i.e. not loading zone shuffled)
        if spoiler.settings.kongs_for_progression and spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all and spoiler.settings.starting_moves_count < 10:
            lockedKongs = [kong for kong in GetKongs() if kong not in spoiler.settings.starting_kong_list]
            for kong in lockedKongs:
                # We need the item representation of the kong
                kongItem = ItemPool.ItemFromKong(kong)
                # To save some cost on the coming method, we know none of the locked kong's moves can be prerequisites
                otherKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
                otherKongs.remove(kong)
                # Get the unplaced prerequisites to this Kong's location - this could indirectly include other Kongs' locations
                directPrerequisiteMoves = GetUnplacedItemPrerequisites(spoiler, kongItem, preplacedPriorityMoves, otherKongs)
                newlyPlacedItems = PlacePriorityItems(spoiler, directPrerequisiteMoves, preplacedPriorityMoves, placedTypes)
                preplacedPriorityMoves.extend(newlyPlacedItems)

    # Handle shared moves before other moves in move rando
    if spoiler.settings.move_rando != MoveRando.off:
        # Shuffle the shared move locations since they must be done first
        ShuffleSharedMoves(spoiler, preplacedPriorityMoves.copy(), placedTypes)
        # Set up remaining kong moves to be shuffled
        itemsToPlace.extend(ItemPool.DonkeyMoves)
        itemsToPlace.extend(ItemPool.DiddyMoves)
        itemsToPlace.extend(ItemPool.LankyMoves)
        itemsToPlace.extend(ItemPool.TinyMoves)
        itemsToPlace.extend(ItemPool.ChunkyMoves)

    # Handle remaining moves/items
    placedTypes.append(Types.Shop)
    placedTypes.append(Types.TrainingBarrel)
    placedTypes.append(Types.Shockwave)
    Reset()
    itemsToPlace = [item for item in itemsToPlace if item not in preplacedPriorityMoves]
    unplaced = PlaceItems(spoiler.settings, FillAlgorithm.assumed, itemsToPlace, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes))
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
            # After setting B. Lockers and bosses, make sure the game is still 101%-able
            Reset()
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckAllReachable):
                print("Failed post-progression 101% check?")
                raise Ex.GameNotBeatableException("Game not able to complete 101% after setting progression.")
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
            # Every 5th fill, retry more aggressively by reshuffling level order, move prices, and starting location as applicable
            if retries % 5 == 0:
                js.postMessage("Retrying fill really hard. Tries: " + str(retries))
                spoiler.settings.shuffle_prices()
                if spoiler.settings.random_starting_region:
                    spoiler.settings.RandomizeStartingLocation()
                if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
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
        settings.boss_maps[i] = Maps.CastleBoss  # This requires nothing, allowing the fill to proceed as normal
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
    # Get sphere 0 GB count
    BlockAccessToLevel(settings, 0)
    Reset()
    accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
    goldenBananaTotals.append(LogicVariables.GoldenBananas)
    # For each level, calculate the available moves and number of bananas
    for level in range(1, 8):
        thisLevel = GetLevelShuffledToIndex(level - 1)
        # Block access to future levels
        BlockAccessToLevel(settings, level + 1)
        settings.BossBananas[thisLevel] = 1000  # also block this level's boss
        # Set up the logic variables with the available locations and items
        Reset()
        accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
        # Save the available counts for this level
        coloredBananaCounts.append(LogicVariables.ColoredBananas[thisLevel])
        goldenBananaTotals.append(LogicVariables.GoldenBananas)
        ownedKongs[thisLevel] = LogicVariables.GetKongs()
        accessibleMoves = [
            LocationList[x].item
            for x in accessible
            if LocationList[x].item != Items.NoItem and LocationList[x].item is not None and ItemList[LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
        ]
        ownedMoves[thisLevel] = accessibleMoves
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
    if settings.troff_max > 0:
        settings.BossBananas = [
            min(settings.troff_0, sum(coloredBananaCounts[0]), round(settings.troff_0 / (settings.troff_max * settings.troff_weight_0) * sum(coloredBananaCounts[0]))),
            min(settings.troff_1, sum(coloredBananaCounts[1]), round(settings.troff_1 / (settings.troff_max * settings.troff_weight_1) * sum(coloredBananaCounts[1]))),
            min(settings.troff_2, sum(coloredBananaCounts[2]), round(settings.troff_2 / (settings.troff_max * settings.troff_weight_2) * sum(coloredBananaCounts[2]))),
            min(settings.troff_3, sum(coloredBananaCounts[3]), round(settings.troff_3 / (settings.troff_max * settings.troff_weight_3) * sum(coloredBananaCounts[3]))),
            min(settings.troff_4, sum(coloredBananaCounts[4]), round(settings.troff_4 / (settings.troff_max * settings.troff_weight_4) * sum(coloredBananaCounts[4]))),
            min(settings.troff_5, sum(coloredBananaCounts[5]), round(settings.troff_5 / (settings.troff_max * settings.troff_weight_5) * sum(coloredBananaCounts[5]))),
            min(settings.troff_6, sum(coloredBananaCounts[6]), round(settings.troff_6 / (settings.troff_max * settings.troff_weight_6) * sum(coloredBananaCounts[6]))),
        ]
    else:
        settings.BossBananas = [0, 0, 0, 0, 0, 0, 0]
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
    accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
    runningGBTotal = LogicVariables.GoldenBananas
    minimumBLockerGBs = 0

    # Reset B. Lockers and T&S to initial values
    settings.EntryGBs = [settings.blocker_0, settings.blocker_1, settings.blocker_2, settings.blocker_3, settings.blocker_4, settings.blocker_5, settings.blocker_6, settings.blocker_7]
    settings.BossBananas = [settings.troff_0, settings.troff_1, settings.troff_2, settings.troff_3, settings.troff_4, settings.troff_5, settings.troff_6]
    if settings.randomize_blocker_required_amounts:  # If amounts are random, they need to be maxed out to properly generate random values
        settings.EntryGBs = [1000, 1000, 1000, 1000, 1000, 1000, 1000, settings.blocker_7]
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
        maxEnterableBlocker = round(runningGBTotal * BLOCKER_MAX)
        openLevels = GetAccessibleOpenLevels(settings, accessible)
        # Pick a random accessible B. Locker
        accessibleIncompleteLevels = [level for level in openLevels if level not in levelsProgressed and settings.EntryGBs[level] <= maxEnterableBlocker]
        # If we have no levels accessible, we need to lower a B. Locker count to make one accessible
        if len(accessibleIncompleteLevels) == 0:
            openUnprogressedLevels = [level for level in openLevels if level not in levelsProgressed]
            if len(openUnprogressedLevels) == 0:
                raise Ex.FillException("E1: Hard level order shuffler failed to progress through levels.")
            # Next level chosen randomly (possible room for improvement here?) from accessible levels
            nextLevelToBeat = choice(openUnprogressedLevels)
            # If the level still isn't accessible, we have to truncate the required amount
            if settings.EntryGBs[nextLevelToBeat] > maxEnterableBlocker:
                # Each B. Locker must be greater than the previous one and at least a specified percentage of availalbe GBs
                highroll = maxEnterableBlocker
                if settings.randomize_blocker_required_amounts:
                    highroll = min(highroll, settings.blocker_max)  # When there are more GBs available than the max B. Locker value
                lowroll = max(minimumBLockerGBs, round(runningGBTotal * BLOCKER_MIN))
                # Often as soon as a seed opens up, the GB count skyrockets. This can lead to the last few B. Lockers being very expensive
                # This check corrects for it assuming we want random non-hard B. Lockers.
                if settings.randomize_blocker_required_amounts and not settings.hard_blockers and runningGBTotal > settings.blocker_max:
                    lowroll = minimumBLockerGBs
                if lowroll > highroll:
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
        accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
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
                    accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
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
            accessible = GetAccessibleLocations(settings, [], SearchMode.GetReachable)
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
    if settings.training_barrels != TrainingBarrels.normal:
        # Vines only matter if we don't have Isles warps activated
        if settings.activate_all_bananaports == ActivateAllBananaports.off and not LogicVariables.vines:
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
        if i >= level - 1:
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
    LogicVariables = None
    LogicVariables = LogicVarHolder(spoiler.settings)
    # Initiate kasplat map with default
    InitKasplatMap(LogicVariables)
    # Handle misc randomizations
    ShuffleMisc(spoiler)
    # Level order rando may have to affect the progression to be fillable - no logic doesn't care about your silly progression, however
    if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all and spoiler.settings.logic_type != LogicType.nologic:
        # Handle Level Order if randomized
        if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
            ShuffleExits.ExitShuffle(spoiler.settings)
            spoiler.UpdateExits()
        # Assume we can progress through the levels, since these will be adjusted within FillKongsAndMovesForLevelOrder
        WipeProgressionRequirements(spoiler.settings)
        # Handle Item Fill
        FillKongsAndMovesForLevelOrder(spoiler)
    else:
        # Handle Loading Zones
        if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
            ShuffleExits.ExitShuffle(spoiler.settings)
            spoiler.UpdateExits()
        # Handle Item Fill
        if spoiler.settings.move_rando != MoveRando.off or spoiler.settings.kong_rando or any(spoiler.settings.shuffled_location_types):
            FillKongsAndMovesGeneric(spoiler)
        else:
            # Just check if normal item locations are beatable with given settings
            ItemPool.PlaceConstants(spoiler.settings)
            if not GetAccessibleLocations(spoiler.settings, [], SearchMode.CheckBeatable):
                raise Ex.VanillaItemsGameNotBeatableException("Game unbeatable.")
    CorrectBossKongLocations(spoiler)
    GeneratePlaythrough(spoiler)
    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        compileHints(spoiler)
    compileMicrohints(spoiler)
    Reset()
    ShuffleExits.Reset()
    spoiler.createJson()
    js.postMessage("Patching ROM...")
    # print(spoiler)
    # print(spoiler.json)
    patch_data = ApplyRandomizer.patching_response(spoiler)
    return patch_data, spoiler


def ShuffleMisc(spoiler):
    """Shuffle miscellaneous objects outside of main fill algorithm, including Kasplats, Bonus barrels, and bananaport warps."""
    # T&S and Wrinkly Door Shuffle
    if spoiler.settings.vanilla_door_rando:
        ShuffleVanillaDoors(spoiler)
    elif spoiler.settings.wrinkly_location_rando or spoiler.settings.tns_location_rando or spoiler.settings.remove_wrinkly_puzzles:
        ShuffleDoors(spoiler)
    # Handle Crown Placement
    if spoiler.settings.crown_placement_rando:
        crown_replacements = {}
        crown_human_replacements = {}
        ShuffleCrowns(crown_replacements, crown_human_replacements)
        spoiler.crown_locations = crown_replacements
        spoiler.human_crowns = dict(sorted(crown_human_replacements.items()))
    # Handle Bananaports
    if spoiler.settings.bananaport_rando == BananaportRando.in_level:
        replacements = []
        human_replacements = {}
        ShuffleWarps(replacements, human_replacements, spoiler.settings.warp_level_list_selected)
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    elif spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
        replacements = []
        human_replacements = {}
        ShuffleWarpsCrossMap(replacements, human_replacements, spoiler.settings.bananaport_rando == BananaportRando.crossmap_coupled, spoiler.settings.warp_level_list_selected)
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    LinkWarps()
    # Handle kasplats - this is the first VerifyWorld check, all shuffles affecting Locations must be before this one
    KasplatShuffle(spoiler, LogicVariables)
    spoiler.human_kasplats = {}
    spoiler.UpdateKasplats(LogicVariables.kasplat_map)
    # Handle bonus barrels
    if spoiler.settings.bonus_barrels in (MinigameBarrels.random, MinigameBarrels.selected) or spoiler.settings.helm_barrels == MinigameBarrels.random:
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # CB Shuffle
    if spoiler.settings.cb_rando:
        ShuffleCBs(spoiler)
    # Coin Shuffle
    if spoiler.settings.coin_rando:
        ShuffleCoins(spoiler)
    # Random Patches
    if spoiler.settings.random_patches:
        human_patches = []
        spoiler.human_patches = ShufflePatches(spoiler, human_patches).copy()
    if spoiler.settings.random_fairies:
        ShuffleFairyLocations(spoiler)
    if spoiler.settings.shuffle_shops:
        ShuffleShopLocations(spoiler)
    # Item Rando
    spoiler.human_item_assignment = {}
    spoiler.settings.update_valid_locations()
