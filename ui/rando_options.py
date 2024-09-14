"""Options for the main rando tab."""

import random
import re

import js

from randomizer.Lists.Songs import MusicSelectionPanel
from ui.bindings import bind, bindList
from ui.randomize_settings import randomize_settings



@bind("click", "randomize_settings")
def shuffle_settings(evt):
    """Randomize all non-cosmetic settings."""
    js.generateToast(f"Randomizing settings ({js.document.getElementById('random-weights').value}).<br>All non-cosmetic settings have been overwritten.")
    randomize_settings()

    # Run additional functions to ensure there are no conflicts.
    js.update_ui_states(evt)


musicToggles = [category.replace(" ", "") for category in MusicSelectionPanel.keys()]


@bindList("click", musicToggles, suffix="_collapse_toggle")
def toggle_collapsible_container(evt):
    """Show or hide a collapsible container."""
    targetElement = evt.target
    if "collapse_toggle" not in targetElement.id:
        # Get the parent of this element.
        targetElement = targetElement.parentElement
    toggledElement = re.search("^(.+)_collapse_toggle$", targetElement.id)[1]
    """Open or close the settings table on the Seed Info tab."""
    settingsTable = js.document.getElementById(toggledElement)
    settingsTable.classList.toggle("collapsed")
    toggledArrow = f'{toggledElement.replace("_", "-")}-expand-arrow'
    settingsArrow = js.document.getElementsByClassName(toggledArrow).item(0)
    settingsArrow.classList.toggle("flipped")
