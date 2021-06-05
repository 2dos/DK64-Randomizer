"""Deal with logic for the footer patch files."""
from browser import document, window


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
        window.progression_clicked()
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


document["nav-seed-gen-tab"].bind("click", disable_input)
document["nav-patch-tab"].bind("click", disable_input)
