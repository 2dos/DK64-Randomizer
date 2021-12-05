if (window.Worker) {
  background_worker = new Worker("./static/js/webworker.js");
  background_worker.onmessage = function (e) {
    event_response_data = JSON.stringify(e.data)
    pyodide.runPython(
      `
    import js
    import json
    exec(json.loads(js.event_response_data).get("returning_func"))
    eval(str(json.loads(js.event_response_data).get("returning_func").split()[-1]) + "(" + js.event_response_data + ")")
    `
    );
  };
} else {
  console.log("Your browser does not support web workers.");
}
