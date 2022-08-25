from jinja2 import Environment, FunctionLoader
import js
import json
import time

def ajax_call(file):
        resp = js.getFile(file)
        return resp

def loader_func(template_name):
    milliseconds = int(round(time.time() * 1000))
    return ajax_call("templates/" + f"{template_name}?currtime={milliseconds}")

async def GenerateSpoiler(spoiler):
    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("spoiler.html.jinja2")
    trimmed_spoiler = ""
    for x in spoiler.split("\n"):
        trimmed_spoiler += x.strip()=
    formatted_spoiler = json.loads(trimmed_spoiler)
    rendered = await template.render(spoiler=formatted_spoiler)
    js.document.getElementById("spoiler_log_text").innerHTML = rendered