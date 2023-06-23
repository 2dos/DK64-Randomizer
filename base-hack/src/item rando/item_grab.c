/**
 * @file item_grab.c
 * @author Ballaam
 * @brief Item Rando elements which pertain to grabbing items
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define BANANA_MEDAL_ITEM_COUNT 17 // Discount nothing item

#define MEDALITEM_GB 0
#define MEDALITEM_BP 1
#define MEDALITEM_KEY 2
#define MEDALITEM_CROWN 3
#define MEDALITEM_SPECIALCOIN 4
#define MEDALITEM_MEDAL 5
#define MEDALITEM_CRANKY 6
#define MEDALITEM_FUNKY 7
#define MEDALITEM_CANDY 8
#define MEDALITEM_TRAINING 9
#define MEDALITEM_BFI 10
#define MEDALITEM_KONG 11
#define MEDALITEM_BEAN 12
#define MEDALITEM_PEARL 13
#define MEDALITEM_FAIRY 14
#define MEDALITEM_RAINBOW 15
#define MEDALITEM_FAKEITEM 16
#define MEDALITEM_JUNKORANGE 17
#define MEDALITEM_JUNKAMMO 18
#define MEDALITEM_JUNKCRYSTAL 19
#define MEDALITEM_JUNKMELON 20
#define MEDALITEM_NOTHING 21

void banana_medal_acquisition(int flag) {
    /**
     * @brief Acquire a banana medal, and handle the item acquired from it
     * 
     * @param flag Flag index of the banana medal
     */
    int item_type = getMedalItem(flag - FLAG_MEDAL_JAPES_DK);
    if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
        if (item_type != MEDALITEM_KEY) {
            setFlag(flag, 1, FLAGTYPE_PERMANENT);
        }
        int song = 0;
        void* sprite = 0;
        int sprite_index = -1;
        short flut_flag = flag;
        helm_hurry_items hh_item = HHITEM_NOTHING;
        updateFlag(FLAGTYPE_PERMANENT, (short*)&flut_flag, (void*)0, -1);
        switch (item_type) {
            case MEDALITEM_GB:
                giveGB(getKong(0), getWorld(CurrentMap, 1));
                song = 18; // GB/Key Get
                sprite_index = 0x3B;
                break;
            case MEDALITEM_BP:
                {
                    song = 69; // BP Get
                    int bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
                    int character_val = getKong(0);
                    if (character_val > 4) {
                        character_val = 0;
                    }
                    sprite_index = bp_sprites[character_val];
                }
                break;
            case MEDALITEM_KEY:
                {
                    // Display key text
                    int key_bitfield = 0;
                    for (int i = 0; i < 8; i++) {
                        if (checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) {
                            key_bitfield |= (1 << i);
                        }
                    }
                    setFlag(flag, 1, FLAGTYPE_PERMANENT);
                    int spawned = 0;
                    for (int i = 0; i < 8; i++) {
                        if ((checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) && ((key_bitfield & (1 << i)) == 0)) {
                            if (!spawned) {
                                spawnItemOverlay(5, 0, getKeyFlag(i), 0);
                                spawned = 1;
                            }
                        }
                    }
                    auto_turn_keys();
                    song = 18; // GB/Key Get
                    sprite_index = 0x8A;
                    hh_item = HHITEM_KEY;
                }
                break;
            case MEDALITEM_CROWN:
                song = 0x97; // Banana Medal Get
                sprite_index = 0x8B;
                hh_item = HHITEM_CROWN;
                break;
            case MEDALITEM_SPECIALCOIN:
                song = 22; // Company Coin Get
                if (flut_flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
                    // Nintendo Coin
                    sprite_index = 0x8D;
                } else {
                    // Rareware Coin
                    sprite_index = 0x8C;
                }
                hh_item = HHITEM_COMPANYCOIN;
                break;
            case MEDALITEM_MEDAL:
                song = 0x97; // Banana Medal Get
                sprite_index = 0x3C;
                hh_item = HHITEM_MEDAL;
                break;
            case MEDALITEM_CRANKY:
                song = 115; // Gun Get
                sprite_index = 0x94;
                hh_item = HHITEM_MOVE;
                break;
            case MEDALITEM_FUNKY:
                song = 115; // Gun Get
                sprite_index = 0x96;
                hh_item = HHITEM_MOVE;
                break;
            case MEDALITEM_CANDY:
                song = 115; // Gun Get
                sprite_index = 0x93;
                hh_item = HHITEM_MOVE;
                break;
            case MEDALITEM_TRAINING:
                song = 115; // Gun Get
                sprite_index = 0x94;
                hh_item = HHITEM_MOVE;
                break;
            case MEDALITEM_BFI:
                song = 115; // Gun Get
                sprite_index = 0x3A;
                hh_item = HHITEM_MOVE;
                break;
            case MEDALITEM_KONG:
                {
                    int kong = -1;
                    for (int i = 0; i < 5; i++) {
                        if (flut_flag == kong_flags[i]) {
                            kong = i;
                        }
                    }
                    int kong_songs[] = {11, 10, 12, 13, 9};
                    if ((kong >= 0) && (kong < 5)) {
                        song = kong_songs[kong];
                        sprite_index = 0xA9 + kong;
                    }
                    refreshItemVisibility();
                }
                break;
            case MEDALITEM_BEAN:
                song = 147; // Bean Get
                sprite = &bean_sprite;
                hh_item = HHITEM_BEAN;
                break;
            case MEDALITEM_PEARL:
                song = 128; // Pearl Get
                sprite = &pearl_sprite;
                hh_item = HHITEM_PEARL;
                break;
            case MEDALITEM_FAIRY:
                song = 46; // Fairy Tick
                sprite_index = 0x89;
                hh_item = HHITEM_FAIRY;
                break;
            case MEDALITEM_RAINBOW:
                giveRainbowCoin();
                song = 145; // Rainbow Coin Get
                sprite_index = 0xA0;
                hh_item = HHITEM_RAINBOWCOIN;
                break;
            case MEDALITEM_FAKEITEM:
                queueIceTrap();
                sprite_index = 0x92;
                hh_item = HHITEM_FAKEITEM;
                break;
            case MEDALITEM_JUNKAMMO:
                giveAmmo();
                sprite_index = 0x48;
                break;
            case MEDALITEM_JUNKCRYSTAL:
                giveCrystal();
                song = 35;
                sprite_index = 0x3A;
                break;
            case MEDALITEM_JUNKMELON:
                giveMelon();
                sprite_index = 0x46;
                song = 33;
                break;
            case MEDALITEM_JUNKORANGE:
                giveOrange();
                sprite_index = 0x2C;
                break;
            case MEDALITEM_NOTHING:
                sprite_index = 0x8E;
                break;
        }
        if (song != 0) {
            playSFX(0xF2);
            playSong(song, 0x3F800000);
        }
        if (sprite == 0) {
            if (sprite_index == -1) {
                sprite_index = 0x3B;
            }
            sprite = sprite_table[sprite_index];
        }
        if (sprite) {
            unkSpriteRenderFunc(200);
            unkSpriteRenderFunc_0();
            loadSpriteFunction(0x8071EFDC);
            displaySpriteAtXYZ(sprite, 0x3F800000, 160.0f, 120.0f, -10.0f);
        }
        if (hh_item != HHITEM_NOTHING) {
            addHelmTime(hh_item, 1);
        }
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 0x3F800000, 160.0f, 120.0f, -10.0f);
    }
}

static unsigned char key_timer = 0;
static unsigned char key_index = 0;
static char key_text[] = "KEY 0";
static unsigned char old_keys = 0;

void keyGrabHook(int song, int vol) {
    /**
     * @brief Hook for grabbing a key
     */

    playSong(song, vol);
    int val = 0;
    for (int i = 0; i < 8; i++) {
        if (checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) {
            val |= (1 << i);
        }
    }
    old_keys = val;
}

int getFlagIndex_Corrected(int start, int level) {
    /**
     * @brief Get a corrected flag index, which will convert Rambi/Enguarde into the kong who entered the transformation crate
     * 
     * @param start Start flag index
     * @param level Level Index
     * 
     * @return New flag index
     */
    return start + (5 * level) + getKong(0);
}

void collectKey(void) {
    /**
     * @brief Collect a key, display the text and turn in keys
     */
    for (int i = 0; i < 8; i++) {
        if (checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) {
            if ((old_keys & (1 << i)) == 0) {
                spawnItemOverlay(5, 0, getKeyFlag(i), 0);
            }
        }
    }
    auto_turn_keys();
}

int itemGrabHook(int collectable_type, int obj_type, int is_homing) {
    /**
     * @brief Hook into the item grab function which is called at the point the flag is set. This is a little later
     * than the generic item grab function
     * 
     * @param collectable type of collectable
     * @param obj_type Object Model 2 Index
     * @param is_homing Is homing ammo crate
     * 
     * @return Collectable Offset
     */
    if (Rando.item_rando) {
        if (obj_type == 0x13C) {
            collectKey();
        } else {
            if (inBossMap(CurrentMap, 1, 0, 0)) {
                for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                    if (obj_type == acceptable_items[j]) {
                        setAction(0x41, 0, 0);
                    }
                }
            }
        }
        if (obj_type != 0x18D) {
            if (inBattleCrown(CurrentMap)) {
                for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                    if (obj_type == acceptable_items[j]) {
                        setAction(0x42, 0, 0);
                    }
                }
            }
        }
        if ((obj_type >= 0x257) && (obj_type <= 0x25B)) {
            // Kong Items
            refreshItemVisibility();
        }
    }
    return getCollectableOffset(collectable_type, obj_type, is_homing);
}

int* controlKeyText(int* dl) {
    /**
     * @brief Handle the key text to be displayed upon picking up a boss key
     * 
     * @param dl Display List address
     * 
     * @return New display list address
     */
    if (key_timer > 0) {
        int key_opacity = 255;
        if (key_timer < 10) {
            key_opacity = 25 * key_timer;
        } else if (key_timer > 90) {
            key_opacity = 25 * (100 - key_timer);
        }
        dl = initDisplayList(dl);
        *(unsigned int*)(dl++) = 0xFCFF97FF;
	    *(unsigned int*)(dl++) = 0xFF2CFE7F;
        *(unsigned int*)(dl++) = 0xFA000000;
        *(unsigned int*)(dl++) = 0xFFFFFF00 | key_opacity;
        dk_strFormat(key_text, "KEY %d", key_index + 1);
        dl = displayText(dl,1,640,750,key_text,0x80);
        key_timer -= 1;
    }
    return dl;
}

void giveFairyItem(int flag, int state, flagtypes type) {
    /**
     * @brief Handle acquisition of the item tied to a fairy
     * 
     * @param flag Flag index of the fairy
     * @param state Target state of the flag. AKA whether to set (1) or clear (0) the flag
     * @param type Flag Type
     */
    int model = getFairyModel(flag);
    int key_bitfield = 0;
    if (model == 0x69) {
        // GB
        int world = getWorld(CurrentMap, 1);
        if (world < 8) {
            giveGB(Character, world);
        }
    } else if (model == 0xF5) {
        // Key
        for (int i = 0; i < 8; i++) {
            if (checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) {
                key_bitfield |= (1 << i);
            }
        }
    } else if (model == 0x10F) {
        // Fake Item
        queueIceTrap();
    }
    setFlag(flag, state, type);
    if (model == 0xF5) {
        // Key - Post flag set
        int spawned = 0;
        for (int i = 0; i < 8; i++) {
            if ((checkFlagDuplicate(getKeyFlag(i), FLAGTYPE_PERMANENT)) && ((key_bitfield & (1 << i)) == 0)) {
                if (!spawned) {
                    spawnItemOverlay(5, 0, getKeyFlag(i), 0);
                    spawned = 1;
                }
            }
        }
        auto_turn_keys();
    }
}

static const unsigned char dance_skip_ban_maps[] = {
    MAP_AZTECBEETLE, // Aztec Beetle
    MAP_FACTORYCARRACE, // Factory Car Race
    MAP_GALLEONSEALRACE, // Galleon Seal Race
    MAP_CAVESBEETLERACE, // Caves Beetle
    MAP_CASTLECARRACE, // Castle Car Race
};

static const unsigned char dance_force_maps[] = {
    MAP_AZTECBEETLE, // Aztec Beetle
    MAP_FACTORYCARRACE, // Factory Car Race
    MAP_GALLEONSEALRACE, // Galleon Seal Race
    MAP_CAVESBEETLERACE, // Caves Beetle
    MAP_CASTLECARRACE, // Castle Car Race
};

int canDanceSkip(void) {
    /**
     * @brief Determine whether the player can dance skip an item
     * 
     * @return Dance Skip enabled
     */
    if (CurrentMap == MAP_GALLEONPUFFTOSS) {
        return 0;
    }
    if ((Player->yPos - Player->floor) >= 100.0f) {
        return 1;
    }
    if (Player->control_state == 99) {
        return 1;
    }
    if ((Player->grounded_bitfield & 4) && ((Player->water_floor - Player->floor) > 20.0f)) {
        return 1;
    }
    if (Rando.quality_of_life.dance_skip) {
        int is_banned_map = inBattleCrown(CurrentMap);
        if (inBossMap(CurrentMap, 1, 0, 0)) {
            is_banned_map = 1;
        }
        for (int i = 0; i < sizeof(dance_skip_ban_maps); i++) {
            if (dance_skip_ban_maps[i] == CurrentMap) {
                is_banned_map = 1;
            }
        }
        if (!is_banned_map) {
            return 1;
        }
    }
    return 0;
}

void forceDance(void) {
    for (int i = 0; i < sizeof(dance_force_maps); i++) {
        if (dance_force_maps[i] == CurrentMap) {
            setAction(0x29, 0, 0);
            return;
        }
    }    
}

void BalloonShoot(int item, int player, int change) {
    addHelmTime(HHITEM_CB, change);
    changeCollectableCount(item, player, change);
}

void getItem(int object_type) {
    /**
     * @brief Item Grab hook, at the point of touching the item, before the flag is set.
     * 
     * @param object_type Object Model 2 Type
     */
    float pickup_volume = 1-(0.3f * *(char*)(0x80745838));
    int song = -1;
    helm_hurry_items hh_item = HHITEM_NOTHING;
    int multiplier = 1;
    switch(object_type) {
        case 0x0A:
        case 0x0D:
        case 0x16:
        case 0x1E:
        case 0x1F:
        case 0x1CF:
        case 0x1D0:
            // CB Single
            playSound(0x2A0, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            hh_item = HHITEM_CB;
            break;
        case 0x2B:
        case 0x205:
        case 0x206:
        case 0x207:
        case 0x208:
            if (Rando.tag_anywhere) {
                hh_item = HHITEM_CB;
                multiplier = 5;
            }
            break;
        case 0x11:
        case 0x8F:
            // Homing Ammo Crate
            playSound(0x157, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x1C:
        case 0x1D:
        case 0x23:
        case 0x24:
        case 0x27:
            // Banana Coin
            playSong(23, *(int*)(&pickup_volume));
            break;
        case 0x48:
        case 0x28F:
            // Company Coin
            if (Rando.item_rando) {
                playSong(22, *(int*)(&pickup_volume));
            }
            hh_item = HHITEM_COMPANYCOIN;
            forceDance();
            break;
        case 0x56:
            // Orange
            playSound(0x147, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x57:
        case 0x25E:
            // Melon Slice
            playSong(0x2F, *(int*)(&pickup_volume));
            forceDance();
            break;
        case 0x59:
        case 0x5B:
        case 0x1F2:
        case 0x1F3:
        case 0x1F5:
        case 0x1F6:
            // Potion
            playSong(115, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            hh_item = HHITEM_MOVE;
            break;
        case 0x74:
        case 0x288:
            // GB
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            // hh_item = HHITEM_GB; // Ignored as it's handled in a separate case
            break;
        case 0x8E:
            // Crystal
            playSong(35, *(int*)(&pickup_volume));
            break;
        case 0x90:
            // Medal
            playSong(0x12, 0x3F800000);
            BananaMedalGet();
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            hh_item = HHITEM_MEDAL;
            break;
        case 0x98:
            // Film
            playSound(0x263, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0xB7:
            // Rainbow Coin
            playSong(0x91, *(int*)(&pickup_volume));
            hh_item = HHITEM_RAINBOWCOIN;
            forceDance();
            break;
        case 0xDD:
        case 0xDE:
        case 0xDF:
        case 0xE0:
        case 0xE1:
            // Blueprint
            playSong(69, *(int*)(&pickup_volume));
            forceDance();
            hh_item = HHITEM_BLUEPRINT;
            break;
        case 0xEC:
        case 0x1D2:
            // Race Coin
            playSong(32, *(int*)(&pickup_volume));
            break;
        case 0x13C:
            // Key
            keyGrabHook(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                unsigned char boss_list[] = {0x08, 0xC5, 0x9A, 0x6F, 0x53, 0xC4, 0xC7};
                int action = 0;
                for (int i = 0; i < sizeof(boss_list); i++) {
                    if (CurrentMap == boss_list[i]) {
                        action = 0x41; // Key Get
                    }
                }
                if (action == 0) {
                    action = 0x29; // GB Get
                }
                setAction(action, 0, 0);
            }
            hh_item = HHITEM_KEY;
            auto_turn_keys();
            break;
        case 0x18D:
            // Crown
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            CrownGet();
            hh_item = HHITEM_CROWN;
            break;
        case 0x198:
            // Bean
            playSong(147, 0x3F800000);
            hh_item = HHITEM_PEARL;
            forceDance();
            break;
        case 0x1B4:
            // Pearl
            {
                playSong(128, 0x3F800000);
                // if (CurrentMap == MAP_GALLEONTREASURECHEST) { // Treasure Chest
                //     int requirement = 5;
                //     if (Rando.fast_gbs) {
                //         requirement = 1;
                //     }
                //     int count = 0;
                //     for (int i = 0; i < 5; i++) {
                //         count += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, FLAGTYPE_PERMANENT);
                //     }
                //     if (count == (requirement - 1)) {
                //         playCutscene((void*)0, 1, 0);
                //     }
                // }
                hh_item = HHITEM_PEARL;
                forceDance();
            }
            break;
        case 0x1D1:
            // Coin Powerup
            playSound(0xAE, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x257:
            song = 11;
        case 0x258:
            if (song == -1) {
                song = 10;
            }
        case 0x259:
            if (song == -1) {
                song = 12;
            }
        case 0x25A:
            if (song == -1) {
                song = 13;
            }
        case 0x25B:
            if (song == -1) {
                song = 9;
            }
            if (song >= 0) {
                playSong(song, 0x3F800000);
            }
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            refreshItemVisibility();
            // hh_item = HHITEM_KONG; // Ignored as it's handled in a separate case
            break;
        case 0x25C:
            playSong(46, 0x3F800000);
            hh_item = HHITEM_FAIRY;
            forceDance();
            break;
        case 0x25D:
            // Fake Item
            forceDance();
            queueIceTrap();
            hh_item = HHITEM_FAKEITEM;
            break;
    }
    if (hh_item != HHITEM_NOTHING) {
        addHelmTime(hh_item, multiplier);
    }
}

int getObjectCollectability(int id, int unk1, int model2_type) {
    /**
     * @brief Determine whether the object is collectable or not
     * 
     * @param id Object ID
     * @param unk1 Unknown
     * @param model2_type Object Model 2 Type
     * 
     * @return Whether item is collectable or not
     */
    int index = indexOfNextObj(id);
    int* m2location = (int*)ObjectModel2Pointer;
    ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
    if (model2_type == 0x11) {
        // Homing
        return (MovesBase[(int)Character].weapon_bitfield & 3) == 3;
    } else if (model2_type == 0x8E) {
        // Crystal
        return crystalsUnlocked(Character);
    } else if (model2_type == 0x8F) {
        // Regular Crate
        return MovesBase[(int)Character].weapon_bitfield & 1;
    } else if (model2_type == 0x56) {
        // Orange
        if (CurrentMap == MAP_TBARREL_ORANGE) { // Orange Barrel
            return 1;
        }
        return checkFlagDuplicate(FLAG_TBARREL_ORANGE, FLAGTYPE_PERMANENT);
    } else if (model2_type == 0x90) {
        // Medal
        if (CurrentMap == MAP_HELM) {
            behaviour_data* behaviour = _object->behaviour_pointer;
            if (behaviour) {
                if (behaviour->unk_64 != 0xFF) {
                    return 0;
                }
            }
        }
    } else if (model2_type == 0x98) {
        // Film
        return checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT);
    }
    int collectable_state = _object->collectable_state;
    if (((collectable_state & 8) == 0) || (Player->new_kong == 2)) {
        if (((collectable_state & 2) == 0) || (Player->new_kong == 3)) {
            if (((collectable_state & 4) == 0) || (Player->new_kong == 5)) {
                if (((collectable_state & 0x10) == 0) || (Player->new_kong == 4)) {
                    if ((collectable_state & 1) && (Player->new_kong != 6)) {
                        return 0;
                    }
                    return 1;
                }
                return 0;
            }
            return 0;
        }
        return 0;
    }
    return 0;
}

int isCollectable(int type) {
    int player_index = FocusedPlayerIndex;
    int kong = -1;
    switch(type) {
        case 0xD: // DK Single
        case 0x1D: // DK Coin
        case 0x2B: // DK Bunch
            kong = KONG_DK;
        case 0xA: // Diddy Single
        case 0x24: // Diddy Coin
        case 0x208: // Diddy Bunch
            if (kong == -1) {
                kong = KONG_DIDDY;
            }
        case 0x1E: // Lanky Single
        case 0x23: // Lanky Coin
        case 0x205: // Lanky Bunch
            if (kong == -1) {
                kong = KONG_LANKY;
            }
        case 0x16: // Tiny Single
        case 0x1C: // Tiny Coin
        case 0x207: // Tiny Bunch
            if (kong == -1) {
                kong = KONG_TINY;
            }
        case 0x1F: // Chunky Single
        case 0x27: // Chunky Coin
        case 0x206: // Chunky Bunch
            if (kong == -1) {
                kong = KONG_CHUNKY;
            }
            if (kong > -1) {
                if (Rando.quality_of_life.rambi_enguarde_pickup) {
                    return SwapObject[player_index].player->new_kong == kong + 2;
                }
                return SwapObject[player_index].player->characterID == kong + 2;
            }
            return 1;
        case 0x11: // Homing Crate
            return (MovesBase[(int)Character].weapon_bitfield & 3) == 3;
        case 0x8E: // Crystal
            return SwapObject[player_index].player->unk_fairycam_bitfield & 2;
        case 0x8F: // Ammo Crate
            return MovesBase[(int)Character].weapon_bitfield & 1;
        case 0x98: // Film
            return checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT);
        case 0x56: // Oranges
            if (CurrentMap != MAP_TBARREL_ORANGE) {
                return checkFlagDuplicate(FLAG_TBARREL_ORANGE, FLAGTYPE_PERMANENT);
            }
    }
    return 1;
}

void handleModelTwoOpacity(short object_type, unsigned char* unk0, short* opacity) {
    if (!isCollectable(object_type)) {
        *unk0 = 0;
        if (*opacity > 100) {
            *opacity = 100;
        }
    }
}