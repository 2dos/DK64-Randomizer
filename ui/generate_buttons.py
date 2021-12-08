"""File containing main UI button events that travel between tabs."""
from sys import path
from js import document
import js
from ui.bindings import bind
import json
import inspect
from ui.rando_options import update_disabled_progression
from randomizer.rando_test import run
import randomizer.worker as worker

# from datetime import datetime


@bind("change", "jsonfileloader")
def lanky_file_changed(event):
    """On the event of a lanky file being loaded.

    Args:
        event (event): Javascript event.
    """

    def onload(e):
        loaded_json = json.loads(e.target.result)
        for key in loaded_json:
            if loaded_json[key] is True:
                document.getElementsByName(key)[0].checked = True
            elif loaded_json[key] is False:
                document.getElementsByName(key)[0].checked = False
            else:
                document.getElementsByName(key)[0].value = loaded_json[key]

    for uploaded_file in document.getElementById("jsonfileloader").files:
        file = uploaded_file
        break
    reader = js.FileReader.new()
    reader.readAsText(file)
    reader.addEventListener("load", onload)


@bind("click", "generate_lanky_seed")
@bind("click", "generate_seed")
def generate_seed(event):
    """Generate a seed based off the current settings.

    Args:
        event (event): Javascript click event.
    """
    if not document.getElementById("input-file-rom").value:
        document.getElementById("input-file-rom").select()
    else:
        js.update_progres_modal("show", "Initalizing", "0%")
        disabled_options = []
        for element in document.getElementsByTagName("input"):
            if element.disabled:
                disabled_options.append(element)
                element.removeAttribute("disabled")
        for element in document.getElementsByTagName("select"):
            if element.disabled:
                disabled_options.append(element)
                element.removeAttribute("disabled")
        form = js.jquery("#form").serializeArray()
        form_data = {}
        for obj in form:
            if obj.value.lower() in ["true", "false"]:
                form_data[obj.name] = bool(obj.value)
            else:
                form_data[obj.name] = obj.value
        for element in document.getElementsByTagName("input"):
            if element.type == "checkbox" and not element.checked:
                if not form_data.get(element.name):
                    form_data[element.name] = False
        for element in disabled_options:
            element.setAttribute("disabled", "disabled")
        # TODO: This is the entrypoint of builds, we need to make sure we properly set this up
        # print(form_data)
        # print(datetime.now())
        # worker.background(run, ["'assumed'"], test)
        # This is what the returning function used to be
        # patch_files.start_randomizing_seed(dict(data.get("form_data"))


@bind("click", "nav-seed-gen-tab")
@bind("click", "nav-patch-tab")
def disable_input(event):
    """Disable input for each tab as we rotate through the navbar.

    Args:
        event (DOMEvent): DOM item that triggered the event.
    """
    ev_type = False
    try:
        if "patch-tab" in event.target.id:
            ev_type = True
    except Exception:
        pass
    if ev_type is False:
        update_disabled_progression(None)
        try:
            document.getElementById("input-file-rom").id = "input-file-rom_2"
        except Exception:
            pass
        document.getElementById("input-file-rom_1").id = "input-file-rom"
    else:
        try:
            document.getElementById("input-file-rom").id = "input-file-rom_1"
        except Exception:
            pass
        document.getElementById("input-file-rom_2").id = "input-file-rom"


disable_input(None)
