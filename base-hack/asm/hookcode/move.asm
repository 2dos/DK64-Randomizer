BarrelMovesFixes:
    LBU 	t0, 0x4238 (t0) // Load Barrel Moves Array Slot
    ADDI 	t0, t0, -1 // Reduce move_value by 1
    ADDIU 	v1, r0, 1
    SLLV 	t0, v1, t0 // Get bitfield value
    AND  	v1, t0, t9
    BEQZ 	v1, BarrelMovesFixes_Finish
    NOP
    ADDIU 	v1, r0, 1

    BarrelMovesFixes_Finish:
        J 		0x806F6EB4
        NOP

ChimpyChargeFix:
    ANDI 	t6, t6, 1
    LUI	 	v1, 0x8080
    J 		0x806E4938
    ADDIU 	v1, v1, 0xBB40

OStandFix:
    LBU 	t2, 0xCA0C (t2)
    ANDI 	t2, t2, 1
    J 		0x806E48B4
    ADDIU 	a0, r0, 0x25

HunkyChunkyFix2:
    BNEL 	v1, at, HunkyChunkyFix2_Finish
    LI 		at, 4
    ANDI 	a2, a0, 1
    BLEZL 	a2, HunkyChunkyFix2_Finish
    LI 		at, 4
    J 		0x8067ECC8
    NOP

    HunkyChunkyFix2_Finish:
        J 		0x8067ECD0
        nop