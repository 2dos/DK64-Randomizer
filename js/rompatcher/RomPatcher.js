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
  webWorkerCrc = new Worker("./js/rompatcher/worker_crc.js");
  webWorkerCrc.onmessage = (event) => {
    romFile._u8array = event.data.u8array;
    romFile._dataView = new DataView(event.data.u8array.buffer);
  };
} catch (e) {}

/* Shortcuts */
function addEvent(e, ev, f) {
  e.addEventListener(ev, f, false);
}

/* initialize app */
addEvent(window, "load", function () {
  fetchPatch("./patches/shrink-dk64.bps");
  addEvent(document.getElementById("input-file-rom_1"), "change", function () {
    romFile = new MarcFile(this, _parseROM);
  });
  addEvent(document.getElementById("input-file-rom_2"), "change", function () {
    romFile = new MarcFile(this, _parseROM);
  });
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

// Patches
function fetchPatch(uri) {
  var patchURI = decodeURI(uri.replace(/\#.*?$/, ""));
  fetch(patchURI)
    .then((result) => result.arrayBuffer()) // Gets the response and returns it as a blob
    .then((arrayBuffer) => {
      patchFile = new MarcFile(arrayBuffer);
      _readPatchFile();
    });
}

function _readPatchFile() {
  patchFile.littleEndian = false;
  patch = parseBPSFile(patchFile);
}

function preparePatchedRom(originalRom, patchedRom, binary_data) {
  patchedRom.fileName = originalRom.fileName =
    "dk64-randomizer-" + document.getElementById("seed").value + ".z64";
  patchedRom.fileType = originalRom.fileType;
  patchedRom.save();
  $("#patchprogress").width("100%");
  $("#progress-text").text("ROM has been patched");
  setTimeout(function () {
    $("#progressmodal").modal("hide");
    $("#patchprogress").width("0%");
    $("#progress-text").text("");
    progression_clicked();
  }, 2000);
}
function expand_rom_size(size) {
  patchedRom._u8array = concatTypedArrays(
    patchedRom._u8array,
    new Uint8Array(size)
  );
}
function concatTypedArrays(a, b) {
  // a, b TypedArray of same type
  var c = new a.constructor(a.length + b.length);
  c.set(a, 0);
  c.set(b, a.length);
  return c;
}

function apply_bps_javascript() {
  if (patch && romFile) {
    var romFile_internal = new MarcFile(romFile._u8array);
    var patchFile_internal = new MarcFile(patchFile._u8array);
    bps = parseBPSFile(patchFile_internal);
    try {
      patchedRom = bps.apply(romFile_internal, false);
    } catch (evt) {
      errorMessage = evt.message;
      console.log(evt)
    }
  }
}
