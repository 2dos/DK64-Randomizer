"""Holds the version for DK64 Rando."""
import js

stable_version = "1.0"
dev_version = "1.0"

url = js.location.href.lower().replace("/", "").replace("http:", "").replace("https:", "")

only_version = "0.0"
current_version = "DK64R 0.0"
if url == "dk64randomizer.com":
    current_version = "DK64 Randomizer v" + stable_version
    only_version = stable_version
else:
    current_version = "DK64R Dev v" + dev_version
    only_version = dev_version

try:
    js.document.title = current_version
except Exception:
    pass
try:
    js.document.getElementById("live-version").text = current_version + " | "
except Exception:
    pass
