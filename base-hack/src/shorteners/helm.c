#include "../../include/common.h"

#define TRIGGER_ELEMENT_SIZE 0x3A

void changeHelmLZ(void) {
	if (Rando.fast_start_helm) {
		if (CurrentMap == MAP_HELMLOBBY) {
			if (ObjectModel2Timer == 3) {
				setPermFlag(FLAG_STORY_HELM); // Helm Story
				setFlag(FLAG_HELM_ROMANDOORS_OPEN,1,FLAGTYPE_TEMPORARY); // Roman Numeral Doors
				for (int j = 0; j < 4; j++) {
					setFlag(FLAG_HELM_GATE_0 + j,1,FLAGTYPE_TEMPORARY); // Gates knocked down
				}
				for (int i = 0; i < TriggerSize; i++) {
					trigger* focused_trigger = getObjectArrayAddr(TriggerArray,TRIGGER_ELEMENT_SIZE,i);
					if (focused_trigger->type == 9) {
						if (focused_trigger->map == MAP_HELM) {
							if (focused_trigger->exit == 0) {
								if (Rando.fast_start_helm == 1) {
									focused_trigger->exit = 3;
								} else if (Rando.fast_start_helm == 2) {
									focused_trigger->exit = 4;
								}
							}
						}
					}
				}
			}
		}
	}
}

void openCrownDoor(void) {
	if (Rando.crown_door_open) {
		setPermFlag(FLAG_HELM_CROWNDOOR);
	}
}

void openCoinDoor(void) {
	if (Rando.coin_door_open) {
		setPermFlag(FLAG_HELM_COINDOOR);
	}
}

static const short minigame_0_flags[] = {0x3C,0x3F,0x3E,0x40,0x3D};
static const short minigame_1_flags[] = {0x41,0x44,0x43,0x45,0x42};

static const short item_setstate[] = {17,22,23,27,30};
static const short item_medallook[] = {61,62,63,64,65};
static const short item_laserlook[] = {16,19,20,26,29};
static const short item_padset[] = {42,33,34,35,36};
static const short item_padlook[] = {1,76,77,78,79};

void HelmInit(int init_stage) {
	if (init_stage == 0) {
		// Set Flags
		for (int i = 0; i < 5; i++) {
			int in_helm = 0;
			for (int j = 0; j < 5; j++) {
				if (Rando.helm_order[j] == i) {
					in_helm = 1;
				}
			}
			if (!in_helm) {
				setFlag(0x4B + i,1,FLAGTYPE_TEMPORARY); // Section Complete
				setFlag(minigame_0_flags[i],1,FLAGTYPE_TEMPORARY);
				setFlag(minigame_1_flags[i],1,FLAGTYPE_TEMPORARY);
			}
		}
		// Tag entrance W1
		setPermFlag(FLAG_WARP_HELM_W1_NEAR);
	} else if (init_stage == 1) {
		// Modify Cutscenes
		int has_ended = 0;
		modifyCutscenePanPoint(0, 1, 0, 1150, -20, 3500, 0xEA48, 0xF000, 0x27F5, 45, 0);
		modifyCutscenePanPoint(0, 1, 1, 777, -76, 3656, 0xEA48, 0, 0x27F5, 45, 0);
		modifyCutscenePanPoint(0, 1, 2, 651, -68, 3775, 0xEA48, 0xC000, 0x27F5, 45, 0);
		modifyCutsceneItem(0, 42, 0x15, 0x2C, 10);
		for (int i = 0; i < 5; i++) {
			if (!has_ended) {
				int cutscene = 4 + i;
				int current_slot = Rando.helm_order[i];
				int next_slot = -1;
				if (i < 4) {
					next_slot = Rando.helm_order[i+1];
				}
				if (next_slot == -1) {
					has_ended = 1;
					cutscene = 8;
				}
				if (current_slot > -1) {
					modifyCutscenePoint(0, cutscene, 0, item_setstate[current_slot]);
					modifyCutscenePoint(0, cutscene, 1, item_medallook[current_slot]);
					modifyCutscenePoint(0, cutscene, 2, item_laserlook[current_slot]);
				}
				if (next_slot > -1) {
					modifyCutscenePoint(0, cutscene, 4, item_padset[next_slot]);
					modifyCutscenePoint(0, cutscene, 5, item_padlook[next_slot]);
				}
			}
		}
		

		/*
			CS 4:
				Shutdown:
					Points 0/1, Item 17/61 (Zoom on Medal)
					Points 2, Item 16 (Laser)
				Next Zone:
					Points 4/5, Item 33/76
			CS 5:
				Shutdown:
					Points 0/1, Item 22/62 (Zoom on Medal)
					Points 2, Item 19 (Laser)
				Next Zone:
					Points 4/5, Item 34/77
			CS 6:
				Shutdown:
					Points 0/1, Item 23/63 (Zoom on Medal)
					Points 2, Item 20 (Laser)
				Next Zone:
					Points 4/5, Item 35/78
			CS 7:
				Shutdown:
					Points 0/1, Item 27/64 (Zoom on Medal)
					Points 2, Item 26 (Laser)
				Next Zone:
					Points 4/5, Item 36/79

			CS 8:
				Shutdown:
					Points 0/1, Item 30/65
					Points 2, Item 29 (Laser)
				Helm Finish Stuff:
					Points 3/5, Item 81/66
		*/
	}
}

void HelmBarrelCode(void) {
	bonus_paad* paad = CurrentActorPointer_0->paad;
	int deleted = 0;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		int barrel_index = -1;
		if (CurrentActorPointer_0->data_pointer) {
			barrel_index = CurrentActorPointer_0->data_pointer->data[2];
		}
		if (checkFlag(FLAG_MODIFIER_HELMBOM, FLAGTYPE_PERMANENT)) {
			deleteActorContainer(CurrentActorPointer_0);
			deleted = 1;
		} else if (barrel_index > -1) {
			if (checkFlag(HelmMinigameFlags[barrel_index], FLAGTYPE_TEMPORARY)) {
				deleteActorContainer(CurrentActorPointer_0);
				deleted = 1;
			}
		}
	}
	if (!deleted) {
		BonusBarrelCode();
		if (CurrentActorPointer_0->control_state == 0xC) {
			if (paad->destroy_timer < 3) {
				setFlag(HelmMinigameFlags[(int)paad->barrel_index],1,FLAGTYPE_TEMPORARY);
				DisplayExplosionSprite();
				deleteActorContainer(CurrentActorPointer_0);
			}
		}
	}
}

#define DOORITEM_DEFAULT 0 // Default
#define DOORITEM_GB 1 // 1 - GBs
#define DOORITEM_BP 2 // 2 - BP
#define DOORITEM_BEAN 3 // 3 - Bean
#define DOORITEM_PEARL 4 // 4 - Pearls
#define DOORITEM_FAIRY 5 // 5 - Fairy
#define DOORITEM_KEY 6 // 6 - Key
#define DOORITEM_MEDAL 7 // 7 - Medal
#define DOORITEM_RAINBOWCOIN 8 // 8 - Rainbow Coins
#define DOORITEM_CROWN 9 // 9 - Crowns
#define DOORITEM_COMPANYCOIN 10 // 10 - Company Coins

int checkDoorItem(int index, int count) {
	switch (index) {
		case DOORITEM_DEFAULT:
			return 1;
		case DOORITEM_GB:
			return getTotalGBs() >= count;
		case DOORITEM_BP:
			return countFlagsDuplicate(FLAG_BP_JAPES_DK_HAS, 40, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_BEAN:
			return checkFlagDuplicate(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
		case DOORITEM_PEARL:
			return countFlagsDuplicate(FLAG_PEARL_0_COLLECTED, 5, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_FAIRY:
			return countFlagsDuplicate(FLAG_FAIRY_1, 20, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_KEY:
			{
				int key_count = 0;
				for (int i = 0; i < 8; i++) {
					key_count += checkFlagDuplicate(normal_key_flags[i], FLAGTYPE_PERMANENT);
				}
				return key_count >= count;
			}
		case DOORITEM_MEDAL:
			return countFlagsDuplicate(FLAG_MEDAL_JAPES_DK, 40, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_RAINBOWCOIN:
			return countFlagsDuplicate(FLAG_RAINBOWCOIN_0, 16, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_CROWN:
			return countFlagsDuplicate(FLAG_CROWN_JAPES, 10, FLAGTYPE_PERMANENT) >= count;
		case DOORITEM_COMPANYCOIN:
			return (checkFlagDuplicate(FLAG_COLLECTABLE_NINTENDOCOIN, FLAGTYPE_PERMANENT) + checkFlagDuplicate(FLAG_COLLECTABLE_RAREWARECOIN, FLAGTYPE_PERMANENT)) >= count;
	}
	return 1;
}

int CrownDoorCheck(void) {
	if (Rando.crown_door_item == DOORITEM_DEFAULT) {
		Rando.crown_door_item = DOORITEM_CROWN;
	}
	if (Rando.crown_door_item_count == 0) {
		Rando.crown_door_item_count = 4;
	}
	return checkDoorItem(Rando.crown_door_item, Rando.crown_door_item_count);
}

int CoinDoorCheck(void) {
	if (Rando.coin_door_item == DOORITEM_DEFAULT) {
		Rando.coin_door_item = DOORITEM_COMPANYCOIN;
	}
	if (Rando.coin_door_item_count == 0) {
		Rando.coin_door_item_count = 2;
	}
	return checkDoorItem(Rando.coin_door_item, Rando.coin_door_item_count);
}