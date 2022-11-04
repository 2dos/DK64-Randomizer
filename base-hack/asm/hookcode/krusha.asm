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

warpGrowFix:
    LUI     at, hi(CurrentActorPointer_0)
    LW      at, lo(CurrentActorPointer_0) (at)
    BEQZ    at, warpGrowFix_Normal
    NOP
    LW      at, 0x58 (at)
    ADDIU   v0, r0, 3
    BNE     at, v0, warpGrowFix_Normal
    NOP
    LUI     at, 0x3C55
    ADDIU   at, at, 0xFDF4
    MTC1    at, f10
    B       warpGrowFix_Finish
    CVT.D.S f10, f10

    warpGrowFix_Normal:
        LUI     at, 0x8076
        LDC1    f10, 0xCFA0 (at)

    warpGrowFix_Finish:
        J   0x806DC350
        NOP
