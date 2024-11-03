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
from randomizer.Lists.Plandomizer import (
    PlandomizerPanels,
    PlannableCustomLocations,
    PlannableItems,
    PlannableKroolPhases,
    PlannableMinigames,
    PlannableSpawns,
    PlannableSwitches,
)
from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""

    def ajax_call(file):
        resp = js.getFile(file)
        return resp

    def loader_func(template_name):
        return ajax_call("templates/" + f"{template_name}")

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    navtemplate = templateEnv.get_template("nav-tabs.html.jinja2")
    template = templateEnv.get_template("base.html.jinja2")
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
        plando_phases=PlannableKroolPhases,
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
