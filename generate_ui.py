"""Generate UI elements via jinja2 to display on page load."""
import js
import micropip
from jinja2 import Environment, FunctionLoader
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

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("frontpage.html.jinja2")
    rendered = await template.render()
    js.document.documentElement.innerHTML = ""
    js.document.open()
    js.document.write(rendered)
    js.document.close()


# Run the script (This will be run as async later on)
initialize()
