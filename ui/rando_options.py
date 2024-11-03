"""Options for the main rando tab."""

import js

from ui.bindings import bind
from ui.randomize_settings import randomize_settings


@bind("click", "randomize_settings")
def shuffle_settings(evt):
    """Randomize all non-cosmetic settings."""
    js.generateToast(f"Randomizing settings ({js.document.getElementById('random-weights').value}).<br>All non-cosmetic settings have been overwritten.")
    randomize_settings()

    # Run additional functions to ensure there are no conflicts.
    js.update_ui_states(evt)
