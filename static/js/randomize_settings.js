/**
 * Function to randomize key HTML settings on the web page.
 */

function random_bool_setting(weight) {
    /** Generate a random value for a boolean setting. */
    return (Math.random() * 100) <= weight;
}

function get_random_normal_value(mean, sdev) {
    /** Return a random number using the Box-Muller transform algorithm. */
    let u1 = Math.random();
    let u2 = Math.random();
    while (u1 === 0) {
        u1 = Math.random();
    }
    while (u2 === 0) {
        u2 = Math.random();
    }
    const r = Math.sqrt(-2.0 * Math.log(u1));
    const theta = 2.0 * Math.PI * u2;
    const u0 = r * Math.cos(theta);
    return mean + (sdev * u0);
}

function random_numeric_setting(weights_obj) {
    /**
     * Generate a random value for a numeric setting.
     * 
     * If there is a provided mean, the resulting number will be biased toward
     * the mean, but can range all the way form the min to the max. If there is
     * no mean, the number will be pulled from a uniform distribution.
     */
    const min = weights_obj["min"];
    const max = weights_obj["max"];

    // If the min equals the max, return that number.
    if (min === max) {
        return min;
    }

    // If there is no mean, obtain a random number between the min and max,
    // evenly distributed.
    if (!Object.hasOwn(weights_obj, "mean")) {
        const range = max - min;
        const randNum = (Math.random() * range) + min;
        return Math.round(randNum);
    }

    const mean = weights_obj["mean"];

    // Determine the standard deviation. This will be 1/3 of the difference
    // between the mean and the min, or the mean and the max, whichever is
    // larger.
    const minDiff = mean - min;
    const maxDiff = max - mean;
    const minBased = minDiff >= maxDiff;
    const sdev = minBased ? (minDiff / 3.0) : (maxDiff / 3.0);
    // We need to determine the scale difference between the minDiff and the
    // maxDiff, since we will use that to adjust numbers outside the range.
    const oppositeScale = minBased ? (maxDiff / minDiff) : (minDiff / maxDiff);

    // Obtain a normally-distributed random number.
    let randNum = get_random_normal_value(mean, sdev);

    // If we're min-based and our number is larger than the mean, or if we're
    // max-based and our number is smaller than the mean, we need to adjust the
    // number so it fits into the different scale of the opposite side.
    if ((minBased && randNum > mean) || (!minBased && randNum < mean)) {
        randNum = ((randNum - mean) * oppositeScale) + mean;
    }

    // Trim the number so it falls within our bounds.
    if (randNum < min) {
        randNum = min;
    } else if (randNum > max) {
        randNum = max;
    }

    // Round to the nearest integer.
    return Math.round(randNum);
}

function random_single_select_setting(weights_obj) {
    /** Generate a randomly selected value for a single-select setting. */
    const totalWeight = Object.values(weights_obj).reduce((acc, val) => acc + val);
    // The random value is multiplied by the sum of all the weights, to ensure
    // an even distribution even if all the weights don't add up to 1.
    let randValue = Math.random() * totalWeight;
    for (const [option, weight] of Object.entries(weights_obj)) {
        // Subtract the current option's weight from the random value. If the
        // random number hits or crosses 0, choose that option.
        randValue -= weight;
        if (randValue <= 0) {
            return option;
        }
    }
    // This should never happen, but in case of weird rounding errors, choose
    // the last option.
    const options = Object.keys(weights_obj);
    return options[options.length - 1];
}

function random_multi_select_setting(weights_obj) {
    /** Generate a random list of values for a multi-select setting. */
    const settingList = [];
    for (const [option, weight] of Object.entries(weights_obj)) {
        let randValue = Math.random() * 100.0;
        if (randValue <= weight) {
            settingList.push(option);
        }
    }
    return settingList;
}

function assign_multi_select_setting(setting_name, options_list) {
    /** Assign a list of values to a multi-select. */
    const selectElem = get_setting_element(setting_name);
    if (selectElem.tagName == "SELECT") {
        // Regular Multi-select
        for (let i = 0; i < selectElem.options.length; i++) {
            const optElem = selectElem.options.item(i);
            optElem.selected = options_list.includes(optElem.value);
        }
    } else {
        // Dropdown Multiselect
        const checkboxes = Array.from(selectElem.getElementsByTagName("input"));
        for (let cb of checkboxes) {
            cb.checked = options_list.includes(cb.value);
        }
    }
}

function get_setting_element(id_or_name) {
    /** Return the setting with the given ID or name. */
    const idElem = document.getElementById(id_or_name);
    if (idElem !== null) {
        return idElem;
    }
    const nameElem = document.getElementsByName(id_or_name);
    if (nameElem.length >= 0) {
        return nameElem[0];
    }
    return undefined;
}

function setSortableToColumn(group_name, shuffled, unshuffled) {
    const container = document.getElementById(`${group_name}-category-container`);
    const sort_sections_items = sort_container.getElementsByClassName("shared");
    const sort_sections_checks = sort_container.getElementsByClassName("sharedchecks");
    const offset = sort_sections_items.length;
    let total_shuffled_html = "";
    let total_unshuffled_html = "";
    for (let i = 0; i < offset; i++) {
        const contents = sort_sections_items[i].getElementsByTagName("li");
        for (let c = 0; c < contents.length; c++) {
            const obj_val = contents[c].getAttribute("value");
            if (shuffled.includes(obj_val)) {
                total_shuffled_html += contents[c].outerHTML;
            } else {
                total_unshuffled_html += contents[c].outerHTML;
            }
        }
    }
    for (let i = 0; i < offset; i++) {
        if (i == 0) {
            sort_sections_items[0].innerHTML = total_unshuffled_html;
        } else if (i == 1) {
            sort_sections_items[1].innerHTML = total_shuffled_html;
        } else {
            sort_sections_items[i].innerHTML = "";
        }
        sort_sections_checks[i].innerHTML = "";
        const event = new Event("change", { bubbles: true, cancelable: false });
        sort_sections_items[i].dispatchEvent(event);
        sort_sections_checks[i].dispatchEvent(event);
    }
    updateCheckItemCounter(container);
}

function randomize_settings() {
    /** Randomize all non-cosmetic settings. */
    const weightsElem = get_setting_element("random-weights");
    let weightName = undefined;
    for (const val of random_settings_presets) {
        if (val.name === weightsElem.value) {
            weightName = val.name;
        }
    }

    // If we somehow have no selection, just return.
    if (!weightName) {
        return;
    }

    const randSettings = {};

    // Start by generating random values and placing them in the object.
    for (const [settingName, data] of Object.entries(random_settings_settings)) {
        console.log(`Reading weight file for ${settingName}`)
        if (data.ignored) {
            continue;
        }
        let parsed_weight_name = weightName;
        const no_qol = 'Difficult with QoL Shuffle';
        const no_qol_internal = no_qol.toLowerCase().replaceAll(" ", "_");
        if (weightName == no_qol && data.qol_uses_hard && !Object.keys(data.options).includes(no_qol_internal)) {
            parsed_weight_name = 'Difficult'
        }
        parsed_weight_name = parsed_weight_name.toLowerCase().replaceAll(" ", "_");

        if (data.setting_type == "bool") {
            // Generate a random number and see if it's below the provided
            // weight.
            let randomValue = random_bool_setting(data.options[parsed_weight_name]);
            randSettings[settingName] = {
                value: randomValue,
                type: "bool"
            };
        } else if (data.setting_type == "range") {
            // Generate a random number from a distribution based on the
            // provided values.
            let randomValue = random_numeric_setting(data.options[parsed_weight_name]);
            randSettings[settingName] = {
                value: randomValue,
                type: "range"
            };
        } else if (data.setting_type == "choice_single") {
            // Generate a random number and see which bucket the number falls
            // into. That bucket's value is chosen.
            let randomValue = random_single_select_setting(data.options[parsed_weight_name]);
            randSettings[settingName] = {
                value: randomValue,
                type: "choice_single"
            };
        } else if (data.setting_type == "choice_multiple") {
            // Generate a random number for every possible value and add that
            // value to the list if the number is's above the provided weight.
            let randomList = random_multi_select_setting(data.options[parsed_weight_name]);
            randSettings[settingName] = {
                value: randomList,
                type: "choice_multiple"
            };
        } else if (data.setting_type == "item_rando") {
            // Special case
            let unshuffled = [];
            let shuffled = [];
            Object.keys(data.options[parsed_weight_name]).forEach(item => {
                let isShuffled = random_bool_setting(data.options[parsed_weight_name][item]);
                if (isShuffled) {
                    shuffled.push(item);
                } else {
                    unshuffled.push(item);
                }
            });
            randSettings["item_rando_list_0"] = {
                value: unshuffled.slice(),
                type: "item_rando",
            };
            randSettings["item_rando_list_1"] = {
                value: shuffled.slice(),
                type: "item_rando",
            };
            for (let i = 0; i < 8; i++) {
                randSettings[`item_rando_list_${i + 2}`] = {
                    value: [],
                    type: "item_rando",
                };
            }
        }
    }
    // Progressive Moves count should be based on the item
    const prog_move_items = {
        "off": 0,
        "req_gb": 201,
        "req_bp": 40,
        "req_key": 8,
        "req_medal": 40,
        "req_crown": 10,
        "req_fairy": 20,
        "req_rainbowcoin": 16,
        "req_pearl": 5,
        "req_cb": 3500,
    }
    const cap = prog_move_items[randSettings["progressive_hint_item"].value]
    randSettings["progressive_hint_count"].value = parseInt((randSettings["progressive_hint_count"].value / 201) * cap);
    // Parse Chaos B. Lockers
    if (randSettings["blocker_selection_behavior"].value == "chaos") {
        // Is going to be a chaos B. Locker
        randSettings["blocker_text"].value = parseInt((randSettings["blocker_text"].value / 201) * 100);
    }
    console.log(randSettings)
    if (randSettings["no_healing"].value) {
        // Disable water is lava if no healing is selected
        randSettings["hard_mode_selected"].value = randSettings["hard_mode_selected"].value.filter(k => k != 'water_is_lava');
    }

    // Reset all starting moves, placing them all into a single list.
    startingMovesFullReset();

    // Now we assign the random values to the HTML settings.
    for (const [settingName, setting_data] of Object.entries(randSettings)) {
        console.log(`Writing to UI for ${settingName}`)
        const settingVal = setting_data.value;
        const settingType = setting_data.type;
        if (settingType == "bool") {
            const settingElem = get_setting_element(settingName);
            settingElem.checked = settingVal;
        } else if (settingType == "choice_multiple") {
            assign_multi_select_setting(settingName, settingVal);
        } else if (settingType != "item_rando") {
            // Both numeric and single-select settings work here.
            const settingElem = get_setting_element(settingName);
            settingElem.value = settingVal;
        }
    }
    setSortableToColumn("item_rando", randSettings["item_rando_list_1"].value, randSettings["item_rando_list_0"].value)
}
