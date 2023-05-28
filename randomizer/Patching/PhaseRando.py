"""Apply K Rool Phase order."""
import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.EntranceRando import intToArr
from randomizer.Patching.Patcher import ROM, LocalROM


def randomize_krool(spoiler):
    """Apply K Rool Phase order based on krool_order from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    # /* 0x058 */ char k_rool_order[5]; // Order of K. Rool phases: [0,1,2,3,4] dictates DK->Diddy->Lanky->Tiny->Chunky. If K. Rool is being shortened to less than 5 phases, put the unused phases as -1
    kroolOffset = 0x058
    LocalROM().seek(varspaceOffset + kroolOffset)
    phaseCount = len(spoiler.settings.krool_order)
    LocalROM().writeBytes(bytearray(spoiler.settings.krool_order))
    for i in range(5 - phaseCount):
        LocalROM().write(255)

    firstPhase = spoiler.settings.krool_order[0]
    if firstPhase != 0:  # If not starting with DK
        KroolPhaseMaps = [Maps.KroolDonkeyPhase, Maps.KroolDiddyPhase, Maps.KroolLankyPhase, Maps.KroolTinyPhase, Maps.KroolChunkyPhase]
        # Get new first phase map to write
        firstPhaseMap = KroolPhaseMaps[firstPhase]

        # Find Isles->DK Phase loading zone in Pointer table 18 and write new destination map
        cont_map_lzs_address = js.pointer_addresses[18]["entries"][Maps.Isles]["pointing_to"]
        LocalROM().seek(cont_map_lzs_address)
        lz_count = int.from_bytes(LocalROM().readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            LocalROM().seek(cont_map_lzs_address + start + 0x12)
            lz_map = int.from_bytes(LocalROM().readBytes(2), "big")
            if lz_map == Maps.KroolDonkeyPhase:
                LocalROM().seek(cont_map_lzs_address + start + 0x12)
                map_bytes = intToArr(firstPhaseMap, 2)
                LocalROM().writeBytes(bytearray(map_bytes))


def randomize_helm(spoiler):
    """Apply Helm Room order based on helm_order from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    helmOffset = 0x190
    LocalROM().seek(varspaceOffset + helmOffset)
    roomCount = len(spoiler.settings.helm_order)
    LocalROM().writeBytes(bytearray(spoiler.settings.helm_order))
    for i in range(5 - roomCount):
        LocalROM().write(255)
