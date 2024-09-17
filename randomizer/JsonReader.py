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
    # Prepare the enum members as a dictionary of key=value pairs
    enum_members = {key: auto() if value == "auto" else value for key, value in values.items()}

    # Check if any of the members use "auto". If so, use Enum, otherwise use IntEnum.
    return IntEnum(name, enum_members)


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
        new_globals[enum_name] = create_enum_class(enum_name, enum_values)
    return new_globals
