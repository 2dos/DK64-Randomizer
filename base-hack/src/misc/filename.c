/**
 * @file filename.c
 * @author Ballaam
 * @brief Changes to give the player an optional filename
 * @version 0.1
 * @date 2022-07-14
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static const char* char_list[] = {
    "A B C D E F G H I J K L M",
    "N O P Q R S T U V W X Y Z",
    "0 1 2 3 4 5 6 7 8 9   b q", // b = (B) q = (A)
};

static char temporary_filename[FILENAME_LENGTH + 1] = "";

Gfx* filename_displaylist(actorData* actor, Gfx* dl) {
	menu_controller_paad* paad = actor->paad;
	float x = 0.0f;
	float y = 0.0f;
	handleTextScrolling(paad, 160.0f, 20.0f, &x, &y, 2, 0, 1.5f);
	short y2 = y * 4;
	dl = printText(dl, 0x280, y2, 0.65f, "ENTER FILENAME");
	dl = printText(dl, 0x280, y2 + 200, 0.65f, temporary_filename);
	handleTextScrolling(paad, 160.0f, 160.0f, &x, &y, 1, 0, 1.5f);
	y2 = y * 4;
    int sy = y2 - 128;
    int dy = 80;
    for (int i = 0; i < 3; i++) { // should be 3
		dl = printText(dl, 0x280, sy + (i * dy), 0.65f, (char*)char_list[i]);
    }
    return dl;
}

void filename_code(actorData* actor, int button_bitfield) {
    /*
		Buttons:
			0001 0000 0000 - Z Button
			0000 1000 0000 - C Down
			0000 0100 0000 - C Up
			0000 0010 0000 - Default
			0000 0001 0000 - Down
			0000 0000 1000 - Right
			0000 0000 0100 - Default
			0000 0000 0010 - B Button
			0000 0000 0001 - A Button
	*/
    menu_controller_paad* paad = actor->paad;
	if (paad->screen_transition_progress == 0.0f) {
		if (paad->unk_4 == 0.0f) {
			if (button_bitfield & 1) { // A
				
			} else if (button_bitfield & 2) { // B
				playSFX(0x2C9);
				paad->prevent_action = 0;
				paad->next_screen = 3;
			}
		}
		// initMenuBackground(paad, 2);
	}
	updateMenuController(actor,paad,1);
}

static char* default_filenames[] = {
	"DONKEY",
	"DIDDY",
	"LANKY",
	"TINY",
	"CHUNKY",
	"KRUSHA",
	"DIXIE",
	"KIDDIE",
	"K. ROOL",
};

void filename_init(actorData* actor) {
	if (filename[0] == 0) {
		dk_strFormat((char*)temporary_filename, "%s", default_filenames[getRNGLower31() & (sizeof(default_filenames) >> 2)]);
	} else {
		dk_strFormat((char*)temporary_filename, "%s", (char*)filename);
	}
}