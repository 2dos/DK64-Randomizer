"Melon crate Randomizer Code "
import js
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Lib import addNewScript, float_to_hex, getNextFreeID
from randomizer.Patching.Patcher import ROM, LocalROM


class MelonCrateShortData:
    """Class to store small parts of information relevant to the placement algorithm."""

    def __init__(self, map, coords, max_size, default, vanilla):
        """Initialize with provided data."""
        self.map = map
        self.coords = coords
        self.max_size = max_size
        self.default = default
        self.vanilla = vanilla

def randomize_melon_crate(spoiler):
      if spoiler.settings.melon_crate_rando:
        placements = []
        vanilla_melon_crate_maps = [
             Maps.JungleJapes,
             Maps.AngryAztec,
             Maps.AztecLlamaTemple,
             Maps.FranticFactory,
             Maps.GloomyGalleon,
             Maps.FungiForest,
             Maps.ForestThornvineBarn,
             Maps.CastleCrypt,
             
        ]
        new_vanilla_crates = []
        action_maps = vanilla_melon_crate_maps.copy()
        ROM_COPY = LocalROM()
        for level in spoiler.crate_locations:
            for crate in spoiler.crate_locations[level]:
                crate_data = CustomLocations[level][crate]
                idx = spoiler.crate_locations[level][crate]
                placements.append(MelonCrateShortData(crate_data.map, crate_data.coords, crate_data.max_size, idx, crate_data.vanilla_crate))
                if crate_data.vanilla_crate:
                    new_vanilla_crates.append(crate_data.map)
                if not crate_data.vanilla_crate:
                    if crate_data.map not in action_maps:
                        action_maps.append(crate_data.map)
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
                if cont_map_id in vanilla_melon_crate_maps and cont_map_id not in new_vanilla_crates and item_type == 0xB5:
                    accept = False  # crate is being removed
                if accept:
                    ROM_COPY.seek(item_start)
                    data = []
                    for int_index in range(int(0x30 / 4)):
                        data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    persisted_m2.append(data)
            crate_ids = []
            for crate in placements:
                if crate.map == cont_map_id and not crate.vanilla:
                    # Place new crate
                    crate_scale = crate.max_size / 160
                    selected_id = getNextFreeID(cont_map_id, crate_ids)
                    crate_ids.append(selected_id)
                    persisted_m2.append(
                        [
                            int(float_to_hex(crate.coords[0]), 16),
                            int(float_to_hex(crate.coords[1]), 16),
                            int(float_to_hex(crate.coords[2]), 16),
                            int(float_to_hex(crate_scale), 16),
                            0x6B0BEE32,
                            0x9B4D326F,
                            0,
                            0,
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
