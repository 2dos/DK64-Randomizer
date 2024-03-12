/**
 * @file enemy_collision.c
 * @author Ballaam
 * @brief Fixes enemy collisions to respond a bit friendlier to the player regarding shockwave
 * @version 0.1
 * @date 2024-02-25
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "../../include/common.h"

static const int fixed_shockwave_collision[] = {
    0xFFFF0004, 0x80676540,
    0x06030200, 0xFFFF0008,
    0x00000000, 0x06080200,
    0xFFFF0400, 0x00000000,
    0x08000200, 0xFFFF0000, // Set first to 0x08000200 (Disables shockwave dmg), Set second to 0xFFFF0000 (Disables slap dmg)
    0x8067641C, 0x06020200,
    0xFFFF0000, 0x00000000, // Set first to 0xFFFF0000 (Disables roll dmg)
    0x06080200, 0xFFFFFFFF,
    0x80676C10, 0x01020200,
    0xFFFFFFFF, 0x00000000,
    0x01050000,
};

void patchCollision(void) {
    *(int*)(0x8074B53C) = (int)&fixed_shockwave_collision; // Purple Klaptrap
    *(int*)(0x8074B4EC) = (int)&fixed_shockwave_collision; // Red Klaptrap
    *(int*)(0x8074BC24) = (int)&fixed_shockwave_collision; // Book
    *(int*)(0x8074BBF0) = (int)&fixed_shockwave_collision; // All Zingers & Bats
}