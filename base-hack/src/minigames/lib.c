// minigame: all
#include "minigame_defs.h"
void renderText(Gfx **dl_ptr, const int x, const int y, const int red, const int green, const int blue, const int alpha, const char *str) {
    // Renders a text string to the screen in the arcade font.
    // Text is (mostly) monospaced
    Gfx *dl = *dl_ptr;
    gDPPipeSync(dl++);
    gDPSetCycleType(dl++, G_CYC_1CYCLE);
    gSPLoadGeometryMode(dl++, 0);
    gSPSetGeometryMode(dl++, G_ZBUFFER | G_SHADING_SMOOTH | 0x00000002);
    gDPSetPrimColor(dl++, 0, 0, red, green, blue, alpha);
    gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
    *dl_ptr = textDraw(dl, 2, x, y, str);
}

void playSFXWrapper(int sfx) {
    // Plays a sound effect
    // See: https://docs.google.com/spreadsheets/d/16uVSmToSKHN9DD8skOUoaxjWFm38xxq05cTKypfPGAU/edit?gid=0#gid=0
    _alSndpPlay(SFXSoundbank, sfx, 0x7FFF, 0x3F, 1.0f, 0, (void*)0);
}

Gfx* drawScreenRect(Gfx* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha) {
    // Draws a rectangle to the screen
    // X and Y coordinates must be multiplied by 4
	gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_FILL);
	gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
	gSPClearGeometryMode(dl++, G_ZBUFFER);
	int color = ((red & 0x1F) << 11) | ((green & 0x1F) << 6) | ((blue & 0x1F) << 1) | (alpha & 0x1);
	gDPSetFillColor(dl++, (color << 16) | color);
	gDPSetScissor(dl++, G_SC_NON_INTERLACE, 10, 10, 309, 229);
	gDPFillRectangle(dl++, x1 >> 2, y1 >> 2, x2 >> 2, y2 >> 2);
	return dl;
}

Gfx *drawTriangleSeries(Gfx *dl, Vtx *vertex_write, short *coordinates, int red, int green, int blue, int point_count) {
    // vertex_write must be a pointer to an array of {point_count} items
    // coordinates must be a pointer to an array of {point_count} x and y coordinates
    // Triangle series must be a convex polygon
    // Point count cannot exceed 32 vertices
    for (int i = 0; i < point_count; i++) {
        // Coords
        vertex_write[i].v.ob[0] = coordinates[i << 1];
        vertex_write[i].v.ob[1] = coordinates[(i << 1) + 1];
        vertex_write[i].v.ob[2] = 0;
        // Misc
        vertex_write[i].v.flag = 0;
        vertex_write[i].v.tc[0] = 0;
        vertex_write[i].v.tc[1] = 0;
        // Color
        vertex_write[i].v.cn[0] = red;
        vertex_write[i].v.cn[1] = green;
        vertex_write[i].v.cn[2] = blue;
        vertex_write[i].v.cn[3] = 0xFF;
    }
    __osWritebackDCache(vertex_write, sizeof(Vtx) * point_count);
    gDPPipeSync(dl++);
    gDPSetCycleType(dl++, G_CYC_1CYCLE);
    gDPSetCombineMode(dl++, G_CC_SHADE, G_CC_SHADE);
    gDPSetRenderMode(dl++, G_RM_OPA_SURF, G_RM_OPA_SURF2);
    gSPClearGeometryMode(dl++, 0xFFFFFFFF);
    gSPSetGeometryMode(dl++, G_SHADE | G_SHADING_SMOOTH);
    gSPSegment(dl++, 0x0, 0x0);
    gSPVertex(dl++, (int)(vertex_write) & 0x7FFFFFFF, point_count, 0);
    int tri_count = point_count - 2;
    int offset_index = 0;
    while (tri_count > 0) {
        // if (tri_count == 1) {
            gSP1Triangle(dl++, 0, offset_index + 1, offset_index + 2, 0);
            tri_count--;
            offset_index++;
        // } else {
        //     gSP2Triangles(dl++, 0, offset_index + 1, offset_index + 2, 0, 0, offset_index + 2, offset_index + 3, 0);
        //     tri_count -= 2;
        //     offset_index += 2;
        // }
    }
    gDPPipeSync(dl++);
    return dl;
}

#define MINIGAME_BONUS_MAP_COUNT 4
typedef struct MinigameSignalStruct {
    unsigned char main_map_id;
    unsigned char bonus_map_ids[MINIGAME_BONUS_MAP_COUNT];
    unsigned char exit_map;
    unsigned short first_reward_perm_flag;
    unsigned short first_reward_temp_flag;
    unsigned short second_reward_perm_flag;
    unsigned short second_reward_temp_flag;
    unsigned short story_flag;
} MinigameSignalStruct;

ROM_DATA static char game_exited = 0;
ROM_DATA static char in_story = 0;
ROM_DATA static char enable_reward = 0;
ROM_RODATA_NUM static const MinigameSignalStruct arcade_data = {
    .main_map_id = MAP_DKARCADE,
    .bonus_map_ids = {
        MAP_ARCADE25M_ONLY,
        MAP_ARCADE50M_ONLY,
        MAP_ARCADE75M_ONLY,
        MAP_ARCADE100M_ONLY,
    },
    .first_reward_perm_flag = FLAG_ARCADE_ROUND1,
    .first_reward_temp_flag = 0x10,
    .second_reward_perm_flag = FLAG_COLLECTABLE_NINTENDOCOIN,
    .second_reward_temp_flag = 0x11,
    .story_flag = 0x63,
    .exit_map = 0,
};
ROM_RODATA_NUM static const MinigameSignalStruct jetpac_data = {
    .main_map_id = MAP_JETPAC,
    .bonus_map_ids = {
        MAP_JETPAC_ROCKET,
        0,
        0,
        0,
    },
    .first_reward_perm_flag = FLAG_COLLECTABLE_RAREWARECOIN,
    .first_reward_temp_flag = 0x62,
    .story_flag = 0x61,
    .exit_map = 5,
};

const MinigameSignalStruct *getMinigameSlot(void) {
    if (CurrentMap == jetpac_data.main_map_id) {
        return &jetpac_data;
    } else {
        for (int i = 0; i < MINIGAME_BONUS_MAP_COUNT; i++) {
            if (jetpac_data.bonus_map_ids[i] == CurrentMap) {
                return &jetpac_data;
            }
        }
    }
    return &arcade_data;
}

void gameInit(void) {
    // Initializes the game parameters.
    // Put this in your initialization code, otherwise the game will not correctly respond to the Nin/RW Coin checks
    const MinigameSignalStruct *ref_data = getMinigameSlot();
    in_story = checkFlag(ref_data->story_flag, FLAGTYPE_TEMPORARY);
}

ROM_RODATA_NUM static const short barrel_types[3] = {0x1C, 0x86, 0x6B};
void exitMinigame(const MinigameSignalStruct *data) {
    if (data->exit_map == 0) {
        ExitFromBonus();
    } else {
        initiateTransition(data->exit_map, 0);
    }
}

void gameExit(void) {
    // Exits the game. Call this for an exit from the game which does not yield the reward
    if (game_exited) {
        return;
    }
    const MinigameSignalStruct *ref_data = getMinigameSlot();
    if (CurrentMap == ref_data->main_map_id) {
        if ((enable_reward) && (in_story)) {
            if (!checkFlag(ref_data->first_reward_perm_flag, FLAGTYPE_PERMANENT)) {
                setFlag(ref_data->first_reward_temp_flag, 1, FLAGTYPE_TEMPORARY);
            } else if (ref_data->second_reward_perm_flag) {
                if (!checkFlag(ref_data->second_reward_perm_flag, FLAGTYPE_PERMANENT)) {
                    setFlag(ref_data->second_reward_temp_flag, 1, FLAGTYPE_TEMPORARY); // Spawn R2 Reward
                }
            }
        }
        if (!in_story) {
            initiateTransition(MAP_MAINMENU, 0);
        } else {
            exitMinigame(ref_data);
        }
    } else {
        if ((enable_reward) && (in_story)) {
            int b = 0;
            int index = getSpawnerIndexOfResolvedBonus(&barrel_types, 3, &b);
            resolveBonus(b, index, 7, 2.0f);
        }
        exitMinigame(ref_data);
    }
    game_exited = 1;
}

void gameVictory(void) {
    // Mostly the same as gameExit(), but just gives the reward. Call this upon game victory
    enable_reward = 1;
    gameExit();
}

Gfx* drawImage(Gfx* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int red, int green, int blue, int opacity) {
	// Draws an image to the screen
    // Image provided is an image in table 14 (HUD Textures)
    // See: https://docs.google.com/spreadsheets/d/18gBPArJ2abdR3P9BeQw3OD_PLAjITFaE3r82bWUdC8U/edit?gid=970976581#gid=970976581
    dl = initDisplayList(dl);
	gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
	gDPSetPrimColor(dl++, 0, 0, red, green, blue, opacity);
	gDPSetCombineLERP(
        dl++,
        TEXEL0, 0, PRIMITIVE, 0,   // RGB = TEXEL0 * PRIMITIVE
        TEXEL0, 0, PRIMITIVE, 0,   // Alpha = TEXEL0 * PRIMITIVE
        TEXEL0, 0, PRIMITIVE, 0,
        TEXEL0, 0, PRIMITIVE, 0
    );
	gDPSetTextureFilter(dl++, G_TF_POINT);
	return displayImage(dl++, text_index, 0, codec_index, img_width, img_height, x, y, xScale, yScale, 0, 0.0f);
}
