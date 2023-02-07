"""Clean up the repo to remove any files it doesn't need."""
import os

[os.remove(f) for f in os.listdir(".") if os.path.isfile(f) and os.path.exists(f) and ".bin" in f]
