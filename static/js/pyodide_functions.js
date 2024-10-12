// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  console.log("Loading " + file);
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
// run_python_file("ui/__init__.py");
var imported_music_json = "";

async function music_selection_filebox() {
  // load pyodide
  await setup_pyodide();
  let input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";

  input.onchange = async (e) => {
    let file = e.target.files[0];
    let json_text = await file.text();
    imported_music_json = json_text;
    pyodide.runPythonAsync(`
        import js
        from ui.music_select import import_music_selections
        import_music_selections(js.imported_music_json)
      `);
  };

  input.click();
}

var imported_plando_json = "";

async function plando_import_filebox() {
  // load pyodide
  await setup_pyodide();
  let input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";

  input.onchange = async (e) => {
    let file = e.target.files[0];
    let json_text = await file.text();
    imported_plando_json = json_text;
    pyodide.runPythonAsync(`
        import js
        from ui.plando_settings import import_plando_options
        import_plando_options(js.imported_plando_json)
      `);
  };

  input.click();
}

async function apply_patch(data, run_async) {
  // load pyodide
  await setup_pyodide();
  // Base64 decode the response
  event_response_data = data;
  var decodedData = base64ToArrayBuffer(data);
  zip = new JSZip();

  try {
    // Load the zip file data into JSZip
    const zipFile = await zip.loadAsync(decodedData);

    // Create an array to store all the promises
    const promises = [];
    query_stats();
    // Iterate over each file in the zip
    zip.forEach(function (relativePath, zipEntry) {
      if (!zipEntry.dir) {
        // Extract the file content as a string or other appropriate format
        // Store the file content in a variable with a name derived from the file name
        fileName = zipEntry.name.replace(/[^a-zA-Z0-9]/g, "_");
        if (fileName == "patch") {
          // Create a promise for each async operation and add it to the array
          const promise = zipEntry
            .async("uint8array")
            .then(function (fileContent) {
              console.log("Applying Xdelta Patch");
              apply_conversion();
              apply_xdelta(fileContent);

              if (run_async == true) {
                
                // Return the promise for pyodide.runPythonAsync
                return pyodide.runPythonAsync(`from pyodide_importer import register_hook  # type: ignore  # noqa
try:
  register_hook("/")  # type: ignore  # noqa
except Exception:
  pass
import js
from randomizer.Patching.ApplyLocal import patching_response
patching_response(str(js.event_response_data), from_patch_gen=True)
                `);
              }
              else{
                // Return the promise for pyodide.runPythonAsync
                return pyodide.runPythonAsync(`from pyodide_importer import register_hook  # type: ignore  # noqa
try:
  register_hook("/")  # type: ignore  # noqa
except Exception:
  pass
import js
from randomizer.Patching.ApplyLocal import patching_response
patching_response(str(js.event_response_data), from_patch_gen=False)
                `);
              }
            });

          promises.push(promise);
        }
      }
    });

    // Wait for all the promises to resolve
    await Promise.all(promises);
  } catch (error) {
    console.error("Error unzipping the file:", error);
  }
}
async function apply_download() {
  if (
    document.getElementById("rom").value.trim().length === 0 ||
    !document.getElementById("rom").classList.contains("is-valid")
  ) {
    document.getElementById("rom").select();
    if (!document.getElementById("rom").classList.contains("is-invalid")) {
      document.getElementById("rom").classList.add("is-invalid");
      return;
    }
  }
  console.log("Applying Download");
  await setup_pyodide();
  return pyodide.runPythonAsync(`from pyodide_importer import register_hook  # type: ignore  # noqa
try:
  register_hook("/")  # type: ignore  # noqa
except Exception:
  pass
import js
from randomizer.Patching.ApplyLocal import patching_response
patching_response(str(js.event_response_data), from_patch_gen=True)
    `);
}

window["apply_download"] = apply_download;
window["apply_patch"] = apply_patch;
window["music_selection_filebox"] = music_selection_filebox;
window["plando_import_filebox"] = plando_import_filebox;
window["imported_music_json"] = imported_music_json;
window["imported_plando_json"] = imported_plando_json;
window["apply_xdelta"] = apply_xdelta;
