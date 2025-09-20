function toggle_logic_type(event) {
  /** Toggle settings based on the presence of logic. */

  // Get the glitch customization modal element
  let glitchCustomization = document.getElementById("glitches_modal");
  let glitchList = document.getElementById("glitches_multiselector");

  // Check the value of the logic_type element and enable or disable the glitches modal
  if (["advanced_glitchless", "glitch"].includes(document.getElementById("logic_type").value)) {
    glitchCustomization.removeAttribute("disabled");
  } else {
    glitchCustomization.setAttribute("disabled", "disabled");
  }
  if (document.getElementById("logic_type").value === "glitch") {
    glitchList.removeAttribute("hidden");
  } else {
    glitchList.setAttribute("hidden", "hidden");
  }
}

const DISABLED_HELM_DOOR_VALUES = [
  "easy_random",
  "medium_random",
  "hard_random",
  "opened",
];

const ITEM_CAPS = {
  "req_gb": 201,
  "req_bp": 40,
  "req_key": 8,
  "req_medal": 40,
  "req_crown": 10,
  "req_fairy": 20,
  "req_bean": 1,
  "req_pearl": 5,
  "req_rainbowcoin": 16,
  "req_bosses": 7,
  "req_bonuses": 53,
  "req_cb": 3500,
  "req_companycoins": 2,
}

// Attach the function as an event listener to the "change" event on the "logic_type" element
document
  .getElementById("logic_type")
  .addEventListener("change", toggle_logic_type);

// Toggle the hint color table
document
  .getElementById("plando_toggle_color_table")
  .addEventListener("click", function (evt) {
    const hintColorTable = document.getElementById("plando_hint_color_table");
    hintColorTable.classList.toggle("hidden");
  });

// Toggle the Custom Locations tab
function plando_toggle_custom_locations_tab() {
  const tabElem = document.getElementById("nav-plando-Locations-tab");
  const arenasEnabled = document.getElementById("plando_place_arenas").checked;
  const patchesEnabled = document.getElementById(
    "plando_place_patches"
  ).checked;
  const fairiesEnabled = document.getElementById(
    "plando_place_fairies"
  ).checked;
  const kasplatsEnabled = document.getElementById(
    "plando_place_kasplats"
  ).checked;
  const cratesEnabled = document.getElementById("plando_place_crates").checked;
  const wrinklyEnabled = document.getElementById(
    "plando_place_wrinkly"
  ).checked;
  const tnsEnabled = document.getElementById("plando_place_tns").checked;

  if (
    arenasEnabled ||
    patchesEnabled ||
    fairiesEnabled ||
    kasplatsEnabled ||
    cratesEnabled ||
    wrinklyEnabled ||
    tnsEnabled
  ) {
    tabElem.style.display = "";
  } else {
    tabElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_arenas")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_patches")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_fairies")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_kasplats")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_crates")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_wrinkly")
  .addEventListener("click", plando_toggle_custom_locations_tab);
document
  .getElementById("plando_place_tns")
  .addEventListener("click", plando_toggle_custom_locations_tab);

// Toggle custom arena locations
function plando_toggle_custom_arena_locations() {
  const arenaElem = document.getElementById(
    "plando_custom_location_panel_arena"
  );
  if (document.getElementById("plando_place_arenas").checked) {
    arenaElem.style.display = "";
  } else {
    arenaElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_arenas")
  .addEventListener("click", plando_toggle_custom_arena_locations);

// Toggle custom patch locations
function plando_toggle_custom_patch_locations() {
  const patchElem = document.getElementById(
    "plando_custom_location_panel_patch"
  );
  if (document.getElementById("plando_place_patches").checked) {
    patchElem.style.display = "";
  } else {
    patchElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_patches")
  .addEventListener("click", plando_toggle_custom_patch_locations);

// Toggle custom fairy locations
function plando_toggle_custom_fairy_locations() {
  const fairyElem = document.getElementById(
    "plando_custom_location_panel_fairy"
  );
  if (document.getElementById("plando_place_fairies").checked) {
    fairyElem.style.display = "";
  } else {
    fairyElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_fairies")
  .addEventListener("click", plando_toggle_custom_fairy_locations);

// Toggle custom Kasplat locations
function plando_toggle_custom_kasplat_locations() {
  const kasplatElem = document.getElementById(
    "plando_custom_location_panel_kasplat"
  );
  if (document.getElementById("plando_place_kasplats").checked) {
    kasplatElem.style.display = "";
  } else {
    kasplatElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_kasplats")
  .addEventListener("click", plando_toggle_custom_kasplat_locations);

// Toggle custom crate locations
function plando_toggle_custom_crate_locations() {
  const crateElem = document.getElementById(
    "plando_custom_location_panel_crate"
  );
  if (document.getElementById("plando_place_crates").checked) {
    crateElem.style.display = "";
  } else {
    crateElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_crates")
  .addEventListener("click", plando_toggle_custom_crate_locations);

// Toggle custom Wrinkly locations
function plando_toggle_custom_wrinkly_locations() {
  const wrinklyElem = document.getElementById(
    "plando_custom_location_panel_wrinkly_door"
  );
  if (document.getElementById("plando_place_wrinkly").checked) {
    wrinklyElem.style.display = "";
  } else {
    wrinklyElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_wrinkly")
  .addEventListener("click", plando_toggle_custom_wrinkly_locations);

// Toggle custom TnS portal locations
function plando_toggle_custom_tns_locations() {
  const tnsElem = document.getElementById(
    "plando_custom_location_panel_tns_portal"
  );
  if (document.getElementById("plando_place_tns").checked) {
    tnsElem.style.display = "";
  } else {
    tnsElem.style.display = "none";
  }
}

document
  .getElementById("plando_place_tns")
  .addEventListener("click", plando_toggle_custom_tns_locations);

// Enable or disable custom locations for battle arenas
function plando_disable_arena_custom_locations() {
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  let crownsShuffled = false;

  for (let option of itemRandoPool) {
    if (option.value === "crown") {
      crownsShuffled = option.selected;
    }
  }

  const randomCrowns = document.getElementById("crown_placement_rando").checked;
  const customCrownsElem = document.getElementById("plando_place_arenas");
  let tooltip = "Allows the user to specify locations for each battle arena.";

  if (crownsShuffled && randomCrowns) {
    customCrownsElem.removeAttribute("disabled");
  } else {
    customCrownsElem.setAttribute("disabled", "disabled");
    customCrownsElem.checked = false;
    tooltip =
      "To use this feature, battle crowns must be in the item pool, and their locations must be shuffled.";
  }

  customCrownsElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("crown_placement_rando")
  .addEventListener("click", plando_disable_arena_custom_locations);

// Enable or disable custom locations for melon crates
function plando_disable_crate_custom_locations() {
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  let cratesShuffled = false;

  for (let option of itemRandoPool) {
    if (option.value === "crateitem") {
      cratesShuffled = option.selected;
    }
  }

  const randomCrates = document.getElementById("random_crates").checked;
  const customCratesElem = document.getElementById("plando_place_crates");
  let tooltip = "Allows the user to specify locations for each melon crate.";

  if (cratesShuffled && randomCrates) {
    customCratesElem.removeAttribute("disabled");
  } else {
    customCratesElem.setAttribute("disabled", "disabled");
    customCratesElem.checked = false;
    tooltip =
      "To use this feature, melon crates must be in the item pool, and their locations must be shuffled.";
  }

  customCratesElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("random_crates")
  .addEventListener("click", plando_disable_crate_custom_locations);

function plando_disable_fairy_custom_locations() {
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  let fairiesShuffled = false;

  for (let option of itemRandoPool) {
    if (option.value === "fairy") {
      fairiesShuffled = option.selected;
    }
  }

  const randomFairies = document.getElementById("random_fairies").checked;
  const customFairiesElem = document.getElementById("plando_place_fairies");
  let tooltip = "Allows the user to specify locations for each banana fairy.";

  if (fairiesShuffled && randomFairies) {
    customFairiesElem.removeAttribute("disabled");
  } else {
    customFairiesElem.setAttribute("disabled", "disabled");
    customFairiesElem.checked = false;
    tooltip =
      "To use this feature, fairies must be in the item pool, and their locations must be shuffled.";
  }

  customFairiesElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("random_fairies")
  .addEventListener("click", plando_disable_fairy_custom_locations);

// Enable or disable custom locations for Kasplats
function plando_disable_kasplat_custom_locations() {
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  let kasplatsShuffled = false;

  for (let option of itemRandoPool) {
    if (option.value === "blueprint") {
      kasplatsShuffled = option.selected;
    }
  }

  const kasplatShuffle = document.getElementById("kasplat_rando_setting").value;
  const customKasplatsElem = document.getElementById("plando_place_kasplats");
  let tooltip = "Allows the user to specify locations for each Kasplat.";

  if (kasplatsShuffled && kasplatShuffle === "location_shuffle") {
    customKasplatsElem.removeAttribute("disabled");
  } else {
    customKasplatsElem.setAttribute("disabled", "disabled");
    customKasplatsElem.checked = false;
    tooltip =
      "To use this feature, blueprints must be in the item pool, and Kasplat locations must be shuffled.";
  }

  customKasplatsElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("kasplat_rando_setting")
  .addEventListener("change", plando_disable_kasplat_custom_locations);

// Enable or disable custom locations for Wrinkly doors
function plando_disable_wrinkly_custom_locations() {
  const randomDoors = document.getElementById("wrinkly_location_rando").checked;
  const progressiveHints = document.getElementById(
    "progressive_hint_item"
  ).value != "off";
  const customWrinklyElem = document.getElementById("plando_place_wrinkly");
  let tooltip = "Allows the user to specify locations for each Wrinkly door.";

  if (randomDoors && !progressiveHints) {
    customWrinklyElem.removeAttribute("disabled");
  } else {
    customWrinklyElem.setAttribute("disabled", "disabled");
    customWrinklyElem.checked = false;
    tooltip =
      "To use this feature, Wrinkly door locations must be shuffled, and progressive hints must be turned off.";
  }

  customWrinklyElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("wrinkly_location_rando")
  .addEventListener("click", plando_disable_wrinkly_custom_locations);
document
  .getElementById("progressive_hint_item")
  .addEventListener("change", plando_disable_wrinkly_custom_locations);


// Enable or disable custom locations for Troff 'n' Scoff portals
function plando_disable_tns_custom_locations() {
  const randomPortals = document.getElementById("tns_location_rando").checked;
  const customTnsElem = document.getElementById("plando_place_tns");
  let tooltip =
    "Allows the user to specify locations for each Troff 'n' Scoff portal.";

  if (randomPortals) {
    customTnsElem.removeAttribute("disabled");
  } else {
    customTnsElem.setAttribute("disabled", "disabled");
    customTnsElem.checked = false;
    tooltip =
      "To use this feature, Troff 'n' Scoff portal locations must be shuffled.";
  }

  customTnsElem.parentElement.setAttribute("data-bs-original-title", tooltip);
}

document
  .getElementById("tns_location_rando")
  .addEventListener("click", plando_disable_tns_custom_locations);

// Disable Helm Hurry Selector when Helm Hurry is off
function disable_helm_hurry() {
  const selector = document.getElementById("helmhurry_list_modal");
  const disabled = !document.getElementById("helm_hurry").checked;

  if (disabled) {
    selector.setAttribute("disabled", "disabled");
  } else {
    selector.removeAttribute("disabled");
  }
}

document
  .getElementById("helm_hurry")
  .addEventListener("click", disable_helm_hurry);

// Disable Points Selector when Spoiler Hints are not set to Points
function disable_points() {
  const selector = document.getElementById("points_list_modal");
  const disabled = document.getElementById("spoiler_hints").value !== "points";

  if (disabled) {
    selector.setAttribute("disabled", "disabled");
  } else {
    selector.removeAttribute("disabled");
  }
}

document
  .getElementById("spoiler_hints")
  .addEventListener("change", disable_points);

// Disable Prog Slam Selector when Prog Slam is off
function disable_slam_selector() {
  const selector = document.getElementById("slamModalActivator");
  const disabled = !document.getElementById("alter_switch_allocation").checked;

  if (disabled) {
    selector.setAttribute("disabled", "disabled");
  } else {
    selector.removeAttribute("disabled");
  }
}
document
.getElementById("alter_switch_allocation")
.addEventListener("click", disable_slam_selector);

// Force Vanilla Door Rando on and enforce DK Portal Rando is enabled
function toggle_dos_door_rando() {
  const dosDoorRando  = document.getElementById("dos_door_rando");
  const vanillaDoorShuffle = document.getElementById("vanilla_door_rando");

  if (dosDoorRando.checked) {
    vanillaDoorShuffle.checked = true;
    vanillaDoorShuffle.setAttribute("disabled", "disabled");
    toggle_vanilla_door_rando();
  } else {
    vanillaDoorShuffle.removeAttribute("disabled");
  }
}

document
  .getElementById("dos_door_rando")
  .addEventListener("click", toggle_dos_door_rando);

// Force Wrinkly and T&S Rando to be on when Vanilla Door Rando is on
function toggle_vanilla_door_rando() {
  const vanillaDoorShuffle = document.getElementById("vanilla_door_rando");
  const wrinklyRando = document.getElementById("wrinkly_location_rando");
  const tnsRando = document.getElementById("tns_location_rando");

  if (vanillaDoorShuffle.checked) {
    wrinklyRando.checked = true;
    wrinklyRando.setAttribute("disabled", "disabled");
    tnsRando.checked = true;
    tnsRando.setAttribute("disabled", "disabled");
  } else {
    wrinklyRando.removeAttribute("disabled");
    tnsRando.removeAttribute("disabled");
  }
}

document
  .getElementById("vanilla_door_rando")
  .addEventListener("click", toggle_vanilla_door_rando);

// Toggle bananaport settings if shuffling is enabled
function toggle_bananaport_selector() {
  const bananaportCustomization = document.getElementById(
    "warp_level_list_modal"
  );

  if (document.getElementById("bananaport_placement_rando").value !== "off") {
    bananaportCustomization.removeAttribute("disabled");
  } else {
    bananaportCustomization.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("bananaport_placement_rando")
  .addEventListener("change", toggle_bananaport_selector);

// Disable non-cosmetic tabs if using patch file
document
  .getElementById("nav-patch-tab")
  .addEventListener("click", function (event) {
    const tabs = [
      "nav-started-tab",
      "nav-item-tab",
      "nav-requirements-tab",
      "nav-overworld-tab",
      "nav-progression-tab",
      "nav-qol-tab",
    ];
    tabs.forEach((tab) =>
      document.getElementById(tab).setAttribute("disabled", "disabled")
    );
    document.getElementById("override_div").removeAttribute("hidden");
    document.getElementById("nav-cosmetics-tab").click();
  });

// Re-enable non-cosmetic tabs and hide override option when generating a new seed
document
  .getElementById("nav-seed-gen-tab")
  .addEventListener("click", function (event) {
    const tabs = [
      "nav-started-tab",
      "nav-item-tab",
      "nav-requirements-tab",
      "nav-overworld-tab",
      "nav-progression-tab",
      "nav-qol-tab",
    ];
    tabs.forEach((tab) =>
      document.getElementById(tab).removeAttribute("disabled")
    );
    document.getElementById("override_div").setAttribute("hidden", "hidden");
    document.getElementById("override_cosmetics").checked = true;
  });

// Hide the override cosmetics setting when clicking the Generate from Past Seed button
document
  .getElementById("nav-pastgen-tab")
  .addEventListener("click", function (event) {
    document.getElementById("override_div").setAttribute("hidden", "hidden");
    document.getElementById("override_cosmetics").checked = true;
  });

// Change between "Default" and "Randomizer" for BGM Music
document
  .getElementById("music_bgm_randomized")
  .addEventListener("change", function (evt) {
    const toggleElem = document.getElementById("music_bgm_randomized");
    const selects = document.getElementsByClassName("BGM-select");

    for (let select of selects) {
      if (toggleElem.checked && select.value === "default_value") {
        select.value = "";
      } else if (!toggleElem.checked && select.value === "") {
        select.value = "default_value";
      }
    }
    //savemusicsettings();
  });

// Change between "Default" and "Randomize" for major item music selection
document
  .getElementById("music_majoritems_randomized")
  .addEventListener("change", function (evt) {
    const toggleElem = document.getElementById("music_majoritems_randomized");
    const selects = document.getElementsByClassName("MajorItem-select");

    for (let select of selects) {
      if (toggleElem.checked && select.value === "default_value") {
        select.value = "";
      } else if (!toggleElem.checked && select.value === "") {
        select.value = "default_value";
      }
    }
    //savemusicsettings();
  });

// Change between "Default" and "Randomize" for minor item music selection
document
  .getElementById("music_minoritems_randomized")
  .addEventListener("change", function (evt) {
    const toggleElem = document.getElementById("music_minoritems_randomized");
    const selects = document.getElementsByClassName("MinorItem-select");

    for (let select of selects) {
      if (toggleElem.checked && select.value === "default_value") {
        select.value = "";
      } else if (!toggleElem.checked && select.value === "") {
        select.value = "default_value";
      }
    }
    //savemusicsettings();
  });

// Change between "Default" and "Randomize" for event music selection
document
  .getElementById("music_events_randomized")
  .addEventListener("change", function (evt) {
    const toggleElem = document.getElementById("music_events_randomized");
    const selects = document.getElementsByClassName("Event-select");

    for (let select of selects) {
      if (toggleElem.checked && select.value === "default_value") {
        select.value = "";
      } else if (!toggleElem.checked && select.value === "") {
        select.value = "default_value";
      }
    }
    //savemusicsettings();
  });

function toggle_key_settings() {
  const disabled = document.getElementById("select_keys").checked;
  const selector = document.getElementById("starting_keys_list_modal");

  if (disabled) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("select_keys")
  .addEventListener("click", toggle_key_settings);

enabled_plando = false;
// Enable and disable the Plandomizer tab
async function enable_plandomizer() {
  const plandoTab = document.getElementById("nav-plando-tab");
  if (document.getElementById("enable_plandomizer").checked) {
    // Open up a Modal stating that we're loading the Plando tab
    if (!enabled_plando){
      $("#plando-modal").modal("show");    
      try {
        await setup_pyodide();
      } catch (error) {
        console.log("Error setting up Pyodide:", error);
      }
      try{
        // Load ui.__init__.py
        await run_python_file("ui/__init__.py");
        enabled_plando = true;
      }
      catch (error) {
        console.log("Error running ui/__init__.py:", error);
      }
    }
    plandoTab.removeAttribute("hidden");
    $("#plando-modal").modal("hide");
  } else {
    plandoTab.setAttribute("hidden", "hidden");
    $("#plando-modal").modal("hide");
  }
}

document
  .getElementById("enable_plandomizer")
  .addEventListener("click", enable_plandomizer);

// Disable SSanity Selector when Switchsanity is off
function disable_switchsanity_modal() {
  const selector = document.getElementById("switchModalActivator");
  if (document.getElementById("switchsanity_enabled").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("switchsanity_enabled")
  .addEventListener("click", disable_switchsanity_modal);

// Switchsanity Resets
const switchsanity_defaults = {
  "switchsanity_switch_isles_to_kroc_top": "tiny",
  "switchsanity_switch_isles_helm_lobby": "gone_pad",
  "switchsanity_switch_isles_aztec_lobby_back_room": "tiny",
  "switchsanity_switch_isles_fungi_lobby_fairy": "tiny",
  "switchsanity_switch_isles_spawn_rocketbarrel": "lanky",
  "switchsanity_switch_japes_to_hive": "tiny",
  "switchsanity_switch_japes_to_rambi": "donkey",
  "switchsanity_switch_japes_to_painting_room": "diddy",
  "switchsanity_switch_japes_to_cavern": "diddy",
  "switchsanity_switch_aztec_to_kasplat_room": "donkey",
  "switchsanity_switch_aztec_llama_front": "donkey",
  "switchsanity_switch_aztec_llama_side": "lanky",
  "switchsanity_switch_aztec_llama_back": "tiny",
  "switchsanity_switch_aztec_sand_tunnel": "donkey",
  "switchsanity_switch_aztec_to_connector_tunnel": "diddy",
  "switchsanity_switch_galleon_to_lighthouse_side": "donkey",
  "switchsanity_switch_galleon_to_shipwreck_side": "diddy",
  "switchsanity_switch_galleon_to_cannon_game": "chunky",
  "switchsanity_switch_fungi_yellow_tunnel": "lanky",
  "switchsanity_switch_fungi_green_tunnel_near": "tiny",
  "switchsanity_switch_fungi_green_tunnel_far": "chunky",
  "switchsanity_switch_japes_free_kong": "donkey",
  "switchsanity_switch_aztec_free_tiny": "diddy",
  "switchsanity_switch_aztec_free_lanky": "donkey",
}
function switchsanity_reset_default() {
  Object.keys(switchsanity_defaults).forEach(key => {
    document.getElementById(key).value = switchsanity_defaults[key];
  })
}

function switchsanity_reset_random() {
  Object.keys(switchsanity_defaults).forEach(key => {
    document.getElementById(key).value = "random";
  })
}

document
  .getElementById("ssanity-reset-vanilla")
  .addEventListener("click", switchsanity_reset_default);
document
  .getElementById("ssanity-reset-random")
  .addEventListener("click", switchsanity_reset_random);

document.getElementById("starting_moves_reset").addEventListener("click", function(evt) {
  // Update the starting move pools to start with no items
  for (let i = 1; i <= 5; i++) {
    const move_selector = document.getElementById("starting_moves_list_count_" + i);
    move_selector.value = 0;
  }
  startingMovesFullReset();
});

document.getElementById("starting_moves_start_vanilla").addEventListener("click", function(evt) {
  // Update the starting move pools to start with vanilla items
  for (let i = 1; i <= 5; i++) {
    const move_selector = document.getElementById("starting_moves_list_count_" + i);
    move_selector.value = i == 2 ? 10 : 0;
  }
  startingMovesFullReset();

  document.getElementById("starting_move_92").selected = true;  // Cranky
  document.getElementById("starting_move_93").selected = true;  // Funky
  document.getElementById("starting_move_94").selected = true;  // Candy
  document.getElementById("starting_move_95").selected = true; // Snide
  document.getElementById("starting_move_8").selected = true; // Vines
  document.getElementById("starting_move_9").selected = true; // Diving
  document.getElementById("starting_move_10").selected = true; // Oranges
  document.getElementById("starting_move_11").selected = true; // Barrels
  document.getElementById("starting_move_12").selected = true; // Climbing
  document.getElementById("starting_move_13").selected = true; // Simian Slam
  moveSelectedStartingMoves(2);
});

document.getElementById("starting_moves_start_all").addEventListener("click", function(evt) {
  // Update the starting move pools to start with all items
  for (let i = 1; i <= 5; i++) {
    const move_selector = document.getElementById("starting_moves_list_count_" + i);
    move_selector.value = i == 1 ? 60 : 0;
  }
  startingMovesFullReset();
});
function disable_custom_cb_locations_modal() {
  const selector = document.getElementById("cb_rando_list_modal");
  if (document.getElementById("cb_rando_enabled").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("cb_rando_enabled")
  .addEventListener("click", disable_custom_cb_locations_modal);

// Hide the plando options for certain Helm phases if they are disabled
function plando_hide_helm_options(evt) {
  const helmPhaseCount = parseInt(
    document.getElementById("helm_phase_count").value
  );
  const helmRandom = document.getElementById("helm_random").checked;
  for (let i = 0; i < 5; i++) {
    const helmPhasePlandoDiv = document.getElementById(
      `plando_helm_order_div_${i}`
    );
    const helmPhasePlando = document.getElementById(`plando_helm_order_${i}`);
    if (i < helmPhaseCount || helmRandom) {
      helmPhasePlandoDiv.classList.remove("disabled-select");
      helmPhasePlando.removeAttribute("disabled");
    } else {
      helmPhasePlandoDiv.classList.add("disabled-select");
      helmPhasePlando.setAttribute("disabled", "disabled");
      helmPhasePlando.value = "";
    }
  }
}

document
  .getElementById("helm_random")
  .addEventListener("click", plando_hide_helm_options);
document
  .getElementById("helm_phase_count")
  .addEventListener("change", plando_hide_helm_options);

// Hide the plando options for certain K. Rool phases if they are disabled
function plando_hide_krool_options(evt) {
  const kroolPhaseCount = parseInt(
    document.getElementById("krool_phase_count").value
  );
  const kroolRandom = document.getElementById("krool_random").checked;
  for (let i = 0; i < 5; i++) {
    const kroolPhasePlandoDiv = document.getElementById(
      `plando_krool_order_div_${i}`
    );
    const kroolPhasePlando = document.getElementById(`plando_krool_order_${i}`);
    if (i < kroolPhaseCount || kroolRandom) {
      kroolPhasePlandoDiv.classList.remove("disabled-select");
      kroolPhasePlando.removeAttribute("disabled");
    } else {
      kroolPhasePlandoDiv.classList.add("disabled-select");
      kroolPhasePlando.setAttribute("disabled", "disabled");
      kroolPhasePlando.value = "";
    }
  }
}

document
  .getElementById("krool_random")
  .addEventListener("click", plando_hide_krool_options);
document
  .getElementById("krool_phase_count")
  .addEventListener("change", plando_hide_krool_options);

// Hide plando options for Isles medal locations if medal CBs aren't shuffled
function plando_disable_isles_medals(evt) {
  const cbShuffle = document.getElementById("cb_rando_enabled").value;
  const kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"];

  if (cbShuffle !== "on_with_isles") {
    for (const kong of kongs) {
      const kongIsleElem = document.getElementById(`plando_Isles${kong}Medal_item`);
      kongIsleElem.setAttribute("disabled", "disabled");
      kongIsleElem.value = "";
      const tooltip = "To assign a reward here, Isles CBs must be shuffled.";
      kongIsleElem.parentElement.setAttribute("data-bs-original-title", tooltip);
    }
  } else {
    for (const kong of kongs) {
      const kongIsleElem = document.getElementById(`plando_Isles${kong}Medal_item`);
      kongIsleElem.removeAttribute("disabled");
      kongIsleElem.parentElement.setAttribute("data-bs-original-title", "");
    }
  }
}

document.getElementById("cb_rando_enabled").addEventListener("change", plando_disable_isles_medals);

// Disable K. Rool phases as bosses if they are not in the boss pool.
function plando_disable_krool_phases_as_bosses(evt) {
  const kroolInBossPool = document.getElementById("krool_in_boss_pool").checked;
  const tnsBossOptions = document.getElementsByClassName("plando-tns-boss");

  if (kroolInBossPool) {
    for (let option of tnsBossOptions) {
      option.removeAttribute("disabled");
    }
  } else {
    for (let option of tnsBossOptions) {
      option.setAttribute("disabled", "disabled");
    }
    for (let i = 0; i < 5; i++) {
      const kroolPhase = document.getElementById(`plando_krool_order_${i}`);
      if (kroolPhase.value.includes("Boss")) {
        kroolPhase.value = "";
      }
    }
  }
}

document.getElementById("krool_in_boss_pool").addEventListener("click", plando_disable_krool_phases_as_bosses);

// Make changes to the plando tab based on other settings
document
  .getElementById("nav-plando-tab")
  .addEventListener("click", function (evt) {
    disable_krool_phases();
    disable_helm_phases();
    plando_toggle_custom_locations_tab(evt);
    plando_toggle_custom_arena_locations(evt);
    plando_toggle_custom_patch_locations(evt);
    plando_toggle_custom_fairy_locations(evt);
    plando_toggle_custom_kasplat_locations(evt);
    plando_toggle_custom_crate_locations(evt);
    plando_toggle_custom_wrinkly_locations(evt);
    plando_toggle_custom_tns_locations(evt);
    plando_disable_arena_custom_locations(evt);
    plando_disable_crate_custom_locations(evt);
    plando_disable_fairy_custom_locations(evt);
    plando_disable_kasplat_custom_locations(evt);
    plando_disable_wrinkly_custom_locations(evt);
    plando_disable_tns_custom_locations(evt);
    plando_disable_isles_medals(evt);
    plando_disable_krool_phases_as_bosses(evt);
});

// Randomize all non-cosmetic settings.
document.getElementById("randomize_settings").addEventListener("click", function (evt) {
  generateToast(`Randomizing settings (${document.getElementById('random-weights').value}).<br>All non-cosmetic settings have been overwritten.`);

  randomize_settings();

  // Run additional functions to ensure there are no conflicts.
  update_ui_states();
});

// Disable color options when Randomize All is selected
function disable_colors() {
  const disabled = document.getElementById("random_kong_colors").checked;
  const KONG_ZONES = {
    DK: ["Fur", "Tie"],
    Diddy: ["Clothes"],
    Lanky: ["Clothes", "Fur"],
    Tiny: ["Clothes", "Hair"],
    Chunky: ["Main", "Other"],
    Rambi: ["Skin"],
    Enguarde: ["Skin"],
  };

  for (const kong in KONG_ZONES) {
    KONG_ZONES[kong].forEach((zone) => {
      const color = document.getElementById(
        `${kong.toLowerCase()}_${zone.toLowerCase()}_colors`
      );
      const picker = document.getElementById(
        `${kong.toLowerCase()}_${zone.toLowerCase()}_custom_color`
      );
      if (disabled) {
        color.setAttribute("disabled", "disabled");
        picker.setAttribute("disabled", "disabled");
      } else {
        try {
          color.removeAttribute("disabled");
          picker.removeAttribute("disabled");
        } catch {}
      }
    });
  }
}

document
  .getElementById("random_kong_colors")
  .addEventListener("click", disable_colors);

// Disable 'Disable Tag Spawn' option when 'Tag Anywhere' is off
function disable_tag_spawn() {
  const tagBarrels = document.getElementById("disable_tag_barrels");
  if (!document.getElementById("enable_tag_anywhere").checked) {
    tagBarrels.setAttribute("disabled", "disabled");
    tagBarrels.checked = false;
  } else {
    tagBarrels.removeAttribute("disabled");
  }
}

document
  .getElementById("enable_tag_anywhere")
  .addEventListener("click", disable_tag_spawn);

// Enable 'Tag Anywhere' if 'Disable Tag Spawn' option is on
document
  .getElementById("disable_tag_barrels")
  .addEventListener("click", function (evt) {
    if (document.getElementById("disable_tag_barrels").checked) {
      document.getElementById("enable_tag_anywhere").checked = true;
    }
  });

// Disable music options when Randomize All is selected
function disable_music() {
  const disabled = document.getElementById("random_music").checked;
  const musicOptions = ["bgm", "majoritems", "minoritems", "events"];

  musicOptions.forEach((option) => {
    const musicElem = document.getElementById(`music_${option}_randomized`);
    if (disabled) {
      musicElem.setAttribute("disabled", "disabled");
      musicElem.setAttribute("checked", "checked");
    } else {
      musicElem.removeAttribute("disabled");
    }
  });
}

document
  .getElementById("random_music")
  .addEventListener("click", disable_music);

// Disable K Rool options when Randomize All is selected
function disable_krool_phases() {
  const krool = document.getElementById("krool_phase_count");
  if (document.getElementById("krool_random").checked) {
    krool.setAttribute("disabled", "disabled");
  } else {
    krool.removeAttribute("disabled");
  }
}

document
  .getElementById("krool_random")
  .addEventListener("click", disable_krool_phases);

// Disable Helm options when Randomize All is selected
function disable_helm_phases() {
  const helm = document.getElementById("helm_phase_count");
  if (document.getElementById("helm_random").checked) {
    helm.setAttribute("disabled", "disabled");
  } else {
    helm.removeAttribute("disabled");
  }
}

document
  .getElementById("helm_random")
  .addEventListener("click", disable_helm_phases);

function refreshItemRandoSortable() {
  updateCheckItemCounter(document.getElementById("item_rando-category-container"));
}

document.getElementById("smaller_shops").addEventListener("click", refreshItemRandoSortable);
document.querySelector("#cb_rando_list_selected option[value='DKIsles']").addEventListener("click", refreshItemRandoSortable);
document.getElementById("cb_rando_enabled").addEventListener("click", refreshItemRandoSortable);

// Enable and disable settings based on the Item Rando pool changing
function item_rando_list_changed(evt) {
  let itemRandoDisabled = true;
  // const itemRandoPool = document.getElementById(
  //   "item_rando_list_selected"
  // ).options;
  const smallerShops = document.getElementById("smaller_shops");
  const moveVanilla = document.getElementById("move_off");
  const moveRando = document.getElementById("move_on");
  const sharedShopWarning = document.getElementById("shared_shop_warning");
  let shopsInPool = false;
  let kongsInPool = false;
  let shockwaveInPool = false;
  let shopownersInPool = false;
  let nothingSelected = true;

  // for (let option of itemRandoPool) {
  //   if (option.value === "shop" && option.selected) shopsInPool = true;
  //   if (option.value === "kong" && option.selected) kongsInPool = true;
  //   if (option.value === "shockwave" && option.selected) shockwaveInPool = true;
  //   if (option.value === "shopowners" && option.selected) shopownersInPool = true;
  //   if (option.selected) nothingSelected = false;
  // }

  // if (nothingSelected) {
    shopsInPool = true;
    kongsInPool = true;
    shockwaveInPool = true;
    shopownersInPool = true;
  // }

  let camera_option = document.getElementById("starting_move_52");
  let shockwave_option = document.getElementById("starting_move_53");
  let cranky_option = document.getElementById("starting_move_92");
  let funky_option = document.getElementById("starting_move_93");
  let candy_option = document.getElementById("starting_move_94");
  let snide_option = document.getElementById("starting_move_95");

  if (shopsInPool) {
    sharedShopWarning.setAttribute("hidden", "hidden");
    // if (moveVanilla.selected || moveRando.selected) {
    //   document.getElementById("move_on_cross_purchase").selected = true;
    // }
    // moveVanilla.setAttribute("disabled", "disabled");
    // moveRando.setAttribute("disabled", "disabled");
    smallerShops.removeAttribute("disabled");

    
    if (!shockwaveInPool) {
      camera_option.setAttribute("hidden", "hidden");
      shockwave_option.setAttribute("hidden", "hidden");
    }
    else {
      camera_option.removeAttribute("hidden");
      shockwave_option.removeAttribute("hidden");
    }
    if (!shopownersInPool) {
      cranky_option.setAttribute("hidden", "hidden");
      funky_option.setAttribute("hidden", "hidden");
      candy_option.setAttribute("hidden", "hidden");
      snide_option.setAttribute("hidden", "hidden");
    }
    else {
      cranky_option.removeAttribute("hidden");
      funky_option.removeAttribute("hidden");
      candy_option.removeAttribute("hidden");
      snide_option.removeAttribute("hidden");
    }

  } else {
    sharedShopWarning.removeAttribute("hidden");
    // moveVanilla.removeAttribute("disabled");
    // moveRando.removeAttribute("disabled");
    smallerShops.setAttribute("disabled", "disabled");
    smallerShops.checked = false;
  }
}

// Validate Fast Start Status
document
  .getElementById("random_starting_region")
  .addEventListener("click", validate_fast_start_status);

function validate_fast_start_status(evt) {
  const loadingZoneStatus = document.getElementById("level_randomization");
  const isRandomStartingRegion = document.getElementById(
    "random_starting_region"
  ).checked;
  const fastStart = document.getElementById("fast_start_beginning_of_game_dummy");

  if (
    isRandomStartingRegion ||
    ["loadingzone", "loadingzonesdecoupled"].includes(loadingZoneStatus.value)
  ) {
    fastStart.setAttribute("disabled", "disabled");
    fastStart.checked = true;
  } else {
    fastStart.removeAttribute("disabled");
  }
}

// Change level randomization
document
  .getElementById("level_randomization")
  .addEventListener("change", change_level_randomization);

function change_level_randomization(evt) {
  validate_fast_start_status(evt);

  const level = document.getElementById("level_randomization");
  const shuffleHelmLocation = document.getElementById("shuffle_helm_location");
  const helmLabel = document.getElementById("shuffle_helm_location_label");

  const isLevelOrder = ["level_order", "level_order_complex", "level_order_moderate"].includes(level.value);
  const disableShuffleHelmLocation = level.value === "vanilla";

  if (disableShuffleHelmLocation) {
      shuffleHelmLocation.setAttribute("disabled", "disabled");
      shuffleHelmLocation.checked = false;
  } else {
      shuffleHelmLocation.removeAttribute("disabled");
      helmLabel.innerText = isLevelOrder ? "Include Helm" : "Shuffle Helm Location";
  }
}

// Randomly generate a seed ID
function randomSeed(evt) {
  document.getElementById("seed").value =
    Math.floor(Math.random() * (999999 - 100000 + 1)) + 100000;
}

// Limit inputs for textboxes
function onInput(event) {
  const targetId = event.target.id;

  if (["blocker_text", "troff_text"].includes(targetId)) return;

  if (targetId.includes("troff")) {
    minMax(event, 0, 500);
  } else if (targetId.includes("blocker")) {
    minMax(event, 0, 200);
  }
}
// Adding event listeners for input event on blocker_ and troff_ fields, as well as blocker_text and troff_text
document
  .querySelectorAll("[id^=blocker_], [id^=troff_], #blocker_text, #troff_text")
  .forEach((element) => {
    element.addEventListener("input", onInput);
  });


// Update Win Condition Number Access
function update_prog_hint_num_access() {
  const DISABLED_PROG_VALUES = [
    "off",
  ];

  const progHintSelection = document.getElementById("progressive_hint_item");
  const progHintContainer = document.getElementById("progressive_hint_container");
  const progHintReq = document.getElementById("progressive_hint_count");
  const disabled = DISABLED_PROG_VALUES.includes(progHintSelection.value);

  if (disabled) {
    progHintContainer.classList.add("hide-input");
  } else {
    progHintContainer.classList.remove("hide-input");
  }

  if (!progHintReq.value) {
    progHintReq.value = 1;
  } else {
    const item_type = progHintSelection.value;
    if (Object.keys(ITEM_CAPS).includes(item_type)) {
      if (parseInt(progHintReq.value) > ITEM_CAPS[item_type]) {
        progHintReq.value = ITEM_CAPS[item_type];
      }
    }
  }
}

document
  .getElementById("progressive_hint_item")
  .addEventListener("change", update_prog_hint_num_access);

// Validate blocker input on loss of focus
function max_randomized_blocker() {
  const blockerText = document.getElementById("blocker_text");
  if (!blockerText.value) {
    blockerText.value = 50;
  } else if (parseInt(blockerText.value) < 0) {
    blockerText.value = 0;
  } else if (parseInt(blockerText.value) > 200) {
    blockerText.value = 200;
  }
}

document
  .getElementById("blocker_text")
  .addEventListener("focusout", max_randomized_blocker);

// Validate troff input on loss of focus
function max_randomized_troff() {
  const troffText = document.getElementById("troff_text");
  if (!troffText.value) {
    troffText.value = 300;
  } else if (parseInt(troffText.value) > 500) {
    troffText.value = 500;
  }
}

document
  .getElementById("troff_text")
  .addEventListener("focusout", max_randomized_troff);

// Validate music volume input on loss of focus
function max_music() {
  const musicText = document.getElementById("music_volume");
  if (!musicText.value) {
    musicText.value = 100;
  } else if (parseInt(musicText.value) > 100) {
    musicText.value = 100;
  } else if (parseInt(musicText.value) < 0) {
    musicText.value = 0;
  }
}

document.getElementById("music_volume").addEventListener("focusout", max_music);

// Validate custom music proportion input on loss of focus
function max_music_proportion() {
  const musicText = document.getElementById("custom_music_proportion");
  if (!musicText.value) {
    musicText.value = 100;
  } else if (parseInt(musicText.value) > 100) {
    musicText.value = 100;
  } else if (parseInt(musicText.value) < 0) {
    musicText.value = 0;
  }
}

document
  .getElementById("custom_music_proportion")
  .addEventListener("focusout", max_music_proportion);

// Validate sfx volume input on loss of focus
function max_sfx() {
  const sfxText = document.getElementById("sfx_volume");
  if (!sfxText.value) {
    sfxText.value = 100;
  } else if (parseInt(sfxText.value) > 100) {
    sfxText.value = 100;
  } else if (parseInt(sfxText.value) < 0) {
    sfxText.value = 0;
  }
}

document.getElementById("sfx_volume").addEventListener("focusout", max_sfx);

// Validate medal requirement input on loss of focus
document
  .getElementById("medal_requirement")
  .addEventListener("focusout", function (event) {
    const medalRequirement = document.getElementById("medal_requirement");
    if (!medalRequirement.value) {
      medalRequirement.value = 15;
    } else if (parseInt(medalRequirement.value) < 0) {
      medalRequirement.value = 0;
    } else if (parseInt(medalRequirement.value) > 40) {
      medalRequirement.value = 40;
    }
  });

// Validate cb medal requirement input on loss of focus
document
  .getElementById("medal_cb_req")
  .addEventListener("focusout", function (event) {
    const medalCbReq = document.getElementById("medal_cb_req");
    if (!medalCbReq.value) {
      medalCbReq.value = 75;
    } else if (parseInt(medalCbReq.value) < 1) {
      medalCbReq.value = 1;
    } else if (parseInt(medalCbReq.value) > 100) {
      medalCbReq.value = 100;
    }
  });

// Validate fairies input on loss of focus
document
  .getElementById("rareware_gb_fairies")
  .addEventListener("focusout", function (event) {
    const fairyReq = document.getElementById("rareware_gb_fairies");
    if (!fairyReq.value) {
      fairyReq.value = 20;
    } else if (parseInt(fairyReq.value) < 1) {
      fairyReq.value = 1;
    } else if (parseInt(fairyReq.value) > 20) {
      fairyReq.value = 20;
    }
  });

// Validate pearls input on loss of focus
document
  .getElementById("mermaid_gb_pearls")
  .addEventListener("focusout", function (event) {
    const pearlReq = document.getElementById("mermaid_gb_pearls");
    if (!pearlReq.value) {
      pearlReq.value = 5;
    } else if (parseInt(pearlReq.value) < 0) {
      pearlReq.value = 0;
    } else if (parseInt(pearlReq.value) > 5) {
      pearlReq.value = 5;
    }
  });

// Update Door 1 Number Access
function update_door_one_num_access() {
  const doorOneSelection = document.getElementById("crown_door_item");
  const doorOneContainer = document.getElementById("door_1_container");
  const doorOneReq = document.getElementById("crown_door_item_count");
  const disabled = DISABLED_HELM_DOOR_VALUES.includes(doorOneSelection.value);

  if (disabled) {
    doorOneContainer.classList.add("hide-input");
  } else {
    doorOneContainer.classList.remove("hide-input");
  }

  if (!doorOneReq.value) {
    doorOneReq.value = 1;
  } else {
    const item_type = doorOneSelection.value == "vanilla" ? "req_crown" : doorOneSelection.value;
    if (Object.keys(ITEM_CAPS).includes(item_type)) {
      if (parseInt(doorOneReq.value) > ITEM_CAPS[item_type]) {
        doorOneReq.value = ITEM_CAPS[item_type];
      }
    }
  }
}

document
  .getElementById("crown_door_item")
  .addEventListener("change", update_door_one_num_access);

// Update Door 2 Number Access
function update_door_two_num_access() {
  const doorTwoSelection = document.getElementById("coin_door_item");
  const doorTwoContainer = document.getElementById("door_2_container");
  const doorTwoReq = document.getElementById("coin_door_item_count");
  const disabled = DISABLED_HELM_DOOR_VALUES.includes(doorTwoSelection.value);

  if (disabled) {
    doorTwoContainer.classList.add("hide-input");
  } else {
    doorTwoContainer.classList.remove("hide-input");
  }

  if (!doorTwoReq.value) {
    doorTwoReq.value = 1;
  } else {
    const item_type = doorTwoSelection.value == "vanilla" ? "req_companycoins" : doorTwoSelection.value;
    if (Object.keys(ITEM_CAPS).includes(item_type)) {
      if (parseInt(doorTwoReq.value) > ITEM_CAPS[item_type]) {
        doorTwoReq.value = ITEM_CAPS[item_type];
      }
    }
  }
}

document
  .getElementById("coin_door_item")
  .addEventListener("change", update_door_two_num_access);

// Update Win Condition Number Access
function update_win_con_num_access() {
  const DISABLED_WIN_VALUES = [
    "easy_random",
    "medium_random",
    "hard_random",
    "beat_krool",
    "get_key8",
    "krem_kapture",
    "dk_rap_items",
    "krools_challenge",
  ];
  const KROOL_WIN_CONS = [
    "easy_random",
    "medium_random",
    "hard_random",
    "beat_krool",
  ]

  const winConSelection = document.getElementById("win_condition_item");
  const winConContainer = document.getElementById("win_condition_container");
  const winConReq = document.getElementById("win_condition_count");
  const disabled = DISABLED_WIN_VALUES.includes(winConSelection.value);
  const kroolSection = document.getElementById("krool_section");
  const isKRool = KROOL_WIN_CONS.includes(winConSelection.value);

  if (disabled) {
    winConContainer.classList.add("hide-input");
  } else {
    winConContainer.classList.remove("hide-input");
  }
  if (isKRool) {
    kroolSection.removeAttribute("hidden");
  } else {
    kroolSection.setAttribute("hidden", "hidden");
  }

  // Set K. Rool's Challenge to always be locked to 5 (all K. Rool phases)
  if (winConSelection.value === "krools_challenge") {
    winConReq.value = 5;
  } else if (!winConReq.value) {
    winConReq.value = 1;
  } else {
    const item_type = winConSelection.value;
    if (Object.keys(ITEM_CAPS).includes(item_type)) {
      if (parseInt(winConReq.value) > ITEM_CAPS[item_type]) {
        winConReq.value = ITEM_CAPS[item_type];
      }
    }
  }
}

document
  .getElementById("win_condition_item")
  .addEventListener("change", update_win_con_num_access);

// Validate Door 1 input on loss of focus
document
  .getElementById("crown_door_item_count")
  .addEventListener("focusout", function (event) {
    const doorOneReq = document.getElementById("crown_door_item_count");
    const doorOneSelection = document.getElementById("crown_door_item");

    if (!doorOneReq.value) {
      doorOneReq.value = 1;
    } else if (parseInt(doorOneReq.value) < 1) {
      doorOneReq.value = 1;
    } else {
      const item_type = doorOneSelection.value == "vanilla" ? "req_crown" : doorOneSelection.value;
      if (Object.keys(ITEM_CAPS).includes(item_type)) {
        if (parseInt(doorOneReq.value) > ITEM_CAPS[item_type]) {
          doorOneReq.value = ITEM_CAPS[item_type];
        }
      }
    }
  });

// Validate Door 2 input on loss of focus
document
  .getElementById("coin_door_item_count")
  .addEventListener("focusout", function (event) {
    const doorTwoReq = document.getElementById("coin_door_item_count");
    const doorTwoSelection = document.getElementById("coin_door_item");

    if (!doorTwoReq.value) {
      doorTwoReq.value = 1;
    } else if (parseInt(doorTwoReq.value) < 1) {
      doorTwoReq.value = 1;
    } else {
      const item_type = doorTwoSelection.value == "vanilla" ? "req_companycoins" : doorTwoSelection.value;
      if (Object.keys(ITEM_CAPS).includes(item_type)) {
        if (parseInt(doorTwoReq.value) > ITEM_CAPS[item_type]) {
          doorTwoReq.value = ITEM_CAPS[item_type];
        }
      }
    }
  });

function update_ice_trap_count() {
  const trapCountEl = document.getElementById("ice_trap_count");
  if (!trapCountEl.value) {
    trapCountEl.value = 0;
  } else if (trapCountEl.value < 0) {
    trapCountEl.value = 0;
  } else if (trapCountEl.value > 999) {
    trapCountEl.value = 999;
  }
}

document.getElementById("ice_trap_count").addEventListener("change", update_ice_trap_count);

// Update B Locker Number Access
function update_blocker_num_access() {
  const blockerSelection = document.getElementById("blocker_selection_behavior");
  const blockerContainer = document.getElementById("b_locker_number_container");
  const blockerReq = document.getElementById("blocker_text");
  const disabled = blockerSelection.value == "pre_selected";

  if (disabled) {
    blockerContainer.classList.add("hide-input");
  } else {
    blockerContainer.classList.remove("hide-input");
  }

  if (blockerSelection.value == "chaos") {
    blockerReq.title = "The percentage of an item's maximum amount that your B. Lockers can roll up to. For example, a Chaos Ratio of 25 would have a maximum GB B. Locker of 50 (25% of 200)."
  } else {
    blockerReq.title = "The maximum number of Golden Bananas required to open a B. Locker."
  }

  if (!blockerReq.value) {
    blockerReq.value = 1;
  } else {
    const selection_type = blockerSelection.value;
    if (selection_type != "pre_selected") {
      if (selection_type == "chaos") {
        if (blockerReq.value > 100) {
          blockerReq.value = 100;
        }
      } else {
        // Random
        if (blockerReq.value > 201) {
          blockerReq.value = 201;
        }
      }
    }
  }
}

document
  .getElementById("blocker_selection_behavior")
  .addEventListener("change", update_blocker_num_access);

// Update T&S Number Access
function update_troff_number_access() {
  const troffSelection = document.getElementById("tns_selection_behavior");
  const troffContainer = document.getElementById("troff_number_container");
  const troffReq = document.getElementById("troff_text");
  const disabled = troffSelection.value == "pre_selected";

  if (disabled) {
    troffContainer.classList.add("hide-input");
  } else {
    troffContainer.classList.remove("hide-input");
  }

  if (!troffReq.value) {
    troffReq.value = 1;
  } else {
    const selection_type = troffSelection.value;
    if (selection_type != "pre_selected") {
      // Random
      if (troffReq.value > 500) {
        troffReq.value = 500;
      }
    }
  }
}

document
  .getElementById("tns_selection_behavior")
  .addEventListener("change", update_troff_number_access);

function item_req_update(behavior, container, count, min, max) {
  const selection = document.getElementById(behavior);
  const containerEl = document.getElementById(container);
  const req = document.getElementById(count);
  const disabled = !["pre_selected", "progressive"].includes(selection.value);

  if (disabled) {
    containerEl.classList.add("hide-input");
  } else {
    containerEl.classList.remove("hide-input");
  }

  if (!req.value) {
    req.value = min;
  } else {
    const selection_type = selection.value;
    if (selection_type == "pre_selected") {
      // Random
      if (req.value > max) {
        req.value = max;
      }
    }
  }
}

document.getElementById("medal_jetpac_behavior")
  .addEventListener("change", () => {
    item_req_update("medal_jetpac_behavior", "medal_jetpac_behavior_container", "medal_requirement", 1, 40);
  });
document.getElementById("pearl_mermaid_behavior")
  .addEventListener("change", () => {
    item_req_update("pearl_mermaid_behavior", "pearl_mermaid_behavior_container", "mermaid_gb_pearls", 1, 5);
  });
document.getElementById("fairy_queen_behavior")
  .addEventListener("change", () => {
    item_req_update("fairy_queen_behavior", "fairy_queen_behavior_container", "rareware_gb_fairies", 1, 20);
  });
document.getElementById("cb_medal_behavior_new")
  .addEventListener("change", () => {
    item_req_update("cb_medal_behavior_new", "cb_medal_behavior_new_container", "medal_cb_req", 1, 100);
  });

$(document).on('mousedown', 'select option.starting_moves_option', function (e) {
    this.selected = !this.selected;
    e.preventDefault();
});

document
  .getElementById("starting_moves_list_mover_1")
  .addEventListener("click", function (event) {
    moveSelectedStartingMoves(1);
  });

document
  .getElementById("starting_moves_list_mover_2")
  .addEventListener("click", function (event) {
    moveSelectedStartingMoves(2);
  });

document
  .getElementById("starting_moves_list_mover_3")
  .addEventListener("click", function (event) {
    moveSelectedStartingMoves(3);
  });

document
  .getElementById("starting_moves_list_mover_4")
  .addEventListener("click", function (event) {
    moveSelectedStartingMoves(4);
  });

document
  .getElementById("starting_moves_list_mover_5")
  .addEventListener("click", function (event) {
    moveSelectedStartingMoves(5);
  });

document
  .getElementById("starting_moves_modal")
  .addEventListener("click", function (event) {
    assessAllItemPoolCounts();
  });

document
  .getElementById("starting_moves_list_count_1").addEventListener("change", function (event) {
    assessItemPoolCount(1);
  });

document
  .getElementById("starting_moves_list_count_2").addEventListener("change", function (event) {
    assessItemPoolCount(2);
  });

document
  .getElementById("starting_moves_list_count_3").addEventListener("change", function (event) {
    assessItemPoolCount(3);
  });

document
  .getElementById("starting_moves_list_count_4").addEventListener("change", function (event) {
    assessItemPoolCount(4);
  });

document
  .getElementById("starting_moves_list_count_5").addEventListener("change", function (event) {
    assessItemPoolCount(5);
  });

function assessAllItemPoolCounts() {
  // Determine the label/coloring status of all item pools at once. This also shows and hides entire columns.
  found_not_empty_item_pool = false;
  for (let i = 5; i >= 1; i--) {
    assessItemPoolCount(i);

    const list_selector = document.getElementById("starting_moves_list_" + i);
    const selector_column = document.getElementById("starting_moves_list_column_" + i);
    selector_column.removeAttribute("hidden");
    const number_of_moves_in_pool = Array.from(list_selector.options).filter(option => !option.hidden).length;
    if (!found_not_empty_item_pool && number_of_moves_in_pool > 0) {
      found_not_empty_item_pool = true;
      for (let j = i+2; j <= 5; j++) {
        const empty_selector_column = document.getElementById("starting_moves_list_column_" + j);
        empty_selector_column.setAttribute("hidden", "hidden");
      }
    }
  }
}

function assessItemPoolCount(target_list_id) {
  // Determine if the given item pool is starting with all, some, or none of the item in the list and update the UI accordingly.
  const move_count = document.getElementById("starting_moves_list_count_" + target_list_id);
  const list_selector = document.getElementById("starting_moves_list_" + target_list_id);
  const mover_button = document.getElementById("starting_moves_list_mover_" + target_list_id);
  const all_label = document.getElementById("starting_moves_list_all_" + target_list_id);
  all_label.setAttribute("hidden", "hidden");
  const some_label = document.getElementById("starting_moves_list_some_" + target_list_id);
  some_label.setAttribute("hidden", "hidden");
  const none_label = document.getElementById("starting_moves_list_none_" + target_list_id);
  none_label.setAttribute("hidden", "hidden");
  const number_of_moves_in_pool = Array.from(list_selector.options).filter(option => !option.hidden).length;
  if (move_count.value == 0 || number_of_moves_in_pool == 0) {
    none_label.removeAttribute("hidden");
    list_selector.style = "border-color: red";
    move_count.style = "border-color: red";
    mover_button.style = "border-color: red";
  } else if (move_count.value >= number_of_moves_in_pool) {
      all_label.removeAttribute("hidden");
      list_selector.style = "border-color: green";
      move_count.style = "border-color: green";
      mover_button.style = "border-color: green";
  } else {
    some_label.removeAttribute("hidden");
    list_selector.style = "border-color: orange";
    move_count.style = "border-color: orange";
    mover_button.style = "border-color: orange";
  }
}

function moveSelectedStartingMoves(target_list_id) {
  let selected_moves = [];
  for (let i = 1; i <= 5; i++) {
    const move_selector = document.getElementById("starting_moves_list_" + i);
    for (let j = 0; j < move_selector.options.length; j++) {
      const move = move_selector.options[j];
      if (move.selected) {
        selected_moves.push(move);
        move_selector.options.remove(j);
        j--;
      }
    }
  }
  const target_selector = document.getElementById("starting_moves_list_" + target_list_id);
  for (let i = 0; i < selected_moves.length; i++) {
    let moved_move = document.createElement('option');
    moved_move.id = selected_moves[i].id;
    moved_move.text = selected_moves[i].text;
    moved_move.classList = selected_moves[i].classList;
    if (selected_moves[i].hidden) {
      moved_move.setAttribute("hidden", "hidden");
    }
    target_selector.appendChild(moved_move);
  }
  assessAllItemPoolCounts();
}

// Move all starting moves back to list #1.
function startingMovesFullReset() {
  for (let i = 2; i <= 5; i++) {
    const move_selector = document.getElementById(`starting_moves_list_${i}`);
    for (const move of move_selector.options) {
      move.selected = true;
    }
  }
  moveSelectedStartingMoves(1);
}

// Min-Max validation for inputs
function minMax(event, min, max) {
  try {
    const value = parseInt(event.target.value);
    if (value >= max) {
      event.preventDefault();
      document.getElementById(event.target.id).value = max;
    } else if (value <= min) {
      event.preventDefault();
      document.getElementById(event.target.id).value = min;
    }
  } catch (error) {
    event.preventDefault();
    document.getElementById(event.target.id).value = min;
  }
}

// Handle keydown event for number inputs, allowing only valid keys
document
  .querySelectorAll("[id^=blocker_], [id^=troff_], #blocker_text, #troff_text")
  .forEach((element) => {
    element.addEventListener("keydown", function (event) {
      const globalKeys = [
        "Backspace",
        "Delete",
        "ArrowLeft",
        "ArrowRight",
        "Control",
        "x",
        "v",
        "c",
      ];
      if (!event.key.match(/\d/) && !globalKeys.includes(event.key)) {
        event.preventDefault();
      }
    });
  });

// Dropdown Multiselect
function toggleDropdown(name) {
  const menu = document.getElementById(`${name}_selected`);
  menu.classList.toggle('show');
}

function pushUpdateToDropdown(name) {
  const ddms = document.getElementById(`dropdown_${name}`);
  const event = new Event("change", { bubbles: true, cancelable: false });
  ddms.dispatchEvent(event);
}

function updateSelected(name) {
  const container = document.getElementById(`${name}_selected`);
  const checkboxes = container ? container.getElementsByTagName('input') : [];
  const countLabel = document.getElementById(`selectedCount_${name}`);

  let selectedCount = 0;
  for (let cb of checkboxes) {
    if (cb.checked) {
        selectedCount++;
    }
  }

  countLabel.innerText = `${selectedCount} item${selectedCount !== 1 ? 's' : ''} selected`;
}

function dropdownForceAll(name, state) {
  const container = document.getElementById(`${name}_selected`);
  const checkboxes = container ? container.getElementsByTagName('input') : [];
  const countLabel = document.getElementById(`selectedCount_${name}`);
  for (let cb of checkboxes) {
    cb.checked = state;
  }
  const selectedCount = state ? checkboxes.length : 0;
  countLabel.innerText = `${selectedCount} item${selectedCount !== 1 ? 's' : ''} selected`;
  pushUpdateToDropdown(name);
}

function hide_irrelevant_details_coupled_item_rando() {
  const value = document.getElementById("decouple_item_rando").checked;
  const details = document.getElementsByClassName("hide-if-ir-decouple");
  const antidetails = document.getElementsByClassName("show-if-ir-decouple");
  if (value) {
    for (let el of details) {
      if (el.classList.contains("decouple-hide")) {
        el.removeAttribute("hidden");
      } else {
        el.classList.add("d-flex");
        el.classList.remove("d-none");
      }
    }
    for (let el of antidetails) {
      if (el.classList.contains("decouple-hide")) {
        el.setAttribute("hidden", "hidden");
      } else {
        el.classList.remove("d-flex");
        el.classList.add("d-none");
      }
    }
  } else {
    for (let el of details) {
      if (el.classList.contains("decouple-hide")) {
        el.setAttribute("hidden", "hidden");
      } else {
        el.classList.remove("d-flex");
        el.classList.add("d-none");
      }
    }
    for (let el of antidetails) {
      if (el.classList.contains("decouple-hide")) {
        el.removeAttribute("hidden");
      } else {
        el.classList.add("d-flex");
        el.classList.remove("d-none");
      }
    }
  }
}
document.getElementById("decouple_item_rando")
  .addEventListener("click", hide_irrelevant_details_coupled_item_rando)

function update_trap_weight(el, default_value, force) {
  let all_zero = true;
  if (!force) {
    Object.keys(default_trap_weights).forEach(s => {
      if (document.getElementById(s).value > 0) {
        all_zero = false;
      }
    })
  }
  if ((!el.value && el.value !== 0) || all_zero) {
    el.value = default_value;
  } else if (el.value < 0) {
    el.value = 0;
  } else if (el.value > 100) {
    el.value = 100;
  }
  return all_zero;
}

function update_all_trap_weights() {
  let force_trap_weight_reset = false;
  Object.keys(default_trap_weights).forEach(stg => {
    document.getElementById(stg).addEventListener("change", (e) => {
      force_trap_weight_reset = update_trap_weight(e.target, default_trap_weights[stg], force_trap_weight_reset);
    })
  })
}

const alterers = document.getElementsByClassName("item-count-alterer");
function getTotalItemCounts() {
    const alt_v = document.getElementsByClassName("item-count-alterer")
    let total = 0;
    for (let a = 0; a < alt_v.length; a++) {
        const local_value = parseInt(alt_v[a].value);
        const local_id = alt_v[a].getAttribute("id");
        const local_header = document.getElementById(`${local_id}_title`);
        let local_min = 1;
        const local_max = 255;
        if (local_id == "total_gbs") {
            local_min = 40;
        } else if (["total_crowns", "total_rainbow_coins"].includes(local_id)) {
            local_min = 0;
        }
        if ((local_value < local_min) || (local_value > local_max)) {
            local_header.style.color = "red";
        } else {
            local_header.style.color = "white";
        }
        total += local_value;
    }
    const notifier = document.getElementById("item_count_collective");
    if (total < 298) {
        notifier.style.color = "white";
    } else {
        notifier.style.color = "red";
    }
}
for (let a = 0; a < alterers.length; a++) {
    alterers[a].addEventListener("change", getTotalItemCounts);
    alterers[a].addEventListener("change", refreshItemRandoSortable);
}

// Bind custom update UI event for "apply_preset"
function update_ui_states() {
  /** Trigger any function that would update the status of a UI element based on the current settings configuration. */
  change_level_randomization(null);
  disable_colors();
  disable_music();
  max_randomized_blocker();
  max_randomized_troff();
  max_music();
  max_music_proportion();
  max_sfx();
  disable_switchsanity_modal();
  item_rando_list_changed(null);
  disable_custom_cb_locations_modal();
  toggle_bananaport_selector();
  disable_helm_hurry(null);
  disable_points(null);
  disable_slam_selector(null);
  toggle_logic_type(null);
  toggle_key_settings(null);
  //max_starting_moves_count(null);
  update_door_one_num_access();
  update_door_two_num_access();
  update_win_con_num_access();
  refreshItemRandoSortable();
  update_prog_hint_num_access();
  update_blocker_num_access();
  update_ice_trap_count();
  getTotalItemCounts();
  update_all_trap_weights();
  update_troff_number_access();
  item_req_update("medal_jetpac_behavior", "medal_jetpac_behavior_container", "medal_requirement", 1, 40);
  item_req_update("pearl_mermaid_behavior", "pearl_mermaid_behavior_container", "mermaid_gb_pearls", 1, 5);
  item_req_update("fairy_queen_behavior", "fairy_queen_behavior_container", "rareware_gb_fairies", 1, 20);
  item_req_update("cb_medal_behavior_new", "cb_medal_behavior_new_container", "medal_cb_req", 1, 100);
  disable_tag_spawn();
  disable_krool_phases();
  disable_helm_phases();
  enable_plandomizer();
  toggle_vanilla_door_rando();
  toggle_dos_door_rando();
  validate_fast_start_status(null);
  hide_irrelevant_details_coupled_item_rando();

  const sliders = document.getElementsByClassName("pretty-slider");
  for (let s = 0; s < sliders.length; s++) {
    const event = new Event("change", { bubbles: true, cancelable: false });
    sliders[s].dispatchEvent(event);
  }
}

document
  .getElementById("apply_preset")
  .addEventListener("custom-update-ui-event", update_ui_states);