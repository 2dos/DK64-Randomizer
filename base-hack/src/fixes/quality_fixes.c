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

static const short tnsportal_flags[] = {
	FLAG_PORTAL_JAPES,
	FLAG_PORTAL_AZTEC,
	FLAG_PORTAL_FACTORY,
	FLAG_PORTAL_GALLEON,
	FLAG_PORTAL_FUNGI,
	FLAG_PORTAL_CAVES,
	FLAG_PORTAL_CASTLE,
};

typedef struct sprite_info {
	/* 0x000 */ char unk_00[0x358];
	/* 0x358 */ int timer;
	/* 0x35C */ char unk_35C[0x360-0x35C];
	/* 0x360 */ float scale_x;
	/* 0x364 */ float scale_z;
	/* 0x368 */ char unk_368[0x36A-0x368];
	/* 0x36A */ unsigned char red;
	/* 0x36B */ unsigned char green;
	/* 0x36C */ unsigned char blue;
	/* 0x36D */ unsigned char alpha;
} sprite_info;

#define SPRITE_ALPHA_IN 8
#define SPRITE_ALPHA_OUT 44
#define SPRITE_ALPHA_END 52

int setAlpha(sprite_info* sprite) {
	if (sprite->timer < SPRITE_ALPHA_IN) {
		float alpha_new = 255 / SPRITE_ALPHA_IN;
		alpha_new *= sprite->timer;
		if (alpha_new > 255) {
			alpha_new = 255;
		}
		sprite->alpha = alpha_new;
	} else if (sprite->timer > SPRITE_ALPHA_OUT) {
		int diff = SPRITE_ALPHA_END - sprite->timer;
		float alpha_new = 255 / (SPRITE_ALPHA_END - SPRITE_ALPHA_OUT);
		alpha_new *= diff;
		if (alpha_new > 255) {
			alpha_new = 255;
		}
		sprite->alpha = alpha_new;
		if (sprite->alpha < 6) {
			return 1;
		}
	} else {
		sprite->alpha = 255;
	}
	return 0;

}

void handleTroffFace(sprite_info* sprite, char* unk0) {
	int hide = setAlpha(sprite);
	sprite->scale_x = 2.0f;
	sprite->scale_z = 2.0f;
	if (hide) {
		*unk0 = 1;
	}
}

void handleTick(sprite_info* sprite, char* unk0) {
	int hide = setAlpha(sprite);
	sprite->scale_x = 1.5f;
	sprite->scale_z = 1.5f;
	sprite->green = 0xFF;
	sprite->red = 0;
	sprite->blue = 0;
	if (hide) {
		*unk0 = 1;
	}
}

void playCBDing(void) {
	playSFX(Bell);
	// unkSpriteRenderFunc(200);
	// unkSpriteRenderFunc_0();
	// loadSpriteFunction((int)&handleTroffFace);
	// displaySpriteAtXYZ(sprite_table[0xA7], 0x3F800000, 0x41F00000, 0x42700000);
	// unkSpriteRenderFunc(200);
	// unkSpriteRenderFunc_0();
	// loadSpriteFunction((int)&handleTick);
	// displaySpriteAtXYZ(sprite_table[0xAE], 0x3F800000, 0x42700000, 0x425C0000);
}

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
				if (!checkFlag(tnsportal_flags[world],0)) {
					playCBDing();
				}
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

void preventMedalHUD(int item, int unk0, int unk1) {
	if (item != 0xA) {
		displayItemOnHUD(item, unk0, unk1);
	}
}

void initHUDDirection(placementData* hud_data, int item) {
	int x_direction = 0;
	int y_direction = 0;
	hud_data->unk_0C = 0;
	switch(item) {
		case 0x0: // CB
		case 0xD: // CB T&S
		case 0xE: // Move Cost
			x_direction = -1;
			break;
		case 0x9: // GBs
		case 0xC: // Blueprint
			y_direction = 1;
			break;
		default:
			x_direction = 1;
		break;
	}
	hud_data->x_direction = x_direction * 0x30;
	hud_data->y_direction = y_direction * 0x30;
}

void* getHUDSprite_HUD(int item) {
	if (item == 0xA) {
		return sprite_table[0xA8];
	} else {
		return getHUDSprite(item);
	}
}

void updateMultibunchCount(void) {
	int world = getWorld(CurrentMap,1);
	int count = 0;
	if (world < 7) {
		count = CBTurnedInArray[world];
		for (int kong = 0; kong < 5; kong++) {
			count += MovesBase[kong].cb_count[world];
		}
	}
	MultiBunchCount = count;
	if (HUD) {
		HUD->item[0xA].visual_item_count = count;
	}
}