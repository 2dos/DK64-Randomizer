"""This is a dummy module that only exists to override the built in pyodide module."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING


def postMessage(message: str) -> None:
    """Fake function for printing messages with JS."""
    print(message)


def getFile(filename):
    """Fake function for loading files with Javascript."""
    with open(filename, "rb") as file:
        return file.read()


def getStringFile(filename):
    """Fake function for loading files with Javascript."""
    with open(filename, "r") as file:
        return file.read()


with open("./static/patches/pointer_addresses.json", "rb") as file:
    pointer_addresses = json.loads(file.read())

with open("./static/patches/symbols.json", "rb") as file:
    rom_symbols = json.loads(file.read())
