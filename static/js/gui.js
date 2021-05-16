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
