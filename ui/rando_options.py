"""Options for the main rando tab."""
from js import document
import js
from ui.bindings import bind
import random


@bind("click", "randomize_progression")
def update_disabled_progression(evt):
    """Disable certain page flags depending on checkboxes."""
    if document.getElementById("randomize_progression").checked:
        try:
            document.getElementById("seed").removeAttribute("disabled")
        except Exception:
            pass
        try:
            document.getElementById("seed_button").removeAttribute("disabled")
        except Exception:
            pass
        document.getElementById("unlock_all_kongs").setAttribute("disabled", "disabled")
        document.getElementById("unlock_all_kongs").checked = True
    else:
        document.getElementById("seed").setAttribute("disabled", "disabled")
        document.getElementById("seed_button").setAttribute("disabled", "disabled")
        try:
            document.getElementById("unlock_all_kongs").removeAttribute("disabled")
        except Exception:
            pass


# Trigger it once so we make sure all options are synced up
update_disabled_progression(None)


@bind("click", "seed_button")
def randomseed(evt):
    """Randomly generate a seed ID."""
    document.getElementById("seed").value = str(random.randint(100000, 999999))


randomseed(None)


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
    if "troff" in event.target.id:
        min_max(event, 1, 500)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)
    elif "seed" in event.target.id:
        if len(event.target.value) > 6:
            document.getElementById(event.target.id).value = event.target.value[:6]
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
            document.getElementById(event.target.id).value = max
        elif int(event.target.value) <= min:
            event.preventDefault()
            document.getElementById(event.target.id).value = min
        else:
            document.getElementById(event.target.id).value = str(event.target.value)
    except Exception:
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
    global_keys = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Control_L", "Control_R", "x", "v", "c"]
    if not event.key.isdigit() and event.key not in global_keys:
        event.preventDefault()
    else:
        pass


@bind("change", "troff_selected")
def set_troff_preset(event):
    """Set the troff n Scoff Presets on the page."""
    element = document.getElementById("troff_selected")
    preset = element.value
    if not preset:
        preset = "Vanilla"
    children = []
    for child in element.children:
        children.append(child.value)
    for val in js.progression_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description_troff")
            element.appendChild(opt)
            if preset == "Vanilla":
                element.value = preset
        if val.get("name") == preset:
            response = val
    count = 0
    for pre in response.get("troff_progression"):
        document.getElementById("troff_" + str(count)).value = pre
        count += 1


@bind("change", "blocker_selected")
def set_blocker_preset(event):
    """Set the Blocker presets on the page."""
    element = document.getElementById("blocker_selected")
    preset = element.value
    if not preset:
        preset = "Vanilla"
    children = []
    for child in element.children:
        children.append(child.value)
    for val in js.progression_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description_blocker")
            element.appendChild(opt)
            if preset == "Vanilla":
                element.value = preset
        if val.get("name") == preset:
            response = val
    count = 0
    for pre in response.get("blocker_progression"):
        document.getElementById("blocker_" + str(count)).value = pre
        count += 1


set_blocker_preset(None)
set_troff_preset(None)
