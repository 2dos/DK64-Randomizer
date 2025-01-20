/**
 * @file lib.c
 * @author Ballaam
 * @brief General Pause Menu functions
 * @version 0.1
 * @date 2022-10-03
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static char igt_text[20] = "IGT: 0000:00:00";
static int stored_igt = 0;

Gfx* printLevelIGT(Gfx* dl, int x, int y, float scale, char* str) {
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
    "WRINKLY DOORS",
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
    "HINTS",
    "JUNK ITEMS",
};

static char check_level = 0;
static char level_check_text[0x18] = "";

typedef struct CheckDataLevelStruct {
    unsigned char level[9];
} CheckDataLevelStruct;

typedef struct CheckDataTypeStruct {
    CheckDataLevelStruct type[CHECK_TERMINATOR];
} CheckDataTypeStruct;

typedef struct CheckDataStruct {
    CheckDataTypeStruct numerator;
    CheckDataTypeStruct denominator;
} CheckDataStruct;

// 7 main levels, isles, helm
static CheckDataStruct check_data = {
    .denominator = {
        .type[CHECK_GB] =      {.level = {20, 20, 20, 20, 20, 20, 20, 21, 0}},
        .type[CHECK_CROWN] =   {.level = {1, 1, 1, 1, 1, 1, 1, 2, 1}},
        .type[CHECK_KEY] =     {.level = {1, 1, 1, 1, 1, 1, 1, 0, 1}},
        .type[CHECK_MEDAL] =   {.level = {5, 5, 5, 5, 5, 5, 5, 0, 5}},
        .type[CHECK_RWCOIN] =  {.level = {1, 0, 0, 0, 0, 0, 0, 0, 0}},
        .type[CHECK_FAIRY] =   {.level = {2, 2, 2, 2, 2, 2, 2, 4, 2}},
        .type[CHECK_NINCOIN] = {.level = {1, 0, 0, 0, 0, 0, 0, 0, 0}},
        .type[CHECK_BP] =      {.level = {5, 5, 5, 5, 5, 5, 5, 5, 0}},
        .type[CHECK_KONG] =    {.level = {5, 0, 0, 0, 0, 0, 0, 0, 0}},
        .type[CHECK_BEAN] =    {.level = {0, 0, 0, 0, 1, 0, 0, 0, 0}},
        .type[CHECK_PEARLS] =  {.level = {0, 0, 0, 5, 0, 0, 0, 0, 0}},
        .type[CHECK_RAINBOW] = {.level = {0, 0, 0, 0, 0, 0, 0, 0, 0}},
        .type[CHECK_HINTS] =   {.level = {5, 5, 5, 5, 5, 5, 5, 0, 0}},
        .type[CHECK_CRATE] =   {.level = {0, 0, 0, 0, 0, 0, 0, 0, 0}},
    }
};

void initItemCheckDenominators(void) {
    if (Rando.isles_cb_rando) {
        check_data.denominator.type[CHECK_MEDAL].level[LEVEL_ISLES] = 5;
    }
    for (int lvl = 0; lvl < 9; lvl++) {
        int rainbow_count = 0;
        int crate_count = 0;
        for (int k = 0; k < 16; k++) {
            if (k < 13) {
                if (getCrateWorld(k) == lvl) {
                    crate_count += 1;
                }
            }
            if (getPatchWorld(k) == lvl) {
                rainbow_count += 1;
            }
        }
        check_data.denominator.type[CHECK_RAINBOW].level[lvl] = rainbow_count;
        check_data.denominator.type[CHECK_CRATE].level[lvl] = crate_count;
    }
}

void checkItemDB(void) {
    /**
     * @brief Check item database for variables, and change check screen totals to accommodate
     */
    //renderScreenTransition(7);
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
            check_data.numerator.type[i].level[j] = 0;
        }
        // Check FLUT
        for (int k = 0; k < (sizeof(item_db) / sizeof(check_struct)); k++) {
            if (item_db[k].type == i) {
                int lvl = item_db[k].associated_level;
                check_data.numerator.type[i].level[lvl] += checkFlag(item_db[k].flag, FLAGTYPE_PERMANENT);
            }
        }
    }
    // Check extra flags
    for (int k = 0; k < 35; k++) {
        if (k < 16)  {
            if (k < 13) {
                check_data.numerator.type[CHECK_CRATE].level[getCrateWorld(k)] += checkFlag(FLAG_MELONCRATE_0 + k, FLAGTYPE_PERMANENT);
            }
            check_data.numerator.type[CHECK_RAINBOW].level[getPatchWorld(k)] += checkFlag(FLAG_RAINBOWCOIN_0 + k, FLAGTYPE_PERMANENT);
        }
        int hint_level = k / 5;
        check_data.numerator.type[CHECK_HINTS].level[hint_level] += checkFlag(FLAG_WRINKLYVIEWED + k, FLAGTYPE_PERMANENT);
    }
}

void handleCShifting(char* value, char limit) {
    if ((NewlyPressedControllerInput.Buttons.c_left) || (NewlyPressedControllerInput.Buttons.d_left)) {
        *value -= 1;
        if (*value < 0) {
            *value = limit - 1;
        }
    } else if ((NewlyPressedControllerInput.Buttons.c_right) || (NewlyPressedControllerInput.Buttons.d_right)) {
        *value += 1;
        if (*value >= limit) {
            *value = 0;
        }
    }
}

Gfx* pauseScreen3And4Header(Gfx* dl) {
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
        return drawHintScreen(dl, level_x);
    } else if (paad->screen == PAUSESCREEN_ITEMLOCATIONS) {
        return drawItemLocationScreen(dl, level_x);
    }
    return dl;
}

static char teststr[5] = "";

Gfx* drawTextPointers(Gfx* dl) {
    if ((TBVoidByte & 2) && (display_billboard_fix)) {
        dk_strFormat((char *)teststr, "%d", hints_initialized);
        dl = drawPixelTextContainer(dl, 0, 0, teststr, 0, 0, 0, 0xFF, 1);
    }
    return dl;
}

Gfx* pauseScreen3And4ItemName(Gfx* dl, int x, int y, float scale, char* text) {
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

Gfx* pauseScreen3And4Counter(int x, int y, int top, int bottom, Gfx* dl, int unk0, int scale) {
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
                top_num += check_data.numerator.type[item_index].level[i];
                bottom_num += check_data.denominator.type[item_index].level[i];
            }
        } else {
            int lvl = check_level - 1;
            if ((item_index == CHECK_RWCOIN) || (item_index == CHECK_NINCOIN) || (item_index == CHECK_KONG)) {
                // Nin/RW Coin, Kongs
                lvl = 0;
            }
            top_num = check_data.numerator.type[item_index].level[lvl];
            bottom_num = check_data.denominator.type[item_index].level[lvl];
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
    if (Rando.quality_of_life.fast_pause_transitions) {
        playSound(0xE9, 0x7FF, 63.0f, 1.0f, 0, 0);
    } else {
        playSFX(0x2C9);
    }
}

int changeSelectedLevel(int unk0, int unk1) {
    /**
     * @brief Change selected level in the checks screen
     */
    pause_paad* paad = CurrentActorPointer_0->paad;
    if (paad->screen == PAUSESCREEN_CHECKS) {
        // Checks Screen
        handleCShifting(&check_level, sizeof(levels) / 4);
    }
    return getPauseWheelRotationProgress(unk0, unk1);
}

void updateFileVariables(void) {
    /**
     * @brief Update file variables on pause menu initialization
     */
    updateFilePercentage();
    getHintRegionText();
    initCarousel_onPause();
}

Gfx* handleOutOfCounters(int x, int y, int top, int bottom, Gfx* dl, int unk0, int scale) {
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
    
    initCarousel_onBoot();
    initHintFlags();
}