"""Setting data related to DKTV."""
import random

import js

from randomizer.Patcher import ROM
from randomizer.Settings import Settings


def randomize_dktv(settings: Settings):
    """Set our DKTV to a random intro.

    Args:
        settings (Settings): Settings post data from the form.
    """
    # Set our seed and randomly format the TV intro based off of it
    random.seed(int(settings.seed))
    tvintro = random.randint(0, 5)
    # Define the entries as a dict so we can format correctly
    tv_dict: dict = js.pointer_addresses[17]["entries"]
    # Load the DKTV Data we're updating
    ROM().seek(tv_dict[tvintro]["pointing_to"])
    stored_data = ROM().readBytes(tv_dict[tvintro]["compressed_size"])
    # Intentionally lock ALL the TVs to the one we selected so all players know they are on the same TV
    for tv in tv_dict:
        ROM().seek(tv["pointing_to"])
        ROM().writeBytes(stored_data)
