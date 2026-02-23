// minigame: wordle
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
} gameStates;

typedef enum guessStates {
    GUESSSTATE_UNGUESSED,
    GUESSSTATE_INCORRECT,
    GUESSSTATE_WRONGSPOT,
    GUESSSTATE_CORRECT,
} guessStates;

ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static char word_to_guess[] = "BEANS";
ROM_DATA static char selected_col = 0;
ROM_DATA static char selected_row = 0;
ROM_DATA static char selected_letter_index = 0;
ROM_DATA static char selected_guess_index = 0;
ROM_DATA static char change_letter = 0;
ROM_DATA static char selected_letter_single = 'A';
#define GUESS_CHAR_SPACING 3
ROM_DATA static char guess[] = "A  B  C  D  E";
ROM_DATA static char *guesses[] = {
    "A  B  C  D  E",
    "G  H  I  J  K",
    "L  M  N  O  P",
    "P  O  N  M  L",
    "K  J  I  H  G",
    "E  D  C  B  A",
};
ROM_DATA static char guess_states[30] = {};
ROM_DATA static char guess_states_temp[5] = {};
ROM_RODATA_NUM static const char letters[] = "A\0B\0C\0D\0E\0F\0G\0H\0I\0J\0K\0L\0M\0N\0O\0P\0Q\0R\0S\0T\0U\0V\0W\0X\0Y\0Z\0b\0a\0";
ROM_DATA static char letter_states[28] = {};
ROM_RODATA_NUM static const char guess_rgb[] = {
    0x04, 0x04, 0x04,
    0x04, 0x04, 0x04,
    0x19, 0x16, 0x0A,
    0x0D, 0x15, 0x0C,
};
ROM_RODATA_NUM static const char letter_rgb[] = {
    0xA0, 0xA0, 0xA0,
    0x20, 0x20, 0x20,
    0xC8, 0xB6, 0x53,
    0x6C, 0xA9, 0x65,
};
ROM_RODATA_NUM static const char title_rgb[] = {
    0x19, 0x16, 0x0A,
    0x0D, 0x15, 0x0C,
    0x04, 0x04, 0x04,
    0x19, 0x16, 0x0A,
    0x0D, 0x15, 0x0C,
    0x04, 0x04, 0x04,
};
ROM_DATA static unsigned char title_timer = 0;
ROM_DATA static unsigned char title_offset = 0;
ROM_DATA static unsigned char revealing_letters_timer = 0;
ROM_DATA static unsigned char queue_win = 0;
#define TIMER_BUFFER 30
#define TIMER_OFFSET 15
#define SQUARE_X_START 0x170
#define SQUARE_Y_START 0x30
#define SQUARE_DIM 0x40
#define SQUARE_SPACING 0x60
#define SQUARE_BORDER 0x4

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    // renderText(&dl, 0x88, 0x50, 0x6C, 0xA9, 0x65, 0xFF, "WOR");
    // renderText(&dl, 0x88, 0x50, 0xC8, 0xB6, 0x53, 0xFF, "   DLE");
    for (int i = 0; i < 6; i++) {
        int x1 = 0x128 + (i * 0x80);
        int y1 = 0x128;
        int index = (i + title_offset) % 6;
        const char *guess_rgba = &title_rgb[index * 3];
        dl = drawScreenRect(dl, x1, y1, x1 + 0x50, y1 + 0x50, guess_rgba[0], guess_rgba[1], guess_rgba[2], 0x1);
    }
    if (title_timer > 0) {
        title_timer--;
    } else if (title_timer == 0) {
        title_timer = 80;
        title_offset++;
        if (title_offset == 6) {
            title_offset = 0;
        }
    }
    renderText(&dl, 0x50, 0x50, 0XFF, 0xFF, 0xFF, 0xFF, "W   O   R   D   L   E");
    renderText(&dl, 0x18, 0x70, 0XFF, 0xFF, 0xFF, 0xFF, "P R E S S  S T A R T  T O  P L A Y");
    if (p1PressedButtons & START_BUTTON) {
        game_state = GAMESTATE_NORMAL;
    } else if (p1PressedButtons & B_BUTTON) {
        gameExit();
    }
    *dl_ptr = dl;
}

void resetGame(void) {
    for (int i = 0; i < 5; i++) {
        guess[i * GUESS_CHAR_SPACING] = ' ';
    }
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 5; j++) {
            guesses[i][j * GUESS_CHAR_SPACING] = ' ';
        }
    }
    for (int i = 0; i < 30; i++) {
        if (i < 28) {
            letter_states[i] = GUESSSTATE_UNGUESSED;
        }
        guess_states[i] = GUESSSTATE_UNGUESSED;
    }
    queue_win = 0;
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    game_state = GAMESTATE_TITLE;
    gameInit();
    resetGame();
    title_timer = 80;
    *dl_ptr = dl;
}

void changeLetter(void) {
    if (change_letter == 1) {
        change_letter = 2;
    }
    if ((MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left) {
        if (change_letter == 0) {
            selected_col--;
            if (selected_col < 0) {
                selected_col = 6;
            }
            change_letter = 1;
        }
    } else if ((MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right) {
        if (change_letter == 0) {
            selected_col++;
            if (selected_col > 6) {
                selected_col = 0;
            }
            change_letter = 1;
        }
    } else if ((MinigameInput->stickY > 0x20) || MinigameInput->Buttons.d_up) {
        if (change_letter == 0) {
            selected_row--;
            if (selected_row < 0) {
                selected_row = 3;
            }
            change_letter = 1;
        }
    } else if ((MinigameInput->stickY < -0x20) || MinigameInput->Buttons.d_down) {
        if (change_letter == 0) {
            selected_row++;
            if (selected_row > 3) {
                selected_row = 0;
            }
            change_letter = 1;
        }
    } else {
        change_letter = 0;
    }
    if (change_letter == 1) {
        selected_letter_single = letters[((7 * selected_row) + selected_col) * 2];
    }
}


void renderBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 5; j++) {
            int x1 = SQUARE_X_START + (j * SQUARE_SPACING);
            int y1 = SQUARE_Y_START + (i * SQUARE_SPACING);
            guessStates guess_state = guess_states[(5 * i) + j];
            const char *guess_rgba = &guess_rgb[guess_state * 3];
            dl = drawScreenRect(dl, x1, y1, x1 + SQUARE_DIM, y1 + SQUARE_DIM, guess_rgba[0], guess_rgba[1], guess_rgba[2], 0x1);
            if (guess_state == GUESSSTATE_UNGUESSED) {
                dl = drawScreenRect(dl, x1 + SQUARE_BORDER, y1 + SQUARE_BORDER, x1 + SQUARE_DIM - SQUARE_BORDER, y1 + SQUARE_DIM - SQUARE_BORDER, 0x0, 0x0, 0x0, 0x1);
            }
        }
        if (i < selected_guess_index) {
            renderText(&dl, 0x60, 0x10 + (i * 0x18), 0xFF, 0xFF, 0xFF, 0xFF, guesses[i]);
        }
    }
    renderText(&dl, 0x60, 0x10 + (selected_guess_index * 0x18), 0xFF, 0xFF, 0xFF, 0xFF, guess);
    *dl_ptr = dl;
}

ROM_RODATA_NUM static const char selected_rgb[] = {0x32, 0x91, 0xA8};
ROM_RODATA_NUM static const unsigned char state_sfx[] = {161, 161, 158, 160};

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 7; j++) {
            guessStates state = letter_states[(i * 7) + j];
            const char *rgb = &letter_rgb[state * 3];
            if ((i == (unsigned int)selected_row) && (j == (unsigned int)selected_col)) {
                rgb = &selected_rgb[0];
            }
            renderText(&dl, 0x60 + (j * 0x10), 0xA8 + (i * 0x10), rgb[0], rgb[1], rgb[2], 0xFF, &letters[((7 * i) + j) * 2]);
        }
    }
    if (revealing_letters_timer == 0) {
        changeLetter();
        if (((p1PressedButtons & A_BUTTON) && (selected_col == 5) && (selected_row == 3)) || (p1PressedButtons & B_BUTTON)) {
            if (selected_letter_index > 0) {
                selected_letter_index--;
                guess[selected_letter_index * GUESS_CHAR_SPACING] = ' ';
            }
        } else if (p1PressedButtons & A_BUTTON) {
            if ((selected_col == 6) && (selected_row == 3)) {
                if (selected_letter_index >= 5) {
                    // Submit Guess
                    int correct_counter = 0;
                    for (int i = 0; i < 5; i++) {
                        guessStates state = GUESSSTATE_INCORRECT;
                        for (int j = 0; j < 5; j++) {
                            if (guess[i * GUESS_CHAR_SPACING] == word_to_guess[j]) {
                                if (i == j) {
                                    state = GUESSSTATE_CORRECT;
                                } else if (state == GUESSSTATE_INCORRECT) {
                                    state = GUESSSTATE_WRONGSPOT;
                                }
                            }
                        }
                        if (state == GUESSSTATE_CORRECT) {
                            correct_counter++;
                        }
                        guess_states_temp[i] = state;
                    }
                    revealing_letters_timer = 6 * TIMER_BUFFER;
                    if (correct_counter == 5) {
                        queue_win = 1;
                    }
                }
            } else {
                if (selected_letter_index < 5) {
                    guess[selected_letter_index * GUESS_CHAR_SPACING] = selected_letter_single;
                    playSFXWrapper(64);
                    selected_letter_index++;
                }
            }
        }
    } else {
        revealing_letters_timer--;
        for (int i = 0; i < 5; i++) {
            if (revealing_letters_timer < (((4 - i) * TIMER_BUFFER) + TIMER_OFFSET)) {
                guess_states[(selected_guess_index * 5) + i] = guess_states_temp[i];
                if ((revealing_letters_timer + 1) == (((4 - i) * TIMER_BUFFER) + TIMER_OFFSET)) { 
                    playSFXWrapper(state_sfx[(int)guess_states_temp[i]]);
                }
                for (int j = 0; j < 28; j++) {
                    if (guess[i * GUESS_CHAR_SPACING] == letters[j * 2]) {
                        letter_states[j] = guess_states_temp[i];
                    }
                }
            }
        }
        if (revealing_letters_timer == 0) {
            for (int i = 0; i < 5; i++) {
                guess_states_temp[i] = GUESSSTATE_UNGUESSED;
                guesses[(int)selected_guess_index][i * GUESS_CHAR_SPACING] = guess[i * GUESS_CHAR_SPACING];
                guess[i * GUESS_CHAR_SPACING] = ' ';
            }
            selected_guess_index++;
            selected_letter_index = 0;
            if (queue_win) {
                // Win
                gameVictory();
            } else if (selected_guess_index == 6) {
                // Lose
                game_state = GAMESTATE_INIT;
            }
        }
    }
    renderBoard(&dl);
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 0, 0, 0, 0);
    }
    switch(game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_NORMAL:
            handleState_normal(&dl);
            break;
        default:
            break;
    }
    *dl_ptr = dl;
}