// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  console.log("Loading " + file);
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
// run_python_file("ui/__init__.py");

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
            .then(async function (fileContent) {
              if (run_async == true) {
                // load pyodide
                await setup_pyodide();
                console.log("Applying Xdelta Patch");
                apply_conversion();
                apply_xdelta(fileContent);
                window["event_response_data"] = data;
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
              } else {
                shared_url_ui(data);
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
async function shared_url_ui(data) {
  // Dictionary to store the extracted variables
  let extracted_variables = {};
  var decodedData = base64ToArrayBuffer(data);

  // Extract the contents of the zip file
  let zip = await JSZip.loadAsync(decodedData);
  let promises = Object.keys(zip.files).map(async (file_name) => {
    let content = await zip.file(file_name).async("arraybuffer");
    let variable_name = file_name.split(".")[0];
    extracted_variables[variable_name] = content;
  });

  // Wait for all files to be processed
  await Promise.all(promises);

  let seed_number = new TextDecoder("utf-8").decode(extracted_variables["seed_number"]);
  let seed_id = new TextDecoder("utf-8").decode(extracted_variables["seed_id"]);
  let version = extracted_variables["version"]
    ? new TextDecoder("utf-8").decode(extracted_variables["version"])
    : "0.0.0";

  let hash_id;
  try {
    hash_id = JSON.parse(new TextDecoder("utf-8").decode(extracted_variables["hash"]));
  } catch (error) {
    hash_id = null;
  }
  let current_version = await getVersion();
  // Make sure we re-load the seed id for patch file creation
  window["event_response_data"] = data;

  let split_version = version.split(".");
  let patch_major = split_version[0];
  let patch_minor = split_version[1];
  let patch_patch = split_version[2];
  // Now using current_version lets split patch version
  let split_current_version = current_version.split(".");
  let major = split_current_version[0];
  let minor = split_current_version[1];
  let patch = split_current_version[2];
  if (major !== patch_major || minor !== patch_minor) {
    document.getElementById("patch_version_warning").hidden = false;
    document.getElementById(
      "patch_warning_message"
    ).innerHTML = `This patch was generated with version ${patch_major}.${patch_minor}.${patch_patch} of the randomizer, but you are using version ${major}.${minor}.${patch}. Cosmetic packs have been disabled for this patch.`;
  }
  let json_data = new TextDecoder("utf-8").decode(
    extracted_variables["spoiler_log"]
  );
  await generateSpoiler(json_data);
  setTimeout(async () => {
    let hash_data = [];
    try {
      apply_conversion();
      hash_data = await get_hash_images("browser", "hash");
    } catch (error) {
      console.log(error)

    }
    if (hash_data.length > 0) {
      document.getElementById("hashdiv").innerHTML = "";
      for (let i = 0; i < hash_id.length; i++) {
        let img = document.getElementById("hash" + i);
        img.src = "data:image/jpeg;base64," + hash_data[hash_id[i]];
        // Flip Horizontally
        img.style = "transform: scaleX(-1);";
      }
    } else {
      document.getElementById("hashdiv").innerHTML =
        "No ROM Cached, No Hash Images Loaded.";
    }
    document.getElementById("nav-settings-tab").style.display = "";
    document.getElementById("spoiler_log_block").style.display = "";
    document.getElementById("generated_seed_id").innerHTML = seed_id;

    // Set the current URL to the seed ID so that it can be shared without reloading the page
    window.history.pushState(
      "generated_seed",
      seed_number,
      `/randomizer?seed_id=${seed_number}`
    );
    check_spoiler_unlocked(seed_number);


    $("#nav-settings-tab").tab("show");
    check_seed_info_tab();
  }, 500);
}
async function getVersion() {
  try {
    const response = await fetch("/version.py");
    const text = await response.text();

    // Use regex to capture the version string
    const versionMatch = text.match(/version\s*=\s*['"](.+?)['"]/);
    if (versionMatch && versionMatch[1]) {
      const version = versionMatch[1];
      console.log("Version:", version);
      return version;
    } else {
      throw new Error("Version not found");
    }
  } catch (error) {
    console.error("Error fetching version:", error);
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
  apply_conversion();
  $("#progressmodal").modal("show");
  $("#patchprogress").width(0);
  $("#progress-text").text("Initializing");
  get_hash_images("browser", "loading-fairy");
  get_hash_images("browser", "loading-dead");

  apply_patch(window.event_response_data, true);
}

window["apply_download"] = apply_download;
window["apply_patch"] = apply_patch;
window["plando_import_filebox"] = plando_import_filebox;
window["imported_plando_json"] = imported_plando_json;
window["apply_xdelta"] = apply_xdelta;
