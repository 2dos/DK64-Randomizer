"""Apply barrel changes."""
import js
import random
import struct
import math
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Lists.Patches import DirtPatchLocations
from randomizer.Lists.MapsAndExits import Maps


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def randomize_setup(spoiler: Spoiler):
    """Randomize setup."""
    pickup_weights = [
        {
            "item": "orange",
            "type": 0x56,
            "weight": 3,
        },
        {
            "item": "film",
            "type": 0x98,
            "weight": 1,
        },
        {
            "item": "crystals",
            "type": 0x8E,
            "weight": 4,
        },
        {"item": "standard_crate", "type": 0x8F, "weight": 4},
        {
            "item": "homing_crate",
            "type": 0x11,
            "weight": 2,
        },
    ]
    pickup_list = []
    for pickup in pickup_weights:
        for count in range(pickup["weight"]):
            pickup_list.append(pickup["type"])
    if spoiler.settings.random_patches:
        isles_dirt_list = []
        round_one_level_dirt_list = []
        round_two_level_dirt_list = []
        drawn_level = ""
        drawn_group = 0
        for x in DirtPatchLocations:
            x.setPatch(False) 
            if x.level_name == "DK Isles":
                isles_dirt_list.append(x.name)
            else:
                round_one_level_dirt_list.append(x.name) 
                round_two_level_dirt_list.append(x.name) 
        #draw 4 DK Isles Dirt Patches
        for x in range(4):
            selected_patch_name = random.choice(isles_dirt_list)
            for y in DirtPatchLocations:
                if y.name == selected_patch_name:
                    y.setPatch(True)
                    print(selected_patch_name)
                    isles_dirt_list.remove(selected_patch_name)
                    drawn_group = y.group
            #clear out all the patches that should not be selected
            for y in DirtPatchLocations:
                if y.group == drawn_group:
                    isles_dirt_list.remove(y.name)
                
        #Draw 7 non-DK Isles Dirt Patches, none of which are in the same level
        for x in range(7):
            selected_patch_name = random.choice(round_one_level_dirt_list)
            for y in DirtPatchLocations:
                if y.name == selected_patch_name:
                    y.setPatch(True)
                    print(selected_patch_name)
                    round_one_level_dirt_list.remove(selected_patch_name)
                    round_two_level_dirt_list.remove(selected_patch_name) #prevents the dirt patch from being selected in round 2
                    drawn_level = y.level_name
                    drawn_group = y.group
            #clear out all the patches that should not be selected
            for y in DirtPatchLocations:
                if y.level_name == drawn_level:
                    round_one_level_dirt_list.remove(y.name)
                    if y.group == drawn_group:
                        round_two_level_dirt_list.remove(y.name)
                   

        #Draw 5 extra non-DK Isles Dirt Patches, none of which are in the same level
        for x in range(5):
            selected_patch_name = random.choice(round_two_level_dirt_list)
            for y in DirtPatchLocations:
                if y.name == selected_patch_name:
                    y.setPatch(True)
                    print(selected_patch_name)
                    round_two_level_dirt_list.remove(selected_patch_name)
                    drawn_level = y.level_name
           #clear out all the patches that should not be selected
            for y in DirtPatchLocations:
                if y.level_name == drawn_level:
                    round_two_level_dirt_list.remove(y.name)

    allowed_settings = [spoiler.settings.skip_arcader1, spoiler.settings.randomize_pickups, spoiler.settings.random_patches, spoiler.settings.puzzle_rando]
    enabled = False
    for setting in allowed_settings:
        enabled = enabled or setting
    swap_list = [
        {"map": Maps.AztecLlamaTemple, "item_list": [0xBC, 0x22B, 0x229, 0x22A]},
        {"map": Maps.CastleMuseum, "item_list": [0x17]},
    ]
    number_gb_data = [
        {
            "subtype": "corner",
            "numbers": [
                {"number": 12, "rot": 0},
                {"number": 3, "rot": 1},
                {"number": 5, "rot": 2},
                {"number": 6, "rot": 3},
            ],
        },
        {
            "subtype": "edge",
            "numbers": [
                {"number": 8, "rot": 0},
                {"number": 10, "rot": 0},
                {"number": 7, "rot": 1},
                {"number": 16, "rot": 1},
                {"number": 14, "rot": 2},
                {"number": 9, "rot": 2},
                {"number": 4, "rot": 3},
                {"number": 1, "rot": 3},
            ],
        },
        {
            "subtype": "center",
            "numbers": [
                {"number": 13, "rot": 0},
                {"number": 15, "rot": 0},
                {"number": 11, "rot": 0},
                {"number": 2, "rot": 0},
            ],
        },
    ]

    if enabled:
        for cont_map_id in range(216):
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            # Puzzle Stuff
            offsets = []
            positions = []
            if cont_map_id == Maps.FranticFactory:
                number_replacement_data = {
                    "corner": {
                        "offsets": [],
                        "positions": [],
                    },
                    "edge": {
                        "offsets": [],
                        "positions": [],
                    },
                    "center": {
                        "offsets": [],
                        "positions": [],
                    },
                }
            for model2_item in range(model2_count):
                item_start = cont_map_setup_address + 4 + (model2_item * 0x30)
                ROM().seek(item_start + 0x28)
                item_type = int.from_bytes(ROM().readBytes(2), "big")
                is_swap = False
                for swap in swap_list:
                    if swap["map"] == cont_map_id and item_type in swap["item_list"]:
                        is_swap = True
                if item_type == 0x196 and spoiler.settings.skip_arcader1 and cont_map_id == Maps.FactoryBaboonBlast:
                    ROM().seek(item_start + 0x28)
                    ROM().writeMultipleBytes(0x74, 2)
                    ROM().seek(item_start + 0xC)
                    ROM().writeMultipleBytes(0x3F000000, 4)  # Scale: 0.5
                elif item_type in pickup_list and spoiler.settings.randomize_pickups:
                    ROM().seek(item_start + 0x28)
                    ROM().writeMultipleBytes(random.choice(pickup_list), 2)
                elif is_swap:
                    if spoiler.settings.puzzle_rando:
                        offsets.append(item_start)
                        ROM().seek(item_start)
                        x = int.from_bytes(ROM().readBytes(4), "big")
                        y = int.from_bytes(ROM().readBytes(4), "big")
                        z = int.from_bytes(ROM().readBytes(4), "big")
                        positions.append([x, y, z])
                elif (cont_map_id == Maps.GalleonBoss or cont_map_id == Maps.HideoutHelm) and item_type == 0x235 and spoiler.settings.puzzle_rando:
                    if cont_map_id == Maps.HideoutHelm:
                        star_donut_center = [1055.704, 3446.966]
                        star_donut_boundaries = [123.128, 235.971]
                        star_height_boundaries = [-131, 500]
                    elif cont_map_id == Maps.GalleonBoss:
                        star_donut_center = [1216, 1478]
                        star_donut_boundaries = [188, 460]
                        star_height_boundaries = []
                    radius = random.uniform(star_donut_boundaries[0], star_donut_boundaries[1])
                    angle = random.uniform(0, math.pi * 2)
                    star_a = random.uniform(0, 360)
                    if angle == math.pi * 2:
                        angle = 0
                    if star_a == 360:
                        star_a = 0
                    star_dx = radius * math.sin(angle)
                    star_dz = radius * math.cos(angle)
                    star_x = star_donut_center[0] + star_dx
                    star_z = star_donut_center[1] + star_dz
                    ROM().seek(item_start)
                    ROM().writeMultipleBytes(int(float_to_hex(star_x), 16), 4)
                    ROM().seek(item_start + 8)
                    ROM().writeMultipleBytes(int(float_to_hex(star_z), 16), 4)
                    ROM().seek(item_start + 0x1C)
                    ROM().writeMultipleBytes(int(float_to_hex(star_a), 16), 4)
                    if len(star_height_boundaries) > 0:
                        star_y = random.uniform(star_height_boundaries[0], star_height_boundaries[1])
                        ROM().seek(item_start + 4)
                        ROM().writeMultipleBytes(int(float_to_hex(star_y), 16), 4)
                elif cont_map_id == Maps.FranticFactory and spoiler.settings.puzzle_rando and item_type >= 0xF4 and item_type <= 0x103:
                    for subtype_item in number_gb_data:
                        for num_item in subtype_item["numbers"]:
                            if num_item["number"] == (item_type - 0xF3):
                                subtype_name = subtype_item["subtype"]
                                ROM().seek(item_start)
                                x = int.from_bytes(ROM().readBytes(4), "big")
                                y = int.from_bytes(ROM().readBytes(4), "big")
                                z = int.from_bytes(ROM().readBytes(4), "big")
                                number_replacement_data[subtype_name]["offsets"].append({"offset": item_start, "rotation": num_item["rot"], "number": item_type - 0xF3})
                                number_replacement_data[subtype_name]["positions"].append({"coords": [x, y, z], "rotation": num_item["rot"]})

            if spoiler.settings.puzzle_rando:
                if len(positions) > 0 and len(offsets) > 0:
                    random.shuffle(positions)
                    for index, offset in enumerate(offsets):
                        ROM().seek(offset)
                        for coord in range(3):
                            ROM().writeMultipleBytes(positions[index][coord], 4)
                if cont_map_id == Maps.FranticFactory:
                    rotation_hexes = [
                        "0x00000000",  # 0
                        "0x42B40000",  # 90
                        "0x43340000",  # 180
                        "0x43870000",  # 270
                    ]
                    for subtype in number_replacement_data:
                        subtype_name = subtype
                        subtype = number_replacement_data[subtype]
                        random.shuffle(subtype["positions"])
                        for index, offset in enumerate(subtype["offsets"]):
                            ROM().seek(offset["offset"])
                            base_rot = offset["rotation"]
                            for coord in range(3):
                                coord_val = subtype["positions"][index]["coords"][coord]
                                if coord == 1:
                                    coord_val = int(float_to_hex(1002), 16)
                                ROM().writeMultipleBytes(coord_val, 4)
                            new_rot = subtype["positions"][index]["rotation"]
                            rot_diff = ((base_rot - new_rot) + 4) % 4
                            print(f"Number {offset['number']} - Rotation Diff: {rot_diff}")
                            if subtype_name == "center":
                                rot_diff = random.randint(0, 3)
                            ROM().seek(offset["offset"] + 0x1C)
                            new_rot = (2 + rot_diff) % 4
                            ROM().writeMultipleBytes(int(rotation_hexes[new_rot], 16), 4)

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
                        used_actor_ids.append(int.from_bytes(ROM().readBytes(2), "big"))
                        ROM().seek(actor_start)
                        for x in range(int(0x38 / 4)):
                            byte_list.append(int.from_bytes(ROM().readBytes(4), "big"))
                        actor_bytes.append(byte_list.copy())
            if spoiler.settings.random_patches:
                new_actor_id = 0x20
                for patch in DirtPatchLocations:
                    if new_actor_id in used_actor_ids:
                        while new_actor_id in used_actor_ids:
                            new_actor_id += 1
                    if patch.map_id == cont_map_id and patch.selected:
                        dirt_bytes = []
                        dirt_bytes.append(int(float_to_hex(patch.x), 16))
                        dirt_bytes.append(int(float_to_hex(patch.y), 16))
                        dirt_bytes.append(int(float_to_hex(patch.z), 16))
                        dirt_bytes.append(int(float_to_hex(1), 16))
                        for x in range(8):
                            dirt_bytes.append(0)
                        rot_type_hex = hex(patch.rotation) + "007B"
                        dirt_bytes.append(int(rot_type_hex, 16))
                        id_something_hex = hex(new_actor_id) + "46D0"
                        used_actor_ids.append(new_actor_id)
                        new_actor_id += 1
                        dirt_bytes.append(int(id_something_hex, 16))
                        actor_bytes.append(dirt_bytes)
                ROM().seek(actor_block_start)
                ROM().writeMultipleBytes(len(actor_bytes), 4)
                for actor in actor_bytes:
                    for byte_list in actor:
                        ROM().writeMultipleBytes(byte_list, 4)
