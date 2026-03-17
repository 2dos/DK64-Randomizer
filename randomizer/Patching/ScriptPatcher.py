"""Patching master file for instance scripts."""

from randomizer.Enums.Maps import Maps
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Patching.Library.Generic import IsDDMSSelected
from randomizer.Enums.Settings import MiscChangesSelected, FasterChecksSelected, ExtraCutsceneSkips
from randomizer.Patching.Library.Scripts import replaceScriptLines, addNewScript

def isQoLEnabled(spoiler, misc_change: MiscChangesSelected):
    """Determine if a faster check setting is enabled."""
    return IsDDMSSelected(spoiler.settings.misc_changes_selected, misc_change)

def patchScripts(spoiler, ROM_COPY):
    """Patch instance scripts."""
    if isQoLEnabled(spoiler, MiscChangesSelected.quicker_galleon_star):
        replaceScriptLines(ROM_COPY, Maps.GloomyGalleon, [0xC], {
            "EXEC 1 | 1 0 0": "EXEC 1 | 3 0 0"
        })
    if isQoLEnabled(spoiler, MiscChangesSelected.remove_galleon_ship_timers):
        obj_ids = [0x11, 0x14, 0x1B, 0x13, 0x12, 0x1D, 0x1C]
        five_door_ids = [0x11, 0x14, 0x1B, 0x13, 0x12]
        two_door_ids = [0x1D, 0x1C]
        # Remove Timer inits
        replaceScriptLines(ROM_COPY, Maps.GloomyGalleon, five_door_ids, {
            "EXEC 102 | 60 0 0": "EXEC 83 | 0 0 0"
        })
        replaceScriptLines(ROM_COPY, Maps.GloomyGalleon, two_door_ids, {
            "EXEC 102 | 30 0 0": "EXEC 83 | 0 0 0"
        })
        # Change next state
        replaceScriptLines(ROM_COPY, Maps.GloomyGalleon, obj_ids, {
            "EXEC 1 | 5 0 0": "EXEC 1 | 6 0 0",
        })
        scripting_data = {
            0x19: {
                # DK
                "flag_id": 0x2F8,
                "timer": 180,
                "timer_2": 105,
                "tied_pad": 0x11,
            },
            0x1A: {
                # Diddy
                "flag_id": 0x2F9,
                "timer": 230,
                "timer_2": 155,
                "tied_pad": 0x14,
            },
            0x17: {
                # Lanky 5D
                "flag_id": 0x2FA,
                "timer": 230,
                "timer_2": 155,
                "tied_pad": 0x12,
            },
            0x18: {
                # Tiny 5D
                "flag_id": 0x2FB,
                "timer": 230,
                "timer_2": 155,
                "tied_pad": 0x13,
            },
            0x20: {
                # Chunky
                "flag_id": 0x2FC,
                "timer": 230,
                "timer_2": 155,
                "tied_pad": 0x1B,
            },
            0x1F: {
                # Lanky 2D
                "flag_id": 0x2FE,
                "timer": 180,
                "timer_2": 110,
                "tied_pad": 0x1D,
            },
            0x1E: {
                # Tiny 2D
                "flag_id": 0x2FF,
                "timer": 230,
                "timer_2": 160,
                "tied_pad": 0x1C,
            },
        }
        addNewScript(ROM_COPY, Maps.GloomyGalleon, list(scripting_data.keys()), ScriptTypes.GalleonShipwreckDoor, scripting_data)
    if IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.galleon_mech_fish):
        replaceScriptLines(ROM_COPY, Maps.GalleonMechafish, [0x3, 0x4, 0x5], {"EXEC 1 | 1 0 0": "EXEC 1 | 5 0 0"})
    if IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.factory_arcade_round_1):
        replaceScriptLines(ROM_COPY, Maps.FactoryBaboonBlast, [0x0], {"COND 1 | 0 0 0": "CONDINV 0 | 0 0 0"})
        replaceScriptLines(ROM_COPY, Maps.FactoryBaboonBlast, [0x0], {"COND 1 | 1 0 0": "CONDINV 0 | 0 0 0"})
        addNewScript(ROM_COPY, Maps.FactoryBaboonBlast, [0x1], ScriptTypes.FactoryBlastController)
    if spoiler.settings.more_cutscene_skips == ExtraCutsceneSkips.auto:
        # Remove Charge Cutscene
        replaceScriptLines(ROM_COPY, Maps.JapesMountain, [0x37], {
            "COND 52 | 3 1 0", "COND 0 | 0 0 0"
        })