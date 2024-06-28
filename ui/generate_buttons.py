"""File containing main UI button events that travel between tabs."""

import asyncio
import json
import random

from pyodide.ffi import create_proxy

import js
from randomizer.Enums.Settings import SettingsMap
from randomizer.SettingStrings import decrypt_settings_string_enum, encrypt_settings_string_enum
from randomizer.Worker import background
from ui.bindings import bind
from ui.plando_validation import validate_plando_options
from ui.progress_bar import ProgressBar
from ui.rando_options import update_ui_states
from ui.serialize_settings import serialize_settings


@bind("click", "export_settings")
def export_settings_string(event):
    """Click event for exporting settings to a string.

    Args:
        event (event): Javascript event object.
    """
    setting_data = serialize_settings()
    settings_string = encrypt_settings_string_enum(setting_data)
    js.settings_string.value = settings_string


def should_clear_setting(select):
    """Return true if the select should be cleared when importing settings."""
    if js.document.querySelector("#nav-cosmetics").contains(select) is True:
        return False
    if js.document.querySelector("#nav-music").contains(select) is True:
        return False
    if select.name.startswith("plando_"):
        return False
    # This should now be obsolete, because of the #nav-music clause, but I really don't feel like trying my luck
    # TODO: change the plando_ clause into a #nav-plando clause and remove the music_select_clause
    if select.name.startswith("music_select_"):
        return False
    return True


@bind("click", "import_settings")
def import_settings_string(event):
    """Click event for importing settings from a string.

    Args:
        event (event): Javascript Event object.
    """
    js.settings_string.value = js.settings_string.value.strip()
    settings_string = js.settings_string.value
    settings = decrypt_settings_string_enum(settings_string)
    # Clear all select boxes on the page so as long as its not in the nav-cosmetics div
    for select in js.document.getElementsByTagName("select"):
        if should_clear_setting(select):
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
    update_ui_states(None)
    js.savesettings()


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
async def generate_previous_seed(event):
    """Generate a seed from a previous seed file."""
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("rom").classList):
        js.document.getElementById("rom").select()
        if "is-invalid" not in list(js.document.getElementById("rom").classList):
            js.document.getElementById("rom").classList.add("is-invalid")
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ProgressBar().update_progress(0, "Loading Previous seed and applying data."))
        js.apply_conversion()
        lanky_from_history = js.document.getElementById("load_patch_file").checked
        from randomizer.Patching.ApplyLocal import patching_response

        await patching_response(str(js.get_previous_seed_data()), True, lanky_from_history, True)


@bind("click", "generate_lanky_seed")
async def generate_seed_from_patch(event):
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
        js.apply_conversion()
        from randomizer.Patching.ApplyLocal import patching_response

        await patching_response(str(js.loaded_patch), True)


@bind("click", "trigger_download_event")
def generate_seed(event):
    """Generate a seed based off the current settings.

    Args:
        event (event): Javascript click event.
    """
    # Hide the div for settings errors.
    settings_errors_element = js.document.getElementById("settings_errors")
    settings_errors_element.style.display = "none"
    # Check if the rom filebox has a file loaded in it.
    if len(str(js.document.getElementById("rom").value).strip()) == 0 or "is-valid" not in list(js.document.getElementById("rom").classList):
        js.document.getElementById("rom").select()
        if "is-invalid" not in list(js.document.getElementById("rom").classList):
            js.document.getElementById("rom").classList.add("is-invalid")
    else:
        # The data is serialized outside of the loop, because validation occurs
        # here and we might stop before attempting to generate a seed.
        plando_enabled = js.document.getElementById("enable_plandomizer").checked
        form_data = serialize_settings(include_plando=plando_enabled)

        if form_data["enable_plandomizer"]:
            plando_errors = validate_plando_options(form_data)
            # If errors are returned, the plandomizer options are invalid.
            # Do not attempt to generate a seed.
            if len(plando_errors) > 0:
                joined_errors = "<br>".join(plando_errors)
                error_html = f"ERROR:<br>{joined_errors}"
                # Show and populate the div for settings errors.
                settings_errors_element.innerHTML = error_html
                settings_errors_element.style = ""
                return

        # Start the progressbar
        from randomizer.Patching.Hash import get_hash_images

        gif_fairy = get_hash_images("browser", "loading-fairy")
        gif_dead = get_hash_images("browser", "loading-dead")
        js.document.getElementById("progress-fairy").src = "data:image/jpeg;base64," + gif_fairy[0]
        js.document.getElementById("progress-dead").src = "data:image/jpeg;base64," + gif_dead[0]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(ProgressBar().update_progress(0, "Initalizing"))
        if not form_data.get("seed"):
            form_data["seed"] = str(random.randint(100000, 999999))
        js.apply_conversion()
        background(form_data)


@bind("click", "load_patch_file")
def update_patch_file(event):
    """Set historical seed text based on the load_patch_file click event.

    Args:
        event (DOMEvent): Javascript dom click event.
    """
    # When we click the download json event just change the button text
    if js.document.getElementById("load_patch_file").checked:
        js.document.getElementById("generate_pastgen_seed").value = "Generate Patch File from History"
    else:
        js.document.getElementById("generate_pastgen_seed").value = "Generate Seed from History"


async def get_args():
    """Get the args from the url and then load the seed from the server if it exists."""
    args = js.window.location.search
    if args.startswith("?"):
        args = args[1:]
    if "&" in args:
        args = args.split("&")
    else:
        args = [args]
    args_dict = {}

    for arg in args:
        try:
            arg_split = arg.split("=")
            args_dict[arg_split[0]] = arg_split[1]
        except Exception:
            pass
    # If someone provided seed_id in the url, lets pull the seed data from the webserver
    if "seed_id" in args_dict:
        # Wait for the page to load
        print("Getting the seed from the server")
        resp = js.get_seed_from_server(args_dict["seed_id"])
        from randomizer.Patching.ApplyLocal import patching_response

        await patching_response(str(resp), False)
    js.document.getElementById("visual_indicator").setAttribute("hidden", "true")
    js.document.getElementById("tab-data").removeAttribute("hidden")
