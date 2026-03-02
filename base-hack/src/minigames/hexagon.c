// minigame: hexagon
#include "minigame_defs.h"

/*
    Note: This game currently only works when placed in Jetpac.
    This is due to a missing guOrtho call in the wrapper code for Arcade.
    This will be solved by the time 6.0 comes out (hopefully).

    For those reading this making their own games with Tri rendering, you may
    experience issues with your game unless you place it in the Jetpac slot
    for this same reason.

    For those reading this, this also only works on slightly inaccurate emulators
    due to assumptions with the RSP with tri rendering. This will be eventually 
    fixed.

    Also incomplete
*/

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_MUSICCORRECT_INIT,  // Used to allow music playing
    GAMESTATE_MUSICCORRECT,  // Used to allow music playing
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_GAMEOVER,
} gameStates;

typedef enum colorStates {
    COLORSTATE_CENTERHEX_BORDER,
    COLORSTATE_BACK_0,
    COLORSTATE_BACK_1,
    COLORSTATE_PLAYER,
} colorStates;

typedef struct patternStruct {
    unsigned char walls[6];
    unsigned char starter;
    unsigned char elements;
} patternStruct;

typedef struct wallStruct {
    unsigned char wall_index;
    unsigned char used;
    float dist;
} wallStruct;


#define WALL_BUFFER_COUNT 100
#define PATTERN_COUNT 4

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static unsigned char hue_shift_timer = 5;
__attribute__((aligned(8)))
ROM_DATA static Vtx center_hex[2][12];
ROM_DATA static Vtx background[2][24];
ROM_DATA static Vtx player[2][3];
ROM_DATA static Vtx hex_walls_vtx[2][WALL_BUFFER_COUNT * 4] = {};


ROM_DATA static int identity_mtx[] = {
    0x00010000, 0x00000000,
    0x00000000, 0x00000000,

    0x00000000, 0x00000000,
    0x00010000, 0x00000000,

    0x00000000, 0x00000000,
    0x00000000, 0x00000000,

    0x00000000, 0x00000000,
    0x00010000, 0x00000000,
};

ROM_DATA static rgb hex_colors[] = {
    {.red = 0xFF, .green = 0x00, .blue = 0x00 }, // COLORSTATE_CENTERHEX_BORDER,
    {.red = 0x40, .green = 0x00, .blue = 0x00 }, // COLORSTATE_BACK_0,
    {.red = 0x60, .green = 0x00, .blue = 0x00 }, // COLORSTATE_BACK_1,
    {.red = 0xC0, .green = 0xC0, .blue = 0xC0 }, // COLORSTATE_PLAYER,
};
ROM_DATA static float angle_offset = 0.0f;
ROM_DATA static float player_angle = 30.0f;
ROM_RODATA_NUM static const patternStruct patterns[] = {
    { .walls = { 0, 1, 1, 1, 1, 1 }, .starter = 1, .elements = 1}, // 5 walls 1 gap
    { .walls = { 0, 1, 0, 1, 0, 1 }, .starter = 1, .elements = 1}, // Alternating
    { .walls = { 0, 1, 0, 0, 1, 0 }, .starter = 1, .elements = 1}, // Opposite
    { .walls = { 0, 1, 0, 1, 1, 1 }, .starter = 1, .elements = 1}, // 2 gaps
};
ROM_DATA static wallStruct hex_walls[WALL_BUFFER_COUNT] = {};
ROM_DATA static patternStruct *last_wall = 0;
ROM_DATA static unsigned char wall_element_counter = 0;
ROM_DATA static unsigned char summon_timer = 0;
ROM_DATA static unsigned char wall_rotational_offset = 0;
ROM_DATA static unsigned short effect_timer = 300;
ROM_DATA static unsigned char rotation_direction = 0;
ROM_DATA static float rotation_speed = 1.0f;
ROM_DATA static float approach_speed = 1.0f;
ROM_DATA static unsigned char burst_timer = 0;
ROM_DATA static unsigned char frame_counter = 0;
ROM_DATA static unsigned short second_counter = 0;
ROM_DATA static char timer_text[] = "0.00";
ROM_RODATA_NUM const char music_types[SONG_COUNT] = {
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_EVENT,
	-1,
	-1,
	-1,
	SONGTYPE_MINORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	-1,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_BGM,
	-1,
};

ROM_DATA static unsigned char current_song = 0;
ROM_DATA static char music_init_timer = 2;
#define CENTER_HEX_DIST 20
#define CENTER_HEX_BORDER 2
#define CENTER_HEX_POP_SIZE 7
#define PLAYER_ANGLE_DIFF 10
#define WALL_THICKNESS 10
ROM_DATA static unsigned char hexagon_size = CENTER_HEX_DIST;


void playRandomBGM(void) {
    while (1) {
        int song = getRNGLower31() & 0xFF;
        if (song < SONG_COUNT) {
            if (music_types[song] == SONGTYPE_BGM) {
                int slot = getSongWriteSlot(song);
                if (slot == 0) {
                    playSong(song, 1.0f);
                    current_song = song;
                    return;
                }
            }
        }
    }
}

void cancelCurrentSong(void) {
    cancelMusic(current_song, 1);
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    *dl_ptr = dl;
}

void resetGame(void) {
    summon_timer = 90;
    last_wall = 0;
    wall_element_counter = 0;
    effect_timer = 300;
    rotation_speed = 1.0f;
    approach_speed = 1.0f;
    frame_counter = 0;
    second_counter = 0;
    burst_timer = 0;
    for (int i = 0; i < WALL_BUFFER_COUNT; i++) {
        hex_walls[i].used = 0;
    }
}

void startGame(void) {
    game_state = GAMESTATE_NORMAL;
    playRandomBGM();
    resetGame();
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    resetGame();
    gameInit();
    game_state = GAMESTATE_MUSICCORRECT_INIT;
    // Play song & get music playing
    setBaseSlotVolume(0, 1.0f);
    setBaseSlotVolume(1, 1.0f);
    setBaseSlotVolume(2, 1.0f);
    *(float*)(0x8075DF88) = 0.0f; // Make LZFadeoutProgress insignificant to the output volume
    *dl_ptr = dl;
}

void fixFading(void) {
    *(int*)(0x8075DF88) = 0x3D042108;  // Restore value back to original glory
}

void handleState_musicCorrect_init(void) {
    music_init_timer--;
    if (music_init_timer == 1) {
        preventSongPlaying = 1;
        // playSong(SONG_KROOLTAKEOFF, 1.0f);
        TransitionSpeed = 1.0f;
    } else if (music_init_timer == 0) {
        game_state = GAMESTATE_MUSICCORRECT;
    }
}

void handleState_musicCorrect(void) {
    startGame();
    TransitionSpeed = -1.0f;
}

float angleAdd(float angle0, float angle1) {
    angle0 += angle1;
    while (angle0 < 0.0f) {
        angle0 += 360.0f;
    }
    while (angle0 >= 360.0f) {
        angle0 -= 360.0f;
    }
    return angle0;
}

void getPoint(short *output, float dist, float angle) {
    angle = angleAdd(angle, angle_offset);
    float rad = (angle / 180) * 3.1415926535f;
    output[0] = 160 + (dist * dk_cos(rad));
    output[1] = 140 + (dist * dk_sin(rad));
}

ROM_DATA static short backdrop_coords[48] = {}; // Has to be outside function otherwise you get a memset error
void renderBackdrop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    int angle = 0;
    int color_offset = 0;
    int vtx_offset = 0;
    for (int i = 0; i < 6;i++) {
        for (int j = 0; j < 4; j++) {
            int dist = 1;
            if ((j > 0) && (j < 3)) {
                dist = 300;
            }
            int vtx_angle = angle;
            if (j > 1) {
                if (angle == 300) {
                    vtx_angle = 0;
                } else {
                    vtx_angle = angle + 60;
                }
            }
            getPoint(&backdrop_coords[(vtx_offset + j) << 1], dist, vtx_angle);
        }
        vtx_offset += 4;
        angle += 60;
    }
    for (int i = 0; i < 6; i++) {
        dl = drawTriangleSeries(dl, &background[(int)SelectedDLIndex][i << 2], &backdrop_coords[i << 3],
            hex_colors[COLORSTATE_BACK_0 + color_offset].red,
            hex_colors[COLORSTATE_BACK_0 + color_offset].green,
            hex_colors[COLORSTATE_BACK_0 + color_offset].blue, 4);
        color_offset ^= 1;
    }
    *dl_ptr = dl;
}

void renderCenterHexagon(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    short center_coords[12] = {};
    short border_coords[12] = {};
    int angle = 0;
    for (int i = 0; i < 6;i++) {
        getPoint(&border_coords[i << 1], hexagon_size, angle);
        getPoint(&center_coords[i << 1], hexagon_size - CENTER_HEX_BORDER, angle);
        angle += 60;
    }
    dl = drawTriangleSeries(dl, &center_hex[(int)SelectedDLIndex][0], &border_coords[0],
        hex_colors[COLORSTATE_CENTERHEX_BORDER].red,
        hex_colors[COLORSTATE_CENTERHEX_BORDER].green,
        hex_colors[COLORSTATE_CENTERHEX_BORDER].blue, 6);
    dl = drawTriangleSeries(dl, &center_hex[(int)SelectedDLIndex][6], &center_coords[0],
        hex_colors[COLORSTATE_BACK_0].red,
        hex_colors[COLORSTATE_BACK_0].green,
        hex_colors[COLORSTATE_BACK_0].blue, 6);
    *dl_ptr = dl;
}

void renderPlayer(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    short player_points[6] = {};
    int vtx_angle = -PLAYER_ANGLE_DIFF;
    for (int i = 0; i < 3; i++) {
        int dist = 25;
        if (i == 1) {
            dist += 3;
        }
        getPoint(&player_points[i << 1], dist, angleAdd(player_angle, vtx_angle));
        vtx_angle += PLAYER_ANGLE_DIFF;
    }
    dl = drawTriangleSeries(dl, &player[(int)SelectedDLIndex][0], &player_points[0],
        hex_colors[COLORSTATE_PLAYER].red,
        hex_colors[COLORSTATE_PLAYER].green,
        hex_colors[COLORSTATE_PLAYER].blue, 3);
    *dl_ptr = dl;
}

void hueShiftRGB(rgb *color, int degrees) {
    int r = color->red;
    int g = color->green;
    int b = color->blue;

    int max = r > g ? (r > b ? r : b) : (g > b ? g : b);
    int min = r < g ? (r < b ? r : b) : (g < b ? g : b);
    int delta = max - min;

    int h = 0;
    int s = 0;
    int v = max;

    /* RGB -> HSV */
    if (delta != 0) {
        if (max == r)
            h = 60 * (g - b) / delta;
        else if (max == g)
            h = 120 + 60 * (b - r) / delta;
        else
            h = 240 + 60 * (r - g) / delta;

        if (h < 0)
            h += 360;
    }

    if (max != 0)
        s = (delta * 255) / max;

    /* Hue shift */
    h = (h + degrees) % 360;
    if (h < 0)
        h += 360;

    /* HSV -> RGB */
    int c = (v * s) / 255;
    int x = c * (60 - ((h % 120) - 60 > 0 ? (h % 120) - 60 : 60 - (h % 120))) / 60;
    int m = v - c;

    int rr, gg, bb;

    if (h < 60)       { rr = c; gg = x; bb = 0; }
    else if (h < 120) { rr = x; gg = c; bb = 0; }
    else if (h < 180) { rr = 0; gg = c; bb = x; }
    else if (h < 240) { rr = 0; gg = x; bb = c; }
    else if (h < 300) { rr = x; gg = 0; bb = c; }
    else              { rr = c; gg = 0; bb = x; }

    color->red = rr + m;
    color->green = gg + m;
    color->blue = bb + m;
}

wallStruct *getWallSlot(void) {
    for (int i = 0; i < WALL_BUFFER_COUNT; i++) {
        if (!hex_walls[i].used) {
            return &hex_walls[i];
        }
    }
    return 0;
}

const patternStruct *getRandomPattern(void) {
    int loop_count = getRNGLower31() & 0xF;
    int i = 0;
    while (loop_count >= 0) {
        if (patterns[i].starter) {
            if (loop_count == 0) {
                return &patterns[i];
            }
            loop_count--;
        }
        i++;
        if (i >= PATTERN_COUNT) {
            i = 0;
        }
    }
    return 0;
}

void summonWalls(void) {
    if (summon_timer > 0) {
        summon_timer--;
        return;
    }
    const patternStruct *selected_pattern;
    // if ((last_wall) && (last_wall->elements > wall_element_counter)) {
    //     selected_pattern = &last_wall[wall_element_counter];
    //     wall_element_counter++;
    //     summon_timer = 10;
    // } else {
        selected_pattern = getRandomPattern();
        if (!selected_pattern) {
            return;
        }
        summon_timer = 70;
        int old_rotational_offset = wall_rotational_offset;
        wall_rotational_offset = (getRNGLower31() & 0xFF) % 6;
        if (old_rotational_offset == wall_rotational_offset) {
            if (getRNGLower31() & 0x3) {
                wall_rotational_offset = (wall_rotational_offset + 1) % 6;
            }
        }
        last_wall = (patternStruct *)selected_pattern;
        wall_element_counter = 1;
    // }
    for (int i = 0; i < 6; i++) {
        if (selected_pattern->walls[i]) {
            // Has a wall
            wallStruct *wall_slot = getWallSlot();
            if (!wall_slot) {
                return;
            }
            wall_slot->used = 1;
            wall_slot->wall_index = (wall_rotational_offset + i) % 6;
            wall_slot->dist = 200;
        }
    }
    
}

void renderWalls(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (int i = 0; i < WALL_BUFFER_COUNT; i++) {
        wallStruct *ref_wall = &hex_walls[i];
        if (ref_wall->used) {
            if (game_state == GAMESTATE_NORMAL) {
                ref_wall->dist -= approach_speed;
            }
            if (ref_wall->dist < 10.0f) {
                ref_wall->used = 0;
            } else {
                // Calculate Verts
                short border_coords[8] = {};
                for (int j = 0; j < 4; j++) {
                    int angle = 60 * ref_wall->wall_index;
                    if (j > 1) {
                        if (angle == 300) {
                            angle = 0;
                        } else {
                            angle += 60;
                        }
                    }
                    int dist = ref_wall->dist;
                    if ((j > 0) && (j < 3)) {
                        dist += WALL_THICKNESS;
                    }
                    getPoint(&border_coords[j << 1], dist, angle);
                }
                dl = drawTriangleSeries(dl,
                    &hex_walls_vtx[(int)SelectedDLIndex][(i << 2)],
                    &border_coords[0],
                    hex_colors[COLORSTATE_CENTERHEX_BORDER].red, 
                    hex_colors[COLORSTATE_CENTERHEX_BORDER].green, 
                    hex_colors[COLORSTATE_CENTERHEX_BORDER].blue, 4);
                // Collision Detection
                if (game_state == GAMESTATE_NORMAL) {
                    int player_angle_int = player_angle;
                    int player_wall = player_angle_int / 60;
                    if (ref_wall->dist <= (33)) {
                        if (ref_wall->dist > (30 - WALL_THICKNESS)) {
                            if (player_wall == ref_wall->wall_index) {
                                playSFXWrapper(0x2D4);  // Laugh
                                game_state = GAMESTATE_GAMEOVER;
                                cancelCurrentSong();
                            }
                        }
                    }
                }
            }
        }
    }
    *dl_ptr = dl;
}

void renderTime(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_FILL);
	gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
	gSPClearGeometryMode(dl++, G_ZBUFFER);
	gDPSetFillColor(dl++, 1);
	gDPFillRectangle(dl++, 0, 0, 60, 16);
    float time_val = frame_counter / 60.0f;
    time_val += second_counter;
    dk_strFormat(&timer_text[0], "%.2f", time_val);
    renderText(&dl, 6, 6, 0xFF, 0xFF, 0xFF, 0xFF, timer_text);
    *dl_ptr = dl;
}

void renderBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderBackdrop(&dl);
    renderWalls(&dl);
    if (game_state == GAMESTATE_NORMAL) {
        // Percussion Pop Mechanic
        if (PercussionPlayed) {
            hexagon_size = CENTER_HEX_DIST + CENTER_HEX_POP_SIZE;
            PercussionPlayed = 0;
        }
        if (hexagon_size > CENTER_HEX_DIST) {
            hexagon_size--;
        }
    }
    renderCenterHexagon(&dl);
    renderPlayer(&dl);
    renderTime(&dl);
    *dl_ptr = dl;
}

int canMove(float angle, float delta) {
    float test_angle = angleAdd(angle, delta);
    int new_wall = test_angle / 60.0f;
    for (int i = 0; i < WALL_BUFFER_COUNT; i++) {
        wallStruct *ref_wall = &hex_walls[i];
        if (ref_wall->used && (ref_wall->wall_index == new_wall)) {
            if (ref_wall->dist <= (33)) {
                if (ref_wall->dist > (30 - WALL_THICKNESS)) {
                    return 0;
                }
            }
        }
    }
    return 1;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    float applied_spin = rotation_speed;
    if (p1PressedButtons & B_BUTTON) {
        fixFading();
        gameExit();
    }
    if (burst_timer > 0) {
        burst_timer--;
        if (burst_timer > 6) {
            applied_spin += 6.0f;
        } else if (burst_timer > 84) {
            applied_spin += (90 - burst_timer);
        } else {
            applied_spin += burst_timer;
        }
    }
    if (rotation_direction) {
        applied_spin = -applied_spin;
    }
    angle_offset = angleAdd(angle_offset, applied_spin);
    renderBoard(&dl);
    frame_counter++;
    if (frame_counter >= 60) {
        second_counter++;
        frame_counter = 0;
    }
    summonWalls();
    if (hue_shift_timer > 0) {
        hue_shift_timer--;
        if (hue_shift_timer == 0) {
            hue_shift_timer = 5;
            hueShiftRGB(&hex_colors[COLORSTATE_CENTERHEX_BORDER], 2);
            hex_colors[COLORSTATE_BACK_0].red = hex_colors[COLORSTATE_CENTERHEX_BORDER].red >> 2;
            hex_colors[COLORSTATE_BACK_0].green = hex_colors[COLORSTATE_CENTERHEX_BORDER].green >> 2;
            hex_colors[COLORSTATE_BACK_0].blue = hex_colors[COLORSTATE_CENTERHEX_BORDER].blue >> 2;
            hex_colors[COLORSTATE_BACK_1].red = hex_colors[COLORSTATE_CENTERHEX_BORDER].red >> 1;
            hex_colors[COLORSTATE_BACK_1].green = hex_colors[COLORSTATE_CENTERHEX_BORDER].green >> 1;
            hex_colors[COLORSTATE_BACK_1].blue = hex_colors[COLORSTATE_CENTERHEX_BORDER].blue >> 1;
        }
    }
    if ((MinigameInput->stickX < -0x20) || (MinigameInput->Buttons.d_left)) {
        if (canMove(player_angle, 6.0f)) {
            player_angle = angleAdd(player_angle, 6.0f);
        }
    } else if ((MinigameInput->stickX > 0x20) || (MinigameInput->Buttons.d_right)) {
        if (canMove(player_angle, -6.0f)) {
          player_angle = angleAdd(player_angle, -6.0f);
        }
    }
    if (effect_timer > 0) {
        effect_timer--;
    } else {
        effect_timer = 300;
        int rng = getRNGLower31() & 0xF;
        if (rng > 0xD) {
            approach_speed += 1.0f;
        } else if (rng > 0x5) {
            rotation_direction ^= 1;
        } else if (rng == 0) {
            burst_timer = 90;
            rotation_direction ^= 1;
        } else {
            rotation_speed += 1.0f;
        }
    }
    *dl_ptr = dl;
}

void handleState_gameover(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    angle_offset = angleAdd(angle_offset, 1.0f);
    renderBoard(&dl);
    if (p1PressedButtons & START_BUTTON) {
        startGame();
    }
    *dl_ptr = dl;
}

ROM_DATA static Vp viewport = {
    .vp = {
        .vscale = { 640, 480, 511, 0 }, // Scale (Screen size * 2)
        .vtrans = { 640, 480, 511, 0 }, // Translation (Center of screen)
    }
};

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
   if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 0, 0, 0, 0);
        gSPViewport(dl++, &viewport);
    } 
    switch(game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_MUSICCORRECT_INIT:
            handleState_musicCorrect_init();
            break;
        case GAMESTATE_MUSICCORRECT:
            handleState_musicCorrect();
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_NORMAL:
            handleState_normal(&dl);
            break;
        case GAMESTATE_GAMEOVER:
            handleState_gameover(&dl);
            break;
        default:
            break;
    }
    handleMusic();
    handleMusic2();
    *dl_ptr = dl;
}