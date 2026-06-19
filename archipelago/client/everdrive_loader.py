"""USB flashcart transports for the DK64 Archipelago client."""

from __future__ import annotations

import struct
from typing import List, Tuple

from archipelago.client import d2xx
from archipelago.client.common import DK64MemoryMap
from archipelago.client.emu_loader import sanitize_and_trim

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

DATATYPE_TEXT = 0x01
DATATYPE_HEARTBEAT = 0x05
DATATYPE_RDRAM_READ = 0x30
DATATYPE_RDRAM_WRITE = 0x31
DATATYPE_RDRAM_DATA = 0x32
DATATYPE_RDRAM_ACK = 0x33
RDRAM_SIZE = 0x800000


class EverdriveError(Exception):
    """Raised on a USB framing/transport error talking to a flashcart."""


def _align2(value: int) -> int:
    """Round up to a multiple of 2 (flashcart FIFOs transfer 16-bit units)."""
    return (value + 1) & ~1


class _UsbInfoStub:
    """Stand-in for ``EmulatorInfo`` so ``n64_client.emulator_info.id.name`` works."""

    def __init__(self, name: str):
        """Capture the backend's display name."""
        self.id = type("_Id", (), {"name": name})()


class _N64UsbBridgeClient:
    """Shared logic for the USB flashcart backends."""

    DISPLAY_NAME = "USB"

    def __init__(self):
        """Initialise an unconnected client."""
        self._device = None
        self.connected = False
        self.emulator_info = _UsbInfoStub(self.DISPLAY_NAME)

    # framing primitives

    def _send(self, datatype: int, payload: bytes):
        raise NotImplementedError

    def _recv(self, expected_type: int) -> bytes:
        raise NotImplementedError

    @staticmethod
    def _device_matches(dev) -> bool:
        raise NotImplementedError

    # device discovery / lifecycle

    @classmethod
    def cart_present(cls) -> bool:
        """Cheaply probe whether this cart looks connected, for auto-detection."""
        try:
            return any(cls._device_matches(dev) for dev in d2xx.list_devices())
        except Exception:
            return False

    def connect(self) -> bool:
        """Open the first matching cart. Returns True on success."""
        if self.is_connected():
            return True
        candidates = [dev for dev in d2xx.list_devices() if self._device_matches(dev)]
        if not candidates:
            logger.info(f"No {self.DISPLAY_NAME} USB device was found. Is the cart connected and the FTDI driver installed?")
            return False

        try:
            self._device = d2xx.D2xxDevice(candidates[0].index)
        except d2xx.FtdiError as exc:
            logger.error(f"{self.DISPLAY_NAME}: {exc}")
            self._device = None
            return False

        self.connected = True
        logger.info(f"Connected to {self.DISPLAY_NAME} over USB")
        print(f"Connected to {self.DISPLAY_NAME} over USB")
        return True

    def disconnect(self):
        """Close the USB device."""
        if self._device is not None:
            try:
                self._device.close()
            except Exception:
                pass
        self._device = None
        self.connected = False

    def is_connected(self) -> bool:
        """Whether a USB device handle is currently open."""
        return self.connected and self._device is not None

    def validate_rom(self) -> bool:
        """Confirm the loaded ROM is a DK64 AP seed and the bridge answers."""
        if not self.is_connected():
            return False
        try:
            return (self.read_u8(DK64MemoryMap.rom_flags) & DK64MemoryMap.rom_flag_ap_status) != 0
        except Exception:
            return False

    def resync(self):
        """Drain any buffered/queued USB data so a fresh exchange starts clean."""
        if self._device is None:
            return
        try:
            self._device.purge()
            for _ in range(64):
                pending = self._device.queue_status()
                if not pending:
                    break
                self._device.read(min(pending, 512))
            self._device.purge()
        except Exception:
            pass

    # ---- memory access (shared) ----

    def read_block(self, address: int, length: int) -> bytes:
        """Read ``length`` bytes of RDRAM starting at ``address`` (logical order)."""
        if length <= 0:
            return b""
        phys = address & 0x7FFFFFFF
        if phys + length > RDRAM_SIZE:
            raise EverdriveError(f"read out of range: 0x{phys:06x}+{length}")
        self._send(DATATYPE_RDRAM_READ, struct.pack(">II", phys, length))
        payload = self._recv(DATATYPE_RDRAM_DATA)
        if len(payload) < length:
            raise EverdriveError(f"short RDRAM read ({len(payload)}/{length})")
        return payload[:length]

    def write_block(self, address: int, data: bytes):
        """Write ``data`` to RDRAM starting at ``address``."""
        data = bytes(data)
        phys = address & 0x7FFFFFFF
        if phys + len(data) > RDRAM_SIZE:
            raise EverdriveError(f"write out of range: 0x{phys:06x}+{len(data)}")
        self._send(DATATYPE_RDRAM_WRITE, struct.pack(">II", phys, len(data)) + data)
        payload = self._recv(DATATYPE_RDRAM_ACK)
        if not payload or payload[0] != 1:
            raise EverdriveError("RDRAM write was not acknowledged")

    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from memory."""
        return self.read_block(address, 1)[0]

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from memory (big-endian)."""
        return int.from_bytes(self.read_block(address, 2), "big")

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from memory (big-endian)."""
        return int.from_bytes(self.read_block(address, 4), "big")

    def write_u8(self, address: int, value: int):
        """Write an 8-bit unsigned integer to memory."""
        self.write_block(address, bytes([value & 0xFF]))

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to memory (big-endian)."""
        self.write_block(address, (value & 0xFFFF).to_bytes(2, "big"))

    def write_u32(self, address: int, value: int):
        """Write a 32-bit unsigned integer to memory (big-endian)."""
        self.write_block(address, (value & 0xFFFFFFFF).to_bytes(4, "big"))

    def read_bytestring(self, address: int, length: int) -> str:
        """Read a null-terminated bytestring from memory as a Python str."""
        data = self.read_block(address, length)
        result = ""
        for byte_val in data:
            if byte_val == 0:
                break
            result += chr(byte_val)
        return result

    def write_bytestring(self, address: int, data: str):
        """Write a sanitized, null-terminated bytestring to memory."""
        sanitized = sanitize_and_trim(data)
        payload = bytes(ord(ch) & 0xFF for ch in sanitized) + b"\x00"
        self.write_block(address, payload)


_ED_HEADER_MAGIC = b"DMA@"
_ED_TRAILER_MAGIC = b"CMPH"


class EverdriveClient(_N64UsbBridgeClient):
    """EverDrive 64 (V3/X7): UNFLoader ``DMA@`` … ``CMPH`` framing over an FT245 FIFO."""

    DISPLAY_NAME = "EverDrive"

    @staticmethod
    def _device_matches(dev) -> bool:
        return dev.looks_like_everdrive()

    def _send(self, datatype: int, payload: bytes):
        size = len(payload)
        frame = bytearray(_ED_HEADER_MAGIC)
        frame.append(datatype & 0xFF)
        frame += size.to_bytes(3, "big")
        frame += payload
        # The N64 reads ALIGN(size, 2) payload bytes, then the 4 trailer bytes.
        if size & 1:
            frame.append(0)
        frame += _ED_TRAILER_MAGIC
        self._device.write(bytes(frame))

    def _recv_frame(self) -> Tuple[int, bytes]:
        header = self._device.read(8)
        if header[0:4] != _ED_HEADER_MAGIC:
            self._device.purge()
            raise EverdriveError(f"bad USB frame header: {header[0:4]!r}")
        datatype = header[4]
        size = int.from_bytes(header[5:8], "big")
        # N64 -> PC frames align (payload + trailer) as a unit to 2 bytes.
        body = self._device.read(_align2(size + 4))
        payload = body[:size]
        if body[size : size + 4] != _ED_TRAILER_MAGIC:
            self._device.purge()
            raise EverdriveError("bad USB frame trailer")
        return datatype, bytes(payload)

    def _recv(self, expected_type: int) -> bytes:
        for _ in range(8):
            datatype, payload = self._recv_frame()
            if datatype == expected_type:
                return payload
            if datatype in (DATATYPE_HEARTBEAT, DATATYPE_TEXT):
                continue
            self._device.purge()
            raise EverdriveError(f"unexpected USB datatype {datatype:#04x}")
        raise EverdriveError("no matching USB response after several frames")


# SC64 USB packet identifiers and the debug command/packet id ('U').
_SC64_CMD = b"CMD"
_SC64_CMP = b"CMP"
_SC64_ERR = b"ERR"
_SC64_PKT = b"PKT"
_SC64_DEBUG_ID = ord("U")  # CMD_DEBUG_WRITE and USB_PACKET_DEBUG


class SC64Client(_N64UsbBridgeClient):
    """SummerCart64: ``CMD``/``CMP``/``PKT`` command protocol over an FT232H.

    Datatype + size are carried in a 4-byte header inside the debug payload, the
    way UNFLoader and libdragon's SC64 driver do it.
    """

    DISPLAY_NAME = "SC64"

    def __init__(self):
        """Initialise, with a queue for async PKTs seen while awaiting a CMP."""
        super().__init__()
        self._pending: List[Tuple[int, bytes]] = []

    @staticmethod
    def _device_matches(dev) -> bool:
        return dev.looks_like_sc64()

    def disconnect(self):
        """Close the device and drop any queued packets."""
        self._pending = []
        super().disconnect()

    def resync(self):
        """Drop queued packets, then drain the USB buffers like the base class."""
        self._pending = []
        super().resync()

    def _read_packet(self) -> Tuple[bytes, int, bytes]:
        """Read one SC64 USB packet: identifier(3) + id(1) + len(4 BE) + data."""
        header = self._device.read(8)
        ident = bytes(header[0:3])
        pkt_id = header[3]
        length = int.from_bytes(header[4:8], "big")
        data = self._device.read(length) if length else b""
        return ident, pkt_id, bytes(data)

    def _send(self, datatype: int, payload: bytes):
        size = len(payload)
        self._device.write(_SC64_CMD + bytes([_SC64_DEBUG_ID]) + struct.pack(">II", datatype, size) + bytes(payload))
        # Consume the command completion, stashing any async PKT that races ahead.
        for _ in range(16):
            ident, pkt_id, data = self._read_packet()
            if ident == _SC64_CMP:
                return
            if ident == _SC64_ERR:
                self._device.purge()
                raise EverdriveError("SC64 command returned an error")
            if ident == _SC64_PKT:
                self._pending.append((pkt_id, data))
                continue
            self._device.purge()
            raise EverdriveError(f"unexpected SC64 packet {ident!r}")
        raise EverdriveError("SC64: no command completion received")

    def _recv(self, expected_type: int) -> bytes:
        for _ in range(16):
            if self._pending:
                pkt_id, data = self._pending.pop(0)
            else:
                ident, pkt_id, data = self._read_packet()
                if ident in (_SC64_CMP, _SC64_ERR):
                    continue  # stray completion; ignore
                if ident != _SC64_PKT:
                    self._device.purge()
                    raise EverdriveError(f"unexpected SC64 packet {ident!r}")
            if pkt_id != _SC64_DEBUG_ID or len(data) < 4:
                continue
            header = int.from_bytes(data[0:4], "big")
            datatype = (header >> 24) & 0xFF
            size = header & 0xFFFFFF
            if datatype == expected_type:
                return data[4 : 4 + size]
            if datatype in (DATATYPE_HEARTBEAT, DATATYPE_TEXT):
                continue
        raise EverdriveError("SC64: no matching response after several packets")
