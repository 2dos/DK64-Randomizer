ObjectRotate:
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x288
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x90
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x18D
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x13C
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDE
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xE0
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xE1
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDD
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDF
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x48
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x28F
    BEQ     v0, at, ObjectRotate_ApplyRotate
    NOP
    J       0x80637150
    NOP

    ObjectRotate_ApplyRotate:
        J       0x80637160
        NOP
        
NintendoCoinEffect:
    BEQ     a0, at, NintendoCoinEffect_Melon
    LUI     t1, 0x8074
    ADDIU   at, r0, 0x48
    BEQ     a0, at, NintendoCoinEffect_Coin
    NOP
    J       0x806F7B18
    NOP

    NintendoCoinEffect_Coin:
        LBU     t1, 0x5838 (t1)
        J       0x806F7BC8
        ADDIU   a0, r0, 22

    NintendoCoinEffect_Melon:
        J       0x806F7BC0
        NOP

RarewareCoinEffect:
    BEQ     t7, at, RarewareCoinEffect_RaceCoin
    ADDIU   at, 0x28F
    BEQ     t7, at, RarewareCoinEffect_Coin
    ADDIU   at, 0x288
    J       0x806F7A2C
    NOP

    RarewareCoinEffect_Coin:
        LUI     t6, 0x8074
        LBU     t6, 0x5838 (t6)
        J       0x806F7ED0
        ADDIU   a0, r0, 22

    RarewareCoinEffect_RaceCoin:
        J       0x806F7EC4
        NOP