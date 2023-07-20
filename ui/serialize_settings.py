"""Function to obtain all settings and convert them to a dictionary."""
import js
from randomizer.Enums.Settings import SettingsMap
from ui.plando_validation import populate_plando_options


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

    # Plandomizer data is processed separately.
    plando_form_data = populate_plando_options(form)
    if plando_form_data is not None:
        form_data["plandomizer"] = plando_form_data

    def is_number(s):
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            pass

    def is_plando_input(inputName):
        """Determine if an input is a plando input."""
        return inputName is not None and inputName.startswith("plando_")

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
        if is_plando_input(obj.name):
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
    return form_data
