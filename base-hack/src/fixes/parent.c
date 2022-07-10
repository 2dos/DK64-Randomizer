#include "../../include/common.h"

#define PARENT_FILTER_THRESHOLD 14
#define LOCK_STACK_THRESHOLD 28

static const unsigned char banned_filter_maps[] = {
	1, // Funky's
	2, // Arcade
	5, // Cranky's
	9, // Jetpac
	15, // Snide's
	0x19, // Candy's
	0x2A, // T&S
	0x33, // Mech FIsh
	0x8, // Japes Dillo
	0xC5, // Aztec Dog
	0x9A, // MJ
	0x6F, // Pufftoss
	0x53, // Fungi Dog
	0xC4, // Caves Dillo
	0xC7, // KKO
	0x29, // Aztec BBlast
	0x36, // Galleon BBlast
	0x6E, // Factory BBlast
	0xBB, // Castle BBlast
	0x25, // Japes BBlast
};

typedef struct cutscene_wipe {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ unsigned char cutscene;
	/* 0x002 */ char cutscene_type;
	/* 0x003 */ char unused;
} cutscene_wipe;

static const cutscene_wipe wipe_prevent_list[] = {
	{
		// Mountain GB Spawn Cutscene
		.map = 7,
		.cutscene = 13,
		.cutscene_type = 0,
	},
	{
		// Fungi Crusher On
		.map = 61,
		.cutscene = 2,
		.cutscene_type = 0,
	},
	{
		// Fungi Turn Waterwheel
		.map = 48,
		.cutscene = 10,
		.cutscene_type = 0,
	},
	{
		// Fungi Mill GB Spawn
		.map = 48,
		.cutscene = 9,
		.cutscene_type = 0,
	},
	{
		// Fungi break box
		.map = 48,
		.cutscene = 11,
		.cutscene_type = 0,
	},
	{
		// Aztec Snoop Door Open
		.map = 38,
		.cutscene = 17,
		.cutscene_type = 0,
	},
	{
		// Fungi Winch
		.map = 48,
		.cutscene = 7,
		.cutscene_type = 0,	
	},
	{
		// Factory Power Shed
		.map = 26,
		.cutscene = 7,
		.cutscene_type = 0,
	},
	{
		// Galleon Ship Spawn
		.map = 30,
		.cutscene = 14,
		.cutscene_type = 0,
	}
};

int isPreventCutscenePlaying(void) {
	if (CutsceneActive) {
		for (int i = 0; i < (sizeof(wipe_prevent_list)/4); i++) {
			if (CutsceneIndex == wipe_prevent_list[i].cutscene) {
				if ((wipe_prevent_list[i].cutscene_type == 1) && ((CutsceneStateBitfield & 4) != 0)) {
					return 1;
				}
				if (CurrentMap == wipe_prevent_list[i].map) {
					if ((wipe_prevent_list[i].cutscene_type == 0) && ((CutsceneStateBitfield & 4) == 0)) {
						return 1;
					}
				}
			}
		}
	}
	return 0;
}

void callParentMapFilter(void) {
	if (Rando.randomize_more_loading_zones) {
		if (ObjectModel2Timer == 2) {
			int curr = CurrentMap;
			int level = levelIndexMapping[curr];
			if (level < 7) {
				setPermFlag(FLAG_STORY_JAPES + level);
			}
			int banned = 0;
			for (int i = 0; i < sizeof(banned_filter_maps); i++) {
				if (banned_filter_maps[i] == curr) {
					banned = 1;
				}
			}
			if ((level == 9) || (level == 0xD)) {
				banned = 1;
			}
			if (isPreventCutscenePlaying()) {
				banned = 1;
			}
			if (!banned) {
				resetMapContainer();
			}
		} else if (ObjectModel2Timer < 2) {
			correctDKPortal();
		}
	}
}