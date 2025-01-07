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

void adjustGunBone(playerData* player) {
    int kong = player->characterID - 2;
    if (kong < 0) {
        return;
    } else if (kong > 4) {
        return;
    }
    custom_kong_models model = Rando.kong_models[kong];
    switch (model) {
        case KONGMODEL_CRANKY:
        case KONGMODEL_KROOL_CUTSCENE:
            player->gun_bone = 5;
            break;
        case KONGMODEL_CANDY:
            player->gun_bone = 2;
            break;
        case KONGMODEL_KROOL_FIGHT:
            player->gun_bone = 6;
            break;
        case KONGMODEL_DEFAULT:
            if (kong == KONG_DIDDY) {
                if (!player->gun_bone) {
                    player->gun_bone = 1;
                } else {
                    player->gun_bone = 0;
                }
                break;
            }
        case KONGMODEL_DISCOCHUNKY:
        case KONGMODEL_KRUSHA:
        default:
            player->gun_bone = 1;
            break;
    }
}

static const unsigned char kong_vanilla_models[] = {3, 0, 5, 8, 0xB};
static const unsigned char model_swap_base_index[] = {
    0x00, // /* 0x000 */ KONGMODEL_DEFAULT,
	0x03, // /* 0x001 */ KONGMODEL_DK,
	0x00, // /* 0x002 */ KONGMODEL_DIDDY,
	0x05, // /* 0x003 */ KONGMODEL_LANKY,
	0x08, // /* 0x004 */ KONGMODEL_TINY,
	0x0B, // /* 0x005 */ KONGMODEL_CHUNKY,
	0x0D, // /* 0x006 */ KONGMODEL_DISCOCHUNKY,
	0xDA, // /* 0x007 */ KONGMODEL_KRUSHA,
	0x48, // /* 0x008 */ KONGMODEL_KROOL_FIGHT,
	0x67, // /* 0x009 */ KONGMODEL_KROOL_CUTSCENE,
	0x10, // /* 0x00A */ KONGMODEL_CRANKY,
	0x12, // /* 0x00B */ KONGMODEL_CANDY,
	0x11, // /* 0x00C */ KONGMODEL_FUNKY,
};

int getCutsceneModelTableIndex(int vanilla_index) {
    if (vanilla_index < 0x88) {
        return vanilla_index;
    }
    int slot = vanilla_index - 0xDB;
    if (slot < 0) {
        return -1;
    } else if (slot >= 8) {
        return -1;
    }
    return slot;
}

static short model_no_shift[] = {KONGMODEL_DEFAULT, KONGMODEL_KRUSHA, KONGMODEL_KROOL_CUTSCENE, KONGMODEL_KROOL_FIGHT};

void fixCutsceneModels(void) {
    for (int i = 0; i < 5; i++) {
        custom_kong_models model = Rando.kong_models[i];
        if (inShortList(model, &model_no_shift[0], sizeof(model_no_shift) >> 1)) {
            continue;
        }
        int dest_index = getCutsceneModelTableIndex(kong_vanilla_models[i]);
        int src_index = getCutsceneModelTableIndex(model_swap_base_index[model]);
        if ((dest_index == -1) || (src_index == -1)) {
            continue;
        }
        CutsceneModelJumpTable[dest_index] = CutsceneModelJumpTable[src_index];
    }
}

void adjustAnimationTables(void) {
    /**
     * @brief Adjust animation tables so that other kongs get Krusha's animations
     */
    /*
        TODO:
        Kamerson — Today at 12:13 PM
        but it still bugs me that Krusha's tag barrel non-selected anim is his losing anim and not his character select anim
    */
    for (int slot = 0; slot < 5; slot++) {
        if (isKrushaAdjacentModel(slot)) {
            if (slot == 2) {
                if (CurrentMap == MAP_KROOLLANKY) {
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
                    if (((CurrentMap == MAP_KROOLLANKY) && (slot == 2)) || ((CurrentMap == MAP_FUNGIDOGADON) && (slot == 4))) {
                        // Punch - During Lanky Phase and Dogadon 2
                        excl_extra = 1;
                    }
                } else if ((i >= 0x30) && (i <= 0x32)) {
                    excl_extra = 1;
                } else if ((i >= 0x48) && (i <= 0x4E)) {
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
                } else if ((i >= 0x3F) && (i <= 0x41) && (CurrentMap == MAP_KROOLLANKY) && (slot == 2)) {
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
    if ((MovesBase[KONG_CHUNKY].special_moves & 2) && (isKrushaAdjacentModel(KONG_CHUNKY)) && (Character == KONG_CHUNKY)) {
        permit = 1;
    } else if ((MovesBase[KONG_LANKY].special_moves & 1) && (isKrushaAdjacentModel(KONG_LANKY)) && (Character == KONG_LANKY)) {
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
    if (MovesBase[KONG_DIDDY].special_moves & 1) {
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
    // if (*model == 0xDB) {
    //     TiedCharacterSpawner->unk_46 |= 0x1000;
    //     CurrentActorPointer_0->obj_props_bitfield |= 0x1400;
    //     CurrentActorPointer_0->unk_CC = 1;
    //     unkCutsceneKongFunction_0(2, 1);
    //     clearGun(actor);
    // }
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
    if ((file == 210) && (isKrushaAdjacentModel(KONG_DIDDY))) {
        // Diddy Swim Animation
        *data = 1.0f;
    } else if ((file == 359) && (isKrushaAdjacentModel(KONG_LANKY))) {
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

typedef struct projectile_paad {
    /* 0x000 */ int init_actor_timer;
    /* 0x004 */ char unk_04[0x13-0x4];
    /* 0x013 */ unsigned char fired_bitfield;
    /* 0x014 */ float unk_14;
    /* 0x018 */ char unk_18[0x1C-0x18];
    /* 0x01C */ int unk_1C;
} projectile_paad;

typedef struct projectile_extra {
    /* 0x000 */ float initial_rotation;
    /* 0x004 */ float initial_velocity;
    /* 0x008 */ float initial_yvelocity;
    /* 0x00C */ float unkC;
    /* 0x010 */ float unk10;
    /* 0x014 */ float unk14;
} projectile_extra;

typedef struct KrushaProjectileColorStruct {
    unsigned char pellet;
    unsigned char red;
    unsigned char green;
    unsigned char blue;
} KrushaProjectileColorStruct;

static KrushaProjectileColorStruct krusha_projectile_colors[] = {
    {.pellet = 48, .red = 0xC0, .green = 0xFF, .blue = 0x00},
    {.pellet = 36, .red = 0xFF, .green = 0x40, .blue = 0x40},
    {.pellet = 42, .red = 0x18, .green = 0x18, .blue = 0xFF},
    {.pellet = 43, .red = 0x80, .green = 0x00, .blue = 0xFF},
    {.pellet = 38, .red = 0x00, .green = 0xFF, .blue = 0x00},
};

void setKrushaAmmoColor(void) {
    int currentPellet = CurrentActorPointer_0->actorType;
    for (int i = 0; i < 5; i++) {
        KrushaProjectileColorStruct *data = &krusha_projectile_colors[i];
        if ((currentPellet == data->pellet) || (i == 4)) {
            changeActorColor(data->red, data->green, data->blue, 0xFF);
            return;
        }
    }
}

void OrangeGunCode(void) {
    /**
     * @brief New code for the orange projectile fired from a gun
     */
    projectile_paad* paad = CurrentActorPointer_0->paad;
    projectile_extra* extra = (projectile_extra*)CurrentActorPointer_0->data_pointer;
    int current_actor_timer = ActorTimer;
    int sprite = 0x80720268;
    int pop_sprite_index = 39;
    int pop_sfx = 0xF6;
    float pop_scale = 2.0f;
    int is_lime = 1;
    if (CurrentActorPointer_0->actorType == 43) {
        // Is Feather actor
        if (Rando.kong_models[KONG_TINY] != KONGMODEL_KRUSHA) {
            // Is not orange
            sprite = (int)&feather_gun_sprite;
            pop_sprite_index = 5;
            pop_sfx = 0x308;
            pop_scale = 0.35f;
            is_lime = 0;
        }
    }
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->grounded &= 0xFFFE;
        CurrentActorPointer_0->rot_y_copy = (extra->initial_rotation / *(float*)(0x8075A170)) * *(float*)(0x8075A174);
        CurrentActorPointer_0->hSpeed = extra->initial_velocity;
        CurrentActorPointer_0->yVelocity = extra->initial_yvelocity;
        CurrentActorPointer_0->noclip_byte = 0x3C;
        unkProjectileCode_0(CurrentActorPointer_0, 60.0f);
        unkProjectileCode_1(CurrentActorPointer_0, 0.0f, 0.0f, 0.0f, 50.0f, -1);
        allocateBone(CurrentActorPointer_0, 0, 0, 0, -1);
        unkSpriteRenderFunc(-1);
        unkSpriteRenderFunc_1(1);
        unkSpriteRenderFunc_2(4);
        if (is_lime) {
            setKrushaAmmoColor();
        }
        displaySpriteAttachedToActor((void*)sprite, extra->unkC, CurrentActorPointer_0, 1, 2);
        paad->unk_14 = extra->unkC;
        paad->init_actor_timer = current_actor_timer;
        CurrentActorPointer_0->obj_props_bitfield |= 0x01080000;
        CurrentActorPointer_0->unk_16E = 0x3C;
        CurrentActorPointer_0->unk_16F = 0x3C;
        int val = extra->unk10;
        if (val < 0) {
            val = 0xFF;
        }
        paad->fired_bitfield = val;
        paad->unk_1C = 0;
    }
    int orange_life = 0x32; // No Sniper
    if (paad->fired_bitfield & 2) { // Homing
        int homing_bitfield = 2;
        if (Rando.quality_of_life.homing_balloons) {
            homing_bitfield = 10;
        }
        if (player_count > 1) {
            homing_bitfield = 3;
        }
        // homing_code(homing_bitfield, CurrentActorPointer_0, 0x80720268, 0); // Produces some weird artifacts with limes
        homing_code(homing_bitfield, CurrentActorPointer_0, 0, 0);
    }
    if (paad->fired_bitfield & 4) { // Sniper
        orange_life = 0x64;
    }
    float life = orange_life;
    unkBonusFunction(CurrentActorPointer_0);
    unkProjectileCode_2(CurrentActorPointer_0);
    unkProjectileCode_3(CurrentActorPointer_0, 0);
    int making_contact = madeContact();
    if (
        (making_contact) ||
        (CurrentActorPointer_0->unk_FD) ||
        ((CurrentActorPointer_0->grounded & 1) && (madeGroundContact() == 1)) ||
        (collisionActive) ||
        ((extra->unk14 != 0.0f) && ((paad->init_actor_timer + 1) < current_actor_timer))
    ) {
        unkSpriteRenderFunc_1(1);
        unkSpriteRenderFunc_3(0x1006E);
        loadSpriteFunction(0x8071A8B0); // TODO(theballaam96): Remove light rendering, saves 4fps
        float x = CurrentActorPointer_0->xPos;
        float y = CurrentActorPointer_0->yPos;
        float z = CurrentActorPointer_0->zPos;
        displaySpriteAtXYZ(sprite_table[pop_sprite_index], pop_scale, x, y, z);
        playSFXFromActor(CurrentActorPointer_0, pop_sfx, 0xFF, 0x7F, 0x1E);
        deleteActorContainer(CurrentActorPointer_0);
        if (*(char*)(0x80750AD0) == 0) {
            for (int i = 0; i < 6; i++) {
                unkSpriteRenderFunc_1(1);
                unkSpriteRenderFunc_3(0xB000000 + (i << 1));
                loadSpriteFunction(0x8071ABDC);
                displaySpriteAtXYZ(sprite_table[38], 0.35f, x, y, z);
            }
        }
    }
    if (player_count > 1) {
        life *= 1.4f;
    }
    if ((paad->init_actor_timer + life) < current_actor_timer) {
        deleteActorContainer(CurrentActorPointer_0);
    }
}