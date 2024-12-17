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
	int more_lz_byte = Rando.randomize_more_loading_zones;
	if (more_lz_byte) {
		if (init_flag) {
			if (more_lz_byte == 1) {
				for (int i = 0; i < 8; i++) {
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
	}
	if ((more_lz_byte == 0) || (more_lz_byte == 2)) {
		if (init_flag) {
			for (int i = 0; i < 9; i++) {
				ReplacementLobbiesArray[i] = LobbiesArray[i];
				ReplacementLobbyExitsArray[i] = 1;
			}
		}
	}
}

static const unsigned char vanilla_blast_maps[] = {
	MAP_JAPESBBLAST,
	MAP_AZTECBBLAST,
	MAP_FACTORYBBLAST,
	MAP_GALLEONBBLAST,
	MAP_FUNGIBBLAST,
	MAP_CAVESBBLAST,
	MAP_CASTLEBBLAST,
};

void blastWarpHandler(maps map, int wrong_cs_enabled) {
	for (int i = 0; i < 7; i++) {
		if (map == vanilla_blast_maps[i]) {
			if (wrong_cs_enabled) {
				setIntroStoryPlaying(2);
				setNextTransitionType(0);
			}
			initiateTransition_0(Rando.blast_entrances[i].map, Rando.blast_entrances[i].exit, 0, 0);
			return;
		}
	}
}