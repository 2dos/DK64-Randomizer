"""Generate UI elements via jinja2 to display on page load."""

import json

import micropip
from jinja2 import Environment, FunctionLoader

import js


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
    # await micropip.install("pyodide-importer")
    url = js.window.location.origin
    await micropip.install(
        [
            f"{url}/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl",
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
    from randomizer.Lists.HardMode import HardSelector
    from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
    from randomizer.Lists.Logic import GlitchSelector
    from randomizer.Lists.Minigame import MinigameSelector
    from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableItems, PlannableMinigames, PlannableSpawns
    from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
    from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectFilter, MusicSelectionPanel, PlannableSongs
    from randomizer.Lists.Warps import VanillaBananaportSelector
    from randomizer.Lists.WrinklyHints import PointSpreadSelector

    # Module of lists and utils used for plandomizer
    from randomizer.PlandoUtils import PlandoItemFilter, PlandoMinigameFilter, PlandoOptionClassAnnotation, PlandoShopSortFilter

    js.listeners = []
    js.progression_presets = []
    js.random_settings_presets = []
    js.background_worker = None

    def ajax_call(file):
        resp = js.getFile(file)
        return resp

    def loader_func(template_name):
        return ajax_call("templates/" + f"{template_name}")

    if js.location.hostname == "dev.dk64randomizer.com":
        presets_url = "https://dev-generate.dk64rando.com/get_presets?return_blank=true"
    elif js.location.hostname == "dk64randomizer.com":
        presets_url = "https://generate.dk64rando.com/get_presets?return_blank=true"
    else:
        presets_url = js.location.origin + "/get_presets?return_blank=true"

    for file in json.loads(ajax_call(presets_url)):
        js.progression_presets.append(file)
    for file in json.loads(ajax_call(f"static/presets/weights/weights_files.json")):
        js.random_settings_presets.append(file)

    # Load our pointer info from the JSON database
    js.pointer_addresses = json.loads(js.getFile("./static/patches/pointer_addresses.json"))

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    # Add custom Jinja2 filter functions.
    templateEnv.filters["music_select_restrict"] = MusicSelectFilter
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
        custom_starting_moves=CustomStartingMoveSelector,
        select_song_panel=MusicSelectionPanel,
        select_songs=PlannableSongs,
        remove_barriers=RemovedBarrierSelector,
        faster_checks=FasterCheckSelector,
    )
    # get the "tab-data" div and replace it with the rendered template
    js.jquery("#tab-data").html(rendered)
    await micropip.install(
        [
            f"{url}/static/js/pyodide/Pillow-10.0.0-cp311-cp311-emscripten_3_1_45_wasm32.whl",
        ],
        deps=False,
    )


# Run the script (This will be run as async later on)
initialize()
