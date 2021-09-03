"""Common functions used across all pages."""
import json

from browser import bind, document, timer, window, aio

import patch_files

jq = window.jQuery


def update_disabled_progression():
    """Disable certain page flags depending on checkboxes."""
    if document["randomize_progression"].checked:
        try:
            del document["seed"].attrs["disabled"]
        except Exception:
            pass
        try:
            del document["seed_button"].attrs["disabled"]
        except Exception:
            pass
        document["unlock_all_kongs"].attrs["disabled"] = "disabled"
        document["unlock_all_kongs"].checked = True
    else:
        document["seed"].attrs["disabled"] = "disabled"
        document["seed_button"].attrs["disabled"] = "disabled"
        try:
            del document["unlock_all_kongs"].attrs["disabled"]
        except Exception:
            pass


window.progression_clicked = update_disabled_progression


@bind(document["jsonfileloader"], "change")
def lanky_file_changed(event):
    """On the event of a lanky file being loaded.

    Args:
        event (event): Javascript event.
    """

    def onload(e):
        loaded_json = json.loads(e.target.result)
        for key in loaded_json:
            if loaded_json[key] == "True":
                document.getElementsByName(key)[0].checked = True
            elif loaded_json[key] == "False":
                document.getElementsByName(key)[0].checked = False
            else:
                document.getElementsByName(key)[0].value = loaded_json[key]

    file = document["jsonfileloader"].files[0]
    reader = window.FileReader.new()
    reader.readAsText(file)
    reader.bind("load", onload)


@bind(document["generate_lanky_seed"], "click")
@bind(document["generate_seed"], "click")
def generate_seed(event):
    """Generate a seed based off the current settings.

    Args:
        event (event): Javascript click event.
    """
    if not document["input-file-rom_1"].value:
        document["input-file-rom_1"].select()
    else:
        jq("#progressmodal").modal("show")
        jq("#patchprogress").width("0%")
        jq("#progress-text").text("Initalizing")
        disabled_options = []
        for element in document.getElementsByTagName("input"):
            if element.attrs.get("disabled"):
                disabled_options.append(element)
                del element.attrs["disabled"]
        for element in document.getElementsByTagName("select"):
            if element.attrs.get("disabled"):
                disabled_options.append(element)
                del element.attrs["disabled"]
        form = jq("#form").serializeArray()
        form_data = {}
        for obj in form:
            if obj.value.lower() in ["true", "false"]:
                form_data[obj.name] = bool(obj.value)
            else:
                form_data[obj.name] = obj.value
        for element in document.getElementsByTagName("input"):
            if element.type == "checkbox" and not element.attrs.get("checked"):
                if not form_data.get(element.name):
                    form_data[element.name] = False
        for element in disabled_options:
            element.attrs["disabled"] = "disabled"
        update_disabled_progression()
        timer.set_timeout(lambda: patch_files.start_randomizing_seed(form_data), 3000)
