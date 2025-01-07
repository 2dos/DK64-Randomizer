"""This module is responsible for deleting old files."""

import json
import time
from os import listdir, makedirs, path, remove

from apscheduler.schedulers.background import BackgroundScheduler


def delete_old_files():
    """Delete files that are older than 4 weeks."""
    folder_path = "generated_seeds"
    current_time = time.time()
    makedirs("generated_seeds", exist_ok=True)
    for filename in listdir(folder_path):
        if filename.endswith(".json"):
            file_path = path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                generated_time = data.get("Generated Time", 0)

                # Check if it's been 4 weeks since unlock_time
                if current_time - generated_time >= 2419200:  # 4 weeks in seconds
                    try:
                        remove(file_path)
                        print(f"Deleted file: {filename}")
                        # also delete the lanky file
                        remove(path.join(folder_path, filename.replace(".json", ".lanky")))
                    except Exception as e:
                        print(e)


def enable_cleanup():
    """Enable the cleanup scheduler."""
    # Setup the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_old_files, trigger="interval", hours=2)
    scheduler.start()
    return scheduler


enable_cleanup()
