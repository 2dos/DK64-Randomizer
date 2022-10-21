#include "../../include/common.h"

int getObjectCollectability(int id, int unk1, int model2_type) {
    int index = indexOfNextObj(id);
    int* m2location = ObjectModel2Pointer;
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

typedef struct collision_info {
    /* 0x000 */ unsigned short type;
    /* 0x002 */ char collectable_type;
    /* 0x003 */ char unk3;
    /* 0x004 */ float unk4;
    /* 0x008 */ float unk8;
    /* 0x00C */ short intended_actor;
    /* 0x00E */ short actor_equivalent;
    /* 0x010 */ short hitbox_y_center;
    /* 0x012 */ short hitbox_scale;
} collision_info;

#define COLLISION_LIMIT 50
#define DEFS_LIMIT 137
static collision_info object_collisions[COLLISION_LIMIT] = {};
static actor_behaviour_def actor_defs[DEFS_LIMIT] = {};

#define COLLECTABLE_AMMOBOX -2
#define COLLECTABLE_NONE -1
#define COLLECTABLE_CB 0
#define COLLECTABLE_COIN 1
#define COLLECTABLE_AMMOPELLET 2
#define COLLECTABLE_ORANGE 4
#define COLLECTABLE_CRYSTAL 5
#define COLLECTABLE_FILM 6
#define COLLECTABLE_GB 8
#define COLLECTABLE_MEDAL 10
#define COLLECTABLE_RACECOIN 11
#define COLLECTABLE_BP 12

#define KONG_NONE -2

int addCollisionInfo(int index, int type, int collectable, int kong, int actor_equivalent, int hitbox_y, int hitbox_scale) {
    object_collisions[index].type = type;
    object_collisions[index].collectable_type = collectable;
    object_collisions[index].unk4 = 0.08f;
    object_collisions[index].unk8 = 0.95f;
    object_collisions[index].intended_actor = kong + 2;
    if ((Rando.any_kong_items & 2) && (collectable == COLLECTABLE_BP)) {
        // Blueprints
        object_collisions[index].intended_actor = 0;
    }
    object_collisions[index].actor_equivalent = actor_equivalent;
    object_collisions[index].hitbox_y_center = hitbox_y;
    object_collisions[index].hitbox_scale = hitbox_scale;
    return index + 1;
}

void initCollectableCollision(void) {
    // Single
    int index = addCollisionInfo(0, 0x000D, COLLECTABLE_CB, KONG_DK, 0, 0, 0);
    index = addCollisionInfo(index, 0x000A, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001F, COLLECTABLE_CB, KONG_CHUNKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001E, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0016, COLLECTABLE_CB, KONG_TINY, 0, 0, 0);
    // Coin
    index = addCollisionInfo(index, 0x0024, COLLECTABLE_COIN, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0023, COLLECTABLE_COIN, KONG_LANKY, 0x35, 0, 0);
    index = addCollisionInfo(index, 0x0027, COLLECTABLE_COIN, KONG_CHUNKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001C, COLLECTABLE_COIN, KONG_TINY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001D, COLLECTABLE_COIN, KONG_DK, 0, 0, 0);
    // Bunch
    index = addCollisionInfo(index, 0x002B, COLLECTABLE_CB, KONG_DK, 0, 0, 0);
    index = addCollisionInfo(index, 0x0208, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0206, COLLECTABLE_CB, KONG_CHUNKY, 0x6E, 0, 0);
    index = addCollisionInfo(index, 0x0205, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0207, COLLECTABLE_CB, KONG_TINY, 0, 0, 0);
    // Pellets
    index = addCollisionInfo(index, 0x0091, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Peanut
    index = addCollisionInfo(index, 0x015D, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Feather
    index = addCollisionInfo(index, 0x015E, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Grape
    index = addCollisionInfo(index, 0x015F, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Pineapple
    index = addCollisionInfo(index, 0x0160, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Coconut
    // Blueprint
    index = addCollisionInfo(index, 0x00DE, COLLECTABLE_BP, KONG_DK, 0x4E, 0, 0);
    index = addCollisionInfo(index, 0x00E0, COLLECTABLE_BP, KONG_DIDDY, 0x4B, 0, 0);
    index = addCollisionInfo(index, 0x00E1, COLLECTABLE_BP, KONG_LANKY, 0x4D, 0, 0);
    index = addCollisionInfo(index, 0x00DD, COLLECTABLE_BP, KONG_TINY, 0x4F, 0, 0);
    index = addCollisionInfo(index, 0x00DF, COLLECTABLE_BP, KONG_CHUNKY, 0x4C, 0, 0);
    // Multiplayer
    index = addCollisionInfo(index, 0x00B7, COLLECTABLE_COIN, KONG_NONE, 0x8C, 0, 0); // Rainbow Coin
    index = addCollisionInfo(index, 0x01CF, COLLECTABLE_NONE, KONG_NONE, 0x78, 0, 0); // Yellow CB Powerup
    index = addCollisionInfo(index, 0x01D0, COLLECTABLE_NONE, KONG_NONE, 0x77, 0, 0); // Blue CB Powerup
    index = addCollisionInfo(index, 0x01D1, COLLECTABLE_NONE, KONG_NONE, 0x76, 0, 0); // Coin Powerup
    index = addCollisionInfo(index, 0x01D2, COLLECTABLE_COIN, KONG_NONE, 0x7A, 0, 0); // Coin Multiplayer
    // Others
    index = addCollisionInfo(index, 0x0074, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4); // Golden Banana
    index = addCollisionInfo(index, 0x0056, COLLECTABLE_ORANGE, KONG_NONE, 0x34, 0, 0); // Orange
    index = addCollisionInfo(index, 0x008F, COLLECTABLE_AMMOBOX, KONG_NONE, 0x33, 0, 0); // Ammo Crate
    index = addCollisionInfo(index, 0x0011, COLLECTABLE_AMMOBOX, KONG_NONE, 0, 0, 0); // Homing Ammo Crate
    index = addCollisionInfo(index, 0x008E, COLLECTABLE_CRYSTAL, KONG_NONE, 0x79, 0, 0); // Crystal
    index = addCollisionInfo(index, 0x0057, COLLECTABLE_NONE, KONG_NONE, 0x2F, 0, 0); // Watermelon
    index = addCollisionInfo(index, 0x0098, COLLECTABLE_FILM, KONG_NONE, 0, 0, 0); // Film
    index = addCollisionInfo(index, 0x0090, COLLECTABLE_MEDAL, KONG_NONE, 0, 0, 0); // Medal
    index = addCollisionInfo(index, 0x00EC, COLLECTABLE_RACECOIN, KONG_NONE, 0x36, 0, 0); // Race Coin
    index = addCollisionInfo(index, 0x013C, COLLECTABLE_NONE, KONG_NONE, 0x48, 0, 0); // Boss Key
    index = addCollisionInfo(index, 0x018D, COLLECTABLE_NONE, KONG_NONE, 0x56, 0, 0); // Battle Crown
    index = addCollisionInfo(index, 0x0288, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4); // Rareware GB
    index = addCollisionInfo(index, 0x0048, COLLECTABLE_NONE, KONG_NONE, 151, 0, 0); // Nintendo Coin
    index = addCollisionInfo(index, 0x028F, COLLECTABLE_NONE, KONG_NONE, 152, 0, 0); // Rareware Coin
    index = addCollisionInfo(index, 0x005B, COLLECTABLE_NONE, KONG_NONE, 157, 0, 0); // Potion DK
    index = addCollisionInfo(index, 0x01F2, COLLECTABLE_NONE, KONG_NONE, 158, 0, 0); // Potion Diddy
    index = addCollisionInfo(index, 0x0059, COLLECTABLE_NONE, KONG_NONE, 159, 0, 0); // Potion Lanky
    index = addCollisionInfo(index, 0x01F3, COLLECTABLE_NONE, KONG_NONE, 160, 0, 0); // Potion Tiny
    index = addCollisionInfo(index, 0x01F5, COLLECTABLE_NONE, KONG_NONE, 161, 0, 0); // Potion Chunky
    index = addCollisionInfo(index, 0x01F6, COLLECTABLE_NONE, KONG_NONE, 162, 0, 0); // Potion Any
    // Write new table to ROM
    int hi = getHi(&object_collisions[0].type);
    int lo = getLo(&object_collisions[0].type);
    *(unsigned short*)(0x806F48D2) = hi;
    *(unsigned short*)(0x806F48D6) = lo;
    *(unsigned short*)(0x806F4A8E) = index;
    *(unsigned short*)(0x806F4E7E) = hi;
    *(unsigned short*)(0x806F4E8E) = lo;
    *(unsigned short*)(0x806F51C2) = getHi(&object_collisions[0].intended_actor);
    *(unsigned short*)(0x806F51CE) = getLo(&object_collisions[0].intended_actor);
    *(unsigned short*)(0x806F5556) = getHi(&object_collisions[0].collectable_type);
    *(unsigned short*)(0x806F5562) = getLo(&object_collisions[0].collectable_type);
    *(unsigned short*)(0x806F626E) = hi;
    *(unsigned short*)(0x806F627A) = lo;
    *(unsigned short*)(0x806F6AC6) = hi;
    *(unsigned short*)(0x806F6ACE) = lo;
    *(unsigned short*)(0x806F742A) = hi;
    *(unsigned short*)(0x806F744A) = lo;
    *(unsigned short*)(0x806F7996) = getHi(&object_collisions[index].type);
    *(unsigned short*)(0x806F799A) = getLo(&object_collisions[index].type);
}

int addActorDef(int index, int actor, int model, unsigned int func_0, unsigned int func_1) {
    actor_defs[index].actor_type = actor;
    actor_defs[index].model = model;
    actor_defs[index].unk4[4] = 0x02;
    actor_defs[index].unk4[5] = 0x26;
    actor_defs[index].code = (void*)func_0;
    actor_defs[index].unk10 = (void*)func_1;
    return index + 1;
}

void initActorDefs(void) {
    dk_memcpy(&actor_defs[0], &ActorBehaviourTable[0], 128*sizeof(actor_behaviour_def));
    int index = addActorDef(128, 151, 0, 0x80689F80, 0x8068A10C);
    index = addActorDef(index, 152, 0, 0x80689F80, 0x8068A10C);
    index = addActorDef(index, 157, 0xEE, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 158, 0xEF, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 159, 0xF0, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 160, 0xF1, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 161, 0xF2, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 162, 0xF3, 0x80689F80, 0x80689FEC);
    index = addActorDef(index, 153, 0, 0x80689F80, 0x8068A10C);
    *(unsigned short*)(0x8068926A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068927A) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D2) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D6) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068945A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x80689466) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068928A) = DEFS_LIMIT;
    *(unsigned short*)(0x80689452) = DEFS_LIMIT;
}

void spawnBonusReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    bonus_paad* paad = CurrentActorPointer_0->paad;
    int index = paad->barrel_index;
    if ((index > 0) && (index < 54)) {
        object = BonusBarrelData[index].spawn_actor;
    }
    spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
}

void spawnRewardAtActor(int object, int flag) {
    int index = CurrentActorPointer_0->reward_index;
    if ((index > 0) && (index < 54)) {
        object = BonusBarrelData[index].spawn_actor;
    }
    spawnObjectAtActor(object, flag);
}

void spawnCrownReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    int new_obj = getCrownItem(CurrentMap);
    if (new_obj != 0) {
        object = new_obj;
    }
    spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
}

void spawnBossReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    int new_obj = getKeyItem(flag);
    if (new_obj != 0) {
        object = new_obj;
    }
    spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
}

int checkFlagDuplicate(short flag, int type) {
    // Duplicate of the check flag function, for the purpose of checking a flag without referencing the lookup table
    if (flag == -1) {
        return 0;
    }
    unsigned char* fba = 0;
    if ((type == 0) || (type == 2)) {
        fba = (unsigned char*)getFlagBlockAddress(type);
    } else {
        fba = (unsigned char*)&TempFlagBlock[0];
    }
    int offset = flag >> 3;
    int shift = flag & 7;
    return (fba[offset] >> shift) & 1;
}

void setFlagDuplicate(short flag, int set, int type) {
    if (flag != -1) {
        unsigned char* fba = 0;
        if ((type == 0) || (type == 2)) {
            fba = (unsigned char*)getFlagBlockAddress(type);
        } else {
            fba = (unsigned char*)&TempFlagBlock[0];
        }
        int offset = flag >> 3;
        int shift = flag & 7;
        if (!set) {
            fba[offset] &= ~(1 << shift);
        } else {
            fba[offset] |= (1 << shift);
        }
        checkVictory_flaghook(flag);
    }
}

int countFlagsForKongFLUT(int startFlag, int start, int cap, int kong) {
    int count = 0;
    if (kong < 5) {
        for (int i = start; i <= cap; i++) {
            int check = getFlagIndex(startFlag, i, kong);
            if (check > -1) {
                count += checkFlag(check, 0);
            }
        }
    }
    return count;
}

static short flut_cache[40] = {};
static unsigned char cache_spot = 0;

void cacheFlag(int input, int output) {
    int slot = cache_spot;
    flut_cache[(2 * slot)] = input;
    flut_cache[(2 * slot) + 1] = output;
    cache_spot = (cache_spot + 1) % 20;
}

int clampFlag(int flag) {
    /*
        Clamp flag for GBs, Medals, Crowns, BPs, Nin/RW Coin, Boss Key
    */
    if ((flag >= 0x1D5) && (flag <= 0x1FC)) {
        return 1; // Blueprints
    }
    if ((flag >= 0x225) && (flag <= 0x24C)) {
        return 1; // Medal
    }
    if ((flag >= 0x261) && (flag <= 0x26A)) {
        return 1; // Crown
    }
    if (flag == 0x17B) {
        return 1; // RW Coin
    }
    if ((flag >= 0x1) && (flag <= 0x1F)) {
        return 1; // Japes GBs + Key 1
    }
    if ((flag >= 0x31) && (flag <= 0x4D)) {
        return 1; // Aztec GBs + Key 2
    }
    if ((flag >= 0x70) && (flag <= 0x8B)) {
        return 1; // Factory GBs + Key 3 + Nintendo Coin
    }
    if ((flag >= 0x9A) && (flag <= 0xA8)) {
        return 1; // Galleon GBs (Group 1) + Key 4
    }
    if ((flag >= 0xB6) && (flag <= 0xEC)) {
        return 1; // Galleon GBs (Group 2) + Fungi GBs (Group 1) + Key 5
    }
    if ((flag >= 0xF7) && (flag <= 0x119)) {
        return 1; // Fungi GBs (Group 2) + Caves GBs (Group 1)
    }
    if ((flag >= 0x124) && (flag <= 0x146)) {
        return 1; // Caves GBs (Group 2) + Key 6 + Castle GBs (Group 1) + Key 7 + Rareware GB
    }
    if ((flag >= 0x15E) && (flag <= 0x161)) {
        return 1; // Castle GBs (Group 2)
    }
    if ((flag == 0x17C) || (flag == 0x17D)) {
        return 1; // Key 8 + First GB
    }
    if ((flag >= 0x18E) && (flag <= 0x1AF)) {
        return 1; // Isles GBs
    }
    return 0;
}

void* checkMove(short* flag, void* fba, int source) {
    if (*flag & 0x8000) {
        // Is Move
        int item_kong = (*flag >> 12) & 7;
        if (item_kong > 4) {
            item_kong = 0;
        }
        int item_type = (*flag >> 8) & 15;
        int item_index = *flag & 0xFF;
        if (item_type == 7) {
            *flag = 0;
            return fba;
        } else {
            char* temp_fba = (char*)&MovesBase[item_kong];
            if (item_index == 0) {
                *flag = 0;
            } else {
                *flag = item_index - 1;
            }
            int init_val = *(char*)(temp_fba + item_type);
            if (((init_val & (1 << *flag)) == 0) && (source == 1)) {
                // Move given
                spawnActor(324,0);
                TextOverlayData.type = item_type;
                TextOverlayData.flag = item_index;
                TextOverlayData.kong = item_kong;
            }
            return temp_fba + item_type;
        }
    }
    return fba;
}

void* updateFlag(int type, short* flag, void* fba, int source) {
    if ((Rando.item_rando) && (type == 0) && (*flag != 0)) {
        int vanilla_flag = *flag;
        if (clampFlag(vanilla_flag)) {
            for (int i = 0; i < 20; i++) {
                if (flut_cache[(2 * i)] == vanilla_flag) {
                    if (flut_cache[(2 * i) + 1] != -1) {
                        *flag = flut_cache[(2 * i) + 1];
                    }
                    return checkMove(flag, fba, source);
                }
            }
            for (int i = 0; i < 400; i++) {
                int lookup = ItemRando_FLUT[(2 * i)];
                if (vanilla_flag == lookup) {
                    *flag = ItemRando_FLUT[(2 * i) + 1];
                    cacheFlag(vanilla_flag, *flag);
                    return checkMove(flag, fba, source);
                } else if (lookup == -1) {
                    cacheFlag(vanilla_flag, -1);
                    return fba;
                }
            }
        }
    }
    return fba;
}

int getKongFromBonusFlag(int flag) {
    if ((Rando.any_kong_items & 1) == 0) {
        for (int i = 0; i < 94; i++) {
            if (bonus_data[i].flag == flag) {
                return bonus_data[i].kong_actor;
            }
        }
    }
    return 0;
}

void banana_medal_acquisition(int flag) {
    /* 
        0 - GB,
        1 - BP,
        2 - Key,
        3 - Crown,
        4 - SpecialCoin,
        5 - Medal,
        6 - Cranky,
        7 - Funky,
        8 - Candy,
        9 - Training Barrel,
        10 - Shockwave,
        11 - Nothing,
    */
    if (!checkFlag(flag, 0)) {
        // Display and play effects if you don't have item
        int item_type = getMedalItem(flag - 549);
        if (item_type < 11) {
            setFlag(flag, 1, 0);
            if (item_type == 0) {
                MovesBase[(int)Character].gb_count[getWorld(CurrentMap,1)] += 1;
            }
            playSFX(0xF2);
            int used_song = 0x97;
            int songs[] = {18,69,18,0x97,22,0x97};
            if (item_type < 6) {
                used_song = songs[item_type];
            }
            playSong(used_song, 0x3F800000);
            unkSpriteRenderFunc(200);
            unkSpriteRenderFunc_0();
            loadSpriteFunction(0x8071EFDC);
            int bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
            int sprite_indexes[] = {0x3B, 0, 0x8A, 0x8B, 0, 0x3B, 0x94, 0x96, 0x93, 0x94, 0x3A};
            int used_sprite = 0x3B;
            if (item_type == 1) {
                int character_val = Character;
                if (character_val > 4) {
                    character_val = 0;
                }
                used_sprite = bp_sprites[character_val];
            } else if (item_type == 4) {
                if (flag == 132) {
                    // Nintendo Coin
                    used_sprite = 0x8C;
                } else {
                    // Rareware Coin
                    used_sprite = 0x8D;
                }
            } else {
                used_sprite = sprite_indexes[item_type];
            }
            displaySpriteAtXYZ(sprite_table[used_sprite], 0x3F800000, 160.0f, 120.0f, -10.0f);
        }
    }
}

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

static const short boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7};
static const short acceptable_items[] = {0x74,0xDE,0xE0,0xE1,0xDD,0xDF,0x48,0x28F,0x13C,0x18D,0x90};

int itemGrabHook(int collectable_type, int obj_type, int is_homing) {
    if (Rando.item_rando) {
        if (obj_type == 0x13C) {
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
        } else {
            for (int i = 0; i < 7; i++) {
                if (CurrentMap == boss_maps[i]) {
                    for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                        if (obj_type == acceptable_items[j]) {
                            Player->control_state = 0x71;
                            Player->control_state_progress = 1;
                            Player->try_again_timer = 1;
                        }
                    }
                }
            }
        }
        if (obj_type != 0x18D) {
            if ((CurrentMap == 0x35) || (CurrentMap == 0x49) || ((CurrentMap >= 0x9B) && (CurrentMap <= 0xA2))) {
                for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                    if (obj_type == acceptable_items[j]) {
                        Player->control_state = 0x72;
                        Player->control_state_progress = 255;
                    }
                }
            }
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

void spriteCode(int sprite_index) {
    void* paad = CurrentActorPointer_0->paad;
    spriteActorGenericCode(4.5f);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        assignGIFToActor(paad, sprite_table[sprite_index], 0x3F800000);
        if (CurrentActorPointer_0->control_state == 99) {
            CurrentActorPointer_0->control_state = 1;
            CurrentActorPointer_0->sub_state = 2;
        }
    }
}

void ninCoinCode(void) {
    spriteCode(0x8D);
}

void rwCoinCode(void) {
    spriteCode(0x8C);
}

void NothingCode(void) {
    deleteActorContainer(CurrentActorPointer_0);
}