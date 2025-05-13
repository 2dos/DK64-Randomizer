"""Apply Coin Rando changes."""

from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM
from randomizer.Enums.Maps import Maps

MINIGAME_MAPS = [
    Maps.StashSnatchEasy,
    Maps.StashSnatchNormal,
    Maps.StashSnatchHard,
    Maps.StashSnatchInsane,
    Maps.SplishSplashSalvageEasy,
    Maps.SplishSplashSalvageNormal,
    Maps.SplishSplashSalvageHard,
    Maps.SpeedySwingSortieEasy,
    Maps.SpeedySwingSortieNormal,
    Maps.SpeedySwingSortieHard,
    Maps.DiveBarrel,
    Maps.VineBarrel,
]


def randomize_coins(spoiler, ROM_COPY: LocalROM):
    """Place Coins into ROM."""
    if spoiler.settings.coin_rando or spoiler.settings.race_coin_rando:
        for cont_map_id in range(216):
            # Wipe setup and paths of Coin information
            if cont_map_id in MINIGAME_MAPS:
                continue
            # SETUP
            items_to_remove = []
            coin_items = [0x1D, 0x24, 0x23, 0x1C, 0x27]  # Has to remain in this order
            if spoiler.settings.coin_rando:
                items_to_remove.extend(coin_items)  # Banana Coins
            if spoiler.settings.race_coin_rando:
                items_to_remove.append(236)  # Race Coins
            setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            # Model Two Coins
            persisted_m2_data = []
            used_m2_ids = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_type not in items_to_remove:  # Not Coin
                    ROM_COPY.seek(item_start + 0x2A)
                    used_m2_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    ROM_COPY.seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    persisted_m2_data.append(item_data)
            ROM_COPY.seek(setup_table + 4 + (0x30 * model2_count))
            mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            # Mystery
            persisted_mys_data = []
            for item in range(mystery_count):
                ROM_COPY.seek(setup_table + 4 + (model2_count * 0x30) + 4 + (item * 0x24))
                item_data = []
                for x in range(int(0x24 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                persisted_mys_data.append(item_data)
            actor_block = setup_table + 4 + (0x30 * model2_count) + 4 + (0x24 * mystery_count)
            ROM_COPY.seek(actor_block)
            actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            # Actors
            persisted_act_data = []
            used_actor_ids = []
            for item in range(actor_count):
                actor_start = actor_block + 4 + (item * 0x38)
                ROM_COPY.seek(actor_start + 0x34)
                used_actor_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(actor_start)
                item_data = []
                for x in range(int(0x38 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                persisted_act_data.append(item_data)
            # Place all new coins
            new_id = 0
            placement_data = [
                {
                    "enabled": spoiler.settings.coin_rando,
                    "placements": spoiler.coin_placements,
                    "kong_arr_check": True,
                    "arr": coin_items,
                },
                {
                    "enabled": spoiler.settings.race_coin_rando,
                    "placements": spoiler.race_coin_placements,
                    "kong_arr_check": False,
                    "arr": [236],
                },
            ]
            for data in placement_data:
                if data["enabled"]:
                    for new_coin in data["placements"]:
                        if new_coin["map"] == cont_map_id:
                            # Model Two Coins
                            for loc in new_coin["locations"]:
                                item_data = []
                                item_data.extend(
                                    [
                                        int(float_to_hex(loc[1]), 16),
                                        int(float_to_hex(loc[2]), 16),
                                        int(float_to_hex(loc[3]), 16),
                                        int(float_to_hex(loc[0]), 16),
                                    ]
                                )
                                item_data.append(2)
                                item_data.append(0x01C7FFFF)
                                for x in range(int((0x24 - 0x18) / 4)):
                                    item_data.append(0)
                                item_data.append(0x40400000)
                                if data["kong_arr_check"]:
                                    coin_item_type = data["arr"][new_coin["kong"]]
                                else:
                                    coin_item_type = data["arr"][0]
                                found_vacant = False
                                found_id = 0
                                while not found_vacant:
                                    if new_id not in used_m2_ids:
                                        used_m2_ids.append(new_id)
                                        found_id = new_id
                                        found_vacant = True
                                    new_id += 1
                                item_data.append((coin_item_type << 16) + found_id)
                                item_data.append((2 << 16) + 1)
                                persisted_m2_data.append(item_data)
            # Recompile Tables
            # SETUP
            ROM_COPY.seek(setup_table)
            ROM_COPY.writeMultipleBytes(len(persisted_m2_data), 4)
            for x in persisted_m2_data:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 4)
            ROM_COPY.writeMultipleBytes(len(persisted_mys_data), 4)
            for x in persisted_mys_data:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 4)
            ROM_COPY.writeMultipleBytes(len(persisted_act_data), 4)
            for x in persisted_act_data:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 4)
