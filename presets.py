"""Manage default data on the form."""
from level_progression import LevelProgression
from browser import window, document
import random


def randomseed(event):
    """Randomly generate a seed ID."""
    document["seed"].value = str(random.randint(100000, 999999))


def set_troff_preset(event):
    """Set the troff n Scoff Presets on the page."""
    preset = document["troff_selected"].text.splitlines()[
        document["troff_selected"].selectedIndex
    ]
    presets = LevelProgression().troff_presets()
    response = []
    if presets.Value.get(preset):
        for val in presets.Value.get(preset):
            response.append(val)
    count = 0
    for pre in response:
        document["troff_" + str(count)].value = pre.Value
        document["troff_" + str(count)].title = pre.ToolTip
        count += 1


def set_blocker_preset(event):
    """Set the Blocker presets on the page."""
    preset = document["blocker_selected"].text.splitlines()[
        document["blocker_selected"].selectedIndex
    ]
    presets = LevelProgression().blocker_presets()
    response = []
    if presets.Value.get(preset):
        for val in presets.Value.get(preset):
            response.append(val)
    count = 0
    for pre in response:
        document["blocker_" + str(count)].value = pre.Value
        document["blocker_" + str(count)].title = pre.ToolTip
        count += 1


def key_up(event):
    """Limits inputs from input boxes on keypress.

    Args:
        event (domevent): The DOMEvent data.

    Returns:
        bool: False if we need to stop the event.
    """
    if "troff" in event.target.id:
        try:
            if int(event.target.value) > 500:
                event.preventDefault()
                document[event.target.id].value = 500
                return False
            elif int(event.target.value) < 1:
                event.preventDefault()
                document[event.target.id].value = 1
                return False
            else:
                document[event.target.id].value = str(event.target.value)
        except Exception:
            event.preventDefault()
            document[event.target.id].value = 1
            return False
    if "blocker" in event.target.id:
        try:
            if int(event.target.value) > 200:
                event.preventDefault()
                document[event.target.id].value = 200
                return False
            elif int(event.target.value) < 0:
                event.preventDefault()
                document[event.target.id].value = 0
                return False
            else:
                document[event.target.id].value = str(event.target.value)
        except Exception:
            event.preventDefault()
            document[event.target.id].value = 0
            return False


document["seed_button"].bind("click", randomseed)
document["troff_selected"].bind("change", set_troff_preset)
document["blocker_selected"].bind("change", set_blocker_preset)
randomseed(None)
for i in range(0, 8):
    try:
        document["blocker_" + str(i)].bind("keypress", key_up)
        document["troff_" + str(i)].bind("keypress", key_up)
    except Exception:
        pass
