/**
 * @file object_instance_script_changes.c
 * @author Ballaam
 * @author OnlySpaghettiCode
 * @brief Contains various hooks from the object instance script assets into C code
 * @version 0.1
 * @date 2022-01-21
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define FUNGI_MINECART_GRATE 0x22
#define SEASICK_SHIP 0x27
#define AZTEC_BEETLE_GRATE 0x1E
#define BALLROOM_MONKEYPORT 0x5
#define MUSEUM_WARP_MONKEYPORT 0x8
#define JAPES_BBLAST 0xA3
#define FACTORY_BBLAST 0x4D
#define CAVES_BBLAST 0x20
#define CASTLE_BBLAST 0x1F
#define AZTEC_BBLAST 0x2E
#define GALLEON_BBLAST 0x34
#define FUNGI_BBLAST 0x4C
#define AZTEC_SNOOPDOOR 0xA1
#define LLAMA_SNOOPPAD 0x69
#define JAPES_DKCAGEGB 0x44
#define JAPES_DKCAGESWITCH 0x40
#define JAPES_MOUNTAINGB 0x52
#define JAPES_MOUNTAINGBSWITCH 0x6
#define FACTORY_DIDDYPRODGB 0x2C
#define FACTORY_DIDDYPRODSWITCH 0x31
#define MILL_WARNINGLIGHTS 0xC
#define MILL_CRUSHER 0x8
#define MILL_TRIANGLEPAD 0x0
#define GMUSH_BOARD 0xB
#define CAVES_GBDOME 0x27
#define CAVES_BOULDERDOME 0x2B
#define CAVES_SMALLBOULDERPAD 0x2E
#define CAVES_BIGBOULDERPAD 0x2F
#define GALLEON_DKSTAR 0xC
#define AZTEC_LLAMACOCONUT 0xD
#define FUNGI_MILLGBINTERIOR 0xA

#define GALLEON_BONGO_PAD 0x11
#define GALLEON_GUITAR_CACTUS_PAD 0x14
#define GALLEON_SAX_PAD 0x13
#define GALLEON_TROMBONE_PAD 0x12
#define GALLEON_TRIANGLE_PAD 0x1B
#define GALLEON_LANKY_SLAM 0x1D
#define GALLEON_TINY_SLAM 0x1C

#define GALLEON_DK_5DSDOOR 0x19
#define GALLEON_DIDDY_5DSDOOR 0x1A
#define GALLEON_LANKY_5DSDOOR 0x17
#define GALLEON_TINY_5DSDOOR 0x18
#define GALLEON_CHUNKY_5DSDOOR 0x20
#define GALLEON_LANKY_2DSDOOR 0x1F
#define GALLEON_TINY_2DSDOOR 0x1E

#define TGROUNDS_BAMBOOGATE 0x49
#define TGROUNDS_SWITCH 0x39
#define JAPES_DIDDYBAMBOOGATE 0x47
#define JAPES_GATE0 0x2D
#define JAPES_GATE1 0x2E
#define JAPES_GATE2 0x2F
#define JAPES_GUNSWITCH0 0x30
#define JAPES_GUNSWITCH1 0x31
#define JAPES_GUNSWITCH2 0x32
#define JAPES_DIDDYFREEGB 0x48
#define LLAMA_BAMBOOGATE 0x11
#define LLAMA_GUNSWITCH 0x12
#define LLAMA_BONGOPAD 0x16
#define LLAMA_LAVAGATE 0x18
#define TTEMPLE_SWITCH 0x0
#define TTEMPLE_GUITARPAD 0x4
#define TTEMPLE_KONGLETTER0 0xC
#define TTEMPLE_KONGLETTER1 0xD
#define TTEMPLE_KONGLETTER2 0xE
#define TTEMPLE_KONGLETTER3 0xF
#define TTEMPLE_BAMBOOGATE 0x15
#define TTEMPLE_CHARGESWITCH 0x14
#define FACTORY_FREESWITCH 0x24
#define FACTORY_CAGE 0x21
#define FACTORY_FREEGB 0x78

#define FACTORY_4231_SWITCH 0x3F
#define FACTORY_3124_SWITCH 0x40
#define FACTORY_1342_SWITCH 0x41

#define ISLES_JAPESBOULDER 0x3
#define ISLES_AZTECDOOR 0x02
#define ISLES_FACTORYPLATFORM 0x05
#define ISLES_FACTORYDOOR 0x06
#define ISLES_GALLEONBARS 0x1A
#define ISLES_FUNGIBOULDER 0x21
#define ISLES_CAVESBOULDER 0x1B
#define ISLES_CASTLEROCK 0x34
#define ISLES_HELMJAW 0x1C
#define ISLES_FACTORYDOORCOLLISION 0x100

#define ISLES_LOWMONKEYPORT 0x38

#define CHUNKY5DC_GGONE 0x6
#define CHUNKY5DC_TARGET0 0x3
#define CHUNKY5DC_TARGET1 0x4
#define CHUNKY5DC_TARGET2 0x5
#define HELMLOBBY_GGONE 0x3

#define LLAMA_MATCHING_HEAD_SOUND0_0 0x1E // Sound 173
#define LLAMA_MATCHING_HEAD_SOUND0_1 0x23
#define LLAMA_MATCHING_HEAD_SOUND1_0 0x24 // Sound 171
#define LLAMA_MATCHING_HEAD_SOUND1_1 0x27
#define LLAMA_MATCHING_HEAD_SOUND2_0 0x1B // Sound 169
#define LLAMA_MATCHING_HEAD_SOUND2_1 0x26
#define LLAMA_MATCHING_HEAD_SOUND3_0 0x1D // Sound 174
#define LLAMA_MATCHING_HEAD_SOUND3_1 0x21
#define LLAMA_MATCHING_HEAD_SOUND4_0 0x1A // Sound 172
#define LLAMA_MATCHING_HEAD_SOUND4_1 0x25
#define LLAMA_MATCHING_HEAD_SOUND5_0 0x20 // Sound 175
#define LLAMA_MATCHING_HEAD_SOUND5_1 0x22
#define LLAMA_MATCHING_HEAD_SOUND6_0 0x19 // Sound 168
#define LLAMA_MATCHING_HEAD_SOUND6_1 0x1F
#define LLAMA_MATCHING_HEAD_SOUND7_0 0x1C // Sound 170
#define LLAMA_MATCHING_HEAD_SOUND7_1 0x28

#define FISH_SHIELD1 0x3
#define FISH_SHIELD2 0x4
#define FISH_SHIELD3 0x5

#define CHEST_PEARL_0 0x0
#define MILLREAR_CHUNKYCHECK_RATE 0xF
#define ROTATING_ROOM_OBJ 0x0
#define FUNGI_BEAN 0x5
#define FUNGI_BEANCONTROLLER 0x4D

#define FACTORY_LARGEMETALSECTION 0x0
#define FACTORY_PIANO 0x14
#define FACTORY_DARTBOARD 0x7F
#define ICE_MAZE 0x0

#define HELM_PAD_BONGO 0x2C
#define HELM_PAD_TRIANGLE 0x2D
#define HELM_PAD_SAX 0x2E
#define HELM_PAD_TROMBONE 0x2F
#define HELM_PAD_GUITAR 0x30
#define HELM_COIN_DOOR 0x3

#define JAPES_CAVE_GATE 0x2B
#define JAPES_PEANUT_MOUNTAIN 0x58
#define JAPES_COCONUT_RAMBI 0x123
#define LLAMA_GRAPE_SWITCH 0x6B
#define FACTORY_SNATCH_GRATE 0x15
#define FACTORY_PAD_TRIANGLE 0x37
#define FACTORY_PAD_GUITAR 0x38
#define FACTORY_PAD_TROMBONE 0x3B
#define ISLES_SWITCH_GRAPE 0x27
#define ISLES_SWITCH_PINEAPPLE 0x28
#define ISLES_SWITCH_FEATHER 0x29
#define ISLES_SWITCH_PEANUT 0x2A
#define ISLES_SWITCH_COCONUT 0x32
#define AZTEC_CHUNKY_CAGE 0x24
#define CRYPT_LT_GRAPE 0x0
#define CRYPT_LT_SIMIAN_SWITCH 0x4
#define CRYPT_DDC_D 0xD
#define CRYPT_DDC_E 0xE
#define CRYPT_DDC_F 0xF
#define DUNGEON_SLAM_DIDDY 0x4
#define DUNGEON_SLAM_DK 0x5
#define DUNGEON_SLAM_LANKY 0x6
#define TREE_DOOR_DK 0x1
#define TREE_DOOR_CHUNKY 0x9

#define TNS_NUMBER 0x15
#define TNS_ITEMINDICATOR 0xF

#define CROWN_CONTROLLER 0x0
#define CROWN_INDICATOR 0x4

#define FACTORY_BLOCKELEVATOR_0 0x18
#define FACTORY_BLOCKELEVATOR_1 0x19
#define FACTORY_BLOCKELEVATOR_2 0x1A
#define FACTORY_BLOCKELEVATOR_3 0x1B
#define FACTORY_BLOCKELEVATOR_4 0x1C
#define FACTORY_BLOCKELEVATOR_5 0x27
#define FACTORY_BLOCKELEVATOR_6 0x28

#define FACTORY_BBLAST_STAR 0x0
#define FACTORY_BBLAST_CONTROLLER 0x1

#define JAPES_RAMBI_DOOR 0x115

void hideObject(behaviour_data* behaviour_pointer) {
	/**
	 * @brief Hide object model 2 item and make it intangible
	 * 
	 * @param behaviour_pointer Behaviour Pointer of Object
	 */
	behaviour_pointer->unk_60 = 1;
	behaviour_pointer->unk_62 = 0;
	behaviour_pointer->unk_66 = 255;
	behaviour_pointer->unk_70 = 0;
	behaviour_pointer->unk_71 = 0;
	setScriptRunState(behaviour_pointer,2,0);
}
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

void getModelTwoItemFromActor(int actor, short* item, float* scale) {
	/**
	 * @brief Converts actor into it's model two equivalent
	 * 
	 * @param actor Actor Index
	 * @param item Address to store item model two index
	 * @param scale Address to store item scale
	 */
	for (int i = 0; i < (sizeof(item_conversions) / sizeof(item_conversion_info)); i++) {
		if (actor == item_conversions[i].actor) {
			*item = item_conversions[i].model_two;
			*scale = item_conversions[i].scale;
			return;
		}	
	}
}

void spawnWrinklyWrapper(behaviour_data* behaviour, int index, int kong, int unk0) {
	setPermFlag(FLAG_WRINKLYVIEWED + kong + (5 * getWorld(CurrentMap, 0)));
	spawnWrinkly(behaviour, index, kong, unk0);
}

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
				setScriptRunState(behaviour,3,300);
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
			setScriptRunState(behaviour,3,distance);
			behaviour->next_state = 1;
		}
	} else if (behaviour->current_state == 1) {
		if (Player) {
			if (Player->touching_object == 1) {
				if (Player->standing_on_index == index) {
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
												setScriptRunState(tied_behaviour,1,0);
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
				setScriptRunState(float_object->behaviour_pointer,1,0);
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

/*
	Shops done:
		Candy
		Funky
		Cranky
		Snides

	Shops not done:
		Floating Candy
		Floating Funky
*/

void shopGenericCode(behaviour_data* behaviour, int index, int id, vendors shop) {
	// Generic Shop Vars
	int range_setting = 4;
	int range_setting_0 = 41;
	int head_icon = 0;
	int appear_sfx = 0;
	int disappear_timer_check = 0;
	int disappear_sfx = 0;
	int disappear_param = 80;
	int disappear_param_0 = 2;
	int init_setting = 0;
	int init_setting_0 = 2;
	int init_setting_1 = 20;
	int appear_subparam = 2;
	int appear_volume = 127;
	int floating_id = -1;
	if (CurrentMap == MAP_GALLEON) {
		if (id == 94) {
			floating_id = 54;
		} else if (id == 500) {
			floating_id = 501;
		}
	}
	if (shop == SHOP_CANDY) {
		range_setting = 2;
		head_icon = 0;
		appear_sfx = 815;
		disappear_timer_check = 8;
		disappear_sfx = 816;
	} else if (shop == SHOP_FUNKY) {
		range_setting = 3;
		head_icon = 2;
		appear_sfx = 814;
		disappear_timer_check = 12;
		disappear_sfx = 814;
		init_setting = 3;
	} else if (shop == SHOP_CRANKY) {
		init_setting = 4;
		init_setting_0 = 3;
		range_setting_0 = 50;
		head_icon = 1;
		disappear_param = 120;
		disappear_param_0 = 4;
	} else if (shop == SHOP_SNIDE) {
		init_setting_1 = 15;
		init_setting_0 = 4;
		range_setting_0 = 28;
		head_icon = 3;
		disappear_param = 50;
		disappear_param_0 = 4;
		appear_sfx = 74;
		appear_subparam = 4;
		appear_volume = 95;
	}
	// Script
	if (floating_id > -1) {
		int float_index = convertIDToIndex(floating_id);
		if (float_index > -1) {
			getObjectPosition(float_index, 1, 1, &collisionPos[0], &collisionPos[1], &collisionPos[2]);
		}
		float x_0 = 0;
		float y_0 = 0;
		float z_0 = 0;
		getObjectPosition(index, 1, 1, &x_0, &y_0, &z_0);
		unkObjFunction15(17, x_0, y_0, z_0);
	}
	if (behaviour->current_state == 0) {
		if ((shop == SHOP_FUNKY) || (shop == SHOP_CRANKY)) {
			unkObjFunction1(index, init_setting, 20);
			unkObjFunction9(index, init_setting, 1);
		}
		int set = 100;
		if (floating_id > -1) {
			set = 120;
		}
		behaviour->unk_68 = set;
		behaviour->unk_6A = set;
		behaviour->unk_6C = set;
		behaviour->unk_67 = 4;
		unkObjFunction1(index, init_setting_0, init_setting_1);
		unkObjFunction9(index, init_setting_0, 1);
		if (shop == SHOP_CRANKY) {
			unkObjFunction1(index, 2, 80);
		}
		unkObjFunction9(index, 1, 1);
		unkObjFunction0(index, 1, 1);
		unkObjFunction1(index, 1, 0);
		if (isPlayerInRangeOfObject(400)) {
			unkObjFunction2(index, range_setting, 65535);
			unkObjFunction10(index, 1, range_setting_0, 1);
			unkObjFunction2(index, 1, 1);
			behaviour->next_state = 1;
			if (shop == SHOP_SNIDE) {
				setScriptRunState(behaviour, 1, 0);
				*(char*)(0x80748094) = 1;
				if (behaviour->unk_10 < 0) {
					behaviour->unk_10 = unkObjFunction12(index, 295, 80, 0, 50, 1.0f, *(char*)(0x80748094)); // Snides update
				}
			}
		} else {
			behaviour->unk_60 = 1;
			behaviour->unk_62 = 0;
			behaviour->unk_66 = 255;
			unkObjFunction10(index, 1, 0, 0);
			unkObjFunction2(index, 1, 1);
			behaviour->next_state = 5;
		}
	} else if (behaviour->current_state == 1) {
		if (((shop == SHOP_CANDY) || (shop == SHOP_FUNKY)) && (floating_id == -1)) {
			setScriptRunState(behaviour, 1, 0);
		}
		unkObjFunction11(index, 1);
		behaviour->next_state = 12;
	} else if (behaviour->current_state == 5) {
		unkObjFunction11(index, 1);
		behaviour->next_state = 10;
	} else if (behaviour->current_state == 10) {
		if (isPlayerInRangeOfObject(1000)) {
			displayShopIcon(behaviour, index, head_icon, 0);
		}
		if (isPlayerInRangeOfObject(400)) {
			behaviour->unk_60 = 0;
			behaviour->unk_62 = 0;
			behaviour->unk_66 = 255;
			unkObjFunction1(index, 1, disappear_param);
			unkObjFunction2(index, 1, 1);
			behaviour->next_state = 11;
			if (floating_id == -1) {
				setScriptRunState(behaviour, 1, 0);
			}
			if (shop != SHOP_CRANKY) {
				playSFXFromObject(index, appear_sfx, 255, appear_volume, 0, 40, 0.3f);
				unkObjFunction2(index, appear_subparam, 65535);
			} else {
				if (behaviour->unk_10 < 0) {
					behaviour->unk_10 = unkObjFunction12(index, 256, 40, 0, 255, 1.0f, 0);
				}
				unkObjFunction13((behaviour->unk_10) & 0xFF, 90, 20);
			}
			if ((shop == SHOP_CRANKY) || (shop == SHOP_FUNKY)) {
				behaviour->timer = 18;
				unkObjFunction2(index, init_setting, 65535);
			}
			if (shop == SHOP_SNIDE) {
				*(char*)(0x80748094) = 1;
				if (behaviour->unk_10 < 0) {
					behaviour->unk_10 = unkObjFunction12(index, 295, 80, 0, 50, 1.0f, *(char*)(0x80748094));
				}
				unkObjFunction2(index, 4, 65535);
			}
		}
	} else if (behaviour->current_state == 11) {
		if (shop == SHOP_FUNKY) {
			if (behaviour->timer == 1) {
				playSFXFromObject(index, 91, 255, 127, 0, 40, 0.3f);
			}
		}
		if (!unkObjFunction8(index, 1)) {
			if (shop == SHOP_CRANKY) {
				if (behaviour->unk_10 > -1) {
					unkObjFunction14(behaviour->unk_10);
					behaviour->unk_10 = -1;
				}
			}
			behaviour->next_state = 12;
		}
	} else if (behaviour->current_state == 12) {
		if (shop != SHOP_SNIDE) {
			hideShop(behaviour, index, 1, 0);
		}
		if (shop == SHOP_CRANKY) {
			if (behaviour->timer == 0) {
				if (!unkObjFunction8(index, 2)) {
					unkObjFunction10(index, 2, 0, 0);
					unkObjFunction2(index, 2, 1);
					behaviour->timer = 100;
				}
			}
			if (behaviour->unk_46 == 0) {
				if (!unkObjFunction8(index, 3)) {
					unkObjFunction10(index, 3, 0, 0);
					unkObjFunction2(index, 3, 1);
					behaviour->timer = 150;
				}
			}
		}
		if (!isPlayerInRangeOfObject(500)) {
			unkObjFunction11(index, disappear_param_0);
			unkObjFunction1(index, 1, disappear_param);
			unkObjFunction2(index, 1, 1);
			behaviour->next_state = 13;
			if (shop == SHOP_FUNKY) {
				unkObjFunction11(index, 3);
			} else if (shop == SHOP_CRANKY) {
				if (behaviour->unk_10 < 0) {
					behaviour->unk_10 = unkObjFunction12(index, 256, 40, 0, 255, 1.0f, 0);
				}
				unkObjFunction13((behaviour->unk_10) & 0xFF, 70, 20);
			} else if (shop == SHOP_SNIDE) {
				if (behaviour->unk_10 > -1) {
					unkObjFunction14(behaviour->unk_10);
					behaviour->unk_10 = -1;
				}
			}
			behaviour->timer = 18;
		}
	} else if (behaviour->current_state == 13) {
		if ((behaviour->timer == disappear_timer_check) && (shop != SHOP_CRANKY) && (shop != SHOP_SNIDE)) {
			playSFXFromObject(index, disappear_sfx, 255, 127, 0, 40, 0.3f);
		} else if (behaviour->timer == 0) {
			playSFXFromObject(index, 661, 255, 127, 0, 40, 0.3f);
			behaviour->next_state = 14;
		}
	} else if (behaviour->current_state == 14) {
		if (!unkObjFunction8(index, 1)) {
			if (shop == SHOP_CRANKY) {
				if (behaviour->unk_10 > -1) {
					unkObjFunction14(behaviour->unk_10);
					behaviour->unk_10 = -1;
				}
			}
			behaviour->unk_60 = 1;
			behaviour->unk_62 = 0;
			behaviour->unk_66 = 255;
			setScriptRunState(behaviour, 0, 0);
			behaviour->next_state = 10;
		}
	}
}

static const short tnsportal_flags[] = {
	FLAG_PORTAL_JAPES,
	FLAG_PORTAL_AZTEC,
	FLAG_PORTAL_FACTORY,
	FLAG_PORTAL_GALLEON,
	FLAG_PORTAL_FUNGI,
	FLAG_PORTAL_CAVES,
	FLAG_PORTAL_CASTLE,
};

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
				behaviour->next_state = 2;
			}
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

static const int crown_maps_flags[] = {
	MAP_BATTLEARENA_BEAVERBRAWL, // Japes
	MAP_BATTLEARENA_KRITTERKARNAGE, // Aztec
	MAP_BATTLEARENA_ARENAAMBUSH, // Factory
	MAP_BATTLEARENA_MOREKRITTERKARNAGE, // Galleon
	MAP_BATTLEARENA_KAMIKAZEKREMLINGS, // Fungi
	MAP_BATTLEARENA_FORESTFRACAS, // Fungi Lobby
	MAP_BATTLEARENA_BISHBASHBRAWL, // Snide's
	MAP_BATTLEARENA_PLINTHPANIC, // Caves
	MAP_BATTLEARENA_PINNACLEPALAVER, // Castle
	MAP_BATTLEARENA_SHOCKWAVESHOWDOWN, // Helm
};

void CrownPadGenericCode(behaviour_data* behaviour, int index, int id, int crown_level_index) {
	/**
	 * @brief Generic code for a Crown Pad
	 * 
	 * @param behaviour Behaviour Pointer for Object
	 * @param index Index of Object in Model Two Array
	 * @param id Crown Pad ID
	 */
	if (behaviour->current_state == 0) {
		setScriptRunState(behaviour, 3, 900);
		behaviour->next_state = 1;
	}
	int world = getWorld(CurrentMap, 1);
	int crown_offset = world;
	if (world > 4) {
		if (world < 7) {
			crown_offset = world + 2;
		} else if (world == 7) {
			crown_offset = 5 + crown_level_index;
		} else {
			crown_offset = 9;
		}
	}
	if (checkFlag(FLAG_CROWN_JAPES + crown_offset, FLAGTYPE_PERMANENT)) {
		behaviour->unk_71 = 0;
		behaviour->unk_60 = 1;
		behaviour->unk_62 = 0;
		behaviour->unk_66 = 255;
		setScriptRunState(behaviour, 2, 0);
	}
	if (Player) {
		if ((Player->obj_props_bitfield & 0x2000) == 0) {
			if ((Player->characterID >= 2) && (Player->characterID <= 6)) {
				if (Player->touching_object == 1) {
					if (index == Player->standing_on_index) {
						if (!checkFlag(FLAG_FTT_CROWNPAD, FLAGTYPE_PERMANENT)) {
							setPermFlag(FLAG_FTT_CROWNPAD);
							*(char*)(0x807F693F) = 1;
							PlayCutsceneFromModelTwoScript(behaviour, 24, 1, 0);
							behaviour->next_state = 2;
						}
						if (Player->standing_on_subposition == 2) {
							if (behaviour->current_state >= 0) {
								createCollision(0, Player, COLLISION_BATTLE_CROWN, crown_maps_flags[crown_offset], 2, collisionPos[0], collisionPos[1], collisionPos[2]);
							}
						}
					}
				}
			}
		}
	}
}

int isBonus(int map) {
	/**
	 * @brief Is map queried a bonus map
	 * 
	 * @param map Map index being queried
	 * 
	 * @return Is bonus map (bool)
	 */
	if (map == 0x50) {
		return 0;
	}
	int level = levelIndexMapping[map];
	return (level == 9) || (level == 0xD);
}

static const unsigned char kong_press_states[] = {0x29,0x2E,0x26,0x29,0x24};
static const unsigned char kong_pellets[] = {48,36,42,43,38};
#define MILL_CRUSHER_PROGRESS 1

int getPressedSwitch(behaviour_data* behaviour_pointer, int bullet_type, int ID) {
	/**
	 * @brief Detect if switch is being hit by a bullet of a certain type
	 * 
	 * @param behaviour_pointer Behaviour Pointer of Object
	 * @param bullet_type Actor Type of bullet that is expected to be made contact with
	 * @param ID Switch Object ID
	 * 
	 * @return Switch is being pressed
	 */
	if (behaviour_pointer->switch_pressed == 1) {
		if (behaviour_pointer->contact_actor_type == bullet_type) {
			if (canHitSwitch()) {
				int index = convertSubIDToIndex(ID);
				int* m2location = (int*)ObjectModel2Pointer;
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
				setSomeTimer(_object->object_type);
				return 1;
			}
		}
	}
	return 0;
}

void setCrusher(void) {
	/**
	 * @brief Set the Crusher in the Fungi Mill to be the correct object state
	 */
	if (CurrentMap == MAP_FUNGIMILLFRONT) {
		if ((ObjectModel2Timer < 10) && (ObjectModel2Timer > 5)) {
			int crusher_index = convertIDToIndex(8);
			int* m2location = (int*)ObjectModel2Pointer;
			if (crusher_index > -1) {
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,crusher_index);
				if (_object) {
					behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
					if (behaviour) {
						if (behaviour->counter == 0) {
							behaviour->counter = MILL_CRUSHER_PROGRESS;
						}
					}
				}
			}
		}
	}
}

int checkControlState(int target_control_state) {
	/**
	 * @brief Check control state of the player to see if player is making the correct contact with the item
	 * 
	 * @param target_control_state Control state which the player is required to be in
	 * 
	 * @return Is the correct control state and control state progress
	 */
	if (Player) {
		if (Player->control_state == target_control_state) {
			if (target_control_state == 0x24) {
				if (Player->control_state_progress == 2) {
					return 1;
				}
			} else {
				if (Player->control_state_progress == 1) {
					return 1;
				}
			}
		}
	}
	return 0;
}

int checkSlamLocation(int kong, int key, int id) {
	/**
	 * @brief Check slam location
	 * 
	 * @param kong Required kong
	 * @param key Index in Object Model Two Array
	 * @param id Object ID of target
	 */
	if (Character == kong) {
		if (Player) {
			if ((Player->obj_props_bitfield & 0x2000) == 0) {
				if (Player->touching_object == 1) {
					if (id == Player->standing_on_index) {
						if (Player->standing_on_subposition == key) {
							return 1;
						}
					}
				}
			}
		}
	}
	return 0;
}

void playSFXContainer(int id, int vanilla_sfx, int new_sfx) {
	/**
	 * @brief Container function for playing a SFX from an object
	 * 
	 * @param id Object ID
	 * @param vanilla_sfx Original SFX
	 * @param new_sfx New SFX to be played. If 0, defaults to vanilla_sfx
	 */
	int index = convertIDToIndex(id);
	if (index == -1) {
		index = 0;
	}
	int sfx_played = new_sfx;
	if (new_sfx == 0) {
		sfx_played = vanilla_sfx;
	}
	playSFXFromObject(index,sfx_played,-1,127,0,0,0.3f);
}

int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2) {
	/**
	 * @brief Perform object script instructions. Can be called either through
	 * COND 6 | 7 index param2
	 * or
	 * EXEC 7 | 125 index param2
	 */
	if (index >= 0) {
		switch(CurrentMap) {
			case MAP_GALLEON:
				{
					int gate_index = -1;
					int gate_flag = -1;
					switch (param2) {
						case SEASICK_SHIP:
							if (Rando.randomize_more_loading_zones) {
								initiateTransition_0((Rando.seasick_ship_enter >> 8) & 0xFF, Rando.seasick_ship_enter & 0xFF, 0, 0);
							} else {
								initiateTransition_0(MAP_GALLEONSEASICKSHIP, 0, 0, 0);
							}
							break;
						case GALLEON_DKSTAR:
							{
								int progress = 1;
								if (Rando.quality_of_life.galleon_star) {
									progress = 3;
								}
								behaviour_pointer->next_state = progress;
							}
							break;
						case GALLEON_BONGO_PAD:
						case GALLEON_GUITAR_CACTUS_PAD:
						case GALLEON_TRIANGLE_PAD:
						case GALLEON_SAX_PAD:
						case GALLEON_TROMBONE_PAD:
						case GALLEON_LANKY_SLAM:
						case GALLEON_TINY_SLAM:
							if (index == 0) { 
								return !Rando.remove_high_requirements;
							} else {
								if (Rando.remove_high_requirements) {
									behaviour_pointer->next_state = 6;
								} else {
									behaviour_pointer->next_state = 5;
								}
							}
							break;
						case GALLEON_DK_5DSDOOR:
							gate_index = 0;
							gate_flag = GALLEON_5DSOPEN_DK;
						case GALLEON_DIDDY_5DSDOOR:
							if (gate_index < 0) {
								gate_index = 1;
								gate_flag = GALLEON_5DSOPEN_DIDDY;
							}
						case GALLEON_LANKY_5DSDOOR:
							if (gate_index < 0) {
								gate_index = 2;
								gate_flag = GALLEON_5DSOPEN_LANKY;
							}
						case GALLEON_TINY_5DSDOOR:
							if (gate_index < 0) {
								gate_index = 3;
								gate_flag = GALLEON_5DSOPEN_TINY;
							}
						case GALLEON_CHUNKY_5DSDOOR:
							if (gate_index < 0) {
								gate_index = 4;
								gate_flag = GALLEON_5DSOPEN_CHUNKY;
							}
						case GALLEON_LANKY_2DSDOOR:
							if (gate_index < 0) {
								gate_index = 5;
								gate_flag = GALLEON_2DSOPEN_LANKY;
							}
						case GALLEON_TINY_2DSDOOR:
							if (gate_index < 0) {
								gate_index = 6;
								gate_flag = GALLEON_2DSOPEN_TINY;
							}
							if (index == 0) {
								if (Rando.remove_high_requirements) {
									if (checkFlag(gate_flag, FLAGTYPE_PERMANENT)) {
										behaviour_pointer->current_state = 10;
										behaviour_pointer->next_state = 10;
									}
								}
							} else {
								if (Rando.remove_high_requirements) {
									setPermFlag(gate_flag);
								}
							}
						break;
					}
				}
				break;
			case MAP_AZTEC:
				if (param2 == AZTEC_BEETLE_GRATE) {
					if (Rando.randomize_more_loading_zones) {
						initiateTransition_0((Rando.aztec_beetle_enter >> 8) & 0xFF, Rando.aztec_beetle_enter & 0xFF, 0, 0);
					} else {
						initiateTransition_0(MAP_AZTECBEETLE, 0, 0, 0);
					}
				} else if (param2 == AZTEC_SNOOPDOOR) {
					if (index == 0) {
						// Flag Check
						if (checkFlag(SNOOPDOOR_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->next_state = 40;
							behaviour_pointer->current_state = 40;
						}
					} else if (index == 1) {
						// Flag Set
						setPermFlag(SNOOPDOOR_OPEN);
						setNextTransitionType(0);
					}
				} else if (param2 == AZTEC_LLAMACOCONUT) {
					if (!Rando.quality_of_life.remove_cutscenes) {
						PlayCutsceneFromModelTwoScript(behaviour_pointer,23,1,0);
					}
				} else if (param2 == AZTEC_CHUNKY_CAGE) {
					return !Rando.tag_anywhere;
				}
				break;
			case MAP_FUNGI:
				if (param2 == FUNGI_MINECART_GRATE) {
					if (Rando.randomize_more_loading_zones) {
						initiateTransition_0((Rando.fungi_minecart_enter >> 8) & 0xFF, Rando.fungi_minecart_enter & 0xFF, 0, 0);
					} else {
						initiateTransition_0(MAP_FUNGIMINECART, 0, 0, 0);
					}
				} else if (param2 == FUNGI_BEANCONTROLLER) {
					return checkFlagDuplicate(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
				}
				break;
			case MAP_CASTLEBALLROOM:
				if (param2 == BALLROOM_MONKEYPORT) {
					if (Rando.randomize_more_loading_zones) {
						createCollisionObjInstance(COLLISION_MAPWARP,(Rando.ballroom_to_museum >> 8 & 0xFF), Rando.ballroom_to_museum & 0xFF);
					} else {
						createCollisionObjInstance(COLLISION_MAPWARP,113,2);
					}
				}
				break;
			case MAP_CASTLEMUSEUM:
				if (param2 == MUSEUM_WARP_MONKEYPORT) {
					if (Rando.randomize_more_loading_zones) {
						createCollisionObjInstance(COLLISION_MAPWARP,(Rando.museum_to_ballroom >> 8 & 0xFF), Rando.museum_to_ballroom & 0xFF);
					} else {
						createCollisionObjInstance(COLLISION_MAPWARP,88,1);
					}
				}
				break;
			case MAP_ISLES:
				if (param2 == ISLES_JAPESBOULDER) {
					if (Rando.lobbies_open_bitfield & 1) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_AZTECDOOR) {
					if (Rando.lobbies_open_bitfield & 2) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_FACTORYPLATFORM) {
					if (Rando.lobbies_open_bitfield & 4) {
						behaviour_pointer->next_state = 5;
						unkObjFunction0(id,1,0);
						unkObjFunction1(id,1,5);
						unkObjFunction2(id,1,1);
					}
				} else if (param2 == ISLES_FACTORYDOOR) {
					if (Rando.lobbies_open_bitfield & 4) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_FACTORYDOORCOLLISION) {
					if ((Rando.lobbies_open_bitfield & 4) || (checkFlag(FLAG_KEYIN_KEY2, FLAGTYPE_PERMANENT) || ((CutsceneIndex == 7) && (CutsceneActive == 1) && ((CutsceneStateBitfield & 4) == 0)))) {
						hideObject(behaviour_pointer);
						behaviour_pointer->next_state = 1;
					}
				} else if (param2 == ISLES_GALLEONBARS) {
					if (Rando.lobbies_open_bitfield & 8) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_FUNGIBOULDER) {
					if (Rando.lobbies_open_bitfield & 0x10) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_CAVESBOULDER) {
					if (Rando.lobbies_open_bitfield & 0x20) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_CASTLEROCK) {
					if (Rando.lobbies_open_bitfield & 0x40) {
						hideObject(behaviour_pointer);
					}
				} else if (param2 == ISLES_HELMJAW) {
					if (Rando.lobbies_open_bitfield & 0x80) {
						behaviour_pointer->current_state = 100;
						behaviour_pointer->next_state = 100;
						unkObjFunction1(id,2,25);
						unkObjFunction2(id,2,1);
						unkObjFunction2(id,3,1);
					}
				} else if ((param2 == ISLES_SWITCH_COCONUT) || (param2 == ISLES_SWITCH_PEANUT) || (param2 == ISLES_SWITCH_GRAPE) || (param2 == ISLES_SWITCH_FEATHER) || (param2 == ISLES_SWITCH_PINEAPPLE)) {
					return !Rando.tag_anywhere;
				} else if (param2 == ISLES_LOWMONKEYPORT) {
					if (index == 0) {
						int gb_count = 0;
						for (int kong = 0; kong < 5; kong++) {
							for (int level = 0; level < 8; level++) {
								gb_count += MovesBase[kong].gb_count[level];
							}
						}
						int max_gbs = 0;
						for (int level = 0; level < 7; level++) {
							if (BLockerDefaultArray[level] > max_gbs) {
								max_gbs = BLockerDefaultArray[level];
							}
						}
						return (gb_count >= max_gbs) && (Rando.microhints != MICROHINTS_NONE); 
					} else if (index == 1) {
						if (Player) {
							if ((Player->obj_props_bitfield & 0x2000) == 0) {
								if (Player->touching_object == 1) {
									if (Player->standing_on_index == id) {
										return (Player->characterID == 5) || (Rando.perma_lose_kongs);
									}
								}
							}
						}
						return 0;
					}
				} else {
					// TestVariable = (int)behaviour_pointer;
					// *(int*)(0x807FF700) = id;
				}
				break;
			case MAP_AZTECLLAMATEMPLE:
				if (param2 == LLAMA_SNOOPPAD) {
					if (checkFlag(SNOOPDOOR_OPEN, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == LLAMA_BONGOPAD) {
					return Character == Rando.free_source_llama;
				} else if (param2 == LLAMA_LAVAGATE) {
					if (Rando.quality_of_life.remove_cutscenes) {
						hideObject(behaviour_pointer);
						behaviour_pointer->pause_state = 1;
					}
				} else if (param2 == LLAMA_BAMBOOGATE) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_llama), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_llama), FLAGTYPE_PERMANENT);
					}
				} else if (param2 == LLAMA_GUNSWITCH) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_llama), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_llama), FLAGTYPE_PERMANENT);
					} else if (index == 2) {
						setPermFlag(getKongFlag(Rando.free_target_llama));
					} else if ((index >= 3) && (index <= 6)) {
						return getPressedSwitch(behaviour_pointer,kong_pellets[(int)Rando.free_source_llama],id);
					}
				} else if (param2 == LLAMA_GRAPE_SWITCH) {
					return !Rando.tag_anywhere;
				} else {
					int head_ids[] = {
						LLAMA_MATCHING_HEAD_SOUND0_0,
						LLAMA_MATCHING_HEAD_SOUND0_1,
						LLAMA_MATCHING_HEAD_SOUND1_0,
						LLAMA_MATCHING_HEAD_SOUND1_1,
						LLAMA_MATCHING_HEAD_SOUND2_0,
						LLAMA_MATCHING_HEAD_SOUND2_1,
						LLAMA_MATCHING_HEAD_SOUND3_0,
						LLAMA_MATCHING_HEAD_SOUND3_1,
						LLAMA_MATCHING_HEAD_SOUND4_0,
						LLAMA_MATCHING_HEAD_SOUND4_1,
						LLAMA_MATCHING_HEAD_SOUND5_0,
						LLAMA_MATCHING_HEAD_SOUND5_1,
						LLAMA_MATCHING_HEAD_SOUND6_0,
						LLAMA_MATCHING_HEAD_SOUND6_1,
						LLAMA_MATCHING_HEAD_SOUND7_0,
						LLAMA_MATCHING_HEAD_SOUND7_1,
					};
					int head_sounds[] = {173,171,169,174,172,175,168,170};
					int selection = -1;
					for (int k = 0; k < sizeof(head_ids)/4; k++) {
						if (param2 == head_ids[k]) {
							selection = k / 2;
						}
					}
					if (selection > -1) {
						playSFXContainer(param2,head_sounds[selection],Rando.matching_game_sounds[selection]);
					}
					
				}
				break;
			case MAP_CAVES5DCCHUNKY:
				if ((param2 == CHUNKY5DC_GGONE) || (param2 == CHUNKY5DC_TARGET0) || (param2 == CHUNKY5DC_TARGET1) || (param2 == CHUNKY5DC_TARGET2)) {
					if (index == 0) {
						return isBonus(PreviousMap);
					} else if (index == 1) {
						return !isBonus(PreviousMap);
					}
				}
				break;
			case MAP_BATTLEARENA_BEAVERBRAWL:
			case MAP_BATTLEARENA_KRITTERKARNAGE:
			case MAP_BATTLEARENA_ARENAAMBUSH:
			case MAP_BATTLEARENA_MOREKRITTERKARNAGE:
			case MAP_BATTLEARENA_FORESTFRACAS:
			case MAP_BATTLEARENA_BISHBASHBRAWL:
			case MAP_BATTLEARENA_KAMIKAZEKREMLINGS:
			case MAP_BATTLEARENA_PLINTHPANIC:
			case MAP_BATTLEARENA_PINNACLEPALAVER:
			case MAP_BATTLEARENA_SHOCKWAVESHOWDOWN:
				if (Rando.location_visuals & 4) {
					if (param2 == CROWN_CONTROLLER) {
						float x = 730.0f;
						float y = 267.0f;
						float z = 728.0f;
						short actor = getCrownItem(CurrentMap);
						short item = -1;
						float scale = 0.0f;
						if (actor != 0) {
							getModelTwoItemFromActor(actor, &item, &scale);
							if (item >= 0) {
								spawnModelTwo(item, *(int*)&x, *(int*)&y, *(int*)&z, scale, 0x4);
								int i = 0;
								while (i < ObjectModel2Count) {
									ModelTwoData* object = (ModelTwoData*)&ObjectModel2Pointer[i];
									if (object) {
										if (object->object_id == 0x4) {
											model_struct* _model = object->model_pointer;
											if (_model) {
												_model->scale = scale;
											}
											break;
										}
									}
									i++;
								}
							}
						}
					} else if (param2 == CROWN_INDICATOR) {
						behaviour_pointer->unk_70 = 0;
						behaviour_pointer->unk_60 = 1;
						behaviour_pointer->unk_62 = 100;
					}
				}
				break;
			case MAP_TROFFNSCOFF:
				if (Rando.location_visuals & 2) {
					if (param2 == TNS_NUMBER) {
						float x = 600.0f;
						float y = 300.0f;
						float z = 400.0f;
						short item = -1;
						float scale = 0.0f;
						int world = getWorld(CurrentMap, 0);
						if (world < 7) {
							int flag = normal_key_flags[world];
							getModelTwoItemFromActor(getKeyItem(flag), &item, &scale);
							if (item >= 0) {
								spawnModelTwo(item, *(int*)&x, *(int*)&y, *(int*)&z, scale, 0x16);
								int i = 0;
								while (i < ObjectModel2Count) {
									ModelTwoData* object = (ModelTwoData*)&ObjectModel2Pointer[i];
									if (object) {
										if (object->object_id == 0xF) {
											model_struct* _model = object->model_pointer;
											if (_model) {
												_model->scale = 2 * scale;
											}
											break;
										}
									}
									i++;
								}

							}
						}
					} else if (param2 == TNS_ITEMINDICATOR) {
						behaviour_pointer->unk_70 = 0;
						behaviour_pointer->unk_60 = 1;
						behaviour_pointer->unk_62 = 100;
					}
				}
				break;
			case MAP_HELMLOBBY:
				if (param2 == HELMLOBBY_GGONE) {
					if (index == 0) {
						return isBonus(PreviousMap);
					} else if (index == 1) {
						int gb_count = 0;
						int max_gbs = 0;
						for (int level = 0; level < 8; level++) {
							for (int kong = 0; kong < 5; kong++) {
								gb_count += MovesBase[kong].gb_count[level];
							}
							if (BLockerDefaultArray[level] > max_gbs) {
								max_gbs = BLockerDefaultArray[level];
							}
						}
						return (gb_count >= max_gbs) && (Rando.microhints != MICROHINTS_NONE); 
					}
				}
				break;
			case MAP_JAPES:
				if (param2 == JAPES_DKCAGEGB) {
					if (index == 0) {
						if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 5;
							behaviour_pointer->next_state = 5;
						}
					} else if (index == 1) {
						setPermFlag(DKJAPESCAGEGB_OPEN);
					} else if (index == 2) {
						if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 6;
							behaviour_pointer->next_state = 6;
						}
					}
				} else if (param2 == JAPES_DKCAGESWITCH) {
					if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == JAPES_MOUNTAINGB) {
					if (index == 0) {
						if (checkFlag(JAPESMOUNTAINSPAWNED, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 20;
							behaviour_pointer->next_state = 20;
						}
					} else if (index == 1) {
						setPermFlag(JAPESMOUNTAINSPAWNED);
					}
				} else if (param2 == JAPES_DIDDYBAMBOOGATE) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					} else if (index == 2) {
						setPermFlag(getKongFlag(Rando.free_target_japes));
					}
				} else if ((param2 == JAPES_GUNSWITCH0) || (param2 == JAPES_GUNSWITCH1) || (param2 == JAPES_GUNSWITCH2)) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					} else if ((index == 2) || (index == 3)) {
						return getPressedSwitch(behaviour_pointer, kong_pellets[(int)Rando.free_source_japes], id);
					} else if (index == 4) {
						return !Rando.quality_of_life.remove_cutscenes; // TODO(theballaam96): Retry this
					}
				} else if ((param2 == JAPES_GATE0) || (param2 == JAPES_GATE1) || (param2 == JAPES_GATE2)) {
					if (Rando.open_level_sections) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == JAPES_DIDDYFREEGB) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_japes), FLAGTYPE_PERMANENT);
					}
				} else if ((param2 == JAPES_CAVE_GATE) || (param2 == JAPES_PEANUT_MOUNTAIN) || (param2 == JAPES_COCONUT_RAMBI)) {
					return !Rando.tag_anywhere;
				} else if (param2 == JAPES_RAMBI_DOOR) {
					if (Player) {
						if ((Rando.quality_of_life.vanilla_fixes) && (Player->control_state == 41)) { // B attack
							return 1;
						}
						return Player->control_state == 47; // Z+B Attack
					}
				}
				break;
			case MAP_JAPESMOUNTAIN:
				if (param2 == JAPES_MOUNTAINGBSWITCH) {
					if (checkFlag(JAPESMOUNTAINSPAWNED, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				}
				break;
			case MAP_FUNGIANTHILL:
				if (param2 == FUNGI_BEAN) {
					if (index == 0) {
						return checkFlag(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						setFlag(FLAG_COLLECTABLE_BEAN, 1, FLAGTYPE_PERMANENT);
					}
				}
				break;
			case MAP_FACTORY:
				if (param2 == FACTORY_DIDDYPRODGB) {
					if (index == 0) {
						if (checkFlag(FACTORYDIDDYPRODSPAWNED, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(FACTORYDIDDYPRODSPAWNED);
					}
				} else if (param2 == FACTORY_DIDDYPRODSWITCH) {
					if (checkFlag(FACTORYDIDDYPRODSPAWNED,0)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == FACTORY_FREESWITCH) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					} else if (index == 2) {
						return Character == Rando.free_source_factory;
					} else if (index == 3) {
						setPermFlag(getKongFlag(Rando.free_target_factory));
					}
				} else if (param2 == FACTORY_CAGE) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					}
				} else if (param2 == FACTORY_FREEGB) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_factory), FLAGTYPE_PERMANENT);
					}
				} else if (param2 == FACTORY_PIANO) {
					if (index < 7) {
						// Kremling appears
						spawnPianoKremling(Rando.piano_game_order[index] + 5,0);
					} else if (index < 14) {
						setAcceptablePianoKey(id, Rando.piano_game_order[index - 7] + 1,2);
					} else if (index < 21) {
						return checkSlamLocation(2, Rando.piano_game_order[index - 14] + 1, id);
					} else if (index < 28) {
						return checkContactSublocation(behaviour_pointer,id,Rando.piano_game_order[index - 21] + 1, 0);
					} else if (index == 28) {
						if (Rando.fast_gbs) {
							behaviour_pointer->next_state = 26;
						} else {
							behaviour_pointer->next_state = 17;
						}
					} else if (index == 29) {
						if (Rando.fast_gbs) {
							behaviour_pointer->next_state = 50;
						} else {
							behaviour_pointer->next_state = 37;
						}
					}
				} else if (param2 == FACTORY_3124_SWITCH || param2 == FACTORY_4231_SWITCH || param2 == FACTORY_1342_SWITCH) {
					if (index == 0) {
						return Rando.fast_gbs;
					} else if (index == 1) {
						// Check if GB is in a state >= 3, this means it was spawned.
						int index = convertIDToIndex(96);
						int* m2location = (int*)ObjectModel2Pointer;
						if (index > -1) {
							ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
							behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
							if (_object && behaviour) {
								if(behaviour->current_state <= 3) {
									behaviour_pointer->current_state = 5;
								}
							}
						}
					} else if (index == 2) {
						if (Rando.fast_gbs) {
							disableDiddyRDDoors();
						} else {
							setScriptRunState(behaviour_pointer, 2, 0);
						}
					}
				} else if (param2 == FACTORY_DARTBOARD) {
					if (index < 6) {
						if (behaviour_pointer->switch_pressed == (Rando.dartboard_order[index] + 1)) {
							if (behaviour_pointer->contact_actor_type == 43) {
								if (canHitSwitch()) {
									int index = convertSubIDToIndex(id);
									int* m2location = (int*)ObjectModel2Pointer;
									ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
									setSomeTimer(_object->object_type);
									return 1;
								}
							}
						}
						return 0;
					}
				} else if (param2 == FACTORY_LARGEMETALSECTION) {
					if (Rando.quality_of_life.vanilla_fixes) {
						behaviour_pointer->current_state = 10;
						unsigned char crusher_compontents[] = {1,3,8,9,4,10,11,12,13,2,5,6,7};
						int* m2location = (int*)ObjectModel2Pointer;
						for (int component = 0; component < sizeof(crusher_compontents); component++) {
							int index = convertIDToIndex(crusher_compontents[component]);
							if (index > -1) {
								ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
								behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
								if (behaviour) {
									behaviour->next_state = 10;
								}
							}
						}
					}
				} else if ((param2 == FACTORY_SNATCH_GRATE) || (param2 == FACTORY_PAD_GUITAR) || (param2 == FACTORY_PAD_TRIANGLE) || (param2 == FACTORY_PAD_TROMBONE)) {
					return !Rando.tag_anywhere;
				} else if (((param2 >= FACTORY_BLOCKELEVATOR_0) && (param2 <= FACTORY_BLOCKELEVATOR_4)) || (param2 == FACTORY_BLOCKELEVATOR_5) || (param2 == FACTORY_BLOCKELEVATOR_6)) {
					behaviour_pointer->timer = (RNG & 63) + 15;
				}
				break;
			case MAP_FUNGIMILLFRONT:
				if (param2 == MILL_WARNINGLIGHTS) {
					if (checkFlag(FUNGICRUSHERON, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = MILL_CRUSHER_PROGRESS * 2;
						behaviour_pointer->next_state = MILL_CRUSHER_PROGRESS * 2;
					}
				} else if (param2 == MILL_CRUSHER) {
					if (index == 0) {
						if (checkFlag(FUNGICRUSHERON, FLAGTYPE_PERMANENT)) {
							if (!checkFlag(FLAG_COLLECTABLE_FUNGI_CHUNKY_KEGGB, FLAGTYPE_PERMANENT)) { // If GB not acquired
								if (behaviour_pointer->counter == 0) {
									behaviour_pointer->current_state = 12;
									behaviour_pointer->next_state = 12;
									unkObjFunction1(id,1,8);
									unkObjFunction2(id,1,65535);
								}
							}
						}
					} else if (index == 1) {
						setPermFlag(FUNGICRUSHERON);
						behaviour_pointer->counter = MILL_CRUSHER_PROGRESS;
					}
				}
				break;
			case MAP_FUNGIMILLREAR:
				if (param2 == MILL_TRIANGLEPAD) {
					if (checkFlag(FUNGICRUSHERON, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 3;
						behaviour_pointer->next_state = 3;
					}
				} else if (param2 == MILLREAR_CHUNKYCHECK_RATE) {
					return Player->characterID == 6 || Rando.quality_of_life.vanilla_fixes;
				}
				break;
			case MAP_FUNGIGIANTMUSHROOM:
				if (param2 == GMUSH_BOARD) {
					int switch_count = 0;
					for (int i = 0; i < 5; i++) {
						if (checkFlag(FLAG_MUSHSWITCH_0 + i, FLAGTYPE_PERMANENT)) {
							switch_count += 1;
						}
					}
					if (switch_count == 5) {
						behaviour_pointer->current_state = 6;
						behaviour_pointer->next_state = 6;
						behaviour_pointer->timer = 465;
					}
				}
				break;
			case MAP_CAVES:
				if (param2 == CAVES_GBDOME) {
					if (index == 0) {
						if (checkFlag(CAVESGBDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
							hideObject(behaviour_pointer);
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(CAVESGBDOME_DESTROYED);
					}
				} else if (param2 == CAVES_SMALLBOULDERPAD) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == CAVES_BOULDERDOME) {
					if (index == 0) {
						if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
							hideObject(behaviour_pointer);
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(CAVESBOULDERDOME_DESTROYED);
					}
				} else if (param2 == CAVES_BIGBOULDERPAD) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
						if (checkFlag(CAVESGBDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
							hideObject(behaviour_pointer);
							behaviour_pointer->current_state = 20;
							behaviour_pointer->next_state = 20;
						} else {
							behaviour_pointer->current_state = 10;
							behaviour_pointer->next_state = 10;
						}
					}
				}
				break;
			case MAP_TRAININGGROUNDS:
				if (param2 == TGROUNDS_SWITCH) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.starting_kong), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.starting_kong), FLAGTYPE_PERMANENT);
					} else if (index == 2) {
						setPermFlag(getKongFlag(Rando.starting_kong));
					}
				} else if (param2 == TGROUNDS_BAMBOOGATE) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.starting_kong), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.starting_kong), FLAGTYPE_PERMANENT);
					}
				}
				break;
			case MAP_CAVESROTATINGROOM:
				if (param2 == ROTATING_ROOM_OBJ) {
					if (index == 0) {
						if (!Rando.disable_rotating_crown) {
							return checkFlag(FLAG_CROWN_CAVES, FLAGTYPE_PERMANENT);
						}
						return 1;
					} else if (index == 1) {
						return !checkFlag(FLAG_COLLECTABLE_ROTATINGGB, FLAGTYPE_PERMANENT);
					}
				}
				break;
			case MAP_GALLEONMECHFISH:
				if ((param2 == FISH_SHIELD1) || (param2 == FISH_SHIELD2) || (param2 == FISH_SHIELD3)) {
					int fish_state = 1;
					if (Rando.fast_gbs) {
						fish_state = 5;
					}
					behaviour_pointer->next_state = fish_state;
				}
				break;
			case MAP_FACTORYBBLAST:
				if (param2 == FACTORY_BBLAST_STAR) {
					if (Rando.fast_gbs) {
						behaviour_pointer->next_state = 20;
						behaviour_pointer->current_state = 20;
					}
				} else if (param2 == FACTORY_BBLAST_CONTROLLER) {
					if (Rando.fast_gbs) {
						if (!checkFlag(FLAG_ARCADE_LEVER,FLAGTYPE_PERMANENT)) {
							if (checkFlag(FLAG_ARCADE_ROUND1,FLAGTYPE_PERMANENT)) {
								isObjectLoadedInMap(MAP_FACTORY, 45, 10); // Run just to load the setup properly
								delayedObjectModel2Change(MAP_FACTORY, 45, 10);
								setNextTransitionType(0);
								setIntroStoryPlaying(2);
								setNextTransitionType(0);
								initiateTransition_0(MAP_FACTORY, 15, 0, 0);
								behaviour_pointer->next_state = 1;
							}
						}
					}
				}
				break;
			// case TREASURE_CHEST:
			// 	if (param2 == CHEST_PEARL_0) {
			// 		if (Rando.fast_gbs) {
			// 			int pearls_collected = 0;
			// 			for (int i = 0; i < 5; i++) {
			// 				pearls_collected += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, FLAGTYPE_PERMANENT);
			// 			}
			// 			if (pearls_collected >= 1) {
			// 				for (int i = 0; i < 5; i++) {
			// 					setFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, 1, FLAGTYPE_PERMANENT);
			// 				}
			// 				behaviour_pointer->next_state = 2;
			// 			}
			// 		}
			// 	}
			// 	break;
			case MAP_CAVES5DIDK:
				if (param2 == ICE_MAZE) {
					if (behaviour_pointer->switch_pressed == index) {
						if ((behaviour_pointer->contact_actor_type >= 2) && (behaviour_pointer->contact_actor_type <= 6)) { // isKong
							if (canHitSwitch()) {
								int index = convertSubIDToIndex(id);
								int* m2location = (int*)ObjectModel2Pointer;
								ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
								setSomeTimer(_object->object_type);
								return 1;
							}
						}
					}
					return 0;
				}
				break;
			case MAP_AZTECTINYTEMPLE:
				if (param2 == TTEMPLE_SWITCH) {
					return Character == 1;
				} else if (param2 == TTEMPLE_GUITARPAD) {
					return Character == 1;
				} else if (param2 == TTEMPLE_BAMBOOGATE) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_ttemple), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						setPermFlag(getKongFlag(Rando.free_target_ttemple));
					}
				} else if (param2 == TTEMPLE_CHARGESWITCH) {
					if (index == 0) {
						return checkFlag(getKongFlag(Rando.free_target_ttemple), FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						return !checkFlag(getKongFlag(Rando.free_target_ttemple), FLAGTYPE_PERMANENT);
					} else if (index == 2) {
						return checkControlState(kong_press_states[(int)Rando.free_source_ttemple]);
					}
				} else if ((param2 == TTEMPLE_KONGLETTER0) || (param2 == TTEMPLE_KONGLETTER1) || (param2 == TTEMPLE_KONGLETTER2) || (param2 == TTEMPLE_KONGLETTER3)) {
					return checkControlState(kong_press_states[(int)Rando.free_source_ttemple]);
				}
				break;
			case MAP_CASTLECRYPTLANKYTINY:
				if (param2 == CRYPT_LT_GRAPE){
					if (index == 0){
						return !Rando.tag_anywhere;
					} else if (index == 1){
						//obtain gate variables
						int id_needed = 1;
						int gateIndex = convertIDToIndex(id_needed);
						int* m2location = (int*)ObjectModel2Pointer;
						int gateSlot = convertIDToIndex(1);
						ModelTwoData* gateModelTwoPointer = getObjectArrayAddr(m2location,0x90,gateSlot);
						if (gateModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* gateBehaviour = gateModelTwoPointer->behaviour_pointer;
							if (gateBehaviour) {
								// If behaviour exists (always should do, but always good to check) initialize the gate
								if(gateIndex != -1 && gateBehaviour->pause_state == 0){
									//vanilla initiation code
									unkObjFunction0(id_needed,1,1);
									unkObjFunction1(id_needed,1,3);
									setScriptRunState(gateBehaviour, 2, 0);
								}
							}
						}

						//obtain other grape switch's variables
						int grape_switch_id_needed = 17;
						int grapeSlot = convertIDToIndex(17);
						int grapeIndex = convertIDToIndex(grape_switch_id_needed);
						ModelTwoData* grapeSwitchModelTwoPointer = getObjectArrayAddr(m2location,0x90,grapeSlot);
						if (grapeSwitchModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* grapeSwitchBehaviour = grapeSwitchModelTwoPointer->behaviour_pointer;
							if (grapeSwitchBehaviour) {
								// If behaviour exists (always should do, but always good to check) initialize the other grape switch
								if(grapeIndex != -1 && grapeSwitchBehaviour->pause_state == 0){
									setObjectScriptState(17, 4, 0);
									//vanilla initiation code
									setScriptRunState(grapeSwitchBehaviour, 2, 0);
									unkObjFunction0(grape_switch_id_needed,1,1);
									unkObjFunction1(grape_switch_id_needed,1,10);
								}
							}
						}

						//play grape switch cutscene
						if(!Rando.quality_of_life.remove_cutscenes){
							PlayCutsceneFromModelTwoScript(behaviour_pointer, 0, 1, 0);
							behaviour_pointer->timer = 110;
						}
						
						//move on to state 3
						behaviour_pointer->next_state = 3;
					}
				} else if (param2 == CRYPT_LT_SIMIAN_SWITCH) {
					//activates the Goo Hands in Tiny's part of the Lanky/Tiny Crypt if all 6 of them are initialized
					unsigned char hands[] = {6, 7, 9, 10, 11, 12};
					//activates the hands
					for(int hand = 0; hand < sizeof(hands); hand++){
						//obtain hand variables
						// Get model two pointer of the Goo Hand in question
						int* m2location = (int*)ObjectModel2Pointer;
						int slot = convertIDToIndex(hands[hand]);
						ModelTwoData* handModelTwoPointer = getObjectArrayAddr(m2location,0x90,slot);
						if (handModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* behaviour = handModelTwoPointer->behaviour_pointer;
							if (behaviour) {
								// If behaviour exists (always should do, but always good to check), activate the Goo Hand
								setObjectScriptState(slot, 10, 0);
								if(slot != -1){
									setScriptRunState(behaviour, 0, 0);
								}
							}
						}
					}
				}
				break;
			case MAP_CASTLECRYPTDKDIDDYCHUNKY:
				if ((param2 == CRYPT_DDC_D) || (param2 == CRYPT_DDC_E) || (param2 == CRYPT_DDC_F)) {
					return !Rando.tag_anywhere;
				}
				break;
			case MAP_CASTLEBASEMENT:
				if ((param2 == DUNGEON_SLAM_DK) || (param2 == DUNGEON_SLAM_DIDDY) || (param2 == DUNGEON_SLAM_LANKY)) {
					return !Rando.tag_anywhere;
				}
				break;
			case MAP_CASTLETREE:
				if ((param2 == TREE_DOOR_DK) || (param2 == TREE_DOOR_CHUNKY)) {
					return !Rando.tag_anywhere;
				}
				break;
			case MAP_HELM:
				{
					int slot = -1;
					int next_slot = -1;
					int previous_slot = -1;
					int current_slot = -1;
					int helm_pad_kong = -1;
					switch(param2) {
						case HELM_COIN_DOOR:
							if (index == 0) {
								return CoinDoorCheck();
							} else if (index == 1) {
								return checkFlagDuplicate(FLAG_HELM_COINDOOR, FLAGTYPE_PERMANENT) || Rando.coin_door_open == 1;
							} else if (index == 2) {
								// Disable coin door text
								return 1;
							}
							break;
						case HELM_PAD_BONGO:
							slot = 0;
							helm_pad_kong = 0;
						case HELM_PAD_TRIANGLE:
							if (slot == -1) {
								slot = 1;
								helm_pad_kong = 4;
							}
						case HELM_PAD_SAX:
							if (slot == -1) {
								slot = 2;
								helm_pad_kong = 3;
							}
						case HELM_PAD_TROMBONE:
							if (slot == -1) {
								slot = 3;
								helm_pad_kong = 2;
							}
						case HELM_PAD_GUITAR:
							if (slot == -1) {
								slot = 4;
								helm_pad_kong = 1;
							}
							if (slot > -1) {
								if (index < 2) {
									for (int i = 0; i < 5; i++) {
										if (Rando.helm_order[i] == slot) {
											current_slot = i;
											if (i > 0) {
												previous_slot = Rando.helm_order[i - 1];
											}
											if (i < 4) {
												next_slot = Rando.helm_order[i + 1];
											}
										}
									}
									if (index == 0) {
										// Barrels complete
										if ((next_slot == -1) && (current_slot > -1)) {
											// Helm Complete
											PlayCutsceneFromModelTwoScript(behaviour_pointer, 8, 1, 0);
											setFlag(FLAG_MODIFIER_HELMBOM, 1, FLAGTYPE_PERMANENT);
											setFlag(0x50,1,FLAGTYPE_TEMPORARY);
										} else if (next_slot > -1) {
											// Move to next
											PlayCutsceneFromModelTwoScript(behaviour_pointer, current_slot + 4, 1, 0);
										}
									} else if (index == 1) {
										if (previous_slot == -1) {
											// First or not in sequence
											return 1;
										}
										return checkFlag(previous_slot + 0x4B, FLAGTYPE_TEMPORARY);
									}
								} else  if (index == 2) {
									if ((Rando.microhints == MICROHINTS_ALL) && ((MovesBase[helm_pad_kong].instrument_bitfield & 1) == 0)) {
										behaviour_pointer->next_state = 20;
										// behaviour_pointer->current_state = 20;
									}
								} else if (index == 3) {
									if (MovesBase[helm_pad_kong].instrument_bitfield & 1) {
										behaviour_pointer->next_state = 0;
										// behaviour_pointer->current_state = 0;
									}
								}
							}
						break;
					}
					break;
				}
			default:
			break;
		}
	} else if (index == -1) {
		// Bananaport generic code
		if (!WarpData) {
			int size = 90 * 10; // 90 Warps, 10 bytes per warp
			WarpData = dk_malloc(size);
			int* file_size;
			*(int*)(&file_size) = size;
			copyFromROM(0x1FF0000,WarpData,&file_size,0,0,0,0);
		}
		bananaportGenericCode(behaviour_pointer, id, param2);
	} else if (index == -2) {
		// Wrinkly Generic Code
		short* cached_data = behaviour_pointer->extra_data;
		int kong = 0;
		if (!cached_data) {
			cached_data = dk_malloc(2);
			int wrinkly_index = convertIDToIndex(param2);
			int* m2location = (int*)ObjectModel2Pointer;
			int wrinkly_doors[] = {0xF0, 0xF2, 0xEF, 0x67, 0xF1};
			if (wrinkly_index > -1) {
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,wrinkly_index);
				for (int i = 0; i < 5; i++) {
					if (_object->object_type == wrinkly_doors[i]) {
						kong = i;
					}
				}
			}
			*cached_data = kong;
			behaviour_pointer->extra_data = cached_data;
		} else {
			kong = *cached_data;
		}
		if (behaviour_pointer->current_state == 0) {
			unkObjFunction7(id,1,0);
			unkObjFunction7(id,2,0);
			displayImageOnObject(id, 1, 1, 0);
			displayImageOnObject(id, 2, 1, 0);
			unkObjFunction0(id, 1, 1);
			unkObjFunction1(id, 1, 10);
			if ((!checkFlag(kong_flags[kong], FLAGTYPE_PERMANENT)) && (!Rando.disable_wrinkly_kong_requirement)) {
				behaviour_pointer->next_state = 20;
			} else {
				displayImageOnObject(id, 1, 0, 0);
				displayImageOnObject(id, 2, 0, 0);
				behaviour_pointer->next_state = 1;
			}
		} else if (behaviour_pointer->current_state == 1) {
			if (isPlayerInRangeOfObject(40)) {
				if (getPlayerObjectDistance()) {
					unkObjFunction2(id, 1, 1);
					PauseText = 1;
					spawnWrinklyWrapper(behaviour_pointer, id, kong, 0);
					playSFXFromObject(id, 19, 255, 127, 20, 0, 0.3f);
					behaviour_pointer->next_state = 2;
				}
			}
		} else if (behaviour_pointer->current_state == 2) {
			if (isWrinklySpawned()) {
				unkObjFunction2(id, 1, 1);
				playSFXFromObject(id, 19, 255, 127, 20, 0, 0.3f);
				PauseText = 0;
				behaviour_pointer->next_state = 3;
			}
		} else if (behaviour_pointer->current_state == 3) {
			if (unkObjFunction8(id, 1) == 0) {
				playSFXFromObject(id, 50, 255, 127, 0, 60, 0.3f);
				behaviour_pointer->next_state = 4;
			}
		} else if (behaviour_pointer->current_state == 4) {
			if (isPlayerInRangeOfObject(60) == 0) {
				behaviour_pointer->next_state = 1;
			}
		}
	} else if (index == -3) {
		TNSPortalGenericCode(behaviour_pointer, id, param2);
	} else if (index == -4) {
		TNSIndicatorGenericCode(behaviour_pointer, id, param2);
	} else if (index == -5) {
		CrownPadGenericCode(behaviour_pointer, id, param2, 0);
	} else if (index == -6) {
		CrownPadGenericCode(behaviour_pointer, id, param2, 1);
	} else if (index == -7) {
		return checkFlag(kong_flags[param2], FLAGTYPE_PERMANENT) || Rando.disable_wrinkly_kong_requirement;
	} else if (index == -8) {
		// Fairy check
		if (Rando.fairy_rando_on) {
			switch (param2) {
				case 0:
					return !Rando.fairy_triggers_disabled.japes_painting; // Japes Painting: ID 5
				case 1:
					return !Rando.fairy_triggers_disabled.factory_funky; // Factory Funky: ID 0x109
				case 2:
					return !Rando.fairy_triggers_disabled.galleon_chest; // Galleon Chest: ID 0x45
				case 3:
					return !Rando.fairy_triggers_disabled.fungi_dark_attic; // Fungi Dark Attic: ID 0x0
				case 4:
					return !Rando.fairy_triggers_disabled.fungi_thornvine_barn; // Fungi Thornvine: ID 0x24
				case 5:
					return !Rando.fairy_triggers_disabled.caves_igloo; // Caves Igloo: ID 0x0
				case 6:
					return !Rando.fairy_triggers_disabled.caves_cabin; // Caves Cabin: ID 0x5
				case 7:
					return !Rando.fairy_triggers_disabled.isles_factory_lobby; // Isles Factory Lobby: ID 0xE
				case 8:
					return !Rando.fairy_triggers_disabled.isles_fungi_lobby; // Isles Fungi Lobby: ID 0x5
			}
		}
		return 1;
	} else if (index == -9) {
		shopGenericCode(behaviour_pointer, id, param2, SHOP_CRANKY);
	} else if (index == -10) {
		shopGenericCode(behaviour_pointer, id, param2, SHOP_FUNKY);
	} else if (index == -11) {
		shopGenericCode(behaviour_pointer, id, param2, SHOP_CANDY);
	} else if (index == -12) {
		shopGenericCode(behaviour_pointer, id, param2, SHOP_SNIDE);
	}
	InstanceScriptParams[1] = id;
	InstanceScriptParams[2] = index;
	InstanceScriptParams[3] = param2;
	return 0;
}

void spawnCannon(actorData* cannon) {
	/**
	 * @brief Set correct cannon data
	 * 
	 * @param cannon Actor Pointer for referenced cannon
	 */
	cannon->shadow_intensity = 0xFF;
	cannon->obj_props_bitfield |= 0x8000;
	cannon->control_state = 0;
	cannon->noclip_byte = 2;
}

int spawnCannonWrapper(void) {
	/**
	 * @brief Container function for spawning a cannon
	 * 
	 * @return Cannon is being spawned
	 */
	if (CurrentMap == MAP_ISLES) {
		int spawner_id = getActorSpawnerIDFromTiedActor(CurrentActorPointer);
		if (spawner_id == 8) { // Castle Cannon
			if (Rando.lobbies_open_bitfield & 0x40) {
				return 1;
			}
		} else if (spawner_id == 18) { // Fungi Cannon
			if (Rando.lobbies_open_bitfield & 0x10) {
				return 1;
			}
		} 
	}
	return 0;
}

void disableDiddyRDDoors(void) {
	/**
	 * @brief Check whether to disable the Diddy R&D Doors
	 * 
	 */
	for(int i = 63; i < 66; ++i) {
		int index = convertIDToIndex(i);
		int* m2location = (int*)ObjectModel2Pointer;
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
		behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
		if (behaviour) {
			setScriptRunState(behaviour,2,0);
		}
	}
}