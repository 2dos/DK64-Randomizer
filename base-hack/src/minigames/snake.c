// minigame: snake
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_GAMEOVER,
    GAMESTATE_WIN,
} gameStates;

typedef enum colorState {
    COLORSTATE_BORDER,
    COLORSTATE_EMPTY,
    COLORSTATE_SNAKE_HEAD,
    COLORSTATE_SNAKE_BODY,
    COLORSTATE_FOOD,
    COLORSTATE_TEXT,
} colorState;

typedef struct SnakeTile {
    unsigned char type; // 0: empty, 1: snake, 2: food
    int body_lifetime;  // How many frames this stays "snake"
} SnakeTile;

#define GRID_DIM_X 15
#define GRID_DIM_Y 11
#define INITIAL_LENGTH 3
#define TICK_RATE 6 

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static SnakeTile board[GRID_DIM_X][GRID_DIM_Y] = {0};
ROM_DATA static int head_x, head_y;
ROM_DATA static int dir_x, dir_y;
ROM_DATA static int next_dir_x, next_dir_y;
ROM_DATA static int snake_length;
ROM_DATA static unsigned char move_timer = 0;
ROM_DATA static unsigned int score = 0;
ROM_DATA static char score_text[8] = "000";

ROM_RODATA_NUM static const rgb game_colors[] = {
    { .red = 0x40, .green = 0x40, .blue = 0x40 }, // BORDER
    { .red = 0x20, .green = 0x20, .blue = 0x20 }, // EMPTY
    { .red = 0x00, .green = 0xFF, .blue = 0x00 }, // HEAD
    { .red = 0x00, .green = 0x80, .blue = 0x00 }, // BODY
    { .red = 0xFF, .green = 0x00, .blue = 0x00 }, // FOOD
    { .red = 0xFF, .green = 0xFF, .blue = 0xFF }, // TEXT
};

void spawnFood(void) {
    while (1) {
        int x = (getRNGLower31() % GRID_DIM_X);
        int y = (getRNGLower31() % GRID_DIM_Y);
        if (board[x][y].type == 0) {
            board[x][y].type = 2;
            return;
        }
    }
}

void resetSnake(void) {
    for (int x = 0; x < GRID_DIM_X; x++) {
        for (int y = 0; y < GRID_DIM_Y; y++) {
            board[x][y].type = 0;
            board[x][y].body_lifetime = 0;
        }
    }
    head_x = GRID_DIM_X / 2;
    head_y = GRID_DIM_Y / 2;
    dir_x = 1; dir_y = 0;
    next_dir_x = 1; next_dir_y = 0;
    snake_length = INITIAL_LENGTH;
    score = 0;
    move_timer = 0;
    spawnFood();
}

void handleInput(void) {
    if ((MinigameInput->stickX < -0x20 || MinigameInput->Buttons.d_left) && dir_x == 0) {
        next_dir_x = -1; next_dir_y = 0;
    } else if ((MinigameInput->stickX > 0x20 || MinigameInput->Buttons.d_right) && dir_x == 0) {
        next_dir_x = 1; next_dir_y = 0;
    } else if ((MinigameInput->stickY > 0x20 || MinigameInput->Buttons.d_up) && dir_y == 0) {
        next_dir_x = 0; next_dir_y = -1;
    } else if ((MinigameInput->stickY < -0x20 || MinigameInput->Buttons.d_down) && dir_y == 0) {
        next_dir_x = 0; next_dir_y = 1;
    }
}

void updateSnake(void) {
    move_timer++;
    if (move_timer < TICK_RATE) return;
    move_timer = 0;

    dir_x = next_dir_x;
    dir_y = next_dir_y;

    int next_x = head_x + dir_x;
    int next_y = head_y + dir_y;

    // SCREEN WRAPPING LOGIC
    if (next_x < 0) next_x = GRID_DIM_X - 1;
    else if (next_x >= GRID_DIM_X) next_x = 0;
    
    if (next_y < 0) next_y = GRID_DIM_Y - 1;
    else if (next_y >= GRID_DIM_Y) next_y = 0;

    // Body Collision (Game Over only happens if hitting self now)
    if (board[next_x][next_y].type == 1) {
        game_state = GAMESTATE_GAMEOVER;
        playSFXWrapper(0x150);
        return;
    }

    // Check Food
    if (board[next_x][next_y].type == 2) {
        snake_length++;
        score += 10;
        playSFXWrapper(686);
        spawnFood();
    }

    // Move Head
    head_x = next_x;
    head_y = next_y;
    board[head_x][head_y].type = 1;
    board[head_x][head_y].body_lifetime = snake_length;

    // Decay Body
    for (int x = 0; x < GRID_DIM_X; x++) {
        for (int y = 0; y < GRID_DIM_Y; y++) {
            if (board[x][y].type == 1) {
                board[x][y].body_lifetime--;
                if (board[x][y].body_lifetime <= 0) {
                    board[x][y].type = 0;
                }
            }
        }
    }
}

#define BOX_DIM 16 // Reduced slightly to fit 15 tiles wide
#define X_START (160 - ((GRID_DIM_X * BOX_DIM) / 2))
#define Y_START (120 - ((GRID_DIM_Y * BOX_DIM) / 2))

void renderSnakeBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    
    // Draw Background/Border
    dl = setFillColor(dl, game_colors[0].red, game_colors[0].green, game_colors[0].blue);
    gDPFillRectangle(dl++, X_START - 2, Y_START - 2, X_START + (GRID_DIM_X * BOX_DIM) + 2, Y_START + (GRID_DIM_Y * BOX_DIM) + 2);

    for (int x = 0; x < GRID_DIM_X; x++) {
        for (int y = 0; y < GRID_DIM_Y; y++) {
            int x0 = X_START + (x * BOX_DIM);
            int y0 = Y_START + (y * BOX_DIM);
            
            int color_idx = COLORSTATE_EMPTY;
            if (board[x][y].type == 2) color_idx = COLORSTATE_FOOD;
            else if (x == head_x && y == head_y) color_idx = COLORSTATE_SNAKE_HEAD;
            else if (board[x][y].type == 1) color_idx = COLORSTATE_SNAKE_BODY;

            const rgb *c = &game_colors[color_idx];
            dl = setFillColor(dl, c->red, c->green, c->blue);
            gDPFillRectangle(dl++, x0 + 1, y0 + 1, x0 + BOX_DIM - 1, y0 + BOX_DIM - 1);
        }
    }

    dk_strFormat(score_text, "%03d", score);
    renderText(&dl, X_START, Y_START - 15, 255, 255, 255, 255, score_text);
    
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 1, 0x00, 0x00, 0x00);
    }

    switch(game_state) {
        case GAMESTATE_INIT:
            gameInit();
            game_state = GAMESTATE_TITLE;
            break;
        case GAMESTATE_TITLE:
            renderText(&dl, 110, 100, 0, 255, 0, 255, "SNAKE");
            renderText(&dl, 90, 140, 255, 255, 255, 255, "PRESS START");
            if (p1PressedButtons & START_BUTTON) {
                resetSnake();
                game_state = GAMESTATE_NORMAL;
            }
            break;
        case GAMESTATE_NORMAL:
            handleInput();
            updateSnake();
            renderSnakeBoard(&dl);
            break;
        case GAMESTATE_GAMEOVER:
            renderSnakeBoard(&dl);
            renderText(&dl, 110, 110, 255, 0, 0, 255, "GAME OVER");
            if (p1PressedButtons & START_BUTTON) game_state = GAMESTATE_TITLE;
        default:
            break;
    }
    *dl_ptr = dl;
}