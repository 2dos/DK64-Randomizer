// Worker script for pyodide scripts
onmessage = async function (e) {
  // Read the passed string as JSON
  content = JSON.parse(e.data);
  // Reload Pyodide
  // TODO: We should probably see about caching this load
  try {
    importScripts("./pyodide/pyodide.js");
    pyodide = await loadPyodide();
    // Load Micropip so we can load the importers
    await pyodide.loadPackage("micropip");

    // Load all our website pages uses the origin of this function
    await pyodide.runPythonAsync(
      `
      import micropip
      await micropip.install(
          [
              "` + this.location.origin + `/static/py_libraries/charset_normalizer-2.1.0-py3-none-any.whl",
              "` + this.location.origin + `/static/py_libraries/urllib3-1.26.11-py2.py3-none-any.whl",
              "` + this.location.origin + `/static/py_libraries/certifi-2022.6.15-py3-none-any.whl",
              "` + this.location.origin + `/static/py_libraries/idna-3.3-py3-none-any.whl",
              "` + this.location.origin + `/static/py_libraries/requests-2.28.1-py3-none-any.whl",
              "` + this.location.origin + `/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl",
          ],
          deps=False
      )
      if "` + this.location.origin + `" in ["dev.dk64randomizer.com", "dk64randomizer.com"]:
        await micropip.install("` + this.location.origin + `/static/py_libraries/dk64rando-1.0.0-py3-none-any.whl")
      from pyodide_importer import register_hook
      register_hook('` +
        this.location.origin +
        `/')
      `
    );
  }
  catch {}
  // Run the passed function
  resp = pyodide.runPython(content["func"]);
  delete content.func
  content.response = resp;
  // Return the response as json
  postMessage(content);
};
