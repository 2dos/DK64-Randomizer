"""Custom exceptions for randomizer operations."""


class FillException(Exception):
    """Exception triggered during the fill process."""

    pass


class ItemPlacementException(FillException):
    """Exception triggered when not all items are placed from running out of reachable locations."""

    pass


class GameNotBeatableException(FillException):
    """Exception triggered when all items were placed but the game was not beatable."""

    pass
