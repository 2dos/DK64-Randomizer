#include "../../include/common.h"

void qualityOfLife_shorteners(void) {
	if (Rando.quality_of_life.reduce_lag) {
        if (CurrentMap == MAP_CASTLE) {
            if (ObjectModel2Timer <= 5) {
                actorData* lzcontroller = (actorData*)findActorWithType(0xC);
                char* lzpaad = (char*)lzcontroller->paad;
                *(char*)(lzpaad) = 0;
            }
        }
	}
}

void fastWarp(void* actor, int player_index) {
    unkMultiplayerWarpFunction(actor,player_index);
    renderScreenTransition(3);
}

void fastWarp_playMusic(void* actor) {
    clearTagSlide(actor);
    playLevelMusic();
}

void fastWarpShockwaveFix(void) {
    if (!Rando.fast_warp) {
        return;
    }
    if (!Player) {
        return;
    }
    if (Player->control_state != 0x54) { // Not Multiplayer Warp
        return;
    }
    if (Player->shockwave_timer == -1) { // Not Charging Shockwave
        return;
    }
    if (Player->shockwave_timer >= 5) {
        return;
    }
    Player->shockwave_timer += 1;
    if (Player->shockwave_timer < 2) {
        Player->shockwave_timer += 1; // Prevent ever being a frame where you can shockwave
    }
}