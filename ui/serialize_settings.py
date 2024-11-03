"""Function to obtain all settings and convert them to a dictionary."""

import json
import js
from randomizer.Enums.Items import Items
from randomizer.Enums.Settings import SettingsMap
from ui.music_select import serialize_music_selections
from ui.plando_validation import populate_plando_options


def serialize_settings(include_plando: bool = False) -> dict:
    """Serialize form settings into an enum-focused JSON object.

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

    # Plandomizer data is processed separately and uses a separate setting string, so it needs to be optionally serializable
    if include_plando:
        plando_form_data = populate_plando_options(form)
        if plando_form_data is not None:
            form_data["enable_plandomizer"] = True
            form_data["plandomizer_data"] = json.dumps(plando_form_data)

    # Custom music data is also processed separately.
    music_selection_data = serialize_music_selections(form)
    form_data["music_selections"] = json.dumps(music_selection_data)

    def is_number(s) -> bool:
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            pass

    def is_plando_input(inputName: str) -> bool:
        """Determine if an input is a plando input."""
        return inputName is not None and inputName.startswith("plando_")

    def is_starting_move_radio_button(inputName: str) -> bool:
        """Determine if an input is a starting move checkbox."""
        return inputName is not None and inputName.startswith("starting_move_box_")

    def is_music_select_input(inputName: str) -> bool:
        """Determine if an input is a song selection input."""
        return inputName is not None and inputName.startswith("music_select_")

    def get_enum_or_string_value(valueString: str, settingName: str):
        """Obtain the enum or string value for the provided setting.

        Args:
            valueString (str) - The value from the HTML input.
            settingName (str) - The name of the HTML input.
        """
        if settingName in SettingsMap:
            return SettingsMap[settingName][valueString]
        else:
            return valueString

    required_starting_moves = []
    random_starting_moves = []

    for obj in form:
        if is_plando_input(obj.name):
            continue
        if is_starting_move_radio_button(obj.name):
            continue
        if is_music_select_input(obj.name):
            continue
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
        if is_plando_input(element.name):
            continue
        if is_starting_move_radio_button(element.name) and element.checked:
            if element.id.startswith("start"):
                required_starting_moves.append(Items(int(element.name[18:])))
            elif element.id.startswith("random"):
                random_starting_moves.append(Items(int(element.name[18:])))
            continue
        if element.type == "checkbox" and not element.checked:
            if not form_data.get(element.name):
                form_data[element.name] = False
    # Re disable all previously disabled options
    for element in disabled_options:
        element.setAttribute("disabled", "disabled")
    # Create value lists for multi-select options
    for element in js.document.getElementsByTagName("select"):
        if "selected" in element.className:
            if is_plando_input(element.getAttribute("name")):
                continue
            length = element.options.length
            values = []
            for i in range(0, length):
                if element.options.item(i).selected:
                    values.append(get_enum_or_string_value(element.options.item(i).value, element.getAttribute("name")))
            form_data[element.getAttribute("name")] = values
    form_data["starting_move_list_selected"] = required_starting_moves
    form_data["random_starting_move_list_selected"] = random_starting_moves

    return form_data
