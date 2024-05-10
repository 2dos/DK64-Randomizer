/**
 * @file crown_pad.c
 * @author Ballaam
 * @brief Functions related to Battle Crown Pads
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

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
		setScriptRunState(behaviour, RUNSTATE_DISTANCERUN, 900);
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
		setScriptRunState(behaviour, RUNSTATE_PAUSED, 0);
	}
	if (Player) {
		if ((Player->obj_props_bitfield & 0x2000) == 0) {
			if ((Player->characterID >= 2) && (Player->characterID <= 6)) {
				if (standingOnM2Object(index)) {
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