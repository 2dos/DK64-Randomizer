"""Manage default data on the form."""
from level_progression import LevelProgression
from browser import window, document
import random


def randomseed(event):
    """Randomly generate a seed ID."""
    document["seed"].value = str(random.randint(100000, 999999))


def set_troff_preset():
    """Set the troff n Scoff Presets on the page."""
    preset = document["troff_selected"].text.splitlines()[document["troff_selected"].selectedIndex]
    presets = LevelProgression().troff_presets()
    response = []
    for item in presets.Value:
        if item.get(preset):
            for val in item.get(preset):
                response.append(val)
    count = 0
    for pre in response:
        document["troff_" + str(count)].value = pre.Value
        document["troff_" + str(count)].title = pre.ToolTip
        count += 1


def set_blocker_preset():
    """Set the Blocker presets on the page."""
    preset = document["blocker_selected"].text.splitlines()[document["blocker_selected"].selectedIndex]
    presets = LevelProgression().blocker_presets()
    response = []
    for item in presets.Value:
        if item.get(preset):
            for val in item.get(preset):
                response.append(val)
    count = 0
    for pre in response:
        document["blocker_" + str(count)].value = pre.Value
        document["blocker_" + str(count)].title = pre.ToolTip
        count += 1


window.blocker_selectionChanged = set_blocker_preset
window.troff_selectionChanged = set_troff_preset
document["seed_button"].bind("click", randomseed)
randomseed(None)
