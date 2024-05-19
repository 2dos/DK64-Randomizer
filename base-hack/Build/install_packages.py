"""Install packages that are required to build the base hack."""

import subprocess
import sys
from pip._internal.operations import freeze

installed_packages_list = freeze.freeze()

required_build_packages = ["pillow", "requests", "PyInstaller"]
current_packages = []

print("Installed Packages:")
for pkg in installed_packages_list:
    print("-", pkg)
    pkg_data = pkg.split("==")
    current_packages.append({"name": pkg_data[0], "version": pkg_data[1]})

print("Checking Packages:")
for req_pkg in required_build_packages:
    installed = False
    installed_name = "Not Installed"
    for cur_pkg in current_packages:
        if cur_pkg["name"].lower() == req_pkg.lower():
            installed = True
            installed_name = f"Installed ({cur_pkg['version']})"
    print(f"\t{req_pkg.capitalize()}: {installed_name}")
    if not installed:
        print(f"\t\tInstalling {req_pkg.capitalize()}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", req_pkg, "--no-warn-script-location"], stdout=subprocess.DEVNULL)
