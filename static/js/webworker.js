onmessage = async function (e) {
  content = JSON.parse(e.data);
  importScripts("https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js");
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/",
  });
  await pyodide.loadPackage("micropip");
  await pyodide.runPythonAsync(
    `
    import micropip
    await micropip.install('pyodide-importer')
    from pyodide_importer import register_hook
    register_hook('` +
      this.location.origin +
      `/')
    `
  );
  resp = pyodide.runPython(content["func"]);
  content.response = resp;
  postMessage(content);
};
