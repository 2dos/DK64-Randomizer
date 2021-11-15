"""Builds the default page."""
import json

from browser import document, timer, window
from browser.template import Template

import common
from level_progression import LevelProgression
from object_data.form_options import form_options

jq = window.jQuery

progression = LevelProgression()

Template("random_tab")
Template("level_progression_tab").render(progression=progression)
Template("spoiler_tab").render()

for opt in form_options:
    if hasattr(opt, "tab"):
        opt.generate_html()


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
