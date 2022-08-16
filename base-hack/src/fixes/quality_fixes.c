#include "../../include/common.h"

#define JAPES_MAIN 7
#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	if (Rando.quality_of_life) {
		if (Gamemode == 0) {
			StorySkip = 1;
		}
		setPermFlag(FLAG_FTT_CRANKY); // Cranky FTT
		setPermFlag(FLAG_TBARREL_SPAWNED); // Training Barrels Spawned
		setPermFlag(FLAG_MODIFIER_KOSHADEAD); // Giant Kosha Dead
		fixkey8();
		if (CurrentMap == JAPES_MAIN) {
			if (Player) {
				if (Character == 6) { // Rambi
					if (Player->detransform_timer == 0) {
						Player->rambi_enabled = 1;
					}
				}
			}
		}
	}
}

void checkNinWarp(void) {
	if (Rando.quality_of_life) {
		WarpToDKTV();
		TransitionType = 0;
	} else {
		initiateTransitionFade(0x4C,0,2);
	}
}

static unsigned short previous_total_cbs = 0xFFFF;
static unsigned char previous_world = 0xFF;

void CBDing(void) {
	if (Rando.quality_of_life) {
		int world = getWorld(CurrentMap, 1);
		int total_cbs = 0;
		if (world < 7) {
			total_cbs = CBTurnedInArray[world];
			for (int kong = 0; kong < 5; kong++) {
				total_cbs += MovesBase[kong].cb_count[world];
			}
			int req_cbs = TroffNScoffReqArray[world];
			if ((previous_total_cbs < req_cbs) && (total_cbs >= req_cbs) && (previous_world == world) && (CurrentMap != 0x2A)) { // Ban in T&S because of delayed update to turn in array
				playSFX(Bell);
			}
		}
		previous_world = world;
		previous_total_cbs = total_cbs;
	}
}

void fixRBSlowTurn(void) {
	controlStateControl(0x1B);
	if (Player) {
		Player->turn_speed = 0x190;
	}
}

void postKRoolSaveCheck(void) {
	if ((CurrentMap != 0x22) || (!CutsceneFadeActive) || (CutsceneFadeIndex != 29)) {
		save();
	}
}

void tagBarrelBackgroundKong(int kong_actor) {
	tagKong(kong_actor);
	Player->new_kong = kong_actor;
}