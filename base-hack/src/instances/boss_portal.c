/**
 * @file boss_portal.c
 * @author Ballaam
 * @brief Functions related to T&S Portals
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"
#define PORTAL_DELTA 40

void alterParentLocationTNS(int id) {
	int* m2location = (int*)ObjectModel2Pointer;
	for (int i = 0; i < 17; i++) {
		if (parentData[i].in_submap) {
			if ((parentData[i].map == CurrentMap) && (parentData[i].transition_properties_bitfield == 3)) {
				int index = convertIDToIndex(id);
				ModelTwoData* tied_object = getObjectArrayAddr(m2location,0x90,index);
				model_struct* model = tied_object->model_pointer;
				float angle = model->rot_y;
				angle /= 360;
				angle *= 4096;
				int angle_int = angle;
				float dx = PORTAL_DELTA * determineXRatioMovement(angle_int);
				float dz = PORTAL_DELTA * determineZRatioMovement(angle_int);
				parentData[i].positions.xPos = tied_object->xPos + dx;
				parentData[i].positions.zPos = tied_object->zPos + dz;
				int opp_angle = angle_int + 2048;
				parentData[i].facing_angle = opp_angle & 0xFFF;
				return;
			}
		}
	}
}

void TNSPortalGenericCode(behaviour_data* behaviour, int index, int id) {
	/**
	 * @brief Generic code for a T&S Portal
	 * 
	 * @param behaviour Behaviour Pointer for Object
	 * @param index Index of Object in Model Two Array
	 * @param id T&S Portal ID
	 */
	int world = getWorld(CurrentMap, 0);
	if (behaviour->current_state == 0) {
		unkObjFunction0(index, 1, 0);
		unkObjFunction1(index, 1, 160);
		unkObjFunction0(index, 3, 0);
		unkObjFunction1(index, 3, 115);
		if (checkFlag(tnsportal_flags[world], FLAGTYPE_PERMANENT)) {
			hideObject(behaviour);
			behaviour->next_state = 20;
		} else {
			behaviour->timer = 45;
			behaviour->next_state = 1;
		}
		if (!checkFlag(normal_key_flags[world], FLAGTYPE_PERMANENT)) {
			unkObjFunction2(index, 1, -1);
			unkObjFunction2(index, 3, -1);
		}
	} else if (behaviour->current_state == 1) {
		if (isPlayerInRangeOfObject(60)) {
			behaviour->timer = behaviour->unk_14;
			exitPortalPath(behaviour, index, 1, 0);
			*(char*)(0x807F693F) = 1;
			PlayCutsceneFromModelTwoScript(behaviour, 29, 0, 15);
			setAction(90,0,0);
			behaviour->next_state = 100;
		} else {
			behaviour->next_state = 2;
		}
	} else if (behaviour->current_state == 2) {
		if (behaviour->timer == 0) {
			behaviour->unk_68 = 60;
			behaviour->unk_6A = 60;
			behaviour->unk_6C = 60;
			behaviour->unk_67 = 3;
			behaviour->next_state = 3;
		}
	} else if (behaviour->current_state == 3) {
		if (checkFlag(tnsportal_flags[world], FLAGTYPE_PERMANENT)) {
			hideObject(behaviour);
			behaviour->next_state = 20;
		}
		if ((behaviour->switch_pressed == 1) && (getInteractionOfContactActor(behaviour->contact_actor_type) & 1) && (canHitSwitch())) {
			setSomeTimer(0x2AC);
			behaviour->timer = 5;
			exitPortalPath(behaviour, index, 0, 0);
			*(char*)(0x807F693F) = 1;
			PlayCutsceneFromModelTwoScript(behaviour, 28, 0, 15);
			setAction(89,0,0);
			behaviour->next_state = 4;
		}
	} else if (behaviour->current_state == 4) {
		if (behaviour->timer == 0) {
			enterPortal(Player);
			initiateTransition_0(MAP_TROFFNSCOFF, 0, 0, 3);
			alterParentLocationTNS(id);
			behaviour->next_state = 5;
		}
	} else if (behaviour->current_state == 40) {
		if (behaviour->timer == 0) {
			behaviour->unk_60 = 1;
			behaviour->unk_62 = 0;
			behaviour->unk_66 = 4;
			behaviour->unk_70 = 0;
			playSFXFromObject(index, 994, 255, 127, 20, 10, 0.3f);
			behaviour->next_state = 41;
		}
	} else if (behaviour->current_state == 41) {
		if (unkObjFunction8(index, 2)) {
			exitPortalPath(behaviour, index, 0, 2);
		} else {
			behaviour->next_state = 20;
		}
	} else if (behaviour->current_state == 100) {
		if (behaviour->timer == 0) {
			if (checkFlag(normal_key_flags[world], FLAGTYPE_PERMANENT)) {
				behaviour->timer = 60;
				setPermFlag(tnsportal_flags[world]);
				behaviour->next_state = 40;
			} else {
				behaviour->next_state = 101;
				behaviour->timer = 60;
			}
		}
	} else if (behaviour->current_state == 101) {
		if (behaviour->timer == 0) {
			behaviour->next_state = 2;
		}
	}
}

void TNSIndicatorGenericCode(behaviour_data* behaviour, int index, int id) {
	/**
	 * @brief Generic code for a T&S Portal Indicator
	 * 
	 * @param behaviour Behaviour Pointer for Object
	 * @param index Index of Object in Model Two Array
	 * @param id T&S Portal ID
	 */
	if (behaviour->current_state == 0) {
		for (int i = 0; i < 3; i++) {
			unkObjFunction7(index, 1, 0);
		}
		int world = getWorld(CurrentMap, 0);
		if ((checkFlag(tnsportal_flags[world], FLAGTYPE_PERMANENT)) || (!Rando.tns_indicator)) {
			behaviour->next_state = 2;
		} else {
			behaviour->next_state = 1;
		}
		if (CurrentMap == MAP_JAPES) {
			if (id == 0x220) {
				int* m2location = (int*)ObjectModel2Pointer;
				int slot = convertIDToIndex(0x220);
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
				model_struct* _model = _object->model_pointer;
				if (_model) {
					_model->x = 722.473f;
					_model->z = 2386.608f;
				}
			}
		}
	} else if (behaviour->current_state == 1) {
		int world = getWorld(CurrentMap, 0);
		int display_number = TroffNScoffReqArray[world] - TroffNScoffTurnedArray[world];
		if (display_number < 0) {
			display_number = 0;
		}
		for (int i = 1; i < 4; i++) {
			int tex = (((10-i) + display_number % 10) % 10) - 1;
			if (i == 1) {
				tex = (((10-i) + display_number % 10) % 10);
			}
			displayNumberOnObject(id,i,tex, 0, 0);
			display_number /= 10;
		}
		if (checkFlag(tnsportal_flags[world], FLAGTYPE_PERMANENT)) {
			behaviour->next_state = 2;
		}
	} else if (behaviour->current_state == 2) {
		hideObject(behaviour);
	}
}