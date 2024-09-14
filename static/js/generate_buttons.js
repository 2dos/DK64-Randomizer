function lanky_file_changed(event) {
    /** On the event of a file being loaded.
    
    Args:
        event (Event): JavaScript event.
    */

    function onload(e) {
        // Load the text of the patch
        const loaded_patch = e.target.result;

        // TODO: Don't just assume the file is valid first
        document.getElementById("patchfileloader").classList.add("is-valid");
        window.loaded_patch = loaded_patch;
    }

    // Attempt to find the loaded file
    const file_input = document.getElementById("patchfileloader");
    const file = file_input.files.length ? file_input.files[0] : null;
    
    const reader = new FileReader();

    // If a file is loaded, set up the event listener to read it as text
    if (file) {
        reader.readAsText(file);
        reader.addEventListener("load", onload);
    }
}

// Bind the function to the change event of the file input
document.getElementById("patchfileloader").addEventListener("change", lanky_file_changed);
var pyodide;
async function generate_previous_seed(event) {
    /** Generate a seed from a previous seed file. */

    // Check if the ROM file box has a file loaded in it
    const romElement = document.getElementById("rom");
    if (romElement.value.trim().length === 0 || !romElement.classList.contains("is-valid")) {
        romElement.select();
        if (!romElement.classList.contains("is-invalid")) {
            romElement.classList.add("is-invalid");
        }
    } else {
        // Show progress update
        await ProgressBar().update_progress(0, "Loading Previous seed and applying data.");
        
        // Apply the conversion
        window.apply_conversion();

        // Additional logic for lanky_from_history can be added here
        await setup_pyodide();
        await pyodide.runPythonAsync(`from pyodide_importer import register_hook  # type: ignore  # noqa
register_hook("/")  # type: ignore  # noqa
from randomizer.Patching.ApplyLocal import patching_response
import js
await patching_response(str(js.get_previous_seed_data()), True, js.document.getElementById("load_patch_file").checked, True)`)
    }
}

// Bind the function to the click event of the element with ID "generate_pastgen_seed"
document.getElementById("generate_pastgen_seed").addEventListener("click", generate_previous_seed);


async function generate_seed_from_patch(event) {
    /** Generate a seed from a patch file. */

    // Check if the ROM file input has a valid file loaded
    const romElement = document.getElementById("rom");
    if (romElement.value.trim().length === 0 || !romElement.classList.contains("is-valid")) {
        romElement.select();
        if (!romElement.classList.contains("is-invalid")) {
            romElement.classList.add("is-invalid");
        }
    } 
    // Check if the patch file input has a valid file loaded
    else {
        const patchElement = document.getElementById("patchfileloader");
        if (patchElement.value.trim().length === 0) {
            patchElement.select();
            if (!patchElement.classList.contains("is-invalid")) {
                patchElement.classList.add("is-invalid");
            }
        } else {
            // Apply the conversion
            window.apply_conversion();
            await setup_pyodide();
            await pyodide.runPythonAsync(`from pyodide_importer import register_hook  # type: ignore  # noqa
register_hook("/")  # type: ignore  # noqa
import js
from randomizer.Patching.ApplyLocal import patching_response
await patching_response(str(js.get_previous_seed_data()), True, js.loaded_patch, True)`)
    
        }
    }
}

// Bind the function to the click event of the element with ID "generate_lanky_seed"
document.getElementById("generate_lanky_seed").addEventListener("click", generate_seed_from_patch);

async function setup_pyodide(){
    try {
        pyodide = await loadPyodide();
    } catch { }
    url = window.location.origin;
    await pyodide.loadPackage(url + "/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl")
    await pyodide.loadPackage("pillow")
    if (location.hostname == "dev.dk64randomizer.com" || location.hostname == "dk64randomizer.com") {
        await pyodide.loadPackage("micropip");
        const micropip = pyodide.pyimport("micropip");
        await micropip.install(url + "/static/py_libraries/dk64rando-1.0.0-py3-none-any.whl")
    }
}

