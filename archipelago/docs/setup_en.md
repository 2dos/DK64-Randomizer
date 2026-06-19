# Donkey Kong 64 Randomizer Setup Guide

Please check the [Archipelago page on the DK64 Randomizer wiki.](https://dk64randomizer.com/wiki/index.html?title=Archipelago#setup-guide).

## Real N64 Hardware (USB flashcart)

You can play on a real N64 with a USB flashcart instead of an emulator. The same DK64
Client connects to the console over the cart's USB port and reads/writes the game's
memory exactly as it does for an emulator. The client auto-detects a connected cart — no
extra flag is needed.

**Supported carts:**
- **EverDrive 64** V3 (OS 3.06 or newer) and X7. The X5 has no USB port and the V2.5 is
  not supported.
- **SummerCart64 (SC64)**. *Implemented but not yet tested*

### 1. Install the FTDI D2XX driver

Both carts talk over FTDI USB (the EverDrive uses an FT245 chip, the SC64 an FT232H), so
the PC needs FTDI's **D2XX** driver. This is the same driver UNFLoader and the cart's own
USB tools use.`

**Windows** — install FTDI's [CDM driver package](https://ftdichip.com/drivers/d2xx-drivers/).
Do **not** run Zadig or replace the driver with WinUSB; that breaks D2XX.

**Linux** — install `libftd2xx` and allow your user to access the device:

```bash
# Driver (Debian/Ubuntu/Mint example; or grab the tarball from ftdichip.com):
sudo apt install libftd2xx2        # provides libftd2xx.so

# Let your user open the cart without root, for any FTDI device (VID 0403):
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="0403", MODE="0666", GROUP="plugdev"' \
  | sudo tee /etc/udev/rules.d/99-n64-flashcart.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

If the kernel's `ftdi_sio` virtual-COM-port driver grabs the cart (a `/dev/ttyUSB*` appears
and the client can't see the device), it is holding the FTDI interface D2XX needs. Unplug
and replug the cable, or `sudo modprobe -r ftdi_sio`.

**macOS** — install FTDI's `libftd2xx` dylib from [ftdichip.com](https://ftdichip.com/drivers/d2xx-drivers/).

### 2. Load the ROM and play

1. Patch your `.chunky` and place the `.z64` in your SD card. 
2. Boot the patched ROM on the console from the cart, with the USB cable connected to your
   PC, and play to the **title screen**.
3. Launch the **DK64 Client** and connect to your Archipelago server as normal — a connected
   cart is auto-detected.

You should see `Connected to <cart> over USB` followed by `<cart> connected to ROM!`.

### Troubleshooting

- *"No … USB device was found"* — check the USB cable, that the FTDI driver is installed,
  and that the cart is powered on.
- *"Could not load the FTDI D2XX driver"* — the D2XX library isn't installed (see step 1).
- *"Failed to open … already in use"* — another program (UNFLoader, the cart's USB tools, a
  serial monitor) is holding the device; close it.
- The cart disappears from USB / a `/dev/ttyUSB*` shows up (Linux) — `ftdi_sio` claimed it;
  replug the cable or `modprobe -r ftdi_sio` (see step 1).
- The client keeps *"waiting … for a valid ROM"* — make sure the booted ROM is this
  multiworld's Archipelago seed and the game has reached the title screen.
