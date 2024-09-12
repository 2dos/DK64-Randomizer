if (typeof window.RufflePlayer !== "undefined") {
  // Ruffle extension is loaded
  var modal = document.createElement("div");
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "9999";

  var modalContent = document.createElement("div");
  modalContent.style.backgroundColor = "#333";
  modalContent.style.padding = "20px";
  modalContent.style.borderRadius = "5px";
  modalContent.style.textAlign = "center";

  var message = document.createElement("p");
  message.textContent =
    "The Ruffle extension causes issues with this site (and we're not really sure why). Please disable it for this site.";
  message.style.color = "#fff";
  message.style.fontFamily = "Arial, sans-serif";
  message.style.fontSize = "16px";

  modalContent.appendChild(message);
  modal.appendChild(modalContent);
  document.body.appendChild(modal);

  // Prevent scrolling while the modal is open
  document.body.style.overflow = "hidden";

  console.log("Ruffle extension is loaded");
} else {
  // Ruffle extension is not loaded
  console.log("Ruffle extension is not loaded");
}
// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  console.log("Loading " + file);
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
run_python_file("ui/__init__.py");
var imported_music_json = "";

function music_selection_filebox() {
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

function plando_import_filebox() {
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
  try {
    pyodide = await loadPyodide();
  } catch {}

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
              apply_xdelta(fileContent);

              if (run_async == true) {
                // Return the promise for pyodide.runPythonAsync
                return pyodide.runPythonAsync(`
                  import js
                  from randomizer.Patching.ApplyLocal import patching_response
                  patching_response(str(js.event_response_data), from_patch_gen=True)
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
