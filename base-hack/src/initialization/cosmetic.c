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

void initDiscoChunky(void) {
    /**
     * @brief Initialize Disco Chunky cosmetic feature
     * 
     */
    if (Rando.disco_chunky) {
        // Disco
        *(char*)(0x8075C45B) = 0xE; // General Model
        *(short*)(0x806F123A) = 0xED; // Instrument. Any devs copying this line, change the write to 0xE **UNLESS* you are also importing the custom disco chunky w/ instrument model.
        *(int*)(0x806CF37C) = 0; // Fix object holding
        *(short*)(0x8074E82C) = 0xE; // Tag Barrel Model
        *(short*)(0x8075EDAA) = 0xE; // Cutscene Chunky Model
        *(short*)(0x8075571E) = 0xE; // Generic Cutscene Model
        *(short*)(0x80755738) = 0xE; // Generic Cutscene Model
        *(int*)(0x806F1274) = 0; // Prevent model change for GGone
        *(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
        *(short*)(0x8075BF3E) = 0x2F5C; // Make CS Model Behave normally
        *(short*)(0x8075013E) = 0xE; // Low Poly Model
    }
}

static short pellets[] = {48, 36, 42, 43, 38};

#define ORANGE_GUN_SFX 400
#define ORANGE_GUN_VARIANCE 5
#define ENABLE_ORANGE_GUN 1

void initKrusha(void) {
    /**
     * @brief Initialize the Krusha Cosmetic/Gameplay feature
     * 
     */
    if (Rando.krusha_slot != -1) {
        // Krusha
        int slot = Rando.krusha_slot;
        KongModelData[slot].model = 0xDB; // General Model
        TagModelData[slot].model = 0xDB; // Tag Barrel Model
        writeFunction(0x80677E94, &adjustAnimationTables); // Give Krusha animations to slot
        writeFunction(0x806C32B8, &updateCutsceneModels); // Fix cutscene models
        RollingSpeeds[slot] = 175; // Increase Krusha slide speed to 175
        KongTagNames[slot] = 6; // Change kong name in Tag Barrel
        KongTextNames[slot] = KongTextNames[5];
        LedgeHangY[slot] = LedgeHangY[5];
        LedgeHangY_0[slot] = LedgeHangY_0[5];
        *(short*)(0x8074AB5A) = 0x0040; // Enables Krusha's spin attack to knock kasplats down
        PotionAnimations[slot] = PotionAnimations[4];
        actor_functions[2 + slot] = (void*)0x806C9F44; // Replace Kong Code w/ Krusha Code
        if (ENABLE_ORANGE_GUN) {
            // Gun Stuff
            int focused_pellet = pellets[slot];
            actor_functions[focused_pellet] = &OrangeGunCode;
            *(short*)(0x806E241A) = focused_pellet;
            *(int*)(0x8075D154 + (slot << 2)) = 0x806E2408;
            setActorDamage(focused_pellet, 3);
            *(int*)(0x8071AAC4) = 0;
            *(int*)(0x8075DBB4 + (slot << 2)) = 0x806FAE0C;
            *(short*)(0x806E240A) = 0x3E80;
        }
        switch (slot) {
            case 0:
                // DK
                *(short*)(0x8075ED4A) = 0xDB; // Cutscene DK Model
                *(short*)(0x8075573E) = 0xDB; // Generic Cutscene Model
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
                *(short*)(0x806F11E6) = 0xDB; // Instrument
                *(short*)(0x8075ED62) = 0xDB; // Cutscene Diddy Model
                *(short*)(0x80755736) = 0xDB; // Generic Cutscene Model
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
                *(short*)(0x806F1202) = 0xDB; // Instrument
                *(short*)(0x8075ED7A) = 0xDB; // Cutscene Lanky Model
                *(short*)(0x8075573A) = 0xDB; // Generic Cutscene Model
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
                *(short*)(0x806F121E) = 0xDB; // Instrument
                *(short*)(0x8075ED92) = 0xDB; // Cutscene Tiny Model
                *(short*)(0x8075573C) = 0xDB; // Generic Cutscene Model
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
                *(short*)(0x806F123A) = 0xDB; // Instrument
                *(int*)(0x806CF37C) = 0; // Fix object holding
                *(short*)(0x8075EDAA) = 0xDB; // Cutscene Chunky Model
                *(short*)(0x8075571E) = 0xDB; // Generic Cutscene Model
                *(short*)(0x80755738) = 0xDB; // Generic Cutscene Model
                *(int*)(0x806F1274) = 0; // Prevent model change for GGone
                *(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
                writeFunction(0x806E4900, &adaptKrushaZBAnimation_PunchOStand); // Allow Krusha to use slide move if fast enough (PPunch)
                *(int*)(0x806E48F8) = 0; // Always run `adaptKrushaZBAnimation`
                *(short*)(0x806F0A9E) = 0; // Remove gun from hands in Tag Barrel
                *(int*)(0x806F0A90) = 0x24050001; // Fix Hand State
            break;
        }
    }
}

void initSkyboxRando(void) {
    /**
     * @brief Initialize the skybox cosmetic randomization
     * 
     */
    if (Rando.colorblind_mode != COLORBLIND_OFF) {
        for (int i = 0; i < 8; i++) {
            Rando.skybox_colors[i].red = 0x31;
            Rando.skybox_colors[i].green = 0x33;
            Rando.skybox_colors[i].blue = 0x38;
        }
    } else if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
        for (int i = 0; i < 8; i++) {
            Rando.skybox_colors[i].red = 0;
            Rando.skybox_colors[i].green = 0;
            Rando.skybox_colors[i].blue = 0;
        }
    }
    if ((Rando.misc_cosmetic_on) || (Rando.colorblind_mode != COLORBLIND_OFF) || (Rando.seasonal_changes == SEASON_HALLOWEEN)) {
        for (int i = 0; i < 8; i++) {
            SkyboxBlends[i].top.red = Rando.skybox_colors[i].red;
            SkyboxBlends[i].top.green = Rando.skybox_colors[i].green;
            SkyboxBlends[i].top.blue = Rando.skybox_colors[i].blue;
            float rgb[3] = {0,0,0};
            float rgb_backup[3] = {0,0,0};
            rgb[0] = Rando.skybox_colors[i].red;
            rgb[1] = Rando.skybox_colors[i].green;
            rgb[2] = Rando.skybox_colors[i].blue;
            for (int j = 0; j < 3; j++) {
                rgb_backup[j] = rgb[j];
                rgb[j] *= 1.2f;
            }
            int exceeded = 0;
            for (int j = 0; j < 3; j++) {
                if (rgb[j] > 255.0f) {
                    exceeded = 1;
                }
            }
            if (exceeded) {
                for (int j = 0; j < 3; j++) {
                    rgb[j] = rgb_backup[j] * 0.8f;
                }
            }
            SkyboxBlends[i].bottom.red = rgb[0];
            SkyboxBlends[i].bottom.green = rgb[1];
            SkyboxBlends[i].bottom.blue = rgb[2];
            for (int j = 0; j < 2; j++) {
                SkyboxBlends[i].unk[j].red = rgb[0];
                SkyboxBlends[i].unk[j].green = rgb[1];
                SkyboxBlends[i].unk[j].blue = rgb[2];
            }
        }
        // Change pufftoss skybox entry
        *(int*)(0x8075E1EC) = 0x80708234; // Pufftoss changed to null skybox, should prevent seizure-inducing effects
    }
}

void initSeasonalChanges(void) {
    if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
        *(int*)(0x8075E0B8) = 0x807080E0; // Makes isles reference Castle skybox data

        // Chains
        *(short*)(0x8069901A) = 0xE; // Vine param
        *(short*)(0x8069903A) = 0xE; // Vine param
        *(int*)(0x80698754) = 0; // Cancel branch
        *(int*)(0x80698B6C) = 0; // Cancel branch
        *(short*)(0x80698B74) = 0x1000; // Force branch
    } else if (Rando.seasonal_changes == SEASON_CHRISTMAS) {
        // Make santa visit Isles
        *(short*)(0x8070637E) = 115; // Moon Image
        *(int*)(0x8075E0B8) = 0x807080E0; // Makes isles reference Castle skybox data
        *(int*)(0x806682C8) = 0x240E0004; // Set ground sfx to snow
        *(int*)(0x806682CC) = 0x240C0004; // Set ground sfx to snow
        *(int*)(0x806682DC) = 0x240E0004; // Set ground sfx to snow

        // for (int i = 0; i < 6; i++) {
        //     *WeatherData[i].texture_pointer = 0x173B;
        //     WeatherData[i].width = 0x40;
        //     WeatherData[i].height = 0x40;
        //     WeatherData[i].codec_info = 0x0301;
        //     WeatherData[i].frame_count = 1;
        // }
        // int addr = 0x80759EC4;
        // for (int i = 0; i < 6; i++) {
        //     *(int*)(addr + (4 * i)) = 0x8068B5D8;
        // }
        // *(int*)(0x80711A64) = 0x24140010;
        // *(int*)(0x80711A5C) = 0x24140010;
        // *(int*)(0x80711A70) = 0x24140010;
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

void writeRGBColor(int value, short* upper_address, short* lower_address) {
    int upper = value >> 8;
    int lower = ((value & 0xFF) << 8) | 0xFF;
    *upper_address = upper;
    *lower_address = lower;
}

typedef struct crosshair_colors {
    /* 0x000 */ int regular;
    /* 0x004 */ int homing;
    /* 0x008 */ int sniper;
} crosshair_colors;

static const crosshair_colors crosshairs[4] = {
    {.regular=0xC80000, .homing=0x00C800, .sniper=0xFFD700},
    {.regular=0x0072FF, .homing=0xFFFFFF, .sniper=0xFDE400},
    {.regular=0x318DFF, .homing=0xFFFFFF, .sniper=0xE3A900},
    {.regular=0xC72020, .homing=0xFFFFFF, .sniper=0x13C4D8},
};

void initColorblindChanges(void) {
    if (Rando.colorblind_mode != COLORBLIND_OFF) {
        writeFunction(0x8069E968, &determineShockwaveColor); // Shockwave handler
        *(short*)(0x8069E974) = 0x1000; // Force first option
        *(int*)(0x8069E9B0) = 0; // Prevent write
        *(int*)(0x8069E9B4) = 0; // Prevent write
        *(int*)(0x8069E9BC) = 0; // Prevent write
    }
    crosshair_colors* hair = (crosshair_colors*)&crosshairs[(int)Rando.colorblind_mode];
    if (hair) {
        // Gun (Sniper) function
        writeRGBColor(hair->sniper, (short*)0x806FFA92, (short*)0x806FFA96);
        writeRGBColor(hair->homing, (short*)0x806FFA76, (short*)0x806FFA7A);
        // Gun (No Sniper) function
        writeRGBColor(hair->regular, (short*)0x806FF0C6, (short*)0x806FF0CA);
        writeRGBColor(hair->homing, (short*)0x806FF0AA, (short*)0x806FF0AE);
    }
}

void initCosmetic(void) {
    /**
     * @brief Initialize all cosmetic functionality
     * 
     */
    if (Rando.krusha_slot == 4) {
        Rando.disco_chunky = 0;
    } else if (Rando.krusha_slot > 4) {
        Rando.krusha_slot = -1;
    }
    initDiscoChunky();
    initKrusha();
    initSkyboxRando();
    initSeasonalChanges();
    initColorblindChanges();
    //loadWidescreen(OVERLAY_BOOT);
}