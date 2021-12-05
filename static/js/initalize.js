async function run_python_file(file) {
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
run_python_file("ui/__init__.py")

function update_progres_modal(status, text, width, mod_class){
  if (status){
    $("#progressmodal").modal(status)
  }
  if (text){
    $("#progress-text").text(text)
  }
  if (width){
    $("#patchprogress").width(width)
  }
  if (mod_class){
    if($("#patchprogress").hasClass(mod_class)){
      $("#patchprogress").removeClass(mod_class)
    }
    else{
      $("#patchprogress").addClass(mod_class)
    }
  }
}