"""Temp file used for testing new logic system."""
import json
import random

from randomizer.Fill import Fill
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


def run(fill_type):
    """Generate a seed with a fill type.

    Args:
        fill_type (str): Fill type of forward or assumed.

    Returns:
        str: Currently just a placeholder string return to prove the data moving back to the main UI.
    """
    random.seed()
    settings = Settings()
    settings.algorithm = fill_type
    spoiler = Spoiler(settings)
    return json.dumps(Fill(spoiler))
