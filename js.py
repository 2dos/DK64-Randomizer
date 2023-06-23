"""This is a dummy module that only exists to override the built in pyodide module."""
import json


def postMessage(message):
    """Fake function for printing messages with JS."""
    print(message)


def getFile(filename):
    """Fake function for loading files with Javascript."""
    with open(filename, "rb") as file:
        return file.read()


with open("./static/patches/pointer_addresses.json", "rb") as file:
    pointer_addresses = json.loads(file.read())
