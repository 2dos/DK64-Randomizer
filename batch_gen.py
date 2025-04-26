import shutil
import os
import threading
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
import random
import math

def genSeed(index, name:str, sdata: str):
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # The settings string is defined either here or in the string above, pick your poison
    settings_dict = decrypt_settings_string_enum(sdata)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

    settings = Settings(settings_dict)
    settings.settings_string = sdata
    spoiler = Spoiler(settings)
    _, spoiler_log, _ = Generate_Spoiler(spoiler)
    with open(f"./batch_spoilers/{name}/seed{index}.json", "w") as outfile:
        outfile.write(spoiler_log.json)

THREAD_COUNT = 16
SEED_GEN_COUNT = 250

settings_data = {
    "banana_breadcrumbs": "fjNPxIMxDIUx0QSpbHPjJSVmUEuC9Wy+c3mI9D6gHhEMhkJUtjXPhEfiNEpEtiFKi47VAhMF6AAd+AA2CAAGGAAOKAAE3nAcMRlOlYFILRS22BbgJJANMmaqIUYpBSimAyZZXq/BQFuAIMBN4CBwNwAYQCOIECQVyAoUDOYGCwd0A4YEXIITIajOqWrwAZTiU1GwkoSjuq1ZLGjMxWkCPT5CotqUvRURYBExFAFYsscjdkvF3kUDkOxl7TsDPJxqyDTanBEIABcKABcMABMOABMQAA9aAA8SAAsUAAcWAA8YAAsaAAdcABafK9AkuVLZ7LIYRzJT67WBgM5dVgOKorKZUWjHFKAFBWDSgE4qLRJFxDTxrSyDSIjXR2AB0AvBsKCxARFBYYGRocHR4gISIoKSwtLi8wNDVdXqy+BggMDSsyX8ACKjHCCgkOEhUjJCUmJ1zEATOdALIAUQA",
    "refined_ruckus": "fjNPxAMxDIUx0QSpbHRUlZlBLgvVsvnN5iPQ+oB4RDIZCVLY1z4RH4jRKRLYhSouO1QITBegAHfgANggADhgABigADN5wJDEZ0wY54FILRS22BbgJJANMmaqIUYpBSimAyZZXq/BQFuAIMBN4CBwNwAYQCOIECQVyAoUDOYGCwd0A4YEXIITIaZOqWrwAZTiU1awkoSjuq1ZLGjMxWkBO0Ki2pS9FTFkATEUAViyxyN2S8XeRQOQ7GXtOwM8nGDIAyqcEQgAFwoAFwwAEw4AExAAD1oADxIACxQABxYADxgACxoAB1wAFp8r0CS5UtnsshhHMlPrtYGAzl1WA4qisplRaMcUoAUFYNKATiotEkXENPGtLINIiNdHYAHQC8IAkKCw4QERIUFRYYGRocHR4gISIjJCUmJygpLC0uLzCsvgYIDA0rMl/AAjQ1wgMqMTPEA1xdXp0AsgBRAA",
}
batch_dir = "./batch_spoilers"
if os.path.exists(batch_dir):
    shutil.rmtree(batch_dir)
os.mkdir(batch_dir)
for name, settings in settings_data.items():
    batches = math.ceil(SEED_GEN_COUNT / THREAD_COUNT)
    os.mkdir(f"{batch_dir}/{name}")
    for batch in range(batches):
        batch_threads = []
        for subbatch in range(THREAD_COUNT):
            x = (THREAD_COUNT * batch) + subbatch
            batch_threads.append(threading.Thread(target=genSeed, args=(x, name, settings)))
        init_batch = THREAD_COUNT * batch
        print(f"[CONSOLE] Generating seeds {init_batch}-{init_batch + THREAD_COUNT}")
        for b in batch_threads:
            b.start()
        for b in batch_threads:
            b.join()

# python .\cli.py --settings_string "bKEGiRqzxNXnerKEDRAejpFjAIbiDLWIQXr5/ANnj4YTRzu6leyszOKbOrYvhTgfVA4IhkQlS2Nc+EaePxGj12ly+IU5Ym04IUBR6QJE0Z4q+ApBbqevwJIBk0UJooZBdZLLBQF0AIMBOoCBwN2AYQCO4ECQV4AoUDPIGCwd6A4YEKENQHtkKRKitZyJTqZcklmi3gRwdItIuCn6KiLAImIoAr1rjkbtV/vsigcxYigDNZsyqMSRYAExgAExoADxwADx4ACyAACyIAByQAByYABygABqcuUOS4VOmEJIIvoE5IMMJUzG0xg4tC0rlgVocthoTiwVGAmDAjKY4p5FJkRqUAVQCXAwwpMJwhCAkKCw2lIisPEBEjLBMUFSQtFxgZJS4bHB0mLx8gISco"  --output "dk64r-seed.z64"