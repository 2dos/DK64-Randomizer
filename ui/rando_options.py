"""Options for the main rando tab."""

import random
import re

import js
from randomizer.Enums.Items import Items
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Lists.Item import StartingMoveOptions
from randomizer.Lists.Songs import MusicSelectionPanel
from randomizer.PlandoUtils import MoveSet
from ui.bindings import bind, bindList
from ui.randomize_settings import randomize_settings

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
