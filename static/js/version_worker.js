importScripts("./md5.min.js");
async function timedCount() {
  fetch("../py_libraries/dk64rando-1.0.0-py3-none-any.whl", {
    cache: "no-store",
  })
    .then((response) => response.text())
    .then((data) => {
      postMessage(md5(data));
    });
  setTimeout("timedCount()", 300000);
}

timedCount();
