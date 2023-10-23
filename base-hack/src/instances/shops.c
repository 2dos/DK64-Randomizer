/**
 * @file shops.c
 * @author Ballaam
 * @brief Functions related to shop objects
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

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