"""Deal with logic for the footer patch files."""
import json

from browser import bind, document, timer, window

import common
from randomize import randomize

jq = window.jQuery


def reset_progress_bar():
    """Reset the progress bar once it has completed."""
    try:
        jq("#patchprogress").removeClass("bg-danger")
    except Exception:
        pass
    jq("#patchprogress").width("0%")
    jq("#progress-text").text("")
    jq("#progressmodal").modal("hide")


@bind(document["nav-seed-gen-tab"], "click")
@bind(document["nav-patch-tab"], "click")
def disable_input(event):
    """Disable input for each tab as we rotate through the navbar.
    Args:
        event (DOMEvent): DOM item that triggered the event.
    """
    ev_type = False
    if "patch-tab" in event.target.id:
        ev_type = True
    inputs = document["form"].select("input")
    for item in document["form"].select(".form-check"):
        inputs.append(item)
    for item in document["form"].select("select"):
        inputs.append(item)
    for item in inputs:
        if ev_type is True:
            item.attrs["disabled"] = "disabled"
        else:
            try:
                del item.attrs["disabled"]
            except Exception:
                pass
    if ev_type is False:
        common.update_disabled_progression()
        try:
            document["input-file-rom"].id = "input-file-rom_2"
        except Exception:
            pass
        document["input-file-rom_1"].id = "input-file-rom"
    else:
        try:
            document["input-file-rom"].id = "input-file-rom_1"
        except Exception:
            pass
        document["input-file-rom_2"].id = "input-file-rom"


def start_randomizing_seed(form_data: dict):
    """Randomize the seed data using the passed dict.
    Args:
        form_data (dict): Passed JSON Data.
    """
    jq("#patchprogress").width("30%")
    jq("#progress-text").text("Randomizing seed")

    def randomize_seed_data():
        randomized_data = randomize(form_data)
        timer.set_timeout(lambda: finish_rando(randomized_data), 1000)

    def finish_rando(randomized_data):
        jq("#patchprogress").width("40%")
        jq("#progress-text").text("Randomizing complete")
        timer.set_timeout(lambda: finish_randomizing_seed(randomized_data, form_data), 1000)

    timer.set_timeout(randomize_seed_data, 1000)


def finish_randomizing_seed(data, form_data):
    """Randomized Generation completed.
    Args:
        data (str): Code of seed randomization.
        form_data (dict): Dict data of the form.
    """
    if data is False:
        jq("#patchprogress").addClass("bg-danger")
        jq("#patchprogress").width("100%")
        jq("#progress-text").text("Failed to successfully generate a seed.")
    else:
        if document["downloadjson"].checked:

            def save_lanky():
                jq("#patchprogress").width("100%")
                jq("#progress-text").text("Patch File Generated.")
                file = window.File.new(
                    [json.dumps(form_data)],
                    "dk64r-settings-" + form_data.get("seed") + ".lanky",
                )
                window.saveAs(file)

            timer.set_timeout(save_lanky, 2000)
        else:
            start_apply_patch()
    timer.set_timeout(reset_progress_bar, 5000)


def start_apply_patch():
    """Apply the stored write seeks to the rom."""
    # Convert the rom type to z64
    window.romFile.convert()
    # Apply the BPS
    jq("#patchprogress").width("80%")
    jq("#progress-text").text("Applying patches")
    window.apply_bps_javascript()
    for opt in window.patchData._data:
        func = dict(opt)
        for key in func:
            if key == "seek":
                window.patchedRom.seek(func.get(key))
            else:
                window.patchedRom.writeU8(func.get(key))
    print("Fixing Checksum")
    timer.set_timeout(fix_checksum, 1000)
    window.patchedRom.fileName = "dk64-randomizer-" + document["seed"].value + ".z64"
    timer.set_timeout(window.patchedRom.save, 3000)


def fix_checksum():
    """Set the security code and update the rom checksum."""
    window.patchedRom.seek(0x3154)
    window.patchedRom.writeU8(0)
    window.fixChecksum(window.patchedRom)
    jq("#patchprogress").width("100%")
    jq("#progress-text").text("Patching Complete")