"""Options for the main rando tab."""

import random
import re

import js
from js import document
from randomizer.Enums.Items import Items
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Settings import SettingsMap
from randomizer.Lists.Item import StartingMoveOptions
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.Songs import MusicSelectionPanel
from randomizer.PlandoUtils import MoveSet
from randomizer.SettingStrings import decrypt_settings_string_enum
from ui.bindings import bind, bindList
from ui.randomize_settings import randomize_settings


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


@bind("focusout", "progressive_hint_text")
def handle_progressive_hint_text(event):
    """Validate blocker input on loss of focus."""
    progressive_hint_text = js.document.getElementById("progressive_hint_text")
    if not progressive_hint_text.value:
        progressive_hint_text.value = 60
    elif int(progressive_hint_text.value) < 1:
        progressive_hint_text.value = 1
    elif int(progressive_hint_text.value) > 201:
        progressive_hint_text.value = 201


@bind("focusout", "chaos_ratio")
def handle_chaos_ratio_text(event):
    """Validate blocker input on loss of focus."""
    chaos_ratio_text = js.document.getElementById("chaos_ratio")
    if not chaos_ratio_text.value:
        chaos_ratio_text.value = 25
    elif int(chaos_ratio_text.value) < 1:
        chaos_ratio_text.value = 1
    elif int(chaos_ratio_text.value) > 100:
        chaos_ratio_text.value = 100


@bind("focusout", "blocker_text")
def max_randomized_blocker(event):
    """Validate blocker input on loss of focus."""
    blocker_text = js.document.getElementById("blocker_text")
    if not blocker_text.value:
        blocker_text.value = 50
    elif int(blocker_text.value) < 0:
        blocker_text.value = 0
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


@bind("focusout", "music_volume")
def max_music(event):
    """Validate music input on loss of focus."""
    music_text = js.document.getElementById("music_volume")
    if not music_text.value:
        music_text.value = 100
    elif int(music_text.value) > 100:
        music_text.value = 100
    elif int(music_text.value) < 0:
        music_text.value = 0


@bind("focusout", "custom_music_proportion")
def max_music_proportion(event):
    """Validate music input on loss of focus."""
    music_text = js.document.getElementById("custom_music_proportion")
    if not music_text.value:
        music_text.value = 100
    elif int(music_text.value) > 100:
        music_text.value = 100
    elif int(music_text.value) < 0:
        music_text.value = 0


@bind("focusout", "sfx_volume")
def max_sfx(event):
    """Validate sfx input on loss of focus."""
    sfx_text = js.document.getElementById("sfx_volume")
    if not sfx_text.value:
        sfx_text.value = 100
    elif int(sfx_text.value) > 100:
        sfx_text.value = 100
    elif int(sfx_text.value) < 0:
        sfx_text.value = 0


@bind("focusout", "medal_requirement")
def max_randomized_medals(event):
    """Validate medal input on loss of focus."""
    medal_requirement = js.document.getElementById("medal_requirement")
    if not medal_requirement.value:
        medal_requirement.value = 15
    elif 0 > int(medal_requirement.value):
        medal_requirement.value = 0
    elif int(medal_requirement.value) > 40:
        medal_requirement.value = 40


@bind("focusout", "medal_cb_req")
def max_randomized_medal_cb_req(event):
    """Validate cb medal input on loss of focus."""
    medal_cb_req = js.document.getElementById("medal_cb_req")
    if not medal_cb_req.value:
        medal_cb_req.value = 75
    elif 1 > int(medal_cb_req.value):
        medal_cb_req.value = 1
    elif int(medal_cb_req.value) > 100:
        medal_cb_req.value = 100


@bind("focusout", "rareware_gb_fairies")
def max_randomized_fairies(event):
    """Validate fairy input on loss of focus."""
    fairy_req = js.document.getElementById("rareware_gb_fairies")
    if not fairy_req.value:
        fairy_req.value = 20
    elif 1 > int(fairy_req.value):
        fairy_req.value = 1
    elif int(fairy_req.value) > 20:
        fairy_req.value = 20


@bind("focusout", "mermaid_gb_pearls")
def max_randomized_pearls(event):
    """Validate pearl input on loss of focus."""
    pearl_req = js.document.getElementById("mermaid_gb_pearls")
    if not pearl_req.value:
        pearl_req.value = 5
    elif 0 > int(pearl_req.value):
        pearl_req.value = 0
    elif int(pearl_req.value) > 5:
        pearl_req.value = 5


@bind("click", "shuffle_items")
@bind("change", "move_rando")
@bind("focusout", "starting_moves_count")
def max_starting_moves_count(event):
    """Validate starting moves count input on loss of focus."""
    move_count = js.document.getElementById("starting_moves_count")
    moves = js.document.getElementById("move_rando")
    item_rando = js.document.getElementById("shuffle_items")
    max_starting_moves = 41
    if not item_rando.checked and moves.value != "off":
        max_starting_moves = 4
    if not move_count.value:
        move_count.value = 4
    elif 0 > int(move_count.value):
        move_count.value = 0
    elif int(move_count.value) > max_starting_moves:
        move_count.value = max_starting_moves


DISABLED_HELM_DOOR_VALUES = ("easy_random", "medium_random", "hard_random", "opened")


@bind("change", "crown_door_item")
def updateDoorOneNumAccess(event):
    """Toggle the textboxes for the first helm door."""
    door_one_selection = js.document.getElementById("crown_door_item")
    door_one_container = js.document.getElementById("door_1_container")
    disabled = door_one_selection.value in DISABLED_HELM_DOOR_VALUES
    door_one_req = js.document.getElementById("crown_door_item_count")
    if disabled:
        door_one_container.classList.add("hide-input")
    else:
        door_one_container.classList.remove("hide-input")
    if not door_one_req.value:
        door_one_req.value = 1
    elif door_one_selection.value == "vanilla" and int(door_one_req.value) > 10:
        door_one_req.value = 10
    elif door_one_selection.value == "req_gb" and int(door_one_req.value) > 201:
        door_one_req.value = 201
    elif door_one_selection.value == "req_bp" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_medal" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_companycoins" and int(door_one_req.value) > 2:
        door_one_req.value = 2
    elif door_one_selection.value == "req_key" and int(door_one_req.value) > 8:
        door_one_req.value = 8
    elif door_one_selection.value == "req_fairy" and int(door_one_req.value) > 18:
        door_one_req.value = 18
    elif door_one_selection.value == "req_bean" and int(door_one_req.value) > 1:
        door_one_req.value = 1
    elif door_one_selection.value == "req_pearl" and int(door_one_req.value) > 5:
        door_one_req.value = 5
    elif door_one_selection.value == "req_rainbowcoin" and int(door_one_req.value) > 16:
        door_one_req.value = 16


@bind("change", "coin_door_item")
def updateDoorTwoNumAccess(event):
    """Toggle the textboxes for the second helm door."""
    door_two_selection = js.document.getElementById("coin_door_item")
    door_two_container = js.document.getElementById("door_2_container")
    disabled = door_two_selection.value in DISABLED_HELM_DOOR_VALUES
    door_two_req = js.document.getElementById("coin_door_item_count")
    if disabled:
        door_two_container.classList.add("hide-input")
    else:
        door_two_container.classList.remove("hide-input")
    if not door_two_req.value:
        door_two_req.value = 1
    elif door_two_selection.value == "vanilla" and int(door_two_req.value) > 2:
        door_two_req.value = 2
    elif door_two_selection.value == "req_gb" and int(door_two_req.value) > 201:
        door_two_req.value = 201
    elif door_two_selection.value == "req_bp" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_key" and int(door_two_req.value) > 8:
        door_two_req.value = 8
    elif door_two_selection.value == "req_medal" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_crown" and int(door_two_req.value) > 10:
        door_two_req.value = 10
    elif door_two_selection.value == "req_fairy" and int(door_two_req.value) > 18:
        door_two_req.value = 18
    elif door_two_selection.value == "req_bean" and int(door_two_req.value) > 1:
        door_two_req.value = 1
    elif door_two_selection.value == "req_pearl" and int(door_two_req.value) > 5:
        door_two_req.value = 5
    elif door_two_selection.value == "req_rainbowcoin" and int(door_two_req.value) > 16:
        door_two_req.value = 16


DISABLED_WIN_VALUES = ("easy_random", "medium_random", "hard_random", "beat_krool", "get_key8", "krem_kapture", "dk_rap_items")


@bind("change", "win_condition_item")
def updateWinConNumAccess(event):
    """Toggle the textboxes for the win condition."""
    win_con_selection = js.document.getElementById("win_condition_item")
    win_con_container = js.document.getElementById("win_condition_container")
    disabled = win_con_selection.value in DISABLED_WIN_VALUES
    win_con_req = js.document.getElementById("win_condition_count")
    if disabled:
        win_con_container.classList.add("hide-input")
    else:
        win_con_container.classList.remove("hide-input")
    if not win_con_req.value:
        win_con_req.value = 1
    elif win_con_selection.value == "req_gb" and int(win_con_req.value) > 201:
        win_con_req.value = 201
    elif win_con_selection.value == "req_bp" and int(win_con_req.value) > 40:
        win_con_req.value = 40
    elif win_con_selection.value == "req_key" and int(win_con_req.value) > 8:
        win_con_req.value = 8
    elif win_con_selection.value == "req_medal" and int(win_con_req.value) > 40:
        win_con_req.value = 40
    elif win_con_selection.value == "req_crown" and int(win_con_req.value) > 10:
        win_con_req.value = 10
    elif win_con_selection.value == "req_fairy" and int(win_con_req.value) > 18:
        win_con_req.value = 18
    elif win_con_selection.value == "req_bean" and int(win_con_req.value) > 1:
        win_con_req.value = 1
    elif win_con_selection.value == "req_pearl" and int(win_con_req.value) > 5:
        win_con_req.value = 5
    elif win_con_selection.value == "req_rainbowcoin" and int(win_con_req.value) > 16:
        win_con_req.value = 16


@bind("focusout", "crown_door_item_count")
def max_doorone_requirement(event):
    """Validate Door 1 input on loss of focus."""
    door_one_req = js.document.getElementById("crown_door_item_count")
    door_one_selection = js.document.getElementById("crown_door_item")
    # Never go below 1 for any option
    if not door_one_req.value:
        door_one_req.value = 1
    elif 1 > int(door_one_req.value):
        door_one_req.value = 1
    if door_one_selection.value == "vanilla" and int(door_one_req.value) > 10:
        door_one_req.value = 10
    elif door_one_selection.value == "req_gb" and int(door_one_req.value) > 201:
        door_one_req.value = 201
    elif door_one_selection.value == "req_bp" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_companycoins" and int(door_one_req.value) > 2:
        door_one_req.value = 2
    elif door_one_selection.value == "req_key" and int(door_one_req.value) > 8:
        door_one_req.value = 8
    elif door_one_selection.value == "req_medal" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_fairy" and int(door_one_req.value) > 18:
        door_one_req.value = 18
    elif door_one_selection.value == "req_bean" and int(door_one_req.value) > 1:
        door_one_req.value = 1
    elif door_one_selection.value == "req_pearl" and int(door_one_req.value) > 5:
        door_one_req.value = 5


@bind("focusout", "coin_door_item_count")
def max_doortwo_requirement(event):
    """Validate Door 2 input on loss of focus."""
    door_two_req = js.document.getElementById("coin_door_item_count")
    door_two_selection = js.document.getElementById("coin_door_item")
    if not door_two_req.value:
        door_two_req.value = 1
    elif 1 > int(door_two_req.value):
        door_two_req.value = 1
    if door_two_selection.value == "vanilla" and int(door_two_req.value) > 2:
        door_two_req.value = 2
    elif door_two_selection.value == "req_gb" and int(door_two_req.value) > 201:
        door_two_req.value = 201
    elif door_two_selection.value == "req_bp" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_key" and int(door_two_req.value) > 8:
        door_two_req.value = 8
    elif door_two_selection.value == "req_medal" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_crown" and int(door_two_req.value) > 10:
        door_two_req.value = 10
    elif door_two_selection.value == "req_fairy" and int(door_two_req.value) > 18:
        door_two_req.value = 18
    elif door_two_selection.value == "req_bean" and int(door_two_req.value) > 1:
        door_two_req.value = 1
    elif door_two_selection.value == "req_pearl" and int(door_two_req.value) > 5:
        door_two_req.value = 5


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


def set_random_weights_options():
    """Set the random settings presets on the page."""
    element = document.getElementById("random-weights")
    children = []
    # Take note of the items currently in the dropdown.
    for child in element.children:
        children.append(child.value)
    # Add all of the random weights presets.
    for val in js.random_settings_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description")
            element.appendChild(opt)
            if val.get("name") == "Standard":
                opt.selected = True


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
    toggle_logic_type(None)
    toggle_bananaport_selector(None)
    updateDoorOneNumAccess(None)
    updateDoorTwoNumAccess(None)
    updateWinConNumAccess(None)

    js.load_data()


@bind("click", "randomize_blocker_required_amounts")
def toggle_b_locker_boxes(event):
    """Toggle the textboxes for BLockers."""
    disabled = True
    if js.document.getElementById("randomize_blocker_required_amounts").checked:
        disabled = False
    blocker_text = js.document.getElementById("blocker_text")
    maximize_helm_blocker = js.document.getElementById("maximize_helm_blocker")
    if disabled:
        blocker_text.setAttribute("disabled", "disabled")
        maximize_helm_blocker.setAttribute("disabled", "disabled")
    else:
        blocker_text.removeAttribute("disabled")
        maximize_helm_blocker.removeAttribute("disabled")
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
def change_level_randomization(evt):
    """Disable certain page flags depending on level randomization."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    shuffle_helm_location = document.getElementById("shuffle_helm_location")

    disable_boss_shuffles = level.value in ("level_order", "level_order_complex") or (level.value == "vanilla" and kong_rando.checked)
    disable_kong_rando = level.value in ("level_order", "level_order_complex")
    disable_shuffle_helm_location = level.value in ("level_order", "level_order_complex", "vanilla")

    if disable_boss_shuffles:
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
    else:
        boss_kong.removeAttribute("disabled")
        boss_location.removeAttribute("disabled")
    if disable_kong_rando:
        kong_rando.setAttribute("disabled", "disabled")
        kong_rando.checked = True
    else:
        kong_rando.removeAttribute("disabled")
    if disable_shuffle_helm_location:
        shuffle_helm_location.setAttribute("disabled", "disabled")
        shuffle_helm_location.checked = False
    else:
        shuffle_helm_location.removeAttribute("disabled")


@bind("click", "kong_rando")
def disable_boss_rando(evt):
    """Disable Boss Kong and Boss Location Rando if Vanilla levels and Kong Rando."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    if kong_rando.checked and level.value == "vanilla" or level.value == "level_order":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
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
    KONG_ZONES = {"DK": ["Fur", "Tie"], "Diddy": ["Clothes"], "Lanky": ["Clothes", "Fur"], "Tiny": ["Clothes", "Hair"], "Chunky": ["Main", "Other"], "Rambi": ["Skin"], "Enguarde": ["Skin"]}
    for kong in KONG_ZONES:
        for zone in KONG_ZONES[kong]:
            color = js.document.getElementById(f"{kong.lower()}_{zone.lower()}_colors")
            picker = js.document.getElementById(f"{kong.lower()}_{zone.lower()}_custom_color")
            try:
                if disabled:
                    color.setAttribute("disabled", "disabled")
                    picker.setAttribute("disabled", "disabled")
                else:
                    color.removeAttribute("disabled")
                    picker.removeAttribute("disabled")
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
    for i in ["bgm", "majoritems", "minoritems", "events"]:
        music = js.document.getElementById(f"music_{i}_randomized")
        try:
            if disabled:
                music.setAttribute("disabled", "disabled")
                music.setAttribute("checked", "checked")
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
    """Disable K Rool options when Randomize All is selected."""
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


@bind("click", "helm_random")
def disable_helm_phases(evt):
    """Disable Helm options when Randomize All is selected."""
    disabled = False
    helm = js.document.getElementById("helm_phase_count")
    if js.document.getElementById("helm_random").checked:
        disabled = True
    try:
        if disabled:
            helm.setAttribute("disabled", "disabled")
        else:
            helm.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "krool_random")
@bind("change", "krool_phase_count")
def plando_hide_krool_options(evt):
    """Hide the plando options to select Kongs for certain K. Rool phases if those phases are disabled."""
    krool_phase_count = int(js.document.getElementById("krool_phase_count").value)
    krool_random = js.document.getElementById("krool_random").checked
    for i in range(0, 5):
        krool_phase_plando_div = js.document.getElementById(f"plando_krool_order_div_{i}")
        krool_phase_plando = js.document.getElementById(f"plando_krool_order_{i}")
        if i < krool_phase_count or krool_random:
            krool_phase_plando_div.classList.remove("disabled-select")
            krool_phase_plando.removeAttribute("disabled")
        else:
            krool_phase_plando_div.classList.add("disabled-select")
            krool_phase_plando.setAttribute("disabled", "disabled")
            krool_phase_plando.value = ""


@bind("click", "helm_random")
@bind("change", "helm_phase_count")
def plando_hide_helm_options(evt):
    """Hide the plando options to select Kongs for certain Helm phases if those phases are disabled."""
    helm_phase_count = int(js.document.getElementById("helm_phase_count").value)
    helm_random = js.document.getElementById("helm_random").checked
    for i in range(0, 5):
        helm_phase_plando_div = js.document.getElementById(f"plando_helm_order_div_{i}")
        helm_phase_plando = js.document.getElementById(f"plando_helm_order_{i}")
        if i < helm_phase_count or helm_random:
            helm_phase_plando_div.classList.remove("disabled-select")
            helm_phase_plando.removeAttribute("disabled")
        else:
            helm_phase_plando_div.classList.add("disabled-select")
            helm_phase_plando.setAttribute("disabled", "disabled")
            helm_phase_plando.value = ""


@bind("click", "nav-plando-tab")
def plando_propagate_options(evt):
    """Make changes to the plando tab based on other settings.

    This is partly a workaround for issues with the Bootstrap slider.
    """
    plando_hide_krool_options(evt)
    plando_hide_helm_options(evt)
    plando_disable_camera_shockwave(evt)
    plando_toggle_custom_locations_tab(evt)
    plando_toggle_custom_arena_locations(evt)
    plando_toggle_custom_patch_locations(evt)
    plando_toggle_custom_fairy_locations(evt)
    plando_toggle_custom_kasplat_locations(evt)
    plando_toggle_custom_crate_locations(evt)
    plando_toggle_custom_wrinkly_locations(evt)
    plando_toggle_custom_tns_locations(evt)
    plando_disable_arena_custom_locations(evt)
    plando_disable_crate_custom_locations(evt)
    plando_disable_fairy_custom_locations(evt)
    plando_disable_kasplat_custom_locations(evt)
    plando_disable_patch_custom_locations(evt)
    plando_disable_wrinkly_custom_locations(evt)
    plando_disable_tns_custom_locations(evt)


@bind("change", "move_rando")
def disable_move_shuffles(evt):
    """Disable some settings based on the move rando setting."""
    moves = js.document.getElementById("move_rando")
    prices = js.document.getElementById("random_prices")
    training_barrels = js.document.getElementById("training_barrels")
    shockwave_status = js.document.getElementById("shockwave_status")
    starting_moves_count = js.document.getElementById("starting_moves_count")
    start_with_slam = js.document.getElementById("start_with_slam")
    try:
        if moves.value == "start_with":
            prices.setAttribute("disabled", "disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 41
            starting_moves_count.setAttribute("disabled", "disabled")
            start_with_slam.checked = True
            start_with_slam.setAttribute("disabled", "disabled")
        elif moves.value == "off":
            prices.removeAttribute("disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 41
            starting_moves_count.setAttribute("disabled", "disabled")
            start_with_slam.checked = True
            start_with_slam.setAttribute("disabled", "disabled")
        else:
            prices.removeAttribute("disabled")
            training_barrels.removeAttribute("disabled")
            shockwave_status.removeAttribute("disabled")
            starting_moves_count.removeAttribute("disabled")
            start_with_slam.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "bonus_barrel_rando")
def disable_barrel_modal(evt):
    """Disable Minigame Selector when Shuffle Bonus Barrels is off."""
    disabled = True
    selector = js.document.getElementById("minigames_list_modal")
    if js.document.getElementById("bonus_barrel_rando").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "enemy_rando")
def disable_enemy_modal(evt):
    """Disable Enemy Selector when Enemy Rando is off."""
    disabled = True
    selector = js.document.getElementById("enemies_modal")
    if js.document.getElementById("enemy_rando").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "hard_mode")
def disable_hard_mode_modal(evt):
    """Disable Hard Mode Selector when Hard Mode is off."""
    disabled = True
    selector = js.document.getElementById("hard_mode_modal")
    if js.document.getElementById("hard_mode").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "hard_bosses")
def disable_hard_bosses_modal(evt):
    """Disable Hard Mode Selector when Hard Mode is off."""
    disabled = True
    selector = js.document.getElementById("hard_bosses_modal")
    if js.document.getElementById("hard_bosses").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "nav-music-tab")
@bind("click", "songs_excluded")
def disable_excluded_songs_modal(evt):
    """Disable Excluded Song Selector when Excluded Songs is off."""
    disabled = True
    selector = js.document.getElementById("excluded_songs_modal")
    if js.document.getElementById("songs_excluded").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "music_filtering")
def disable_music_filtering_modal(evt):
    """Disable Excluded Song Selector when Excluded Songs is off."""
    disabled = True
    selector = js.document.getElementById("music_filtering_modal")
    if js.document.getElementById("music_filtering").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "shuffle_items")
def toggle_item_rando(evt):
    """Enable and disable settings based on Item Rando being on/off."""
    disabled = True
    selector = js.document.getElementById("item_rando_list_modal")
    item_rando_pool = document.getElementById("item_rando_list_selected").options
    smaller_shops = document.getElementById("smaller_shops")
    shockwave = document.getElementById("shockwave_status_shuffled")
    move_vanilla = document.getElementById("move_off")
    move_rando = document.getElementById("move_on")
    enemy_drop_rando = document.getElementById("enemy_drop_rando")
    non_item_rando_warning = document.getElementById("non_item_rando_warning")
    shared_shop_warning = document.getElementById("shared_shop_warning")
    kong_rando = document.getElementById("kong_rando")
    shops_in_pool = False
    kongs_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
        if option.value == "kong":
            if option.selected:
                kongs_in_pool = True
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
        kongs_in_pool = True
    if js.document.getElementById("shuffle_items").checked:
        disabled = False
    try:
        if disabled:
            # Prevent item rando modal from opening, smaller shop setting, and dropsanity setting
            selector.setAttribute("disabled", "disabled")
            smaller_shops.setAttribute("disabled", "disabled")
            smaller_shops.checked = False
            shockwave.removeAttribute("disabled")
            move_vanilla.removeAttribute("disabled")
            move_rando.removeAttribute("disabled")
            enemy_drop_rando.setAttribute("disabled", "disabled")
            enemy_drop_rando.checked = False
            non_item_rando_warning.removeAttribute("hidden")
            shared_shop_warning.removeAttribute("hidden")
            kong_rando.removeAttribute("disabled")
        else:
            # Enable item rando modal, prevent shockwave/camera coupling, enable dropsanity, and enable smaller shops if it's in the pool
            selector.removeAttribute("disabled")
            enemy_drop_rando.removeAttribute("disabled")
            non_item_rando_warning.setAttribute("hidden", "hidden")
            if shops_in_pool:
                shared_shop_warning.setAttribute("hidden", "hidden")
                if shockwave.selected is True:
                    document.getElementById("shockwave_status_shuffled_decoupled").selected = True
                if move_vanilla.selected is True or move_rando.selected is True:
                    document.getElementById("move_on_cross_purchase").selected = True
                shockwave.setAttribute("disabled", "disabled")
                move_vanilla.setAttribute("disabled", "disabled")
                move_rando.setAttribute("disabled", "disabled")
                smaller_shops.removeAttribute("disabled")
                # Prevent UI breaking if Vanilla/Unlock All moves was selected before selection Shops in Item Rando
                js.document.getElementById("shockwave_status").removeAttribute("disabled")
                js.document.getElementById("random_prices").removeAttribute("disabled")
            if kongs_in_pool:
                kong_rando.setAttribute("disabled", "disabled")
                kong_rando.checked = True
            else:
                kong_rando.removeAttribute("disabled")
    except AttributeError as e:
        pass


@bind("click", "item_rando_list_select_all")
@bind("click", "item_rando_list_reset")
@bind("click", "item_rando_list_selected")
def item_rando_list_changed(evt):
    """Enable and disable settings based on the Item Rando pool changing."""
    item_rando_disabled = True
    item_rando_pool = document.getElementById("item_rando_list_selected").options
    shockwave = document.getElementById("shockwave_status_shuffled")
    smaller_shops = document.getElementById("smaller_shops")
    move_vanilla = document.getElementById("move_off")
    move_rando = document.getElementById("move_on")
    shared_shop_warning = document.getElementById("shared_shop_warning")
    kong_rando = document.getElementById("kong_rando")
    shops_in_pool = False
    kongs_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
        if option.value == "kong":
            if option.selected:
                kongs_in_pool = True
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
        kongs_in_pool = True
    if js.document.getElementById("shuffle_items").checked:
        item_rando_disabled = False
    if shops_in_pool and not item_rando_disabled:
        # Prevent camera/shockwave from being coupled and enable smaller shops if shops are in the pool
        shared_shop_warning.setAttribute("hidden", "hidden")
        if shockwave.selected is True:
            document.getElementById("shockwave_status_shuffled_decoupled").selected = True
        if move_vanilla.selected is True or move_rando.selected is True:
            document.getElementById("move_on_cross_purchase").selected = True
        shockwave.setAttribute("disabled", "disabled")
        move_vanilla.setAttribute("disabled", "disabled")
        move_rando.setAttribute("disabled", "disabled")
        smaller_shops.removeAttribute("disabled")
        # Prevent UI breaking if Vanilla/Unlock All moves was selected before selection Shops in Item Rando
        js.document.getElementById("shockwave_status").removeAttribute("disabled")
        js.document.getElementById("random_prices").removeAttribute("disabled")
    else:
        # Enable coupled camera/shockwave and disable smaller shops if shops are not in the pool
        shared_shop_warning.removeAttribute("hidden")
        shockwave.removeAttribute("disabled")
        move_vanilla.removeAttribute("disabled")
        move_rando.removeAttribute("disabled")
        smaller_shops.setAttribute("disabled", "disabled")
        smaller_shops.checked = False
    if kongs_in_pool and not item_rando_disabled:
        kong_rando.setAttribute("disabled", "disabled")
        kong_rando.checked = True
    else:
        kong_rando.removeAttribute("disabled")
    plando_disable_arena_custom_locations(None)
    plando_disable_crate_custom_locations(None)
    plando_disable_fairy_custom_locations(None)
    plando_disable_kasplat_custom_locations(None)
    plando_disable_patch_custom_locations(None)
    plando_disable_wrinkly_custom_locations(None)
    plando_disable_tns_custom_locations(None)


def should_reset_select_on_preset(selectElement):
    """Return true if the element should be reset when applying a preset."""
    if js.document.querySelector("#nav-cosmetics").contains(selectElement):
        return False
    if js.document.querySelector("#nav-music").contains(selectElement) is True:
        return False
    if selectElement.name.startswith("plando_"):
        return False
    # This should now be obsolete, because of the #nav-music clause, but I really don't feel like trying my luck
    # TODO: change the plando_ clause into a #nav-plando clause and remove the music_select_clause
    if selectElement.name.startswith("music_select_"):
        return False
    if selectElement.id == "random-weights":
        return False
    return True


@bind("click", "apply_preset")
def preset_select_changed(event):
    """Trigger a change of the form via the JSON templates."""
    element = document.getElementById("presets")
    presets = None
    for val in js.progression_presets:
        if val.get("name") == element.value:
            presets = val
    # if presets is None:
    #     js.generateToast()
    #     return
    if presets is not None and "settings_string" in presets:
        # Pass in setting string
        js.generateToast(f"\"{presets['name']}\" preset applied.<br />All non-cosmetic settings have been overwritten.")
        settings = decrypt_settings_string_enum(presets["settings_string"])
        for select in js.document.getElementsByTagName("select"):
            if should_reset_select_on_preset(select):
                select.selectedIndex = -1
        # Uncheck all starting move radio buttons for the import to then set them correctly
        for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
            starting_move_button.checked = False
        js.document.getElementById("presets").selectedIndex = 0
        for key in settings:
            try:
                if type(settings[key]) is bool:
                    if settings[key] is False:
                        js.jq(f"#{key}").checked = False
                        js.document.getElementsByName(key)[0].checked = False
                    else:
                        js.jq(f"#{key}").checked = True
                        js.document.getElementsByName(key)[0].checked = True
                    js.jq(f"#{key}").removeAttr("disabled")
                elif type(settings[key]) is list:
                    if key in ("starting_move_list_selected", "random_starting_move_list_selected"):
                        for item in settings[key]:
                            radio_buttons = js.document.getElementsByName("starting_move_box_" + str(int(item)))
                            if key == "starting_move_list_selected":
                                start_button = [button for button in radio_buttons if button.id.startswith("start")][0]
                                start_button.checked = True
                            else:
                                random_button = [button for button in radio_buttons if button.id.startswith("random")][0]
                                random_button.checked = True
                        continue
                    selector = js.document.getElementById(key)
                    if selector.tagName == "SELECT":
                        for item in settings[key]:
                            for option in selector.options:
                                if option.value == item.name:
                                    option.selected = True
                else:
                    selector = js.document.getElementById(key)
                    # If the selector is a select box, set the selectedIndex to the value of the option
                    if selector.tagName == "SELECT":
                        for option in selector.options:
                            if option.value == SettingsMap[key](settings[key]).name:
                                # Set the value of the select box to the value of the option
                                option.selected = True
                                break
                    else:
                        js.jq(f"#{key}").val(settings[key])
                    js.jq(f"#{key}").removeAttr("disabled")
            except Exception as e:
                print(e)
                pass
    else:
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
                elif type(presets[key]) is list:
                    selector = js.document.getElementById(key)
                    for i in range(0, selector.options.length):
                        selector.item(i).selected = selector.item(i).value in presets[key]
                else:
                    js.jq(f"#{key}").val(presets[key])
                    js.jq(f"#{key}").removeAttr("disabled")
            except Exception as e:
                pass
    update_ui_states(None)
    js.savesettings()


@bind("custom-update-ui-event", "apply_preset")
def update_ui_states(event):
    """Trigger any function that would update the status of a UI element based on the current settings configuration."""
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    change_level_randomization(None)
    disable_colors(None)
    disable_music(None)
    disable_move_shuffles(None)
    max_randomized_blocker(None)
    handle_progressive_hint_text(None)
    handle_chaos_ratio_text(None)
    max_randomized_troff(None)
    max_music(None)
    max_music_proportion(None)
    max_sfx(None)
    disable_barrel_modal(None)
    item_rando_list_changed(None)
    toggle_item_rando(None)
    disable_enemy_modal(None)
    disable_hard_mode_modal(None)
    disable_hard_bosses_modal(None)
    disable_excluded_songs_modal(None)
    disable_music_filtering_modal(None)
    toggle_bananaport_selector(None)
    disable_helm_hurry(None)
    disable_remove_barriers(None)
    disable_faster_checks(None)
    toggle_logic_type(None)
    toggle_key_settings(None)
    max_starting_moves_count(None)
    updateDoorOneNumAccess(None)
    updateDoorTwoNumAccess(None)
    updateWinConNumAccess(None)
    disable_tag_spawn(None)
    disable_krool_phases(None)
    disable_helm_phases(None)
    enable_plandomizer(None)
    toggle_medals_box(None)
    toggle_extreme_prices_option(None)
    toggle_vanilla_door_rando(None)
    sliders = js.document.getElementsByClassName("pretty-slider")
    for s in range(len(sliders)):
        event = js.document.createEvent("HTMLEvents")
        event.initEvent("change", True, False)
        sliders[s].dispatchEvent(event)


@bind("click", "enable_plandomizer")
def enable_plandomizer(evt):
    """Enable and disable the Plandomizer tab."""
    disabled = True
    plando_tab = js.document.getElementById("nav-plando-tab")
    if js.document.getElementById("enable_plandomizer").checked:
        disabled = False
    try:
        if disabled:
            plando_tab.style.display = "none"
        else:
            plando_tab.style = ""
    except AttributeError:
        pass


@bind("change", "plando_starting_kongs_selected")
def plando_disable_kong_items(evt):
    """Do not allow starting Kongs to be placed as items."""
    starting_kongs = js.document.getElementById("plando_starting_kongs_selected")
    selected_kongs = {x.value for x in starting_kongs.selectedOptions}
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    for kong in ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]:
        if kong.lower() in selected_kongs:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Disable this Kong as a dropdown option.
            for option in kong_options:
                option.setAttribute("disabled", "disabled")
            # De-select this Kong everywhere they are selected.
            for dropdown in item_dropdowns:
                if dropdown.value == kong:
                    dropdown.value = ""
        else:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Re-enable this Kong as a dropdown option.
            for option in kong_options:
                option.removeAttribute("disabled")


startingMoveValues = [str(item.value) for item in StartingMoveOptions]


@bindList("click", startingMoveValues, prefix="none-")
@bindList("click", startingMoveValues, prefix="start-")
@bindList("click", startingMoveValues, prefix="random-")
def plando_disable_starting_moves(evt):
    """Do not allow starting moves to be placed as items."""
    # Create a list of selected starting moves.
    selectedStartingMoves = set()
    for startingMove in startingMoveValues:
        selectedElem = js.document.getElementById(f"start-{startingMove}")
        if selectedElem.checked:
            selectedStartingMoves.add(Items(int(startingMove)))

    # Obtain the list of PlandoItems moves to disable.
    progressiveMoves = [PlandoItems.ProgressiveAmmoBelt, PlandoItems.ProgressiveInstrumentUpgrade, PlandoItems.ProgressiveSlam]
    selectedPlandoMoves = set([ItemToPlandoItemMap[move] for move in selectedStartingMoves if ItemToPlandoItemMap[move] not in progressiveMoves])
    # Progressive moves are handled differently. Only disable these if all
    # instances are included as starting moves.
    if set([Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveSlam)
    if set([Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveAmmoBelt)
    if set([Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveInstrumentUpgrade)

    # Disable all the plando moves across the dropdowns.
    for moveName in MoveSet:
        moveEnum = PlandoItems[moveName]
        # Ignore these moves.
        if moveEnum in {PlandoItems.Camera, PlandoItems.Shockwave}:
            continue
        move_options = js.document.getElementsByClassName(f"plando-{moveName}-option")
        if moveEnum in selectedPlandoMoves:
            # Disable this move as a dropdown option.
            for option in move_options:
                option.setAttribute("disabled", "disabled")
        else:
            # Re-enable this move as a dropdown option.
            for option in move_options:
                option.removeAttribute("disabled")
    # Deselect all the plando moves across the dropdowns.
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    for dropdown in item_dropdowns:
        if dropdown.value == "":
            continue
        move = PlandoItems[dropdown.value]
        if move in selectedPlandoMoves:
            dropdown.value = ""


@bind("click", "random_medal_requirement")
def toggle_medals_box(event):
    """Toggle the textbox for Banana Medals."""
    disabled = False
    if js.document.getElementById("random_medal_requirement").checked:
        disabled = True
    medal = js.document.getElementById("medal_requirement")
    if disabled:
        medal.setAttribute("disabled", "disabled")
    else:
        medal.removeAttribute("disabled")


@bind("change", "shockwave_status")
def toggle_extreme_prices_option(event):
    """Determine the visibility of the extreme prices option."""
    unlocked_shockwave = document.getElementById("shockwave_status").value == "start_with"
    logic_disabled = document.getElementById("logic_type").value == "nologic"
    option = document.getElementById("extreme_price_option")
    if unlocked_shockwave or logic_disabled:
        option.removeAttribute("disabled")
    else:
        option.setAttribute("disabled", "disabled")
        price_option = document.getElementById("random_prices")
        if price_option.value == "extreme":
            price_option.value = "high"


@bind("change", "shockwave_status")
def plando_disable_camera_shockwave(evt):
    """Disable placement of camera/shockwave if they are not shuffled."""
    shockwave_status = document.getElementById("shockwave_status").value
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    move_options = js.document.getElementsByClassName(f"plando-camera-shockwave-option")
    disabled = shockwave_status == "start_with" or shockwave_status == "vanilla"
    if disabled:
        # Disable Camera and Shockwave dropdown options.
        for option in move_options:
            option.setAttribute("disabled", "disabled")
        # Remove these items anywhere they've been selected.
        for dropdown in item_dropdowns:
            if dropdown.value == "Camera" or dropdown.value == "Shockwave":
                dropdown.value = ""
    else:
        # Re-enable Camera and Shockwave dropdown options.
        for option in move_options:
            option.removeAttribute("disabled")


@bind("change", "logic_type")
def toggle_logic_type(event):
    """Toggle settings based on the presence of logic."""
    toggle_extreme_prices_option(event)
    glitch_customization = document.getElementById("glitches_modal")
    if document.getElementById("logic_type").value == "glitch":
        glitch_customization.removeAttribute("disabled")
    else:
        glitch_customization.setAttribute("disabled", "disabled")


@bind("change", "bananaport_placement_rando")
def toggle_bananaport_selector(event):
    """Toggle bananaport settings if shuffling is enabled."""
    bananaport_customization = document.getElementById("warp_level_list_modal")
    if document.getElementById("bananaport_placement_rando").value != "off":
        bananaport_customization.removeAttribute("disabled")
    else:
        bananaport_customization.setAttribute("disabled", "disabled")


@bind("click", "nav-patch-tab")
def toggle_patch_ui(event):
    """Disable non-cosmetic tabs if using patch file."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).setAttribute("disabled", "disabled")
    document.getElementById("override_div").removeAttribute("hidden")
    document.getElementById("nav-cosmetics-tab").click()


@bind("click", "nav-seed-gen-tab")
def toggle_patch_ui(event):
    """Re-enable non-cosmetic tabs and hide override option if generating a new seed."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).removeAttribute("disabled")
    document.getElementById("override_div").setAttribute("hidden", "hidden")
    document.getElementById("override_cosmetics").checked = True


@bind("click", "nav-pastgen-tab")
def hide_override_cosmetics(event):
    """Hide the override cosmetics setting when clicking the Generate from Past Seed button."""
    document.getElementById("override_div").setAttribute("hidden", "hidden")
    document.getElementById("override_cosmetics").checked = True


@bind("change", "music_bgm_randomized")
def rename_default_bgm_options(evt):
    """Change between "Default" and "Randomizer" for BGM Music."""
    toggleElem = js.document.getElementById("music_bgm_randomized")
    selects = js.document.getElementsByClassName("BGM-select")
    if toggleElem.checked:
        for select in selects:
            if select.value == "default_value":
                select.value = ""
    else:
        for select in selects:
            if select.value == "":
                select.value = "default_value"
    js.savemusicsettings()


@bind("change", "music_majoritems_randomized")
def rename_default_majoritems_options(evt):
    """Change between "Default" and "Randomize" for major item music selection."""
    toggleElem = js.document.getElementById(f"music_majoritems_randomized")
    selects = js.document.getElementsByClassName(f"MajorItem-select")
    if toggleElem.checked:
        for select in selects:
            if select.value == "default_value":
                select.value = ""
    else:
        for select in selects:
            if select.value == "":
                select.value = "default_value"
    js.savemusicsettings()


@bind("change", "music_minoritems_randomized")
def rename_default_minoritems_options(evt):
    """Change between "Default" and "Randomize" for minor item music selection."""
    toggleElem = js.document.getElementById(f"music_minoritems_randomized")
    selects = js.document.getElementsByClassName(f"MinorItem-select")
    if toggleElem.checked:
        for select in selects:
            if select.value == "default_value":
                select.value = ""
    else:
        for select in selects:
            if select.value == "":
                select.value = "default_value"
    js.savemusicsettings()


@bind("change", "music_events_randomized")
def rename_default_events_options(evt):
    """Change between "Default" and "Randomize" for event music selection."""
    toggleElem = js.document.getElementById(f"music_events_randomized")
    selects = js.document.getElementsByClassName(f"Event-select")
    if toggleElem.checked:
        for select in selects:
            if select.value == "default_value":
                select.value = ""
    else:
        for select in selects:
            if select.value == "":
                select.value = "default_value"
    js.savemusicsettings()


@bind("click", "select_keys")
def toggle_key_settings(event):
    """Disable other keys settings when selecting keys. Toggle Key Selector Modal."""
    disabled = False
    if js.document.getElementById("select_keys").checked:
        disabled = True
    selector = js.document.getElementById("starting_keys_list_modal")
    if disabled:
        selector.removeAttribute("disabled")
    else:
        selector.setAttribute("disabled", "disabled")


@bind("click", "key_8_helm")
@bind("click", "select_keys")
@bind("click", "starting_keys_list_selected")
def plando_disable_keys(evt):
    """Disable keys from being selected for locations in the plandomizer, depending on the current settings."""
    # This dict will map our key strings to enum values.
    keyDict = {1: "JungleJapesKey", 2: "AngryAztecKey", 3: "FranticFactoryKey", 4: "GloomyGalleonKey", 5: "FungiForestKey", 6: "CrystalCavesKey", 7: "CreepyCastleKey", 8: "HideoutHelmKey"}
    # Determine which keys are enabled and which are disabled.
    disabled_keys = set()
    if js.document.getElementById("select_keys").checked:
        starting_keys_list_selected = js.document.getElementById("starting_keys_list_selected")
        # All keys the user starts with are disabled.
        disabled_keys.update({x.value for x in starting_keys_list_selected.selectedOptions})
    # If Key 8 is locked in Helm, it gets disabled.
    if js.document.getElementById("key_8_helm").checked:
        disabled_keys.add("HideoutHelmKey")
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    # Look at every key and react if it's enabled or disabled.
    for i in range(1, 9):
        key_string = keyDict[i]
        if key_string in disabled_keys:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Disable this key as a dropdown option.
            for option in key_options:
                option.setAttribute("disabled", "disabled")
            # De-select this key everywhere it is selected.
            for dropdown in item_dropdowns:
                if dropdown.value == key_string:
                    dropdown.value = ""
        else:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Re-enable this key as a dropdown option.
            for option in key_options:
                option.removeAttribute("disabled")


@bind("click", "helm_hurry")
def disable_helm_hurry(evt):
    """Disable Helm Hurry Selector when Helm Hurry is off."""
    disabled = True
    selector = js.document.getElementById("helmhurry_list_modal")
    if js.document.getElementById("helm_hurry").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "remove_barriers_enabled")
def disable_remove_barriers(evt):
    """Disable Remove Barriers Selector when Remove Barriers is off."""
    disabled = True
    selector = js.document.getElementById("remove_barriers_modal")
    if js.document.getElementById("remove_barriers_enabled").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "faster_checks_enabled")
def disable_faster_checks(evt):
    """Disable Faster Checks Selector when Faster Checks is off."""
    disabled = True
    selector = js.document.getElementById("faster_checks_modal")
    if js.document.getElementById("faster_checks_enabled").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "vanilla_door_rando")
def toggle_vanilla_door_rando(evt):
    """Force Wrinkly and T&S Rando to be on when Vanilla Door Rando is on."""
    vanilla_door_shuffle = js.document.getElementById("vanilla_door_rando")
    wrinkly_rando = js.document.getElementById("wrinkly_location_rando")
    tns_rando = js.document.getElementById("tns_location_rando")
    if vanilla_door_shuffle.checked:
        wrinkly_rando.checked = True
        wrinkly_rando.setAttribute("disabled", "disabled")
        tns_rando.checked = True
        tns_rando.setAttribute("disabled", "disabled")
    else:
        wrinkly_rando.removeAttribute("disabled")
        tns_rando.removeAttribute("disabled")


@bind("click", "starting_moves_reset")
def reset_starting_moves(evt):
    """Reset the starting move selector to have nothing selected."""
    for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
        starting_move_button.checked = starting_move_button.id.startswith("none")
    # Update the plandomizer dropdowns.
    plando_disable_starting_moves(evt)


@bind("click", "starting_moves_start_all")
def start_all_starting_moves(evt):
    """Update the starting move selector to start with all items."""
    for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
        starting_move_button.checked = starting_move_button.id.startswith("start")
    # Update the plandomizer dropdowns.
    plando_disable_starting_moves(evt)


@bind("click", "randomize_settings")
def shuffle_settings(evt):
    """Randomize all non-cosmetic settings."""
    js.generateToast(f"Randomizing settings ({js.document.getElementById('random-weights').value}).<br>All non-cosmetic settings have been overwritten.")
    randomize_settings()

    # Run additional functions to ensure there are no conflicts.
    update_ui_states(evt)


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


@bind("click", "plando_toggle_color_table")
def toggle_plando_hint_color_table(evt):
    """Show or hide the table that shows possible hint colors."""
    hintColorTable = js.document.getElementById("plando_hint_color_table")
    hintColorTable.classList.toggle("hidden")


@bind("click", "plando_place_arenas")
@bind("click", "plando_place_patches")
@bind("click", "plando_place_fairies")
@bind("click", "plando_place_kasplats")
@bind("click", "plando_place_crates")
@bind("click", "plando_place_wrinkly")
@bind("click", "plando_place_tns")
def plando_toggle_custom_locations_tab(evt):
    """Show/hide the Custom Locations tab."""
    tabElem = js.document.getElementById("nav-plando-Locations-tab")
    arenasEnabled = js.document.getElementById("plando_place_arenas").checked
    patchesEnabled = js.document.getElementById("plando_place_patches").checked
    fairiesEnabled = js.document.getElementById("plando_place_fairies").checked
    kasplatsEnabled = js.document.getElementById("plando_place_kasplats").checked
    cratesEnabled = js.document.getElementById("plando_place_crates").checked
    wrinklyEnabled = js.document.getElementById("plando_place_wrinkly").checked
    tnsEnabled = js.document.getElementById("plando_place_tns").checked
    if arenasEnabled or patchesEnabled or fairiesEnabled or kasplatsEnabled or cratesEnabled or wrinklyEnabled or tnsEnabled:
        tabElem.style = ""
    else:
        tabElem.style.display = "none"


@bind("click", "plando_place_arenas")
def plando_toggle_custom_arena_locations(evt):
    """Show/hide custom arena locations in the plandomizer."""
    arenaElem = js.document.getElementById("plando_custom_location_panel_arena")
    if js.document.getElementById("plando_place_arenas").checked:
        arenaElem.style = ""
    else:
        arenaElem.style.display = "none"


@bind("click", "plando_place_patches")
def plando_toggle_custom_patch_locations(evt):
    """Show/hide custom patch locations in the plandomizer."""
    patchElem = js.document.getElementById("plando_custom_location_panel_patch")
    if js.document.getElementById("plando_place_patches").checked:
        patchElem.style = ""
    else:
        patchElem.style.display = "none"


@bind("click", "plando_place_fairies")
def plando_toggle_custom_fairy_locations(evt):
    """Show/hide custom fairy locations in the plandomizer."""
    fairyElem = js.document.getElementById("plando_custom_location_panel_fairy")
    if js.document.getElementById("plando_place_fairies").checked:
        fairyElem.style = ""
    else:
        fairyElem.style.display = "none"


@bind("click", "plando_place_kasplats")
def plando_toggle_custom_kasplat_locations(evt):
    """Show/hide custom Kasplat locations in the plandomizer."""
    kasplatElem = js.document.getElementById("plando_custom_location_panel_kasplat")
    if js.document.getElementById("plando_place_kasplats").checked:
        kasplatElem.style = ""
    else:
        kasplatElem.style.display = "none"


@bind("click", "plando_place_crates")
def plando_toggle_custom_crate_locations(evt):
    """Show/hide custom crate locations in the plandomizer."""
    crateElem = js.document.getElementById("plando_custom_location_panel_crate")
    if js.document.getElementById("plando_place_crates").checked:
        crateElem.style = ""
    else:
        crateElem.style.display = "none"


@bind("click", "plando_place_wrinkly")
def plando_toggle_custom_wrinkly_locations(evt):
    """Show/hide custom Wrinkly door locations in the plandomizer."""
    wrinklyElem = js.document.getElementById("plando_custom_location_panel_wrinkly_door")
    if js.document.getElementById("plando_place_wrinkly").checked:
        wrinklyElem.style = ""
    else:
        wrinklyElem.style.display = "none"


@bind("click", "plando_place_tns")
def plando_toggle_custom_tns_locations(evt):
    """Show/hide custom TnS portal locations in the plandomizer."""
    tnsElem = js.document.getElementById("plando_custom_location_panel_tns_portal")
    if js.document.getElementById("plando_place_tns").checked:
        tnsElem.style = ""
    else:
        tnsElem.style.display = "none"


@bind("click", "crown_placement_rando")
def plando_disable_arena_custom_locations(evt):
    """Enable or disable custom locations for battle arenas."""
    itemRandoPool = document.getElementById("item_rando_list_selected").options
    crownsShuffled = False
    for option in itemRandoPool:
        if option.value == "crown":
            crownsShuffled = option.selected
    randomCrowns = js.document.getElementById("crown_placement_rando").checked
    customCrownsElem = js.document.getElementById("plando_place_arenas")
    tooltip = "Allows the user to specify locations for each battle arena."
    if crownsShuffled and randomCrowns:
        customCrownsElem.removeAttribute("disabled")
    else:
        customCrownsElem.setAttribute("disabled", "disabled")
        customCrownsElem.checked = False
        tooltip = "To use this feature, battle crowns must be in the item pool, and their locations must be shuffled."
    customCrownsElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("click", "random_crates")
def plando_disable_crate_custom_locations(evt):
    """Enable or disable custom locations for melon crates."""
    itemRandoPool = document.getElementById("item_rando_list_selected").options
    cratesShuffled = False
    for option in itemRandoPool:
        if option.value == "crateitem":
            cratesShuffled = option.selected
    randomCrates = js.document.getElementById("random_crates").checked
    customCratesElem = js.document.getElementById("plando_place_crates")
    tooltip = "Allows the user to specify locations for each melon crate."
    if cratesShuffled and randomCrates:
        customCratesElem.removeAttribute("disabled")
    else:
        customCratesElem.setAttribute("disabled", "disabled")
        customCratesElem.checked = False
        tooltip = "To use this feature, melon crates must be in the item pool, and their locations must be shuffled."
    customCratesElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("click", "random_fairies")
def plando_disable_fairy_custom_locations(evt):
    """Enable or disable custom locations for banana fairies."""
    itemRandoPool = document.getElementById("item_rando_list_selected").options
    fairiesShuffled = False
    for option in itemRandoPool:
        if option.value == "fairy":
            fairiesShuffled = option.selected
    randomFairies = js.document.getElementById("random_fairies").checked
    customFairiesElem = js.document.getElementById("plando_place_fairies")
    tooltip = "Allows the user to specify locations for each banana fairy."
    if fairiesShuffled and randomFairies:
        customFairiesElem.removeAttribute("disabled")
    else:
        customFairiesElem.setAttribute("disabled", "disabled")
        customFairiesElem.checked = False
        tooltip = "To use this feature, fairies must be in the item pool, and their locations must be shuffled."
    customFairiesElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("change", "kasplat_rando_setting")
def plando_disable_kasplat_custom_locations(evt):
    """Enable or disable custom locations for Kasplats."""
    itemRandoPool = document.getElementById("item_rando_list_selected").options
    kasplatsShuffled = False
    for option in itemRandoPool:
        if option.value == "blueprint":
            kasplatsShuffled = option.selected
    kasplatShuffle = js.document.getElementById("kasplat_rando_setting").value
    customKasplatsElem = js.document.getElementById("plando_place_kasplats")
    tooltip = "Allows the user to specify locations for each Kasplat."
    if kasplatsShuffled and kasplatShuffle == "location_shuffle":
        customKasplatsElem.removeAttribute("disabled")
    else:
        customKasplatsElem.setAttribute("disabled", "disabled")
        customKasplatsElem.checked = False
        tooltip = "To use this feature, blueprints must be in the item pool, and Kasplat locations must be shuffled."
    customKasplatsElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("click", "random_patches")
def plando_disable_patch_custom_locations(evt):
    """Enable or disable custom locations for dirt patches."""
    itemRandoPool = document.getElementById("item_rando_list_selected").options
    patchesShuffled = False
    for option in itemRandoPool:
        if option.value == "rainbowcoin":
            patchesShuffled = option.selected
    randomPatches = js.document.getElementById("random_patches").checked
    customPatchesElem = js.document.getElementById("plando_place_patches")
    tooltip = "Allows the user to specify locations for each dirt patch."
    if patchesShuffled and randomPatches:
        customPatchesElem.removeAttribute("disabled")
    else:
        customPatchesElem.setAttribute("disabled", "disabled")
        customPatchesElem.checked = False
        tooltip = "To use this feature, rainbow coins must be in the item pool, and dirt patch locations must be shuffled."
    customPatchesElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("click", "enable_progressive_hints")
@bind("click", "wrinkly_location_rando")
def plando_disable_wrinkly_custom_locations(evt):
    """Enable or disable custom locations for Wrinkly doors."""
    randomDoors = js.document.getElementById("wrinkly_location_rando").checked
    progressiveHints = js.document.getElementById("enable_progressive_hints").checked
    customWrinklyElem = js.document.getElementById("plando_place_wrinkly")
    tooltip = "Allows the user to specify locations for each Wrinkly door."
    if randomDoors and not progressiveHints:
        customWrinklyElem.removeAttribute("disabled")
    else:
        customWrinklyElem.setAttribute("disabled", "disabled")
        customWrinklyElem.checked = False
        tooltip = "To use this feature, Wrinkly door locations must be shuffled, and progressive hints must be turned off."
    customWrinklyElem.parentElement.setAttribute("data-bs-original-title", tooltip)


@bind("click", "tns_location_rando")
def plando_disable_tns_custom_locations(evt):
    """Enable or disable custom locations for Wrinkly doors."""
    randomPortals = js.document.getElementById("tns_location_rando").checked
    customTnsElem = js.document.getElementById("plando_place_tns")
    tooltip = "Allows the user to specify locations for each Troff 'n' Scoff portal."
    if randomPortals:
        customTnsElem.removeAttribute("disabled")
    else:
        customTnsElem.setAttribute("disabled", "disabled")
        customTnsElem.checked = False
        tooltip = "To use this feature, Troff 'n' Scoff portal locations must be shuffled."
    customTnsElem.parentElement.setAttribute("data-bs-original-title", tooltip)
