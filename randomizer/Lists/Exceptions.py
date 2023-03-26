"""Custom exceptions for randomizer operations."""


class EntrancePlacementException(Exception):
    """Exception triggered when shuffled entrances fails to produce a valid world."""

    pass


class EntranceOutOfDestinations(EntrancePlacementException):
    """Exception triggered when an entrance attempted to be shuffled has no valid destinations."""

    pass


class EntranceAttemptCountExceeded(EntrancePlacementException):
    """Exception triggered when too many attempts were made to place entrances."""

    pass


class BarrelPlacementException(Exception):
    """Exception triggered when shuffled barrel minigames fails to produce a valid world."""

    pass


class BarrelOutOfMinigames(BarrelPlacementException):
    """Exception triggered when a barrel attempted to be shuffled has no valid minigames."""

    pass


class BarrelAttemptCountExceeded(BarrelPlacementException):
    """Exception triggered when too many attempts were made to place minigames."""

    pass


class KasplatPlacementException(Exception):
    """Exception triggered when shuffled kasplats minigames fails to produce a valid world."""

    pass


class KasplatOutOfKongs(KasplatPlacementException):
    """Exception triggered when a kasplat attempted to be shuffled has no valid kongs."""

    pass


class KasplatAttemptCountExceeded(KasplatPlacementException):
    """Exception triggered when too many attempts were made to place kasplats."""

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


class MusicPlacementExceededMapThreshold(Exception):
    """Exception triggered when shuffled music leads to a map having too big music files."""

    pass


class MusicAttemptCountExceeded(Exception):
    """Exception triggered when too many attempts were made to place music."""

    pass


class BossOutOfLocationsException(FillException):
    """Exception triggered when there are no valid levels to put a boss."""

    pass


class CBFillFailureException(FillException):
    """Exception triggered when CB rando fails to correctly generate a valid set of groups."""

    pass


class CoinFillFailureException(FillException):
    """Exception triggered when coin rando fails to correctly generate a valid set of groups."""

    pass


class SettingsIncompatibleException(FillException):
    """Exception triggered when conditions arise that are most likely a settings incompatibility."""

    pass
