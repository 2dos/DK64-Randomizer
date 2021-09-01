.align
ApplyFastStart:
    SW      ra, @ReturnAddress
    LA      a0, FastStartOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, ApplyFastStart_Finish
    NOP
    LA      a0, FastStartFlags
    JAL     SetAllFlags
    NOP
    LA      a0, TrainingBarrelFlags
    JAL     SetAllFlags
    NOP
    LA      a0, FairyQueenRewards
    JAL     SetAllFlags
    NOP
    // Slam
    LI      a0, 4
    LI      a1, @MovesBase
    LBU     a2, 0x1(a1)
    BNEZ    a2, ApplyFastStart_Finish
    NOP
    
    ApplyFastStart_WriteSlam:
        LI      t3, 0x1
        SB      t3, 0x1 (a1) // Slam Level 1
        BEQZ    a0, ApplyFastStart_Finish
        ADDI    a0, a0, -1 // Decrement Value for next kong
        B       ApplyFastStart_WriteSlam
        ADDIU   a1, a1, 0x5E // Next kong base

    ApplyFastStart_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

IslesSpawn:
    LA      a0, FastStartOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, IslesSpawn_Finish
    NOP
    SW      r0, 0x80714540 // Cancels check

    IslesSpawn_Finish:
        JR      ra
        NOP

.align 
FastStartOn:
    .byte 1

.align 
FastStartFlags:
    .half 386
    .half 387
    .half 388
    .half 389
    .half 0x1BB
    .half 0x186
    .half 0x17F
    .half 0x180
    .half 385

.align
FairyQueenRewards:
    .half 377