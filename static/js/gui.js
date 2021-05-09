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
    $("#leveltable")
      .find("input, textarea, button, select")
      .removeAttr("disabled");
    $("#seed").removeAttr("disabled");
    $("#seed_button").removeAttr("disabled");
    $("#unlock_all_kongs").attr("disabled", "disabled");
    $("#unlock_all_kongs").prop("checked", true);
  } else {
    $("#leveltable")
      .find("input, textarea, button, select")
      .attr("disabled", "disabled");
    $("#seed").attr("disabled", "disabled");
    $("#seed_button").attr("disabled", "disabled");
    $("#unlock_all_kongs").removeAttr("disabled");
  }
}

function submitdata() {
  $("input:disabled, select:disabled").each(function () {
    $(this).removeAttr("disabled");
  });
  $("#form").trigger("submit");
}
