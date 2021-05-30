"""Holds the version for DK64 Rando."""
from browser import document, window

stable_version = "0.4 Beta"
dev_version = "0.4 Beta"

url = window.location.href.lower().replace("/", "").replace("http:", "").replace("https:", "")

if url == "dk64randomizer.com":
    current_version = "DK64 Randomizer v" + stable_version
else:
    current_version = "DK64R Dev v" + dev_version

document.title = current_version
document["live-version"].text = current_version + " | "
