"""This module provides fake functions for printing messages and loading files with Javascript.

This module also defines a class `jsdoc` that represents a Javascript document, with methods for getting elements by ID and evaluating input.
"""

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


with open("./static/patches/pointer_addresses.json", "rb") as file:
    pointer_addresses = json.loads(file.read())


class jsdoc:
    """Represents a Javascript document, with methods for getting elements by ID and evaluating input."""

    def __init__(self, title="", content="", language=""):
        """Generate dummy vars for the document."""
        self.title = title
        self.content = content
        self.language = language
        self.elements = {}
        self.majoritems = {}
        self.minoritems = {}
        self.events = {}
        self.bgm = {}
        self.hostname = "localhost"

    def getElementById(self, element_id):
        """Get an element by its ID."""
        return self.elements.get(element_id, None)


document = jsdoc()
cosmetics = document
cosmetic_names = document
location = document


def eval(input):
    """Evaluate input."""
    pass
