#include "../../include/common.h"

/*
	Exiting races:
		- Aztec Beetle Race (!)
		- Caves Beetle Race (!)
		- Seal Race (!)
		- Factory Car Race (!)
		- Castle Car Race (!)
	Exiting Levels (!)
	Entering Levels (!)
	Entering Seasick (!)
	Entering Mech Fish // Ignore - This one is weird
	Entering Aztec Beetle Race (!)
	Enter Fungi Minecart (!)
	Exit K Rool (!)
	Exit Fungi Minecart (!)
	Exit Japes Minecart (!)
	Exit Castle Minecart (!)
	Enter Castle Lobby (!)
*/

typedef struct race_exit_mapping {
	/* 0x000 */ maps map_index;
	/* 0x004 */ LZREntrance* entrance;
} race_exit_mapping;

static const race_exit_mapping race_exits[] = {
	{.map_index = MAP_JAPESMINECART, .entrance = &Rando.japes_minecart_exit},
	{.map_index = MAP_AZTECBEETLE, .entrance = &Rando.aztec_beetle_exit},
	{.map_index = MAP_FACTORYCARRACE, .entrance = &Rando.factory_car_exit},
	{.map_index = MAP_GALLEONSEALRACE, .entrance = &Rando.seal_race_exit},
	{.map_index = MAP_FUNGIMINECART, .entrance = &Rando.fungi_minecart_exit},
	{.map_index = MAP_CAVESBEETLERACE, .entrance = &Rando.caves_beetle_exit},
	{.map_index = MAP_CASTLEMINECART, .entrance = &Rando.castle_minecart_exit},
	{.map_index = MAP_CASTLECARRACE, .entrance = &Rando.castle_car_exit},
};

void replace_zones(int init_flag) {
	if (Rando.randomize_more_loading_zones) {
		if (init_flag) {
			if (Rando.randomize_more_loading_zones == 1) {
				for (int i = 0; i < 8; i++) {
					if (i < 7) {
						WorldArray[i] = Rando.enter_levels[i].map;
						WorldExitArray[i] = Rando.enter_levels[i].exit;
						if ((WorldArray[i] != MAP_CASTLE) || (WorldExitArray[i] != 0)) {
							WorldCutsceneArray[i] = 0;
						}
					}
					ReplacementLobbiesArray[i] = Rando.exit_levels[i].map;
					ReplacementLobbyExitsArray[i] = Rando.exit_levels[i].exit;
					ReplacementLobbiesArray[8] = ReplacementLobbiesArray[7];
					ReplacementLobbyExitsArray[8] = ReplacementLobbyExitsArray[7];
				}
				for (int i = 0; i < 8; i++) {
					int target_map = RaceExitArray[i].race_map;
					for (int j = 0; j < (int)(sizeof(race_exits) / sizeof(race_exit_mapping)); j++) {
						if (target_map == race_exits[j].map_index) {
							RaceExitArray[i].container_map = race_exits[j].entrance->map;
							RaceExitArray[i].container_exit = race_exits[j].entrance->exit;
						}
					}
				}
			}
		} else {
			if (TransitionSpeed < 0) {
				if (CurrentMap == MAP_ISLES) {
					if (isRDRAM(CastleCannonPointer)) {
						if (CastleCannonPointer->source_map == MAP_ISLES) {
							CastleCannonPointer->destination_map = Rando.castle_lobby_enter.map;
							CastleCannonPointer->destination_exit = Rando.castle_lobby_enter.exit;
						}
					}
				}
			}
		}
	} else {
		if (init_flag) {
			for (int i = 0; i < 9; i++) {
				ReplacementLobbiesArray[i] = LobbiesArray[i];
				ReplacementLobbyExitsArray[i] = 1;
			}
		}
	}
}