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

int changeStat(bonus_stat statistic, int delta) {
    int old = getStat(statistic);
    SaveExtraData(EGD_BONUSSTAT, statistic, old + delta);
    return old + delta;
}

void setStat(bonus_stat statistic, int amount) {
    SaveExtraData(EGD_BONUSSTAT, statistic, amount);
}

int getStat(bonus_stat statistic) {
    return ReadExtraData(EGD_BONUSSTAT, statistic);
}

typedef struct bonus_stat_info {
    /* 0x000 */ unsigned char index;
    /* 0x001 */ unsigned char count;
    /* 0x002 */ unsigned char required_bits;
} bonus_stat_info;

static bonus_stat_info sub_counts[] = {
    {.index = EGD_LEVELIGT, .count=9, .required_bits=19},
    {.index = EGD_HELMHURRYIGT, .count=1, .required_bits=22},
    {.index = EGD_HELMHURRYDISABLE, .count=1, .required_bits=1},
    {.index = EGD_BONUSSTAT, .count=STAT_TERMINATOR, .required_bits=16},
    {.index = EGD_KONGIGT, .count=5, .required_bits=20},
};
#define BONUS_COUNT 5

unsigned char* getBonusBlockStart(void) {
    int bits_total = 0;
    for (int i = 0; i < BONUS_COUNT; i++) {
        bits_total += (sub_counts[i].count * sub_counts[i].required_bits);
    }
    int head = 0x807ED6A8 - ((bits_total >> 3) + 1);
    head &= 0xFFFFFFFC;
    return (unsigned char*)head;
}

int getBitOffset(extra_global_data data_type, int sub_index) {
    int bits_total = 0;
    for (int i = 0; i < BONUS_COUNT; i++) {
        if (sub_counts[i].index == data_type) {
            bits_total += (sub_index * sub_counts[i].required_bits);
            return bits_total;
        } else {
            bits_total += (sub_counts[i].count * sub_counts[i].required_bits);
        }
    }
    return bits_total;
}

int getBitSize(extra_global_data data_type, int sub_index) {
    for (int i = 0; i < BONUS_COUNT; i++) {
        if (sub_counts[i].index == data_type) {
            return sub_counts[i].required_bits;
        }
    }
    return 0;
}

int ReadExtraData(extra_global_data data_type, int sub_index) {
    int bit_offset = getBitOffset(data_type, sub_index);
    unsigned char* start = getBonusBlockStart() + (bit_offset >> 3);
    bit_offset &= 7;
    int size = getBitSize(data_type, sub_index);
    int value = 0;
    for (int i = 0; i < size; i++) {
        int local_value = ((*start) >> bit_offset) & 1;
        value <<= 1;
        value |= local_value;
        bit_offset += 1;
        if (bit_offset >= 8) {
            bit_offset = 0;
            start += 1;
        }
    }
    return value;
}

void SaveExtraData(extra_global_data data_type, int sub_index, int value) {
    int bit_offset = getBitOffset(data_type, sub_index);
    unsigned char* start = getBonusBlockStart() + (bit_offset >> 3);
    bit_offset &= 7;
    int size = getBitSize(data_type, sub_index);
    for (int i = 0; i < size; i++) {
        int bit = (value >> ((size - 1) - i)) & 1;
        unsigned char and_comparator = 0xFF - (1 << bit_offset);
        *start = *start & and_comparator; // clear bit
        *start = *start | (bit << bit_offset); // Set bit
        bit_offset += 1;
        if (bit_offset >= 8) {
            bit_offset = 0;
            start += 1;
        }
    }
}

void ResetExtraData(extra_global_data data_type, int sub_index) {
    SaveExtraData(data_type, sub_index, 0);
}

static int igt_running_lasttag = 0;

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
                int old = ReadExtraData(EGD_KONGIGT, current_kong);
                SaveExtraData(EGD_KONGIGT, current_kong, old + current_kong_diff);
            }
        }
        setKongIgt();
    }
}

void genericStatUpdate(bonus_stat stat) {
    if (isGamemode(GAMEMODE_ADVENTURE, 1) && (canSaveHelmHurry())) {
        changeStat(stat, 1);
        if (stat == STAT_TAGCOUNT) {
            updatePercentageKongStat();
        }
        SaveToGlobal();
    }
}

void updateTagStat(void* data) {
    int next_kong = Character;
    int prev_kong = Player->characterID - 2;
    if (next_kong != prev_kong) {
        if (next_kong <= KONG_CHUNKY) {
            if (prev_kong <= KONG_CHUNKY) {
                genericStatUpdate(STAT_TAGCOUNT);
            }
        }
    }
    updateModel(data);
}

void updateFairyStat(void) {
    genericStatUpdate(STAT_PHOTOSTAKEN);
    changeCollectableCount(6, 0, -1);
}

void updateKopStat(void) {
    genericStatUpdate(STAT_KOPCAUGHT);
}

void updateEnemyKillStat(void) {
    // Change character for K Rool
    fixKRoolKong();
    resetDisplayedMusic(); // Just to prevent against free issues
    // Update Stat
    if (isGamemode(GAMEMODE_ADVENTURE, 1) && (canSaveHelmHurry())) {
        changeStat(STAT_ENEMIESKILLED, EnemiesKilledCounter);
        SaveToGlobal();
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
    {.header = "GAME STATISTICS", .global_data = 0, .sub_data = 0, .has_data = 0},
    {.header = "KONG PLAYTIME", .global_data = 0, .sub_data = 0, .has_data = 0},
    {.header = "DK: ", .global_data = EGD_KONGIGT, .sub_data = 0, .has_data = 1},
    {.header = "DIDDY: ", .global_data = EGD_KONGIGT, .sub_data = 1, .has_data = 1},
    {.header = "LANKY: ", .global_data = EGD_KONGIGT, .sub_data = 2, .has_data = 1},
    {.header = "TINY: ", .global_data = EGD_KONGIGT, .sub_data = 3, .has_data = 1},
    {.header = "CHUNKY: ", .global_data = EGD_KONGIGT, .sub_data = 4, .has_data = 1},
    {.header = "MISC STATS", .global_data = 0, .sub_data = 0, .has_data = 0},
    {.header = "TAGS: ", .global_data = EGD_BONUSSTAT, .sub_data = STAT_TAGCOUNT, .has_data = 1},
    {.header = "PHOTOS TAKEN: ", .global_data = EGD_BONUSSTAT, .sub_data = STAT_PHOTOSTAKEN, .has_data = 1},
    {.header = "CAUGHT BY KOPS: ", .global_data = EGD_BONUSSTAT, .sub_data = STAT_KOPCAUGHT, .has_data = 1},
    {.header = "ENEMIES KILLED: ", .global_data = EGD_BONUSSTAT, .sub_data = STAT_ENEMIESKILLED, .has_data = 1},
};

static char number_text[10] = "";

#define STATIC_CREDITS_ALLOCATION 0x300
#define DYNAMIC_CREDITS_ALLOCATION 0x200

char* createEndSeqCreditsFile(void) {
    char* text_data = dk_malloc(STATIC_CREDITS_ALLOCATION + DYNAMIC_CREDITS_ALLOCATION);
    int write_position = 0;
    int raw_write_location = (int)text_data;
    for (int i = 0; i < (int)(sizeof(stat_credits_items)/sizeof(dynamic_credits_item)); i++) {
        int header_length = cstring_strlen(stat_credits_items[i].header);
        dk_memcpy((void*)(raw_write_location + write_position), stat_credits_items[i].header, header_length);
        write_position += header_length;
        if (stat_credits_items[i].has_data) {
            int value = 0;
            int global_data = stat_credits_items[i].global_data;
            if (global_data == EGD_BONUSSTAT) {
                value = getStat(stat_credits_items[i].sub_data);
                dk_strFormat(number_text, "%d", value);
            } else if (global_data == EGD_KONGIGT) {
                int current_kong = 0;
                int total_kong = 0;
                for (int j = 0; j < 5; j++) {
                    int local_kong = ReadExtraData(EGD_KONGIGT, j);
                    if (j == stat_credits_items[i].sub_data) {
                        current_kong = local_kong;
                    }
                    total_kong += local_kong;
                }
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