// Main UI thread for the webworker
if (window.Worker) {
  // Establishes the webworker.
  background_worker = new Worker("./static/js/webworker.js");
  // When we get a message back from the webworker for whatever we have run
  background_worker.onmessage = function (e) {
    // Convert the data sent as json to a string and store it as a global var we can pass
    // We convert it back to a string so we don't have to deal with inserting it into the function as a string
    event_response_data = JSON.stringify(e.data);
    // Load the data saved as a var in javascript, convert it back to json and then eval the return function string so we can call it
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
