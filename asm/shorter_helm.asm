// Shorter Helm
// Spawn in Blast-o-Matic Area
ChangeLZToHelm:
    SW      ra, @ReturnAddress
    LA      a0, FastStartHelmOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, ChangeLZToHelm_Finish
    NOP
    LW      a0, @CurrentMap
    LI      a1, 0xAA
    BNE     a0, a1, ChangeLZToHelm_Finish
    NOP
    LW      a0, @ObjectTimer
    LI      a1, 3
    BNE     a0, a1, ChangeLZToHelm_Finish
    NOP
    LW      a0, @LZArray
    LHU     a1, @LZSize

    ChangeLZToHelm_CheckLZ:
        LHU     a2, 0x10 (a0)
        LI      a3, 9
        BNE     a2, a3, ChangeLZToHelm_Enumerate
        NOP
        LHU     a2, 0x12 (a0)
        LI      a3, 0x11
        BNE     a2, a3, ChangeLZToHelm_Enumerate
        NOP
        LHU     a2, 0x14 (a0)
        BNEZ    a2, ChangeLZToHelm_Enumerate
        NOP
        LI      a3, 3
        SH      a3, 0x14 (a0)
        // Story: Helm
        JAL     CodedSetPermFlag
        LI      a0, 0x1CC
        // Open I-II-III-IV-V doors
        LI      a0, 0x3B
        LI      a1, 1
        JAL     @SetFlag
        LI      a2, 2
        // Gates knocked down
        LI      a0, 0x46
        LI      a1, 1
        JAL     @SetFlag
        LI      a2, 2
        LI      a0, 0x47
        LI      a1, 1
        JAL     @SetFlag
        LI      a2, 2
        LI      a0, 0x48
        LI      a1, 1
        JAL     @SetFlag
        LI      a2, 2
        LI      a0, 0x49
        LI      a1, 1
        JAL     @SetFlag
        LI      a2, 2
        B       ChangeLZToHelm_Finish
        NOP

    ChangeLZToHelm_Enumerate:
        ADDIU   a0, a0, 0x3A
        ADDI    a1, a1, -1
        BEQZ    a1, ChangeLZToHelm_Finish
        NOP
        B       ChangeLZToHelm_CheckLZ
        NOP

    ChangeLZToHelm_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
FastStartHelmOn:
    .byte 1