function toggle_logic_type(event) {
  /** Toggle settings based on the presence of logic. */

  // Get the glitch customization modal element
  let glitchCustomization = document.getElementById("glitches_modal");

  // Check the value of the logic_type element and enable or disable the glitches modal
  if (document.getElementById("logic_type").value === "glitch") {
    glitchCustomization.removeAttribute("disabled");
  } else {
    glitchCustomization.setAttribute("disabled", "disabled");
  }
}

const DISABLED_HELM_DOOR_VALUES = [
  "easy_random",
  "medium_random",
  "hard_random",
  "opened",
];

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
function plando_disable_patch_custom_locations() {
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  let patchesShuffled = false;

  for (let option of itemRandoPool) {
    if (option.value === "rainbowcoin") {
      patchesShuffled = option.selected;
    }
  }

  const randomPatches = document.getElementById("random_patches").checked;
  const customPatchesElem = document.getElementById("plando_place_patches");
  let tooltip = "Allows the user to specify locations for each dirt patch.";

  if (patchesShuffled && randomPatches) {
    customPatchesElem.removeAttribute("disabled");
  } else {
    customPatchesElem.setAttribute("disabled", "disabled");
    customPatchesElem.checked = false;
    tooltip =
      "To use this feature, rainbow coins must be in the item pool, and dirt patch locations must be shuffled.";
  }

  customPatchesElem.parentElement.setAttribute(
    "data-bs-original-title",
    tooltip
  );
}

document
  .getElementById("random_patches")
  .addEventListener("click", plando_disable_patch_custom_locations);

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

// Disable Remove Barriers Selector when Remove Barriers is off
function disable_remove_barriers() {
  const selector = document.getElementById("remove_barriers_modal");
  const disabled = !document.getElementById("remove_barriers_enabled").checked;

  if (disabled) {
    selector.setAttribute("disabled", "disabled");
  } else {
    selector.removeAttribute("disabled");
  }
}

document
  .getElementById("remove_barriers_enabled")
  .addEventListener("click", disable_remove_barriers);

// Disable Faster Checks Selector when Faster Checks is off
function disable_faster_checks() {
  const selector = document.getElementById("faster_checks_modal");
  const disabled = !document.getElementById("faster_checks_enabled").checked;

  if (disabled) {
    selector.setAttribute("disabled", "disabled");
  } else {
    selector.removeAttribute("disabled");
  }
}

document
  .getElementById("faster_checks_enabled")
  .addEventListener("click", disable_faster_checks);

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
      "nav-random-tab",
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
      "nav-random-tab",
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

// Toggle the textbox for Banana Medals
function toggle_medals_box() {
  const disabled = document.getElementById("random_medal_requirement").checked;
  const medal = document.getElementById("medal_requirement");

  if (disabled) {
    medal.setAttribute("disabled", "disabled");
  } else {
    medal.removeAttribute("disabled");
  }
}

// Enable and disable the Plandomizer tab
async function enable_plandomizer() {
  const plandoTab = document.getElementById("nav-plando-tab");
  if (document.getElementById("enable_plandomizer").checked) {
    // Open up a Modal stating that we're loading the Plando tab
    $("#plando-modal").modal("show");    
    try {
      await setup_pyodide();
    } catch (error) {
      console.log("Error setting up Pyodide:", error);
    }
    try{
      // Load ui.__init__.py
      await run_python_file("ui/__init__.py");
    }
    catch (error) {
      console.log("Error running ui/__init__.py:", error);
    }
    plandoTab.style.display = "";
    $("#plando-modal").modal("hide");
  } else {
    plandoTab.style.display = "none";
    $("#plando-modal").modal("hide");
  }
}

document
  .getElementById("enable_plandomizer")
  .addEventListener("click", enable_plandomizer);

// Disable Minigame Selector when Shuffle Bonus Barrels is off
function disable_barrel_modal() {
  const selector = document.getElementById("minigames_list_modal");
  if (document.getElementById("bonus_barrel_rando").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("bonus_barrel_rando")
  .addEventListener("click", disable_barrel_modal);

function disable_enemy_modal() {
  const selector = document.getElementById("enemies_modal");
  if (document.getElementById("enemy_rando").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("enemy_rando")
  .addEventListener("click", disable_enemy_modal);

// Disable Hard Mode Selector when Hard Mode is off
function disable_hard_mode_modal() {
  const selector = document.getElementById("hard_mode_modal");
  if (document.getElementById("hard_mode").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}
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

document
  .getElementById("hard_mode")
  .addEventListener("click", disable_hard_mode_modal);

// Disable Hard Bosses Selector when Hard Bosses is off
function disable_hard_bosses_modal() {
  const selector = document.getElementById("hard_bosses_modal");
  if (document.getElementById("hard_bosses").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("hard_bosses")
  .addEventListener("click", disable_hard_bosses_modal);

// Disable Excluded Song Selector when Excluded Songs is off
function disable_excluded_songs_modal(evt) {
  const selector = document.getElementById("excluded_songs_modal");
  if (document.getElementById("songs_excluded").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

// Adding event listeners for nav-music-tab and songs_excluded
document
  .getElementById("nav-music-tab")
  .addEventListener("click", disable_excluded_songs_modal);
document
  .getElementById("songs_excluded")
  .addEventListener("click", disable_excluded_songs_modal);

// Disable Music Filtering Selector when Music Filtering is off
function disable_music_filtering_modal() {
  const selector = document.getElementById("music_filtering_modal");
  if (document.getElementById("music_filtering").checked) {
    selector.removeAttribute("disabled");
  } else {
    selector.setAttribute("disabled", "disabled");
  }
}

document
  .getElementById("music_filtering")
  .addEventListener("click", disable_music_filtering_modal);

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
      tooltip = "To assign a reward here, Isles CBs must be shuffled.";
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
    disable_krool_phases(evt);
    disable_helm_phases(evt);
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
    plando_disable_patch_custom_locations(evt);
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
  update_ui_states(evt);
});

// Disable Boss Kong and Boss Location Rando if Vanilla levels and Kong Rando
document.getElementById("kong_rando").addEventListener("click", function (evt) {
  const level = document.getElementById("level_randomization");
  const bossLocation = document.getElementById("boss_location_rando");
  const bossKong = document.getElementById("boss_kong_rando");
  const kongRando = document.getElementById("kong_rando");

  if (
    kongRando.checked &&
    (level.value === "vanilla" || level.value === "level_order")
  ) {
    bossLocation.setAttribute("disabled", "disabled");
    bossLocation.checked = true;
    bossKong.setAttribute("disabled", "disabled");
    bossKong.checked = true;
  } else {
    bossKong.removeAttribute("disabled");
    bossLocation.removeAttribute("disabled");
  }
});

// Disable color options when Randomize All is selected
function disable_colors() {
  const disabled = document.getElementById("random_colors").checked;
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
  .getElementById("random_colors")
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
// Enable Kong Rando if less than 5 starting kongs
document
  .getElementById("starting_kongs_count")
  .addEventListener("change", function (evt) {
    const kongRando = document.getElementById("kong_rando");
    if (document.getElementById("starting_kongs_count").value == "5") {
      kongRando.checked = false;
      kongRando.setAttribute("disabled", "disabled");
    } else {
      kongRando.removeAttribute("disabled");
    }
  });

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

// Disable some settings based on the move rando setting
function disable_move_shuffles() {
  const moves = document.getElementById("move_rando");
  const prices = document.getElementById("random_prices");
  if (moves) {
    if (moves.value === "start_with" || moves.value === "off") {
      if (prices) {
        prices.setAttribute("disabled", "disabled");
      }
    } else {
      if (prices) {
        prices.removeAttribute("disabled");
      }
    }
  }
}

document
  .getElementById("move_rando")
  .addEventListener("change", disable_move_shuffles);

// Enable and disable settings based on Item Rando being on/off
function toggle_item_rando() {
  const elements = {
    selector: document.getElementById("item_rando_list_modal"),
    itemRandoPool: document.getElementById("item_rando_list_selected").options,
    smallerShops: document.getElementById("smaller_shops"),
    moveVanilla: document.getElementById("move_off"),
    moveRando: document.getElementById("move_on"),
    enemyDropRando: document.getElementById("enemy_drop_rando"),
    nonItemRandoWarning: document.getElementById("non_item_rando_warning"),
    sharedShopWarning: document.getElementById("shared_shop_warning"),
    kongRando: document.getElementById("kong_rando"),
    shuffleItems: document.getElementById("shuffle_items"),
    moveOnCrossPurchase: document.getElementById("move_on_cross_purchase"),
    randomPrices: document.getElementById("random_prices"),
  };

  let shopsInPool = false;
  let kongsInPool = false;
  let nothingSelected = true;

  for (let option of elements.itemRandoPool) {
    if (option.selected) {
      nothingSelected = false;
      if (option.value === "shop") shopsInPool = true;
      if (option.value === "kong") kongsInPool = true;
    }
  }

  if (nothingSelected) {
    shopsInPool = kongsInPool = true;
  }

  const disabled = !elements.shuffleItems.checked;

  elements.selector.toggleAttribute("disabled", disabled);
  elements.smallerShops.toggleAttribute("disabled", disabled || !shopsInPool);
  if (disabled || !shopsInPool) {
    elements.smallerShops.checked = false;
  }
  elements.moveVanilla.toggleAttribute("disabled", shopsInPool && !disabled);
  elements.moveRando.toggleAttribute("disabled", shopsInPool && !disabled);
  elements.enemyDropRando.toggleAttribute("disabled", disabled);
  if (disabled) {
    elements.enemyDropRando.checked = false;
  }
  elements.nonItemRandoWarning.toggleAttribute("hidden", !disabled);
  elements.sharedShopWarning.toggleAttribute("hidden", shopsInPool && !disabled);
  if (!disabled) {
    elements.kongRando.toggleAttribute("disabled", kongsInPool);
    elements.kongRando.checked = kongsInPool;
  }

  if (!disabled && shopsInPool) {
    if (elements.moveVanilla.selected || elements.moveRando.selected) {
      elements.moveOnCrossPurchase.selected = true;
    }
    elements.randomPrices.removeAttribute("disabled");
  }
}


document
  .getElementById("shuffle_items")
  .addEventListener("click", toggle_item_rando);
// Enable and disable settings based on the Item Rando pool changing
document
  .getElementById("item_rando_list_select_all")
  .addEventListener("click", item_rando_list_changed);
document
  .getElementById("item_rando_list_reset")
  .addEventListener("click", item_rando_list_changed);
document
  .getElementById("item_rando_list_selected")
  .addEventListener("click", item_rando_list_changed);

function item_rando_list_changed(evt) {
  let itemRandoDisabled = true;
  const itemRandoPool = document.getElementById(
    "item_rando_list_selected"
  ).options;
  const smallerShops = document.getElementById("smaller_shops");
  const moveVanilla = document.getElementById("move_off");
  const moveRando = document.getElementById("move_on");
  const sharedShopWarning = document.getElementById("shared_shop_warning");
  const kongRando = document.getElementById("kong_rando");
  let shopsInPool = false;
  let kongsInPool = false;
  let shockwaveInPool = false;
  let shopownersInPool = false;
  let nothingSelected = true;

  for (let option of itemRandoPool) {
    if (option.value === "shop" && option.selected) shopsInPool = true;
    if (option.value === "kong" && option.selected) kongsInPool = true;
    if (option.value === "shockwave" && option.selected) shockwaveInPool = true;
    if (option.value === "shopowners" && option.selected) shopownersInPool = true;
    if (option.selected) nothingSelected = false;
  }

  if (nothingSelected) {
    shopsInPool = true;
    kongsInPool = true;
    shockwaveInPool = true;
    shopownersInPool = true;
  }

  if (document.getElementById("shuffle_items").checked) {
    itemRandoDisabled = false;
  }

  let camera_option = document.getElementById("starting_move_52");
  let shockwave_option = document.getElementById("starting_move_53");
  let cranky_option = document.getElementById("starting_move_92");
  let funky_option = document.getElementById("starting_move_93");
  let candy_option = document.getElementById("starting_move_94");
  let snide_option = document.getElementById("starting_move_95");

  if (itemRandoDisabled) {
    camera_option.setAttribute("hidden", "hidden");
    shockwave_option.setAttribute("hidden", "hidden");
    cranky_option.setAttribute("hidden", "hidden");
    funky_option.setAttribute("hidden", "hidden");
    candy_option.setAttribute("hidden", "hidden");
    snide_option.setAttribute("hidden", "hidden");
  }

  if (shopsInPool && !itemRandoDisabled) {
    sharedShopWarning.setAttribute("hidden", "hidden");
    if (moveVanilla.selected || moveRando.selected) {
      document.getElementById("move_on_cross_purchase").selected = true;
    }
    moveVanilla.setAttribute("disabled", "disabled");
    moveRando.setAttribute("disabled", "disabled");
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
    moveVanilla.removeAttribute("disabled");
    moveRando.removeAttribute("disabled");
    smallerShops.setAttribute("disabled", "disabled");
    smallerShops.checked = false;
  }

  if (kongsInPool && !itemRandoDisabled) {
    kongRando.setAttribute("disabled", "disabled");
    kongRando.checked = true;
  } else {
    kongRando.removeAttribute("disabled");
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
  const fastStart = document.getElementById("fast_start_beginning_of_game");

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

// Toggle the textboxes for BLockers
document.getElementById("randomize_blocker_required_amounts").addEventListener("click", toggle_b_locker_boxes);

function toggle_b_locker_boxes(evt) {
    const disabled = !document.getElementById("randomize_blocker_required_amounts").checked;
    const blockerText = document.getElementById("blocker_text");
    const maximizeHelmBlocker = document.getElementById("maximize_helm_blocker");

    if (disabled) {
        blockerText.disabled = true;
        maximizeHelmBlocker.disabled = true;

        for (let i = 0; i < 10; i++) {
            var blocker = document.getElementById(`blocker_${i}`);
            if (blocker){ 
                blocker.removeAttribute("disabled");
            }
        }
    } else {
        blockerText.removeAttribute("disabled");
        maximizeHelmBlocker.removeAttribute("disabled");

        for (let i = 0; i < 10; i++) {
            var blocker = document.getElementById(`blocker_${i}`);
            if (blocker){ 
                blocker.disabled = true;
            }
        }
    }
}

// Toggle the textboxes for Troff
document.getElementById("randomize_cb_required_amounts").addEventListener("click", toggle_counts_boxes);

function toggle_counts_boxes(evt) {
    const disabled = !document.getElementById("randomize_cb_required_amounts").checked;
    const troffText = document.getElementById("troff_text");

    if (disabled) {
        troffText.disabled = true;

        for (let i = 0; i < 10; i++) {
            var troff = document.getElementById(`troff_${i}`);
            if (troff) {
                troff.removeAttribute("disabled");
            }
        }
    } else {
        troffText.removeAttribute("disabled");

        for (let i = 0; i < 10; i++) {
            var troff = document.getElementById(`troff_${i}`);
            if (troff) {
                troff.disabled = true;
            }
        }
    }
}


// Change level randomization
document
  .getElementById("level_randomization")
  .addEventListener("change", change_level_randomization);

function change_level_randomization(evt) {
  validate_fast_start_status(evt);

    const level = document.getElementById("level_randomization");
    const bossLocation = document.getElementById("boss_location_rando");
    const bossKong = document.getElementById("boss_kong_rando");
    const kongRando = document.getElementById("kong_rando");
    const shuffleHelmLocation = document.getElementById("shuffle_helm_location");
    const helmLabel = document.getElementById("shuffle_helm_location_label");

    const isLevelOrder = ["level_order", "level_order_complex"].includes(level.value);
    const disableBossShuffles = ["level_order", "level_order_complex"].includes(level.value) || (level.value === "vanilla" && kongRando.checked);
    const disableKongRando = ["level_order", "level_order_complex"].includes(level.value);
    const disableShuffleHelmLocation = level.value === "vanilla";

  if (disableBossShuffles) {
    bossLocation.setAttribute("disabled", "disabled");
    bossLocation.checked = true;
    bossKong.setAttribute("disabled", "disabled");
    bossKong.checked = true;
  } else {
    bossLocation.removeAttribute("disabled");
    bossKong.removeAttribute("disabled");
  }

  if (disableKongRando) {
    kongRando.setAttribute("disabled", "disabled");
    kongRando.checked = true;
  } else {
    kongRando.removeAttribute("disabled");
  }

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
  } else if (
    progHintSelection.value === "req_gb" &&
    parseInt(progHintReq.value) > 201
  ) {
    progHintReq.value = 201;
  } else if (
    progHintSelection.value === "req_bp" &&
    parseInt(progHintReq.value) > 40
  ) {
    progHintReq.value = 40;
  } else if (
    progHintSelection.value === "req_key" &&
    parseInt(progHintReq.value) > 8
  ) {
    progHintReq.value = 8;
  } else if (
    progHintSelection.value === "req_medal" &&
    parseInt(progHintReq.value) > 40
  ) {
    progHintReq.value = 40;
  } else if (
    progHintSelection.value === "req_crown" &&
    parseInt(progHintReq.value) > 10
  ) {
    progHintReq.value = 10;
  } else if (
    progHintSelection.value === "req_fairy" &&
    parseInt(progHintReq.value) > 18
  ) {
    progHintReq.value = 18;
  } else if (
    progHintSelection.value === "req_bean" &&
    parseInt(progHintReq.value) > 1
  ) {
    progHintReq.value = 1;
  } else if (
    progHintSelection.value === "req_pearl" &&
    parseInt(progHintReq.value) > 5
  ) {
    progHintReq.value = 5;
  } else if (
    progHintSelection.value === "req_rainbowcoin" &&
    parseInt(progHintReq.value) > 16
  ) {
    progHintReq.value = 16;
  } else if (
    progHintSelection.value === "req_cb" &&
    parseInt(progHintReq.value) > 3500
  ) {
    progHintReq.value = 3500;
  }
}

document
  .getElementById("progressive_hint_item")
  .addEventListener("change", update_prog_hint_num_access);

// Validate chaos ratio input on loss of focus
function handle_chaos_ratio_text() {
  const chaosRatioText = document.getElementById("chaos_ratio");
  if (!chaosRatioText.value) {
    chaosRatioText.value = 25;
  } else if (parseInt(chaosRatioText.value) < 1) {
    chaosRatioText.value = 1;
  } else if (parseInt(chaosRatioText.value) > 100) {
    chaosRatioText.value = 100;
  }
}

document
  .getElementById("chaos_ratio")
  .addEventListener("focusout", handle_chaos_ratio_text);

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

// // Validate starting moves count input on loss of focus
// // Function to handle validation of starting moves count
// function max_starting_moves_count() {
//   const moveCount = document.getElementById("starting_moves_count");
//   const moves = document.getElementById("move_rando");
//   const itemRando = document.getElementById("shuffle_items");
//   let maxStartingMoves = 41;

//   if (!itemRando.checked && moves.value !== "off") {
//     maxStartingMoves = 4;
//   }

//   if (!moveCount.value) {
//     moveCount.value = 4;
//   } else if (parseInt(moveCount.value) < 0) {
//     moveCount.value = 0;
//   } else if (parseInt(moveCount.value) > maxStartingMoves) {
//     moveCount.value = maxStartingMoves;
//   }
// }

// Adding event listeners for shuffle_items, move_rando, and starting_moves_count
// document
//   .getElementById("shuffle_items")
//   .addEventListener("click", max_starting_moves_count);
// document
//   .getElementById("move_rando")
//   .addEventListener("change", max_starting_moves_count);
// document
//   .getElementById("starting_moves_count")
//   .addEventListener("focusout", max_starting_moves_count);

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
  } else if (
    doorOneSelection.value === "vanilla" &&
    parseInt(doorOneReq.value) > 10
  ) {
    doorOneReq.value = 10;
  } else if (
    doorOneSelection.value === "req_gb" &&
    parseInt(doorOneReq.value) > 201
  ) {
    doorOneReq.value = 201;
  } else if (
    doorOneSelection.value === "req_bp" &&
    parseInt(doorOneReq.value) > 40
  ) {
    doorOneReq.value = 40;
  } else if (
    doorOneSelection.value === "req_companycoins" &&
    parseInt(doorOneReq.value) > 2
  ) {
    doorOneReq.value = 2;
  } else if (
    doorOneSelection.value === "req_key" &&
    parseInt(doorOneReq.value) > 8
  ) {
    doorOneReq.value = 8;
  } else if (
    doorOneSelection.value === "req_fairy" &&
    parseInt(doorOneReq.value) > 18
  ) {
    doorOneReq.value = 18;
  } else if (
    doorOneSelection.value === "req_bean" &&
    parseInt(doorOneReq.value) > 1
  ) {
    doorOneReq.value = 1;
  } else if (
    doorOneSelection.value === "req_pearl" &&
    parseInt(doorOneReq.value) > 5
  ) {
    doorOneReq.value = 5;
  } else if (
    doorOneSelection.value === "req_rainbowcoin" &&
    parseInt(doorOneReq.value) > 16
  ) {
    doorOneReq.value = 16;
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
  } else if (
    doorTwoSelection.value === "vanilla" &&
    parseInt(doorTwoReq.value) > 2
  ) {
    doorTwoReq.value = 2;
  } else if (
    doorTwoSelection.value === "req_gb" &&
    parseInt(doorTwoReq.value) > 201
  ) {
    doorTwoReq.value = 201;
  } else if (
    doorTwoSelection.value === "req_bp" &&
    parseInt(doorTwoReq.value) > 40
  ) {
    doorTwoReq.value = 40;
  } else if (
    doorTwoSelection.value === "req_key" &&
    parseInt(doorTwoReq.value) > 8
  ) {
    doorTwoReq.value = 8;
  } else if (
    doorTwoSelection.value === "req_medal" &&
    parseInt(doorTwoReq.value) > 40
  ) {
    doorTwoReq.value = 40;
  } else if (
    doorTwoSelection.value === "req_crown" &&
    parseInt(doorTwoReq.value) > 10
  ) {
    doorTwoReq.value = 10;
  } else if (
    doorTwoSelection.value === "req_fairy" &&
    parseInt(doorTwoReq.value) > 18
  ) {
    doorTwoReq.value = 18;
  } else if (
    doorTwoSelection.value === "req_bean" &&
    parseInt(doorTwoReq.value) > 1
  ) {
    doorTwoReq.value = 1;
  } else if (
    doorTwoSelection.value === "req_pearl" &&
    parseInt(doorTwoReq.value) > 5
  ) {
    doorTwoReq.value = 5;
  } else if (
    doorTwoSelection.value === "req_rainbowcoin" &&
    parseInt(doorTwoReq.value) > 16
  ) {
    doorTwoReq.value = 16;
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
  ];

  const winConSelection = document.getElementById("win_condition_item");
  const winConContainer = document.getElementById("win_condition_container");
  const winConReq = document.getElementById("win_condition_count");
  const disabled = DISABLED_WIN_VALUES.includes(winConSelection.value);

  if (disabled) {
    winConContainer.classList.add("hide-input");
  } else {
    winConContainer.classList.remove("hide-input");
  }

  if (!winConReq.value) {
    winConReq.value = 1;
  } else if (
    winConSelection.value === "req_gb" &&
    parseInt(winConReq.value) > 201
  ) {
    winConReq.value = 201;
  } else if (
    winConSelection.value === "req_bp" &&
    parseInt(winConReq.value) > 40
  ) {
    winConReq.value = 40;
  } else if (
    winConSelection.value === "req_key" &&
    parseInt(winConReq.value) > 8
  ) {
    winConReq.value = 8;
  } else if (
    winConSelection.value === "req_medal" &&
    parseInt(winConReq.value) > 40
  ) {
    winConReq.value = 40;
  } else if (
    winConSelection.value === "req_crown" &&
    parseInt(winConReq.value) > 10
  ) {
    winConReq.value = 10;
  } else if (
    winConSelection.value === "req_fairy" &&
    parseInt(winConReq.value) > 18
  ) {
    winConReq.value = 18;
  } else if (
    winConSelection.value === "req_bean" &&
    parseInt(winConReq.value) > 1
  ) {
    winConReq.value = 1;
  } else if (
    winConSelection.value === "req_pearl" &&
    parseInt(winConReq.value) > 5
  ) {
    winConReq.value = 5;
  } else if (
    winConSelection.value === "req_rainbowcoin" &&
    parseInt(winConReq.value) > 16
  ) {
    winConReq.value = 16;
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
    } else if (
      doorOneSelection.value === "vanilla" &&
      parseInt(doorOneReq.value) > 10
    ) {
      doorOneReq.value = 10;
    } else if (
      doorOneSelection.value === "req_gb" &&
      parseInt(doorOneReq.value) > 201
    ) {
      doorOneReq.value = 201;
    } else if (
      doorOneSelection.value === "req_bp" &&
      parseInt(doorOneReq.value) > 40
    ) {
      doorOneReq.value = 40;
    } else if (
      doorOneSelection.value === "req_companycoins" &&
      parseInt(doorOneReq.value) > 2
    ) {
      doorOneReq.value = 2;
    } else if (
      doorOneSelection.value === "req_key" &&
      parseInt(doorOneReq.value) > 8
    ) {
      doorOneReq.value = 8;
    } else if (
      doorOneSelection.value === "req_medal" &&
      parseInt(doorOneReq.value) > 40
    ) {
      doorOneReq.value = 40;
    } else if (
      doorOneSelection.value === "req_fairy" &&
      parseInt(doorOneReq.value) > 18
    ) {
      doorOneReq.value = 18;
    } else if (
      doorOneSelection.value === "req_bean" &&
      parseInt(doorOneReq.value) > 1
    ) {
      doorOneReq.value = 1;
    } else if (
      doorOneSelection.value === "req_pearl" &&
      parseInt(doorOneReq.value) > 5
    ) {
      doorOneReq.value = 5;
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
    }

    if (
      doorTwoSelection.value === "vanilla" &&
      parseInt(doorTwoReq.value) > 2
    ) {
      doorTwoReq.value = 2;
    } else if (
      doorTwoSelection.value === "req_gb" &&
      parseInt(doorTwoReq.value) > 201
    ) {
      doorTwoReq.value = 201;
    } else if (
      doorTwoSelection.value === "req_bp" &&
      parseInt(doorTwoReq.value) > 40
    ) {
      doorTwoReq.value = 40;
    } else if (
      doorTwoSelection.value === "req_key" &&
      parseInt(doorTwoReq.value) > 8
    ) {
      doorTwoReq.value = 8;
    } else if (
      doorTwoSelection.value === "req_medal" &&
      parseInt(doorTwoReq.value) > 40
    ) {
      doorTwoReq.value = 40;
    } else if (
      doorTwoSelection.value === "req_crown" &&
      parseInt(doorTwoReq.value) > 10
    ) {
      doorTwoReq.value = 10;
    } else if (
      doorTwoSelection.value === "req_fairy" &&
      parseInt(doorTwoReq.value) > 18
    ) {
      doorTwoReq.value = 18;
    } else if (
      doorTwoSelection.value === "req_bean" &&
      parseInt(doorTwoReq.value) > 1
    ) {
      doorTwoReq.value = 1;
    } else if (
      doorTwoSelection.value === "req_pearl" &&
      parseInt(doorTwoReq.value) > 5
    ) {
      doorTwoReq.value = 5;
    }
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
// Bind custom update UI event for "apply_preset"
function update_ui_states() {
  /** Trigger any function that would update the status of a UI element based on the current settings configuration. */
  toggle_counts_boxes(null);
  toggle_b_locker_boxes(null);
  change_level_randomization(null);
  disable_colors(null);
  disable_music(null);
  disable_move_shuffles(null);
  max_randomized_blocker(null);
  handle_chaos_ratio_text(null);
  max_randomized_troff(null);
  max_music(null);
  max_music_proportion(null);
  max_sfx(null);
  disable_barrel_modal(null);
  item_rando_list_changed(null);
  toggle_item_rando(null);
  disable_enemy_modal(null);
  disable_hard_mode_modal(null);
  disable_hard_bosses_modal(null);
  disable_excluded_songs_modal(null);
  disable_music_filtering_modal(null);
  toggle_bananaport_selector(null);
  disable_helm_hurry(null);
  disable_remove_barriers(null);
  disable_faster_checks(null);
  toggle_logic_type(null);
  toggle_key_settings(null);
  //max_starting_moves_count(null);
  update_door_one_num_access(null);
  update_door_two_num_access(null);
  update_win_con_num_access(null);
  update_prog_hint_num_access(null);
  disable_tag_spawn(null);
  disable_krool_phases(null);
  disable_helm_phases(null);
  enable_plandomizer(null);
  toggle_medals_box(null);
  toggle_vanilla_door_rando(null);
  toggle_dos_door_rando(null);
  validate_fast_start_status(null);

  const sliders = document.getElementsByClassName("pretty-slider");
  for (let s = 0; s < sliders.length; s++) {
    const event = new Event("change", { bubbles: true, cancelable: false });
    sliders[s].dispatchEvent(event);
  }
}

document
  .getElementById("apply_preset")
  .addEventListener("custom-update-ui-event", update_ui_states);
