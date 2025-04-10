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


def display_error_box(title: str, text: str) -> bool | None:
    """Display an error message box."""
    from tkinter import Tk, messagebox

    root = Tk()
    root.withdraw()
    ret = messagebox.showerror(title, text)
    root.update()
    return ret


class PJ64Client:
    """PJ64Client is a class that provides an interface to connect to and interact with an N64 emulator."""

    def __init__(self, address="127.0.0.1", port=55356):
        """Initialize a new instance of the class.

        Args:
            address (str): The IP address to connect to. Defaults to "127.0.0.1".
            port (int): The port number to connect to. Defaults to 55356.
        """
        self._check_client()
        self.address = address
        self.port = port
        self.socket = None
        self.connected_message = False
        self._connect()

    def _check_client(self):
        """Ensure the Project 64 executable and the required adapter script are properly set up.

        Raises:
            PJ64Exception: If the Project 64 executable is not found or if the `ap_adapter.js` file is in use.
        """
        options = get_settings()
        executable = options.get("project64_options", {}).get("executable")
        # Verify the file exists, if it does not, ask the user to select it
        if executable and not os.path.isfile(executable):
            executable = None
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
                display_error_box("Permission Error", "Unable to add adapter file to Project64, you may need to run AP as an administrator or close Project64.")
                raise PJ64Exception("Unable to add adapter file to Project64, you may need to run this script as an administrator or close Project64.")
        self._verify_pj64_config(os.path.join(os.path.dirname(executable), "Config", "Project64.cfg"))
        # Check if project 64 is running
        if not self._is_exe_running(os.path.basename(executable)):
            # Request the user to provide their ROM
            rom = open_filename("Select ROM", (("N64 ROM", (".n64", ".z64", ".v64")),))
            if self.is_project64_background():
                # Kill project 64
                if sys.platform == "win32":
                    os.system(f'taskkill /f /im "{os.path.basename(executable)}"')
                else:
                    os.system(f'pkill -f "{os.path.basename(executable)}"')
            if rom:
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

    def is_project64_background(self):
        """Specifically deals with if Project64 is running in the background in a broken state."""
        if sys.platform != "win32":
            return False

        import ctypes
        import ctypes.wintypes
        from subprocess import check_output, CalledProcessError

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi

        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        MAX_PATH = 260
        GW_OWNER = 4

        found_visible = False

        EnumWindows = user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)

        def callback(hwnd, lParam):
            nonlocal found_visible
            if not user32.IsWindowVisible(hwnd):
                return True
            if user32.GetWindow(hwnd, GW_OWNER):
                return True

            pid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid.value)
            if not h_process:
                return True

            exe_path = (ctypes.c_wchar * MAX_PATH)()
            psapi.GetModuleFileNameExW(h_process, None, exe_path, MAX_PATH)
            kernel32.CloseHandle(h_process)

            exe_name = os.path.basename(exe_path.value).lower()
            if exe_name == "project64.exe":
                found_visible = True
            return True

        EnumWindows(EnumWindowsProc(callback), 0)

        try:
            output = check_output('tasklist /FI "IMAGENAME eq Project64.exe"', shell=True, text=True)
            if "Project64.exe" in output and not found_visible:
                return True
        except CalledProcessError:
            pass

        return False

    def _verify_pj64_config(self, config_file):
        """Verify and update the configuration file for Project64.

        This method ensures that the specified configuration file contains the
        required sections and settings for proper operation. If the necessary
        sections or settings are missing, they are added or updated accordingly.
        Args:
            config_file (str): The path to the configuration file to be verified and updated.
        Behavior:
            - Ensures the [Settings] section exists and sets 'Basic Mode' to "0".
            - Ensures the [Debugger] section exists and sets 'Debugger' to "1".
            - Write the updated configuration back to the file.
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
        """Establish a connection to the specified address and port using a socket.

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
            self.connected_message = False
            raise PJ64Exception("Connection refused or reset")
        except OSError:
            # We're already connected, just move on
            pass

    def _send_command(self, command):
        """Send a command to the emulator and retrieves the response."""
        try:
            self._connect()
            self.socket.sendall(command.encode())
            response = self.socket.recv(8192).decode()
            if not response or len(str(response).strip()) == 0:
                raise PJ64Exception("No data received from the server")
            return response
        except Exception:
            self.socket = None
            self.connected_message = False
            raise PJ64Exception("Connection refused or reset")

    def _read_memory(self, address, size):
        """Read an unsigned integer of the given size from memory."""
        return int(self._send_command(f"read u{size * 8} {hex(address)} {size}"))

    def rominfo(self):
        """Retrieve ROM information from the emulator."""
        return json.loads(self._send_command("romInfo"))

    def read_u8(self, address):
        """Read an 8-bit unsigned integer from memory."""
        return self._read_memory(address, 1)

    def read_u16(self, address):
        """Read a 16-bit unsigned integer from memory."""
        return self._read_memory(address, 2)

    def read_u32(self, address):
        """Read a 32-bit unsigned integer from memory."""
        return self._read_memory(address, 4)

    def read_dict(self, dict):
        """Read a dictionary of memory addresses and returns the values."""
        return self._send_command(f"dict {json.dumps(dict, separators=(',', ':'))}")

    def read_bytestring(self, address, length):
        """Read a bytestring from memory."""
        return self._send_command(f"read bytestring {hex(address)} {length}")

    def _write_memory(self, command, address, data):
        """Write data to memory and returns the emulator response."""
        return self._send_command(f"{command} {hex(address)} {data}")

    def write_u8(self, address, data):
        """Write an 8-bit unsigned integer to memory."""
        return self._write_memory("write u8", address, [data])

    def write_u16(self, address, data):
        """Write a 16-bit unsigned integer to memory."""
        return self._write_memory("write u16", address, [data])

    def write_u32(self, address, data):
        """Write a 32-bit unsigned integer to memory."""
        return self._write_memory("write u32", address, [data])

    def write_bytestring(self, address, data):
        """Write a bytestring to memory."""
        return self._write_memory("write bytestring", address, str(data).upper() + "\x00")

    def validate_rom(self, name, memory_location=None):
        """Validate the ROM by comparing its name and optional memory location."""
        rom_info = self.rominfo()
        if not rom_info:
            return False
        if rom_info.get("goodName", "").upper() == name.upper():
            return memory_location is None or self.read_u32(memory_location) != 0
        return False
