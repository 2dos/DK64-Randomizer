// Used for generating the UI for the downloadable app
const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
var static = require("node-static");
var file = new static.Server(`${__dirname}`);

let mainWindow = null;

require("http")
  .createServer(function (request, response) {
    request
      .addListener("end", function () {
        file.serve(request, response);
      })
      .resume();
  })
  .listen(9990);

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1024,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
    },
    icon: __dirname + "/base-hack/assets/DKTV/logo3.png",
  });
  mainWindow.loadURL(
    require("url").format({
      pathname: "127.0.0.1:9990/randomizer.html",
      protocol: "http:",
      slashes: true,
    })
  );
  mainWindow.setMenuBarVisibility(false);
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
};
app.on("ready", createWindow);
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
