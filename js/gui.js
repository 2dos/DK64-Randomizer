window.onload = load_inital;

function load_inital() {
  brython();
  $("#progressmodal").modal({
    show: false,
    backdrop: "static",
  });
  $("#loading").modal({
    show: true,
    backdrop: "static",
  });
  $("#loading").modal("show");
  setTimeout(function () {
    var savedUserJsonString = getCookie("settings");
    if (savedUserJsonString.length === 0) {
      if (
        document
          .getElementById("blocker_selected")
          .options[0].value.toLowerCase() == "vanilla"
      ) {
        const e = new Event("change");
        element = document.querySelector("#blocker_selected");
        element.dispatchEvent(e);
        element = document.querySelector("#troff_selected");
        element.dispatchEvent(e);
      }
    } else {
      var jsonresp = JSON.parse(savedUserJsonString);
      for (var k in jsonresp) {
        try {
          document.getElementsByName(k)[0].value = jsonresp[k];
        } catch (e) {}
      }
    }
    progression_clicked();
    $("#loading").modal("hide");
  }, 2000);
}

function progression_clicked() {
  if ($("#randomize_progression")[0].checked) {
    $("#seed").removeAttr("disabled");
    $("#seed_button").removeAttr("disabled");
    $("#unlock_all_kongs").attr("disabled", "disabled");
    $("#unlock_all_kongs").prop("checked", true);
  } else {
    $("#seed").attr("disabled", "disabled");
    $("#seed_button").attr("disabled", "disabled");
    $("#unlock_all_kongs").removeAttr("disabled");
  }
}

function randomizeseed(formdata) {
  return new Promise((resolve, reject) => {
    $("#patchprogress").width("30%");
    $("#progress-text").text("Randomizing seed");
    setTimeout(function () {
      response = randomize_data(formdata);
      setTimeout(function () {
        $("#patchprogress").width("40%");
        $("#progress-text").text("Randomizing complete");
        setTimeout(function () {
          resolve(response);
        }, 1000);
      }, 1000);
    }, 1000);
  });
}

function generate_asm(asm) {
  return new Promise((resolve, reject) => {
    $(function () {
      $("#patchprogress").width("60%");
      $("#progress-text").text("Generating ASM");
      L.execute(
        `
      function convert(code_filename)
          lips = require "lips.init";
          local code = {};
          function codeWriter(key, value)
              function isPointer(value)
                  return type(value) == "number" and value >= 0x80000000 and value < 0x80800000;
              end
              if isPointer(key) then
                  table.insert(code, {key - 0x80000000, value});
              end
          end
          lips(code_filename, codeWriter);
          local formatted_code = "";
          for k,v in pairs(code) do
            local pair_string = "";
            for key, value in pairs(v) do
              if(key == 1)
              then
                pair_string = pair_string .. value .. ":";
              else
                pair_string = pair_string .. value;
              end
            end
            formatted_code = formatted_code .. pair_string .. "\\n";
          end
          window.asmcode = formatted_code;
      end
      convert([[` +
          asm +
          "]])"
      );
      setTimeout(function () {
        $("#patchprogress").width("70%");
        $("#progress-text").text("ASM Generated");
        setTimeout(function () {
          resolve(window.asmcode);
        }, 1000);
      }, 1000);
    });
  });
}
function submitdata() {
  downloadlankyfile = false;
  if (document.getElementById("downloadjson").checked) {
    downloadlankyfile = document.getElementById("downloadjson").checked;
  }
  if ($("#input-file-rom").val() == "") {
    $("#input-file-rom").select();
  } else {
    curr_status = [];
    $("input:disabled, select:disabled").each(function () {
      curr_status.push($(this));
      $(this).removeAttr("disabled");
    });
    var x = $('#form').serializeArray();
    $('#form').find(':checkbox:not(:checked)').map(function () { 
      x.push({ name: this.name, value: this.checked ? this.value : "False" }); 
    });
    var form = {};
    $(x).each(function(index, obj){
        form[obj.name] = obj.value;
    });
    form = new URLSearchParams(form).toString();
    curr_status.forEach(function (item) {
      $(item).prop("disabled", true);
    });
    $("#progressmodal").modal("show");
    progression_clicked();

    setTimeout(function () {
      randomizeseed(form).then(function (rando) {
        //downloadToFile(rando, 'settings.asm', 'text/plain');
        if (rando == false) {
          setTimeout(function () {
            $("#patchprogress").addClass("bg-danger");
            $("#patchprogress").width("100%");
            $("#progress-text").text("Failed to successfully generate a seed.");
            setTimeout(function () {
              $("#progressmodal").modal("hide");
              $("#patchprogress").removeClass("bg-danger");
              $("#patchprogress").width("0%");
              $("#progress-text").text("");
            }, 5000);
          }, 1000);
        } else {
          JSONData = JSON.parse(queryStringToJSON(form));
          if (downloadlankyfile) {
            setTimeout(function () {
              downloadToFile(
                JSON.stringify(JSONData),
                "dk64r-settings-" + JSONData["seed"] + ".lanky",
                "text/plain"
              );
              $("#patchprogress").width("100%");
              $("#progress-text").text("Patch File Generated.");
              setTimeout(function () {
                $("#progressmodal").modal("hide");
                $("#patchprogress").width("0%");
                $("#progress-text").text("");
              }, 5000);
            }, 1000);
          } else {
            generate_asm(rando).then(function (binary_data) {
              applyPatch(patch, romFile, false, binary_data);
            });
          }
        }
      });
    }, 1000);
    JSONData = JSON.parse(queryStringToJSON(form));
    delete JSONData["seed"];
    setCookie("settings", JSON.stringify(JSONData), 30);
  }
}
const downloadToFile = (content, filename, contentType) => {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
};

function queryStringToJSON(qs) {
  qs = qs || location.search.slice(1);

  var pairs = qs.split("&");
  var result = {};
  pairs.forEach(function (p) {
    var pair = p.split("=");
    var key = pair[0];
    var value = decodeURIComponent(pair[1] || "");

    if (result[key]) {
      if (Object.prototype.toString.call(result[key]) === "[object Array]") {
        result[key].push(value);
      } else {
        result[key] = [result[key], value];
      }
    } else {
      result[key] = value;
    }
  });
  return JSON.stringify(result);
}
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function loadlankyfile() {
  if ($("#input-file-rom").val() == "") {
    $("#input-file-rom").select();
  } else if ($("#jsonfileloader").val() == "") {
    $("#jsonfileloader").select();
  } else {
    var file_hook = document.getElementById("jsonfileloader");
    var fr = new FileReader();
    fr.onload = function () {
      jsonresp = JSON.parse(fr.result);
      for (var k in jsonresp) {
        try {
          document.getElementsByName(k)[0].value = jsonresp[k];
        } catch (e) {}
      }
      submitdata();
    };
    fr.readAsText(file_hook.files[0]);
  }
}

var file_hook = document.getElementById("jsonfileloader");
file_hook.addEventListener("change", function () {
  var fr = new FileReader();
  fr.onload = function () {
    for (var k in JSON.parse(fr.result)) {
      try {
        if (JSON.parse(fr.result)[k] == "True") {
          document.getElementsByName(k)[0].checked = true;
        } else if (JSON.parse(fr.result)[k] == "False") {
          document.getElementsByName(k)[0].checked = false;
        } else {
          document.getElementsByName(k)[0].value = JSON.parse(fr.result)[k];
        }
      } catch (e) {}
    }
  };
  fr.readAsText(file_hook.files[0]);
});
