KrushaConditionalScaleDown:
    LW      at, 0x58 (s2)
    LUI     t7, hi(KrushaSlot)
    LBU     t7, lo(KrushaSlot) (t7)
    ADDIU   t7, t7, 2
    BNE     at, t7, KrushaConditionalScaleDown_Default
    ADDIU   t7, r0, 5
    BEQ     at, t7, KrushaConditionalScaleDown_ScaleTiny
    ADDIU   t7, r0, 3
    BNE     at, t7, KrushaConditionalScaleDown_Default
    NOP

    KrushaConditionalScaleDown_ScaleDiddy:
        LUI     at, 0x3E05
        ADDIU   at, at, 0x1EB8
        B       KrushaConditionalScaleDown_Finish
        MTC1    at, f2

    KrushaConditionalScaleDown_ScaleTiny:
        LUI     at, 0x3DCD
        ADDIU   at, at, 0xCCCD
        B       KrushaConditionalScaleDown_Finish
        MTC1    at, f2
    
    KrushaConditionalScaleDown_Default:
        LUI     at, 0x8075
        LWC1    f2, 0x7360 (at)

    KrushaConditionalScaleDown_Finish:
        J   0x806135B8
        NOP

controlKrushaSpeedup_Y:
    LWC1    f0, 0x38 (v0)
    LW      at, 0x58 (s0)
    LUI     t8, hi(KrushaSlot)
    LBU     t8, lo(KrushaSlot) (t8)
    ADDIU   t8, t8, 2
    BNE     at, t8, controlKrushaSpeedup_YFinish
    ADDIU   t8, r0, 5
    BEQ     at, t8, controlKrushaSpeedup_YScaleTiny
    ADDIU   t8, r0, 3
    BNE     at, t8, controlKrushaSpeedup_YFinish
    NOP

    controlKrushaSpeedup_YScaleDiddy:
        LUI     at, 0x3F94
        ADDIU   at, at, 0xB13B
        MTC1    at, f8
        B       controlKrushaSpeedup_YFinish
        MUL.S   f0, f0, f8

    controlKrushaSpeedup_YScaleTiny:
        LUI     at, 0x3FC0
        ADDIU   at, at, 0x0000
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
    LUI     v0, hi(KrushaSlot)
    LBU     v0, lo(KrushaSlot) (v0)
    ADDIU   v0, v0, 2
    BNE     at, v0, warpGrowFix_Normal
    ADDIU   v0, r0, 5
    BEQ     at, v0, warpGrowFix_ShrinkTiny
    ADDIU   v0, r0, 3
    BNE     at, v0, warpGrowFix_Normal
    NOP

    warpGrowFix_ShrinkDiddy:
        LUI     at, 0x3C55
        ADDIU   at, at, 0xFDF4
        MTC1    at, f10
        B       warpGrowFix_Finish
        CVT.D.S f10, f10

    warpGrowFix_ShrinkTiny:
        LUI     at, 0x3C24
        ADDIU   at, at, 0xD70A
        MTC1    at, f10
        B       warpGrowFix_Finish
        CVT.D.S f10, f10

    warpGrowFix_Normal:
        LUI     at, 0x8076
        LDC1    f10, 0xCFA0 (at)

    warpGrowFix_Finish:
        J   0x806DC350
        NOP

FallTooFarFix:
    LWC1    f4, 0x38 (t7)
    LW      t8, 0x58 (t6)
    LUI     t9, hi(KrushaSlot)
    LBU     t9, lo(KrushaSlot) (t9)
    ADDIU   t9, t9, 2
    BNE     t8, t9, FallTooFarFix_Finish
    ADDIU   t9, r0, 3
    BEQ     t8, t9, FallTooFarFix_Diddy
    ADDIU   t9, r0, 5
    BNE     t8, t9, FallTooFarFix_Finish
    NOP

    FallTooFarFix_Tiny:
        B       FallTooFarFix_ApplyScale
        LUI     t9, 0x3FC0

    FallTooFarFix_Diddy:
        LUI     t9, 0x3F94
        ADDIU   t9, t9, 0xB13A

    FallTooFarFix_ApplyScale:
        MTC1    t9, f6
        MUL.S   f4, f4, f6

    FallTooFarFix_Finish:
        J       0x806D362C
        LUI     t8, 0x8080