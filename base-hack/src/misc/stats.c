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

static unsigned char sub_counts[] = {
    EGD_LEVELIGT, 9,
    EGD_HELMHURRYIGT, 1,
    EGD_BONUSSTAT, STAT_TERMINATOR,
    EGD_KONGIGT, 5,
    EGD_FILENAME, 8,
};

int getExtraDataIndex(extra_global_data data_type, int sub_index) {
    int index = 0;
    for (int i = 0; i < (sizeof(sub_counts) >> 1); i++) {
        if (sub_counts[2 * i] < data_type) {
            index += sub_counts[(2 * i) + 1];
        }
    }
    return index + sub_index;
}

int ReadExtraData(extra_global_data data_type, int sub_index) {
    return ExtraSaveData[getExtraDataIndex(data_type, sub_index)];
}

void SaveExtraData(extra_global_data data_type, int sub_index, int value) {
    ExtraSaveData[getExtraDataIndex(data_type, sub_index)] = value;
}

void ResetExtraData(extra_global_data data_type, int sub_index) {
    ExtraSaveData[getExtraDataIndex(data_type, sub_index)] = 0;
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