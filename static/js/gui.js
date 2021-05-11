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

function dumpFile() {
  return new Promise((resolve, reject) => {
    var form_data = new FormData();
    form_data.append("file", $("#romfile").prop("files")[0]);
    $("#patchprogress").width(20);
    $(function () {
      $.ajax({
        type: "POST",
        url: "/prep_rom",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        complete: function (data) {
          $("#patchprogress").width(90);
          resolve();
        },
      });
    });
    $("#patchprogress").width(140);
  });
}
function submitdata() {
  $("input:disabled, select:disabled").each(function () {
    $(this).removeAttr("disabled");
  });
  if ($("#romfile").val() == "") {
    return false;
  } else {
    $("#progressmodal").modal("show");
    dumpFile().then(function () {
      $("#patchprogress").width(260);
      $.ajax({
        type: "POST",
        url: "/",
        data: $("#form").serialize(),
        async: true,
        complete: function (data) {
          $("#patchprogress").width(360);
          $("#progressmodal").modal("hide");
          $("#modal").modal("show");
        },
      });
      $("#patchprogress").width(320);
    });
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
  resp = JSON.parse(
    $.ajax({
      url: "/load_settings",
      async: false,
    }).responseText
  );
  if (resp == "None") {
    blocker_selectionChanged();
    troff_selectionChanged();
  } else {
    for (var k in resp) {
      document.getElementsByName(k)[0].value = resp[k];
    }
  }
}
window.onload = load_inital;
