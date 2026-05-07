/**
 * @file carousel.c
 * @author Ballaam
 * @brief Item Carousel Functions
 * @version 0.1
 * @date 2023-10-11
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

PauseItemStruct pause_items[CHECK_TERMINATOR] = {
    { .sprite_index = 9,                        .item_cap = 201 }, // GB
    { .sprite_pointer = (void*)0x807210EC,      .item_cap = 10 }, // Crown
    { .sprite_pointer = (void*)0x807210B8,      .item_cap = 8 }, // Key
    { .sprite_index = 0xA,                      .item_cap = 40 }, // Medals
    { .sprite_pointer = (void*)0x80721110,      .item_cap = 1 }, // RW
    { .sprite_pointer = (void*)0x80721094,      .item_cap = 20 }, // Fairies
    { .sprite_pointer = (void*)0x80721134,      .item_cap = 1 }, // Nintendo
    { .sprite_index = 0xC,                      .item_cap = 40 }, // BP
    { .sprite_pointer = (void*)0x807214A0,      .item_cap = 5 }, // Kong
    { .sprite_pointer = &bean_sprite,           .item_cap = 1 }, // Bean
    { .sprite_pointer = &pearl_sprite,          .item_cap = 5 }, // Pearls
    { .sprite_pointer = (void*)0x80721378,      .item_cap = 16 }, // Rainbow Coins
    { .sprite_pointer = (void*)0x80721530,      .item_cap = 35 }, // Hint
    { .sprite_pointer = (void*)0x80720710,      .item_cap = 0 }, // Crate
    { .sprite_pointer = &potion_sprite,         .item_cap = 42 }, // Shops
    { .sprite_pointer = (void*)0x80721238,      .item_cap = 0 }, // Snide Rewards
    { .sprite_pointer = &boulder_sprite,        .item_cap = 0 }, // Holdables
    { .sprite_pointer = (void*)0x8071FFD4,      .item_cap = 0 }, // Enemy Drops
    { .sprite_pointer = &halfmedal_sprite,        .item_cap = 0 }, // Half-Medals
};

void updatePauseScreenWheel(pause_paad* write_location, void* sprite, int x, int y, float scale, int local_index, int index) {
    /**
     * @brief Update the pause screen wheel to be a carousel instead.
     */
    int control = 16;
    ItemsInWheel = CHECK_TERMINATOR - ROTATION_TOTALS_REDUCTION;
    if (write_location->screen == PAUSESCREEN_CHECKS) {
        control = 17;
        ItemsInWheel = CHECK_TERMINATOR;
    }
    if (local_index >= ItemsInWheel) {
        return;
    }
    displaySprite(write_location, sprite, local_index, 0x78, 1.0f, 2, control);
}

void newPauseSpriteCode(sprite_struct* sprite, char* render, int is_totals) {
    /**
     * @brief Sprite code for the carousel pause screen effect
     */
    spriteControlCode(sprite, render);
    pause_paad* pause_control = (pause_paad*)sprite->control;
    // Define Rotaion Parameters
    int rotation = ROTATION_SPLIT;
    int item_cap = CHECK_TERMINATOR;
    if (is_totals) {
        rotation = ROTATION_SPLIT_TOTALS;
        // item_cap = CHECK_TERMINATOR - ROTATION_TOTALS_REDUCTION;
    }
    // Width information
    float width = 640.0f;
    float right_bound = width * 1.5f;
    float left_bound = width * 0.5f;
    float quarter_width = width / 4.0f;
    float width_diff = width / 8.0f;
    int width_diff_int = width_diff;

    int index = sprite->unk384[2] / 4;
    int viewed_item = ((float)(pause_control->control) / rotation);
    int diff = index - viewed_item;
    if (diff == (item_cap - 1)) {
        diff = -1;
    } else if (diff == (item_cap - 2)) {
        diff = -2;
    } else if (diff == (1 - item_cap)) {
        diff = 1;
    } else if (diff == (2 - item_cap)) {
        diff = 2;
    }
    int pos_diff = diff;
    if (pos_diff > 0) {
        pos_diff += 1;
    } else  if (pos_diff < 0) {
        pos_diff -= 1;
    }
    float diff_increment = ((pause_control->control - (rotation * viewed_item)) * width_diff_int * item_cap) >> 12;
    if ((pos_diff >= 3) || (pos_diff <= -2)) {
        diff_increment /= 2;
    }
    

    sprite->x = (quarter_width + (pos_diff * (width_diff / 2.0f)) - diff_increment) * 4;
    float scale = 0.0f;
    if (sprite->x > width) {
        // Right of center
        if (sprite->x < right_bound) {
            // 8-4
            float x_diff = width - sprite->x;
            scale = 8.0f + (x_diff / width_diff);
        } else {
            // 4-2-0
            float x_diff = right_bound - sprite->x;
            scale = 4.0f + (x_diff / width_diff);
            if (scale < 0.0f) {
                scale = 0.0f;
            }
        }
    } else if (sprite->x < width) {
        // Left of center
        if (sprite->x > left_bound) {
            // 4-8
            float x_diff = width - sprite->x;
            scale = 8.0f - (x_diff / width_diff);
        } else {
            // 0-2-4
            float x_diff = left_bound - sprite->x;
            scale = 4.0f - (x_diff / width_diff);
            if (scale < 0.0f) {
                scale = 0.0f;
            }
        }
    } else {
        scale = 8.0f;
    }
    int brightness = scale * 32;
    if (brightness > 255) {
        brightness = 255;
    }
    sprite->scale_x = scale;
    sprite->scale_z = scale;
    sprite->red = brightness;
    sprite->green = brightness;
    sprite->blue = brightness;
}

void totalsSprite(sprite_struct* sprite, char* render) {
    newPauseSpriteCode(sprite, render, 1);
}

void checksSprite(sprite_struct* sprite, char* render) {
    newPauseSpriteCode(sprite, render, 0);
}

void initCarousel_onPause(void) {
    for (int i = 0; i < 8; i++) {
        pause_items[i].item_count = FileVariables[i];
    }
    pause_items[CHECK_PEARLS].item_count = getItemCount_new(REQITEM_PEARL, 0, 0);
    pause_items[CHECK_RAINBOW].item_count = getItemCount_new(REQITEM_RAINBOWCOIN, 0, 0);
    pause_items[CHECK_HINTS].item_count = getItemCount_new(REQITEM_HINT, -1, -1);
    pause_items[CHECK_BEAN].item_count = getItemCount_new(REQITEM_BEAN, 0, 0);
    pause_items[CHECK_KONG].item_count = getItemCount_new(REQITEM_KONG, -1, -1);
    pause_items[CHECK_CRATE].item_count = getItemCount_new(REQITEM_JUNK, 0, 0);
    pause_items[CHECK_SHOPS].item_count = getTotalMoveCount();
    pause_items[CHECK_KEY].item_count = getItemCount_new(REQITEM_KEY, -1, -1);
}