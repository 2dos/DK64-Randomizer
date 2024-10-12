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

// Function to generate a GIF frame from the image with transparency applied
function genGIFFrame(image, cap = 128) {
  const canvas = document.createElement("canvas"); // Create a canvas element for rendering the image
  const ctx = canvas.getContext("2d");
  canvas.width = image.width;
  canvas.height = image.height;
  ctx.drawImage(image, 0, 0); // Draw image on canvas

  // Get image data (RGBA) for manipulation
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const alpha = imageData.data; // Alpha channel manipulation

  // Apply transparency cap (255 where alpha is below the cap)
  for (let i = 0; i < alpha.length; i += 4) {
    if (alpha[i + 3] <= cap) {
      alpha[i + 3] = 255;
    }
  }
  ctx.putImageData(imageData, 0, 0);
  return canvas; // Return the updated canvas
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
      gifFrames.push(genGIFFrame(canvas, mode === "loading-dead" ? 10 : 128)); // Handle GIF frames
    }
  }

  // TODO: Handle GIF creation logic if necessary

  return loadedImages; // Return base64-encoded images
}
