"""Minimal pure-ctypes wrapper around the FTDI D2XX driver."""

from __future__ import annotations

import ctypes
import platform
from typing import List, Optional

# FT_STATUS return codes
FT_OK = 0

# FT_Purge masks.
FT_PURGE_RX = 1
FT_PURGE_TX = 2

# FTDI USB vendor id
FTDI_VID = 0x0403


class FtdiError(Exception):
    """Raised when the D2XX driver is missing or a D2XX call fails."""


class _DeviceListInfoNode(ctypes.Structure):
    """Mirror of FTDI's FT_DEVICE_LIST_INFO_NODE structure."""

    _fields_ = [
        ("Flags", ctypes.c_uint32),
        ("Type", ctypes.c_uint32),
        ("ID", ctypes.c_uint32),
        ("LocId", ctypes.c_uint32),
        ("SerialNumber", ctypes.c_char * 16),
        ("Description", ctypes.c_char * 64),
        ("ftHandle", ctypes.c_void_p),
    ]


class DeviceInfo:
    """Lightweight description of an enumerated FTDI device."""

    def __init__(self, index: int, node: _DeviceListInfoNode):
        """Capture the fields we use to identify an EverDrive."""
        self.index = index
        self.id = node.ID
        self.vid = (node.ID >> 16) & 0xFFFF
        self.pid = node.ID & 0xFFFF
        self.serial = node.SerialNumber.decode("ascii", "ignore")
        self.description = node.Description.decode("ascii", "ignore")

    def is_ftdi(self) -> bool:
        """Whether this is an FTDI device (the EverDrive's USB chip is FTDI)."""
        return self.vid == FTDI_VID

    def looks_like_everdrive(self) -> bool:
        """Heuristic for an EverDrive 64's USB chip, for safe auto-detection."""

        desc = self.description.upper()
        return self.is_ftdi() and ("245" in desc or "FIFO" in desc or "EVERDRIVE" in desc)

    def looks_like_sc64(self) -> bool:
        """Heuristic for a SummerCart64's USB chip, for safe auto-detection."""

        desc = self.description.upper()
        return self.is_ftdi() and (self.pid == 0x6014 or "SC64" in desc or "SUMMERCART" in desc)


_lib = None


def _candidate_library_names() -> List[str]:
    """Return platform-appropriate D2XX library names to try, in order."""
    system = platform.system()
    if system == "Windows":
        return ["ftd2xx64.dll", "ftd2xx.dll"]
    if system == "Darwin":
        return ["libftd2xx.dylib", "/usr/local/lib/libftd2xx.dylib"]
    return ["libftd2xx.so", "libftd2xx.so.1"]


def _load_library():
    """Load and configure the D2XX shared library, caching the handle."""
    global _lib
    if _lib is not None:
        return _lib

    names = _candidate_library_names()
    loader = ctypes.WinDLL if platform.system() == "Windows" else ctypes.CDLL
    last_error: Optional[Exception] = None
    lib = None
    for name in names:
        try:
            lib = loader(name)
            break
        except OSError as exc:
            last_error = exc
    if lib is None:
        raise FtdiError(
            "Could not load the FTDI D2XX driver (tried: " + ", ".join(names) + "). "
            "Install the FTDI driver for your platform to use EverDrive mode. " + (f"({last_error})" if last_error else "")
        )

    # FT_HANDLE is a void*; FT_STATUS is a uint32. Declare signatures so the
    # calls are correct on every architecture (notably 32-bit).
    handle = ctypes.c_void_p
    status = ctypes.c_uint32
    dword = ctypes.c_uint32

    lib.FT_CreateDeviceInfoList.argtypes = [ctypes.POINTER(dword)]
    lib.FT_CreateDeviceInfoList.restype = status
    lib.FT_GetDeviceInfoList.argtypes = [ctypes.POINTER(_DeviceListInfoNode), ctypes.POINTER(dword)]
    lib.FT_GetDeviceInfoList.restype = status
    lib.FT_Open.argtypes = [ctypes.c_int, ctypes.POINTER(handle)]
    lib.FT_Open.restype = status
    lib.FT_Close.argtypes = [handle]
    lib.FT_Close.restype = status
    lib.FT_Read.argtypes = [handle, ctypes.c_void_p, dword, ctypes.POINTER(dword)]
    lib.FT_Read.restype = status
    lib.FT_Write.argtypes = [handle, ctypes.c_void_p, dword, ctypes.POINTER(dword)]
    lib.FT_Write.restype = status
    lib.FT_SetTimeouts.argtypes = [handle, dword, dword]
    lib.FT_SetTimeouts.restype = status
    lib.FT_SetLatencyTimer.argtypes = [handle, ctypes.c_ubyte]
    lib.FT_SetLatencyTimer.restype = status
    lib.FT_GetQueueStatus.argtypes = [handle, ctypes.POINTER(dword)]
    lib.FT_GetQueueStatus.restype = status
    lib.FT_Purge.argtypes = [handle, dword]
    lib.FT_Purge.restype = status
    lib.FT_ResetDevice.argtypes = [handle]
    lib.FT_ResetDevice.restype = status

    _lib = lib
    return _lib


def driver_available() -> bool:
    """Return True if the D2XX driver can be loaded."""
    try:
        _load_library()
        return True
    except FtdiError:
        return False


def list_devices() -> List[DeviceInfo]:
    """Enumerate connected FTDI/D2XX devices. Empty if the driver is missing."""
    try:
        lib = _load_library()
    except FtdiError:
        return []

    count = ctypes.c_uint32(0)
    if lib.FT_CreateDeviceInfoList(ctypes.byref(count)) != FT_OK or count.value == 0:
        return []

    array = (_DeviceListInfoNode * count.value)()
    if lib.FT_GetDeviceInfoList(array, ctypes.byref(count)) != FT_OK:
        return []

    return [DeviceInfo(i, array[i]) for i in range(count.value)]


class D2xxDevice:
    """An open D2XX device handle with the few operations the bridge needs."""

    def __init__(self, index: int):
        """Open the FTDI device at the given enumeration index."""
        self._lib = _load_library()
        self._handle = ctypes.c_void_p()
        if self._lib.FT_Open(index, ctypes.byref(self._handle)) != FT_OK:
            self._handle = None
            raise FtdiError(f"Failed to open FTDI device {index}. Is it already in use by another program?")
        self._lib.FT_SetTimeouts(self._handle, 1000, 1000)
        self._lib.FT_SetLatencyTimer(self._handle, 1)
        self.purge()

    def purge(self):
        """Discard any buffered receive/transmit data."""
        if self._handle is not None:
            self._lib.FT_Purge(self._handle, FT_PURGE_RX | FT_PURGE_TX)

    def queue_status(self) -> int:
        """Return the number of bytes waiting in the receive queue."""
        pending = ctypes.c_uint32(0)
        if self._lib.FT_GetQueueStatus(self._handle, ctypes.byref(pending)) != FT_OK:
            raise FtdiError("FT_GetQueueStatus failed")
        return pending.value

    def write(self, data: bytes) -> int:
        """Write all bytes to the device; raise on a short/failed write."""
        buf = ctypes.create_string_buffer(bytes(data), len(data))
        written = ctypes.c_uint32(0)
        if self._lib.FT_Write(self._handle, buf, len(data), ctypes.byref(written)) != FT_OK:
            raise FtdiError("FT_Write failed")
        if written.value != len(data):
            raise FtdiError(f"FT_Write short write ({written.value}/{len(data)})")
        return written.value

    def read(self, nbytes: int) -> bytes:
        """Read exactly nbytes and raise on timeout/short read."""
        out = bytearray()
        while len(out) < nbytes:
            remaining = nbytes - len(out)
            buf = ctypes.create_string_buffer(remaining)
            got = ctypes.c_uint32(0)
            if self._lib.FT_Read(self._handle, buf, remaining, ctypes.byref(got)) != FT_OK:
                raise FtdiError("FT_Read failed")
            if got.value == 0:
                raise FtdiError(f"FT_Read timed out ({len(out)}/{nbytes} bytes)")
            out += buf.raw[: got.value]
        return bytes(out)

    def close(self):
        """Close the device handle."""
        if self._handle is not None:
            try:
                self._lib.FT_Close(self._handle)
            finally:
                self._handle = None
