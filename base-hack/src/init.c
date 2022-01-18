#include "../include/common.h"

void initHack(void) {
	if ((LoadedHooks == 0) && (CurrentMap == 0x28)) {
		DebugInfoOn = 1;
		*(int*)(0x80731F78) = 0; // Debug 1 Column
		*(int*)(0x8060E04C) = 0; // Prevent moves overwrite
		*(short*)(0x8060DDAA) = 0; // Writes readfile data to moves
		*(short*)(0x806C9CDE) = 7; // GiveEverything, write to bitfield. Seems to be unused but might as well
		// Strong Kong
		*(int*)(0x8067ECFC) = 0x30810002; // ANDI $at $a0 2
		*(int*)(0x8067ED00) = 0x50200003; // BEQL $at $r0 3
		// Rocketbarrel
		*(int*)(0x80682024) = 0x31810002; // ANDI $at $t4 2
		*(int*)(0x80682028) = 0x50200006; // BEQL $at $r0 0x6
		// OSprint
		*(int*)(0x8067ECE0) = 0x30810004; // ANDI $at $a0 4
		*(int*)(0x8067ECE4) = 0x10200002; // BEQZ $at, 2
		// Mini Monkey
		*(int*)(0x8067EC80) = 0x30830001; // ANDI $v1 $a0 1
		*(int*)(0x8067EC84) = 0x18600002; // BLEZ $v1 2
		// Hunky Chunky (Not Dogadon)
		*(int*)(0x8067ECA0) = 0x30810001; // ANDI $at $a0 1
		*(int*)(0x8067ECA4) = 0x18200002; // BLEZ $at 2
		// PTT
		*(int*)(0x806E20F0) = 0x31010002; // ANDI $at $t0 2
		*(int*)(0x806E20F4) = 0x5020000F; // BEQL $at $r0 0xF
		// PPUnch
		*(int*)(0x806E48F4) = 0x31810002; // ANDI $at $t4 2
		*(int*)(0x806E48F8) = 0x50200074; // BEQL $at $r0 0xF
		replace_zones(1);
		randomize_bosses();
		loadExtraHooks();
		LoadedHooks = 1;
	}
}