"""This module contains the task that generates a seed."""

import codecs
import json
import random
import time
import traceback
import zipfile
from datetime import UTC, datetime
from io import BytesIO

from vidua import bps
from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Patching.Patcher import load_base_rom
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler
from version import version


def generate_seed(settings_dict):
    """Generate a seed with the given settings."""
    print("Running task with")
    try:
        if isinstance(settings_dict, str):
            settings_dict = json.loads(settings_dict)
        delayed_timestamp = settings_dict.get("delayed_spoilerlog_release", 0)
        patch = open("./static/patches/shrink-dk64.bps", "rb")
        original = open("dk64.z64", "rb")
        patched = BytesIO(bps.patch(original, patch).read())
        if not settings_dict.get("seed"):
            settings_dict["seed"] = random.randint(0, 100000000)
        load_base_rom(default_file=patched)
        settings_obj = Settings(cleanup_settings(settings_dict))
        spoiler = Spoiler(settings_obj)
        patch, spoiler, password = Generate_Spoiler(spoiler)
        spoiler.FlushAllExcessSpoilerData()
        return update_seed_results(patch, spoiler, settings_dict, password, delayed_timestamp)

    except Exception as e:
        print(traceback.format_exc())
        # Return the error and the type of error.
        error = str(type(e).__name__) + ": " + str(e)
        raise e
        # queue.put(error)


def cleanup_settings(settings):
    """Cleanup the settings dictionary."""
    # Convert string data to enums where possible.
    for k, v in settings.items():
        if k in SettingsMap:
            if type(v) is list:
                values = []
                for val in v:
                    if type(val) is int:
                        values.append(SettingsMap[k](val))
                    else:
                        values.append(SettingsMap[k][val])
                settings[k] = values
            elif type(v) is int:
                settings[k] = SettingsMap[k](v)
            else:
                try:
                    settings[k] = SettingsMap[k][v]
                except Exception:
                    pass
    return settings


def update_seed_results(patch, spoiler, settings_dict, password, delayed_timestamp):
    """Update the seed results."""
    # Assuming post_body.get("delayed_spoilerlog_release") is an int, and its the number of hours to delay the spoiler log release convert that to time.time() + hours as seconds.
    try:
        spoiler_log_release = int(delayed_timestamp)
    except ValueError:
        spoiler_log_release = 0

    timestamp = time.time()
    if spoiler_log_release == 0:
        # Lets set it to 5 years from now if we don't have a delayed spoiler log release, it'll be deleted after 4 weeks anyway.
        unlock_time = timestamp + 157784760
    else:
        unlock_time = timestamp + (spoiler_log_release * 3600)
    if spoiler.settings.generate_spoilerlog:
        unlock_time = 0

    hash = spoiler.settings.seed_hash
    spoiler_log = json.loads(spoiler.json)
    # Encrypt the time and hash with the encryption key.

    current_seed_number = update_total()
    file_name = str(current_seed_number)
    spoiler_log["Unlock Time"] = unlock_time
    spoiler_log["Generated Time"] = timestamp

    # write the spoiler log to a file in generated_seeds folder. Create the folder if it doesn't exist.
    with open("generated_seeds/" + file_name + ".json", "w") as f:
        f.write(str(json.dumps(spoiler_log)))

    sections_to_retain = [
        "Settings",
        "Cosmetics",
        "Spoiler Hints",
        "Spoiler Hints Data",
        "Generated Time",
        "Item Pool",
    ]
    if spoiler.settings.generate_spoilerlog is False:
        spoiler_log = {k: v for k, v in spoiler_log.items() if k in sections_to_retain}
    else:
        del spoiler_log["Unlock Time"]

    # Always remove Password from the spoiler log.
    if spoiler.settings.has_password:
        try:
            del spoiler_log["Password"]
        except Exception:
            try:
                del spoiler_log["password"]
            except Exception:
                pass

    # Zip all the data into a single file.
    # Create a new zip file
    zip_data = BytesIO()

    with zipfile.ZipFile(zip_data, "w") as zip_file:
        # Write each variable to the zip file
        zip_file.writestr("patch", patch)
        zip_file.writestr("hash", str(hash))
        zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
        zip_file.writestr("seed_id", str(spoiler.settings.seed_id))
        zip_file.writestr("generated_time", str(timestamp))
        zip_file.writestr("version", version)
        zip_file.writestr("seed_number", str(current_seed_number))
    zip_data.seek(0)
    # Convert the zip to a string of base64 data
    zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()

    # Store the patch file in generated_seeds folder.
    with open("generated_seeds/" + file_name + ".lanky", "w") as f:
        f.write(zip_conv)
    if password:
        return {"patch": zip_conv, "hash": hash, "seed_number": current_seed_number, "password": password}
    return {"patch": zip_conv, "hash": hash, "seed_number": current_seed_number}


def update_total():
    """Update the total seeds generated."""
    max_retries = 5  # Maximum number of retries
    retry_delay = random.uniform(0, 3)
    for _ in range(max_retries):
        try:
            # Try to read and update the current total
            with open("current_total.cfg", "r+") as f:
                try:
                    current_total = int(f.read())
                except ValueError:
                    # If the file is empty or has invalid content
                    current_total = 0

                current_total += 1
                f.seek(0)  # Move the file pointer to the beginning
                f.write(str(current_total))
                f.truncate()  # Truncate the file to the current length
                break
        except IOError:
            # If a read/write error occurs, wait for a random delay and retry
            time.sleep(retry_delay)

    # Update last_generated_time
    last_generated_time = datetime.now(UTC)
    with open("last_generated_time.cfg", "w") as f:
        f.write(str(last_generated_time))
    return current_total
