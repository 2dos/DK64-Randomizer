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
        *(short*)(0x806F123A) = 0xED; // Instrument
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
        *(int*)(0x80677E94) = 0x0C000000 | (((int)&adjustAnimationTables & 0xFFFFFF) >> 2); // Give Krusha animations to slot
        *(int*)(0x806C32B8) = 0x0C000000 | (((int)&updateCutsceneModels & 0xFFFFFF) >> 2); // Fix cutscene models
        RollingSpeeds[slot] = 175; // Increase Krusha slide speed to 175
        KongTagNames[slot] = 6; // Change kong name in Tag Barrel
        KongTextNames[slot] = KongTextNames[5];
        LedgeHangY[slot] = LedgeHangY[5];
        LedgeHangY_0[slot] = LedgeHangY_0[5];
        *(short*)(0x8074AB5A) = 0x0040; // Enables Krusha's spin attack to knock kasplats down
        PotionAnimations[slot] = PotionAnimations[4];
        actor_functions[2 + slot] = (void*)0x806C9F44; // Replace Kong Code w/ Krusha Code
        switch (slot) {
            case 0:
                // DK
                *(short*)(0x8075ED4A) = 0xDB; // Cutscene DK Model
                *(short*)(0x8075573E) = 0xDB; // Generic Cutscene Model
                *(short*)(0x806F0AFE) = 0; // Remove gun from hands in Tag Barrel
                *(int*)(0x806F0AF0) = 0x24050001; // Fix Hand State
                *(int*)(0x806D5EC4) = 0; // Prevent Moving Ground Attack pop up
                *(short*)(0x8064AF5E) = 5; // Reduce slam range for DK Dungeon GB Slam
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
                *(int*)(0x806E495C) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_Charge & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (Charge)
                *(int*)(0x806E499C) = 0; // NOP Animation calls
                *(int*)(0x806E49C8) = 0; // NOP Animation calls
                *(int*)(0x806E49F0) = 0; // NOP Animation calls
                *(short*)(0x806CF5F0) = 0x5000; // Prevent blink special cases
                *(int*)(0x806CF76C) = 0; // Prevent blink special cases
                *(int*)(0x806832B8) = 0; // Prevent tag blinking
                *(int*)(0x806C1050) = 0; // Prevent Cutscene Kong blinking
                *(unsigned char*)(0x8075D19F) = 0xA0; // Fix Gun Firing
                *(int*)(0x806141B4) = 0x0C000000 | (((int)&DiddySwimFix & 0xFFFFFF) >> 2); // Fix Diddy's Swim Animation
                *(short*)(0x80749764) = 10; // Fix Diddy Swimming (A)
                *(short*)(0x80749758) = 10; // Fix Diddy Swimming (B)
                *(short*)(0x8074974C) = 10; // Fix Diddy Swimming (Z/First Person)
                *(int*)(0x806E903C) = 0x0C000000 | (((int)&MinecartJumpFix & 0xFFFFFF) >> 2); // Fix Diddy Minecart Jump
                *(int*)(0x806D259C) = 0x0C000000 | (((int)&MinecartJumpFix_0 & 0xFFFFFF) >> 2); // Fix Diddy Minecart Jump
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
                *(int*)(0x806E48BC) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_PunchOStand & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (OStand)
                *(int*)(0x806E48B4) = 0; // Always run `adaptKrushaZBAnimation`
                *(int*)(0x806F0AB0) = 0x24050001; // Fix Hand State
                *(short*)(0x80749C74) = 10; // Fix Lanky Swimming (A)
                *(short*)(0x80749C80) = 10; // Fix Lanky Swimming (B)
                *(short*)(0x80749CA4) = 10; // Fix Lanky Swimming (Z/First Person)
                *(int*)(0x806141B4) = 0x0C000000 | (((int)&DiddySwimFix & 0xFFFFFF) >> 2); // Fix Lanky's Swim Animation
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
                *(int*)(0x806E4900) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_PunchOStand & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (PPunch)
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
    if (Rando.misc_cosmetic_on) {
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

void initKlaptraps(void) {
    /**
     * @brief Fix Klaptraps in Beaver Bother, so if no model is selected, it will default to a green klaptrap.
     * 
     */
    // Change Beaver Bother Klaptrap Model
    if (Rando.klaptrap_color_bbother == 0) {
        Rando.klaptrap_color_bbother = 0x21; // Set to default model if no model assigned
    }
}

void initWrinklyColoring(void) {
    /**
     * @brief Alter Wrinkly's color. Do not change color if misc cosmetics off or all fields are 0.
     * 
     */
    if (Rando.misc_cosmetic_on) {
        int pass = 0;
        for (int i = 0; i < 3; i++) {
            if (Rando.wrinkly_rgb[i] > 0) {
                pass = 1;
            }
        }
        if (pass) {
            *(short*)(0x8064F052) = Rando.wrinkly_rgb[0];
            *(short*)(0x8064F04A) = Rando.wrinkly_rgb[1];
            *(short*)(0x8064F046) = Rando.wrinkly_rgb[2];
        }
    }
}

void initSeasonalChanges(void) {
    if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
        *(int*)(0x8075E0B8) = 0x807080E0; // Makes isles reference Castle skybox data
    } else if (Rando.seasonal_changes == SEASON_CHRISTMAS) {
        for (int i = 0; i < 6; i++) {
            *WeatherData[i].texture_pointer = 0x173B;
            WeatherData[i].width = 0x40;
            WeatherData[i].height = 0x40;
            WeatherData[i].codec_info = 0x0301;
            WeatherData[i].frame_count = 1;
        }
        int addr = 0x80759EC4;
        for (int i = 0; i < 6; i++) {
            *(int*)(addr + (4 * i)) = 0x8068B5D8;
        }
        *(int*)(0x80711A64) = 0x24140010;
        *(int*)(0x80711A5C) = 0x24140010;
        *(int*)(0x80711A70) = 0x24140010;
    }
}

static const rgb kong_shockwave_colors[15] = {
    // Protan
    {.red=0x00, .green=0x00, .blue=0x00}, // DK
    {.red=0x00, .green=0x72, .blue=0xFF}, // Diddy
    {.red=0x76, .green=0x6D, .blue=0x5A}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xFD, .green=0xE4, .blue=0x00}, // Chunky
    // Deutan
    {.red=0x00, .green=0x00, .blue=0x00}, // DK
    {.red=0x31, .green=0x8D, .blue=0xFF}, // Diddy
    {.red=0x7F, .green=0x6D, .blue=0x59}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xE3, .green=0xA9, .blue=0x00}, // Chunky
    // Tritan
    {.red=0x00, .green=0x00, .blue=0x00}, // DK
    {.red=0xC7, .green=0x20, .blue=0x20}, // Diddy
    {.red=0x13, .green=0xC4, .blue=0xD8}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xFF, .green=0xA4, .blue=0xA4}, // Chunky
};

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
        paad->light_rgb.red = kong_shockwave_colors[offset + kong_index].red;
        paad->light_rgb.green = kong_shockwave_colors[offset + kong_index].green;
        paad->light_rgb.blue = kong_shockwave_colors[offset + kong_index].blue;
    }
    return model;
}

void initColorblindChanges(void) {
    if (Rando.colorblind_mode != COLORBLIND_OFF) {
        *(int*)(0x8069E968) = 0x0C000000 | (((int)&determineShockwaveColor & 0xFFFFFF) >> 2); // Shockwave handler
        *(short*)(0x8069E974) = 0x1000; // Force first option
        *(int*)(0x8069E9B0) = 0; // Prevent write
        *(int*)(0x8069E9B4) = 0; // Prevent write
        *(int*)(0x8069E9BC) = 0; // Prevent write
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
    initKlaptraps();
    initWrinklyColoring();
    initSeasonalChanges();
    initColorblindChanges();
}