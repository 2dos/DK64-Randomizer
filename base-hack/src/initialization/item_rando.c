/**
 * @file item_rando.c
 * @author Ballaam
 * @brief Initializes all item rando elements
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

actor_spawn_packet bp_item_table[40] = {
    // Kasplat Rewards
    {.actor = 78, .item_level=0, .item_kong=KONG_DK},
    {.actor = 75, .item_level=0, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=0, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=0, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=0, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=1, .item_kong=KONG_DK},
    {.actor = 75, .item_level=1, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=1, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=1, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=1, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=2, .item_kong=KONG_DK},
    {.actor = 75, .item_level=2, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=2, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=2, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=2, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=3, .item_kong=KONG_DK},
    {.actor = 75, .item_level=3, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=3, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=3, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=3, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=4, .item_kong=KONG_DK},
    {.actor = 75, .item_level=4, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=4, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=4, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=4, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=5, .item_kong=KONG_DK},
    {.actor = 75, .item_level=5, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=5, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=5, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=5, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=6, .item_kong=KONG_DK},
    {.actor = 75, .item_level=6, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=6, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=6, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=6, .item_kong=KONG_CHUNKY},
    {.actor = 78, .item_level=7, .item_kong=KONG_DK},
    {.actor = 75, .item_level=7, .item_kong=KONG_DIDDY},
    {.actor = 77, .item_level=7, .item_kong=KONG_LANKY},
    {.actor = 79, .item_level=7, .item_kong=KONG_TINY},
    {.actor = 76, .item_level=7, .item_kong=KONG_CHUNKY},
};
item_packet medal_item_table[85] = {
    // Medal Rewards
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
};
item_packet wrinkly_item_table[35] = {
    // Wrinkly Rewards
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_CHUNKY},
};
actor_spawn_packet crown_item_table[10] = {
    // Crown Rewards
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
    {.actor = 86},
};
actor_spawn_packet key_item_table[8] = {
    // Boss Rewards
    {.actor = 72, .item_level=0},
    {.actor = 72, .item_level=1},
    {.actor = 72, .item_level=2},
    {.actor = 72, .item_level=3},
    {.actor = 72, .item_level=4},
    {.actor = 72, .item_level=5},
    {.actor = 72, .item_level=6},
    {.actor = 72, .item_level=7},
};
model_item_data fairy_item_table[20] = {
    // Fairy Rewards
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
};
actor_spawn_packet rcoin_item_table[16] = {
    // Dirt Patch Rewards
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
    {.actor = 0x8C},
};
actor_spawn_packet crate_item_table[16] = {
    // Crate Rewards
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
    {.actor = 0x2F},
};
actor_spawn_packet extra_actor_spawns[2] = {
    {.actor = 45}, // Japes Boulder
    {.actor = 45}, // Aztec Vulture
};
patch_db_item patch_flags[16] = {}; // Flag table for dirt patches to differentiate it from balloons
BoulderItemStruct boulder_item_table[16] = {
    // Holdable Object Rewards
    { .map = MAP_ISLES, .spawner_id = 1},
    { .map = MAP_ISLES, .spawner_id = 1},
    { .map = MAP_AZTEC, .spawner_id = 4},
    { .map = MAP_CAVES, .spawner_id = 0},
    { .map = MAP_CAVES, .spawner_id = 1},
    { .map = MAP_CASTLEMUSEUM, .spawner_id = 0},
    { .map = MAP_JAPESLOBBY, .spawner_id = 2},
    { .map = MAP_CASTLELOBBY, .spawner_id = 0},
    { .map = MAP_CAVESLOBBY, .spawner_id = 5},
    { .map = MAP_FUNGIMILLFRONT, .spawner_id = 5},
    { .map = MAP_FUNGIMILLFRONT, .spawner_id = 7},
    { .map = MAP_FUNGIMILLREAR, .spawner_id = 4},
    { .map = MAP_AZTEC, .spawner_id = 3},
    { .map = MAP_AZTEC, .spawner_id = 2},
    { .map = MAP_AZTEC, .spawner_id = 1},
    { .map = MAP_AZTEC, .spawner_id = 0},
};
bonus_barrel_info bonus_data[BONUS_DATA_COUNT] = {
    {.flag=0x186,               .spawn_actor=45,                    .kong_actor=1},
    {.flag=0xe0,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1c4,               .spawn_actor=45,                    .kong_actor=0},
    {.flag=0x131,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x132,               .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x2,                 .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1,                 .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1c,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x87,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0xe3,                .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0xeb,                .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0x86,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x88,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x89,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0xb,                 .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x74,                .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x3c,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x3b,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x107,               .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x137,               .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x13b,               .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0xd3,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x49,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0xa3,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0xa4,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x13c,               .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x3e,                .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0x34,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x13f,               .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x44,                .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x18,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0xb8,                .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x18e,               .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x192,               .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x194,               .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0x13e,               .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0xfe,                .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0x196,               .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x19a,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x19f,               .spawn_actor=45,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1a0,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1a8,               .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1a9,               .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1ac,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x126,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x127,               .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x12a,               .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0xc6,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0xc5,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0xc8,                .spawn_actor=45,                    .kong_actor=2 + KONG_DK},
    {.flag=0xca,                .spawn_actor=45,                    .kong_actor=2 + KONG_TINY},
    {.flag=0xfa,                .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x19,                .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x15e,               .spawn_actor=45,                    .kong_actor=2 + KONG_DIDDY},
    // Kasplat Rewards
    {.flag=0x1d5,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1d6,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1d7,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1d8,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1d9,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1da,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1db,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1dc,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1dd,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1de,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1df,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1e0,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1e1,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1e2,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1e3,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1e4,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1e5,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1e6,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1e7,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1e8,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1e9,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1ea,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1eb,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1ec,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1ed,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1ee,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1ef,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1f0,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1f1,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1f2,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1f3,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1f4,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1f5,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1f6,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1f7,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    {.flag=0x1f8,               .spawn_actor=78,                    .kong_actor=2 + KONG_DK},
    {.flag=0x1f9,               .spawn_actor=75,                    .kong_actor=2 + KONG_DIDDY},
    {.flag=0x1fa,               .spawn_actor=77,                    .kong_actor=2 + KONG_LANKY},
    {.flag=0x1fb,               .spawn_actor=79,                    .kong_actor=2 + KONG_TINY},
    {.flag=0x1fc,               .spawn_actor=76,                    .kong_actor=2 + KONG_CHUNKY},
    // Misc
    {.flag=215,                 .spawn_actor=45,                    .kong_actor=2 + KONG_CHUNKY},  // Chunky Minecart
    {.flag=FLAG_TBARREL_DIVE,   .spawn_actor=NEWACTOR_POTIONANY,    .kong_actor=0},
    {.flag=FLAG_TBARREL_VINE,   .spawn_actor=NEWACTOR_POTIONANY,    .kong_actor=0},
    {.flag=FLAG_TBARREL_ORANGE, .spawn_actor=NEWACTOR_POTIONANY,    .kong_actor=0},
    {.flag=FLAG_TBARREL_BARREL, .spawn_actor=NEWACTOR_POTIONANY,    .kong_actor=0},
};
meloncrate_db_item crate_flags[16] = {}; // Melon crate table
model_item_data kong_check_data[4] = {
    // Kong table
    {.model =  1, .item = {.item_type = REQITEM_KONG, .kong = KONG_DIDDY}},
    {.model =  6, .item = {.item_type = REQITEM_KONG, .kong = KONG_LANKY}},
    {.model =  9, .item = {.item_type = REQITEM_KONG, .kong = KONG_TINY}},
    {.model = 12, .item = {.item_type = REQITEM_KONG, .kong = KONG_CHUNKY}},
};
item_packet company_coin_table[2] = {
    {.item_type = REQITEM_COMPANYCOIN, .kong = 0}, // Nintendo Coin
    {.item_type = REQITEM_COMPANYCOIN, .kong = 1}, // Rareware Coin
};

int getCrownIndex(maps map) {
    /**
     * @brief Get Crown item from map index
     * 
     * @param map Map Index
     * 
     * @return Actor Index of the reward
     */
	for (int i = 0; i < 10; i++) {
		if (map == crown_maps[i]) {
			return i;
		}
	}
	return 0;
}

int getKeyIndex(int old_flag) {
    /**
     * @brief Get Boss Reward from the original flag
     * 
     * @param old_flag Original Flag of the reward
     * 
     * @return Actor Index of the reward
     */
	for (int i = 0; i < 8; i++) {
		if (old_flag == normal_key_flags[i]) {
			return i;
		}
	}
	return 0;
}

int getPatchFlag(int id) {
    /**
     * @brief Get Patch flag from the ID of the patch
     * 
     * @param id Patch ID inside the map
     * 
     * @return flag index of the patch
     */
	for (int i = 0; i < 16; i++) {
		if (CurrentMap == patch_flags[i].map) {
			if (id == patch_flags[i].id) {
				return FLAG_RAINBOWCOIN_0 + i;
			}
		}
	}
	return 0;
}

int getPatchWorld(int index) {
    /**
     * @brief Gets the world which the patch is in
     * 
     * @param index Patch Index inside the flag table
     * 
     * @return World index of the patch
     */
	return patch_flags[index].world;
}

int getCrateFlag(int id) {
    /**
     * @brief Get Melon Crate flag from the ID of the Melon Crate
     * 
     * @param id Melon Crate ID inside the map
     * 
     * @return flag index of the crate
     */
	for (int i = 0; i < 16; i++) {
		if (CurrentMap == crate_flags[i].map) {
			if (id == crate_flags[i].id) {
				return FLAG_MELONCRATE_0 + i;
			}
		}
	}
	return 0;
}

int getCrateWorld(int index) {
    /**
     * @brief Gets the world which the melon crate is in
     * 
     * @param index Crate Index inside the flag table
     * 
     * @return World index of the crate
     */
	return crate_flags[index].world;
}

void populatePatchItem(int id, int map, int index, int world) {
    /**
     * @brief Populate the patch table with a dirt patch
     * 
     * @param id Patch ID
     * @param map Patch Map
     * @param index Index inside the patch table
     * @param world World where the patch is
     */
    patch_flags[index].id = id;
    patch_flags[index].map = map;
    patch_flags[index].world = world;
}

void populateCrateItem(int id, int map, int index, int world) {
    /**
     * @brief Populate the Crate table with a Melon Crate
     * 
     * @param id Crate ID
     * @param map Crate Map
     * @param index Index inside the Crate table
     * @param world World where the Crate is
     */
    crate_flags[index].id = id;
    crate_flags[index].map = map;
    crate_flags[index].world = world;
}

int getBonusFlag(int index) {
    /**
     * @brief Get bonus barrel flag from barrel index
     * 
     * @param index Barrel Index
     * 
     * @return Flag index
     */
    if (index == 0) {
        return -1;
    }
    return bonus_data[index].flag;
}

void updateBoulderId(int index, int id) {
    boulder_item_table[index].spawner_id = id;
}

int getBoulderIndex(void) {
    int id = getActorSpawnerIDFromTiedActor(CurrentActorPointer_0);
    for (int i = 0; i < 16; i++) {
        if (boulder_item_table[i].map == CurrentMap) {
            if (boulder_item_table[i].spawner_id == id) {
                return i;
            }
        }
    }
    return -1;
}

int getBoulderItem(int index) {
    if (index < 0) {
        return 0;
    }
    return boulder_item_table[index].item;
}

typedef struct barrel_skin_tie {
    /* 0x000 */ unsigned short actor;
    /* 0x002 */ unsigned char reqitem;
    /* 0x003 */ unsigned char skin;
    /* 0x004 */ char level;
    /* 0x005 */ char kong;
} barrel_skin_tie;

static const barrel_skin_tie bonus_skins[] = {
    {.actor = 78,                               .reqitem=REQITEM_BLUEPRINT,         .level=-1, .kong=-1, .skin=SKIN_BLUEPRINT},
    {.actor = 75,                               .reqitem=REQITEM_BLUEPRINT,         .level=-1, .kong=-1, .skin=SKIN_BLUEPRINT},
    {.actor = 77,                               .reqitem=REQITEM_BLUEPRINT,         .level=-1, .kong=-1, .skin=SKIN_BLUEPRINT},
    {.actor = 79,                               .reqitem=REQITEM_BLUEPRINT,         .level=-1, .kong=-1, .skin=SKIN_BLUEPRINT},
    {.actor = 76,                               .reqitem=REQITEM_BLUEPRINT,         .level=-1, .kong=-1, .skin=SKIN_BLUEPRINT},
    {.actor = NEWACTOR_NINTENDOCOIN,            .reqitem=REQITEM_COMPANYCOIN,       .level=-1, .kong= 0, .skin=SKIN_NINTENDO_COIN},
    {.actor = NEWACTOR_RAREWARECOIN,            .reqitem=REQITEM_COMPANYCOIN,       .level=-1, .kong= 1, .skin=SKIN_RAREWARE_COIN},
    {.actor = 72,                               .reqitem=REQITEM_KEY,               .level=-1, .kong=-1, .skin=SKIN_KEY},
    {.actor = 86,                               .reqitem=REQITEM_CROWN,             .level=-1, .kong=-1, .skin=SKIN_CROWN},
    {.actor = NEWACTOR_MEDAL,                   .reqitem=REQITEM_MEDAL,             .level=-1, .kong=-1, .skin=SKIN_MEDAL},
    {.actor = NEWACTOR_POTIONDK,                .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONDIDDY,             .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONLANKY,             .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONTINY,              .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONCHUNKY,            .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONANY,               .reqitem=REQITEM_MOVE,              .level=-1, .kong=-1, .skin=SKIN_POTION},
    {.actor = NEWACTOR_KONGDK,                  .reqitem=REQITEM_KONG,              .level=-1, .kong= 0, .skin=SKIN_KONG_DK},
    {.actor = NEWACTOR_KONGDIDDY,               .reqitem=REQITEM_KONG,              .level=-1, .kong= 1, .skin=SKIN_KONG_DIDDY},
    {.actor = NEWACTOR_KONGLANKY,               .reqitem=REQITEM_KONG,              .level=-1, .kong= 2, .skin=SKIN_KONG_LANKY},
    {.actor = NEWACTOR_KONGTINY,                .reqitem=REQITEM_KONG,              .level=-1, .kong= 3, .skin=SKIN_KONG_TINY},
    {.actor = NEWACTOR_KONGCHUNKY,              .reqitem=REQITEM_KONG,              .level=-1, .kong= 4, .skin=SKIN_KONG_CHUNKY},
    {.actor = NEWACTOR_BEAN,                    .reqitem=REQITEM_BEAN,              .level=-1, .kong=-1, .skin=SKIN_BEAN},
    {.actor = NEWACTOR_PEARL,                   .reqitem=REQITEM_PEARL,             .level=-1, .kong=-1, .skin=SKIN_PEARL},
    {.actor = NEWACTOR_FAIRY,                   .reqitem=REQITEM_FAIRY,             .level=-1, .kong=-1, .skin=SKIN_FAIRY},
    {.actor = 140,                              .reqitem=REQITEM_RAINBOWCOIN,       .level=-1, .kong=-1, .skin=SKIN_RAINBOW_COIN},
    {.actor = NEWACTOR_ICETRAPGB,               .reqitem=REQITEM_ICETRAP,           .level= 0, .kong=-1, .skin=SKIN_FAKE_ITEM},
    {.actor = 0x2F,                             .reqitem=REQITEM_JUNK,              .level=-1, .kong=-1, .skin=SKIN_JUNK_ITEM},
    {.actor = NEWACTOR_CRANKYITEM,              .reqitem=REQITEM_SHOPKEEPER,        .level=-1, .kong= 0, .skin=SKIN_CRANKY},
    {.actor = NEWACTOR_FUNKYITEM,               .reqitem=REQITEM_SHOPKEEPER,        .level=-1, .kong= 1, .skin=SKIN_FUNKY},
    {.actor = NEWACTOR_CANDYITEM,               .reqitem=REQITEM_SHOPKEEPER,        .level=-1, .kong= 2, .skin=SKIN_CANDY},
    {.actor = NEWACTOR_SNIDEITEM,               .reqitem=REQITEM_SHOPKEEPER,        .level=-1, .kong= 3, .skin=SKIN_SNIDE},
    {.actor = NEWACTOR_ICETRAPBEAN,             .reqitem=REQITEM_ICETRAP,           .level= 1, .kong=-1, .skin=SKIN_FAKE_BEAN},
    {.actor = NEWACTOR_ICETRAPKEY,              .reqitem=REQITEM_ICETRAP,           .level= 2, .kong=-1, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPFAIRY,            .reqitem=REQITEM_ICETRAP,           .level= 3, .kong=-1, .skin=SKIN_FAKE_FAIRY},
    {.actor = NEWACTOR_HINTITEMDK,              .reqitem=REQITEM_HINT,              .level=-1, .kong=-1, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMDIDDY,           .reqitem=REQITEM_HINT,              .level=-1, .kong=-1, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMLANKY,           .reqitem=REQITEM_HINT,              .level=-1, .kong=-1, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMTINY,            .reqitem=REQITEM_HINT,              .level=-1, .kong=-1, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMCHUNKY,          .reqitem=REQITEM_HINT,              .level=-1, .kong=-1, .skin=SKIN_HINT},
    {.actor = NEWACTOR_ARCHIPELAGOITEM,         .reqitem=REQITEM_AP,                .level=-1, .kong=-1, .skin=SKIN_AP},
};

enum_bonus_skin getBarrelSkinIndex(int actor) {
    for (int i = 0; i < (sizeof(bonus_skins) / sizeof(barrel_skin_tie)); i++) {
        if (bonus_skins[i].actor == actor) {
            return bonus_skins[i].skin;
        }
    }
    return SKIN_GB;
}

enum_bonus_skin getShopSkinIndex(purchase_struct *data) {
    for (int i = 0; i < (sizeof(bonus_skins) / sizeof(barrel_skin_tie)); i++) {
        if (bonus_skins[i].reqitem == data->item.item_type) {
            if ((bonus_skins[i].level == -1) || (bonus_skins[i].level == data->item.level)) {
                if ((bonus_skins[i].kong == -1) || (bonus_skins[i].kong == data->item.kong)) {
                    return bonus_skins[i].skin;
                }
            }
        }
    }
    return SKIN_GB;
}

int alterBonusVisuals(int index) {
    if (Rando.location_visuals.bonus_barrels) {
        if (index < BONUS_DATA_COUNT) {
            int actor = bonus_data[index].spawn_actor;
            enum_bonus_skin skin = getBarrelSkinIndex(actor);
            if (skin != SKIN_GB) {
                for (int i = 0; i < 2; i++) {
                    //retextureZone(CurrentActorPointer_0, i, skin);
                    blink(CurrentActorPointer_0, i, 1);
                    applyImageToActor(CurrentActorPointer_0, i, 0);
                    adjustColorPalette(CurrentActorPointer_0, i, skin, 0.0f);
                    unkPaletteFunc(CurrentActorPointer_0, i, 0);
                }
            }
        }
    }
    return getBonusFlag(index);
}

int getDirtPatchSkin(int flag, flagtypes flag_type) {
    if (checkFlag(flag, flag_type)) {
        return 1;
    }
    if (Rando.location_visuals.dirt_patches) {
        int index = flag - FLAG_RAINBOWCOIN_0;
        if (index < 16) {
            int actor = rcoin_item_table[flag - FLAG_RAINBOWCOIN_0].actor;
            enum_bonus_skin skin = getBarrelSkinIndex(actor);
            blink(CurrentActorPointer_0, 0, 1);
            applyImageToActor(CurrentActorPointer_0, 0, 0);
            adjustColorPalette(CurrentActorPointer_0, 0, skin + 1, 0.0f);
            unkPaletteFunc(CurrentActorPointer_0, 0, 0);
        }
    }
    return 0;
}

void initItemRando(void) {
    /**
     * @brief Initialize Item Rando functionality
     */
        
    // Checks Screen
    pausescreenlist screen_count = PAUSESCREEN_TERMINATOR; // 4 screens vanilla + hint screen + check screen + move tracker
    *(short*)(0x806A8672) = screen_count - 1; // Screen decrease cap
    *(short*)(0x806A8646) = screen_count; // Screen increase cap

    // Head Size - It shouldn't be here, but haha funny game crash if placed in base init
    int load_size = 0xED;
    unsigned char* head_write = getFile(load_size, 0x1FEE800);
    for (int i = 0; i < load_size; i++) {
        HeadSize[i] = head_write[i];
    }
    // Other init
    initActorDefs();
}