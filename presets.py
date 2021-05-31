"""Manage default data on the form."""
from level_progression import LevelProgression
from browser import document
import random


def randomseed(event):
    """Randomly generate a seed ID."""
    document["seed"].value = str(random.randint(100000, 999999))


def set_troff_preset(event):
    """Set the troff n Scoff Presets on the page."""
    preset = document["troff_selected"].text.splitlines()[document["troff_selected"].selectedIndex]
    if preset is "":
        preset = "Vanilla"
    presets = LevelProgression().troff_presets()
    response = []
    if presets.Value.get(preset):
        for val in presets.Value.get(preset):
            response.append(val)
    count = 0
    for pre in response:
        document["troff_" + str(count)].value = pre.Value
        document["troff_" + str(count)].title = pre.ToolTip
        count += 1


def set_blocker_preset(event):
    """Set the Blocker presets on the page."""
    preset = document["blocker_selected"].text.splitlines()[document["blocker_selected"].selectedIndex]
    if preset is "":
        preset = "Vanilla"
    presets = LevelProgression().blocker_presets()
    response = []
    if presets.Value.get(preset):
        for val in presets.Value.get(preset):
            response.append(val)
    count = 0
    for pre in response:
        document["blocker_" + str(count)].value = pre.Value
        document["blocker_" + str(count)].title = pre.ToolTip
        count += 1


def on_input(event):
    """Limits inputs from input boxes on keypress.

    Args:
        event (domevent): The DOMEvent data.

    Returns:
        bool: False if we need to stop the event.
    """
    if "troff" in event.target.id:
        min_max(event, 1, 500)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)
    elif "seed" in event.target.id:
        if len(event.target.value) > 6:
            document[event.target.id].value = event.target.value[:6]
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
        if int(event.target.value) >= max:
            event.preventDefault()
            document[event.target.id].value = max
        elif int(event.target.value) <= min:
            event.preventDefault()
            document[event.target.id].value = min
        else:
            document[event.target.id].value = str(event.target.value)
    except Exception:
        event.preventDefault()
        document[event.target.id].value = min


def key_down(event):
    """Check if a key is a proper number, deletion, navigation, Copy/Cut/Paste.

    Args:
        event (DomEvent): Event from the DOM.
    """
    global_keys = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Control_L", "Control_R", "x", "v", "c"]
    if not event.key.isdigit() and event.key not in global_keys:
        event.preventDefault()
    else:
        pass


document["seed_button"].bind("click", randomseed)
document["troff_selected"].bind("change", set_troff_preset)
document["blocker_selected"].bind("change", set_blocker_preset)
document["seed"].bind("keydown", key_down)
document["seed"].bind("input", on_input)
randomseed(None)
for i in range(0, 8):
    try:
        document["blocker_" + str(i)].bind("input", on_input)
        document["blocker_" + str(i)].bind("keydown", key_down)
        document["troff_" + str(i)].bind("input", on_input)
        document["troff_" + str(i)].bind("keydown", key_down)
    except Exception:
        pass
