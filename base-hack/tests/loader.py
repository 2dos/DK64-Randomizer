import psutil
import pymem
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import IntEnum, auto

## Heavily based on the autoconnector work in GSTHD by JXJacob

@dataclass
class EmulatorInfo:
    ID: str
    readable_emulator_name: str
    process_name: str
    find_dll: bool
    dll_name: Optional[str]
    additional_lookup: bool
    lower_offset_range: int
    upper_offset_range: int
    range_step: int = 16
    extra_offset: int = 0

class Emulators(IntEnum):
    Project64 = auto()
    BizHawk = auto()
    Project64_v4 = auto()
    RMG = auto()
    Simple64 = auto()
    ParallelLauncher = auto()
    RetroArch = auto()

EMULATOR_CONFIGS = {
    Emulators.Project64: EmulatorInfo("Project64", "Project64", "project64", False, None, False, 0xDFD00000, 0xE01FFFFF),
    Emulators.Project64_v4: EmulatorInfo("Project64_4", "Project64", "project64", False, None, False, 0xFDD00000, 0xFE1FFFFF),
    Emulators.BizHawk: EmulatorInfo("Bizhawk", "Bizhawk", "emuhawk", True, "mupen64plus.dll", False, 0x5A000, 0x5658DF),
    Emulators.RMG: EmulatorInfo("RMG", "Rosalie's Mupen GUI", "rmg", True, "mupen64plus.dll", True, 0x29C15D8, 0x2FC15D8, extra_offset=0x80000000),
    Emulators.Simple64: EmulatorInfo("simple64", "simple64", "simple64-gui", True, "libmupen64plus.dll", True, 0x1380000, 0x29C95D8),
    Emulators.ParallelLauncher: EmulatorInfo("parallel", "Parallel Launcher", "retroarch", True, "parallel_n64_next_libretro.dll", True, 0x845000, 0xD56000),
    Emulators.RetroArch: EmulatorInfo("retroarch", "RetroArch", "retroarch", True, "mupen64plus_next_libretro.dll", True, 0, 0xFFFFFF, range_step=4),
}

def attach_to_emulator(emu_key: str) -> Optional[Tuple[pymem.Pymem, int]]:
    emu_info = EMULATOR_CONFIGS[emu_key]

    # Find process by name
    target_proc = None
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower().startswith(emu_info.process_name.lower()):
            target_proc = proc
            break
    if not target_proc:
        print(f"Could not find process '{emu_info.process_name}'")
        return None

    pm = pymem.Pymem(target_proc.name())

    game_info = [
        0x759290,
        32,
        0x52414D42,
    ]
    if not game_info:
        return None

    address_dll = 0
    if emu_info.find_dll:
        for module in list(pm.list_modules()):
            if module.name.lower() == emu_info.dll_name.lower():
                address_dll = module.lpBaseOfDll
                break

        if address_dll == 0 and emu_info.ID == "Bizhawk":
            address_dll = 2024407040  # fallback guess
        elif address_dll == 0:
            print(f"Could not find {emu_info.dll_name} in {emu_info.readable_emulator_name}")
            return None

    has_seen_nonzero = False
    for pot_off in range(emu_info.lower_offset_range, emu_info.upper_offset_range, emu_info.range_step):
        if emu_info.additional_lookup:
            rom_addr_start = address_dll + pot_off
            try:
                read_address = pm.read_longlong(rom_addr_start)
            except:
                continue
            if read_address != 0:
                has_seen_nonzero = True
        else:
            read_address = address_dll + pot_off

        addr = read_address + emu_info.extra_offset + game_info[0]

        try:
            test_value = pm.read_int(addr)
        except:
            continue
        if test_value != 0:
            has_seen_nonzero = True
        if test_value == game_info[2]:
            print("FOUND")
            return pm, read_address + emu_info.extra_offset

    if not has_seen_nonzero:
        print(f"Could not read any data from {emu_info.readable_emulator_name}")
    return None


print(attach_to_emulator(Emulators.Project64))