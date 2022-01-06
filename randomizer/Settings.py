"""Settings class and functions."""

from randomizer.Enums.Kongs import Kongs

class Settings:
    """Class used to store settings for seed generation."""

    def __init__(self):
        """Initialize all settings to empty initially."""
        # Algorithm: str
        # forward
        # assumed
        self.Algorithm = "forward"

        # EntryGBs: list(int)
        self.EntryGBs = [
            0, # Japes
            0, # Aztec
            0, # Factory
            0, # Galleon
            0, # Forest
            0, # Caves
            0, # Castle
            100, # Helm
        ]

        # BossBananas: list(int)
        self.BossBananas = [
            50, # Japes
            120, # Aztec
            200, # Factory
            250, # Galleon
            300, # Forest
            350, # Caves
            400, # Castle
        ]

        # TrainingBarrels: str
        # normal
        # shuffled
        # startwith
        self.TrainingBarrels = "normal"

        # StartingKong: Kongs enum
        self.StartingKong = Kongs.donkey

        # ShuffleItems: bool
        self.ShuffleItems = False

        # StartWithKongs: bool
        self.StartWithKongs = False

        # StartWithShopMoves: bool
        self.StartWithShopMoves = False

        # ProgressiveUpgrades: bool
        self.ProgressiveUpgrades = False

        # OpenCrownDoor: bool
        self.OpenCrownDoor = False

        # OpenCoinDoor: bool
        self.OpenCoinDoor = False

        # StartWithCameraAndShockwave: bool
        self.StartWithCameraAndShockwave = False

        # ShuffleLoadingZones: bool
        self.ShuffleLoadingZones = False
