"""Place Shuffled Shops."""

from randomizer.Spoiler import Spoiler
import js
from randomizer.ShuffleShopLocations import available_shops
from randomizer.Enums.Regions import Regions
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM


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
                search_model = -1
                search_lz = -1
                search_vars = [shop, new_shop]
                for x_i, x in enumerate(search_vars):
                    if x == Regions.CrankyGeneric:
                        if x_i == 0:
                            search_model = 0x73
                            search_lz = Maps.Cranky
                        else:
                            new_model = 0x73
                            new_lz = Maps.Cranky
                    elif x == Regions.CandyGeneric:
                        if x_i == 0:
                            search_model = 0x124
                            search_lz = Maps.Candy
                        else:
                            new_model = 0x124
                            new_lz = Maps.Candy
                    elif x == Regions.FunkyGeneric:
                        if x_i == 0:
                            search_model = 0x7A
                            search_lz = Maps.Funky
                        else:
                            new_model = 0x7A
                            new_lz = Maps.Funky
                    elif x == Regions.Snide:
                        if x_i == 0:
                            search_model = 0x79
                            search_lz = Maps.Snide
                        else:
                            new_model = 0x79
                            new_lz = Maps.Snide
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
                        shop_data["replace_zone"] = new_lz
                        placement_data.append(shop_data)
                    else:
                        print(f"ERROR: Couldn't find LZ or Model attributed to shop ({model_index} | {zone_index})")
                else:
                    print("ERROR: Couldn't find shop in assortment")
            for placement in placement_data:
                ROM().seek(setup_address + 4 + (placement["model_index"] * 0x30) + 0x28)
                ROM().writeMultipleBytes(placement["replace_model"], 2)
                ROM().seek(lz_address + 2 + (placement["zone_index"] * 0x38) + 0x12)
                ROM().writeMultipleBytes(placement["replace_zone"], 2)
