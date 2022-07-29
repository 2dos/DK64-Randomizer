"""Place Shuffled Shops."""

from randomizer.Spoiler import Spoiler
import js
import struct
import math
from randomizer.ShuffleShopLocations import available_shops
from randomizer.Enums.Regions import Regions
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex(hex(intf)[2:]))[0]


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def ushort_to_short(ushort):
    """Convert unsigned short to signed short."""
    if ushort > 32767:
        return ushort - 65536
    return ushort


def ApplyShopRandomizer(spoiler: Spoiler):
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
                            search_scale = 1
                        else:
                            new_model = 0x73
                            new_lz = Maps.Cranky
                            new_rot = 180
                            new_scale = 1
                    elif x == Regions.CandyGeneric:
                        if x_i == 0:
                            search_model = 0x124
                            search_lz = Maps.Candy
                            search_rot = 0
                            search_scale = 1
                        else:
                            new_model = 0x124
                            new_lz = Maps.Candy
                            new_rot = 0
                            new_scale = 1
                    elif x == Regions.FunkyGeneric:
                        if x_i == 0:
                            search_model = 0x7A
                            search_lz = Maps.Funky
                            search_rot = 90
                            search_scale = 1
                        else:
                            new_model = 0x7A
                            new_lz = Maps.Funky
                            new_rot = 90
                            new_scale = 1
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
                    ROM().seek(setup_address)
                    model2_count = int.from_bytes(ROM().readBytes(4), "big")
                    for model2_index in range(model2_count):
                        if model_index == -1:
                            obj_start = setup_address + 4 + (model2_index * 0x30)
                            ROM().seek(obj_start + 0x28)
                            obj_type = int.from_bytes(ROM().readBytes(2), "big")
                            if obj_type == search_model:
                                model_index = model2_index
                    ROM().seek(lz_address)
                    lz_count = int.from_bytes(ROM().readBytes(2), "big")
                    for lz_index in range(lz_count):
                        if zone_index == -1:
                            lz_start = lz_address + 2 + (lz_index * 0x38)
                            ROM().seek(lz_start + 0x10)
                            lz_type = int.from_bytes(ROM().readBytes(2), "big")
                            if lz_type == 16:
                                ROM().seek(lz_start + 0x12)
                                lz_map = int.from_bytes(ROM().readBytes(2), "big")
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
                ROM().seek(setup_item + 0x28)
                ROM().writeMultipleBytes(placement["replace_model"], 2)
                # Angle
                if placement["angle_change"] != 0:
                    ROM().seek(setup_item + 0x1C)
                    original_angle = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                    new_angle = original_angle + placement["angle_change"]
                    if new_angle < 0:
                        new_angle += 360
                    elif new_angle >= 360:
                        new_angle -= 360
                    ROM().seek(setup_item + 0x1C)
                    ROM().writeMultipleBytes(int(float_to_hex(new_angle), 16), 4)
                # Scale
                ROM().seek(setup_item + 0xC)
                original_scale = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                new_scale = original_scale * placement["scale_factor"]
                ROM().seek(setup_item + 0xC)
                ROM().writeMultipleBytes(int(float_to_hex(new_scale), 16), 4)
                # Get Model X and Z
                ROM().seek(setup_item)
                model_x = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                ROM().seek(setup_item + 0x8)
                model_z = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                # Get Base Zone X and Z
                ROM().seek(zone_item)
                zone_x = ushort_to_short(int.from_bytes(ROM().readBytes(2), "big"))
                ROM().seek(zone_item + 0x4)
                zone_z = ushort_to_short(int.from_bytes(ROM().readBytes(2), "big"))
                # Get Base Distance
                dx = zone_x - model_x
                dz = zone_z - model_z
                base_dist = math.sqrt((dx * dx) + (dz * dz))
                # Get New Model -> LZ distance
                base_model_scale = 1
                if placement["replace_model"] == 0x73:
                    # Cranky
                    base_model_scale = 35
                elif placement["replace_model"] == 0x7A:
                    # Funky
                    base_model_scale = 43
                elif placement["replace_model"] == 0x124:
                    # Candy
                    base_model_scale = 35
                elif placement["replace_model"] == 0x79:
                    # Snide
                    base_model_scale = 50
                dist_aim = base_model_scale * new_scale
                dist_ratio = dist_aim / base_dist
                new_dx = dx * dist_ratio
                new_dz = dz * dist_ratio
                new_x = model_x + new_dx
                new_z = model_z + new_dz
                if new_x < 0:
                    new_x += 65536
                if new_z < 0:
                    new_z += 65536
                ROM().seek(zone_item + 0x0)
                ROM().writeMultipleBytes(new_x, 2)
                ROM().seek(zone_item + 0x4)
                ROM().writeMultipleBytes(new_z, 2)
                # Loading Zone
                ROM().seek(zone_item + 0x12)
                ROM().writeMultipleBytes(placement["replace_zone"], 2)
