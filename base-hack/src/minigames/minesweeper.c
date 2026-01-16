// minigame: minesweeper
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_MINE,
    GAMESTATE_WIN,
} gameStates;

typedef enum colorState {
    COLORSTATE_BORDER,
    COLORSTATE_SQUARE,
    COLORSTATE_MINE,
    COLORSTATE_SELECTBORDER,
    COLORSTATE_NUM1,
    COLORSTATE_NUM2,
    COLORSTATE_NUM3,
    COLORSTATE_NUM4,
    COLORSTATE_NUM5,
    COLORSTATE_NUM6,
    COLORSTATE_NUM7,
    COLORSTATE_NUM8,
    COLORSTATE_DIGGEDBORDER,
} colorState;

typedef struct TileStruct {
    unsigned char has_mine;
    unsigned char uncovered;
    unsigned char adjacent_mines;
    unsigned char calculated;
    unsigned char flagged;
    char text[2];
} TileStruct;

#define GRID_DIMENSIONS 9
#define MINES 10
ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static TileStruct tiles[GRID_DIMENSIONS][GRID_DIMENSIONS] = {};
ROM_DATA static unsigned char guess_count = 0;
ROM_DATA static int selected_x = 0;
ROM_DATA static int selected_y = 0;
ROM_DATA static char change_slot = 0;
ROM_DATA static char digging = 0;
ROM_DATA static char flagging = 0;
ROM_DATA static unsigned char ending_timer = 0;
ROM_RODATA_NUM static const rgb game_colors[] = {
    { .red = 0x80, .green = 0x80, .blue = 0x80 }, // COLORSTATE_BORDER,
    { .red = 0xC0, .green = 0xC0, .blue = 0xC0 }, // COLORSTATE_SQUARE,
    { .red = 0xFF, .green = 0x00, .blue = 0x00 }, // COLORSTATE_MINE,
    { .red = 0x00, .green = 0x80, .blue = 0x80 }, // COLORSTATE_SELECTBORDER,
    { .red = 0x00, .green = 0x00, .blue = 0xFF }, // COLORSTATE_NUM1,
    { .red = 0x00, .green = 0x80, .blue = 0x00 }, // COLORSTATE_NUM2,
    { .red = 0xFF, .green = 0x00, .blue = 0x00 }, // COLORSTATE_NUM3,
    { .red = 0x00, .green = 0x00, .blue = 0x80 }, // COLORSTATE_NUM4,
    { .red = 0x80, .green = 0x00, .blue = 0x00 }, // COLORSTATE_NUM5,
    { .red = 0x00, .green = 0x80, .blue = 0x80 }, // COLORSTATE_NUM6,
    { .red = 0x00, .green = 0x00, .blue = 0x00 }, // COLORSTATE_NUM7,
    { .red = 0x80, .green = 0x80, .blue = 0x80 }, // COLORSTATE_NUM8,
    { .red = 0xDB, .green = 0xDB, .blue = 0xDB }, // COLORSTATE_DIGGEDBORDER,
};
ROM_RODATA_NUM static const char title_text[] = "M\0I\0N\0E\0S\0W\0E\0E\0P\0E\0R\0";
ROM_RODATA_NUM static const char title_subtext[] = "P\0R\0E\0S\0S\0 \0S\0T\0A\0R\0T\0";
ROM_DATA static unsigned char frame_timer = 0;
ROM_DATA static unsigned short second_timer = 0;
ROM_DATA static char timer_text[4] = "000";
ROM_DATA static char mine_text[4] = "000";

Gfx *setFillColor(Gfx *dl, int red, int green, int blue) {
    gDPSetFillColor(dl++, (((red >> 3) & 0x1F) << 11) | (((green >> 3) & 0x1F) << 6) | (((blue >> 3) & 0x1F) << 1) | 1);
    return dl;
}

void placeMine(void) {
    while (1) {
        int x = ((getRNGLower31() >> 10) & 0xFF) % GRID_DIMENSIONS;
        int y = ((getRNGLower31() >> 10) & 0xFF) % GRID_DIMENSIONS;
        if (!tiles[x][y].has_mine) {
            tiles[x][y].has_mine = 1;
            return;
        }
    }
}

void resetGame(void) {
    for (int x = 0; x < GRID_DIMENSIONS; x++) {
        for (int y = 0; y < GRID_DIMENSIONS; y++) {
            TileStruct *tile = &tiles[x][y];
            tile->has_mine = 0;
            tile->uncovered = 0;
            tile->adjacent_mines = 0;
            tile->calculated = 0;
            tile->flagged = 0;
        }
    }
    guess_count = 0;
    frame_timer = 0;
    second_timer = 0;
}

int isTileMine(int x, int y) {
    if ((x < 0) || (y < 0)) {
        return 0;
    }
    if ((x >= GRID_DIMENSIONS) || (y >= GRID_DIMENSIONS)) {
        return 0;
    }
    return tiles[x][y].has_mine;
}

void calculateNumber(int x, int y, TileStruct *tile) {
    int mines = 0;
    // Corner mines first
    mines += isTileMine(x - 1, y - 1);
    mines += isTileMine(x - 1, y + 1);
    mines += isTileMine(x + 1, y + 1);
    mines += isTileMine(x + 1, y - 1);
    // Edge Mines
    mines += isTileMine(x - 1, y);
    mines += isTileMine(x + 1, y);
    mines += isTileMine(x, y - 1);
    mines += isTileMine(x, y + 1);
    tile->calculated = 1;
    tile->adjacent_mines = mines;
    if (mines == 0) {
        tile->text[0] = 0;
    } else {
        tile->text[0] = '0' + mines;
    }
}

void calculateGrid(void) {
    for (int x = 0; x < GRID_DIMENSIONS; x++) {
        for (int y = 0; y < GRID_DIMENSIONS; y++) {
            calculateNumber(x, y, &tiles[x][y]);
        }
    }
}

void generateBoard(void) {
    for (int i = 0; i < MINES; i++) {
        placeMine();
    }
    calculateGrid();
}

void digCellZeroCheck(int x, int y, int skip_zero_mines) {
    if ((x < 0) || (y < 0)) {
        return;
    }
    if ((x >= GRID_DIMENSIONS) || (y >= GRID_DIMENSIONS)) {
        return;
    }
    if (tiles[x][y].adjacent_mines != 0) {
        if (skip_zero_mines) {
            skip_zero_mines = 0;
        } else {
            return;
        }
    }
    if (tiles[x][y].has_mine) {
        return;
    }
    if (tiles[x][y].uncovered) {
        return;
    }
    tiles[x][y].uncovered = 1;
    digCellZeroCheck(x - 1, y - 1, skip_zero_mines);
    digCellZeroCheck(x - 1, y, skip_zero_mines);
    digCellZeroCheck(x - 1, y + 1, skip_zero_mines);
    digCellZeroCheck(x + 1, y - 1, skip_zero_mines);
    digCellZeroCheck(x + 1, y, skip_zero_mines);
    digCellZeroCheck(x + 1, y + 1, skip_zero_mines);
    digCellZeroCheck(x, y - 1, skip_zero_mines);
    digCellZeroCheck(x, y + 1, skip_zero_mines);
}

int victoryCheck(void) {
    for (int x = 0; x < GRID_DIMENSIONS; x++) {
        for (int y = 0; y < GRID_DIMENSIONS; y++) {
            TileStruct *tile = &tiles[x][y];
            if (!tile->uncovered && !tile->has_mine) {
                return 0;
            }
        }
    }
    return 1;
}

void checkWin(void) {
    if (victoryCheck()) {
        game_state = GAMESTATE_WIN;
        playSFXWrapper(71);
        ending_timer = 180;
    }
}

void digCell(void) {
    TileStruct *tile = &tiles[selected_x][selected_y];
    if (tile->uncovered) {
        return;
    }
    if ((guess_count == 0) && tile->has_mine) {
        placeMine(); // Place this mine somewhere else to prevent a first-cell death
        tile->has_mine = 0;
        calculateGrid();
    }
    guess_count++;
    tile->uncovered = 1;
    if (tile->has_mine) {
        game_state = GAMESTATE_MINE;
        ending_timer = 120;
        playSFXWrapper(246);
    } else {
        if (tile->adjacent_mines == 0) {
            digCellZeroCheck(selected_x - 1, selected_y - 1, 1);
            digCellZeroCheck(selected_x - 1, selected_y, 1);
            digCellZeroCheck(selected_x - 1, selected_y + 1, 1);
            digCellZeroCheck(selected_x + 1, selected_y - 1, 1);
            digCellZeroCheck(selected_x + 1, selected_y, 1);
            digCellZeroCheck(selected_x + 1, selected_y + 1, 1);
            digCellZeroCheck(selected_x, selected_y - 1, 1);
            digCellZeroCheck(selected_x, selected_y + 1, 1);
        }
        checkWin();
    }
    playSFXWrapper(3);
}

#define BOX_DIM 20
#define BOX_BORDER 2
#define X_START (160 - (((float)(GRID_DIMENSIONS) / 2) * BOX_DIM))
#define Y_START (120 - (((float)(GRID_DIMENSIONS) / 2) * BOX_DIM))

int getXStart(int dimension) {
    return 160 - (((float)(dimension) / 2) * BOX_DIM);
}

int getYStart(int dimension) {
    return 120 - (((float)(dimension) / 2) * BOX_DIM);
}

void renderBoard(Gfx **dl_ptr, int show_progress, int dimension_override) {
    const rgb *color = 0;
    int x0 = 0;
    int y0 = 0;
    TileStruct *tile = 0;
    
    Gfx *dl = *dl_ptr;

    // Process
    int dim = GRID_DIMENSIONS;
    if (dimension_override != 0) {
        dim = dimension_override;
    }
    int x_start = getXStart(dim);
    int y_start = getYStart(dim);
    if (show_progress) {
        dl = setFillColor(dl, 0, 0, 0);
        gDPFillRectangle(dl++, x_start, y_start - 14, x_start + 30, y_start - 4);
        int x_end = x_start + (BOX_DIM * GRID_DIMENSIONS);
        gDPFillRectangle(dl++, x_end - 30, y_start - 14, x_end, y_start - 4);
    }
    for (int x = 0; x < dim; x++) {
        for (int y = 0; y < dim; y++) {
            x0 = x_start + (x * BOX_DIM);
            y0 = y_start + (y * BOX_DIM);
            // Border
            colorState cstate = COLORSTATE_BORDER;
            if (show_progress) {
                tile = &tiles[x][y];
                if (tile->uncovered) {
                    cstate = COLORSTATE_DIGGEDBORDER;
                }
                if ((x == selected_x) && (y == selected_y)) {
                    cstate = COLORSTATE_SELECTBORDER;
                }
            }
            color = &game_colors[cstate];
            dl = setFillColor(dl, color->red, color->green, color->blue);
            gDPFillRectangle(dl++, x0, y0, x0 + BOX_DIM, y0 + BOX_DIM);
            // Center
            cstate = COLORSTATE_SQUARE;
            if (show_progress) {
                tile = &tiles[x][y];
                if (tile->uncovered && tile->has_mine) {
                    cstate = COLORSTATE_MINE;
                }
            }
            color = &game_colors[cstate];
            dl = setFillColor(dl, color->red, color->green, color->blue);
            gDPFillRectangle(dl++, x0 + BOX_BORDER, y0 + BOX_BORDER, x0 + (BOX_DIM - BOX_BORDER), y0 + (BOX_DIM - BOX_BORDER));
            if (show_progress) {
                tile = &tiles[x][y];
                if (tile->flagged) {
                    dl = setFillColor(dl, 0, 0, 0);
                    gDPFillRectangle(dl++, x0 + 7, y0 + 4, x0 + 8, y0 + 16);
                    dl = setFillColor(dl, 255, 0, 0);
                    gDPFillRectangle(dl++, x0 + 9, y0 + 4, x0 + 14, y0 + 8);
                }
            }
        }
    }
    if (show_progress) {
        int mine_count = MINES;
        for (int x = 0; x < GRID_DIMENSIONS; x++) {
            for (int y = 0; y < GRID_DIMENSIONS; y++) {
                x0 = X_START + (x * BOX_DIM);
                y0 = Y_START + (y * BOX_DIM);
                tile = &tiles[x][y];
                if (tile->flagged) {
                    mine_count--;
                    if (mine_count < 0) {
                        mine_count = 0;
                    }
                }
                // Number
                if (tile->uncovered && (tile->adjacent_mines != 0) && (!tile->has_mine)) {
                    color = &game_colors[(tile->adjacent_mines - 1) + COLORSTATE_NUM1];
                    renderText(&dl, x0 + 6, y0 + 6, color->red, color->green, color->blue, 255, &tile->text[0]);
                }
            }
        }
        dk_strFormat(timer_text, "%03d", second_timer);
        dk_strFormat(mine_text, "%03d", mine_count);
        int x_end = x_start + (BOX_DIM * GRID_DIMENSIONS);
        renderText(&dl, x_start, y_start -12, 0xFF, 0x00, 0x00, 255, mine_text);
        renderText(&dl, x_end - 24, y_start -12, 0xFF, 0x00, 0x00, 255, timer_text);
        // Smiling Face
        int picture = 0x2F;
        if (game_state == GAMESTATE_MINE) {
            picture = 0x43;
        }
        dl = drawImage(dl, picture, 1, 64, 64, 640, 80, 1.0f, 1.0f, 0xFF, 0xD7, 0x00, 255);
    }
    *dl_ptr = dl;
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    game_state = GAMESTATE_TITLE;
    gameInit();
    *dl_ptr = dl;
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderBoard(&dl, 0, 11);
    int x_start = getXStart(11);
    int y_start = getYStart(11);
    for (int i = 0; i < 11; i++) {
        int x0 = x_start + (i * BOX_DIM) + 6;
        int y0 = y_start + (5 * BOX_DIM) + 6;
        int index = i & 7;
        const rgb *color = &game_colors[COLORSTATE_NUM1 + index];
        renderText(&dl, x0, y0, color->red, color->green, color->blue, 0xFF, &title_text[i << 1]);
        color = &game_colors[COLORSTATE_NUM1 + (7 - index)];
        renderText(&dl, x0, y0 + BOX_DIM, color->red, color->green, color->blue, 0xFF, &title_subtext[i << 1]);
    }
    if (MinigameInput->Buttons.start) {
        resetGame();
        generateBoard();
        game_state = GAMESTATE_NORMAL;
    }
    *dl_ptr = dl;
}

void changeSlot(void) {
    if (change_slot == 1) {
        change_slot = 2;
    }
    if ((MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left) {
        if (change_slot == 0) {
            selected_x--;
            if (selected_x < 0) {
                selected_x = (GRID_DIMENSIONS - 1);
            }
            change_slot = 1;
        }
    } else if ((MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right) {
        if (change_slot == 0) {
            selected_x++;
            if (selected_x > (GRID_DIMENSIONS - 1)) {
                selected_x = 0;
            }
            change_slot = 1;
        }
    } else if ((MinigameInput->stickY > 0x20) || MinigameInput->Buttons.d_up) {
        if (change_slot == 0) {
            selected_y--;
            if (selected_y < 0) {
                selected_y = (GRID_DIMENSIONS - 1);
            }
            change_slot = 1;
        }
    } else if ((MinigameInput->stickY < -0x20) || MinigameInput->Buttons.d_down) {
        if (change_slot == 0) {
            selected_y++;
            if (selected_y > (GRID_DIMENSIONS - 1)) {
                selected_y = 0;
            }
            change_slot = 1;
        }
    } else {
        change_slot = 0;
    }
}

void handleState_normal(Gfx **dl_ptr, gameStates state) {
    Gfx *dl = *dl_ptr;
    renderBoard(&dl, 1, 0);
    if (state == GAMESTATE_NORMAL) {
        // Controls
        changeSlot();
        if (MinigameInput->Buttons.a) {
            if (!digging) {
                digCell();
            }
            digging = 1;
        } else {
            digging = 0;
        }
        if (MinigameInput->Buttons.r) {
            if (!flagging) {
                tiles[selected_x][selected_y].flagged ^= 1;
                playSFXWrapper(25);
                checkWin();
            }
            flagging = 1;
        } else {
            flagging = 0;
        }
        frame_timer++;
        if (frame_timer > 59) {
            frame_timer = 0;
            second_timer++;
            if (second_timer > 999) {
                second_timer = 999;
            }
        }
    } else if (state == GAMESTATE_MINE) {
        if (ending_timer > 0) {
            ending_timer--;
            if (ending_timer == 0) {
                game_state = GAMESTATE_TITLE;
            }
        }
    } else if (state == GAMESTATE_WIN) {
        if (ending_timer > 0) {
            ending_timer--;
            if (ending_timer == 0) {
                gameVictory();
            }
        }
    }
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        gDPPipeSync(dl++);
        gDPSetCycleType(dl++, G_CYC_FILL);
        gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
        gSPClearGeometryMode(dl++, G_ZBUFFER);
        dl = setFillColor(dl, 0x80, 0x80, 0x80);
        gDPSetScissor(dl++, G_SC_NON_INTERLACE, 0, 0, 319, 239);
        gDPFillRectangle(dl++, 0, 0, 319, 239);
    }
    switch(game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_NORMAL:
        case GAMESTATE_MINE:
        case GAMESTATE_WIN:
            handleState_normal(&dl, game_state);
            break;
        default:
            break;
    }
    *dl_ptr = dl;
}