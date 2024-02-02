"""Main worker class for the bot."""

from racetime_bot import Bot

from handler import RandoHandler
from dk64 import DK64


class RandoBot(Bot):
    """RandoBot base class."""

    def __init__(self, *args, **kwargs):
        """Set up the bot."""
        super().__init__(*args, **kwargs)
        self.DK64 = DK64()

    def get_handler_class(self):
        """Class override."""
        return RandoHandler

    def get_handler_kwargs(self, *args, **kwargs):
        """Kwargs override."""
        return {
            **super().get_handler_kwargs(*args, **kwargs),
            "dk64": self.DK64,
        }
