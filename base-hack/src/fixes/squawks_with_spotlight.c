#include "../../include/common.h"

void squawks_with_spotlight_actor_code() {
    //float local4; //sw ra, local4(sp)

    shine_light_at_kong(10, 0x14, 0x240);

}

void shine_light_at_kong(unsigned short height_variance, short min_follow_distance, unsigned short param_3) {
    spotlight_hold_paad* pointerLightBrightness = 0;
    unsigned int half_speed = 0;
    int param_2_variable = 0;
    float distance_x = 0;
    float distance_z = 0;
    int distance = 0;
    float actor_height_variance = 0;
    float height_variance_multiplier = 0.03;
    
    initCharSpawnerActor();
    distance_x = (CurrentActorPointer_0->xPos) - (PlayerPointer_0->xPos);
    distance_z = (CurrentActorPointer_0->zPos) - (PlayerPointer_0->zPos);
    distance_x = dk_sqrt(distance_x * distance_x + distance_z * distance_z);
    distance = distance_x;
    
    //TODO: remove this line

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
        TiedCharacterSpawner->unk_3C = 1.0f;
                        /* if actor_type == 0xf0 (240) means if actor_type == spotlight fish */
        if (CurrentActorPointer_0->actorType == 0xf0) {
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
    setActorSpeed(CurrentActorPointer_0,(half_speed + half_speed));
                        /* 0 if spotlight fish, height_variance = 10 if squawks */
    actor_height_variance = height_variance * height_variance_multiplier;
    unkLightFunc_1(0x23, height_variance, (PlayerPointer_0->xPos), (PlayerPointer_0->yPos + actor_height_variance), (PlayerPointer_0->zPos), 0x1e, *(float*)(0x8075c398), param_3 | 0x2000); //8072a920
    float movement_cycle_height = determineXRatioMovement((ObjectModel2Timer * 0x280000) >> 0x10);
    CurrentActorPointer_0->yPos = CurrentActorPointer_0->yPos + (actor_height_variance * movement_cycle_height);
    unkLightFunc_2(); //806c6530
    renderActor(CurrentActorPointer_0, 0);

    //TODO: remove this line
    *(float*)(0x807FF700) = CurrentActorPointer_0->xPos;
    *(float*)(0x807FF704) = CurrentActorPointer_0->yPos;
    *(float*)(0x807FF708) = CurrentActorPointer_0->zPos;
    return;
}