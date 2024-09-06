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


def timectime(ts: int):
    """Convert Unix time into human-readable time."""
    return datetime.fromtimestamp(ts).strftime("%d-%m-%Y %H:%M:%S")


def hasListUnion(lst1: list, lst2: list):
    """Return whether there is an item that is present in both lists."""
    for item in lst1:
        if item in lst2:
            return True
    return False


def filterId(id_string: str):
    """Filter an id to remove illegal characters."""
    return id_string.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "")


def getWotHPathIndex(spoiler_dict: dict):
    """Get the index of the WotH Path item in the spoiler dict, for usage in the id system."""
    order = 1
    for key in spoiler_dict:
        if key == "WotH Paths":
            return order
        order += 1
    return None


TIED_POOL_ITEMS = {
    "Kongs": ["Kong"],
    "Moves": ["TrainingBarrel", "Shop", "PreGivenMove", "Shockwave"],
    "Golden Bananas": ["Banana", "ToughBanana", "BlueprintBanana"],
    "Blueprints": ["Blueprint"],
    "Fairies": ["Fairy"],
    "Keys": ["Key"],
    "Crowns": ["Crown"],
    "Company Coins": ["NintendoCoin", "RarewareCoin"],
    "Medals": ["Medal"],
    "Miscellaneous Items": ["Bean", "Pearl"],
    "Rainbow Coins": ["RainbowCoin"],
    "Junk Items": ["JunkItem"],
    "Melon Crates": ["CrateItem"],
    "Enemy Drops": ["Enemies"],
    "Shop Owners": ["Cranky", "Funky", "Candy", "Snide"],
    "Ice Traps": ["FakeItem"],
}


async def GenerateSpoiler(spoiler):
    """Pass spoiler to jinja2 file and modify DOM with rendered jinja2 file."""
    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    templateEnv.filters["timeconvert"] = timectime
    templateEnv.filters["filterId"] = filterId
    templateEnv.filters["wothpathindex"] = getWotHPathIndex
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
    if "Hints" in formatted_spoiler:
        if "Wrinkly Hints" in formatted_spoiler["Hints"]:
            if "First Time Talk" in formatted_spoiler["Hints"]["Wrinkly Hints"]:
                del formatted_spoiler["Hints"]["Wrinkly Hints"]["First Time Talk"]
    # Custom Locations
    formatted_spoiler["Misc Custom Locations"] = {}
    location_mapping = {
        "Coin Locations": "Banana Coins",
        "Shuffled Banana Fairies": "Banana Fairies",
        "Shuffled Dirt Patches": "Dirt Patches",
        "Shuffled Melon Crates": "Melon Crates",
        "Battle Arena Locations": "Battle Arenas",
        "DK Portal Locations": "DK Portals",
    }
    for hint_attr in location_mapping:
        if hint_attr in formatted_spoiler:
            formatted_spoiler["Misc Custom Locations"][location_mapping[hint_attr]] = formatted_spoiler[hint_attr]
            formatted_spoiler.pop(hint_attr)
    # Item Pool Cleanup
    if "Item Pool" in formatted_spoiler:
        deleted_keys = []
        for key in formatted_spoiler["Items (Sorted by Item)"]:
            if key in TIED_POOL_ITEMS:
                if not hasListUnion(TIED_POOL_ITEMS[key], formatted_spoiler["Item Pool"]):
                    deleted_keys.append(key)
        for key in deleted_keys:
            del formatted_spoiler["Items (Sorted by Item)"][key]
    # End Game Cleanup
    if "Requirements" not in formatted_spoiler:
        formatted_spoiler["Requirements"] = {}
    if "Bosses" not in formatted_spoiler:
        formatted_spoiler["Bosses"] = {}
    if "End Game" in formatted_spoiler:
        if "K. Rool" in formatted_spoiler["End Game"]:
            if "K Rool Phases" in formatted_spoiler["End Game"]["K. Rool"]:
                formatted_spoiler["Bosses"]["The Final Battle"] = formatted_spoiler["End Game"]["K. Rool"]["K Rool Phases"].copy()
                del formatted_spoiler["End Game"]["K. Rool"]["K Rool Phases"]
            if "Keys Required for K Rool" in formatted_spoiler["End Game"]["K. Rool"]:
                formatted_spoiler["Requirements"]["Keys Required for K. Rool"] = formatted_spoiler["End Game"]["K. Rool"]["Keys Required for K Rool"]
                del formatted_spoiler["End Game"]["K. Rool"]["Keys Required for K Rool"]
        if "Helm" in formatted_spoiler["End Game"]:
            if "Helm Rooms" in formatted_spoiler["End Game"]["Helm"]:
                formatted_spoiler["Requirements"]["Helm Rooms"] = formatted_spoiler["End Game"]["Helm"]["Helm Rooms"]
                del formatted_spoiler["End Game"]["Helm"]["Helm Rooms"]
    del formatted_spoiler["End Game"]
    del formatted_spoiler["Randomizer Version"]

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
