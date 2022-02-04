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
from randomizer.LogicClasses import TransitionBack, TransitionFront

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
        exit.dest = exit.originalDest
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


def AttemptConnect(settings, front, frontId, back, backId):
    """Attempt to connect two exits, checking if the world is valid if they are connected."""
    # Remove connections to world root
    frontExit = None
    if not settings.decoupled_loading_zones:
        # Prevents an error if trying to assign an entrance back to itself
        if frontId == backId:
            return False
        frontExit = GetRootExit(frontId)
        RemoveRootExit(frontExit)
    backExit = GetRootExit(backId)
    RemoveRootExit(backExit)
    # Add connection between selected exits
    front.shuffled = True
    front.dest = backId
    if not settings.decoupled_loading_zones:
        back.shuffled = True
        back.dest = frontId
    # Attempt to verify world
    valid = VerifyWorld(settings)
    # If world is not valid, restore root connections and undo new connections
    if not valid:
        AddRootExit(backExit)
        front.shuffled = False
        front.dest = None
        if not settings.decoupled_loading_zones:
            AddRootExit(frontExit)
            back.shuffled = False
            back.dest = None
    return valid


def ShuffleExitsInPool(settings, frontpool, backpool):
    """Shuffle exits within a specific pool."""
    NonTagRegions = [x for x in backpool if not Logic.Regions[ShufflableExits[x].region].tagbarrel]
    NonTagLeaves = [x for x in NonTagRegions if ShufflableExits[x].category is None]
    random.shuffle(NonTagLeaves)
    NonTagNonLeaves = [x for x in NonTagRegions if x not in NonTagLeaves]
    random.shuffle(NonTagNonLeaves)

    TagRegions = [x for x in backpool if x not in NonTagRegions]
    TagLeaves = [x for x in TagRegions if ShufflableExits[x].category is None]
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
        back = ShufflableExits[backId]
        # Filter origins to make sure that if this target requires a certain kong's access, then the entrance will be accessible by that kong
        origins = [x for x in frontpool if ShufflableExits[x].entryKongs.issuperset(back.regionKongs)]
        if not settings.decoupled_loading_zones and back.category is None:
            # In coupled, if both front & back are leaves, the result will be invalid
            origins = [x for x in origins if ShufflableExits[x].category is not None]
        # Select a random origin
        for frontId in origins:
            front = ShufflableExits[frontId]
            if AttemptConnect(settings, front, frontId, back, backId):
                # print("Assigned " + front.name + " --> " + back.name)
                frontpool.remove(frontId)
                if not settings.decoupled_loading_zones:
                    # If coupled, the opposite pairing also needs to be removed from the pool
                    frontpool.remove(backId)
                    backpool.remove(frontId)
                break
        if not front.shuffled:
            # print("Failed to connect to " + back.name + " from any of the remaining " + str(len(origins)) + " origins!")
            raise Ex.EntranceOutOfDestinations


def AssumeExits(settings, frontpool, backpool, newpool):
    """Split exit pool into front and back pools, and assumes exits reachable from root."""
    for i in range(len(newpool)):
        exitId = newpool[i]
        exit = ShufflableExits[exitId]
        # "front" is the entrance you go into, "back" is the exit you come out of
        frontpool.append(exitId)
        backpool.append(exitId)
        # Set up assumed connection
        # 1) Break connection
        exit.dest = None
        exit.toBeShuffled = True
        # 2) Attach to root of world (DK Isles)
        newExit = TransitionFront(exit.region, lambda l: True, exitId, True)
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
