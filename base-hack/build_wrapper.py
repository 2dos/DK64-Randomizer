"""Wrapper script to determine what script file to use depending on your OS."""

import os
import platform
import subprocess
import sys
import stat

# Determine the OS
current_os = platform.system()  # 'Windows', 'Linux', 'Darwin'

# Get the script arguments
args = sys.argv[1:]

# Choose the correct build file
if current_os == "Windows":
    build_file = "build.bat"
    shell = True  # run in cmd
else:
    build_file = "./build.sh"
    shell = True  # run in bash

# Check if build file exists
if not os.path.exists(build_file):
    print(f"Error: {build_file} not found.")
    sys.exit(1)

# Dynamically set executable permission on Linux/macOS
if current_os in ("Linux", "Darwin"):
    st = os.stat(build_file)
    os.chmod(build_file, st.st_mode | stat.S_IEXEC)  # add execute permission
    st = os.stat("build/flips-linux")
    os.chmod("build/flips-linux", st.st_mode | stat.S_IEXEC)  # add execute permission

# Run the build file with the passed arguments
try:
    subprocess.run([build_file, *args], check=True)
except subprocess.CalledProcessError as e:
    print(f"Build failed with exit code {e.returncode}")
    sys.exit(e.returncode)
