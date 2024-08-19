"""Generate UI elements via jinja2 to display on page load."""

import json
import PIL
from jinja2 import Environment, FunctionLoader
from pyodide_importer import register_hook  # type: ignore  # noqa
import js

register_hook("/")  # type: ignore  # noqa
# Module of Lists used for list_selector macros
from randomizer.Enums.Types import ItemRandoSelector, KeySelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Lists.HardMode import HardSelector, HardBossSelector
from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
from randomizer.Lists.Logic import GlitchSelector
from randomizer.Lists.Minigame import MinigameSelector
from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableCustomLocations, PlannableItems, PlannableMinigames, PlannableSpawns, PlannableSwitches
from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectFilter, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector

# Module of lists and utils used for plandomizer
from randomizer.PlandoUtils import PlandoCustomLocationFilter, PlandoCustomLocationItemFilter, PlandoItemFilter, PlandoMinigameFilter, PlandoOptionClassAnnotation, PlandoShopSortFilter


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
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
    js.rom_symbols = json.loads(js.getFile("./static/patches/symbols.json"))

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    # Add custom Jinja2 filter functions.
    templateEnv.filters["music_select_restrict"] = MusicSelectFilter
    templateEnv.filters["plando_custom_loc_restrict"] = PlandoCustomLocationFilter
    templateEnv.filters["plando_custom_loc_item_restrict"] = PlandoCustomLocationItemFilter
    templateEnv.filters["plando_item_restrict"] = PlandoItemFilter
    templateEnv.filters["plando_minigame_restrict"] = PlandoMinigameFilter
    templateEnv.filters["plando_shop_sort"] = PlandoShopSortFilter
    navtemplate = templateEnv.get_template("nav-tabs.html.jinja2")
    template = templateEnv.get_template("base.html.jinja2")
    # Add custom Jinja2 functions.
    template.globals.update({"plando_option_class_annotation": PlandoOptionClassAnnotation})
    rendered = await template.render(
        minigames=MinigameSelector,
        misc_changes=QoLSelector,
        hard_mode=HardSelector,
        hard_bosses=HardBossSelector,
        enemies=EnemySelector,
        excluded_songs=ExcludedSongsSelector,
        song_filters=SongFilteringSelector,
        itemRando=ItemRandoSelector,
        keys=KeySelector,
        glitches=GlitchSelector,
        helm_hurry_items=HHItemSelector,
        vanilla_warps=VanillaBananaportSelector,
        plando_custom_locations=PlannableCustomLocations,
        plando_items=PlannableItems,
        plando_minigames=PlannableMinigames,
        plando_panels=PlandomizerPanels,
        plando_spawns=PlannableSpawns,
        plando_switches=PlannableSwitches,
        points_spread=PointSpreadSelector,
        custom_starting_moves=CustomStartingMoveSelector,
        select_song_panel=MusicSelectionPanel,
        select_songs=PlannableSongs,
        remove_barriers=RemovedBarrierSelector,
        faster_checks=FasterCheckSelector,
    )
    nav_rendered = await navtemplate.render()
    # get the "tab-data" div and replace it with the rendered template
    js.jquery("#tab-data").html(rendered)
    js.jquery("#nav-tab-list").html(nav_rendered)


# Run the script (This will be run as async later on)
initialize()
