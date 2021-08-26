FixCastleAutowalk:
    LW      a0, @CurrentMap
    LI      a1, 0x57 // Castle
    BNE     a0, a1, FixCastleAutowalk_Finish
    NOP
    LBU     a0, @CutsceneActive
    BEQZ    a0, FixCastleAutowalk_Finish
    NOP
    LHU     a0, @CutsceneIndex
    LI      a1, 29 // Exit Portal
    BNE     a0, a1, FixCastleAutowalk_Finish
    NOP
    LW      a0, @CutsceneType
    LI      a1, 0x807F5BF0
    BNE     a0, a1, FixCastleAutowalk_Finish
    NOP
    LBU     a0, @IsAutowalking
    BEQZ    a0, FixCastleAutowalk_Finish
    NOP
    //SB      r0, @IsAutowalking

    FixCastleAutowalk_Finish:
        JR      ra
        NOP