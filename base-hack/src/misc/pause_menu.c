/**
 * @file pause_menu.c
 * @author Ballaam
 * @brief Pause Menu functions
 * @version 0.1
 * @date 2022-10-03
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static char igt_text[20] = "IGT: 0000:00:00";
static int stored_igt = 0;
static char hint_region_text[32] = "";

int* printLevelIGT(int* dl, int x, int y, float scale, char* str) {
    /**
     * @brief Print Level In-Game time to screen
     */
    dl = printText(dl, x, y, scale, str);
    int level_index = -1;
    for (int i = 0; i < 12; i++) {
        if ((int)LevelNamesPointer[i] == (int)str) {
            level_index = i;
        }
    }
    int igt_data = 0;
    if (level_index < 9) {
        igt_data = ReadExtraData(EGD_LEVELIGT, level_index);
    }
    int igt_h = igt_data / 3600;
    int igt_m = (igt_data / 60) % 60;
    int igt_s = igt_data % 60;
    if (igt_data < 3600) {
        dk_strFormat(igt_text, "TIME: %02d:%02d", igt_m, igt_s);
    } else {
        dk_strFormat(igt_text, "TIME: %d:%02d:%02d", igt_h, igt_m, igt_s);
    }
    dl = printText(dl, x, y + 0x38, 0.5f, (char*)igt_text);
    return dl;
}

static char* levels[] = {
    "ALL",
    "JUNGLE JAPES",
    "ANGRY AZTEC",
    "FRANTIC FACTORY",
    "GLOOMY GALLEON",
    "FUNGI FOREST",
    "CRYSTAL CAVES",
    "CREEPY CASTLE",
    "DK ISLES",
    "HIDEOUT HELM",
};
static char* items[] = {
    "GOLDEN BANANAS",
    "CROWN PADS",
    "BOSSES AND FINAL KEY",
    "BANANA MEDALS",
    "JETPAC",
    "BANANA FAIRIES",
    "DK ARCADE",
    "KASPLATS",
    "KONG CAGES",
    "ANTHILL SECOND REWARD",
    "TREASURE CHEST CLAMS",
    "DIRT PATCHES",
    "MELON CRATES",
};
static char* raw_items[] = {
    "GOLDEN BANANAS",
    "BATTLE CROWNS",
    "BOSS KEYS",
    "BANANA MEDALS",
    "RAREWARE COIN",
    "BANANA FAIRIES",
    "NINTENDO COIN",
    "BLUEPRINTS",
    "KONGS",
    "BEAN",
    "PEARLS",
    "RAINBOW COINS",
    "JUNK ITEMS",
};

static char check_level = 0;
static char hint_level = 0;
static char level_check_text[0x18] = "";
static char level_hint_text[0x18] = "";

static unsigned char check_data[2][9][CHECK_TERMINATOR] = {}; // 8 items, 9 levels, numerator + denominator

static char hints_initialized = 0;

static char display_billboard_fix = 0;

void initHints(void) {
    if (!hints_initialized) {
        for (int i = 0; i < 35; i++) {
            hint_pointers[i] = (int)getTextPointer(41, 1+i, 0);
        }
        hints_initialized = 1;
    }
    display_billboard_fix = 0;
}

void wipeHintCache(void) {
    for (int i = 0; i < 35; i++) {
        hint_pointers[i] = 0;
    }
    hints_initialized = 0;
}

void checkItemDB(void) {
    /**
     * @brief Check item database for variables, and change check screen totals to accommodate
     */
    if ((!Rando.true_widescreen) || (!WS_REMOVE_TRANSITIONS)) {
        renderScreenTransition(7);
    }
    initTracker();
    initHints();
    stored_igt = getNewSaveTime();
    if (Rando.helm_hurry_mode) {
        if (ReadFile(DATA_HELMHURRYOFF, 0, 0, 0)) {
            stored_igt = IGT;
        }
    }
    for (int i = 0; i < CHECK_TERMINATOR; i++) {
        // Wipe data upon every search
        for (int j = 0; j < 9; j++) {
            check_data[0][j][i] = 0;
            check_data[1][j][i] = 0;
        }
        // Check FLUT
        for (int k = 0; k < (sizeof(item_db) / sizeof(check_struct)); k++) {
            if (item_db[k].type == i) {
                int search_flag = item_db[k].flag;
                int lvl = item_db[k].associated_level;
                check_data[0][lvl][i] += checkFlag(search_flag, FLAGTYPE_PERMANENT);
            }
        }
        // Check Rainbow Flags
        if (i == CHECK_RAINBOW) {
            for (int k = 0; k < 16; k++) {
                int search_flag = FLAG_RAINBOWCOIN_0 + k;
                int lvl = getPatchWorld(k);
                check_data[0][lvl][i] += checkFlag(search_flag, FLAGTYPE_PERMANENT);
            }
        } else if (i == CHECK_CRATE) {
            for (int k = 0; k < 13; k++) {
                int search_flag = FLAG_MELONCRATE_0 + k;
                int lvl = getCrateWorld(k);
                check_data[0][lvl][i] += checkFlag(search_flag, FLAGTYPE_PERMANENT);
            }
        }
        // Get Denominator
        for (int j = 0; j < 9; j++) {
            int denominator = 0;
            switch (i) {
                case CHECK_GB:
                    if (j < 8) {
                        if (j == 7) {
                            denominator = 21;
                        } else {
                            denominator = 20;
                        }
                    }
                    break;
                case CHECK_CROWN:
                    if (j == 7) {
                        denominator = 2;
                    } else {
                        denominator = 1;
                    }
                    break;
                case CHECK_KEY:
                    if (j != 7) {
                        denominator = 1;
                    }
                    break;
                case CHECK_MEDAL:
                    if (j != 7) {
                        denominator = 5;
                    }
                    break;
                case CHECK_RWCOIN:
                case CHECK_NINCOIN:
                    check_data[1][0][i] = 1;
                    break;
                case CHECK_FAIRY:
                    if (j == 7) {
                        denominator = 4;
                    } else {
                        denominator = 2;
                    }
                    break;
                case CHECK_BP:
                    if (j < 8) {
                        denominator = 5;
                    }
                    break;
                case CHECK_KONG:
                    check_data[1][0][i] = 5;
                    break;
                case CHECK_BEAN:
                    if (j == 4) {
                        denominator = 1;
                    }
                    break;
                case CHECK_PEARLS:
                    if (j == 3) {
                        denominator = 5;
                    }
                    break;
                case CHECK_RAINBOW:
                    for (int k = 0; k < 16; k++) {
                        if (getPatchWorld(k) == j) {
                            denominator += 1;
                        }
                    }
                    break;
                case CHECK_CRATE:
                    for (int k = 0; k < 13; k++) {
                        if (getCrateWorld(k) == j) {
                            denominator += 1;
                        }
                    }
                break;
            }
            check_data[1][j][i] = denominator;
        }
    }
}

#define STRING_MAX_SIZE 256
static char string_copy[STRING_MAX_SIZE] = "";
static char mtx_counter = 0;

int* drawHintText(int* dl, char* str, int x, int y) {
    mtx_item mtx0;
    mtx_item mtx1;
    _guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
    float position = y;
    int pos_f = *(int*)&position;
    float hint_x = 640.0f;
    if (Rando.true_widescreen) {
        hint_x = SCREEN_WD_FLOAT * 2;
    }
    _guTranslateF(&mtx1, *(int*)(&hint_x), pos_f, 0x0);
    _guMtxCatF(&mtx0, &mtx1, &mtx0);
    _guTranslateF(&mtx1, 0, 0x42400000, 0);
    _guMtxCatF(&mtx0, &mtx1, &mtx0);
    _guMtxF2L(&mtx0, &static_mtx[(int)mtx_counter]);

    *(unsigned int*)(dl++) = 0xDE000000;
	*(unsigned int*)(dl++) = 0x01000118;
	*(unsigned int*)(dl++) = 0xDA380002;
	*(unsigned int*)(dl++) = 0x02000180;
	*(unsigned int*)(dl++) = 0xE7000000;
	*(unsigned int*)(dl++) = 0x00000000;
	*(unsigned int*)(dl++) = 0xFCFF97FF;
	*(unsigned int*)(dl++) = 0xFF2CFE7F;
	*(unsigned int*)(dl++) = 0xFA000000;
    *(unsigned int*)(dl++) = 0xFFFFFFFF;
    *(unsigned int*)(dl++) = 0xDA380002;
    *(unsigned int*)(dl++) = (int)&static_mtx[(int)mtx_counter];
    dl = displayText((int*)dl,6,0,0,str,0x80);
    mtx_counter += 1;
    *(unsigned int*)(dl++) = 0xD8380002;
    *(unsigned int*)(dl++) = 0x00000040;
    return dl;
}

int* drawSplitString(int* dl, char* str, int x, int y, int y_sep) {
    int curr_y = y;
    int string_length = cstring_strlen(str);
    int string_copy_ref = (int)string_copy;
    wipeMemory(string_copy, STRING_MAX_SIZE);
    dk_memcpy(string_copy, str, string_length);
    int header = 0;
    int last_safe = 0;
    int line_count = 0;
    while (1) {
        char referenced_character = *(char*)(string_copy_ref + header);
        int is_control = 0;
        if (referenced_character == 0) {
            // Terminator
            return drawHintText(dl, (char*)(string_copy_ref), x, curr_y);
        } else if (referenced_character == 0x20) {
            // Space
            last_safe = header;
        } else if ((referenced_character > 0) && (referenced_character <= 0x10)) {
            // Control byte character
            is_control = 1;
            int end = (int)(string_copy) + (STRING_MAX_SIZE - 1);
            int size = end - (string_copy_ref + header + 1);
            dk_memcpy((void*)(string_copy_ref + header), (void*)(string_copy_ref + header + 1), size);
        }
        if (!is_control) {
            if (header > 50) {
                *(char*)(string_copy_ref + last_safe) = 0; // Stick terminator in last safe
                dl = drawHintText(dl, (char*)(string_copy_ref), x, curr_y);
                line_count += 1;
                if (line_count == 3) {
                    return dl;
                }
                curr_y += y_sep;
                string_copy_ref += (last_safe + 1);
                header = 0;
                last_safe = 0;
            } else {
                header += 1;
            }
        }
    }
    return dl;
}

#define GAME_HINT_COUNT 35

int getHintGBRequirement(int level, int kong) {
    int cap = Rando.progressive_hint_gb_cap;
    int slot = (5 * level) + kong;
    if (slot < 34) {
        /*
            Little bit of chunking to reduce amount of times checking the pause menu
            You'll get:
                1  2  3  4  - Price of hint 1
                5  6  7  8  - Price of hint 5
                9  10 11 12 - Price of hint 9
                13 14 15 16 - Price of hint 13
                17 18 19 20 - Price of hint 17
                21 22 23 24 - Price of hint 21
                25 26 27 28 - Price of hint 25
                29 30 31 32 - Price of hint 29
                33 34       - Price of hint 33
                35          - Price of hint 35
        */
        slot &= 0xFC;
    }
    float req = 1;
    req /= GAME_HINT_COUNT;
    req *= (slot + 1);
    req += 3.0f;
    req *= 1.570796f; // 0.5pi
    req = dk_sin(req) * cap;
    req += cap;
    int req_i = req;
    if (req_i <= 0) {
        req_i = 1; // Ensure no hints are free
    } else if (slot == (GAME_HINT_COUNT - 1)) {
        req_i = cap; // Ensure last hint is always at cap
    }
    return req_i;
}

int getPluralCharacter(int amount) {
    if (amount != 1) {
        return 0x53; // "S"
    }
    return 0;
}

int showHint(int level, int kong) {
    int slot = (5 * level) + kong;
    if (Rando.progressive_hint_gb_cap > 0) {
        int req = getHintGBRequirement(level, kong);
        int gb_count = getTotalGBs();
        return gb_count >= req;
    }
    // Not progressive hints
    return checkFlag(FLAG_WRINKLYVIEWED + slot, FLAGTYPE_PERMANENT);
}

static char* unknown_hints[] = {
    "??? - 000 GOLDEN BANANAS",
    "??? - 001 GOLDEN BANANAS",
    "??? - 002 GOLDEN BANANAS",
    "??? - 003 GOLDEN BANANAS",
    "??? - 004 GOLDEN BANANAS",
};

int* pauseScreen3And4Header(int* dl) {
    /**
     * @brief Alter pause screen totals header to display the checks screen
     * 
     * @param dl Display List Address
     * 
     * @return New display list address
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    display_billboard_fix = 0;
    int level_x = 0x280;
    if (Rando.true_widescreen) {
        level_x = SCREEN_WD * 2;
    }
    if (paad->screen == PAUSESCREEN_TOTALS) {
        return printText(dl, level_x, 0x3C, 0.65f, "TOTALS");
    } else if (paad->screen == PAUSESCREEN_CHECKS) {
        dl = printText(dl, level_x, 0x3C, 0.65f, "CHECKS");
        dk_strFormat((char*)level_check_text, "w %s e", levels[(int)check_level]);
        return printText(dl, level_x, 160, 0.5f, level_check_text);
    } else if (paad->screen == PAUSESCREEN_MOVES) {
        dl = display_file_images(dl, -50);
        int igt_h = stored_igt / 3600;
        int igt_s = stored_igt % 60;
        int igt_m = (stored_igt / 60) % 60;
        dk_strFormat((char*)igt_text, "%03d:%02d:%02d", igt_h, igt_m, igt_s);
        dl = printText(dl, level_x, 675, 0.5f, igt_text);
        return printText(dl, level_x, 0x3C, 0.65f, "MOVES");
    } else if (paad->screen == PAUSESCREEN_HINTS) {
        display_billboard_fix = 1;
        dl = printText(dl, level_x, 0x3C, 0.65f, "HINTS");
        // Handle Controls
        int hint_level_cap = 7;
        if (NewlyPressedControllerInput.Buttons.c_left) {
            hint_level -= 1;
            if (hint_level < 0) {
                hint_level = hint_level_cap - 1;
            }
        } else if (NewlyPressedControllerInput.Buttons.c_right) {
            hint_level += 1;
            if (hint_level >= hint_level_cap) {
                hint_level = 0;
            }
        }
        // Display level
        dk_strFormat((char*)level_hint_text, "w %s e", levels[(int)hint_level + 1]);
        dl = printText(dl, level_x, 120, 0.5f, level_hint_text);
        // Display Hints
        *(unsigned int*)(dl++) = 0xFA000000;
        *(unsigned int*)(dl++) = 0xFFFFFF96;
        int bubble_x = 625;
        if (Rando.true_widescreen) {
            bubble_x = (2 * SCREEN_WD) - 15;
        }
        dl = displayImage(dl, 107, 0, RGBA16, 48, 32, bubble_x, 465, 24.0f, 20.0f, 0, 0.0f);
        mtx_counter = 0;
        TestVariable = getHintGBRequirement(6, 4);
        for (int i = 0; i < 5; i++) {
            if (showHint(hint_level, i)) {
                dl = drawSplitString(dl, (char*)hint_pointers[(5 * hint_level) + i], level_x, 140 + (120 * i), 40);
            } else {
                if (Rando.progressive_hint_gb_cap == 0) {
                    unknown_hints[i] = "???";
                } else {
                    int requirement = getHintGBRequirement(hint_level, i);
                    dk_strFormat(unknown_hints[i], "??? - %d GOLDEN BANANA%c", requirement, getPluralCharacter(requirement));
                }
                dl = drawSplitString(dl, unknown_hints[i], level_x, 140 + (120 * i), 40);
            }
            
        }
        return dl;
    }
    return dl;
}

static char teststr[5] = "";

int* drawTextPointers(int* dl) {
    if ((TBVoidByte & 2) && (display_billboard_fix)) {
        dk_strFormat((char *)teststr, "%d", hints_initialized);
        dl = drawPixelTextContainer(dl, 0, 0, teststr, 0xFF, 0xFF, 0xFF, 0xFF, 1);
    }
    return dl;
}

int* pauseScreen3And4ItemName(int* dl, int x, int y, float scale, char* text) {
    /**
     * @brief Changes the item name depending on the screen you're on
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    int item_index = MenuActivatedItems[ViewedPauseItem];
    if (paad->screen == PAUSESCREEN_TOTALS) {
        return printText(dl, x, y, scale, raw_items[item_index]);
    } else if (paad->screen == PAUSESCREEN_CHECKS) {
        return printText(dl, x, y, scale, items[item_index]);
    }
    return dl;
}

int* pauseScreen3And4Counter(int x, int y, int top, int bottom, int* dl, int unk0, int scale) {
    /**
     * @brief Changes the counter on-screen depending on what screen you're on
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == PAUSESCREEN_TOTALS) {
        return printOutOfCounter(x, y, top, bottom, dl, unk0, scale);
    } else if (paad->screen == PAUSESCREEN_CHECKS) {
        int item_index = MenuActivatedItems[ViewedPauseItem];
        int top_num = 0;
        int bottom_num = 0;
        if (check_level == 0) {
            // All
            for (int i = 0; i < 9; i++) {
                top_num += check_data[0][i][item_index];
                bottom_num += check_data[1][i][item_index];
            }
        } else {
            int lvl = check_level - 1;
            if ((item_index == 4) || (item_index == 6) || (item_index == 8)) {
                // Nin/RW Coin, Kongs
                lvl = 0;
            }
            top_num = check_data[0][lvl][item_index];
            bottom_num = check_data[1][lvl][item_index];
        }
        return printOutOfCounter(x, y, top_num, bottom_num, dl, unk0, scale);
    }
    return dl;
}

void changePauseScreen(void) {
    /**
     * @brief Hook into the change pause screen function
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    if ((paad->screen != PAUSESCREEN_MOVES) && (paad->next_screen == PAUSESCREEN_MOVES)) {
        resetTracker();
    }
    playSFX(0x2C9);
}

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
    if (Rando.true_widescreen) {
        width = SCREEN_WD_FLOAT * 2;
        sprite->y = SCREEN_HD_FLOAT * 2;
    }
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

int changeSelectedLevel(int unk0, int unk1) {
    /**
     * @brief Change selected level in the checks screen
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == PAUSESCREEN_CHECKS) {
        // Checks Screen
        if (NewlyPressedControllerInput.Buttons.c_left) {
            check_level -= 1;
            if (check_level < 0) {
                check_level = (sizeof(levels) / 4) - 1;
            }
        } else if (NewlyPressedControllerInput.Buttons.c_right) {
            check_level += 1;
            if (check_level >= (sizeof(levels) / 4)) {
                check_level = 0;
            }
        }
    }
    return getPauseWheelRotationProgress(unk0, unk1);
}

static short file_items[16] = {
    0, 0, 0, 0, // GBs, Crowns, Keys, Medals
    0, 0, 0, 0, // RW, Fairy, Nintendo, BP
    0, 0, 0, 0, // Kongs, Beans, Pearls, Rainbow
    0, 0, 0, 0, // Crates
};

static int file_sprites[17] = {
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
    0x80720710, // Crate
    0, 0, 0,
    0, // Null Item, Leave Empty
};
static short file_item_caps[16] = {
    201, 10, 8, 40,
    1, 20, 1, 40,
    5, 1, 5, 16,
    0, 0, 0, 0, // First here is Junk Items
};

#define REFERENCE_PARENT -3
#define NO_HINT_REGION -2
#define INCONSISTENT_HINT_REGION -1

static const char map_hint_regions[] = {
    /*
        Only for situations where an entire map is a singular hint region
        Key:
            -3 = Reference parent
            -2 = No hint region at all
            -1 = Hint region differs depending on context
            >= 0 = Hint region is always a certain enum value
    */
    NO_HINT_REGION, // test_map
    REFERENCE_PARENT, // funkys_store
    REGION_FACTORYSTORAGE, // dk_arcade
    REFERENCE_PARENT, // k_rool_barrel_lankys_maze
    REGION_JAPESCAVERNS, // jungle_japes_mountain
    REFERENCE_PARENT, // crankys_lab
    REGION_JAPESCAVERNS, // jungle_japes_minecart
    INCONSISTENT_HINT_REGION, // jungle_japes
    REGION_OTHERTNS, // jungle_japes_army_dillo
    REGION_JETPAC, // jetpac
    REFERENCE_PARENT, // kremling_kosh_very_easy
    REFERENCE_PARENT, // stealthy_snoop_normal_no_logo
    REGION_JAPESHIVE, // jungle_japes_shell
    REGION_JAPESCAVERNS, // jungle_japes_lankys_cave
    REGION_AZTECOASISTOTEM, // angry_aztec_beetle_race
    REFERENCE_PARENT, // snides_hq
    REGION_AZTECTINY, // angry_aztec_tinys_temple
    REGION_OTHERHELM, // hideout_helm
    REFERENCE_PARENT, // teetering_turtle_trouble_very_easy
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_dk
    REGION_AZTECLLAMA, // angry_aztec_llama_temple
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_diddy
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_tiny
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_lanky
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_chunky
    REFERENCE_PARENT, // candys_music_shop
    INCONSISTENT_HINT_REGION, // frantic_factory
    REGION_FACTORYRESEARCH, // frantic_factory_car_race
    NO_HINT_REGION, // hideout_helm_level_intros_game_over
    REGION_FACTORYSTORAGE, // frantic_factory_power_shed
    INCONSISTENT_HINT_REGION, // gloomy_galleon
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_k_rools_ship
    REFERENCE_PARENT, // batty_barrel_bandit_very_easy
    REGION_JAPESCAVERNS, // jungle_japes_chunkys_cave
    INCONSISTENT_HINT_REGION, // dk_isles_overworld
    REFERENCE_PARENT, // k_rool_barrel_dks_target_game
    REGION_FACTORYPROD, // frantic_factory_crusher_room
    REGION_JAPESLOW, // jungle_japes_barrel_blast
    INCONSISTENT_HINT_REGION, // angry_aztec
    REGION_GALLEONSHIPYARD, // gloomy_galleon_seal_race
    NO_HINT_REGION, // nintendo_logo
    REGION_AZTECOASISTOTEM, // angry_aztec_barrel_blast
    REGION_OTHERTNS, // troff_n_scoff
    REGION_GALLEONSHIP, // gloomy_galleon_shipwreck_diddy_lanky_chunky
    REGION_GALLEONTREASURE, // gloomy_galleon_treasure_chest
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_mermaid
    REGION_GALLEONSHIP, // gloomy_galleon_shipwreck_dk_tiny
    REGION_GALLEONSHIPYARD, // gloomy_galleon_shipwreck_lanky_tiny
    INCONSISTENT_HINT_REGION, // fungi_forest
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_lighthouse
    REFERENCE_PARENT, // k_rool_barrel_tinys_mushroom_game
    REGION_GALLEONSHIPYARD, // gloomy_galleon_mechanical_fish
    REGION_FORESTOWL, // fungi_forest_ant_hill
    REFERENCE_PARENT, // battle_arena_beaver_brawl
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_barrel_blast
    REGION_FORESTSTART, // fungi_forest_minecart
    REGION_FORESTMILLS, // fungi_forest_diddys_barn
    REGION_FORESTMILLS, // fungi_forest_diddys_attic
    REGION_FORESTMILLS, // fungi_forest_lankys_attic
    REGION_FORESTMILLS, // fungi_forest_dks_barn
    REGION_FORESTMILLS, // fungi_forest_spider
    REGION_FORESTMILLS, // fungi_forest_front_part_of_mill
    REGION_FORESTMILLS, // fungi_forest_rear_part_of_mill
    REGION_FORESTGMINT, // fungi_forest_mushroom_puzzle
    REGION_FORESTGMINT, // fungi_forest_giant_mushroom
    REFERENCE_PARENT, // stealthy_snoop_normal
    REFERENCE_PARENT, // mad_maze_maul_hard
    REFERENCE_PARENT, // stash_snatch_normal
    REFERENCE_PARENT, // mad_maze_maul_easy
    REFERENCE_PARENT, // mad_maze_maul_normal
    REGION_FORESTGMINT, // fungi_forest_mushroom_leap
    REGION_FORESTGMINT, // fungi_forest_shooting_game
    INCONSISTENT_HINT_REGION, // crystal_caves
    REFERENCE_PARENT, // battle_arena_kritter_karnage
    REFERENCE_PARENT, // stash_snatch_easy
    REFERENCE_PARENT, // stash_snatch_hard
    NO_HINT_REGION, // dk_rap
    REFERENCE_PARENT, // minecart_mayhem_easy
    REFERENCE_PARENT, // busy_barrel_barrage_easy
    REFERENCE_PARENT, // busy_barrel_barrage_normal
    NO_HINT_REGION, // main_menu
    NO_HINT_REGION, // title_screen_not_for_resale_version
    REGION_CAVESMAIN, // crystal_caves_beetle_race
    REGION_OTHERTNS, // fungi_forest_dogadon
    REGION_CAVESIGLOO, // crystal_caves_igloo_tiny
    REGION_CAVESIGLOO, // crystal_caves_igloo_lanky
    REGION_CAVESIGLOO, // crystal_caves_igloo_dk
    REGION_CASTLEEXT, // creepy_castle
    REGION_CASTLEROOMS, // creepy_castle_ballroom
    REGION_CAVESCABINS, // crystal_caves_rotating_room
    REGION_CAVESCABINS, // crystal_caves_shack_chunky
    REGION_CAVESCABINS, // crystal_caves_shack_dk
    REGION_CAVESCABINS, // crystal_caves_shack_diddy_middle_part
    REGION_CAVESCABINS, // crystal_caves_shack_tiny
    REGION_CAVESCABINS, // crystal_caves_lankys_hut
    REGION_CAVESIGLOO, // crystal_caves_igloo_chunky
    REFERENCE_PARENT, // splish_splash_salvage_normal
    REGION_ISLESKREM, // k_lumsy
    REGION_CAVESMAIN, // crystal_caves_ice_castle
    REFERENCE_PARENT, // speedy_swing_sortie_easy
    REFERENCE_PARENT, // crystal_caves_igloo_diddy
    REFERENCE_PARENT, // krazy_kong_klamour_easy
    REFERENCE_PARENT, // big_bug_bash_very_easy
    REFERENCE_PARENT, // searchlight_seek_very_easy
    REFERENCE_PARENT, // beaver_bother_easy
    REGION_CASTLEROOMS, // creepy_castle_tower
    REGION_CASTLEUNDERGROUND, // creepy_castle_minecart
    NO_HINT_REGION, // kong_battle_battle_arena
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt_lanky_tiny
    REFERENCE_PARENT, // kong_battle_arena_1
    REGION_FACTORYSTORAGE, // frantic_factory_barrel_blast
    REGION_OTHERTNS, // gloomy_galleon_pufftoss
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt_dk_diddy_chunky
    REGION_CASTLEROOMS, // creepy_castle_museum
    REGION_CASTLEROOMS, // creepy_castle_library
    REFERENCE_PARENT, // kremling_kosh_easy
    REFERENCE_PARENT, // kremling_kosh_normal
    REFERENCE_PARENT, // kremling_kosh_hard
    REFERENCE_PARENT, // teetering_turtle_trouble_easy
    REFERENCE_PARENT, // teetering_turtle_trouble_normal
    REFERENCE_PARENT, // teetering_turtle_trouble_hard
    REFERENCE_PARENT, // batty_barrel_bandit_easy
    REFERENCE_PARENT, // batty_barrel_bandit_normal
    REFERENCE_PARENT, // batty_barrel_bandit_hard
    REFERENCE_PARENT, // mad_maze_maul_insane
    REFERENCE_PARENT, // stash_snatch_insane
    REFERENCE_PARENT, // stealthy_snoop_very_easy
    REFERENCE_PARENT, // stealthy_snoop_easy
    REFERENCE_PARENT, // stealthy_snoop_hard
    REFERENCE_PARENT, // minecart_mayhem_normal
    REFERENCE_PARENT, // minecart_mayhem_hard
    REFERENCE_PARENT, // busy_barrel_barrage_hard
    REFERENCE_PARENT, // splish_splash_salvage_hard
    REFERENCE_PARENT, // splish_splash_salvage_easy
    REFERENCE_PARENT, // speedy_swing_sortie_normal
    REFERENCE_PARENT, // speedy_swing_sortie_hard
    REFERENCE_PARENT, // beaver_bother_normal
    REFERENCE_PARENT, // beaver_bother_hard
    REFERENCE_PARENT, // searchlight_seek_easy
    REFERENCE_PARENT, // searchlight_seek_normal
    REFERENCE_PARENT, // searchlight_seek_hard
    REFERENCE_PARENT, // krazy_kong_klamour_normal
    REFERENCE_PARENT, // krazy_kong_klamour_hard
    REFERENCE_PARENT, // krazy_kong_klamour_insane
    REFERENCE_PARENT, // peril_path_panic_very_easy
    REFERENCE_PARENT, // peril_path_panic_easy
    REFERENCE_PARENT, // peril_path_panic_normal
    REFERENCE_PARENT, // peril_path_panic_hard
    REFERENCE_PARENT, // big_bug_bash_easy
    REFERENCE_PARENT, // big_bug_bash_normal
    REFERENCE_PARENT, // big_bug_bash_hard
    REGION_CASTLEUNDERGROUND, // creepy_castle_dungeon
    NO_HINT_REGION, // hideout_helm_intro_story
    NO_HINT_REGION, // dk_isles_dk_theatre
    REGION_OTHERTNS, // frantic_factory_mad_jack
    REFERENCE_PARENT, // battle_arena_arena_ambush
    REFERENCE_PARENT, // battle_arena_more_kritter_karnage
    REFERENCE_PARENT, // battle_arena_forest_fracas
    REFERENCE_PARENT, // battle_arena_bish_bash_brawl
    REFERENCE_PARENT, // battle_arena_kamikaze_kremlings
    REFERENCE_PARENT, // battle_arena_plinth_panic
    REFERENCE_PARENT, // battle_arena_pinnacle_palaver
    REFERENCE_PARENT, // battle_arena_shockwave_showdown
    REGION_CASTLEUNDERGROUND, // creepy_castle_basement
    REGION_CASTLEEXT, // creepy_castle_tree
    REFERENCE_PARENT, // k_rool_barrel_diddys_kremling_game
    REGION_CASTLEEXT, // creepy_castle_chunkys_toolshed
    REGION_CASTLEEXT, // creepy_castle_trash_can
    REGION_CASTLEEXT, // creepy_castle_greenhouse
    REGION_ISLESLOBBIES0, // jungle_japes_lobby
    REGION_ISLESLOBBIES1, // hideout_helm_lobby
    REGION_ISLESMAIN, // dks_house
    NO_HINT_REGION, // rock_intro_story
    REGION_ISLESLOBBIES0, // angry_aztec_lobby
    REGION_ISLESLOBBIES0, // gloomy_galleon_lobby
    REGION_ISLESLOBBIES0, // frantic_factory_lobby
    REGION_ISLESMAIN, // training_grounds
    REFERENCE_PARENT, // dive_barrel
    REGION_ISLESLOBBIES0, // fungi_forest_lobby
    REGION_GALLEONSHIPYARD, // gloomy_galleon_submarine
    REFERENCE_PARENT, // orange_barrel
    REFERENCE_PARENT, // barrel_barrel
    REFERENCE_PARENT, // vine_barrel
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt
    REFERENCE_PARENT, // enguarde_arena
    REGION_CASTLEROOMS, // creepy_castle_car_race
    REGION_CAVESMAIN, // crystal_caves_barrel_blast
    REGION_CASTLEEXT, // creepy_castle_barrel_blast
    REGION_FORESTGMEXT, // fungi_forest_barrel_blast
    INCONSISTENT_HINT_REGION, // fairy_island
    REFERENCE_PARENT, // kong_battle_arena_2
    REFERENCE_PARENT, // rambi_arena
    REFERENCE_PARENT, // kong_battle_arena_3
    REGION_ISLESLOBBIES1, // creepy_castle_lobby
    REGION_ISLESLOBBIES1, // crystal_caves_lobby
    REGION_ISLESKREM, // dk_isles_snides_room
    REGION_OTHERTNS, // crystal_caves_army_dillo
    REGION_OTHERTNS, // angry_aztec_dogadon
    NO_HINT_REGION, // training_grounds_end_sequence
    REGION_OTHERTNS, // creepy_castle_king_kut_out
    REGION_CAVESCABINS, // crystal_caves_shack_diddy_upper_part
    REFERENCE_PARENT, // k_rool_barrel_diddys_rocketbarrel_game
    REFERENCE_PARENT, // k_rool_barrel_lankys_shooting_game
    REGION_ISLESKROOL, // k_rool_fight_dk_phase
    REGION_ISLESKROOL, // k_rool_fight_diddy_phase
    REGION_ISLESKROOL, // k_rool_fight_lanky_phase
    REGION_ISLESKROOL, // k_rool_fight_tiny_phase
    REGION_ISLESKROOL, // k_rool_fight_chunky_phase
    NO_HINT_REGION, // bloopers_ending
    REFERENCE_PARENT, // k_rool_barrel_chunkys_hidden_kremling_game
    REFERENCE_PARENT, // k_rool_barrel_tinys_pony_tail_twirl_game
    REFERENCE_PARENT, // k_rool_barrel_chunkys_shooting_game
    REFERENCE_PARENT, // k_rool_barrel_dks_rambi_game
    NO_HINT_REGION, // k_lumsy_ending
    REGION_ISLESKROOL, // k_rools_shoe
    REGION_ISLESKROOL, // k_rools_arena
};

int setHintRegion(void) {
    int current_region = map_hint_regions[CurrentMap];
    if (current_region >= 0) {
        return current_region;
    } else if (current_region == NO_HINT_REGION) {
        return -1;
    } else if (current_region == REFERENCE_PARENT) {
        if (inShop(CurrentMap, 1)) {
            int level = getWorld(CurrentMap, 1);
            if (level == 7) {
                return REGION_SHOPISLES;
            }
            if (level < 7) {
                return REGION_SHOPJAPES + level;
            }
        } else {
            int parent_map = 0;
            int parent_exit = 0;
            getParentMap(&parent_map, &parent_exit);
            if ((parent_map >= 0) && (parent_map < 216)) {
                current_region = map_hint_regions[parent_map];
                if (current_region >= 0) {
                    return current_region;
                }
            }
        }
    }
    if (current_region == INCONSISTENT_HINT_REGION) {
        int chunk = Player->chunk;
        int px = Player->xPos;
        int py = Player->yPos;
        int pz = Player->zPos;
        switch (CurrentMap) {
            case MAP_FAIRYISLAND:
                if (chunk == 1) {
                    return REGION_ISLESRAREWARE;
                }
                return REGION_ISLESOUTER;
            case MAP_CAVES:
                if (chunk == 4) {
                    return REGION_CAVESCABINS;
                } else if ((chunk == 8) || (chunk == 13)) {
                    // 8 = Igloos, 13 = GK Room
                    return REGION_CAVESIGLOO;
                }
                return REGION_CAVESMAIN;
            case MAP_FUNGI:
                if ((chunk == 0) || (chunk == 7) || (chunk == 8) || (chunk == 9)) {
                    // 0 = Starting area, 7 = Green Tunnel, 8 = Apple area, 9 = Beanstalk Area
                    return REGION_FORESTSTART;
                } else if ((chunk >= 1) && (chunk <= 6)) {
                    // 1 = Blue Tunnel
                    // 2 = Mills Main
                    // 3 = Snide Area
                    // 4 = Dark Attic Area
                    // 5 = Thornvine Area
                    // 6 = Rear of Thornvine Barn
                    return REGION_FORESTMILLS;
                } else if ((chunk >= 12) && (chunk <= 17)) {
                    // 12 = Yellow Tunnel
                    // 13 = Start of owl tree area
                    // 14 = Owl Tree Area Main
                    // 15 = Rabbit Race Area
                    // 16 = Anthill Area
                    // 17 = Owl Tree Rocketbarrel Area
                    return REGION_FORESTOWL;
                }
                return REGION_FORESTGMEXT;
            case MAP_AZTEC:
                if ((chunk == 4) || (chunk == 12)) {
                    // 4 = Oasis, 12 = Totem
                    return REGION_AZTECOASISTOTEM;
                }
                return REGION_AZTECTUNNELS;
            case MAP_ISLES:
                {
                    if (chunk == 1) {
                        return REGION_ISLESKREM;
                    }
                    // Check fungi island
                    int dx = px - 2594;
                    int dz = pz - 922;
                    if (py > 1450) {
                        if (((dx * dx) + (dz * dz)) < 52900) {
                            return REGION_ISLESOUTER;
                        }
                    }
                    // check outside isles cylinder
                    dx = px - 2880;
                    dz = pz - 1624;
                    if (((dx * dx) + (dz * dz)) > 1270800) {
                        return REGION_ISLESOUTER;
                    }
                    return REGION_ISLESMAIN;
                    
                }
            case MAP_GALLEON:
                if ((chunk >= 9) && (chunk <= 11)) {
                    // 9 = Lighthouse Room
                    // 10 = Behind Ship Door
                    // 11 = Enguarde Room
                    return REGION_GALLEONLIGHTHOUSE;
                } else if ((chunk == 16) || (chunk == 17)) {
                    // 16 = Tunnel to treasure room
                    // 17 = Treasure Room
                    return REGION_GALLEONTREASURE;
                } else if ((chunk >= 0) && (chunk <= 8)) {
                    // 0 = Galleon Start
                    // 1 = Crossroads left
                    // 2 = Crossroads start
                    // 3 = Crossroads right
                    // 4 = Tunnel to Cannon Room
                    // 5 = Cannon Room
                    // 6 = Main Cranky Room
                    // 7 = Main Cranky Room 2
                    // 8 = Chest Room
                    return REGION_GALLEONCAVERNS;
                }
                return REGION_GALLEONSHIPYARD;
            case MAP_FACTORY:
                if (chunk == 12) {
                    // 12 = Tunnel to pole
                    // Chunk has 2 regions, subdivide by x position
                    if (px > 1860) {
                        return REGION_FACTORYTESTING;
                    }
                    return REGION_FACTORYSTART;
                }
                if ((chunk == 9) || (chunk == 11)) {
                    // 9 = Lobby with warps, 11 = Lobby with switch
                    return REGION_FACTORYSTART;
                } else if ((chunk == 10) || ((chunk >= 13) && (chunk <= 19))) {
                    // 10 = Snide Area
                    // 13 = Pink Tunnel
                    // 14 = Number Game
                    // 15 = Pink Tunnel End
                    // 16 = Block Tower
                    // 17 = Number Game Tunnel
                    // 18 = Funky's
                    // 19 = Tunnel to R&D Pole
                    return REGION_FACTORYTESTING;
                } else if ((chunk >= 4) && (chunk <= 6)) {
                    // 4 = Tunnel to Storage
                    // 5 = Production Room
                    // 6 = Tunnel to Hatch
                    return REGION_FACTORYPROD;
                } else if ((chunk >= 22) && (chunk <= 30)) {
                    // 22 = Tunnel from Pole to R&D
                    // 23 = Main R&D
                    // 24 = BHDM Room & Tunnel
                    // 25 = Pincode Room & Tunnel
                    // 26 = Piano Room & Tunnel
                    // 27 = Hatch Room & Tunnel
                    // 28 = Car Race Lobby
                    // 29 = Gorilla Grab Room
                    // 30 = Tunnel to Car Race
                    return REGION_FACTORYRESEARCH;
                }
                return REGION_FACTORYSTORAGE;
            case MAP_JAPES:
                if (chunk == 3) {
                    // 3 = Main Area (Both japes hillside and lowlands)
                    // Subdivide based on z position
                    if (pz > 1647) {
                        if (py < 270) {
                            return REGION_JAPESLOW;
                        }
                        if (px > 2258) {
                            if (pz < 1795) {
                                return REGION_JAPESLOW;
                            }
                        }
                        return REGION_JAPESHIGH;
                    }
                    return REGION_JAPESLOW;
                }
                if ((chunk == 0) || (chunk == 1) || (chunk == 2) || (chunk == 18)) {
                    // 0 = Starting Area
                    // 1 = Starting Tunnel
                    // 2 = Diddy Alcove
                    // 18 = Japes Tunnel Exit
                    return REGION_JAPESLOW;
                } else if ((chunk >= 4) && (chunk <= 7)) {
                    // 4 = Hive Tunnel Near
                    // 5 = Hive Tunnel Mid
                    // 6 = Hive Tunnel Far
                    // 7 = Hive area
                    return REGION_JAPESHIVE;
                } else if ((chunk >= 8) && (chunk <= 16)) {
                    // 8 = Tunnel Middle Branch
                    // 9 = Pit
                    // 10 = Tunnel Right Branch
                    // 11 = Tunnel Crossroads
                    // 12 = Near Rambi Door
                    // 13 = Fairy pool
                    // 14 = Storm Area
                    // 15 = Bunch Boulder Area
                    // 16 = Lanky Kasplat Alcove
                    return REGION_JAPESSTORM;
                }
                return REGION_JAPESHIGH;
            default:
                break;

        }
    }
    return -1;
}

void getHintRegionText() {
    int index = setHintRegion();
    if (index < 0) {
        dk_memcpy(hint_region_text, "UNKNOWN", 8);
    } else {
        char* text = getTextPointer(43, index, 0);
        wipeMemory(hint_region_text, 0x20);
        dk_memcpy(hint_region_text, text, 0x20);
    }
}

int* displayHintRegion(int* dl, int x, int y, float scale, char* text) {
    dl = printText(dl, x, y, scale, text);
    int y_req = 0x198;
    if (Rando.warp_to_isles_enabled) {
        y_req = InitialPauseHeight;
    }
    if (y != y_req) {
        return dl;
    }
    int x_hint = 0x280;
    int y_bottom = 240;
    if (Rando.true_widescreen) {
        x_hint = SCREEN_WD << 1;
        y_bottom = SCREEN_HD;
    }
    *(unsigned int*)(dl++) = 0xFA000000;
    *(unsigned int*)(dl++) = 0xFFFFFFFF;
    return printText(dl, x_hint, (y_bottom << 2) - 100, 0.45f, (char*)&hint_region_text);
}

void updateFileVariables(void) {
    /**
     * @brief Update file variables on pause menu initialization
     */
    updateFilePercentage();
    getHintRegionText();
    for (int i = 0; i < 8; i++) {
        file_items[i] = FileVariables[i];
    }
    file_items[CHECK_KONG] = 0;
    file_items[CHECK_BEAN] = checkFlagDuplicate(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
    file_items[CHECK_PEARLS] = 0;
    file_items[CHECK_RAINBOW] = 0;
    file_items[CHECK_CRATE] = 0;
    for (int i = 0; i < 5; i++) {
        file_items[CHECK_KONG] += checkFlagDuplicate(kong_flags[i], FLAGTYPE_PERMANENT);
        file_items[CHECK_PEARLS] += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, FLAGTYPE_PERMANENT);
    }
    for (int i = 0; i < 16; i++) {
        file_items[CHECK_RAINBOW] += checkFlagDuplicate(FLAG_RAINBOWCOIN_0 + i, FLAGTYPE_PERMANENT);
    }
    for (int i = 0; i < 100; i++) {
        file_items[CHECK_CRATE] += checkFlagDuplicate(FLAG_JUNKITEM + i, FLAGTYPE_PERMANENT);
    }
}

int* handleOutOfCounters(int x, int y, int top, int bottom, int* dl, int unk0, int scale) {
    /**
     * @brief Handle the "out of" counters to be corrected
     */
    if (Rando.item_rando) {
        char text[4] = "";
        dk_strFormat((char*)&text, "%d", top);
        return displayText(dl, 1, x, y, &text, 0x80);
    }
    return printOutOfCounter(x, y, top, bottom, dl, unk0, scale);
}

void initPauseMenu(void) {
    /**
     * @brief Initialize the pause menu changes for Rando
     */
    *(short*)(0x806AB35A) = getHi(&file_sprites[0]);
    *(short*)(0x806AB35E) = getLo(&file_sprites[0]);
    writeFunction(0x806A84C8, &updateFileVariables); // Update file variables to transfer old locations to current
    *(short*)(0x806AB2CA) = getHi(&file_items[0]);
    *(short*)(0x806AB2DA) = getLo(&file_items[0]);
    *(short*)(0x806A9FC2) = getHi(&file_items[0]);
    *(short*)(0x806AA036) = getLo(&file_items[0]);
    *(short*)(0x806AA00E) = getHi(&file_item_caps[0]);
    *(short*)(0x806AA032) = getLo(&file_item_caps[0]);
    *(short*)(0x806AB2CE) = getHi(&file_items[CHECK_TERMINATOR]);
    *(short*)(0x806AB2D6) = getLo(&file_items[CHECK_TERMINATOR]);
    *(short*)(0x806AB3F6) = CHECK_TERMINATOR;
    if (Rando.item_rando) {
        writeFunction(0x806A9D50, &handleOutOfCounters); // Print out of counter, depending on item rando state
        writeFunction(0x806A9EFC, &handleOutOfCounters); // Print out of counter, depending on item rando state
        *(int*)(0x806A9C80) = 0; // Show counter on Helm Menu - Kong specific screeen
        *(int*)(0x806A9E54) = 0; // Show counter on Helm Menu - All Kongs screen
        // *(int*)(0x806AA860) = 0x31EF0007; // ANDI $t7, $t7, 7 - Show GB (Kong Specific)
        // *(int*)(0x806AADC4) = 0x33390007; // ANDI $t9, $t9, 7 - Show GB (All Kongs)
        // *(int*)(0x806AADC8) = 0xAFB90058; // SW $t9, 0x58 ($sp) - Show GB (All Kongs)
    }
    // Prevent GBs being required to view extra screens
    *(int*)(0x806A8624) = 0; // GBs doesn't lock other pause screens
    *(int*)(0x806AB468) = 0; // Show R/Z Icon
    *(int*)(0x806AB318) = 0x24060001; // ADDIU $a2, $r0, 1
    *(int*)(0x806AB31C) = 0xA466C83C; // SH $a2, 0xC83C ($v1) | Overwrite trap func, Replace with overwrite of wheel segments
    *(short*)(0x8075056C) = 201; // Change GB Item cap to 201
    // In-Level IGT
    writeFunction(0x8060DF28, &updateLevelIGT); // Modify Function Call
    writeFunction(0x806ABB0C, &printLevelIGT); // Modify Function Call
    *(short*)(0x806ABB32) = 106; // Adjust kong name height
    // Pause Totals/Checks Revamp
    writeFunction(0x806AB3C4, &updatePauseScreenWheel); // Change Wheel to scroller
    *(int*)(0x806AB3B4) = 0xAFB00018; // SW $s0, 0x18 ($sp). Change last param to index
    *(int*)(0x806AB3A0) = 0xAFA90014; // SW $t1, 0x14 ($sp). Change 2nd-to-last param to local index
    *(int*)(0x806AB444) = 0; // Prevent joystick sprite rendering
    writeFunction(0x806AB528, &handleSpriteCode); // Change sprite control function
    *(int*)(0x806AB52C) = 0x8FA40060; // LW $a0, 0x60 ($sp). Change param
    *(short*)(0x806A8DB2) = 0x0029; // Swap left/right direction
    *(short*)(0x806A8DBA) = 0xFFD8; // Swap left/right direction
    *(short*)(0x806A8DB4) = 0x5420; // BEQL -> BNEL
    *(short*)(0x806A8DF0) = 0x1020; // BNE -> BEQ
    writeFunction(0x806A9F74, &pauseScreen3And4ItemName); // Item Name
    // Disable Item Checks
    *(int*)(0x806AB2E8) = 0;
    *(int*)(0x806AB360) = 0;
    *(short*)(0x806ABFCE) = FLAG_BP_JAPES_DK_HAS; // Change BP trigger to being collecting BP rather than turning it in
}