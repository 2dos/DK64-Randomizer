"""Randomize Entrances passed from Misc options."""
import js

from randomizer.MapsAndExits import Maps
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler

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


def randomize_entrances(spoiler: Spoiler):
    """Randomize Entrances based on shuffled_exit_instructions."""
    if spoiler.settings.shuffle_loading_zones == "all" and spoiler.shuffled_exit_instructions is not None:
        varspaceOffset = 0x1FED020  # TODO: Define this as constant in a more global place
        # /* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
        moreLoadingZonesOffset = 0x05D
        ROM().seek(varspaceOffset + moreLoadingZonesOffset)
        ROM().write(1)
        for cont_map in spoiler.shuffled_exit_instructions:
            # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
            cont_map_id = int(cont_map["container_map"])
            cont_map_lzs_address = js.pointer_addresses[18]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM().readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM().seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM().readBytes(2), "big")
                # print(lz_type)
                if lz_type in valid_lz_types:
                    ROM().seek(cont_map_lzs_address + start + 0x12)
                    lz_map = int.from_bytes(ROM().readBytes(2), "big")
                    ROM().seek(cont_map_lzs_address + start + 0x14)
                    lz_exit = int.from_bytes(ROM().readBytes(2), "big")
                    for zone in cont_map["zones"]:
                        if lz_map == zone["vanilla_map"]:
                            if lz_exit == zone["vanilla_exit"]:
                                ROM().seek(cont_map_lzs_address + start + 0x12)
                                map_bytes = intToArr(zone["new_map"], 2)
                                ROM().writeBytes(bytearray(map_bytes))
                                ROM().seek(cont_map_lzs_address + start + 0x14)
                                exit_bytes = intToArr(zone["new_exit"], 2)
                                ROM().writeBytes(bytearray(exit_bytes))
                                # /* 0x05E */ unsigned short aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
                                if cont_map_id == Maps.AngryAztec and lz_map == Maps.AztecTinyRace:
                                    ROM().seek(varspaceOffset + 0x05E)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x060 */ unsigned short aztec_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.AztecTinyRace and lz_map == Maps.AngryAztec:
                                    ROM().seek(varspaceOffset + 0x060)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x062 */ unsigned short caves_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.CavesLankyRace and lz_map == Maps.CrystalCaves:
                                    ROM().seek(varspaceOffset + 0x062)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x064 */ unsigned short seal_race_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.GalleonSealRace and lz_map == Maps.GloomyGalleon:
                                    ROM().seek(varspaceOffset + 0x064)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x066 */ unsigned short factory_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.FactoryTinyRace and lz_map == Maps.FranticFactory:
                                    ROM().seek(varspaceOffset + 0x066)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x068 */ unsigned short castle_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.CastleTinyRace and lz_map == Maps.CastleMuseum:
                                    ROM().seek(varspaceOffset + 0x068)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x06A */ unsigned short seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.GloomyGalleon and lz_map == Maps.GalleonSickBay:
                                    ROM().seek(varspaceOffset + 0x06A)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x06C */ unsigned short fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.FungiForest and lz_map == Maps.ForestMinecarts:
                                    ROM().seek(varspaceOffset + 0x06C)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x06E */ unsigned short fungi_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.ForestMinecarts and lz_map == Maps.FungiForest:
                                    ROM().seek(varspaceOffset + 0x06E)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x070 */ unsigned short japes_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.JapesMinecarts and lz_map == Maps.JungleJapes:
                                    ROM().seek(varspaceOffset + 0x070)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x072 */ unsigned short castle_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.CastleMinecarts and lz_map == Maps.CastleCrypt:
                                    ROM().seek(varspaceOffset + 0x072)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x074 */ unsigned short castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.Isles and lz_map == Maps.CreepyCastleLobby:
                                    ROM().seek(varspaceOffset + 0x074)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x120 */ unsigned short ballroom_to_museum; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.CastleBallroom and lz_map == Maps.CastleMuseum:
                                    ROM().seek(varspaceOffset + 0x120)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x122 */ unsigned short museum_to_ballroom; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.CastleMuseum and lz_map == Maps.CastleBallroom:
                                    ROM().seek(varspaceOffset + 0x122)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x078 */ unsigned short exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.JungleJapes and lz_map == Maps.JungleJapesLobby:
                                    ROM().seek(varspaceOffset + 0x078)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.AngryAztec and lz_map == Maps.AngryAztecLobby:
                                    ROM().seek(varspaceOffset + 0x07A)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.FranticFactory and lz_map == Maps.FranticFactoryLobby:
                                    ROM().seek(varspaceOffset + 0x07C)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.GloomyGalleon and lz_map == Maps.GloomyGalleonLobby:
                                    ROM().seek(varspaceOffset + 0x07E)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.FungiForest and lz_map == Maps.FungiForestLobby:
                                    ROM().seek(varspaceOffset + 0x080)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.CrystalCaves and lz_map == Maps.CrystalCavesLobby:
                                    ROM().seek(varspaceOffset + 0x082)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.CreepyCastle and lz_map == Maps.CreepyCastleLobby:
                                    ROM().seek(varspaceOffset + 0x084)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                # /* 0x088 */ unsigned short enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
                                elif cont_map_id == Maps.JungleJapesLobby and lz_map == Maps.JungleJapes:
                                    ROM().seek(varspaceOffset + 0x088)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.AngryAztecLobby and lz_map == Maps.AngryAztec:
                                    ROM().seek(varspaceOffset + 0x08A)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.FranticFactoryLobby and lz_map == Maps.FranticFactory:
                                    ROM().seek(varspaceOffset + 0x08C)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.GloomyGalleonLobby and lz_map == Maps.GloomyGalleon:
                                    ROM().seek(varspaceOffset + 0x08E)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.FungiForestLobby and lz_map == Maps.FungiForest:
                                    ROM().seek(varspaceOffset + 0x090)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.CrystalCavesLobby and lz_map == Maps.CrystalCaves:
                                    ROM().seek(varspaceOffset + 0x092)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])
                                elif cont_map_id == Maps.CreepyCastleLobby and lz_map == Maps.CreepyCastle:
                                    ROM().seek(varspaceOffset + 0x094)
                                    ROM().write(zone["new_map"])
                                    ROM().write(zone["new_exit"])

