// NOTE: pyodide_functions.js is NOT currently loaded, some functions will fail
var jquery = $;
$.ajax({
  url: "/get_selector_info",
  dataType: "json",
  async: false,
  success: function (data) {
    var env = nunjucks.configure('/templates', { autoescape: true });
    env.addFilter("music_select_restrict", function(songList, location) {
        return songList;
    });
    env.addFilter("plando_custom_loc_restrict", function(locationList, locationId) {
        return locationList;
    });
    env.addFilter("plando_custom_loc_item_restrict", PlandoCustomLocationItemFilter);
    env.addFilter("plando_item_restrict", function(itemList, location) {
        return itemList;
    });
    env.addFilter("plando_minigame_restrict", PlandoMinigameFilter);
    env.addFilter("plando_shop_sort", PlandoShopSortFilter);
    env.addGlobal("plando_option_class_annotation", PlandoOptionClassAnnotation);
    var renderedHTML = env.render("base.html.jinja2", data);
    var navRenderedHTML = env.render("nav-tabs.html.jinja2", {});
    $("#tab-data").html(renderedHTML);
    $("#nav-tab-list").html(navRenderedHTML);
  },
});
// Initialize arrays for listeners, progression presets, and random settings presets
const listeners = [];
const progression_presets = [];
const random_settings_presets = [];

// Determine the correct URL for fetching presets based on the hostname
let presets_url;
if (location.hostname === "dev.dk64randomizer.com") {
  presets_url =
    "https://dev-generate.dk64rando.com/get_presets?return_blank=true";
} else if (location.hostname === "dk64randomizer.com") {
  presets_url = "https://generate.dk64rando.com/get_presets?return_blank=true";
} else {
  presets_url = `${location.origin}/get_presets?return_blank=true`;
}

// Use fetch to get the presets and populate progression_presets and random_settings_presets
$.ajax({
  url: presets_url,
  dataType: "json",
  async: false,
  success: function (data) {
    data.forEach((file) => {
      progression_presets.push(file);
    });
  },
});
$.ajax({
  url: "static/presets/weights/weights_files.json",
  dataType: "json",
  async: false,
  success: function (data) {
    data.forEach((file) => {
      random_settings_presets.push(file);
    });
  },
});

$.ajax({
  url: "./static/patches/pointer_addresses.json",
  dataType: "json",
  async: false,
  success: function (data) {
    pointer_addresses = data;
  },
});

$.ajax({
  url: "./static/patches/symbols.json",
  dataType: "json",
  async: false,
  success: function (data) {
    rom_symbols = data;
  },
});

let user_agent = navigator.userAgent;
if (window.location.protocol != "https:") {
  if (location.hostname != "localhost" && location.hostname != "127.0.0.1") {
    location.href = location.href.replace("http://", "https://");
  }
}

// if the domain is not the main domain, hide dev site warnings and features
if (location.hostname == "dk64randomizer.com") {
  document.getElementById("spoiler_warning_1").style.display = "none";
  document.getElementById("spoiler_warning_2").style.background = "";
  document.getElementById("spoiler_warning_3").style.display = "none";
  document.getElementById("spoiler_warning_4").style.display = "none";
  document.getElementById("plandomizer_container").style.display = "none";
}
if (location.hostname != "localhost") {
  document.getElementById("plando_string_section").style.display = "none";
}

function decrypt_settings_string_enum(settings_string) {
  // fetch the web endpoint /convert_settings_string using ajax syncronously
  var response = $.ajax({
    type: "POST",
    url: "/convert_settings_string",
    data: JSON.stringify({ settings_string: settings_string }),
    contentType: "application/json",
    async: false,
  }).responseText;
  // Convert the json response to a string
  var settings = JSON.parse(response);
  return settings;
}

function encrypt_settings_string_enum(settings) {
  // fetch the web endpoint /convert_settings_string using ajax syncronously
  var response = $.ajax({
    type: "POST",
    url: "/convert_settings_enum",
    data: JSON.stringify({ settings_json: settings }),
    contentType: "application/json",
    async: false,
  }).responseText;
  // Convert the json response to a string
  var set = JSON.parse(response);
  var settings_string = set["settings_string"];
  return settings_string;
}

async function try_to_load_from_args() {
  /** Get the args from the URL and then load the seed from the server if it exists. */

  let args = window.location.search;
  if (args.startsWith("?")) {
    args = args.substring(1);
  }

  // Split arguments by "&"
  let argsArray = args.includes("&") ? args.split("&") : [args];
  let argsDict = {};

  // Populate argsDict with key-value pairs
  argsArray.forEach((arg) => {
    try {
      let [key, value] = arg.split("=");
      argsDict[key] = value;
    } catch (e) {
      // Continue silently on error
    }
  });

  // If "seed_id" is provided in the URL, fetch seed data from the server
  if ("seed_id" in argsDict) {
    console.log("Getting the seed from the server");

    let resp = await getSeedFromServer(argsDict["seed_id"]);

    // Assuming patchingResponse is available globally as an async function
    await patchingResponse(String(resp), false);
  }

  // Update the DOM: hide visual indicator and show tab-data
  document.getElementById("visual_indicator").setAttribute("hidden", "true");
  document.getElementById("tab-data").removeAttribute("hidden");
}

// Sleep function to run functions after X seconds
async function sleep(seconds, func, args) {
  setTimeout(function () {
    func(...args);
  }, seconds * 1000);
}
function save_text_as_file(text, file) {
  var blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  saveAs(blob, file);
}

window.onerror = function (error) {
  banned_errors_text = [
    '"undefined" is not valid JSON', // Loading up the site without any cookies
    "Unexpected non-whitespace character after JSON at position", // Loading up the site when your cookies reflect a prior version
    "Unexpected non-whitespace character after JSON data at line", // Same as above
    "Unexpected token ; in JSON", // Token Error
    "Uncaught Error: Invalid Rom", // Token Error
  ];
  is_banned = false;
  banned_errors_text.forEach((item) => {
    if (error.toString().toLowerCase().indexOf(item.toLowerCase()) > -1) {
      is_banned = true;
    }
  });
  if (!is_banned) {
    toast_alert(error.toString());
  }
};
function toast_alert(text) {
  try {
    _LTracker.push({ text: text, agent: user_agent });
  } catch {}
  generateToast(text, true);
}
function getFile(file) {
  return $.ajax({
    type: "GET",
    url: file,
    async: false,
  }).responseText;
}

var valid_extensions = [".bin", ".candy"];

function validFilename(filename, dir, valid_extension = null) {
  if (filename.includes(dir)) {
    if (valid_extension == null) {
      for (let v = 0; v < valid_extensions.length; v++) {
        var ext = valid_extensions[v];
        if (filename.slice(0 - ext.length) == ext) {
          return true;
        }
      }
    } else {
      if (filename.slice(0 - valid_extension.length) == valid_extension) {
        return true;
      }
    }
  }
  return false;
}

function filterFilename(filename) {
  for (let v = 0; v < valid_extensions.length; v++) {
    var ext = valid_extensions[v];
    if (filename.slice(0 - ext.length) == ext) {
      return {
        file: filename.slice(0, 0 - ext.length),
        extension: ext,
      };
    }
  }
  return {
    file: filename,
    extension: 0,
  };
}

function createMusicLoadPromise(jszip, filename) {
  return new Promise((resolve, reject) => {
    jszip
      .file(filename)
      .async("Uint8Array")
      .then(function (content) {
        resolve({
          name: filterFilename(filename).file,
          file: content,
          extension: filterFilename(filename).extension,
        });
      });
  });
}

function sortLoadedMusic(musicList) {
  musicList.sort((a, b) => {
    aName = a.name.toUpperCase();
    bName = b.name.toUpperCase();
    if (aName < bName) {
      return -1;
    } else if (aName > bName) {
      return 1;
    } else {
      return 0;
    }
  });
}
var current_seed_data;
var cosmetics;
var cosmetic_names;
var cosmetic_extensions;
var cosmetic_truncated_names = {
  bgm: [],
  majoritems: [],
  minoritems: [],
  events: [],
};

function load_music_file_from_db() {
  console.log("Trying to load file from DB");
  try {
    // If we actually have a file in the DB load it
    var db = musicdatabase.result;
    var tx = db.transaction("MusicStorage", "readwrite");
    var store = tx.objectStore("MusicStorage");

    // Get our music file
    var getMusicFile = store.get("music");
    getMusicFile.onsuccess = function () {
      console.log("Successfully loaded file from DB");
      // When we pull it from the DB load it in as a global var
      try {
        cosmetic_pack_event(getMusicFile.result.value, true);
        $("#music_file_text").attr("placeholder", "Using cached music file");
        $("#music_file_text").val("Using cached music file");
      } catch (error) {
        console.log("Error loading music file from the database:", error);
      }
    };
  } catch (error) {
    console.log("Error accessing the music database:", error);
  }
}

function music_filebox() {
  var input = document.createElement("input");
  input.type = "file";
  input.accept = ".zip";

  input.onchange = (e) => {
    var file = e.target.files[0];
    $("#music_file_text").attr("placeholder", file.name);
    $("#music_file_text").val(file.name);
    // Get the original file
    try {
      var db = musicdatabase.result;
      var tx = db.transaction("MusicStorage", "readwrite");
      var store = tx.objectStore("MusicStorage");
      // Store it in the database
      store.put({ music: "music", value: file });
      console.log("Successfully stored file in the database.");
    } catch (error) {
      console.log("Error storing file in the database:", error);
    }
    // Make sure we load the file into the rompatcher
    cosmetic_pack_event(file);
  };

  input.click();
}

function cosmetic_pack_event(fileToLoad, isInitialLoad = false) {
  var fileReader = new FileReader();
  fileReader.onload = function (fileLoadedEvent) {
    var new_zip = new JSZip();
    new_zip.loadAsync(fileLoadedEvent.target.result).then(async function () {
      let bgm_promises = [];
      let majoritem_promises = [];
      let minoritem_promises = [];
      let event_promises = [];
      let transition_promises = [];
      let portal_promises = [];
      let painting_promises = [];

      for (var filename of Object.keys(new_zip.files)) {
        if (validFilename(filename, "bgm/")) {
          bgm_promises.push(createMusicLoadPromise(new_zip, filename));
        } else if (validFilename(filename, "majoritems/")) {
          majoritem_promises.push(createMusicLoadPromise(new_zip, filename));
        } else if (validFilename(filename, "minoritems/")) {
          minoritem_promises.push(createMusicLoadPromise(new_zip, filename));
        } else if (validFilename(filename, "events/")) {
          event_promises.push(createMusicLoadPromise(new_zip, filename));
        } else if (validFilename(filename, "textures/transitions/", ".png")) {
          transition_promises.push(createMusicLoadPromise(new_zip, filename));
        } else if (validFilename(filename, "textures/tns_portal/", ".png")) {
          portal_promises.push(createMusicLoadPromise(new_zip, filename))
        } else if (validFilename(filename, "textures/paintings/", ".png")) {
          painting_promises.push(createMusicLoadPromise(new_zip, filename))
        }
      }

      let bgm_files = await Promise.all(bgm_promises);
      sortLoadedMusic(bgm_files);
      let majoritem_files = await Promise.all(majoritem_promises);
      sortLoadedMusic(majoritem_files);
      let minoritem_files = await Promise.all(minoritem_promises);
      sortLoadedMusic(minoritem_files);
      let event_files = await Promise.all(event_promises);
      sortLoadedMusic(event_files);
      let transition_files = await Promise.all(transition_promises);
      let portal_files = await Promise.all(portal_promises);
      let painting_files = await Promise.all(painting_promises);

      // BGM
      let bgm = bgm_files.map((x) => x.file);
      let bgm_names = bgm_files.map((x) => x.name);
      let bgm_ext = bgm_files.map((x) => x.extension);

      // Major Items
      let majoritems = majoritem_files.map((x) => x.file);
      let majoritem_names = majoritem_files.map((x) => x.name);
      let majoritem_ext = majoritem_files.map((x) => x.extension);

      // Minor Items
      let minoritems = minoritem_files.map((x) => x.file);
      let minoritem_names = minoritem_files.map((x) => x.name);
      let minoritem_ext = minoritem_files.map((x) => x.extension);

      // Events
      let events = event_files.map((x) => x.file);
      let event_names = event_files.map((x) => x.name);
      let event_ext = event_files.map((x) => x.extension);

      // Transitions
      let transitions = transition_files.map((x) => x.file);
      let transition_names = transition_files.map((x) => x.name);

      // T&S Portals
      let tns_portals = portal_files.map((x) => x.file);
      let tns_portal_names = portal_files.map((x) => x.name);
      
      // Paintings
      let paintings = painting_files.map((x) => x.file);
      let painting_names = painting_files.map((x) => x.name);

      cosmetics = {
        bgm: bgm,
        majoritems: majoritems,
        minoritems: minoritems,
        events: events,
        transitions: transitions,
        tns_portals: tns_portals,
        paintings: paintings,
      };
      cosmetic_names = {
        bgm: bgm_names,
        majoritems: majoritem_names,
        minoritems: minoritem_names,
        events: event_names,
        transitions: transition_names,
        tns_portals: tns_portal_names,
        paintings: painting_names,
      };
      cosmetic_extensions = {
        bgm: bgm_ext,
        majoritems: majoritem_ext,
        minoritems: minoritem_ext,
        events: event_ext,
      };

      update_music_select_options(isInitialLoad);
    });
  };

  fileReader.readAsArrayBuffer(fileToLoad);
}

function get_truncated_song_name(songName) {
  return songName.replaceAll(/[^A-Za-z0-9]/g, "");
}

function get_custom_song_display_name(songName) {
  let splitName = songName.split("/");
  let trimmedName = splitName[splitName.length - 1];
  return `Custom Song: ${trimmedName}`;
}

async function update_music_select_options(isInitialLoad) {
  customSongDict = {
    BGM: cosmetic_names.bgm,
    MajorItem: cosmetic_names.majoritems,
    MinorItem: cosmetic_names.minoritems,
    Event: cosmetic_names.events,
  };
  cosmetic_truncated_names = {
    bgm: [],
    majoritems: [],
    minoritems: [],
    events: [],
  };
  for (const [category, songs] of Object.entries(customSongDict)) {
    // Map each song's truncated name to its full string path.
    for (const song of songs) {
      if (category === "BGM") {
        cosmetic_truncated_names.bgm.push(get_truncated_song_name(song));
      } else if (category === "MajorItem") {
        cosmetic_truncated_names.majoritems.push(get_truncated_song_name(song));
      } else if (category === "MinorItem") {
        cosmetic_truncated_names.minoritems.push(get_truncated_song_name(song));
      } else {
        cosmetic_truncated_names.events.push(get_truncated_song_name(song));
      }
    }

    const dropdowns = document.getElementsByClassName(`${category}-select`);
    for (const dropdown of dropdowns) {
      // Remove any existing custom music options from this dropdown.
      for (let i = dropdown.options.length - 1; i >= 0; i--) {
        const option = dropdown.options.item(i);
        if (option.classList.contains("custom-song")) {
          if (dropdown.value == option.value) {
            dropdown.value = "";
          }
          dropdown.remove(i);
        } else {
          // We can safely break here, because all of the custom songs are
          // guaranteed to be at the end of each dropdown. This speeds the
          // process up considerably.
          break;
        }
      }
      // Add new custom music options to this dropdown.
      for (const song of songs) {
        const opt = document.createElement("option");
        opt.value = get_truncated_song_name(song);
        opt.innerHTML = get_custom_song_display_name(song);
        opt.classList.add("custom-song");
        dropdown.appendChild(opt);
      }
    }
  }

  // If this is the initial load, we want to read from the database and restore
  // custom song selections.
  if (isInitialLoad) {
    let musicDb = await loadDataFromIndexedDB("saved_music");
    let musicDbContents = JSON.parse(musicDb);
    for (const [selectName, selectValue] of Object.entries(musicDbContents)) {
      selectElem = document.getElementById(selectName);
      selectElem.value = selectValue;
    }
  }
}

jq = $;

function savesettings() {
  var disabled = $("form").find(":input:disabled").removeAttr("disabled");
  data = new FormData(document.querySelector("form"));
  disabled.attr("disabled", "disabled");
  json = Object.fromEntries(data.entries());
  for (element of document.getElementsByTagName("select")) {
    if (element.className.includes("selected")) {
      length = element.options.length;
      values = [];
      for (let i = 0; i < length; i++) {
        if (element.options.item(i).selected) {
          values.push(element.options.item(i).value);
        }
      }
      json[element.name] = values;
    }
  }
  var starting_move_box_buttons = $(
    ":input[name^='starting_move_box_']:checked"
  );
  for (element of starting_move_box_buttons) {
    if (element.id.includes("start")) {
      json[element.name] = "start";
    } else if (element.id.includes("random")) {
      json[element.name] = "random";
    }
  }
  saveDataToIndexedDB("saved_settings", JSON.stringify(json));
}

// Music settings have to be saved separately, because the value we're trying
// to load may not exist on the page when load_data() is called.
function savemusicsettings() {
  music_json = {};
  for (element of document.getElementsByTagName("select")) {
    if (element.id.startsWith("music_select_")) {
      music_json[element.id] = element.value;
    }
  }
  saveDataToIndexedDB("saved_music", JSON.stringify(music_json));
}

$("#form input").on("input change", function (e) {
  //This would be called if any of the input elements receive a change inside the form
  savesettings();
});
$("#form select").on("change", function (e) {
  //This would be called if any of the select elements receive a change inside the form
  savesettings();
  savemusicsettings();
});

function filebox() {
  var input = document.createElement("input");
  input.type = "file";
  input.accept = ".z64,.n64,.v64";

  input.onchange = (e) => {
    var file = e.target.files[0];
    $("#rom").attr("placeholder", file.name);
    $("#rom").val(file.name);
    $("#rom_2").val(file.name);
    $("#rom_2").attr("placeholder", file.name);
    $("#rom_3").val(file.name);
    $("#rom_3").attr("placeholder", file.name);
    // Get the original fiile
    try {
      var db = romdatabase.result;
      var tx = db.transaction("ROMStorage", "readwrite");
      var store = tx.objectStore("ROMStorage");
      // Store it in the database
      store.put({ ROM: "N64", value: file });
    } catch {}
    // Make sure we load the file into the rompatcher
    romFile = new MarcFile(file, _parseROM);
  };

  input.click();
}

// This works on all devices/browsers, and uses IndexedDBShim as a final fallback
var indexedDB =
  window.indexedDB ||
  window.mozIndexedDB ||
  window.webkitIndexedDB ||
  window.msIndexedDB ||
  window.shimIndexedDB;

// Open (or create) the database
var seeddatabase = indexedDB.open("SeedStorage", 1);
var settingsdatabase = indexedDB.open("SettingsDB", 1);
var musicdatabase = indexedDB.open("MusicStorage", 1);
var romdatabase = indexedDB.open("ROMStorage", 1);

musicdatabase.onupgradeneeded = function () {
  try {
    var musicdb = musicdatabase.result;
    musicdb.createObjectStore("MusicStorage", { keyPath: "music" });
  } catch {}
};
musicdatabase.onsuccess = function () {
  load_music_file_from_db();
};
settingsdatabase.onupgradeneeded = function () {
  try {
    var settingsdb = settingsdatabase.result;
    settingsdb.createObjectStore("saved_settings");
  } catch {}
};
settingsdatabase.onsuccess = function () {
  load_data();
};
// Create the schema
romdatabase.onupgradeneeded = function () {
  try {
    var db = romdatabase.result;
    db.createObjectStore("ROMStorage", { keyPath: "ROM" });
  } catch {}
};

seeddatabase.onupgradeneeded = function () {
  try {
    var seed_db = seeddatabase.result;
    seed_db.createObjectStore("SeedStorage", {
      keyPath: "id",
    });
  } catch {}
};

seeddatabase.onsuccess = function () {
  load_old_seeds();
};

romdatabase.onsuccess = function () {
  load_file_from_db();
};

function write_seed_history(seed_id, seed_data, seed_hash) {
  // Get the original fiile
  try {
    var seed_db = seeddatabase.result;
    var seed_tx = seed_db.transaction("SeedStorage", "readwrite");
    var seed_store = seed_tx.objectStore("SeedStorage");
    // Store it in the database
    const now = new Date();
    seed_store.put({
      id: Math.random(),
      value: seed_data,
      hash: seed_hash,
      seed_id: seed_id,
      date: now,
    });
    // Write it to most_recent_seed_id and most_recent_seed_date on the UI page so we can display it
    document.getElementById("most_recent_seed_id").innerHTML =
      "<strong>Most Recent Seed ID:</strong> " + seed_id;
    document.getElementById("most_recent_seed_date").innerHTML =
      "<strong>Most Recent Seed Date:</strong> " +
      now.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
  } catch (error) {
    console.log(error);
  }
}

function load_old_seeds() {
  try {
    // If we actually have a file in the DB load it
    var seed_db = seeddatabase.result;
    var seed_tx = seed_db.transaction("SeedStorage", "readwrite");
    var seed_store = seed_tx.objectStore("SeedStorage");

    var all_seeds = seed_store.getAll();
    all_seeds.onsuccess = function () {
      try {
        const hook = document.getElementById("pastgenlist");
        hook.innerHTML = "";
        var arrayLength = all_seeds.result.length;
        var sorted_array = all_seeds.result;
        sorted_array.sort(function (a, b) {
          return new Date(b.date) - new Date(a.date);
        });
        for (var i = 0; i < arrayLength; i++) {
          if (sorted_array[i].date == undefined) {
            seed_store.delete(sorted_array[i].id);
          }
          if (i > 10) {
            seed_store.delete(sorted_array[i].id);
          }
          document.getElementById("nav-pastgen-tab").style.display = "block";
          const hook = document.getElementById("pastgenlist");
          const option_el = document.createElement("option");
          const option_dt = sorted_array[i].date.toLocaleDateString(undefined, {
            year: "numeric",
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          });
          const option_str =
            option_dt + " (Seed: " + sorted_array[i].seed_id + ")";
          const option_txt = document.createTextNode(option_str);
          option_el.appendChild(option_txt);
          option_el.lanky_data = sorted_array[i].value;
          hook.appendChild(option_el);
        }
        // Write the most recent seed to the UI
        document.getElementById("most_recent_seed_id").innerHTML =
          "<strong>Most Recent Seed ID:</strong> " + sorted_array[0].seed_id;
        document.getElementById("most_recent_seed_date").innerHTML =
          "<strong>Most Recent Seed Date:</strong> " +
          sorted_array[0].date.toLocaleDateString(undefined, {
            year: "numeric",
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          });
      } catch {}
    };
  } catch {}
}

function get_previous_seed_data() {
  var sel = document.getElementById("pastgenlist");
  var text = sel.options[sel.selectedIndex].lanky_data;
  return text;
}
function load_file_from_db() {
  try {
    // If we actually have a file in the DB load it
    var db = romdatabase.result;
    var tx = db.transaction("ROMStorage", "readwrite");
    var store = tx.objectStore("ROMStorage");

    // Get our ROM file
    var getROM = store.get("N64");
    getROM.onsuccess = function () {
      // When we pull it from the DB load it in as a global var
      try {
        romFile = new MarcFile(getROM.result.value, _parseROM);
        $("#rom").attr("placeholder", "Using cached ROM");
        $("#rom").val("Using cached ROM");
        $("#rom_2").attr("placeholder", "Using cached ROM");
        $("#rom_3").attr("placeholder", "Using cached ROM");
        $("#rom_3").val("Using cached ROM");

        try_to_load_from_args();
      } catch {
        try_to_load_from_args();
      }
    };
  } catch {
    try_to_load_from_args();
  }
}
var w;
var CurrentRomHash;

243;

function base64ToArrayBuffer(base64) {
  var binaryString = atob(base64);
  var bytes = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

function to2Digit(value) {
  if (value >= 10) {
    return value;
  }
  return `0${value}`;
}

gen_error_count = 0;
previous_queue_position = null;

function pushToHistory(message, emphasize = false) {
  let prog_hist = document.getElementById("progress-history");
  old_history = prog_hist.innerHTML;
  dt = new Date();
  emph_start = "";
  emph_end = "";
  if (emphasize) {
    emph_start = "<span style='font-size:21px'>";
    emph_end = "</span>";
  }
  new_history = `${old_history}${emph_start}[${to2Digit(
    dt.getHours()
  )}:${to2Digit(dt.getMinutes())}:${to2Digit(
    dt.getSeconds()
  )}] ${message}${emph_end}<br />`;
  prog_hist.innerHTML = new_history;
  prog_hist.scrollTop = prog_hist.scrollHeight;
}

function postToastMessage(message, is_warning, progress_ratio) {
  // Write Toast
  $("#progress-text").text(message);
  pushToHistory(message);
  // Handle Progress Bar
  perc = Math.floor(100 * progress_ratio);
  if (is_warning) {
    document.getElementById("progress-fairy").style.display = "none";
    img_data = document.getElementById("progress-dead").src;
    document.getElementById("progress-dead").style.display = "";
    document.getElementById("progress-dead").src = "";
    document.getElementById("progress-dead").src = img_data;
    setTimeout(() => {
      document.getElementById("progress-dead").style.display = "none";
    }, 1000);
    gen_error_count += 1;
    if (gen_error_count >= 3) {
      pushToHistory(
        `You have failed generation ${gen_error_count} times. We would highly advise you report this as a bug to the developers at <a href='discord.dk64randomizer.com' class='no-decoration'>the discord</a> or <a href='https://github.com/2dos/DK64-Randomizer/issues/new' class='no-decoration'>GitHub</a>`,
        true
      );
    }
    document.getElementById("close-modal").style.display = "";
    document.getElementById("close-modal-btn").addEventListener("click", () => {
      hideModal();
    });
  } else {
    document.getElementById("progress-fairy").style.display = "";
    document.getElementById("progress-dead").style.display = "none";
    $("#patchprogress").width(`${perc}%`);
    document.getElementById("close-modal").style.display = "none";
  }
}

function hideModal() {
  $("#progressmodal").modal("hide");
  postToastMessage("Initializing", false, 0);
  document.getElementById("progress-history").innerHTML = "";
  previous_queue_position = null;
}

function wipeToastHistory() {
  document.getElementById("progress-history").innerHTML = "";
  previous_queue_position = null;
}

function generate_seed(url, json, git_branch) {
  $.ajax(url, {
    data: JSON.stringify({
      branch: git_branch,
      post_body: json,
    }),
    contentType: "application/json",
    type: "POST",
    success: function (data, textStatus, xhr) {
      if (xhr.status == 202) {
        console.log("seed gen waiting in queue");
        // Get the position in the queue
        position = data["position"];
        if (position != previous_queue_position) {
          postToastMessage("Position in Queue: " + position, false, 0.4);
          if (position == 0) {
            postToastMessage("Your seed is now generating.");
          }
        }
        previous_queue_position = position;
        setTimeout(function () {
          generate_seed(url, json, git_branch);
        }, 5000);
      } else if (xhr.status == 201) {
        console.log("seed gen queued");
        postToastMessage("Seed Generation Queued", false, 0.3);
        setTimeout(function () {
          generate_seed(url, json, git_branch);
        }, 5000);
      } else if (xhr.status == 208) {
        console.log(data);
        postToastMessage(data, true, 1);
      } else {
        postToastMessage(
          "Seed Generation Complete, applying cosmetics",
          false,
          0.8
        );
        apply_patch(data, true);
      }
    },
    error: function (data, textStatus, xhr) {
      postToastMessage("Something went wrong please try again", true, 1);
    },
  });
}

// if the tab is set to seed info get the generate_seed button and change the text to "Download Seed" we want to check this on every nav tab change
function check_seed_info_tab() {
  if (
    document.getElementById("nav-settings-tab").classList.contains("active")
  ) {
    document.getElementById("generate_seed").value = "Download Seed";
    document.getElementById("generate_seed").onclick = null;
    document.getElementById("generate_seed").onclick = function () {
      apply_download();
    };
  } else {
    // if document.getElementById("download_patch_file").checked set it to Generate Patch File
    if (document.getElementById("download_patch_file").checked) {
      document.getElementById("generate_seed").value = "Generate Patch File";
    } else {
      document.getElementById("generate_seed").value = "Generate Seed";
    }
    // Remove the onclick event
    document.getElementById("generate_seed").onclick = null;
    document.getElementById("generate_seed").onclick = function () {
      document.getElementById("trigger_download_event").click();
    };
  }
}
function toggleDelayedSpoilerLogInput() {
  var generateSpoilerLogCheckbox = document.getElementById(
    "delayed_spoilerlog_container"
  );
  if (!document.getElementById("generate_spoilerlog").checked) {
    generateSpoilerLogCheckbox.removeAttribute("hidden");
  } else {
    generateSpoilerLogCheckbox.setAttribute("hidden", "");
  }
}

// Call the function on page load to set the initial state
toggleDelayedSpoilerLogInput();
// check on any button with the nav-item class is clicked
document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    check_seed_info_tab();
  });
});
check_seed_info_tab();

function saveDataToIndexedDB(key, value) {
  try {
    var settingsdb = settingsdatabase.result;
    transaction = settingsdb.transaction("saved_settings", "readwrite");
    objectStore = transaction.objectStore("saved_settings");
    objectStore.put(value, key);
  } catch {}
}

function loadDataFromIndexedDB(key) {
  return new Promise((resolve, reject) => {
    try {
      var settingsdb = settingsdatabase.result;
      transaction = settingsdb.transaction("saved_settings", "readonly");
      objectStore = transaction.objectStore("saved_settings");
      request = objectStore.get(key);
      request.onerror = function (event) {
        reject("Transaction error: " + event.target.errorCode);
      };

      request.onsuccess = function (event) {
        value = event.target.result;
        resolve(value);
      };
    } catch {
      reject("Read Error");
    }
  });
}

function unlock_spoiler_log(hash) {
  console.log("Unlocking spoiler log");
  // GET to localhost:8000/get_spoiler_log with the args hash with search_query as the value
  // Get the website location
  if (window.location.hostname == "dev.dk64randomizer.com") {
    var url = "https://dev-generate.dk64rando.com/get_spoiler_log";
  } else if (window.location.hostname == "dk64randomizer.com") {
    var url = "https://generate.dk64rando.com/get_spoiler_log";
  } else {
    var url = "http://localhost:8000/get_spoiler_log";
  }
  $.ajax({
    url: url,
    type: "GET",
    data: {
      hash: hash,
    },
    success: function (data, textStatus, xhr) {
      if (xhr.status === 200) {
        console.log("Success");
        save_text_as_file(
          JSON.stringify(data, null, 2),
          document.getElementById("generated_seed_id").innerHTML +
            "-spoilerlog.json"
        );
      } else if (xhr.status === 425) {
        console.log("Not unlocked yet");
        // set the contents of spoiler_log_download_messages to "The spoiler log is not unlocked yet."
        document.getElementById("spoiler_log_download_messages").innerHTML =
          "The spoiler log is not unlocked yet.";
        // display download_modal
        $("#download_modal").modal("show");
        // hide the modal after 5 seconds
        setTimeout(function () {
          $("#download_modal").modal("hide");
        }, 5000);
      } else {
        console.log("Spoiler log is no longer available");
        // set the contents of spoiler_log_download_messages to "The spoiler log is no longer available."
        document.getElementById("spoiler_log_download_messages").innerHTML =
          "The spoiler log is no longer available.";
        // display download_modal
        $("#download_modal").modal("show");
        // hide the modal after 5 seconds
        setTimeout(function () {
          $("#download_modal").modal("hide");
        }, 5000);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log("Error:", errorThrown);
      // set the contents of spoiler_log_download_messages to "There was an error downloading the spoiler log."
      document.getElementById("spoiler_log_download_messages").innerHTML =
        "There was an error downloading the spoiler log.";
      // display download_modal
      $("#download_modal").modal("show");
      // hide the modal after 5 seconds
      setTimeout(function () {
        $("#download_modal").modal("hide");
      }, 5000);
    },
  });
}

function get_seed_from_server(hash) {
  // GET to localhost:8000/get_spoiler_log with the args hash with search_query as the value
  // Get the website location
  if (window.location.hostname == "dev.dk64randomizer.com") {
    var url = "https://dev-generate.dk64rando.com/get_seed";
  } else if (window.location.hostname == "dk64randomizer.com") {
    var url = "https://generate.dk64rando.com/get_seed";
  } else {
    var url = "http://localhost:8000/get_seed";
  }
  // Make the ajax call synchronously
  return_data = $.ajax({
    url: url,
    async: false,
    type: "GET",
    data: {
      hash: hash,
    },
    success: function (data, textStatus, xhr) {
      if (xhr.status === 200) {
        return data;
      } else {
        document.getElementById("spoiler_log_download_messages").innerHTML =
          "Seed is no longer available.";
        // display download_modal
        $("#download_modal").modal("show");
        // hide the modal after 5 seconds
        setTimeout(function () {
          $("#download_modal").modal("hide");
        }, 5000);
        return_data = "Seed is no longer available.";
        return return_data;
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log("Error:", errorThrown);
      document.getElementById("spoiler_log_download_messages").innerHTML =
        "There was an error downloading the seed.";
      // display download_modal
      $("#download_modal").modal("show");
      // hide the modal after 5 seconds
      setTimeout(function () {
        $("#download_modal").modal("hide");
      }, 5000);
      return_data = "There was an error downloading the seed.";
      return return_data;
    },
  });
  // wait for the ajax call to finish
  while (return_data.readyState != 4) {
    sleep(1);
  }
  return return_data.responseText;
}

function should_reset_select_on_preset(selectElement) {
  /** Return true if the element should be reset when applying a preset. */
  if (document.querySelector("#nav-cosmetics").contains(selectElement)) {
    return false;
  }
  if (document.querySelector("#nav-music").contains(selectElement) === true) {
    return false;
  }
  if (selectElement.name.startsWith("plando_")) {
    return false;
  }
  // This should now be obsolete, because of the #nav-music clause
  if (selectElement.name.startsWith("music_select_")) {
    return false;
  }
  if (selectElement.id === "random-weights") {
    return false;
  }
  return true;
}

// Bind click event for "apply_preset"
function preset_select_changed(event) {
  /** Trigger a change of the form via the JSON templates. */
  console.log("PRESET CHANGED");
  const element = document.getElementById("presets");
  let presets = null;

  for (const val of progression_presets) {
    if (val.name === element.value) {
      presets = val;
    }
  }

  if (presets && "settings_string" in presets) {
    // Pass in setting string
    generateToast(
      `"${presets.name}" preset applied.<br />All non-cosmetic settings have been overwritten.`
    );
    const settings = decrypt_settings_string_enum(presets.settings_string);

    for (const select of document.getElementsByTagName("select")) {
      if (should_reset_select_on_preset(select)) {
        select.selectedIndex = -1;
      }
    }

    // Uncheck all starting move radio buttons for the import to then set them correctly
    for (const starting_move_button of document.querySelectorAll(
      "input[name^='starting_move_box_']"
    )) {
      starting_move_button.checked = false;
    }

    document.getElementById("presets").selectedIndex = 0;

    for (const key in settings) {
      try {
        if (typeof settings[key] === "boolean") {
          const checked = settings[key] ? true : false;
          document.querySelector(`#${key}`).checked = checked;
          document.getElementsByName(key)[0].checked = checked;
          document.querySelector(`#${key}`).removeAttribute("disabled");
        } else if (Array.isArray(settings[key])) {
          if (
            [
              "starting_move_list_selected",
              "random_starting_move_list_selected",
            ].includes(key)
          ) {
            for (const item of settings[key]) {
              const radio_buttons = document.getElementsByName(
                `starting_move_box_${parseInt(item)}`
              );
              if (key === "starting_move_list_selected") {
                radio_buttons.find((button) =>
                  button.id.startsWith("start")
                ).checked = true;
              } else {
                radio_buttons.find((button) =>
                  button.id.startsWith("random")
                ).checked = true;
              }
            }
            continue;
          }

          const selector = document.getElementById(key);
          if (selector.tagName === "SELECT") {
            for (const item of settings[key]) {
              for (const option of selector.options) {
                if (option.value === item.name) {
                  option.selected = true;
                }
              }
            }
          }
        } else {
          const selector = document.getElementById(key);
          if (selector.tagName === "SELECT") {
            for (const option of selector.options) {
              // TODO: SETTINGSMAP DOSEN'T FRICKING EXIST YET
              if (option.value === SettingsMap[key](settings[key]).name) {
                option.selected = true;
                break;
              }
            }
          } else {
            document.querySelector(`#${key}`).value = settings[key];
          }
          document.querySelector(`#${key}`).removeAttribute("disabled");
        }
      } catch (e) {
        console.error(e);
      }
    }
  } else {
    for (const key in presets) {
      try {
        if (typeof presets[key] === "boolean") {
          const checked = presets[key] ? true : false;
          document.querySelector(`#${key}`).checked = checked;
          document.getElementsByName(key)[0].checked = checked;
          document.querySelector(`#${key}`).removeAttribute("disabled");
        } else if (Array.isArray(presets[key])) {
          const selector = document.getElementById(key);
          for (let i = 0; i < selector.options.length; i++) {
            selector.options[i].selected = presets[key].includes(
              selector.options[i].value
            );
          }
        } else {
          document.querySelector(`#${key}`).value = presets[key];
          document.querySelector(`#${key}`).removeAttribute("disabled");
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  update_ui_states(null);
  savesettings();
}

document
  .getElementById("apply_preset")
  .addEventListener("click", preset_select_changed);
function set_preset_options() {
  // Set the Blocker presets on the page

  // Check what the selected dropdown item is
  let element = document.getElementById("presets");
  let children = [];

  // Find all the items in the dropdown
  for (let child of element.children) {
    children.push(child.value);
  }

  // Find out dropdown item and set our selected item text to it
  for (let val of progression_presets) {
    if (!children.includes(val.name)) {
      let opt = document.createElement("option");
      opt.value = val.name;
      opt.innerHTML = val.name;
      opt.title = val.description;
      element.appendChild(opt);

      if (val.name === "-- Select a Preset --") {
        opt.disabled = true;
        opt.hidden = true;
      }
    }
  }

  // Set the default value of the dropdown
  $("#presets").val("-- Select a Preset --");

  // Toggle elements and update the page according to the preset
  toggle_counts_boxes(null);
  toggle_b_locker_boxes(null);
  toggle_logic_type(null);
  toggle_bananaport_selector(null);
  update_door_one_num_access(null);
  update_door_two_num_access(null);
  update_win_con_num_access(null);

  // Load the data
  load_data();
}

set_preset_options();
function set_random_weights_options() {
  // Set the random settings presets on the page

  let element = document.getElementById("random-weights");
  let children = [];

  // Take note of the items currently in the dropdown
  for (let child of element.children) {
    children.push(child.value);
  }

  // Add all of the random weights presets
  for (let val of random_settings_presets) {
    if (!children.includes(val.name)) {
      let opt = document.createElement("option");
      opt.value = val.name;
      opt.innerHTML = val.name;
      opt.title = val.description;
      element.appendChild(opt);

      // Select the "Standard" preset by default
      if (val.name === "Standard") {
        opt.selected = true;
      }
    }
  }
}
set_random_weights_options();
function load_data() {
  try {
    // make sure all sliders are initialized
    for (element of document.getElementsByTagName("input")) {
      if (element.hasAttribute("data-slider-value")) {
        // check if the slider has already been initialized
        if (!element.hasAttribute("data-slider-initialized")) {
          element.setAttribute("data-slider-initialized", "true");
          $("#" + element.name).slider();
        }
      }
    }
    var settingsdb = settingsdatabase.result;
    transaction = settingsdb.transaction("saved_settings", "readonly");
    objectStore = transaction.objectStore("saved_settings");
    getRequest = objectStore.get("saved_settings");
    getRequest.onerror = function (event) {
      console.error("Failed to retrieve saved settings");
    };
    getRequest.onsuccess = function (event) {
      try {
        if (getRequest.result) {
          json = JSON.parse(getRequest.result);
          if (json !== null) {
            for (var key in json) {
              element = document.getElementsByName(key)[0];
              if (json[key] == "True") {
                element.checked = true;
              } else if (json[key] == "False") {
                element.checked = false;
              } else if (key.includes("starting_move_box")) {
                var starting_move_buttons = document.getElementsByName(key);
                for (element of starting_move_buttons) {
                  if (element.id.includes(json[key])) {
                    element.checked = true;
                  }
                }
              }
              try {
                element.value = json[key];
                if (element.hasAttribute("data-slider-value")) {
                  $("#" + key).slider("setValue", json[key]);
                }
                if (element.className.includes("selected")) {
                  for (var i = 0; i < element.options.length; i++) {
                    element.options[i].selected =
                      json[key].indexOf(element.options[i].value) >= 0;
                  }
                }
              } catch {}
            }
          }
          savesettings();
        } else {
          preset_select_changed();
        }
        // Once all the options and toggles are set, trigger various UI events to set up enable/disable states correctly
        var apply_preset_element = document.getElementById("apply_preset");
        apply_preset_element.dispatchEvent(new Event("custom-update-ui-event"));
      } catch {
        preset_select_changed();
      }
    };
  } catch {
    preset_select_changed();
  }
}
load_data();
