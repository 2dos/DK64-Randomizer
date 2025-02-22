/**
 * @file bonus.c
 * @author Ballaam
 * @brief Bonus Barrel Changes
 * @version 0.1
 * @date 2023-08-27
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

typedef struct arena_controller_paad {
    /* 0x000 */ short cooldown_timer;
    /* 0x002 */ char unk2;
    /* 0x003 */ char unk3;
    /* 0x004 */ short time_limit;
    /* 0x006 */ char unk6;
    /* 0x007 */ char unk7;
    /* 0x008 */ short displayed_score;
    /* 0x00A */ short internal_score;
    /* 0x00C */ short unkC;
} arena_controller_paad;

int wonArena(void) {
    arena_controller_paad* paad = CurrentActorPointer_0->paad;
    int score = paad->internal_score;
    if (CurrentMap == MAP_RAMBIARENA) {
        int mult = RambiArenaComboSize > 1 ? 2 : 1;
        for (int i = 0; i < RambiArenaComboSize; i++) {
            score -= (RambiArenaComboChain[i] * mult);
        }
    }
    return score <= 0;
}

static short barrel_types[3] = {0x1C, 0x86, 0x6B};

void warpOutOfArenas(void) {
    if (isGamemode(GAMEMODE_DKBONUS, 0)) {
        initiateTransition(MAP_MAINMENU, 0); // Warp back to main menu
        return;
    }
    if (!wonArena()) {
        failBonus(1, 1);
        return;
    }
    if (!isGamemode(GAMEMODE_SNIDEGAMES, 0)) {
        int b = 0;
        int index = getSpawnerIndexOfResolvedBonus(&barrel_types, 3, &b);
        resolveBonus(b, index, 7, 2.0f);
    }
    ExitFromBonus();
}

void failTraining(int play_cutscene, int text_index) {
    // actorData* parent = CurrentActorPointer_0->parent;
    // parent->control_state = 0;
    // char* str = getTextPointer(0x1A, text_index, 1);
    // spawnOver
    playSong(SONG_FAILURERACES, 1.0f);
    setAction(0x43, (void*)0, 0);
    // CurrentActorPointer_0->control_state += 1;
    if (play_cutscene) {
        playBonusCutsceneWrapper(Player, 5, 0x21, 5);
    }
}

void warpOutOfTraining(void) {
    if (isGamemode(GAMEMODE_DKBONUS, 0)) {
        initiateTransition(MAP_MAINMENU, 0); // Warp back to main menu
        return;
    }
    int beaten_training = *(unsigned char*)(0x80029FA8);
    if (!beaten_training) {
        failTraining(1, 1);
        return;
    }
    if (!isGamemode(GAMEMODE_SNIDEGAMES, 0)) {
        int b = 0;
        int index = getSpawnerIndexOfResolvedBonus(&barrel_types, 3, &b);
        resolveBonus(b, index, 7, 2.0f);
    }
    ExitFromBonus();
}

void ArenaTagKongCode(void) {
    playCutscene(0, 0, 1);
    arena_controller_paad* paad = CurrentActorPointer_0->paad;
    int initial_score = 0;
    if (CurrentMap == MAP_RAMBIARENA) {
        tagKong(8);
        Player->control_state = 0xC;
        Player->control_state_progress = 0;
        playAnimation(Player, 9);
        Player->hSpeed = 0.0f;
        Player->yPos = Player->floor + 50.0f;
        if (!isGamemode(GAMEMODE_DKBONUS, 0)) {
            initial_score = 100;
        }
    } else if (CurrentMap == MAP_ENGUARDEARENA) {
        tagKong(9);
        int new_control_state = 0x7F;
        if (Player->water_floor < Player->yPos) {
            new_control_state = 0x82;
        }
        Player->control_state = new_control_state;
        Player->control_state_progress = 0;
        playActorAnimation(Player, 0x317);
        Player->hSpeed = 100.0f;
        if (!isGamemode(GAMEMODE_DKBONUS, 0)) {
            initial_score = 100;
        }
    }
    if (initial_score > 0) {
        paad->internal_score = initial_score;
        paad->displayed_score = initial_score;
    }
}

void ArenaEarlyCompletionCheck(void) {
    if (CurrentActorPointer_0->control_state == 2) {
        if (!isGamemode(GAMEMODE_DKBONUS, 0)) {
            if (wonArena()) {
                winBonus(1, 0);
            }
        }
    }
    addDLToOverlay((void*)0x8002D010, CurrentActorPointer_0, 3);
}