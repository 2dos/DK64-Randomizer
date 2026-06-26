// minigame: connect4
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_PIECE_DROP,
    GAMESTATE_GAMEOVER,
} gameStates;

typedef enum colorState {
    COLORSTATE_BG,
    COLORSTATE_BOARD,
    COLORSTATE_EMPTY_SLOT,
    COLORSTATE_PLAYER1,
    COLORSTATE_AI,
    COLORSTATE_TEXT,
} colorState;

#define GRID_M 7 // Columns
#define GRID_N 6 // Rows
#define DROP_SPEED_FRAMES 4 // Number of frames per row drop step
#define AI_THINK_FRAMES 45  // Delay frames to simulate AI "thinking"

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static unsigned char board[GRID_M][GRID_N] = {0}; // 0: Empty, 1: Player (Red), 2: AI (Yellow)
ROM_DATA static int selected_col = 0;
ROM_DATA static unsigned char current_turn = 2; // AI goes first (2)
ROM_DATA static char input_cooldown = 0;
ROM_DATA static int winning_player = 0;
ROM_DATA static int ai_thinking_timer = 0;
ROM_DATA static int animating_col = 0;
ROM_DATA static int animating_target_row = 0;
ROM_DATA static int animating_current_row = 0;
ROM_DATA static int animating_piece_type = 0;
ROM_DATA static int animation_frame_timer = 0;
ROM_DATA static int victory_delay_timer = 0;

ROM_RODATA_NUM static const rgb game_colors[] = {
    { .red = 0x1A, .green = 0x1A, .blue = 0x1A }, // BG (Dark Grey)
    { .red = 0x00, .green = 0x44, .blue = 0xCC }, // BOARD (Classic Blue)
    { .red = 0x2A, .green = 0x2A, .blue = 0x2A }, // EMPTY SLOT
    { .red = 0xCC, .green = 0x00, .blue = 0x00 }, // PLAYER 1 (Red)
    { .red = 0xDD, .green = 0xBB, .blue = 0x00 }, // AI (Yellow)
    { .red = 0xFF, .green = 0xFF, .blue = 0xFF }, // TEXT
};

void resetGame(void) {
    for (int x = 0; x < GRID_M; x++) {
        for (int y = 0; y < GRID_N; y++) {
            board[x][y] = 0;
        }
    }
    selected_col = GRID_M / 2;
    current_turn = 2; // AI goes first upon reset
    winning_player = 0;
    input_cooldown = 0;
    victory_delay_timer = 0;
    ai_thinking_timer = 0;
}

int checkWinCondition(int p) {
    // Horizontal check
    for (int y = 0; y < GRID_N; y++) {
        for (int x = 0; x < GRID_M - 3; x++) {
            if (board[x][y] == p && board[x+1][y] == p && board[x+2][y] == p && board[x+3][y] == p) return 1;
        }
    }
    // Vertical check
    for (int x = 0; x < GRID_M; x++) {
        for (int y = 0; y < GRID_N - 3; y++) {
            if (board[x][y] == p && board[x][y+1] == p && board[x][y+2] == p && board[x][y+3] == p) return 1;
        }
    }
    // Ascending Diagonal check
    for (int x = 0; x < GRID_M - 3; x++) {
        for (int y = 3; y < GRID_N; y++) {
            if (board[x][y] == p && board[x+1][y-1] == p && board[x+2][y-2] == p && board[x+3][y-3] == p) return 1;
        }
    }
    // Descending Diagonal check
    for (int x = 0; x < GRID_M - 3; x++) {
        for (int y = 0; y < GRID_N - 3; y++) {
            if (board[x][y] == p && board[x+1][y+1] == p && board[x+2][y+2] == p && board[x+3][y+3] == p) return 1;
        }
    }
    return 0;
}

int isBoardFull(void) {
    for (int x = 0; x < GRID_M; x++) {
        if (board[x][0] == 0) return 0;
    }
    return 1;
}

int getLowestRow(int col) {
    for (int y = GRID_N - 1; y >= 0; y--) {
        if (board[col][y] == 0) return y;
    }
    return -1;
}

int scoreWindow(int p1_count, int ai_count, int empty_count) {
    if (ai_count == 4) return 1000000;    // Absolute priority: Win immediately
    if (p1_count == 3 && empty_count == 1) return 200000; // Critical priority: Block player from winning 4-in-a-row
    if (ai_count == 3 && empty_count == 1) return 50;     // Setup active offense lines
    if (ai_count == 2 && empty_count == 2) return 10;     // Minor strategic placement
    return 0;
}

int evaluateBoardPosition(void) {
    int score = 0;
    int center_col = GRID_M / 2;
    for (int y = 0; y < GRID_N; y++) {
        if (board[center_col][y] == 2) score += 4;
    }

    for (int y = 0; y < GRID_N; y++) {
        for (int x = 0; x < GRID_M - 3; x++) {
            int p1 = 0, ai = 0, emp = 0;
            for (int i = 0; i < 4; i++) {
                if (board[x+i][y] == 1) p1++;
                else if (board[x+i][y] == 2) ai++;
                else emp++;
            }
            score += scoreWindow(p1, ai, emp);
        }
    }

    for (int x = 0; x < GRID_M; x++) {
        for (int y = 0; y < GRID_N - 3; y++) {
            int p1 = 0, ai = 0, emp = 0;
            for (int i = 0; i < 4; i++) {
                if (board[x][y+i] == 1) p1++;
                else if (board[x][y+i] == 2) ai++;
                else emp++;
            }
            score += scoreWindow(p1, ai, emp);
        }
    }

    for (int x = 0; x < GRID_M - 3; x++) {
        for (int y = 0; y < GRID_N - 3; y++) {
            int p1 = 0, ai = 0, emp = 0;
            for (int i = 0; i < 4; i++) {
                if (board[x+i][y+i] == 1) p1++;
                else if (board[x+i][y+i] == 2) ai++;
                else emp++;
            }
            score += scoreWindow(p1, ai, emp);
        }
    }
    for (int x = 0; x < GRID_M - 3; x++) {
        for (int y = 3; y < GRID_N; y++) {
            int p1 = 0, ai = 0, emp = 0;
            for (int i = 0; i < 4; i++) {
                if (board[x+i][y-i] == 1) p1++;
                else if (board[x+i][y-i] == 2) ai++;
                else emp++;
            }
            score += scoreWindow(p1, ai, emp);
        }
    }
    return score;
}

void startPieceDropAnimation(int col, int target_row, int piece_type) {
    animating_col = col;
    animating_target_row = target_row;
    animating_current_row = 0;
    animating_piece_type = piece_type;
    animation_frame_timer = 0;
    game_state = GAMESTATE_PIECE_DROP;
}

void updatePieceDropAnimation(void) {
    animation_frame_timer++;
    if (animation_frame_timer >= DROP_SPEED_FRAMES) {
        animation_frame_timer = 0;
        
        if (animating_current_row < animating_target_row) {
            animating_current_row++;
        } else {
            board[animating_col][animating_target_row] = animating_piece_type;
            playSFXWrapper(158); 

            if (checkWinCondition(animating_piece_type)) {
                winning_player = animating_piece_type;
                game_state = GAMESTATE_GAMEOVER;
                if (winning_player == 1) {
                    playSFXWrapper(71);
                    victory_delay_timer = 60; 
                } else {
                    playSFXWrapper(0x2D4); // Laugh 
                }
                return;
            }

            if (isBoardFull()) {
                winning_player = 0;
                game_state = GAMESTATE_GAMEOVER;
                return;
            }

            current_turn = (animating_piece_type == 1) ? 2 : 1;
            ai_thinking_timer = 0; 
            game_state = GAMESTATE_NORMAL;
        }
    }
}

void executeAITurn(void) {
    ai_thinking_timer++;
    if (ai_thinking_timer < AI_THINK_FRAMES) {
        return; 
    }

    int best_score = -9999999;
    int best_col = 0;

    for (int col = 0; col < GRID_M; col++) {
        int row = getLowestRow(col);
        if (row != -1) {
            // 1. Simulate AI placing its piece
            board[col][row] = 2;
            
            int current_position_score = evaluateBoardPosition();

            // 2. Lookahead validation: Check if this move enables an instant player win directly above it
            if (row > 0) {
                board[col][row - 1] = 1;
                if (checkWinCondition(1)) {
                    current_position_score -= 500000;
                }
                board[col][row - 1] = 0;
            }

            board[col][row] = 0;

            current_position_score += (getRNGLower31() % 16);

            if (current_position_score > best_score) {
                best_score = current_position_score;
                best_col = col;
            }
        }
    }

    int target_row = getLowestRow(best_col);
    if (target_row != -1) {
        startPieceDropAnimation(best_col, target_row, 2);
    }
}

void tryDropPlayerPiece(void) {
    int row = getLowestRow(selected_col);
    if (row != -1) {
        startPieceDropAnimation(selected_col, row, 1);
    } else {
        playSFXWrapper(246); 
    }
}

ROM_DATA static char prev_stick_left = 0;
ROM_DATA static char prev_stick_right = 0;

void handleControls(void) {
    char curr_left = (MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left;
    char curr_right = (MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right;

    if (curr_left && !prev_stick_left) {
        selected_col--;
        if (selected_col < 0) selected_col = GRID_M - 1;
        playSFXWrapper(64); 
    }
    else if (curr_right && !prev_stick_right) {
        selected_col++;
        if (selected_col >= GRID_M) selected_col = 0;
        playSFXWrapper(64);
    }

    prev_stick_left = curr_left;
    prev_stick_right = curr_right;

    if (p1PressedButtons & A_BUTTON) {
        tryDropPlayerPiece();
    }
}

#define BOX_DIM 24
#define BOARD_PADDING 4
#define X_START (160 - ((GRID_M * BOX_DIM) / 2))
#define Y_START (130 - ((GRID_N * BOX_DIM) / 2))

Gfx* maskCornerRectangles(Gfx *dl, int x0, int y0, const rgb *board_color) {
    dl = setFillColor(dl, board_color->red, board_color->green, board_color->blue);
    
    // Top-Left
    gDPFillRectangle(dl++, x0 + 2, y0 + 2, x0 + 5, y0 + 3);
    gDPFillRectangle(dl++, x0 + 2, y0 + 3, x0 + 3, y0 + 5);

    // Top-Right
    gDPFillRectangle(dl++, x0 + BOX_DIM - 5, y0 + 2, x0 + BOX_DIM - 2, y0 + 3);
    gDPFillRectangle(dl++, x0 + BOX_DIM - 3, y0 + 3, x0 + BOX_DIM - 2, y0 + 5);

    // Bottom-Left
    gDPFillRectangle(dl++, x0 + 2, y0 + BOX_DIM - 3, x0 + 5, y0 + BOX_DIM - 2);
    gDPFillRectangle(dl++, x0 + 2, y0 + BOX_DIM - 5, x0 + 3, y0 + BOX_DIM - 3);

    // Bottom-Right
    gDPFillRectangle(dl++, x0 + BOX_DIM - 5, y0 + BOX_DIM - 2, x0 + BOX_DIM - 2, y0 + BOX_DIM - 2);
    gDPFillRectangle(dl++, x0 + BOX_DIM - 3, y0 + BOX_DIM - 5, x0 + BOX_DIM - 2, y0 + BOX_DIM - 3);

    return dl;
}

void renderConnectBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    const rgb *b_color = &game_colors[COLORSTATE_BOARD];
    
    if (current_turn == 1 && game_state == GAMESTATE_NORMAL) {
        int sel_x = X_START + (selected_col * BOX_DIM) + (BOX_DIM / 2) - 4;
        const rgb *turn_color = &game_colors[COLORSTATE_PLAYER1];
        dl = setFillColor(dl, turn_color->red, turn_color->green, turn_color->blue);
        gDPFillRectangle(dl++, sel_x, Y_START - 14, sel_x + 8, Y_START - 10);
        gDPFillRectangle(dl++, sel_x + 2, Y_START - 10, sel_x + 6, Y_START - 6);
    }

    dl = setFillColor(dl, b_color->red, b_color->green, b_color->blue);
    gDPFillRectangle(dl++, X_START - BOARD_PADDING, Y_START - BOARD_PADDING, 
                     X_START + (GRID_M * BOX_DIM) + BOARD_PADDING, 
                     Y_START + (GRID_N * BOX_DIM) + BOARD_PADDING);

    for (int x = 0; x < GRID_M; x++) {
        for (int y = 0; y < GRID_N; y++) {
            int x0 = X_START + (x * BOX_DIM);
            int y0 = Y_START + (y * BOX_DIM);
            
            int color_idx = COLORSTATE_EMPTY_SLOT;
            if (board[x][y] == 1) color_idx = COLORSTATE_PLAYER1;
            else if (board[x][y] == 2) color_idx = COLORSTATE_AI;

            const rgb *c = &game_colors[color_idx];
            dl = setFillColor(dl, c->red, c->green, c->blue);
            gDPFillRectangle(dl++, x0 + 2, y0 + 2, x0 + BOX_DIM - 2, y0 + BOX_DIM - 2);

            dl = maskCornerRectangles(dl, x0, y0, b_color);
        }
    }

    if (game_state == GAMESTATE_PIECE_DROP) {
        int drop_x = X_START + (animating_col * BOX_DIM);
        int drop_y = Y_START + (animating_current_row * BOX_DIM);
        int anim_color_idx = (animating_piece_type == 1) ? COLORSTATE_PLAYER1 : COLORSTATE_AI;
        const rgb *ac = &game_colors[anim_color_idx];
        
        dl = setFillColor(dl, ac->red, ac->green, ac->blue);
        gDPFillRectangle(dl++, drop_x + 2, drop_y + 2, drop_x + BOX_DIM - 2, drop_y + BOX_DIM - 2);

        dl = maskCornerRectangles(dl, drop_x, drop_y, b_color);
    }

    if (game_state == GAMESTATE_NORMAL) {
        if (current_turn == 1) {
            renderText(&dl, 20, 20, 255, 0, 0, 255, "YOUR TURN");
        } else {
            renderText(&dl, 20, 20, 255, 220, 0, 255, "K. ROOL THINKING...");
        }
    }

    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 1, game_colors[COLORSTATE_BG].red, 
                                     game_colors[COLORSTATE_BG].green, 
                                     game_colors[COLORSTATE_BG].blue);
    }

    switch(game_state) {
        case GAMESTATE_INIT:
            gameInit();
            game_state = GAMESTATE_TITLE;
            break;

        case GAMESTATE_TITLE:
            renderText(&dl, 95, 90, 0, 100, 255, 255, "CONNECT 4");
            renderText(&dl, 85, 155, 255, 255, 255, 255, "PRESS START TO PLAY");
            if (p1PressedButtons & START_BUTTON) {
                resetGame();
                game_state = GAMESTATE_NORMAL;
            } else if (p1PressedButtons & B_BUTTON) {
                gameExit();
            }
            break;

        case GAMESTATE_NORMAL:
            if (current_turn == 1) {
                handleControls();
            } else {
                executeAITurn();
            }
            renderConnectBoard(&dl);
            break;

        case GAMESTATE_PIECE_DROP:
            updatePieceDropAnimation();
            renderConnectBoard(&dl);
            break;

        case GAMESTATE_GAMEOVER:
            if (winning_player == 1 && victory_delay_timer > 0) {
                victory_delay_timer--;
                if (victory_delay_timer == 0) {
                    gameVictory(); 
                    return;
                }
            }
            
            renderConnectBoard(&dl);
            
            if (winning_player == 0) {
                renderText(&dl, 130, 20, 255, 255, 255, 255, "TIE GAME");
                renderText(&dl, 75, 215, 255, 255, 255, 255, "START BUTTON TO RESTART");
                if (p1PressedButtons & START_BUTTON) game_state = GAMESTATE_TITLE;
            } else if (winning_player == 2) {
                renderText(&dl, 110, 15, 255, 50, 50, 255, "YOU LOSE");
                renderText(&dl, 95, 30, 220, 220, 220, 255, "TRY AGAIN?");
                renderText(&dl, 75, 215, 255, 255, 255, 255, "PRESS START TO TRY AGAIN");
                if (p1PressedButtons & START_BUTTON) {
                    resetGame();
                    game_state = GAMESTATE_NORMAL;
                } else if (p1PressedButtons & B_BUTTON) {
                    gameExit();
                }
            }
            break;
    }
    *dl_ptr = dl;
}