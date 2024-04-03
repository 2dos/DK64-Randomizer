/**
 * @file melon_crate.c
 * @author Ballaam
 * @brief Functions related to melon crates
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void MelonCrateGenericCode(behaviour_data* behaviour, int index, int id) {
	if (behaviour->current_state == 0) {
		behaviour->unk_68 = 50;
		behaviour->unk_6A = 50;
		behaviour->unk_6C = 50;
		behaviour->unk_67 = 4;
		unkObjFunction1(index, 1, 255);
		unkObjFunction2(index, 1, -1);
		setScriptRunState(behaviour, RUNSTATE_DISTANCERUN, 500);
		unkObjFunction9(index, 1, 1);
		behaviour->next_state = 1;
	} else if (behaviour->current_state == 1) {
		if (behaviour->counter == 0) {
			short a = 0;
			float b = 0;
			char c = 0;
			unkObjFunction16(index, 1, &a, &b, &c);
			if ((a == 18) || (a == 19)) {
				int pitch = 80;
				if (a == 19) {
					pitch = 70;
				}
				playSFXFromObject(index, 757, 100, 127, 20, pitch, 0.3f);
				behaviour->counter_next = 1;
			} else {
				behaviour->counter_next = 0;
			}
		}
		if ((behaviour->switch_pressed == 1) && (canHitSwitch())) {
			int interaction = getInteractionOfContactActor(behaviour->contact_actor_type);
			if (interaction & 0x4) { // Projectile
				int idx_0 = convertSubIDToIndex(index);
				setSomeTimer(ObjectModel2Pointer[idx_0].object_type);
				behaviour->next_state = 2;
			}
			if (interaction & 0x1) { // Player
				if (Player->unk_132 & 0x7F8) {
					behaviour->next_state = 2;
				}
			}
		}
		if (Player->control_state == 28) {
			if (standingOnM2Object(index)) {
				behaviour->next_state = 2;
			}
		}
	} else if (behaviour->current_state == 2) {
		playSong(SONG_MELONSLICEDROP, 1.0f);
		playSFXFromObject(index, 35, 255, 127, 0, 0, 0.3f);
		melonCrateItemHandler(behaviour, index, 0, 0);
		int val = unkSoundIndex;
		if (val != 0x10) {
			int idx_0 = convertSubIDToIndex(index);
			unkSoundArray[val] = ObjectModel2Pointer[idx_0].object_id;
			unkSoundIndex += 1;
		}
	}
}