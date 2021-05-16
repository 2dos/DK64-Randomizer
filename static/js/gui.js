function blocker_selectionChanged() {
  option = $("#blocker_selected option:selected").text().trim();
  resp = $.ajax({
    url: "/blocker/" + option,
    async: false,
  }).responseJSON;
  for (var key in resp) {
    $("#blocker_" + key).val(resp[key][0]);
    $("#blocker_" + key).prop("title", resp[key][1]);
  }
}

function troff_selectionChanged() {
  option = $("#troff_selected option:selected").text().trim();
  resp = $.ajax({
    url: "/troff/" + option,
    async: false,
  }).responseJSON;
  for (var key in resp) {
    $("#troff_" + key).val(resp[key][0]);
    $("#troff_" + key).prop("title", resp[key][1]);
  }
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

function copyToClipboard() {
  var clipboardText = "";
  clipboardText = $("#settings_string").val();
  var textArea = document.createElement("textarea");
  textArea.value = clipboardText;
  document.body.appendChild(textArea);
  textArea.select();

  try {
    document.execCommand("copy");
  } catch (err) {}
  document.body.removeChild(textArea);
}

function request_seed() {
  $("#seed").val(
    $.ajax({
      url: "/random_seed",
      async: false,
    }).responseText
  );
}

function load_inital() {
  $("#progressmodal").modal({
    show: false,
    backdrop: "static",
  });
  resp = $.ajax({
    url: "/load_settings",
    async: false,
  }).responseText;
  if (resp == "None") {
    blocker_selectionChanged();
    troff_selectionChanged();
  } else {
    var jsonresp = JSON.parse(resp);
    for (var k in jsonresp) {
      document.getElementsByName(k)[0].value = jsonresp[k];
    }
  }
}
window.onload = load_inital;

function randomizeseed(formdata) {
  return new Promise((resolve, reject) => {
    $("#patchprogress").width("30%");
    $("#progress-text").text("Randomizing seed");
    $(function () {
      $.ajax({
        type: "POST",
        url: "/",
        data: formdata,
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("50%");
            $("#progress-text").text("Seed Randomized");
            setTimeout(function () {
              resolve(data.responseText);
            }, 1000);
          }, 1000);
        },
      });
    });
  });
}

function generate_asm(asm) {
  return new Promise((resolve, reject) => {
    $(function () {
      $("#patchprogress").width("60%");
      $("#progress-text").text("Generating ASM");
      $.ajax({
        type: "POST",
        url: "/asm_patch",
        data: { asm: String(asm) },
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("70%");
            $("#progress-text").text("ASM Generated");
            setTimeout(function () {
              resolve(data.responseText);
            }, 1000);
          }, 1000);
        },
      });
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
// TODO: Move all the progress stuff to a toggle function
