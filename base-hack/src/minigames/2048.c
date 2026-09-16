// minigame: 2048
// 2048 — slide tiles, merge equal pairs, reach the 2048 tile to win.
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_PLAY,
    GAMESTATE_WIN,
    GAMESTATE_LOSE,
} gameStates;

#define GRID_N 4
// Win target is set based on current map
//   main arcade/jetpac slot  -> 512 (log 9)
//   bonus barrel sub-maps    -> 128 (log 7)
#define WIN_LOG_MAIN 9
#define WIN_LOG_BONUS 7
#define TILE_SIZE 36
#define TILE_GAP 4
#define BOARD_W (GRID_N * TILE_SIZE + (GRID_N + 1) * TILE_GAP)
#define BOARD_X ((320 - BOARD_W) / 2)
#define BOARD_Y 50
#define END_FRAMES 240
#define ANIM_FRAMES 8

#define DIR_UP 0
#define DIR_RIGHT 1
#define DIR_DOWN 2
#define DIR_LEFT 3

// One source tile sliding to a destination cell. After a merge, two
// source tiles record the same dst.
typedef struct {
    signed char src_r;
    signed char src_c;
    signed char dst_r;
    signed char dst_c;
    unsigned char val;  // value of the sliding tile (pre-merge)
} Movement;

#define MAX_MOVEMENTS (GRID_N * GRID_N)

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
// grid[r][c] = log2 of tile value (0 = empty, 1 = 2, 2 = 4, ..., 11 = 2048)
ROM_DATA static unsigned char grid[GRID_N][GRID_N] = {};
ROM_DATA static unsigned int score = 0;
ROM_DATA static unsigned char highest = 0;
ROM_DATA static unsigned char last_dir_held = 0;
ROM_DATA static unsigned char won_flag = 0;
ROM_DATA static unsigned short state_timer = 0;
ROM_DATA static char buf[16];

ROM_DATA static Movement movements[MAX_MOVEMENTS];
ROM_DATA static unsigned char movement_count = 0;
ROM_DATA static unsigned char animating = 0;
ROM_DATA static unsigned char anim_frame = 0;
ROM_DATA static unsigned char win_log = WIN_LOG_MAIN;
ROM_RODATA_NUM static const rgb tile_colors[] = {
    {0x3D, 0x39, 0x32},  // 0  empty slot
    {0xEE, 0xE4, 0xDA},  // 1  -> 2
    {0xED, 0xE0, 0xC8},  // 2  -> 4
    {0xF2, 0xB1, 0x79},  // 3  -> 8
    {0xF5, 0x95, 0x63},  // 4  -> 16
    {0xF6, 0x7C, 0x5F},  // 5  -> 32
    {0xF6, 0x5E, 0x3B},  // 6  -> 64
    {0xED, 0xCF, 0x72},  // 7  -> 128 (Bonus Barrel win)
    {0xED, 0xCC, 0x61},  // 8  -> 256
    {0xED, 0xC8, 0x50},  // 9  -> 512 (Jetpac/Arcade win)
};
#define NUM_TILE_COLORS ((int)(sizeof(tile_colors) / sizeof(tile_colors[0])))

void fillRect(Gfx **dl_ptr, int x0, int y0, int x1, int y1, int r, int g, int b) {
    Gfx *dl = *dl_ptr;
    dl = setFillColor(dl, r, g, b);
    gDPSetCycleType(dl++, G_CYC_FILL);
    gDPFillRectangle(dl++, x0, y0, x1, y1);
    *dl_ptr = dl;
}

int countDigits(int n) {
    int d = 1;
    while (n >= 10) {
        n /= 10;
        d++;
    }
    return d;
}

int cellPxX(int c) {
    return BOARD_X + TILE_GAP + c * (TILE_SIZE + TILE_GAP);
}
int cellPxY(int r) {
    return BOARD_Y + TILE_GAP + r * (TILE_SIZE + TILE_GAP);
}

int isBonusMap(void) {
    return (CurrentMap == MAP_ARCADE25M_ONLY)
        || (CurrentMap == MAP_ARCADE50M_ONLY)
        || (CurrentMap == MAP_ARCADE75M_ONLY)
        || (CurrentMap == MAP_ARCADE100M_ONLY)
        || (CurrentMap == MAP_JETPAC_ROCKET);
}

void spawnTile(void) {
    int empties[GRID_N * GRID_N];
    int count = 0;
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N; c++) {
            if (grid[r][c] == 0) {
                empties[count++] = r * GRID_N + c;
            }
        }
    }
    if (count == 0) return;
    int idx = empties[((getRNGLower31() >> 4) & 0xFF) % count];
    int r = idx / GRID_N;
    int c = idx % GRID_N;
    unsigned char v = ((getRNGLower31() & 0xF) < 14) ? 1 : 2;
    grid[r][c] = v;
}

void resetGame(void) {
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N; c++) {
            grid[r][c] = 0;
        }
    }
    score = 0;
    highest = 0;
    won_flag = 0;
    last_dir_held = 0;
    movement_count = 0;
    animating = 0;
    anim_frame = 0;
    win_log = isBonusMap() ? WIN_LOG_BONUS : WIN_LOG_MAIN;
    spawnTile();
    spawnTile();
}

// Slide a 4-tile line toward index 0
int slideLine(unsigned char *line, signed char *dst_per_src) {
    unsigned char vals[GRID_N];
    signed char srcs[GRID_N];
    for (int i = 0; i < GRID_N; i++) dst_per_src[i] = -1;
    int idx = 0;
    for (int i = 0; i < GRID_N; i++) {
        if (line[i] != 0) {
            vals[idx] = line[i];
            srcs[idx] = i;
            idx++;
        }
    }
    unsigned char result[GRID_N];
    for (int i = 0; i < GRID_N; i++) result[i] = 0;
    int ridx = 0;
    int i = 0;
    while (i < idx) {
        if (((i + 1) < idx) && (vals[i] == vals[i + 1])) {
            unsigned char merged = vals[i] + 1;
            result[ridx] = merged;
            dst_per_src[srcs[i]] = ridx;
            dst_per_src[srcs[i + 1]] = ridx;
            score += (1u << merged);
            if (merged > highest) highest = merged;
            if (merged >= win_log) won_flag = 1;
            ridx++;
            i += 2;
        } else {
            result[ridx] = vals[i];
            dst_per_src[srcs[i]] = ridx;
            ridx++;
            i += 1;
        }
    }
    int changed = 0;
    for (int j = 0; j < GRID_N; j++) {
        if (line[j] != result[j]) changed = 1;
        line[j] = result[j];
    }
    return changed;
}

void recordMovement(int src_r, int src_c, int dst_r, int dst_c, unsigned char val) {
    if (movement_count >= MAX_MOVEMENTS) return;
    Movement *m = &movements[movement_count++];
    m->src_r = src_r;
    m->src_c = src_c;
    m->dst_r = dst_r;
    m->dst_c = dst_c;
    m->val = val;
}

int doMove(int dir) {
    int changed = 0;
    movement_count = 0;
    if (dir == DIR_LEFT) {
        for (int r = 0; r < GRID_N; r++) {
            unsigned char prev[GRID_N];
            for (int i = 0; i < GRID_N; i++) prev[i] = grid[r][i];
            signed char dst[GRID_N];
            changed |= slideLine(grid[r], dst);
            for (int c = 0; c < GRID_N; c++) {
                if (dst[c] >= 0) recordMovement(r, c, r, dst[c], prev[c]);
            }
        }
    } else if (dir == DIR_RIGHT) {
        for (int r = 0; r < GRID_N; r++) {
            unsigned char rev[GRID_N];
            for (int i = 0; i < GRID_N; i++) rev[i] = grid[r][GRID_N - 1 - i];
            unsigned char prev[GRID_N];
            for (int i = 0; i < GRID_N; i++) prev[i] = rev[i];
            signed char dst[GRID_N];
            int ch = slideLine(rev, dst);
            for (int i = 0; i < GRID_N; i++) grid[r][GRID_N - 1 - i] = rev[i];
            changed |= ch;
            for (int i = 0; i < GRID_N; i++) {
                if (dst[i] >= 0) {
                    recordMovement(r, GRID_N - 1 - i, r, GRID_N - 1 - dst[i], prev[i]);
                }
            }
        }
    } else if (dir == DIR_UP) {
        for (int c = 0; c < GRID_N; c++) {
            unsigned char col[GRID_N];
            for (int i = 0; i < GRID_N; i++) col[i] = grid[i][c];
            unsigned char prev[GRID_N];
            for (int i = 0; i < GRID_N; i++) prev[i] = col[i];
            signed char dst[GRID_N];
            int ch = slideLine(col, dst);
            for (int i = 0; i < GRID_N; i++) grid[i][c] = col[i];
            changed |= ch;
            for (int i = 0; i < GRID_N; i++) {
                if (dst[i] >= 0) recordMovement(i, c, dst[i], c, prev[i]);
            }
        }
    } else {
        for (int c = 0; c < GRID_N; c++) {
            unsigned char col[GRID_N];
            for (int i = 0; i < GRID_N; i++) col[i] = grid[GRID_N - 1 - i][c];
            unsigned char prev[GRID_N];
            for (int i = 0; i < GRID_N; i++) prev[i] = col[i];
            signed char dst[GRID_N];
            int ch = slideLine(col, dst);
            for (int i = 0; i < GRID_N; i++) grid[GRID_N - 1 - i][c] = col[i];
            changed |= ch;
            for (int i = 0; i < GRID_N; i++) {
                if (dst[i] >= 0) {
                    recordMovement(GRID_N - 1 - i, c, GRID_N - 1 - dst[i], c, prev[i]);
                }
            }
        }
    }
    return changed;
}

int hasValidMoves(void) {
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N; c++) {
            if (grid[r][c] == 0) return 1;
        }
    }
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N - 1; c++) {
            if (grid[r][c] == grid[r][c + 1]) return 1;
        }
    }
    for (int r = 0; r < GRID_N - 1; r++) {
        for (int c = 0; c < GRID_N; c++) {
            if (grid[r][c] == grid[r + 1][c]) return 1;
        }
    }
    return 0;
}

void renderTile(Gfx **dl_ptr, int x, int y, int log_val) {
    Gfx *dl = *dl_ptr;
    int idx = log_val;
    if (idx >= NUM_TILE_COLORS) idx = NUM_TILE_COLORS - 1;
    const rgb *c = &tile_colors[idx];
    fillRect(&dl, x, y, x + TILE_SIZE, y + TILE_SIZE, c->red, c->green, c->blue);
    if (log_val > 0) {
        int val = 1 << log_val;
        char buf2[8];
        dk_strFormat(buf2, "%d", val);
        int digits = countDigits(val);
        int text_x = x + (TILE_SIZE - digits * 8) / 2;
        int text_y = y + (TILE_SIZE - 14) / 2;
        int dark = (log_val <= 2);
        int tr = dark ? 0x77 : 0xF9;
        int tg = dark ? 0x6E : 0xF6;
        int tb = dark ? 0x65 : 0xF2;
        renderText(&dl, text_x, text_y, tr, tg, tb, 0xFF, buf2);
    }
    *dl_ptr = dl;
}

void renderHUD(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    dk_strFormat(buf, "SCORE %d", score);
    renderText(&dl, 14, 16, 0xFF, 0xFF, 0xFF, 0xFF, buf);
    if (highest > 0) {
        int best_val = 1 << highest;
        dk_strFormat(buf, "BEST %d", best_val);
        renderText(&dl, 210, 16, 0xFF, 0xFF, 0xFF, 0xFF, buf);
    }
    *dl_ptr = dl;
}

void renderSlots(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    fillRect(&dl, BOARD_X, BOARD_Y, BOARD_X + BOARD_W, BOARD_Y + BOARD_W, 0xBB, 0xAD, 0xA0);
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N; c++) {
            renderTile(&dl, cellPxX(c), cellPxY(r), 0);
        }
    }
    *dl_ptr = dl;
}

void renderBoardStatic(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderSlots(&dl);
    for (int r = 0; r < GRID_N; r++) {
        for (int c = 0; c < GRID_N; c++) {
            if (grid[r][c] > 0) {
                renderTile(&dl, cellPxX(c), cellPxY(r), grid[r][c]);
            }
        }
    }
    renderHUD(&dl);
    *dl_ptr = dl;
}

void renderBoardAnimating(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderSlots(&dl);
    for (int i = 0; i < movement_count; i++) {
        Movement *m = &movements[i];
        int sx = cellPxX(m->src_c);
        int sy = cellPxY(m->src_r);
        int dx = cellPxX(m->dst_c);
        int dy = cellPxY(m->dst_r);
        int x = sx + ((dx - sx) * anim_frame) / ANIM_FRAMES;
        int y = sy + ((dy - sy) * anim_frame) / ANIM_FRAMES;
        renderTile(&dl, x, y, m->val);
    }
    renderHUD(&dl);
    *dl_ptr = dl;
}

void handleState_init(Gfx **dl_ptr) {
    game_state = GAMESTATE_TITLE;
    gameInit();
}

void renderLogoTile(Gfx **dl_ptr, int x, int y, int size,
                    int br, int bgc, int bb,
                    int tr, int tg, int tb,
                    const char *digit) {
    Gfx *dl = *dl_ptr;
    fillRect(&dl, x, y, x + size, y + size, br, bgc, bb);
    int text_x = x + (size - 8) / 2;
    int text_y = y + (size - 14) / 2;
    renderText(&dl, text_x, text_y, tr, tg, tb, 0xFF, digit);
    *dl_ptr = dl;
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    const int tt = 36;
    const int gap = 6;
    int total_w = 4 * tt + 3 * gap;
    int sx = (320 - total_w) / 2;
    int sy = 24;
    // "2": tile-2 beige with dark text
    renderLogoTile(&dl, sx + 0 * (tt + gap), sy, tt, 0xEE, 0xE4, 0xDA, 0x77, 0x6E, 0x65, "2");
    // "0": dark slate with light text
    renderLogoTile(&dl, sx + 1 * (tt + gap), sy, tt, 0x77, 0x6E, 0x65, 0xF9, 0xF6, 0xF2, "0");
    // "4": tile-4 darker beige with dark text
    renderLogoTile(&dl, sx + 2 * (tt + gap), sy, tt, 0xED, 0xE0, 0xC8, 0x77, 0x6E, 0x65, "4");
    // "8": tile-8 orange with light text
    renderLogoTile(&dl, sx + 3 * (tt + gap), sy, tt, 0xF2, 0xB1, 0x79, 0xF9, 0xF6, 0xF2, "8");

    // Goal — gold-accented to match the higher tiles.
    int target = isBonusMap() ? (1 << WIN_LOG_BONUS) : (1 << WIN_LOG_MAIN);
    char goal_buf[24];
    dk_strFormat(goal_buf, "REACH %d TO WIN", target);
    renderText(&dl, 92, 80, 0xED, 0xC8, 0x50, 0xFF, goal_buf);

    // Subtle divider between header and instructions.
    fillRect(&dl, 60, 100, 260, 102, 0x40, 0x3C, 0x36);

    // Instructions
    renderText(&dl, 60, 114, 0xD0, 0xCA, 0xC0, 0xFF, "STICK OR DPAD TO SLIDE");
    renderText(&dl, 54, 132, 0xD0, 0xCA, 0xC0, 0xFF, "MERGE EQUAL TILES TO GROW");
    renderText(&dl, 62, 150, 0xD0, 0xCA, 0xC0, 0xFF, "EACH MOVE ADDS A TILE");

    // Prompts at the bottom — green for go, soft red for back.
    renderText(&dl, 96, 192, 0x80, 0xFF, 0x80, 0xFF, "START - PLAY");
    renderText(&dl, 128, 212, 0xFF, 0xA0, 0xA0, 0xFF, "B - EXIT");

    if (p1PressedButtons & START_BUTTON) {
        resetGame();
        game_state = GAMESTATE_PLAY;
    } else if (p1PressedButtons & B_BUTTON) {
        gameExit();
    }
    *dl_ptr = dl;
}

void handleState_play(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;

    if (animating) {
        anim_frame++;
        if (anim_frame > ANIM_FRAMES) {
            animating = 0;
            spawnTile();
            if (won_flag) {
                game_state = GAMESTATE_WIN;
                state_timer = END_FRAMES;
                playSFXWrapper(71);
            } else if (!hasValidMoves()) {
                game_state = GAMESTATE_LOSE;
                state_timer = END_FRAMES;
                playSFXWrapper(246);
            }
            renderBoardStatic(&dl);
        } else {
            renderBoardAnimating(&dl);
        }
        *dl_ptr = dl;
        return;
    }

    unsigned char now = 0;
    if ((MinigameInput->stickY > 0x20) || MinigameInput->Buttons.d_up) now |= (1 << DIR_UP);
    if ((MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right) now |= (1 << DIR_RIGHT);
    if ((MinigameInput->stickY < -0x20) || MinigameInput->Buttons.d_down) now |= (1 << DIR_DOWN);
    if ((MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left) now |= (1 << DIR_LEFT);
    unsigned char just = now & ~last_dir_held;
    last_dir_held = now;

    int dir = -1;
    if (just & (1 << DIR_UP)) dir = DIR_UP;
    else if (just & (1 << DIR_RIGHT)) dir = DIR_RIGHT;
    else if (just & (1 << DIR_DOWN)) dir = DIR_DOWN;
    else if (just & (1 << DIR_LEFT)) dir = DIR_LEFT;

    if (dir >= 0) {
        int changed = doMove(dir);
        if (changed) {
            playSFXWrapper(25);
            animating = 1;
            anim_frame = 0;
            // Render the first animation frame immediately
            renderBoardAnimating(&dl);
            *dl_ptr = dl;
            return;
        }
    }

    renderBoardStatic(&dl);
    *dl_ptr = dl;
}

void handleState_win(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderBoardStatic(&dl);
    fillRect(&dl, 80, 100, 240, 144, 0x10, 0x10, 0x18);
    renderText(&dl, 122, 116, 0x00, 0xFF, 0x00, 0xFF, "YOU WIN");
    if (state_timer > 0) {
        state_timer--;
    } else {
        gameVictory();
    }
    *dl_ptr = dl;
}

void handleState_lose(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderBoardStatic(&dl);
    fillRect(&dl, 80, 100, 240, 144, 0x10, 0x10, 0x18);
    renderText(&dl, 120, 116, 0xFF, 0x00, 0x00, 0xFF, "GAME OVER");
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
        dl = minigame_dl_init(dl, 1, 0x20, 0x1E, 0x28);
    }
    switch (game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_PLAY:
            handleState_play(&dl);
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
