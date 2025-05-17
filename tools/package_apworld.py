"""Package DK64 Rando into an APWorld file."""

import os
import shutil
import subprocess
import sys
import zipfile

# Define paths
dk64_folder = "dk64"
vendor_folder = "dk64/vendor"
requirements_file = "requirements.txt"

# Files and folders to copy into dk64
files_to_copy = ["__init__.py", "js.py", "version.py", "static/compiled.jsonc", "ap_version.py"]
folders_to_copy = ["archipelago", "base-hack/assets/arcade_jetpac", "base-hack/assets/DKTV", "randomizer", "static/patches"]

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

# Create vendor directory
os.makedirs(vendor_folder, exist_ok=True)


# Function to install dependencies into a specific folder
def install_dependencies(target_folder, platform):
    """Install dependencies into a specific folder."""
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file, "--target", target_folder, "--platform", platform, "--only-binary=:all:"], check=True)


# Install Windows dependencies
windows_vendor = os.path.join(vendor_folder, "windows")
os.makedirs(windows_vendor, exist_ok=True)
install_dependencies(windows_vendor, "win_amd64")

# Install Linux dependencies
linux_vendor = os.path.join(vendor_folder, "linux")
os.makedirs(linux_vendor, exist_ok=True)
install_dependencies(linux_vendor, "manylinux2014_x86_64")


# Function to zip a folder
def zip_folder(folder_path, zip_name, preserve_root=False):
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


# Zip Windows dependencies
zip_folder(windows_vendor, "dk64/vendor/windows.zip")
# Delete the folder
shutil.rmtree(windows_vendor)
# Zip Linux dependencies
zip_folder(linux_vendor, "dk64/vendor/linux.zip")
# Delete the folder
shutil.rmtree(linux_vendor)

# # Test move, dk64/vendor/windows to the root
# # Move all files and folders
# for item in os.listdir(windows_vendor):
#     src_path = os.path.join(windows_vendor, item)
#     dst_path = os.path.join(dk64_folder, item)

#     # If destination already exists, you can choose to overwrite or skip
#     if os.path.exists(dst_path):
#         print(f"Skipping '{dst_path}' (already exists)")
#         continue

#     shutil.move(src_path, dst_path)
#     print(f"Moved '{src_path}' to '{dst_path}'")


# Zip dk64 directory
zip_folder(dk64_folder, "dk64.apworld", preserve_root=True)
# Delete the folder
shutil.rmtree(dk64_folder)

print("All files have been copied and zipped successfully.")
