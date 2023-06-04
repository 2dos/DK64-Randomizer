"""Crown Randomizer Placement Code."""
import js
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.CrownLocations import CrownLocations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Lib import addNewScript, float_to_hex, getNextFreeID
from randomizer.Patching.Patcher import ROM, LocalROM


class CrownPlacementShortData:
    """Class to store small parts of information relevant to the placement algorithm."""

    def __init__(self, map, coords, scale, default, vanilla):
        """Initialize with provided data."""
        self.map = map
        self.coords = coords
        self.scale = scale
        self.default = default
        self.vanilla = vanilla


def randomize_crown_pads(spoiler):
    """Place Crown Pads."""
    if spoiler.settings.crown_placement_rando:
        placements = []
        vanilla_crown_maps = [
            Maps.JungleJapes,
            Maps.AztecTinyTemple,
            Maps.FranticFactory,
            Maps.GloomyGalleon,
            Maps.FungiForest,
            Maps.CavesRotatingCabin,  # Isn't an actual pad, part of rotating room obj
            Maps.CastleGreenhouse,
            Maps.IslesSnideRoom,
            Maps.FungiForestLobby,
            Maps.HideoutHelm,
        ]
        new_vanilla_crowns = []
        action_maps = vanilla_crown_maps.copy()
        for level in spoiler.crown_locations:
            for crown in spoiler.crown_locations[level]:
                crown_data = CrownLocations[level][crown]
                idx = spoiler.crown_locations[level][crown]
                placements.append(CrownPlacementShortData(crown_data.map, crown_data.coords, crown_data.scale, idx, crown_data.is_vanilla))
                if crown_data.is_vanilla:
                    new_vanilla_crowns.append(crown_data.map)
                if not crown_data.is_vanilla:
                    if crown_data.map not in action_maps:
                        action_maps.append(crown_data.map)
        for cont_map_id in action_maps:
            if cont_map_id == Maps.CavesRotatingCabin:
                if cont_map_id not in new_vanilla_crowns:
                    # Remove Caves Crown
                    sav = spoiler.settings.rom_data
                    LocalROM().seek(sav + 0x195)
                    LocalROM().write(1)
            else:
                setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
                LocalROM().seek(setup_table)
                model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
                persisted_m2 = []
                for model2_item in range(model2_count):
                    accept = True
                    item_start = setup_table + 4 + (model2_item * 0x30)
                    LocalROM().seek(item_start + 0x28)
                    item_type = int.from_bytes(LocalROM().readBytes(2), "big")
                    if cont_map_id in vanilla_crown_maps and cont_map_id not in new_vanilla_crowns and item_type == 0x1C6:
                        accept = False  # Crown is being removed
                    if accept:
                        LocalROM().seek(item_start)
                        data = []
                        for int_index in range(int(0x30 / 4)):
                            data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                        persisted_m2.append(data)
                crown_ids = []
                for crown in placements:
                    if crown.map == cont_map_id and not crown.vanilla:
                        # Place new crown
                        selected_id = getNextFreeID(cont_map_id, crown_ids)
                        crown_ids.append(selected_id)
                        persisted_m2.append(
                            [
                                int(float_to_hex(crown.coords[0]), 16),
                                int(float_to_hex(crown.coords[1]), 16),
                                int(float_to_hex(crown.coords[2]), 16),
                                int(float_to_hex(crown.scale), 16),
                                0x6B0BEE32,
                                0x9B4D326F,
                                0,
                                0,
                                0,
                                0,
                                (0x1C6 << 16) | selected_id,
                                1 << 16,
                            ]
                        )
                        if crown.default == 0:
                            addNewScript(cont_map_id, [selected_id], ScriptTypes.CrownMain)
                        elif crown.default == 1:
                            addNewScript(cont_map_id, [selected_id], ScriptTypes.CrownIsles2)
                LocalROM().seek(setup_table + 4 + (model2_count * 0x30))
                mystery_count = int.from_bytes(LocalROM().readBytes(4), "big")
                extra_data = [mystery_count]
                for mys_item in range(mystery_count):
                    for int_index in range(int(0x24 / 4)):
                        extra_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                actor_count = int.from_bytes(LocalROM().readBytes(4), "big")
                extra_data.append(actor_count)
                for act_item in range(actor_count):
                    for int_index in range(int(0x38 / 4)):
                        extra_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                LocalROM().seek(setup_table)
                LocalROM().writeMultipleBytes(len(persisted_m2), 4)
                for model2 in persisted_m2:
                    for int_val in model2:
                        LocalROM().writeMultipleBytes(int_val, 4)
                for int_val in extra_data:
                    LocalROM().writeMultipleBytes(int_val, 4)
