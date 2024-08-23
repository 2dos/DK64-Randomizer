/**
 * @file hints.c
 * @author Ballaam
 * @brief Pause Hints Handling Functions
 * @version 0.1
 * @date 2023-10-11
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define STRING_MAX_SIZE 256
#define ELLIPSIS_CUTOFF 125
#define GAME_HINT_COUNT 35
#define HINT_SOLVED_OPACITY 0x80

typedef enum itemloc_subgroups {
    ITEMLOC_DKMOVES,
    ITEMLOC_DIDDYMOVES,
    ITEMLOC_LANKYMOVES,
    ITEMLOC_TINYMOVES,
    ITEMLOC_CHUNKYMOVES,
    ITEMLOC_GUNUPGRADES,
    ITEMLOC_BFITRAINING,
    ITEMLOC_INSUPG,
    ITEMLOC_KONGS,
    ITEMLOC_SHOPKEEPERS,
    ITEMLOC_EARLYKEYS,
    ITEMLOC_LATEKEYS,
    ITEMLOC_TERMINATOR,
} itemloc_subgroups;

typedef struct itemloc_data {
    /* 0x000 */ char* header;
    /* 0x004 */ unsigned short flags[6];
    /* 0x010 */ char lengths[6];
} itemloc_data;

char hints_initialized = 0;
char display_billboard_fix = 0;
static char string_copy[STRING_MAX_SIZE] = "";
static char mtx_counter = 0;
static char* unk_string = "???";
static short hint_clear_flags[35] = {};
static short hint_item_regions[35] = {};
static char hint_level = 0;
static char item_subgroup = 0;
static char level_hint_text[0x40] = "";
static char item_loc_text[0x40] = "";

static itemloc_data itemloc_textnames[] = {
    {
        .header="DONKEY MOVES", 
        .flags={0x8001, 0x8002, 0x8003, 0x8201, 0x8401, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="DIDDY MOVES", 
        .flags={0x9001, 0x9002, 0x9003, 0x9201, 0x9401, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="LANKY MOVES", 
        .flags={0xA001, 0xA002, 0xA003, 0xA201, 0xA401, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="TINY MOVES", 
        .flags={0xB001, 0xB002, 0xB003, 0xB201, 0xB401, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="CHUNKY MOVES", 
        .flags={0xC001, 0xC002, 0xC003, 0xC201, 0xC401, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="GUN UPGRADES AND FAIRY MOVES", 
        .flags={0xD202, 0xD203, FLAG_ITEM_BELT_0, FLAG_ABILITY_CAMERA, FLAG_ABILITY_SHOCKWAVE, 0}, 
        .lengths={1, 1, 2, 1, 1, -1}
    }, // 6
    {
        .header="BASIC MOVES", 
        .flags={FLAG_TBARREL_DIVE, FLAG_TBARREL_ORANGE, FLAG_TBARREL_BARREL, FLAG_TBARREL_VINE, FLAG_ABILITY_CLIMBING, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="INSTRUMENT UPGRADES AND SLAMS", 
        .flags={FLAG_ITEM_INS_0, FLAG_ITEM_SLAM_0, 0, 0, 0, 0}, 
        .lengths={3, 3, -1, -1, -1, -1}
    }, // 6
    {
        .header="KONGS", 
        .flags={FLAG_KONG_DK, FLAG_KONG_DIDDY, FLAG_KONG_LANKY, FLAG_KONG_TINY, FLAG_KONG_CHUNKY, 0}, 
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="SHOPKEEPERS", 
        .flags={FLAG_ITEM_CRANKY, FLAG_ITEM_CANDY, FLAG_ITEM_FUNKY, FLAG_ITEM_SNIDE, 0, 0}, 
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 4
    {
        .header="EARLY KEYS", 
        .flags={FLAG_KEYHAVE_KEY1, FLAG_KEYHAVE_KEY2, FLAG_KEYHAVE_KEY3, FLAG_KEYHAVE_KEY4, 0, 0}, 
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 5
    {
        .header="LATE KEYS", 
        .flags={FLAG_KEYHAVE_KEY5, FLAG_KEYHAVE_KEY6, FLAG_KEYHAVE_KEY7, FLAG_KEYHAVE_KEY8, 0, 0}, 
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 5
};

static unsigned char progressive_ding_timer = 0;

void initProgressiveTimer(void) {
    progressive_ding_timer = 52;
}

Gfx* renderProgressiveSprite(Gfx* dl) {
    return renderIndicatorSprite(dl, 108, 0, &progressive_ding_timer, 48, 48, IA8);
}

void playProgressiveDing(void) {
    initProgressiveTimer();
    playSFX(0x2EA);
}

void handleProgressiveIndicator(int delta) {
    if (Rando.progressive_hint_gb_cap == 0) {
        return;
    }
    int gb_count = getTotalGBs();
    int old_progressive_level = -1;
    int new_progressive_level = -1;
    for (int i = 0; i < GAME_HINT_COUNT; i++) {
        int local_req = getHintGBRequirement(i);
        if (gb_count >= local_req) {
            new_progressive_level = i;
        }
        if ((gb_count - delta) >= local_req) {
            old_progressive_level = i;
        }
    }
    if (old_progressive_level != new_progressive_level) {
        playProgressiveDing();
    }
}

void initHints(void) {
    if (!hints_initialized) {
        for (int i = 0; i < 35; i++) {
            hint_pointers[i] = (int)getTextPointer(45, 1+i, 0); // 41 if you want to read from the regular wrinkly hint file
        }
        for (int i = 0; i < LOCATION_ITEM_COUNT; i++) {
            itemloc_pointers[i] = getTextPointer(44, i, 0);
        }
        hints_initialized = 1;
    }
    display_billboard_fix = 0;
}

void wipeHintCache(void) {
    for (int i = 0; i < 35; i++) {
        hint_pointers[i] = 0;
    }
    for (int i = 0; i < LOCATION_ITEM_COUNT; i++) {
        itemloc_pointers[i] = (char*)0;
    }
    hints_initialized = 0;
}

Gfx* drawHintText(Gfx* dl, char* str, int x, int y, int opacity, int center, int enable_recolor) {
    mtx_item mtx0;
    mtx_item mtx1;
    _guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
    float position = y;
    float hint_x = x;
    if (center) {
        hint_x = 640.0f;
    }
    _guTranslateF(&mtx1, hint_x, position, 0.0f);
    _guMtxCatF(&mtx0, &mtx1, &mtx0);
    _guTranslateF(&mtx1, 0.0f, 48.0f, 0.0f);
    _guMtxCatF(&mtx0, &mtx1, &mtx0);
    _guMtxF2L(&mtx0, &static_mtx[(int)mtx_counter]);
    gSPDisplayList(dl++, 0x01000118);
    gSPMatrix(dl++, 0x02000180, G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
    gDPPipeSync(dl++);
    gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(dl++, 0, 0, (base_text_color >> 24) & 0xFF, (base_text_color >> 16) & 0xFF, (base_text_color >> 8) & 0xFF, opacity);
    gSPMatrix(dl++, (int)&static_mtx[(int)mtx_counter], G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
    int data = 0x80;
    if (!center) {
        data = 0;
    }
    if (Rando.pause_hints_colored == 0) {
        enable_recolor = 0;
    }
    if (enable_recolor) {
        setCharacterRecoloring(1, str);
        data |= 0x12;
    }
    dl = displayText(dl,6,0,0,str,data);
    setCharacterRecoloring(0, (char*)0);
    mtx_counter += 1;
    gSPPopMatrix(dl++, G_MTX_MODELVIEW);
    return dl;
}

#define SPLIT_STRING_LINE_LIMIT 50
  
Gfx* drawSplitString(Gfx* dl, char* str, int x, int y, int y_sep, int opacity) {
    int curr_y = y;
    int string_length = cstring_strlen(str);
    int trigger_ellipsis = 0;
    if ((unsigned int)(string_length) > STRING_MAX_SIZE) {
        string_length = STRING_MAX_SIZE;
    }
    int string_copy_ref = (int)string_copy;
    wipeMemory(string_copy, STRING_MAX_SIZE);
    dk_memcpy(string_copy, str, string_length);
    string_copy[STRING_MAX_SIZE - 2] = 0;
    string_copy[STRING_MAX_SIZE - 1] = 0;
    int header = 0;
    int letter_count = 0;
    int last_safe = 0;
    int line_count = 0;
    int color_index = 0;
    int force_split = 0;
    while (1) {
        char referenced_character = *(char*)(string_copy_ref + header);
        int is_control = 0;
        if (referenced_character == 0) {
            // Terminator
            return drawHintText(dl, (char*)(string_copy_ref), x, curr_y, opacity, 1, 1);
        } else if (referenced_character == 0x20) {
            // Space
            last_safe = header;
            int seg_addition = 1;
            while (1) {
                char ref_seg_character = *(char*)(string_copy_ref + header + seg_addition);
                if ((ref_seg_character == 0) || (ref_seg_character == 0x20)) {
                    break;
                } else {
                    seg_addition++;
                }
            }
            if ((header + seg_addition) > SPLIT_STRING_LINE_LIMIT) {
                force_split = 1;
            }
        } else if ((referenced_character > 0) && (referenced_character <= 0x10)) {
            // Control byte character
            if ((referenced_character >= 4) && (referenced_character <= 0xD)) {
                int temp_color = referenced_character - 3;
                if (temp_color == color_index) {
                    color_index = 0;
                } else {
                    color_index = temp_color;
                }
            }
            is_control = 1;
            int end = (int)(string_copy) + (STRING_MAX_SIZE - 1);
            int size = end - (string_copy_ref + header + 1);
            dk_memcpy((void*)(string_copy_ref + header), (void*)(string_copy_ref + header + 1), size);
        } else {
            // Actual letter or punctuation
            letter_count += 1;
            if(letter_count >= ELLIPSIS_CUTOFF){
                *(char*)(referenced_character) = 0;
                if(header > 2){
                    // It should be impossible to hit 125 characters without being more than 2 characters into the third line
                    // Insert ellipsis 
                    *(char*)(string_copy_ref + header - 1) = 0x2E;
                    *(char*)(string_copy_ref + header - 2) = 0x2E;
                    *(char*)(string_copy_ref + header - 3) = 0x2E;
                }
                // It's also now a terminator, so:
                return drawHintText(dl, (char*)(string_copy_ref), x, curr_y, opacity, 1, 1);
            }
        }
        setCharacterColor(header, color_index, opacity);
        if (!is_control) {
            if ((header > SPLIT_STRING_LINE_LIMIT) || (force_split)) {
                *(char*)(string_copy_ref + last_safe) = 0; // Stick terminator in last safe
                dl = drawHintText(dl, (char*)(string_copy_ref), x, curr_y, opacity, 1, 1);
                line_count += 1;
                if (line_count == 3) {
                    return dl;
                }
                curr_y += y_sep;
                string_copy_ref += (last_safe + 1);
                header = 0;
                last_safe = 0;
                force_split = 0;
            } else {
                header += 1;
            }
        }
    }
    return dl;
}

static unsigned char hints_per_screen = 5;
static unsigned char hint_screen_count = 7;
static unsigned char hint_offset = 140;

int getHintGBRequirement(int slot) {
    int cap = Rando.progressive_hint_gb_cap;
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

regions getHintItemRegion(int slot) {
    return hint_item_regions[slot];
}

int getPluralCharacter(int amount) {
    if (amount != 1) {
        return 0x53; // "S"
    }
    return 0;
}

int showHint(int slot) {
    if (Rando.progressive_hint_gb_cap > 0) {
        int req = getHintGBRequirement(slot);
        int gb_count = getTotalGBs();
        return gb_count >= req;
    }
    // Not progressive hints
    return checkFlagDuplicate(FLAG_WRINKLYVIEWED + slot, FLAGTYPE_PERMANENT);
}

Gfx* displayBubble(Gfx* dl) {
    int opacity = 0xFF;
    int bubble_x = 625;
    int y = 480;
    float x_scale = 26.0f;
    float y_scale = 21.5f;
    if (Rando.dark_mode_textboxes) {
        opacity = 0x96;
        y = 465;
        x_scale = 24.0f;
        y_scale = 20.0f;
    }
    gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, opacity);
    return displayImage(dl, 107, 0, RGBA16, 48, 32, bubble_x, y, x_scale, y_scale, 0, 0.0f);
}

int getTiedShopmoveFlag(int flag) {
    if (flag == FLAG_ITEM_SLAM_0) {
        return FLAG_SHOPMOVE_SLAM_0;
    } else if (flag == FLAG_ITEM_INS_0) {
        return FLAG_SHOPMOVE_INS_0;
    } else if (flag == FLAG_ITEM_BELT_0) {
        return FLAG_SHOPMOVE_BELT_0;
    }
    return 0;
}

void getItemSpecificity(char** str, int step, int flag) {
    int tied_flag = getTiedShopmoveFlag(flag);
    if (tied_flag == 0) {
        return;
    }
    int base_set = checkFlagDuplicate(flag + step, FLAGTYPE_PERMANENT) || checkFlagDuplicate(tied_flag + step, FLAGTYPE_PERMANENT);
    if (base_set) {
        return;
    }
    if (flag == FLAG_ITEM_SLAM_0) {
        int slams[] = {Rando.moves_pregiven.slam_upgrade_0, Rando.moves_pregiven.slam_upgrade_1, Rando.moves_pregiven.slam_upgrade_2};
        if (slams[step]) {
            return;
        }
    } else if (flag == FLAG_ITEM_BELT_0) {
        int belts[] = {Rando.moves_pregiven.belt_upgrade_0, Rando.moves_pregiven.belt_upgrade_1};
        if (belts[step]) {
            return;
        }
    } else if (flag == FLAG_ITEM_INS_0) {
        int instrument_upgrades[] = {Rando.moves_pregiven.ins_upgrade_0, Rando.moves_pregiven.ins_upgrade_1, Rando.moves_pregiven.ins_upgrade_2};
        if (instrument_upgrades[step]) {
            return;
        }
    } else {
        return;
    }
    *str = unk_string;
}

void initHintFlags(void) {
    unsigned short* hint_clear_write = getFile(GAME_HINT_COUNT << 1, 0x1FFE000);
    unsigned short* hint_reg_write = getFile(GAME_HINT_COUNT << 1, 0x1FFE080);
    if (Rando.progressive_hint_gb_cap > 0) {
        hints_per_screen = 4;
        hint_screen_count = 9;
        hint_offset = 170;
    }
    for (int i = 0; i < GAME_HINT_COUNT; i++) {
        hint_clear_flags[i] = hint_clear_write[i];
        hint_item_regions[i] = hint_reg_write[i];
    }
}

Gfx* drawHintScreen(Gfx* dl, int level_x) {
    display_billboard_fix = 1;
    dl = printText(dl, level_x, 0x3C, 0.65f, "HINTS");
    // Handle Controls
    handleCShifting(&hint_level, hint_screen_count);
    // Display level
    if (Rando.progressive_hint_gb_cap > 0) {
        if (hint_level == 8) {
            dk_strFormat((char*)level_hint_text, "w BATCHES 9 AND 10 e");
        } else {
            dk_strFormat((char*)level_hint_text, "w BATCH %d e", hint_level + 1);
        }
    } else {
        dk_strFormat((char*)level_hint_text, "w %s e", levels[(int)hint_level + 1]);
    }
    dl = printText(dl, level_x, 120, 0.5f, level_hint_text);
    // Display Hints
    dl = displayBubble(dl);
    mtx_counter = 0;
    for (int i = 0; i < hints_per_screen; i++) {
        int hint_local_index = (hints_per_screen * hint_level) + i;
        if (hint_local_index > 34) {
            return dl;
        }
        if (showHint(hint_local_index)) {
            int opacity = 0xFF;
            int assoc_flag = hint_clear_flags[hint_local_index];
            if (assoc_flag != -1) {
                if (hasMove(assoc_flag)) {
                    opacity = HINT_SOLVED_OPACITY;
                }
            }
            dl = drawSplitString(dl, (char*)hint_pointers[hint_local_index], level_x, hint_offset + (120 * i), 40, opacity);
        } else {
            if (Rando.progressive_hint_gb_cap == 0) {
                regions tied_region = getHintItemRegion(hint_local_index);
                if (tied_region == REGION_NULLREGION) {
                    unknown_hints[i] = "???";
                } else {
                    dk_strFormat(unknown_hints[i], "??? - %s", hint_region_names[tied_region]);
                }
            } else {
                int requirement = getHintGBRequirement(hint_local_index);
                dk_strFormat(unknown_hints[i], "??? - %d GOLDEN BANANA%c", requirement, getPluralCharacter(requirement));
            }
            dl = drawSplitString(dl, unknown_hints[i], level_x, hint_offset + (120 * i), 40, 0xFF);
        }
        
    }
    return dl;
}

Gfx* drawItemLocationScreen(Gfx* dl, int level_x) {
    display_billboard_fix = 1;
    dl = printText(dl, level_x, 0x3C, 0.65f, "ITEM LOCATIONS");
    // Handle Controls
    handleCShifting(&item_subgroup, ITEMLOC_TERMINATOR);
    // Display subgroup
    dk_strFormat(&item_loc_text[0], "w %s e", itemloc_textnames[(int)item_subgroup].header);
    dl = printText(dl, level_x, 120, 0.5f, &item_loc_text[0]);
    // Display Hints
    dl = displayBubble(dl);
    int item_loc_x = 200;
    mtx_counter = 0;
    int head = 0;
    int k = 0;
    while (k < item_subgroup) {
        for (int l = 0; l < 6; l++) {
            head += itemloc_textnames[k].lengths[l];
            head += 1;
        }
        k++;
    }
    int i = 0;
    int y = 140;
    while (i < 6) {
        int size = itemloc_textnames[(int)item_subgroup].lengths[i];
        if (size == -1) {
            break;
        }
        dl = drawHintText(dl, itemloc_pointers[head], item_loc_x, y, 0xFF, 0, 0);
        for (int j = 0; j < size; j++) {
            y += 40;
            char* str = itemloc_pointers[head + 1 + j];
            short base_flag = itemloc_textnames[(int)item_subgroup].flags[i];
            short flag = base_flag + j;
            if ((base_flag == FLAG_ITEM_BELT_0) || (base_flag == FLAG_ITEM_INS_0) || (base_flag == FLAG_ITEM_SLAM_0)) {
                getItemSpecificity(&str, j, base_flag);
            } else {
                if (!hasMove(flag)) {
                    str = unk_string;
                }
            }
            
            dl = drawHintText(dl, str, item_loc_x, y, 0xC0, 0, 0);
        }
        head += 1 + size;
        y += 60;
        i++;
    }
    return dl;
}