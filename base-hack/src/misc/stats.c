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
    SaveToFile(DATA_BONUSSTAT, 0, statistic, 0, old + delta);
    return old + delta;
}

void setStat(bonus_stat statistic, int amount) {
    SaveToFile(DATA_BONUSSTAT, 0, statistic, 0, amount);
}

int getStat(bonus_stat statistic) {
    return ReadFile(DATA_BONUSSTAT, 0, statistic, 0);
}

#define FILE_COUNT 1
void GrabParameters_Global(int index, int level, short* file_base, char* bit_size) {
    *file_base = (((((((*(short*)(0x807ECEA0) + getNewFileSize()) & 0xFFC0) + 0x27) & 0xFFF8) * FILE_COUNT) + 0x3F) & 0xFFC0) + 0x40;
    *bit_size = 0;
    switch (index) {
        case DATA_FILENAME:
            if (*bit_size == 0) {
                *bit_size = LETTER_BITS;
                *file_base = *file_base + (level * LETTER_BITS);
            }
            *file_base = *file_base + (IGT_BITS * 5);
        case DATA_KONGIGT:
            if (*bit_size == 0) {
                *bit_size = IGT_BITS;
                *file_base = *file_base + (level * IGT_BITS);
            }
            *file_base = *file_base + (STAT_BITS * STAT_TERMINATOR);
        case DATA_BONUSSTAT:
            if (*bit_size == 0) {
                *bit_size = STAT_BITS;
                *file_base = *file_base + (level * STAT_BITS);
            }
            *file_base = *file_base + HELM_HURRY_BITS;
        case DATA_HELMHURRYIGT:
            if (*bit_size == 0) {
                *bit_size = HELM_HURRY_BITS;
            }
            *file_base = *file_base + 1;
        case DATA_HELMHURRYOFF:
            if (*bit_size == 0) {
                *bit_size = 1;
            }
            *file_base = *file_base + (IGT_BITS * 9);
        case DATA_LEVELIGT:
            if (*bit_size == 0) {
                *bit_size = IGT_BITS;
                *file_base = *file_base + (level * IGT_BITS);
            }
            *file_base = *file_base + 1;
        case DATA_CAMERATYPE:
            if (*bit_size == 0) {
                *bit_size = 1;
            }
            *file_base = *file_base + 3;
        case DATA_LANGUAGE:
            if (*bit_size == 0) {
                *bit_size = 3;
            }
            *file_base = *file_base + 2;
        case DATA_SOUNDTYPE:
            if (*bit_size == 0) {
                *bit_size = 2;
            }
            *file_base = *file_base + 0x2D;
        case DATA_ENGUARDEHISCORE_NUM:
            if (*bit_size == 0) {
                *bit_size = 9;
                *file_base = *file_base + (level * 9);
            }
            *file_base = *file_base + 0x19;
        case DATA_ENGUARDEHISCORE_CHAR2:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_ENGUARDEHISCORE_CHAR1:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_ENGUARDEHISCORE_CHAR0:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x2D;
        case DATA_RAMBIHISCORE_NUM:
            if (*bit_size == 0) {
                *bit_size = 9;
                *file_base = *file_base + (level * 9);
            }
            *file_base = *file_base + 0x19;
        case DATA_RAMBIHISCORE_CHAR2:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_RAMBIHISCORE_CHAR1:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_RAMBIHISCORE_CHAR0:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x4B;
        case DATA_ARCADEHISCORE_NUM:
            if (*bit_size == 0) {
                *bit_size = 15;
                *file_base = *file_base + (level * 15);
            }
            *file_base = *file_base + 0x19;
        case DATA_ARCADEHISCORE_CHAR2:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_ARCADEHISCORE_CHAR1:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x19;
        case DATA_ARCADEHISCORE_CHAR0:
            if (*bit_size == 0) {
                *bit_size = 5;
                *file_base = *file_base + (level * 5);
            }
            *file_base = *file_base + 0x12;
        case DATA_JETPACHISCORE:
            if (*bit_size) {
                return;
            }
            *bit_size = 0x12;
        default:
            break;
    }   
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
            int old = ReadFile(DATA_KONGIGT, 0, current_kong, 0);
            SaveToFile(DATA_KONGIGT, 0, current_kong, 0, old + current_kong_diff);
        }
        for (int i = 0; i < 5; i++) {
            *(int*)(0x807FF700 + (i << 2)) = ReadFile(DATA_KONGIGT, 0, i, 0);
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