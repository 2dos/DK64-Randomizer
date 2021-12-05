"""Deal with logic for the footer patch files."""
import json
from randomize import randomize
import js

# TODO: This file is still mostly broken at the moment, but all functionality for this file will be retained
# So for now we're just moving it into the proper location and using it as needed


def reset_progress_bar():
    """Reset the progress bar once it has completed."""
    try:
        js.jquery("#patchprogress").removeClass("bg-danger")
    except Exception:
        pass
    js.update_progres_modal("hide", "", "0%")


def start_randomizing_seed(form_data: dict):
    """Randomize the seed data using the passed dict.

    Args:
        form_data (dict): Passed JSON Data.
    """
    js.update_progres_modal("show", "Randomizing Seed.", "30%")

    def randomize_seed_data():
        randomized_data = randomize(form_data)
        timer.set_timeout(lambda: finish_rando(randomized_data), 1000)

    def finish_rando(randomized_data):
        js.update_progres_modal("show", "Randomizing Complete.", "40%")
        timer.set_timeout(lambda: finish_randomizing_seed(randomized_data, form_data), 1000)

    timer.set_timeout(randomize_seed_data, 1000)


def finish_randomizing_seed(data, form_data):
    """Randomized Generation completed.

    Args:
        data (str): Code of seed randomization.
        form_data (dict): Dict data of the form.
    """
    if data is False:
        js.update_progres_modal("show", "Failed to successfully generate a seed.", "100%", "bg-danger")
    else:
        if document["downloadjson"].checked:

            def save_lanky():
                js.update_progres_modal("show", "Patch File Generated.", "100%")
                file = js.File.new(
                    [json.dumps(form_data)],
                    "dk64r-settings-" + form_data.get("seed") + ".lanky",
                )
                js.saveAs(file)

            timer.set_timeout(save_lanky, 2000)
        else:
            start_apply_patch()
    timer.set_timeout(reset_progress_bar, 5000)


def start_apply_patch():
    """Apply the stored write seeks to the rom."""
    # Convert the rom type to z64
    js.romFile.convert()
    # Apply the BPS
    js.update_progres_modal("show", "Applying Patches", "80%")

    js.apply_bps_javascript()
    for opt in js.patchData._data:
        func = dict(opt)
        for key in func:
            if key == "seek":
                js.patchedRom.seek(func.get(key))
            else:
                js.patchedRom.writeU8(func.get(key))
    print("Fixing Checksum")
    timer.set_timeout(fix_checksum, 1000)
    js.patchedRom.fileName = "dk64-randomizer-" + document["seed"].value + ".z64"
    timer.set_timeout(js.patchedRom.save, 3000)


def fix_checksum():
    """Set the security code and update the rom checksum."""
    js.patchedRom.seek(0x3154)
    js.patchedRom.writeU8(0)
    js.fixChecksum(js.patchedRom)
    js.update_progres_modal("show", "Patching Complete", "100%")
