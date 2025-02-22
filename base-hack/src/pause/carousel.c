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

short file_items[16] = {
    0, 0, 0, 0, // GBs, Crowns, Keys, Medals
    0, 0, 0, 0, // RW, Fairy, Nintendo, BP
    0, 0, 0, 0, // Kongs, Beans, Pearls, Rainbow
    0, 0, 0, 0, // Hints, Crates
};

int file_sprites[17] = {
    0x9, // GB
    0x807210EC, // Crown
    0x807210B8, // Key
    0xA, // Medals
    0x80721110, // RW
    0x80721094, // Fairies
    0x80721134, // Nintendo
    0xC, // BP
    0x807214A0, // Kong
    (int)&bean_sprite, // Bean
    (int)&pearl_sprite, // Pearls
    0x80721378, // Rainbow Coins
    0x80721530, // Hint
    0x80720710, // Crate
    0, 0,
    0, // Null Item, Leave Empty
};
short file_item_caps[16] = {
    201, 10, 8, 40,
    1, 20, 1, 40,
    5, 1, 5, 16,
    35, 0, 0, 0, // Second here is Junk Items
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

void handleSpriteCode(int control_type) {
    /**
     * @brief Changes sprite code to be the carousel effect if the index is greater than 16
     * 
     * @param control_type Type of sprite that's being displayed and the controls you have access to
     */
    if (control_type < 16) {
        loadSpriteFunction(0x806AC07C);
    } else if (control_type == 16) {
        loadSpriteFunction((int)&totalsSprite);
    } else if (control_type == 17) {
        loadSpriteFunction((int)&checksSprite);
    }
}

typedef struct CarouselBoundStruct {
    /* 0x000 */ unsigned char check_type;
    /* 0x001 */ unsigned char flag_count;
    /* 0x002 */ short starting_flag;
} CarouselBoundStruct;

static CarouselBoundStruct carousel_bounds[] = {
    {.check_type = CHECK_CRATE, .flag_count = ENEMIES_TOTAL, .starting_flag = FLAG_ENEMY_KILLED_0}, // Make sure this is always first
    {.check_type = CHECK_PEARLS, .flag_count = 5, .starting_flag = FLAG_PEARL_0_COLLECTED},
    {.check_type = CHECK_RAINBOW, .flag_count = 16, .starting_flag = FLAG_RAINBOWCOIN_0},
    {.check_type = CHECK_HINTS, .flag_count = 35, .starting_flag = FLAG_WRINKLYVIEWED},
    {.check_type = CHECK_BEAN, .flag_count = 1, .starting_flag = FLAG_COLLECTABLE_BEAN},
};

void initCarousel_onPause(void) {
    for (int i = 0; i < 8; i++) {
        file_items[i] = FileVariables[i];
    }
    if (!Rando.enemy_item_rando) {
        carousel_bounds[0].flag_count = 0;
    }
    file_items[CHECK_KONG] = 0;
    for (int i = 0; i < 5; i++) {
        int check_type = carousel_bounds[i].check_type;
        int start_flag = carousel_bounds[i].starting_flag;
        int count = carousel_bounds[i].flag_count;
        file_items[check_type] = 0;
        for (int j = 0; j < count; j++) {
            file_items[check_type] += checkFlagDuplicate(start_flag + j, FLAGTYPE_PERMANENT);
        }
        file_items[CHECK_KONG] += checkFlagDuplicate(kong_flags[i], FLAGTYPE_PERMANENT);
    }
    for (int i = 0; i < 100; i++) {
        // Junk Item Check
        if (isIceTrapFlag(FLAG_JUNKITEM + i) == DYNFLAG_JUNK) {
            file_items[CHECK_CRATE] += checkFlagDuplicate(FLAG_JUNKITEM + i, FLAGTYPE_PERMANENT);
        }
    }
}

void initCarousel_onBoot(void) {
    if (Rando.isles_cb_rando) {
        file_item_caps[3] = 45;
    }
    *(short*)(0x806AB2CE) = getHi(&file_items[CHECK_TERMINATOR]);
    *(short*)(0x806AB2D6) = getLo(&file_items[CHECK_TERMINATOR]);
    *(short*)(0x806AB3F6) = CHECK_TERMINATOR;
}