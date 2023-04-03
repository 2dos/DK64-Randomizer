"""File containing main UI button events that travel between tabs."""
import asyncio
import json
import random

from pyodide import create_proxy

import js
from randomizer.BackgroundRandomizer import generate_playthrough
from randomizer.Enums.Settings import SettingsMap
from randomizer.Patching.ApplyRandomizer import patching_response
from randomizer.SettingStrings import decrypt_settings_string_enum, encrypt_settings_string_enum
from randomizer.Worker import background
from ui.bindings import bind
from ui.progress_bar import ProgressBar
from ui.rando_options import (
    disable_barrel_modal,
    disable_colors,
    disable_music,
    disable_move_shuffles,
    max_randomized_blocker,
    max_randomized_troff,
    toggle_b_locker_boxes,
    updateDoorOneNumAccess,
    updateDoorTwoNumAccess,
    updateDoorOneCountText,
    updateDoorTwoCountText,
    toggle_counts_boxes,
    update_boss_required,
)


@bind("click", "export_settings")
def export_settings_string(event):
    """Click event for exporting settings to a string.

    Args:
        event (event): Javascript event object.
    """
    setting_data = serialize_settings()
    settings_string = encrypt_settings_string_enum(setting_data)
    js.settings_string.value = settings_string


@bind("click", "import_settings")
def import_settings_string(event):
    """Click event for importing settings from a string.

    Args:
        event (event): Javascript Event object.
    """
    settings_string = js.settings_string.value
    settings = decrypt_settings_string_enum(settings_string)
    # Clear all select boxes on the page so as long as its not in the nav-cosmetics div
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
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    update_boss_required(None)
    disable_colors(None)
    disable_music(None)
    disable_move_shuffles(None)
    max_randomized_blocker(None)
    max_randomized_troff(None)
    disable_barrel_modal(None)
    updateDoorOneCountText(None)
    updateDoorTwoCountText(None)


@bind("change", "patchfileloader")
def lanky_file_changed(event):
    """On the event of a lanky file being loaded.

    Args:
        event (event): Javascript event.
    """

    def onload(e):
        # Load the text of the patch
        loaded_patch = str(e.target.result)
        # TODO: Don't just assume the file is valid first
        js.document.getElementById("patchfileloader").classList.add("is-valid")
        js.loaded_patch = loaded_patch

    # Attempt to find what file was loaded
    file = None
    for uploaded_file in js.document.getElementById("patchfileloader").files:
        file = uploaded_file
        break
    reader = js.FileReader.new()
    # If we loaded a file, set up the event listener to wait for it to be loaded
    if file is not None:
        reader.readAsText(file)
        function = create_proxy(onload)
        reader.addEventListener("load", function)


@bind("click", "generate_pastgen_seed")
def generate_previous_seed(event):
    """Generate a seed from a previous seed file."""
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("rom").classList):
        js.document.getElementById("rom").select()
        if "is-invalid" not in list(js.document.getElementById("rom").classList):
            js.document.getElementById("rom").classList.add("is-invalid")
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ProgressBar().update_progress(0, "Loading Previous seed and applying data."))
        js.apply_bps_javascript()
        patching_response(str(js.get_previous_seed_data()))


@bind("click", "generate_lanky_seed")
def generate_seed_from_patch(event):
    """Generate a seed from a patch file."""
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("rom").classList):
        js.document.getElementById("rom").select()
        if "is-invalid" not in list(js.document.getElementById("rom").classList):
            js.document.getElementById("rom").classList.add("is-invalid")
    elif len(str(js.document.getElementById("patchfileloader").value).strip()) == 0:
        js.document.getElementById("patchfileloader").select()
        if "is-invalid" not in list(js.document.getElementById("patchfileloader").classList):
            js.document.getElementById("patchfileloader").classList.add("is-invalid")
    else:
        js.apply_bps_javascript()
        patching_response(str(js.loaded_patch))


def serialize_settings():
    """Serialize form settings into an enum-focused JSON string.

    Returns:
        dict: Dictionary of form settings.
    """
    # Remove all the disabled attributes and store them for later
    disabled_options = []
    for element in js.document.getElementsByTagName("input"):
        if element.disabled:
            disabled_options.append(element)
            element.removeAttribute("disabled")
    for element in js.document.getElementsByTagName("select"):
        if element.disabled:
            disabled_options.append(element)
            element.removeAttribute("disabled")
    for element in js.document.getElementsByTagName("option"):
        if element.disabled:
            disabled_options.append(element)
            element.removeAttribute("disabled")
    # Serialize the form into json
    form = js.jquery("#form").serializeArray()
    form_data = {}

    def is_number(s):
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            pass

    def get_enum_or_string_value(valueString, settingName):
        """Obtain the enum or string value for the provided setting.

        Args:
            valueString (str) - The value from the HTML input.
            settingName (str) - The name of the HTML input.
        """
        if settingName in SettingsMap:
            return SettingsMap[settingName][valueString]
        else:
            return valueString

    for obj in form:
        # Verify each object if its value is a string convert it to a bool
        if obj.value.lower() in ["true", "false"]:
            form_data[obj.name] = bool(obj.value)
        else:
            if is_number(obj.value):
                form_data[obj.name] = int(obj.value)
            else:
                form_data[obj.name] = get_enum_or_string_value(obj.value, obj.name)
    # find all input boxes and verify their checked status
    for element in js.document.getElementsByTagName("input"):
        if element.type == "checkbox" and not element.checked:
            if not form_data.get(element.name):
                form_data[element.name] = False
    # Re disable all previously disabled options
    for element in disabled_options:
        element.setAttribute("disabled", "disabled")
    # Create value lists for multi-select options
    for element in js.document.getElementsByTagName("select"):
        if "selected" in element.className:
            length = element.options.length
            values = []
            for i in range(0, length):
                if element.options.item(i).selected:
                    values.append(get_enum_or_string_value(element.options.item(i).value, element.getAttribute("name")))
            form_data[element.getAttribute("name")] = values
    return form_data


@bind("click", "generate_seed")
def generate_seed(event):
    """Generate a seed based off the current settings.

    Args:
        event (event): Javascript click event.
    """
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("rom").classList):
        js.document.getElementById("rom").select()
        if "is-invalid" not in list(js.document.getElementById("rom").classList):
            js.document.getElementById("rom").classList.add("is-invalid")
    else:
        # Start the progressbar
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ProgressBar().update_progress(0, "Initalizing"))
        form_data = serialize_settings()
        if not form_data.get("seed"):
            form_data["seed"] = str(random.randint(100000, 999999))
        js.apply_bps_javascript()
        loop.run_until_complete(ProgressBar().update_progress(2, "Randomizing, this may take some time depending on settings."))
        # background(generate_playthrough, ["'''" + json.dumps(form_data) + "'''"], patching_response)
        background(form_data)


@bind("click", "download_patch_file")
def update_seed_text(event):
    """Set seed text based on the download_patch_file click event.

    Args:
        event (DOMEvent): Javascript dom click event.
    """
    # When we click the download json event just change the button text
    if js.document.getElementById("download_patch_file").checked:
        js.document.getElementById("generate_seed").value = "Generate Patch File and Seed"
    else:
        js.document.getElementById("generate_seed").value = "Generate Seed"
