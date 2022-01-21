"""Generate Playthrough from the logic core."""
import json

from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


def generate_playthrough(form_string: str):
    """Trigger a generation of the playthrough in a webworker.

    Args:
        form_string (str): The form data as json submitted.

    Returns:
        str: The Json data as a string.
    """
    form_data = json.loads(form_string)
    settings = Settings(form_data)
    spoiler = Spoiler(settings)
    # settings.shuffle_items = True
    # settings.shuffle_loading_zones = True
    # settings.decoupled_loading_zones = True

    # Doing generation
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    return spoiler.toJson()
