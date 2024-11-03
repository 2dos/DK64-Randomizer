/* Rom Patcher JS v20201106 - Marc Robledo 2016-2020 - http://www.marcrobledo.com/license */

var romFile,
  patchFile,
  patch,
  romFile1,
  romFile2,
  tempFile,
  headerSize,
  oldHeader,
  patchedRom;

try {
  webWorkerCrc = new Worker("./static/js/rompatcher/worker_crc.js");
  webWorkerCrc.onmessage = (event) => {
    romFile._u8array = event.data.u8array;
    romFile._dataView = new DataView(event.data.u8array.buffer);
    // We're disabling this here now so we speed up page load
    //apply_conversion();
    boxes = ["input-file-rom", "input-file-rom_1", "input-file-rom_2", "rom", "rom_2", "rom_3"];
    for (var input_box in boxes) {
      try {
        document.getElementById(boxes[input_box]).classList.remove("is-valid");
        document
          .getElementById(boxes[input_box])
          .classList.remove("is-invalid");
      } catch {}
      if (
        ["d44b4fc6", "aa0a5979", "96972d67"].includes(
          padZeroes(crc32(romFile), 4)
        )
      ) {
        try {
          document.getElementById(boxes[input_box]).title =
            "CRC32: " + padZeroes(crc32(romFile), 4);
          document.getElementById(boxes[input_box]).classList.add("is-valid");
        } catch {}
      } else {
        try {
          document.getElementById(boxes[input_box]).title =
            "CRC32: " + padZeroes(crc32(romFile), 4);
          document.getElementById(boxes[input_box]).classList.add("is-invalid");
          generateToast("ROM is invalid and is unsupported by the randomizer.", true);
        } catch {}
      }
    }
  };
} catch (e) {}

/* Shortcuts */
function addEvent(e, ev, f) {
  e.addEventListener(ev, f, false);
}

/* initialize app */
addEvent(window, "load", function () {
  try {
    addEvent(document.getElementById("input-file-rom"), "change", async function () {
      romFile = new MarcFile(this, _parseROM);
    });
  } catch {}
  try {
    addEvent(
      document.getElementById("input-file-rom_1"),
      "change",
      async function () {
        romFile = new MarcFile(this, _parseROM);
      }
    );
  } catch {}
  try {
    addEvent(
      document.getElementById("input-file-rom_2"),
      "change",
      async function () {
        romFile = new MarcFile(this, _parseROM);
      }
    );
  } catch {}
});

function _parseROM() {
  updateChecksums(romFile, 0);
  getChecksum(romFile);
}

function updateChecksums(file, startOffset, force) {
  if (file === romFile && file.fileSize > 33554432 && !force) {
    return false;
  }

  webWorkerCrc.postMessage(
    { u8array: file._u8array, startOffset: startOffset },
    [file._u8array.buffer]
  );
}


function apply_xdelta(patchFile){
  u8_array = new Uint8Array(patchFile)
  patch=parseVCDIFF(new MarcFile(patchFile));
  var romFile_internal = new MarcFile(romFile._u8array);
  patchedRom = patch.apply(romFile_internal, false);
}

function apply_conversion() {
  console.log("Converting Rom");
  romFile.convert();
}

function getDate() {
  return new Date().toUTCString();
}
