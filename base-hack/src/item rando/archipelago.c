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
    }
}

void initAPCounter(void) {
    if (isAPEnabled()) {
        ap_info.counter = ReadFile(DATA_APCOUNTER, 0, 0, FileIndex);
    }
}

void saveAPCounter(void) {
    if (isAPEnabled()) {
        SaveToFile(DATA_APCOUNTER, 0, 0, FileIndex, ap_info.counter);
    }
}

void handleSentItem(void) {
    archipelago_items FedItem = ap_info.fed_item;
    switch (FedItem) {
        case TRANSFER_ITEM_GB:
            giveGB();
            break;
        case TRANSFER_ITEM_CROWN:
            giveItem(REQITEM_CROWN, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_PEARL:
            giveItem(REQITEM_PEARL, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_MEDAL:
            giveItem(REQITEM_PEARL, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_FAIRY:
            giveItem(REQITEM_FAIRY, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_KEY1:
        case TRANSFER_ITEM_KEY2:
        case TRANSFER_ITEM_KEY3:
        case TRANSFER_ITEM_KEY4:
        case TRANSFER_ITEM_KEY5:
        case TRANSFER_ITEM_KEY6:
        case TRANSFER_ITEM_KEY7:
        case TRANSFER_ITEM_KEY8:
            giveItem(REQITEM_KEY, FedItem - TRANSFER_ITEM_KEY1, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            auto_turn_keys();
            break;
        case TRANSFER_ITEM_RAINBOWCOIN:
            giveItem(REQITEM_RAINBOWCOIN, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1, .give_coins = 1});
            break;
        case TRANSFER_ITEM_FAKEITEM:
            queueIceTrap(ICETRAP_BUBBLE);
            giveItem(REQITEM_ICETRAP, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_FAKEITEM_SLOW:
            queueIceTrap(ICETRAP_SLOWED);
            giveItem(REQITEM_ICETRAP, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_FAKEITEM_REVERSE:
            queueIceTrap(ICETRAP_REVERSECONTROLS);
            giveItem(REQITEM_ICETRAP, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_JUNKITEM:
            applyDamageMask(0, 1);
            giveItem(REQITEM_JUNK, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
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
            giveItem(REQITEM_MOVE, 8, FedItem - TRANSFER_ITEM_BONGOS, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_COCONUT:
        case TRANSFER_ITEM_PEANUT:
        case TRANSFER_ITEM_GRAPE:
        case TRANSFER_ITEM_FEATHER:
        case TRANSFER_ITEM_PINEAPPLE:
            giveItem(REQITEM_MOVE, 4, FedItem - TRANSFER_ITEM_COCONUT, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_SLAMUPGRADE:
            giveSlamLevel();
            break;
        case TRANSFER_ITEM_HOMING:
            giveItem(REQITEM_MOVE, 5, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_SNIPER:
            giveItem(REQITEM_MOVE, 6, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_BELTUPGRADE:
            giveItem(REQITEM_MOVE, 7, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_INSTRUMENTUPGRADE:
            giveItem(REQITEM_MOVE, 9, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case TRANSFER_ITEM_CAMERA:
            setFlagMove(FLAG_ABILITY_CAMERA);
            break;
        case TRANSFER_ITEM_SHOCKWAVE:
            setFlagMove(FLAG_ABILITY_SHOCKWAVE);
            break;
        case TRANSFER_ITEM_CAMERASHOCKWAVECOMBO:
            setFlagMove(FLAG_ABILITY_CAMERA);
            setFlagMove(FLAG_ABILITY_SHOCKWAVE);
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
            int vacant_spot = spawnItemOverlay(REQITEM_AP, 0, 1, 1);
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
    ap_info.can_die = cc_allower_spawnkop();
    if (CutsceneActive > 1) {
        ap_info.can_die = 0;
    }
    if (ap_info.can_die) {
        if (ap_info.receive_death) {
            cc_enabler_spawnkop();
            ap_info.receive_death = 0;
        }
    }
}

void sendDeath(void) {
    if (isAPEnabled()) {
        if (!isActorLoaded(CUSTOM_ACTORS_START + NEWACTOR_KOPDUMMY)) {
            ap_info.send_death = 1;
        }
    }
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