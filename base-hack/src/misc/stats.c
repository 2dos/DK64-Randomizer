/**
 * @file stats.c
 * @author Ballaam
 * @brief Changes regarding file statistics
 * @version 0.1
 * @date 2023-04-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

static int igt_running_lasttag = 0;
unsigned short GameStats[STAT_TERMINATOR] = {0};

void setKongIgt(void) {
    igt_running_lasttag = FrameReal / 60;
}

void updatePercentageKongStat(void) {
    int current_kong_diff = (FrameReal / 60) - igt_running_lasttag;
    if (current_kong_diff > 0) {
        int current_kong = Character;
        if (Player) {
            current_kong = Player->characterID - 2;
        }
        if (current_kong <= 4) {
            if (CurrentMap != MAP_MAINMENU) {
                int old = ReadFile(DATA_IGT_DK + current_kong, 0, 0, FileIndex);
                SaveToFile(DATA_IGT_DK + current_kong, 0, 0, FileIndex, old + current_kong_diff);
            }
        }
        setKongIgt();
    }
}

void updateTagStat(void* data) {
    int next_kong = Character;
    int prev_kong = Player->characterID - 2;
    if (next_kong != prev_kong) {
        if (next_kong <= KONG_CHUNKY) {
            if (prev_kong <= KONG_CHUNKY) {
                GameStats[STAT_TAGCOUNT]++;
                updatePercentageKongStat();
            }
        }
    }
    updateModel(data);
}

void updateFairyStat(void) {
    GameStats[STAT_PHOTOSTAKEN]++;
    changeCollectableCount(6, 0, -1);
}

void updateEnemyKillStat(void) {
    // Change character for K Rool
    if (Rando.race_coins_shuffled) {
        if (levelIndexMapping[DestMap] != LEVEL_BONUS) {
            // Using dest map because it's early in the loadmap process
            RaceCoinCount = getItemCount_new(REQITEM_RACECOIN, 0, 0);
        }
    }
    fixKRoolKong();
    resetDisplayedMusic(); // Just to prevent against free issues
    // Update Stat
    if (isGamemode(GAMEMODE_ADVENTURE, 1) && (canSaveHelmHurry())) {
        GameStats[STAT_ENEMIESKILLED] += EnemiesKilledCounter;
    }
    handleMusicTransition();
}

typedef struct dynamic_credits_item {
    /* 0x000 */ char* header;
    /* 0x004 */ unsigned char global_data;
    /* 0x005 */ unsigned char sub_data;
    /* 0x006 */ unsigned char has_data;
} dynamic_credits_item;

static const dynamic_credits_item stat_credits_items[] = {
    {.header = "GAME STATISTICS",   .global_data = 0,                       .sub_data = 0, .has_data = 0},
    {.header = "KONG PLAYTIME",     .global_data = 0,                       .sub_data = 0, .has_data = 0},
    {.header = "DK: ",              .global_data = DATA_IGT_DK,             .sub_data = 1, .has_data = 1},
    {.header = "DIDDY: ",           .global_data = DATA_IGT_DIDDY,          .sub_data = 1, .has_data = 1},
    {.header = "LANKY: ",           .global_data = DATA_IGT_LANKY,          .sub_data = 1, .has_data = 1},
    {.header = "TINY: ",            .global_data = DATA_IGT_TINY,           .sub_data = 1, .has_data = 1},
    {.header = "CHUNKY: ",          .global_data = DATA_IGT_CHUNKY,         .sub_data = 1, .has_data = 1},
    {.header = "MISC STATS",        .global_data = 0,                       .sub_data = 0, .has_data = 0},
    {.header = "TAGS: ",            .global_data = DATA_STAT_TAG,           .sub_data = 2, .has_data = 1},
    {.header = "PHOTOS TAKEN: ",    .global_data = DATA_STAT_PHOTOS,        .sub_data = 2, .has_data = 1},
    {.header = "CAUGHT BY KOPS: ",  .global_data = DATA_STAT_KAUGHT,        .sub_data = 2, .has_data = 1},
    {.header = "ENEMIES KILLED: ",  .global_data = DATA_STAT_ENEMY_KILLS,   .sub_data = 2, .has_data = 1},
    {.header = "TIMES TRAPPED: ",   .global_data = DATA_STAT_TRAPPED,       .sub_data = 2, .has_data = 1},
    {.header = "DEATHS: ",          .global_data = DATA_STAT_DEATHS,        .sub_data = 2, .has_data = 1},
};

static char number_text[10] = "";

#define STATIC_CREDITS_ALLOCATION 0x300
#define DYNAMIC_CREDITS_ALLOCATION 0x200

char* createEndSeqCreditsFile(void) {
    char* text_data = dk_malloc(STATIC_CREDITS_ALLOCATION + DYNAMIC_CREDITS_ALLOCATION);
    int write_position = 0;
    int raw_write_location = (int)text_data;
    // Calculate total kong IGT
    int total_kong = 0;
    for (int j = 0; j < 5; j++) {
        total_kong += ReadFile(DATA_IGT_DK + j, 0, 0, FileIndex);
    }
    // Calculate Strings
    for (int i = 0; i < (int)(sizeof(stat_credits_items)/sizeof(dynamic_credits_item)); i++) {
        int header_length = cstring_strlen(stat_credits_items[i].header);
        dk_memcpy((void*)(raw_write_location + write_position), stat_credits_items[i].header, header_length);
        write_position += header_length;
        if (stat_credits_items[i].has_data) {
            int value = 0;
            int global_data = stat_credits_items[i].global_data;
            if (stat_credits_items[i].sub_data == 2) {
                // Stats
                value = ReadFile(global_data, 0, 0, FileIndex);
                dk_strFormat(number_text, "%d", value);
            } else if (stat_credits_items[i].sub_data == 1) {
                // Kong IGT
                int current_kong = ReadFile(global_data, 0, 0, FileIndex);
                float value_f = 0.0f;
                if (total_kong != 0) {
                    value_f = 100 * current_kong;
                    value_f /= total_kong;
                }
                dk_strFormat(number_text, "%.1f%%", value_f);
            }
            dk_memcpy((void*)(raw_write_location + write_position), number_text, 10);
            write_position += cstring_strlen(number_text);
        }
        *(char*)(raw_write_location + write_position) = 0xA; // Newline character
        write_position += 1;
    }
    void* raw_text_data = getMapData(0x13, 7, 1, 1);
    dk_memcpy((void*)(raw_write_location + write_position), raw_text_data, STATIC_CREDITS_ALLOCATION);
    return text_data;
}