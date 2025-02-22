/**
 * @file cutscene_remove.c
 * @author Ballaam
 * @brief 
 * @version 0.1
 * @date 2022-10-03
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include "../../include/common.h"

static char skip_cutscenes = 0;
char enable_skip_check = 0;

void updateSkipCheck(void) {
	enable_skip_check = Rando.cutscene_skip_setting == CSSKIP_AUTO;
	if (Rando.cutscene_skip_setting == CSSKIP_PRESS) {
		enable_skip_check = skip_cutscenes;
	}
}

int isCutsceneSkipped(int cutscene) {
	int offset = (cutscene >> 5) & 1;
	int shift = cutscene & 31;
	if (cs_skip_db[offset] & (1 << shift)) {
		return 1;
	}
	return 0;
}

void CancelCutsceneInternals(int cs_index) {
	if (!CutsceneBanks[0].cutscene_databank) {
		return;
	}
	cutscene_item_data* databank = CutsceneBanks[0].cutscene_databank;
	cutscene_item_data* data = (cutscene_item_data*)&databank[cs_index];
	if (data) {
		for (int j = 0; j < data->num_points; j++) {
			short* write_spot = (short*)&data->length_array[j];
			if (write_spot) {
				*(short*)write_spot = 0;
			}
		}
	}
}

void clearQueuedCutsceneFunctions(void) {
	if (QueuedCutsceneFunctions) {
		queued_cutscene_function* data = QueuedCutsceneFunctions;
		while (data) {
			data->action_timer = 0x80000000 | ActorTimer;
			data = (queued_cutscene_function*)data->next;
			if (!data) {
				return;
			}
		}
	}
}

void pressToSkip(void) {
	if (!NewlyPressedControllerInput.Buttons.start) { // Not pressing start
		return;
	}
	if (CutsceneActive != 1) { // Cutscene not active
		return;
	}
	if (CutsceneStateBitfield & 4) { // Cutscene is global
		return;
	}
	if (isCutsceneSkipped(CutsceneIndex)) {
		CancelCutsceneInternals(CutsceneIndex);
		clearQueuedCutsceneFunctions();
		skip_cutscenes = 1;
	}
}

void clearSkipCache(void) {
	if (!CutsceneActive) {
		skip_cutscenes = 0;
	} else {
		pressToSkip();
	}
}

#define CUTSCENE_SKIP_LIMIT 2

void pressSkipHandler(void* actor) {
	if (skip_cutscenes) {
		if (CameraStateChangeTimer > CUTSCENE_SKIP_LIMIT) {
			CameraStateChangeTimer = CUTSCENE_SKIP_LIMIT;
		}
	}
	unkCutsceneFunction(actor);
}

void updateSkippableCutscenes(void) {
	/**
	 * @brief Parse the skip cutscenes database and set all cutscenes that will be skipped to
	 * have their segments set to 0 length
	 */
	if (CurrentMap < 216) {
		if (CutsceneBanks[0].cutscene_databank) {
			for (int i = 0; i < 64; i++) {
				if (isCutsceneSkipped(i)) {
					CancelCutsceneInternals(i);
				}
			}
		}
	}
}

void renderScreenTransitionCheck(int applied_transition) {
	/**
	 * @brief Alter the screen transition effect so that if it's a skipped cutscene, the transition won't play
	 * 
	 * @param applied_transition Transition index
	 */
	int permit = Rando.cutscene_skip_setting == CSSKIP_AUTO;
	if ((Rando.cutscene_skip_setting == CSSKIP_PRESS) && (skip_cutscenes)) {
		permit = 1;
	}
	if (permit) {
		if ((CurrentMap < 216) && ((CutsceneStateBitfield & 4) == 0)) {
			if (isCutsceneSkipped(CutsceneIndex)) {
				return;
			}
		}
	}
	renderScreenTransition(applied_transition);
}