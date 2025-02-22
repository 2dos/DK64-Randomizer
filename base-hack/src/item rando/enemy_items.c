/**
 * @file enemy_items.c
 * @author Ballaam
 * @brief Enemmy Items
 * @version 0.1
 * @date 2023-09-10
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define ENEMY_ITEM_MAP_CAP 128

static enemy_item_db_item current_map_items[ENEMY_ITEM_MAP_CAP] = {};
unsigned char enemy_rewards_spawned[ENEMY_REWARD_CACHE_SIZE] = {};
static char enemy_db_populated = 0;

void setEnemyDBPopulation(int value) {
    enemy_db_populated = value;
}

void populateEnemyMapData(void) {
    if (enemy_db_populated) {
        return;
    }
    for (int i = 0; i < ENEMY_ITEM_MAP_CAP; i++) {
        current_map_items[i].spawn.actor = 0; // Wipe Cache
        current_map_items[i].spawn.flag = 0; // Wipe Cache
    }
    // Pull table from ROM
    int table_size = ENEMIES_TOTAL * sizeof(enemy_item_rom_item);
    enemy_item_rom_item* enemy_write = getFile(table_size, 0x1FF9000);
    for (int i = 0; i < ENEMIES_TOTAL; i++) {
        if (enemy_write[i].map == CurrentMap) {
            int spawn_id = enemy_write[i].char_spawner_id;
            current_map_items[spawn_id].spawn.actor = enemy_write[i].actor;
            current_map_items[spawn_id].global_index = i;
        }
    }
    setEnemyDBPopulation(1);
}

int getEnemyItem(int id) {
    if (current_map_items[id].spawn.actor != 0) {
        return getActorIndex(current_map_items[id].spawn.actor);
    }
    return -1;
}

int getEnemyFlag(int id) {
    if (current_map_items[id].spawn.actor != 0) {
        return FLAG_ENEMY_KILLED_0 + current_map_items[id].global_index;
    }
    return 0;
}

void wipeEnemySpawnBitfield(void) {
    for (int i = 0; i < ENEMY_REWARD_CACHE_SIZE; i++) {
        enemy_rewards_spawned[i] = 0;
    }
}

void setSpawnBitfield(int id, int state) {
    int offset = id >> 3;
    int shift = id & 7;
    if (state > 0) {
        enemy_rewards_spawned[offset] |= (1 << shift);
    } else {
        enemy_rewards_spawned[offset] &= (0xFF - (1 << shift));
    }
}

void setSpawnBitfieldFromFlag(int flag, int state) {
    if (flag == 0) {
        return;
    }
    for (int i = 0; i < ENEMY_ITEM_MAP_CAP; i++) {
        int proposed_flag = current_map_items[i].global_index + FLAG_ENEMY_KILLED_0;
        if (proposed_flag == flag) {
            setSpawnBitfield(i, state);
            return;
        }
    }
}

int canSpawnEnemyReward(void) {
    int spawn_id = TiedCharacterSpawner->spawn_trigger;
    int offset = spawn_id >> 3;
    int shift = spawn_id & 7;
    if (enemy_rewards_spawned[offset] & (1 << shift)) {
        return 0;
    }
    int flag = getEnemyFlag(spawn_id);
    if (flag == 0) {
        return 0;
    }
    return !checkFlag(flag, FLAGTYPE_PERMANENT);
}

float getRNGWithinRange(float min, float max) {
    // return 0.0f;
    int bytes = getRNGLower31() & 0xFF;
    float ratio = bytes;
    ratio /= 255;
    float offset = (max - min) * ratio;
    return min + offset;
}

void indicateCollectionStatus(void) {
    *(char*)(0x807F94AE) = 0;
    *(char*)(0x807F94AF) = 0;
    *(char*)(0x807F94B0) = 0;
    *(char*)(0x807F94B7) = 0;
    if (!Rando.enemy_item_rando) {
        return;
    }
    int spawn_id = TiedCharacterSpawner->spawn_trigger;
    int timer = ObjectModel2Timer + (spawn_id * 5);
    if (timer % 10) {
        return;
    }
    if (!canSpawnEnemyReward()) {
        return;
    }
    *(char*)(0x807FDB18) = 1; // Adjust Z-Indexing
    *(short*)(0x807FDB36) = 4; // Fix rendering
    float x_offset = getRNGWithinRange(-20.f, 20.0f);
    float y_offset = getRNGWithinRange(5.0f, 25.0f);
    float z_offset = getRNGWithinRange(-20.f, 20.0f);
    int sprite = 0x5E;
    if (getRNGLower31() & 1) {
        sprite = 0x69;
    }
    displaySpriteAtXYZ(
        sprite_table[sprite],
        0.6f,
        CurrentActorPointer_0->xPos + x_offset,
        CurrentActorPointer_0->yPos + y_offset,
        CurrentActorPointer_0->zPos + z_offset);
}


void fireballEnemyDeath(float x, float y, float z, float scale, char unk0, char unk1) {
    spawnFireballExplosion(x, y, z, scale, unk0, unk1);
    spawnEnemyDrops(CurrentActorPointer_0);
    if (Rando.crown_timer_reduction) {
        handleCrownTimerInternal();
    }
}

void rulerEnemyDeath(void) {
    if (CurrentActorPointer_0->control_state == 0x37) {
        if (CurrentActorPointer_0->control_state_progress == 3) {
            spawnEnemyDrops(CurrentActorPointer_0);
        }
    }
    renderActor(CurrentActorPointer_0, 1);
}