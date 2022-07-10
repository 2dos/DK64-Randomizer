#include "../../include/common.h"

#define HELM_LOBBY 0xAA
#define HELM_MAIN 0x11
#define TRIGGER_ELEMENT_SIZE 0x3A

void changeHelmLZ(void) {
	if (Rando.fast_start_helm) {
		if (CurrentMap == HELM_LOBBY) {
			if (ObjectModel2Timer == 3) {
				setPermFlag(0x1CC); // Helm Story
				setFlag(0x3B,1,2); // Roman Numeral Doors
				for (int j = 0; j < 4; j++) {
					setFlag(0x46 + j,1,2); // Gates knocked down
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
		setPermFlag(0x304);
	}
}

void openCoinDoor(void) {
	if (Rando.coin_door_open) {
		setPermFlag(0x303);
	}
}