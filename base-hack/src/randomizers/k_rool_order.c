#include "../../include/common.h"

typedef struct boss_spawn_info {
	/* 0x000 */ unsigned char map_id;
	/* 0x001 */ char pen_id; // -1 for "doesn't respond to pen id"
	/* 0x002 */ short x;
	/* 0x004 */ short y;
	/* 0x006 */ short z;
	/* 0x008 */ short unk0;
	/* 0x00A */ char unk1;
	/* 0x00B */ char spawn_location; // 0 = respond to xyz, 1 = at boss, 2 = at player
} boss_spawn_info;

static const boss_spawn_info boss_spawn_data[] = {
	{.map_id = MAP_JAPESDILLO, .pen_id = 4, .x = 0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 6, .spawn_location=0}, // Japes Dillo
	{.map_id = MAP_CAVESDILLO, .pen_id = -1, .x = 0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=1}, // Caves Dillo - Spawns at boss, not sure what unk0 is
	{.map_id = MAP_GALLEONPUFFTOSS, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 1, .spawn_location=1}, // Pufftoss - Spawns at boss
	{.map_id = MAP_FUNGIDOGADON, .pen_id = 0x10, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 4, .spawn_location=0}, // Fungi Dogadon
	{.map_id = MAP_AZTECDOGADON, .pen_id = 0x10, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 4, .spawn_location=0}, // Aztec Dogadon
	{.map_id = MAP_CASTLEKUTOUT, .pen_id = -1, .x=0, .y=200, .z=40, .unk0 = 0x800, .unk1 = 1, .spawn_location=1}, // KKO - Spawns at boss
	{.map_id = MAP_FACTORYJACK, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x5DC, .unk1 = 1, .spawn_location=1}, // Mad Jack
	{.map_id = MAP_KROOLDK, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=2}, // K. Rool - DK Phase
	{.map_id = MAP_KROOLDIDDY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=2}, // K. Rool - Diddy Phase
	{.map_id = MAP_KROOLLANKY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=2}, // K. Rool - Lanky Phase
	{.map_id = MAP_KROOLTINY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=2}, // K. Rool - Tiny Phase
	{.map_id = MAP_KROOLCHUNKY, .pen_id = -1, .x=0, .y=0, .z=0, .unk0 = 0x800, .unk1 = 5, .spawn_location=2}, // K. Rool - Chunky Phase
};

/*
	TODO: Swap K Rool model in "K Rool gets booted" to whatever the boss in the last phase is
	- Might be difficult with KKO
	- Maybe for non KR win cons, have the model be based on the level you acquired the win con item from
*/

typedef struct boss_map_to_model {
	/* 0x000 */ short map;
	/* 0x002 */ short model;
} boss_map_to_model;

static const boss_map_to_model model_data[] = {
	{.map = MAP_JAPESDILLO, .model=0x38}, // Dillo - With Shell
	{.map = MAP_AZTECDOGADON, .model=0x3C}, // Dogadon
	{.map = MAP_FACTORYJACK, .model=0x25}, // Mad Jack
	{.map = MAP_GALLEONPUFFTOSS, .model=0x3B}, // Puff
	{.map = MAP_FUNGIDOGADON, .model=0x3C}, // Dogadon
	{.map = MAP_CAVESDILLO, .model=0x63}, // Dillo - No Shell
	{.map = MAP_CASTLEKUTOUT, .model=0xDC}, // KKO - Head
};

void swap_ending_cutscene_model(void) {
	int model = 0x68;
	if (CurrentMap == MAP_ISLES) {
		int phase_map = 0xFF;
		for (int i = 0; i < 5; i++) {
			if (Rando.k_rool_order[i] != 0xFF) {
				phase_map = Rando.k_rool_order[i];
			}
		}
		for (int i = 0; i < 7; i++) {
			if (phase_map == model_data[i].map) {
				model = model_data[i].model;
			}
		}
	}
	*(short*)(0x80755764) = model;
}

static short maps_with_extended_end_cs[] = {
	// MAP_KROOLDK, // n64 lol
	// MAP_KROOLDIDDY, // n64 lol
	// MAP_KROOLLANKY, // n64 lol
	// MAP_KROOLTINY, // n64 lol
	MAP_KROOLCHUNKY,
};

void completeBoss(void) {
	// Spawn Key
	for (int i = 0; i < 7; i++) {
		if (BossMapArray[i] == CurrentMap) {
			for (int j = 0; j < sizeof(boss_spawn_data) / sizeof(boss_spawn_info); j++) {
				boss_spawn_info* tied_data = &boss_spawn_data[j];
				if (tied_data->map_id == CurrentMap) {
					if (tied_data->spawn_location == 1) {
						spawnKey(normal_key_flags[i], CurrentActorPointer_0->xPos + tied_data->x, CurrentActorPointer_0->yPos + tied_data->y, CurrentActorPointer_0->zPos + tied_data->z, tied_data->unk0, tied_data->unk1);
					} else if (tied_data->spawn_location == 2) {
						spawnKey(normal_key_flags[i], Player->xPos + tied_data->x, Player->yPos + tied_data->y, Player->zPos + tied_data->z, tied_data->unk0, tied_data->unk1);
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
				// Ending phase
				if (inShortList(CurrentMap, &maps_with_extended_end_cs, sizeof(maps_with_extended_end_cs) >> 1)) {
					playCutscene(CurrentActorPointer_0, 0x1A, 1);
					renderingParamsData* render = Player->rendering_param_pointer;
					render->scale_x = 0.0f;
					render->scale_y = 0.0f;
					render->scale_z = 0.0f;
				} else {
					initiateTransitionFade(MAP_ISLES, 29, GAMEMODE_ADVENTURE);
				}
			} else {
				maps next_map = Rando.k_rool_order[i + 1];
				initiateTransition(next_map, 0);
				// Some minor logic to prevent unbeatable bosses with no K Rool progress save
				if (next_map == MAP_FUNGIDOGADON) {
					Character = KONG_CHUNKY;
				} else if (next_map == MAP_FACTORYJACK) {
					Character = KONG_TINY;
				}
			}
			return;
		}
	}
}

void fixKRoolKong(void) {
	for (int i = 0; i < 5; i++) {
		if (Rando.k_rool_order[i] == DestMap) {
			if (DestMap == MAP_FACTORYJACK) {
				Character = KONG_TINY;
			} else if (DestMap == MAP_FUNGIDOGADON) {
				Character = KONG_CHUNKY;
			}
			return;
		}
	}
}

static unsigned char valid_lz_types[] = {9, 12, 13, 16};
void handleKRoolSaveProgress(void) {
	if (Rando.quality_of_life.save_krool_progress) {
		// Save Progress
		for (int i = 0; i < 5; i++) {
			if (Rando.k_rool_order[i] == CurrentMap) {
				setFlag(FLAG_KROOL_ENTERED + i, 1, FLAGTYPE_PERMANENT);
			}
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
				if (checkFlag(FLAG_KROOL_ENTERED + i, FLAGTYPE_PERMANENT)) {
					if (Rando.k_rool_order[i] != 0xFF) {
						latest_map = Rando.k_rool_order[i];
					}
				}
			}
			if (latest_map > -1) {
				for (int i = 0; i < TriggerSize; i++) {
					if (inBossMap(TriggerArray[i].map, 1, 1, 1)) {
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