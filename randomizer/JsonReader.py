import json
import re
from enum import IntEnum, auto
import pathlib


def remove_comments(jsonc_str):
    # Remove single-line comments (//)
    jsonc_str = re.sub(r"//.*", "", jsonc_str)
    # Remove multi-line comments (/* ... */)
    jsonc_str = re.sub(r"/\*.*?\*/", "", jsonc_str, flags=re.DOTALL)
    return jsonc_str


def load_jsonc(filename):
    jsonc_str = filename.read()

    # Remove comments
    json_str = remove_comments(jsonc_str)

    # Parse JSON
    return json.loads(json_str)


def create_enum_class(name, values):
    """
    Dynamically creates an Enum or IntEnum class based on the JSON data.
    :param name: Name of the enum class
    :param values: Dictionary of enum members
    :return: Enum class
    """
    enum_members = {key: auto() if value == "auto" else value for key, value in values.items()}

    # Check if all members are integers for IntEnum, or handle string eval for others
    if all(isinstance(value, int) for value in enum_members.values()):
        return IntEnum(name, enum_members)
    else:
        for key, value in enum_members.items():
            # Evaluate the string directly into an object
            if isinstance(value, str):
                enum_members[key] = eval(value, globals(), locals())
        return enum_members


def process_value(value):
    """
    Process the value to check if it's a dictionary containing the 'obj' key.
    If so, return the value associated with 'obj', otherwise return the original value.
    """
    if isinstance(value, dict) and 'obj' in value:
        return value['obj']
    return value


def set_nested_dict(d, keys, value):
    """
    Recursively create nested dictionaries for keys containing periods.
    :param d: Dictionary to update
    :param keys: List of keys after splitting on period
    :param value: The value to set at the final nested key
    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def process_keys_with_period(data):
    """
    Recursively processes a dictionary and handles keys with periods by creating nested dictionaries.
    :param data: The dictionary with keys to process
    :return: Processed dictionary with nested structures for keys containing periods
    """
    processed_data = {}
    for key, value in data.items():
        if '.' in key:
            keys = key.split('.')
            set_nested_dict(processed_data, keys, value)
        else:
            processed_data[key] = value
    return processed_data


def generate_globals(path):
    # Convert JSON string to a Python dictionary
    path = path.replace(str(pathlib.Path().resolve()), "")
    # Replace the .py extension with .json
    path = path.replace(".py", ".jsonc")
    # If the path starts with a slash, remove it
    if path.startswith("/"):
        path = path[1:]
    
    with open(path) as f:
        enums_data = load_jsonc(f)

    new_globals = {}
    
    for enum_name, enum_values in enums_data.items():
        # Process the enum values to handle dicts with 'obj' keys
        processed_values = {key: process_value(value) for key, value in enum_values.items()}
        
        # Handle period in keys to convert them to nested objects
        processed_values = process_keys_with_period(processed_values)
        
        new_globals[enum_name] = create_enum_class(enum_name, processed_values)
        # Add new_globals to the globals() dictionary for just this file
        globals().update(new_globals)
    
    return new_globals
