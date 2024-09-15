import json
import os
from pathlib import Path

# Paths to directories
SOURCE_DIR = Path("randomizer/Enums")
DEST_DIR = Path("typings/randomizer/Enums")


def generate_pyi_stubs():
    # Ensure the destination directory exists
    if not DEST_DIR.exists():
        os.makedirs(DEST_DIR)

    # Iterate over all JSON files in the source directory
    for json_file in SOURCE_DIR.glob("*.json"):
        create_stub(json_file)


def create_stub(json_file):
    # Get the filename and construct the output .pyi file path
    json_file_name = json_file.stem
    pyi_file_path = DEST_DIR / f"{json_file_name}.pyi"

    # Read JSON content
    with open(json_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")
            return

    # Generate .pyi content
    pyi_content = create_pyi_content(data)

    # Write the .pyi file
    with open(pyi_file_path, "w") as pyi_file:
        pyi_file.write(pyi_content)
    print(f"Generated {pyi_file_path}")


def create_pyi_content(data: dict) -> str:
    pyi_lines = []
    use_intenum = False  # Track if we need to import IntEnum

    # Iterate through each key-value pair in the JSON
    for key, value in data.items():
        if isinstance(value, dict):
            # Create an IntEnum for each dictionary entry
            pyi_lines.append(f"class {key}(IntEnum):")
            for sub_key, sub_value in value.items():
                pyi_lines.append(f"    {sub_key} = {sub_value}")
            pyi_lines.append("")  # Newline after each enum definition
            use_intenum = True  # We need to import IntEnum

    # Add necessary imports
    imports = []
    if use_intenum:
        imports.append("from enum import IntEnum")

    if imports:
        return "\n".join(imports) + "\n\n" + "\n".join(pyi_lines)
    else:
        return "\n".join(pyi_lines)


if __name__ == "__main__":
    generate_pyi_stubs()
