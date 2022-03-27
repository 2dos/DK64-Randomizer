"""Options for the main rando tab."""
import random

import js
from js import document

from ui.bindings import bind


@bind("click", "shuffle_levels")
def update_disabled_progression(evt):
    """Disable certain page flags depending on checkboxes."""
    # Check the checked status of the randomize progression button
    if document.getElementById("shuffle_levels").checked:
        # Disable the kongs button
        document.getElementById("unlock_all_kongs").setAttribute("disabled", "disabled")
        document.getElementById("unlock_all_kongs").checked = True
    else:
        # Swap the kong
        try:
            document.getElementById("unlock_all_kongs").removeAttribute("disabled")
        except Exception:
            pass


@bind("click", "loading_zone_rando")
def toggle_loading_zone_coupling(event):
    """Set toggling for loading zone coupling."""
    if document.getElementById("loading_zone_rando").checked:
        js.document.getElementById("loading_zone_coupled").removeAttribute("disabled")
    else:
        js.document.getElementById("loading_zone_coupled").setAttribute("disabled", "disabled")


@bind("click", "loading_zone_rando")
@bind("click", "shuffle_levels")
def toggle_loading_zone_level_order(event):
    """Set toggling for level order."""
    try:
        if event.target.id == "loading_zone_rando":
            if document.getElementById("loading_zone_rando").checked:
                js.document.getElementById("shuffle_levels").setAttribute("disabled", "disabled")
                js.document.getElementById("shuffle_levels").removeAttribute("checked")
            else:
                js.document.getElementById("shuffle_levels").removeAttribute("disabled")
        elif event.target.id == "shuffle_levels":
            if document.getElementById("shuffle_levels").checked:
                js.document.getElementById("loading_zone_rando").setAttribute("disabled", "disabled")
                js.document.getElementById("loading_zone_rando").removeAttribute("checked")
            else:
                js.document.getElementById("loading_zone_rando").removeAttribute("disabled")
    except Exception:
        pass


def randomseed(evt):
    """Randomly generate a seed ID."""
    document.getElementById("seed").value = str(random.randint(100000, 999999))


@bind("input", "seed")
@bind("input", "blocker_", 8)
@bind("input", "troff_", 8)
def on_input(event):
    """Limits inputs from input boxes on keypress.

    Args:
        event (domevent): The DOMEvent data.

    Returns:
        bool: False if we need to stop the event.
    """
    # Make sure we limit the max items in each of these text boxes values
    if "troff" in event.target.id:
        min_max(event, 1, 500)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)
    elif "seed" in event.target.id:
        # If we make a seed id longer than 6 numbers truncate
        if len(event.target.value) > 6:
            document.getElementById(event.target.id).value = event.target.value[:6]
        # If we go below 0 just generate a random seed
        elif len(event.target.value) <= 0:
            randomseed(None)


def min_max(event, min, max):
    """Check if the data is within bounds of requirements.

    Args:
        event (DomEvent): The doms event.
        min (int): Minimum Value to keep.
        max (int): Maximum value to allow.

    Returns:
        bool: Deny or Success for Handled
    """
    try:
        # Attempt to cap our min and max for events on numbers
        if int(event.target.value) >= max:
            event.preventDefault()
            document.getElementById(event.target.id).value = max
        elif int(event.target.value) <= min:
            event.preventDefault()
            document.getElementById(event.target.id).value = min
        else:
            document.getElementById(event.target.id).value = str(event.target.value)
    except Exception:
        # Set the value to min if something goes wrong
        event.preventDefault()
        document.getElementById(event.target.id).value = min


@bind("keydown", "seed")
@bind("keydown", "blocker_", 8)
@bind("keydown", "troff_", 8)
def key_down(event):
    """Check if a key is a proper number, deletion, navigation, Copy/Cut/Paste.

    Args:
        event (DomEvent): Event from the DOM.
    """
    # Disable all buttons that are not in the list below or a digit
    global_keys = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Control_L", "Control_R", "x", "v", "c"]
    if not event.key.isdigit() and event.key not in global_keys:
        event.preventDefault()
    else:
        pass


def set_preset_options():
    """Set the Blocker presets on the page."""
    # Check what the selected dropdown item is
    element = document.getElementById("presets")
    children = []
    # Find all the items in the dropdown
    for child in element.children:
        children.append(child.value)
    # Find out dropdown item and set our selected item text to it
    for val in js.progression_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description")
            element.appendChild(opt)
    js.jq("#presets").val("Vanilla")


@bind("change", "presets")
def preset_select_changed(event):
    """Trigger a change of the form via the JSON templates."""
    element = document.getElementById("presets")
    presets = None
    for val in js.progression_presets:
        if val.get("name") == element.value:
            presets = val
    for key in presets:
        try:
            if type(presets[key]) is bool:
                if presets[key] is False:
                    document.getElementsByName(key)[0].removeAttribute("checked")
                else:
                    document.getElementsByName(key)[0].setAttribute("checked")
            else:
                js.jq(f"#{key}").val(presets[key])
        except Exception:
            pass
