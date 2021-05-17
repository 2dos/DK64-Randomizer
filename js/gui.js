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

        for (let retries = 0; retries < 20; retries++) {
          setTimeout(function () {
            if (document.getElementById("blocker_selected").options[0] == "Vanilla") {
              blocker_selectionChanged();
              troff_selectionChanged();
            }
          }, 1000);
        }
    } else {
      var jsonresp = JSON.parse(savedUserJsonString);
      for (var k in jsonresp) {
        try {
          document.getElementsByName(k)[0].value = jsonresp[k];
        } catch {}
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
    response = randomize_data(formdata);
    setTimeout(function () {
      $("#patchprogress").width("40%");
      $("#progress-text").text("Randomizing complete");
      setTimeout(function () {
        resolve(response);
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
  $("input:disabled, select:disabled").each(function () {
    $(this).removeAttr("disabled");
  });
  if ($("#input-file-rom").val() == "") {
    $("#input-file-rom").select();
  } else {
    form = $("#form").serialize();
    $("#progressmodal").modal("show");
    progression_clicked();

    randomizeseed(form).then(function (rando) {
      generate_asm(rando).then(function (binary_data) {
        applyPatch(patch, romFile, false, binary_data);
      });
    });
    JSONData = JSON.parse(queryStringToJSON(form));
    delete JSONData["seed"];
    setCookie("settings", JSON.stringify(JSONData), 30);
  }
}
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
