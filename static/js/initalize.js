if (typeof window.RufflePlayer !== "undefined") {
  // Ruffle extension is loaded
  var modal = document.createElement("div");
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "9999";

  var modalContent = document.createElement("div");
  modalContent.style.backgroundColor = "#333";
  modalContent.style.padding = "20px";
  modalContent.style.borderRadius = "5px";
  modalContent.style.textAlign = "center";

  var message = document.createElement("p");
  message.textContent =
    "The Ruffle extension causes issues with this site (and we're not really sure why). Please disable it for this site.";
  message.style.color = "#fff";
  message.style.fontFamily = "Arial, sans-serif";
  message.style.fontSize = "16px";

  modalContent.appendChild(message);
  modal.appendChild(modalContent);
  document.body.appendChild(modal);

  // Prevent scrolling while the modal is open
  document.body.style.overflow = "hidden";

  console.log("Ruffle extension is loaded");
} else {
  // Ruffle extension is not loaded
  console.log("Ruffle extension is not loaded");
}

// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  console.log("Loading " + file)
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
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

run_python_file("ui/__init__.py");
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

function validFilename(filename, dir, valid_extension=null) {
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
  })
}
var current_seed_data;
var cosmetics;
var cosmetic_names;
var cosmetic_extensions;
var cosmetic_truncated_names = {
  bgm: [],
  majoritems: [],
  minoritems: [],
  events: []
}

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

var imported_music_json = "";

function music_selection_filebox() {
  let input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";

  input.onchange = async (e) => {
    let file = e.target.files[0];
    let json_text = await file.text();
    imported_music_json = json_text;
    pyodide.runPythonAsync(`
      import js
      from ui.music_select import import_music_selections
      import_music_selections(js.imported_music_json)
    `);
  };

  input.click();
}

var imported_plando_json = "";

function plando_import_filebox() {
  let input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";

  input.onchange = async (e) => {
    let file = e.target.files[0];
    let json_text = await file.text();
    imported_plando_json = json_text;
    pyodide.runPythonAsync(`
      import js
      from ui.plando_settings import import_plando_options
      import_plando_options(js.imported_plando_json)
    `);
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
          transition_promises.push(createMusicLoadPromise(new_zip, filename))
        } else if (validFilename(filename, "textures/tns_portal/", ".png")) {
          portal_promises.push(createMusicLoadPromise(new_zip, filename))
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

      cosmetics = {
        bgm: bgm,
        majoritems: majoritems,
        minoritems: minoritems,
        events: events,
        transitions: transitions,
        tns_portals: tns_portals,
      };
      cosmetic_names = {
        bgm: bgm_names,
        majoritems: majoritem_names,
        minoritems: minoritem_names,
        events: event_names,
        transitions: transition_names,
        tns_portals: tns_portal_names,
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
    "BGM": cosmetic_names.bgm,
    "MajorItem": cosmetic_names.majoritems,
    "MinorItem": cosmetic_names.minoritems,
    "Event": cosmetic_names.events,
  }
  cosmetic_truncated_names = {
    bgm: [],
    majoritems: [],
    minoritems: [],
    events: []
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
  var starting_move_box_buttons = $(":input[name^='starting_move_box_']:checked");
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

async function load_presets() {
  await pyodide.runPythonAsync(`from ui.rando_options import preset_select_changed
preset_select_changed(None)`);
}

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
async function try_to_load_from_args() {
  await pyodide.runPythonAsync(`from ui.generate_buttons import get_args
get_args()`);
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
    document.getElementById("most_recent_seed_id").innerHTML = "<strong>Most Recent Seed ID:</strong> " + seed_id;
    document.getElementById("most_recent_seed_date").innerHTML = "<strong>Most Recent Seed Date:</strong> " + now.toLocaleDateString(
      undefined,
      {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }
    );
  } catch (error) {console.log(error)}
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
        document.getElementById("most_recent_seed_id").innerHTML = "<strong>Most Recent Seed ID:</strong> " + sorted_array[0].seed_id;
        document.getElementById("most_recent_seed_date").innerHTML = "<strong>Most Recent Seed Date:</strong> " + sorted_array[0].date.toLocaleDateString( undefined, {  year: "numeric",  month: "short",  day: "2-digit",  hour: "2-digit",  minute: "2-digit",  second: "2-digit",});
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
        
        try_to_load_from_args()

      } catch {try_to_load_from_args()}
    };
  } catch {try_to_load_from_args()}
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

function apply_download() {
  if (document.getElementById("rom").value.trim().length === 0 || !document.getElementById("rom").classList.contains("is-valid")) {
    document.getElementById("rom").select();
    if (!document.getElementById("rom").classList.contains("is-invalid")) {
      document.getElementById("rom").classList.add("is-invalid");
      return
    }
  }
  console.log("Applying Download");
  return pyodide.runPythonAsync(`
    import js
    from randomizer.Patching.ApplyLocal import patching_response
    patching_response(str(js.event_response_data), from_patch_gen=True)
  `);
}
// if the tab is set to seed info get the generate_seed button and change the text to "Download Seed" we want to check this on every nav tab change
function check_seed_info_tab() {
  
  if (document.getElementById("nav-settings-tab").classList.contains("active")) {
    document.getElementById("generate_seed").value = "Download Seed";
    document.getElementById("generate_seed").onclick = null;
    document.getElementById("generate_seed").onclick = function() {apply_download()};
  }
  else {
    // if document.getElementById("download_patch_file").checked set it to Generate Patch File
    if (document.getElementById("download_patch_file").checked) {
      document.getElementById("generate_seed").value = "Generate Patch File";
    }
    else{
      document.getElementById("generate_seed").value = "Generate Seed";
    }
    // Remove the onclick event
    document.getElementById("generate_seed").onclick = null;
    document.getElementById("generate_seed").onclick = function() {document.getElementById("trigger_download_event").click()};
  }
}
function toggleDelayedSpoilerLogInput() {
  var generateSpoilerLogCheckbox = document.getElementById('delayed_spoilerlog_container');
  if (!document.getElementById('generate_spoilerlog').checked) {
      generateSpoilerLogCheckbox.removeAttribute('hidden');
  }
  else {
      generateSpoilerLogCheckbox.setAttribute('hidden', '');
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
async function apply_patch(data, run_async) {
  // Base64 decode the response
  event_response_data = data;
  var decodedData = base64ToArrayBuffer(data);
  zip = new JSZip();

  try {
    // Load the zip file data into JSZip
    const zipFile = await zip.loadAsync(decodedData);

    // Create an array to store all the promises
    const promises = [];
    query_stats();
    // Iterate over each file in the zip
    zip.forEach(function (relativePath, zipEntry) {
      if (!zipEntry.dir) {
        // Extract the file content as a string or other appropriate format
        // Store the file content in a variable with a name derived from the file name
        fileName = zipEntry.name.replace(/[^a-zA-Z0-9]/g, "_");
        if (fileName == "patch") {
          // Create a promise for each async operation and add it to the array
          const promise = zipEntry
            .async("uint8array")
            .then(function (fileContent) {
              console.log("Applying Xdelta Patch");
              apply_xdelta(fileContent);

              if (run_async == true) {
                // Return the promise for pyodide.runPythonAsync
                return pyodide.runPythonAsync(`
                import js
                from randomizer.Patching.ApplyLocal import patching_response
                patching_response(str(js.event_response_data), from_patch_gen=True)
              `);
              }
            });

          promises.push(promise);
        }
      }
    });

    // Wait for all the promises to resolve
    await Promise.all(promises);
  } catch (error) {
    console.error("Error unzipping the file:", error);
  }
}

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
  }
  else if (window.location.hostname == "dk64randomizer.com") {
    var url = "https://generate.dk64rando.com/get_spoiler_log";
  }
  else {
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
        save_text_as_file(JSON.stringify(data, null, 2), document.getElementById('generated_seed_id').innerHTML + '-spoilerlog.json')
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
    }
  });
}

function get_seed_from_server(hash) {
  // GET to localhost:8000/get_spoiler_log with the args hash with search_query as the value
  // Get the website location
  if (window.location.hostname == "dev.dk64randomizer.com") {
    var url = "https://dev-generate.dk64rando.com/get_seed";
  }
  else if (window.location.hostname == "dk64randomizer.com") {
    var url = "https://generate.dk64rando.com/get_seed";
  }
  else {
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
    }
  });
  // wait for the ajax call to finish
  while (return_data.readyState != 4) {
    sleep(1);
  }
  return return_data.responseText;
}

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
                var starting_move_buttons = document.getElementsByName(key)
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
          load_presets();
        }
        // Once all the options and toggles are set, trigger various UI events to set up enable/disable states correctly
        var apply_preset_element = document.getElementById("apply_preset");
        apply_preset_element.dispatchEvent(new Event('custom-update-ui-event'));
      } catch {
        load_presets();
      }
    };
  } catch {
    load_presets();
  }
}
load_data();