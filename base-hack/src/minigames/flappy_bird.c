// minigame: flappy_bird
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_DEAD,
} gameStates;

typedef enum guessStates {
    GUESSSTATE_UNGUESSED,
    GUESSSTATE_INCORRECT,
    GUESSSTATE_WRONGSPOT,
    GUESSSTATE_CORRECT,
} guessStates;

/*
    Note: Incomplete. Bugged collision logic
*/

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
#define BIRD_X 80
ROM_RODATA_NUM static const char flappy_bird_0[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/flappy_up.png", "RGBA5551");
ROM_RODATA_NUM static const char flappy_bird_1[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/flappy_mid.png", "RGBA5551");
ROM_RODATA_NUM static const char flappy_bird_2[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/flappy_down.png", "RGBA5551");
ROM_RODATA_NUM static const char flappy_bird_dead[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/flappy_dead.png", "RGBA5551");
ROM_RODATA_NUM static const char pipe_sprite[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/pipe.png", "IA8");
ROM_RODATA_NUM static const char pipe_sprite_invert[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/pipe_vertical.png", "IA8");

#define FLAPPY_FRAMERATE 10
ROM_DATA static char flappy_frame = 0;
ROM_DATA static char flappy_subframe = FLAPPY_FRAMERATE;
ROM_DATA static float bird_y = 80;
ROM_DATA static float bird_yvel = 0.0f;
ROM_DATA static float bird_yacc = 0.1f;
ROM_DATA static char bird_dead_timer = 0;

typedef struct PipeStruct {
    unsigned char render;
    short x;
    short y_upper;
    short y_lower;
} PipeStruct;
ROM_DATA static PipeStruct pipes[4] = {};
#define PIPE_GAP 120
#define PIPE_WIDTH 30
ROM_DATA static unsigned char spawn_pipe_timer = PIPE_GAP;

void resetGame(void) {
    bird_y = 80.0f;
    bird_yvel = 0.0f;
    flappy_frame = 0;
    flappy_subframe = FLAPPY_FRAMERATE;
    for (int i = 0; i < 4; i++) {
        pipes[i].render = 0;
    }
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    resetGame();
    game_state = GAMESTATE_NORMAL;
    *dl_ptr = dl;
}

int getPipeSpawnIndex(void) {
    for (int i = 0; i < 4; i++) {
        if (!pipes[i].render) {
            return i;
        }
    }
    return -1;
}

void spawnPipe(void) {
    int spawn_index = getPipeSpawnIndex();
    int rng = getRNGLower31();
    PipeStruct *pipe = &pipes[spawn_index];
    pipe->y_lower = (((rng >> 4) & 0xFFF) % 100) + 140;
    pipe->y_upper = (pipe->y_lower - 80) - (rng & 0xF);
    pipe->render = 1;
    pipe->x = 320;
}

void renderPipe(Gfx **dl_ptr, PipeStruct *pipe) {
    Gfx *dl = *dl_ptr;
	gDPSetPrimColor(dl++, 0, 0, 0, 0xFF, 0, 0xFF);
    dl = displayImageCustom(dl, &pipe_sprite_invert, 3, IA8, 32, 128, pipe->x, pipe->y_upper - 128, 4.0f, 4.0f, 0, 0.0f);
    dl = displayImageCustom(dl, &pipe_sprite, 3, IA8, 32, 128, pipe->x, pipe->y_lower, 4.0f, 4.0f, 0, 0.0f);
    *dl_ptr = dl;
}

void handlePipe(Gfx **dl_ptr, PipeStruct *pipe) {
    if (game_state == GAMESTATE_NORMAL) {
        pipe->x -= 1;
    }
    Gfx *dl = *dl_ptr;
    renderPipe(&dl, pipe);
    *dl_ptr = dl;
    if (pipe->x < -PIPE_WIDTH) {
        pipe->render = 0;
        return;
    }
    if (game_state == GAMESTATE_NORMAL) {
        if ((pipe->x >= BIRD_X) && (pipe->x < (BIRD_X + PIPE_WIDTH))) {
            // Collision code
            int ref_y = bird_y + 128;
            if ((ref_y < pipe->y_upper) || (ref_y > pipe->y_lower)) {
                game_state = GAMESTATE_DEAD;
                bird_yvel = -2.0f;
                bird_dead_timer = 120;
            }
        }
    }
}

void birdCode(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    // Behavior Code
    if (p1PressedButtons & A_BUTTON) {
        bird_yvel = -2.0f;
    }
    bird_y += bird_yvel;
    if (bird_y < 0.0f) {
        bird_y = 0.0f;
    }
    if (bird_y > 240.0f) {
        bird_y = 240.0f;
    }
    bird_yvel += bird_yacc;
    if (bird_yvel > 2.0f) {
        bird_yvel = 2.0f;
    }
    // Animation Code
    if (flappy_subframe > 0) {
        flappy_subframe--;
    } else {
        flappy_subframe = FLAPPY_FRAMERATE;
        flappy_frame++;
        if (flappy_frame == 4) {
            flappy_frame = 0;
        }
    }
    // Render Bird
    dl = initDisplayList(dl);
	gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
	gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
	gDPSetCombineLERP(
        dl++,
        TEXEL0, 0, PRIMITIVE, 0,   // RGB = TEXEL0 * PRIMITIVE
        TEXEL0, 0, PRIMITIVE, 0,   // Alpha = TEXEL0 * PRIMITIVE
        TEXEL0, 0, PRIMITIVE, 0,
        TEXEL0, 0, PRIMITIVE, 0
    );
	gDPSetTextureFilter(dl++, G_TF_POINT);
    const void *tex = &flappy_bird_1;
    if (flappy_frame == 0) {
        tex = &flappy_bird_0;
    } else if (flappy_frame == 2) {
        tex = &flappy_bird_2;
    }
    if (game_state == GAMESTATE_DEAD) {
        tex = &flappy_bird_dead;
    }
    dl = displayImageCustom(dl, tex, 0, RGBA16, 44, 44, BIRD_X, bird_y, 2.0f, 2.0f, 0, 0.0f);
    //
    *dl_ptr = dl;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    birdCode(&dl);
    if (game_state == GAMESTATE_DEAD) {
        if (bird_dead_timer > 0) {
            bird_dead_timer--;
            if (bird_dead_timer == 0) {
                game_state = GAMESTATE_INIT;
            }
        }
    }
    if (spawn_pipe_timer > 0) {
        spawn_pipe_timer--;
        if (spawn_pipe_timer == 0) {
            spawn_pipe_timer = PIPE_GAP;
            spawnPipe();
        }
    }
    for (int i = 0; i < 4; i++) {
        PipeStruct *pipe = &pipes[i];
        if (pipe->render) {
            handlePipe(&dl, pipe);
        }
    }
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    switch(game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_NORMAL:
        case GAMESTATE_DEAD:
            handleState_normal(&dl);
            break;
        default:
            break;
    }
    *dl_ptr = dl;
}