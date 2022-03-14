// This is a wrapper script to just load the UI python scripts and call python as needed.
async function run_python_file(file) {
  await pyodide.runPythonAsync(await (await fetch(file)).text());
}
run_python_file("ui/__init__.py");
// Sleep function to run functions after X seconds
async function sleep(seconds, func, args) {
  setTimeout(function () {
    func(...args);
  }, seconds * 1000);
}

var cosmetics;
document
  .getElementById("music_file")
  .addEventListener("change", function (evt) {
    var fileToLoad = document.getElementById("music_file").files[0];
    var fileReader = new FileReader();
    fileReader.onload = function (fileLoadedEvent) {
      var new_zip = new JSZip();
      new_zip.loadAsync(fileLoadedEvent.target.result).then(function () {
        bgm = [];
        fanfares = [];
        events = [];
        for (var file in new_zip.files) {
          if (file.includes("bgm/") && file.slice(-4) == ".bin") {
            new_zip
              .file(file)
              .async("Uint8Array")
              .then(function (content) {
                bgm.push(content);
              });
          } else if (file.includes("fanfares/") && file.slice(-4) == ".bin") {
            new_zip
              .file(file)
              .async("Uint8Array")
              .then(function (content) {
                fanfares.push(content);
              });
          } else if (file.includes("events/") && file.slice(-4) == ".bin") {
            new_zip
              .file(file)
              .async("Uint8Array")
              .then(function (content) {
                events.push(content);
              });
          }
        }
        cosmetics = { bgm: bgm, fanfares: fanfares, events: events };
      });
    };

    fileReader.readAsArrayBuffer(fileToLoad);
  });

jq = $