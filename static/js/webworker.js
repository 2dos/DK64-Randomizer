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
      await micropip.install("` + this.location.origin + `/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl")
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
