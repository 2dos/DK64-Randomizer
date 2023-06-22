// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
let user_agent = navigator.userAgent;
if (window.location.protocol != "https:") {
  if (location.hostname != "localhost" && location.hostname != "127.0.0.1") {
    location.href = location.href.replace("http://", "https://");
  }
}

// if the domain is not the main domain, hide spoiler_warning_2 and spoiler_warning_1
if (location.hostname == "dk64randomizer.com") {
  document.getElementById("spoiler_warning_2").style.display = "none";
  document.getElementById("spoiler_warning_1").style.display = "none";
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
  Toastify({
    text: text,
    duration: 15000,
    close: true,
    gravity: "top",
    position: "right",
    stopOnFocus: true,
    style: {
      background: "#800000",
    },
    onClick: function () {},
  }).showToast();
}
function getFile(file) {
  return $.ajax({
    type: "GET",
    url: file,
    async: false,
  }).responseText;
}
var cosmetics;
var cosmetic_names;
document
  .getElementById("music_file")
  .addEventListener("change", function (evt) {
    var fileToLoad = document.getElementById("music_file").files[0];
    var fileReader = new FileReader();
    fileReader.onload = function (fileLoadedEvent) {
      var new_zip = new JSZip();
      new_zip.loadAsync(fileLoadedEvent.target.result).then(async function () {
        let bgm_promises = [];
        let majoritem_promises = [];
        let minoritem_promises = [];
        let event_promises = [];

        for (var filename of Object.keys(new_zip.files)) {
          if (filename.includes("bgm/") && filename.slice(-4) == ".bin") {
            bgm_promises.push(new Promise((resolve, reject) => {
              var current_filename = filename;
              new_zip
                .file(current_filename)
                .async("Uint8Array")
                .then(function (content) {
                  resolve({
                    name: current_filename.slice(0, -4),
                    file: content
                  })
                });
            }));
          } else if (filename.includes("majoritems/") && filename.slice(-4) == ".bin") {
            majoritem_promises.push(new Promise((resolve, reject) => {
              var current_filename = filename;
              new_zip
                .file(current_filename)
                .async("Uint8Array")
                .then(function (content) {
                  resolve({
                    name: current_filename.slice(0, -4),
                    file: content
                  })
                });
            }));
          } else if (filename.includes("minoritems/") && filename.slice(-4) == ".bin") {
            minoritem_promises.push(new Promise((resolve, reject) => {
              var current_filename = filename;
              new_zip
                .file(current_filename)
                .async("Uint8Array")
                .then(function (content) {
                  resolve({
                    name: current_filename.slice(0, -4),
                    file: content
                  })
                });
            }));
          } else if (filename.includes("events/") && filename.slice(-4) == ".bin") {
            event_promises.push(new Promise((resolve, reject) => {
              var current_filename = filename;
              new_zip
                .file(current_filename)
                .async("Uint8Array")
                .then(function (content) {
                  resolve({
                    name: current_filename.slice(0, -4),
                    file: content
                  })
                });
            }));
          }
        }

        let bgm_files = await Promise.all(bgm_promises);
        let majoritem_files = await Promise.all(majoritem_promises);
        let minoritem_files = await Promise.all(minoritem_promises);
        let event_files = await Promise.all(event_promises);

        let bgm = bgm_files.map(x => x.file);
        let bgm_names = bgm_files.map(x => x.name);
        let majoritems = majoritem_files.map(x => x.file);
        let majoritem_names = majoritem_files.map(x => x.name);
        let minoritems = minoritem_files.map(x => x.file);
        let minoritem_names = minoritem_files.map(x => x.name);
        let events = event_files.map(x => x.file);
        let event_names = event_files.map(x => x.name);

        cosmetics = { bgm: bgm, majoritems: majoritems, minoritems: minoritems, events: events };
        cosmetic_names = {bgm: bgm_names, majoritems: majoritem_names, minoritems: minoritem_names, events: event_names };
      });
    };

    fileReader.readAsArrayBuffer(fileToLoad);
  });

jq = $;

$("#form input").on("input change", function (e) {
  //This would be called if any of the input element has got a change inside the form
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
  saveDataToIndexedDB("saved_settings", JSON.stringify(json));
});
$("#form select").on("change", function (e) {
  //This would be called if any of the input element has got a change inside the form
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
  saveDataToIndexedDB("saved_settings", JSON.stringify(json));
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
    try{
      var db = romdatabase.result;
      var tx = db.transaction("ROMStorage", "readwrite");
      var store = tx.objectStore("ROMStorage");
      // Store it in the database
      store.put({ ROM: "N64", value: file });
    }
    catch{}
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
var romdatabase = indexedDB.open("ROMStorage", 1);
var seeddatabase = indexedDB.open("SeedStorage", 1);
var settingsdatabase = indexedDB.open("SettingsDB", 1);
settingsdatabase.onupgradeneeded = function () {
  try {
    var settingsdb = settingsdatabase.result;
    settingsdb.createObjectStore("saved_settings");
  } catch{}
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
  try{
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
  }
  catch{}
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
      } catch {}
    };
  } catch {}
}

var w;
var CurrentRomHash;

243


function base64ToArrayBuffer(base64) {
    var binaryString = atob(base64);
    var bytes = new Uint8Array(binaryString.length);
    for (var i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
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
        console.log("seed gen waiting in queue")
        $("#progress-text").text(
          "Waiting in queue for other seeds to generate."
        );
        $("#patchprogress").width("40%");
        setTimeout(function () {
          generate_seed(url, json, git_branch);
        }, 5000);
      } else if (xhr.status == 201) {
        console.log("seed gen queued")
        $("#progress-text").text("Seed Gen Queued");
        $("#patchprogress").width("30%");
        setTimeout(function () {
          generate_seed(url, json, git_branch);
        }, 5000);
        
      } else if (xhr.status == 203) {
        console.log("seed gen started")
        $("#progress-text").text("Seed Gen Started");
        $("#patchprogress").width("50%");
        setTimeout(function () {
          generate_seed(url, json, git_branch);
        }, 5000);
        
      } else if (xhr.status == 208) {
        console.log(data)
        $("#progress-text").text(data);
        $("#patchprogress").addClass("bg-danger");
        $("#patchprogress").width("100%");
        setTimeout(function () {
          $("#progressmodal").modal("hide");
          $("#patchprogress").removeClass("bg-danger");
          $("#patchprogress").width("0%");
          $("#progress-text").text("");
        }, 5000);
        
      } else {
        $("#progress-text").text("Seed Gen Complete");
        $("#patchprogress").width("80%");    
        apply_patch(data, true);       
      }
    },
    error: function (data, textStatus, xhr) {
      $("#patchprogress").addClass("bg-danger");
      $("#progress-text").text("Something went wrong please try again");
      $("#patchprogress").width("100%");
      setTimeout(function () {
        $("#progressmodal").modal("hide");
        $("#patchprogress").removeClass("bg-danger");
        $("#patchprogress").width("0%");
        $("#progress-text").text("");
      }, 1000);
    },
  });
}

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

    // Iterate over each file in the zip
    zip.forEach(function(relativePath, zipEntry) {
      if (!zipEntry.dir) {
        // Extract the file content as a string or other appropriate format
        // Store the file content in a variable with a name derived from the file name
        fileName = zipEntry.name.replace(/[^a-zA-Z0-9]/g, '_');
        if (fileName == "patch") {
          // Create a promise for each async operation and add it to the array
          const promise = zipEntry.async('uint8array').then(function(fileContent) {
            console.log("Applying Xdelta Patch");
            apply_xdelta(fileContent);

            if (run_async == true) {
              // Return the promise for pyodide.runPythonAsync
              return pyodide.runPythonAsync(`
                import js
                from randomizer.Patching.ApplyLocal import patching_response
                patching_response(str(js.event_response_data))
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
    console.error('Error unzipping the file:', error);
  }
}

function saveDataToIndexedDB(key, value) {
  try{
    var settingsdb = settingsdatabase.result;
    transaction = settingsdb.transaction("saved_settings", "readwrite");
    objectStore = transaction.objectStore("saved_settings");
    objectStore.put(value, key);
  }
  catch{}
}

function loadDataFromIndexedDB(key) {
  return new Promise((resolve, reject) => {
   try{
      var settingsdb = settingsdatabase.result;
      transaction = settingsdb.transaction("saved_settings", "readonly");
      objectStore = transaction.objectStore("saved_settings");
      request = objectStore.get(key);
      request.onerror = function (event) {
        reject("Transaction error: " + event.target.errorCode);
      };

      request.onsuccess = function (event) {
        value = event.target.result;
        console.log(value)
        resolve(value);
      };
    }
    catch{reject("Read Error")}
  });
}


function load_data() {


  try{
    var settingsdb = settingsdatabase.result;
    transaction = settingsdb.transaction("saved_settings", "readonly");
    objectStore = transaction.objectStore("saved_settings");
    getRequest = objectStore.get("saved_settings");
    getRequest.onerror = function(event) {
      console.error("Failed to retrieve saved settings");
    };
    getRequest.onsuccess = function(event) {
      try{
        if (getRequest.result) {
          json = JSON.parse(getRequest.result);
          if (json !== null) {
            for (var key in json) {
              element = document.getElementsByName(key)[0];
              if (json[key] == "True") {
                element.checked = true;
              } else if (json[key] == "False") {
                element.checked = false;
              }
              try {
                element.value = json[key];
                if (element.hasAttribute("data-slider-value")) {
                  element.setAttribute("data-slider-value", json[key]);
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
        } else {
          load_presets();
        }
      }
      catch{load_presets();}
    };
  }
  catch{
    load_presets();
  }

}
load_data();