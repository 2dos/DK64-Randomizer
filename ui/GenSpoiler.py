"""Push jinja2 file to spoiler."""

import json
from datetime import datetime

from jinja2 import Environment, FunctionLoader

import js


def ajax_call(file):
    """Get file."""
    resp = js.getFile(file)
    return resp


def loader_func(template_name):
    """Load template file."""
    return ajax_call("templates/" + f"{template_name}")

def timectime(ts):
    return datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

async def GenerateSpoiler(spoiler):
    """Pass spoiler to jinja2 file and modify DOM with rendered jinja2 file."""
    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    templateEnv.filters['timeconvert'] = timectime
    template = templateEnv.get_template("spoiler_new.html.jinja2")
    trimmed_spoiler = ""
    for x in json.dumps(spoiler).split("\n"):
        trimmed_spoiler += x.strip()
    formatted_spoiler = json.loads(trimmed_spoiler)
    # Site Spoiler Modifications
    if "Spoiler Hints Data" in formatted_spoiler:
        formatted_spoiler.pop("Spoiler Hints Data")
    # Hints
    formatted_spoiler["Hints"] = {}
    for hint_attr in ("Wrinkly Hints", "Direct Item Hints"):
        if hint_attr in formatted_spoiler:
            formatted_spoiler["Hints"][hint_attr] = formatted_spoiler[hint_attr]
            formatted_spoiler.pop(hint_attr)
    # Custom Locations
    formatted_spoiler["Misc Custom Locations"] = {}
    location_mapping = {
        "Coin Locations": "Banana Coins",
        "Shuffled Banana Fairies": "Banana Fairies",
        "Shuffled Dirt Patches": "Dirt Patches",
        "Shuffled Melon Crates": "Melon Crates",
        "Battle Arena Locations": "Battle Arenas"
    }
    for hint_attr in location_mapping:
        if hint_attr in formatted_spoiler:
            formatted_spoiler["Misc Custom Locations"][location_mapping[hint_attr]] = formatted_spoiler[hint_attr]
            formatted_spoiler.pop(hint_attr)

    # modified_spoiler.update(formatted_spoiler)
    # print(modified_spoiler)

    lzr_type = "none"
    if formatted_spoiler.get("Settings", {}).get("Loading Zones Shuffled", "") == "all":
        if formatted_spoiler["Settings"]["Decoupled Loading Zones"] is False:
            lzr_type = "coupled"
        else:
            lzr_type = "decoupled"

    rendered = await template.render(spoiler=formatted_spoiler, lzr_type=lzr_type)
    js.document.getElementById("spoiler_log_text").value = json.dumps(spoiler, indent=4)
    js.document.getElementById("spoiler_log_text").innerHTML = rendered
