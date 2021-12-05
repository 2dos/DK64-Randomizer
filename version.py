"""Holds the version for DK64 Rando."""
import js

stable_version = "0.4 Beta"
dev_version = "0.4.5 Beta"

url = js.location.href.lower().replace("/", "").replace("http:", "").replace("https:", "")

if url == "dk64randomizer.com":
    current_version = "DK64 Randomizer v" + stable_version
else:
    current_version = "DK64R Dev v" + dev_version

js.document.title = current_version
js.document.getElementById("live-version").text = current_version + " | "
