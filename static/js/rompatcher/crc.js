/* Rom Patcher JS - CRC32/MD5/SHA-1/checksums calculators v20200926 - Marc Robledo 2016-2020 - http://www.marcrobledo.com/license */

function padZeroes(intVal, nBytes) {
  var hexString = intVal.toString(16);
  while (hexString.length < nBytes * 2) hexString = "0" + hexString;
  return hexString;
}

/* CRC32 - from Alex - https://stackoverflow.com/a/18639999 */
CRC32_TABLE = (function () {
  var c,
    crcTable = [];
  for (var n = 0; n < 256; n++) {
    c = n;
    for (var k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    crcTable[n] = c;
  }
  return crcTable;
})();
function crc32(marcFile, headerSize, ignoreLast4Bytes) {
  var data = headerSize
    ? new Uint8Array(marcFile._u8array.buffer, headerSize)
    : marcFile._u8array;

  var crc = 0 ^ -1;

  var len = ignoreLast4Bytes ? data.length - 4 : data.length;
  for (var i = 0; i < len; i++)
    crc = (crc >>> 8) ^ CRC32_TABLE[(crc ^ data[i]) & 0xff];

  return (crc ^ -1) >>> 0;
}

function getChecksum(marcFile) {
  try {
    return marcFile._u8array.slice(0x10, 0x19);
  } catch (e) {
    return 0;
  }
}
function byteArrayToLong(byteArray) {
  var value = 0;
  for (var i = 0; i <= byteArray.length - 1; i++) {
    value = value * 256 + byteArray[i];
  }
  return value;
}
function modulo(a, b) {
  return a - Math.floor(a / b) * b;
}
function ToUint32(x) {
  return modulo(ToInteger(x), Math.pow(2, 32));
}
function ToInteger(x) {
  x = Number(x);
  return x < 0 ? Math.ceil(x) : Math.floor(x);
}
function ROL(i, b) {
  return ToUint32(((i << b) | (i >>> (32 - b))) >>> 0);
}
function recalculateChecksum(marcFile) {
  let n = 0x00001000;
  seed = 0xdf26f436;
  t1 = t2 = t3 = t4 = t5 = t6 = seed;
  while (n < 0x00001000 + 0x00100000) {
    d =
      byteArrayToLong([
        Number(marcFile._u8array[n]),
        Number(marcFile._u8array[n + 1]),
        Number(marcFile._u8array[n + 2]),
        Number(marcFile._u8array[n + 3]),
      ]) >>> 0;
    if (ToUint32(t6 + d) < t6) {
      t4 += 1 >>> 0;
      t4 = ToUint32(t4);
    }
    t6 += d >>> 0;
    t6 = ToUint32(t6);
    t3 = (t3 ^ d) >>> 0;
    r = ROL(d, d & 0x1f) >>> 0;
    t5 += r >>> 0;
    t5 = ToUint32(t5);
    if (t2 > d) {
      t2 = (t2 ^ r) >>> 0;
    } else {
      t2 = (t2 ^ t6 ^ d) >>> 0;
    }
    t1 +=
      (byteArrayToLong([
        marcFile._u8array[0x40 + 0x0710 + (n & 0xff)],
        marcFile._u8array[0x40 + 0x0710 + ((n & 0xff) + 1)],
        marcFile._u8array[0x40 + 0x0710 + ((n & 0xff) + 2)],
        marcFile._u8array[0x40 + 0x0710 + ((n & 0xff) + 3)],
      ]) ^
        d) >>>
      0;
    t1 = ToUint32(t1);

    n = n + 4;
  }
  crc = [];
  crc[0] = (t6 ^ t4 ^ t3) >>> 0;
  crc[1] = (t5 ^ t2 ^ t1) >>> 0;

  return crc;
}
function toBytesInt32(num) {
  arr = new ArrayBuffer(4); // an Int32 takes 4 bytes
  view = new DataView(arr);
  view.setUint32(0, num, false); // byteOffset = 0; litteEndian = false
  return arr;
}
function updateChecksum(marcFile, newChecksum) {
  marcFile.seek(0x10);
  marcFile.writeBytes(new Uint8Array(toBytesInt32(newChecksum[0])));
  marcFile.seek(0x14);
  marcFile.writeBytes(new Uint8Array(toBytesInt32(newChecksum[1])));
}

function fixChecksum(marcFile) {
  var newChecksum = recalculateChecksum(marcFile);
  updateChecksum(marcFile, newChecksum);
}
