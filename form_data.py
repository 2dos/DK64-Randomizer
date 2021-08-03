"""Builds the default page."""
import json

from browser import document, timer, window
from browser.template import Template

import common
from level_progression import LevelProgression
from misc import Misc
from rando_options import Randomizers

jq = window.jQuery

randos = Randomizers()
progression = LevelProgression()
misc = Misc()

Template("random_tab").render(randos=randos)
Template("level_progression_tab").render(progression=progression)
Template("misc_tab").render(misc=misc)
Template("spoiler_tab").render()


def loading_finished():
    """Run once the loading of the main index has finished."""
    cookie_data = document.cookie
    if cookie_data:
        for cookie in cookie_data.split(";"):
            if "settings=" in cookie:
                settings_cookie = str(cookie).replace("settings=", "")
                break
        json_data = json.loads(settings_cookie)
        for key in json_data:
            try:
                document[key].value = json_data[key]
            except Exception:
                pass
    else:
        if document["blocker_selected"].options[0].value == "Vanilla":
            document["blocker_selected"].dispatchEvent(window.MouseEvent.new("change"))
            document["troff_selected"].dispatchEvent(window.MouseEvent.new("change"))
    common.update_disabled_progression()
    jq("#progressmodal").modal("hide")
    jq("#loading").modal("hide")


timer.set_timeout(loading_finished, 2000)
