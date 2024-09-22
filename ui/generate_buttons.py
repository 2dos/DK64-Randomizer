"""File containing main UI button events that travel between tabs."""

import asyncio
import json
import random

import time
import uuid
import js
from randomizer.Enums.Settings import SettingsMap
from randomizer.SettingStrings import decrypt_settings_string_enum, encrypt_settings_string_enum
from ui.bindings import bind
from ui.plando_validation import validate_plando_options
from ui.progress_bar import ProgressBar



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
        if js.should_clear_setting(select):
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
                if selector.tagName == "SELECT" and key != "random-weights":
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
    js.update_ui_states(None)
    js.savesettings()
    js.generateToast("Imported settings string.<br />All non-cosmetic settings have been overwritten.")


