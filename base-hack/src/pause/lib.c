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
static char level_check_text[0x18] = "";

static unsigned char check_data[2][9][CHECK_TERMINATOR] = {}; // 8 items, 9 levels, numerator + denominator

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
        return drawHintScreen(dl, level_x);
    } else if (paad->screen == PAUSESCREEN_ITEMLOCATIONS) {
        return drawItemLocationScreen(dl, level_x);
    }
    return dl;
}

static char teststr[5] = "";

int* drawTextPointers(int* dl) {
    if ((TBVoidByte & 2) && (display_billboard_fix)) {
        dk_strFormat((char *)teststr, "%d", hints_initialized);
        dl = drawPixelTextContainer(dl, 0, 0, teststr, 0, 0, 0, 0xFF, 1);
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
    
    writeFunction(0x806A84C8, &updateFileVariables); // Update file variables to transfer old locations to current
    initCarousel_onBoot();
    if (Rando.item_rando) {
        writeFunction(0x806A9D50, &handleOutOfCounters); // Print out of counter, depending on item rando state
        writeFunction(0x806A9EFC, &handleOutOfCounters); // Print out of counter, depending on item rando state
        *(int*)(0x806A9C80) = 0; // Show counter on Helm Menu - Kong specific screeen
        *(int*)(0x806A9E54) = 0; // Show counter on Helm Menu - All Kongs screen
        // *(int*)(0x806AA860) = 0x31EF0007; // ANDI $t7, $t7, 7 - Show GB (Kong Specific)
        // *(int*)(0x806AADC4) = 0x33390007; // ANDI $t9, $t9, 7 - Show GB (All Kongs)
        // *(int*)(0x806AADC8) = 0xAFB90058; // SW $t9, 0x58 ($sp) - Show GB (All Kongs)
    }
    if (Rando.quality_of_life.fast_pause_transitions) {
        *(float*)(0x8075AC00) = 1.3f; // Pause Menu Progression Rate
        *(int*)(0x806A901C) = 0; // NOP - Remove thud
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
    // Disable Item Checks
    *(int*)(0x806AB2E8) = 0;
    *(int*)(0x806AB360) = 0;
    *(short*)(0x806ABFCE) = FLAG_BP_JAPES_DK_HAS; // Change BP trigger to being collecting BP rather than turning it in
    *(short*)(0x806A932A) = 0x2710; // Increase memory allocated for displaying the Pause menu (fixes hints corrupting the heap) Increase to 12500 at a later time
    initHintFlags();
}