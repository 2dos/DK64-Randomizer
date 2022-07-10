"""Generate UI elements via jinja2 to display on page load."""
import json

import micropip
from jinja2 import Environment, FunctionLoader
import time

import js
from js import document


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
    # await micropip.install("pyodide-importer")
    url = js.window.location.origin
    await micropip.install(f"{url}/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl")
    await micropip.install("pillow")
    # Against normal logic we have to import the hook register because we install it as we load the page
    from pyodide_importer import register_hook  # type: ignore  # noqa

    try:
        register_hook("/")
    except Exception:
        pass
    js.listeners = []
    js.progression_presets = []
    js.background_worker = None

    def ajax_call(file):
        resp = js.getFile(file)
        return resp

    def loader_func(template_name):
        milliseconds = int(round(time.time() * 1000))
        return ajax_call("templates/" + f"{template_name}?currtime={milliseconds}")

    milliseconds = int(round(time.time() * 1000))
    for file in json.loads(ajax_call(f"static/presets/preset_files.json?currtime={milliseconds}")).get("progression"):
        js.progression_presets.append(json.loads(ajax_call("static/presets/" + file)))

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("base.html.jinja2")
    rendered = await template.render()
    js.document.documentElement.innerHTML = ""
    js.document.open()
    js.document.write(rendered)
    js.document.close()

    # Load settings from the cookies if it exists
    try:
        cookie_data = document.cookie
        if cookie_data:
            for cookie in cookie_data.split(";"):
                if "settings=" in cookie:
                    settings_cookie = str(cookie).replace("settings=", "")
                    break
            json_data = json.loads(settings_cookie)
            for key in json_data:
                try:
                    # TODO: Validate this still works now that we switched engines
                    document.getElementById(key).value = json_data[key]
                except Exception:
                    pass
    except Exception:
        pass

    # Load our pointer info from the JSON database
    js.pointer_addresses = json.loads(js.getFile("./static/patches/pointer_addresses.json"))


# Run the script (This will be run as async later on)
initialize()
