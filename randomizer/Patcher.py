"""Patcher class and Functions for modifying ROM files."""
import js


class ROM:
    """Patcher for ROM files loaded via Rompatcherjs."""

    def __init__(self, file=None):
        """Patch functions for the ROM loaded within Rompatcherjs.

        This is mostly a hint file, you could directly call the javascript functions,
        but to keep this a bit more logical for team members we just import it and treat
        this like a bytesIO object.

        Args:
            file ([type], optional): [description]. Defaults to None.
        """
        if file is None:
            self.rom = js.patchedRom
        else:
            self.rom = file

    def write(self, val: int):
        """Write value to current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            val (int): Int value to write.
        """
        self.rom.writeU8(val)

    def writeBytes(self, byte_data: bytes):
        """Write an array a bytes to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            byte_data (bytes): Bytes object to write to current position.
        """
        self.rom.writeBytes(bytes(byte_data))

    def writeString(self, string: str, length: int):
        """Write a string to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            string (str): String to write.
            length (int): Length in bytes to write.
        """
        self.rom.writeString(string, length)

    def writeMultipleBytes(self, value: int, size: int):
        """Write multiple bytes of a size to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            value (int): Value to write.
            size (int): Size of the bytes to write.
        """
        arr = []
        temp = value
        for x in range(size):
            arr.append(0)
        will_pass = True
        idx = size - 1
        while will_pass:
            write = temp % 256
            arr[idx] = write
            temp = int((temp - write) / 256)
            if idx == 0 or temp == 0:
                will_pass = False
            idx -= 1
        for x in arr:
            self.write(x)

    def isEOF(self):
        """Get if we are currently at the end of the ROM.

        Returns:
            bool: True or False if we are at the end of the file.
        """
        return bool(self.rom.isEOF())

    def save(self, file_name: str):
        """Save the patched file to a downloadable file.

        You need to pass the whole file and extension.
        eg save("dk64-randomizer-12345.z64")

        Args:
            file_id (str): Name of file to save as.
        """
        self.rom.fileName = file_name
        self.rom.save()

    def slice(self, offset: int, length: int):
        """Slice the rom at a position.

        Args:
            offset (int): Starting location to offset.
            length (int): Length to retain.

        Returns:
            javascriptPatch: RompatcherJS MarcFile for patching.
        """
        return self.rom.slice(offset, length)

    def seek(self, val: int):
        """Seek to position in current file.

        Args:
            val (int): Position to seek to.
        """
        self.rom.seek(val)

    def read(self):
        """Read at the current Position.

        Starts at 0x0 as the inital position without seeking.

        Returns:
            int: Value read.
        """
        return int(self.rom.readU8())

    def readString(self, len: int):
        """Read data as a string.

        Starts at 0x0 as the inital position without seeking.

        Args:
            len (int): Length to read.

        Returns:
            string: Data read in rom.
        """
        return str(self.rom.readString(len))

    def readBytes(self, len: int):
        """Read bytes from current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            len (int): Length to read.

        Returns:
            bytes: List of bytes read from current position.
        """
        return bytes(self.rom.readBytes(len))

    def fixChecksum(self):
        """Fix the checksum of the current file."""
        js.fixChecksum(self.rom)

    def fixSecurityValue(self):
        """Set the security code and update the rom checksum."""
        self.seek(0x3154)
        self.write(0)
        self.fixChecksum()
