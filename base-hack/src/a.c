/**
 * @file a.c
 * @author Ballaam
 * @brief File to 16-byte align static_mtx
 * @version 0.1
 * @date 2023-05-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../include/common.h"

/* Anything that is initialized to 0 has to go here */

ROM_DATA mtx_item static_mtx[22];
ROM_DATA move_text_overlay_struct text_overlay_data[TEXT_OVERLAY_BUFFER] = {};
ROM_DATA unsigned int cs_skip_db[2] = {0, 0};
ROM_DATA FastTextStruct hint_pointers[35] = {};
ROM_DATA char* itemloc_pointers[LOCATION_ITEM_COUNT] = {};
ROM_DATA char tag_locked = 0;
ROM_DATA unsigned short guard_tag_timer = 0;
ROM_DATA int force_enable_diving_timer = 0;
ROM_DATA unsigned char HeadSize[MODEL_COUNT];
ROM_DATA int balloon_path_pointers[PATH_CAP];
ROM_DATA patch_db_item patch_flags[16] = {}; // Flag table for dirt patches to differentiate it from balloons
ROM_DATA meloncrate_db_item crate_flags[16] = {}; // Melon crate table
ROM_DATA unsigned int base_text_color = 0x00000000;
ROM_DATA char bonus_shown = 0;
ROM_DATA unsigned char enemy_rewards_spawned[ENEMY_REWARD_CACHE_SIZE] = {};
ROM_DATA ICE_TRAP_TYPES ice_trap_queued = ICETRAP_OFF;
ROM_DATA char enable_skip_check = 0;
ROM_DATA unsigned short GameStats[STAT_TERMINATOR] = {0};
ROM_DATA short file_items[16] = {
    0, 0, 0, 0, // GBs, Crowns, Keys, Medals
    0, 0, 0, 0, // RW, Fairy, Nintendo, BP
    0, 0, 0, 0, // Kongs, Beans, Pearls, Rainbow
    0, 0, 0, 0, // Hints, Crates, Shops
};
ROM_DATA char hints_initialized = 0;
ROM_DATA char display_billboard_fix = 0;
ROM_DATA spoiler_struct spoiler_items[SPOILER_COUNT] = {
    {.flag = 0},
};