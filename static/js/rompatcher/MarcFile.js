/* MODDED VERSION OF MarcFile.js v20181020 - Marc Robledo 2014-2018 - http://www.marcrobledo.com/license */

function MarcFile(source, onLoad) {
  if (typeof source === "object" && source.files)
    /* get first file only if source is input with multiple files */
    source = source.files[0];

  this.littleEndian = false;
  this.offset = 0;
  this._lastRead = null;

  if (typeof source === "object" && source.name && source.size) {
    /* source is file */
    if (typeof window.FileReader !== "function")
      throw new Error("Incompatible Browser");

    this.fileName = source.name;
    this.fileType = source.type;
    this.fileSize = source.size;

    this._fileReader = new FileReader();
    this._fileReader.marcFile = this;
    this._fileReader.addEventListener(
      "load",
      function () {
        this.marcFile._u8array = new Uint8Array(this.result);
        this.marcFile._dataView = new DataView(this.result);

        if (onLoad) onLoad.call();
      },
      false
    );

    this._fileReader.readAsArrayBuffer(source);
  } else if (
    typeof source === "object" &&
    typeof source.fileName === "string" &&
    typeof source.littleEndian === "boolean"
  ) {
    /* source is MarcFile */
    this.fileName = source.fileName;
    this.fileType = source.fileType;
    this.fileSize = source.fileSize;

    var ab = new ArrayBuffer(source);
    this._u8array = new Uint8Array(this.fileType);
    this._dataView = new DataView(this.fileType);

    source.copyToFile(this, 0);
    if (onLoad) onLoad.call();
  } else if (
    typeof source === "object" &&
    typeof source.byteLength === "number"
  ) {
    /* source is ArrayBuffer or TypedArray */
    this.fileName = "file.bin";
    this.fileType = "application/octet-stream";
    this.fileSize = source.byteLength;

    if (typeof source.buffer !== "undefined") source = source.buffer;
    this._u8array = new Uint8Array(source);
    this._dataView = new DataView(source);

    if (onLoad) onLoad.call();
  } else if (typeof source === "number") {
    /* source is integer (new empty file) */
    this.fileName = "file.bin";
    this.fileType = "application/octet-stream";
    this.fileSize = source;

    var ab = new ArrayBuffer(source);
    this._u8array = new Uint8Array(ab);
    this._dataView = new DataView(ab);

    if (onLoad) onLoad.call();
  } else {
    throw new Error("Invalid source");
  }
}
MarcFile.IS_MACHINE_LITTLE_ENDIAN = (function () {
  /* https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView#Endianness */
  var buffer = new ArrayBuffer(2);
  new DataView(buffer).setInt16(0, 256, true /* littleEndian */);
  // Int16Array uses the platform's endianness.
  return new Int16Array(buffer)[0] === 256;
})();

MarcFile.prototype.convert = function () {
  function convertchunk(chunk, byteswp, wordswp) {
    output = [chunk[0], chunk[1], chunk[2], chunk[3]];
    if (byteswp == true) {
      output[0] = chunk[1];
      output[1] = chunk[0];
      output[2] = chunk[3];
      output[3] = chunk[2];
    }
    if (wordswp == true) {
      output[0] = chunk[3];
      output[1] = chunk[2];
      output[2] = chunk[1];
      output[3] = chunk[0];
    }
    return output;
  }

  magic = [
    this._u8array[0],
    this._u8array[1],
    this._u8array[2],
    this._u8array[3],
  ];
  validate = [
    this._u8array[0],
    this._u8array[1],
    this._u8array[2],
    this._u8array[3],
  ];
  first = magic[0];
  if (
    validate.sort().toString() != [0x37, 0x12, 0x40, 0x80].sort().toString()
  ) {
    throw new Error("Invalid Rom");
  }
  byteswapped = [0x37, 0x12].includes(first);
  wordswapped = [0x40, 0x12].includes(first);
  convert = false;
  if (byteswapped == false && wordswapped == false) {
    console.log("z64")
  } else if (byteswapped == true && wordswapped == false) {
    console.log("v64")
    convert = true;
  } else if (byteswapped == false && wordswapped == true) {
    console.log("n64")
    convert = true;
  } else if (byteswapped == true && wordswapped == true) {
    console.log("v64+n64")
    convert = true;
  }
  if (convert == true) {
    this.seek(0);
    resp = convertchunk(magic, byteswapped, wordswapped);
    this.writeU8(resp[0]);
    this.writeU8(resp[1]);
    this.writeU8(resp[2]);
    this.writeU8(resp[3]);
    position = 4;
    while (true) {
      data = [
        this._u8array[position],
        this._u8array[position + 1],
        this._u8array[position + 2],
        this._u8array[position + 3],
      ];
      if (this._u8array[position + 4] == null) {
        break;
      }
      converted_chunk = convertchunk(data, byteswapped, wordswapped);
      this.writeU8(converted_chunk[0]);
      this.writeU8(converted_chunk[1]);
      this.writeU8(converted_chunk[2]);
      this.writeU8(converted_chunk[3]);
      position += 4;
    }
    position = 4;
    this.seek(0);
  }
};

MarcFile.prototype.seek = function (offset) {
  this.offset = offset;
};
MarcFile.prototype.skip = function (nBytes) {
  this.offset += nBytes;
};
MarcFile.prototype.isEOF = function () {
  return !(this.offset < this.fileSize);
};

MarcFile.prototype.slice = function (offset, len) {
  len = len || this.fileSize - offset;

  var newFile;

  if (typeof this._u8array.buffer.slice !== "undefined") {
    newFile = new MarcFile(0);
    newFile.fileSize = len;
    newFile._u8array = new Uint8Array(
      this._u8array.buffer.slice(offset, offset + len)
    );
  } else {
    newFile = new MarcFile(len);
    this.copyToFile(newFile, offset, len, 0);
  }
  newFile.fileName = this.fileName;
  newFile.fileType = this.fileType;
  newFile.littleEndian = this.littleEndian;
  return newFile;
};

MarcFile.prototype.copyToFile = function (
  target,
  offsetSource,
  len,
  offsetTarget
) {
  if (typeof offsetTarget === "undefined") offsetTarget = offsetSource;

  len = len || this.fileSize - offsetSource;

  for (var i = 0; i < len; i++) {
    target._u8array[offsetTarget + i] = this._u8array[offsetSource + i];
  }
};

MarcFile.prototype.save = function () {
  var blob;
  try {
    blob = new Blob([this._u8array], { type: this.fileType });
  } catch (e) {
    //old browser, use BlobBuilder
    window.BlobBuilder =
      window.BlobBuilder ||
      window.WebKitBlobBuilder ||
      window.MozBlobBuilder ||
      window.MSBlobBuilder;
    if (e.name === "InvalidStateError" && window.BlobBuilder) {
      var bb = new BlobBuilder();
      bb.append(this._u8array.buffer);
      blob = bb.getBlob(this.fileType);
    } else {
      throw new Error("Incompatible Browser");
    }
  }
  saveAs(blob, this.fileName);
};

MarcFile.prototype.readU8 = function () {
  this._lastRead = this._u8array[this.offset];

  this.offset++;
  return this._lastRead;
};
MarcFile.prototype.readU16 = function () {
  if (this.littleEndian)
    this._lastRead =
      this._u8array[this.offset] + (this._u8array[this.offset + 1] << 8);
  else
    this._lastRead =
      (this._u8array[this.offset] << 8) + this._u8array[this.offset + 1];

  this.offset += 2;
  return this._lastRead >>> 0;
};
MarcFile.prototype.readU24 = function () {
  if (this.littleEndian)
    this._lastRead =
      this._u8array[this.offset] +
      (this._u8array[this.offset + 1] << 8) +
      (this._u8array[this.offset + 2] << 16);
  else
    this._lastRead =
      (this._u8array[this.offset] << 16) +
      (this._u8array[this.offset + 1] << 8) +
      this._u8array[this.offset + 2];

  this.offset += 3;
  return this._lastRead >>> 0;
};
MarcFile.prototype.readU32 = function () {
  if (this.littleEndian)
    this._lastRead =
      this._u8array[this.offset] +
      (this._u8array[this.offset + 1] << 8) +
      (this._u8array[this.offset + 2] << 16) +
      (this._u8array[this.offset + 3] << 24);
  else
    this._lastRead =
      (this._u8array[this.offset] << 24) +
      (this._u8array[this.offset + 1] << 16) +
      (this._u8array[this.offset + 2] << 8) +
      this._u8array[this.offset + 3];

  this.offset += 4;
  return this._lastRead >>> 0;
};

MarcFile.prototype.readBytes = function (len) {
  this._lastRead = new Array(len);
  for (var i = 0; i < len; i++) {
    this._lastRead[i] = this._u8array[this.offset + i];
  }

  this.offset += len;
  return this._lastRead;
};

MarcFile.prototype.readString = function (len) {
  this._lastRead = "";
  for (
    var i = 0;
    i < len &&
    this.offset + i < this.fileSize &&
    this._u8array[this.offset + i] > 0;
    i++
  )
    this._lastRead =
      this._lastRead + String.fromCharCode(this._u8array[this.offset + i]);

  this.offset += len;
  return this._lastRead;
};

MarcFile.prototype.writeU8 = function (u8) {
  this._u8array[this.offset] = u8;

  this.offset++;
};
MarcFile.prototype.writeU16 = function (u16) {
  if (this.littleEndian) {
    this._u8array[this.offset] = u16 & 0xff;
    this._u8array[this.offset + 1] = u16 >> 8;
  } else {
    this._u8array[this.offset] = u16 >> 8;
    this._u8array[this.offset + 1] = u16 & 0xff;
  }

  this.offset += 2;
};
MarcFile.prototype.writeU24 = function (u24) {
  if (this.littleEndian) {
    this._u8array[this.offset] = u24 & 0x0000ff;
    this._u8array[this.offset + 1] = (u24 & 0x00ff00) >> 8;
    this._u8array[this.offset + 2] = (u24 & 0xff0000) >> 16;
  } else {
    this._u8array[this.offset] = (u24 & 0xff0000) >> 16;
    this._u8array[this.offset + 1] = (u24 & 0x00ff00) >> 8;
    this._u8array[this.offset + 2] = u24 & 0x0000ff;
  }

  this.offset += 3;
};
MarcFile.prototype.writeU32 = function (u32) {
  if (this.littleEndian) {
    this._u8array[this.offset] = u32 & 0x000000ff;
    this._u8array[this.offset + 1] = (u32 & 0x0000ff00) >> 8;
    this._u8array[this.offset + 2] = (u32 & 0x00ff0000) >> 16;
    this._u8array[this.offset + 3] = (u32 & 0xff000000) >> 24;
  } else {
    this._u8array[this.offset] = (u32 & 0xff000000) >> 24;
    this._u8array[this.offset + 1] = (u32 & 0x00ff0000) >> 16;
    this._u8array[this.offset + 2] = (u32 & 0x0000ff00) >> 8;
    this._u8array[this.offset + 3] = u32 & 0x000000ff;
  }

  this.offset += 4;
};

MarcFile.prototype.writeBytes = function (a) {
  if (a.type == "bytes") {
    a = new Uint8Array(a);
  }
  for (var i = 0; i < a.length; i++) this._u8array[this.offset + i] = a[i];

  this.offset += a.length;
};

MarcFile.prototype.writeString = function (str, len) {
  len = len || str.length;
  for (var i = 0; i < str.length && i < len; i++)
    this._u8array[this.offset + i] = str.charCodeAt(i);

  for (; i < len; i++) this._u8array[this.offset + i] = 0x00;

  this.offset += len;
};
