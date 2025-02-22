"""Handler for compiling the build routine for the base hack."""

import PyInstaller.__main__
import hashlib
import os
from pathlib import Path


def md5_update_from_dir(directory: str, hash):
    """Get the md5 hash of a directory of python files."""
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file() and str(path)[-3:] == ".py":
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
    return hash


def md5_dir(directory: str) -> str:
    """Get the md5 hash of the provided directory."""
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()


def compilePython():
    """Compile Python code."""
    print("Compiling Cranky's Lab")
    dir_hash = None
    dir_hash_file = "./Build/dir_hash.txt"
    if os.path.exists(dir_hash_file):
        with open(dir_hash_file, "r") as fh:
            dir_hash = fh.read()
    target_hash = md5_dir("./Build/")
    print("- Stored Hash:", "None" if dir_hash is None else dir_hash)
    print("- Calculated Hash", target_hash)
    if not os.path.exists("./Build/dist") or not os.path.exists("./Build/dist/build.exe"):
        print("- Executable: Doesn't Exist, Recompiling")
    else:
        if dir_hash is not None and dir_hash == target_hash:
            print("- Result: Ignoring")
            return
    print("- Result: Recompiling")
    print("- Recompilation: Starting...")
    with open(dir_hash_file, "w") as fh:
        fh.write(target_hash)
    segs = ["--onefile", "Build/build.py", "--distpath", "./Build/dist", "--workpath", "./Build/build", "--log-level=INFO"]

    hidden_imports = [
        "getMoveSignLocations",
        "place_vines",
    ]
    for x in hidden_imports:
        segs.extend(["--hidden-import", x])

    PyInstaller.__main__.run(segs)
    print("- Recompilation: Done")


compilePython()
