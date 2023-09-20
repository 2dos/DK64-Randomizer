"""Wheel File Creation for the website for efficient loading."""
from setuptools import find_packages, setup
from mypyc.build import mypycify

packages = find_packages(exclude=["tests", "base-hack", "build", "dist", "docs", "scripts", "tmp", "wiki-lists"])
paths = [
"randomizer/Lists/HardMode.py",
"randomizer/Lists/KasplatLocations.py",
"randomizer/Lists/LevelInfo.py",
"randomizer/Lists/Location.py",
"randomizer/Lists/Logic.py",
"randomizer/Lists/Minigame.py",
"randomizer/Lists/QoL.py",
"randomizer/Lists/Warps.py",
"randomizer/Lists/WrinklyHints.py",
"randomizer/Logic.py"
        ]
setup(
    name="dk64rando",
    # Note if you're going to change this version also change the version in the generate_*ui.py files for loading it along with
    # Copying the file in prepare_live.py
    version="1.0.0",
    packages=packages,
    ext_modules=mypycify(
        paths, only_compile_paths=paths
    ),
)
