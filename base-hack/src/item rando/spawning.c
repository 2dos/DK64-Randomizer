/**
 * @file spawning.c
 * @author Ballaam
 * @brief Item Rando elements pertaining to the spawning process of items
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

typedef struct actorSpawnStruct {
    float spawn_type;
    float unk0;
    float flag;
    unsigned char item_type;  // Non-standard, but just to prevent float conversion issues
    unsigned char item_level;  // Non-standard, but just to prevent float conversion issues
    unsigned char item_kong;  // Non-standard, but just to prevent float conversion issues
} actorSpawnStruct;

void spawnActorWithFlagHandler(int object, float x, float y, float z, int unk0, int spawn_type, int flag, int unk1, int item_level, int item_kong) {
    actorSpawnStruct data;
    float temp = *(float*)(0x8075A9A0);
    if (*(int*)(0x807FBB68) & 0x10) {
        temp *= 2;
    }
    data.spawn_type = spawn_type;
    data.unk0 = unk0;
    data.flag = flag;
    data.item_type = 0;
    data.item_level = item_level;
    data.item_kong = item_kong;
    spawnActorSpawnerContainer(object, x, y, z, 0, temp, unk1, &data);
}

void spawnWeirdReward(int index, int flag) {
    actor_spawn_packet *def = &extra_actor_spawns[index];
    spawnActorWithFlagHandler(def->actor,
        CurrentActorPointer_0->xPos,
        CurrentActorPointer_0->yPos,
        CurrentActorPointer_0->zPos,
        0, 0, flag,
        CurrentActorPointer_0,
        def->item_level,
        def->item_kong
    );
}

void spawnWeirdReward0(int index, float x, float y, float z, int unk0, int spawn_type, int flag, int unk1) {
    actor_spawn_packet *def = &extra_actor_spawns[index];
    spawnActorWithFlagHandler(def->actor,
        x, y, z, unk0, spawn_type, flag, unk1,
        def->item_level, def->item_kong
    );
}

void spawnBonusReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn bonus reward
     * 
     * @param object Actor Index
     * @param x X Position
     * @param y Y Position
     * @param z Z Position
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    bonus_paad* paad = CurrentActorPointer_0->paad;
    int index = paad->barrel_index;
    if ((index > 0) && (index < BONUS_DATA_COUNT)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != NEWACTOR_NULL) {
        spawnActorWithFlagHandler(object, x, y, z, unk0, cutscene, flag, unk1, bonus_data[index].item_level, bonus_data[index].item_kong);
    }
}

void spawnRewardAtActor(int object, int flag) {
    /**
     * @brief Spawns a reward at the position as an actor, based on the bonus reward table
     * 
     * @param object Actor Index
     * @param flag Flag Index
     */
    int index = CurrentActorPointer_0->reward_index;
    if ((index > 0) && (index < BONUS_DATA_COUNT)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != NEWACTOR_NULL) {
        if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
            spawnActorWithFlagHandler(object,
                CurrentActorPointer_0->xPos,
                CurrentActorPointer_0->yPos,
                CurrentActorPointer_0->zPos,
                0, 0, flag, CurrentActorPointer_0,
                bonus_data[index].item_level,
                bonus_data[index].item_kong
            );
        }
    }
}

void spawnMinecartReward(int object, int flag) {
    /**
     * @brief Spawns a minecart reward at an actor
     * 
     * @param object Actor Index
     * @param flag Flag Index
     */
    for (int i = 0; i < BONUS_DATA_COUNT; i++) {
        if (bonus_data[i].flag == flag) {
            if (bonus_data[i].spawn_actor != NEWACTOR_NULL) {
                spawnActorWithFlagHandler(bonus_data[i].spawn_actor, Player->xPos, Player->yPos, Player->zPos, 0, 0, flag, 0, bonus_data[i].item_level, bonus_data[i].item_kong);
            }
            return;
        }
    }
}

void spawnCrownReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn Crown Reward
     * 
     * @param object Actor Index
     * @param x X Position
     * @param y Y Position
     * @param z Z Position
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int reward_index = getCrownIndex(CurrentMap);
    int new_obj = crown_item_table[reward_index].actor;
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != NEWACTOR_NULL) {
        spawnActorWithFlagHandler(object, x, y, z, unk0, cutscene, flag, unk1, crown_item_table[reward_index].item_level, crown_item_table[reward_index].item_kong);
    }
}

void spawnBossReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn boss reward
     * 
     * @param object Actor Index
     * @param x X Position
     * @param y Y Position
     * @param z Z Position
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int table_index = getKeyIndex(flag);
    int new_obj = key_item_table[table_index].actor;
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != NEWACTOR_NULL) {
        // Protect against null objects
        if ((actor_master_types[object] == ACTORMASTER_SPRITE) && ((CurrentMap == MAP_FUNGIDOGADON) || (CurrentMap == MAP_AZTECDOGADON))) {
            // Sprite & Dogadon Fight
            cutscene = 1;
            x = 475.0f;
            y = 215.0f;
            z = 750.0f;
        } else if ((object != 72) && (CurrentMap == MAP_GALLEONPUFFTOSS)) {
            // Pufftoss - Not a key
            cutscene = 100;
        }
        if ((CurrentMap == MAP_FACTORYJACK) || (CurrentMap == MAP_CAVESDILLO)) {
            // AD2/MJ
            cutscene = 1;
        }
        spawnActorWithFlagHandler(object, x, y, z, unk0, cutscene, flag, unk1, key_item_table[table_index].item_level, key_item_table[table_index].item_kong);
        // Fix items which have short spawn ranges
        ActorSpawnerPointer->spawn_range = 4000000.0f;
    }
}

void spawnDirtPatchReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn dirt patch reward
     * 
     * @param object Actor Index
     * @param x X Position
     * @param y Y Position
     * @param z Z Position
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int idx = flag - FLAG_RAINBOWCOIN_0;
    int new_obj = rcoin_item_table[idx].actor;
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != NEWACTOR_NULL) {
        if (isBounceObject(object)) {
            cutscene = 2;
        }
        spawnActorWithFlagHandler(object, x, y, z, unk0, cutscene, flag, unk1, rcoin_item_table[idx].item_level, rcoin_item_table[idx].item_kong);
    }
}

static const unsigned char pair_data[] = {
	MAP_JAPES,
	MAP_AZTECLLAMATEMPLE,
	MAP_AZTECTINYTEMPLE,
	MAP_FACTORY,
};

void spawnCharSpawnerActor(int actor, SpawnerInfo* spawner) {
    /**
     * @brief Change Character Spawner Information to account for Fairy Rando
     * 
     * @param actor Actor index of the spawned item
     * @param spawner Spawner Object for the spawned item
     */
    if (actor == 248) {
        // Fairy
        int model = 0x3D;
        for (int i = 0; i < 31; i++) {
            if ((charspawnerflags[i].map == CurrentMap) && (charspawnerflags[i].spawner_id == spawner->spawn_trigger)) {
                model = fairy_item_table[charspawnerflags[i].tied_flag - 589].model;
            }
        }
        spawnActor(actor, model);
    } else if (actor == 141) {
        // Cutscene Kong
        int check_index = 0;
        for (int i = 0; i < 4; i++) {
            if (pair_data[i] == CurrentMap) {
                check_index = i;
            }
        }
        spawnActor(actor, kong_check_data[check_index].model);
    } else {
        spawnActor(actor, CharSpawnerActorData[spawner->alt_enemy_value].model);
    }
}

void melonCrateItemHandler(behaviour_data* behaviour_pointer, int index, int p1, int p2) {
    int id = ObjectModel2Pointer[convertSubIDToIndex(index)].object_id;
    int flag = getCrateFlag(id);
    int spawn_count = 1;
    int idx = flag - FLAG_MELONCRATE_0;
    int object = crate_item_table[idx].actor;
    int cutscene = 1;
    if (object == 0x2F) {
        // Junk Item. Set flag as we're spawning 4 unflagged melons and we want it to update check screen
        setPermFlag(flag);
    }
    if (checkFlag(flag, FLAGTYPE_PERMANENT) || (object == NEWACTOR_NULL)) {
        spawn_count = 4;
        flag = -1;
        object = 0x2F;
        cutscene = 1;
    } else if (isBounceObject(object)) {
        cutscene = 2;
    }
    float x = collisionPos[0];
    float y = collisionPos[1] + 15.0f;
    float z = collisionPos[2];
    for (int i = 0; i < spawn_count; i++) {
        spawnActorWithFlagHandler(object, x, y, z, 0x400 * i, cutscene, flag, 0, crate_item_table[idx].item_level, crate_item_table[idx].item_kong);
    }
    unkSpriteRenderFunc_1(1);
    displaySpriteAtXYZ(sprite_table[31], 2.5f, x, y + 15.0f, z);
}

typedef struct steel_keg_struct {
    unsigned char map;
    unsigned char grabbable_id;
    unsigned char spawner_id;
} steel_keg_struct;

static steel_keg_struct SteelKegMapping[] = {
    {.map = MAP_FUNGIMILLFRONT, .grabbable_id = GRABBABLE_MILL_FRONT_NEAR, .spawner_id = 4},
    {.map = MAP_FUNGIMILLFRONT, .grabbable_id = GRABBABLE_MILL_FRONT_FAR, .spawner_id = 6},
    {.map = MAP_FUNGIMILLREAR, .grabbable_id = GRABBABLE_MILL_REAR, .spawner_id = 6},
};

void* updateKegIDs(int actor, float x, float y, float z) {
    int id = getNextUnassignedId();
    int spawner_id = getActorSpawnerIDFromTiedActor(CurrentActorPointer_0);
    for (int i = 0; i < 3; i++) {
        if (CurrentMap == SteelKegMapping[i].map) {
            if (spawner_id == SteelKegMapping[i].spawner_id) {
                updateBoulderId(SteelKegMapping[i].grabbable_id, id);
            }
        }
    }
    return spawnActorAtXYZ(actor, x, y, z);
}

int isValidBoulderObject(int index) {
    if (index < 0) {
        return 0;
    }
    if (HoldableSpawnBitfield & (1 << index)) {
        return 0;
    }
    int flag = FLAG_GRABBABLES_DESTROYED + index;
    if (checkFlag(flag, FLAGTYPE_PERMANENT)) {
        return 0;
    }
    int item = getBoulderItem(index);
    if (item == NEWACTOR_NULL) {
        return 0;
    }
    return item;
}

void spawnBoulderObject(actorData *actor) {
    int index = getBoulderIndex();
    int item = isValidBoulderObject(index);
    if (!item) {
        return;
    }
    int cutscene = 1;
    if (isBounceObject(item)) {
        cutscene = 2;
    }
    spawnActorWithFlagHandler(item,
        actor->xPos,
        actor->yPos,
        actor->zPos,
        0, cutscene,
        FLAG_GRABBABLES_DESTROYED + index, 0,
        boulder_item_table[index].level,
        boulder_item_table[index].kong);
    HoldableSpawnBitfield |= (1 << index);
}

void renderBoulderSparkles(actorData *actor) {
    unkBonusFunction(actor);
    int index = getBoulderIndex();
    int item = isValidBoulderObject(index);
    if (!item) {
        return;
    }
    int timer = ObjectModel2Timer + (index * 5);
    if (timer % 10) {
        return;
    }
    float scale = 1.0f;
    if (index == GRABBABLE_CAVES_LARGE) {
        scale = 3.0f;
    }
    renderSparkles(scale);
}