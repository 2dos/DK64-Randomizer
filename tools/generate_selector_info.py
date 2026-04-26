"""Build-time generator: populate SelectorInfo proto from Python selector sources."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.protobuf import json_format
from google.protobuf.struct_pb2 import Struct

from randomizer.Enums.Types import ItemRandoSelector, KeySelector, ItemRandoFillerSelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Lists.HardMode import HardBossSelector, HardSelector
from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
from randomizer.Lists.Logic import GlitchSelector, TrickSelector
from randomizer.Lists.Minigame import MinigameSelector
from randomizer.Lists.Multiselectors import FasterCheckSelector, QoLSelector, RemovedBarrierSelector, CBRandoSelector, RandomColorSelector, BossesSelector
from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableCustomLocations, PlannableItems, PlannableKroolPhases, PlannableMinigames, PlannableSpawns
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector
from randomizer.proto_gen import selector_info_pb2

_REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
_PB_OUT = os.path.join(_REPO_ROOT, "static", "data", "selector_info.pb")
_JS_OUT = os.path.join(_REPO_ROOT, "static", "js", "selector_info.js")


def _fill_entries(target_list, source):
    """Populate a repeated SelectorEntry field from a list of dicts."""
    for item in source:
        entry = target_list.add()
        entry.name = str(item.get("name", ""))
        entry.value = str(item.get("value", ""))
        entry.tooltip = str(item.get("tooltip", ""))
        if "shift" in item and item["shift"] is not None:
            entry.shift = int(item["shift"])
        if "default" in item and item["default"] is not None:
            entry.default = int(item["default"])
        if "check_count" in item:
            entry.check_count = int(item["check_count"])
        if "item_count" in item:
            entry.item_count = int(item["item_count"])
        if "is_check" in item:
            entry.is_check = bool(item["is_check"])
        if "tied" in item and item["tied"] is not None:
            entry.tied = str(item["tied"])
        if "num_val" in item:
            entry.num_val = int(item["num_val"])


def _json_to_struct(data) -> Struct:
    """Convert a JSON-serialisable Python dict to google.protobuf.Struct."""
    s = Struct()
    if isinstance(data, dict):
        s.update(json.loads(json.dumps(data)))
    return s


def build() -> selector_info_pb2.SelectorInfo:
    """Build and return a fully-populated SelectorInfo message."""
    msg = selector_info_pb2.SelectorInfo()

    _fill_entries(msg.minigames, MinigameSelector)
    _fill_entries(msg.misc_changes, QoLSelector)
    _fill_entries(msg.bosses, BossesSelector)
    _fill_entries(msg.hard_mode, HardSelector)
    _fill_entries(msg.hard_bosses, HardBossSelector)
    _fill_entries(msg.enemies, EnemySelector)
    _fill_entries(msg.excluded_songs, ExcludedSongsSelector)
    _fill_entries(msg.random_colors, RandomColorSelector)
    _fill_entries(msg.song_filters, SongFilteringSelector)
    _fill_entries(msg.item_rando, ItemRandoSelector)
    _fill_entries(msg.item_filler, ItemRandoFillerSelector)
    _fill_entries(msg.keys, KeySelector)
    _fill_entries(msg.glitches, GlitchSelector)
    _fill_entries(msg.tricks, TrickSelector)
    _fill_entries(msg.helm_hurry_items, HHItemSelector)
    _fill_entries(msg.vanilla_warps, VanillaBananaportSelector)
    _fill_entries(msg.plando_items, PlannableItems)
    _fill_entries(msg.plando_minigames, PlannableMinigames)
    _fill_entries(msg.plando_phases, PlannableKroolPhases)
    _fill_entries(msg.plando_spawns, PlannableSpawns)
    _fill_entries(msg.points_spread, PointSpreadSelector)
    _fill_entries(msg.custom_starting_moves, CustomStartingMoveSelector)
    _fill_entries(msg.remove_barriers, RemovedBarrierSelector)
    _fill_entries(msg.faster_checks, FasterCheckSelector)
    _fill_entries(msg.cb_rando_levels, CBRandoSelector)

    msg.plando_custom_locations.CopyFrom(_json_to_struct(PlannableCustomLocations))
    msg.plando_panels.CopyFrom(_json_to_struct(PlandomizerPanels))
    msg.select_song_panel.CopyFrom(_json_to_struct(MusicSelectionPanel))
    msg.select_songs.CopyFrom(_json_to_struct(PlannableSongs))

    return msg


def build_json_dict(msg: selector_info_pb2.SelectorInfo) -> dict:
    """Convert proto message to a JSON-compatible dict matching the legacy API shape."""
    d = json_format.MessageToDict(
        msg,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )
    # Rename the one camelCase key that templates expect as `itemRando`
    if "item_rando" in d:
        d["itemRando"] = d.pop("item_rando")
    return d


def main():
    """Entry point: build message, write .pb binary and JS bootstrap artifacts."""
    msg = build()

    # Write binary proto
    serialized = msg.SerializeToString()
    os.makedirs(os.path.dirname(_PB_OUT), exist_ok=True)
    with open(_PB_OUT, "wb") as f:
        f.write(serialized)
    print(f"Wrote {_PB_OUT} ({len(serialized)} bytes)")

    # Write JS bootstrap — window.SELECTOR_INFO is the plain JSON object.
    # Templates and all existing JS read it exactly as they read the former AJAX response.
    data = build_json_dict(msg)
    js_payload = json.dumps(data, sort_keys=False, indent=2)
    os.makedirs(os.path.dirname(_JS_OUT), exist_ok=True)
    with open(_JS_OUT, "w") as f:
        f.write("// Auto-generated by tools/generate_selector_info.py — do not edit.\n")
        f.write(f"window.SELECTOR_INFO = {js_payload};\n")
    print(f"Wrote {_JS_OUT} ({len(js_payload)} chars JSON)")


if __name__ == "__main__":
    main()
