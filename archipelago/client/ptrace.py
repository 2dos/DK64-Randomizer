"""Helper module for managing Linux ptrace scope permissions."""

import os
import platform
import subprocess

IS_LINUX = platform.system() == "Linux"

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


def setup_passwordless_ptrace() -> bool:
    """Set up sudoers rule to allow ptrace changes without password.

    Returns:
        True if successfully set up or already configured
        False if setup failed
    """
    sudoers_file = "/etc/sudoers.d/dk64-ptrace"
    tee_path = "/usr/bin/tee"
    ptrace_scope_path = "/proc/sys/kernel/yama/ptrace_scope"

    # Check if rule already exists
    if os.path.exists(sudoers_file):
        return True

    # Create sudoers content (allows tee to ptrace_scope without password)
    # Using %sudo and %wheel to cover common group names
    sudoers_content = f"""# Allow DK64 Randomizer to modify ptrace scope without password
%sudo ALL=(ALL) NOPASSWD: {tee_path} {ptrace_scope_path}
%wheel ALL=(ALL) NOPASSWD: {tee_path} {ptrace_scope_path}
"""

    try:
        logger.info("Setting up passwordless ptrace access (one-time setup)...")
        logger.info("You may be prompted for your sudo password.")

        # Write sudoers rule using visudo for safety
        # First create temp file, then validate and move it
        temp_file = "/tmp/dk64-ptrace-sudoers"
        with open(temp_file, "w") as f:
            f.write(sudoers_content)

        # Validate the sudoers file
        result = subprocess.run(["sudo", "visudo", "-c", "-f", temp_file], capture_output=True, timeout=30)

        if result.returncode == 0:
            # Valid, now move it
            result = subprocess.run(["sudo", "cp", temp_file, sudoers_file], timeout=30)

            if result.returncode == 0:
                # Set proper permissions
                subprocess.run(["sudo", "chmod", "0440", sudoers_file], timeout=5)
                os.remove(temp_file)
                logger.info("Successfully configured passwordless ptrace access.")
                return True

        # Cleanup temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)

        return False

    except Exception as e:
        logger.warning(f"Failed to setup passwordless ptrace: {e}")
        return False


def check_and_fix_ptrace_scope() -> bool:
    """Check if ptrace scope is restrictive and attempt to fix it.

    Returns:
        True if ptrace is available (either already set or successfully fixed)
        False if ptrace restrictions couldn't be fixed
    """
    if not IS_LINUX:
        return True

    ptrace_scope_path = "/proc/sys/kernel/yama/ptrace_scope"

    # Check if ptrace scope file exists
    if not os.path.exists(ptrace_scope_path):
        # No ptrace restrictions on this system
        return True

    try:
        # Read current ptrace scope
        with open(ptrace_scope_path, "r") as f:
            scope = int(f.read().strip())

        # 0 = classic ptrace (no restrictions)
        # 1 = restricted ptrace (default on many distros)
        # 2 = admin-only attach
        # 3 = no attach allowed
        if scope == 0:
            return True

        # Need to set ptrace scope to 0
        logger.info(f"Detected restrictive ptrace scope ({scope}). Attempting to enable memory access...")

        # Try to set up passwordless access first (one-time)
        setup_passwordless_ptrace()

        # Try to set ptrace scope using sudo (no password if rule exists)
        try:
            result = subprocess.run(["sudo", "-n", "tee", ptrace_scope_path], input=b"0\n", capture_output=True, timeout=1)
            if result.returncode == 0:
                logger.info("Successfully enabled ptrace access.")
                return True
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

        # -n failed, try interactive sudo (should only happen on first run)
        logger.info("You may be prompted for your sudo password.")
        try:
            result = subprocess.run(["sudo", "tee", ptrace_scope_path], input=b"0\n", timeout=30)
            if result.returncode == 0:
                logger.info("Successfully enabled ptrace access.")
                return True
            else:
                logger.warning("Failed to set ptrace scope. You may need to run manually:")
                logger.warning(f"  echo 0 | sudo tee {ptrace_scope_path}")
                return False
        except subprocess.TimeoutExpired:
            logger.warning("Sudo prompt timed out.")
            return False
        except Exception as e:
            logger.warning(f"Failed to set ptrace scope: {e}")
            logger.warning(f"You may need to run manually: echo 0 | sudo tee {ptrace_scope_path}")
            return False

    except Exception as e:
        logger.warning(f"Could not check ptrace scope: {e}")
        return True  # Assume it's fine if we can't check
