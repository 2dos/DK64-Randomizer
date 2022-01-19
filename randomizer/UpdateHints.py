"""Update wrinkly hints compressed file."""
import gzip
from io import BytesIO

import js

from randomizer.Enums.WrinklyKong import WrinklyKong
from randomizer.Patcher import ROM
from randomizer.Lists.WrinklyHints import Hint


def UpdateHint(WrinklyHint: Hint, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    ROM().seek(js.pointer_addresses[12]["entries"][41]["pointing_to"])
    byte_data = ROM().readBytes(js.pointer_addresses[12]["entries"][41]["compressed_size"])
    decompressed = gzip.decompress(byte_data)
    loadedBytes = BytesIO(decompressed)
    loadedBytes.seek(WrinklyHint.address)
    padding = ""
    if len(message) <= WrinklyHint.length:
        # We're safely below the character limit
        pass
    else:
        raise Exception("Hint message is longer than allowed.")

    loadedBytes.write(message + padding)
    loadedBytes.seek(0)
    new_bytes = loadedBytes.read()
    ROM().writeBytes(gzip.compress(new_bytes, compresslevel=9))
