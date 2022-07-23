#include "../../include/common.h"

static char warp_timer = 0;
static unsigned char bad_guard_states[] = {
    0x18, // BBlast Pad
    0x52, // Bananaport
    0x53, // Monkeyport
    0x54, // MP Bananaport
    0x67, // Instrument
};

int isBadMovementState(void) {
    if (Player) {
        int control_state = Player->control_state;
        for (int i = 0; i < sizeof(bad_guard_states); i++) {
            if (control_state == bad_guard_states[i]) {
                return 1;
            }
        }
        return 0;
    }
    return 1;
}

void guardCatch(void) {
    if (Player) {
        if ((warp_timer == 0) && (TransitionSpeed == 0) && (!isBadMovementState()) && (CutsceneActive == 0)) {
            warp_timer = 80;
            tagKong(Player->new_kong);
            Player->noclip = 1;
            if (Player->control_state != 0x7D) {
                if ((Player->grounded_bitfield & 4) == 0) {
                    if ((Player->grounded_bitfield & 2) == 0) {
                        playAnimation(Player,0x5D);
                    }
                } else {
                    playAnimation(Player,0x34);
                }
            }
            Player->control_state = 0x70;
            Player->control_state_progress = 0;
            Player->yVelocity = 0;
            Player->hSpeed = 0;
            playSong(42,0x3F800000);
        }
    }
}

void catchWarpHandle(void) {
    if (warp_timer > 0) {
        if ((warp_timer == 1) && (TransitionSpeed == 0)) {
            if ((CurrentMap == 0x11) && (Rando.fast_start_helm > 0)) {
                if (Rando.fast_start_helm == 1) {
                    initiateTransition(0x11,3);
                } else if (Rando.fast_start_helm == 2) {
                    initiateTransition(0x11,4);
                } else {
                    voidWarp();
                }
            } else {
                voidWarp();
            }
        }
        warp_timer -= 1;
    }
}