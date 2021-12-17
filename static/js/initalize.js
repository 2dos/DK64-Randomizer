// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
run_python_file("ui/__init__.py");
async function sleep(seconds, func, args) {
  setTimeout(function () {
    func(...args);
  }, seconds * 1000);
}