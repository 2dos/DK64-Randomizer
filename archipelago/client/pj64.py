"""Contains the PJ64Client class for interacting with Project64."""

import socket
import json
import sys
import os
import subprocess
import pkgutil
from configparser import ConfigParser
from Utils import open_filename
from Utils import get_settings


class PJ64Exception(Exception):
    """
    Custom exception class for PJ64-related errors.

    This exception is raised when an error specific to PJ64 operations occurs.

    Attributes:
        message (str): Explanation of the error.
    """

    pass


class PJ64Client:
    """
    PJ64Client is a class that provides an interface to connect to and interact with an N64 emulator.
    """

    def __init__(self, address="127.0.0.1", port=1337):
        """
        Initializes a new instance of the class.

        Args:
            address (str): The IP address to connect to. Defaults to "127.0.0.1".
            port (int): The port number to connect to. Defaults to 1337.
        """
        self._check_client()
        self.address = address
        self.port = port
        self.socket = None
        self.connected_message = False
        self._connect()

    def _check_client(self):
        """Ensures the Project 64 executable and the required adapter script are properly set up.

        Raises:
            PJ64Exception: If the Project 64 executable is not found or if the `ap_adapter.js` file is in use.
        """
        options = get_settings()
        executable = options.get("project64_options", {}).get("executable")
        if not executable:
            executable = open_filename("Project 64 4.0 Executable", (("Project64 Executable", (".exe",)),), "Project64.exe")
            if not executable:
                raise PJ64Exception("Project 64 executable not found.")
            options.update({"project64_options": {"executable": executable}})
            options.save()

        # Check if the file ap_adapter exists in the subfolder of the executable, the folder Scripts
        # If it does not exist, copy it from worlds/dk64/client/adapter.js
        adapter_path = os.path.join(os.path.dirname(executable), "Scripts", "ap_adapter.js")
        # Read the existing file from the world
        try:
            with open("worlds/dk64/archipelago/client/adapter.js", "r") as f:
                adapter_content = f.read()
        except Exception:
            adapter_content = pkgutil.get_data(__name__, "adapter.js").decode()
        # Check if the file is in use
        matching_content = False
        # Check if the contents match
        try:
            with open(adapter_path, "r") as f:
                if f.read() == adapter_content:
                    matching_content = True
        except FileNotFoundError:
            pass
        if not matching_content:
            try:
                with open(adapter_path, "w") as f:
                    f.write(adapter_content)
            except PermissionError:
                raise PJ64Exception("Unable to add adapter file to Project64, you may need to run this script as an administrator or close Project64.")
        self._verify_pj64_config(os.path.join(os.path.dirname(executable), "Config", "Project64.cfg"))
        # Check if project 64 is running
        if not self._is_exe_running(os.path.basename(executable)):
            # Request the user to provide their ROM
            rom = open_filename("Select ROM", (("N64 ROM", (".n64", ".z64", ".v64")),))
            # Run project 64
            os.popen(f'"{executable}" "{rom}"')

    def _is_exe_running(self, exe_name):
        """Check if a given executable is running without using psutil."""
        exe_name = exe_name.lower()

        if sys.platform == "win32":
            try:
                output = subprocess.check_output(["tasklist"], text=True, errors="ignore")
                return exe_name in output.lower()
            except subprocess.CalledProcessError:
                return False

        else:  # Unix-based (Linux/macOS)
            try:
                result = subprocess.run(["pgrep", "-f", exe_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                return result.returncode == 0
            except FileNotFoundError:
                return False  # `pgrep` not available

        return False

    def _verify_pj64_config(self, config_file):
        """Verifies and updates the configuration file for Project64.
        This method ensures that the specified configuration file contains the
        required sections and settings for proper operation. If the necessary
        sections or settings are missing, they are added or updated accordingly.
        Args:
            config_file (str): The path to the configuration file to be verified and updated.
        Behavior:
            - Ensures the [Settings] section exists and sets 'Basic Mode' to "0".
            - Ensures the [Debugger] section exists and sets 'Debugger' to "1".
            - Writes the updated configuration back to the file.
        Note:
            If an exception occurs while writing to the file, it is silently ignored.
        """
        # Read the CFG file
        config = ConfigParser()
        config.read(config_file)

        # Ensure the [Settings] section exists and update 'Basic Mode'
        if "Settings" not in config:
            config.add_section("Settings")
        config.set("Settings", "Basic Mode", "0")

        # Ensure the [Debugger] section exists and set 'Debugger'
        if "Debugger" not in config:
            config.add_section("Debugger")
        config.set("Debugger", "Debugger", "1")
        config.set("Debugger", "Autorun Scripts", "ap_adapter.js")

        # Write the updated settings back to the file
        try:
            with open(config_file, "w") as configfile:
                config.write(configfile, space_around_delimiters=False)
        except Exception:
            pass

    def _connect(self):
        """
        Establishes a connection to the specified address and port using a socket.
        If the socket is not already created, it initializes a new socket with
        AF_INET and SOCK_STREAM parameters and sets a timeout of 0.1 seconds.
        Raises:
            PJ64Exception: If the connection is refused, reset, or aborted.
            OSError: If the socket is already connected.
        """
        if self.connected_message:
            return
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(0.1)
        try:
            self.socket.connect((self.address, self.port))
            self.connected_message = True
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError):
            self.socket = None
            raise PJ64Exception("Connection refused or reset")
        except OSError:
            # We're already connected, just move on
            pass

    def _send_command(self, command):
        """Sends a command to the emulator and retrieves the response."""
        try:
            self._connect()
            self.socket.sendall(command.encode())
            response = self.socket.recv(4096).decode()
            if not response:
                raise PJ64Exception("No data received from the server")
            return response
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError):
            raise PJ64Exception("Connection refused or reset")

    def _read_memory(self, address, size):
        """Reads an unsigned integer of the given size from memory."""
        return int(self._send_command(f"read u{size * 8} {hex(address)} {size}"))

    def rominfo(self):
        """Retrieves ROM information from the emulator."""
        return json.loads(self._send_command("romInfo"))

    def read_u8(self, address):
        """Reads an 8-bit unsigned integer from memory."""
        return self._read_memory(address, 1)

    def read_u16(self, address):
        """Reads a 16-bit unsigned integer from memory."""
        return self._read_memory(address, 2)

    def read_u32(self, address):
        """Reads a 32-bit unsigned integer from memory."""
        return self._read_memory(address, 4)

    def read_dict(self, dict):
        """Reads a dictionary of memory addresses and returns the values."""
        return self._send_command(f"dict {json.dumps(dict, separators=(',', ':'))}")

    def read_bytestring(self, address, length):
        """Reads a bytestring from memory."""
        return self._send_command(f"read bytestring {hex(address)} {length}")

    def _write_memory(self, command, address, data):
        """Writes data to memory and returns the emulator response."""
        return self._send_command(f"{command} {hex(address)} {data}")

    def write_u8(self, address, data):
        """Writes an 8-bit unsigned integer to memory."""
        return self._write_memory("write u8", address, [data])

    def write_u32(self, address, data):
        """Writes a 32-bit unsigned integer to memory."""
        return self._write_memory("write u32", address, [data])

    def write_bytestring(self, address, data):
        """Writes a bytestring to memory."""
        return self._write_memory("write bytestring", address, str(data).upper() + "\x00")

    def validate_rom(self, name, memory_location=None):
        """Validates the ROM by comparing its name and optional memory location."""
        rom_info = self.rominfo()
        if not rom_info:
            return False
        if rom_info.get("goodName", "").upper() == name.upper():
            return memory_location is None or self.read_u32(memory_location) != 0
        return False
