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

static archipelago_data ap_info;
static char main_title[0x30];
static char sub_title[0x30];

int isAPEnabled(void) {
    if (Rando.rom_flags.archipelago) {
        return 1;
    }
    return 0;
}

void initAP(void) {
    if (isAPEnabled()) {
        APData = &ap_info;
        ap_info.text_timer = 0x82;
        ap_info.start_flag = FLAG_ENEMY_KILLED_0 + 16;
        if (Rando.enemy_item_rando) {
            ap_info.start_flag += ENEMIES_TOTAL;
        }
        ap_info.tag_kong = -1;
    }
}

void initAPCounter(void) {
    if (isAPEnabled()) {
        int counter = 0;
        for (int i = 0; i < 16; i++) {
            counter <<= 1;
            if (checkFlag((ap_info.start_flag - 16) + i, FLAGTYPE_PERMANENT)) {
                counter += 1;
            }
        }
        ap_info.counter = counter;
    }
}

void saveAPCounter(void) {
    if (isAPEnabled()) {
        int counter = ap_info.counter;
        for (int i = 0; i < 16; i++) {
            int state = counter & 1;
            setFlag((ap_info.start_flag - 1) - i, state, FLAGTYPE_PERMANENT);
            counter >>= 1;
        }
    }
}

void handleSentItem(void) {
    archipelago_items FedItem = ap_info.fed_item;
    int check_count = -1;
    int check_start_flag = -1;
    int i = 0;
    unsigned char *file_data = 0;
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
            file_data = &Rando.crowns_in_file[0];
        case TRANSFER_ITEM_PEARL:
            if (check_count == -1) {
                check_count = 5;
                check_start_flag = FLAG_PEARL_0_COLLECTED;
                file_data = &Rando.pearls_in_file;
            }
        case TRANSFER_ITEM_MEDAL:
            if (check_count == -1) {
                check_count = 40;
                if (Rando.isles_cb_rando) {
                    check_count = 45;
                }
                check_start_flag = FLAG_MEDAL_JAPES_DK;
                file_data = &Rando.medals_in_file[0];
            }
        case TRANSFER_ITEM_FAIRY:
            {
                if (check_count == -1) {
                    check_count = 20;
                    check_start_flag = FLAG_FAIRY_1;
                    file_data = &Rando.fairies_in_file[0];
                }
                for (int i = 0; i < check_count; i++) {
                    int offset = i >> 3;
                    int shift = i & 7;
                    if ((file_data[offset] & (1 << shift)) == 0) {
                        if (!checkFlagDuplicate(check_start_flag + i, FLAGTYPE_PERMANENT)) {
                            setFlagDuplicate(check_start_flag + i, 1, FLAGTYPE_PERMANENT);
                            return;
                        }
                    }
                    if ((i == 39) && (FedItem == TRANSFER_ITEM_MEDAL)) {
                        check_start_flag = FLAG_MEDAL_ISLES_DK - 40;
                    }
                }
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
        case TRANSFER_ITEM_RAINBOWCOIN:
            for (int i = 0; i < 5; i++) {
                MovesBase[i].coins += 5;
            }
            break;
        case TRANSFER_ITEM_FAKEITEM:
            queueIceTrap(ICETRAP_BUBBLE);
            break;
        case TRANSFER_ITEM_FAKEITEM_SLOW:
            queueIceTrap(ICETRAP_SLOWED);
            break;
        case TRANSFER_ITEM_FAKEITEM_REVERSE:
            queueIceTrap(ICETRAP_REVERSECONTROLS);
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
    if (ap_info.connection > 0) {
        ap_info.connection -= 1;
    }
    if ((TBVoidByte & 3) || (!canReceiveItem())) {
        // Paused
        if (ap_info.safety_text_timer == 0) {
            ap_info.safety_text_timer = 5; // Block text going through 
        }
    } else {
        if (ap_info.safety_text_timer > 0) {
            ap_info.safety_text_timer--;
        }
    }
    if (canReceiveItem()) {
        if (ap_info.fed_item != TRANSFER_ITEM_NULL) {
            handleSentItem();
            ap_info.fed_item = TRANSFER_ITEM_NULL;
        }
        if (ap_info.fed_string[0] != 0) {
            int vacant_spot = spawnItemOverlay(PURCHASE_ARCHIPELAGO, 0, 1, 1);
            if (vacant_spot == -1) {
                return;
            }
            ap_info.safety_text_timer = ap_info.text_timer + 50;
            // Main Title
            text_overlay_data[vacant_spot].string = &main_title;
            dk_memcpy(text_overlay_data[vacant_spot].string, &ap_info.fed_string, 0x21);
            ap_info.fed_string[0] = 0;
            if (ap_info.fed_subtitle[0]) {
                // Subtitle
                text_overlay_data[vacant_spot].subtitle = &sub_title;
                dk_memcpy(text_overlay_data[vacant_spot].subtitle, &ap_info.fed_subtitle, 0x21);
                ap_info.fed_subtitle[0] = 0;
            }
        }
    }
    // Deathlink
    ap_info.can_die = canDie();
    if (CutsceneActive > 1) {
        ap_info.can_die = 0;
    }
    if (ap_info.can_die) {
        if (ap_info.receive_death) {
            cc_enabler_spawnkop();
            ap_info.receive_death = 0;
        }
    }
    // Tag Link
    ap_info.can_tag = getTAState();
    if (ap_info.tag_kong > -1) {
        if (ap_info.tag_kong < 5) {
            changeKong(ap_info.tag_kong);
        } else if (ap_info.tag_kong == 5) {
            int kong = 5;
            while (kong > 4) {
                kong = getRNGLower31() & 7;
                if (!hasAccessToKong(kong)) {
                    kong = 5;
                }
            }
            changeKong(kong);
        }
        ap_info.tag_kong = -1;
    }

}

int canDie(void) {
    // Check if the spawn kop CC effect can be triggered to simulate death without issues
    if(ObjectModel2Timer < 31){
        return 0;
    }
    if(!cc_allower_generic()){
        // No cc effects in general would be allowed
        return 0;
    }
    int level = levelIndexMapping[CurrentMap];
    if(level == LEVEL_BONUS || level == LEVEL_SHARED){
        // In a bonus/shared map
        return 0;
    }
    if(!cc_allower_spawnkop()){
        // This cc effect is already active or a transition isn't quite finished yet
        return 0;
    }
    if ((TBVoidByte & 0x30) == 0) {
        // In a tag barrel. Kops hate this one trick.
        return 0;
    }
    return 1;
}

void sendDeath(void) {
    if (isAPEnabled()) {
        if (!isActorLoaded(CUSTOM_ACTORS_START + NEWACTOR_KOPDUMMY)) {
            ap_info.send_death = 1;
        }
    }
}

int isFlagAPItem(int flag) {
    if (isAPEnabled()) {
        return isFlagInRange(flag, ap_info.start_flag, 1000 - 16);
    }
    return 0;
}

static char *ap_strings[] = {
    "APCLIENT CONNECTED",
    "APCLIENT DISCONNECTED"
};

Gfx *displayAPConnection(Gfx *dl) {
    if (isAPEnabled()) {
        int index = 1;
        if (ap_info.connection > 0) {
            index = 0;
        }
        dl = drawPixelTextContainer(dl, 15, 215, ap_strings[index], 0xFF, 0xFF, 0xFF, 0xFF, 1);
    }
    return dl;
}