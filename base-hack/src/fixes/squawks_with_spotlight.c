/**
 * @file squawks_with_spotlight.c
 * @author AlmostSeagull
 * @brief Make Squawks-with-spotlight follow the Kong more closely in Fungi Forest's dark attic (rewrite of vanilla functions)
 * @version 1.0
 * @date 2023-01-24
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

void shine_light_at_kong(unsigned short height_variance, unsigned short min_follow_distance, unsigned short param_3, int is_char_spawner) {
    /**
     * @brief Rewrite of Squawk's vanilla function 
     * Makes Squawks follow the Kong around with a spotlight to light the way. 
     * @param height_variance: variation in height between his highest and lowest points at a given point
     * @param min_follow_distance: how close to its target Squawks will go. If closer than this distance, Squawks will not move (on the x-z plane)
     * @param param_3: unknown, as of yet
     * 
     */
    spotlight_hold_paad* pointerLightBrightness = 0;
    short half_speed = 0;
    int param_2_variable = 0;
    float distance_x = 0;
    float distance_z = 0;
    int distance = 0;
    float actor_height_variance = 0;
    float height_variance_multiplier = 0.06; //TODO(AlmostSeagull): figure out good value, closer to 0.06 than 0.03
    
    if (is_char_spawner) {
        initCharSpawnerActor();
    }
    distance_x = (CurrentActorPointer_0->xPos) - (PlayerPointer_0->xPos);
    distance_z = (CurrentActorPointer_0->zPos) - (PlayerPointer_0->zPos);
    distance_x = dk_sqrt(distance_x * distance_x + distance_z * distance_z);
    distance = distance_x;

    if (distance < 0) {
        distance = -1;
    }
                        /* if thing % 16 == 0 */
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        pointerLightBrightness = (spotlight_hold_paad*) CurrentActorPointer_0->paad2;
        CurrentActorPointer_0->unk_64 = CurrentActorPointer_0->unk_64 | 4;
        CurrentActorPointer_0->obj_props_bitfield = CurrentActorPointer_0->obj_props_bitfield | 0x800000;
        CurrentActorPointer_0->rgb_mask[0] = 0xff;
        CurrentActorPointer_0->rgb_mask[1] = 0xff;
        CurrentActorPointer_0->rgb_mask[2] = 0xff;
        pointerLightBrightness->unk2 = 0;
        pointerLightBrightness->unk0 = 0xff;
        if (is_char_spawner) {
            TiedCharacterSpawner->unk_3C = 1.0f;
        }
                        /* if actor_type == 0xf0 (240) means if actor_type == spotlight fish */
        if ((CurrentActorPointer_0->actorType == 0xf0) || (CurrentActorPointer_0->actorType == 151)) {
            unkLightFunc_0(CurrentActorPointer_0, 0x132, 0, 0, 0); //80604cbc
            param_2_variable = (int)min_follow_distance;
        } else {
            param_2_variable = (int)min_follow_distance;
        }
    } else {
        param_2_variable = (int)min_follow_distance;
    }
    distance = (distance & 0xffff) - param_2_variable;
    half_speed = distance & 0xffff;
    if (distance < 0) {
        half_speed = 0;
    }
    if (is_char_spawner) {
        setActorSpeed(CurrentActorPointer_0,(half_speed + half_speed));
    }
                        /* 0 if spotlight fish, height_variance = 10 if squawks */
    actor_height_variance = height_variance;
    actor_height_variance *= height_variance_multiplier;
    kongFollowingLightFunc(0x23, height_variance, (PlayerPointer_0->xPos), (PlayerPointer_0->yPos + actor_height_variance + 29.4), (PlayerPointer_0->zPos), 0x1e, *(float*)(0x8075c398), 100.0f, param_3 | 0x2000); //8072a920
    float movement_cycle_height = determineXRatioMovement((ObjectModel2Timer * 0x280000) >> 0x10);
    CurrentActorPointer_0->yPos = CurrentActorPointer_0->yPos + (actor_height_variance * movement_cycle_height);  // goal is ~38 to 49 to be the squawk's Y levels
    lightShiningLightFunc(); //806c6530
    renderActor(CurrentActorPointer_0, 0);
    return;
}

void squawks_with_spotlight_actor_code() {
    /**
     * @brief Initializes a rewritten version of Squawk's main function
     * 
     */
    //float local4; //sw ra, local4(sp)

    shine_light_at_kong(10, 0x0, 0x240, 1);
    return;
}