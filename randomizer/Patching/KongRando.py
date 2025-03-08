"""Apply cosmetic elements of Kong Rando."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Enums.Enemies import Enemies
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.Generic import getModelFromItem

def apply_kongrando_cosmetic(spoiler, ROM_COPY: LocalROM):
    """Write kong cage changes for kong rando."""
    if Types.Kong in spoiler.settings.shuffled_location_types:
        kong_locations = [x for x in spoiler.item_assignment if x.location in (
            Locations.DiddyKong,
            Locations.LankyKong,
            Locations.TinyKong,
            Locations.ChunkyKong,
        )]
        for x in kong_locations:
            item = x.new_subitem
            item_type = x.new_item
            flag = x.new_flag
            model = 0
            if item is None:
                item = Items.NoItem
                item_type = Types.NoItem
                flag = 0
            else:
                model = getModelFromItem(item, item_type, flag, x.shared)
            print(x.name)
            print(item, item_type, flag)
            if model is not None:
                spoiler.WriteKongPlacement(x.location, item, item_type, model, flag)

    if spoiler.settings.kong_rando:
        gunswitches = [0x129, 0x126, 0x128, 0x127, 0x125]
        greenslamswitches = [0x94, 0x93, 0x95, 0x96, 0xB8]
        instrumentpads = [0xA8, 0xA9, 0xAC, 0xAA, 0xAB]
        forceSwitches = [0xE3, 0xE3, 0xE3, 0xE3, 0x70]

        japesPuzzleKong = spoiler.shuffled_kong_placement["Jungle Japes"]["puzzle"]["kong"]
        japesLockedData = spoiler.shuffled_kong_placement["Jungle Japes"]["locked"]

        tinyTemplePuzzleKong = spoiler.shuffled_kong_placement["Tiny Temple"]["puzzle"]["kong"]
        tinyTempleLockedData = spoiler.shuffled_kong_placement["Tiny Temple"]["locked"]

        llamaPuzzleKong = spoiler.shuffled_kong_placement["Llama Temple"]["puzzle"]["kong"]
        llamaLockedData = spoiler.shuffled_kong_placement["Llama Temple"]["locked"]

        factoryPuzzleKong = spoiler.shuffled_kong_placement["Frantic Factory"]["puzzle"]["kong"]
        factoryLockedData = spoiler.shuffled_kong_placement["Frantic Factory"]["locked"]

        llama_entrance_switch = []
        # if llamaPuzzleKong in [1, 4]:
        #     llama_entrance_switch.append({"index": 0xD, "new_type": gunswitches[llamaPuzzleKong]})
        kong_settings = [japesLockedData, llamaLockedData, tinyTempleLockedData, factoryLockedData]
        ROM_COPY.seek(0x1FF1020)
        for item_data in kong_settings:
            ROM_COPY.writeMultipleBytes(item_data["flag"], 2)
            ROM_COPY.writeMultipleBytes(item_data["model"], 2)

        kongrando_changes = [
            {
                "map_index": 7,
                "model2_changes": [
                    {"index": 0x30, "new_type": gunswitches[japesPuzzleKong]},
                    {"index": 0x31, "new_type": gunswitches[japesPuzzleKong]},
                    {"index": 0x32, "new_type": gunswitches[japesPuzzleKong]},
                ],
                "charspawner_changes": [{"type": Enemies.CutsceneDiddy, "new_type": Enemies.CharSpawnerItem}],
            },
            {"map_index": 0x26, "model2_changes": llama_entrance_switch, "charspawner_changes": []},
            {
                "map_index": 0x14,
                "model2_changes": [
                    {"index": 0x16, "new_type": instrumentpads[llamaPuzzleKong]},
                    {"index": 0x12, "new_type": gunswitches[llamaPuzzleKong]},
                ],
                "charspawner_changes": [{"type": Enemies.CutsceneLanky, "new_type": Enemies.CharSpawnerItem}],
            },
            {
                "map_index": 0x10,
                "model2_changes": [
                    {"index": 0x14, "new_type": forceSwitches[tinyTemplePuzzleKong]}
                ],
                "charspawner_changes": [{"type": Enemies.CutsceneTiny, "new_type": Enemies.CharSpawnerItem}],
            },
            {
                "map_index": 0x1A,
                "model2_changes": [{"index": 0x24, "new_type": greenslamswitches[factoryPuzzleKong]}],
                "charspawner_changes": [{"type": Enemies.CutsceneChunky, "new_type": Enemies.CharSpawnerItem}],
            },
        ]
        for kong_map in spoiler.shuffled_kong_placement.keys():
            for link_type in spoiler.shuffled_kong_placement[kong_map].keys():
                if link_type != "locked":
                    ROM_COPY.seek(spoiler.settings.rom_data + spoiler.shuffled_kong_placement[kong_map][link_type]["write"])
                    ROM_COPY.writeMultipleBytes(spoiler.shuffled_kong_placement[kong_map][link_type]["kong"], 1)

        for cont_map in kongrando_changes:
            cont_map_id = int(cont_map["map_index"])
            # Setup
            cont_map_setup_address = getPointerLocation(TableNames.Setups, cont_map_id)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM_COPY.seek(start + 0x2A)
                obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                has_id = False
                new_type = 0
                for model2 in cont_map["model2_changes"]:
                    if model2["index"] == obj_id:
                        has_id = True
                        new_type = model2["new_type"]
                if has_id:
                    ROM_COPY.seek(start + 0x28)
                    ROM_COPY.writeMultipleBytes(new_type, 2)
            # Character Spawners
            cont_map_spawner_address = getPointerLocation(TableNames.Spawners, cont_map_id)
            ROM_COPY.seek(cont_map_spawner_address)
            fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset = 2
            if fence_count > 0:
                for x in range(fence_count):
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point0_count * 10) + 6
            ROM_COPY.seek(cont_map_spawner_address + offset)
            spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += 2
            for x in range(spawner_count):
                ROM_COPY.seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
                init_offset = offset
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                has_id = False
                new_type = 0
                for char in cont_map["charspawner_changes"]:
                    if char["type"] == enemy_id:
                        has_id = True
                        new_type = char["new_type"]
                if has_id:
                    ROM_COPY.seek(cont_map_spawner_address + init_offset)
                    ROM_COPY.writeMultipleBytes(new_type, 1)
