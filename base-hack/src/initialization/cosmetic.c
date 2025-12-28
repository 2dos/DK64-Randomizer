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

#define ORANGE_GUN_SFX 400
#define ORANGE_GUN_VARIANCE 5

static const char* krool_name = "K. ROOL";
static const char* cranky_name = "CRANKY";
static const char* candy_name = "CANDY";
static const char* funky_name = "FUNKY";

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
                if (Rando.kong_models[i] != KONGMODEL_KRUSHA) {
                    KongTextNames[i] = krool_name;
                }
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

void getRainbowAmmoColor(rgba *color) {
    int pos = FrameReal % 1536;
    int step = pos >> 8;
    switch (step) {
        case 0:
            // 0 <= pos <= 255
            color->red = 255;
            color->green = pos;
            break;
        case 1:
            // 255 < pos <= 511
            color->red = 511 - pos;
            color->green = 255;
            break;
        case 2:
            // 511 < pos <= 767
            color->green = 255;
            color->blue = pos - 512;
            break;
        case 3:
            // 767 < pos <= 1023
            color->green = 1023 - pos;
            color->blue = 255;
            break;
        case 4:
            // 1023 < pos <= 1279
            color->red = pos - 1024;
            color->blue = 255;
            break;
        default:
            // 1280 < pos <= 1535
            color->red = 255;
            color->blue = 1535 - pos;
            break;
    }
}

void updateSpriteColor(sprite_info *sprite) {
    rgba temp = {.alpha = 0xFF};
    getRainbowAmmoColor(&temp);
    sprite->red = temp.red;
    sprite->green = temp.green;
    sprite->blue = temp.blue;
}

void colorRainbowAmmo(void* actor, float x, float y, float z, int unk0) {
    allocateBone(actor, x, y, z, unk0);
    if (Rando.rainbow_ammo) {
        loadSpriteFunction(&updateSpriteColor);
    }
}

void colorRainbowAmmoHUD(sprite_info *sprite) {
    HUDSpriteUpdate(sprite);
    if (Rando.rainbow_ammo) {
        updateSpriteColor(sprite);
    }
}

void colorRainbowAmmoHUD_0(sprite_info *sprite) {
    PauseSpriteUpdate(sprite);
    if (Rando.rainbow_ammo) {
        updateSpriteColor(sprite);
    }
}

void setHUDUpdateFunction(void* function, int item_index) {
    if ((item_index == 2) || (item_index == 3)) {
        loadSpriteFunction(&colorRainbowAmmoHUD);
    } else {
        loadSpriteFunction(function);
    }
}

void setHUDUpdateFunction_0(void* function, int item_index, int control_type) {
    if ((item_index == 2) || (item_index == 3)) {
        loadSpriteFunction(&colorRainbowAmmoHUD_0);
    } else if (control_type == 16) {
        loadSpriteFunction((int)&totalsSprite);
    } else if (control_type == 17) {
        loadSpriteFunction((int)&checksSprite);
    } else {
        loadSpriteFunction(function);
    }
}

static unsigned char bonus_ost[] = {
    SONG_MINIGAMES,
    SONG_STEALTHYSNOOP,
    SONG_BATTLEARENA,
    SONG_MADMAZEMAUL,
    SONG_MINECARTMAYHEM,
    SONG_MONKEYSMASH,
    SONG_HELMBONUS,
    SONG_ENGUARDE,
    SONG_RAMBI,
};

static unsigned char boss_ost[] = {
    SONG_JAPESDILLO,
    SONG_AZTECDOGADON,
    SONG_FACTORYJACK,
    SONG_GALLEONPUFFTOSS,
    SONG_FORESTDOGADON,
    SONG_CAVESDILLO,
    SONG_CASTLEKUTOUT,
    SONG_KROOLBATTLE,
    SONG_MINIBOSS,
    SONG_FORESTSPIDER,
};

int pickRandomFromPool(unsigned char* pool, int count) {
    int rng = getRNGLower31() & 0xFF;
    while (rng >= count) {
        // Yes, I know rng % count is better, but if I don't do this, Wii U will crash
        // What an A tier console....
        rng -= count;
    }
    return pool[rng];
}

void playBonusSong(songs song, float volume) {
    if (Rando.bonus_music_rando) {
        song = pickRandomFromPool(&bonus_ost, sizeof(bonus_ost));
    }
    playSong(song, volume);
}

void playBossSong(songs song, float volume) {
    if (Rando.boss_music_rando) {
        song = pickRandomFromPool(&boss_ost, sizeof(boss_ost));
    }
    playSong(song, volume);
}

void playSongWCheck(songs song, float volume) {
    if (Rando.bonus_music_rando && inU8List(song, &bonus_ost, sizeof(bonus_ost))) {
        song = pickRandomFromPool(&bonus_ost, sizeof(bonus_ost));
    }
    if (Rando.boss_music_rando && inU8List(song, &boss_ost, sizeof(boss_ost))) {
        song = pickRandomFromPool(&boss_ost, sizeof(boss_ost));
    }
    playSong(song, volume);
}