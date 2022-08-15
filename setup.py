"""Wheel File Creation for the website for efficient loading."""
from setuptools import setup, find_packages

packages = find_packages(exclude=["tests", "base-hack", "build", "dist", "docs", "scripts", "tmp"])

setup(
    name="dk64rando",
    version="web",
    packages=packages,
)
