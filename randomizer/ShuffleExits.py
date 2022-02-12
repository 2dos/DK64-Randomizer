"""File that shuffles loading zone exits."""
from ast import And
import random

import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Regions import Regions
from randomizer.Enums.SearchMode import SearchMode
from randomizer.ItemPool import AllItems, PlaceConstants
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.LogicClasses import TransitionBack, TransitionFront

LevelExitPool = [
    Transitions.IslesToJapes,
    Transitions.JapesToIsles,
    Transitions.IslesToAztec,
    Transitions.AztecToIsles,
    Transitions.IslesToFactory,
    Transitions.FactoryToIsles,
    Transitions.IslesToGalleon,
    Transitions.GalleonToIsles,
    Transitions.IslesToForest,
    Transitions.ForestToIsles,
    Transitions.IslesToCaves,
    Transitions.CavesToIsles,
    Transitions.IslesToCastle,
    Transitions.CastleToIsles,
]

# Root is the starting spawn, which is the main area of DK Isles.
root = Regions.IslesMain


def GetRootExit(exitId):
    """Query the world root to return an exit with a matching exit id."""
    return [
        x for x in Logic.Regions[root].exits if x.assumed and x.exitShuffleId is not None and x.exitShuffleId == exitId
    ][0]


def RemoveRootExit(exit):
    """Remove an exit from the world root."""
    Logic.Regions[root].exits.remove(exit)


def AddRootExit(exit):
    """Add an exit to the world root."""
    Logic.Regions[root].exits.append(exit)


def Reset():
    """Reset shufflable exit properties set during shuffling."""
    for exit in ShufflableExits.values():
        exit.shuffledId = None
        exit.shuffled = False
    assumedExits = []
    for exit in [x for x in Logic.Regions[root].exits if x.assumed]:
        assumedExits.append(exit)
    for exit in assumedExits:
        RemoveRootExit(exit)


def VerifyWorld(settings):
    """Make sure all item locations are reachable on current world graph with constant items placed and all other items owned."""
    PlaceConstants(settings)
    unreachables = Fill.GetAccessibleLocations(settings, AllItems(settings), SearchMode.GetUnreachable)
    isValid = len(unreachables) == 0
    Fill.Reset()
    return isValid


def AttemptConnect(settings, frontExit, frontId, backExit, backId):
    """Attempt to connect two exits, checking if the world is valid if they are connected."""
    # Remove connections to world root
    frontReverse = None
    if not settings.decoupled_loading_zones:
        # Prevents an error if trying to assign an entrance back to itself
        if frontExit.back.reverse == backId:
            return False
        frontReverse = GetRootExit(frontExit.back.reverse)
        RemoveRootExit(frontReverse)
    backRootExit = GetRootExit(backId)
    RemoveRootExit(backRootExit)
    # Add connection between selected exits
    frontExit.shuffled = True
    frontExit.shuffledId = backId
    if not settings.decoupled_loading_zones:
        backReverse = ShufflableExits[backExit.back.reverse]
        backReverse.shuffled = True
        backReverse.shuffledId = frontExit.back.reverse
    # Attempt to verify world
    valid = VerifyWorld(settings)
    # If world is not valid, restore root connections and undo new connections
    if not valid:
        AddRootExit(backRootExit)
        frontExit.shuffled = False
        frontExit.shuffledId = None
        if not settings.decoupled_loading_zones:
            AddRootExit(frontReverse)
            backReverse.shuffled = False
            backReverse.shuffledId = None
    return valid


def ShuffleExitsInPool(settings, frontpool, backpool):
    """Shuffle exits within a specific pool."""
    NonTagRegions = [x for x in backpool if not Logic.Regions[ShufflableExits[x].back.regionId].tagbarrel]
    NonTagLeaves = [x for x in NonTagRegions if len(Logic.Regions[ShufflableExits[x].back.regionId].exits) == 1]
    random.shuffle(NonTagLeaves)
    NonTagNonLeaves = [x for x in NonTagRegions if x not in NonTagLeaves]
    random.shuffle(NonTagNonLeaves)

    TagRegions = [x for x in backpool if x not in NonTagRegions]
    TagLeaves = [x for x in TagRegions if len(Logic.Regions[ShufflableExits[x].back.regionId].exits) == 1]
    random.shuffle(TagLeaves)
    TagNonLeaves = [x for x in TagRegions if x not in TagLeaves]
    random.shuffle(TagNonLeaves)

    backpool = NonTagLeaves
    backpool.extend(NonTagNonLeaves)
    backpool.extend(TagLeaves)
    backpool.extend(TagNonLeaves)

    random.shuffle(frontpool)

    # For each back exit, select a random valid front entrance to attach to it
    while len(backpool) > 0:
        backId = backpool.pop(0)
        backExit = ShufflableExits[backId]
        # Filter origins to make sure that if this target requires a certain kong's access, then the entrance will be accessible by that kong
        origins = [x for x in frontpool if ShufflableExits[x].entryKongs.issuperset(backExit.regionKongs)]
        if not settings.decoupled_loading_zones and backExit.category is None:
            # In coupled, if both front & back are leaves, the result will be invalid
            origins = [x for x in origins if ShufflableExits[ShufflableExits[x].back.reverse].category is not None]
            # Also validate the entry & region kongs overlap in reverse direction
            origins = [x for x in origins if ShufflableExits[backExit.back.reverse].entryKongs.issuperset(ShufflableExits[ShufflableExits[x].back.reverse].regionKongs)]
        # Select a random origin
        for frontId in origins:
            frontExit = ShufflableExits[frontId]
            if AttemptConnect(settings, frontExit, frontId, backExit, backId):
                # print("Assigned " + frontExit.name + " --> " + backExit.name)
                frontpool.remove(frontId)
                if not settings.decoupled_loading_zones:
                    # If coupled, the opposite pairing also needs to be removed from the pool
                    # print("Assigned " + ShufflableExits[backExit.back.reverse].name + " --> " + ShufflableExits[frontExit.back.reverse].name)
                    frontpool.remove(backExit.back.reverse)
                    backpool.remove(frontExit.back.reverse)
                break
        if not frontExit.shuffled:
            print("Failed to connect to " + backExit.name + " from any of the remaining " + str(len(origins)) + " origins!")
            raise Ex.EntranceOutOfDestinations


def AssumeExits(settings, frontpool, backpool, newpool):
    """Split exit pool into front and back pools, and assumes exits reachable from root."""
    for i in range(len(newpool)):
        exitId = newpool[i]
        exit = ShufflableExits[exitId]
        # When coupled, only transitions which have a reverse path can be included in the pools
        if settings.decoupled_loading_zones == False and exit.back.reverse is None:
            continue
        # "front" is the entrance you go into, "back" is the exit you come out of
        frontpool.append(exitId)
        backpool.append(exitId)
        # Set up assumed connection
        # 1) Break connection
        exit.shuffledId = None
        exit.toBeShuffled = True
        # 2) Attach to root of world (DK Isles)
        newExit = TransitionFront(exit.back.regionId, lambda l: True, exitId, True)
        AddRootExit(newExit)


def ShuffleExits(settings):
    """Shuffle exit pools depending on settings."""
    # Set up front and back entrance pools for each setting
    # Assume all shuffled exits reachable by default
    frontpool = []
    backpool = []
    if settings.shuffle_loading_zones == "levels":
        AssumeExits(settings, frontpool, backpool, LevelExitPool)
    elif settings.shuffle_loading_zones == "all":
        AssumeExits(settings, frontpool, backpool, [x for x in ShufflableExits.keys()])
    # Shuffle each entrance pool
    ShuffleExitsInPool(settings, frontpool, backpool)


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
