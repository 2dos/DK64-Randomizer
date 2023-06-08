"""Apply Patch data to the ROM."""
import json
import os

from randomizer.Enums.Settings import BananaportRando, CrownEnemyRando, DamageAmount, HelmDoorItem, MiscChangesSelected, ShockwaveStatus, ShuffleLoadingZones, WrinklyHints
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.EnemyTypes import Enemies, EnemySelector
from randomizer.Lists.QoL import QoLSelector
from randomizer.Patching.BananaPlacer import randomize_cbs
from randomizer.Patching.BananaPortRando import randomize_bananaport
from randomizer.Patching.BarrelRando import randomize_barrels
from randomizer.Patching.BossRando import randomize_bosses
from randomizer.Patching.CoinPlacer import randomize_coins
from randomizer.Patching.CosmeticColors import applyHelmDoorCosmetics, updateCryptLeverTexture, updateMillLeverTexture, writeBootMessages
from randomizer.Patching.CrownPlacer import randomize_crown_pads
from randomizer.Patching.DoorPlacer import place_door_locations, remove_existing_indicators
from randomizer.Patching.EnemyRando import randomize_enemies
from randomizer.Patching.EntranceRando import enableSpiderText, filterEntranceType, randomize_entrances
from randomizer.Patching.FairyPlacer import PlaceFairies
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.ItemRando import place_randomized_items
from randomizer.Patching.KasplatLocationRando import randomize_kasplat_locations
from randomizer.Patching.KongRando import apply_kongrando_cosmetic
from randomizer.Patching.MiscSetupChanges import randomize_setup, updateRandomSwitches
from randomizer.Patching.MoveLocationRando import place_pregiven_moves, randomize_moves
from randomizer.Patching.Patcher import LocalROM, load_base_rom
from randomizer.Patching.PhaseRando import randomize_helm, randomize_krool
from randomizer.Patching.PriceRando import randomize_prices
from randomizer.Patching.PuzzleRando import randomize_puzzles, shortenCastleMinecart
from randomizer.Patching.ShopRandomizer import ApplyShopRandomizer
from randomizer.Patching.UpdateHints import PushHints, replaceIngameText, wipeHints

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def patching_response(spoiler):
    """Apply the patch data to the ROM in the local server to be returned to the client."""
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()

    # Write date to ROM for debugging purposes
    from datetime import datetime

    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    temp_json = json.loads(spoiler.json)
    temp_json["Settings"]["Generation Timestamp"] = dt
    spoiler.json = json.dumps(temp_json, indent=4)
    LocalROM().seek(0x1FFF200)
    LocalROM().writeBytes(dt.encode("ascii"))
    # Initialize Text Changes
    spoiler.text_changes = {}

    # Starting index for our settings
    sav = spoiler.settings.rom_data

    # Shuffle Levels
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        LocalROM().seek(sav + 0)
        LocalROM().write(1)

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
            LocalROM().seek(sav + 1 + order)
            LocalROM().write(vanilla_lobby_exit_order.index(spoiler.shuffled_exit_data[int(level)].reverse))
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
                LocalROM().seek(sav + 0x01E + order)
                LocalROM().writeMultipleBytes(key_mapping[int(new_world)], 2)
                order += 2
        else:
            for key in key_mapping:
                LocalROM().seek(sav + 0x1E + order)
                LocalROM().writeMultipleBytes(key_mapping[key], 2)
                order += 2

    # Color Banana Requirements
    order = 0
    for count in spoiler.settings.BossBananas:
        LocalROM().seek(sav + 0x008 + order)
        LocalROM().writeMultipleBytes(count, 2)
        order += 2

    # Golden Banana Requirements
    order = 0
    for count in spoiler.settings.EntryGBs:
        LocalROM().seek(sav + 0x016 + order)
        LocalROM().writeMultipleBytes(count, 1)
        order += 1

    # Unlock All Kongs
    if spoiler.settings.starting_kongs_count == 5:
        LocalROM().seek(sav + 0x02C)
        LocalROM().write(0x1F)
    else:
        bin_value = 0
        for x in spoiler.settings.starting_kong_list:
            bin_value |= 1 << x
        LocalROM().seek(sav + 0x02C)
        LocalROM().write(bin_value)

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
        BooleanProperties(spoiler.settings.open_levels, 0x137),  # Open Levels
        BooleanProperties(spoiler.settings.shorten_boss, 0x13B),  # Shorten Boss Fights
        BooleanProperties(spoiler.settings.fast_warps, 0x13A),  # Fast Warps
        BooleanProperties(spoiler.settings.high_req, 0x179),  # Remove High Requirements
        BooleanProperties(spoiler.settings.fast_gbs, 0x17A),  # Fast GBs
        BooleanProperties(spoiler.settings.auto_keys, 0x15B),  # Auto-Turn Keys
        BooleanProperties(spoiler.settings.tns_location_rando, 0x10E),  # T&S Portal Location Rando
        BooleanProperties(spoiler.settings.cb_rando, 0x10B),  # Remove Rock Bunch
        BooleanProperties(spoiler.settings.wrinkly_location_rando or spoiler.settings.remove_wrinkly_puzzles, 0x11F),  # Wrinkly Rando
        BooleanProperties(spoiler.settings.helm_hurry, 0xAE),  # Helm Hurry
        BooleanProperties(spoiler.settings.hard_enemies, 0x116),  # Hard Enemies
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
            LocalROM().seek(sav + prop.offset)
            LocalROM().write(prop.target)

    # Fast Hideout
    LocalROM().seek(sav + 0x031)
    # The HelmSetting enum is indexed to allow this.
    LocalROM().write(int(spoiler.settings.helm_setting))

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
        LocalROM().seek(sav + 0x4C)
        LocalROM().write(door_checks[spoiler.settings.crown_door_item])
        LocalROM().seek(sav + 0x4D)
        LocalROM().write(spoiler.settings.crown_door_item_count)
    if spoiler.settings.coin_door_item in door_checks.keys():
        LocalROM().seek(sav + 0x4E)
        LocalROM().write(door_checks[spoiler.settings.coin_door_item])
        LocalROM().seek(sav + 0x4F)
        LocalROM().write(spoiler.settings.coin_door_item_count)

    # Camera unlocked
    given_moves = []
    if spoiler.settings.shockwave_status == ShockwaveStatus.start_with:
        given_moves.extend([39, 40])  # 39 = Camera, 40 = Shockwave
    move_bitfields = [0] * 6
    for move in given_moves:
        offset = int(move >> 3)
        check = int(move % 8)
        move_bitfields[offset] |= 0x80 >> check
    for offset, value in enumerate(move_bitfields):
        LocalROM().seek(sav + 0xD5 + offset)
        LocalROM().writeMultipleBytes(value, 1)

    # Free Trade Agreement
    if spoiler.settings.free_trade_items:
        LocalROM().seek(sav + 0x113)
        old = int.from_bytes(LocalROM().readBytes(1), "big")
        LocalROM().seek(sav + 0x113)
        LocalROM().write(old | 1)
    if spoiler.settings.free_trade_blueprints:
        LocalROM().seek(sav + 0x113)
        old = int.from_bytes(LocalROM().readBytes(1), "big")
        LocalROM().seek(sav + 0x113)
        LocalROM().write(old | 2)
    # Quality of Life
    if spoiler.settings.quality_of_life:
        enabled_qol = spoiler.settings.misc_changes_selected.copy()
        if len(enabled_qol) == 0:
            for item in QoLSelector:
                enabled_qol.append(MiscChangesSelected[item["value"]])
        write_data = [0] * 3
        for item in QoLSelector:
            if MiscChangesSelected[item["value"]] in enabled_qol and item["shift"] >= 0:
                offset = int(item["shift"] >> 3)
                check = int(item["shift"] % 8)
                write_data[offset] |= 0x80 >> check
        LocalROM().seek(sav + 0x0B0)
        for byte_data in write_data:
            LocalROM().writeMultipleBytes(byte_data, 1)

    # Damage amount
    damage_multipliers = {
        DamageAmount.default: 1,
        DamageAmount.double: 2,
        DamageAmount.quad: 4,
        DamageAmount.ohko: 12,
    }
    LocalROM().seek(sav + 0x0A5)
    LocalROM().write(damage_multipliers[spoiler.settings.damage_amount])

    # Microhints
    LocalROM().seek(sav + 0x102)
    # The MicrohintsEnabled enum is indexed to allow this.
    LocalROM().write(int(spoiler.settings.microhints_enabled))

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
    LocalROM().seek(sav + 0xE2)
    for bonus in helm_hurry_bonuses:
        if bonus < 0:
            bonus += 65536
        LocalROM().writeMultipleBytes(bonus, 2)

    # Activate Bananaports
    LocalROM().seek(sav + 0x138)
    # The ActivateAllBananaports enum is indexed to allow this.
    LocalROM().write(int(spoiler.settings.activate_all_bananaports))

    # Fast GBs - Change jetpac text
    if spoiler.settings.fast_gbs:
        cranky_index = 8
        data = {"textbox_index": 2, "mode": "replace", "search": "5000", "target": "2500"}
        if cranky_index in spoiler.text_changes:
            spoiler.text_changes[8].append(data)
        else:
            spoiler.text_changes[8] = [data]

    if spoiler.settings.hard_bosses:
        # KKO Phase Order
        for phase_slot in range(3):
            LocalROM().seek(sav + 0x17B + phase_slot)
            LocalROM().write(spoiler.settings.kko_phase_order[phase_slot])
        # Random Toe Sequence
        LocalROM().seek(sav + 0x41)
        LocalROM().write(1)
        for slot in range(10):
            LocalROM().seek(sav + 0x37 + slot)
            LocalROM().write(spoiler.settings.toe_order[slot])

    # Win Condition
    LocalROM().seek(sav + 0x11D)
    # The WinCondition enum is indexed to allow this.
    LocalROM().write(int(spoiler.settings.win_condition))

    # Mill Levers
    if spoiler.settings.mill_levers[0] > 0:
        mill_text = ""
        for x in range(5):
            LocalROM().seek(sav + 0xD0 + x)
            LocalROM().write(spoiler.settings.mill_levers[x])
            if spoiler.settings.mill_levers[x] > 0:
                mill_text += str(spoiler.settings.mill_levers[x])
        # Change default wrinkly hint
        if spoiler.settings.wrinkly_hints == WrinklyHints.off:
            if spoiler.settings.fast_gbs or spoiler.settings.puzzle_rando:
                wrinkly_index = 41
                data = {"textbox_index": 21, "mode": "replace", "search": "21132", "target": mill_text}
                if wrinkly_index in spoiler.text_changes:
                    spoiler.text_changes[41].append(data)
                else:
                    spoiler.text_changes[41] = [data]

    # Crypt Levers
    if spoiler.settings.crypt_levers[0] > 0:
        for xi, x in enumerate(spoiler.settings.crypt_levers):
            LocalROM().seek(sav + 0xCD + xi)
            LocalROM().write(x)

    keys_turned_in = [0, 1, 2, 3, 4, 5, 6, 7]
    if len(spoiler.settings.krool_keys_required) > 0:
        for key in spoiler.settings.krool_keys_required:
            key_index = key - 4
            if key_index in keys_turned_in:
                keys_turned_in.remove(key_index)
    key_bitfield = 0
    for key in keys_turned_in:
        key_bitfield = key_bitfield | (1 << key)
    LocalROM().seek(sav + 0x127)
    LocalROM().write(key_bitfield)

    if spoiler.settings.medal_requirement != 15:
        LocalROM().seek(sav + 0x150)
        LocalROM().write(spoiler.settings.medal_requirement)

    if spoiler.settings.rareware_gb_fairies != 20:
        LocalROM().seek(sav + 0x36)
        LocalROM().write(spoiler.settings.rareware_gb_fairies)

    if spoiler.settings.medal_cb_req != 75:
        LocalROM().seek(sav + 0x112)
        LocalROM().write(spoiler.settings.medal_cb_req)

    if len(spoiler.settings.enemies_selected) == 0 and (spoiler.settings.enemy_rando or spoiler.settings.crown_enemy_rando != CrownEnemyRando.off):
        lst = []
        for enemy in EnemySelector:
            lst.append(Enemies[enemy["value"]])
        spoiler.settings.enemies_selected = lst

    if spoiler.settings.random_starting_region:
        LocalROM().seek(sav + 0x10C)
        LocalROM().write(spoiler.settings.starting_region["map"])
        LocalROM().write(spoiler.settings.starting_region["exit"])
    if spoiler.settings.alter_switch_allocation:
        LocalROM().seek(sav + 0x103)
        LocalROM().write(1)
        for x in range(7):
            LocalROM().seek(sav + 0x104 + x)
            LocalROM().write(spoiler.settings.switch_allocation[x])

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
    PlaceFairies(spoiler)
    filterEntranceType()
    replaceIngameText(spoiler)
    updateRandomSwitches(spoiler)  # Has to be after all setup changes that may alter the item type of slam switches

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        wipeHints()
    PushHints(spoiler)

    writeBootMessages()
    enableSpiderText(spoiler)
    shortenCastleMinecart(spoiler)

    updateMillLeverTexture(spoiler.settings)
    updateCryptLeverTexture(spoiler.settings)
    applyHelmDoorCosmetics(spoiler.settings)

    # D-Pad Display
    LocalROM().seek(sav + 0x139)
    # The DPadDisplays enum is indexed to allow this.
    LocalROM().write(int(spoiler.settings.dpad_display))

    # Apply Hash
    order = 0
    for count in spoiler.settings.seed_hash:
        LocalROM().seek(sav + 0x129 + order)
        LocalROM().write(count)
        order += 1

    # Write the LocalROM.rom bytesIo to a file
    with open("patch.z64", "wb") as f:
        f.write(LocalROM().rom.getvalue())

    import pyxdelta

    pyxdelta.run("dk64.z64", "patch.z64", "patch.xdelta")
    # Read the patch file
    with open("patch.xdelta", "rb") as f:
        patch = f.read()
    # Delete the patch.z64 file
    os.remove("patch.z64")
    os.remove("patch.xdelta")
    load_base_rom()
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
