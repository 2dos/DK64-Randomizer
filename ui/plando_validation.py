"""Code to collect and validate the selected plando options."""
import js


def populate_plando_options(form):
    """Collect all of the plandomizer options into one object.

    Args:
        form (dict): The serialized form data containing all HTML inputs.
    """
    # If the plandomizer is disabled, return nothing.
    enable_plandomizer = js.document.getElementById("enable_plandomizer")
    if not enable_plandomizer.checked:
        return None

    plando_form_data = {}
    item_objects = []
    shop_item_objects = []
    shop_cost_objects = []
    minigame_objects = []
    hint_objects = []
    for obj in form:
        if not obj.name.startswith("plando_"):
            continue
        # Sort the selects into their appropriate lists.
        if obj.name.endswith("_shop_item"):
            shop_item_objects.append(obj)
            continue
        elif obj.name.endswith("_shop_cost"):
            shop_cost_objects.append(obj)
            continue
        elif obj.name.endswith("_item"):
            item_objects.append(obj)
            continue
        elif obj.name.endswith("_minigame"):
            minigame_objects.append(obj)
            continue
        elif obj.name.endswith("_hint"):
            hint_objects.append(obj)
            continue

        def is_number(s):
            """Check if a string is a number or not."""
            try:
                int(s)
                return True
            except ValueError:
                return False

        # Process any input that hasn't been sorted.
        if obj.value.lower() in ["true", "false"]:
            plando_form_data[obj.name] = bool(obj.value)
        else:
            if is_number(obj.value):
                plando_form_data[obj.name] = int(obj.value)
            else:
                plando_form_data[obj.name] = obj.value
    
    return plando_form_data
