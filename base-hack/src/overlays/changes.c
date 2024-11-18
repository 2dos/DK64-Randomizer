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
		case OVERLAY_BOSS:
			overlay_mod_boss();
			break;
		case OVERLAY_BONUS:
			overlay_mod_bonus();
			break;
		case OVERLAY_ARCADE:
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
}

void parseCutsceneData(void) {
	/**
	 * @brief Handle Cutscene Data
	 */
	resetDisplayedMusic();
	wipeCounterImageCache();
	initQoL_Cutscenes();
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