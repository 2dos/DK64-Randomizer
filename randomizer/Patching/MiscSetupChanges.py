"""Apply misc setup changes."""

import math
import random

import js
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Settings import (
    DamageAmount,
    PuzzleRando,
    MiscChangesSelected,
    FasterChecksSelected,
    RemovedBarriersSelected,
    KongModels,
    SlamRequirement,
    HardBossesSelected,
    WinConditionComplex,
)
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Enums.Maps import Maps
from randomizer.Lists.MapsAndExits import LevelMapTable
from randomizer.Patching.Lib import IsItemSelected, float_to_hex, intf_to_float
from randomizer.Patching.Patcher import LocalROM


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


def SpeedUpFungiRabbit():
    """Change the speed of the Fungi Rabbit."""
    ROM_COPY = LocalROM()
    file_start = js.pointer_addresses[16]["entries"][Maps.FungiForest]["pointing_to"]
    ROM_COPY.seek(file_start)
    fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset = 2
    fence_bytes = []
    used_fence_ids = []
    if fence_count > 0:
        for x in range(fence_count):
            fence = []
            fence_start = file_start + offset
            ROM_COPY.seek(file_start + offset)
            point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += (point_count * 6) + 2
            ROM_COPY.seek(file_start + offset)
            point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += (point0_count * 10) + 6
            fence_finish = file_start + offset
            fence_size = fence_finish - fence_start
            ROM_COPY.seek(fence_finish - 4)
            used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            ROM_COPY.seek(fence_start)
            for y in range(int(fence_size / 2)):
                fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            fence_bytes.append(fence)
            ROM_COPY.seek(fence_finish)
    spawner_count_location = file_start + offset
    ROM_COPY.seek(spawner_count_location)
    spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset += 2
    spawner_bytes = []
    fairy_spawner_id = None
    for x in range(spawner_count):
        # Parse spawners
        ROM_COPY.seek(file_start + offset)
        enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(file_start + offset + 0x13)
        enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
        init_offset = offset
        ROM_COPY.seek(file_start + offset + 0x11)
        extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        offset += 0x16 + (extra_count * 2)
        end_offset = offset
        if enemy_index == 2:
            # If enemy is the rabbit, adjust stats
            speed_buff = 0.7
            ROM_COPY.seek(file_start + init_offset + 0xD)
            ROM_COPY.write(int(136 * speed_buff))


def getRandomGalleonStarLocation() -> tuple:
    """Get location for the DK Star which opens the treasure room."""
    STAR_MAX_Y = 1657  # Star Y in vanilla game
    boxes = [
        [(1136, 1469, 1704), (1370, STAR_MAX_Y, 2207)],
        [(2010, 1374, 1671), (2912, STAR_MAX_Y, 2216)],
        [(2980, 663, 766), (2983, STAR_MAX_Y, 1311)],
        [(3388, 594, 1834), (3441, STAR_MAX_Y, 2044)],
        [(3731, 515, 1514), (3769, STAR_MAX_Y, 1833)],
    ]
    bound = random.choice(boxes)
    coord = [0, 0, 0]
    for x in range(3):
        coord[x] = random.randint(bound[0][x], bound[1][x])
    return tuple(coord)


def randomize_setup(spoiler):
    """Randomize setup."""
    SpeedUpFungiRabbit()
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
        if pickup["item"] == "film" and spoiler.settings.win_condition_item == WinConditionComplex.krem_kapture:
            # Kremling Kapture requires a lot more film
            pickup["weight"] = 5
        for _ in range(pickup["weight"]):
            pickup_list.append(pickup["type"])

    arcade_r1_shortened = IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterChecksSelected.factory_arcade_round_1)
    lighthouse_on = IsItemSelected(spoiler.settings.remove_barriers_enabled, spoiler.settings.remove_barriers_selected, RemovedBarriersSelected.galleon_seasick_ship)
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

    ROM_COPY = LocalROM()
    diddy_5di_pads = pickRandomPositionsMult(287.94, 312.119, 0, 140, 6, 40)
    lanky_fungi_mush = pickRandomPositionsMult(274.9, 316.505, 40, 160, 5, 40)
    chunky_5dc_pads = pickChunkyCabinPadPositions()
    random.shuffle(vase_puzzle_positions)
    vase_puzzle_rando_progress = 0
    raise_patch = IsItemSelected(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, MiscChangesSelected.raise_fungi_dirt_patch)
    random_pufftoss_stars = IsItemSelected(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardBossesSelected.pufftoss_star_rando)
    higher_pufftoss_stars = IsItemSelected(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardBossesSelected.pufftoss_star_raised)
    removed_crypt_doors = IsItemSelected(spoiler.settings.remove_barriers_enabled, spoiler.settings.remove_barriers_selected, RemovedBarriersSelected.castle_crypt_doors)
    for cont_map_id in range(216):
        cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
        ROM_COPY.seek(cont_map_setup_address)
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        # Puzzle Stuff
        offsets = []
        positions = []
        if cont_map_id == Maps.FranticFactory:
            number_replacement_data = {"corner": {"offsets": [], "positions": []}, "edge": {"offsets": [], "positions": []}, "center": {"offsets": [], "positions": []}}
        for model2_item in range(model2_count):
            item_start = cont_map_setup_address + 4 + (model2_item * 0x30)
            ROM_COPY.seek(item_start + 0x28)
            item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            ROM_COPY.seek(item_start + 0x2A)
            item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            is_swap = False
            for swap in swap_list:
                if swap["map"] == cont_map_id and item_type in swap["item_list"]:
                    is_swap = True
            if item_type == 0x196 and arcade_r1_shortened and cont_map_id == Maps.FactoryBaboonBlast:
                ROM_COPY.seek(item_start + 0x28)
                ROM_COPY.writeMultipleBytes(0x74, 2)
                ROM_COPY.seek(item_start + 0xC)
                ROM_COPY.writeMultipleBytes(0x3F000000, 4)  # Scale: 0.5
            elif item_type in pickup_list and spoiler.settings.randomize_pickups:
                if cont_map_id != Maps.OrangeBarrel:
                    ROM_COPY.seek(item_start + 0x28)
                    ROM_COPY.writeMultipleBytes(random.choice(pickup_list), 2)
            elif is_swap:
                if spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off:
                    offsets.append(item_start)
                    ROM_COPY.seek(item_start)
                    x = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    y = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    z = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(item_start + 0x1C)
                    ry = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    positions.append([x, y, z, ry])
            elif item_type == 0x235 and (
                (cont_map_id == Maps.GalleonBoss and random_pufftoss_stars) or (cont_map_id == Maps.HideoutHelm and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off)
            ):
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
                ROM_COPY.seek(item_start)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(star_x), 16), 4)
                ROM_COPY.seek(item_start + 8)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(star_z), 16), 4)
                ROM_COPY.seek(item_start + 0x1C)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(star_a), 16), 4)
                if len(star_height_boundaries) > 0:
                    star_y = random.uniform(star_height_boundaries[0], star_height_boundaries[1])
                    ROM_COPY.seek(item_start + 4)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(star_y), 16), 4)
            elif item_type == 0x74 and cont_map_id == Maps.GalleonLighthouse and lighthouse_on:
                new_gb_coords = [407.107, 720, 501.02]
                for coord_i, coord in enumerate(new_gb_coords):
                    ROM_COPY.seek(item_start + (coord_i * 4))
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(coord), 16), 4)
            elif cont_map_id == Maps.FranticFactory and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off and item_type >= 0xF4 and item_type <= 0x103:
                for subtype_item in number_gb_data:
                    for num_item in subtype_item["numbers"]:
                        if num_item["number"] == (item_type - 0xF3):
                            subtype_name = subtype_item["subtype"]
                            ROM_COPY.seek(item_start)
                            x = int.from_bytes(ROM_COPY.readBytes(4), "big")
                            y = int.from_bytes(ROM_COPY.readBytes(4), "big")
                            z = int.from_bytes(ROM_COPY.readBytes(4), "big")
                            number_replacement_data[subtype_name]["offsets"].append({"offset": item_start, "rotation": num_item["rot"], "number": item_type - 0xF3})
                            number_replacement_data[subtype_name]["positions"].append({"coords": [x, y, z], "rotation": num_item["rot"]})
            elif cont_map_id == Maps.ForestLankyMushroomsRoom and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off:
                if item_type >= 0x1BA and item_type <= 0x1BE:  # Mushrooms
                    spawner_pos = lanky_fungi_mush["picked"][lanky_fungi_mush["index"]]
                    ROM_COPY.seek(item_start)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                    ROM_COPY.seek(item_start + 8)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                    lanky_fungi_mush["index"] += 1
                elif item_type == 0x205:  # Lanky Bunch
                    spawner_pos = lanky_fungi_mush["picked"][0]
                    ROM_COPY.seek(item_start)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                    ROM_COPY.seek(item_start + 8)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
            elif cont_map_id == Maps.AngryAztec and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off and (item_type == 0x121 or (item_type >= 0x226 and item_type <= 0x228)):
                # Is Vase Pad
                ROM_COPY.seek(item_start)
                for coord in range(3):
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(vase_puzzle_positions[vase_puzzle_rando_progress][coord]), 16), 4)
                vase_puzzle_rando_progress += 1
            elif cont_map_id == Maps.CavesChunkyCabin and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off and item_type == 0x203:
                spawner_pos = chunky_5dc_pads["picked"][chunky_5dc_pads["index"]]
                ROM_COPY.seek(item_start)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                ROM_COPY.seek(item_start + 8)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                chunky_5dc_pads["index"] += 1
            elif cont_map_id == Maps.GloomyGalleon and item_id == 0xC and spoiler.settings.puzzle_rando_difficulty not in (PuzzleRando.off, PuzzleRando.easy):
                coords = list(getRandomGalleonStarLocation())
                ROM_COPY.seek(item_start)
                for x in coords:
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(x), 16), 4)
            # Regular if because it can be combined with regular hard bosses
            if item_type == 0x235 and cont_map_id == Maps.GalleonBoss and higher_pufftoss_stars:
                ROM_COPY.seek(item_start + 4)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(345), 16), 4)
            elif item_type == 0xCE and cont_map_id == Maps.HelmBarrelLankyMaze and spoiler.settings.sprint_barrel_requires_sprint:
                ROM_COPY.seek(item_start + 0x28)
                ROM_COPY.writeMultipleBytes(611, 2)  # Overwrite type of obj to custom "Sprint Switch"
            if spoiler.settings.chunky_phase_slam_req_internal and cont_map_id == Maps.KroolChunkyPhase and item_type == 0x16A:
                slam_pads = {
                    SlamRequirement.green: 0x92,
                    SlamRequirement.blue: 0x16A,
                    SlamRequirement.red: 0x165,
                }
                ROM_COPY.seek(item_start + 0x28)
                ROM_COPY.writeMultipleBytes(slam_pads[spoiler.settings.chunky_phase_slam_req_internal], 2)
            # Delete crypt doors
            if removed_crypt_doors:
                size_down = False
                if cont_map_id == Maps.CastleLowerCave:
                    size_down = item_id in (0x9, 0x6, 0x5, 0x7, 0x8, 0x4, 0x3)
                elif cont_map_id == Maps.CastleCrypt:
                    size_down = item_id in (0xF, 0xE, 0xD)
                if size_down:
                    ROM_COPY.seek(item_start + 0xC)
                    ROM_COPY.writeMultipleBytes(0, 4)

        if spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off:
            if len(positions) > 0 and len(offsets) > 0:
                random.shuffle(positions)
                for index, offset in enumerate(offsets):
                    ROM_COPY.seek(offset)
                    for coord in range(3):
                        ROM_COPY.writeMultipleBytes(positions[index][coord], 4)
                    ROM_COPY.seek(offset + 0x1C)
                    ROM_COPY.writeMultipleBytes(positions[index][3], 4)
            if cont_map_id == Maps.FranticFactory:
                rotation_hexes = ["0x00000000", "0x42B40000", "0x43340000", "0x43870000"]  # 0  # 90  # 180  # 270
                for subtype in number_replacement_data:
                    subtype_name = subtype
                    subtype = number_replacement_data[subtype]
                    random.shuffle(subtype["positions"])
                    for index, offset in enumerate(subtype["offsets"]):
                        ROM_COPY.seek(offset["offset"])
                        base_rot = offset["rotation"]
                        for coord in range(3):
                            coord_val = subtype["positions"][index]["coords"][coord]
                            if coord == 1:
                                coord_val = int(float_to_hex(1002), 16)
                            ROM_COPY.writeMultipleBytes(coord_val, 4)
                        new_rot = subtype["positions"][index]["rotation"]
                        rot_diff = ((base_rot - new_rot) + 4) % 4
                        if subtype_name == "center":
                            rot_diff = random.randint(0, 3)
                        ROM_COPY.seek(offset["offset"] + 0x1C)
                        new_rot = (2 + rot_diff) % 4
                        ROM_COPY.writeMultipleBytes(int(rotation_hexes[new_rot], 16), 4)

        # Mystery
        ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30))
        mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        actor_block_start = cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24)
        ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
        actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        actor_bytes = []
        used_actor_ids = []
        for actor_item in range(actor_count):
            actor_start = actor_block_start + 4 + (actor_item * 0x38)
            ROM_COPY.seek(actor_start + 0x32)
            actor_type = int.from_bytes(ROM_COPY.readBytes(2), "big") + 0x10
            if spoiler.settings.random_patches:
                if not actor_type == 139:
                    byte_list = []
                    ROM_COPY.seek(actor_start + 0x34)
                    id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    used_actor_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    if spoiler.settings.fix_lanky_tiny_prod and cont_map_id == Maps.FranticFactory and id == 16:
                        ROM_COPY.seek(actor_start + 0x14)
                        ROM_COPY.writeMultipleBytes(1, 4)
                    ROM_COPY.seek(actor_start)
                    for x in range(int(0x38 / 4)):
                        byte_list.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    actor_bytes.append(byte_list.copy())
        if spoiler.settings.random_patches:
            new_actor_id = 0x20
            for dirt_item in spoiler.dirt_patch_placement:
                for patch in CustomLocations[dirt_item["level"]]:
                    if patch.map == cont_map_id and patch.name == dirt_item["name"]:
                        patch_scale = min(patch.max_size / 64, 1)
                        if new_actor_id in used_actor_ids:
                            while new_actor_id in used_actor_ids:
                                new_actor_id += 1
                        dirt_bytes = []
                        dirt_bytes.append(int(float_to_hex(patch.coords[0]), 16))
                        if patch.is_fungi_hidden_patch and raise_patch:
                            dirt_bytes.append(int(float_to_hex(155), 16))
                        else:
                            dirt_bytes.append(int(float_to_hex(patch.coords[1]), 16))
                        dirt_bytes.append(int(float_to_hex(patch.coords[2]), 16))
                        dirt_bytes.append(int(float_to_hex(patch_scale), 16))
                        for x in range(8):
                            dirt_bytes.append(0)
                        rot_type_hex = hex(patch.rot_y) + "007B"
                        dirt_bytes.append(int(rot_type_hex, 16))
                        id_something_hex = hex(new_actor_id) + "46D0"
                        used_actor_ids.append(new_actor_id)
                        new_actor_id += 1
                        dirt_bytes.append(int(id_something_hex, 16))
                        actor_bytes.append(dirt_bytes)
                ROM_COPY.seek(actor_block_start)
                ROM_COPY.writeMultipleBytes(len(actor_bytes), 4)
                for actor in actor_bytes:
                    for byte_list in actor:
                        ROM_COPY.writeMultipleBytes(byte_list, 4)
        # Re-run through actor stuff for changes
        ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
        actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        for actor_item in range(actor_count):
            actor_start = actor_block_start + 4 + (actor_item * 0x38)
            ROM_COPY.seek(actor_start + 0x32)
            actor_type = int.from_bytes(ROM_COPY.readBytes(2), "big") + 0x10
            ROM_COPY.seek(actor_start + 0x34)
            actor_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if actor_type >= 100 and actor_type <= 105 and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off and cont_map_id == Maps.CavesDiddyIgloo:  # 5DI Spawner
                spawner_pos = diddy_5di_pads["picked"][diddy_5di_pads["index"]]
                ROM_COPY.seek(actor_start)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[0]), 16), 4)
                ROM_COPY.seek(actor_start + 8)
                ROM_COPY.writeMultipleBytes(int(float_to_hex(spawner_pos[1]), 16), 4)
                diddy_5di_pads["index"] += 1
            elif actor_type >= 64 and actor_type <= 66 and spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off and cont_map_id == Maps.AngryAztec:  # Exclude O Vase to force it to be vanilla
                # Vase
                ROM_COPY.seek(actor_start)
                for coord in range(3):
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(vase_puzzle_positions[vase_puzzle_rando_progress][coord]), 16), 4)
                vase_puzzle_rando_progress += 1
            elif actor_type == 139 and raise_patch and not spoiler.settings.random_patches:
                if cont_map_id == Maps.FungiForest and actor_id == 47:
                    ROM_COPY.seek(actor_start + 4)
                    ROM_COPY.writeMultipleBytes(int(float_to_hex(155), 16), 4)


def updateRandomSwitches(spoiler):
    """Update setup to account for random switch placement."""
    if spoiler.settings.alter_switch_allocation:
        ROM_COPY = LocalROM()
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
                    ROM_COPY.seek(file_start)
                    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    for model2_item in range(model2_count):
                        item_start = file_start + 4 + (model2_item * 0x30)
                        ROM_COPY.seek(item_start + 0x28)
                        item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                        if item_type in all_switches:
                            for kong in switches:
                                if item_type in switches[kong]:
                                    ROM_COPY.seek(item_start + 0x28)
                                    ROM_COPY.writeMultipleBytes(switches[kong][switch_level], 2)


def updateSwitchsanity(spoiler):
    """Update setup to account for switchsanity."""
    if spoiler.settings.switchsanity:
        ROM_COPY = LocalROM()
        switches = {
            SwitchType.SlamSwitch: [
                0x94,
                0x16C,
                0x167,  # DK
                0x93,
                0x16B,
                0x166,  # Diddy
                0x95,
                0x16D,
                0x168,  # Lanky
                0x96,
                0x16E,
                0x169,  # Tiny
                0xB8,
                0x16A,
                0x165,  # Chunky
            ],
            SwitchType.GunSwitch: [0x129, 0x126, 0x128, 0x127, 0x125],
            SwitchType.InstrumentPad: [0xA8, 0xA9, 0xAC, 0xAA, 0xAB],
            SwitchType.PadMove: [0x97, 0xD4, 0x10C, 0x10B, 0x10A],
            SwitchType.MiscActivator: [0x28, 0xC3],
        }
        switchsanity_maps = []
        # Get list of maps which contain a switch affected by switchsanity, to reduce references to pointer table
        for slot in spoiler.settings.switchsanity_data:
            map_id = spoiler.settings.switchsanity_data[slot].map_id
            if map_id not in switchsanity_maps:
                switchsanity_maps.append(map_id)
        for map_id in switchsanity_maps:
            # Get list of ids of objects in map which are affected by switchsanity
            ids_in_map = []
            for slot in spoiler.settings.switchsanity_data:
                if map_id == spoiler.settings.switchsanity_data[slot].map_id:
                    obj_ids = spoiler.settings.switchsanity_data[slot].ids
                    ids_in_map.extend(obj_ids)
            # Handle setup
            file_start = js.pointer_addresses[9]["entries"][map_id]["pointing_to"]
            ROM_COPY.seek(file_start)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for model2_item in range(model2_count):
                item_start = file_start + 4 + (model2_item * 0x30)
                ROM_COPY.seek(item_start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_id in ids_in_map:
                    switch_kong = None
                    switch_type = None
                    switch_offset = None
                    switch_slot = None
                    for slot in spoiler.settings.switchsanity_data:
                        if map_id == spoiler.settings.switchsanity_data[slot].map_id:
                            if item_id in spoiler.settings.switchsanity_data[slot].ids:
                                switch_kong = spoiler.settings.switchsanity_data[slot].kong
                                switch_type = spoiler.settings.switchsanity_data[slot].switch_type
                                switch_offset = int(switch_kong)
                                switch_slot = slot
                                if switch_type == SwitchType.SlamSwitch:
                                    ROM_COPY.seek(item_start + 0x28)
                                    old_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                                    old_level = switches[SwitchType.SlamSwitch].index(old_type) % 3
                                    switch_offset = (3 * int(switch_kong)) + old_level
                    if switch_kong is not None and switch_type is not None and switch_offset is not None:
                        new_obj = switches[switch_type][switch_offset]
                        ROM_COPY.seek(item_start + 0x28)
                        ROM_COPY.writeMultipleBytes(new_obj, 2)
                        if switch_slot == Switches.IslesHelmLobbyGone and switch_type == SwitchType.MiscActivator:
                            if switch_kong == Kongs.diddy:
                                ROM_COPY.seek(item_start + 0xC)
                                ROM_COPY.writeMultipleBytes(0x3F400000, 4)
                            # elif switch_kong == Kongs.donkey:
                            #     ROM_COPY.seek(item_start + 0x1C)
                            #     ROM_COPY.writeMultipleBytes(0, 4)


def updateKrushaMoveNames(spoiler):
    """Replace move names for the kong that Krusha replaces."""
    move_data = {
        Kongs.donkey: [
            {"textbox_index": 36, "mode": "replace_whole", "target": "LIME BAZOOKA"},
            {"textbox_index": 6, "mode": "replace_whole", "target": "KANNON BLAST"},
            {"textbox_index": 8, "mode": "replace_whole", "target": "STRONG KROC"},
            {"textbox_index": 10, "mode": "replace_whole", "target": "GATOR GRAB"},
            {"textbox_index": 62, "mode": "replace_whole", "target": "KRUSHA BLUEPRINT"},
            {"textbox_index": 81, "mode": "replace_whole", "target": "KRUSHA"},
        ],
        Kongs.diddy: [
            {"textbox_index": 37, "mode": "replace_whole", "target": "LIME BAZOOKA"},
            {"textbox_index": 12, "mode": "replace_whole", "target": "KREMLING KHARGE"},
            {"textbox_index": 14, "mode": "replace_whole", "target": "ROCKET REPTILE"},
            {"textbox_index": 16, "mode": "replace_whole", "target": "SALAMANDER SPRING"},
            {"textbox_index": 63, "mode": "replace_whole", "target": "KRUSHA BLUEPRINT"},
            {"textbox_index": 82, "mode": "replace_whole", "target": "KRUSHA"},
        ],
        Kongs.lanky: [
            {"textbox_index": 38, "mode": "replace_whole", "target": "LIME BAZOOKA"},
            {"textbox_index": 18, "mode": "replace_whole", "target": "KREMSTAND"},
            {"textbox_index": 20, "mode": "replace_whole", "target": "KABOOM BALLOON"},
            {"textbox_index": 22, "mode": "replace_whole", "target": "KREMSTAND SPRINT"},
            {"textbox_index": 64, "mode": "replace_whole", "target": "KRUSHA BLUEPRINT"},
            {"textbox_index": 83, "mode": "replace_whole", "target": "KRUSHA"},
        ],
        Kongs.tiny: [
            {"textbox_index": 39, "mode": "replace_whole", "target": "LIME BAZOOKA"},
            {"textbox_index": 24, "mode": "replace_whole", "target": "MINI DILE"},
            {"textbox_index": 26, "mode": "replace_whole", "target": "LIZARD TWIRL"},
            {"textbox_index": 28, "mode": "replace_whole", "target": "KROCOPORT"},
            {"textbox_index": 65, "mode": "replace_whole", "target": "KRUSHA BLUEPRINT"},
            {"textbox_index": 84, "mode": "replace_whole", "target": "KRUSHA"},
        ],
        Kongs.chunky: [
            {"textbox_index": 40, "mode": "replace_whole", "target": "LIME BAZOOKA"},
            {"textbox_index": 30, "mode": "replace_whole", "target": "HUNKY KRUSHY"},
            {"textbox_index": 32, "mode": "replace_whole", "target": "KREMLING PUNCH"},
            {"textbox_index": 34, "mode": "replace_whole", "target": "KHAMELEO GONE"},
            {"textbox_index": 66, "mode": "replace_whole", "target": "KRUSHA BLUEPRINT"},
            {"textbox_index": 85, "mode": "replace_whole", "target": "KRUSHA"},
        ],
    }
    name_replacements = {
        Kongs.donkey: [
            {"old": "Coconut Gun", "new": "LIME BAZOOKA"},
            {"old": "Baboon Blast", "new": "KANNON BLAST"},
            {"old": "Strong Kong", "new": "STRONG KROC"},
            {"old": "Gorilla Grab", "new": "GATOR GRAB"},
            {"old": "Donkey Kong", "new": "KRUSHA"},
        ],
        Kongs.diddy: [
            {"old": "Peanut Popguns", "new": "LIME BAZOOKA"},
            {"old": "Chimpy Charge", "new": "KREMLING KHARGE"},
            {"old": "Rocketbarrel Boost", "new": "ROCKET REPTILE"},
            {"old": "Simian Spring", "new": "SALAMANDER SPRING"},
            {"old": "Diddy Kong", "new": "KRUSHA"},
        ],
        Kongs.lanky: [
            {"old": "Grape Shooter", "new": "LIME BAZOOKA"},
            {"old": "Orangstand", "new": "KREMSTAND"},
            {"old": "Baboon Balloon", "new": "KABOOM BALLOON"},
            {"old": "Orangstand Sprint", "new": "KREMSTAND SPRINT"},
            {"old": "Lanky Kong", "new": "KRUSHA"},
        ],
        Kongs.tiny: [
            {"old": "Feather Bow", "new": "LIME BAZOOKA"},
            {"old": "Mini Monkey", "new": "MINI DILE"},
            {"old": "Pony Tail Twirl", "new": "LIZARD TWIRL"},
            {"old": "Monkeyport", "new": "KROCOPORT"},
            {"old": "Tiny Kong", "new": "KRUSHA"},
        ],
        Kongs.chunky: [
            {"old": "Pineapple Launcher", "new": "LIME BAZOOKA"},
            {"old": "Hunky Chunky", "new": "HUNKY KRUSHY"},
            {"old": "Primate Punch", "new": "KREMLING PUNCH"},
            {"old": "Gorilla Gone", "new": "KHAMELEO GONE"},
            {"old": "Chunky Kong", "new": "KRUSHA"},
        ],
    }
    settings_values = [
        spoiler.settings.kong_model_dk,
        spoiler.settings.kong_model_diddy,
        spoiler.settings.kong_model_lanky,
        spoiler.settings.kong_model_tiny,
        spoiler.settings.kong_model_chunky,
    ]
    text_replacements = []
    for index, value in enumerate(settings_values):
        if value == KongModels.krusha:
            text_replacements.extend(move_data[index])
            chosen_replacements = name_replacements[index]
            for reference in spoiler.location_references:
                for replacement in chosen_replacements:
                    if reference.item_name == replacement["old"]:
                        reference.item_name = replacement["new"]
                        chosen_replacements.remove(replacement)
    spoiler.text_changes[39] = text_replacements
