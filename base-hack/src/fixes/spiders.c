/**
 * @file spiders.c
 * @author Ballaam
 * @brief All functions pertaining to the spider enemy.
 * @version 0.1
 * @date 2022-08-01
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

void HandleSpiderSilkSpawn(void) {
	if (CurrentMap != MAP_FUNGISPIDER) {
		return;
	}
	CurrentActorPointer_0->control_state = 0x1E;
	playActorAnimation(CurrentActorPointer_0, 0x2F8);
	spawnSpiderSilk();
}

void SpiderBossExtraCode(void) {
	if (checkFlag(FLAG_COLLECTABLE_SPIDERBOSSGB, FLAGTYPE_PERMANENT)) { // Has reward
		if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
			for (int i = 0; i < TriggerSize; i++) {
				int cutscene = TriggerArray[i].map;
				if ((TriggerArray[i].type == 10) && ((cutscene == 3) || (cutscene == 9))) {
					TriggerArray[i].active = 0;
				}
			}
		}
		return;
	}
	renderActor(CurrentActorPointer_0, 0);
}