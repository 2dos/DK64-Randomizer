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

void replace_zones(int init_flag) {
	int race_flag = 0;
	int race_container_map = 0;
	int race_container_exit = 0;
	int krool_exit_map = 0;
	int krool_exit_exit = 0;
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