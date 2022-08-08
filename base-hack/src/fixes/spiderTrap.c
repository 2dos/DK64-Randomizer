#include "../../include/common.h"

static const unsigned char bad_movement_states[] = {
	//0x02, // First Person Camera
	//0x03, // First Person Camera (Water)
	0x04, // Fairy Camera
	0x05, // Fairy Camera (Water)
	0x06, // Locked (Bonus Barrel)
	0x15, // Slipping
	0x16, // Slipping
	0x18, // Baboon Blast Pad
	//0x1C, // Simian Slam // Note: As far as I know this doesn't break anything, so we'll save the CPU cycles
	0x20, // Falling/Splat, // Note: Prevents quick recovery from fall damage, and I guess maybe switching to avoid fall damage?
	0x31, // Damaged
	0x32, // Stunlocked
	0x33, // Damaged
	0x35, // Damaged
	0x36, // Death
	0x37, // Damaged (Underwater)
	0x38, // Damaged
	0x39, // Shrinking
	0x42, // Barrel
	0x43, // Barrel (Underwater)
	0x44, // Baboon Blast Shot
	0x45, // Cannon Shot
	0x52, // Bananaporter
	0x53, // Monkeyport
	0x54, // Bananaporter (Multiplayer)
	0x56, // Locked
	0x57, // Swinging on Vine
	0x58, // Leaving Vine
	0x59, // Climbing Tree
	0x5A, // Leaving Tree
	0x5B, // Grabbed Ledge
	0x5C, // Pulling up on Ledge
	0x63, // Rocketbarrel // Note: Covered by crystal HUD check except for Helm & K. Rool
	0x64, // Taking Photo
	0x65, // Taking Photo
	0x67, // Instrument
	0x69, // Car
	0x6A, // Learning Gun // Note: Handled by map check
	0x6B, // Locked
	0x6C, // Feeding T&S // Note: Handled by map check
	0x6D, // Boat
	0x6E, // Baboon Balloon
	0x6F, // Updraft
	0x70, // GB Dance
	0x71, // Key Dance
	0x72, // Crown Dance
	0x73, // Loss Dance
	0x74, // Victory Dance
	0x78, // Gorilla Grab
	0x79, // Learning Move // Note: Handled by map check
	0x7A, // Locked
	0x7B, // Locked
	0x7C, // Trapped (spider miniBoss)
	0x7D, // Klaptrap Kong (beaver bother) // Note: Handled by map check
	0x83, // Fairy Refill
	0x87, // Entering Portal
	0x88, // Exiting Portal
};

void handleSpiderTrapCode(void) {
    if (CurrentMap != 0x3C) { // Only have custom behaviour outside of Spider fight
        int rng = 0;
        if (CurrentActorPointer_0->control_state == 0x23) {
            rng = getRNGLower31();
            if (979 < ((rng >> 0xF) % 1000)) { // Chance they are gonna goop you (1%)
                if (CurrentActorPointer_0->grounded & 1) {
                    CurrentActorPointer_0->control_state = 0x28;
                    CurrentActorPointer_0->control_state_progress = 0;
                }
            }
        }
        if (CurrentActorPointer_0->control_state == 0x28) {
            if (CurrentActorPointer_0->control_state_progress == 0) {
                int in_bad_state = 0;
                for (int i = 0; i < sizeof(bad_movement_states); i++) {
                    if (bad_movement_states[i] == Player->control_state) {
                        in_bad_state = 1;
                    }
                }
                if (in_bad_state == 0) {
                    updateActorProjectileInfo(CurrentActorPointer_0,1);
                    rng = getRNGLower31();
					int rng_target_diff = ((getRNGLower31() >> 0xF) % 2000);
					float target_diff = (rng_target_diff / 1000) + 10.0f;
					float diff_x = getXRatioMovement(PlayerPointer_0->rot_y) * target_diff;
					float diff_z = getZRatioMovement(PlayerPointer_0->rot_y) * target_diff;
					float target_x = PlayerPointer_0->xPos + diff_x;
					float target_y = PlayerPointer_0->yPos + PlayerPointer_0->height_offset;
					float target_z = PlayerPointer_0->zPos + diff_z;
                    spawnProjectile(0x116, ((rng >> 0xF) % 3) + 1, 0x3F800000, target_x, target_y, target_z, 300.0f, CurrentActorPointer_0);
                }
            }
        }
    }
    renderActor(CurrentActorPointer_0,0);
}