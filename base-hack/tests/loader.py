"""Loader script for tracking the success of tests."""

import psutil
import pymem
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import IntEnum, auto

## Heavily based on the autoconnector work in GSTHD by JXJacob


@dataclass
class EmulatorInfo:
    """Class to store emulator information."""

    def __init__(
        self,
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

    def attach_to_emulator(self, emu_key: str) -> Optional[Tuple[pymem.Pymem, int]]:
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

            if address_dll == 0 and emu_key == Emulators.BizHawk:
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
                except:
                    continue
                if read_address != 0:
                    has_seen_nonzero = True
            else:
                read_address = address_dll + pot_off

            addr = read_address + self.extra_offset + 0x759290

            try:
                test_value = pm.read_int(addr)
            except:
                continue
            if test_value != 0:
                has_seen_nonzero = True
            if test_value == 0x52414D42:
                print("FOUND")
                self.connected_process = pm
                self.connected_offset = read_address + self.extra_offset

        if not has_seen_nonzero:
            print(f"Could not read any data from {self.readable_emulator_name}")


class Emulators(IntEnum):
    """Emulator enum."""

    Project64 = auto()
    BizHawk = auto()
    Project64_v4 = auto()
    RMG = auto()
    Simple64 = auto()
    ParallelLauncher = auto()
    RetroArch = auto()


EMULATOR_CONFIGS = {
    Emulators.Project64: EmulatorInfo("Project64", "project64", False, None, False, 0xDFD00000, 0xE01FFFFF),
    Emulators.Project64_v4: EmulatorInfo("Project64", "project64", False, None, False, 0xFDD00000, 0xFE1FFFFF),
    Emulators.BizHawk: EmulatorInfo("Bizhawk", "emuhawk", True, "mupen64plus.dll", False, 0x5A000, 0x5658DF),
    Emulators.RMG: EmulatorInfo("Rosalie's Mupen GUI", "rmg", True, "mupen64plus.dll", True, 0x29C15D8, 0x2FC15D8, extra_offset=0x80000000),
    Emulators.Simple64: EmulatorInfo("simple64", "simple64-gui", True, "libmupen64plus.dll", True, 0x1380000, 0x29C95D8),
    Emulators.ParallelLauncher: EmulatorInfo("Parallel Launcher", "retroarch", True, "parallel_n64_next_libretro.dll", True, 0x845000, 0xD56000),
    Emulators.RetroArch: EmulatorInfo("RetroArch", "retroarch", True, "mupen64plus_next_libretro.dll", True, 0, 0xFFFFFF, range_step=4),
}

EMULATOR_CONFIGS[Emulators.Project64].attach_to_emulator(Emulators.Project64)
print(EMULATOR_CONFIGS[Emulators.Project64].connected_process)
print(EMULATOR_CONFIGS[Emulators.Project64].connected_offset)
