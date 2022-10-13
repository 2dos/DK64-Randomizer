"""Apply item rando changes."""
import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Types import Types
from randomizer.Enums.Locations import Locations
from randomizer.Patching.Lib import intf_to_float, float_to_hex

model_two_indexes = {
    Types.Banana: 0x74,
    Types.Blueprint: [0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
    Types.Coin: [0x48, 0x28F],  # Nintendo, Rareware
    Types.Key: 0x13C,
    Types.Crown: 0x18D,
    Types.Medal: 0x90,
}

model_two_scales = {
    Types.Banana: 0.25,
    Types.Blueprint: 2,
    Types.Coin: 0.4,
    Types.Key: 0.17,
    Types.Crown: 0.25,
    Types.Medal: 0.22,
}

actor_indexes = {
    Types.Banana: 45,
    Types.Blueprint: [78, 75, 77, 79, 76],
    Types.Key: 72,
    Types.Crown: 86,
}


def place_randomized_items(spoiler: Spoiler):
    """Place randomized items into ROM."""
    if spoiler.settings.item_rando:
        sav = spoiler.settings.rom_data
        ROM().seek(sav + 0x034)
        ROM().write(1)  # Item Rando Enabled
        item_data = spoiler.item_assignment
        model_two_items = [
            0x74,  # GB
            0xDE,  # BP - DK
            0xE0,  # BP - Diddy
            0xE1,  # BP - Lanky
            0xDD,  # BP - Tiny
            0xDF,  # BP - Chunky
            0x48,  # Nintendo Coin
            0x28F,  # Rareware Coin
            0x13C,  # Key
            0x18D,  # Crown
            0x90,  # Medal
            0x288,  # Rareware GB
        ]
        map_items = {}
        bonus_table_offset = 0
        flut_offset = 0  # Flag Look Up Table. Maximum of 399 items (Currently ~261)
        for item in item_data:
            if not item.reward_spot:
                for map_id in item.placement_data:
                    if map_id not in map_items:
                        map_items[map_id] = []
                    numerator = model_two_scales[item.new_item]
                    denominator = model_two_scales[item.old_item]
                    upscale = numerator / denominator
                    map_items[map_id].append(
                        {
                            "id": item.placement_data[map_id],
                            "obj": item.new_item,
                            "kong": item.new_kong,
                            "flag": item.new_flag,
                            "upscale": upscale,
                        }
                    )
            else:
                if item.old_item != Types.Medal:
                    if item.new_item == Types.Blueprint:
                        actor_index = actor_indexes[Types.Blueprint][item.new_kong]
                    else:
                        actor_index = actor_indexes[item.new_item]
                if item.old_item == Types.Blueprint:
                    # Write to BP Table
                    # Just needs to store an array of actors spawned
                    offset = item.old_flag - 469
                    ROM().seek(0x1FF1000 + offset)
                    ROM().write(actor_index)
                elif item.old_item == Types.Crown:
                    # Write to Crown Table
                    crown_flags = [0x261, 0x262, 0x263, 0x264, 0x265, 0x268, 0x269, 0x266, 0x26A, 0x267]
                    ROM().seek(0x1FF10C0 + crown_flags.index(item.old_flag))
                    ROM().write(actor_index)
                elif item.old_item == Types.Key:
                    key_flags = [26, 74, 138, 168, 236, 292, 317, 380]
                    ROM().seek(0x1FF10D0 + key_flags.index(item.old_flag))
                    ROM().write(actor_index)
                elif item.old_item == Types.Medal:
                    # Write to Medal Table
                    # Just need offset of subtype:
                    # 0 = Banana
                    # 1 = BP
                    # 2 = Key
                    # 3 = Crown
                    # 4 = Special Coin
                    # 5 = Medal
                    slots = [Types.Banana, Types.Blueprint, Types.Key, Types.Crown, Types.Coin, Types.Medal]
                    offset = item.old_flag - 549
                    ROM().seek(0x1FF1080 + offset)
                    ROM().write(slots.index(item.new_item))
                elif item.location == Locations.JapesChunkyBoulder:
                    # Write to Boulder Spawn Location
                    ROM().seek(sav + 0x114)
                    ROM().write(actor_index)
                elif item.location == Locations.AztecLankyVulture:
                    # Write to Vulture Spawn Location
                    ROM().seek(sav + 0x115)
                    ROM().write(actor_index)
                elif item.old_item == Types.Banana:
                    # Bonus GB Table
                    ROM().seek(0x1FF1200 + (4 * bonus_table_offset))
                    ROM().writeMultipleBytes(item.old_flag, 2)
                    ROM().writeMultipleBytes(actor_index, 1)
                    bonus_table_offset += 1
            # Write flag lookup table
            ROM().seek(0x1FF2000 + (4 * flut_offset))
            ROM().writeMultipleBytes(item.old_flag, 2)
            ROM().writeMultipleBytes(item.new_flag, 2)
            flut_offset += 1
        # Terminate FLUT
        ROM().seek(0x1FF2000 + (4 * flut_offset))
        ROM().writeMultipleBytes(0xFFFF, 2)
        ROM().writeMultipleBytes(0xFFFF, 2)
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
                            # Scaling fix
                            ROM().seek(start + 0xC)
                            old_scale = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                            new_scale = old_scale * item_slot["upscale"]
                            ROM().seek(start + 0xC)
                            ROM().writeMultipleBytes(int(float_to_hex(new_scale), 16), 4)
                            # Y Offset Fix
                            if item_slot["obj"] == Types.Blueprint:
                                ROM().seek(start + 0x4)
                                old_y = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                                new_y = old_y + (item_slot["upscale"] * 1.25)
                                ROM().seek(start + 0x4)
                                ROM().writeMultipleBytes(int(float_to_hex(new_y), 16), 4)
