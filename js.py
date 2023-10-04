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


with open("./static/patches/pointer_addresses.json", "rb") as file:
    pointer_addresses = json.loads(file.read())


class jsdoc:
    def __init__(self, title="", content="", language=""):
        self.title = title
        self.content = content
        self.language = language
        self.elements = {}
        self.majoritems = {}
        self.minoritems = {}
        self.events = {}
        self.bgm = {}

    def getElementById(self, element_id):
        return self.elements.get(element_id, None)


document = jsdoc()
cosmetics = document
cosmetic_names = document
