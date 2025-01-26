function lanky_file_changed(event) {
    /** On the event of a file being loaded.
    
    Args:
        event (Event): JavaScript event.
    */

    function onload(e) {
        // Load the text of the patch
        const loaded_patch = e.target.result;

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
        await apply_patch(get_previous_seed_data(), true)
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
            if (typeof window.romFile === "undefined") {
                document.getElementById("rom").select();
                if (!document.getElementById("rom").classList.contains("is-invalid")) {
                    document.getElementById("rom").classList.add("is-invalid");
                    return;
                }
            }
            // Apply the patch
            await apply_patch(loaded_patch, true)
         }
    }
}

// Bind the function to the click event of the element with ID "generate_lanky_seed"
document.getElementById("generate_lanky_seed").addEventListener("click", generate_seed_from_patch);

async function setup_pyodide() {
    try {
        // Check if pyodide is already loaded
        if (!window.pyodide) {
            pyodide = await loadPyodide();
            const url = window.location.origin;
            await pyodide.loadPackage(url + "/static/py_libraries/pyodide_importer-0.0.2-py2.py3-none-any.whl");
            await pyodide.loadPackage("pillow");
            if (location.hostname == "dev.dk64randomizer.com" || location.hostname == "dk64randomizer.com") {
                await pyodide.loadPackage("micropip");
                const micropip = pyodide.pyimport("micropip");
                await micropip.install(url + "/static/py_libraries/dk64rando-1.0.0-py3-none-any.whl");
            }
        }
    } catch (error) {
        console.error("Error setting up Pyodide:", error);
    }
}

document.getElementById("load_patch_file").addEventListener("click", async function(event) {
    /**
     * Set historical seed text based on the load_patch_file click event.
     *
     * @param {Event} event - JavaScript DOM click event.
     */
    let loadPatchFileElem = document.getElementById("load_patch_file");
    let generatePastgenSeedElem = document.getElementById("generate_pastgen_seed");

    if (loadPatchFileElem.checked) {
        generatePastgenSeedElem.value = "Generate Patch File from History";
    } else {
        generatePastgenSeedElem.value = "Generate Seed from History";
    }
});

function should_clear_setting(select) {
    /**
     * Return true if the select should be cleared when importing settings.
     *
     * @param {HTMLSelectElement} select - The select element to evaluate.
     * @returns {boolean} - Whether the select should be cleared.
     */
    if (document.querySelector("#nav-cosmetics").contains(select)) {
        return false;
    }
    if (document.querySelector("#nav-music").contains(select)) {
        return false;
    }
    if (select.name.startsWith("plando_")) {
        return false;
    }
    // This should now be obsolete, because of the #nav-music clause, but leaving it as-is for safety
    // TODO: change the plando_ clause into a #nav-plando clause and remove the music_select_ clause
    if (select.name.startsWith("music_select_")) {
        return false;
    }
    return true;
}

// Assuming Items and SettingsMap objects are already defined

function serialize_settings(include_plando = false) {
    /**
     * Serialize form settings into an enum-focused JSON object.
     *
     * @returns {object} Dictionary of form settings.
     */
    
    // Remove all the disabled attributes and store them for later
    let disabled_options = [];
    
    let inputElements = document.getElementsByTagName("input");
    for (let element of inputElements) {
        if (element.disabled) {
            disabled_options.push(element);
            element.removeAttribute("disabled");
        }
    }

    let selectElements = document.getElementsByTagName("select");
    for (let element of selectElements) {
        if (element.disabled) {
            disabled_options.push(element);
            element.removeAttribute("disabled");
        }
    }

    let optionElements = document.getElementsByTagName("option");
    for (let element of optionElements) {
        if (element.disabled) {
            disabled_options.push(element);
            element.removeAttribute("disabled");
        }
    }

    // Serialize the form into json
    let form = $("#form").serializeArray();
    let form_data = {};

    // Plandomizer data is processed separately and uses a separate setting string, so it needs to be optionally serializable
    if (include_plando) {
        pyodide.runPython(`from pyodide_importer import register_hook  # type: ignore  # noqa
try:
  register_hook("/")  # type: ignore  # noqa
except Exception:
  pass
import js
import json
from ui.plando_settings import populate_plando_options
plando_form_data = populate_plando_options(js.form)
if plando_form_data:
    js.plando_form_data = json.dumps(plando_form_data)
else:
    js.plando_form_data = "None"
                `);
        let plando_form_data = window.plando_form_data;
        if (plando_form_data !== null && plando_form_data !== undefined && plando_form_data !== "None") {
            form_data["enable_plandomizer"] = true;
            form_data["plandomizer_data"] = JSON.parse(plando_form_data)
        }
    }
    // if plandomizer_data is not present, the plandomizer is disabled so lets just fill in the form_data with that
    if (!form_data["plandomizer_data"]) {
        form_data["enable_plandomizer"] = false;
    }
    

    // Custom music data is also processed separately.
    let music_selection_data = serialize_music_selections(form);
    form_data["music_selections"] = JSON.stringify(music_selection_data);

    function is_number(s) {
        /** Check if a string is a number or not. */
        try {
            let parsed = parseInt(s);
            return !isNaN(parsed);
        } catch (e) {
            return false;
        }
    }

    function is_plando_input(inputName) {
        /** Determine if an input is a plando input. */
        return inputName && inputName.startsWith("plando_");
    }

    function is_starting_move_radio_button(inputName) {
        /** Determine if an input is a starting move checkbox. */
        return inputName && inputName.startsWith("starting_move_box_");
    }

    function is_music_select_input(inputName) {
        /** Determine if an input is a song selection input. */
        return inputName && inputName.startsWith("music_select_");
    }

    function get_enum_or_string_value(valueString, settingName) {
        /** Obtain the enum or string value for the provided setting.
         *
         * @param {string} valueString - The value from the HTML input.
         * @param {string} settingName - The name of the HTML input.
         */
        if (SettingsMap[settingName]) {
            return SettingsMap[settingName][valueString];
        } else {
            return valueString;
        }
    }

    function get_value_or_default(element) {
        /** Get the value or the default if empty.
         *
         * @param {HTMLInputElement} element - The input element.
         */
        if (element.value === "" && element.hasAttribute("default")) {
            return element.getAttribute("default");
        }
        return element.value;
    }

    for (let obj of form) {
        if (is_plando_input(obj.name)) continue;
        if (is_starting_move_radio_button(obj.name)) continue;
        if (is_music_select_input(obj.name)) continue;

        // Verify each object if its value is a string convert it to a bool
        let value = get_value_or_default(document.querySelector(`[name="${obj.name}"]`));

        if (["true", "false"].includes(value.toLowerCase())) {
            form_data[obj.name] = value.toLowerCase() === "true";
        } else if (is_number(value)) {
            form_data[obj.name] = parseInt(value);
        } else {
            form_data[obj.name] = get_enum_or_string_value(value, obj.name);
        }
    }

    // find all input boxes and verify their checked status
    for (let element of inputElements) {
        if (is_plando_input(element.name)) continue;
        if (is_starting_move_radio_button(element.name) && element.checked) {
            continue;
        }
        if (element.type === "checkbox" && !element.checked) {
            if (!form_data[element.name]) {
                form_data[element.name] = false;
            }
        }
    }

    // Re-disable all previously disabled options
    for (let element of disabled_options) {
        element.setAttribute("disabled", "disabled");
    }

    // Create value lists for multi-select options
    for (let element of selectElements) {
        if (element.className.includes("selected")) {
            if (is_plando_input(element.getAttribute("name"))) continue;

            let length = element.options.length;
            let values = [];
            for (let i = 0; i < length; i++) {
                if (element.options[i].selected) {
                    values.push(get_enum_or_string_value(element.options[i].value, element.getAttribute("name")));
                }
            }
            form_data[element.getAttribute("name")] = values;
        }
        if (element.id.startsWith("starting_moves_list_")) {
            let move_list = []
            for (let option of element.options) {
                if (!option.hasAttribute("hidden")) {
                    for (let item in Items) {
                        if (Items[item] === parseInt(option.id.slice(14))) {
                            move_list.push(Items[item]);
                        }
                    }
                }
            }
            form_data[element.id] = move_list;
        }
    }

    return JSON.stringify(form_data);
}

// Event binding for exporting settings to a string
document.getElementById("export_settings").addEventListener("click", export_settings_string);

function export_settings_string(event) {
    /**
     * Click event for exporting settings to a string.
     *
     * @param {object} event - Javascript event object.
     */
    let setting_data = serialize_settings();
    // Convert settings_data back into json from the string
    setting_data = JSON.parse(setting_data);
    let settings_string = encrypt_settings_string_enum(setting_data);
    document.getElementById("settings_string").value = settings_string;
    generateToast("Exported settings string to the setting string input field.");
}

// Event binding for generating a seed
document.getElementById("trigger_download_event").addEventListener("click", generate_seed);

async function generate_seed(event) {
    /**
     * Generate a seed based off the current settings.
     *
     * @param {object} event - Javascript click event.
     */
    // Hide the div for settings errors.
    let settings_errors_element = document.getElementById("settings_errors");
    settings_errors_element.style.display = "none";

    // Check if the rom filebox has a file loaded in it.
    if (document.getElementById("rom").value.trim().length === 0 || 
        !document.getElementById("rom").classList.contains("is-valid")) {
        document.getElementById("rom").select();
        if (!document.getElementById("rom").classList.contains("is-invalid")) {
            document.getElementById("rom").classList.add("is-invalid");
        }
    } else {
        // Do a double check that romFile var exists, if its not, then the rom file is not loaded, throw an invalid class on the rom file box.
        if (typeof window.romFile === "undefined") {
            document.getElementById("rom").select();
            if (!document.getElementById("rom").classList.contains("is-invalid")) {
                document.getElementById("rom").classList.add("is-invalid");
                return;
            }
        }
        // The data is serialized outside of the loop, because validation occurs
        // here and we might stop before attempting to generate a seed.
        let plando_enabled = document.getElementById("enable_plandomizer").checked;
        let form_data = serialize_settings(plando_enabled);
        form_data = JSON.parse(form_data);
        if (form_data["enable_plandomizer"]) {
            //let plando_errors = validate_plando_options(form_data);
            pyodide.runPython(`from pyodide_importer import register_hook  # type: ignore  # noqa
try:
    register_hook("/")  # type: ignore  # noqa
except Exception:
    pass
import js
from ui.plando_validation import validate_plando_options
plando_errors = validate_plando_options(js.form)
js.plando_errors = plando_errors
                            `);
            let plando_errors = window.plando_errors;
            // If errors are returned, the plandomizer options are invalid.
            // Do not attempt to generate a seed.
            if (plando_errors.length > 0) {
                let joined_errors = plando_errors.join("<br>");
                let error_html = `ERROR:<br>${joined_errors}`;
                // Show and populate the div for settings errors.
                settings_errors_element.innerHTML = error_html;
                settings_errors_element.style.display = "";
                return;
            }
        }
        apply_conversion();

        // Start the progress bar
        get_hash_images("browser", "loading-fairy")
        get_hash_images("browser", "loading-dead")
        // Append the gif_fairy to the bottom of the DOM, we just want to validate its working
        // If there isin't already an src set them
        //document.getElementById("progress-fairy").src = gif_fairy;
        //document.getElementById("progress-dead").src = gif_dead;


        $("#progressmodal").modal("show");
        $("#patchprogress").width(0);
        $("#progress-text").text("Initializing");

        if (!form_data["seed"]) {
            form_data["seed"] = Math.floor(Math.random() * 900000 + 100000).toString();
        }

        let branch, url;
        if (window.location.hostname === "dev.dk64randomizer.com" || window.location.hostname === "dk64randomizer.com") {
            branch = "dev";
            if (!window.location.hostname.toLowerCase().includes("dev")) {
                branch = "stable";
                url = "https://api.dk64rando.com/api";
            } else {
                url = "https://api.dk64rando.com/api";
                branch = "dev";
            }
        } else {
            url = `http://${window.location.hostname}:8000/api`;
            branch = "dev";
        }

        wipeToastHistory();
        postToastMessage("Initializing", false, 0);
        submit_seed_generation(url, JSON.stringify(form_data), branch);
    }
}

function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
      (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
    );
  }

async function import_settings_string(event) {
    // Click event for importing settings from a string.

    event.preventDefault();
    
    document.getElementById("settings_string").value = document.getElementById("settings_string").value.trim();
    const settingsString = document.getElementById("settings_string").value;
    const settings = decrypt_settings_string_enum(settingsString);
    // Remove enable_plandomizer from the settings object
    if (settings.hasOwnProperty("enable_plandomizer")) {
        delete settings["enable_plandomizer"];
    }

    // Clear all select boxes on the page except those in the nav-cosmetics div
    const selects = document.getElementsByTagName("select");
    for (let select of selects) {
        if (should_clear_setting(select)) {
            select.selectedIndex = -1;
        }
    }

    // Uncheck all starting move radio buttons to reset before importing settings
    const startingMoveButtons = Array.from(document.getElementsByTagName("input"))
        .filter(element => element.name.startsWith("starting_move_box_"));
    
    startingMoveButtons.forEach(button => button.checked = false);

    document.getElementById("presets").selectedIndex = 0;

    for (let key in settings) {
        try {
            if (typeof settings[key] === "boolean") {
                if (settings[key] === false) {
                    document.getElementsByName(key)[0].checked = false;
                } else {
                    document.getElementsByName(key)[0].checked = true;
                }
                document.getElementsByName(key)[0].removeAttribute("disabled");
            } else if (Array.isArray(settings[key])) {
                if (key.startsWith("starting_moves_list_")) {
                    select = document.getElementById(key);
                    settings[key].forEach(value => {
                        let existing_option = document.getElementById("starting_move_" + value);
                        const parentSelect = existing_option.parentNode;
                        parentSelect.removeChild(existing_option);
                        select.appendChild(existing_option);
                    });
                    continue;
                }

                const selector = document.getElementById(key);

                if (selector.tagName === "SELECT") {
                    let MapName = SettingsMap[key];
                    // Flip the attributes so the value is the key and the key is the value
                    let flipped = {};
                    for (let key in MapName) {
                        flipped[MapName[key]] = key;
                    }
                    // Pre clear all selections
                    for (let option of selector.options) {
                        option.selected = false;
                    }
                    settings[key].forEach(item => {
                        // Find the selected option by the value of the option
                        for (let option of selector.options) {
                            if (option.value === flipped[item]) {
                                option.selected = true;
                            }
                        }
                    });
                }
            } else {
                const selector = document.getElementById(key);
                if (selector.tagName === "SELECT" && key !== "random-weights") {
                    let MapName = SettingsMap[key];
                    // Flip the attributes so the value is the key and the key is the value
                    let flipped = {};
                    for (let key in MapName) {
                        flipped[MapName[key]] = key;
                    }
                    // Clear all selections
                    for (let option of selector.options) {
                        option.selected = false;
                    }
                    // Set the value of the select box to the value in the settings
                    selector.value = flipped[settings[key]];
                    // Set the selected attribute to true for the selected option we need to search by the name of the option
                    for (let option of selector.options) {
                        if (option.value === flipped[settings[key]]) {
                            option.selected = true;
                        }
                    }

                } else {
                    document.getElementById(key).value = settings[key];
                }
                document.getElementById(key).removeAttribute("disabled");
            }
        } catch (e) {
            console.log(e);
        }
    }

    update_ui_states(null);
    generateToast("Imported settings string.<br />All non-cosmetic settings have been overwritten.");
}

document.getElementById("import_settings").addEventListener("click", import_settings_string);

window["setup_pyodide"] = setup_pyodide;