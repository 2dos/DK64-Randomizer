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

ROM_DATA static gameStates game_state = GAMESTATE_TITLE;
ROM_DATA static char word_to_guess[] = "BEANS";
ROM_DATA static char selected_col = 0;
ROM_DATA static char selected_row = 0;
ROM_DATA static char selected_letter_index = 0;
ROM_DATA static char selected_guess_index = 0;
ROM_DATA static char change_letter = 0;
ROM_RODATA_PTR static const char *letters[] = {
    "A B C D E F G",
    "H I J K L M N",
    "O P Q R S T U",
    "V W X Y Z ba",
};
ROM_DATA static char selected_letter_single = 'A';
ROM_DATA static char selected_letter_row[] = "A            ";
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

extern void wordleEntry(void); // Needed for rerouting

void renderText(Gfx **dl_ptr, const int x, const int y, const int red, const int green, const int blue, const int alpha, const char *str) {
    Gfx *dl = *dl_ptr;
    gDPPipeSync(dl++);
    gDPSetCycleType(dl++, G_CYC_1CYCLE);
    gSPLoadGeometryMode(dl++, 0);
    gSPSetGeometryMode(dl++, G_ZBUFFER | G_SHADING_SMOOTH | 0x00000002);
    gDPSetPrimColor(dl++, 0, 0, red, green, blue, alpha);
    gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
    *dl_ptr = textDraw(dl, 2, x, y, str);
}

void playSFXWrapper(int sfx) {
    playSFXArcade(0x8076D1F8, sfx, 0x7FFF, 0x3F, 1.0f, 0, 0);
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    renderText(&dl, 0x88, 0x50, 0x6C, 0xA9, 0x65, 0xFF, "WOR");
    renderText(&dl, 0x88, 0x50, 0xC8, 0xB6, 0x53, 0xFF, "   DLE");
    renderText(&dl, 0x50, 0x70, 0XFF, 0xFF, 0xFF, 0xFF, "PRESS START TO PLAY");
    if (MinigameInput->Buttons.start) {
        game_state = GAMESTATE_NORMAL;
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
        guess_states[i] = GUESSSTATE_UNGUESSED;
    }
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    game_state = GAMESTATE_TITLE;
    resetGame();
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
        for (unsigned int i = 0; i < 13; i++) {
            selected_letter_row[i] = ' ';
        }
        int row_slot = 11;
        if ((selected_row != 3) || (selected_col != 6)) {
            row_slot = selected_col * 2;
        }
        selected_letter_single = letters[(int)selected_row][row_slot];
        selected_letter_row[selected_col * 2] = selected_letter_single;
    }
}

#define SQUARE_X_START 0x60
#define SQUARE_Y_START 0x20
#define SQUARE_DIM 0xC
#define SQUARE_SPACING 0x10

Gfx* drawScreenRect(Gfx* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha) {
	gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_FILL);
	gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
	gSPClearGeometryMode(dl++, G_ZBUFFER);
	gDPSetFillColor(dl++, ((red & 0x1F) << 11) | ((green & 0x1F) << 6) | ((blue & 0x1F) << 1) | (alpha & 0x1));
	gDPSetScissor(dl++, G_SC_NON_INTERLACE, 10, 10, 309, 229);
	gDPFillRectangle(dl++, x1 >> 2, y1 >> 2, x2 >> 2, y2 >> 2);
	return dl;
}

void renderBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 5; j++) {
            int x1 = SQUARE_X_START + (j * SQUARE_SPACING);
            int y1 = SQUARE_Y_START + (j * SQUARE_SPACING);
            dl = drawScreenRect(dl, x1, y1, x1 + SQUARE_DIM, y1 + SQUARE_DIM, 0x4, 0x4, 0x4, 0x1);
        }
        if (i < selected_guess_index) {
            renderText(&dl, 0x60, 0x20 + (i * 0x10), 0xFF, 0xFF, 0xFF, 0xFF, guesses[i]);
        }
    }
    renderText(&dl, 0x60, 0x20 + (selected_guess_index * 0x10), 0xFF, 0xFF, 0xFF, 0xFF, guess);
    *dl_ptr = dl;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (unsigned int i = 0; i < 4; i++) {
        renderText(&dl, 0x60, 0x90 + (i * 0x10), 0xFF, 0xFF, 0xFF, 0xFF, letters[i]);
    }
    renderText(&dl, 0x60, 0x90 + (selected_row * 0x10), 0x32, 0x91, 0xA8, 0xFF, selected_letter_row);
    changeLetter();
    if (((p1PressedButtons & A_BUTTON) && (selected_col == 5) && (selected_row == 3)) || (p1PressedButtons & B_BUTTON)) {
        if (selected_letter_index > 0) {
            selected_letter_index--;
            guess[selected_letter_index * GUESS_CHAR_SPACING] = ' ';
        }
    } else if (p1PressedButtons & A_BUTTON) {
        if ((selected_col == 6) && (selected_row == 3)) {
            if (selected_letter_index == 5) {
                // Submit Guess
            }
        } else {
            if (selected_letter_index < 5) {
                guess[selected_letter_index * GUESS_CHAR_SPACING] = selected_letter_single;
            }
        }
        selected_letter_index++;
    }
    renderBoard(&dl);
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
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
    *dl_ptr = &dl[-1];
}