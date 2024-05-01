/**
 * @file bananaport.c
 * @author Ballaam
 * @brief Functions related to bananaports
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

typedef struct warp_info_data {
	/* 0x000 */ unsigned char warp_map;
	/* 0x001 */ unsigned char tied_warp_index;
	/* 0x002 */ unsigned short id;
	/* 0x004 */ short active_flag;
	/* 0x006 */ short appear_flag;
	/* 0x008 */ unsigned char tied_exit;
	/* 0x009 */ char unk9;
} warp_info_data;

typedef struct warp_extra_info {
	/* 0x000 */ unsigned short current_index;
	/* 0x002 */ unsigned short tied_index;
} warp_extra_info;

void bananaportGenericCode(behaviour_data* behaviour, int index, int id) {
	/**
	 * @brief Generic code for a bananaport
	 * 
	 * @param behaviour Behaviour Pointer for Object
	 * @param index Index of item in Model Two Array
	 * @param id Object ID of Warp
	 */
	int current_index = 0;
	int tied_index = 0;
	int* warploc = WarpData;
	int* m2location = (int*)ObjectModel2Pointer;
	warp_extra_info* cached_data = (warp_extra_info*)behaviour->extra_data;
	if (!cached_data) {
		cached_data = dk_malloc(4);
		for (int i = 0; i < 90; i++) {
			warp_info_data* warp_info = getObjectArrayAddr(warploc,0xA,i);
			if ((warp_info->id == id) && (warp_info->warp_map == CurrentMap)) {
				cached_data->current_index = i;
				cached_data->tied_index = warp_info->tied_warp_index;
			}
		}
		behaviour->extra_data = cached_data;
	}
	current_index = cached_data->current_index;
	tied_index = cached_data->tied_index;
	warp_info_data* selected_warp = getObjectArrayAddr(warploc,0xA,current_index);
	warp_info_data* tied_warp = getObjectArrayAddr(warploc,0xA,tied_index);
	int float_index = -1;
	if (CurrentMap == MAP_GALLEON) {
		int float_id = -1;
		if (selected_warp->id == 0x6C) {
			float_id = 100;
		} else if (selected_warp->id == 0x56) {
			float_id = 98;
		} else if (selected_warp->id == 0x15) {
			float_id = 99;
		}
		if (float_id > -1) {
			float_index = convertIDToIndex(float_id);
			if (float_index > -1) {
				getObjectPosition(float_index, 1, 1, &collisionPos[0], &collisionPos[1], &collisionPos[2]);
			}
		}
	}
	if (behaviour->current_state == 0) {
		if ((selected_warp->appear_flag > -1) && (Rando.activate_all_bananaports != 1)) {
			// Has an appear flag
			if (checkFlag(selected_warp->appear_flag, FLAGTYPE_PERMANENT)) {
				setPermFlag(selected_warp->active_flag);
			}
			if (checkFlag(selected_warp->appear_flag, FLAGTYPE_PERMANENT)) {
				if (!checkFlag(selected_warp->active_flag, FLAGTYPE_PERMANENT)) {
					behaviour->unk_60 = 1;
					behaviour->unk_62 = 70;
					behaviour->unk_66 = 255;
				}
			}
			if (checkFlag(selected_warp->active_flag, FLAGTYPE_PERMANENT) == 0) {
				behaviour->unk_71 = 0;
				behaviour->unk_60 = 1;
				behaviour->unk_62 = 0;
				behaviour->unk_66 = 255;
				behaviour->next_state = 50;
			}
			if (checkFlag(selected_warp->active_flag, FLAGTYPE_PERMANENT) || checkFlag(selected_warp->appear_flag, FLAGTYPE_PERMANENT)) {
				setScriptRunState(behaviour, RUNSTATE_DISTANCERUN, 300);
				behaviour->next_state = 1;
			}

		} else {
			// Always shown
			if (checkFlag(selected_warp->active_flag, FLAGTYPE_PERMANENT) == 0) {
				behaviour->unk_60 = 1;
				behaviour->unk_62 = 70;
				behaviour->unk_66 = 255;
			}
			int distance = 300;
			if (float_index > -1) {
				distance = 600;
			}
			setScriptRunState(behaviour, RUNSTATE_DISTANCERUN, distance);
			behaviour->next_state = 1;
		}
	} else if (behaviour->current_state == 1) {
		if (Player) {
			if (standingOnM2Object(index)) {
				if (Player->standing_on_subposition == 2) {
					if (checkFlag(selected_warp->active_flag, FLAGTYPE_PERMANENT) == 0) {
						// Play Warp Tagging Effect
						if (Character < 5) {
							// Sparkles
							playSFXFromObject(index, 612, 255, 127, 0, 40, 0.3f);
							behaviour->unk_60 = 0;
							behaviour->unk_62 = 0;
							behaviour->unk_66 = 5;
							setPermFlag(selected_warp->active_flag);
							displayWarpSparkles(behaviour, index, 0, 0);
							// Cutscene
							if (checkFlag(FLAG_FTT_BANANAPORT, FLAGTYPE_PERMANENT) == 0) {
								*(char*)(0x807F693F) = 1;
								PlayCutsceneFromModelTwoScript(behaviour,16,1,0);
								if (float_index == -1) {
									*(char*)(0x807F6902) = 1;
									behaviour->counter_next = 1;
								}
								setPermFlag(FLAG_FTT_BANANAPORT);
							}
						}
					} else {
						if (checkFlag(tied_warp->active_flag, FLAGTYPE_PERMANENT)) {
							// Execute Warp
							if (Character < 5) {
								if (selected_warp->warp_map == tied_warp->warp_map) {
									setObjectScriptState(tied_warp->id, 20, 0);
									int tied_index = convertIDToIndex(tied_warp->id);
									if (tied_index > -1) {
										ModelTwoData* tied_object = getObjectArrayAddr(m2location,0x90,tied_index);
										behaviour_data* tied_behaviour = (behaviour_data*)tied_object->behaviour_pointer;
										if (tied_behaviour) {
											setScriptRunState(tied_behaviour, RUNSTATE_RUNNING, 0);
										}
									}
								} else {
									createCollision(0,Player,COLLISION_MAPWARP,tied_warp->warp_map,tied_warp->tied_exit,0,0,0);
								}
							}
						}
					}
				}
			}
		}
		if (*(unsigned char*)(0x807F6903)) {
			behaviour->next_state = 2;
		}
	} else if (behaviour->current_state == 2) {
		if (*(unsigned char*)(0x807F6903) == 0) {
			behaviour->next_state = 1;
		}
	} else if (behaviour->current_state == 20) {
		if (float_index > -1) {
			ModelTwoData* float_object = getObjectArrayAddr(m2location,0x90,float_index);
			if (float_object->behaviour_pointer) {
				setScriptRunState(float_object->behaviour_pointer, RUNSTATE_RUNNING, 0);
			}
		}
		createCollision(0,Player,COLLISION_BANANAPORT,0,0,*(int*)(0x807F621C),*(int*)(0x807F6220),*(int*)(0x807F6224));
		behaviour->next_state = 0;
	} else if (behaviour->current_state == 50) {
		if ((selected_warp->appear_flag > -1) && (Rando.activate_all_bananaports != 1)) {
			if (checkFlag(selected_warp->appear_flag, FLAGTYPE_PERMANENT)) {
				behaviour->timer = 30;
				behaviour->next_state = 51;
			}
		}
	} else if (behaviour->current_state == 51) {
		if (behaviour->timer == 0) {
			behaviour->timer = 100;
			behaviour->next_state = 52;
		}
	} else if (behaviour->current_state == 52) {
		if (behaviour->timer == 90) {
			playSFXFromObject(index, 747, 255, 127, 0, 0, 0.3f);
			behaviour->unk_71 = 1;
			behaviour->unk_60 = 0;
			behaviour->unk_62 = 0;
			behaviour->unk_66 = 5;
			behaviour->next_state = 0;
			setPermFlag(selected_warp->active_flag);
		}
	}
	if ((behaviour->counter == 1) && (float_index == -1)) {
		if (CutsceneActive != 1) {
			*(char*)(0x807F6902) = 0;
			behaviour->counter_next = 2;
		}
	}
}