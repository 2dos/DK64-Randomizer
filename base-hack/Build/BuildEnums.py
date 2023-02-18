"""Enums for the build process."""
from enum import IntEnum, auto


class ChangeType(IntEnum):
    """Change Type Enum."""

    Undefined = auto()
    PointerTable = auto()
    FixedLocation = auto()


class TextureFormat(IntEnum):
    """Texture Format Enum."""

    Null = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    I8 = auto()
    I4 = auto()
    IA8 = auto()
    IA4 = auto()


class TableNames(IntEnum):
    """Pointer Table Enum."""

    MusicMIDI = 0
    MapGeometry = auto()
    MapWalls = auto()
    MapFloors = auto()
    ModelTwoGeometry = auto()
    ActorGeometry = auto()
    Unknown6 = auto()
    TexturesUncompressed = auto()
    Cutscenes = auto()
    Setups = auto()
    InstanceScripts = auto()
    Animations = auto()
    Text = auto()
    Unknown13 = auto()
    TexturesHUD = auto()
    Paths = auto()
    Spawners = auto()
    DKTVInputs = auto()
    Triggers = auto()
    Unknown19 = auto()
    Unknown20 = auto()
    Autowalks = auto()
    Unknown22 = auto()
    Exits = auto()
    RaceCheckpoints = auto()
    TexturesGeometry = auto()
    UncompressedFileSizes = auto()
    Unknown27 = auto()
    Unknown28 = auto()
    Unknown29 = auto()
    Unknown30 = auto()
    Unknown31 = auto()
