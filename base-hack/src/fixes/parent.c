/**
 * @file parent.c
 * @author Ballaam
 * @brief Parent map filtration code
 * @version 0.1
 * @date 2022-03-25
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

#define PARENT_FILTER_THRESHOLD 14 // Parent chain length limit regarding filtration
#define LOCK_STACK_THRESHOLD 28 // Lock Stack length limit regarding filtration

static const unsigned char banned_filter_maps[] = {
	// Maps where the filtration process is banned
	MAP_FUNKY, // Funky's
	MAP_DKARCADE, // Arcade
	MAP_CRANKY, // Cranky's
	MAP_JETPAC, // Jetpac
	MAP_SNIDE, // Snide's
	MAP_CANDY, // Candy's
	MAP_TROFFNSCOFF, // T&S
	MAP_GALLEONMECHFISH, // Mech FIsh
	MAP_JAPESDILLO, // Japes Dillo
	MAP_AZTECDOGADON, // Aztec Dog
	MAP_FACTORYJACK, // MJ
	MAP_GALLEONPUFFTOSS, // Pufftoss
	MAP_FUNGIDOGADON, // Fungi Dog
	MAP_CAVESDILLO, // Caves Dillo
	MAP_CASTLEKUTOUT, // KKO
	MAP_AZTECBBLAST, // Aztec BBlast
	MAP_GALLEONBBLAST, // Galleon BBlast
	MAP_FACTORYBBLAST, // Factory BBlast
	MAP_CASTLEBBLAST, // Castle BBlast
	MAP_JAPESBBLAST, // Japes BBlast
	MAP_KROOLDK, // DK Phase
	MAP_KROOLDIDDY, // Diddy Phase
	MAP_KROOLLANKY, // Lanky Phase
	MAP_KROOLTINY, // Tiny Phase
	MAP_KROOLCHUNKY, // Chunky Phase
	MAP_KROOLSHOE, // Tiny Phase: Shoe
	MAP_KROOLARENA, // Arena (Used for the ran out of time cutscene)
};

typedef struct cutscene_wipe {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ unsigned char cutscene;
	/* 0x002 */ char cutscene_type;
	/* 0x003 */ char unused;
} cutscene_wipe;

static const cutscene_wipe wipe_prevent_list[] = {
	// Cutscenes where the filtration process is prevented, regardless of map permissions
	{
		// Mountain GB Spawn Cutscene
		.map = MAP_JAPES,
		.cutscene = 13,
		.cutscene_type = 0,
	},
	{
		// Fungi Crusher On
		.map = MAP_FUNGIMILLFRONT,
		.cutscene = 2,
		.cutscene_type = 0,
	},
	{
		// Fungi Turn Waterwheel
		.map = MAP_FUNGI,
		.cutscene = 10,
		.cutscene_type = 0,
	},
	{
		// Fungi Mill GB Spawn
		.map = MAP_FUNGI,
		.cutscene = 9,
		.cutscene_type = 0,
	},
	{
		// Fungi break box
		.map = MAP_FUNGI,
		.cutscene = 11,
		.cutscene_type = 0,
	},
	{
		// Aztec Snoop Door Open
		.map = MAP_AZTEC,
		.cutscene = 17,
		.cutscene_type = 0,
	},
	{
		// Fungi Winch
		.map = MAP_FUNGI,
		.cutscene = 7,
		.cutscene_type = 0,	
	},
	{
		// Factory Power Shed
		.map = MAP_FACTORY,
		.cutscene = 7,
		.cutscene_type = 0,
	},
	{
		// Galleon Ship Spawn
		.map = MAP_GALLEON,
		.cutscene = 14,
		.cutscene_type = 0,
	}
};

int isPreventCutscenePlaying(void) {
	/**
	 * @brief Check if a cutscene which prevents the filtration process is playing
	 */
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
	/**
	 * @brief Call the parent map filtration process
	 */
	if (!Rando.call_parent_filter) {
		return;
	}
	if (ObjectModel2Timer < 2) {
		// Fix DK Portal to be in state 2
		correctDKPortal();
		return;
	}
	if (ObjectModel2Timer != 2) {
		return;
	}
	int curr = CurrentMap;
	int level = levelIndexMapping[curr];
	if (level <= LEVEL_CASTLE) {
		// Set permanent flag to clear the story cutscene of the level you're in
		setPermFlag(FLAG_STORY_JAPES + level);
	}
	for (int i = 0; i < sizeof(banned_filter_maps); i++) {
		if (banned_filter_maps[i] == curr) {
			return;
		}
	}
	if ((level == LEVEL_BONUS) || (level == LEVEL_SHARED)) {
		return;
	}
	if (isPreventCutscenePlaying()) {
		return;
	}
	// Reset Parent Chain
	resetMapContainer();
}