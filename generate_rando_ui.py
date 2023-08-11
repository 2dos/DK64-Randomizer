"""Generate UI elements via jinja2 to display on page load."""
import json
import time

import micropip
from jinja2 import Environment, FunctionLoader

import js
from js import document


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
    # await micropip.install("pyodide-importer")
    url = js.window.location.origin
    await micropip.install(
        [
            f"{url}/static/py_libraries/charset_normalizer-2.1.0-py3-none-any.whl",
            f"{url}/static/py_libraries/urllib3-1.26.11-py2.py3-none-any.whl",
            f"{url}/static/py_libraries/certifi-2022.6.15-py3-none-any.whl",
            f"{url}/static/py_libraries/idna-3.3-py3-none-any.whl",
            f"{url}/static/py_libraries/requests-2.28.1-py3-none-any.whl",
            f"{url}/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl",
            "pillow",
        ],
        deps=False,
    )
    if js.location.hostname in ["dev.dk64randomizer.com", "dk64randomizer.com"]:
        await micropip.install(f"{url}/static/py_libraries/dk64rando-1.0.0-py3-none-any.whl")
    # Against normal logic we have to import the hook register because we install it as we load the page
    from pyodide_importer import register_hook  # type: ignore  # noqa

    try:
        register_hook("/")
    except Exception:
        pass

    # Module of Lists used for list_selector macros
    from randomizer.Enums.Types import ItemRandoSelector, KeySelector
    from randomizer.Lists.EnemyTypes import EnemySelector
    from randomizer.Lists.Item import HHItemSelector, StartingMoveSelector
    from randomizer.Lists.Logic import GlitchSelector
    from randomizer.Lists.Minigame import MinigameSelector
    from randomizer.Lists.QoL import QoLSelector
    from randomizer.Lists.HardMode import HardSelector
    from randomizer.Lists.Warps import VanillaBananaportSelector
    from randomizer.Lists.Songs import ExcludedSongsSelector
    from randomizer.Lists.WrinklyHints import PointSpreadSelector

    # Module of lists and utils used for plandomizer
    from randomizer.PlandoUtils import PlandoItemFilter, PlandoMinigameFilter, PlandoOptionClassAnnotation, PlandoShopSortFilter
    from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableItems, PlannableMinigames, PlannableSpawns

    js.listeners = []
    js.progression_presets = []
    js.background_worker = None

    def ajax_call(file):
        resp = js.getFile(file)
        return resp

    def loader_func(template_name):
        milliseconds = int(round(time.time() * 1000))
        return ajax_call("templates/" + f"{template_name}?currtime={milliseconds}")

    milliseconds = int(round(time.time() * 1000))
    for file in json.loads(ajax_call(f"static/presets/preset_files.json?currtime={milliseconds}")).get("progression"):
        js.progression_presets.append(json.loads(ajax_call("static/presets/" + file)))

    # Load our pointer info from the JSON database
    js.pointer_addresses = json.loads(js.getFile("./static/patches/pointer_addresses.json"))

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    # Add custom Jinja2 filter functions.
    templateEnv.filters["plando_item_restrict"] = PlandoItemFilter
    templateEnv.filters["plando_minigame_restrict"] = PlandoMinigameFilter
    templateEnv.filters["plando_shop_sort"] = PlandoShopSortFilter
    template = templateEnv.get_template("base.html.jinja2")
    # Add custom Jinja2 functions.
    template.globals.update({"plando_option_class_annotation": PlandoOptionClassAnnotation})
    rendered = await template.render(
        minigames=MinigameSelector,
        misc_changes=QoLSelector,
        hard_mode=HardSelector,
        enemies=EnemySelector,
        excluded_songs=ExcludedSongsSelector,
        itemRando=ItemRandoSelector,
        keys=KeySelector,
        glitches=GlitchSelector,
        helm_hurry_items=HHItemSelector,
        vanilla_warps=VanillaBananaportSelector,
        plando_items=PlannableItems,
        plando_minigames=PlannableMinigames,
        plando_panels=PlandomizerPanels,
        plando_spawns=PlannableSpawns,
        points_spread=PointSpreadSelector,
        starting_moves=StartingMoveSelector,
    )
    js.document.documentElement.innerHTML = ""
    js.document.open()
    js.document.write(rendered)
    js.document.close()


# Run the script (This will be run as async later on)
initialize()
