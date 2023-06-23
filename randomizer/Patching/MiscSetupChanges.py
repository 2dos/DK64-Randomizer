"""Apply misc setup changes."""
import math
import random

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Settings import DamageAmount, MiscChangesSelected
from randomizer.Lists.MapsAndExits import LevelMapTable, Maps
from randomizer.Lists.Patches import DirtPatchLocations
from randomizer.Patching.Lib import float_to_hex
from randomizer.Patching.Patcher import ROM, LocalROM


def pickRandomPositionCircle(center_x, center_z, min_radius, max_radius):
    """Pick a random position within a torus where the center and radius boundaries are specified."""
    radius = min_radius + (math.sqrt(random.random()) * (max_radius - min_radius))
    angle = random.uniform(0, math.pi * 2)
    if angle == math.pi * 2:
        angle = 0
    item_dx = radius * math.sin(angle)
    item_dz = radius * math.cos(angle)
    item_x = center_x + item_dx
    item_z = center_z + item_dz
    return [item_x, item_z]


def pickRandomPositionsMult(center_x, center_z, min_radius, max_radius, count, min_dist):
    """Pick multiple points within a torus where the center and radius boundaries are defined. There is a failsafe to make sure 2 points aren't within a certain specified distance away from each other."""
    picked = []
    for item in range(count):
        good_place = False
        while not good_place:
            selected = pickRandomPositionCircle(center_x, center_z, min_radius, max_radius)
            if len(picked) == 0:
                good_place = True
            else:
                good_place = True
                for picked_item in picked:
                    dx = picked_item[0] - selected[0]
                    dz = picked_item[1] - selected[1]
                    delta = math.sqrt((dx * dx) + (dz * dz))
                    if delta < min_dist:
                        good_place = False
            if good_place:
                picked.append(selected)
    return {"picked": picked.copy(), "index": 0}


def pickChunkyCabinPadPositions():
    """Pick 3 points within a torus in Chunky's 5-door cabin where the center and radius boundaries are defined. There are failsafes to make sure 2 points are far enough apart and all points are easy enough to reach for casual game play purposes."""
    picked_pads = []
    # lamp_halfway_points are the center of the moving light circles when they are in their halfway points along their routes
    lamp_halfway_points = [[169.53, 205.91], [435.219, 483.118]]
    center_of_room = [294.594, 337.22]
    lamp_radius = 70  # lamp radius is 65-70 but safe to use 70
    for count in range(3):
        good_pad = False
        while not good_pad:
            pad = pickRandomPositionCircle(center_of_room[0], center_of_room[1], 70, 180)
            # check if pad is in a difficult spot to clear and if so, get the pad out of the difficult spot
            for lamp in lamp_halfway_points:
                # check if pad is in a lamp's radius when said lamp is on its halfway point
                dx = pad[0] - lamp[0]
                dz = pad[1] - lamp[1]
                delta = math.sqrt((dx * dx) + (dz * dz))
                # pad is in the radius mentioned in the comment above. Move the pad out of this radius
                if delta < lamp_radius:
                    suggested_x = pad[0]
                    if lamp[0] < center_of_room[0]:
                        suggested_x = suggested_x + 70
                    else:
                        suggested_x = suggested_x - 70
                    suggested_z = pad[1]
                    if lamp[1] < center_of_room[1]:
                        suggested_z = suggested_z + 70
                    else:
                        suggested_z = suggested_z - 70
                    pad = random.choice([[suggested_x, pad[1]], [pad[0], suggested_z]])
            # check if the pad is far inside and near the lamp radius (not in it, as that's what we fixed above)
            # top right has a Low X and Low Z coordinate, bottom left has a high X and High Z coordinate
            is_far_inside_top_right = lamp_halfway_points[0][0] < pad[0] < center_of_room[0] and lamp_halfway_points[0][1] < pad[1] < center_of_room[1]
            is_far_inside_bottom_left = center_of_room[0] < pad[0] < lamp_halfway_points[1][0] and center_of_room[1] < pad[1] < lamp_halfway_points[1][1]
            if is_far_inside_top_right or is_far_inside_bottom_left:
                # flip the coordinates horizontally, this effectively moves the pad one quadrant clockwise
                mirror_line = 294.594
                difference = pad[0] - mirror_line
                pad[0] = mirror_line - difference
            # check if any pads overlap
            if len(picked_pads) == 0:
                good_pad = True
            else:
                good_pad = True
                for previously_picked_item in picked_pads:
                    dx = previously_picked_item[0] - pad[0]
                    dz = previously_picked_item[1] - pad[1]
                    delta = math.sqrt((dx * dx) + (dz * dz))
                    if delta < 70:
                        good_pad = False
            if good_pad:
                picked_pads.append(pad)
    return {"picked": picked_pads.copy(), "index": 0}


def randomize_setup(spoiler):
    """Randomize setup."""
    pickup_weights = [
        {"item": "orange", "type": 0x56, "weight": 3},
        {"item": "film", "type": 0x98, "weight": 1},
        {"item": "crystals", "type": 0x8E, "weight": 4},
        {"item": "standard_crate", "type": 0x8F, "weight": 4},
        {"item": "homing_crate", "type": 0x11, "weight": 2},
        # {
        #     "item": "feather_single",
        #     "type": 0x15D,
        #     "weight": 3,
        # },
        # {
        #     "item": "grape_single",
        #     "type": 0x15E,
        #     "weight": 3,
        # },
        # {
        #     "item": "pineapple_single",
        #     "type": 0x15F,
        #     "weight": 3,
        # },
        # {
        #     "item": "coconut_single",
        #     "type": 0x160,
        #     "weight": 3,
        # },
        # {
        #     "item": "peanut_single",
        #     "type": 0x91,
        #     "weight": 3,
        # },
    ]
    pickup_list = []
    for pickup in pickup_weights:
        for count in range(pickup["weight"]):
            pickup_list.append(pickup["type"])

    allowed_settings = [
        spoiler.settings.fast_gbs,
        spoiler.settings.randomize_pickups,
        spoiler.settings.random_patches,
        spoiler.settings.puzzle_rando,
        spoiler.settings.hard_bosses,
        spoiler.settings.high_req,
        MiscChangesSelected.raise_fungi_dirt_patch in spoiler.settings.misc_changes_selected,
    ]
    enabled = False
    for setting in allowed_settings:
        enabled = enabled or setting
    swap_list = [
        {"map": Maps.AztecLlamaTemple, "item_list": [0xBC, 0x22B, 0x229, 0x22A]},
        {"map": Maps.AztecTinyTemple, "item_list": [0xA7, 0xA6, 0xA5, 0xA4]},
        {"map": Maps.FranticFactory, "item_list": [0x14D, 0x14C, 0x14B, 0x14A]},
        {"map": Maps.CastleCrypt, "item_list": [0x247, 0x248, 0x249, 0x24A]},
    ]
    if not spoiler.settings.perma_death and spoiler.settings.damage_amount not in (DamageAmount.quad, DamageAmount.ohko):
        swap_list.append({"map": Maps.CastleMuseum, "item_list": [0x17]})
    number_gb_data = [
        {"subtype": "corner", "numbers": [{"number": 12, "rot": 0}, {"number": 3, "rot": 1}, {"number": 5, "rot": 2}, {"number": 6, "rot": 3}]},
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
        {"subtype": "center", "numbers": [{"number": 13, "rot": 0}, {"number": 15, "rot": 0}, {"number": 11, "rot": 0}, {"number": 2, "rot": 0}]},
    ]
    vase_puzzle_positions = [
        # [365.533, 138.167, 717.282], # Exclude center to force it to be a vase
        [212.543, 120.5, 963.536],
        [100.017, 120.5, 569.51],
        [497.464, 120.5, 458.709],
        [401.557, 138.167, 754.136],
        [318.119, 138.167, 752.011],
        [311.555, 138.167, 666.162],
        [398.472, 138.167, 668.426],
    ]

    if enabled:
        diddy_5di_pads = pickRandomPositionsMult(287.94, 312.119, 0, 140, 6, 40)
        lanky_fungi_mush = pickRandomPositionsMult(274.9, 316.505, 40, 160, 5, 40)
        chunky_5dc_pads = pickChunkyCabinPadPositions()
        random.shuffle(vase_puzzle_positions)
        vase_puzzle_rando_progress = 0
        raise_patch = (MiscChangesSelected.raise_fungi_dirt_patch in spoiler.settings.misc_changes_selected) or (len(spoiler.settings.misc_changes_selected) == 0)
        for cont_map_id in range(216):
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            LocalROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            # Puzzle Stuff
            offsets = []
            positions = []
            if cont_map_id == Maps.FranticFactory:
                number_replacement_data = {"corner": {"offsets": [], "positions": []}, "edge": {"offsets": [], "positions": []}, "center": {"offsets": [], "positions": []}}
            for model2_item in range(model2_count):
                item_start = cont_map_setup_address + 4 + (model2_item * 0x30)
                LocalROM().seek(item_start + 0x28)
                item_type = int.from_bytes(LocalROM().readBytes(2), "big")
                is_swap = False
                for swap in swap_list:
                    if swap["map"] == cont_map_id and item_type in swap["item_list"]:
                        is_swap = True
                if item_type == 0x196 and spoiler.settings.fast_gbs and cont_map_id == Maps.FactoryBaboonBlast:
                    LocalROM().seek(item_start + 0x28)
                    LocalROM().writeMultipleBytes(0x74, 2)
                    LocalROM().seek(item_start + 0xC)
                    LocalROM().writeMultipleBytes(0x3F000000, 4)  # Scale: 0.5
                elif item_type in pickup_list and spoiler.settings.randomize_pickups:
                    LocalROM().seek(item_start + 0x28)
                    LocalROM().writeMultipleBytes(random.choice(pickup_list), 2)
                elif is_swap:
                    if spoiler.settings.puzzle_rando:
                        offsets.append(item_start)
                        LocalROM().seek(item_start)
                        x = int.from_bytes(LocalROM().readBytes(4), "big")
                        y = int.from_bytes(LocalROM().readBytes(4), "big")
                        z = int.from_bytes(LocalROM().readBytes(4), "big")
                        LocalROM().seek(item_start + 0x1C)
                        ry = int.from_bytes(LocalROM().readBytes(4), "big")
                        positions.append([x, y, z, ry])
                elif item_type == 0x235 and ((cont_map_id == Maps.GalleonBoss and spoiler.settings.hard_bosses) or (cont_map_id == Maps.HideoutHelm and spoiler.settings.puzzle_rando)):
                    if cont_map_id == Maps.HideoutHelm:
                        y_position = random.uniform(-131, 500)
                        star_donut_center = [1055.704, 3446.966]
                        if y_position < 0:
                            star_donut_boundaries = [230, 300.971]
                        else:
                            star_donut_boundaries = [123.128, 235.971]
                        star_height_boundaries = [y_position, y_position]
                    elif cont_map_id == Maps.GalleonBoss:
                        star_donut_center = [1216, 1478]
                        star_donut_boundaries = [200, 460]
                        star_height_boundaries = []
                    star_pos = pickRandomPositionCircle(star_donut_center[0], star_donut_center[1], star_donut_boundaries[0], star_donut_boundaries[1])
                    star_a = random.uniform(0, 360)
                    if star_a == 360:
                        star_a = 0
                    star_x = star_pos[0]
                    star_z = star_pos[1]
                    LocalROM().seek(item_start)
                    LocalROM().writeMultipleBytes(int(float_to_hex(star_x), 16), 4)
                    LocalROM().seek(item_start + 8)
                    LocalROM().writeMultipleBytes(int(float_to_hex(star_z), 16), 4)
                    LocalROM().seek(item_start + 0x1C)
                    LocalROM().writeMultipleBytes(int(float_to_hex(star_a), 16), 4)
                    if len(star_height_boundaries) > 0:
                        star_y = random.uniform(star_height_boundaries[0], star_height_boundaries[1])
                        LocalROM().seek(item_start + 4)
                        LocalROM().writeMultipleBytes(int(float_to_hex(star_y), 16), 4)
                elif item_type == 0x74 and cont_map_id == Maps.GalleonLighthouse and spoiler.settings.high_req:
                    new_gb_coords = [407.107, 720, 501.02]
                    for coord_i, coord in enumerate(new_gb_coords):
                        LocalROM().seek(item_start + (coord_i * 4))
                        LocalROM().writeMultipleBytes(int(float_to_hex(coord), 16), 4)
                elif cont_map_id == Maps.FranticFactory and spoiler.settings.puzzle_rando and item_type >= 0xF4 and item_type <= 0x103:
                    for subtype_item in number_gb_data:
                        for num_item in subtype_item["numbers"]:
                            if num_item["number"] == (item_type - 0xF3):
                                subtype_name = subtype_item["subtype"]
                                LocalROM().seek(item_start)
                                x = int.from_bytes(LocalROM().readBytes(4), "big")
                                y = int.from_bytes(LocalROM().readBytes(4), "big")
                                z = int.from_bytes(LocalROM().readBytes(4), "big")
                                number_replacement_data[subtype_name]["offsets"].append({"offset": item_start, "rotation": num_item["rot"], "number": item_type - 0xF3})
                                number_replacement_data[subtype_name]["positions"].append({"coords": [x, y, z], "rotation": num_item["rot"]})
                elif cont_map_id == Maps.ForestLankyMushroomsRoom and spoiler.settings.puzzle_rando:
                    if item_type >= 0x1BA and item_type <= 0x1BE:  # Mushrooms
                        spawner_pos = lanky_fungi_mush["picked"][lanky_fungi_mush["index"]]
                        LocalROM().seek(item_start)
                        LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                        LocalROM().seek(item_start + 8)
                        LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                        lanky_fungi_mush["index"] += 1
                    elif item_type == 0x205:  # Lanky Bunch
                        spawner_pos = lanky_fungi_mush["picked"][0]
                        LocalROM().seek(item_start)
                        LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                        LocalROM().seek(item_start + 8)
                        LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                elif cont_map_id == Maps.AngryAztec and spoiler.settings.puzzle_rando and (item_type == 0x121 or (item_type >= 0x226 and item_type <= 0x228)):
                    # Is Vase Pad
                    LocalROM().seek(item_start)
                    for coord in range(3):
                        LocalROM().writeMultipleBytes(int(float_to_hex(vase_puzzle_positions[vase_puzzle_rando_progress][coord]), 16), 4)
                    vase_puzzle_rando_progress += 1
                elif cont_map_id == Maps.CavesChunkyCabin and spoiler.settings.puzzle_rando and item_type == 0x203:
                    spawner_pos = chunky_5dc_pads["picked"][chunky_5dc_pads["index"]]
                    LocalROM().seek(item_start)
                    LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                    LocalROM().seek(item_start + 8)
                    LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                    chunky_5dc_pads["index"] += 1

            if spoiler.settings.puzzle_rando:
                if len(positions) > 0 and len(offsets) > 0:
                    random.shuffle(positions)
                    for index, offset in enumerate(offsets):
                        LocalROM().seek(offset)
                        for coord in range(3):
                            LocalROM().writeMultipleBytes(positions[index][coord], 4)
                        LocalROM().seek(offset + 0x1C)
                        LocalROM().writeMultipleBytes(positions[index][3], 4)
                if cont_map_id == Maps.FranticFactory:
                    rotation_hexes = ["0x00000000", "0x42B40000", "0x43340000", "0x43870000"]  # 0  # 90  # 180  # 270
                    for subtype in number_replacement_data:
                        subtype_name = subtype
                        subtype = number_replacement_data[subtype]
                        random.shuffle(subtype["positions"])
                        for index, offset in enumerate(subtype["offsets"]):
                            LocalROM().seek(offset["offset"])
                            base_rot = offset["rotation"]
                            for coord in range(3):
                                coord_val = subtype["positions"][index]["coords"][coord]
                                if coord == 1:
                                    coord_val = int(float_to_hex(1002), 16)
                                LocalROM().writeMultipleBytes(coord_val, 4)
                            new_rot = subtype["positions"][index]["rotation"]
                            rot_diff = ((base_rot - new_rot) + 4) % 4
                            if subtype_name == "center":
                                rot_diff = random.randint(0, 3)
                            LocalROM().seek(offset["offset"] + 0x1C)
                            new_rot = (2 + rot_diff) % 4
                            LocalROM().writeMultipleBytes(int(rotation_hexes[new_rot], 16), 4)

            LocalROM().seek(cont_map_setup_address + 4 + (model2_count * 0x30))
            mystery_count = int.from_bytes(LocalROM().readBytes(4), "big")
            actor_block_start = cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24)
            LocalROM().seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
            actor_count = int.from_bytes(LocalROM().readBytes(4), "big")
            actor_bytes = []
            used_actor_ids = []
            for actor_item in range(actor_count):
                actor_start = actor_block_start + 4 + (actor_item * 0x38)
                LocalROM().seek(actor_start + 0x32)
                actor_type = int.from_bytes(LocalROM().readBytes(2), "big") + 0x10
                if spoiler.settings.random_patches:
                    if not actor_type == 139:
                        byte_list = []
                        LocalROM().seek(actor_start + 0x34)
                        used_actor_ids.append(int.from_bytes(LocalROM().readBytes(2), "big"))
                        LocalROM().seek(actor_start)
                        for x in range(int(0x38 / 4)):
                            byte_list.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                        actor_bytes.append(byte_list.copy())
            if spoiler.settings.random_patches:
                new_actor_id = 0x20
                for dirt_item in spoiler.dirt_patch_placement:
                    for patch in DirtPatchLocations:
                        if patch.map_id == cont_map_id and patch.name == dirt_item["name"]:
                            if new_actor_id in used_actor_ids:
                                while new_actor_id in used_actor_ids:
                                    new_actor_id += 1
                            dirt_bytes = []
                            dirt_bytes.append(int(float_to_hex(patch.x), 16))
                            if patch.is_fungi_hidden_patch and raise_patch:
                                dirt_bytes.append(int(float_to_hex(155), 16))
                            else:
                                dirt_bytes.append(int(float_to_hex(patch.y), 16))
                            dirt_bytes.append(int(float_to_hex(patch.z), 16))
                            dirt_bytes.append(int(float_to_hex(patch.scale), 16))
                            for x in range(8):
                                dirt_bytes.append(0)
                            rot_type_hex = hex(patch.rotation) + "007B"
                            dirt_bytes.append(int(rot_type_hex, 16))
                            id_something_hex = hex(new_actor_id) + "46D0"
                            used_actor_ids.append(new_actor_id)
                            new_actor_id += 1
                            dirt_bytes.append(int(id_something_hex, 16))
                            actor_bytes.append(dirt_bytes)
                    LocalROM().seek(actor_block_start)
                    LocalROM().writeMultipleBytes(len(actor_bytes), 4)
                    for actor in actor_bytes:
                        for byte_list in actor:
                            LocalROM().writeMultipleBytes(byte_list, 4)
            # Re-run through actor stuff for changes
            LocalROM().seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
            actor_count = int.from_bytes(LocalROM().readBytes(4), "big")
            diddy_5di_pos = []
            for actor_item in range(actor_count):
                actor_start = actor_block_start + 4 + (actor_item * 0x38)
                LocalROM().seek(actor_start + 0x32)
                actor_type = int.from_bytes(LocalROM().readBytes(2), "big") + 0x10
                LocalROM().seek(actor_start + 0x34)
                actor_id = int.from_bytes(LocalROM().readBytes(2), "big")
                if actor_type >= 100 and actor_type <= 105 and spoiler.settings.puzzle_rando and cont_map_id == Maps.CavesDiddyIgloo:  # 5DI Spawner
                    spawner_pos = diddy_5di_pads["picked"][diddy_5di_pads["index"]]
                    LocalROM().seek(actor_start)
                    LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                    LocalROM().seek(actor_start + 8)
                    LocalROM().writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                    diddy_5di_pads["index"] += 1
                elif actor_type >= 64 and actor_type <= 66 and spoiler.settings.puzzle_rando and cont_map_id == Maps.AngryAztec:  # Exclude O Vase to force it to be vanilla
                    # Vase
                    LocalROM().seek(actor_start)
                    for coord in range(3):
                        LocalROM().writeMultipleBytes(int(float_to_hex(vase_puzzle_positions[vase_puzzle_rando_progress][coord]), 16), 4)
                    vase_puzzle_rando_progress += 1
                elif actor_type == 139 and raise_patch and not spoiler.settings.random_patches:
                    if cont_map_id == Maps.FungiForest and actor_id == 47:
                        LocalROM().seek(actor_start + 4)
                        LocalROM().writeMultipleBytes(int(float_to_hex(155), 16), 4)


def updateRandomSwitches(spoiler):
    """Update setup to account for random switch placement."""
    if spoiler.settings.alter_switch_allocation:
        switches = {
            Kongs.donkey: [0x94, 0x16C, 0x167],
            Kongs.diddy: [0x93, 0x16B, 0x166],
            Kongs.lanky: [0x95, 0x16D, 0x168],
            Kongs.tiny: [0x96, 0x16E, 0x169],
            Kongs.chunky: [0xB8, 0x16A, 0x165],
        }
        all_switches = []
        for kong in switches:
            all_switches.extend(switches[kong])
        for level in LevelMapTable:
            if level not in (Levels.DKIsles, Levels.HideoutHelm):
                switch_level = spoiler.settings.switch_allocation[level]
                if switch_level > 0:
                    switch_level -= 1
                acceptable_maps = LevelMapTable[level].copy()
                if level == Levels.GloomyGalleon:
                    acceptable_maps.append(Maps.GloomyGalleonLobby)  # Galleon lobby internally in the game is galleon, but isn't in rando files. Quick fix for this
                for map in acceptable_maps:
                    file_start = js.pointer_addresses[9]["entries"][map]["pointing_to"]
                    LocalROM().seek(file_start)
                    model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
                    for model2_item in range(model2_count):
                        item_start = file_start + 4 + (model2_item * 0x30)
                        LocalROM().seek(item_start + 0x28)
                        item_type = int.from_bytes(LocalROM().readBytes(2), "big")
                        if item_type in all_switches:
                            for kong in switches:
                                if item_type in switches[kong]:
                                    LocalROM().seek(item_start + 0x28)
                                    LocalROM().writeMultipleBytes(switches[kong][switch_level], 2)
