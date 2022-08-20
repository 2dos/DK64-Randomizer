importScripts("./md5.min.js");
async function timedCount() {
  var myHeaders = new Headers();
myHeaders.append('pragma', 'no-cache');
myHeaders.append('cache-control', 'no-cache');

var myInit = {
  method: 'GET',
  headers: myHeaders,
};

  fetch("../py_libraries/dk64rando-1.0.0-py3-none-any.whl", {cache: "no-store"})
  .then(response => response.text())
  .then(data => {
  	// Do something with your data
    postMessage(md5(data))
  });
  setTimeout("timedCount()", 60000);
}

timedCount();