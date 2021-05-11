"""Convert Rom types to Z64."""
import numpy


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def get_rom_format(rom_header):
    """Locate the rom type via the header.

    Args:
        rom_header (str): The header data.

    Returns:
        str: The rom type.
    """
    if rom_header == b"\x40\x12\x37\x80":
        return ".n64"
    elif rom_header == b"\x80\x37\x12\x40":
        return ".z64"
    elif rom_header == b"\x37\x80\x40\x12":
        return ".v64"
    else:
        return None


def swap_bytes(b):
    """Swap the bytes to the correct format."""
    chunk_bytearray = bytearray(b)
    byteswapped = bytearray(len(b))
    byteswapped[0::2] = chunk_bytearray[1::2]
    byteswapped[1::2] = chunk_bytearray[0::2]
    return byteswapped


def convert_format(infile, outfile):
    """Convert the rom type to the correct format."""
    with open(infile, "rb") as rom_file:
        rom_header = rom_file.read(4)
        rom_format = get_rom_format(rom_header)
        if not rom_format:
            return False
        rom_file.seek(0)

        with open(outfile, "wb") as out_file:
            if rom_format == ".z64":  # Just copy it
                for chunk in read_in_chunks(rom_file):
                    out_file.write(chunk)

            elif rom_format == ".n64":  # Little Endian
                for chunk in read_in_chunks(rom_file):
                    out_file.write(numpy.frombuffer(chunk, numpy.float32).byteswap())

            elif rom_format == ".v64":  # Byteswapped
                for chunk in read_in_chunks(rom_file):
                    out_file.write(swap_bytes(chunk))
        return True
