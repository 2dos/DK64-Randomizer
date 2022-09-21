#include "../../include/common.h"

void beatGame(void) {
    setPermFlag(FLAG_GAME_BEATEN);
    save();
    loadEndSeq(0);
}

void checkSeedVictory(void) {
    if (!checkFlag(FLAG_GAME_BEATEN,0)) {
        switch(Rando.win_condition) {
            case GOAL_KEY8:
                if (checkFlag(FLAG_KEYHAVE_KEY8,0)) {
                    beatGame();
                }
                break;
            case GOAL_ALLFAIRIES:
                for (int i = 0; i < 20; i++) {
                    if (!checkFlag(FLAG_FAIRY_1 + i,0)) {
                        return;
                    }
                }
                beatGame();
                break;
            case GOAL_ALLBLUEPRINTS:
                for (int i = 0; i < 40; i++) {
                    if (!checkFlag(FLAG_BP_JAPES_DK_HAS + i,0)) {
                        return;
                    }
                }
                beatGame();
                break;
            case GOAL_ALLMEDALS:
                for (int i = 0; i < 40; i++) {
                    if (!checkFlag(FLAG_MEDAL_JAPES_DK + i,0)) {
                        return;
                    }
                }
                beatGame();
                break;
            case GOAL_POKESNAP:
            break;
        }
    }
}

void checkVictory_flaghook(int flag) {
    checkGlobalProgress(flag);
    checkSeedVictory();
}