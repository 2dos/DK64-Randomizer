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

#define ENEMY_ITEM_MAP_CAP 64

static enemy_item_db_item current_map_items[ENEMY_ITEM_MAP_CAP] = {};
unsigned char enemy_rewards_spawned[8] = {};
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
    enemy_item_rom_item* enemy_write = dk_malloc(table_size);
    int* table_file_size;
    *(int*)(&table_file_size) = table_size;
    copyFromROM(0x1FF9000,enemy_write,&table_file_size,0,0,0,0);
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
    for (int i = 0; i < 8; i++) {
        enemy_rewards_spawned[i] = 0;
    }
}

void setSpawnBitfield(int id) {
    int offset = id >> 3;
    int shift = id & 7;
    enemy_rewards_spawned[offset] |= (1 << shift);
}

void setSpawnBitfieldFromFlag(int flag) {
    if (flag == 0) {
        return;
    }
    for (int i = 0; i < ENEMY_ITEM_MAP_CAP; i++) {
        int proposed_flag = current_map_items[i].global_index + FLAG_ENEMY_KILLED_0;
        if (proposed_flag == flag) {
            setSpawnBitfield(i);
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

void indicateCollectionStatus(void) {
    *(char*)(0x807F94AE) = 0;
    *(char*)(0x807F94AF) = 0;
    *(char*)(0x807F94B0) = 0;
    *(char*)(0x807F94B7) = 0;
    if (!Rando.enemy_item_rando) {
        return;
    }
    if (canSpawnEnemyReward()) {
        return;
    }
    int spawn_id = TiedCharacterSpawner->spawn_trigger;
    int timer = ObjectModel2Timer + (spawn_id * 5);
    if (timer % 7) {
        return;
    }
    *(char*)(0x807FDB1C) = 3;
    int channel = 0xF0;
    changeActorColor(channel, channel, channel, 0xFF);
    *(char*)(0x807FDB18) = 1;
    // CurrentActorPointer_0, 1, 0, 0, 0, 0, -0x50
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    if (CurrentActorPointer_0) {
        updatePosition(CurrentActorPointer_0, 1, &x, &y, &z);
    }
    loadSpriteFunction(0x80718080);
    *(int*)(0x807FDB2C) = -0x50;
    sprite_struct* sprite = displaySpriteAtXYZ((void*)(0x8071FFA0), 1.0f, x, y + 5.0f, z);
    sprite->actor = CurrentActorPointer_0;
}