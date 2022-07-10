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
    if event.target.id == "blocker_text":
        return
    elif event.target.id == "troff_text":
        return
    elif "troff" in event.target.id:
        min_max(event, 0, 500)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)


@bind("focusout", "blocker_text")
def max_randomized_blocker(event):
    """Validate blocker input on loss of focus."""
    blocker_text = js.document.getElementById("blocker_text")
    if not blocker_text.value:
        blocker_text.value = 50
    elif 0 <= int(blocker_text.value) < 8:
        blocker_text.value = 8
    elif int(blocker_text.value) > 200:
        blocker_text.value = 200


@bind("focusout", "troff_text")
def max_randomized_troff(event):
    """Validate troff input on loss of focus."""
    troff_text = js.document.getElementById("troff_text")
    if not troff_text.value:
        troff_text.value = 300
    elif int(troff_text.value) > 500:
        troff_text.value = 500


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
            if val.get("name") == "-- Select a Preset --":
                opt.disabled = True
                opt.hidden = True
    js.jq("#presets").val("-- Select a Preset --")
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    js.load_cookies()


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
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    shop = document.getElementById("shop_location_rando")
    unlock_moves = document.getElementById("unlock_all_moves")
    if level.value == "level_order":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.setAttribute("disabled", "disabled")
        kong_rando.checked = True
        shop.setAttribute("disabled", "disabled")
        shop.checked = True
    elif level.value == "vanilla" and kong_rando.checked:
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.removeAttribute("disabled")
        shop.removeAttribute("disabled")
    else:
        try:
            boss_kong.removeAttribute("disabled")
            boss_location.removeAttribute("disabled")
            kong_rando.removeAttribute("disabled")
            shop.removeAttribute("disabled")
        except Exception:
            pass
    if unlock_moves.checked:
        try:
            shop.setAttribute("disabled", "disabled")
            shop.checked = False
        except Exception:
            pass


@bind("click", "kong_rando")
def disable_boss_rando(evt):
    """Disable Boss Kong and Boss Location Rando if Vanilla levels and Kong Rando."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    shop = document.getElementById("shop_location_rando")
    if kong_rando.checked and level.value == "vanilla":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        shop.removeAttribute("disabled")
    else:
        boss_kong.removeAttribute("disabled")
        boss_location.removeAttribute("disabled")
        kong_rando.removeAttribute("disabled")


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


@bind("click", "unlock_all_moves")
def disable_shuffle_shop(evt):
    """Disable Shuffle Shop Move Location when All Moves are Unlocked."""
    disabled = False
    shop = js.document.getElementById("shop_location_rando")
    prices = js.document.getElementById("random_prices")
    moves = js.document.getElementById("unlock_all_moves")
    if moves.checked:
        disabled = True
    try:
        if disabled:
            shop.setAttribute("disabled", "disabled")
            shop.checked = False
            prices.setAttribute("disabled", "disabled")
        elif js.document.getElementById("level_randomization").value != "level_order":
            shop.removeAttribute("disabled")
            prices.removeAttribute("disabled")
        else:
            prices.removeAttribute("disabled")
            shop.checked = True
    except AttributeError:
        pass


@bind("click", "gnawty_barrels")
def disable_barrel_rando(evt):
    """Disable Bonus Barrel Rando when Oops All Beaver Bother is selected."""
    disabled = False
    barrel = js.document.getElementById("bonus_barrel_rando")
    if js.document.getElementById("gnawty_barrels").checked:
        disabled = True
    try:
        if disabled:
            barrel.setAttribute("disabled", "disabled")
            barrel.checked = False
        else:
            barrel.removeAttribute("disabled")
    except AttributeError:
        pass


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
                    js.jq(f"#{key}").checked = False
                    js.document.getElementsByName(key)[0].checked = False
                else:
                    js.jq(f"#{key}").checked = True
                    js.document.getElementsByName(key)[0].checked = True
                js.jq(f"#{key}").removeAttr("disabled")
            else:
                if js.document.getElementsByName(key)[0].hasAttribute("data-slider-value"):
                    js.jq(f"#{key}").slider("setValue", presets[key])
                    js.jq(f"#{key}").slider("enable")
                    js.jq(f"#{key}").parent().find(".slider-disabled").removeClass("slider-disabled")
                else:
                    js.jq(f"#{key}").val(presets[key])
                js.jq(f"#{key}").removeAttr("disabled")
        except Exception as e:
            pass
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    update_boss_required(None)
    disable_colors(None)
    disable_music(None)
    disable_shuffle_shop(None)
    max_randomized_blocker(None)
    max_randomized_troff(None)
    disable_barrel_rando(None)
