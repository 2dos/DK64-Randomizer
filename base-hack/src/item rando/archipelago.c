/**
 * @file archipelago.c
 * @author Ballaam
 * @brief Functions related to Archipelago functionality
 * @version 0.1
 * @date 2023-03-28
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void handleSentItem(void) {
    int check_count = -1;
    int check_start_flag = -1;
    int check_flag_index = 0;
    switch (FedItem) {
        case TRANSFER_ITEM_GB:
            {
                int min_amount = 100;
                int min_kong = 0;
                int min_level = 0;
                for (int level = 0; level < 8; level++) {
                    for (int kong = 0; kong < 5; kong++) {
                        int count = MovesBase[kong].gb_count[level];
                        if (count < min_amount) {
                            min_amount = count;
                            min_kong = kong;
                            min_level = level;
                        }
                    }
                }
                giveGB(min_kong, min_level);
                break;
            }
        case TRANSFER_ITEM_CROWN:
            check_count = 10;
            check_start_flag = FLAG_CROWN_JAPES;
        case TRANSFER_ITEM_BP:
            if (check_count == -1) {
                check_count = 40;
                check_start_flag = FLAG_BP_JAPES_DK_HAS;
            }
        case TRANSFER_ITEM_PEARL:
            if (check_count == -1) {
                check_count = 5;
                check_start_flag = FLAG_PEARL_0_COLLECTED;
            }
        case TRANSFER_ITEM_MEDAL:
            if (check_count == -1) {
                check_count = 40;
                check_start_flag = FLAG_MEDAL_JAPES_DK;
            }
        case TRANSFER_ITEM_FAIRY:
            if (check_count == -1) {
                check_count = 20;
                check_start_flag = FLAG_FAIRY_1;
            }
            check_flag_index = 0;
            while (check_flag_index < check_count) {
                if (!checkFlagDuplicate(check_start_flag + check_flag_index, FLAGTYPE_PERMANENT)) {
                    setFlagDuplicate(check_start_flag + check_flag_index, 1, FLAGTYPE_PERMANENT);
                    return;
                }
                check_flag_index += 1;
            }
            break;
        case TRANSFER_ITEM_KEY1:
        case TRANSFER_ITEM_KEY2:
        case TRANSFER_ITEM_KEY3:
        case TRANSFER_ITEM_KEY4:
        case TRANSFER_ITEM_KEY5:
        case TRANSFER_ITEM_KEY6:
        case TRANSFER_ITEM_KEY7:
        case TRANSFER_ITEM_KEY8:
            setFlagDuplicate(normal_key_flags[FedItem - TRANSFER_ITEM_KEY1], 1, FLAGTYPE_PERMANENT);
            auto_turn_keys();
            break;
        case TRANSFER_ITEM_NINTENDOCOIN:
            setFlagDuplicate(FLAG_COLLECTABLE_NINTENDOCOIN, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_RAREWARECOIN:
            setFlagDuplicate(FLAG_COLLECTABLE_RAREWARECOIN, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_DK:
        case TRANSFER_ITEM_DIDDY:
        case TRANSFER_ITEM_LANKY:
        case TRANSFER_ITEM_TINY:
        case TRANSFER_ITEM_CHUNKY:
            setFlagDuplicate(kong_flags[FedItem - TRANSFER_ITEM_DK], 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_RAINBOWCOIN:
            for (int i = 0; i < 5; i++) {
                MovesBase[i].coins += 5;
            }
            break;
        case TRANSFER_ITEM_BEAN:
            setFlagDuplicate(FLAG_COLLECTABLE_BEAN, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_FAKEITEM:
            queueIceTrap(ICETRAP_BUBBLE); // For now, always make ice
            break;
        case TRANSFER_ITEM_JUNKITEM:
            applyDamageMask(0, 1);
            break;
        case TRANSFER_ITEM_BABOONBLAST:
        case TRANSFER_ITEM_STRONGKONG:
        case TRANSFER_ITEM_GORILLAGRAB:
        case TRANSFER_ITEM_CHIMPYCHARGE:
        case TRANSFER_ITEM_ROCKETBARREL:
        case TRANSFER_ITEM_SIMIANSPRING:
        case TRANSFER_ITEM_ORANGSTAND:
        case TRANSFER_ITEM_BABOONBALLOON:
        case TRANSFER_ITEM_ORANGSTANDSPRINT:
        case TRANSFER_ITEM_MINIMONKEY:
        case TRANSFER_ITEM_TWIRL:
        case TRANSFER_ITEM_MONKEYPORT:
        case TRANSFER_ITEM_HUNKYCHUNKY:
        case TRANSFER_ITEM_PRIMATEPUNCH:
        case TRANSFER_ITEM_GORILLAGONE:
            {
                int offset = FedItem - TRANSFER_ITEM_BABOONBLAST;
                int kong = offset / 3;
                int shift = 1 << (offset % 3);
                MovesBase[kong].special_moves |= shift;
                break;
            }
        case TRANSFER_ITEM_BONGOS:
        case TRANSFER_ITEM_GUITAR:
        case TRANSFER_ITEM_TROMBONE:
        case TRANSFER_ITEM_SAX:
        case TRANSFER_ITEM_TRIANGLE:
            MovesBase[FedItem - TRANSFER_ITEM_BONGOS].instrument_bitfield |= 1;
            if (CollectableBase.Melons < 2) {
                CollectableBase.Melons = 2;
                CollectableBase.Health = 8;
            }
            break;
        case TRANSFER_ITEM_COCONUT:
        case TRANSFER_ITEM_PEANUT:
        case TRANSFER_ITEM_GRAPE:
        case TRANSFER_ITEM_FEATHER:
        case TRANSFER_ITEM_PINEAPPLE:
            MovesBase[FedItem - TRANSFER_ITEM_COCONUT].weapon_bitfield |= 1;
            break;
        case TRANSFER_ITEM_SLAMUPGRADE:
            giveSlamLevel();
            break;
        case TRANSFER_ITEM_HOMING:
            for (int i = 0; i < 5; i++) {
                MovesBase[i].weapon_bitfield |= 2;
            }
            break;
        case TRANSFER_ITEM_SNIPER:
            for (int i = 0; i < 5; i++) {
                MovesBase[i].weapon_bitfield |= 4;
            }
            break;
        case TRANSFER_ITEM_BELTUPGRADE:
            {
                int belt_level = MovesBase[0].ammo_belt;
                if (belt_level < 2) {
                    for (int i = 0; i < 5; i++) {
                        MovesBase[i].ammo_belt = belt_level + 1;
                    }
                }
                break;
            }
        case TRANSFER_ITEM_INSTRUMENTUPGRADE:
            {
                int ins_level = 0;
                for (int i = 1; i < 4; i++) {
                    if (MovesBase[0].instrument_bitfield & (1 << i)) {
                        ins_level = i;
                    }
                }
                if (ins_level < 3) {
                    for (int i = 0; i < 5; i++) {
                        MovesBase[i].instrument_bitfield |= (1 << (ins_level + 1));
                    }
                }
                if (CollectableBase.Melons < 2) {
                    CollectableBase.Melons = 2;
                    CollectableBase.Health = 8;
                } else if (ins_level > 0) {
                    CollectableBase.Melons = 3;
                    CollectableBase.Health = 12;
                }
                break;
            }
        case TRANSFER_ITEM_CAMERA:
            setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_SHOCKWAVE:
            setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_CAMERASHOCKWAVECOMBO:
            setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, FLAGTYPE_PERMANENT);
            setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_DIVE:
            setFlagDuplicate(FLAG_TBARREL_DIVE, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_ORANGE:
            setFlagDuplicate(FLAG_TBARREL_ORANGE, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_BARREL:
            setFlagDuplicate(FLAG_TBARREL_BARREL, 1, FLAGTYPE_PERMANENT);
            break;
        case TRANSFER_ITEM_VINE:
            setFlagDuplicate(FLAG_TBARREL_VINE, 1, FLAGTYPE_PERMANENT);
            break;
        default:
        break;
    }
}

int canReceiveItem(void) {
    if (isGamemode(GAMEMODE_ADVENTURE, 1) || isGamemode(GAMEMODE_SNIDEGAMES, 1)) {
        if (LZFadeoutProgress == 0) {
            return 1;
        }
    }
    return 0;
}

void handleArchipelagoFeed(void) {
    if (canReceiveItem()) {
        if (FedItem != TRANSFER_ITEM_NULL) {
            handleSentItem();
            FedItem = TRANSFER_ITEM_NULL;
        }
    }
}

void handleArchipelagoString(void) {
    if (canReceiveItem()) {
        if (FedString[0] != 0) {
            int vacant_spot = spawnItemOverlay(8, 0, 1, 1);
            if (vacant_spot == -1) {
                return;
            }
            text_overlay_data[vacant_spot].string = dk_malloc(0x30);
            dk_memcpy(text_overlay_data[vacant_spot].string, &FedString[0], 0x21);
            FedString[0] = 0;
        }
    }
}