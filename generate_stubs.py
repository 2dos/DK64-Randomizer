"""Generate Python and TypeScript stub files for the randomizer Enums."""

import json
import os
from pathlib import Path
from randomizer.JsonReader import load_jsonc

# Paths to directories
SOURCE_DIR = Path("randomizer/Enums")
DEST_DIR = Path("typings/randomizer/Enums")


def generate_stubs():
    """Generate Python and TypeScript stub files for the randomizer Enums."""
    # Ensure the destination directory exists
    if not DEST_DIR.exists():
        os.makedirs(DEST_DIR)

    # Iterate over all JSON files in the source directory
    for json_file in SOURCE_DIR.glob("*.jsonc"):
        create_stub(json_file)


def create_stub(json_file):
    """Create a .pyi and .d.ts file based on the JSON content."""
    # Get the filename and construct the output .pyi and .d.ts file paths
    json_file_name = json_file.stem
    pyi_file_path = DEST_DIR / f"{json_file_name}.pyi"
    dts_file_path = DEST_DIR / f"{json_file_name}.d.ts"

    # Read JSON content
    with open(json_file, "r") as file:
        try:
            data = load_jsonc(file.read())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")
            return

    # Process the data to replace "obj" key values and handle class keys
    data = resolve_obj_references(data)

    # Generate .pyi content
    pyi_content = create_pyi_content(data)
    # Generate .d.ts content
    dts_content = create_dts_content(data)

    # Write the .pyi file
    with open(pyi_file_path, "w") as pyi_file:
        pyi_file.write(pyi_content)
    print(f"Generated {pyi_file_path}")

    # Write the .d.ts file
    with open(dts_file_path, "w") as dts_file:
        dts_file.write(dts_content)
    print(f"Generated {dts_file_path}")


def resolve_obj_references(data: dict) -> dict:
    """Recursively resolve dictionaries with 'obj' keys and handle class keys."""
    for key, value in data.items():
        if isinstance(value, dict):
            # Check if the dictionary contains the "obj" key
            if "obj" in value:
                # Replace the current dict with the value of "obj"
                data[key] = value["obj"]
            else:
                # Recurse into nested dictionaries
                data[key] = resolve_obj_references(value)
        elif "." in key:
            # If the key contains a period, treat it as an object reference
            class_name = key.split(".")[0]
            data[class_name] = resolve_obj_references(value) if isinstance(value, dict) else value
    return data


def create_pyi_content(data: dict) -> str:
    """Generate Python stub file content based on the JSON data."""
    pyi_lines = []
    use_intenum = False  # Track if we need to import IntEnum

    # Iterate through each key-value pair in the JSON
    for key, value in data.items():
        if isinstance(value, dict):
            # Handle cases where the key contains a period (object reference)
            if all(isinstance(sub_value, int) for sub_value in value.values()):
                pyi_lines.append(f"class {key}(IntEnum):")
                for sub_key, sub_value in value.items():
                    if "." in sub_key:
                        pyi_lines.append(f"    {sub_key} = {sub_value}")
                    else:
                        pyi_lines.append(f"    {sub_key} = {sub_value}")
                pyi_lines.append("")  # Newline after each enum definition
                use_intenum = True
            else:
                # Handle dictionary-like structures and object references
                pyi_lines.append(f"{key}: dict = {{")
                for sub_key, sub_value in value.items():
                    # Handle cases where the key contains a period (no quotes)
                    if "." in sub_key:
                        pyi_lines.append(f"    {sub_key}: {sub_value},")
                    else:
                        pyi_lines.append(f"    '{sub_key}': {sub_value},")
                pyi_lines.append("}")
                pyi_lines.append("")  # Newline after each dictionary

    # Add necessary imports
    imports = []
    if use_intenum:
        imports.append("from enum import IntEnum")

    if imports:
        return "\n".join(imports) + "\n\n" + "\n".join(pyi_lines)
    else:
        return "\n".join(pyi_lines)


def create_dts_content(data: dict) -> str:
    """Generate TypeScript stub file content based on the JSON data."""
    dts_lines = []

    # Iterate through each key-value pair in the JSON
    for key, value in data.items():
        if isinstance(value, dict):
            # Handle cases where the key contains a period (object reference)
            if all(isinstance(sub_value, int) for sub_value in value.values()):
                dts_lines.append(f"export enum {key} {{")
                for sub_key, sub_value in value.items():
                    if "." in sub_key:
                        dts_lines.append(f"    {sub_key} = {sub_value},")
                    else:
                        dts_lines.append(f"    {sub_key} = {sub_value},")
                dts_lines.append("}")  # Close the enum
            else:
                # Handle dictionary-like structures and object references
                dts_lines.append(f"export const {key} = {{")
                for sub_key, sub_value in value.items():
                    # Handle cases where the key contains a period (no quotes)
                    if "." in sub_key:
                        dts_lines.append(f"    {sub_key}: {sub_value},")
                    else:
                        dts_lines.append(f"    '{sub_key}': {sub_value},")
                dts_lines.append("}")  # Close the object
            dts_lines.append("")  # Newline after each enum or object

    return "\n".join(dts_lines)


if __name__ == "__main__":
    generate_stubs()
