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

typedef struct item_info {
    /* 0x000 */ songs song;
    /* 0x004 */ int sprite;
    /* 0x008 */ helm_hurry_items helm_hurry_item;
} item_info;

static const unsigned char bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
static const unsigned char instrument_songs[] = {SONG_BONGOS, SONG_GUITAR, SONG_TROMBONE, SONG_SAXOPHONE, SONG_TRIANGLE};

static const item_info item_detection_data[] = {
    {.song = SONG_SILENCE, .sprite = 0x8E, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_NONE
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_KONG
	{.song = SONG_GUNGET, .sprite = 0x94, .helm_hurry_item = HHITEM_MOVE}, // REQITEM_MOVE
	{.song = SONG_GBGET, .sprite = 0x3B, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_GOLDENBANANA
	{.song = SONG_BLUEPRINTGET, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_BLUEPRINT
	{.song = SONG_FAIRYTICK, .sprite = 0x89, .helm_hurry_item = HHITEM_FAIRY}, // REQITEM_FAIRY
	{.song = SONG_GBGET, .sprite = 0x8A, .helm_hurry_item = HHITEM_KEY}, // REQITEM_KEY
	{.song = SONG_BANANAMEDALGET, .sprite = 0x8B, .helm_hurry_item = HHITEM_CROWN}, // REQITEM_CROWN
	{.song = SONG_COMPANYCOINGET, .sprite = -1, .helm_hurry_item = HHITEM_COMPANYCOIN}, // REQITEM_COMPANYCOIN
	{.song = SONG_BANANAMEDALGET, .sprite = 0x3C, .helm_hurry_item = HHITEM_MEDAL}, // REQITEM_MEDAL
	{.song = SONG_BEANGET, .sprite = -1, .helm_hurry_item = HHITEM_BEAN}, // REQITEM_BEAN
	{.song = SONG_PEARLGET, .sprite = -1, .helm_hurry_item = HHITEM_PEARL}, // REQITEM_PEARL
	{.song = SONG_RAINBOWCOINGET, .sprite = 0xA0, .helm_hurry_item = HHITEM_RAINBOWCOIN}, // REQITEM_RAINBOWCOIN
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_FAKEITEM}, // REQITEM_ICETRAP
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_GAMEPERCENTAGE
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_COLOREDBANANA
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_BOSSES
	{.song = SONG_SILENCE, .sprite = -1, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_BONUSES
	{.song = SONG_MELONSLICEGET, .sprite = 0x46, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_JUNK
	{.song = SONG_SILENCE, .sprite = 0xAF, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_HINT
	{.song = SONG_GUNGET, .sprite = 0x94, .helm_hurry_item = HHITEM_KONG}, // REQITEM_SHOPKEEPER
    {.song = SONG_BLUEPRINTGET, .sprite = 0x92, .helm_hurry_item = HHITEM_NOTHING}, // REQITEM_AP
};

static const unsigned char move_sprites[] = {0x94, 0x96, 0x93, 0x38, 0x3A}; // Cranky, Funky, Candy, Camera, Shockwave
static const unsigned char shopkeeper_sprites[] = {0x94, 0x96, 0x93, 0x95}; // Cranky, Funky, Candy, Snide

void displayMedalOverlay(int flag, item_packet *item_send) {
    float reward_x = 160.f;
    float reward_y = 120.0f;
    if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
        setPermFlag(flag);
        giveItemFromPacket(item_send, 0);
        void* sprite = 0;
        requirement_item item_type = item_send->item_type;
        int item_kong = item_send->kong;
        songs song = item_detection_data[item_type].song;
        int sprite_index = item_detection_data[item_type].sprite;
        switch(item_type) {
            case REQITEM_KONG:
                song = instrument_songs[item_kong];
                sprite_index = 0xA9 + item_kong;
                refreshItemVisibility();
                break;
            case REQITEM_BLUEPRINT:
                sprite_index = bp_sprites[item_kong];
                break;
            case REQITEM_KEY:
                auto_turn_keys();
                break;
            case REQITEM_COMPANYCOIN:
                sprite_index = item_kong == 0 ? 0x8D : 0x8C;
                break;
            case REQITEM_MOVE:
                sprite = &potion_sprite;
                break;
            case REQITEM_BEAN:
                sprite = &bean_sprite;
                break;
            case REQITEM_PEARL:
                sprite = &pearl_sprite;
                break;
            case REQITEM_ICETRAP:
                sprite = &fool_overlay_sprite;
                break;
            case REQITEM_JUNK:
                applyDamageMask(0, 1);
                break;
            case REQITEM_HINT:
                playSFX(0x2EA);
                break;
            case REQITEM_SHOPKEEPER:
                sprite_index = shopkeeper_sprites[item_kong];
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
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 1.0f, reward_x, reward_y, -10.0f);
    }
}

void banana_medal_check(int count, int change, int requirement, int flag, int index) {
    if (requirement < 1) {
        requirement = 1;
    }
    if (count < requirement) {
        return;
    }
    if ((count - change) >= requirement) {
        return;
    }
    displayMedalOverlay(flag, &medal_item_table[index]);
}

void banana_medal_acquisition(int cb_count, int world, int change) {
    /**
     * @brief Acquire a banana medal, and handle the item acquired from it
     * 
     * @param flag Flag index of the banana medal
     */
    int requirement = Rando.cb_medal_requirement[world];
    int flag = 0;
    int kong = getKong(0);
    int offset = (5 * world) + kong;
    if (Rando.include_half_medals) {
        flag = FLAG_HALF_MEDAL_JAPES_DK + offset;
        banana_medal_check(cb_count, change, requirement >> 1, flag, 45 + offset);
    }
    flag = FLAG_MEDAL_JAPES_DK + offset;
    if (world == 7) {
        flag = FLAG_MEDAL_ISLES_DK + kong;
        offset = 40 + kong;
    }
    banana_medal_check(cb_count, change, requirement, flag, offset);
    
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

void giveItemFromSend(item_packet *send) {
    int item_type = send->item_type;
    int item_kong = send->kong;
    giveItem(item_type, send->level, item_kong, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1, .give_coins = 1, .apply_ice_trap = 1});
    switch(item_type) {
        case REQITEM_KONG:
            refreshItemVisibility();
            break;
        case REQITEM_KEY:
            auto_turn_keys();
            break;
        case REQITEM_JUNK:
            applyDamageMask(0, 1);
            break;
    }
}

void giveItemFromKongData(model_item_data *db_item, int flag) {
    giveItemFromSend(&db_item->item);
    setPermFlag(flag);
}

void giveFairyItem(int flag, int state, flagtypes type) {
    /**
     * @brief Handle acquisition of the item tied to a fairy
     * 
     * @param flag Flag index of the fairy
     * @param state Target state of the flag. AKA whether to set (1) or clear (0) the flag
     * @param type Flag Type
     */
    item_packet *item_send = &fairy_item_table[flag - 589].item;
    giveItemFromSend(item_send);
    setPermFlag(flag);
}

static const unsigned char dance_skip_ban_maps[] = {
    MAP_AZTECBEETLE, // Aztec Beetle
    MAP_FACTORYCARRACE, // Factory Car Race
    MAP_GALLEONSEALRACE, // Galleon Seal Race
    MAP_CASTLECARRACE, // Castle Car Race
};

static const unsigned char dance_force_maps[] = {
    MAP_AZTECBEETLE, // Aztec Beetle
    MAP_FACTORYCARRACE, // Factory Car Race
    MAP_GALLEONSEALRACE, // Galleon Seal Race
    MAP_CASTLECARRACE, // Castle Car Race
};

int isCavesBeetleReward(void) {
    if (CurrentMap != MAP_CAVESBEETLERACE) {
        return 0;
    }
    return Player->yPos < 0;
}

int canDanceSkip(void) {
    /**
     * @brief Determine whether the player can dance skip an item
     * 
     * @return Dance Skip enabled
     */
    if ((CurrentMap == MAP_GALLEONPUFFTOSS) || (CurrentMap == MAP_KROOLDIDDY)) {
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
        if (inBattleCrown(CurrentMap)) {
            return 0;
        }
        if (inBossMap(CurrentMap, 1, 1, 0)) {
            return 0;
        }
        if (isCavesBeetleReward()) {
            return 0;
        }
        for (int i = 0; i < sizeof(dance_skip_ban_maps); i++) {
            if (dance_skip_ban_maps[i] == CurrentMap) {
                return 0;
            }
        }
        return 1;
    }
    return 0;
}

void forceDance(void) {
    if (isCavesBeetleReward()) {
        setAction(0x29, 0, 0);
        return;
    }
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
    ICE_TRAP_TYPES it_type = -1;
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
            break;
        case 0x98:
            // Film
            playSound(0x263, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0xB7:
            // Rainbow Coin
            playSong(SONG_RAINBOWCOINGET, pickup_volume);
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
            break;
        case 0xEC:
        case 0x1D2:
            // Race Coin
            playSong(SONG_MINECARTCOINGET, pickup_volume);
            break;
        case 0x13C:
            // Key
            if (!canDanceSkip()) {
                int action = 0x29; // GB Get
                if (inBossMap(CurrentMap, 1, 1, 0)) {
                    action = 0x41; // Key Get
                }
                setAction(action, 0, 0);
            }
            playSong(SONG_GBGET, 1.0f);
            break;
        case 0x18D:
            // Crown
            playSong(SONG_GBGET, 1.0f);
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            CrownGet();
            break;
        case 0x198:
            // Bean
            playSong(SONG_BEANGET, 1.0f);
            forceDance();
            break;
        case 0x1B4:
            // Pearl
            playSong(SONG_PEARLGET, 1.0f);
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
        case 0x25D:
        case 0x264:
        case 0x265:
        case 0x299:
            forceDance();
            break;
        case 0x27E:
        case 649:
        case 650:
        case 651:
        case 652:
            // Hint item
            forceDance();
            playSound(0x2EA, 0x7FFF, 63.0f, 1.0f, 5, 0);
            break;
        case 0x291:
        case 0x292:
        case 0x293:
        case 0x294:
            {
                // Archi Item
                float speed = 1.0f;
                if (object_type == 0x294) {
                    speed = 0.5f;
                }
                forceDance();
                playSound(69, 0x7FFF, 63.0f, speed, 5, 0);
            }
            break;
    }
    addHelmTime(hh_item, multiplier);
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
    ModelTwoData* _object = &ObjectModel2Pointer[index];
    if (model2_type == 0x11) {
        // Homing
        return 1;
        // return (MovesBase[(int)Character].weapon_bitfield & 3) == 3;
    } else if (model2_type == 0x8E) {
        // Crystal
        return 1;
        // return crystalsUnlocked(Character);
    } else if (model2_type == 0x8F) {
        // Regular Crate
        return 1;
        // return MovesBase[(int)Character].weapon_bitfield & 1;
    } else if (model2_type == 0x56) {
        // Orange
        return 1;
        // if (CurrentMap == MAP_TBARREL_ORANGE) { // Orange Barrel
        //     return 1;
        // }
        // return hasFlagMove(FLAG_TBARREL_ORANGE);
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
        return 1;
        // return hasFlagMove(FLAG_ABILITY_CAMERA);
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

typedef struct collectable_render {
    /* 0x000 */ short cb_single; // Make sure these 3 are consecutive
    /* 0x002 */ short coin;
    /* 0x004 */ short cb_bunch;
    /* 0x006 */ short kong;
} collectable_render;

static collectable_render CollectableRenderData[] = {
    {.cb_single = 0x000D, .cb_bunch = 0x002B, .coin = 0x001D, .kong = KONG_DK},
    {.cb_single = 0x000A, .cb_bunch = 0x0208, .coin = 0x0024, .kong = KONG_DIDDY},
    {.cb_single = 0x001E, .cb_bunch = 0x0205, .coin = 0x0023, .kong = KONG_LANKY},
    {.cb_single = 0x0016, .cb_bunch = 0x0207, .coin = 0x001C, .kong = KONG_TINY},
    {.cb_single = 0x001F, .cb_bunch = 0x0206, .coin = 0x0027, .kong = KONG_CHUNKY},
};

int isCollectable(int type) {
    int player_index = FocusedPlayerIndex;
    for (int i = 0; i < 5; i++) {
        if (inShortList(type, &CollectableRenderData[i].cb_single, 3)) {
            int kong = CollectableRenderData[i].kong;
            if (Rando.quality_of_life.rambi_enguarde_pickup) {
                return SwapObject[player_index].player->new_kong == kong + 2;
            }
            return SwapObject[player_index].player->characterID == kong + 2;
        }
    }
    // if (type == 0x11) {
    //     // Homing Crate
    //     // return (MovesBase[(int)Character].weapon_bitfield & 3) == 3;
    // } else if (type == 0x8E) {
    //     // Crystal
    //     return SwapObject[player_index].player->unk_fairycam_bitfield & 2;
    // } else if (type == 0x8F) {
    //     // Ammo Crate
    //     return MovesBase[(int)Character].weapon_bitfield & 1;
    // } else if (type == 0x98) {
    //     // Film
    //     return hasFlagMove(FLAG_ABILITY_CAMERA);
    // } else if (type == 0x56) {
    //     // Oranges
    //     return hasFlagMove(FLAG_TBARREL_ORANGE);
    // }
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

void getFlagMappingData(int index, char *level, char *kong) {
    int om2_index = indexOfNextObj(index);
    *level = ObjectModel2Pointer[om2_index].unk_8D[1];
    *kong = ObjectModel2Pointer[om2_index].unk_8D[2];
}

void updateItemTotalsHandler(int player, int obj_type, int is_homing, int index) {
    // rewrite of coincbcollecthandle
    // Added index as 4th arg
    if ((MapProperties.in_training) && (obj_type != 0x56)) {
        *(char*)(0x80029FA0) = *(char*)(0x80029FA0) - 1;
        return;
    }
    if (CurrentMap == MAP_SNIDE) {
        return;
    }
    int save_game = 0;
    int collectable_type = -1;
    char item_level = -1;
    char item_kong = -1;
    getFlagMappingData(index, &item_level, &item_kong);
    int is_acceptable_item = inShortList(obj_type, &acceptable_items, sizeof(acceptable_items) >> 1);
    if (is_acceptable_item) {
        if (inBossMap(CurrentMap, 1, 1, 0)) {
            if (obj_type != 0x13C) {
                setAction(0x41, 0, 0);
            }
        } else if (inBattleCrown(CurrentMap)) {
            if (obj_type != 0x18D) {
                setAction(0x42, 0, 0);
            }
        }
    }
    switch (obj_type) {
        case 0x1C:
        case 0x1D:
        case 0x23:
        case 0x24:
        case 0x27:
            // Coins
            setPermFlag(0x18C);
            changeCollectableCount(1, player, 1);
            break;
        case 0x48:
            // Nintendo Coin
            giveItem(REQITEM_COMPANYCOIN, 0, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x56:
            // Orange
            setPermFlag(0x173);
            changeCollectableCount(4, player, 1);
            break;
        case 0x57:
        case 0x25E:
            // Watermelon
            applyDamage(player, 1);
            break;
        case 0x8E:
            // Crystal
            changeCollectableCount(5, player, 150);
            break;
        case 0x90:
            giveItem(REQITEM_MEDAL, 0, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x98:
            // Film
            changeCollectableCount(6, player, 1);
            break;
        case 0xB7:
            // Rainbow Coin
            giveItem(REQITEM_RAINBOWCOIN, 0, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1, .give_coins = 1});
            RainbowCoinFTT();
            break;
        case 0xDD:
        case 0xDE:
        case 0xDF:
        case 0xE0:
        case 0xE1:
            // Blueprint
            giveItem(REQITEM_BLUEPRINT, item_level, item_kong, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            save_game = 1;
            break;
        case 0xEC:
            // Race Coin
            if ((levelIndexMapping[CurrentMap] == LEVEL_BONUS) || (!Rando.race_coins_shuffled)) {
                // Bonus map, or unshuffled coins
                changeCollectableCount(11, player, 1);
            } else {
                giveItem(REQITEM_RACECOIN, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            }
            break;
        case 0x13C:
            // Boss Key
            giveItem(REQITEM_KEY, item_level, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            auto_turn_keys();
            save_game = 1;
            break;
        case 0x91:
        case 0x15D:
        case 0x15E:
        case 0x15F:
        case 0x160:
            // Single Ammo
            collectable_type = is_homing ? 3 : 2;
            playSound(0x331, 0x7FFF, 63.0f, 1.0f, 5, 0);
        case 0x0A:
        case 0x0D:
        case 0x16:
        case 0x1E:
        case 0x1F:
            // CB Single
            if (collectable_type == -1) {
                collectable_type = 0;
            }
            setPermFlag(0x18B);
            changeCollectableCount(collectable_type, player, 1);
            break;
        case 0x18D:
            // Crown
            giveItem(REQITEM_CROWN, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            save_game = 1;
            break;
        case 0x198:
            // Bean
            giveItem(REQITEM_BEAN, 0, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x1B4:
            // Pearls
            giveItem(REQITEM_PEARL, 0, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
        case 0x1D2:
            // Coin Multi
            changeCollectableCount(1, player, 1);
            break;
        case 0x74: // Regular GB
        case 0x288: // Rareware GB
            changeCollectableCount(8, player, 1);
            save_game = 1;
            break;
        case 0x5B:
        case 0x1F2:
        case 0x59:
        case 0x1F3:
        case 0x1F5:
        case 0x1F6:
            // Potion
            giveItem(REQITEM_MOVE, item_level, item_kong, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x257:
        case 0x258:
        case 0x259:
        case 0x25A:
        case 0x25B:
            // Kong Item
            giveItem(REQITEM_KONG, 0, obj_type - 0x257, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            refreshItemVisibility();
            break;
        case 0x25C:
            giveItem(REQITEM_FAIRY, 0, 0, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x25F: // Cranky
        case 0x260: // Funky
        case 0x261: // Candy
        case 0x262: // Snide
            // Shopkeepers
            giveItem(REQITEM_SHOPKEEPER, 0, obj_type - 0x25F, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x25D:
        case 0x264:
        case 0x265:
        case 0x299:
            giveItem(REQITEM_ICETRAP, item_level, item_kong, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1, .apply_ice_trap=1});
            break;
        case 0x27E:
        case 0x289:
        case 0x28A:
        case 0x28B:
        case 0x28C:
            // Hint
            giveItem(REQITEM_HINT, item_level, item_kong, (giveItemConfig){.display_item_text = 1, .apply_helm_hurry = 1});
            break;
        case 0x28F:
            // Rareware Coin
            giveItem(REQITEM_COMPANYCOIN, 0, 1, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1});
            break;
    }
    if (save_game) {
        save();
    }
}