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
    ITEMLOC_SPECIALITEMS,
    ITEMLOC_TERMINATOR,
} itemloc_subgroups;

typedef struct itemloc_data {
    /* 0x000 */ char* header;
    /* 0x004 */ char lengths[6];
    /* 0x00A */ char pad[2];
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

short itemloc_flags[] = {
    // DK Moves
    FLAG_SHOPFLAG + (LEVEL_JAPES * 5) + KONG_DK,
    FLAG_SHOPFLAG + (LEVEL_AZTEC * 5) + KONG_DK,
    FLAG_SHOPFLAG + (LEVEL_FACTORY * 5) + KONG_DK,
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_JAPES * 5) + KONG_DK,
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_AZTEC - LEVEL_AZTEC) * 5) + KONG_DK,
    // Diddy Moves
    FLAG_SHOPFLAG + (LEVEL_JAPES * 5) + KONG_DIDDY,
    FLAG_SHOPFLAG + (LEVEL_AZTEC * 5) + KONG_DIDDY,
    FLAG_SHOPFLAG + (LEVEL_FACTORY * 5) + KONG_DIDDY,
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_JAPES * 5) + KONG_DIDDY,
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_AZTEC - LEVEL_AZTEC) * 5) + KONG_DIDDY,
    // Lanky Moves
    FLAG_SHOPFLAG + (LEVEL_JAPES * 5) + KONG_LANKY,
    FLAG_SHOPFLAG + (LEVEL_AZTEC * 5) + KONG_LANKY,
    FLAG_SHOPFLAG + (LEVEL_FACTORY * 5) + KONG_LANKY,
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_JAPES * 5) + KONG_LANKY,
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_AZTEC - LEVEL_AZTEC) * 5) + KONG_LANKY,
    // Tiny Moves
    FLAG_SHOPFLAG + (LEVEL_JAPES * 5) + KONG_TINY,
    FLAG_SHOPFLAG + (LEVEL_AZTEC * 5) + KONG_TINY,
    FLAG_SHOPFLAG + (LEVEL_FACTORY * 5) + KONG_TINY,
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_JAPES * 5) + KONG_TINY,
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_AZTEC - LEVEL_AZTEC) * 5) + KONG_TINY,
    // Chunky Moves
    FLAG_SHOPFLAG + (LEVEL_JAPES * 5) + KONG_CHUNKY,
    FLAG_SHOPFLAG + (LEVEL_AZTEC * 5) + KONG_CHUNKY,
    FLAG_SHOPFLAG + (LEVEL_FACTORY * 5) + KONG_CHUNKY,
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_JAPES * 5) + KONG_CHUNKY,
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_AZTEC - LEVEL_AZTEC) * 5) + KONG_CHUNKY,
    // Gun Upgrades & Fairy Moves
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_FUNGI * 5) + KONG_DK, // Homing
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_CASTLE * 5) + KONG_DK, // Sniper
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_FACTORY * 5) + KONG_DK, // Ammo Belt
    FLAG_SHOPFLAG + (8 * 5) + (LEVEL_CAVES * 5) + KONG_DK, // Ammo Belt
    FLAG_ABILITY_SHOCKWAVE, // Camera
    FLAG_ABILITY_SHOCKWAVE, // Shockwave
    // Basic Moves
    FLAG_TBARREL_DIVE,
    FLAG_TBARREL_ORANGE,
    FLAG_TBARREL_BARREL,
    FLAG_TBARREL_VINE,
    FLAG_ABILITY_CLIMBING,
    // Instrument Upgrades and Slams
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + ((LEVEL_GALLEON - LEVEL_AZTEC) * 5) + KONG_DK, // Instrument Upgrade
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + (3 * 5) + ((LEVEL_CAVES - LEVEL_CAVES) * 5) + KONG_DK, // Instrument Upgrade
    FLAG_SHOPFLAG + (8 * 5) + (7 * 5) + (3 * 5) + ((LEVEL_CASTLE - LEVEL_CAVES) * 5) + KONG_DK, // Instrument Upgrade
    FLAG_ABILITY_SIMSLAM, // Slam
    FLAG_SHOPFLAG + (LEVEL_FUNGI * 5) + KONG_DK, // Slam
    FLAG_SHOPFLAG + (LEVEL_CASTLE * 5) + KONG_DK, // Slam
    // Kongs
    FLAG_KONG_DK,
    FLAG_KONG_DIDDY,
    FLAG_KONG_LANKY,
    FLAG_KONG_TINY,
    FLAG_KONG_CHUNKY,
    // Shopkeepers
    FLAG_ITEM_CRANKY,
    FLAG_ITEM_CANDY,
    FLAG_ITEM_FUNKY,
    FLAG_ITEM_SNIDE,
    // Keys
    FLAG_KEYHAVE_KEY1,
    FLAG_KEYHAVE_KEY2,
    FLAG_KEYHAVE_KEY3,
    FLAG_KEYHAVE_KEY4,
    FLAG_KEYHAVE_KEY5,
    FLAG_KEYHAVE_KEY6,
    FLAG_KEYHAVE_KEY7,
    FLAG_KEYHAVE_KEY8,
    // Special Items
    FLAG_COLLECTABLE_BEAN,
    FLAG_COLLECTABLE_NINTENDOCOIN,
    FLAG_COLLECTABLE_RAREWARECOIN,
};

static itemloc_data itemloc_textnames[] = {
    {
        .header="DONKEY MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="DIDDY MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="LANKY MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="TINY MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="CHUNKY MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="GUN UPGRADES AND FAIRY MOVES",
        .lengths={1, 1, 2, 1, 1, -1}
    }, // 6
    {
        .header="BASIC MOVES",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="INSTRUMENT UPGRADES AND SLAMS",
        .lengths={3, 3, -1, -1, -1, -1}
    }, // 6
    {
        .header="KONGS",
        .lengths={1, 1, 1, 1, 1, -1}
    }, // 5
    {
        .header="SHOPKEEPERS",
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 4
    {
        .header="EARLY KEYS",
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 4
    {
        .header="LATE KEYS",
        .lengths={1, 1, 1, 1, -1, -1}
    }, // 4
    {
        .header="SPECIAL ITEMS",
        .lengths={1, 1, 1, -1, -1, -1}
    }, // 3
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

static int old_progressive_level = -1;

void handleProgressiveIndicator(int allow_ding) {
    if (Rando.progressive_hint_gb_cap == 0) {
        return;
    }
    int item_count = getItemCountReq(Rando.prog_hint_item);
    int new_progressive_level = -1;
    for (int i = 0; i < GAME_HINT_COUNT; i++) {
        if (item_count >= getHintRequirement(i)) {
            new_progressive_level = i;
        }
    }
    if ((CurrentMap != MAP_MAINMENU) && (allow_ding)) {
        if (new_progressive_level > old_progressive_level) {
            playProgressiveDing();
        }
    }
    old_progressive_level = new_progressive_level;
}

void resetProgressive(void) {
    old_progressive_level = -1;
    handleProgressiveIndicator(0);
}

void initHints(void) {
    if (!hints_initialized) {
        // Wrinkly Hints (Pause Menu)
        int hint_index = 0;
        int line_index = 0;
        char *hint_text = getMapData(TABLE_UNK06, COMP_TEXT_WRINKLYSHORT - 0x40, 1, 1);
        hint_pointers[0].lines[0] = hint_text;
        while (hint_index < 35) {
            int val = *hint_text++;
            if (val == 0) {
                hint_index++;
                line_index = 0;
                if (hint_index < 35) {
                    hint_pointers[hint_index].lines[0] = hint_text;
                }
            } else if (val == 0xF) {
                hint_text[-1] = 0;
                line_index++;
                if (line_index < 3) {
                    hint_pointers[hint_index].lines[line_index] = hint_text;
                }
            }
        }
        // Item Locations
        int item_loc_index = 0;
        char *itemloc_text = getMapData(TABLE_UNK06, COMP_TEXT_ITEMLOCATIONS - 0x40, 1, 1);
        itemloc_pointers[0] = itemloc_text;
        while (item_loc_index < LOCATION_ITEM_COUNT) {
            int val = *itemloc_text++;
            if (val == 0) {
                item_loc_index++;
                if (item_loc_index < LOCATION_ITEM_COUNT) {
                    itemloc_pointers[item_loc_index] = itemloc_text;
                }
            }
        }
        hints_initialized = 1;
    }
    display_billboard_fix = 0;
}

void wipeHintCache(void) {
    for (int i = 0; i < 35; i++) {
        for (int j = 0; j < 3; j++) {
            hint_pointers[i].lines[j] = 0;
        }
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
  
Gfx* drawSplitString(Gfx* dl, FastTextStruct * data, int x, int y, int y_sep, int opacity) {
    int curr_y = y;
    int color_index = 0;
    for (int i = 0; i < 3; i++) {
        if (data->lines[i]) {
            char *txt = data->lines[i];
            int index = 0;
            while (1) {
                int character = *txt++;
                if (character == 0) {
                    break;
                } else if ((character >= 4) && (character <= 0xD)) {
                    int temp_color = character - 3;
                    if (temp_color == color_index) {
                        color_index = 0;
                    } else {
                        color_index = temp_color;
                    }
                }
                setCharacterColor(index, color_index, opacity);
                index++;
            }
            dl = drawHintText(dl, data->lines[i], x, curr_y, opacity, 1, 1);
        }
        curr_y += y_sep;
    }
    return dl;
}

static unsigned char hints_per_screen = 5;
static unsigned char hint_screen_count = 7;
static unsigned char hint_offset = 140;

int getHintRequirement(int slot) {
    int cap = Rando.progressive_hint_gb_cap;
    int batch_index = 9;
    if (slot < 34) {
        batch_index = slot >> 2;
    }
    return Rando.progressive_bounds[batch_index];
}

void displayCBCount(pause_paad *handler, void* sprite, int x, int y, float scale, int unk0, int unk1) {
    displaySprite(handler, sprite, x, y, scale, unk0, unk1);
    if (handler->screen == PAUSESCREEN_HINTS) {
        int cb_count = getItemCountReq(REQITEM_COLOREDBANANA);
        displayPauseSpriteNumber(handler, 0x24, 0x1C, 0xC, -10, cb_count, 1, 0);
        displaySprite(handler, (void*)0x80721474, 0x24, 0x1C, 0.75f, 2, 1);
    }
}

regions getHintItemRegion(int slot) {
    return hint_item_regions[slot];
}

int showHint(int slot) {
    if (Rando.progressive_hint_gb_cap > 0) {
        int req = getHintRequirement(slot);
        int gb_count = getItemCountReq(Rando.prog_hint_item);
        return gb_count >= req;
    }
    // Not progressive hints
    int level = slot / 5;
    return getItemCount_new(REQITEM_HINT, level, slot % 5);
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

const char* item_names[] = {
    "NOTHING",
    "KONG",
    "MOVE",
    "GOLDEN BANANA",
    "BLUEPRINT",
    "FAIRY",
    "KEY",
    "CROWN",
    "COMPANY COIN",
    "MEDAL",
    "BEAN",
    "PEARL",
    "RAINBOW COIN",
    "ICE TRAP",
    "%",
    "COLORED BANANA",
};
char item_name_plural[] = "COLORED BANANAS";

char* getItemName(int item_index, int item_count) {
    if ((item_count == 1) || (item_index == 14)) {
        // Item index 14 is game percentage, avoid pluralizing
        return item_names[item_index];
    }
    if (item_index == 5) {
        // We love grammar
        return "FAIRIES";
    }
    dk_strFormat(&item_name_plural, "%s%c", item_names[item_index], 'S');
    return &item_name_plural;
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
                if (checkFlag(assoc_flag, FLAGTYPE_PERMANENT)) {
                    opacity = HINT_SOLVED_OPACITY;
                }
            }
            dl = drawSplitString(dl, &hint_pointers[hint_local_index], level_x, hint_offset + (120 * i), 40, opacity);
        } else {
            if (Rando.progressive_hint_gb_cap == 0) {
                regions tied_region = getHintItemRegion(hint_local_index);
                if (tied_region == REGION_NULLREGION) {
                    dk_strFormat(unknown_hints[i].lines[0], "???");
                } else {
                    dk_strFormat(unknown_hints[i].lines[0], "??? - %s", hint_region_names[tied_region]);
                }
            } else {
                int requirement = getHintRequirement(hint_local_index);
                dk_strFormat(unknown_hints[i].lines[0], "??? - %d %s", requirement, getItemName(Rando.prog_hint_item, requirement));
            }
            dl = drawSplitString(dl, &unknown_hints[i], level_x, hint_offset + (120 * i), 40, 0xFF);
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
    int flag_head = 0;
    for (int k = 0; k < item_subgroup; k++) {
        for (int l = 0; l < 6; l++) {
            int length = itemloc_textnames[k].lengths[l];
            head += length;
            if (length > -1) {
                flag_head += length;
            }
            head += 1;
        }
    }
    int y = 140;
    for (int i = 0; i < 6; i++) {
        int size = itemloc_textnames[(int)item_subgroup].lengths[i];
        if (size == -1) {
            return dl;
        }
        dl = drawHintText(dl, itemloc_pointers[head], item_loc_x, y, 0xFF, 0, 0);
        for (int j = 0; j < size; j++) {
            y += 40;
            char* str = itemloc_pointers[head + 1 + j];
            short flag = itemloc_flags[flag_head + j];
            if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
                str = unk_string;
            }
            dl = drawHintText(dl, str, item_loc_x, y, 0xC0, 0, 0);
        }
        head += 1 + size;
        flag_head += size;
        y += 60;
    }
    return dl;
}