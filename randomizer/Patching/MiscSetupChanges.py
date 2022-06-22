"""Apply barrel changes."""
import js
import random
import struct
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Lists.Patches import DirtPatchLocations

def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])

def randomize_setup(spoiler: Spoiler):
    """Randomize setup."""
    pickup_list = [
        0x56,  # Oranges
        0x98,  # Film
        0x8E,  # Crystals
        0x8F,  # Standard Ammo Crate
        0x11,  # Homing Ammo Crate
    ]
    if spoiler.settings.random_patches:
        dirt_list = []
        for x in DirtPatchLocations:
            x.setPatch(False)
            dirt_list.append(x.name)
        for x in range(16):
            selected_patch_name = random.choice(dirt_list)
            for y in DirtPatchLocations:
                if y.name == selected_patch_name:
                    y.setPatch(True)
                    print(selected_patch_name)
                    dirt_list.remove(selected_patch_name)

    if spoiler.settings.skip_arcader1 or spoiler.settings.randomize_pickups or spoiler.settings.random_patches:
        for cont_map_id in range(216):
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
            ROM().seek(cont_map_setup_address + 4 + (model2_count * 0x30))
            mystery_count = int.from_bytes(ROM().readBytes(4), "big")
            actor_block_start = cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24)
            ROM().seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
            actor_count = int.from_bytes(ROM().readBytes(4), "big")
            actor_bytes = []
            used_actor_ids = []
            for actor_item in range(actor_count):
                actor_start = actor_block_start + 4 + (actor_item * 0x38)
                ROM().seek(actor_start + 0x32)
                actor_type = int.from_bytes(ROM().readBytes(2), "big") + 0x10
                if spoiler.settings.random_patches:
                    if not actor_type == 139:
                        byte_list = []
                        ROM().seek(actor_start + 0x34)
                        used_actor_ids.append(int.from_bytes(ROM().readBytes(2),"big"))
                        ROM().seek(actor_start)
                        for x in range(int(0x38/4)):
                            byte_list.append(int.from_bytes(ROM().readBytes(4),"big"))
                        actor_bytes.append(byte_list.copy())
            if spoiler.settings.random_patches:
                new_actor_id = 0x20
                for patch in DirtPatchLocations:
                    if new_actor_id in used_actor_ids:
                        while new_actor_id in used_actor_ids:
                            new_actor_id += 1
                    if patch.map_id == cont_map_id and patch.selected:
                        dirt_bytes = []
                        dirt_bytes.append(int(float_to_hex(patch.x),16))
                        dirt_bytes.append(int(float_to_hex(patch.y),16))
                        dirt_bytes.append(int(float_to_hex(patch.z),16))
                        dirt_bytes.append(int(float_to_hex(1),16))
                        for x in range(8):
                            dirt_bytes.append(0)
                        rot_type_hex = hex(patch.rotation) + "007B"
                        dirt_bytes.append(int(rot_type_hex,16))
                        id_something_hex = hex(new_actor_id) + "46D0"
                        used_actor_ids.append(new_actor_id)
                        new_actor_id += 1
                        dirt_bytes.append(int(id_something_hex,16))
                        actor_bytes.append(dirt_bytes)
                ROM().seek(actor_block_start)
                ROM().writeMultipleBytes(len(actor_bytes),4)
                for actor in actor_bytes:
                    for byte_list in actor:
                        ROM().writeMultipleBytes(byte_list,4)
                

