import shutil
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
import random
import threading

def genSeed(index, name:str, sdata: str):
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    print("Genning: ", index)
    subprocess.run(["python", "./cli.py", "--settings_string", sdata, "--output", f"./batch_spoilers/{name}/seed{index}.z64", "--batch", "True"])

# Example usage
settings_data = {}
batch_dir = './batch_spoilers'
if not os.path.exists(batch_dir):
    os.mkdir(batch_dir)

SEED_GEN_COUNT = 1000
THREAD_COUNT = 16

for name, settings in settings_data.items():
    if os.path.exists(f"{batch_dir}/{name}"):
        shutil.rmtree(f"{batch_dir}/{name}")
    os.mkdir(f"{batch_dir}/{name}")

    print(f"[CONSOLE] Generating {SEED_GEN_COUNT} seeds")

    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = [
            executor.submit(genSeed, x, name, settings)
            for x in range(SEED_GEN_COUNT)
        ]

        # Wait for completion
        for future in futures:
            future.result()

# python .\cli.py --settings_string "bKEGiRqzxNXnerKEDRAejpFjAIbiDLWIQXr5/ANnj4YTRzu6leyszOKbOrYvhTgfVA4IhkQlS2Nc+EaePxGj12ly+IU5Ym04IUBR6QJE0Z4q+ApBbqevwJIBk0UJooZBdZLLBQF0AIMBOoCBwN2AYQCO4ECQV4AoUDPIGCwd6A4YEKENQHtkKRKitZyJTqZcklmi3gRwdItIuCn6KiLAImIoAr1rjkbtV/vsigcxYigDNZsyqMSRYAExgAExoADxwADx4ACyAACyIAByQAByYABygABqcuUOS4VOmEJIIvoE5IMMJUzG0xg4tC0rlgVocthoTiwVGAmDAjKY4p5FJkRqUAVQCXAwwpMJwhCAkKCw2lIisPEBEjLBMUFSQtFxgZJS4bHB0mLx8gISco"  --output "dk64r-seed.z64"