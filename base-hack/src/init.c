#include "../include/common.h"

static const char exittoisles[] = "EXIT TO ISLES";

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

void fixMusicRando(void) {
	// Music
	if (Rando.music_rando_on) {
		int size = 0x160;
		musicInfo* write_space = dk_malloc(size);
		int* file_size;
		*(int*)(&file_size) = size;
		copyFromROM(0x1FFF000,write_space,&file_size,0,0,0,0);
		for (int i = 0; i < 0xB0; i++) {
			int subchannel = (write_space->data[i] & 6) >> 1;
			int channel = (write_space->data[i] & 0x78) >> 3;
			songData[i] &= 0xFF81;
			songData[i] |= (subchannel & 3) << 1;
			songData[i] |= (channel & 0xF) << 3;
		}
		complex_free(write_space);
	}
}

void writeEndSequence(void) {
	int size = 0x84;
	int* file_size;
	*(int*)(&file_size) = size;
	copyFromROM(0x1FFF800,(int*)0x807506D0,&file_size,0,0,0,0);
}

static const short kong_flags[] = {385,6,70,66,117};
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
		DamageMultiplier = Rando.damage_multiplier;
		WarpToIslesEnabled = Rando.warp_to_isles_enabled;
		permaLossMode = Rando.perma_lose_kongs;
		preventTagSpawn = Rando.prevent_tag_spawn;
		bonusAutocomplete = Rando.resolve_bonus;
		QoLOn = Rando.quality_of_life;
		LobbiesOpen = Rando.lobbies_open_bitfield;
		changeCharSpawnerFlag(0x14, 2, 93); // Tie llama spawn to lanky help me cutscene flag
		changeCharSpawnerFlag(0x7, 1, kong_flags[(int)Rando.free_target_japes]);
		changeCharSpawnerFlag(0x10, 0x13, kong_flags[(int)Rando.free_target_ttemple]);
		changeCharSpawnerFlag(0x14, 1, kong_flags[(int)Rando.free_target_llama]);
		changeCharSpawnerFlag(0x1A, 1, kong_flags[(int)Rando.free_target_factory]);
		alterGBKong(0x22, 0x4, Rando.starting_kong); // First GB
		alterGBKong(0x7, 0x69, Rando.free_source_japes); // Front of Diddy Cage GB
		alterGBKong(0x7, 0x48, Rando.free_source_japes); // In Diddy's Cage
		alterGBKong(0x10, 0x5B, Rando.free_source_ttemple); // In Tiny's Cage
		alterGBKong(0x14, 0x6C, Rando.free_source_llama); // Free Lanky GB
		alterGBKong(0x1A, 0x78, Rando.free_source_factory); // Free Chunky GB
		if (Rando.no_health_refill) {
			*(int*)(0x80683A34) = 0; // Cancel Tag Health Refill
			// *(int*)(0x8060DD10) = 0; // Load File
			// *(int*)(0x806C8010) = 0; // Load into map with < 1 health
			// *(int*)(0x806C94E4) = 0; // ?
			// *(int*)(0x806C9BC0) = 0; // Multiplayer
			*(int*)(0x806CB340) = 0; // Voiding
			*(int*)(0x806DEFE4) = 0; // Fairies
			// *(int*)(0x80708C9C) = 0; // Bonus Barrels (Taking Damge) & Watermelons
			// *(int*)(0x80708CA4) = 0; // Bonus Barrels (Full Health) & Watermelons
			*(int*)(0x806A6EA8) = 0; // Bonus Barrels
		} else {
			*(int*)(0x806A6EA8) = 0x0C1C2519; // Set Bonus Barrel to refill health

		}
		if (Rando.resolve_bonus & 1) {
			*(short*)(0x806818DE) = 0x4248; // Make Aztec Lobby GB spawn above the trapdoor)
			*(int*)(0x80681690) = 0; // Make some barrels not play a cutscene
			*(int*)(0x8068188C) = 0; // Prevent disjoint mechanic for Caves/Fungi BBlast Bonus
			*(short*)(0x80681898) = 0x1000;
			*(int*)(0x8068191C) = 0; // Remove Oh Banana
		}
		if (Rando.kong_recolor_enabled) {
			*(char*)(0x8068A62F) = 0;
			*(int*)(0x8068A450) = 0;
			*(int*)(0x8068A458) = 0;
		}
		// for (int i = 0; i < 5; i++) {
		// 	DKTVData[i] = Rando.dktv_data[i];
		// }
		replace_zones(1);
		randomize_bosses();
		loadExtraHooks();
		no_enemy_drops();
		// Moves & Prices
		replace_moves();
		price_rando();
		if (!Rando.move_rando_on) {
			moveTransplant();
			if (!Rando.price_rando_on) {
				priceTransplant();
			}
		}
		if (Rando.disable_boss_kong_check) {
			*(int*)(0x8064EC00) = 0x24020001;
		}
		*(int*)(0x8074C1B8) = (int)&newCounterCode;
		fixMusicRando();
		// Disable Sniper Scope Overlay
		int asm_code = 0x00801025; // OR $v0, $a0, $r0
		*(int*)(0x806FF80C) = asm_code;
		*(int*)(0x806FF85C) = asm_code;
		*(int*)(0x806FF8AC) = asm_code;
		*(int*)(0x806FF8FC) = asm_code;
		*(int*)(0x806FF940) = asm_code;
		*(int*)(0x806FF988) = asm_code;
		*(int*)(0x806FF9D0) = asm_code;
		*(int*)(0x806FFA18) = asm_code;
		// Change Sniper Crosshair color
		*(short*)(0x806FFA92) = 0xFFD7;
		*(short*)(0x806FFA96) = 0x00FF;
		// *(int*)(0x806FFA90) = 0x3C0D8080;
		// *(int*)(0x806FFA94) = 0x8DADFFFC;
		// Style 6 Mtx
		int base_mtx = 75;
		style6Mtx[0x0] = base_mtx;
		style6Mtx[0x5] = base_mtx;
		style6Mtx[0xF] = 100;
		style6Mtx[0x8] = 0xEA00;
		style6Mtx[0x9] = 0xFD00;
		base_mtx = 12;
		style2Mtx[0x0] = base_mtx;
		style2Mtx[0x5] = base_mtx;
		style2Mtx[0xF] = 10;
		base_mtx = 50;
		style128Mtx[0x0] = base_mtx;
		style128Mtx[0x5] = base_mtx;
		style128Mtx[0xF] = 100;
		writeCoinRequirements(0);
		writeEndSequence();
		if (Rando.warp_to_isles_enabled) {
			// Pause Menu Exit To Isles Slot
			*(short*)(0x806A85EE) = 4; // Yes/No Prompt
			*(short*)(0x806A8716) = 4; // Yes/No Prompt
			//*(short*)(0x806A87BE) = 3;
			*(short*)(0x806A880E) = 4; // Yes/No Prompt
			//*(short*)(0x806A8766) = 4;
			*(short*)(0x806A986A) = 4; // Yes/No Prompt
			*(int*)(0x806A9990) = 0x2A210270; // SLTI $at, $s1, 0x2A8
			PauseSlot3TextPointer = (char*)&exittoisles;
		}
		if (Rando.quality_of_life) {
			*(int*)(0x80748010) = 0x8064F2F0; // Cancel Sandstorm
			*(short*)(0x80750680) = 0x22;
			*(short*)(0x80750682) = 0x1;
			*(int*)(0x806BDC24) = 0x0C17FCDE; // Change takeoff warp func
			*(short*)(0x806BDC8C) = 0x1000; // Apply no cutscene to all keys
			*(short*)(0x806BDC3C) = 0x1000; // Apply shorter timer to all keys
		}
		// Object Instance Scripts
		*(int*)(0x80748064) = (int)&change_object_scripts;
		*(int*)(0x806416BC) = 0; // Prevent parent map check in cross-map object change communications
		// Sniper Scope Check
		*(int*)(0x806D2988) = 0x93190002; // LBU $t9, 0x2 ($t8)
		*(int*)(0x806D2990) = 0x33210004; // ANDI $at, $t9, 0x4
		*(short*)(0x806D299C) = 0x1020; // BEQ $at, $r0
		// Speedy T&S Turn-Ins
		*(int*)(0x806BE3E0) = 0; // NOP
		// EEPROM Patch
		*(int*)(0x8060D588) = 0; // NOP
		// Cancel Tamper
		*(int*)(0x8060AEFC) = 0; // NOP
		*(int*)(0x80611788) = 0; // NOP
		// Fix HUD if DK not free
		*(int*)(0x806FA324) = 0; // NOP
		*(short*)(0x807505AE) = 385; // Set Flag to DK Flag
		// Fix CB Spawning
		*(short*)(0x806A7882) = 385; // DK Balloon
		// Fix Boss Doors if DK not free
		*(int*)(0x80649358) = 0; // NOP
		// Textbox Cancel
		*(int*)(0x8070E84C) = 0;
		*(int*)(0x8070E874) = 0;
		*(int*)(0x8070E888) = 0;
		LoadedHooks = 1;
	}
}