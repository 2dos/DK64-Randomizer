#include "../../include/common.h"

#define HELM_LOBBY 0xAA
#define HELM_MAIN 0x11
#define TRIGGER_ELEMENT_SIZE 0x3A

void changeHelmLZ(void) {
	if (Rando.fast_start_helm) {
		if (CurrentMap == HELM_LOBBY) {
			if (ObjectModel2Timer == 3) {
				setPermFlag(FLAG_STORY_HELM); // Helm Story
				setFlag(FLAG_HELM_ROMANDOORS_OPEN,1,2); // Roman Numeral Doors
				for (int j = 0; j < 4; j++) {
					setFlag(FLAG_HELM_GATE_0 + j,1,2); // Gates knocked down
				}
				for (int i = 0; i < TriggerSize; i++) {
					trigger* focused_trigger = getObjectArrayAddr(TriggerArray,TRIGGER_ELEMENT_SIZE,i);
					if (focused_trigger->type == 9) {
						if (focused_trigger->map == HELM_MAIN) {
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
	if (Rando.coin_door_open == 1) { // Always Open
		setPermFlag(FLAG_HELM_COINDOOR);
	} else if (Rando.coin_door_open == 2) { // Only requires RW Coin
		if (checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN,0)) { // Has Nintendo Coin
			setPermFlag(FLAG_HELM_COINDOOR);
		}
	} else if (Rando.coin_door_open == 3) { // Only requires Nin Coin
		if (checkFlag(FLAG_COLLECTABLE_RAREWARECOIN,0)) { // Has Rareware Coin
			setPermFlag(FLAG_HELM_COINDOOR);
		}
	}
}

static const short minigame_0_flags[] = {0x3C,0x3F,0x3E,0x40,0x3D};
static const short minigame_1_flags[] = {0x41,0x44,0x43,0x45,0x42};

static const short item_setstate[] = {17,22,23,27,30};
static const short item_medallook[] = {61,62,63,64,65};
static const short item_laserlook[] = {16,19,20,26,29};
static const short item_padset[] = {-1,33,34,35,36};
static const short item_padlook[] = {-1,76,77,78,79};

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
				setFlag(0x4B + i,1,2); // Section Complete
				setFlag(minigame_0_flags[i],1,2);
				setFlag(minigame_1_flags[i],1,2);
			}
		}
		// Tag entrance W1
		setPermFlag(FLAG_WARP_HELM_W1_NEAR);
	} else if (init_stage == 1) {
		// Modify Cutscenes
		int has_ended = 0;
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
					modifyCutsceneItem(0, cutscene, 0, item_setstate[current_slot]);
					modifyCutsceneItem(0, cutscene, 1, item_medallook[current_slot]);
					modifyCutsceneItem(0, cutscene, 2, item_laserlook[current_slot]);
				}
				if (next_slot > -1) {
					modifyCutsceneItem(0, cutscene, 4, item_padset[next_slot]);
					modifyCutsceneItem(0, cutscene, 5, item_padlook[next_slot]);
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

typedef struct bonus_paad {
	/* 0x000 */ float oscillation_y;
	/* 0x004 */ short unk4;
	/* 0x006 */ short unk6;
	/* 0x008 */ short unk8;
	/* 0x00A */ short barrel_index;
	/* 0x00C */ char other_timer;
	/* 0x00D */ char destroy_timer;
	/* 0x00E */ char raise_timer;
} bonus_paad;

void HelmBarrelCode(void) {
	bonus_paad* paad = CurrentActorPointer_0->paad;
	int deleted = 0;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		int barrel_index = -1;
		if (CurrentActorPointer_0->data_pointer) {
			barrel_index = CurrentActorPointer_0->data_pointer->data[2];
		}
		if (checkFlag(FLAG_MODIFIER_HELMBOM,0)) {
			deleteActorContainer(CurrentActorPointer_0);
			deleted = 1;
		} else if (barrel_index > -1) {
			if (checkFlag(HelmMinigameFlags[barrel_index],2)) {
				deleteActorContainer(CurrentActorPointer_0);
				deleted = 1;
			}
		}
	}
	if (!deleted) {
		BonusBarrelCode();
		if (CurrentActorPointer_0->control_state == 0xC) {
			if (paad->destroy_timer < 3) {
				setFlag(HelmMinigameFlags[(int)paad->barrel_index],1,2);
				DisplayExplosionSprite();
				deleteActorContainer(CurrentActorPointer_0);
			}
		}
	}
}