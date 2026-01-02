let plando_data = {};
let plando_item_options = null;
async function loadPlandomizerData() {
  try {
    const response = await fetch('static/presets/plandomizer/data.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    console.error('Failed to fetch JSON:', err);
    return null;
  }
}

const exclusion_rules = {
    "plando_kong_rescue_tiny": ["donkey", "lanky", "tiny"],
}

function addOptions(obj, element_id) {
    let text = "";
    for (const [key, value] of Object.entries(obj)) {
        // Any exclusion rules
        if (Object.keys(exclusion_rules).includes(element_id)) {
            if (exclusion_rules[element_id].includes(key)) {
                continue;
            }
        }
        text += `<option value="${key}">${value}</option>`
    }
    return text;
}

async function initializePlandomizer() {
    plando_data = await loadPlandomizerData();
    console.log(plando_data)
    Object.keys(plando_data).forEach(obj_key => {
        const is_grouped = plando_data.grouped.includes(obj_key);
        const selects = document.getElementsByClassName(`plando-load-${obj_key}`);
        for (let s = 0; s < selects.length; s++) {
            let text = "";
            const element_id = selects[s].getAttribute("id");
            if (selects[s].classList.contains("plando-inc-randomize")) {
                text += "<option value=''>-- Randomize --</option>"
            }
            if (is_grouped) {
                Object.keys(plando_data[obj_key]).forEach(group => {
                    text += `<optgroup label="${group}">`
                    text += addOptions(plando_data[obj_key][group], element_id);
                    text += "</optgroup>"
                })
            } else {
                text += addOptions(plando_data[obj_key], element_id);
            }
            selects[s].innerHTML = text;
        }
    })
}

function deleteRow(e) {
    const targ = e.target.closest("tr");
    targ.remove();
}

function addLocationUI(location_name, location_id, item = null) {
    const hook = document.getElementById("plando_location_container");
    document.getElementById("plando_location_table").removeAttribute("hidden");
    document.getElementById("plando_reset_location").removeAttribute("hidden");
    hook.insertAdjacentHTML("beforeend", `<tr>
        <td>${location_name}</td>
        <td>
            <select id="plando_${location_id}_item" name="plando_${location_id}_item" class="form-select"></select>
        </td>
        <td>
            <button class="btn btn-danger" id="plando_itemdel_${location_id}" type="button">
                <i class="fa-solid fa-trash"></i>
            </button>
        </td>
    </tr>`);
    document.getElementById(`plando_itemdel_${location_id}`).addEventListener("click", deleteRow);
    if (plando_item_options === null) {
        plando_item_options = "";
        for (const [key, value] of Object.entries(plando_data["item_list"])) {
            // Any exclusion rules
            let sel_text = "";
            if (item !== null) {
                if (key === item) {
                    sel_text = "selected"
                }
            }
            plando_item_options += `<option value="${key}" ${sel_text}>${value}</option>`
        }
    }
    document.getElementById(`plando_${location_id}_item`).innerHTML = plando_item_options;
}

function addLocation() {
    const sel = document.getElementById("plando_location_adder");
    const sel_option = sel.selectedOptions[0];
    const internal_name = sel_option.value;
    if (internal_name == "") {
        return;
    }
    const pretty_name = sel_option.text;
    addLocationUI(pretty_name, internal_name);
    sel_option.disabled = true;
    sel_option.hidden = true;
    const firstValidOption = Array.from(sel.options).find(
        option => !option.disabled && !option.hidden
    );

    if (firstValidOption) {
        sel.value = firstValidOption.value;
    }
}

function resetLocations() {
    document.getElementById("plando_location_container").innerHTML = "";
    const options = document.querySelectorAll("#plando_location_adder option[hidden]");
    for (let option of options) {
        option.removeAttribute("hidden");
        option.removeAttribute("disabled");
    }
}

document.getElementById("plando_add_location").addEventListener("click", addLocation);
document.getElementById("plando_reset_location").addEventListener("click", resetLocations);

initializePlandomizer()