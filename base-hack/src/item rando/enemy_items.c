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
static char enemy_db_populated = 0;

void setEnemyDBPopulation(int value) {
    enemy_db_populated = value;
}

void populateEnemyMapData(void) {
    if (enemy_db_populated) {
        return;
    }
    for (int i = 0; i < ENEMY_ITEM_MAP_CAP; i++) {
        current_map_items[i].spawn.flag = 0; // Wipe Cache
    }
    // Pull table from ROM
    int table_size = ENEMIES_TOTAL * sizeof(enemy_item_rom_item);
    enemy_item_rom_item* enemy_write = dk_malloc(table_size);
    int* table_file_size;
    *(int*)(&table_file_size) = table_size;
    copyFromROM(0x1FF1000,enemy_write,&table_file_size,0,0,0,0);
    for (int i = 0; i < ENEMIES_TOTAL; i++) {
        if (enemy_write[i].map == CurrentMap) {
            int spawn_id = enemy_write[i].char_spawner_id;
            current_map_items[spawn_id].spawn.actor = enemy_write[i].spawn_data.actor;
            current_map_items[spawn_id].spawn.flag = enemy_write[i].spawn_data.flag;
            current_map_items[spawn_id].global_index = i;
        }
    }
    setEnemyDBPopulation(1);
}

int getEnemyItem(int id) {
    if (current_map_items[id].spawn.flag != 0) {
        if (current_map_items[id].spawn.actor != 0) {
            return current_map_items[id].spawn.actor;
        }
    }
    return -1;
}

int getEnemyFlag(int id) {
    if (current_map_items[id].spawn.flag != 0) {
        if (current_map_items[id].spawn.actor != 0) {
            return FLAG_ENEMY_KILLED_0 + current_map_items[id].global_index;
        }
    }
    return 0;
}