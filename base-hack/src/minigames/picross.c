// minigame: picross
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_WIN,
    GAMESTATE_LOSE,
} gameStates;

#define GRID_SIZE 10
#define CELL_SIZE 14
#define MAX_CLUES 5
#define NUM_PUZZLES 6
#define MAX_MISTAKES 5
#define MOVE_DELAY 6
#define END_FRAMES 180

#define CLUE_LEFT_W 60
#define CLUE_TOP_H 66
#define CLUE_STEP_X 11
#define CLUE_STEP_Y 12
#define BOARD_GRID_W (GRID_SIZE * CELL_SIZE)
#define BOARD_GRID_H (GRID_SIZE * CELL_SIZE)
#define GRID_X ((320 - BOARD_GRID_W) / 2)
#define GRID_Y 80
#define BOARD_OFFSET_X (GRID_X - CLUE_LEFT_W)
#define BOARD_OFFSET_Y (GRID_Y - CLUE_TOP_H)

#define CELL_EMPTY 0
#define CELL_FILLED 1
#define CELL_MARKED 2

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static unsigned char cells[GRID_SIZE][GRID_SIZE] = {};
ROM_DATA static unsigned char cursor_x = 0;
ROM_DATA static unsigned char cursor_y = 0;
ROM_DATA static unsigned char mistakes = 0;
ROM_DATA static unsigned short state_timer = 0;
ROM_DATA static unsigned char move_timer = 0;
ROM_DATA static unsigned char row_clues[GRID_SIZE][MAX_CLUES] = {};
ROM_DATA static unsigned char col_clues[GRID_SIZE][MAX_CLUES] = {};

// Each row is a 10-bit mask. Bit (GRID_SIZE - 1 - x) corresponds to column x,
// so the left-most column maps to the highest bit and the literal reads
// left-to-right like the image.
// Try to avoid any row or column being all-filled for now
ROM_DATA static unsigned char selected_puzzle[GRID_SIZE][GRID_SIZE] = {};
void fillRect(Gfx **dl_ptr, int x0, int y0, int x1, int y1, int r, int g, int b) {
    Gfx *dl = *dl_ptr;
    dl = setFillColor(dl, r, g, b);
    gDPSetCycleType(dl++, G_CYC_FILL);
    gDPFillRectangle(dl++, x0, y0, x1, y1);
    *dl_ptr = dl;
}

void generateRandomPuzzle(void) {
    int polarity = getRNGLower31() & 1;
    int ticker = (getRNGLower31() & 7) + 1;
    for (int y = 0; y < GRID_SIZE; y++) {
        for (int x = 0; x < GRID_SIZE; x++) {
            if (ticker == 0) {
                polarity = 1 ^ polarity;
                ticker = (getRNGLower31() & 7) + 1;
            } else {
                ticker--;
            }
            selected_puzzle[x][y] = polarity;
        }
    }
}

int solutionAt(int x, int y) {
    return selected_puzzle[x][y];
}

void computeClues(void) {
    for (int y = 0; y < GRID_SIZE; y++) {
        int idx = 0;
        int run = 0;
        for (int x = 0; x < GRID_SIZE; x++) {
            if (solutionAt(x, y)) {
                run++;
            } else {
                if ((run > 0) && (idx < MAX_CLUES)) {
                    row_clues[y][idx++] = run;
                }
                run = 0;
            }
        }
        if ((run > 0) && (idx < MAX_CLUES)) {
            row_clues[y][idx++] = run;
        }
        while (idx < MAX_CLUES) {
            row_clues[y][idx++] = 0;
        }
    }
    for (int x = 0; x < GRID_SIZE; x++) {
        int idx = 0;
        int run = 0;
        for (int y = 0; y < GRID_SIZE; y++) {
            if (solutionAt(x, y)) {
                run++;
            } else {
                if ((run > 0) && (idx < MAX_CLUES)) {
                    col_clues[x][idx++] = run;
                }
                run = 0;
            }
        }
        if ((run > 0) && (idx < MAX_CLUES)) {
            col_clues[x][idx++] = run;
        }
        while (idx < MAX_CLUES) {
            col_clues[x][idx++] = 0;
        }
    }
}

void resetGame(void) {
    generateRandomPuzzle();
    cursor_x = GRID_SIZE / 2;
    cursor_y = GRID_SIZE / 2;
    mistakes = 0;
    move_timer = 0;
    for (int y = 0; y < GRID_SIZE; y++) {
        for (int x = 0; x < GRID_SIZE; x++) {
            cells[y][x] = CELL_EMPTY;
        }
    }
    computeClues();
}

void checkWin(void) {
    for (int y = 0; y < GRID_SIZE; y++) {
        for (int x = 0; x < GRID_SIZE; x++) {
            int sol = solutionAt(x, y);
            int filled = (cells[y][x] == CELL_FILLED) ? 1 : 0;
            if (sol != filled) {
                return;
            }
        }
    }
    game_state = GAMESTATE_WIN;
    state_timer = END_FRAMES;
    playSFXWrapper(71);
}

void doFill(void) {
    unsigned char *cell = &cells[cursor_y][cursor_x];
    if (*cell == CELL_FILLED) {
        return;
    }
    if (solutionAt(cursor_x, cursor_y)) {
        *cell = CELL_FILLED;
        playSFXWrapper(25);
        checkWin();
    } else {
        *cell = CELL_MARKED;
        mistakes++;
        playSFXWrapper(246);
        if (mistakes >= MAX_MISTAKES) {
            game_state = GAMESTATE_LOSE;
            state_timer = END_FRAMES;
        }
    }
}

void doMark(void) {
    unsigned char *cell = &cells[cursor_y][cursor_x];
    if (*cell == CELL_FILLED) {
        return;
    }
    if (*cell == CELL_MARKED) {
        *cell = CELL_EMPTY;
    } else {
        *cell = CELL_MARKED;
    }
    playSFXWrapper(3);
}

void handleCursor(void) {
    int dx = 0;
    int dy = 0;
    if ((MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right) {
        dx = 1;
    } else if ((MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left) {
        dx = -1;
    }
    if ((MinigameInput->stickY > 0x20) || MinigameInput->Buttons.d_up) {
        dy = -1;
    } else if ((MinigameInput->stickY < -0x20) || MinigameInput->Buttons.d_down) {
        dy = 1;
    }
    if ((dx == 0) && (dy == 0)) {
        move_timer = 0;
        return;
    }
    if (move_timer > 0) {
        move_timer--;
        return;
    }
    cursor_x = (cursor_x + dx + GRID_SIZE) % GRID_SIZE;
    cursor_y = (cursor_y + dy + GRID_SIZE) % GRID_SIZE;
    move_timer = MOVE_DELAY;
}

int isRowSolved(int y) {
    for (int x = 0; x < GRID_SIZE; x++) {
        int sol = solutionAt(x, y);
        int filled = (cells[y][x] == CELL_FILLED) ? 1 : 0;
        if (sol != filled) {
            return 0;
        }
    }
    return 1;
}

int isColSolved(int x) {
    for (int y = 0; y < GRID_SIZE; y++) {
        int sol = solutionAt(x, y);
        int filled = (cells[y][x] == CELL_FILLED) ? 1 : 0;
        if (sol != filled) {
            return 0;
        }
    }
    return 1;
}

void renderGrid(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    fillRect(&dl, GRID_X - 2, GRID_Y - 2,
             GRID_X + BOARD_GRID_W + 2, GRID_Y + BOARD_GRID_H + 2,
             0x80, 0x80, 0x80);
    for (int y = 0; y < GRID_SIZE; y++) {
        for (int x = 0; x < GRID_SIZE; x++) {
            int cx = GRID_X + (x * CELL_SIZE);
            int cy = GRID_Y + (y * CELL_SIZE);
            int state = cells[y][x];
            int r, g, b;
            if (state == CELL_FILLED) {
                r = 0x18; g = 0x18; b = 0x18;
            } else {
                int q = ((x / 5) ^ (y / 5)) & 1;
                if (q) {
                    r = 0xB0; g = 0xB0; b = 0xB0;
                } else {
                    r = 0xD8; g = 0xD8; b = 0xD8;
                }
            }
            fillRect(&dl, cx + 1, cy + 1, cx + CELL_SIZE - 1, cy + CELL_SIZE - 1, r, g, b);
        }
    }
    for (int y = 0; y < GRID_SIZE; y++) {
        for (int x = 0; x < GRID_SIZE; x++) {
            if (cells[y][x] == CELL_MARKED) {
                int cx = GRID_X + (x * CELL_SIZE);
                int cy = GRID_Y + (y * CELL_SIZE);
                renderText(&dl, cx + 3, cy + 2, 0x90, 0x30, 0x30, 0xFF, "X");
            }
        }
    }
    {
        int cx = GRID_X + (cursor_x * CELL_SIZE);
        int cy = GRID_Y + (cursor_y * CELL_SIZE);
        fillRect(&dl, cx - 1, cy - 1, cx + CELL_SIZE + 1, cy + 1, 0xFF, 0xFF, 0x00);
        fillRect(&dl, cx - 1, cy + CELL_SIZE - 1, cx + CELL_SIZE + 1, cy + CELL_SIZE + 1, 0xFF, 0xFF, 0x00);
        fillRect(&dl, cx - 1, cy - 1, cx + 1, cy + CELL_SIZE + 1, 0xFF, 0xFF, 0x00);
        fillRect(&dl, cx + CELL_SIZE - 1, cy - 1, cx + CELL_SIZE + 1, cy + CELL_SIZE + 1, 0xFF, 0xFF, 0x00);
    }
    for (int y = 0; y < GRID_SIZE; y++) {
        int count = 0;
        for (int i = 0; i < MAX_CLUES; i++) {
            if (row_clues[y][i]) {
                count++;
            }
        }
        int solved = isRowSolved(y);
        int cr = solved ? 0x50 : 0xFF;
        int cg = solved ? 0x50 : 0xFF;
        int cb = solved ? 0x50 : 0xFF;
        int ry = GRID_Y + (y * CELL_SIZE) + 3;
        if (count == 0) {
            renderText(&dl, GRID_X - 4 - CLUE_STEP_X, ry, cr, cg, cb, 0xFF, "0");
            continue;
        }
        int group_w = count * CLUE_STEP_X;
        int start_x = GRID_X - 4 - group_w;
        int j = 0;
        for (int i = 0; i < MAX_CLUES; i++) {
            if (row_clues[y][i]) {
                char buf[4];
                dk_strFormat(buf, "%d", row_clues[y][i]);
                renderText(&dl, start_x + (j * CLUE_STEP_X), ry, cr, cg, cb, 0xFF, buf);
                j++;
            }
        }
    }
    for (int x = 0; x < GRID_SIZE; x++) {
        int count = 0;
        for (int i = 0; i < MAX_CLUES; i++) {
            if (col_clues[x][i]) {
                count++;
            }
        }
        int solved = isColSolved(x);
        int cr = solved ? 0x50 : 0xFF;
        int cg = solved ? 0x50 : 0xFF;
        int cb = solved ? 0x50 : 0xFF;
        int rx = GRID_X + (x * CELL_SIZE) + 3;
        if (count == 0) {
            renderText(&dl, rx, GRID_Y - 4 - CLUE_STEP_Y, cr, cg, cb, 0xFF, "0");
            continue;
        }
        int group_h = count * CLUE_STEP_Y;
        int start_y = GRID_Y - 4 - group_h;
        int j = 0;
        for (int i = 0; i < MAX_CLUES; i++) {
            if (col_clues[x][i]) {
                char buf[4];
                dk_strFormat(buf, "%d", col_clues[x][i]);
                renderText(&dl, rx, start_y + (j * CLUE_STEP_Y), cr, cg, cb, 0xFF, buf);
                j++;
            }
        }
    }
    char mistake_text[8];
    dk_strFormat(mistake_text, "X %d:%d", mistakes, MAX_MISTAKES);
    renderText(&dl, 14, 6, 0xFF, 0x80, 0x80, 0xFF, mistake_text);
    *dl_ptr = dl;
}

void handleState_init(Gfx **dl_ptr) {
    game_state = GAMESTATE_TITLE;
    gameInit();
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderText(&dl, 132, 40, 0xFF, 0xFF, 0xFF, 0xFF, "PICROSS");
    renderText(&dl, 76, 76, 0xC0, 0xC0, 0xC0, 0xFF, "REVEAL THE PICTURE");
    renderText(&dl, 100, 108, 0xC0, 0xC0, 0xC0, 0xFF, "A: FILL CELL");
    renderText(&dl, 100, 124, 0xC0, 0xC0, 0xC0, 0xFF, "B: MARK X");
    renderText(&dl, 64, 152, 0xC0, 0x80, 0x80, 0xFF, "FIVE MISTAKES AND YOU LOSE");
    renderText(&dl, 110, 184, 0x80, 0xC0, 0x80, 0xFF, "START-PLAY");
    renderText(&dl, 126, 200, 0x80, 0xC0, 0x80, 0xFF, "B-EXIT");
    if (p1PressedButtons & START_BUTTON) {
        resetGame();
        game_state = GAMESTATE_NORMAL;
    } else if (p1PressedButtons & B_BUTTON) {
        gameExit();
    }
    *dl_ptr = dl;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    handleCursor();
    if (p1PressedButtons & A_BUTTON) {
        doFill();
    }
    if (p1PressedButtons & B_BUTTON) {
        doMark();
    }
    renderGrid(&dl);
    *dl_ptr = dl;
}

void handleState_win(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderGrid(&dl);
    renderText(&dl, 132, 110, 0x00, 0xFF, 0x00, 0xFF, "SOLVED");
    if (state_timer > 0) {
        state_timer--;
    } else {
        gameVictory();
    }
    *dl_ptr = dl;
}

void handleState_lose(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderGrid(&dl);
    renderText(&dl, 124, 110, 0xFF, 0x00, 0x00, 0xFF, "GAME OVER");
    if (state_timer > 0) {
        state_timer--;
    } else {
        game_state = GAMESTATE_TITLE;
    }
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 1, 0x10, 0x14, 0x28);
    }
    switch (game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_NORMAL:
            handleState_normal(&dl);
            break;
        case GAMESTATE_WIN:
            handleState_win(&dl);
            break;
        case GAMESTATE_LOSE:
            handleState_lose(&dl);
            break;
        default:
            break;
    }
    *dl_ptr = dl;
}
