/**
 * @file krusha.c
 * @author Ballaam
 * @brief Live adjustments for implementing Krusha in-game
 * @version 0.1
 * @date 2022-09-25
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

void adjustAnimationTables(void) {
    /**
     * @brief Adjust animation tables so that other kongs get Krusha's animations
     */
    int slot = Rando.krusha_slot;
    if ((slot >= 0) && (slot <= 4)) {
        if (slot == 2) {
            if (CurrentMap == 0xCD) {
                *(short*)(0x8075D7CE) = 0x3320; // Allow arm stretching
            } else {
                *(short*)(0x8075D7CE) = 0x36B4; // Prevent arm stretching (DK64 is a giant meme)
            }
        }
        for (int i = 0; i < 0x8D; i++) {
            if (i < 0x31) {
                AnimationTable3[(7 * i) + slot] = AnimationTable3[(7 * i) + 5];
            }
            int excl_extra = 0;
            if ((i >= 0x63) && (i <= 0x65)) {
                // Instrument
                excl_extra = 1;
            } else if ((i >= 0x50) && (i <= 0x52)) {
                if (((CurrentMap == 0xCD) && (slot == 2)) || ((CurrentMap == 0x53) && (slot == 4))) {
                    // Punch - During Lanky Phase and Dogadon 2
                    excl_extra = 1;
                }
            } else if ((i >= 0x30) && (i <= 0x32)) {
                excl_extra = 1;
            } else if ((i >= 0x48) && (i <= 0x4E)) {
                // excl_extra = 1;
            } else if ((i == 0x26) && (slot == 0) && (CurrentMap == 0xBC)) {
                // BBlast
                // excl_extra = 1;
            }
            if (i < 0x6E) {
                if (!excl_extra) {
                    AnimationTable2[(7 * i) + slot] = AnimationTable2[(7 * i) + 5];
                }
            }
            /*
                Fixes a collision glitch with actors underwater if set to 2.
                However, this causes the animation to be pretty bugged out.
                if (slot == 2) {
                    for (int i = 0; i < 3; i++) {
                        int anim_targ = 0x30 + i;
                        AnimationTable2[(7 * anim_targ) + slot] = AnimationTable2[(7 * *(int*)(0x807FF700)) + 5];
                    }
                }
            */
            int excl_base = 0;
            int dances[] = {0x43A, 0x434};
            if (i == 0x5A) {
                // Instrument
                excl_base = 1;
            } else if ((i >= 0x3F) && (i <= 0x41) && (CurrentMap == 0xCD) && (slot == 2)) {
                // Punch - During Lanky Phase
                excl_base = 1;
            } else if ((i >= 0x5C) && (i <= 0x5D)) {
                // Dances
                /*
                    Animation 0x5B is also a good dance (Animation 0x43A), but replacing it will mean that you aren't transitioned out in crowns
                */
                AnimationTable1[(7 * i) + slot] = dances[i - 0x5C];
                excl_base = 1;
            } else if ((i >= 0x8A) && (i <= 0x8C)) {
                // Tag Animation
                int dance = dances[1];
                if (i == 0x8B) {
                    dance = dances[0];
                }
                AnimationTable1[(7 * i) + slot] = dance;
                excl_base = 1;
            }
            if (!excl_base) {
                AnimationTable1[(7 * i) + slot] = AnimationTable1[(7 * i) + 5];
            }
        }
    }
    clearActorList();
}

void KrushaSlide(void) {
    /**
     * @brief Code to play Krusha's skating animation
     */
    Player->yAccel = -20.0f;
    CurrentActorPointer_0->control_state = 0x2B;
    CurrentActorPointer_0->control_state_progress = 0;
    playAnimation(CurrentActorPointer_0, 0x45);
    Player->shockwave_timer = 50;
}

void adaptKrushaZBAnimation_PunchOStand(int action, void* player, int player_index) {
    /**
     * @brief Handle the Z+B process for Krusha on Lanky/Chunky
     * 
     * @param action Action being forced on the player
     * @param player Player actor
     * @param player_index Player Index
     */
    int permit = 0;
    if ((MovesBase[4].special_moves & 2) && (Rando.krusha_slot == 4)) {
        permit = 1;
    } else if ((MovesBase[2].special_moves & 1) && (Rando.krusha_slot == 2)) {
        permit = 1;
    }
    if (permit) {
        if (Player) {
            if (Player->hSpeed < 70) {
                // Primate Punch
                setAction(action, player, player_index);
            } else {
                // Slide
                KrushaSlide();
            }
        }
    } else {
        // Slide
        KrushaSlide();
    }
}

void adaptKrushaZBAnimation_Charge(actorData* actor, int anim) {
    /**
     * @brief Handle the Z+B process for Krusha on Diddy
     * 
     * @param actor Player
     * @param anim Charge Animation
     */
    if (MovesBase[1].special_moves & 1) {
        if (Player->hSpeed < 70) {
            Player->turn_speed = 100;
            actor->control_state = 0x2E;
            actor->control_state_progress = 0;
            playAnimation(actor, anim);
            Player->unk_1E8 = ChargeVelocities_0[(int)Character] << 2;
            Player->velocity_cap = ChargeVelocities_1[(int)Character] << 1;
            Player->unk_1B0 = ChargeDeceleration[(int)Character];
        } else {
            KrushaSlide();
        }
    } else {
        KrushaSlide();
    }
}

void updateCutsceneModels(actorData* actor, int size) {
    /**
     * @brief Change cutscene models to account for Krusha
     * 
     * @param actor Player actor
     * @param size Player scale
     */
    short* model = actor->paad3;
    if (*model == 0xDB) {
        TiedCharacterSpawner->unk_46 |= 0x1000;
        CurrentActorPointer_0->obj_props_bitfield |= 0x1400;
        CurrentActorPointer_0->unk_CC = 1;
        unkCutsceneKongFunction_0(2, 1);
        clearGun(actor);
    }
    updateModelScales(actor, size);
}

void* DiddySwimFix(int ptr, int file, int c0, int c1) {
    /**
     * @brief Fix Diddy & Lanky's swimming animations
     * 
     * @param ptr Pointer table index
     * @param file File Index
     * @param c0 Unk Compression Var
     * @param c1 Unk Compression Var
     */
    float* data = (float*)getMapData(ptr, file, c0, c1);
    if ((file == 210) && (KrushaSlot == 1)) {
        // Diddy Swim Animation
        *data = 1.0f;
    } else if ((file == 359) && (KrushaSlot == 2)) {
        *data = 1.0f;
    }
    return (void*)data;
}

void MinecartJumpFix(void* player, int anim) {
    /**
     * @brief Fix Minecart jumping being broken as Krusha
     */
    CurrentActorPointer_0->control_state_progress = 1;
    playAnimation(player, anim);
}

void MinecartJumpFix_0(void) {
    /**
     * @brief Fix Minecart jumping being broken as Krusha
     * 
     */
    if (CurrentActorPointer_0->yVelocity < 0) {
        CurrentActorPointer_0->yAccel = -20.f;
    }
    if (CurrentActorPointer_0->grounded & 1) {
        CurrentActorPointer_0->control_state = 7;
        CurrentActorPointer_0->control_state_progress = 0;
    }
}