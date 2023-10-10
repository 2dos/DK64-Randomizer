"""Wheel File Creation for the website for efficient loading."""
from setuptools import find_packages, setup

packages = find_packages(exclude=["tests", "base-hack", "build", "dist", "docs", "scripts", "tmp", "wiki-lists"])

setup(
    name="dk64rando",
    # Note if you're going to change this version also change the version in the generate_*ui.py files for loading it along with
    # Copying the file in prepare_live.py
    version="1.0.0",
    packages=packages,
)
