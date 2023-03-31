"""Clean up the repo to remove any files it doesn't need."""
import os

[os.remove(f) for f in os.listdir(".") if os.path.isfile(f) and os.path.exists(f) and ".bin" in f]
instance_dir = "./assets/instance_scripts/"
for f in os.listdir(instance_dir):
    joined = os.path.join(instance_dir, f)
    if os.path.isfile(joined) and os.path.exists(joined) and ".raw" in f:
        os.remove(joined)
