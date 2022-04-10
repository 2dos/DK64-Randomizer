#include "../../include/common.h"
/*
	Kong is going to be stored in the 0x4 slot of the purchase struct
	Price is changed to a byte, changed to 0x5 slot
	struct {
		short type;
		short value
		unsigned char kong;
		unsigned char price;
	}
*/

void crossKongInit(void) {
	// Change target kong (Progressive)
	*(int*)(0x80025EA0) = 0x90850004; // LBU 	a1, 0x4 (a0)
	// Change target kong (Bitfield)
	*(int*)(0x80025E80) = 0x90850004; // LBU 	a1, 0x4 (a0)
	// Change price check
	*(int*)(0x80026200) = 0x90CF0005; // LBU 	t7, 0x5 (a2)
}

/* 
	HOOKCODE

	Placement_80026140:
		// Stores price & kong correctly
		LH 		v0, 0x4 (a1)
		SH 		v0, 0x4 (s2)
		ANDI 	t8, v0, 0xFF
		J 		0x8002614C
		SH 		t8, 0x0 (t2)

	Placement_80025FC0:
		// Replaces param2 with the start of the character collectable base
		OR 		s2, a0, r0
		LUI 	a1, hi(MovesBase)
		ADDIU	a1, a1, lo(MovesBase)
		J 		0x80025FC8
		OR 		s3, a1, r0

	Placement_800260F0:
		// Sets the move base to the correct kong (Bitfield)
		LH 		t4, 0x2 (a1)
		ADDU 	t8, s3, a0
		LBU 	t9, 0x4 (a1)
		ADDIU 	t6, r0, 0x5E
		MULT 	t9, t6
		MFLO 	t9
		J 		0x800260F8
		ADDU 	t8, t8, t9

	Placement_8002611C:
		// Sets the move base to the correct kong (Progressive)
		LBU 	t6, 0x4 (a1)
		ADDIU 	t5, r0, 0x5E
		MULT 	t6, t5
		MFLO	t6
		ADDU 	t4, t4, t6
		LBU 	t6, 0x0 (t4)
		J 		0x80026124
		LH 		t5, 0x2 (a1)
*/