"""Webworker module to run python via pyodide."""
from browser import bind, self
from urllib.parse import urlparse


@bind(self, "message")
def message(evt):
    """Inbound message from the webworker to run against pyodide.

    Args:
        evt (javascript.object): Javascript object that can be converted to a dict.
    """
    data = dict(evt.data)

    async def load():
        self.importScripts("https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js")
        self.pyodide = await self.loadPyodide(
            {
                "indexURL": "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/",
            }
        )
        await self.pyodide.loadPackage("micropip")
        url = urlparse(str(self.location.href).replace("blob:", ""))
        domain = url.scheme + "://" + url.netloc + "/"
        await self.pyodide.runPythonAsync(
            "import micropip\nawait micropip.install('pyodide-importer')\nfrom pyodide_importer import register_hook\nregister_hook('"
            + domain
            + "')"
        )
        resp = self.pyodide.runPython(data.get("func"))
        data["response"] = resp
        self.send(data)

    load().send(None)
