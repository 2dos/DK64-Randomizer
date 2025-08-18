"""Script to run all test functions."""

from loader import Emulators, EmulatorInfo, attachWrapper
from test_enums import Maps
from time import sleep


def test_does_boot(container: EmulatorInfo):
    """Test whether the game successfully performs the boot procedure."""
    sleep(3)
    res = container.readBytes(0x8076A0A8, 4)
    return res != Maps.NintendoLogo


class Test:
    """Test class."""

    def __init__(self, fn, name: str):
        """Initialize with given variables."""
        self.fn = fn
        self.name = name


tests = [
    Test(test_does_boot, "ROM Boots"),
]


def runTests():
    """Run all associated ROM Tests."""
    container = attachWrapper(Emulators.Project64)
    input("Ensure that the emulator is unpaused. Once unpaused, press Enter...")
    successful_tests = 0
    for test in tests:
        valid_test = test.fn(container)
        if valid_test:
            successful_tests += 1
        print(f"{'✅' if valid_test else '❌'} {test.name}")


runTests()
