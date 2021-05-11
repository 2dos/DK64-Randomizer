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

function dumpFile() {
  return new Promise((resolve, reject) => {
    var form_data = new FormData();
    form_data.append("file", $("#romfile").prop("files")[0]);
    $(function () {
      $.ajax({
        type: "POST",
        url: "/prep_rom",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("20%");
            $("#progress-text").text("Rom Loaded");
            setTimeout(function () {
              resolve();
            }, 1000);
          }, 1000);
        },
      });
    });
    $("#patchprogress").width("10%");
    $("#progress-text").text("Started Loading Rom");
  });
}

function randomizeseed(formdata) {
  return new Promise((resolve, reject) => {
    $(function () {
      $.ajax({
        type: "POST",
        url: "/",
        data: formdata,
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("40%");
            $("#progress-text").text("Applied BPS");
            setTimeout(function () {
              resolve();
            }, 1000);
          }, 1000);
        },
      });
    });
    $("#patchprogress").width("30%");
    $("#progress-text").text("Applying BPS");
  });
}

function applybps(formdata) {
  return new Promise((resolve, reject) => {
    $(function () {
      $.ajax({
        type: "POST",
        url: "/bps_patch",
        data: formdata,
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("60%");
            $("#progress-text").text("Applied BPS");
            setTimeout(function () {
              resolve();
            }, 1000);
          }, 1000);
        },
      });
    });
    $("#patchprogress").width("50%");
    $("#progress-text").text("Applying BPS");
  });
}

function applyasm(formdata) {
  return new Promise((resolve, reject) => {
    $(function () {
      $.ajax({
        type: "POST",
        url: "/asm_patch",
        data: formdata,
        complete: function (data) {
          setTimeout(function () {
            $("#patchprogress").width("80%");
            $("#progress-text").text("Applied ASM");
            setTimeout(function () {
              resolve();
            }, 1000);
          }, 1000);
        },
      });
    });
    $("#patchprogress").width("70%");
    $("#progress-text").text("Applying ASM");
  });
}

function submitdata() {
  $("input:disabled, select:disabled").each(function () {
    $(this).removeAttr("disabled");
  });
  if ($("#romfile").val() == "") {
    $("#romfile").select();
  } else {
    form = $("#form").serialize();
    $("#progressmodal").modal("show");
    dumpFile().then(function () {
      randomizeseed(form).then(function () {
        applybps(form).then(function () {
          applyasm(form).then(function () {
            $("#patchprogress").width("100%");
            $("#progress-text").text("Rom has been patched");
            setTimeout(function () {
              $("#progressmodal").modal("hide");
              $("#modal").modal("show");
            }, 2000);
          });
        });
      });
    });
  }
}
