"""Import functions within the UI folder to have them run on load of the UI."""

try:
    from pyodide_importer import register_hook  # type: ignore  # noqa

    register_hook("/")  # type: ignore  # noqa
except Exception:
    pass
import ui.plando_settings
