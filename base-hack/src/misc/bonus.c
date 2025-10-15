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
    return paad->internal_score <= 0;
}

static short barrel_types[3] = {0x1C, 0x86, 0x6B};

void resolveBonusContainer(void) {
    int b = 0;
    int index = getSpawnerIndexOfResolvedBonus(&barrel_types, 3, &b);
    resolveBonus(b, index, 7, 2.0f);
}

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
        resolveBonusContainer();
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

/*
    Alt Minecart Mayhem:
    - Spawn Timer: Minecart::80025340
    - Win condition check: getItemCount(0xB, 0) >= req
    - bonus::80024000 shows the get counter?
*/

int getMinecartMayhemCoinReq(void) {
    if (CurrentMap == MAP_MMAYHEM_EASY) {
        return 10;
    } else if (CurrentMap == MAP_MMAYHEM_NORMAL) {
        return 12;
    } else if (CurrentMap == MAP_MMAYHEM_HARD) {
        return 15;
    }
    return 0;
}

typedef struct MinecartMinigame {
    /* 0x000 */ char pad0[2];
    /* 0x002 */ short hit_req;
    /* 0x004 */ short hit_req_hud;
    /* 0x006 */ char pad6[2];
    /* 0x008 */ unsigned char text;
    /* 0x009 */ unsigned char unk9;
} MinecartMinigame;

Gfx *renderGet(Gfx *dl, actorData *actor) {
    MinecartMinigame *data = actor->paad2;
    if (isCutsceneBarsPresent()) {
        gSPDisplayList(dl++, 0x01000118);
        dl = unkDLFunction(dl);
        gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
        gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
        gSPMatrix(dl++, 0x02000180, G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
        dl = getDLFunction0(dl, data->unk9, 8, 30.0f, 36.0f, 0.0f, 1.5f);
        dl = getDLFunction1(dl, 0x26, 0x32, &data->hit_req, data->hit_req_hud, &data->text);
    }
    return dl;
}

int renderGetWrapper(void) {
    MinecartMinigame *data = CurrentActorPointer_0->paad2;
    data->hit_req_hud = getMinecartMayhemCoinReq() - getItemCount(ITEMID_RACECOIN, 0);
    addDLToOverlay(&renderGet, CurrentActorPointer_0, 3);
    return isCutsceneActive();
}

int wonMinecartMayhem(void) {
    if (getItemCount(ITEMID_RACECOIN, 0) >= getMinecartMayhemCoinReq()) {
        return 1;
    }
    return 0;
}

short mayhem_minecart_size[3] = {0x2E, 10, 0};

void initMMayhem(actorData *actor, int cutscene, int type) {
    MinecartMinigame *data = CurrentActorPointer_0->paad2;
    data->hit_req = getMinecartMayhemCoinReq();
    data->hit_req_hud = data->hit_req;
    void *text = getTextPointer(0x1A, 3, 1);
    data->text = unkTextFunction1(1, text, 8, 0.0f, 0.0f, 0.0f);
    playCutscene(actor, cutscene, type);
}

