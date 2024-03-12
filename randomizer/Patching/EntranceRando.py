"""Randomize Entrances passed from Misc options."""

import js
from randomizer.Enums.Settings import ShuffleLoadingZones
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Maps import Maps
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId, MapExitTable
from randomizer.Patching.Patcher import LocalROM

valid_lz_types = [9, 12, 13, 16]


def intToArr(val, size):
    """Convert INT to an array.

    Args:
        val (int): Value to convert
        size (int): Size to write as

    Returns:
        array: int array
    """
    tmp = val
    arr = []
    for x in range(size):
        arr.append(0)
    slot = size - 1
    while slot > -1:
        tmpv = tmp % 256
        arr[slot] = tmpv
        slot -= 1
        tmp = int((tmp - tmpv) / 256)
        if slot == -1:
            break
        elif tmp == 0:
            break
    return arr


def randomize_entrances(spoiler):
    """Randomize Entrances based on shuffled_exit_instructions."""
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all and spoiler.shuffled_exit_instructions is not None:
        ROM_COPY = LocalROM()
        for cont_map in spoiler.shuffled_exit_instructions:
            # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
            cont_map_id = int(cont_map["container_map"])
            cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
            ROM_COPY.seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                # print(lz_type)
                if lz_type in valid_lz_types:
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                    lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                    lz_exit = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    for zone in cont_map["zones"]:
                        if lz_map == zone["vanilla_map"]:
                            if lz_exit == zone["vanilla_exit"] or (lz_map == Maps.FactoryCrusher):
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                                map_bytes = intToArr(zone["new_map"], 2)
                                ROM_COPY.writeBytes(bytearray(map_bytes))
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                                exit_bytes = intToArr(zone["new_exit"], 2)
                                ROM_COPY.writeBytes(bytearray(exit_bytes))
        varspaceOffset = spoiler.settings.rom_data
        # Force call parent filter
        ROM_COPY.seek(varspaceOffset + 0x47)
        ROM_COPY.write(1)
        # /* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
        moreLoadingZonesOffset = 0x05D
        ROM_COPY.seek(varspaceOffset + moreLoadingZonesOffset)
        ROM_COPY.write(1)
        # /* 0x05E */ unsigned short aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecMainToRace]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x060 */ unsigned short aztec_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecRaceToMain]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x062 */ unsigned short caves_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CavesRaceToMain]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x064 */ unsigned short seal_race_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonSealToShipyard]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x066 */ unsigned short factory_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.FactoryRaceToRandD]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x068 */ unsigned short castle_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleRaceToMuseum]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x06A */ unsigned short seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonLighthouseAreaToSickBay]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x06C */ unsigned short fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.ForestMainToCarts in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestMainToCarts]
            ROM_COPY.write(GetMapId(shuffledBack.regionId))
            ROM_COPY.write(GetExitId(shuffledBack))
        else:
            ROM_COPY.write(Maps.ForestMinecarts)
            ROM_COPY.write(0)
        # /* 0x06E */ unsigned short fungi_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.ForestCartsToMain in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestCartsToMain]
            ROM_COPY.write(GetMapId(shuffledBack.regionId))
            ROM_COPY.write(GetExitId(shuffledBack))
        else:
            ROM_COPY.write(Maps.FungiForest)
            ROM_COPY.write(MapExitTable[Maps.FungiForest].index("From Minecart"))
        # /* 0x070 */ unsigned short japes_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.JapesCartsToMain in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.JapesCartsToMain]
            ROM_COPY.write(GetMapId(shuffledBack.regionId))
            ROM_COPY.write(GetExitId(shuffledBack))
        else:
            ROM_COPY.write(Maps.JungleJapes)
            ROM_COPY.write(MapExitTable[Maps.JungleJapes].index("From Minecart"))
        # /* 0x072 */ unsigned short castle_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleCartsToCrypt]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x074 */ unsigned short castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesMainToCastleLobby]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x076 */ unsigned short k_rool_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        # K rool exit is always vanilla
        ROM_COPY.write(Maps.Isles)
        ROM_COPY.write(12)
        # /* 0x078 */ unsigned short exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.JapesToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.FactoryToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CavesToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleToIsles]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # Helm exit is always vanilla
        ROM_COPY.write(Maps.HideoutHelmLobby)
        ROM_COPY.write(1)
        # /* 0x088 */ unsigned short enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToJapes]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToAztec]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToFactory]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToGalleon]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToForest]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToCaves]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToCastle]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x120 */ unsigned short ballroom_to_museum; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleBallroomToMuseum]
        ROM_COPY.seek(varspaceOffset + 0x130)
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))
        # /* 0x122 */ unsigned short museum_to_ballroom; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleMuseumToBallroom]
        ROM_COPY.write(GetMapId(shuffledBack.regionId))
        ROM_COPY.write(GetExitId(shuffledBack))


def filterEntranceType():
    """Change LZ Type for some entrances so that warps from crown pads work correctly."""
    ROM_COPY = LocalROM()
    for cont_map_id in range(216):
        cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
        ROM_COPY.seek(cont_map_lzs_address)
        lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
            lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if lz_type == 0x10 and lz_map not in (Maps.Cranky, Maps.Candy, Maps.Funky, Maps.Snide):
                # Change type to 0xC
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                ROM_COPY.writeMultipleBytes(0xC, 2)
                # Change fade type to spin
                ROM_COPY.seek(cont_map_lzs_address + start + 0x16)
                ROM_COPY.writeMultipleBytes(0, 2)


class ItemPreviewCutscene:
    """Class to store information regarding an item preview cutscene."""

    def __init__(self, map: Maps, old_cutscene: int, new_cutscene: int):
        """Initialize with given parameters."""
        self.map = map
        self.old_cutscene = old_cutscene
        self.new_cutscene = new_cutscene


ITEM_PREVIEW_CUTSCENES = [
    ItemPreviewCutscene(Maps.ForestSpider, 3, 9),
    # ItemPreviewCutscene(Maps.CavesChunkyIgloo, 0, 5),
]


def enableTriggerText(spoiler):
    """Change the cutscene trigger in Spider Boss and Chunky Igloo to the specific item reward cutscene."""
    if spoiler.settings.item_reward_previews:
        ROM_COPY = LocalROM()
        for cs in ITEM_PREVIEW_CUTSCENES:
            cont_map_lzs_address = js.pointer_addresses[18]["entries"][cs.map]["pointing_to"]
            ROM_COPY.seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                lz_cutscene = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if lz_type == 10 and lz_cutscene == cs.old_cutscene:
                    # Change cutscene
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                    ROM_COPY.writeMultipleBytes(cs.new_cutscene, 2)
