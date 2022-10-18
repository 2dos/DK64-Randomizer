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
    ADDIU   at, r0, 0x5B
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F2
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F3
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F5
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F6
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x59
    BEQ     v0, at, ObjectRotate_ApplyRotate
    NOP
    J       0x80637150
    NOP

    ObjectRotate_ApplyRotate:
        J       0x80637160
        NOP
        
NintendoCoinEffect:
    BEQ     a0, at, NintendoCoinEffect_Orange
    ADDIU   a1, r0, 0x7FFF
    ADDIU   at, r0, 0x48
    BEQ     a0, at, NintendoCoinEffect_Coin
    NOP
    J       0x806F7B38
    NOP

    NintendoCoinEffect_Coin:
        LUI     t1, 0x8074
        LBU     t1, 0x5838 (t1)
        J       0x806F7BC8
        ADDIU   a0, r0, 22

    NintendoCoinEffect_Orange:
        J       0x806F7C20
        NOP

RarewareCoinEffect:
    BEQ     t7, at, RarewareCoinEffect_RaceCoin
    ADDIU   at, r0, 0x28F
    BEQ     t7, at, RarewareCoinEffect_Coin
    ADDIU   at, r0, 0x1F2
    BEQ     t7, at, RarewareCoinEffect_Potion
    ADDIU   at, r0, 0x1F3
    BEQ     t7, at, RarewareCoinEffect_Potion
    ADDIU   at, r0, 0x1F5
    BEQ     t7, at, RarewareCoinEffect_Potion
    ADDIU   at, r0, 0x1F6
    BEQ     t7, at, RarewareCoinEffect_Potion
    ADDIU   at, r0, 0x288
    J       0x806F7A2C
    NOP

    RarewareCoinEffect_Coin:
        LUI     t6, 0x8074
        LBU     t6, 0x5838 (t6)
        J       0x806F7ED0
        ADDIU   a0, r0, 22
    
    RarewareCoinEffect_Potion:
        LUI     t6, 0x8074
        LBU     t6, 0x5838 (t6)
        J       0x806F7ED0
        ADDIU   a0, r0, 115

    RarewareCoinEffect_RaceCoin:
        J       0x806F7EC4
        NOP

PotionEffect:
    BEQ     a0, at, PotionEffect_Melon
    LUI     t0, 0x8074
    ADDIU   at, r0, 0x5B
    BEQ     a0, at, PotionEffect_Potion
    ADDIU   at, r0, 0x59
    BEQ     a0, at, PotionEffect_Potion
    NOP
    J       0x806F7AFC
    NOP

    PotionEffect_Potion:
        LBU     t0, 0x5838 (t0)
        J       0x806F7B68
        ADDIU   a0, r0, 115

    PotionEffect_Melon:
        J       0x806F7B60
        NOP