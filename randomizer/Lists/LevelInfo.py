"""Stores information about levels, currently specifically used for assigning keys."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Transitions import Transitions


class LevelInfo:
    """Class which stores some information about levels."""

    def __init__(self, TransitionTo, TransitionFrom, KeyLocation, KeyItem):
        """Initialize with given parameters."""
        self.TransitionTo = TransitionTo
        self.TransitionsFrom = TransitionFrom
        self.KeyLocation = KeyLocation
        self.KeyItem = KeyItem


LevelInfoList = {
    Levels.JungleJapes: LevelInfo(Transitions.IslesMainToJapesLobby, Transitions.IslesJapesLobbyToMain, Locations.JapesKey, Items.JungleJapesKey),
    Levels.AngryAztec: LevelInfo(Transitions.IslesMainToAztecLobby, Transitions.IslesAztecLobbyToMain, Locations.AztecKey, Items.AngryAztecKey),
    Levels.FranticFactory: LevelInfo(Transitions.IslesMainToFactoryLobby, Transitions.IslesFactoryLobbyToMain, Locations.FactoryKey, Items.FranticFactoryKey),
    Levels.GloomyGalleon: LevelInfo(Transitions.IslesMainToGalleonLobby, Transitions.IslesGalleonLobbyToMain, Locations.GalleonKey, Items.GloomyGalleonKey),
    Levels.FungiForest: LevelInfo(Transitions.IslesMainToForestLobby, Transitions.IslesForestLobbyToMain, Locations.ForestKey, Items.FungiForestKey),
    Levels.CrystalCaves: LevelInfo(Transitions.IslesMainToCavesLobby, Transitions.IslesCavesLobbyToMain, Locations.CavesKey, Items.CrystalCavesKey),
    Levels.CreepyCastle: LevelInfo(Transitions.IslesMainToCastleLobby, Transitions.IslesCastleLobbyToMain, Locations.CastleKey, Items.CreepyCastleKey),
}
