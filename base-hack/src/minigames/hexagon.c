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
ROM_DATA static Vtx timer_backdrop[2][8];
ROM_DATA static Vtx press_start_backdrop[2][8];

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
ROM_DATA static char timer_text[10] = "0.00";
ROM_DATA static char warping_out = 0;
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
typedef struct title_data_struct {
    unsigned char x;
    unsigned char y;
    unsigned char width;
    unsigned char height;
} title_data_struct;
ROM_RODATA_NUM static const title_data_struct title_data[] = {
    { .x=0, .y=4, .width=39, .height=6 },
    { .x=0, .y=10, .width=10, .height=5 },
    { .x=0, .y=15, .width=39, .height=9 },
    { .x=0, .y=30, .width=39, .height=7 },
    { .x=0, .y=37, .width=38, .height=1 },
    { .x=0, .y=38, .width=37, .height=1 },
    { .x=0, .y=44, .width=23, .height=2 },
    { .x=0, .y=46, .width=24, .height=4 },
    { .x=0, .y=50, .width=6, .height=13 },
    { .x=0, .y=63, .width=24, .height=4 },
    { .x=0, .y=67, .width=23, .height=1 },
    { .x=1, .y=2, .width=38, .height=2 },
    { .x=2, .y=1, .width=37, .height=1 },
    { .x=2, .y=68, .width=20, .height=1 },
    { .x=4, .y=0, .width=35, .height=1 },
    { .x=18, .y=50, .width=6, .height=13 },
    { .x=29, .y=29, .width=10, .height=1 },
    { .x=27, .y=45, .width=23, .height=1 },
    { .x=27, .y=46, .width=24, .height=4 },
    { .x=27, .y=50, .width=6, .height=13 },
    { .x=27, .y=63, .width=24, .height=4 },
    { .x=27, .y=67, .width=23, .height=1 },
    { .x=28, .y=44, .width=22, .height=1 },
    { .x=28, .y=68, .width=21, .height=1 },
    { .x=29, .y=24, .width=10, .height=1 },
    { .x=30, .y=25, .width=9, .height=4 },
    { .x=44, .y=0, .width=9, .height=29 },
    { .x=44, .y=29, .width=10, .height=1 },
    { .x=44, .y=30, .width=38, .height=7 },
    { .x=44, .y=62, .width=7, .height=1 },
    { .x=45, .y=37, .width=37, .height=1 },
    { .x=45, .y=50, .width=6, .height=12 },
    { .x=46, .y=38, .width=36, .height=1 },
    { .x=54, .y=44, .width=22, .height=1 },
    { .x=54, .y=45, .width=23, .height=1 },
    { .x=54, .y=46, .width=24, .height=4 },
    { .x=54, .y=50, .width=6, .height=19 },
    { .x=72, .y=29, .width=10, .height=1 },
    { .x=72, .y=50, .width=6, .height=19 },
    { .x=73, .y=0, .width=9, .height=29 },
    { .x=81, .y=44, .width=6, .height=9 },
    { .x=81, .y=53, .width=24, .height=1 },
    { .x=81, .y=54, .width=23, .height=2 },
    { .x=81, .y=56, .width=21, .height=1 },
    { .x=81, .y=57, .width=23, .height=2 },
    { .x=81, .y=59, .width=6, .height=9 },
    { .x=81, .y=68, .width=5, .height=1 },
    { .x=87, .y=0, .width=38, .height=10 },
    { .x=87, .y=10, .width=9, .height=10 },
    { .x=87, .y=20, .width=38, .height=7 },
    { .x=87, .y=27, .width=37, .height=1 },
    { .x=87, .y=28, .width=36, .height=1 },
    { .x=87, .y=29, .width=9, .height=10 },
    { .x=98, .y=59, .width=6, .height=1 },
    { .x=99, .y=44, .width=6, .height=9 },
    { .x=99, .y=60, .width=6, .height=8 },
    { .x=99, .y=68, .width=5, .height=1 },
    { .x=108, .y=45, .width=24, .height=5 },
    { .x=108, .y=50, .width=5, .height=3 },
    { .x=108, .y=53, .width=24, .height=6 },
    { .x=108, .y=59, .width=6, .height=1 },
    { .x=108, .y=60, .width=5, .height=2 },
    { .x=108, .y=62, .width=6, .height=1 },
    { .x=108, .y=63, .width=24, .height=5 },
    { .x=109, .y=44, .width=23, .height=1 },
    { .x=109, .y=68, .width=23, .height=1 },
    { .x=115, .y=19, .width=10, .height=1 },
    { .x=116, .y=10, .width=9, .height=9 },
    { .x=130, .y=0, .width=38, .height=10 },
    { .x=130, .y=10, .width=9, .height=5 },
    { .x=130, .y=15, .width=38, .height=9 },
    { .x=130, .y=24, .width=10, .height=1 },
    { .x=130, .y=25, .width=9, .height=4 },
    { .x=130, .y=29, .width=10, .height=1 },
    { .x=130, .y=30, .width=38, .height=7 },
    { .x=131, .y=37, .width=37, .height=1 },
    { .x=132, .y=38, .width=36, .height=1 },
    { .x=135, .y=44, .width=6, .height=9 },
    { .x=135, .y=53, .width=24, .height=5 },
    { .x=136, .y=58, .width=22, .height=1 },
    { .x=143, .y=59, .width=7, .height=1 },
    { .x=144, .y=60, .width=6, .height=9 },
    { .x=153, .y=44, .width=6, .height=9 },
    { .x=162, .y=45, .width=24, .height=5 },
    { .x=162, .y=50, .width=6, .height=13 },
    { .x=162, .y=63, .width=24, .height=5 },
    { .x=163, .y=44, .width=23, .height=1 },
    { .x=164, .y=68, .width=22, .height=1 },
    { .x=173, .y=0, .width=36, .height=1 },
    { .x=173, .y=1, .width=37, .height=1 },
    { .x=173, .y=2, .width=38, .height=1 },
    { .x=173, .y=3, .width=39, .height=7 },
    { .x=173, .y=10, .width=9, .height=10 },
    { .x=173, .y=20, .width=39, .height=1 },
    { .x=173, .y=21, .width=38, .height=2 },
    { .x=173, .y=23, .width=37, .height=1 },
    { .x=173, .y=24, .width=35, .height=1 },
    { .x=173, .y=25, .width=36, .height=1 },
    { .x=173, .y=26, .width=38, .height=2 },
    { .x=173, .y=28, .width=39, .height=1 },
    { .x=173, .y=29, .width=9, .height=10 },
    { .x=179, .y=62, .width=7, .height=1 },
    { .x=180, .y=53, .width=5, .height=1 },
    { .x=180, .y=54, .width=6, .height=8 },
    { .x=189, .y=45, .width=23, .height=1 },
    { .x=189, .y=46, .width=24, .height=4 },
    { .x=189, .y=50, .width=6, .height=13 },
    { .x=189, .y=63, .width=24, .height=4 },
    { .x=189, .y=67, .width=23, .height=1 },
    { .x=190, .y=44, .width=22, .height=1 },
    { .x=190, .y=68, .width=21, .height=1 },
    { .x=200, .y=19, .width=12, .height=1 },
    { .x=202, .y=10, .width=10, .height=9 },
    { .x=202, .y=29, .width=10, .height=10 },
    { .x=206, .y=62, .width=7, .height=1 },
    { .x=207, .y=50, .width=6, .height=12 },
    { .x=216, .y=44, .width=22, .height=1 },
    { .x=216, .y=45, .width=23, .height=1 },
    { .x=216, .y=46, .width=24, .height=4 },
    { .x=216, .y=50, .width=6, .height=19 },
    { .x=234, .y=50, .width=6, .height=18 },
};
ROM_DATA static char duration_notifier[] = "LAST 30 SECONDS TO WIN";
ROM_DATA static char win_duration = 30;

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
    output[1] = 120 + (dist * dk_sin(rad));
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
#define TIMER_BACKDROP_WIDTH 60
#define TIMER_BACKDROP_HEIGHT 20
#define TIMER_BACKDROP_BORDER 5
#define TIMER_BACKDROP_INSET 10

#define PRESS_START_X_OFFSET 80
#define PRESS_START_Y_OFFSET 190
#define PRESS_START_HEIGHT 30

// Parallelogram helper functions
#define _PARA_HYPOT(h, slant) \
    __builtin_sqrtf(((float)(slant) * (slant)) + ((float)(h) * (h)))
#define _PARA_EXACT_INSET(h, slant, border) \
    (((float)(border) * _PARA_HYPOT(h, slant)) / (h))
    
#define GENERATE_PARALLELOGRAM_COORDS(x, y, w, h, slant, border) { \
    /* --- Outer Parallelogram (Clockwise) --- */ \
    (short)(x),                               (short)(y),               /* 0: Top-Left     */ \
    (short)((x) + (w)),                       (short)(y),               /* 1: Top-Right    */ \
    (short)((x) + (w) - (slant)),             (short)((y) + (h)),       /* 2: Bottom-Right */ \
    (short)((x) - (slant)),                   (short)((y) + (h)),       /* 3: Bottom-Left  */ \
                                                                                                  \
    /* --- Inner Parallelogram (Clockwise) --- */ \
    (short)((x) + _PARA_EXACT_INSET(h, slant, border)), \
    (short)((y) + (border)),                                            /* 4: Inner Top-Left     */ \
                                                                                                  \
    (short)((x) + (w) - _PARA_EXACT_INSET(h, slant, border)), \
    (short)((y) + (border)),                                            /* 5: Inner Top-Right    */ \
                                                                                                  \
    (short)((x) + (w) - (slant) - _PARA_EXACT_INSET(h, slant, border)), \
    (short)((y) + (h) - (border)),                                      /* 6: Inner Bottom-Right */ \
                                                                                                  \
    (short)((x) - (slant) + _PARA_EXACT_INSET(h, slant, border)), \
    (short)((y) + (h) - (border))                                       /* 7: Inner Bottom-Left  */ \
}

ROM_RODATA_NUM static const short timer_backdrop_coords[] = {
    0, 0,
    TIMER_BACKDROP_WIDTH + TIMER_BACKDROP_BORDER, 0,
    (TIMER_BACKDROP_WIDTH - TIMER_BACKDROP_INSET) + 2, TIMER_BACKDROP_HEIGHT + TIMER_BACKDROP_BORDER,
    0, TIMER_BACKDROP_HEIGHT + TIMER_BACKDROP_BORDER,
    0, 0,
    TIMER_BACKDROP_WIDTH, 0,
    TIMER_BACKDROP_WIDTH - TIMER_BACKDROP_INSET, TIMER_BACKDROP_HEIGHT,
    0, TIMER_BACKDROP_HEIGHT,
};

ROM_RODATA_NUM static const short press_start_coords[] = GENERATE_PARALLELOGRAM_COORDS(
    PRESS_START_X_OFFSET,
    PRESS_START_Y_OFFSET,
    320 - (2 * PRESS_START_X_OFFSET),
    PRESS_START_HEIGHT,
    TIMER_BACKDROP_INSET,
    TIMER_BACKDROP_BORDER
);

void renderParallelogram(Gfx **dl_ptr, Vtx *backdrop, short *coords) {
    Gfx *dl = *dl_ptr;
    dl = drawTriangleSeries(dl,
        &backdrop[0],
        (short*)&coords[0], 
        hex_colors[COLORSTATE_BACK_1].red + hex_colors[COLORSTATE_BACK_0].red, 
        hex_colors[COLORSTATE_BACK_1].green + hex_colors[COLORSTATE_BACK_0].green, 
        hex_colors[COLORSTATE_BACK_1].blue + hex_colors[COLORSTATE_BACK_0].blue, 4);
    dl = drawTriangleSeries(dl,
        &backdrop[4],
        (short*)&coords[8], 
        hex_colors[COLORSTATE_BACK_0].red, 
        hex_colors[COLORSTATE_BACK_0].green, 
        hex_colors[COLORSTATE_BACK_0].blue, 4);
    *dl_ptr = dl;
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderBackdrop(&dl);
    renderParallelogram(&dl, &press_start_backdrop[(int)SelectedDLIndex][0], (short*)&press_start_coords[0]);
    renderText(&dl, 110, 200, 255, 255, 255, 255, "PRESS START");
    dk_strFormat(duration_notifier, "LAST %d SECONDS TO WIN", win_duration);
    for (int i = 0; i < 2; i++) {
        int color = (0x100 - i) & 0xFF;
        int shift = 2 - (i << 1);
        renderText(&dl, 60 + shift, 135 + shift, color, color, color, 255, "LEFT OR RIGHT: MOVE PLAYER");
        renderText(&dl, 100 + shift, 150 + shift, color, color, color, 255, "AVOID THE WALLS");
        renderText(&dl, 75 + shift, 165 + shift, color, color, color, 255, duration_notifier);
    }

    angle_offset = angleAdd(angle_offset, 1.0f);
    if (!warping_out) {
        if (p1PressedButtons & START_BUTTON) {
            startGame();
        } else if (p1PressedButtons & B_BUTTON) {
            gameExit();
            warping_out = 1;
        }
    }
    gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_FILL);
	gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
	gSPClearGeometryMode(dl++, G_ZBUFFER);
    dl = setFillColor(dl, 0x00, 0x00, 0x00);
    for (unsigned int i = 0; i < sizeof(title_data)/sizeof(title_data_struct); i++) {
        int x0 = 42 + title_data[i].x;
        int y0 = 42 + title_data[i].y;
        gDPFillRectangle(dl++, x0, y0, x0 + title_data[i].width, y0 + title_data[i].height);
    }
    dl = setFillColor(dl, 0xFF, 0xFF, 0xFF);
    for (unsigned int i = 0; i < sizeof(title_data)/sizeof(title_data_struct); i++) {
        int x0 = 40 + title_data[i].x;
        int y0 = 40 + title_data[i].y;
        gDPFillRectangle(dl++, x0, y0, x0 + title_data[i].width, y0 + title_data[i].height);
    }
    *dl_ptr = dl;
}

typedef struct map_duration_struct {
    unsigned char map;
    unsigned char duration;
} map_duration_struct;

ROM_RODATA_NUM static const map_duration_struct map_durations[] = {
    { .map = MAP_DKARCADE, .duration = 45 },
    { .map = MAP_JETPAC, .duration = 45 },
    { .map = MAP_ARCADE25M_ONLY, .duration = 25 },
    { .map = MAP_ARCADE50M_ONLY, .duration = 30 },
    { .map = MAP_ARCADE75M_ONLY, .duration = 35 },
    { .map = MAP_ARCADE100M_ONLY, .duration = 40 },
    { .map = MAP_JETPAC_ROCKET, .duration = 30 },
};

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    resetGame();
    gameInit();
    for (int i = 0; i < 7; i++) {
        if (CurrentMap == map_durations[i].map) {
            win_duration = map_durations[i].duration;
        }
    }
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
    game_state = GAMESTATE_TITLE;
    TransitionSpeed = -1.0f;
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
            if ((game_state == GAMESTATE_NORMAL) && (!warping_out)) {
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
                if ((game_state == GAMESTATE_NORMAL) && (!warping_out)) {
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
    float time_val = frame_counter / 60.0f;
    time_val += second_counter;
    dl = drawTriangleSeries(dl,
        &timer_backdrop[(int)SelectedDLIndex][0],
        (short*)&timer_backdrop_coords[0], 
        hex_colors[COLORSTATE_BACK_1].red + hex_colors[COLORSTATE_BACK_0].red, 
        hex_colors[COLORSTATE_BACK_1].green + hex_colors[COLORSTATE_BACK_0].green, 
        hex_colors[COLORSTATE_BACK_1].blue + hex_colors[COLORSTATE_BACK_0].blue, 4);
    dl = drawTriangleSeries(dl,
        &timer_backdrop[(int)SelectedDLIndex][4],
        (short*)&timer_backdrop_coords[8], 
        hex_colors[COLORSTATE_BACK_0].red, 
        hex_colors[COLORSTATE_BACK_0].green, 
        hex_colors[COLORSTATE_BACK_0].blue, 4);
    dk_strFormat(&timer_text[0], "%.2f", time_val);
    if (!warping_out) {
        if (time_val > win_duration) {
            if (game_state == GAMESTATE_NORMAL) {
                playSFXWrapper(71);
                gameVictory();
                warping_out = 1;
            }
        }
    }
    renderText(&dl, 6, 8, 0xFF, 0xFF, 0xFF, 0xFF, timer_text);
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
        if (canMove(player_angle, -6.0f)) {
            player_angle = angleAdd(player_angle, -6.0f);
        }
    } else if ((MinigameInput->stickX > 0x20) || (MinigameInput->Buttons.d_right)) {
        if (canMove(player_angle, 6.0f)) {
          player_angle = angleAdd(player_angle, 6.0f);
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

ROM_DATA static Mtx ortho_mtx;
ROM_DATA static Mtx identity_mtx_model;
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
        // Build ortho matrix once: maps (0,0)-(320,240) to screen
        guOrtho(&ortho_mtx, 0.0f, 320.0f, 240.0f, 0.0f, -1.0f, 1.0f, 1.0f);
        guMtxIdent(&identity_mtx_model);
        gSPViewport(dl++, &viewport);
        // Force ortho projection regardless of what D_1000090/D_1000040 set up
        gSPMatrix(dl++, &ortho_mtx,
            G_MTX_PROJECTION | G_MTX_LOAD | G_MTX_NOPUSH);
        gSPMatrix(dl++, &identity_mtx_model,
            G_MTX_MODELVIEW | G_MTX_LOAD | G_MTX_NOPUSH);
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