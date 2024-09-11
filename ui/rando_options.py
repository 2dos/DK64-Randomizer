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
    js.toggle_counts_boxes(None)
    js.toggle_b_locker_boxes(None)
    toggle_logic_type(None)
    js.toggle_bananaport_selector(None)
    js.updateDoorOneNumAccess(None)
    js.updateDoorTwoNumAccess(None)
    js.updateWinConNumAccess(None)

    js.load_data()


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
    js.toggle_counts_boxes(None)
    js.toggle_b_locker_boxes(None)
    js.change_level_randomization(None)
    js.disable_colors(None)
    js.disable_music(None)
    js.disable_move_shuffles(None)
    js.max_randomized_blocker(None)
    js.handle_progressive_hint_text(None)
    js.handle_chaos_ratio_text(None)
    js.max_randomized_troff(None)
    js.max_music(None)
    js.max_music_proportion(None)
    js.max_sfx(None)
    js.disable_barrel_modal(None)
    js.item_rando_list_changed(None)
    js.toggle_item_rando(None)
    js.disable_enemy_modal(None)
    js.disable_hard_mode_modal(None)
    js.disable_hard_bosses_modal(None)
    js.disable_excluded_songs_modal(None)
    js.disable_music_filtering_modal(None)
    js.toggle_bananaport_selector(None)
    js.disable_helm_hurry(None)
    js.disable_remove_barriers(None)
    js.disable_faster_checks(None)
    toggle_logic_type(None)
    js.toggle_key_settings(None)
    js.max_starting_moves_count(None)
    js.updateDoorOneNumAccess(None)
    js.updateDoorTwoNumAccess(None)
    js.updateWinConNumAccess(None)
    js.disable_tag_spawn(None)
    js.disable_krool_phases(None)
    js.disable_helm_phases(None)
    js.enable_plandomizer(None)
    js.toggle_medals_box(None)
    js.toggle_extreme_prices_option(None)
    js.toggle_vanilla_door_rando(None)
    js.validate_fast_start_status(None)
    sliders = js.document.getElementsByClassName("pretty-slider")
    for s in range(len(sliders)):
        event = js.document.createEvent("HTMLEvents")
        event.initEvent("change", True, False)
        sliders[s].dispatchEvent(event)


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


@bind("change", "logic_type")
def toggle_logic_type(event):
    """Toggle settings based on the presence of logic."""
    js.toggle_extreme_prices_option(event)
    glitch_customization = document.getElementById("glitches_modal")
    if document.getElementById("logic_type").value == "glitch":
        glitch_customization.removeAttribute("disabled")
    else:
        glitch_customization.setAttribute("disabled", "disabled")


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
