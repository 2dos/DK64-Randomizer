// Helper functions
function timectime(ts) {
    /** Convert Unix time into human-readable time. */
    return new Date(ts * 1000).toLocaleString("en-GB", { timeZone: "UTC", hour12: false });
}

function hasListUnion(lst1, lst2) {
    /** Return whether there is an item that is present in both lists. */
    return lst1.some(item => lst2.includes(item));
}

function filterId(id_string) {
    /** Filter an id to remove illegal characters. */
    return id_string.toLowerCase().replace(/\s+/g, "_").replace(/[()&]/g, "");
}

function getWotHPathIndex(spoiler_dict) {
    /** Get the index of the WotH Path item in the spoiler dict, for usage in the id system. */
    let order = 1;
    for (const key in spoiler_dict) {
        if (key === "WotH Paths") {
            return order;
        }
        order += 1;
    }
    return null;
}

const TIED_POOL_ITEMS = {
    "Kongs": ["Kong"],
    "Moves": ["TrainingBarrel", "Shop", "PreGivenMove", "Shockwave"],
    "Golden Bananas": ["Banana", "ToughBanana", "BlueprintBanana"],
    "Blueprints": ["Blueprint"],
    "Fairies": ["Fairy"],
    "Keys": ["Key"],
    "Crowns": ["Crown"],
    "Company Coins": ["NintendoCoin", "RarewareCoin"],
    "Medals": ["Medal"],
    "Miscellaneous Items": ["Bean", "Pearl"],
    "Rainbow Coins": ["RainbowCoin"],
    "Junk Items": ["JunkItem"],
    "Melon Crates": ["CrateItem"],
    "Enemy Drops": ["Enemies"],
    "Shop Owners": ["Cranky", "Funky", "Candy", "Snide"],
    "Ice Traps": ["FakeItem"],
};

async function generateSpoiler(spoiler) {
    /** Pass spoiler to the template and modify DOM with rendered content. */
    //const templateEnv = new nunjucks.Environment();
    var env = nunjucks.configure('/templates', { autoescape: false });
    env.addFilter("timeconvert", timectime);
    env.addFilter("filterId", filterId);
    env.addFilter("wothpathindex", getWotHPathIndex);

    // Prepare spoiler data
    let trimmed_spoiler = spoiler.replace(/\n\s*/g, "");
    let formatted_spoiler = JSON.parse(trimmed_spoiler);
    // Clone formatted_spoiler to avoid modifying the original object
    let cloned_spoiler = JSON.parse(JSON.stringify(formatted_spoiler));

    // Spoiler hints data cleanup
    if (formatted_spoiler["Spoiler Hints Data"]) {
        delete formatted_spoiler["Spoiler Hints Data"];
    }

    // Move hints into the "Hints" section
    formatted_spoiler["Hints"] = {};
    ["Wrinkly Hints", "Direct Item Hints"].forEach(hint_attr => {
        if (formatted_spoiler[hint_attr]) {
            formatted_spoiler["Hints"][hint_attr] = formatted_spoiler[hint_attr];
            delete formatted_spoiler[hint_attr];
        }
    });

    if (formatted_spoiler["Hints"]?.["Wrinkly Hints"]?.["First Time Talk"]) {
        delete formatted_spoiler["Hints"]["Wrinkly Hints"]["First Time Talk"];
    }

    // Custom Locations Mapping
    formatted_spoiler["Misc Custom Locations"] = {};
    const location_mapping = {
        "Coin Locations": "Banana Coins",
        "Shuffled Banana Fairies": "Banana Fairies",
        "Shuffled Dirt Patches": "Dirt Patches",
        "Shuffled Melon Crates": "Melon Crates",
        "Battle Arena Locations": "Battle Arenas",
        "DK Portal Locations": "DK Portals"
    };
    for (const hint_attr in location_mapping) {
        if (formatted_spoiler[hint_attr]) {
            formatted_spoiler["Misc Custom Locations"][location_mapping[hint_attr]] = formatted_spoiler[hint_attr];
            delete formatted_spoiler[hint_attr];
        }
    }

    // Item Pool Cleanup
    if (formatted_spoiler["Item Pool"]) {
        let deleted_keys = [];
        for (const key in formatted_spoiler["Items (Sorted by Item)"]) {
            if (TIED_POOL_ITEMS[key] && !hasListUnion(TIED_POOL_ITEMS[key], formatted_spoiler["Item Pool"])) {
                deleted_keys.push(key);
            }
        }
        deleted_keys.forEach(key => delete formatted_spoiler["Items (Sorted by Item)"][key]);
    }

    // End Game Cleanup
    formatted_spoiler["Requirements"] = formatted_spoiler["Requirements"] || {};
    formatted_spoiler["Bosses"] = formatted_spoiler["Bosses"] || {};
    
    if (formatted_spoiler["End Game"]) {
        if (formatted_spoiler["End Game"]["K. Rool"]) {
            const kRoolData = formatted_spoiler["End Game"]["K. Rool"];
            if (kRoolData["K Rool Phases"]) {
                const order_names = ["First", "Second", "Third", "Fourth", "Fifth"]
                let order_data = {}
                kRoolData["K Rool Phases"].forEach((boss, index) => {
                    order_data[`${order_names[index]} Phase`] = boss;
                })
                formatted_spoiler["Bosses"]["The Final Battle"] = order_data;
                delete kRoolData["K Rool Phases"];
            }
            if (kRoolData["Keys Required for K Rool"]) {
                formatted_spoiler["Requirements"]["Keys Required for K. Rool"] = kRoolData["Keys Required for K Rool"];
                delete kRoolData["Keys Required for K Rool"];
            }
        }
        if (formatted_spoiler["End Game"]["Helm"]?.["Helm Rooms"]) {
            formatted_spoiler["Requirements"]["Helm Rooms"] = formatted_spoiler["End Game"]["Helm"]["Helm Rooms"];
            delete formatted_spoiler["End Game"]["Helm"]["Helm Rooms"];
        }
        delete formatted_spoiler["End Game"];
        delete formatted_spoiler["Randomizer Version"];
    }

    // Determine Loading Zone Randomization Type
    let lzr_type = "none";
    if (formatted_spoiler.Settings?.["Loading Zones Shuffled"] === "all") {
        lzr_type = formatted_spoiler.Settings?.["Decoupled Loading Zones"] ? "decoupled" : "coupled";
    }

    // Render template and update the DOM
    try {
        env.addFilter('isIterable', function(value) {
            // Check if value is not null and has the Symbol.iterator property
            const isIterable = value != null && typeof value[Symbol.iterator] === 'function';
            const isString = typeof value === 'string';
            const isMapping = value != null && typeof value === 'object' && !Array.isArray(value);
          
            return isIterable && !isString && !isMapping;
          });
        const rendered = await env.render("spoiler_new.html", { "spoiler": formatted_spoiler, "lzr_type": lzr_type });
        document.getElementById("spoiler_log_text").value = JSON.stringify(cloned_spoiler, null, 4);
        document.getElementById("spoiler_log_text").innerHTML = rendered;
    } catch (error) {
        console.error("Error rendering spoiler template:", error);
        console.error("Error details:", {
            message: error.message,
            stack: error.stack,
            name: error.name
        });
    }
}
window["GenerateSpoiler"] = generateSpoiler;
