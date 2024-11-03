"""Code to create files and download them to the user's computer."""

import js
import json


def download_json_file(jsonData: dict, filename: str):
    """Download the provided dictionary as a JSON file.

    Args:
        jsonData (dict) - The dictionary containing the data to be downloaded.
        filename (str) - The name of the file to be downloaded.
    """
    # Create a link to the file and download it automatically.
    jsonString = json.dumps(jsonData, indent=4)
    blob = js.Blob.new([jsonString], {type: "application/json"})
    blob.name = filename
    url = js.window.URL.createObjectURL(blob)
    link = js.document.createElement("a")
    link.href = url
    link.download = blob.name
    js.document.body.appendChild(link)
    link.click()

    # Delete the link.
    js.document.body.removeChild(link)
    js.window.URL.revokeObjectURL(url)
