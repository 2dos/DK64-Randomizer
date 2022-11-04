KrushaConditionalScaleDown:
    LW      at, 0x58 (s2)
    ADDIU   t7, r0, 3
    BNE     at, t7, KrushaConditionalScaleDown_Default
    NOP
    LUI     at, 0x3E05
    ADDIU   at, at, 0x1EB8
    B       KrushaConditionalScaleDown_Finish
    MTC1    at, f2
    
    KrushaConditionalScaleDown_Default:
        LUI     at, 0x8075
        LWC1    f2, 0x7360 (at)

    KrushaConditionalScaleDown_Finish:
        J   0x806135B8
        NOP

controlKrushaSpeedup_Y:
    LW      at, 0x58 (s0)
    ADDIU   t8, r0, 3
    BNE     at, t8, controlKrushaSpeedup_YFinish
    LWC1    f0, 0x38 (v0)
    LUI     at, 0x3F94
    ADDIU   at, at, 0xB13B
    MTC1    at, f8
    MUL.S   f0, f0, f8

    controlKrushaSpeedup_YFinish:
        J       0x8066525C
        NOP