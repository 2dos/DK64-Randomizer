/**
 * Function to randomize key HTML settings on the web page.
 */

function random_bool_setting(weight) {
    /** Generate a random value for a boolean setting. */
    return Math.random() <= weight;
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
        let randValue = Math.random();
        if (randValue <= weight) {
            settingList.push(option);
        }
    }
    return settingList;
}

function assign_multi_select_setting(setting_name, options_list) {
    /** Assign a list of values to a multi-select. */
    const selectElem = get_setting_element(setting_name);
    for (let i = 0; i < selectElem.options.length; i++) {
        const optElem = selectElem.options.item(i);
        optElem.selected = options_list.includes(optElem.value);
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

function is_bool_setting(setting_id) {
    const elem = get_setting_element(setting_id);
    if (!elem) {
        return false;
    }
    return elem.tagName === "INPUT" && elem.type === "checkbox";
}

function is_numeric_setting(setting_id) {
    const elem = get_setting_element(setting_id);
    if (!elem) {
        return false;
    }
    return elem.tagName === "INPUT" && elem.type === "number";
}

function is_single_select_setting(setting_id) {
    const elem = get_setting_element(setting_id);
    if (!elem) {
        return false;
    }
    return elem.tagName === "SELECT" && !elem.multiple;
}

function is_multi_select_setting(setting_id) {
    const elem = get_setting_element(setting_id);
    if (!elem) {
        return false;
    }
    return elem.tagName === "SELECT" && elem.multiple;
}

function randomize_settings() {
    /** Randomize all non-cosmetic settings. */
    const weightsElem = get_setting_element("random-weights");
    let weightData = undefined;
    for (const val of random_settings_presets) {
        if (val["name"] === weightsElem.value) {
            weightData = val;
        }
    }

    // If we somehow have no selection, just return.
    if (!weightData) {
        return;
    }

    const randSettings = {};
    const ignoredFields = [
        "name",
        "description",
    ];

    // Start by generating random values and placing them in the object.
    for (const [settingName, weights] of Object.entries(weightData)) {
        if (ignoredFields.includes(settingName)) {
            continue;
        }

        if (is_bool_setting(settingName)) {
            // Generate a random number and see if it's below the provided
            // weight.
            let randomValue = random_bool_setting(weights);
            randSettings[settingName] = randomValue;
        } else if (is_numeric_setting(settingName)) {
            // Generate a random number from a distribution based on the
            // provided values.
            let randomValue = random_numeric_setting(weights);
            randSettings[settingName] = randomValue;
        } else if (is_single_select_setting(settingName)) {
            // Generate a random number and see which bucket the number falls
            // into. That bucket's value is chosen.
            let randomValue = random_single_select_setting(weights);
            randSettings[settingName] = randomValue;
        } else if (is_multi_select_setting(settingName)) {
            // Generate a random number for every possible value and add that
            // value to the list if the number is's above the provided weight.
            let randomList = random_multi_select_setting(weights);
            randSettings[settingName] = randomList;
        }
    }

    // If logic isn't glitched logic, remove selected glitches.
    if (randSettings["logic_type"] !== "glitch") {
        randSettings["glitches_selected"] = [];
    }
    // Only enable individual hard mode settings if hard mode is enabled.
    if (!randSettings["hard_mode"]) {
        randSettings["hard_mode_selected"] = [];
    }
    // Remove all selected minigames if they aren't being randomized.
    if (!randSettings["bonus_barrel_rando"]) {
        randSettings["minigames_list_selected"] = [];
    }
    // Remove all selected levels if the CBs in them aren't being randomized.
    if (!randSettings["cb_rando_enabled"]) {
        randSettings["cb_rando_list_selected"] = [];
    }
    // Remove all selected enemies if they aren't being randomized.
    if (!randSettings["enemy_rando"]) {
        randSettings["enemies_selected"] = [];
    }
    // Ignore the warp level list if bananaports are not shuffled.
    if (randSettings["bananaport_placement_rando"] === "off") {
        randSettings["warp_level_list_selected"] = [];
    }

    // Reset all starting moves, placing them all into a single list.
    startingMovesFullReset();

    // Now we assign the random values to the HTML settings.
    for (const [settingName, settingVal] of Object.entries(randSettings)) {
        if (is_bool_setting(settingName)) {
            const settingElem = get_setting_element(settingName);
            settingElem.checked = settingVal;
        } else if (is_multi_select_setting(settingName)) {
            assign_multi_select_setting(settingName, settingVal);
        } else {
            // Both numeric and single-select settings work here.
            const settingElem = get_setting_element(settingName);
            settingElem.value = settingVal;
        }
    }
}
