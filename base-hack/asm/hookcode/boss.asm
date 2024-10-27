KRoolLankyPhaseFix:
    lui $a1, 0x8003
    lbu $a2, 0x43 ($sp)
    sll $a2, $a2, 1
    addu $a1, $a1, $a2
    j 0x80028CD4
    lh $a1, 0x59A0 ($a1)

KKOPhaseHandler:
    lui $v0, hi(KKOPhaseOrder)
    addiu $v0, $v0, lo(KKOPhaseOrder)
    lb $a0, 0x0 ($v0)
    bne $t7, $a0, KKOPhaseHandler_Slot2
    nop
    b KKOPhaseHandler_Finish
    lb $t8, 0x1 ($v0)

    KKOPhaseHandler_Slot2:
        lb $a0, 0x1 ($v0)
        bne $t7, $a0, KKOPhaseHandler_Slot3
        nop
        b KKOPhaseHandler_Finish
        lb $t8, 0x2 ($v0)

    KKOPhaseHandler_Slot3:
        lb $a0, 0x2 ($v0)
        bne $t7, $a0, KKOPhaseHandler_Finish
        nop
        b KKOPhaseHandler_Finish
        addiu $t8, $zero, 4

    KKOPhaseHandler_Finish:
        sb $t8, 0x12 ($s0)
        j 0x80032578
        lb $v0, 0x12 ($s0)

KKOInitPhase:
    lui $at, hi(KKOPhaseOrder)
    lb $at, lo(KKOPhaseOrder) ($at)
    sb $at, 0x12 ($s0)
    j 0x80031B34
    lui $at, 0x8003

MadJackShort:
    addiu $t1, $zero, 1 ; Phase 2
    beq $t1, $t8, MadJackShort_Skip
    nop
    addiu $t1, $zero, 3 ; Phase 4
    bne $t1, $t8, MadJackShort_Finish
    nop

    MadJackShort_Skip:
        addiu $t8, $t8, 1

    MadJackShort_Finish:
        andi $t1, $t8, 0xFF
        j 0x80035128
        sll $t0, $t1, 2

PufftossShort:
    addiu $t6, $zero, 1 ; Phase 2
    beq $t5, $t6, PufftossShort_Skip
    nop
    addiu $t6, $zero, 3 ; Phase 4
    bne $t5, $t6, PufftossShort_Finish
    nop

    PufftossShort_Skip:
        addiu $t5, $t5, 1

    PufftossShort_Finish:
        andi $t6, $t5, 0xFF
        j 0x80029AB4
        sll $t7, $t6, 2

DogadonRematchShort:
    addiu v0, $zero, 0x53 ; Dogadon 2 Map
    lui $t1, hi(CurrentMap)
    lw $t1, lo(CurrentMap) ($t1)
    bne v0, $t1, DogadonRematchShort_Finish
    nop
    addiu v0, $zero, 1 ; Phase 2
    bne $t0, v0, DogadonRematchShort_Finish
    nop
    addiu $t0, $t0, 1

    DogadonRematchShort_Finish:
        andi v0, $t0, 0xFF
        j 0x8002ACB8
        sll $t1, v0, 2

DilloRematchShort:
    addiu $t4, $t3, 1
    addiu $t5, $zero, 0xC4 ; Dillo 2 Map
    lui $at, hi(CurrentMap)
    lw $at, lo(CurrentMap) ($at)
    bne $t5, $at, DilloRematchShort_Finish
    nop
    addiu $t5, $zero, 1 ; Phase 2
    bne $t5, $t4, DilloRematchShort_Finish
    nop
    addiu $t4, $t4, 1

    DilloRematchShort_Finish:
        j 0x800257D4
        lui $t5, 0x8077

DKPhaseShort:
    addiu $t4, $zero, 2 ; Phase 3
    bne $t4, $t3, DKPhaseShort_Finish
    nop
    addiu $t3, $t3, 1

    DKPhaseShort_Finish:
        andi $t4, $t3, 0xFF
        j 0x8002DB18
        sll $t5, $t4, 2

TinyPhaseShort:
    jal handleFootProgress
    or $a0, $s0, $zero
    j 0x800303DC
    nop

ChunkyPhaseShort:
    addiu $t6, $zero, 2 ; Phase 3
    bne $t6, $t5, ChunkyPhaseShort_Finish
    nop
    addiu $t5, $t5, 1

    ChunkyPhaseShort_Finish:
        andi $t6, $t5, 0xFF
        j 0x800314BC
        sll $t7, $t6, 2

ChunkyPhaseAddedSave:
    lui $a2, hi(WinCondition)
    lbu $a2, lo(WinCondition) ($a2)
    bnez $a2, ChunkyPhaseAddedSave_Finish
    nop
    jal setFlag
    or $a2, $zero, $zero

    ChunkyPhaseAddedSave_Finish:
        jal 0x8060DEC8
        nop
        j 0x80031380
        nop

FixPufftossInvalidWallCollision:
    lw $s0, 0x8C ($s6)
    beqz $s0, FixPufftossInvalidWallCollision_Invalid
    nop
    sra $t9, $s0, 16
    sltiu $t9, $t9, 0x8000 ; 1 if < 0x80000000
    bnez $t9, FixPufftossInvalidWallCollision_Invalid
    nop
    sra $t9, $s0, 16
    sltiu $t9, $t9, 0x8080 ; 0 if > 0x80800000
    beqz $t9, FixPufftossInvalidWallCollision_Invalid
    nop
    j 0x80677C20
    nop

    FixPufftossInvalidWallCollision_Invalid:
        j 0x80677C78
        nop