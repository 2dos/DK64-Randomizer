/**
 * Includes utility functions for plandomizer support.
 */


// This map allows us to efficiently sort the shop locations. Shops are sorted
// first by level, then by vendor, then by Kong. This sorting is easier to
// visually browse, as a user.
var shopLocationOrderingMap = new Map([
    ["simian_slam", 1],  // DK Isles Cranky Shared
    ["donkey_isles_potion", 2],  // DK Isles Cranky Donkey
    ["diddy_isles_potion", 3],  // DK Isles Cranky Diddy
    ["lanky_isles_potion", 4],  // DK Isles Cranky Lanky
    ["tiny_isles_potion", 5],  // DK Isles Cranky Tiny
    ["chunky_isles_potion", 6],  // DK Isles Cranky Chunky
    ["shared_japes_potion", 7],  // Japes Cranky Shared
    ["baboon_blast", 8],  // Japes Cranky Donkey
    ["chimpy_charge", 9],  // Japes Cranky Diddy
    ["orangstand", 10],  // Japes Cranky Lanky
    ["mini_monkey", 11],  // Japes Cranky Tiny
    ["hunky_chunky", 12],  // Japes Cranky Chunky
    ["shared_japes_gun", 13],  // Japes Funky Shared
    ["coconut_gun", 14],  // Japes Funky Donkey
    ["peanut_gun", 15],  // Japes Funky Diddy
    ["grape_gun", 16],  // Japes Funky Lanky
    ["feather_gun", 17],  // Japes Funky Tiny
    ["pineapple_gun", 18],  // Japes Funky Chunky
    ["shared_aztec_potion", 19],  // Aztec Cranky Shared
    ["strong_kong", 20],  // Aztec Cranky Donkey
    ["rocketbarrel_boost", 21],  // Aztec Cranky Diddy
    ["lanky_aztec_potion", 22],  // Aztec Cranky Lanky
    ["tiny_aztec_potion", 23],  // Aztec Cranky Tiny
    ["chunky_aztec_potion", 24],  // Aztec Cranky Chunky
    ["shared_aztec_gun", 25],  // Aztec Funky Shared
    ["donkey_aztec_gun", 26],  // Aztec Funky Donkey
    ["diddy_aztec_gun", 27],  // Aztec Funky Diddy
    ["lanky_aztec_gun", 28],  // Aztec Funky Lanky
    ["tiny_aztec_gun", 29],  // Aztec Funky Tiny
    ["chunky_aztec_gun", 30],  // Aztec Funky Chunky
    ["shared_aztec_instrument", 31],  // Aztec Candy Shared
    ["bongos", 32],  // Aztec Candy Donkey
    ["guitar", 33],  // Aztec Candy Diddy
    ["trombone", 34],  // Aztec Candy Lanky
    ["saxophone", 35],  // Aztec Candy Tiny
    ["triangle", 36],  // Aztec Candy Chunky
    ["shared_factory_potion", 37],  // Factory Cranky Shared
    ["gorilla_grab", 38],  // Factory Cranky Donkey
    ["simian_spring", 39],  // Factory Cranky Diddy
    ["baboon_balloon", 40],  // Factory Cranky Lanky
    ["pony_tail_twirl", 41],  // Factory Cranky Tiny
    ["primate_punch", 42],  // Factory Cranky Chunky
    ["ammo_belt_1", 43],  // Factory Funky Shared
    ["donkey_factory_gun", 44],  // Factory Funky Donkey
    ["diddy_factory_gun", 45],  // Factory Funky Diddy
    ["lanky_factory_gun", 46],  // Factory Funky Lanky
    ["tiny_factory_gun", 47],  // Factory Funky Tiny
    ["chunky_factory_gun", 48],  // Factory Funky Chunky
    ["shared_factory_instrument", 49],  // Factory Candy Shared
    ["donkey_factory_instrument", 50],  // Factory Candy Donkey
    ["diddy_factory_instrument", 51],  // Factory Candy Diddy
    ["lanky_factory_instrument", 52],  // Factory Candy Lanky
    ["tiny_factory_instrument", 53],  // Factory Candy Tiny
    ["chunky_factory_instrument", 54],  // Factory Candy Chunky
    ["shared_galleon_potion", 55],  // Galleon Cranky Shared
    ["donkey_galleon_potion", 56],  // Galleon Cranky Donkey
    ["diddy_galleon_potion", 57],  // Galleon Cranky Diddy
    ["lanky_galleon_potion", 58],  // Galleon Cranky Lanky
    ["tiny_galleon_potion", 59],  // Galleon Cranky Tiny
    ["chunky_galleon_potion", 60],  // Galleon Cranky Chunky
    ["shared_galleon_gun", 61],  // Galleon Funky Shared
    ["donkey_galleon_gun", 62],  // Galleon Funky Donkey
    ["diddy_galleon_gun", 63],  // Galleon Funky Diddy
    ["lanky_galleon_gun", 64],  // Galleon Funky Lanky
    ["tiny_galleon_gun", 65],  // Galleon Funky Tiny
    ["chunky_galleon_gun", 66],  // Galleon Funky Chunky
    ["music_upgrade_1", 67],  // Galleon Candy Shared
    ["donkey_galleon_instrument", 68],  // Galleon Candy Donkey
    ["diddy_galleon_instrument", 69],  // Galleon Candy Diddy
    ["lanky_galleon_instrument", 70],  // Galleon Candy Lanky
    ["tiny_galleon_instrument", 71],  // Galleon Candy Tiny
    ["chunky_galleon_instrument", 72],  // Galleon Candy Chunky
    ["super_simian_slam", 73],  // Forest Cranky Shared
    ["donkey_forest_potion", 74],  // Forest Cranky Donkey
    ["diddy_forest_potion", 75],  // Forest Cranky Diddy
    ["lanky_forest_potion", 76],  // Forest Cranky Lanky
    ["tiny_forest_potion", 77],  // Forest Cranky Tiny
    ["chunky_forest_potion", 78],  // Forest Cranky Chunky
    ["homing_ammo", 79],  // Forest Funky Shared
    ["donkey_forest_gun", 80],  // Forest Funky Donkey
    ["diddy_forest_gun", 81],  // Forest Funky Diddy
    ["lanky_forest_gun", 82],  // Forest Funky Lanky
    ["tiny_forest_gun", 83],  // Forest Funky Tiny
    ["chunky_forest_gun", 84],  // Forest Funky Chunky
    ["shared_caves_potion", 85],  // Caves Cranky Shared
    ["donkey_caves_potion", 86],  // Caves Cranky Donkey
    ["diddy_caves_potion", 87],  // Caves Cranky Diddy
    ["orangstand_sprint", 88],  // Caves Cranky Lanky
    ["monkeyport", 89],  // Caves Cranky Tiny
    ["gorilla_gone", 90],  // Caves Cranky Chunky
    ["ammo-belt_2", 91],  // Caves Funky Shared
    ["donkey_caves_gun", 92],  // Caves Funky Donkey
    ["diddy_caves_gun", 93],  // Caves Funky Diddy
    ["lanky_caves_gun", 94],  // Caves Funky Lanky
    ["tiny_caves_gun", 95],  // Caves Funky Tiny
    ["chunky_caves_gun", 96],  // Caves Funky Chunky
    ["third_melon", 97],  // Caves Candy Shared
    ["donkey_caves_instrument", 98],  // Caves Canky Donkey
    ["diddy_caves_instrument", 99],  // Caves Candy Diddy
    ["lanky_caves_instrument", 100],  // Caves Candy Lanky
    ["tiny_caves_instrument", 101],  // Caves Candy Tiny
    ["chunky_caves_instrument", 102],  // Caves Candy Chunky
    ["super_duper_simian_slam", 103],  // Castle Cranky Shared
    ["donkey_castle_potion", 104],  // Castle Cranky Donkey
    ["diddy_castle_potion", 105],  // Castle Cranky Diddy
    ["lanky_castle_potion", 106],  // Castle Cranky Lanky
    ["tiny_castle_potion", 107],  // Castle Cranky Tiny
    ["chunky_castle_potion", 108],  // Castle Cranky Chunky
    ["sniper_sight", 109],  // Castle Funky Shared
    ["donkey_castle_gun", 110],  // Castle Funky Donkey
    ["diddy_castle_gun", 111],  // Castle Funky Diddy
    ["lanky_castle_gun", 112],  // Castle Funky Lanky
    ["tiny_castle_gun", 113],  // Castle Funky Tiny
    ["chunky_castle_gun", 114],  // Castle Funky Chunky
    ["music_upgrade_2", 115],  // Castle Candy Shared
    ["donkey_castle_instrument", 116],  // Castle Candy Donkey
    ["diddy_castle_instrument", 117],  // Castle Candy Diddy
    ["lanky_castle_instrument", 118],  // Castle Candy Lanky
    ["tiny_castle_instrument", 119],  // Castle Candy Tiny
    ["chunky_castle_instrument", 120],  // Castle Candy Chunky
    ["rareware_coin", 121],  // Jetpac
]);
// A dictionary indicating which mini-games are unavailable to certain Kongs.
var kongMinigameRestrictions = new Map([
    ["Donkey", new Set([
        "diddy_rocketbarrel",
        "tiny_pony_tail_twirl",
        "chunky_hidden_kremling",
    ])],
    ["Diddy", new Set([
        "speedy_swing_sortie_normal",
        "donkey_target",
        "tiny_pony_tail_twirl",
        "chunky_hidden_kremling",
    ])],
    ["Lanky", new Set([
        "busy_barrel_barrage_easy",
        "busy_barrel_barrage_normal",
        "busy_barrel_barrage_hard",
        "speedy_swing_sortie_normal",
        "donkey_target",
        "tiny_pony_tail_twirl",
        "chunky_hidden_kremling",
    ])],
    ["Tiny", new Set([
        "donkey_target",
        "chunky_hidden_kremling",
    ])],
    ["Chunky", new Set([
        "speedy_swing_sortie_normal",
        "donkey_target",
        "tiny_pony_tail_twirl",
    ])],
]);




// Some common item sets that may be used in multiple places.
var KongSet = new Set([
    "donkey",
    "diddy",
    "lanky",
    "tiny",
    "chunky",
]);
var KeySet = new Set([
    "jungle_japes_key",
    "angry_aztec_key",
    "frantic_factory_key",
    "gloomy_galleon_key",
    "fungi_forest_key",
    "crystal_caves_key",
    "creepy_castle_key",
    "hideout_helm_key",
]);
var MoveSet = new Set([
    "vines",
    "swim",
    "oranges",
    "barrels",
    "climbing",
    "progressive_slam",
    "baboon_blast",
    "strong_kong",
    "gorilla_grab",
    "chimpy_charge",
    "rocketbarrel_boost",
    "simian_spring",
    "orangstand",
    "baboon_balloon",
    "orangstand_sprint",
    "mini_monkey",
    "pony_tail_twirl",
    "monkeyport",
    "hunky_chunky",
    "primate_punch",
    "gorilla_gone",
    "coconut",
    "peanut",
    "grape",
    "feather",
    "pineapple",
    "homing_ammo",
    "sniper_sight",
    "progressive_ammo_belt",
    "bongos",
    "guitar",
    "trombone",
    "saxophone",
    "triangle",
    "progressive_instrument_upgrade",
    "camera",
    "shockwave",
]);
var BlueprintItemSet = new Set([
    "donkey_blueprint",
    "diddy_blueprint",
    "lanky_blueprint",
    "tiny_blueprint",
    "chunky_blueprint",
]);

// Banana fairy locations have a handful of limitations.
var BananaFairyRestrictedItems = new Set([
    "camera",
    "nintendo_coin",
    "rareware_coin",
    "banana_medal",
    "bean",
    "pearl",
    "rainbow_coin",
    "junk_item",
    "donkey_blueprint",
    "diddy_blueprint",
    "lanky_blueprint",
    "tiny_blueprint",
    "chunky_blueprint",
]);


// A map of custom locations, mapped to a set of new locations that are invalid
// assignments. This will be used to filter the dropdowns used in the
// plandomizer.
var LocationRestrictionsPerCustomLocation = new Map([
    ["isles_battle_arena_1", new Set(["Fungi Lobby: Gorilla Gone Box"])],
    ["isles_battle_arena_2", new Set(["Snide's Room: Under Rock"])],
]);


/**
 * Return a filtered list of plando locations that are permitted for the given
 * custom location.
 * @param {obj[]} locationList 
 * @param {str} locationId 
 * @returns 
 */
function PlandoCustomLocationFilter(locationList, locationId) {
    var locationName = locationId.match(/^plando_(.+)_location$/g)[0];
    if (!LocationRestrictionsPerCustomLocation.has(locationName)) {
        return locationList;
    }
    return locationList.filter((loc) => !LocationRestrictionsPerCustomLocation.get(locationName).has(loc["value"]));
}


// A map of custom location types, mapped to a set of which items may not
// appear in that location type. This will be used to filter the dropdowns used
// in the plandomizer.
var CrownItemSet = new Set(BlueprintItemSet);
CrownItemSet.add("junk_item");
var ItemRestrictionsPerLocationType = new Map([
    ["crownpad", CrownItemSet],
    ["dirtpatch", BlueprintItemSet],
    ["fairy", BananaFairyRestrictedItems],
    ["kasplat", new Set()],
    ["meloncrate", new Set(["junk_item"])],
]);


/**
 * Return a filtered list of plando items that are permitted for the given
 * location type.
 * @param {*} itemList 
 * @param {str} locType 
 * @returns The filtered list.
 */
function PlandoCustomLocationItemFilter(itemList, locType) {
    // lower the case of the locType
    locType = locType.toLowerCase();
    return itemList.filter((item) => !ItemRestrictionsPerLocationType.get(locType).has(item["value"]));
}



/**
 * Return a filtered list of minigames that can be played by each Kong.
 * @param {*} minigameList 
 * @param {str} kong 
 * @returns The filtered list.
 */
function PlandoMinigameFilter(minigameList, kong) {
    if (kong == "All Kongs") {
        return minigameList;
    }
    return minigameList.filter((game) => !kongMinigameRestrictions.get(kong).has(game["value"]));
}


/**
 * Return a sorted list of shop locations. These are sorted by level, then by
 * vendor, then by Kong. This makes the full list easier to browse.
 * @param {string[]} shopLocationList 
 * @returns 
 */
function PlandoShopSortFilter(shopLocationList) {
    return shopLocationList.sort((a, b) => shopLocationOrderingMap.get(a) - shopLocationOrderingMap.get(b));
}


/**
 * Apply certain CSS classes to dropdown menu options.
 * 
 * This allows for the frontend to quickly enable or disable options if they
 * conflict with the existing settings.
 * @param {str} panel 
 * @param {str} kong 
 * @param {str} location 
 * @param {str} item 
 * @returns 
 */
function PlandoOptionClassAnnotation(panel, kong, location, item) {
    var classSet = new Set()

    // Each key gets its own class.
    if (KeySet.has(item)) {
        classSet.add(`plando-${item}-option`);
    }

    // Each Kong gets their own class.
    if (KongSet.has(item)) {
        classSet.add(`plando-${item}-option`);
    }

    // Each move gets its own class.
    if (MoveSet.has(item)) {
        classSet.add(`plando-${item}-option`);
    }

    // Camera and Shockwave get their own class.
    if (item === "camera" || item === "shockwave") {
        classSet.add("plando-camera-shockwave-option");
    }

    if (classSet.size > 0) {
        return `class=\"${Array.from(classSet).join(" ")}\"`;
    } else {
        return "";
    }
}

// Set all the functions to window scope.
window.PlandoCustomLocationFilter = PlandoCustomLocationFilter;
window.PlandoCustomLocationItemFilter = PlandoCustomLocationItemFilter;
window.PlandoMinigameFilter = PlandoMinigameFilter;
window.PlandoShopSortFilter = PlandoShopSortFilter;
window.PlandoOptionClassAnnotation = PlandoOptionClassAnnotation;
window.MoveSet = MoveSet;
