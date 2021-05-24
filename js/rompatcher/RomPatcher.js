/* Rom Patcher JS v20201106 - Marc Robledo 2016-2020 - http://www.marcrobledo.com/license */

let romFile,
  patchFile,
  patch,
  romFile1,
  romFile2,
  tempFile,
  headerSize,
  oldHeader

let webWorkerApply, webWorkerCreate, webWorkerCrc
try {
  webWorkerApply = new Worker('./js/rompatcher/worker_apply.js')
  webWorkerApply.onmessage = (event) => {
    // retrieve arraybuffers back from webworker
    try {
      romFile._u8array = event.data.romFileU8Array
      romFile._dataView = new DataView(romFile._u8array.buffer)
    } catch (err) {}
    patchFile._u8array = event.data.patchFileU8Array
    patchFile._dataView = new DataView(patchFile._u8array.buffer)

    if (event.data.patchedRomU8Array) {
      preparePatchedRom(
        romFile,
        new MarcFile(event.data.patchedRomU8Array.buffer),
        event.data.binary_data
      )
    }
  }

  webWorkerCrc = new Worker('./js/rompatcher/worker_crc.js')
  webWorkerCrc.onmessage = (event) => {
    // document.getElementById("input-file-rom").innerHTML = padZeroes(
    //  event.data.crc32,
    //  4
    // );
    romFile._u8array = event.data.u8array
    romFile._dataView = new DataView(event.data.u8array.buffer)
  }
} catch (e) {}

/* Shortcuts */
function addEvent (e, ev, f) {
  e.addEventListener(ev, f, false)
}

/* initialize app */
addEvent(window, 'load', function () {
  fetchPatch('./patches/shrink-dk64.bps')
  addEvent(document.getElementById('input-file-rom'), 'change', function () {
    romFile = new MarcFile(this, _parseROM)
  })
})

function _parseROM () {
  updateChecksums(romFile, 0)
}

function updateChecksums (file, startOffset, force) {
  if (file === romFile && file.fileSize > 33554432 && !force) {
    return false
  }

  // document.getElementById("input-file-rom").innerHTML = "Calculating...";

  webWorkerCrc.postMessage(
    { u8array: file._u8array, startOffset: startOffset },
    [file._u8array.buffer]
  )
}

// Patches
function fetchPatch (uri) {
  const patchURI = decodeURI(uri.replace(/\#.*?$/, ''))
  fetch(patchURI)
    .then((result) => result.arrayBuffer()) // Gets the response and returns it as a blob
    .then((arrayBuffer) => {
      patchFile = new MarcFile(arrayBuffer)
      _readPatchFile()
    })
}

function _readPatchFile () {
  patchFile.littleEndian = false
  patch = parseBPSFile(patchFile)
}

function preparePatchedRom (originalRom, patchedRom, binary_data) {
  applyASMtoPatchedRom(patchedRom, binary_data)

  // Deal with the security entry
  patchedRom.seek(0x3154)
  patchedRom.writeU8(0)

  // I don't know why we need to do any of this block but it makes the rom work
  patchedRom.seek(0x10)
  patchedRom.writeBytes([0xce, 0xd5, 0xae, 0xbc, 0x3d, 0x46, 0x79, 0x67, 0x00])
  patchedRom.seek(0x200042b)
  patchedRom.writeBytes([0xfe])

  // TODO: We need to move this earlier in the process to modify the rom type
  rom_type(patchedRom._u8array)

  patchedRom.fileName = originalRom.fileName =
    'dk64-randomizer-' + document.getElementById('seed').value + '.z64'
  patchedRom.fileType = originalRom.fileType
  patchedRom.save()
  $('#patchprogress').width('100%')
  $('#progress-text').text('Rom has been patched')
  setTimeout(function () {
    $('#progressmodal').modal('hide')
    progression_clicked()
  }, 2000)
}

function applyASMtoPatchedRom (patchedRom, binary_data) {
  const data = binary_data.split('\n')

  datacap = 0
  for (var i = 0; i < data.length; i++) {
    if (data[i].split(':')[0] > datacap) {
      datacap = data[i].split(':')[0]
    }
  }
  patchedRom._u8array = concatTypedArrays(
    patchedRom._u8array,
    new Uint8Array(3028)
  )

  for (var i = 0; i < data.length; i++) {
    format = data[i].split(':')
    addr = Number(format[0])
    val = Number(format[1])
    if (addr >= 0x72c && addr < 0x72c + 8) {
      // console.log("boot hook code");
      diff = addr - 0x72c
      patchedRom.seek(0x132c + diff)
      patchedRom.writeU8(val)
    } else if (addr >= 0xa30 && addr < 0xa30 + 1696) {
      // console.log("Expansion Pak Draw Code");
      diff = addr - 0xa30
      patchedRom.seek(0x1630 + diff)
      patchedRom.writeU8(val)
    } else if (addr >= 0xde88 && addr < 0xde88 + 3920) {
      // console.log("Expansion Pak Picture");
      diff = addr - 0xde88
      patchedRom.seek(0xea88 + diff)
      patchedRom.writeU8(val)
    } else if (addr >= 0x5dae00 && addr < 0x5dae00 + 0x20000) {
      // console.log("Heap Shrink Space");
      diff = addr - 0x5dae00
      patchedRom.seek(0x2000000 + diff)
      patchedRom.writeU8(val)
    }
  }
}
function concatTypedArrays (a, b) {
  // a, b TypedArray of same type
  const c = new a.constructor(a.length + b.length)
  c.set(a, 0)
  c.set(b, a.length)
  return c
}
function rom_type (val) {
  // Find out what rom type we have
  arr = new Uint8Array(val)
  if ([128, 55, 18, 64].every((v, i) => v === arr.slice(0, 4)[i])) {
    console.log('Already Z64')
  } else if ([64, 85, 55, 128].every((v, i) => v === arr.slice(0, 4)[i])) {
    console.log('N64')
    // TODO: Convert Type
  } else if ([55, 128, 64, 18].every((v, i) => v === arr.slice(0, 4)[i])) {
    console.log('V64')
    // TODO: Convert Type
  } else {
    alert('Invalid Rom Type, can only be Z64, N64, or V64.')
  }
}

function applyPatch (p, r, validateChecksums, binary_data) {
  if (p && r) {
    let error
    $('#patchprogress').width('80%')
    $('#progress-text').text('Applying patches')
    setTimeout(function () {
      for (let retries = 0; retries < 3; retries++) {
        try {
          webWorkerApply.postMessage(
            {
              romFileU8Array: r._u8array,
              patchFileU8Array: patchFile._u8array,
              validateChecksums: validateChecksums,
              binary_data: binary_data
            },
            [r._u8array.buffer, patchFile._u8array.buffer]
          )
          return true
        } catch (err) {
          error = err
        }
      }
    }, 1000)
  }
}
