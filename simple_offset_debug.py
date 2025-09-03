#!/usr/bin/env python3
"""Simple debug script to test writing to offset 0x02A."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'archipelago'))

from client.emu_loader import EmuLoaderClient


def simple_debug():
    """Simple test - connect, validate, get memory pointer, and write to 0x02A."""
    print("=== Simple Debug - Testing 0x02A Offset ===")
    
    # Connect
    n64_client = EmuLoaderClient()
    if not n64_client.connect():
        print("❌ Failed to connect")
        return False
    
    # Validate ROM
    # 0x807FFF1C is the memory pointer from the map
    if not n64_client.validate_rom("DONKEY KONG 64", 0x807FFF1C):
        print("❌ Invalid ROM")
        return False
    
    # Get memory pointer
    memory_pointer = n64_client.read_u32(0x807FFF1C)
    if memory_pointer == 0:
        print("❌ Memory pointer is 0")
        return False
    
    print(f"✅ Connected and validated")
    print(f"Memory pointer: 0x{memory_pointer:08X}")
    
    # Test 0x02A offset
    offset = 0x02A
    test_address = memory_pointer + offset
    print(f"Testing address: 0x{test_address:08X} (offset 0x{offset:03X})")
    
    # Read current value
    current = n64_client.read_u8(test_address)
    print(f"Current value: 0x{current:02X}")
    
    # Write 0xFF
    print("Writing 0xFF...")
    n64_client.write_u8(test_address, 0xFF)
    
    # Read back
    result = n64_client.read_u8(test_address)
    print(f"Read back: 0x{result:02X}")
    
    if result == 0xFF:
        print("✅ SUCCESS - Write to 0x02A worked!")
    else:
        print("❌ FAILED - Write to 0x02A didn't work")
    
    n64_client.disconnect()
    return result == 0xFF


if __name__ == "__main__":
    simple_debug()
