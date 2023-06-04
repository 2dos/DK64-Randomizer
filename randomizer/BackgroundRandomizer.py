"""Generate Playthrough from the logic core."""
import codecs
import json
import pickle
import random
import traceback

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
    try:
        form_data = json.loads(form_string)
        random.seed(form_data.get("seed"))
        settings = Settings(form_data)
        # Doing generation
        spoiler = Spoiler(settings)
        Generate_Spoiler(spoiler)
        return codecs.encode(pickle.dumps(spoiler), "base64").decode()
    except Exception as e:
        print("error: " + traceback.format_exc())
        return json.dumps({"error": str(traceback.format_exc())})
