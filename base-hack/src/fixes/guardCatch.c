#include "../../include/common.h"

static char warp_timer = 0;

void guardCatch(void) {
    if ((warp_timer == 0) && (TransitionSpeed == 0)) {
        warp_timer = 80;
        if (Player) {
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
            Player->control_state = 0x73;
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
            voidWarp();
        }
        warp_timer -= 1;
    }
}