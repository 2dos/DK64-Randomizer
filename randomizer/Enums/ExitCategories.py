"""Exit Categories enum."""
from enum import IntEnum, auto


class ExitCategories(IntEnum):
    """These categories are used to categorize maps with multiple entrances."""

    IslesExterior = auto()
    IslesTrainingGrounds = auto()
    JapesLobby = auto()
    AztecLobby = auto()
    FactoryLobby = auto()
    GalleonLobby = auto()
    ForestLobby = auto()
    CavesLobby = auto()
    CastleLobby = auto()
    JapesExterior = auto()
    AztecExterior = auto()
    FactoryExterior = auto()
    GalleonExterior = auto()
    ForestExterior = auto()
    ForestMushroom = auto()
    ForestMill = auto()
    ForestGrinder = auto()
    CavesExterior = auto()
    CastleExterior = auto()
    CastleLower = auto()
    CastleUpper = auto()
    CastleBallroom = auto()
    CastleCarRaceExterior = auto()
    CastleCrypt = auto()
