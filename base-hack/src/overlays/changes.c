/**
 * @file overlay_changes.c
 * @author Ballaam
 * @brief Changes which need to be applied on overlay initialization
 * @version 0.1
 * @date 2022-01-12
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include "../../include/common.h"

void* getPointerFile(int table, int file) {
	/**
	 * @brief Get a pointer table file without using getMapData for instances where getMapData will crash the game.
	 */
	int ptr_offset = 0x101C50;
	int* ptr_table = getFile(32*4, ptr_offset);
	int table_addr = ptr_table[table] + ptr_offset;
	int* table_loc = getFile(8, table_addr + (file * 4));
	int file_start = table_loc[0] + ptr_offset;
	int file_end = table_loc[1] + ptr_offset;
	int file_size = file_end - file_start;
	return getFile(file_size, file_start);
}

void overlay_changes(void) {
	/**
	 * @brief All changes upon loading an overlay
	 */
	overlays loaded_overlay = getOverlayFromMap(CurrentMap);
	switch (loaded_overlay) {
		case OVERLAY_MENU:
			// Also contains shops
			overlay_mod_menu();
			break;
		case OVERLAY_CRITTER:
			// Known as "Water" in Ghidra repo
			overlay_mod_critter();
			break;
		case OVERLAY_BOSS:
			overlay_mod_boss();
			break;
		case OVERLAY_BONUS:
			overlay_mod_bonus();
			break;
		case OVERLAY_ARCADE:
			initArcade();
			break;
		case OVERLAY_JETPAC:
			initJetpac();
			break;
		case OVERLAY_RACE:
			overlay_mod_race();
			break;
		default:
			break;
	}
	if (CurrentMap == MAP_HELM) {
		// Initialize Helm
		HelmInit(0);
	}
	if (ObjectModel2Timer < 2) {
		// Wipe warp data pointer to prevent pointing to free memory
		WarpData = 0;
	}
	fixTBarrelsAndBFI(0);
	loadWidescreen(loaded_overlay);
}

void parseCutsceneData(void) {
	/**
	 * @brief Handle Cutscene Data
	 */
	wipeCounterImageCache();
	if ((CurrentMap >= MAP_KROOLDK) && (CurrentMap <= MAP_KROOLCHUNKY)) {
		int phase = CurrentMap - MAP_KROOLDK;
		initKRool(phase);
	}
	if (Rando.cutscene_skip_setting == CSSKIP_AUTO) {
		updateSkippableCutscenes();
	}
	if (Rando.quality_of_life.fast_hints) {
		modifyCutscenePointTime(1, 0x22, 1, 1);
		modifyCutscenePointTime(1, 0x22, 3, 1);
	}
	if ((Rando.faster_checks.castle_cart) && (CurrentMap == MAP_CASTLEMINECART)) {
		int rx = 8931;
		int ry = 0;
		int rz = 7590;
		modifyCutscenePanPoint(0, 7, 0, 3100, 500, 500, rx, ry, rz, 45, 0);
		modifyCutscenePanPoint(0, 7, 1, 3200, 500, 500, rx, ry, rz, 45, 0);
	}
	loadDKTVData(); // Has to be last
}