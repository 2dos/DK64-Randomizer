// minigame: flappy_bird
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_GAMEOVER
} gameStates;

#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 240
#define BIRD_X 60
#define BIRD_SIZE 8
#define GRAVITY 0.25f
#define JUMP_STRENGTH -3.0f
#define PIPE_WIDTH 30
#define PIPE_GAP 70
#define PIPE_SPEED 1.25f
#define MAX_PIPES 3

typedef struct {
    float x;
    float gap_y;
    unsigned char passed;
} Pipe;

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static float bird_y = 120.0f;
ROM_DATA static float bird_vy = 0.0f;
ROM_DATA static Pipe pipes[MAX_PIPES];
ROM_DATA static int score = 0;
ROM_DATA static char score_text[8];

#define COLOR_BLACK 0
#define COLOR_WHITE 0xFF

typedef struct NumberGraphicStruct {
    unsigned char x;
    unsigned char y;
    unsigned char width;
    unsigned char height;
    unsigned char color;
} NumberGraphicStruct;

typedef struct NumberDisplayStruct {
    unsigned char width;
    unsigned char graphic_count;
    const NumberGraphicStruct *graphics;
} NumberDisplayStruct;

ROM_RODATA_NUM static const NumberGraphicStruct number_0[] = {
    { .x = 0, .y = 0, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 8, .height = 13, .color = COLOR_WHITE },
    { .x = 4, .y = 4, .width = 1, .height = 7, .color = COLOR_BLACK },
};

ROM_RODATA_NUM static const NumberGraphicStruct number_1[] = {
    { .x = 0, .y = 0, .width = 7, .height = 5, .color = COLOR_BLACK },
    { .x = 2, .y = 1, .width = 5, .height = 14, .color = COLOR_BLACK },
    { .x = 3, .y = 1, .width = 5, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 5, .height = 3, .color = COLOR_WHITE },
    { .x = 3, .y = 4, .width = 3, .height = 10, .color = COLOR_WHITE },
};

ROM_RODATA_NUM static const NumberGraphicStruct number_2[] = {
    { .x = 0, .y = 0, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 8, .height = 13, .color = COLOR_WHITE },
    { .x = 1, .y = 4, .width = 4, .height = 1, .color = COLOR_BLACK },
    { .x = 5, .y = 9, .width = 4, .height = 1, .color = COLOR_BLACK },
};

ROM_RODATA_NUM static const NumberGraphicStruct number_3[] = {
    { .x = 0, .y = 0, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 10, .height = 15, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 8, .height = 13, .color = COLOR_WHITE },
    { .x = 1, .y = 5, .width = 4, .height = 1, .color = COLOR_BLACK },
    { .x = 1, .y = 9, .width = 4, .height = 1, .color = COLOR_BLACK },
};

ROM_RODATA_NUM static const NumberGraphicStruct number_4[] = {
    { .x = 0, .y = 0, .width = 10, .height = 10, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 10, .height = 10, .color = COLOR_BLACK },
    { .x = 3, .y = 10, .width = 8, .height = 5, .color = COLOR_BLACK },
    { .x = 4, .y = 11, .width = 7, .height = 5, .color = COLOR_BLACK },
    { .x = 1, .y = 1, .width = 8, .height = 8, .color = COLOR_WHITE },
    { .x = 5, .y = 9, .width = 4, .height = 5, .color = COLOR_WHITE },
    { .x = 4, .y = 1, .width = 1, .height = 4, .color = COLOR_BLACK },
};

ROM_RODATA_NUM static const NumberDisplayStruct number_displays[] = {
    { .width = 16, .graphic_count = 4, .graphics = &number_0[0], },
    { .width = 16, .graphic_count = 5, .graphics = &number_1[0], },
    { .width = 16, .graphic_count = 5, .graphics = &number_2[0], },
    { .width = 16, .graphic_count = 5, .graphics = &number_3[0], },
    { .width = 16, .graphic_count = 7, .graphics = &number_4[0], },
};

void resetGame(void) {
    bird_y = 100.0f;
    bird_vy = 0.0f;
    score = 0;
    for (int i = 0; i < MAX_PIPES; i++) {
        // Stagger pipes horizontally across and off the screen
        pipes[i].x = SCREEN_WIDTH + (i * 120);
        pipes[i].gap_y = 40 + (getRNGLower31() % 110);
        pipes[i].passed = 0;
    }
}

Gfx *drawRectHelper(Gfx *dl, int x0, int y0, int x1, int y1, int red, int green, int blue) {
    if (x1 <= 0 || y1 <= 0) {
        return dl;
    }
    if (x0 >= SCREEN_WIDTH || y0 >= SCREEN_HEIGHT) {
        return dl;
    }
    if (x0 < 0) x0 = 0;
    if (y0 < 0) y0 = 0;
    if (x1 > SCREEN_WIDTH)  x1 = SCREEN_WIDTH;
    if (y1 > SCREEN_HEIGHT) y1 = SCREEN_HEIGHT;

    if (x1 <= x0 || y1 <= y0) {
        return dl;
    }

    // Safe to send to the RDP
    dl = setFillColor(dl, red, green, blue);
    gDPFillRectangle(dl++, x0, y0, x1, y1);
    
    return dl;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;

    // 1. Physics Engine & Input Tracking
    bird_vy += GRAVITY;
    bird_y += bird_vy;

    if (p1PressedButtons & A_BUTTON) {
        bird_vy = JUMP_STRENGTH;
        playSFXWrapper(3); // Flap audio feedback
    }

    // 2. Obstacle Logic & Precise Collision Check
    for (int i = 0; i < MAX_PIPES; i++) {
        pipes[i].x -= PIPE_SPEED;

        // Recycle pipe to the right edge once it scrolls entirely off-screen
        if (pipes[i].x < -PIPE_WIDTH - 4) { 
            pipes[i].x = SCREEN_WIDTH;
            pipes[i].gap_y = 40 + (getRNGLower31() % 110);
            pipes[i].passed = 0;
        }

        // Score progression check
        if (!pipes[i].passed && pipes[i].x < BIRD_X) {
            score++;
            pipes[i].passed = 1;
            playSFXWrapper(71); // Score point ding
        }

        // AABB Collision Check against the pipe structures
        if (BIRD_X + BIRD_SIZE > pipes[i].x && BIRD_X < pipes[i].x + PIPE_WIDTH) {
            if (bird_y < pipes[i].gap_y || bird_y + BIRD_SIZE > pipes[i].gap_y + PIPE_GAP) {
                game_state = GAMESTATE_GAMEOVER;
                playSFXWrapper(246); // Impact crash sound
                return;
            }
        }
    }

    // Out of bounds screen boundary collision
    if (bird_y > SCREEN_HEIGHT - 10 || bird_y < 0) {
        game_state = GAMESTATE_GAMEOVER;
        playSFXWrapper(246);
        return;
    }

    // 3. Rendering Multi-Quad Pipes (Pseudo-3D Art Style)
    for (int i = 0; i < MAX_PIPES; i++) {
        int px = (int)pipes[i].x;
        int py = (int)pipes[i].gap_y;
        
        int rim_height = 12;
        int rim_outset = 4; // Width expansion for the rim lip
        
        // --- TOP OPAQUE PIPE ---
        // Main structural core
        dl = drawRectHelper(dl, px, 0, px + PIPE_WIDTH, py - rim_height, 34, 139, 34);
        
        // Left side highlight strip
        dl = drawRectHelper(dl, px + 2, 0, px + 6, py - rim_height, 144, 238, 144);
        
        // Right side ambient shadow strip
        dl = drawRectHelper(dl, px + PIPE_WIDTH - 6, 0, px + PIPE_WIDTH, py - rim_height, 0, 100, 0);
        
        // Top Pipe Flanged Lip
        dl = drawRectHelper(dl, px - rim_outset, py - rim_height, px + PIPE_WIDTH + rim_outset, py, 34, 139, 34);
        
        // Top Pipe Flanged Lip Accents
        dl = drawRectHelper(dl, px - rim_outset + 2, py - rim_height, px - rim_outset + 6, py, 144, 238, 144);
        dl = drawRectHelper(dl, px + PIPE_WIDTH + rim_outset - 6, py - rim_height, px + PIPE_WIDTH + rim_outset, py, 0, 100, 0);

        // --- BOTTOM OPAQUE PIPE ---
        // Main structural core
        dl = drawRectHelper(dl, px, py + PIPE_GAP + rim_height, px + PIPE_WIDTH, SCREEN_HEIGHT, 34, 139, 34);
        
        // Left side highlight strip
        dl = drawRectHelper(dl, px + 2, py + PIPE_GAP + rim_height, px + 6, SCREEN_HEIGHT, 144, 238, 144);
        
        // Right side ambient shadow strip
        dl = drawRectHelper(dl, px + PIPE_WIDTH - 6, py + PIPE_GAP + rim_height, px + PIPE_WIDTH, SCREEN_HEIGHT, 0, 100, 0);
        
        // Bottom Pipe Flanged Lip
        dl = drawRectHelper(dl, px - rim_outset, py + PIPE_GAP, px + PIPE_WIDTH + rim_outset, py + PIPE_GAP + rim_height, 34, 139, 34);
        
        // Bottom Pipe Flanged Lip Accents
        dl = drawRectHelper(dl, px - rim_outset + 2, py + PIPE_GAP, px - rim_outset + 6, py + PIPE_GAP + rim_height, 144, 238, 144);
        dl = drawRectHelper(dl, px + PIPE_WIDTH + rim_outset - 6, py + PIPE_GAP, px + PIPE_WIDTH + rim_outset, py + PIPE_GAP + rim_height, 0, 100, 0);
    }

    // 4. Render Dynamic Elements (Player & HUD)
    // Draw Bird Actor
    dl = setFillColor(dl, 255, 255, 0); // Yellow
    gDPFillRectangle(dl++, BIRD_X, (int)bird_y, BIRD_X + BIRD_SIZE, (int)bird_y + BIRD_SIZE);

    // Render Text HUD Score
    dk_strFormat(score_text, "%d", score);
    renderText(&dl, 155, 20, 255, 255, 255, 255, score_text);

    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    
    // Clear and draw background using solid Sky Blue Fill
    dl = minigame_dl_init(dl, 1, 135, 206, 235);

    switch(game_state) {
        case GAMESTATE_INIT:
            gameInit();
            game_state = GAMESTATE_TITLE;
            break;

        case GAMESTATE_TITLE:
            renderText(&dl, 110, 100, 255, 255, 255, 255, "F L A P P Y\0");
            renderText(&dl, 100, 130, 0, 0, 0, 255, "PRESS START\0");
            if (p1PressedButtons & START_BUTTON) {
                resetGame();
                game_state = GAMESTATE_NORMAL;
            }
            break;

        case GAMESTATE_NORMAL:
            handleState_normal(&dl);
            break;

        case GAMESTATE_GAMEOVER:
            // Display game over screen overlay over the last scene frame
            renderText(&dl, 120, 110, 255, 0, 0, 255, "GAME OVER\0");
            if (p1PressedButtons & START_BUTTON) {
                game_state = GAMESTATE_TITLE;
            }
            break;
    }
    *dl_ptr = dl;
}