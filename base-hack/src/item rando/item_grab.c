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

typedef enum MEDAL_ITEMS {
    /*  0 */ MEDALITEM_GB,
    /*  1 */ MEDALITEM_BP,
    /*  2 */ MEDALITEM_KEY,
    /*  3 */ MEDALITEM_CROWN,
    /*  4 */ MEDALITEM_SPECIALCOIN,
    /*  5 */ MEDALITEM_MEDAL,
    /*  6 */ MEDALITEM_CRANKY,
    /*  7 */ MEDALITEM_FUNKY,
    /*  8 */ MEDALITEM_CANDY,
    /*  9 */ MEDALITEM_TRAINING,
    /* 10 */ MEDALITEM_BFI,
    /* 11 */ MEDALITEM_KONG,
    /* 12 */ MEDALITEM_BEAN,
    /* 13 */ MEDALITEM_PEARL,
    /* 14 */ MEDALITEM_FAIRY,
    /* 15 */ MEDALITEM_RAINBOW,
    /* 16 */ MEDALITEM_ICETRAP_BUBBLE,
    /* 17 */ MEDALITEM_JUNKMELON,
    /* 18 */ MEDALITEM_CRANKYITEM,
    /* 19 */ MEDALITEM_FUNKYITEM,
    /* 20 */ MEDALITEM_CANDYITEM,
    /* 21 */ MEDALITEM_SNIDEITEM,
    /* 22 */ MEDALITEM_NOTHING,
    /* 23 */ MEDALITEM_ICETRAP_REVERSE,
    /* 24 */ MEDALITEM_ICETRAP_SLOW,
    /* 25 */ MEDALITEM_HINT,
} MEDAL_ITEMS;

typedef struct item_info {
    /* 0x000 */ songs song;
    /* 0x004 */ int sprite;
    /* 0x008 */ helm_hurry_items helm_hurry_item;
    /* 0x00C */ short fairy_model;
    /* 0x00E */ char pad_e;
    /* 0x00F */ char pad_f;
} item_info;

static const unsigned char bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
static const unsigned char instrument_songs[] = {SONG_BONGOS, SONG_GUITAR, SONG_TROMBONE, SONG_SAXOPHONE, SONG_TRIANGLE};

#define MODEL_GENERIC_POTION 0x2001
#define MODEL_GENERIC_KONG 0x2002

static const item_info item_detection_data[] = {
    {.song = SONG_GBGET, .sprite = 0x3B, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = 0x69}, // GB - Handled by a separate function
    {.song = SONG_BLUEPRINTGET, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = -1}, // BP
    {.song = SONG_GBGET, .sprite = 0x8A, .helm_hurry_item = HHITEM_KEY, .fairy_model = 0xF5}, // Key
    {.song = SONG_BANANAMEDALGET, .sprite = 0x8B, .helm_hurry_item = HHITEM_CROWN, .fairy_model = 0xF4}, // Crown
    {.song = SONG_COMPANYCOINGET, .sprite = -1, .helm_hurry_item = HHITEM_COMPANYCOIN, .fairy_model = -1}, // Company Coin
    {.song = SONG_BANANAMEDALGET, .sprite = 0x3C, .helm_hurry_item = HHITEM_MEDAL, .fairy_model = -1}, // Medal
    {.song = SONG_GUNGET, .sprite = 0x94, .helm_hurry_item = HHITEM_MOVE, .fairy_model = MODEL_GENERIC_POTION}, // Cranky Move
    {.song = SONG_GUNGET, .sprite = 0x96, .helm_hurry_item = HHITEM_MOVE, .fairy_model = MODEL_GENERIC_POTION}, // Funky Move
    {.song = SONG_GUNGET, .sprite = 0x93, .helm_hurry_item = HHITEM_MOVE, .fairy_model = MODEL_GENERIC_POTION}, // Candy Move
    {.song = SONG_GUNGET, .sprite = 0x94, .helm_hurry_item = HHITEM_MOVE, .fairy_model = MODEL_GENERIC_POTION}, // Training Move
    {.song = SONG_GUNGET, .sprite = 0x3A, .helm_hurry_item = HHITEM_MOVE, .fairy_model = MODEL_GENERIC_POTION}, // BFI Move
    {.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = MODEL_GENERIC_KONG}, // Kong
    {.song = SONG_BEANGET, .sprite = -1, .helm_hurry_item = HHITEM_BEAN, .fairy_model = -1}, // Bean
    {.song = SONG_PEARLGET, .sprite = -1, .helm_hurry_item = HHITEM_PEARL, .fairy_model = -1}, // Pearl
    {.song = SONG_FAIRYTICK, .sprite = 0x89, .helm_hurry_item = HHITEM_FAIRY, .fairy_model = 0x3D}, // Fairy
    {.song = SONG_RAINBOWCOINGET, .sprite = 0xA0, .helm_hurry_item = HHITEM_RAINBOWCOIN, .fairy_model = -1}, // Rainbow Coin
    {.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_FAKEITEM, .fairy_model = 0x103}, // Fake Item (Bubble)
    {.song = SONG_MELONSLICEGET, .sprite = 0x46, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = -1}, // Junk Item (Melon)
    {.song = SONG_GUNGET, .sprite = 0x94, .helm_hurry_item = HHITEM_KONG, .fairy_model = 0x11}, // Cranky
    {.song = SONG_GUNGET, .sprite = 0x96, .helm_hurry_item = HHITEM_KONG, .fairy_model = 0x12}, // Funky
    {.song = SONG_GUNGET, .sprite = 0x93, .helm_hurry_item = HHITEM_KONG, .fairy_model = 0x13}, // Candy
    {.song = SONG_BLUEPRINTGET, .sprite = 0x95, .helm_hurry_item = HHITEM_KONG, .fairy_model = 0x1F}, // Snide
    {.song = SONG_SILENCE, .sprite = 0x8E, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = -1}, // Nothing
    {.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_FAKEITEM, .fairy_model = 0x103}, // Fake Item (Reversed Controls)
    {.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_FAKEITEM, .fairy_model = 0x103}, // Fake Item (Slowed)
    {.song = SONG_SILENCE, .sprite = 0xAF, .helm_hurry_item = HHITEM_NOTHING, .fairy_model = 0xD2}, // Hint Item
};

void displayMedalOverlay(int flag, int item_type) {
    float reward_x = 160.f;
    float reward_y = 120.0f;
    if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
        if (item_type != MEDALITEM_KEY) {
            setFlag(flag, 1, FLAGTYPE_PERMANENT);
        }
        void* sprite = 0;
        short flut_flag = flag;
        int kong = getKong(0);
        updateFlag(FLAGTYPE_PERMANENT, (short*)&flut_flag, (void*)0, -1);
        songs song = item_detection_data[item_type].song;
        int sprite_index = item_detection_data[item_type].sprite;
        helm_hurry_items hh_item = item_detection_data[item_type].helm_hurry_item;
        switch (item_type) {
            case MEDALITEM_GB:
                giveGB(kong, getWorld(CurrentMap, 1));
                break;
            case MEDALITEM_BP:
                {
                    int bp_index = flut_flag - FLAG_BP_JAPES_DK_HAS;
                    int bp_kong = bp_index % 5;
                    if (bp_kong > 4) {
                        bp_kong = 0;
                    }
                    sprite_index = bp_sprites[bp_kong];
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
                }
                break;
            case MEDALITEM_SPECIALCOIN:
                if (flut_flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
                    // Nintendo Coin
                    sprite_index = 0x8D;
                } else {
                    // Rareware Coin
                    sprite_index = 0x8C;
                }
                break;
            case MEDALITEM_KONG:
                {
                    int kong_index = -1;
                    for (int i = 0; i < 5; i++) {
                        if (flut_flag == kong_flags[i]) {
                            kong_index = i;
                        }
                    }
                    if ((kong_index >= 0) && (kong_index < 5)) {
                        song = instrument_songs[kong_index];
                        sprite_index = 0xA9 + kong_index;
                    }
                    refreshItemVisibility();
                }
                break;
            case MEDALITEM_BEAN:
                sprite = &bean_sprite;
                break;
            case MEDALITEM_PEARL:
                sprite = &pearl_sprite;
                break;
            case MEDALITEM_RAINBOW:
                giveRainbowCoin();
                break;
            case MEDALITEM_ICETRAP_BUBBLE:
                queueIceTrap(ICETRAP_BUBBLE);
                sprite = &fool_overlay_sprite;
                break;
            case MEDALITEM_ICETRAP_REVERSE:
                queueIceTrap(ICETRAP_REVERSECONTROLS);
                sprite = &fool_overlay_sprite;
                break;
            case MEDALITEM_ICETRAP_SLOW:
                queueIceTrap(ICETRAP_SLOWED);
                sprite = &fool_overlay_sprite;
                break;
            case MEDALITEM_JUNKMELON:
                giveMelon();
                break;
            case MEDALITEM_HINT:
                playSFX(0x2EA);
                break;
        }
        if (song != SONG_SILENCE) {
            playSFX(0xF2);
            playSong(song, 1.0f);
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
            
            displaySpriteAtXYZ(sprite, 1.0f, reward_x, reward_y, -10.0f);
        }
        if (hh_item != HHITEM_NOTHING) {
            addHelmTime(hh_item, 1);
        }
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 1.0f, reward_x, reward_y, -10.0f);
    }
}

void banana_medal_acquisition(int flag) {
    /**
     * @brief Acquire a banana medal, and handle the item acquired from it
     * 
     * @param flag Flag index of the banana medal
     */
    int item_type = 0;
    if (flag >= FLAG_MEDAL_ISLES_DK) {
        item_type = getMedalItem((flag - FLAG_MEDAL_ISLES_DK) + 40);
    } else {
        item_type = getMedalItem(flag - FLAG_MEDAL_JAPES_DK);
    }
    displayMedalOverlay(flag, item_type);
}

static unsigned char key_timer = 0;
static unsigned char key_index = 0;
static char key_text[] = "KEY 0";
static unsigned char old_keys = 0;

void keyGrabHook(int song, float vol) {
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

int getFlagIndex_MedalCorrected(int start, int level) {
    /**
     * @brief Get a corrected flag index for a medal, which will convert Rambi/Enguarde into the kong who entered the transformation crate
     * 
     * @param start Start flag index
     * @param level Level Index
     * 
     * @return New flag index
     */
    if (level < 7) {
        return getFlagIndex_Corrected(start, level);
    }
    return FLAG_MEDAL_ISLES_DK + getKong(0);
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
            if (inBossMap(CurrentMap, 1, 1, 0)) {
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

Gfx* controlKeyText(Gfx* dl) {
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
        gDPSetCombineLERP(dl++, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0);
        gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, key_opacity);
        dk_strFormat(key_text, "KEY %d", key_index + 1);
        dl = displayText(dl,1,640,750,key_text,0x80);
        key_timer -= 1;
    }
    return dl;
}

static short kong_models[] = {4, 1, 6, 9, 0xC};

void giveFairyItem(int flag, int state, flagtypes type) {
    /**
     * @brief Handle acquisition of the item tied to a fairy
     * 
     * @param flag Flag index of the fairy
     * @param state Target state of the flag. AKA whether to set (1) or clear (0) the flag
     * @param type Flag Type
     */
    int model = getFairyModel(flag);
    int model_key = model;
    if ((model_key >= 0xF6) && (model_key <= 0xFB)) {
        model_key = MODEL_GENERIC_POTION;
    } else if (inShortList(model_key, &kong_models[0], 5)) {
        model_key = MODEL_GENERIC_KONG;
    }
    ICE_TRAP_TYPES ice_trap_type = ICETRAP_OFF;
    if ((model_key >= -4) && (model_key <= -2)) {
        ice_trap_type = model_key + 5;
        model_key = 0x103;
        model = 0x103;
    }
    if (model_key > -1) {
        int i = 0;
        int cap = sizeof(item_detection_data) / sizeof(item_info);
        while (i < cap) {
            if (item_detection_data[i].fairy_model == model_key) {
                helm_hurry_items hh_item = item_detection_data[i].helm_hurry_item;
                if (hh_item != HHITEM_NOTHING) {
                    addHelmTime(hh_item, 1);
                }
                break;
            }
            i++;
        }
    }
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
    } else if (model == 0x103) {
        // Fake Item
        queueIceTrap(ice_trap_type);
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
    if ((Player->control_state == 99) && (CurrentMap != MAP_KROOLDIDDY)) {
        return 1;
    }
    if ((Player->grounded_bitfield & 4) && ((Player->water_floor - Player->floor) > 20.0f)) {
        return 1;
    }
    if (Rando.quality_of_life.dance_skip) {
        int is_banned_map = inBattleCrown(CurrentMap);
        if (inBossMap(CurrentMap, 1, 1, 0)) {
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
    ICE_TRAP_TYPES it_type = ICETRAP_BUBBLE;
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
            playSound(0x2A0, 0x7FFF, 63.0f, 1.0f, 5, 0);
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
            playSound(0x157, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0x1C:
        case 0x1D:
        case 0x23:
        case 0x24:
        case 0x27:
            // Banana Coin
            playSong(SONG_BANANACOINGET, pickup_volume);
            break;
        case 0x48:
        case 0x28F:
            // Company Coin
            if (Rando.item_rando) {
                playSong(SONG_COMPANYCOINGET, pickup_volume);
            }
            hh_item = HHITEM_COMPANYCOIN;
            forceDance();
            break;
        case 0x56:
            // Orange
            playSound(0x147, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0x25E:
            // Full Melon
            applyDamage(0, 1);
        case 0x57:
            // Melon Slice
            playSong(SONG_MELONSLICEGET, pickup_volume);
            forceDance();
            break;
        case 0x25F:
        case 0x260:
        case 0x261:
        case 0x262:
            // Shopkeepers
            hh_item = HHITEM_KONG;
        case 0x59:
        case 0x5B:
        case 0x1F2:
        case 0x1F3:
        case 0x1F5:
        case 0x1F6:
            // Potion
            playSong(SONG_GUNGET, 1.0f);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            if (hh_item == HHITEM_NOTHING) {
                hh_item = HHITEM_MOVE;
            }
            break;
        case 0x74:
        case 0x288:
            // GB
            playSong(SONG_GBGET, 1.0f);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            // hh_item = HHITEM_GB; // Ignored as it's handled in a separate case
            break;
        case 0x8E:
            // Crystal
            playSong(SONG_CRYSTALCOCONUTGET, pickup_volume);
            break;
        case 0x90:
            // Medal
            playSong(SONG_GBGET, 1.0f);
            BananaMedalGet();
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            hh_item = HHITEM_MEDAL;
            break;
        case 0x98:
            // Film
            playSound(0x263, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0xB7:
            // Rainbow Coin
            playSong(SONG_RAINBOWCOINGET, pickup_volume);
            hh_item = HHITEM_RAINBOWCOIN;
            setFlag(FLAG_FIRST_COIN_COLLECTION, 1, FLAGTYPE_PERMANENT);
            forceDance();
            break;
        case 0xDD:
        case 0xDE:
        case 0xDF:
        case 0xE0:
        case 0xE1:
            // Blueprint
            playSong(SONG_BLUEPRINTGET, pickup_volume);
            forceDance();
            hh_item = HHITEM_BLUEPRINT;
            break;
        case 0xEC:
        case 0x1D2:
            // Race Coin
            playSong(SONG_MINECARTCOINGET, pickup_volume);
            break;
        case 0x13C:
            // Key
            keyGrabHook(SONG_GBGET, 1.0f);
            if (!canDanceSkip()) {
                int action = 0x29; // GB Get
                if (inBossMap(CurrentMap, 1, 1, 0)) {
                    action = 0x41; // Key Get
                }
                setAction(action, 0, 0);
            }
            hh_item = HHITEM_KEY;
            auto_turn_keys();
            break;
        case 0x18D:
            // Crown
            playSong(SONG_GBGET, 1.0f);
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            CrownGet();
            hh_item = HHITEM_CROWN;
            break;
        case 0x198:
            // Bean
            playSong(SONG_BEANGET, 1.0f);
            hh_item = HHITEM_BEAN;
            forceDance();
            break;
        case 0x1B4:
            // Pearl
            playSong(SONG_PEARLGET, 1.0f);
            hh_item = HHITEM_PEARL;
            forceDance();
            break;
        case 0x1D1:
            // Coin Powerup
            playSound(0xAE, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0x257:
        case 0x258:
        case 0x259:
        case 0x25A:
        case 0x25B:
            song = instrument_songs[object_type - 0x257];
            if (song >= 0) {
                playSong(song, 1.0f);
            }
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            refreshItemVisibility();
            // hh_item = HHITEM_KONG; // Ignored as it's handled in a separate case
            break;
        case 0x25C:
            playSong(SONG_FAIRYTICK, 1.0f);
            hh_item = HHITEM_FAIRY;
            forceDance();
            break;
        case 0x25D:
        case 0x264:
        case 0x265:
            // Fake Item
            if (object_type == 0x25D) {
                it_type = ICETRAP_BUBBLE;
            } else if (object_type == 0x264) {
                it_type = ICETRAP_REVERSECONTROLS;
            } else if (object_type == 0x265) {
                it_type = ICETRAP_SLOWED;
            }
            forceDance();
            queueIceTrap(it_type);
            hh_item = HHITEM_FAKEITEM;
            break;
        case 0x27E:
            // Hint item
            forceDance();
            playSound(0x2EA, 0x7FFF, 63.0f, 1.0f, 5, 0);
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
            return checkFlagDuplicate(FLAG_TBARREL_ORANGE, FLAGTYPE_PERMANENT);
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