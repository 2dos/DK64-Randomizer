"""Options for the main rando tab."""
import random

import js
from js import document
from randomizer.Enums.Settings import SettingsMap
from randomizer.SettingStrings import decrypt_settings_string_enum
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


@bind("focusout", "starting_moves_count")
def max_starting_moves_count(event):
    """Validate starting moves count input on loss of focus."""
    move_count = js.document.getElementById("starting_moves_count")
    if not move_count.value:
        move_count.value = 4
    elif 0 > int(move_count.value):
        move_count.value = 0
    elif int(move_count.value) > 40:
        move_count.value = 40


@bind("change", "crown_door_item")
def updateDoorOneNumAccess(event):
    """Toggle the textboxes for the first helm door."""
    door_one_selection = js.document.getElementById("crown_door_item")
    disabled = (door_one_selection.value == "random") or (door_one_selection.value == "opened")
    door_one_req = js.document.getElementById("crown_door_item_count")
    if disabled:
        door_one_req.setAttribute("disabled", "disabled")
    else:
        door_one_req.removeAttribute("disabled")
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


@bind("click", "nav-progression-tab")
@bind("change", "crown_door_item")
def updateDoorOneCountText(evt):
    """Change the text of the door 1 item count label."""
    label_text_map = {
        "vanilla": "Crowns",
        "req_gb": "Bananas",
        "req_bp": "Blueprints",
        "req_companycoins": "Coins",
        "req_key": "Keys",
        "req_medal": "Medals",
        "req_fairy": "Fairies",
        "req_rainbowcoin": "Coins",
        "req_bean": "Bean",
        "req_pearl": "Pearls",
    }
    door_one_text = js.document.getElementById("door-1-select-title")
    door_one_selection = js.document.getElementById("crown_door_item").value
    if door_one_selection in label_text_map:
        door_one_text.innerText = f"{label_text_map[door_one_selection]} Needed For Door 1"
    else:
        door_one_text.innerText = "Door 1 Item Count"


@bind("change", "coin_door_item")
def updateDoorTwoNumAccess(event):
    """Toggle the textboxes for the second helm door."""
    door_two_selection = js.document.getElementById("coin_door_item")
    disabled = (door_two_selection.value == "random") or (door_two_selection.value == "opened")
    door_two_req = js.document.getElementById("coin_door_item_count")
    if disabled:
        door_two_req.setAttribute("disabled", "disabled")
    else:
        door_two_req.removeAttribute("disabled")
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


@bind("click", "nav-progression-tab")
@bind("change", "coin_door_item")
def updateDoorTwoCountText(evt):
    """Change the text of the door 2 item count label."""
    label_text_map = {
        "vanilla": "Coins",
        "req_gb": "Bananas",
        "req_bp": "Blueprints",
        "req_key": "Keys",
        "req_medal": "Medals",
        "req_crown": "Crowns",
        "req_fairy": "Fairies",
        "req_rainbowcoin": "Coins",
        "req_bean": "Bean",
        "req_pearl": "Pearls",
    }
    door_two_text = js.document.getElementById("door-2-select-title")
    door_two_selection = js.document.getElementById("coin_door_item").value
    if door_two_selection in label_text_map:
        door_two_text.innerText = f"{label_text_map[door_two_selection]} Needed For Door 2"
    else:
        door_two_text.innerText = "Door 2 Item Count"


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
def update_boss_required(evt):
    """Disable certain page flags depending on checkboxes."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    moves = document.getElementById("move_off")
    hard_level_progression = document.getElementById("hard_level_progression")
    if level.value == "level_order":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.setAttribute("disabled", "disabled")
        kong_rando.checked = True
        if moves.selected is True:
            document.getElementById("move_on").selected = True
        moves.setAttribute("disabled", "disabled")
        hard_level_progression.removeAttribute("disabled")
    elif level.value == "vanilla" and kong_rando.checked:
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.removeAttribute("disabled")
        moves.removeAttribute("disabled")
        hard_level_progression.setAttribute("disabled", "disabled")
        hard_level_progression.checked = False
    else:
        try:
            boss_kong.removeAttribute("disabled")
            boss_location.removeAttribute("disabled")
            kong_rando.removeAttribute("disabled")
            moves.removeAttribute("disabled")
            hard_level_progression.setAttribute("disabled", "disabled")
            hard_level_progression.checked = False
        except Exception:
            pass


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
    for i in ["dk", "diddy", "tiny", "lanky", "chunky", "rambi", "enguarde"]:
        color = js.document.getElementById(f"{i}_colors")
        try:
            if disabled:
                color.setAttribute("disabled", "disabled")
            else:
                color.removeAttribute("disabled")
        except AttributeError:
            pass
    hide_rgb(None)


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
    """Disable K Rool options when Randomize All is selected."""
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


@bind("change", "move_rando")
def disable_move_shuffles(evt):
    """Disable some settings based on the move rando setting."""
    moves = js.document.getElementById("move_rando")
    prices = js.document.getElementById("random_prices")
    training_barrels = js.document.getElementById("training_barrels")
    shockwave_status = js.document.getElementById("shockwave_status")
    starting_moves_count = js.document.getElementById("starting_moves_count")
    try:
        if moves.value == "start_with":
            prices.setAttribute("disabled", "disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 40
            starting_moves_count.setAttribute("disabled", "disabled")
        elif moves.value == "off":
            prices.removeAttribute("disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 40
            starting_moves_count.setAttribute("disabled", "disabled")
        else:
            prices.removeAttribute("disabled")
            training_barrels.removeAttribute("disabled")
            shockwave_status.removeAttribute("disabled")
            starting_moves_count.removeAttribute("disabled")
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


@bind("click", "item_rando_list_select_all")
@bind("click", "item_rando_list_reset")
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
    shops_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
                break
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
    if js.document.getElementById("shuffle_items").checked:
        disabled = False
    try:
        if disabled:
            # Prevent item rando modal from opening and smaller shop setting
            selector.setAttribute("disabled", "disabled")
            smaller_shops.setAttribute("disabled", "disabled")
            smaller_shops.checked = False
            shockwave.removeAttribute("disabled")
            move_vanilla.removeAttribute("disabled")
            move_rando.removeAttribute("disabled")
        else:
            # Enable item rando modal, prevent shockwave/camera coupling, and enable smaller shops if it's in the pool
            selector.removeAttribute("disabled")
            if shops_in_pool:
                if shockwave.selected is True:
                    document.getElementById("shockwave_status_shuffled_decoupled").selected = True
                shockwave.setAttribute("disabled", "disabled")
                smaller_shops.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "item_rando_list_selected")
def item_rando_list_changed(evt):
    """Enable and disable settings based on the Item Rando pool changing."""
    item_rando_pool = document.getElementById("item_rando_list_selected").options
    shockwave = document.getElementById("shockwave_status_shuffled")
    smaller_shops = document.getElementById("smaller_shops")
    move_vanilla = document.getElementById("move_off")
    move_rando = document.getElementById("move_on")
    shops_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
                break
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
    if shops_in_pool:
        # Prevent camera/shockwave from being coupled and enable smaller shops if shops are in the pool
        if shockwave.selected is True:
            document.getElementById("shockwave_status_shuffled_decoupled").selected = True
        if move_vanilla.selected is True or move_rando.selected is True:
            document.getElementById("move_on_cross_purchase").selected = True
        shockwave.setAttribute("disabled", "disabled")
        move_vanilla.setAttribute("disabled", "disabled")
        move_rando.setAttribute("disabled", "disabled")
        smaller_shops.removeAttribute("disabled")
        # Prevent UI breaking if Vanilla/Unlock All moves was selected before selection Shops in Item Rando
        js.document.getElementById("training_barrels").removeAttribute("disabled")
        js.document.getElementById("shockwave_status").removeAttribute("disabled")
        js.document.getElementById("random_prices").removeAttribute("disabled")
    else:
        # Enable coupled camera/shockwave and disable smaller shops if shops are not in the pool
        shockwave.removeAttribute("disabled")
        move_vanilla.removeAttribute("disabled")
        move_rando.removeAttribute("disabled")
        smaller_shops.setAttribute("disabled", "disabled")
        smaller_shops.checked = False


@bind("click", "apply_preset")
def preset_select_changed(event):
    """Trigger a change of the form via the JSON templates."""
    element = document.getElementById("presets")
    presets = None
    for val in js.progression_presets:
        if val.get("name") == element.value:
            presets = val
    if presets is not None and "settings_string" in presets:
        # Pass in setting string
        settings = decrypt_settings_string_enum(presets["settings_string"])
        for select in js.document.getElementsByTagName("select"):
            if js.document.querySelector("#nav-cosmetics").contains(select) is False:
                select.selectedIndex = -1
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
                    selector = js.document.getElementById(key)
                    if selector.tagName == "SELECT":
                        for item in settings[key]:
                            for option in selector.options:
                                if option.value == item.name:
                                    option.selected = True
                else:
                    if js.document.getElementsByName(key)[0].hasAttribute("data-slider-value"):
                        js.jq(f"#{key}").slider("setValue", settings[key])
                        js.jq(f"#{key}").slider("enable")
                        js.jq(f"#{key}").parent().find(".slider-disabled").removeClass("slider-disabled")
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
    disable_move_shuffles(None)
    max_randomized_blocker(None)
    max_randomized_troff(None)
    max_music(None)
    max_sfx(None)
    disable_barrel_modal(None)


@bind("change", "dk_colors")
@bind("change", "diddy_colors")
@bind("change", "lanky_colors")
@bind("change", "tiny_colors")
@bind("change", "chunky_colors")
@bind("change", "rambi_colors")
@bind("change", "enguarde_colors")
def hide_rgb(event):
    """Show RGB Selector if Custom Color is selected."""
    for i in ["dk", "diddy", "lanky", "tiny", "chunky", "rambi", "enguarde"]:
        hidden = True
        color = js.document.getElementById(f"{i}_custom")
        if js.document.getElementById(f"{i}_colors").value == "custom":
            hidden = False
        try:
            if hidden or js.document.getElementById("random_colors").checked:
                color.style.display = "none"
            else:
                color.style = ""
        except AttributeError:
            pass


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


@bind("change", "logic_type")
def toggle_logic_type(event):
    """Toggle settings based on the presence of logic."""
    toggle_extreme_prices_option(event)
    glitch_customization = document.getElementById("glitches_modal")
    if document.getElementById("logic_type").value == "glitch":
        glitch_customization.removeAttribute("disabled")
    else:
        glitch_customization.setAttribute("disabled", "disabled")


@bind("change", "bananaport_rando")
def toggle_bananaport_selector(event):
    """Toggle bananaport settings if shuffling is enabled."""
    bananaport_customization = document.getElementById("warp_level_list_modal")
    if document.getElementById("bananaport_rando").value != "off":
        bananaport_customization.removeAttribute("disabled")
    else:
        bananaport_customization.setAttribute("disabled", "disabled")


@bind("click", "nav-patch-tab")
def toggle_patch_ui(event):
    """Disable non-cosmetic tabs if using patch file."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).setAttribute("disabled", "disabled")
    document.getElementById("nav-cosmetics-tab").click()


@bind("click", "nav-seed-gen-tab")
def toggle_patch_ui(event):
    """Re-enable non-cosmetic tabs and hide override option if generating a new seed."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).removeAttribute("disabled")
    document.getElementById("override_div").setAttribute("hidden", "hidden")


@bind("click", "select_keys")
def toggle_key_settings(event):
    """Disable other keys settings when selecting keys. Toggle Key Selector Modal."""
    disabled = False
    if js.document.getElementById("select_keys").checked:
        disabled = True
    krool_access = js.document.getElementById("krool_access")
    keys_random = js.document.getElementById("keys_random")
    selector = js.document.getElementById("starting_keys_list_modal")
    if disabled:
        krool_access.setAttribute("disabled", "disabled")
        krool_access.checked = False
        keys_random.setAttribute("disabled", "disabled")
        selector.removeAttribute("disabled")
    else:
        krool_access.removeAttribute("disabled")
        keys_random.removeAttribute("disabled")
        selector.setAttribute("disabled", "disabled")


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
