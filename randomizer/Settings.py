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
        self.TrainingBarrels = "shuffled"

        # StartingKong: Kongs enum
        self.StartingKong = Kongs.donkey

        # StartWithKongs: bool
        self.StartWithKongs = False

        # StartWithCrankyMoves: bool
        self.StartWithCrankyMoves = True

        # ProgressiveUpgrades: bool
        self.ProgressiveUpgrades = True

        # OpenCrownDoor: bool
        self.OpenCrownDoor = True

        # OpenCoinDoor: bool
        self.OpenCoinDoor = True

        # StartWithCameraAndShockwave: bool
        self.StartWithCameraAndShockwave = True
