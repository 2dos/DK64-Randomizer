/**
 * @file cosmetic.c
 * @author Ballaam
 * @brief Initialization of Cosmetic Changes
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

static short pellets[] = {48, 36, 42, 43, 38};

#define ORANGE_GUN_SFX 400
#define ORANGE_GUN_VARIANCE 5
#define ENABLE_ORANGE_GUN 1

static const char* krool_name = "K. ROOL";
static const char* cranky_name = "CRANKY";
static const char* candy_name = "CANDY";
static const char* funky_name = "FUNKY";

void initKrusha(int slot) {
    /**
     * @brief Initialize the Krusha Cosmetic/Gameplay feature
     * 
     */
    writeFunction(0x80677E94, &adjustAnimationTables); // Give Krusha animations to slot
    writeFunction(0x806C32B8, &updateCutsceneModels); // Fix cutscene models
    RollingSpeeds[slot] = 175; // Increase Krusha slide speed to 175
    if (Rando.kong_models[slot] == KONGMODEL_KRUSHA) {
        KongTextNames[slot] = KongTextNames[5];
        KongTagNames[slot] = 6; // Change kong name in Tag Barrel
    } else {
        KongTextNames[slot] = krool_name;
        KongTagNames[slot] = 7; // Change kong name in Tag Barrel
    }
    LedgeHangY[slot] = LedgeHangY[5];
    LedgeHangY_0[slot] = LedgeHangY_0[5];
    *(short*)(0x8074AB5A) = 0x0040; // Enables Krusha's spin attack to knock kasplats down
    PotionAnimations[slot] = PotionAnimations[4];
    actor_functions[2 + slot] = (void*)0x806C9F44; // Replace Kong Code w/ Krusha Code
    if (ENABLE_ORANGE_GUN) {
        // Gun Stuff
        int focused_pellet = pellets[slot];
        actor_functions[focused_pellet] = &OrangeGunCode;
        setActorDamage(focused_pellet, 3);
        *(int*)(0x8071AAC4) = 0;
        *(int*)(0x8075DBB4 + (slot << 2)) = 0x806FAE0C;
        *(short*)(0x806E240A) = 0x3E80;
    }
    switch (slot) {
        case 0:
            // DK
            *(short*)(0x806F0AFE) = 0; // Remove gun from hands in Tag Barrel
            *(int*)(0x806F0AF0) = 0x24050001; // Fix Hand State
            *(int*)(0x806D5EC4) = 0; // Prevent Moving Ground Attack pop up
            *(short*)(0x8064AF5E) = 5; // Reduce slam range for DK Dungeon GB Slam
            if (ENABLE_ORANGE_GUN) {
                *(short*)(0x806E2AA2) = ORANGE_GUN_SFX; // SFX
                *(short*)(0x806E2AA6) = ORANGE_GUN_VARIANCE; // Variance
            }
            break;
        case 1:
            // Diddy
            *(int*)(0x806F0A6C) = 0x0C1A29D9; // Replace hand state call
            *(int*)(0x806F0A78) = 0; // Replace hand state call
            *(int*)(0x806E4938) = 0; // Always run adapt code
            *(int*)(0x806E4940) = 0; // NOP Animation calls
            *(int*)(0x806E4950) = 0; // NOP Animation calls
            *(int*)(0x806E4958) = 0; // NOP Animation calls
            writeFunction(0x806E495C, &adaptKrushaZBAnimation_Charge); // Allow Krusha to use slide move if fast enough (Charge)
            *(int*)(0x806E499C) = 0; // NOP Animation calls
            *(int*)(0x806E49C8) = 0; // NOP Animation calls
            *(int*)(0x806E49F0) = 0; // NOP Animation calls
            *(short*)(0x806CF5F0) = 0x5000; // Prevent blink special cases
            *(int*)(0x806CF76C) = 0; // Prevent blink special cases
            *(int*)(0x806832B8) = 0; // Prevent tag blinking
            *(int*)(0x806C1050) = 0; // Prevent Cutscene Kong blinking
            *(unsigned char*)(0x8075D19F) = 0xA0; // Fix Gun Firing
            writeFunction(0x806141B4, &DiddySwimFix); // Fix Diddy's Swim Animation
            *(short*)(0x80749764) = 10; // Fix Diddy Swimming (A)
            *(short*)(0x80749758) = 10; // Fix Diddy Swimming (B)
            *(short*)(0x8074974C) = 10; // Fix Diddy Swimming (Z/First Person)
            writeFunction(0x806E903C, &MinecartJumpFix); // Fix Diddy Minecart Jump
            writeFunction(0x806D259C, &MinecartJumpFix_0); // Fix Diddy Minecart Jump
            if (ENABLE_ORANGE_GUN) {
                *(short*)(0x806E2AB2) = ORANGE_GUN_SFX; // SFX
            }
            break;
        case 2:
            // Lanky
            /*
                Issues:
                    Lanky Phase arm extension has a poly tri not correctly aligned
            */
            *(short*)(0x806F0ABE) = 0; // Remove gun from hands in Tag Barrel
            writeFunction(0x806E48BC, &adaptKrushaZBAnimation_PunchOStand); // Allow Krusha to use slide move if fast enough (OStand)
            *(int*)(0x806E48B4) = 0; // Always run `adaptKrushaZBAnimation`
            *(int*)(0x806F0AB0) = 0x24050001; // Fix Hand State
            *(short*)(0x80749C74) = 10; // Fix Lanky Swimming (A)
            *(short*)(0x80749C80) = 10; // Fix Lanky Swimming (B)
            *(short*)(0x80749CA4) = 10; // Fix Lanky Swimming (Z/First Person)
            writeFunction(0x806141B4, &DiddySwimFix); // Fix Lanky's Swim Animation
            if (ENABLE_ORANGE_GUN) {
                *(short*)(0x806E2A7E) = ORANGE_GUN_SFX; // SFX
                *(short*)(0x806E2A86) = ORANGE_GUN_VARIANCE; // Variance
            }
            break;
        case 3:
            // Tiny
            *(short*)(0x806F0ADE) = 0; // Remove gun from hands in Tag Barrel
            *(int*)(0x806E47F8) = 0; // Prevent slide bounce
            *(short*)(0x806CF784) = 0x5000; // Prevent blink special cases
            *(short*)(0x806832C0) = 0x5000; // Prevent tag blinking
            *(int*)(0x806C1058) = 0; // Prevent Cutscene Kong blinking
            *(int*)(0x806F0AD0) = 0x24050001; // Fix Hand State
            if (ENABLE_ORANGE_GUN) {
                changeFeatherToSprite();
                *(short*)(0x806E2A8A) = ORANGE_GUN_SFX; // SFX
                *(int*)(0x806E2A90) = 0x24030000 | ORANGE_GUN_VARIANCE; // Variance
                *(float*)(0x80753E38) = 350.0f;
            }
            break;
        case 4:
            // Chunky
            *(int*)(0x806CF37C) = 0; // Fix object holding
            *(int*)(0x806F1274) = 0; // Prevent model change for GGone
            *(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
            writeFunction(0x806E4900, &adaptKrushaZBAnimation_PunchOStand); // Allow Krusha to use slide move if fast enough (PPunch)
            *(int*)(0x806E48F8) = 0; // Always run `adaptKrushaZBAnimation`
            *(short*)(0x806F0A9E) = 0; // Remove gun from hands in Tag Barrel
            *(int*)(0x806F0A90) = 0x24050001; // Fix Hand State
        break;
    }
}

typedef struct kongmodel_recolor_data {
    /* 0x000 */ unsigned char kong;
    /* 0x001 */ unsigned char model;
} kongmodel_recolor_data;

static const kongmodel_recolor_data kongmodel_rc[] = {
    {.kong = KONG_DK, .model=KONGMODEL_CRANKY},
    {.kong = KONG_TINY, .model=KONGMODEL_CANDY},
    {.kong = KONG_DIDDY, .model=KONGMODEL_FUNKY},
};

void* updateKongTB(int malloc_size) {
    unsigned short* paad = CurrentActorPointer_0->paad;
    for (int k = 0; k < sizeof(kongmodel_rc)/sizeof(kongmodel_recolor_data); k++) {
        int kong_index = kongmodel_rc[k].kong;
        if (*paad == (2 + kong_index)) {
            if (Rando.kong_models[kong_index] == kongmodel_rc[k].model) {
                CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFEFFF;
            }
        }
    }
    return dk_malloc(malloc_size);
} 

void updateActorHandStates(actorData* actor, int type) {
    custom_kong_models model = KONGMODEL_DEFAULT;
    if ((type >= 2) && (type <= 6)) {
        model = Rando.kong_models[type - 2];
    }
    if ((type >= 196) && (type <= 200)) {
        model = Rando.kong_models[type - 196];
    }
    int resolved = 0;
    if (model != KONGMODEL_DEFAULT) {
        switch (model) {
            case KONGMODEL_KRUSHA:
                addToHandState(actor, 1);
            case KONGMODEL_CRANKY:
                removeFromHandState(actor, 0);
                resolved = 1;
                break;
            case KONGMODEL_KROOL_CUTSCENE:
            case KONGMODEL_KROOL_FIGHT:
                addToHandState(actor, 0);
                removeFromHandState(actor, 1);
                resolved = 1;
                break;
            default:
                break;
        }
    }
    if (resolved) {
        return;
    }
    handleCutsceneKong(actor, type);
}

static const char tied_model_actors[] = {
    -1, 3, 3, 3, // 0-3
    2, 2, 4, 4, // 4-7
    4, 5, 5, 5, // 8-11
    6, 6, 6, 6, // 12-15
    6, // 16
};

void clearGunHandler(actorData* actor) {
    int model_index = getActorModelIndex(actor);
    if (model_index <= 16) {
        int tied_actor = tied_model_actors[model_index];
        if (tied_actor > 0) {
            updateActorHandStates(actor, tied_actor);
        }   
    }
    int interaction = actor->interaction_bitfield;
    if (interaction & 1) {
        // Is Player
        playerData* player = (playerData*)actor;
        if (player->was_gun_out) {
            playGunSFX(player);
            player->was_gun_out = 0;
        }
    }
}

void updateActorHandStates_gun(actorData* actor, int type) {
    custom_kong_models model = KONGMODEL_DEFAULT;
    if ((type >= 2) && (type <= 6)) {
        model = Rando.kong_models[type - 2];
    }
    if ((type >= 196) && (type <= 200)) {
        model = Rando.kong_models[type - 196];
    }
    int resolved = 0;
    if (model != KONGMODEL_DEFAULT) {
        switch (model) {
            case KONGMODEL_KRUSHA:
                removeFromHandState(actor, 1);
            case KONGMODEL_CRANKY:
                addToHandState(actor, 0);
                resolved = 1;
                break;
            case KONGMODEL_KROOL_CUTSCENE:
            case KONGMODEL_KROOL_FIGHT:
                removeFromHandState(actor, 0);
                addToHandState(actor, 1);
                resolved = 1;
                break;
            default:
                break;
        }
    }
    if (resolved) {
        return;
    }
    switch (type) {
        case 2:
        case 196:
        case 4:
        case 198:
        case 5:
        case 199:
        case 6:
        case 200:
            removeFromHandState(actor, 0);
            addToHandState(actor, 1);
            break;
        case 3:
        case 197:
            addToHandState(actor, 0);
            addToHandState(actor, 1);
            break;
    }
}

void pullOutGunHandler(actorData* actor) {
    int model_index = getActorModelIndex(actor);
    if (model_index <= 16) {
        int tied_actor = tied_model_actors[model_index];
        if (tied_actor > 0) {
            updateActorHandStates_gun(actor, tied_actor);
        }   
    }
    int interaction = actor->interaction_bitfield;
    if (interaction & 1) {
        // Is Player
        playerData* player = (playerData*)actor;
        if (!player->was_gun_out) {
            switch (Character) {
                case 0:
                    playSFXFromActor(actor, 0x186, 0xFF, 100, 0x19);
                    playSFXFromActor(actor, 0x17C, 0xFF, 100, 0x19);
                    break;
                case 1:
                    playSFXFromActor(actor, 0x17C, 200, 0xBE, 5);
                    break;
                case 2:
                    playSFXFromActor(actor, 0x186, 0xFF, 0x7F, 0x19);
                    playSFXFromActor(actor, 0x17C, 0xFF, 0xA0, 5);
                    break;
                case 3:
                    playSFXFromActor(actor, 0x185, 0xFF, 0x7F, 0x19);
                    break;
                case 4:
                    playSFXFromActor(actor, 0x18E, 0xFF, 0x7F, 0x19);
                    break;
            }
            player->was_gun_out = 1;
        }
    }
}

void initModelChanges(void) {
    for (int i = 0; i < 5; i++) {
        custom_kong_models model = Rando.kong_models[i];
        if (model == KONGMODEL_DEFAULT) {
            continue;
        }
        switch (model) {
            case KONGMODEL_KRUSHA:
            case KONGMODEL_KROOL_CUTSCENE:
            case KONGMODEL_KROOL_FIGHT:
                initKrusha(i);
                break;
            case KONGMODEL_CRANKY:
                KongTagNames[i] = 8;
                KongTextNames[i] = cranky_name;
                break;
            case KONGMODEL_CANDY:
                KongTagNames[i] = 9;
                KongTextNames[i] = candy_name;
                break;
            case KONGMODEL_FUNKY:
                KongTagNames[i] = 10;
                KongTextNames[i] = funky_name;
                break;
            case KONGMODEL_DISCOCHUNKY:
                if (i == 4) {
                    *(int*)(0x806CF37C) = 0; // Fix object holding
                    *(int*)(0x806F1274) = 0; // Prevent model change for GGone
                    *(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
                    *(short*)(0x8075BF3E) = 0x2F5C; // Make CS Model Behave normally
                }
                break;
            default:
                break;
        }
    }
}

typedef struct shockwave_paad {
    /* 0x000 */ char unk_00[0x10];
    /* 0x010 */ rgb light_rgb;
} shockwave_paad;

int determineShockwaveColor(actorData* shockwave) {
    shockwave_paad* paad = shockwave->paad;
    int model = getActorModelIndex(shockwave);
    int shockwave_models[] = {0xAD,0xAE,0xD0,0xD1,0xCF};
    int kong_index = -1;
    int offset = ((Rando.colorblind_mode - 1) * 5);
    for (int i = 0; i < 5; i++) {
        if (shockwave_models[i] == model) {
            kong_index = i;
        }
    }
    if (kong_index > -1) {
        paad->light_rgb.red = colorblind_colors[offset + kong_index].red;
        paad->light_rgb.green = colorblind_colors[offset + kong_index].green;
        paad->light_rgb.blue = colorblind_colors[offset + kong_index].blue;
    }
    return model;
}

static FogMapping fog_data[] = {
    {.rgb.red = 0x8A, .rgb.green = 0x52, .rgb.blue = 0x16, .map_index = MAP_AZTEC, .fog_entry=990, .fog_cap = 999},
    {.rgb.red = 0, .rgb.green = 0, .rgb.blue = 0, .map_index = MAP_CAVES, .fog_entry=990, .fog_cap = 999},
    {.rgb.red = 0, .rgb.green = 0, .rgb.blue = 0, .map_index = MAP_CASTLE, .fog_entry=990, .fog_cap = 999},
    {.rgb.red = 0, .rgb.green = 0, .rgb.blue = 0, .map_index = MAP_TESTMAP, .fog_entry=990, .fog_cap = 999}, // What's used for default
};

void initCosmetic(void) {
    /**
     * @brief Initialize all cosmetic functionality
     * 
     */
    initModelChanges();
    for (int i = 0; i < 3; i++) {
        int red = Rando.fog[i].red;
        int green = Rando.fog[i].green;
        int blue = Rando.fog[i].blue;
        if ((red != 0) || (green != 0) || (blue != 0)) {
            fog_data[i].rgb = Rando.fog[i];
            if (i != 0) {
                fog_data[i].fog_entry = 995;
                fog_data[i].fog_cap = 1003;
            }
        }
    }
}

void setFog(int enabled) {
    EnvironmentFog.enabled = enabled;
    EnvironmentFog.opacity = 0;
    for (int i = 0; i < 4; i++) {
        if ((CurrentMap == fog_data[i].map_index) || (i == 3)) {
            EnvironmentFog.rgb = fog_data[i].rgb;
            EnvironmentFog.entry_range = fog_data[i].fog_entry;
            EnvironmentFog.cap_range = fog_data[i].fog_cap;
            return;
        }
    }
}