"""Test crowd control dumps for things blocking effects."""

from typing import BinaryIO
import struct
from enum import IntEnum, auto
import os

ADDR_STATE_POINTER = 0x807FFFB4
ADDR_MAP_TIMER = 0x8076A064
ADDR_PLAYER_POINTER = 0x807FBB4C
ADDR_AUTOWALK_STATE = 0x807463B8
ADDR_CURRENT_GAMEMODE = 0x80755314
ADDR_NEXT_GAMEMODE = 0x80755318
ADDR_TBVOID_BYTE = 0x807FBB63
ADDR_KONG_BASE = 0x807FC950
ADDR_RANDO_CANARY = 0x807FFFF4
ADDR_CUTSCENE_ACTIVE = 0x807444EC
ADDR_TRANSITION_SPEED = 0x807FD88C
ADDR_STANDARD_AMMO = 0x807FCC40
ADDR_HOMING_AMMO = 0x807FCC42
ADDR_ORANGES = 0x807FCC44
ADDR_CRYSTALS = 0x807FCC46
ADDR_FILM = 0x807FCC48
ADDR_HEALTH = 0x807FCC4B
ADDR_MELONS = 0x807FCC4C
ADDR_GLOBAL_INSTRUMENT = 0x807FCC4E
ADDR_APPLIED_DAMAGE_MULTIPLIER = 0x807FF8A5
ADDR_ORIGINAl_DAMAGE_MULTIPLIER = 0x807FFFF9
ADDR_BASE_ASPECT = 0x80010520
ADDR_CURRENT_MAP = 0x8076A0AB
ADDR_LEVEL_TABLE = 0x807445E0


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def readAddr(fh: BinaryIO, addr: int, size: int, is_float: bool = False):
    """Read address at offset"""
    fh.seek(addr - 0x80000000)
    data = int.from_bytes(fh.read(size), "big")
    if size == 4 and is_float:
        return intf_to_float(data)
    return data


class GameState(IntEnum):
    Unknown = auto()
    WrongMode = auto()
    BadPlayerState = auto()
    Paused = auto()
    SafeArea = auto()
    Unmodded = auto()
    PipelineBusy = auto()
    Ready = auto()


class Kickback:

    def __init__(self, state: GameState, message: str):
        self.state = state
        self.message = message


def parseFile(file_name: str) -> Kickback:
    """Parse a specific dump."""
    with open(file_name, "rb") as fh:
        current_gamemode = readAddr(fh, ADDR_CURRENT_GAMEMODE, 1)
        next_gamemode = readAddr(fh, ADDR_NEXT_GAMEMODE, 1)
        map_timer = readAddr(fh, ADDR_MAP_TIMER, 4)
        player_pointer = readAddr(fh, ADDR_PLAYER_POINTER, 4)
        tb_void_byte = readAddr(fh, ADDR_TBVOID_BYTE, 1)
        rando_version = readAddr(fh, ADDR_RANDO_CANARY, 1)
        cutscene_state = readAddr(fh, ADDR_CUTSCENE_ACTIVE, 1)
        transition_speed = readAddr(fh, ADDR_TRANSITION_SPEED, 4, True)
        state_pointer = readAddr(fh, ADDR_STATE_POINTER, 4, True)
        if rando_version != 4:
            return Kickback(GameState.Unknown, "Wrong Rando Version")
        if state_pointer == 0:
            return Kickback(GameState.Unknown, "Invalid State Pointer")
        if (current_gamemode != 6) or (next_gamemode != 6):
            return Kickback(GameState.WrongMode, "Incorrect Gamemode")
        if map_timer < 2:
            return Kickback(GameState.BadPlayerState, "Map Timer too low")
        if player_pointer == 0:
            return Kickback(GameState.BadPlayerState, "No player")
        if readAddr(fh, ADDR_AUTOWALK_STATE, 1) != 0:
            return Kickback(GameState.BadPlayerState, "Autowalking")
        if (tb_void_byte & 3) != 0:
            return Kickback(GameState.Paused, "Paused Game")
        if (tb_void_byte & 0x30) == 0:
            return Kickback(GameState.BadPlayerState, "In Tag Barrel")
        if cutscene_state in (3, 4):
            return Kickback(GameState.SafeArea, "In 8Bit Minigame")
        if cutscene_state != 0:
            return Kickback(GameState.Paused, "In cutscene")
        if transition_speed > 0.0:
            return Kickback(GameState.BadPlayerState, "Transitioning")
        return Kickback(GameState.Ready, "Valid")


def main():
    """Main pipeline."""
    for file in os.listdir("./dumps"):
        state = parseFile(f"./dumps/{file}")
        output = f'State of file "{file}": {state.state.name}'
        if state.state != GameState.Ready:
            output += f" ({state.message})"
        print(output)


if __name__ == "__main__":
    main()
