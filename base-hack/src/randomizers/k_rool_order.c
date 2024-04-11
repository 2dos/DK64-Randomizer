#include "../../include/common.h"

typedef struct boss_spawn_info {
	/* 0x000 */ unsigned char map_id;
	/* 0x001 */ char pen_id; // -1 for "doesn't respond to pen id"
	/* 0x002 */ short x;
	/* 0x004 */ short y;
	/* 0x006 */ short z;
	/* 0x008 */ short unk0;
	/* 0x00A */ char unk1;
	/* 0x00B */ char spawn_at_boss;
} boss_spawn_info;

static const boss_spawn_info boss_spawn_data[] = {
	{.map_id = MAP_JAPESDILLO, .pen_id = 4, .x = 0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 6, .spawn_at_boss=0}, // Japes Dillo
	{.map_id = MAP_CAVESDILLO, .pen_id = -1, .x = 0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // Caves Dillo - Spawns at boss, not sure what unk0 is
	{.map_id = MAP_GALLEONPUFFTOSS, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 1, .spawn_at_boss=1}, // Pufftoss - Spawns at boss
	{.map_id = MAP_FUNGIDOGADON, .pen_id = 0x10, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 4, .spawn_at_boss=0}, // Fungi Dogadon
	{.map_id = MAP_AZTECDOGADON, .pen_id = 0x10, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 4, .spawn_at_boss=0}, // Aztec Dogadon
	{.map_id = MAP_CASTLEKUTOUT, .pen_id = -1, .x=0, .y=200, .z=40, .unk0 = 0x800, .unk1 = 1, .spawn_at_boss=1}, // KKO - Spawns at boss
	{.map_id = MAP_FACTORYJACK, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 1, .spawn_at_boss=1}, // Mad Jack
	{.map_id = MAP_KROOLDK, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // K. Rool - DK Phase
	{.map_id = MAP_KROOLDIDDY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // K. Rool - Diddy Phase
	{.map_id = MAP_KROOLLANKY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // K. Rool - Lanky Phase
	{.map_id = MAP_KROOLTINY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // K. Rool - Tiny Phase
	{.map_id = MAP_KROOLCHUNKY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_at_boss=1}, // K. Rool - Chunky Phase
};

/*
	TODO: Swap K Rool model in "K Rool gets booted" to whatever the boss in the last phase is
	- Might be difficult with KKO
*/

void completeBoss(void) {
	// Spawn Key
	for (int i = 0; i < 7; i++) {
		if (BossMapArray[i] == CurrentMap) {
			for (int j = 0; j < sizeof(boss_spawn_data) / sizeof(boss_spawn_info); j++) {
				boss_spawn_info* tied_data = &boss_spawn_data[j];
				if (tied_data->map_id == CurrentMap) {
					if (tied_data->spawn_at_boss) {
						spawnKey(normal_key_flags[i], CurrentActorPointer_0->xPos + tied_data->x, CurrentActorPointer_0->yPos + tied_data->y, CurrentActorPointer_0->zPos + tied_data->z, tied_data->unk0, tied_data->unk1);
					} else if (tied_data->pen_id > -1) {
						pen_a_data* tied_pen = &FenceInformation->pen_A[tied_data->pen_id];
						spawnKey(normal_key_flags[i], tied_pen->x, tied_pen->y, tied_pen->z, tied_data->unk0, tied_data->unk1);
					} else {
						spawnKey(normal_key_flags[i], tied_data->x, tied_data->y, tied_data->z, tied_data->unk0, tied_data->unk1);
					}
					return;
				}
			}
			return;
		}
	}
	// Go to next boss in sequence
	for (int i = 0; i < 5; i++) {
		if (Rando.k_rool_order[i] == CurrentMap) {
			if ((i == 4) || (Rando.k_rool_order[i + 1] == 0xFF)) {
				if (CurrentMap != MAP_KROOLCHUNKY) {
					// Ending phase
					initiateTransitionFade(MAP_ISLES, 29, GAMEMODE_ADVENTURE);
				} else {
					playCutscene(CurrentActorPointer_0, 0x1A, 1);
				}
			} else {
				initiateTransition(Rando.k_rool_order[i + 1], 0);
			}
			return;
		}
	}
}

static unsigned char valid_lz_types[] = {9, 12, 13, 16};
void handleKRoolSaveProgress(void) {
	return;
	if (Rando.quality_of_life.save_krool_progress) {
		// Save Progress
		int krool_phase_diff = CurrentMap - MAP_KROOLDK;
		if ((krool_phase_diff >= 0) && (krool_phase_diff < 5)) {
			setFlag(FLAG_KROOL_ENTERED + krool_phase_diff, 1, FLAGTYPE_PERMANENT);
		}
		if (CurrentMap == MAP_ISLES) {
			// Wipe Progress
			if (
				((CutsceneActive == 1) && (CutsceneIndex == 29) && ((CutsceneStateBitfield & 4) == 0)) ||
				((CutsceneFadeActive) && (CutsceneFadeIndex == 29))	
			) {
				// K Rool flying cutscene
				for (int i = 0; i < 5; i++) {
					setFlag(FLAG_KROOL_ENTERED + i, 0, FLAGTYPE_PERMANENT);
				}
			}
			// Load Progress
			int latest_map = -1;
			for (int i = 1; i < 5; i++) {
				if (Rando.k_rool_order[i] != -1) {
					if (checkFlag(FLAG_KROOL_ENTERED + Rando.k_rool_order[i], 0)) {
						latest_map = MAP_KROOLDK + Rando.k_rool_order[i];
					}
				}
			}
			if (latest_map > -1) {
				for (int i = 0; i < TriggerSize; i++) {
					if ((TriggerArray[i].map >= MAP_KROOLDK) && (TriggerArray[i].map <= MAP_KROOLCHUNKY)) {
						for (int j = 0; j < sizeof(valid_lz_types); j++) {
							if (TriggerArray[i].type == valid_lz_types[j]) {
								TriggerArray[i].map = latest_map;
								return;
							}
						}
					}
				}
			}
		}
	}
}