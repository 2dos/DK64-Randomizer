#include "../../include/common.h"

void initKongRando(void) {
	changeCharSpawnerFlag(MAP_AZTECLLAMATEMPLE, 2, 93); // Tie llama spawn to lanky help me cutscene flag
	alterGBKong(MAP_ISLES, 0x4, Rando.starting_kong); // First GB
	alterGBKong(MAP_JAPES, 0x69, Rando.free_source_japes); // Front of Diddy Cage GB
	alterGBKong(MAP_JAPES, 0x48, Rando.free_source_japes); // In Diddy's Cage
	alterGBKong(MAP_AZTECTINYTEMPLE, 0x5B, Rando.free_source_ttemple); // In Tiny's Cage
	alterGBKong(MAP_AZTECLLAMATEMPLE, 0x6C, Rando.free_source_llama); // Free Lanky GB
	alterGBKong(MAP_FACTORY, 0x78, Rando.free_source_factory); // Free Chunky GB
}