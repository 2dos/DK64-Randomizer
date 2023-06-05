"""This is a dummy module that only exists to override the built in pyodide module."""


def postMessage(message):
    """Fake function for printing messages with JS."""
    print(message)


def getFile(filename):
    """Fake function for loading files with Javascript."""
    with open(filename, "rb") as file:
        return file.read()
