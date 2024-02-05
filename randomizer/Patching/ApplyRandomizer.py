"""Apply Patch data to the ROM."""

import json
import os
from datetime import datetime as Datetime
from datetime import UTC
import time
from tempfile import mktemp

from randomizer.Enums.Settings import (
    BananaportRando,
    CrownEnemyRando,
    DamageAmount,
    FasterChecksSelected,
    FungiTimeSetting,
    GalleonWaterSetting,
    HardModeSelected,
    HelmDoorItem,
    MiscChangesSelected,
    RemovedBarriersSelected,
    ShockwaveStatus,
    ShuffleLoadingZones,
    WrinklyHints,
)
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Enums.Items import Items
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.EnemyTypes import Enemies, EnemySelector
from randomizer.Lists.HardMode import HardSelector
from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
from randomizer.Patching.BananaPlacer import randomize_cbs
from randomizer.Patching.BananaPortRando import randomize_bananaport
from randomizer.Patching.BarrelRando import randomize_barrels
from randomizer.Patching.BossRando import randomize_bosses
from randomizer.Patching.CoinPlacer import randomize_coins
from randomizer.Patching.CosmeticColors import applyHelmDoorCosmetics, applyKrushaKong, updateCryptLeverTexture, updateMillLeverTexture, writeBootMessages, updateDiddyDoors
from randomizer.Patching.CratePlacer import randomize_melon_crate
from randomizer.Patching.CrownPlacer import randomize_crown_pads
from randomizer.Patching.DoorPlacer import place_door_locations, remove_existing_indicators
from randomizer.Patching.EnemyRando import randomize_enemies
from randomizer.Patching.EntranceRando import enableTriggerText, filterEntranceType, randomize_entrances
from randomizer.Patching.FairyPlacer import PlaceFairies
from randomizer.Patching.ItemRando import place_randomized_items
from randomizer.Patching.KasplatLocationRando import randomize_kasplat_locations
from randomizer.Patching.KongRando import apply_kongrando_cosmetic
from randomizer.Patching.Lib import setItemReferenceName, addNewScript, IsItemSelected
from randomizer.Patching.MiscSetupChanges import randomize_setup, updateKrushaMoveNames, updateRandomSwitches, updateSwitchsanity
from randomizer.Patching.MoveLocationRando import place_pregiven_moves, randomize_moves
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.PhaseRando import randomize_helm, randomize_krool
from randomizer.Patching.PriceRando import randomize_prices
from randomizer.Patching.PuzzleRando import randomize_puzzles, shortenCastleMinecart
from randomizer.Patching.ShopRandomizer import ApplyShopRandomizer
from randomizer.Patching.UpdateHints import PushHints, replaceIngameText, wipeHints, PushItemLocations, PushHelpfulHints
from randomizer.Patching.ASMPatcher import patchAssembly

# from randomizer.Spoiler import Spoiler


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def writeMultiselector(enabled: bool, enabled_selections: list, selector: list[dict], selection_enum, data_length: int, ROM_COPY: LocalROM, write_start: int):
    """Write multiselector choices to ROM."""
    if enabled:
        force = len(enabled_selections) == 0
        write_data = [0] * data_length
        for item in selector:
            if item["shift"] >= 0:
                if force or selection_enum[item["value"]] in enabled_selections:
                    offset = int(item["shift"] >> 3)
                    check = int(item["shift"] % 8)
                    write_data[offset] |= 0x80 >> check
        ROM_COPY.seek(write_start)
        for byte_data in write_data:
            ROM_COPY.writeMultipleBytes(byte_data, 1)


def patching_response(spoiler):
    """Apply the patch data to the ROM in the local server to be returned to the client."""
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()

    # Write date to ROM for debugging purposes

    dt = Datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    temp_json = json.loads(spoiler.json)
    temp_json["Settings"]["Generation Timestamp"] = dt
    spoiler.json = json.dumps(temp_json, indent=4)
    ROM_COPY = LocalROM()
    ROM_COPY.seek(0x1FFF200)
    ROM_COPY.writeBytes(dt.encode("ascii"))
    # Initialize Text Changes
    spoiler.text_changes = {}

    # Starting index for our settings
    sav = spoiler.settings.rom_data

    # Shuffle Levels
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        ROM_COPY.seek(sav + 0)
        ROM_COPY.write(1)

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
            ROM_COPY.seek(sav + 1 + order)
            ROM_COPY.write(vanilla_lobby_exit_order.index(spoiler.shuffled_exit_data[int(level)].reverse))
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
                ROM_COPY.seek(sav + 0x01E + order)
                ROM_COPY.writeMultipleBytes(key_mapping[int(new_world)], 2)
                order += 2
        else:
            for key in key_mapping:
                ROM_COPY.seek(sav + 0x1E + order)
                ROM_COPY.writeMultipleBytes(key_mapping[key], 2)
                order += 2

    # Color Banana Requirements
    order = 0
    for count in spoiler.settings.BossBananas:
        ROM_COPY.seek(sav + 0x008 + order)
        ROM_COPY.writeMultipleBytes(count, 2)
        order += 2

    # Golden Banana Requirements
    order = 0
    for count in spoiler.settings.EntryGBs:
        ROM_COPY.seek(sav + 0x016 + order)
        ROM_COPY.writeMultipleBytes(count, 1)
        order += 1

    # Unlock All Kongs
    kong_items = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
    starting_kongs = []
    if spoiler.settings.starting_kongs_count == 5:
        ROM_COPY.seek(sav + 0x02C)
        ROM_COPY.write(0x1F)
        starting_kongs = kong_items.copy()
    else:
        bin_value = 0
        for x in spoiler.settings.starting_kong_list:
            bin_value |= 1 << x
            starting_kongs.append(kong_items[x])
        ROM_COPY.seek(sav + 0x02C)
        ROM_COPY.write(bin_value)
    for kong in starting_kongs:
        setItemReferenceName(spoiler, kong, 0, "Starting Kong")

    boolean_props = [
        BooleanProperties(True, 0x2E),  # Fast Start Game
        BooleanProperties(spoiler.settings.enable_tag_anywhere, 0x30),  # Tag Anywhere
        BooleanProperties(spoiler.settings.fps_display, 0x96),  # FPS Display
        BooleanProperties(spoiler.settings.crown_door_item == HelmDoorItem.opened, 0x32),  # Crown Door Open
        BooleanProperties(spoiler.settings.no_healing, 0xA6),  # Disable Healing
        BooleanProperties(spoiler.settings.no_melons, 0x128),  # No Melon Drops
        BooleanProperties(spoiler.settings.bonus_barrel_auto_complete, 0x126),  # Auto-Complete Bonus Barrels
        BooleanProperties(spoiler.settings.warp_to_isles, 0x135),  # Warp to Isles
        BooleanProperties(spoiler.settings.perma_death, 0x14D),  # Permadeath
        BooleanProperties(spoiler.settings.perma_death, 0x14E),  # Disable Boss Door Check
        BooleanProperties(spoiler.settings.disable_tag_barrels, 0x14F),  # Disable Tag Spawning
        BooleanProperties(spoiler.settings.shorten_boss, 0x13B),  # Shorten Boss Fights
        BooleanProperties(spoiler.settings.fast_warps, 0x13A),  # Fast Warps
        BooleanProperties(spoiler.settings.auto_keys, 0x15B),  # Auto-Turn Keys
        BooleanProperties(spoiler.settings.tns_location_rando, 0x10E),  # T&S Portal Location Rando
        BooleanProperties(spoiler.settings.cb_rando, 0x10B),  # Remove Rock Bunch
        BooleanProperties(spoiler.settings.wrinkly_location_rando or spoiler.settings.remove_wrinkly_puzzles, 0x11F),  # Wrinkly Rando
        BooleanProperties(spoiler.settings.helm_hurry, 0xAE),  # Helm Hurry
        BooleanProperties(spoiler.settings.wrinkly_available, 0x52),  # Remove Wrinkly Kong Checks
        BooleanProperties(spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled), 0x47),  # Parent Map Filter
        BooleanProperties(spoiler.settings.shop_indicator, 0x134, 2),  # Shop Indicator
        BooleanProperties(spoiler.settings.open_lobbies, 0x14C, 0xFF),  # Open Lobbies
        BooleanProperties(not spoiler.settings.enable_shop_hints, 0x14B, 0),  # Disable Shop Hints
        BooleanProperties(spoiler.settings.coin_door_item == HelmDoorItem.opened, 0x33),  # Coin Door Open
        BooleanProperties(spoiler.settings.item_reward_previews, 0x101, 7),  # Bonus Matches Contents
        BooleanProperties(spoiler.settings.portal_numbers, 0x11E),  # Portal Numbers
    ]

    for prop in boolean_props:
        if prop.check:
            ROM_COPY.seek(sav + prop.offset)
            ROM_COPY.write(prop.target)

    # Fast Hideout
    ROM_COPY.seek(sav + 0x031)
    # The HelmSetting enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.helm_setting))

    # Crown Door & Coin Door
    # define DOORITEM_DEFAULT 0 // Default
    # define DOORITEM_GB 1 // 1 - GBs
    # define DOORITEM_BP 2 // 2 - BP
    # define DOORITEM_BEAN 3 // 3 - Bean
    # define DOORITEM_PEARL 4 // 4 - Pearls
    # define DOORITEM_FAIRY 5 // 5 - Fairy
    # define DOORITEM_KEY 6 // 6 - Key
    # define DOORITEM_MEDAL 7 // 7 - Medal
    # define DOORITEM_RAINBOWCOIN 8 // 8 - Rainbow Coins
    # define DOORITEM_CROWN 9 // 9 - Crowns
    # define DOORITEM_COMPANYCOIN 10 // 10 - Company Coins
    door_checks = {
        HelmDoorItem.vanilla: 0,
        HelmDoorItem.req_gb: 1,
        HelmDoorItem.req_bp: 2,
        HelmDoorItem.req_bean: 3,
        HelmDoorItem.req_pearl: 4,
        HelmDoorItem.req_fairy: 5,
        HelmDoorItem.req_key: 6,
        HelmDoorItem.req_medal: 7,
        HelmDoorItem.req_rainbowcoin: 8,
        HelmDoorItem.req_crown: 9,
        HelmDoorItem.req_companycoins: 10,
    }
    if spoiler.settings.crown_door_item in door_checks.keys():
        ROM_COPY.seek(sav + 0x4C)
        ROM_COPY.write(door_checks[spoiler.settings.crown_door_item])
        ROM_COPY.seek(sav + 0x4D)
        ROM_COPY.write(spoiler.settings.crown_door_item_count)
    if spoiler.settings.coin_door_item in door_checks.keys():
        ROM_COPY.seek(sav + 0x4E)
        ROM_COPY.write(door_checks[spoiler.settings.coin_door_item])
        ROM_COPY.seek(sav + 0x4F)
        ROM_COPY.write(spoiler.settings.coin_door_item_count)

    if spoiler.settings.switchsanity:
        for slot in spoiler.settings.switchsanity_data:
            ROM_COPY.seek(sav + spoiler.settings.switchsanity_data[slot].rom_offset)
            pad_kong = spoiler.settings.switchsanity_data[slot].kong
            pad_type = spoiler.settings.switchsanity_data[slot].switch_type
            if slot == Switches.IslesMonkeyport:
                if pad_kong == Kongs.lanky:
                    ROM_COPY.writeMultipleBytes(2, 1)
                elif pad_kong == Kongs.donkey:
                    ROM_COPY.writeMultipleBytes(1, 1)
            elif slot == Switches.IslesHelmLobbyGone:
                if pad_type == SwitchType.MiscActivator:
                    if pad_kong == Kongs.donkey:
                        ROM_COPY.writeMultipleBytes(6, 1)
                    elif pad_kong == Kongs.diddy:
                        ROM_COPY.writeMultipleBytes(7, 1)
                elif pad_type != SwitchType.PadMove:
                    ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)
            else:
                ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)

    # Camera unlocked
    given_moves = []
    if spoiler.settings.shockwave_status == ShockwaveStatus.start_with:
        given_moves.extend([39, 40])  # 39 = Camera, 40 = Shockwave
        setItemReferenceName(spoiler, Items.CameraAndShockwave, 0, "Extra Training")
    move_bitfields = [0] * 6
    for move in given_moves:
        offset = int(move >> 3)
        check = int(move % 8)
        move_bitfields[offset] |= 0x80 >> check
    for offset, value in enumerate(move_bitfields):
        ROM_COPY.seek(sav + 0xD5 + offset)
        ROM_COPY.writeMultipleBytes(value, 1)

    # Free Trade Agreement
    if spoiler.settings.free_trade_items:
        ROM_COPY.seek(sav + 0x113)
        old = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(sav + 0x113)
        ROM_COPY.write(old | 1)
    if spoiler.settings.free_trade_blueprints:
        ROM_COPY.seek(sav + 0x113)
        old = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(sav + 0x113)
        ROM_COPY.write(old | 2)
    writeMultiselector(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, QoLSelector, MiscChangesSelected, 3, ROM_COPY, sav + 0x0B0)
    writeMultiselector(spoiler.settings.remove_barriers_enabled, spoiler.settings.remove_barriers_selected, RemovedBarrierSelector, RemovedBarriersSelected, 2, ROM_COPY, sav + 0x1DE)
    writeMultiselector(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterCheckSelector, FasterChecksSelected, 2, ROM_COPY, sav + 0x1E0)
    writeMultiselector(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardSelector, HardModeSelected, 1, ROM_COPY, sav + 0x0C6)

    keys = 0xFF
    if spoiler.settings.k_rool_vanilla_requirement:
        keys = 0x84  # 8765 4321 bitfield, only enable the keys 3 and 8 bits, meaning 0b1000 0100, which is 0x84
    ROM_COPY.seek(sav + 0x1DD)
    ROM_COPY.write(keys)

    # Damage amount
    damage_multipliers = {
        DamageAmount.default: 1,
        DamageAmount.double: 2,
        DamageAmount.quad: 4,
        DamageAmount.ohko: 12,
    }
    ROM_COPY.seek(sav + 0x0A5)
    ROM_COPY.write(damage_multipliers[spoiler.settings.damage_amount])

    ROM_COPY.seek(sav + 0x0C5)
    ROM_COPY.write(int(Types.Enemies in spoiler.settings.shuffled_location_types))

    # Progressive Hints
    ROM_COPY.seek(sav + 0x115)
    count = 0
    if spoiler.settings.enable_progressive_hints:
        count = spoiler.settings.progressive_hint_text
    ROM_COPY.writeMultipleBytes(count, 1)

    # Microhints
    ROM_COPY.seek(sav + 0x102)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.microhints_enabled))

    # Cutscene Skip Setting
    ROM_COPY.seek(sav + 0x116)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.more_cutscene_skips))

    # Helm Hurry

    helm_hurry_bonuses = [
        spoiler.settings.helmhurry_list_starting_time,
        spoiler.settings.helmhurry_list_golden_banana,
        spoiler.settings.helmhurry_list_blueprint,
        spoiler.settings.helmhurry_list_company_coins,
        spoiler.settings.helmhurry_list_move,
        spoiler.settings.helmhurry_list_banana_medal,
        spoiler.settings.helmhurry_list_rainbow_coin,
        spoiler.settings.helmhurry_list_boss_key,
        spoiler.settings.helmhurry_list_battle_crown,
        spoiler.settings.helmhurry_list_bean,
        spoiler.settings.helmhurry_list_pearl,
        spoiler.settings.helmhurry_list_kongs,
        spoiler.settings.helmhurry_list_fairies,
        spoiler.settings.helmhurry_list_colored_bananas,
        spoiler.settings.helmhurry_list_ice_traps,
    ]
    ROM_COPY.seek(sav + 0xE2)
    for bonus in helm_hurry_bonuses:
        if bonus < 0:
            bonus += 65536
        ROM_COPY.writeMultipleBytes(bonus, 2)

    # Activate Bananaports
    ROM_COPY.seek(sav + 0x138)
    # The ActivateAllBananaports enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.activate_all_bananaports))

    # Fast GBs - Change jetpac text
    if IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterChecksSelected.jetpac):
        cranky_index = 8
        data = {"textbox_index": 2, "mode": "replace", "search": "5000", "target": "2500"}
        if cranky_index in spoiler.text_changes:
            spoiler.text_changes[8].append(data)
        else:
            spoiler.text_changes[8] = [data]

    if HardModeSelected.hard_bosses in spoiler.settings.hard_mode_selected:
        # KKO Phase Order
        for phase_slot in range(3):
            ROM_COPY.seek(sav + 0x17B + phase_slot)
            ROM_COPY.write(spoiler.settings.kko_phase_order[phase_slot])
        # Random Toe Sequence
        ROM_COPY.seek(sav + 0x41)
        ROM_COPY.write(1)
        for slot in range(10):
            ROM_COPY.seek(sav + 0x37 + slot)
            ROM_COPY.write(spoiler.settings.toe_order[slot])

    # Win Condition
    ROM_COPY.seek(sav + 0x11D)
    # The WinCondition enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.win_condition))

    # Fungi Time of Day
    fungi_times = (FungiTimeSetting.day, FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)
    progressive_removals = [5, 4]  # Day Switch, Night Switch
    dusk_removals = {
        Maps.FungiForest: [
            5,  # Day Switch
            4,  # Night Switch
            0xC,  # Day Gate - Mill Front Entry
            0xE,  # Day Gate - Punch Door
            0x12,  # Day Gate - Snide Area
            8,  # Night Gate - Mill Lanky Attic
            0xB,  # Night Gate - Mill Winch Attic
            0xD,  # Night Gate - Dark Attic
            0x11,  # Night Gate - Thornvine Area
            0x2A,  # Night Gate - Mill GB
            0x53,  # Night Gate - Owl Tree Diddy Coins
            0x48,  # Night Gate - Beanstalk T&S
            0x1F1,  # Night Gate - Mushroom Night Door
            0x46,  # Night Gate - Crown Trapdoor
        ],
        Maps.ForestGiantMushroom: [0x11],  # Night Gate - GMush Interior
        Maps.ForestMillFront: [0xB],  # Night Gate - Mill Front
        Maps.ForestMillBack: [
            0xF,  # Night Gate - Mill Rear
            0x2,  # Night Gate - Spider Web
        ],
    }
    time_val = spoiler.settings.fungi_time_internal
    if time_val in fungi_times:
        ROM_COPY.seek(sav + 0x1DB)
        ROM_COPY.write(fungi_times.index(time_val))
        if time_val == FungiTimeSetting.progressive:
            addNewScript(Maps.FungiForest, progressive_removals, ScriptTypes.DeleteItem)
        elif time_val == FungiTimeSetting.dusk:
            for map_val in dusk_removals:
                addNewScript(map_val, dusk_removals[map_val], ScriptTypes.DeleteItem)

    # Galleon Water Level
    if spoiler.settings.galleon_water_internal == GalleonWaterSetting.raised:
        ROM_COPY.seek(sav + 0x1DC)
        ROM_COPY.writeMultipleBytes(1, 1)

    # ROM Flags
    rom_flags = 0
    rom_flags |= 0x80 if spoiler.settings.enable_plandomizer else 0
    rom_flags |= 0x40 if spoiler.settings.generate_spoilerlog else 0
    ROM_COPY.seek(sav + 0xC4)
    ROM_COPY.writeMultipleBytes(rom_flags, 1)

    # Mill Levers
    if spoiler.settings.mill_levers[0] > 0:
        mill_text = ""
        for x in range(5):
            ROM_COPY.seek(sav + 0xD0 + x)
            ROM_COPY.write(spoiler.settings.mill_levers[x])
            if spoiler.settings.mill_levers[x] > 0:
                mill_text += str(spoiler.settings.mill_levers[x])
        # Change default wrinkly hint
        if spoiler.settings.wrinkly_hints == WrinklyHints.off:
            if IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, FasterChecksSelected.forest_mill_conveyor) or spoiler.settings.puzzle_rando:
                wrinkly_index = 41
                data = {"textbox_index": 21, "mode": "replace", "search": "21132", "target": mill_text}
                if wrinkly_index in spoiler.text_changes:
                    spoiler.text_changes[41].append(data)
                else:
                    spoiler.text_changes[41] = [data]

    # Crypt Levers
    if spoiler.settings.crypt_levers[0] > 0:
        for xi, x in enumerate(spoiler.settings.crypt_levers):
            ROM_COPY.seek(sav + 0xCD + xi)
            ROM_COPY.write(x)

    # Diddy R&D Codes
    enable_code = False
    encoded_codes = []
    for code in spoiler.settings.diddy_rnd_doors:
        value = 0
        if sum(code) > 0:  # Has a non-zero element
            enable_code = True
        for subindex in range(4):
            shift = 12 - (subindex << 2)
            shifted = (code[subindex] & 3) << shift
            value |= shifted
        encoded_codes.append(value)
    if enable_code:
        ROM_COPY.seek(sav + 0x1B8)
        for code in encoded_codes:
            ROM_COPY.writeMultipleBytes(code, 2)

    keys_turned_in = [0, 1, 2, 3, 4, 5, 6, 7]
    if len(spoiler.settings.krool_keys_required) > 0:
        for key in spoiler.settings.krool_keys_required:
            key_index = key - 4
            if key_index in keys_turned_in:
                keys_turned_in.remove(key_index)
    key_bitfield = 0
    for key in keys_turned_in:
        key_bitfield = key_bitfield | (1 << key)
    ROM_COPY.seek(sav + 0x127)
    ROM_COPY.write(key_bitfield)

    if spoiler.settings.medal_requirement != 15:
        ROM_COPY.seek(sav + 0x150)
        ROM_COPY.write(spoiler.settings.medal_requirement)

    if spoiler.settings.rareware_gb_fairies != 20:
        ROM_COPY.seek(sav + 0x36)
        ROM_COPY.write(spoiler.settings.rareware_gb_fairies)

    if spoiler.settings.medal_cb_req != 75:
        ROM_COPY.seek(sav + 0x112)
        ROM_COPY.write(spoiler.settings.medal_cb_req)

    if len(spoiler.settings.enemies_selected) == 0 and (spoiler.settings.enemy_rando or spoiler.settings.crown_enemy_rando != CrownEnemyRando.off):
        lst = []
        for enemy in EnemySelector:
            lst.append(Enemies[enemy["value"]])
        spoiler.settings.enemies_selected = lst

    if spoiler.settings.random_starting_region:
        ROM_COPY.seek(sav + 0x10C)
        ROM_COPY.write(spoiler.settings.starting_region["map"])
        ROM_COPY.write(spoiler.settings.starting_region["exit"])
    if spoiler.settings.alter_switch_allocation:
        ROM_COPY.seek(sav + 0x103)
        ROM_COPY.write(1)
        for x in range(7):
            ROM_COPY.seek(sav + 0x104 + x)
            ROM_COPY.write(spoiler.settings.switch_allocation[x])

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
    randomize_coins(spoiler)
    ApplyShopRandomizer(spoiler)
    place_randomized_items(spoiler)  # Has to be after kong rando cosmetic and moves
    place_pregiven_moves(spoiler)
    remove_existing_indicators(spoiler)
    place_door_locations(spoiler)
    randomize_crown_pads(spoiler)
    randomize_melon_crate(spoiler)
    PlaceFairies(spoiler)
    filterEntranceType()
    updateKrushaMoveNames(spoiler)
    updateSwitchsanity(spoiler)
    updateRandomSwitches(spoiler)  # Has to be after all setup changes that may alter the item type of slam switches
    PushItemLocations(spoiler)

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        wipeHints()
        PushHints(spoiler)
        if spoiler.settings.dim_solved_hints:
            PushHelpfulHints(spoiler, ROM_COPY)

    writeBootMessages()
    enableTriggerText(spoiler)
    shortenCastleMinecart(spoiler)

    if "PYTEST_CURRENT_TEST" not in os.environ:
        replaceIngameText(spoiler)
        updateMillLeverTexture(spoiler.settings)
        updateCryptLeverTexture(spoiler.settings)
        updateDiddyDoors(spoiler.settings)
        applyHelmDoorCosmetics(spoiler.settings)
        applyKrushaKong(spoiler.settings)

    patchAssembly(ROM_COPY, spoiler)

    # Apply Hash
    order = 0
    for count in spoiler.settings.seed_hash:
        ROM_COPY.seek(sav + 0x129 + order)
        ROM_COPY.write(count)
        order += 1

    # Create a dummy time to attach to the end of the file name non decimal
    str(time.time()).replace(".", "")
    if "PYTEST_CURRENT_TEST" not in os.environ:
        created_tempfile = mktemp()
        delta_tempfile = mktemp()
        # Write the LocalROM.rom bytesIo to a file
        with open(created_tempfile, "wb") as f:
            f.write(ROM_COPY.rom.getvalue())

        import pyxdelta

        pyxdelta.run("dk64.z64", created_tempfile, delta_tempfile)
        # Read the patch file
        with open(delta_tempfile, "rb") as f:
            patch = f.read()
        # Delete the patch.z64 file
        os.remove(created_tempfile)
        os.remove(delta_tempfile)
    else:
        patch = None
    return patch


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result
