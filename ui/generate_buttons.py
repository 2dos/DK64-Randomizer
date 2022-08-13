"""File containing main UI button events that travel between tabs."""
import asyncio
import json
import random

import js
from randomizer.BackgroundRandomizer import generate_playthrough
from randomizer.Patching.ApplyRandomizer import patching_response
from randomizer.Worker import background
from ui.bindings import bind
from ui.progress_bar import ProgressBar
from ui.settings_strings import encrypt_settings_string, decrypt_setting_string
from ui.rando_options import (
    toggle_counts_boxes,
    toggle_b_locker_boxes,
    update_boss_required,
    disable_colors,
    disable_music,
    disable_prices,
    max_randomized_blocker,
    max_randomized_troff,
    disable_barrel_rando,
    disable_boss_rando,
    hide_rgb,
    toggle_medals_box,
    max_randomized_medals,
    disable_rw,
)
from pyodide import create_proxy


@bind("click", "export_settings")
def export_settings_string(event):
    """Click event for exporting settings to a string.

    Args:
        event (event): Javascript event object.
    """
    form_data = serialize_settings()
    settings_string = encrypt_settings_string(form_data)
    js.settings_string.value = settings_string


@bind("click", "import_settings")
def import_settings_string(event):
    """Click event for importing settings from a string.

    Args:
        event (event): Javascript Event object.
    """
    settings_string = js.settings_string.value
    try:
        settings = decrypt_setting_string(settings_string)
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
                else:
                    if js.document.getElementsByName(key)[0].hasAttribute("data-slider-value"):
                        js.jq(f"#{key}").slider("setValue", settings[key])
                        js.jq(f"#{key}").slider("enable")
                        js.jq(f"#{key}").parent().find(".slider-disabled").removeClass("slider-disabled")
                    else:
                        js.jq(f"#{key}").val(settings[key])
                    js.jq(f"#{key}").removeAttr("disabled")
            except Exception as e:
                pass
        toggle_counts_boxes(None)
        toggle_b_locker_boxes(None)
        update_boss_required(None)
        disable_colors(None)
        disable_music(None)
        disable_prices(None)
        max_randomized_blocker(None)
        max_randomized_troff(None)
        disable_barrel_rando(None)
    except Exception:
        pass


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


@bind("click", "generate_lanky_seed")
def generate_seed_from_patch(event):
    """Generate a seed from a patch file."""
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("input-file-rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("input-file-rom").classList):
        js.document.getElementById("input-file-rom").select()
        if "is-invalid" not in list(js.document.getElementById("input-file-rom").classList):
            js.document.getElementById("input-file-rom").classList.add("is-invalid")
    elif len(str(js.document.getElementById("patchfileloader").value).strip()) == 0:
        js.document.getElementById("patchfileloader").select()
        if "is-invalid" not in list(js.document.getElementById("patchfileloader").classList):
            js.document.getElementById("patchfileloader").classList.add("is-invalid")
    else:
        js.apply_bps_javascript()
        patching_response(str(js.loaded_patch))


def serialize_settings():
    """Serialize form settings into a JSON string.

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

    for obj in form:
        # Verify each object if its value is a string convert it to a bool
        if obj.value.lower() in ["true", "false"]:
            form_data[obj.name] = bool(obj.value)
        else:
            if is_number(obj.value):
                form_data[obj.name] = int(obj.value)
            else:
                form_data[obj.name] = obj.value
    # find all input boxes and verify their checked status
    for element in js.document.getElementsByTagName("input"):
        if element.type == "checkbox" and not element.checked:
            if not form_data.get(element.name):
                form_data[element.name] = False
    # Re disable all previously disabled options
    for element in disabled_options:
        element.setAttribute("disabled", "disabled")
    return form_data


@bind("click", "generate_seed")
def generate_seed(event):
    """Generate a seed based off the current settings.

    Args:
        event (event): Javascript click event.
    """
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("input-file-rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("input-file-rom").classList):
        js.document.getElementById("input-file-rom").select()
        if "is-invalid" not in list(js.document.getElementById("input-file-rom").classList):
            js.document.getElementById("input-file-rom").classList.add("is-invalid")
    else:
        # Start the progressbar
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ProgressBar().update_progress(0, "Initalizing"))
        form_data = serialize_settings()
        if not form_data.get("seed"):
            form_data["seed"] = str(random.randint(100000, 999999))
        js.apply_bps_javascript()
        loop.run_until_complete(ProgressBar().update_progress(2, "Randomizing, this may take some time depending on settings."))
        background(generate_playthrough, ["'''" + json.dumps(form_data) + "'''"], patching_response)


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


@bind("click", "nav-seed-gen-tab")
@bind("click", "nav-patch-tab")
def disable_input(event):
    """Disable input for the ROM Boxes as we rotate through the navbar.

    Args:
        event (DOMEvent): DOM item that triggered the event.
    """
    # Try to determine of the patch tab was what triggered the event.
    ev_type = False
    try:
        if "patch-tab" in event.target.id:
            ev_type = True
    except Exception:
        pass
    # As we rotate between the tabs, verify our disabled progression status
    # and set our input file box as the correct name so we can use two fileboxes as the same name
    if ev_type is False:
        if not js.document.getElementById("input-file-rom_2"):
            try:
                js.document.getElementById("input-file-rom").id = "input-file-rom_2"
            except Exception:
                pass
        try:
            js.document.getElementById("input-file-rom_1").id = "input-file-rom"
        except Exception:
            pass
    else:
        if not js.document.getElementById("input-file-rom_1"):
            try:
                js.document.getElementById("input-file-rom").id = "input-file-rom_1"
            except Exception:
                pass
        try:
            js.document.getElementById("input-file-rom_2").id = "input-file-rom"
        except Exception:
            pass
