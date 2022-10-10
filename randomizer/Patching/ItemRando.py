"""Apply item rando changes."""
import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Types import Types

model_two_indexes = {
    Types.Banana: 0x74,
    Types.Blueprint: [0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
    Types.Coin: [0x48, 0x28F],  # Nintendo, Rareware
    Types.Key: 0x13C,
    Types.Crown: 0x18D,
    Types.Medal: 0x90,
}


def place_randomized_items(spoiler: Spoiler):
    """Place randomized items into ROM."""
    if spoiler.settings.item_rando:
        item_data = spoiler.item_assignment
        model_two_items = [
            0x74,
            0xDE,
            0xE0,
            0xE1,
            0xDD,
            0xDF,
            0x48,
            0x28F,
            0x13C,
            0x18D,
            0x90,
            0x288,
        ]
        map_items = {}
        for item in item_data:
            if not item.reward_spot:
                for map_id in item.placement_data:
                    if map_id not in map_items:
                        map_items[map_id] = []
                    map_items[map_id].append(
                        {
                            "id": item.placement_data[map_id],
                            "obj": item.new_item,
                            "kong": item.new_kong,
                            "flag": item.new_flag,
                        }
                    )
        # Setup Changes
        for map_id in map_items:
            cont_map_setup_address = js.pointer_addresses[9]["entries"][map_id]["pointing_to"]
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            for item in range(model2_count):
                start = cont_map_setup_address + 4 + (item * 0x30)
                ROM().seek(start + 0x2A)
                item_id = int.from_bytes(ROM().readBytes(2), "big")
                for item_slot in map_items[map_id]:
                    if item_slot["id"] == item_id:
                        ROM().seek(start + 0x28)
                        old_item = int.from_bytes(ROM().readBytes(2), "big")
                        if old_item in model_two_items:
                            ROM().seek(start + 0x28)
                            item_obj_index = 0
                            if item_slot["obj"] == Types.Blueprint:
                                item_obj_index = model_two_indexes[Types.Blueprint][item_slot["kong"]]
                            elif item_slot["obj"] == Types.Coin:
                                item_obj_index = model_two_indexes[Types.Coin][0]
                                if item_slot["flag"] == 379:
                                    item_obj_index = model_two_indexes[Types.Coin][1]
                            else:
                                item_obj_index = model_two_indexes[item_slot["obj"]]
                            ROM().writeMultipleBytes(item_obj_index, 2)
