"""Settings class and functions."""


class Settings:
    """Class used to store settings for seed generation."""

    def __init__(self):
        """Initialize all settings to empty initially."""
        # Algorithm: str
        # forward
        # assumed
        self.Algorithm = "forward"
        # ShuffleTrainingBarrels: bool
        self.ShuffleTrainingBarrels = False
        # ProgressiveUpgrades: bool
        self.ProgressiveUpgrades = True
