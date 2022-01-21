"""File that shuffles loading zone exits."""
import random

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Enums.Exits import Exits
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.ItemPool import AllItems, PlaceConstants
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.LogicClasses import Exit

LevelExitPool = [
    Exits.IslesToJapes,
    Exits.JapesToIsles,
    Exits.IslesToAztec,
    Exits.AztecToIsles,
    Exits.IslesToFactory,
    Exits.FactoryToIsles,
    Exits.IslesToGalleon,
    Exits.GalleonToIsles,
    Exits.IslesToForest,
    Exits.ForestToIsles,
    Exits.IslesToCaves,
    Exits.CavesToIsles,
    Exits.IslesToCastle,
    Exits.CastleToIsles,
    Exits.IslesToHelm,
    Exits.HelmToIsles,
]

# Root is the starting spawn, which is the main area of DK Isles.
root = Regions.IslesMain


def GetRootExit(exitId):
    """Query the world root to return an exit with a matching exit id."""
    return [x for x in Logic.Regions[root].exits if x.exitShuffleId is not None and x.exitShuffleId == exitId][0]


def RemoveRootExit(exit):
    """Remove an exit from the world root."""
    Logic.Regions[root].exits.remove(exit)


def AddRootExit(exit):
    """Add an exit to the world root."""
    Logic.Regions[root].exits.append(exit)


def Reset():
    """Reset shufflable exit properties set during shuffling."""
    for exit in ShufflableExits.values():
        exit.dest = exit.reverse
        exit.shuffled = False


def VerifyWorld(settings):
    """Make sure all item locations are reachable on current world graph with constant items placed and all other items owned."""
    PlaceConstants(settings)
    allReachable = Fill.GetAccessibleLocations(AllItems(settings), SearchMode.CheckAllReachable)
    Fill.Reset()
    return allReachable


def AttemptConnect(settings, front, frontId, back, backId):
    """Attempt to connect two exits, checking if the world is valid if they are connected."""
    # Remove connections to world root
    frontExit = GetRootExit(frontId)
    RemoveRootExit(frontExit)
    # if not decoupled
    backExit = GetRootExit(backId)
    RemoveRootExit(backExit)
    # Add connection between selected exits
    front.shuffled = True
    front.dest = backId
    # if not decoupled
    back.shuffled = True
    back.dest = frontId
    # Attempt to verify world
    valid = VerifyWorld(settings)
    # If world is not valid, restore root connections and undo new connections
    if not valid:
        AddRootExit(frontExit)
        front.shuffled = False
        front.dest = None
        # if not decoupled
        AddRootExit(backExit)
        back.shuffled = False
        back.dest = None
    return valid


def ShuffleExitsInPool(settings, frontpool, backpool):
    """Shuffle exits within a specific pool."""
    random.shuffle(frontpool)
    # For each front exit, select a random valid back exit to attach to it
    while len(frontpool) > 0:
        frontId = frontpool.pop()
        front = ShufflableExits[frontId]
        destinations = backpool.copy()
        # If our target exit to shuffle has a category, ensure it's not shuffled to entrances with the same category
        if front.category is not None:
            destinations = [
                x
                for x in destinations
                if ShufflableExits[x].category is None or ShufflableExits[x].category != front.category
            ]
        random.shuffle(destinations)
        # Select the destination
        for backId in destinations:
            back = ShufflableExits[backId]
            if AttemptConnect(settings, front, frontId, back, backId):
                # if not decoupled
                backpool.remove(backId)
                break
        if not front.shuffled:
            raise Ex.EntranceOutOfDestinations


def AssumeExits(pools, newpool):
    """Split exit pool into front and back pools, and assumes exits reachable from root."""
    frontpool = []
    backpool = []
    for i in range(len(newpool)):
        exitId = newpool[i]
        exit = ShufflableExits[exitId]
        # Even-numbered exits are "front", odd-numbered are "back"
        if i % 2 == 0:
            frontpool.append(exitId)
        else:
            backpool.append(exitId)
        # Set up assumed connection
        # 1) Break connection
        exit.dest = None
        # 2) Attach to root of world (DK Isles)
        newExit = Exit(exit.region, lambda l: True, exitId)
        AddRootExit(newExit)
    pools.append(frontpool)
    pools.append(backpool)


def ShuffleExits(settings):
    """Shuffle exit pools depending on settings."""
    # Set up front and back entrance pools for each setting
    # Assume all shuffled exits reachable by default
    pools = []
    if settings.shuffle_levels:
        AssumeExits(pools, LevelExitPool)
    if settings.shuffle_loading_zones:
        LoadingZonePool = [x for x in ShufflableExits.keys() if x not in LevelExitPool]
        AssumeExits(pools, LoadingZonePool)
    # Shuffle each entrance pool
    for i in range(0, len(pools), 2):
        ShuffleExitsInPool(settings, pools[i], pools[i + 1])


def ExitShuffle(settings):
    """Facilitate shuffling of exits."""
    retries = 0
    while True:
        try:
            # Shuffle entrances based on settings
            ShuffleExits(settings)
            # Verify world by assuring all locations are still reachable
            if not VerifyWorld(settings):
                raise Ex.EntrancePlacementException
            return
        except Ex.EntrancePlacementException:
            if retries == 20:
                print("Entrance placement failed, out of retries.")
                raise Ex.EntranceAttemptCountExceeded
            else:
                retries += 1
                print("Entrance placement failed. Retrying. Tries: " + str(retries))
                Reset()
