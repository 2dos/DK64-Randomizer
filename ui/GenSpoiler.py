"""Push jinja2 file to spoiler."""

import json
import time

from jinja2 import Environment, FunctionLoader

import js


def ajax_call(file):
    """Get file."""
    resp = js.getFile(file)
    return resp


def loader_func(template_name):
    """Load template file."""
    milliseconds = int(round(time.time() * 1000))
    return ajax_call("templates/" + f"{template_name}?currtime={milliseconds}")


async def GenerateSpoiler(spoiler):
    """Pass spoiler to jinja2 file and modify DOM with rendered jinja2 file."""
    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("spoiler.html.jinja2")
    trimmed_spoiler = ""
    for x in json.dumps(spoiler).split("\n"):
        trimmed_spoiler += x.strip()
    formatted_spoiler = json.loads(trimmed_spoiler)
    # modified_spoiler = formatted_spoiler.pop("Settings")
    # modified_spoiler.update(formatted_spoiler)
    # print(modified_spoiler)

    lzr_type = "none"
    if formatted_spoiler["Settings"]["Loading Zones Shuffled"] == "all":
        if formatted_spoiler["Settings"]["Decoupled Loading Zones"] is False:
            lzr_type = "coupled"
        else:
            lzr_type = "decoupled"

    rendered = await template.render(spoiler=formatted_spoiler, lzr_type=lzr_type)
    js.document.getElementById("spoiler_log_text").value = json.dumps(spoiler, indent=4)
    js.document.getElementById("spoiler_log_text").innerHTML = rendered
