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
    {.index = EGD_FILENAME, .count=8, .required_bits=8},
};
#define BONUS_COUNT 6

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
        int current_kong = 0;
        if (Player) {
            current_kong = Player->characterID - 2;
        }
        if (current_kong <= 4) {
            int old = ReadExtraData(EGD_KONGIGT, current_kong);
            SaveExtraData(EGD_KONGIGT, current_kong, old + current_kong_diff);
        }
        setKongIgt();
    }
}


void updateTagStat(void* data) {
    if (isGamemode(GAMEMODE_ADVENTURE, 1) && (canSaveHelmHurry())) {
        changeStat(STAT_TAGCOUNT, 1);
        updatePercentageKongStat();
        SaveToGlobal();
    }
    updateModel(data);
}


void initStatistics(void) {
    writeFunction(0x806C8ED0, &updateTagStat);
}