"""Apply barrel changes."""
import js
import random
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def randomize_setup(spoiler: Spoiler):
    """Randomize setup."""
    pickup_list = [
        0x56,  # Oranges
        0x98,  # Film
        0x8E,  # Crystals
        0x8F,  # Standard Ammo Crate
        0x11,  # Homing Ammo Crate
    ]
    if spoiler.settings.skip_arcader1 or spoiler.settings.randomize_pickups:
        for cont_map_id in range(216):
            if (not spoiler.settings.randomize_pickups and spoiler.settings.skip_arcader1 and cont_map_id == 0x6E) or spoiler.settings.randomize_pickups:
                cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
                ROM().seek(cont_map_setup_address)
                model2_count = int.from_bytes(ROM().readBytes(4), "big")
                for model2_item in range(model2_count):
                    item_start = cont_map_setup_address + 4 + (model2_item * 0x30)
                    ROM().seek(item_start + 0x28)
                    item_type = int.from_bytes(ROM().readBytes(2), "big")
                    if item_type == 0x196 and spoiler.settings.skip_arcader1 and cont_map_id == 0x6E:
                        ROM().seek(item_start + 0x28)
                        ROM().writeMultipleBytes(0x74, 2)
                        ROM().seek(item_start + 0xC)
                        ROM().writeMultipleBytes(0x3F000000, 4)  # Scale: 0.5
                    elif item_type in pickup_list and spoiler.settings.randomize_pickups:
                        ROM().seek(item_start + 0x28)
                        ROM().writeMultipleBytes(random.choice(pickup_list), 2)
