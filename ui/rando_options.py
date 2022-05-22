"""Options for the main rando tab."""
import random

import js
from js import document
from ui.bindings import bind


def randomseed(evt):
    """Randomly generate a seed ID."""
    document.getElementById("seed").value = str(random.randint(100000, 999999))


@bind("input", "blocker_", 8)
@bind("input", "troff_", 8)
@bind("input", "blocker_text")
@bind("input", "troff_text")
def on_input(event):
    """Limits inputs from input boxes on keypress.

    Args:
        event (domevent): The DOMEvent data.

    Returns:
        bool: False if we need to stop the event.
    """
    # Make sure we limit the max items in each of these text boxes values
    if "troff" in event.target.id:
        min_max(event, 0, 500)
    elif event.target.id == "blocker_text":  # Maybe change depending on how we handing low randomized maximums
        min_max(event, 0, 200)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)


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


@bind("keydown", "blocker_", 8)
@bind("keydown", "troff_", 8)
@bind("keydown", "blocker_text")
@bind("keydown", "troff_text")
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
    js.jq("#presets").val("Suggested")
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    js.load_cookies()


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
                    document.getElementsByName(key)[0].setAttribute("checked", "checked")
            else:
                js.jq(f"#{key}").val(presets[key])
        except Exception as e:
            pass


@bind("click", "randomize_blocker_required_amounts")
def toggle_b_locker_boxes(event):
    """Toggle the textboxes for BLockers."""
    disabled = True
    if js.document.getElementById("randomize_blocker_required_amounts").checked:
        disabled = False
    blocker_text = js.document.getElementById("blocker_text")
    if disabled:
        blocker_text.setAttribute("disabled", "disabled")
    else:
        blocker_text.removeAttribute("disabled")
    for i in range(0, 10):
        blocker = js.document.getElementById(f"blocker_{i}")
        try:
            if disabled:
                blocker.removeAttribute("disabled")
            else:
                blocker.setAttribute("disabled", "disabled")
        except AttributeError:
            pass


@bind("click", "randomize_cb_required_amounts")
def toggle_counts_boxes(event):
    """Toggle the textboxes for Troff."""
    disabled = True
    if js.document.getElementById("randomize_cb_required_amounts").checked:
        disabled = False
    troff_text = js.document.getElementById("troff_text")
    if disabled:
        troff_text.setAttribute("disabled", "disabled")
    else:
        troff_text.removeAttribute("disabled")
    for i in range(0, 10):
        troff = js.document.getElementById(f"troff_{i}")
        try:
            if disabled:
                troff.removeAttribute("disabled")
            else:
                troff.setAttribute("disabled", "disabled")
        except AttributeError:
            pass


@bind("change", "level_randomization")
def update_boss_required(evt):
    """Disable certain page flags depending on checkboxes."""
    element = document.getElementById("level_randomization")
    if element.value == "level_order":
        document.getElementById("boss_location_rando").setAttribute("disabled", "disabled")
        document.getElementById("boss_location_rando").checked = True
        document.getElementById("boss_kong_rando").setAttribute("disabled", "disabled")
        document.getElementById("boss_kong_rando").checked = True
        document.getElementById("kong_rando").setAttribute("disabled", "disabled")
        document.getElementById("kong_rando").checked = True
    else:
        try:
            document.getElementById("boss_kong_rando").removeAttribute("disabled")
            document.getElementById("boss_location_rando").removeAttribute("disabled")
            document.getElementById("kong_rando").removeAttribute("disabled")
        except Exception:
            pass


@bind("click", "random_colors")
def disable_colors(evt):
    """Disable color options when Randomize All is selected."""
    disabled = False
    if js.document.getElementById("random_colors").checked:
        disabled = True
    for i in ["dk", "diddy", "tiny", "lanky", "chunky"]:
        color = js.document.getElementById(f"{i}_colors")
        try:
            if disabled:
                color.setAttribute("disabled", "disabled")
            else:
                color.removeAttribute("disabled")
        except AttributeError:
            pass


@bind("click", "enable_tag_anywhere")
def disable_tag_spawn(evt):
    """Disable 'Disable Tag Spawn' option when 'Tag Anywhere' is off."""
    disabled = False
    if js.document.getElementById("enable_tag_anywhere").checked is False:
        disabled = True
    if disabled:
        js.document.getElementById("disable_tag_barrels").setAttribute("disabled", "disabled")
        js.document.getElementById("disable_tag_barrels").checked = False
    else:
        js.document.getElementById("disable_tag_barrels").removeAttribute("disabled")


@bind("click", "disable_tag_barrels")
def enable_tag_anywhere(evt):
    """Enable 'Tag Anywhere' if 'Disable Tag Spawn' option is on."""
    if js.document.getElementById("disable_tag_barrels").checked:
        js.document.getElementById("enable_tag_anywhere").checked = True


@bind("click", "random_music")
def disable_music(evt):
    """Disable music options when Randomize All is selected."""
    disabled = False
    if js.document.getElementById("random_music").checked:
        disabled = True
    for i in ["bgm", "fanfares", "events"]:
        music = js.document.getElementById(f"music_{i}")
        try:
            if disabled:
                music.setAttribute("disabled", "disabled")
            else:
                music.removeAttribute("disabled")
        except AttributeError:
            pass


@bind("change", "starting_kongs_count")
def enable_kong_rando(evt):
    """Enable Kong Rando if less than 5 starting kongs."""
    print("Lanky")
    kong_rando = js.document.getElementById("kong_rando")
    if js.document.getElementById("starting_kongs_count").value == "5":
        kong_rando.checked = False
        kong_rando.setAttribute("disabled", "disabled")
    else:
        kong_rando.removeAttribute("disabled")


@bind("click", "krool_random")
def disable_krool_phases(evt):
    """Disable music options when Randomize All is selected."""
    disabled = False
    krool = js.document.getElementById("krool_phase_count")
    if js.document.getElementById("krool_random").checked:
        disabled = True
    try:
        if disabled:
            krool.setAttribute("disabled", "disabled")
        else:
            krool.removeAttribute("disabled")
    except AttributeError:
        pass