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
#define MEDALITEM_NOTHING 17

void banana_medal_acquisition(int flag) {
    int item_type = getMedalItem(flag - FLAG_MEDAL_JAPES_DK);
    if (!checkFlag(flag, 0)) {
        if (item_type != MEDALITEM_KEY) {
            setFlag(flag, 1, 0);
        }
        int song = 0;
        void* sprite = 0;
        int sprite_index = -1;
        short flut_flag = flag;
        updateFlag(0, (short*)&flut_flag, (void*)0, -1);
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
                        if (checkFlagDuplicate(getKeyFlag(i), 0)) {
                            key_bitfield |= (1 << i);
                        }
                    }
                    setFlag(flag, 1, 0);
                    int spawned = 0;
                    for (int i = 0; i < 8; i++) {
                        if ((checkFlagDuplicate(getKeyFlag(i), 0)) && ((key_bitfield & (1 << i)) == 0)) {
                            if (!spawned) {
                                spawnActor(324, 0);
                                TextOverlayData.type = 5;
                                TextOverlayData.flag = getKeyFlag(i);
                                TextOverlayData.kong = 0;
                                spawned = 1;
                            }
                        }
                    }
                    auto_turn_keys();
                    song = 18; // GB/Key Get
                    sprite_index = 0x8A;
                }
                break;
            case MEDALITEM_CROWN:
                song = 0x97; // Banana Medal Get
                sprite_index = 0x8B;
                break;
            case MEDALITEM_SPECIALCOIN:
                song = 22; // Company Coin Get
                if (flut_flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
                    // Nintendo Coin
                    sprite_index = 0x8C;
                } else {
                    // Rareware Coin
                    sprite_index = 0x8D;
                }
                break;
            case MEDALITEM_MEDAL:
                song = 0x97; // Banana Medal Get
                sprite_index = 0x3C;
                break;
            case MEDALITEM_CRANKY:
                song = 115; // Gun Get
                sprite_index = 0x94;
                break;
            case MEDALITEM_FUNKY:
                song = 115; // Gun Get
                sprite_index = 0x96;
                break;
            case MEDALITEM_CANDY:
                song = 115; // Gun Get
                sprite_index = 0x93;
                break;
            case MEDALITEM_TRAINING:
                song = 115; // Gun Get
                sprite_index = 0x94;
                break;
            case MEDALITEM_BFI:
                song = 115; // Gun Get
                sprite_index = 0x3A;
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
                break;
            case MEDALITEM_PEARL:
                song = 128; // Pearl Get
                sprite = &pearl_sprite;
                break;
            case MEDALITEM_FAIRY:
                song = 46; // Fairy Tick
                sprite_index = 0x89;
                break;
            case MEDALITEM_RAINBOW:
                giveRainbowCoin();
                song = 145; // Rainbow Coin Get
                sprite_index = 0xA0;
                break;
            case MEDALITEM_FAKEITEM:
                initIceTrap();
                sprite_index = 0x92;
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
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 0x3F800000, 160.0f, 120.0f, -10.0f);
    }
}

/*
    void banana_medal_acquisition(int flag) {
    int item_type = getMedalItem(flag - FLAG_MEDAL_JAPES_DK);
    if (!checkFlag(flag, 0)) {
        // Display and play effects if you don't have item
        if (item_type < (BANANA_MEDAL_ITEM_COUNT + 1)) {
            int kong = -1;
            short flut_flag = flag;
            updateFlag(0, (short*)&flut_flag, (void*)0, -1);
            if (item_type == 11) {
                for (int i = 0; i < 5; i++) {
                    if (flut_flag == kong_flags[i]) {
                        kong = i;
                    }
                }
            }
            if (item_type == 2) {
                // Display key text
                int key_bitfield = 0;
                for (int i = 0; i < 8; i++) {
                    if (checkFlagDuplicate(getKeyFlag(i), 0)) {
                        key_bitfield |= (1 << i);
                    }
                }
                setFlag(flag, 1, 0);
                int spawned = 0;
                for (int i = 0; i < 8; i++) {
                    if ((checkFlagDuplicate(getKeyFlag(i), 0)) && ((key_bitfield & (1 << i)) == 0)) {
                        if (!spawned) {
                            spawnActor(324, 0);
                            TextOverlayData.type = 5;
                            TextOverlayData.flag = getKeyFlag(i);
                            TextOverlayData.kong = 0;
                            spawned = 1;
                        }
                    }
                }
                auto_turn_keys();
            } else if (item_type < BANANA_MEDAL_ITEM_COUNT) {
                setFlag(flag, 1, 0);
            }
            if (item_type == 0) {
                giveGB(getKong(0), getWorld(CurrentMap, 1));
            } else if (item_type == 15) {
                giveRainbowCoin();
            }
            if (item_type < BANANA_MEDAL_ITEM_COUNT) {
                playSFX(0xF2);
                int used_song = 0x97;
                int kong_songs[] = {11, 10, 12, 13, 9};
                int songs[] = {
                    18, // GB (GB/Key Get)
                    69, // BP (BP Get)
                    18, // Key (GB/Key Get)
                    0x97, // Crown (Banana Medal Get)
                    22, // Company Coin
                    0x97, // Medal (Banana Medal Get)
                    115, // Cranky (Gun Get)
                    115, // Funky (Gun Get)
                    115, // Candy (Gun Get)
                    115, // Training (Gun Get)
                    115, // Shockwave (Gun Get)
                    0, // Kong - Use kong array
                    147, // Bean (Bean Get)
                    128, // Pearl (Pearl Get)
                    46, // Fairy (Fairy Tick)
                    145, // Rainbow Coin Get
                    0, // K Rool Laugh (Use SFX)
                };
                if (item_type == 11) {
                    used_song = kong_songs[kong];
                } else if (item_type == 16) {
                    initIceTrap();
                } else if (item_type < BANANA_MEDAL_ITEM_COUNT) {
                    used_song = songs[item_type];
                }
                if (item_type != 16) {
                    playSong(used_song, 0x3F800000);
                }
            }
            unkSpriteRenderFunc(200);
            unkSpriteRenderFunc_0();
            loadSpriteFunction(0x8071EFDC);
            int bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
            int sprite_indexes[] = {
                0x3B, // GB
                0, // BP - Use bp sprite array
                0x8A,  // Key
                0x8B,  // Crown
                0, // Company Coin - Use separate check
                0x3C, // Medal
                0x94, // Cranky
                0x96, // Funky
                0x93, // Candy
                0x94, // Training Barrel
                0x3A, // Shockwave
                0, // Kong - Use separate check
                0x92, // Bean
                0x92, // Pearl
                0x89, // Fairy
                0xA0, // Rainbow Coin
                0x92, // Fake Item - Use separate check
            };
            int used_sprite = 0x3B;
            if (item_type == 1) {
                int character_val = Character;
                if (character_val > 4) {
                    character_val = 0;
                }
                used_sprite = bp_sprites[character_val];
            } else if (item_type == 4) {
                if (flut_flag == 132) {
                    // Nintendo Coin
                    used_sprite = 0x8C;
                } else {
                    // Rareware Coin
                    used_sprite = 0x8D;
                }
            } else if (item_type == 11) {
                used_sprite = 0xA9 + kong;
                refreshItemVisibility();
            } else if (item_type == BANANA_MEDAL_ITEM_COUNT) {
                used_sprite = 0x8E;
            } else {
                used_sprite = sprite_indexes[item_type];
            }
            void* sprite_addr = sprite_table[used_sprite];
            if (item_type == 12) {
                sprite_addr = &bean_sprite;
            } else if (item_type == 13) {
                sprite_addr = &pearl_sprite;
            }
            displaySpriteAtXYZ(sprite_addr, 0x3F800000, 160.0f, 120.0f, -10.0f);
        }
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 0x3F800000, 160.0f, 120.0f, -10.0f);
    }
}
*/

static unsigned char key_timer = 0;
static unsigned char key_index = 0;
static char key_text[] = "KEY 0";
static unsigned char old_keys = 0;

void keyGrabHook(int song, int vol) {
    playSong(song, vol);
    int val = 0;
    for (int i = 0; i < 8; i++) {
        if (checkFlagDuplicate(getKeyFlag(i), 0)) {
            val |= (1 << i);
        }
    }
    old_keys = val;
}

int getFlagIndex_Corrected(int start, int level) {
    return start + (5 * level) + getKong(0);
}

static const short boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7};

void collectKey(void) {
    for (int i = 0; i < 8; i++) {
        if (checkFlagDuplicate(getKeyFlag(i), 0)) {
            if ((old_keys & (1 << i)) == 0) {
                spawnActor(324,0);
                TextOverlayData.type = 5;
                TextOverlayData.flag = getKeyFlag(i);
                TextOverlayData.kong = 0;
            }
        }
    }
    auto_turn_keys();
}

int itemGrabHook(int collectable_type, int obj_type, int is_homing) {
    if (Rando.item_rando) {
        if (obj_type == 0x13C) {
            collectKey();
        } else {
            for (int i = 0; i < 7; i++) {
                if (CurrentMap == boss_maps[i]) {
                    for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                        if (obj_type == acceptable_items[j]) {
                            setAction(0x41, 0, 0);
                        }
                    }
                }
            }
        }
        if (obj_type != 0x18D) {
            if ((CurrentMap == 0x35) || (CurrentMap == 0x49) || ((CurrentMap >= 0x9B) && (CurrentMap <= 0xA2))) {
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

void initKeyText(int ki) {
    key_index = ki;
    key_timer = 100;
}

void giveFairyItem(int flag, int state, int type) {
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
            if (checkFlagDuplicate(getKeyFlag(i), 0)) {
                key_bitfield |= (1 << i);
            }
        }
    } else if (model == 0x10E) {
        // Fake Item
        initIceTrap();
    } else if (model == 0x10D) {
        giveRainbowCoin();
    }
    setFlag(flag, state, type);
    if (model == 0xF5) {
        // Key - Post flag set
        int spawned = 0;
        for (int i = 0; i < 8; i++) {
            if ((checkFlagDuplicate(getKeyFlag(i), 0)) && ((key_bitfield & (1 << i)) == 0)) {
                if (!spawned) {
                    spawnActor(324, 0);
                    TextOverlayData.type = 5;
                    TextOverlayData.flag = getKeyFlag(i);
                    TextOverlayData.kong = 0;
                    spawned = 1;
                }
            }
        }
        auto_turn_keys();
    }
}

static const unsigned char dance_skip_ban_maps[] = {
    0x0E, // Aztec Beetle
    0x1B, // Factory Car Race
    0x27, // Galleon Seal Race
    0x52, // Caves Beetle
    0xB9, // Castle Car Race
    0x08, // AD1
    0xC5, // Dog1
    0x9A, // MJ
    0x6F, // Pufftoss
    0x53, // Dog2
    0xC4, // AD2
    0xC7, // KKO
    0x35, // Japes: Crown
    0x49, // Aztec: Crown
    0x9B, // Factory: Crown
    0x9C, // Galleon: Crown
    0x9F, // Fungi: Crown
    0xA0, // Caves: Crown
    0xA1, // Castle: Crown
    0xA2, // Helm: Crown
    0x9D, // Isles: Lobby Crown
    0x9E, // Isles: Snide Crown
};

int canDanceSkip(void) {
    if (CurrentMap == 0x6F) {
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
        int is_banned_map = 0;
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

void getItem(int object_type) {
    float pickup_volume = 1-(0.3f * *(char*)(0x80745838));
    int song = -1;
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
            break;
        case 0x56:
            // Orange
            playSound(0x147, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x57:
            // Melon Slice
            playSong(0x2F, *(int*)(&pickup_volume));
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
            break;
        case 0x74:
        case 0x288:
            // GB
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
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
            break;
        case 0x98:
            // Film
            playSound(0x263, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0xB7:
            // Rainbow Coin
            playSong(0x91, *(int*)(&pickup_volume));
            break;
        case 0xDD:
        case 0xDE:
        case 0xDF:
        case 0xE0:
        case 0xE1:
            // Blueprint
            playSong(69, *(int*)(&pickup_volume));
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
            auto_turn_keys();
            break;
        case 0x18D:
            // Crown
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            CrownGet();
            break;
        case 0x198:
            // Bean
            playSong(147, 0x3F800000);
            break;
        case 0x1B4:
            // Pearl
            {
                playSong(128, 0x3F800000);
                // if (CurrentMap == 0x2C) { // Treasure Chest
                //     int requirement = 5;
                //     if (Rando.fast_gbs) {
                //         requirement = 1;
                //     }
                //     int count = 0;
                //     for (int i = 0; i < 5; i++) {
                //         count += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, 0);
                //     }
                //     if (count == (requirement - 1)) {
                //         playCutscene((void*)0, 1, 0);
                //     }
                // }
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
            break;
        case 0x25C:
            playSong(46, 0x3F800000);
            break;
        case 0x25D:
            // Fake Item
            initIceTrap();
            break;
    }
}

void initIceTrap(void) {
    trapPlayer();
    Player->trap_bubble_timer = 200;
    playSFX(0x2D4); // K Rool Laugh
    applyDamage(0, -1);
}

int getObjectCollectability(int id, int unk1, int model2_type) {
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
    } else if (model2_type == 0x90) {
        // Medal
        if (CurrentMap == 0x11) {
            behaviour_data* behaviour = _object->behaviour_pointer;
            if (behaviour) {
                if (behaviour->unk_64 != 0xFF) {
                    return 0;
                }
            }
        }
    } else if (model2_type == 0x98) {
        // Film
        return checkFlag(FLAG_ABILITY_CAMERA,0);
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