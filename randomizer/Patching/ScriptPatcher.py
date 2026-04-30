"""Patching master file for instance scripts."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Settings import MiscChangesSelected, FasterChecksSelected, ExtraCutsceneSkips, RemovedBarriersSelected, SwitchsanityGone, MicrohintsEnabled
from randomizer.Lists.Minigame import MinigameRequirements
from randomizer.Patching.Library.Generic import IsDDMSSelected
from randomizer.Patching.Library.Scripts import replaceScriptLines, addNewScript

def isQoLEnabled(spoiler, misc_change: MiscChangesSelected):
    """Determine if a faster check setting is enabled."""
    return IsDDMSSelected(spoiler.settings.misc_changes_selected, misc_change)

def isBarrierRemoved(spoiler, barrier: RemovedBarriersSelected):
    """Determine if a barrier setting is enabled."""
    return IsDDMSSelected(spoiler.settings.remove_barriers_selected, barrier)

def patchScripts(spoiler, ROM_COPY):
    """Patch instance scripts."""
    if isQoLEnabled(spoiler, MiscChangesSelected.quicker_galleon_star):
        replaceScriptLines(ROM_COPY, Maps.GloomyGalleon, [0xC], {
            "EXEC 1 | 1 0 0": "EXEC 1 | 3 0 0"
        })
    if isQoLEnabled(spoiler, MiscChangesSelected.vanilla_bug_fixes):
        # Speed up Fungi ToD transition
        replaceScriptLines(ROM_COPY, Maps.FungiForest, [0x4, 0x5], {
            "EXEC 3 | 0 70 0": "EXEC 83 | 0 0 0"
        })
    if isQoLEnabled(spoiler, MiscChangesSelected.remove_enemy_cabin_timer):
        # Speed up Fungi ToD transition
        replaceScriptLines(ROM_COPY, Maps.CavesDiddyLowerCabin, [0x0], {
            "COND 0 | 0 0 1": "CONDINV 0 | 0 0 0"
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
        # Remove Aztec Coconut Cutscene
        replaceScriptLines(ROM_COPY, Maps.AngryAztec, [0xD], {
            "EXEC 37 | 23 1 0": "EXEC 83 | 0 0 0"
        })
    # Helm Pads
    helm_pad_data = {
        0x2C: {
            # Bongo
            "temp_flags": [60, 65, 75],
            "glass_panel": 55,
            "hint_cs": 18,
            "kong_id": Kongs.donkey,
            "microhint": int(spoiler.settings.microhints_enabled) == 2,
            "req_minigames": int(spoiler.settings.helm_room_bonus_count),
            "helm_order": spoiler.settings.helm_order,
        },
        0x30: {
            # Guitar
            "temp_flags": [61, 66, 79],
            "glass_panel": 57,
            "hint_cs": 22,
            "kong_id": Kongs.diddy,
            "microhint": int(spoiler.settings.microhints_enabled) == 2,
            "req_minigames": int(spoiler.settings.helm_room_bonus_count),
            "helm_order": spoiler.settings.helm_order,
        },
        0x2F: {
            # Trombone
            "temp_flags": [64, 69, 78],
            "glass_panel": 56,
            "hint_cs": 21,
            "kong_id": Kongs.lanky,
            "microhint": int(spoiler.settings.microhints_enabled) == 2,
            "req_minigames": int(spoiler.settings.helm_room_bonus_count),
            "helm_order": spoiler.settings.helm_order,
        },
        0x2E: {
            # Sax
            "temp_flags": [62, 67, 77],
            "glass_panel": 52,
            "hint_cs": 20,
            "kong_id": Kongs.tiny,
            "microhint": int(spoiler.settings.microhints_enabled) == 2,
            "req_minigames": int(spoiler.settings.helm_room_bonus_count),
            "helm_order": spoiler.settings.helm_order,
        },
        0x2D: {
            # Triangle
            "temp_flags": [63, 68, 76],
            "glass_panel": 54,
            "hint_cs": 19,
            "kong_id": Kongs.chunky,
            "microhint": int(spoiler.settings.microhints_enabled) == 2,
            "req_minigames": int(spoiler.settings.helm_room_bonus_count),
            "helm_order": spoiler.settings.helm_order,
        },
    }
    addNewScript(ROM_COPY, Maps.HideoutHelm, list(helm_pad_data.keys()), ScriptTypes.HelmInstrumentPad, helm_pad_data)
    # Llama Temple Head Sounds
    original_sounds = [173, 171, 169, 174, 172, 175, 168, 170]
    ids = [
        [0x1E, 0x23],
        [0x24, 0x27],
        [0x1B, 0x26],
        [0x1D, 0x21],
        [0x1A, 0x25],
        [0x20, 0x22],
        [0x19, 0x1F],
        [0x1C, 0x28],
    ]
    for pair_index, pair in enumerate(ids):
        old_sound = original_sounds[pair_index]
        new_sound = spoiler.settings.matching_game_sounds[pair_index]
        replaceScriptLines(ROM_COPY, Maps.AztecLlamaTemple, pair, {
            f"EXEC 15 | {old_sound} 0 0": f"EXEC 15 | {new_sound} 0 0"
        })
    # Chunky Cabin Minigame check
    cabin_minigame_map = 139
    helm_lobby_minigame_map = 117
    if len(spoiler.settings.minigames_list_selected) > 0:
        for minigame_data in spoiler.shuffled_barrel_data.values():
            if minigame_data.map == Maps.CavesChunkyCabin:
                cabin_minigame_map = MinigameRequirements[minigame_data.minigame].map
            elif minigame_data.map == Maps.HideoutHelmLobby:
                helm_lobby_minigame_map = MinigameRequirements[minigame_data.minigame].map
        replaceScriptLines(ROM_COPY, Maps.CavesChunkyCabin, [0x3, 0x4, 0x5, 0x6], {
            "COND 50 | 139 0 0": f"COND 50 | {cabin_minigame_map} 0 0"
        })
        replaceScriptLines(ROM_COPY, Maps.CavesChunkyCabin, [0x3, 0x4, 0x5, 0x6], {
            "CONDINV 50 | 139 0 0": f"CONDINV 50 | {cabin_minigame_map} 0 0"
        })
    gone_pad = SwitchsanityGone.gone_pad
    gone_kong = spoiler.settings.switchsanity_data[Switches.IslesHelmLobbyGone].kong
    gone_type = spoiler.settings.switchsanity_data[Switches.IslesHelmLobbyGone].switch_type
    if gone_type == SwitchType.InstrumentPad:
        gone_pad = SwitchsanityGone.bongos + (gone_kong - Kongs.donkey)
    elif gone_type == SwitchType.MiscActivator:
        if gone_kong == Kongs.donkey:
            gone_pad = SwitchsanityGone.lever
        elif gone_kong == Kongs.diddy:
            gone_pad = SwitchsanityGone.gong
    addNewScript(ROM_COPY, Maps.HideoutHelmLobby, [0x3], ScriptTypes.HelmLobbyPadGrab, {
        "activator": gone_pad,
        "bonus_map": helm_lobby_minigame_map,
        "microhint": spoiler.settings.microhints_enabled != MicrohintsEnabled.off,
    })
    port_kong = spoiler.settings.switchsanity_data[Switches.IslesMonkeyport].kong
    addNewScript(ROM_COPY, Maps.Isles, [0x38], ScriptTypes.KrocIslePort, {
        "kong": port_kong,
        "microhint": spoiler.settings.microhints_enabled != MicrohintsEnabled.off,
    })
    if port_kong != Kongs.tiny:
        addNewScript(ROM_COPY, Maps.Isles, [0x37], ScriptTypes.DeleteItem)
    if isBarrierRemoved(spoiler, RemovedBarriersSelected.aztec_llama_switches):
        # Aztec Llama Switches
        replaceScriptLines(ROM_COPY, Maps.AngryAztec, [0xD, 0xE, 0xF], {
            "CONDINV 45 | 50 0 0": "CONDINV 0 | 0 0 0"
        })
        replaceScriptLines(ROM_COPY, Maps.AngryAztec, [0xD, 0xE, 0xF], {
            "COND 45 | 50 0 0": "COND 0 | 0 0 0"
        })
    if not spoiler.settings.sprint_barrel_requires_sprint:
        replaceScriptLines(ROM_COPY, Maps.HelmBarrelLankyMaze, [0x0], {
            "COND 38 | 0 32 0": "COND 0 | 0 0 0"
        })
    if isBarrierRemoved(spoiler, RemovedBarriersSelected.japes_coconut_gates):
        addNewScript(ROM_COPY, Maps.JungleJapes, [0x2D, 0x2E, 0x2F], ScriptTypes.DeleteItem)
    addNewScript(ROM_COPY, Maps.FranticFactory, [0x14], ScriptTypes.Piano, {
        "piano_order": spoiler.settings.piano_game_order,
        "fast_piano": IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.factory_piano_game),
    })