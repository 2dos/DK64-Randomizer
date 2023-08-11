"""Melon crate Randomizer Code."""
import js
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Lib import addNewScript, float_to_hex, getNextFreeID
from randomizer.Patching.Patcher import ROM, LocalROM


class MelonCrateShortData:
    """Class to store small parts of information relevant to the placement algorithm."""

    def __init__(self, map, coords, max_size, rot_y, is_galleon_floating_crate):
        """Initialize with provided data."""
        self.map = map
        self.coords = coords
        self.max_size = max_size
        self.rot_y = rot_y
        self.is_galleon_floating_crate = is_galleon_floating_crate


def randomize_melon_crate(spoiler):
    """Place Melon Crates."""
    if spoiler.settings.random_crates:
        placements = []

        action_maps = [
            # Start with vanilla crate maps
            Maps.JungleJapes,  # Two crates in Japes Main
            Maps.AztecLlamaTemple,  # One in Llama Temple
            Maps.AngryAztec,  # Two in Aztec Main
            Maps.FranticFactory,  # Two in Factory Main
            Maps.GloomyGalleon,  # One in Galleon
            Maps.FungiForest,  # Three in Fungi Main
            Maps.ForestThornvineBarn,  # One inside Thornvine Barn
            Maps.CastleLowerCave,  # One in Crypt Hub
        ]
        keep_galleon_crate = False
        ROM_COPY = LocalROM()
        for crate_item in spoiler.meloncrate_placement:
            for crate in CustomLocations[crate_item["level"]]:
                if crate.name == crate_item["name"]:
                    placements.append(MelonCrateShortData(crate.map, crate.coords, crate.max_size, crate.rot_y, crate.is_galleon_floating_crate))
                    if crate.map not in action_maps:
                        action_maps.append(crate.map)
                    if crate.is_galleon_floating_crate:
                        keep_galleon_crate = True

        for cont_map_id in action_maps:
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            persisted_m2 = []
            for model2_item in range(model2_count):
                accept = True
                item_start = setup_table + 4 + (model2_item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if (not (cont_map_id == Maps.GloomyGalleon and keep_galleon_crate)) and item_type == 0xB5:
                    accept = False  # crate is being removed
                if accept:
                    ROM_COPY.seek(item_start)
                    data = []
                    for int_index in range(int(0x30 / 4)):
                        data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    persisted_m2.append(data)
            crate_ids = []
            for crate in placements:
                if crate.map == cont_map_id and not crate.is_galleon_floating_crate:
                    # Place new crate
                    crate_scale = min(crate.max_size / 33, 1)
                    rotation = (crate.rot_y * 360) / 4096
                    selected_id = getNextFreeID(cont_map_id, crate_ids)
                    crate_ids.append(selected_id)
                    persisted_m2.append(
                        [
                            int(float_to_hex(crate.coords[0]), 16),
                            int(float_to_hex(crate.coords[1]), 16),
                            int(float_to_hex(crate.coords[2]), 16),
                            int(float_to_hex(crate_scale), 16),
                            0x027B0002,
                            0x05800640,
                            0,
                            int(float_to_hex(rotation), 16),
                            0,
                            0,
                            (0xB5 << 16) | selected_id,
                            1 << 16,
                        ]
                    )
                    addNewScript(cont_map_id, [selected_id], ScriptTypes.MelonCrate)
            ROM_COPY.seek(setup_table + 4 + (model2_count * 0x30))
            mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            extra_data = [mystery_count]
            for mys_item in range(mystery_count):
                for int_index in range(int(0x24 / 4)):
                    extra_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            extra_data.append(actor_count)
            for act_item in range(actor_count):
                for int_index in range(int(0x38 / 4)):
                    extra_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            ROM_COPY.seek(setup_table)
            ROM_COPY.writeMultipleBytes(len(persisted_m2), 4)
            for model2 in persisted_m2:
                for int_val in model2:
                    ROM_COPY.writeMultipleBytes(int_val, 4)
            for int_val in extra_data:
                ROM_COPY.writeMultipleBytes(int_val, 4)
