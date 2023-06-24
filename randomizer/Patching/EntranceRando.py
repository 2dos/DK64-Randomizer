"""Randomize Entrances passed from Misc options."""
import js
from randomizer.Enums.Settings import ShuffleLoadingZones
from randomizer.Enums.Transitions import Transitions
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId, MapExitTable, Maps
from randomizer.Patching.Patcher import ROM, LocalROM

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
        for cont_map in spoiler.shuffled_exit_instructions:
            # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
            cont_map_id = int(cont_map["container_map"])
            cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
            LocalROM().seek(cont_map_lzs_address)
            lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                LocalROM().seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(LocalROM().readBytes(2), "big")
                # print(lz_type)
                if lz_type in valid_lz_types:
                    LocalROM().seek(cont_map_lzs_address + start + 0x12)
                    lz_map = int.from_bytes(LocalROM().readBytes(2), "big")
                    LocalROM().seek(cont_map_lzs_address + start + 0x14)
                    lz_exit = int.from_bytes(LocalROM().readBytes(2), "big")
                    for zone in cont_map["zones"]:
                        if lz_map == zone["vanilla_map"]:
                            if lz_exit == zone["vanilla_exit"] or (lz_map == Maps.FactoryCrusher):
                                LocalROM().seek(cont_map_lzs_address + start + 0x12)
                                map_bytes = intToArr(zone["new_map"], 2)
                                LocalROM().writeBytes(bytearray(map_bytes))
                                LocalROM().seek(cont_map_lzs_address + start + 0x14)
                                exit_bytes = intToArr(zone["new_exit"], 2)
                                LocalROM().writeBytes(bytearray(exit_bytes))
        varspaceOffset = spoiler.settings.rom_data
        # Force call parent filter
        LocalROM().seek(varspaceOffset + 0x47)
        LocalROM().write(1)
        # /* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
        moreLoadingZonesOffset = 0x05D
        LocalROM().seek(varspaceOffset + moreLoadingZonesOffset)
        LocalROM().write(1)
        # /* 0x05E */ unsigned short aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecMainToRace]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x060 */ unsigned short aztec_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecRaceToMain]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x062 */ unsigned short caves_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CavesRaceToMain]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x064 */ unsigned short seal_race_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonSealToShipyard]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x066 */ unsigned short factory_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.FactoryRaceToRandD]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x068 */ unsigned short castle_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleRaceToMuseum]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x06A */ unsigned short seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonLighthouseAreaToSickBay]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x06C */ unsigned short fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.ForestMainToCarts in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestMainToCarts]
            LocalROM().write(GetMapId(shuffledBack.regionId))
            LocalROM().write(GetExitId(shuffledBack))
        else:
            LocalROM().write(Maps.ForestMinecarts)
            LocalROM().write(0)
        # /* 0x06E */ unsigned short fungi_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.ForestCartsToMain in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestCartsToMain]
            LocalROM().write(GetMapId(shuffledBack.regionId))
            LocalROM().write(GetExitId(shuffledBack))
        else:
            LocalROM().write(Maps.FungiForest)
            LocalROM().write(MapExitTable[Maps.FungiForest].index("From Minecart"))
        # /* 0x070 */ unsigned short japes_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        if Transitions.JapesCartsToMain in spoiler.shuffled_exit_data:
            shuffledBack = spoiler.shuffled_exit_data[Transitions.JapesCartsToMain]
            LocalROM().write(GetMapId(shuffledBack.regionId))
            LocalROM().write(GetExitId(shuffledBack))
        else:
            LocalROM().write(Maps.JungleJapes)
            LocalROM().write(MapExitTable[Maps.JungleJapes].index("From Minecart"))
        # /* 0x072 */ unsigned short castle_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleCartsToCrypt]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x074 */ unsigned short castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesMainToCastleLobby]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x076 */ unsigned short k_rool_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        # K rool exit is always vanilla
        LocalROM().write(Maps.Isles)
        LocalROM().write(12)
        # /* 0x078 */ unsigned short exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.JapesToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.AztecToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.FactoryToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.GalleonToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.ForestToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CavesToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleToIsles]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # Helm exit is always vanilla
        LocalROM().write(Maps.HideoutHelmLobby)
        LocalROM().write(1)
        # /* 0x088 */ unsigned short enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToJapes]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToAztec]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToFactory]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToGalleon]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToForest]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToCaves]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToCastle]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x120 */ unsigned short ballroom_to_museum; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleBallroomToMuseum]
        LocalROM().seek(varspaceOffset + 0x130)
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))
        # /* 0x122 */ unsigned short museum_to_ballroom; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        shuffledBack = spoiler.shuffled_exit_data[Transitions.CastleMuseumToBallroom]
        LocalROM().write(GetMapId(shuffledBack.regionId))
        LocalROM().write(GetExitId(shuffledBack))


def filterEntranceType():
    """Change LZ Type for some entrances so that warps from crown pads work correctly."""
    for cont_map_id in range(216):
        cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
        LocalROM().seek(cont_map_lzs_address)
        lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            LocalROM().seek(cont_map_lzs_address + start + 0x10)
            lz_type = int.from_bytes(LocalROM().readBytes(2), "big")
            lz_map = int.from_bytes(LocalROM().readBytes(2), "big")
            if lz_type == 0x10 and lz_map not in (Maps.Cranky, Maps.Candy, Maps.Funky, Maps.Snide):
                # Change type to 0xC
                LocalROM().seek(cont_map_lzs_address + start + 0x10)
                LocalROM().writeMultipleBytes(0xC, 2)
                # Change fade type to spin
                LocalROM().seek(cont_map_lzs_address + start + 0x16)
                LocalROM().writeMultipleBytes(0, 2)


def enableSpiderText(spoiler):
    """Change the cutscene trigger in Spider Boss to the specific item reward cutscene."""
    if spoiler.settings.item_reward_previews:
        cont_map_lzs_address = js.pointer_addresses[18]["entries"][Maps.ForestSpider]["pointing_to"]
        LocalROM().seek(cont_map_lzs_address)
        lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            LocalROM().seek(cont_map_lzs_address + start + 0x10)
            lz_type = int.from_bytes(LocalROM().readBytes(2), "big")
            lz_cutscene = int.from_bytes(LocalROM().readBytes(2), "big")
            if lz_type == 10 and lz_cutscene == 3:
                # Change cutscene to 9
                LocalROM().seek(cont_map_lzs_address + start + 0x12)
                LocalROM().writeMultipleBytes(9, 2)
