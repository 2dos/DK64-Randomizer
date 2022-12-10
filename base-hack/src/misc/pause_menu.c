#include "../../include/common.h"

static char igt_text[20] = "IGT: 0000:00:00";

int* printLevelIGT(int* dl, int x, int y, float scale, char* str) {
    dl = printText(dl, x, y, scale, str);
    int level_index = -1;
    for (int i = 0; i < 12; i++) {
        if ((int)LevelNamesPointer[i] == (int)str) {
            level_index = i;
        }
    }
    int igt_data = 0;
    if (level_index < 9) {
        igt_data = StoredSettings.file_extra.level_igt[level_index];
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
    "KONGS",
    "BEAN",
    "PEARLS",
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
};

static char check_level = 0;
static char level_check_text[0x18] = "";

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

#define PAUSE_ITEM_COUNT 11
#define ROTATION_SPLIT 372 // 0x1000 / PAUSE_ITEM_COUNT

static unsigned char check_data[2][9][PAUSE_ITEM_COUNT] = {}; // 8 items, 9 levels, numerator + denominator

void checkItemDB(void) {
    renderScreenTransition(7);
    initTracker();
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
                check_data[1][lvl][i] += 1;
                check_data[0][lvl][i] += checkFlag(search_flag, 0);
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
                break;
            }
        }
    }
}

int* pauseScreen3And4Header(int* dl) {
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == 3) {
        return printText(dl, 0x280, 0x3C, 0.65f, "TOTALS");
    } else if (paad->screen == 4) {
        dl = printText(dl, 0x280, 0x3C, 0.65f, "CHECKS");
        dk_strFormat((char*)level_check_text, "w %s e", levels[(int)check_level]);
        return printText(dl, 0x280, 160, 0.5f, level_check_text);
    } else if (paad->screen == 5) {
        dl = display_file_images(dl, -50);
        return printText(dl, 0x280, 0x3C, 0.65f, "MOVES");
    }
    return dl;
}

int* pauseScreen3And4ItemName(int* dl, int x, int y, float scale, char* text) {
    pause_paad* paad = CurrentActorPointer_0->paad;
    int item_index = MenuActivatedItems[ViewedPauseItem];
    if (paad->screen == 3) {
        return printText(dl, x, y, scale, raw_items[item_index]);
    } else if (paad->screen == 4) {
        return printText(dl, x, y, scale, items[item_index]);
    }
    return dl;
}

int* pauseScreen3And4Counter(int x, int y, int top, int bottom, int* dl, int unk0, int scale) {
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == 3) {
        return printOutOfCounter(x, y, top, bottom, dl, unk0, scale);
    } else if (paad->screen == 4) {
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
    pause_paad* paad = CurrentActorPointer_0->paad;
    if ((paad->screen != 5) && (paad->next_screen == 5)) {
        resetTracker();
    }
    playSFX(0x2C9);
}

void updatePauseScreenWheel(void* write_location, void* sprite, int x, int y, float scale, int local_index, int index) {
    displaySprite(write_location, sprite, local_index, 0x78, 1.0f, 2, 16);
}

void newPauseSpriteCode(sprite_struct* sprite, char* render) {
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
    if (control_type < 16) {
        loadSpriteFunction(0x806AC07C);
    } else {
        loadSpriteFunction((int)&newPauseSpriteCode);
    }
}

int changeSelectedLevel(int unk0, int unk1) {
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == 4) {
        // Checks Screen
        if (NewlyPressedControllerInput.Buttons & C_Left) {
            check_level -= 1;
            if (check_level < 0) {
                check_level = (sizeof(levels) / 4) - 1;
            }
        } else if (NewlyPressedControllerInput.Buttons & C_Right) {
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
    0, 0, 0, 0, // Kongs, Beans, Pearls
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
    0,
    0, 0, 0, 0,
    0, // Null Item, Leave Empty
};
static short file_item_caps[16] = {
    201, 10, 8, 40,
    1, 20, 1, 40,
    5, 1, 5, 0,
    0, 0, 0, 0,
};

void updateFileVariables(void) {
    updateFilePercentage();
    for (int i = 0; i < 8; i++) {
        file_items[i] = FileVariables[i];
    }
    file_items[8] = 0;
    file_items[9] = checkFlagDuplicate(FLAG_COLLECTABLE_BEAN, 0);
    file_items[10] = 0;
    for (int i = 0; i < 5; i++) {
        file_items[8] += checkFlagDuplicate(kong_flags[i], 0);
        file_items[10] += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, 0);
    }
}

int* handleOutOfCounters(int x, int y, int top, int bottom, int* dl, int unk0, int scale) {
    if (Rando.item_rando) {
        char text[4] = "";
        dk_strFormat((char*)&text, "%d", top);
        return displayText(dl, 1, x, y, &text, 0x80);
    }
    return printOutOfCounter(x, y, top, bottom, dl, unk0, scale);
}

void initPauseMenu(void) {
    *(short*)(0x806AB35A) = getHi(&file_sprites[0]);
    *(short*)(0x806AB35E) = getLo(&file_sprites[0]);
    *(int*)(0x806A84C8) = 0x0C000000 | (((int)&updateFileVariables & 0xFFFFFF) >> 2); // Update file variables to transfer old locations to current
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
        *(int*)(0x806A9D50) = 0x0C000000 | (((int)&handleOutOfCounters & 0xFFFFFF) >> 2); // Print out of counter, depending on item rando state
        *(int*)(0x806A9EFC) = 0x0C000000 | (((int)&handleOutOfCounters & 0xFFFFFF) >> 2); // Print out of counter, depending on item rando state
        *(int*)(0x806A9C80) = 0; // Show counter on Helm Menu - Kong specific screeen
        *(int*)(0x806A9E54) = 0; // Show counter on Helm Menu - All Kongs screen
        // *(int*)(0x806AA860) = 0x31EF0007; // ANDI $t7, $t7, 7 - Show GB (Kong Specific)
        // *(int*)(0x806AADC4) = 0x33390007; // ANDI $t9, $t9, 7 - Show GB (All Kongs)
        // *(int*)(0x806AADC8) = 0xAFB90058; // SW $t9, 0x58 ($sp) - Show GB (All Kongs)

    }
}