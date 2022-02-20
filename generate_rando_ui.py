"""Generate UI elements via jinja2 to display on page load."""
import json

import js
import micropip
from jinja2 import Environment, FunctionLoader
from js import document
from pyodide import to_js


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
    await micropip.install("pyodide-importer")
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
        resp = js.jquery.ajax(js.Object.fromEntries(to_js({"type": "GET", "url": file, "async": False}))).responseText
        return resp

    def loader_func(template_name):
        return ajax_call("templates/" + template_name)

    for file in json.loads(ajax_call("static/presets/preset_files.json")).get("progression"):
        js.progression_presets.append(json.loads(ajax_call("static/presets/" + file)))

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("base.html.jinja2")
    rendered = await template.render()
    js.document.documentElement.innerHTML = ""
    js.document.open()
    js.document.write(rendered)
    js.document.close()

    # Load settings from the cookies if it exists
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

    # Load our pointer info from the JSON database
    js.pointer_addresses = json.loads(js.jquery.ajax(js.Object.fromEntries(to_js({"url": "./static/patches/pointer_addresses.json", "async": False}))).responseText)


# Run the script (This will be run as async later on)
initialize()
