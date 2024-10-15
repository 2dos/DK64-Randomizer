// Class to store the image information
class ImageInfo {
  constructor(name, format, table, index, width, height, mode) {
    this.name = name;
    this.format = format;
    this.table = table;
    this.index = index;
    this.width = width;
    this.height = height;
    this.mode = mode;
  }
}
// Helper function to create a 16-bit integer in little-endian format
function uint16LE(value) {
  return [value & 0xff, (value >> 8) & 0xff];
}

// Helper function to create a 32-bit integer in little-endian format
function uint32LE(value) {
  return [value & 0xff, (value >> 8) & 0xff, (value >> 16) & 0xff, (value >> 24) & 0xff];
}

// Helper function to convert canvas to RGB pixel data
function canvasToRGBData(canvas) {
  const ctx = canvas.getContext("2d");
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  return imgData.data;
}

// Function to create the GIF from frames
function createGIF(frames, width, height, delay = 100) {
  const GIF_HEADER = [
    // GIF Signature
    0x47, 0x49, 0x46, 0x38, 0x39, 0x61, // "GIF89a" signature

    // Logical Screen Descriptor (Screen width, height, GCT flag, color resolution, sort flag, size of GCT)
    ...uint16LE(width), ...uint16LE(height), 0xf7, 0x00, 0x00,

    // Global Color Table (256 colors RGB)
    // This is a simple grayscale color table for demonstration, you can change it to a custom palette
    ...Array.from({ length: 256 * 3 }, (_, i) => i % 256),

    // Application Extension Block for animation
    0x21, 0xff, 0x0b, // Extension Introducer, Application Label
    0x4e, 0x45, 0x54, 0x53, 0x43, 0x41, 0x50, 0x45, 0x32, 0x2e, 0x30, // "NETSCAPE2.0"
    0x03, 0x01, 0x00, 0x00, 0x00 // Data Sub-blocks, Loop count (0 means infinite)
  ];

  const GIF_FOOTER = [0x3b]; // GIF trailer

  let gifData = [...GIF_HEADER]; // Initialize with header data

  for (let frame of frames) {
    // Graphic Control Extension (for frame delay and transparency)
    gifData.push(
      0x21, 0xf9, 0x04, 0x08, ...uint16LE(delay), 0x00, 0x00 // Delay and other GCE params
    );

    // Image Descriptor (frame position and size)
    gifData.push(
      0x2c, // Image Separator
      0x00, 0x00, 0x00, 0x00, // Image Position X, Y (0,0)
      ...uint16LE(width), ...uint16LE(height), // Image width and height
      0x00 // No local color table, no interlace
    );

    // Image Data (compressed LZW data)
    const imageData = canvasToRGBData(frame); // Convert the canvas frame to RGB data
    const lzwData = encodeLZW(imageData, width * height); // LZW encoding of the image

    gifData.push(0x08); // LZW minimum code size
    gifData.push(...lzwData); // Add the LZW-encoded image data
    gifData.push(0x00); // Block terminator
  }

  gifData.push(...GIF_FOOTER); // Add the GIF footer

  // Convert the binary array to a base64 string and return the result
  const binaryData = new Uint8Array(gifData);
  const gifBase64 = btoa(String.fromCharCode(...binaryData));
  return `data:image/gif;base64,${gifBase64}`;
}

// Helper function to encode image data using LZW compression (GIF requirement)
function encodeLZW(imageData, pixelCount) {
  // Basic LZW encoding implementation for GIFs
  // This will compress the image data, but LZW is a bit complex.
  // You could use a library or a simple implementation, but here’s a basic idea:

  const clearCode = 256;
  const endOfInformation = 257;

  let dictionary = [];
  for (let i = 0; i < 256; i++) {
    dictionary[[i]] = i;
  }

  let codeStream = [];
  let currentCode = [];

  for (let i = 0; i < pixelCount; i++) {
    const pixel = imageData[i];

    if (dictionary[currentCode.concat([pixel])] !== undefined) {
      currentCode.push(pixel);
    } else {
      codeStream.push(dictionary[currentCode]);
      dictionary[currentCode.concat([pixel])] = Object.keys(dictionary).length;
      currentCode = [pixel];
    }
  }

  if (currentCode.length) {
    codeStream.push(dictionary[currentCode]);
  }

  codeStream.push(endOfInformation);

  // Convert codes to bytes
  let byteStream = [];
  for (let code of codeStream) {
    byteStream.push(code & 0xff, (code >> 8) & 0xff);
  }

  return byteStream;
}

// Usage example with canvases:
function generateGifFromFrames(canvasFrames) {
  const width = canvasFrames[0].width;
  const height = canvasFrames[0].height;
  const gifDataURL = createGIF(canvasFrames, width, height, 100); // 100ms delay per frame
  return gifDataURL;
}

// Main function to load hash images
function get_hash_images(type = "local", mode = "hash") {
  // List of images with properties like format, size, etc.
  const images = [
    new ImageInfo("bongos", "rgba16", 25, 5548, 40, 40, "hash"),
    new ImageInfo("crown", "rgba16", 25, 5893, 44, 44, "hash"),
    new ImageInfo("dk_coin", "rgba16", 7, 500, 48, 44, "hash"),
    new ImageInfo("fairy", "rgba32", 25, 5869, 32, 32, "hash"),
    new ImageInfo("guitar", "rgba16", 25, 5547, 40, 40, "hash"),
    new ImageInfo("nin_coin", "rgba16", 25, 5912, 44, 44, "hash"),
    new ImageInfo("orange", "rgba16", 7, 309, 32, 32, "hash"),
    new ImageInfo("rainbow_coin", "rgba16", 25, 5963, 48, 44, "hash"),
    new ImageInfo("rw_coin", "rgba16", 25, 5905, 44, 44, "hash"),
    new ImageInfo("saxophone", "rgba16", 25, 5549, 40, 40, "hash"),
  ];

  // Append additional fairy and explosion images to the list
  for (let x = 0; x < 0x8; x++) {
    images.push(
      new ImageInfo(
        `Fairy Image ${x}`,
        "rgba32",
        25,
        0x16ed + x,
        32,
        32,
        "loading-fairy"
      )
    );
  }
  for (let x = 0; x < 0x1b; x++) {
    images.push(
      new ImageInfo(
        `Explosion Image ${x}`,
        "rgba32",
        25,
        0x1539 + x,
        32,
        32,
        "loading-dead"
      )
    );
  }
  const ptrOffset = 0x101c50; // Pointer offset for ROM access
  let loadedImages = [];
  let gifFrames = [];

  // Set romType to the provided romFile (direct access)
  let romType = romFile;
  
  // Filter images based on the mode ('hash', 'loading-fairy', or 'loading-dead')
  let filteredList = images.filter((image) => image.mode === mode);
  console.log(filteredList)
  // Loop through filtered images and load data from the ROM
  for (let imageInfo of filteredList) {
    // Seek to the pointer table entry for the current image
    romType.seek(ptrOffset + imageInfo.table * 4);
    let ptrTable = ptrOffset + new DataView(Uint8Array.from(romType.readBytes(4)).buffer).getUint32(0, false);
    // Read Bytes comes back as comma seperated bytes, merge them together
    // Seek to the start and end of the image data
    romType.seek(ptrTable + imageInfo.index * 4);
    let imgStart = ptrOffset + new DataView(Uint8Array.from(romType.readBytes(4)).buffer).getUint32(0, false);
    romType.seek(ptrTable + (imageInfo.index + 1) * 4);
    let imgEnd = ptrOffset + new DataView(Uint8Array.from(romType.readBytes(4)).buffer).getUint32(0, false);
    let imgSize = imgEnd - imgStart;
    // Read the image data from the ROM
    romType.seek(imgStart);
    let imgData = Uint8Array.from(romType.readBytes(imgSize));
    // Decompress image data if necessary
    let dec = imgData;
    if (imageInfo.table === 25) {
      dec = new pako.inflate(imgData); // Use pako for zlib decompression
    }
    // Create canvas and draw image based on format (rgba16/rgba32)
    let canvas = document.createElement("canvas");
    canvas.width = imageInfo.width;
    canvas.height = imageInfo.height;
    let ctx = canvas.getContext("2d");
    let imgImageData = ctx.createImageData(imageInfo.width, imageInfo.height);
    let pixels = imgImageData.data;

    // Process pixel data based on image format
    for (let pixel = 0; pixel < imageInfo.width * imageInfo.height; pixel++) {
      let start, red, green, blue, alpha;
      if (imageInfo.format === "rgba16") {
        start = pixel * 2;
        let pixelData = (dec[start] << 8) | dec[start + 1];
        red = (((pixelData >> 11) & 0x1f) * 0xff) / 0x1f;
        green = (((pixelData >> 6) & 0x1f) * 0xff) / 0x1f;
        blue = (((pixelData >> 1) & 0x1f) * 0xff) / 0x1f;
        alpha = (pixelData & 1) * 0xff;
      } else if (imageInfo.format === "rgba32") {
        start = pixel * 4;
        red = dec[start];
        green = dec[start + 1];
        blue = dec[start + 2];
        alpha = dec[start + 3];
      }
      let pixIndex = pixel * 4;
      pixels[pixIndex] = red;
      pixels[pixIndex + 1] = green;
      pixels[pixIndex + 2] = blue;
      pixels[pixIndex + 3] = alpha;
    }

    ctx.putImageData(imgImageData, 0, 0); // Put image data back to the canvas

    // Save as base64-encoded PNG if in hash mode
    if (mode === "hash") {
      const imgBase64 = canvas.toDataURL("image/png").split(",")[1]; // Get base64 PNG data
      loadedImages.push(imgBase64); // Add image to the list of loaded images
    } else {
      const imgBase64 = canvas.toDataURL("image/png").split(",")[1]; // Get base64 PNG data
      gifFrames.push(imgBase64); // Handle GIF frames
    }
  }
  // TODO: Handle GIF creation logic if necessary
  if (mode !== "hash") {
    return generateGifFromFrames(gifFrames);; // Return GIF data URL
  }
  return loadedImages; // Return base64-encoded images
}
