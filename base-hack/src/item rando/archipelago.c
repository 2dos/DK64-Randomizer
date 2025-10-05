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
        ap_info.tag_kong = -1;
        ap_info.deferred_cranky = 0;
        ap_info.deferred_funky = 0;
        ap_info.deferred_candy = 0;
        ap_info.deferred_snide = 0;
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

void sendTrap(ICE_TRAP_TYPES trap_type) {
    giveItem(REQITEM_ICETRAP, 0, trap_type, (giveItemConfig){.display_item_text = 0, .apply_ice_trap = 1});
}

static unsigned char ice_trap_feds[] = {
    TRANSFER_ITEM_FAKEITEM,
    TRANSFER_ITEM_FAKEITEM_REVERSE,
    TRANSFER_ITEM_FAKEITEM_SLOW,
    0, // Super Bubble
    TRANSFER_ITEM_FAKEITEM_DISABLEA,
    TRANSFER_ITEM_FAKEITEM_DISABLEB,
    TRANSFER_ITEM_FAKEITEM_DISABLEZ,
    TRANSFER_ITEM_FAKEITEM_DISABLECU,
    TRANSFER_ITEM_FAKEITEM_GETOUT,
    TRANSFER_ITEM_FAKEITEM_DRY,
    TRANSFER_ITEM_FAKEITEM_FLIP,
    TRANSFER_ITEM_FAKEITEM_ICEFLOOR,
    TRANSFER_ITEM_FAKEITEM_PAPER,
    0, // Non-Instant Slip Trap
    TRANSFER_ITEM_FAKEITEM_SLIP,
};

void handleSentItem(void) {
    archipelago_items FedItem = ap_info.fed_item;
    switch (FedItem) {
        case TRANSFER_ITEM_GB:
            giveGB();
            break;
        case TRANSFER_ITEM_RAINBOWCOIN:
            giveItem(REQITEM_RAINBOWCOIN, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1, .give_coins = 1});
            break;
        case TRANSFER_ITEM_FAKEITEM:
        case TRANSFER_ITEM_FAKEITEM_REVERSE:
        case TRANSFER_ITEM_FAKEITEM_SLOW:
        case TRANSFER_ITEM_FAKEITEM_DISABLEA:
        case TRANSFER_ITEM_FAKEITEM_DISABLEB:
        case TRANSFER_ITEM_FAKEITEM_DISABLEZ:
        case TRANSFER_ITEM_FAKEITEM_DISABLECU:
        case TRANSFER_ITEM_FAKEITEM_GETOUT:
        case TRANSFER_ITEM_FAKEITEM_DRY:
        case TRANSFER_ITEM_FAKEITEM_FLIP:
        case TRANSFER_ITEM_FAKEITEM_ICEFLOOR:
        case TRANSFER_ITEM_FAKEITEM_PAPER:
        case TRANSFER_ITEM_FAKEITEM_SLIP:
            for (int i = 0; i < sizeof(ice_trap_feds); i++) {
                if (ice_trap_feds[i] == FedItem) {
                    sendTrap(ICETRAP_BUBBLE + i);
                } 
            }
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
    }
}

void sendTrapLink(ICE_TRAP_TYPES trap_type) {
    if (isAPEnabled()) {
        ap_info.is_trapped = trap_type;
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
    // Trap link
    if (ap_info.sent_trap) {
        queueIceTrap(ap_info.sent_trap, 0);
        ap_info.sent_trap = 0;
    }
    // Helm Hurry item handling
    if (ap_info.helm_hurry_item) {
        addHelmTime(ap_info.helm_hurry_item, 1);
        ap_info.helm_hurry_item = 0;
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
        if (!isActorLoaded(NEWACTOR_KOPDUMMY)) {
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