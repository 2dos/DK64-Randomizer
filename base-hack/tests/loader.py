"""Loader script for tracking the success of tests."""

import psutil
import pymem
from typing import Optional, Tuple
from enum import IntEnum, auto

# Heavily based on the autoconnector work in GSTHD by JXJacob


class Emulators(IntEnum):
    """Emulator enum."""

    Project64 = auto()
    BizHawk = auto()
    Project64_v4 = auto()
    RMG = auto()
    Simple64 = auto()
    ParallelLauncher = auto()
    RetroArch = auto()


class EmulatorInfo:
    """Class to store emulator information."""

    def __init__(
        self,
        id: Emulators,
        readable_emulator_name: str,
        process_name: str,
        find_dll: bool,
        dll_name: Optional[str],
        additional_lookup: bool,
        lower_offset_range: int,
        upper_offset_range: int,
        range_step: int = 16,
        extra_offset: int = 0,
    ):
        """Initialize with given parameters."""
        self.id = id
        self.readable_emulator_name = readable_emulator_name
        self.process_name = process_name
        self.find_dll = find_dll
        self.dll_name = dll_name
        self.additional_lookup = additional_lookup
        self.lower_offset_range = lower_offset_range
        self.upper_offset_range = upper_offset_range
        self.range_step = range_step
        self.extra_offset = extra_offset
        self.connected_process: pymem.Pymem = None
        self.connected_offset: int = None

    def attach_to_emulator(self) -> Optional[Tuple[pymem.Pymem, int]]:
        """Grab  memory addresses of where emulated RDRAM is."""
        # Reset
        self.connected_process = None
        self.connected_offset = None
        # Find process by name
        target_proc = None
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and proc.info["name"].lower().startswith(self.process_name.lower()):
                target_proc = proc
                break
        if not target_proc:
            print(f"Could not find process '{self.process_name}'")
            return

        pm = pymem.Pymem(target_proc.name())
        address_dll = 0
        if self.find_dll:
            for module in list(pm.list_modules()):
                if module.name.lower() == self.dll_name.lower():
                    address_dll = module.lpBaseOfDll
                    break

            if address_dll == 0 and self.id == Emulators.BizHawk:
                address_dll = 2024407040  # fallback guess
            elif address_dll == 0:
                print(f"Could not find {self.dll_name} in {self.readable_emulator_name}")
                return

        has_seen_nonzero = False
        for pot_off in range(self.lower_offset_range, self.upper_offset_range, self.range_step):
            if self.additional_lookup:
                rom_addr_start = address_dll + pot_off
                try:
                    read_address = pm.read_longlong(rom_addr_start)
                except Exception:
                    continue
                if read_address != 0:
                    has_seen_nonzero = True
            else:
                read_address = address_dll + pot_off

            addr = read_address + self.extra_offset + 0x759290

            try:
                test_value = pm.read_int(addr)
            except Exception:
                continue
            if test_value != 0:
                has_seen_nonzero = True
            if test_value == 0x52414D42:
                print("FOUND")
                self.connected_process = pm
                self.connected_offset = read_address + self.extra_offset
                return

        if not has_seen_nonzero:
            print(f"Could not read any data from {self.readable_emulator_name}")

    def readBytes(self, address: int, size: int) -> int:
        """Read a series of bytes and cast to an int."""
        if self.connected_process is None:
            raise Exception("Not connected to a process, exiting")
        if address & 0x80000000:
            address &= 0x7FFFFFFF
        mem_address = self.connected_offset + address
        value = 0
        for offset in range(size):
            local_value = self.connected_process.read_uchar(mem_address + offset)
            value <<= 8
            value += local_value
        return value

    def writeBytes(self, address: int, size: int, value: int):
        """Write a series of bytes to memory."""
        if self.connected_process is None:
            raise Exception("Not connected to a process, exiting")
        if address & 0x80000000:
            address &= 0x7FFFFFFF
        mem_address = self.connected_offset + address
        val_series = [0] * size
        local_value = value
        for x in range(size):
            val_series[(size - 1) - x] = local_value & 0xFF
            local_value >>= 8
        for offset, val in enumerate(val_series):
            self.connected_process.write_uchar(mem_address + offset, val)


EMULATOR_CONFIGS = {
    Emulators.Project64: EmulatorInfo(Emulators.Project64, "Project64", "project64", False, None, False, 0xDFD00000, 0xE01FFFFF),
    Emulators.Project64_v4: EmulatorInfo(Emulators.Project64_v4, "Project64", "project64", False, None, False, 0xFDD00000, 0xFE1FFFFF),
    Emulators.BizHawk: EmulatorInfo(Emulators.BizHawk, "Bizhawk", "emuhawk", True, "mupen64plus.dll", False, 0x5A000, 0x5658DF),
    Emulators.RMG: EmulatorInfo(Emulators.RMG, "Rosalie's Mupen GUI", "rmg", True, "mupen64plus.dll", True, 0x29C15D8, 0x2FC15D8, extra_offset=0x80000000),
    Emulators.Simple64: EmulatorInfo(Emulators.Simple64, "simple64", "simple64-gui", True, "libmupen64plus.dll", True, 0x1380000, 0x29C95D8),
    Emulators.ParallelLauncher: EmulatorInfo(Emulators.ParallelLauncher, "Parallel Launcher", "retroarch", True, "parallel_n64_next_libretro.dll", True, 0x845000, 0xD56000),
    Emulators.RetroArch: EmulatorInfo(Emulators.RetroArch, "RetroArch", "retroarch", True, "mupen64plus_next_libretro.dll", True, 0, 0xFFFFFF, range_step=4),
}


def attachWrapper(emu: Emulators) -> EmulatorInfo:
    """Wrap function for attaching to an emulator."""
    EMULATOR_CONFIGS[emu].attach_to_emulator()
    return EMULATOR_CONFIGS[emu]
