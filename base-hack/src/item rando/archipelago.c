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

ROM_DATA static archipelago_data ap_info;
ROM_DATA static char main_title[0x30];
ROM_DATA static char sub_title[0x30];

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

void handleSentItem(void) {
    // New generic packet-based approach
    // Python sends an ap_item_packet struct with all giveItem parameters
    ap_item_packet *packet = (ap_item_packet*)&ap_info.fed_item;
    
    // Unpack config flags into giveItemConfig struct
    giveItemConfig config = {
        .display_item_text = (packet->config_flags & 0x01) ? 1 : 0,
        .apply_helm_hurry = (packet->config_flags & 0x02) ? 1 : 0,
        .give_coins = (packet->config_flags & 0x04) ? 1 : 0,
        .apply_ice_trap = (packet->config_flags & 0x08) ? 1 : 0,
        .force_display_item_text = (packet->config_flags & 0x10) ? 1 : 0,
    };
    
    // Special handling for certain item types
    requirement_item item_type = (requirement_item)packet->item_type;
    
    switch (item_type) {
        case REQITEM_GOLDENBANANA:
            // GB has its own function
            giveGB();
            break;
        case REQITEM_ICETRAP:
            // Ice traps use kong field as trap_type
            sendTrap((ICE_TRAP_TYPES)packet->kong);
            break;
        case REQITEM_MOVE:
            // Special moves (item_type=2) can use direct bitfield manipulation for speed
            // but we'll keep giveItem for consistency
            giveItem(item_type, packet->level, packet->kong, config);
            break;
        default:
            // All other items use the generic giveItem function
            giveItem(item_type, packet->level, packet->kong, config);
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

int canReceiveShopkeeperItem(void) {
    if (inShop(CurrentMap, 1)) {
        return 0;
    }
    return canReceiveItem();
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
            text_overlay_data[vacant_spot].string = (char*)&main_title;
            dk_memcpy(text_overlay_data[vacant_spot].string, &ap_info.fed_string, 0x21);
            ap_info.fed_string[0] = 0;
            if (ap_info.fed_subtitle[0]) {
                // Subtitle
                text_overlay_data[vacant_spot].subtitle = (char*)&sub_title;
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
    ap_info.can_receive_shopkeeper = canReceiveShopkeeperItem();
}

void sendDeath(void) {
    if (isAPEnabled()) {
        if (!isActorLoaded(NEWACTOR_KOPDUMMY)) {
            ap_info.send_death = 1;
        }
    }
}

ROM_DATA static char *ap_strings[] = {
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