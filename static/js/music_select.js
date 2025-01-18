
// Create an array of music toggle IDs based on the keys of MusicSelectionPanel
let musicToggles = Object.keys(MusicSelectionPanel).map(category => category.replace(" ", ""));

// Add event listeners to the elements based on the musicToggles array
musicToggles.forEach(toggle => {
    document.getElementById(`${toggle}_collapse_toggle`).addEventListener("click", toggle_collapsible_container);
});
// Utility function to zip two arrays together.
function zipArr(arr1, arr2) {
  return arr1.map((value, index) => [value, arr2[index]]);
}
function toggle_collapsible_container(evt) {
    /**
     * Show or hide a collapsible container.
     *
     * @param {Event} evt - The click event triggered on the toggle element.
     */
    let targetElement = evt.target;

    if (!targetElement.id.includes("collapse_toggle")) {
        // Get the parent of this element if the ID doesn't contain "collapse_toggle"
        targetElement = targetElement.parentElement;
    }

    let toggledElement = targetElement.id.match(/^(.+)_collapse_toggle$/)[1];

    // Open or close the settings table on the Seed Info tab
    let settingsTable = document.getElementById(toggledElement);
    settingsTable.classList.toggle("collapsed");

    // Toggle the arrow direction (flipped state)
    let toggledArrow = `${toggledElement.replace("_", "-")}-expand-arrow`;
    let settingsArrow = document.getElementsByClassName(toggledArrow).item(0);
    settingsArrow.classList.toggle("flipped");
}

function serialize_music_selections(form, for_file = false) {
  // Serialize music selections into an enum-focused JSON object.
  // Flip the Songs Object to be {value: key} instead of {key: value}.
  let MapSongs = Object.keys(Songs).reduce((obj, key) => {
    obj[Songs[key]] = key;
    return obj;
  }, {});
  function get_value(enum_val) {
    // Return either the value of a given enum or the display name.
    return MapSongs[enum_val] || enum_val;
  }

  function is_music_select_input(inputName) {
    // Determine if an input is a song selection input.
    return inputName && inputName.startsWith("music_select_");
  }

  let songs_map = {
    vanilla: {},
    custom: {},
  };

  for (let obj of form) {
    if (!is_music_select_input(obj.name)) {
      continue;
    }

    // Extract the location name using regular expressions.
    let location_name_match = obj.name.match(/^music_select_(.+)$/);
    let location_name = location_name_match ? location_name_match[1] : null;
    if (!location_name) continue;

    let location = get_value(Songs[location_name]);
    if (obj.value !== "") {
      let chosen_song = obj.value;

      // Default values are handled specially.
      if (chosen_song === "default_value") {
        if (for_file) {
          let category = get_music_category(location_name);
          if (is_song_category_randomized(category)) {
            songs_map["vanilla"][location] = get_value(Songs[location_name]);
          }
          continue;
        } else {
          // Assign the appropriate song and continue.
          chosen_song = location_name;
        }
      }

      // If this is an in-game song, use the enum value.
      let chosen_val = Songs[chosen_song];
      if (chosen_val) {
        songs_map["vanilla"][location] = get_value(chosen_val);
      } else{
        // If this is a custom song, find and use the full string path.
        let bgm_map = zipArr(cosmetic_truncated_names.bgm, cosmetic_names.bgm);
        let major_map = zipArr(
          cosmetic_truncated_names.majoritems,
          cosmetic_names.majoritems
        );
        let minor_map = zipArr(
          cosmetic_truncated_names.minoritems,
          cosmetic_names.minoritems
        );
        let event_map = zipArr(
          cosmetic_truncated_names.events,
          cosmetic_names.events
        );
        let music_map = [...bgm_map, ...major_map, ...minor_map, ...event_map];

        for (let [truncated_name, path_name] of music_map) {
          if (chosen_song === truncated_name) {
            let final_path_name = path_name;
            if (for_file) {
              final_path_name = get_serialized_custom_path_name(path_name);
            }
            songs_map["custom"][location] = final_path_name;
            break;
          }
        }
      }
    }
  }

  return songs_map;
}

async function import_music_selections(jsonString) {
  // Import music selections from a JSON string.
  const fileContents = JSON.parse(jsonString);

  // Inform the user their current settings will be erased.
  if (!window.confirm("This will replace your current music selections. Continue?")) {
      return;
  }

  // Ensure this is an actual valid music selections file.
  validate_music_file(fileContents);

  // Update the names of all custom songs to match the currently loaded pack.
  const musicData = update_custom_song_names(fileContents);

  // Reset all of the music selections to their defaults.
  reset_music_selections_no_prompt();

  // Set all of the options specified in the music file.
  for (const [location, songName] of Object.entries(musicData["vanilla"])) {
      const locationElem = document.getElementById(`music_select_${location}`);
      locationElem.value = songName;
  }
  for (const [location, songName] of Object.entries(musicData["custom"])) {
      const locationElem = document.getElementById(`music_select_${location}`);
      // Find the matching select value.
      const category = songName.split("/")[0];
      const customSongList = get_custom_song_map()[category];
      for (const [customSongName, customTruncatedName] of customSongList) {
          if (songName === customSongName) {
              locationElem.value = customTruncatedName;
              break;
          }
      }
  }
}

function validate_music_file(fileContents) {
  // Ensure that the provided music file is valid and not malformed.
  const musicErrorsElement = document.getElementById("music_import_errors");
  musicErrorsElement.style.display = "none";

  for (const [location, song] of Object.entries(fileContents["vanilla"])) {
      validate_music_location(location);
      validate_vanilla_song(song);
  }
  for (const [location, song] of Object.entries(fileContents["custom"])) {
      validate_music_location(location);
      validate_custom_song(song);
  }
}


function is_song_category_randomized(category) {
  /**
   * Return true if this song category is randomized.
   *
   * @param {string} category - The song category name.
   * @returns {boolean} - True if the song category is randomized.
   */
  let categoryCheckbox = document.getElementById(
    `music_${category}_randomized`
  );
  return categoryCheckbox ? categoryCheckbox.checked : false;
}

function get_music_category(songLocation) {
  /**
   * Return the music category for this song location.
   *
   * @param {string} songLocation - The song location name.
   * @returns {string} - The music category for the song location.
   * @throws {Error} - If the songLocation is invalid.
   */
  let locationSelect = document.getElementById(`music_select_${songLocation}`);
  if (!locationSelect) {
    throw new Error(
      `Value ${songLocation} should not be fed as input to get_music_category.`
    );
  }

  const categories = ["BGM", "MajorItem", "MinorItem", "Event"];
  for (let category of categories) {
    if (locationSelect.classList.contains(`${category}-select`)) {
      return category === "BGM"
        ? category.toLowerCase()
        : `${category.toLowerCase()}s`;
    }
  }

  throw new Error(
    `Value ${songLocation} should not be fed as input to get_music_category.`
  );
}
function reset_music_selections_no_prompt() {
  /**
   * Reset all music selection options to their default settings.
   */
  for (let songLocation of SongLocationList) {
    let songElement = document.getElementById(`music_select_${songLocation}`);
    let category = get_music_category(songLocation);

    if (is_song_category_randomized(category)) {
      songElement.value = "";
    } else {
      songElement.value = "default_value";
    }

    songElement.value = ""; // This line will overwrite the previous line
  }
}
document
  .getElementById("export_music_selections")
  .addEventListener("click", function (evt) {
    /**
     * Save the current music selections to a JSON file.
     */
    let form = $("#form").serializeArray(); // Using jQuery to serialize the form data
    let musicSelectData = serialize_music_selections(form, true);
    download_json_file(musicSelectData, "music_selections.json");
  });

document
  .getElementById("reset_music_selections")
  .addEventListener("click", function (evt) {
    /**
     * Reset all music selection options to their default settings.
     * Issues a prompt first, warning the user.
     */
    if (
      window.confirm("Are you sure you want to reset all music selections?")
    ) {
      reset_music_selections_no_prompt();
    }
  });

function is_custom_music_loaded() {
  /**
   * Return true if a custom music pack has been loaded.
   */
  return cosmetic_names !== null;
}

function get_custom_song_map() {
  /**
   * Return a map between song categories and their relevant lists.
   */
  return {
    bgm: zipArr(cosmetic_names.bgm, cosmetic_truncated_names.bgm),
    majoritems: zipArr(
      cosmetic_names.majoritems,
      cosmetic_truncated_names.majoritems
    ),
    minoritems: zipArr(
      cosmetic_names.minoritems,
      cosmetic_truncated_names.minoritems
    ),
    events: zipArr(cosmetic_names.events, cosmetic_truncated_names.events),
  };
}

function update_custom_path_name(pathName, prefix) {
  /**
   * Replace the prefix of a custom path name with a new prefix.
   *
   * @param {string} pathName - The original path name.
   * @param {string} prefix - The new prefix to replace.
   * @returns {string} - The updated path name.
   */
  return `${prefix}/${pathName.split("/").slice(-2).join("/")}`;
}

function get_serialized_custom_path_name(pathName) {
  /**
   * Obtain a path name for a custom song for writing to file.
   *
   * @param {string} pathName - The original path name.
   * @returns {string} - The serialized path name.
   */
  return pathName.split("/").slice(-2).join("/");
}

function get_current_pack_prefix() {
  /**
   * Get the prefix of the currently loaded music pack, if there is one.
   *
   * This will either return the first time one of our lists is non-empty, or it
   * will return null at the very end. It's a silly way to write a function, but
   * jsProxy objects are hard to work with.
   *
   * @returns {string|null} - The prefix of the currently loaded music pack.
   */
  for (let song of cosmetic_names.bgm) {
    return song.split("/").slice(0, -2).join("/");
  }
  for (let song of cosmetic_names.majoritems) {
    return song.split("/").slice(0, -2).join("/");
  }
  for (let song of cosmetic_names.minoritems) {
    return song.split("/").slice(0, -2).join("/");
  }
  for (let song of cosmetic_names.events) {
    return song.split("/").slice(0, -2).join("/");
  }
  // No custom music has been loaded.
  return null;
}

function raise_music_validation_error(errString) {
  /**
   * Raise an error and display a message about an invalid music file.
   *
   * @param {string} errString - The error message to display.
   * @throws {Error} - Throws a JavaScript error with the provided error message.
   */
  let musicErrorsElement = document.getElementById("music_import_errors");
  if (musicErrorsElement) {
    musicErrorsElement.innerText = errString;
    musicErrorsElement.style.display = ""; // Reset the style to display the error message
  }
  throw new Error(errString); // Raises an error in JavaScript
}
function update_custom_song_names(fileContents) {
  /**
   * Update custom music with the name of the newest music zip file.
   *
   * This prevents an issue where the user uploads one music file, saves
   * their selections to file, uploads a music pack with a new name, then
   * tries to import the same file. As long as the songs are in the right
   * place, with the right names, the name of the pack should be irrelevant.
   *
   * @param {Object} fileContents - The contents of the imported file.
   * @returns {Object} - Updated music data with the newest pack prefix.
   */
  let currentPackName = get_current_pack_prefix();
  if (!currentPackName) {
    return fileContents;
  }

  let musicData = {
    vanilla: fileContents["vanilla"],
    custom: {},
  };

  for (let [location, song] of Object.entries(fileContents["custom"])) {
    let pathName = update_custom_path_name(song, currentPackName);
    musicData["custom"][location] = pathName;
  }

  return musicData;
}
function validate_music_location(locationName) {
  /**
   * Ensure that a given location is a valid song location.
   *
   * @param {string} locationName - The location name to validate.
   * @throws {Error} - If the location is invalid.
   */
  try {
    let _ = Songs[locationName];
  } catch (error) {
    let errString = `The music selection file is invalid: "${locationName}" is not a valid song location.`;
    raise_music_validation_error(errString);
  }
}

function validate_custom_song(songPath) {
  /**
   * Ensure that a given song represents a currently loaded custom song.
   *
   * @param {string} songPath - The song path to validate.
   * @throws {Error} - If the custom song is invalid.
   */
  // Check to see if the path is correctly formed.
  let splitPath = songPath.split("/");
  if (splitPath.length !== 2) {
    let errString = `The music selection file is invalid: song name "${songPath}" is malformed.`;
    raise_music_validation_error(errString);
  }

  let [category, songName] = splitPath;

  // Check to see if the path has a valid category.
  if (!["bgm", "majoritems", "minoritems", "events"].includes(category)) {
    let errString = `The music selection file is invalid: song name "${songPath}" has an invalid category "${category}".`;
    raise_music_validation_error(errString);
  }

  // Check to see if any custom music has been loaded.
  if (!is_custom_music_loaded()) {
    let errString = `The music selection file contains custom songs, but no custom songs have been loaded.`;
    raise_music_validation_error(errString);
  }

  // Search for the song in the currently loaded songs.
  let customSongList = get_custom_song_map()[category];
  let songFound = false;
  for (let [loadedSong, _] of customSongList) {
    let loadedSongName = loadedSong.split("/").pop();
    if (songName === loadedSongName) {
      songFound = true;
      break;
    }
  }

  if (!songFound) {
    let errString = `The custom song "${songName}" is not in the currently loaded pack.`;
    raise_music_validation_error(errString);
  }
}
async function music_selection_filebox() {
  // load pyodide
  let input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";

  input.onchange = async (e) => {
    let file = e.target.files[0];
    let json_text = await file.text();
    let imported_music_json = json_text;
    import_music_selections(imported_music_json);
  };

  input.click();
}
function validate_vanilla_song(songName) {
  /**
   * Ensure that a given song represents a valid song from the base game.
   *
   * @param {string} songName - The song name to validate.
   * @throws {Error} - If the song is invalid.
   */
  try {
    let _ = Songs[songName];
  } catch (error) {
    let errString = `The music selection file is invalid: "${songName}" is not a valid song name.`;
    raise_music_validation_error(errString);
  }
}
