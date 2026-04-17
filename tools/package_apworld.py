"""Package DK64 Rando into an APWorld file."""

import os
import shutil
import zipfile

# Define paths
dk64_folder = "dk64"
# vendor_folder removed - no longer needed

# Files and folders to copy into dk64
files_to_copy = ["__init__.py", "js.py", "version.py", "static/compiled.jsonc", "archipelago.json"]
folders_to_copy = ["archipelago", "base-hack/assets/arcade_jetpac", "base-hack/assets/DKTV", "base-hack/assets/displays", "randomizer", "static/patches", "base-hack/minigame"]

# Ensure dk64 directory exists
os.makedirs(dk64_folder, exist_ok=True)

# Copy specified files
for file in files_to_copy:
    if os.path.exists(file):
        # Make the directory if it doesn't exist
        os.makedirs(os.path.join(dk64_folder, os.path.dirname(file)), exist_ok=True)
        shutil.copy(file, os.path.join(dk64_folder, file))

# Copy specified folders
for folder in folders_to_copy:
    if os.path.exists(folder):
        # Make the directory if it doesn't exist
        os.makedirs(os.path.join(dk64_folder, folder), exist_ok=True)
        shutil.copytree(folder, os.path.join(dk64_folder, folder), dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))



# Function to zip a folder
def zip_folder(folder_path: str, zip_name: str, preserve_root: bool = False):
    """Zip a folder."""
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        folder_basename = os.path.basename(folder_path)  # "dk64"
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if preserve_root:
                    arcname = os.path.join(folder_basename, os.path.relpath(file_path, start=folder_path))
                    # Ensures dk64/ appears only once in zip
                else:
                    arcname = os.path.relpath(file_path, start=folder_path)  # No extra nesting
                zipf.write(file_path, arcname)


# Vendor dependency zipping removed - no longer packaging PIL/pyxdelta dependencies

# Zip dk64 directory
zip_folder(dk64_folder, "dk64.apworld", preserve_root=True)
# Delete the folder
shutil.rmtree(dk64_folder)

print("All files have been copied and zipped successfully.")
