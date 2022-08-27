"""Generate UI elements via jinja2 to display on page load."""
import time

import micropip
from jinja2 import Environment, FunctionLoader

import js


async def initialize():
    """Shifted code into an async function so we can properly lint await calls."""
    url = js.window.location.origin
    await micropip.install(
        [
            f"{url}/static/py_libraries/charset_normalizer-2.1.0-py3-none-any.whl",
            f"{url}/static/py_libraries/urllib3-1.26.11-py2.py3-none-any.whl",
            f"{url}/static/py_libraries/certifi-2022.6.15-py3-none-any.whl",
            f"{url}/static/py_libraries/idna-3.3-py3-none-any.whl",
            f"{url}/static/py_libraries/requests-2.28.1-py3-none-any.whl",
            f"{url}/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl",
        ],
        deps=False,
    )
    # Against normal logic we have to import the hook register because we install it as we load the page
    from pyodide_importer import register_hook  # type: ignore  # noqa

    try:
        register_hook("/")
    except Exception:
        pass

    # We import version after register_hook so we can actively use it.
    import version

    js.listeners = []
    js.progression_presets = []
    js.background_worker = None

    def ajax_call(file):
        resp = js.getFile(file)
        return resp

    def loader_func(template_name):
        milliseconds = int(round(time.time() * 1000))
        return ajax_call("templates/" + f"{template_name}?currtime={milliseconds}")

    templateEnv = Environment(loader=FunctionLoader(loader_func), enable_async=True)
    template = templateEnv.get_template("frontpage.html.jinja2")
    rendered = await template.render(version=version)
    js.document.documentElement.innerHTML = ""
    js.document.open()
    js.document.write(rendered)
    js.document.close()


# Run the script (This will be run as async later on)
initialize()
