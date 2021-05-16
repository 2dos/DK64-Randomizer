window.onload = load_inital;

function load_inital() {
  brython();
  $("#progressmodal").modal({
    show: false,
    backdrop: "static",
  });
  resp = $.ajax({
    url: "/load_settings",
    async: false,
  }).responseText;
  // if (resp == "None") {
  //   blocker_selectionChanged();
  //   troff_selectionChanged();
  // } else {
  //   var jsonresp = JSON.parse(resp);
  //   for (var k in jsonresp) {
  //     document.getElementsByName(k)[0].value = jsonresp[k];
  //   }
  // }
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

function saveCurrentSettings() {
  $.ajax({
    url: "/save_settings",
    type: "POST",
    dataType: "json",
    data: { params: JSON.stringify($("#form").serializeArray()) },
  });
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
      resolve(window.asmcode);
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
  }
}
