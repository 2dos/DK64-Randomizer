"""Place Shuffled Shops."""

import math

import js
from randomizer.Enums.Regions import Regions
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Lib import float_to_hex, intf_to_float
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.ShuffleShopLocations import available_shops


def ApplyShopRandomizer(spoiler):
    """Write shop locations to ROM."""
    if spoiler.settings.shuffle_shops:
        shop_assortment = spoiler.shuffled_shop_locations
        shop_placement_maps = []
        for level in available_shops:
            shop_array = available_shops[level]
            for shop in shop_array:
                if shop.map not in shop_placement_maps:
                    shop_placement_maps.append(shop.map)
        for map in shop_placement_maps:
            setup_address = js.pointer_addresses[9]["entries"][map]["pointing_to"]
            lz_address = js.pointer_addresses[18]["entries"][map]["pointing_to"]
            shops_in_map = []
            map_level = 0
            for level in available_shops:
                shop_array = available_shops[level]
                for shop in shop_array:
                    if shop.map == map and not shop.locked:
                        shops_in_map.append(shop.shop)
                        map_level = level
            placement_data = []
            for shop in shops_in_map:
                if map_level not in shop_assortment.keys():
                    continue
                shop_data = {}
                new_shop = shop_assortment[map_level][shop]
                new_model = -1
                new_lz = -1
                new_rot = -1
                new_scale = -1
                search_model = -1
                search_lz = -1
                search_rot = -1
                search_scale = -1
                search_vars = [shop, new_shop]
                for x_i, x in enumerate(search_vars):
                    if x == Regions.CrankyGeneric:
                        if x_i == 0:
                            search_model = 0x73
                            search_lz = Maps.Cranky
                            search_rot = 180
                            search_scale = 0.95
                        else:
                            new_model = 0x73
                            new_lz = Maps.Cranky
                            new_rot = 180
                            new_scale = 0.95
                    elif x == Regions.CandyGeneric:
                        if x_i == 0:
                            search_model = 0x124
                            search_lz = Maps.Candy
                            search_rot = 0
                            search_scale = 0.95
                        else:
                            new_model = 0x124
                            new_lz = Maps.Candy
                            new_rot = 0
                            new_scale = 0.95
                    elif x == Regions.FunkyGeneric:
                        if x_i == 0:
                            search_model = 0x7A
                            search_lz = Maps.Funky
                            search_rot = 90
                            search_scale = 1.045
                        else:
                            new_model = 0x7A
                            new_lz = Maps.Funky
                            new_rot = 90
                            new_scale = 1.045
                    elif x == Regions.Snide:
                        if x_i == 0:
                            search_model = 0x79
                            search_lz = Maps.Snide
                            search_rot = 270
                            search_scale = 3
                        else:
                            new_model = 0x79
                            new_lz = Maps.Snide
                            new_rot = 270
                            new_scale = 3
                if new_model > -1 and new_lz > -1 and search_model > -1 and search_lz > -1:
                    model_index = -1
                    zone_index = -1
                    LocalROM().seek(setup_address)
                    model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
                    for model2_index in range(model2_count):
                        if model_index == -1:
                            obj_start = setup_address + 4 + (model2_index * 0x30)
                            LocalROM().seek(obj_start + 0x28)
                            obj_type = int.from_bytes(LocalROM().readBytes(2), "big")
                            if obj_type == search_model:
                                model_index = model2_index
                    LocalROM().seek(lz_address)
                    lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
                    for lz_index in range(lz_count):
                        if zone_index == -1:
                            lz_start = lz_address + 2 + (lz_index * 0x38)
                            LocalROM().seek(lz_start + 0x10)
                            lz_type = int.from_bytes(LocalROM().readBytes(2), "big")
                            if lz_type == 16:
                                LocalROM().seek(lz_start + 0x12)
                                lz_map = int.from_bytes(LocalROM().readBytes(2), "big")
                                if lz_map == search_lz:
                                    zone_index = lz_index
                    if model_index > -1 and zone_index > -1:
                        shop_data["model_index"] = model_index
                        shop_data["zone_index"] = zone_index
                        shop_data["replace_model"] = new_model
                        shop_data["original_model"] = search_model
                        shop_data["replace_zone"] = new_lz
                        shop_data["angle_change"] = search_rot - new_rot
                        shop_data["scale_factor"] = search_scale / new_scale
                        placement_data.append(shop_data)
                    else:
                        print(f"ERROR: Couldn't find LZ or Model attributed to shop ({model_index} | {zone_index})")
                else:
                    print("ERROR: Couldn't find shop in assortment")
            for placement in placement_data:
                setup_item = setup_address + 4 + (placement["model_index"] * 0x30)
                zone_item = lz_address + 2 + (placement["zone_index"] * 0x38)
                # Type
                LocalROM().seek(setup_item + 0x28)
                LocalROM().writeMultipleBytes(placement["replace_model"], 2)
                # Angle
                if placement["angle_change"] != 0:
                    LocalROM().seek(setup_item + 0x1C)
                    original_angle = intf_to_float(int.from_bytes(LocalROM().readBytes(4), "big"))
                    new_angle = original_angle + placement["angle_change"]
                    if new_angle < 0:
                        new_angle += 360
                    elif new_angle >= 360:
                        new_angle -= 360
                    LocalROM().seek(setup_item + 0x1C)
                    LocalROM().writeMultipleBytes(int(float_to_hex(new_angle), 16), 4)
                # Scale
                LocalROM().seek(setup_item + 0xC)
                original_scale = intf_to_float(int.from_bytes(LocalROM().readBytes(4), "big"))
                new_scale = original_scale * placement["scale_factor"]
                LocalROM().seek(setup_item + 0xC)
                LocalROM().writeMultipleBytes(int(float_to_hex(new_scale), 16), 4)
                # Get Model X and Z
                LocalROM().seek(setup_item)
                model_x = intf_to_float(int.from_bytes(LocalROM().readBytes(4), "big"))
                LocalROM().seek(setup_item + 0x8)
                model_z = intf_to_float(int.from_bytes(LocalROM().readBytes(4), "big"))
                # Get Base Zone X and Z
                if model_x < 0:
                    model_x = int(model_x) + 65536
                else:
                    model_x = int(model_x)
                if model_z < 0:
                    model_z = int(model_z) + 65536
                else:
                    model_z = int(model_z)
                LocalROM().seek(zone_item)
                LocalROM().writeMultipleBytes(model_x, 2)
                LocalROM().seek(zone_item + 0x4)
                LocalROM().writeMultipleBytes(model_z, 2)
                # Overwrite new radius
                base_model_scale = 88
                if placement["replace_model"] == 0x73:
                    # Cranky
                    base_model_scale = 50
                elif placement["replace_model"] == 0x7A:
                    # Funky
                    base_model_scale = 55
                elif placement["replace_model"] == 0x124:
                    # Candy
                    base_model_scale = 40.1
                elif placement["replace_model"] == 0x79:
                    # Snide
                    base_model_scale = 87.5
                LocalROM().seek(zone_item + 0x6)
                LocalROM().writeMultipleBytes(int(base_model_scale * new_scale), 2)
                # Loading Zone
                LocalROM().seek(zone_item + 0x12)
                LocalROM().writeMultipleBytes(placement["replace_zone"], 2)
