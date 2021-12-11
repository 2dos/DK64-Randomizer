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
    apply_bps_javascript();
    try {
      document.getElementById("input-file-rom").title =
        "CRC32: " + padZeroes(crc32(romFile), 4);
    } catch {}
    try {
      document.getElementById("input-file-rom_1").title =
        "CRC32: " + padZeroes(crc32(romFile), 4);
    } catch {}
    try {
      document.getElementById("input-file-rom_2").title =
        "CRC32: " + padZeroes(crc32(romFile), 4);
    } catch {}
  };
} catch (e) {}

/* Shortcuts */
function addEvent(e, ev, f) {
  e.addEventListener(ev, f, false);
}

/* initialize app */
addEvent(window, "load", function () {
  fetchPatch("./static/patches/shrink-dk64.bps");
  try {
    addEvent(document.getElementById("input-file-rom"), "change", function () {
      romFile = new MarcFile(this, _parseROM);
    });
  } catch {}
  try {
    addEvent(
      document.getElementById("input-file-rom_1"),
      "change",
      function () {
        romFile = new MarcFile(this, _parseROM);
      }
    );
  } catch {}
  try {
    addEvent(
      document.getElementById("input-file-rom_2"),
      "change",
      function () {
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

function apply_bps_javascript() {
  console.log("Converting Rom");
  romFile.convert();
  console.log("Applying base BPS");
  if (patch && romFile) {
    var romFile_internal = new MarcFile(romFile._u8array);
    var patchFile_internal = new MarcFile(patchFile._u8array);
    bps = parseBPSFile(patchFile_internal);
    try {
      patchedRom = bps.apply(romFile_internal, false);
    } catch (evt) {
      errorMessage = evt.message;
      console.log(evt);
    }
  }
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
