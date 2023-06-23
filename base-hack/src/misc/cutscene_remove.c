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

void updateSkippableCutscenes(void) {
	/**
	 * @brief Parse the skip cutscenes database and set all cutscenes that will be skipped to
	 * have their segments set to 0 length
	 */
	if (CurrentMap < 216) {
		if (CutsceneBanks[0].cutscene_databank) {
			for (int i = 0; i < 64; i++) {
				int offset = 1;
				int shift = i - 32;
				if (i < 32) {
					offset = 0;
					shift = i;
				}
				if (cs_skip_db[(2 * CurrentMap) + offset] & (1 << shift)) {
					cutscene_item_data* databank = CutsceneBanks[0].cutscene_databank;
					cutscene_item_data* data = (cutscene_item_data*)&databank[i];
					if (data) {
						for (int j = 0; j < data->num_points; j++) {
							short* write_spot = (short*)&data->length_array[j];
							if (write_spot) {
								*(short*)write_spot = 0;
							}
						}
					}
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
    if ((CurrentMap < 216) && ((CutsceneStateBitfield & 4) == 0)) {
        int offset = 1;
        int shift = CutsceneIndex - 32;
        if (CutsceneIndex < 32) {
            offset = 0;
            shift = CutsceneIndex;
        }
        if (cs_skip_db[(2 * CurrentMap) + offset] & (1 << shift)) {
            return;
        }
    }
    renderScreenTransition(applied_transition);
}