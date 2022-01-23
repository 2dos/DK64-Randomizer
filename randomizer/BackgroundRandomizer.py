"""Generate Playthrough from the logic core."""
import codecs
import json
import pickle
import random

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
    random.seed(form_data.get("seed"))
    settings = Settings(form_data)
    # Doing generation
    spoiler = Spoiler(settings)
    try:
        Generate_Spoiler(spoiler)
    except Exception as e:
        return json.dumps({"error": str(e)})
    return codecs.encode(pickle.dumps(spoiler), "base64").decode()
