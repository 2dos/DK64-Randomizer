"""Code to collect and validate the selected plando options."""
import js
import re

from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems
from randomizer.Enums.Regions import Regions
from randomizer.Lists.Location import LocationList
from randomizer.Lists.Plandomizer import PlannableItemLimits
from randomizer.LogicFiles.Shops import LogicRegions
from randomizer.PlandoUtils import GetNameFromPlandoItem, PlandoEnumMap


def populate_plando_options(form):
    """Collect all of the plandomizer options into one object.

    Args:
        form (dict) - The serialized form data containing all HTML inputs.
    Returns:
        plando_form_data (dict) - The collected plando data. May be None if
            plandomizer is disabled, or the selections are invalid.
        err (str[]) - A list of error strings to be displayed to the user.
            Will be an empty list if there are no errors.
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

    def is_number(s):
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            return False

    def get_enum_or_string_value(valueString, settingName):
        """Obtain the enum or string value for the provided setting.

        Args:
            valueString (str) - The value from the HTML input.
            settingName (str) - The name of the HTML input.
        """
        # Convert empty string values to PlandoItems.Randomize.
        # This is always valid for the plandomizer specifically.
        if valueString == "":
            return PlandoItems.Randomize
        elif settingName in PlandoEnumMap:
            return PlandoEnumMap[settingName][valueString]
        else:
            return valueString

    def is_plando_input(inputName):
        """Determine if an input is a plando input."""
        return inputName is not None and inputName.startswith("plando_")

    # Process all the plando-related inputs.
    for obj in form:
        if not is_plando_input(obj.name):
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

        # Process any input that hasn't been sorted.
        if obj.value.lower() in ["true", "false"]:
            plando_form_data[obj.name] = bool(obj.value)
        else:
            if is_number(obj.value):
                plando_form_data[obj.name] = int(obj.value)
            else:
                plando_form_data[obj.name] = get_enum_or_string_value(obj.value, obj.name)

    # Find all input boxes and verify their checked status.
    for element in js.document.getElementsByTagName("input"):
        if not is_plando_input(element.name):
            continue
        if element.type == "checkbox" and not element.checked:
            if not plando_form_data.get(element.name):
                plando_form_data[element.name] = False

    # Modify multi-selects to provide value lists.
    for element in js.document.getElementsByTagName("select"):
        if not is_plando_input(element.getAttribute("name")):
            continue
        if element.getAttribute("name").endswith("_selected"):
            length = element.options.length
            values = []
            for i in range(0, length):
                if element.options.item(i).selected:
                    val = get_enum_or_string_value(element.options.item(i).value, element.getAttribute("name"))
                    values.append(val)
            plando_form_data[element.getAttribute("name")] = values
    
    locations_map = {}
    # Process all of the inputs we previously sorted into lists.
    for item in item_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_item$", item.name)[1]
        location = Locations[location_name]
        item_value = PlandoItems.Randomize
        if item.value != "":
            item_value = PlandoItems[item.value]
        locations_map[location] = item_value
    # Place Golden Bananas on all of the blueprint rewards.
    for blueprint in LogicRegions[Regions.Snide].locations:
        locations_map[blueprint.id] = PlandoItems.GoldenBanana
    plando_form_data["locations"] = locations_map
    
    shops_map = {}
    for shop_item in shop_item_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_shop_item$", shop_item.name)[1]
        location = Locations[location_name]
        item_value = PlandoItems.Randomize
        if shop_item.value != "":
            item_value = PlandoItems[shop_item.value]
        # Create an object with both the item and the cost. The cost defaults
        # to PlandoItems.Randomize (-1), but may be overwritten later.
        shops_map[location] = {
            "item": item_value,
            "cost": PlandoItems.Randomize
        }
    for shop_cost in shop_cost_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_shop_cost$", shop_cost.name)[1]
        location = Locations[location_name]
        item_cost = PlandoItems.Randomize
        if shop_cost.value != "":
            item_cost = int(shop_cost.value)
            # Update this shop item with the cost.
            shops_map[location]["cost"] = item_cost
    plando_form_data["shops"] = shops_map
    
    minigames_map = {}
    for minigame in minigame_objects:
        # Extract the barrel location name.
        location_name = re.search("^plando_(.+)_minigame$", minigame.name)[1]
        location = Locations[location_name]
        minigame_value = PlandoItems.Randomize
        if minigame.value != "":
            minigame_value = Minigames[minigame.value]
        minigames_map[location] = minigame_value
    plando_form_data["minigames"] = minigames_map
    
    hints_map = {}
    for hint in hint_objects:
        # Extract the hint location.
        location_name = re.search("^plando_(.+)_hint$", hint.name)[1]
        location = Locations[location_name]
        hint_value = PlandoItems.Randomize
        if hint.value != "":
            hint_value = hint.value
        hints_map[location] = hint_value
    plando_form_data["hints"] = hints_map

    return validate_plando_options(plando_form_data)

def validate_plando_options(plando_dict):
    """Validate the plando options against a set of rules.
    
    Args:
        plando_dict (str) - The dictionary containing the plando data.
    """
    errList = []
    # Count all of the items to ensure none have been over-placed.
    count_dict = {}
    for item in plando_dict["locations"].values():
        if item == PlandoItems.Randomize:
            continue
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    for shop in plando_dict["shops"].values():
        if shop["item"] == PlandoItems.Randomize:
            continue
        if shop["item"] in count_dict:
            count_dict[shop["item"]] += 1
        else:
            count_dict[shop["item"]] = 1
    # If any items have exceeded their maximum amounts, add an error.
    for item, itemCount in count_dict.items():
        if item not in PlannableItemLimits:
            continue
        itemMax = PlannableItemLimits[item]
        if itemCount > itemMax:
            maybePluralTimes = "time" if itemMax == 1 else "times"
            errString = f"Item \"{GetNameFromPlandoItem(item)}\" can be placed at most {itemMax} {maybePluralTimes}, but has been placed {itemCount} times."
            if item == PlandoItems.GoldenBanana:
                errString += " (40 Golden Bananas are always allocated to blueprint rewards.)"
            errList.append(errString)
    
    # Ensure that shop costs are within allowed limits.
    for shopLocation, shop in plando_dict["shops"].items():
        shopCost = shop["cost"]
        if shopCost == PlandoItems.Randomize:
            continue
        if shopCost < 0 or shopCost > 255:
            shopName = LocationList[shopLocation].name
            errString = f"Shop costs must be between 0 and 255 coins, but shop \"{shopName}\" has a cost of {shopCost} coins."
            errList.append(errString)
    
    # Ensure that the user starts with at least one Kong.
    if len(plando_dict["plando_starting_kongs_selected"]) < 1:
        errString = "At least one starting Kong, or Random Kong(s), must be selected."
        errList.append(errString)

    return (plando_dict, errList)
