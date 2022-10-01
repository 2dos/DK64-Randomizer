"""Apply item rando changes."""
import random

import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


class ItemData:
    """Stores information about an item placement in ROM."""

    def __init__(self, type, count, model):
        """Initialize with given parameters."""
        self.type = type
        self.count = count
        self.model = model
        self.init_count = count

    def reset(self):
        self.count = self.init_count

    def place(self):
        self.count -= 1


item_distribution = [
    ItemData("golden_banana", 160, 0x74),  # Minus Rareware GB & the 40 Snide GBs
    ItemData("medal", 40, 0x90),
    ItemData("bp_dk", 8, 0xDE),
    ItemData("bp_diddy", 8, 0xE0),
    ItemData("bp_lanky", 8, 0xE1),
    ItemData("bp_tiny", 8, 0xDD),
    ItemData("bp_chunky", 8, 0xDF),
    ItemData("crown", 10, 0x18D),
    ItemData("key", 8, 0x13C),
    ItemData("nintendo_coin", 1, 0x48),
    ItemData("rareware_coin", 1, 0x28F),
    ItemData("rareware_gb", 1, 0x288),
]


def place_randomized_items(spoiler: Spoiler):
    if spoiler.settings.item_rando:
        model_list = []
        for item in item_distribution:
            item.reset()
            if item.model not in model_list:
                model_list.append(item.model)
        for cont_map_id in range(216):
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            for model2_item in range(model2_count):
                item_start = cont_map_setup_address + 4 + (model2_item * 0x30)
                ROM().seek(item_start + 0x28)
                item_type = int.from_bytes(ROM().readBytes(2), "big")
                if item_type in model_list:
                    # Select Item
                    selection = []
                    for item in item_distribution:
                        for count in range(item.count):
                            selection.append(item.type)
                    selected_item = random.choice(selection)
                    selected_item_model = -1
                    for item in item_distribution:
                        if item.type == selected_item:
                            item.place()
                            selected_item_model = item.model
                    if selected_item_model > -1:
                        ROM().seek(item_start + 0x28)
                        ROM().writeMultipleBytes(selected_item_model, 2)
                        item_id = int.from_bytes(ROM().readBytes(2), "big")
                        print(f"Placed {selected_item} at ID {hex(item_id)} in map {hex(cont_map_id)}")
