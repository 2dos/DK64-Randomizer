/**
 * @file file.c
 * @author Ballaam
 * @brief Initialize save file changes
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

static int new_file_size = 0;

int getNewFileSize(void) {
	return new_file_size;
}

void expandSaveFile(int static_expansion, int actor_count) {
	/**
	 * @brief Expand save file to account for expanded data, including flags and larger GB capacity
	 * 
	 */
	/*
		File cannot be bigger than 0x200 bytes

		File Structure:
			0x000->0x320 = Flags
			0x320->c+0x320 = Model2
			c+0x320->c+0x645 = Kong Vars
			c+0x645->c+0x6B7 = File Global Vars

		Generalized:
			0 -> f = Flags
			f -> f+c = Model 2
			f+c -> f+c+5k = Kong Vars
			f+c+5k -> f+c+5k+0x72 = File Global Vars
	*/
	// int expansion = static_expansion;
	int expansion = static_expansion + actor_count;
	int flag_block_size = 0x320 + expansion;
	int targ_gb_bits = 5; // Max 127
	int added_bits = (targ_gb_bits - 3) * 8;
	int kong_var_size = 0xA1 + added_bits;
	int file_info_location = flag_block_size + (5 * kong_var_size);
	int file_default_size = file_info_location + 0x72;
	new_file_size = file_default_size;
	// Flag Block Size
	*(short*)(0x8060E36A) = file_default_size;
	*(short*)(0x8060E31E) = file_default_size;
	*(short*)(0x8060E2C6) = file_default_size;
	*(short*)(0x8060D54A) = file_default_size;
	*(short*)(0x8060D4A2) = file_default_size;
	*(short*)(0x8060D45E) = file_default_size;
	*(short*)(0x8060D3C6) = file_default_size;
	*(short*)(0x8060D32E) = file_default_size;
	*(short*)(0x8060D23E) = file_default_size;
	*(short*)(0x8060CF62) = file_default_size;
	*(short*)(0x8060CC52) = file_default_size;
	*(short*)(0x8060C78A) = file_default_size;
	*(short*)(0x8060C352) = file_default_size;
	*(short*)(0x8060BF96) = file_default_size;
	*(short*)(0x8060BA7A) = file_default_size;
	*(short*)(0x8060BEC6) = file_info_location;
	// Increase GB Storage Size
	*(short*)(0x8060BE12) = targ_gb_bits; // Bit Size
	*(short*)(0x8060BE06) = targ_gb_bits << 3; // Allocation for all levels
	*(short*)(0x8060BE2A) = 0x4021; // SUBU -> ADDU
	*(int*)(0x8060BCC0) = 0x24090000 | kong_var_size; // ADDIU $t1, $r0, kong_var_size
	*(int*)(0x8060BCC4) = 0x01C90019; // MULTU $t1, $t6
	*(int*)(0x8060BCC8) = 0x00004812; // MFLO $t1
	*(int*)(0x8060BCCC) = 0; // NOP
	// Model 2 Start
	*(short*)(0x8060C2F2) = flag_block_size;
	*(short*)(0x8060BCDE) = flag_block_size;
	// Reallocate Balloons + Patches
	*(short*)(0x80688BCE) = 0x320 + static_expansion; // Reallocated to just before model 2 block
}

void initFiles(void) {
	/**
	 * @brief Initialize file changes, including reducing the file count from 4 to 1
	 * 
	 */
    // Save File Expansion
    int balloon_patch_count = 300; // Normally 121
	int static_expansion = static_expansion_size;
	if (Rando.archipelago) {
		static_expansion += ARCHIPELAGO_FLAG_SIZE;
	}
    expandSaveFile(static_expansion,balloon_patch_count);
    // 1-File Fixes
    *(int*)(0x8060CF34) = 0x240E0001; // Slot 1
    *(int*)(0x8060CF38) = 0x240F0002; // Slot 2
    *(int*)(0x8060CF3C) = 0x24180003; // Slot 3
    *(int*)(0x8060CF40) = 0x240D0000; // Slot 0
    *(int*)(0x8060D3AC) = 0; // Prevent EEPROM Shuffle
    *(int*)(0x8060DCE8) = 0; // Prevent EEPROM Shuffle
    // *(int*)(0x8060C760) = 0x24900000; // Always load file 0
    // *(short*)(0x8060CC22) = 1; // File Loop Cancel 1
    *(short*)(0x8060CD1A) = 1; // File Loop Cancel 2
    *(short*)(0x8060CE7E) = 1; // File Loop Cancel 3
    *(short*)(0x8060CE5A) = 1; // File Loop Cancel 4
    *(short*)(0x8060CF0E) = 1; // File Loop Cancel 5
    *(short*)(0x8060CF26) = 1; // File Loop Cancel 6
    //*(short*)(0x8060D0DE) = 1; // File Loop Cancel 7
    *(short*)(0x8060D106) = 1; // File Loop Cancel 8
    *(short*)(0x8060D43E) = 1; // File Loop Cancel 8
    *(int*)(0x8060CD08) = 0x26670000; // Save to File - File Index
    *(int*)(0x8060CE48) = 0x26670000; // Save to File - File Index
    *(int*)(0x8060CF04) = 0x26270000; // Save to File - File Index
    *(int*)(0x8060BFA4) = 0x252A0000; // Global Block after 1 file entry
    *(int*)(0x8060E378) = 0x258D0000; // Global Block after 1 file entry
    *(int*)(0x8060D33C) = 0x254B0000; // Global Block after 1 file entry
    *(int*)(0x8060D470) = 0x256C0000; // Global Block after 1 file entry
    *(int*)(0x8060D4B0) = 0x252A0000; // Global Block after 1 file entry
    *(int*)(0x8060D558) = 0x258D0000; // Global Block after 1 file entry
    *(int*)(0x8060CF74) = 0x25090000; // Global Block after 1 file entry
    // *(int*)(0x8060CFCC) = 0x25AE0000; // Global Block after 1 file entry
    *(int*)(0x8060D24C) = 0x25AE0000; // Global Block after 1 file entry
    *(int*)(0x8060C84C) = 0xA02067C8; // Force file 0
    *(int*)(0x8060C654) = 0x24040000; // Force file 0 - Save
    *(int*)(0x8060C664) = 0xAFA00034; // Force file 0 - Save
    *(int*)(0x8060C6C4) = 0x24040000; // Force file 0 - Read
    *(int*)(0x8060C6D4) = 0xAFA00034; // Force file 0 - Read
    *(int*)(0x8060D294) = 0; // Cartridge EEPROM Wipe cancel
}