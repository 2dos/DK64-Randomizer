#include "../../include/common.h"

ROM_RODATA_NUM const unsigned short replacement_lobbies_array[9] = {
	0xA9, 0xAD, 0xAF,
	0xAE, 0xB2, 0xC2,
	0xC1, 0xAA, 0xAA,
};
ROM_RODATA_NUM const unsigned short replacement_lobby_exits_array[9] = {
	1, 1, 1,
	1, 1, 1,
	1, 1, 1,
};

ROM_RODATA_NUM static const unsigned char vanilla_blast_maps[] = {
	MAP_JAPESBBLAST,
	MAP_AZTECBBLAST,
	MAP_FACTORYBBLAST,
	MAP_GALLEONBBLAST,
	MAP_FUNGIBBLAST,
	MAP_CAVESBBLAST,
	MAP_CASTLEBBLAST,
};

LZREntrance blast_entrances[] = {
	{.map = MAP_JAPESBBLAST, .exit = 0},
	{.map = MAP_AZTECBBLAST, .exit = 0},
	{.map = MAP_FACTORYBBLAST, .exit = 0},
	{.map = MAP_GALLEONBBLAST, .exit = 0},
	{.map = MAP_FUNGIBBLAST, .exit = 0},
	{.map = MAP_CAVESBBLAST, .exit = 0},
	{.map = MAP_CASTLEBBLAST, .exit = 0},
	{.map = MAP_ISLES, .exit = 23},  // Isles Blast warp
};

LZREntrance *blastWarpGetter(maps map) {
	if (map == MAP_ISLES) {
		return &blast_entrances[7];
	}
	for (int i = 0; i < 7; i++) {
		if (map == vanilla_blast_maps[i]) {
			return &blast_entrances[i];
		}
	}
	return 0;
}

void blastWarpHandler(maps map, int wrong_cs_enabled) {
	LZREntrance *temp = blastWarpGetter(map);
	if (!temp) {
		return;
	}
	if (wrong_cs_enabled) {
		setIntroStoryPlaying(2);
		setNextTransitionType(0);
	}
	initiateTransition_0(temp->map, temp->exit, 0, 0);
}