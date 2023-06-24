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

/*
        0 = GB
        1 = Crown
        2 = Keys
        3 = Medals
        4 = RW Coin
        5 = Fairies
        6 = N Coin
        7 = Blueprints
    */

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
};

static char check_level = 0;
static char hint_level = 0;
static char level_check_text[0x18] = "";
static char level_hint_text[0x18] = "";

#define CHECK_GB 0
#define CHECK_CROWN 1
#define CHECK_KEY 2
#define CHECK_MEDAL 3
#define CHECK_RWCOIN 4
#define CHECK_FAIRY 5
#define CHECK_NINCOIN 6
#define CHECK_BP 7
#define CHECK_KONG 8
#define CHECK_BEAN 9
#define CHECK_PEARLS 10
#define CHECK_RAINBOW 11

#define PAUSE_ITEM_COUNT 12
#define ROTATION_SPLIT 341 // 0x1000 / PAUSE_ITEM_COUNT

static unsigned char check_data[2][9][PAUSE_ITEM_COUNT] = {}; // 8 items, 9 levels, numerator + denominator

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
    renderScreenTransition(7);
    initTracker();
    initHints();
    stored_igt = getNewSaveTime();
    if (Rando.helm_hurry_mode) {
        if (ReadFile(DATA_HELMHURRYOFF, 0, 0, 0)) {
            stored_igt = IGT;
        }
    }
    for (int i = 0; i < PAUSE_ITEM_COUNT; i++) {
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
        }
        // Get Denominator
        for (int j = 0; j < 9; j++) {
            switch (i) {
                case CHECK_GB:
                    if (j < 8) {
                        if (j == 7) {
                            check_data[1][j][CHECK_GB] = 21;
                        } else {
                            check_data[1][j][CHECK_GB] = 20;
                        }
                    }
                    break;
                case CHECK_CROWN:
                    if (j == 7) {
                        check_data[1][j][CHECK_CROWN] = 2;
                    } else {
                        check_data[1][j][CHECK_CROWN] = 1;
                    }
                    break;
                case CHECK_KEY:
                    if (j != 7) {
                        check_data[1][j][CHECK_KEY] = 1;
                    }
                    break;
                case CHECK_MEDAL:
                    if (j != 7) {
                        check_data[1][j][CHECK_MEDAL] = 5;
                    }
                    break;
                case CHECK_RWCOIN:
                case CHECK_NINCOIN:
                    check_data[1][0][i] = 1;
                    break;
                case CHECK_FAIRY:
                    if (j == 7) {
                        check_data[1][j][CHECK_FAIRY] = 4;
                    } else {
                        check_data[1][j][CHECK_FAIRY] = 2;
                    }
                    break;
                case CHECK_BP:
                    if (j < 8) {
                        check_data[1][j][CHECK_BP] = 5;
                    }
                    break;
                case CHECK_KONG:
                    check_data[1][0][i] = 5;
                    break;
                case CHECK_BEAN:
                    if (j == 4) {
                        check_data[1][j][CHECK_BEAN] = 1;
                    }
                    break;
                case CHECK_PEARLS:
                    if (j == 3) {
                        check_data[1][j][CHECK_PEARLS] = 5;
                    }
                    break;
                case CHECK_RAINBOW:
                    if (!Rando.item_rando) {
                        if (j == 7) {
                            check_data[1][j][CHECK_RAINBOW] = 7;
                        } else if ((j == 1) || (j == 4)) {
                            check_data[1][j][CHECK_RAINBOW] = 2;
                        } else {
                            check_data[1][j][CHECK_RAINBOW] = 1;
                        }
                    } else {
                        for (int k = 0; k < 16; k++) {
                            if ((getPatchWorld(k) == j) && (j < 8)) {
                                check_data[1][j][CHECK_RAINBOW] += 1;
                            }
                        }
                    }
                break;
            }
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
    _guTranslateF(&mtx1, 0x44200000, pos_f, 0x0);
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
    if (paad->screen == PAUSESCREEN_TOTALS) {
        return printText(dl, 0x280, 0x3C, 0.65f, "TOTALS");
    } else if (paad->screen == PAUSESCREEN_CHECKS) {
        dl = printText(dl, 0x280, 0x3C, 0.65f, "CHECKS");
        dk_strFormat((char*)level_check_text, "w %s e", levels[(int)check_level]);
        return printText(dl, 0x280, 160, 0.5f, level_check_text);
    } else if (paad->screen == PAUSESCREEN_MOVES) {
        dl = display_file_images(dl, -50);
        int igt_h = stored_igt / 3600;
        int igt_s = stored_igt % 60;
        int igt_m = (stored_igt / 60) % 60;
        dk_strFormat((char*)igt_text, "%03d:%02d:%02d", igt_h, igt_m, igt_s);
        dl = printText(dl, 0x280, 675, 0.5f, igt_text);
        return printText(dl, 0x280, 0x3C, 0.65f, "MOVES");
    } else if (paad->screen == PAUSESCREEN_HINTS) {
        display_billboard_fix = 1;
        dl = printText(dl, 0x280, 0x3C, 0.65f, "HINTS");
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
        dl = printText(dl, 0x280, 120, 0.5f, level_hint_text);
        // Display Hints
        *(unsigned int*)(dl++) = 0xFA000000;
        *(unsigned int*)(dl++) = 0xFFFFFF96;
        dl = displayImage(dl, 107, 0, RGBA16, 48, 32, 625, 465, 24.0f, 20.0f, 0, 0.0f);
        mtx_counter = 0;
        for (int i = 0; i < 5; i++) {
            if (checkFlag(FLAG_WRINKLYVIEWED + (5 * hint_level) + i, FLAGTYPE_PERMANENT)) {
                dl = drawSplitString(dl, (char*)hint_pointers[(5 * hint_level) + i], 640, 140 + (120 * i), 40);
            } else {
                dl = drawSplitString(dl, "???", 640, 140 + (120 * i), 40);
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

void updatePauseScreenWheel(void* write_location, void* sprite, int x, int y, float scale, int local_index, int index) {
    /**
     * @brief Update the pause screen wheel to be a carousel instead.
     */
    displaySprite(write_location, sprite, local_index, 0x78, 1.0f, 2, 16);
}

void newPauseSpriteCode(sprite_struct* sprite, char* render) {
    /**
     * @brief Sprite code for the carousel pause screen effect
     */
    spriteControlCode(sprite, render);
    pause_paad* pause_control = (pause_paad*)sprite->control;
    // float opacity_scale = 1.0f;
    // float test_opacity = (pause_control->unkC[(int)sprite->unk384[1]] * 4) - pause_control->unk0;
    // if (test_opacity < 0.0f) {
    //     test_opacity = 0.0f;
    // }
    // if (test_opacity <= 1.0f) {
    //     opacity_scale = test_opacity;
    // }
    // sprite->alpha = opacity_scale * 255.0f;
    int index = sprite->unk384[2] / 4;
    int viewed_item = ((float)(pause_control->control) / ROTATION_SPLIT);
    int diff = index - viewed_item;
    if (diff == (PAUSE_ITEM_COUNT - 1)) {
        diff = -1;
    } else if (diff == (PAUSE_ITEM_COUNT - 2)) {
        diff = -2;
    } else if (diff == (1 - PAUSE_ITEM_COUNT)) {
        diff = 1;
    } else if (diff == (2 - PAUSE_ITEM_COUNT)) {
        diff = 2;
    }
    int pos_diff = diff;
    if (pos_diff > 0) {
        pos_diff += 1;
    } else  if (pos_diff < 0) {
        pos_diff -= 1;
    }
    float diff_increment = ((pause_control->control - (ROTATION_SPLIT * viewed_item)) * 80 * PAUSE_ITEM_COUNT) >> 12;
    if ((pos_diff >= 3) || (pos_diff <= -2)) {
        diff_increment /= 2;
    }
    sprite->x = (0xA0 + (pos_diff * 0x28) - diff_increment) * 4;
    float scale = 0.0f;
    if (sprite->x > 640.0f) {
        // Right of center
        if (sprite->x < 960.0f) {
            // 8-4
            float x_diff = 640.f - sprite->x;
            scale = 8.0f + (x_diff / 80.0f);
        } else {
            // 4-2-0
            float x_diff = 960.0f - sprite->x;
            scale = 4.0f + (x_diff / 80.0f);
            if (scale < 0.0f) {
                scale = 0.0f;
            }
        }
    } else if (sprite->x < 640.0f) {
        // Left of center
        if (sprite->x > 320.0f) {
            // 4-8
            float x_diff = 640.0f - sprite->x;
            scale = 8.0f - (x_diff / 80.0f);
        } else {
            // 0-2-4
            float x_diff = 320.0f - sprite->x;
            scale = 4.0f - (x_diff / 80.0f);
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

void handleSpriteCode(int control_type) {
    /**
     * @brief Changes sprite code to be the carousel effect if the index is greater than 16
     * 
     * @param control_type Type of sprite that's being displayed and the controls you have access to
     */
    if (control_type < 16) {
        loadSpriteFunction(0x806AC07C);
    } else {
        loadSpriteFunction((int)&newPauseSpriteCode);
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
    0, 0, 0, 0,
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
    0, 0, 0, 0,
    0, // Null Item, Leave Empty
};
static short file_item_caps[16] = {
    201, 10, 8, 40,
    1, 20, 1, 40,
    5, 1, 5, 16,
    0, 0, 0, 0,
};

void updateFileVariables(void) {
    /**
     * @brief Update file variables on pause menu initialization
     */
    updateFilePercentage();
    for (int i = 0; i < 8; i++) {
        file_items[i] = FileVariables[i];
    }
    file_items[CHECK_KONG] = 0;
    file_items[CHECK_BEAN] = checkFlagDuplicate(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
    file_items[CHECK_PEARLS] = 0;
    file_items[CHECK_RAINBOW] = 0;
    for (int i = 0; i < 5; i++) {
        file_items[CHECK_KONG] += checkFlagDuplicate(kong_flags[i], FLAGTYPE_PERMANENT);
        file_items[CHECK_PEARLS] += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, FLAGTYPE_PERMANENT);
    }
    for (int i = 0; i < 16; i++) {
        file_items[CHECK_RAINBOW] += checkFlagDuplicate(FLAG_RAINBOWCOIN_0 + i, FLAGTYPE_PERMANENT);
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
    *(short*)(0x806AB2CE) = getHi(&file_items[PAUSE_ITEM_COUNT]);
    *(short*)(0x806AB2D6) = getLo(&file_items[PAUSE_ITEM_COUNT]);
    *(short*)(0x806AB3F6) = PAUSE_ITEM_COUNT;
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