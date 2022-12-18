"""Apply Patch data to the ROM."""
import asyncio
import codecs
import json
import math
import pickle
import random

import js
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Patching.BananaPortRando import randomize_bananaport
from randomizer.Patching.BarrelRando import randomize_barrels
from randomizer.Patching.BossRando import randomize_bosses
from randomizer.Patching.CosmeticColors import apply_cosmetic_colors, overwrite_object_colors, applyKrushaKong, writeMiscCosmeticChanges, applyHolidayMode
from randomizer.Patching.DKTV import randomize_dktv
from randomizer.Patching.EnemyRando import randomize_enemies
from randomizer.Patching.EntranceRando import randomize_entrances, filterEntranceType
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.KasplatLocationRando import randomize_kasplat_locations
from randomizer.Patching.KongRando import apply_kongrando_cosmetic
from randomizer.Patching.MiscSetupChanges import randomize_setup
from randomizer.Patching.MoveLocationRando import randomize_moves
from randomizer.Patching.MusicRando import randomize_music
from randomizer.Patching.ItemRando import place_randomized_items
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.PhaseRando import randomize_helm, randomize_krool
from randomizer.Patching.PriceRando import randomize_prices
from randomizer.Patching.PuzzleRando import randomize_puzzles
from randomizer.Patching.UpdateHints import PushHints, wipeHints, replaceIngameText
from randomizer.Patching.MiscSetupChanges import randomize_setup
from randomizer.Patching.BananaPlacer import randomize_cbs
from randomizer.Patching.ShopRandomizer import ApplyShopRandomizer
from randomizer.Patching.CrownPlacer import randomize_crown_pads
from ui.GenTracker import generateTracker
from ui.GenSpoiler import GenerateSpoiler
from randomizer.Patching.UpdateHints import PushHints, wipeHints
from randomizer.Patching.DoorPlacer import place_door_locations
from randomizer.Lists.QoL import QoLSelector
from randomizer.Lists.EnemyTypes import EnemySelector

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings
from ui.GenTracker import generateTracker
from ui.progress_bar import ProgressBar


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def patching_response(responded_data):
    """Response data from the background task.

    Args:
        responded_data (str): Pickled data (or json)
    """
    loop = asyncio.get_event_loop()

    try:
        loaded_data = json.loads(responded_data)
        if loaded_data.get("error"):
            error = loaded_data.get("error")
            ProgressBar().set_class("bg-danger")
            js.toast_alert(error)
            loop.run_until_complete(ProgressBar().update_progress(10, f"Error: {error}"))
            loop.run_until_complete(ProgressBar().reset())
            return None
    except Exception:
        pass

    loop.run_until_complete(ProgressBar().update_progress(8, "Applying Patches"))
    # spoiler: Spoiler = pickle.loads(codecs.decode(responded_data.encode(), "base64"))
    spoiler = pickle.loads(codecs.decode(responded_data.encode(), "base64"))
    spoiler.settings.verify_hash()
    Settings({"seed": 0}).compare_hash(spoiler.settings.public_hash)
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()
    if spoiler.settings.download_patch_file:
        spoiler.settings.download_patch_file = False

        js.save_text_as_file(codecs.encode(pickle.dumps(spoiler), "base64").decode(), f"dk64-{spoiler.settings.seed_id}.lanky")
    js.write_seed_history(spoiler.settings.seed_id, codecs.encode(pickle.dumps(spoiler), "base64").decode(), spoiler.settings.public_hash)
    # Write date to ROM for debugging purposes
    dt = js.getDate()
    temp_json = json.loads(spoiler.json)
    temp_json["Settings"]["Generation Timestamp"] = dt
    spoiler.json = json.dumps(temp_json, indent=4)
    ROM().seek(0x1FFF200)
    ROM().writeBytes(dt.encode("ascii"))
    # Initialize Text Changes
    spoiler.text_changes = {}

    # Starting index for our settings
    sav = spoiler.settings.rom_data

    # Shuffle Levels
    if spoiler.settings.shuffle_loading_zones == "levels":
        ROM().seek(sav + 0)
        ROM().write(1)

        # Update Level Order
        vanilla_lobby_entrance_order = [
            Transitions.IslesMainToJapesLobby,
            Transitions.IslesMainToAztecLobby,
            Transitions.IslesMainToFactoryLobby,
            Transitions.IslesMainToGalleonLobby,
            Transitions.IslesMainToForestLobby,
            Transitions.IslesMainToCavesLobby,
            Transitions.IslesMainToCastleLobby,
        ]
        vanilla_lobby_exit_order = [
            Transitions.IslesJapesLobbyToMain,
            Transitions.IslesAztecLobbyToMain,
            Transitions.IslesFactoryLobbyToMain,
            Transitions.IslesGalleonLobbyToMain,
            Transitions.IslesForestLobbyToMain,
            Transitions.IslesCavesLobbyToMain,
            Transitions.IslesCastleLobbyToMain,
        ]
        order = 0
        for level in vanilla_lobby_entrance_order:
            ROM().seek(sav + 1 + order)
            ROM().write(vanilla_lobby_exit_order.index(spoiler.shuffled_exit_data[int(level)].reverse))
            order += 1

        # Key Order
        map_pointers = {
            Transitions.IslesMainToJapesLobby: Transitions.IslesJapesLobbyToMain,
            Transitions.IslesMainToAztecLobby: Transitions.IslesAztecLobbyToMain,
            Transitions.IslesMainToFactoryLobby: Transitions.IslesFactoryLobbyToMain,
            Transitions.IslesMainToGalleonLobby: Transitions.IslesGalleonLobbyToMain,
            Transitions.IslesMainToForestLobby: Transitions.IslesForestLobbyToMain,
            Transitions.IslesMainToCavesLobby: Transitions.IslesCavesLobbyToMain,
            Transitions.IslesMainToCastleLobby: Transitions.IslesCastleLobbyToMain,
        }
        key_mapping = {
            # key given in each level. (Item 1 is Japes etc. flags=[0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D] <- Item 1 of this array is Key 1 etc.)
            Transitions.IslesJapesLobbyToMain: 0x1A,
            Transitions.IslesAztecLobbyToMain: 0x4A,
            Transitions.IslesFactoryLobbyToMain: 0x8A,
            Transitions.IslesGalleonLobbyToMain: 0xA8,
            Transitions.IslesForestLobbyToMain: 0xEC,
            Transitions.IslesCavesLobbyToMain: 0x124,
            Transitions.IslesCastleLobbyToMain: 0x13D,
        }
        order = 0
        if Types.Key not in spoiler.settings.shuffled_location_types:
            for key, value in map_pointers.items():
                new_world = spoiler.shuffled_exit_data.get(key).reverse
                ROM().seek(sav + 0x01E + order)
                ROM().writeMultipleBytes(key_mapping[int(new_world)], 2)
                order += 2
        else:
            for key in key_mapping:
                ROM().seek(sav + 0x1E + order)
                ROM().writeMultipleBytes(key_mapping[key], 2)
                order += 2

    # Color Banana Requirements
    order = 0
    for count in spoiler.settings.BossBananas:
        ROM().seek(sav + 0x008 + order)
        ROM().writeMultipleBytes(count, 2)
        order += 2

    # Golden Banana Requirements
    order = 0
    for count in spoiler.settings.EntryGBs:
        ROM().seek(sav + 0x016 + order)
        ROM().writeMultipleBytes(count, 1)
        order += 1

    # Unlock All Kongs
    if spoiler.settings.starting_kongs_count == 5:
        ROM().seek(sav + 0x02C)
        ROM().write(0x1F)
    else:
        bin_value = 0
        for x in spoiler.settings.starting_kong_list:
            bin_value |= 1 << x
        ROM().seek(sav + 0x02C)
        ROM().write(bin_value)

    boolean_props = [
        BooleanProperties(spoiler.settings.unlock_all_moves, 0x2D),  # Unlock All Moves
        BooleanProperties(True, 0x2E),  # Fast Start Game
        BooleanProperties(spoiler.settings.shockwave_status == "start_with", 0x2F),  # Unlock Shockwave
        BooleanProperties(spoiler.settings.enable_tag_anywhere, 0x30),  # Tag Anywhere
        BooleanProperties(spoiler.settings.fps_display, 0x96),  # FPS Display
        BooleanProperties(spoiler.settings.crown_door_open, 0x32),  # Crown Door Open
        BooleanProperties(spoiler.settings.no_healing, 0xA6),  # Disable Healing
        BooleanProperties(spoiler.settings.no_melons, 0x128),  # No Melon Drops
        BooleanProperties(spoiler.settings.bonus_barrel_auto_complete, 0x126),  # Auto-Complete Bonus Barrels
        BooleanProperties(spoiler.settings.warp_to_isles, 0x135),  # Warp to Isles
        BooleanProperties(spoiler.settings.perma_death, 0x14D),  # Permadeath
        BooleanProperties(spoiler.settings.perma_death, 0x14E),  # Disable Boss Door Check
        BooleanProperties(spoiler.settings.disable_tag_barrels, 0x14F),  # Disable Tag Spawning
        BooleanProperties(spoiler.settings.open_levels, 0x137),  # Open Levels
        BooleanProperties(spoiler.settings.shorten_boss, 0x13B),  # Shorten Boss Fights
        BooleanProperties(spoiler.settings.fast_warps, 0x13A),  # Fast Warps
        BooleanProperties(spoiler.settings.dpad_display, 0x139),  # DPad Display
        BooleanProperties(spoiler.settings.high_req, 0x179),  # Remove High Requirements
        BooleanProperties(spoiler.settings.fast_gbs, 0x17A),  # Fast GBs
        BooleanProperties(spoiler.settings.auto_keys, 0x15B),  # Auto-Turn Keys
        BooleanProperties(spoiler.settings.disco_chunky, 0x12F),  # Disco Chunky
        BooleanProperties(spoiler.settings.tns_location_rando, 0x10E),  # T&S Portal Location Rando
        BooleanProperties(spoiler.settings.cb_rando, 0xAF),  # Show CBs/Coins
        BooleanProperties(spoiler.settings.cb_rando, 0x10B),  # Remove Rock Bunch
        BooleanProperties(
            spoiler.settings.wrinkly_location_rando or ("remove_wrinkly_puzzles" in spoiler.settings.misc_changes_selected or len(spoiler.settings.misc_changes_selected) == 0), 0x11F
        ),  # Wrinkly Rando
        BooleanProperties(spoiler.settings.helm_hurry, 0xAE),  # Helm Hurry
        BooleanProperties(spoiler.settings.remove_water_oscillation, 0x10F),  # Remove Water Oscillation
        BooleanProperties(spoiler.settings.hard_enemies, 0x116),  # Hard Enemies
        BooleanProperties(spoiler.settings.wrinkly_available, 0x52),  # Remove Wrinkly Kong Checks
        BooleanProperties(spoiler.settings.bananaport_rando in ("crossmap_coupled", "crossmap_decoupled"), 0x47),  # Parent Map Filter
        BooleanProperties(spoiler.settings.shop_indicator, 0x134, 2),  # Shop Indicator
        BooleanProperties(spoiler.settings.open_lobbies, 0x14C, 0xFF),  # Open Lobbies
        BooleanProperties(spoiler.settings.disable_shop_hints, 0x14B, 0),  # Disable Shop Hints
    ]

    for prop in boolean_props:
        if prop.check:
            ROM().seek(sav + prop.offset)
            ROM().write(prop.target)

    # Fast Hideout
    ROM().seek(sav + 0x031)
    ROM().write(("default", "skip_start", "skip_all").index(spoiler.settings.helm_setting))

    # Coin Door Requirements
    ROM().seek(sav + 0x033)
    ROM().write(("need_both", "need_zero", "need_nin", "need_rw").index(spoiler.settings.coin_door_open))

    # Free Trade Agreement
    if spoiler.settings.free_trade_items:
        ROM().seek(sav + 0x113)
        old = int.from_bytes(ROM().readBytes(1), "big")
        ROM().seek(sav + 0x113)
        ROM().write(old | 1)
    if spoiler.settings.free_trade_blueprints:
        ROM().seek(sav + 0x113)
        old = int.from_bytes(ROM().readBytes(1), "big")
        ROM().seek(sav + 0x113)
        ROM().write(old | 2)
    # Quality of Life
    if spoiler.settings.quality_of_life:
        enabled_qol = spoiler.settings.misc_changes_selected.copy()
        if len(enabled_qol) == 0:
            for item in QoLSelector:
                enabled_qol.append(item["value"])
        write_data = [0, 0]
        for item in QoLSelector:
            if item["value"] in enabled_qol and item["shift"] >= 0:
                offset = int(item["shift"] >> 3)
                check = int(item["shift"] % 8)
                write_data[offset] |= 0x80 >> check
        ROM().seek(sav + 0x0B0)
        for byte_data in write_data:
            ROM().writeMultipleBytes(byte_data, 1)

    # Damage amount
    damage_multipliers = {
        "default": 1,
        "double": 2,
        "quad": 4,
        "ohko": 12,
    }
    ROM().seek(sav + 0x0A5)
    ROM().write(damage_multipliers[spoiler.settings.damage_amount])

    # Activate Bananaports
    ROM().seek(sav + 0x138)
    ROM().write(("off", "all", "isles").index(spoiler.settings.activate_all_bananaports))

    if spoiler.settings.hard_bosses:
        # KKO Phase Order
        for phase_slot in range(3):
            ROM().seek(sav + 0x17B + phase_slot)
            ROM().write(spoiler.settings.kko_phase_order[phase_slot])
        # Random Toe Sequence
        ROM().seek(sav + 0x41)
        ROM().write(1)
        for slot in range(10):
            ROM().seek(sav + 0x37 + slot)
            ROM().write(spoiler.settings.toe_order[slot])

    # Win Condition
    conditions = ["beat_krool", "get_key8", "all_fairies", "all_blueprints", "all_medals", "poke_snap", "all_keys"]
    if spoiler.settings.win_condition in conditions:
        condition_index = conditions.index(spoiler.settings.win_condition)
        ROM().seek(sav + 0x11D)
        ROM().write(condition_index)

    keys_turned_in = [0, 1, 2, 3, 4, 5, 6, 7]
    if len(spoiler.settings.krool_keys_required) > 0:
        for key in spoiler.settings.krool_keys_required:
            key_index = key - 4
            if key_index in keys_turned_in:
                keys_turned_in.remove(key_index)
    key_bitfield = 0
    for key in keys_turned_in:
        key_bitfield = key_bitfield | (1 << key)
    ROM().seek(sav + 0x127)
    ROM().write(key_bitfield)

    if spoiler.settings.medal_requirement != 15:
        ROM().seek(sav + 0x150)
        ROM().write(spoiler.settings.medal_requirement)

    if spoiler.settings.rareware_gb_fairies != 20:
        ROM().seek(sav + 0x36)
        ROM().write(spoiler.settings.rareware_gb_fairies)

    if spoiler.settings.medal_cb_req != 75:
        ROM().seek(sav + 0x112)
        ROM().write(spoiler.settings.medal_cb_req)

    if len(spoiler.settings.enemies_selected) == 0 and (spoiler.settings.enemy_rando or spoiler.settings.crown_enemy_rando != "off"):
        lst = []
        for enemy in EnemySelector:
            lst.append(enemy["value"])
        spoiler.settings.enemies_selected = lst

    if spoiler.settings.random_starting_region:
        ROM().seek(sav + 0x10C)
        ROM().write(spoiler.settings.starting_region["map"])
        ROM().write(spoiler.settings.starting_region["exit"])

    # randomize_dktv()
    randomize_entrances(spoiler)
    randomize_moves(spoiler)
    randomize_prices(spoiler)
    randomize_bosses(spoiler)
    randomize_krool(spoiler)
    randomize_helm(spoiler)
    randomize_barrels(spoiler)
    randomize_bananaport(spoiler)
    randomize_kasplat_locations(spoiler)
    randomize_enemies(spoiler)
    apply_kongrando_cosmetic(spoiler)
    randomize_setup(spoiler)
    randomize_puzzles(spoiler)
    randomize_cbs(spoiler)
    ApplyShopRandomizer(spoiler)
    place_randomized_items(spoiler)  # Has to be after kong rando cosmetic and moves
    place_door_locations(spoiler)
    randomize_crown_pads(spoiler)
    filterEntranceType()
    replaceIngameText(spoiler)

    random.seed(spoiler.settings.seed)
    randomize_music(spoiler)
    applyKrushaKong(spoiler)
    apply_cosmetic_colors(spoiler)
    overwrite_object_colors(spoiler)
    writeMiscCosmeticChanges(spoiler)
    applyHolidayMode(spoiler)
    random.seed(spoiler.settings.seed)

    if spoiler.settings.wrinkly_hints in ["standard", "cryptic"]:
        wipeHints()
        PushHints(spoiler)

    # Apply Hash
    order = 0
    loaded_hash = get_hash_images()
    for count in spoiler.settings.seed_hash:
        ROM().seek(sav + 0x129 + order)
        ROM().write(count)
        js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
        order += 1

    loop.run_until_complete(ProgressBar().update_progress(10, "Seed Generated."))
    js.document.getElementById("nav-settings-tab").style.display = ""
    if spoiler.settings.generate_spoilerlog is True:
        js.document.getElementById("spoiler_log_block").style.display = ""
        loop.run_until_complete(GenerateSpoiler(spoiler.json))
        js.document.getElementById("tracker_text").value = generateTracker(spoiler.json)
    else:
        js.document.getElementById("spoiler_log_text").innerHTML = ""
        js.document.getElementById("spoiler_log_text").value = ""
        js.document.getElementById("tracker_text").value = ""
        js.document.getElementById("spoiler_log_block").style.display = "none"

    js.document.getElementById("generated_seed_id").innerHTML = spoiler.settings.seed_id
    loaded_settings = json.loads(spoiler.json)["Settings"]
    tables = {}
    t = 0
    for i in range(0, 3):
        js.document.getElementById(f"settings_table_{i}").innerHTML = ""
        tables[i] = js.document.getElementById(f"settings_table_{i}")
    for setting, value in loaded_settings.items():
        hidden_settings = ["Seed", "algorithm"]
        if setting not in hidden_settings:
            if tables[t].rows.length > math.ceil((len(loaded_settings.items()) - len(hidden_settings)) / len(tables)):
                t += 1
            row = tables[t].insertRow(-1)
            name = row.insertCell(0)
            description = row.insertCell(1)
            name.innerHTML = setting
            description.innerHTML = FormatSpoiler(value)
    ROM().fixSecurityValue()
    ROM().save(f"dk64-{spoiler.settings.seed_id}.z64")
    loop.run_until_complete(ProgressBar().reset())
    js.jq("#nav-settings-tab").tab("show")


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result
