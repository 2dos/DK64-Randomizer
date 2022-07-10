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

#define ISLES_OVERWORLD 0x22

void replace_zones(int init_flag) {
	int race_flag = 0;
	int race_container_map = 0;
	int race_container_exit = 0;
	int krool_exit_map = 0;
	int krool_exit_exit = 0;
	if (Rando.randomize_more_loading_zones) {
		if (init_flag) {
			for (int i = 0; i < 8; i++) {
				if (i < 7) {
					WorldArray[i] = (Rando.enter_levels[i] >> 8) & 0xFF;
					WorldExitArray[i] = Rando.enter_levels[i] & 0xFF;
				}
				ReplacementLobbiesArray[i] = (Rando.exit_levels[i] >> 8) & 0xFF;
				ReplacementLobbyExitsArray[i] = Rando.exit_levels[i] & 0xFF;
				ReplacementLobbiesArray[8] = ReplacementLobbiesArray[7];
				ReplacementLobbyExitsArray[8] = ReplacementLobbyExitsArray[7];
			}
			krool_exit_map = (Rando.k_rool_exit >> 8) & 0xFF;
			krool_exit_exit = Rando.k_rool_exit & 0xFF;
			*(short*)(0x806A8986) = krool_exit_map;
			*(short*)(0x806A898E) = krool_exit_exit;
			*(short*)(0x80628032) = krool_exit_map;
			*(short*)(0x8062803A) = krool_exit_exit;
			for (int i = 0; i < 8; i++) {
				race_flag = 0;
				switch(RaceExitArray[i].race_map) {
					case 0x06: // Japes Minecart
						race_flag = 1;
						race_container_map = (Rando.japes_minecart_exit >> 8) & 0xFF;
						race_container_exit = Rando.japes_minecart_exit & 0xFF;
						break;
					case 0x0E: // Aztec Beetle Race
						race_flag = 1;
						race_container_map = (Rando.aztec_beetle_exit >> 8) & 0xFF;
						race_container_exit = Rando.aztec_beetle_exit & 0xFF;
						break;
					case 0x1B: // Factory Car Race
						race_flag = 1;
						race_container_map = (Rando.factory_car_exit >> 8) & 0xFF;
						race_container_exit = Rando.factory_car_exit & 0xFF;
						break;
					case 0x27: // Seal Race
						race_flag = 1;
						race_container_map = (Rando.seal_race_exit >> 8) & 0xFF;
						race_container_exit = Rando.seal_race_exit & 0xFF;
						break;
					case 0x37: // Fungi Minecart
						race_flag = 1;
						race_container_map = (Rando.fungi_minecart_exit >> 8) & 0xFF;
						race_container_exit = Rando.fungi_minecart_exit & 0xFF;
						break;
					case 0x52: // Caves Beetle Race
						race_flag = 1;
						race_container_map = (Rando.caves_beetle_exit >> 8) & 0xFF;
						race_container_exit = Rando.caves_beetle_exit & 0xFF;
						break;
					case 0x6A: // Castle Minecart
						race_flag = 1;
						race_container_map = (Rando.castle_minecart_exit >> 8) & 0xFF;
						race_container_exit = Rando.castle_minecart_exit & 0xFF;
						break;
					case 0xB9: // Castle Car Race
						race_flag = 1;
						race_container_map = (Rando.castle_car_exit >> 8) & 0xFF;
						race_container_exit = Rando.castle_car_exit & 0xFF;
					break;
				}
				if (race_flag) {
					RaceExitArray[i].container_map = race_container_map;
					RaceExitArray[i].container_exit = race_container_exit;
				}
			}
		} else {
			if (TransitionSpeed < 0) {
				if (CurrentMap == ISLES_OVERWORLD) {
					if (isRDRAM(CastleCannonPointer)) {
						if (CastleCannonPointer->source_map == ISLES_OVERWORLD) {
							CastleCannonPointer->destination_map = (Rando.castle_lobby_enter >> 8) & 0xFF;
							CastleCannonPointer->destination_exit = Rando.castle_lobby_enter & 0xFF;
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