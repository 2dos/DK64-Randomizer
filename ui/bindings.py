"""Decorator function for UI elements to bind events to buttons."""
from functools import wraps

from pyodide import create_proxy

import js
from js import document
from randomizer.Enums.Settings import SettingsMap
from ui.plando_validation import populate_plando_options


def bind(event, id, iterations=0):
    """Bind a function to an event for a buttton.

    Args:
        event (str): Event to bind to eg: click
        id (str): ID of the element to bind to.
        iterations (int, optional): If we want to run this function multiple times with an increasing iteration. Defaults to 0.
    """

    def real_decorator(function):
        """Return the main decorator back this is the main response.

        Args:
            function (func): The original function.

        Returns:
            func: The original function to return.
        """
        function = create_proxy(function)
        if iterations == 0:
            document.getElementById(id).addEventListener(event, function, False)
        else:
            for i in range(0, iterations):
                try:
                    document.getElementById(id + str(i)).addEventListener(event, function)
                except Exception:
                    pass

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap our existing function with our passed function.

            Returns:
                func: The function to wrap.
            """
            retval = function(*args, **kwargs)
            return retval

        return wrapper

    return real_decorator


def bindList(event, idList, *, prefix="", suffix=""):
    """Bind a function to an event for a list of buttons.

    Args:
        event (str): Event to bind to eg: click
        idList (str[]): A list of IDs of the elements to bind to.
        prefix (str, optional): A string prefix to add to the start of each ID.
        suffix (str, optional): A string suffix to add to the end of each ID.
    """

    def real_decorator(function):
        """Return the main decorator back this is the main response.

        Args:
            function (func): The original function.

        Returns:
            func: The original function to return.
        """
        function = create_proxy(function)
        for id in idList:
            try:
                elementName = prefix + id + suffix
                document.getElementById(elementName).addEventListener(event, function)
            except Exception:
                pass

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap our existing function with our passed function.

            Returns:
                func: The function to wrap.
            """
            retval = function(*args, **kwargs)
            return retval

        return wrapper

    return real_decorator


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
