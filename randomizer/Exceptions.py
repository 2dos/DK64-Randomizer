"""Custom exceptions for randomizer operations."""

class EntrancePlacementException(Exception):
    """Exception triggered when shuffled entrances fails to produce a valid world."""

    pass

class EntranceAttemptCountExceeded(EntrancePlacementException):
    """Exception triggered when too many attempts were made to place entrances."""

    pass

class FillException(Exception):
    """Exception triggered during the fill process."""

    pass


class ItemPlacementException(FillException):
    """Exception triggered when not all items are placed from running out of reachable locations."""

    pass


class GameNotBeatableException(FillException):
    """Exception triggered when all items were placed but the game was not beatable."""

    pass

class VanillaItemsGameNotBeatableException(FillException):
    """Exception triggered when all locations have vanilla items but the game was not beatable."""

    pass