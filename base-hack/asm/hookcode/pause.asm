PauseExtraHeight:
    lui $s1, hi(InitialPauseHeight)
    lhu $s1, lo(InitialPauseHeight) ($s1)
    j 0x806A9820
    addiu $s0, $s0, 0x5CC

PauseExtraSlotCode:
    lui $t9, hi(InitialPauseHeight)
    lhu $t9, lo(InitialPauseHeight) ($t9)
    addiu $t9, $t9, 0xCC
    bne $s1, $t9, PauseExtraSlotCode_Normal
    nop
    lui $t9, hi(ExpandPauseMenu)
    lbu $t9, lo(ExpandPauseMenu) ($t9)
    beqz $t9, PauseExtraSlotCode_Skip
    sra $t4, $a2, 0x10
    sll $t6, $t7, 2
    lui $t9, hi(PauseSlot3TextPointer)
    j 0x806A996C
    addiu $t8, $t9, lo(PauseSlot3TextPointer)

    PauseExtraSlotCode_Skip:
        j 0x806A9980
        nop

    PauseExtraSlotCode_Normal:
        lw $t9, 0x0 ($s6)
        j 0x806A9964
        sra $t4, $a2, 0x10

PauseExtraSlotClamp0:
    lui $a2, 0x427C
    lui $t4, hi(ExpandPauseMenu)
    lbu $t4, lo(ExpandPauseMenu) ($t4)
    j 0x806A87C4
    addiu $t4, $t4, 2

PauseExtraSlotClamp1:
    lui $a3, 0x3F80
    lui $at, hi(ExpandPauseMenu)
    lbu $at, lo(ExpandPauseMenu) ($at)
    subu $at, $t8, $at
    j 0x806A8768
    slti $at, $at, 0x3

PauseExtraSlotCustomCode:
    lb v0, 0x17 ($s0) ; Load Slot Position
    addiu $at, $zero, 3
    bne $at, v0, PauseExtraSlotCustomCode_Finish
    nop
    jal warpToIsles ; Init Map Change
    nop
    jal resetMapContainer
    nop
    j 0x806A8A20
    addiu $at, $zero, 2
    
    PauseExtraSlotCustomCode_Finish:
        j 0x806A880C
        addiu $at, $zero, 2

PauseCounterCap:
    andi $t4, $s4, 0xFF
    addiu $t8, $zero, 4
    bne $t8, $s3, PauseCounterCap_Finish
    nop
    addiu $s3, $zero, 3

    PauseCounterCap_Finish:
        j 0x806A98A0
        or $t8, $t6, $s2

PauseControl_Control:
    ; 806A86FC
    beq $a1, $at, PauseControl_Control_Finish
    lui $t8, 0x8080
    addiu $at, $zero, 4
    beq $a1, $at, PauseControl_Control_Finish
    nop
    j 0x806A8704
    nop

    PauseControl_Control_Finish:
        j 0x806A8D08
        nop

PauseControl_Sprite:
    ; 806AA414
    beq v0, $at, PauseControl_Sprite_Finish
    or $s0, $zero, $zero
    addiu $at, $zero, 4
    beq v0, $at, PauseControl_Sprite_Finish
    nop
    j 0x806AA41C
    nop

    PauseControl_Sprite_Finish:
        j 0x806AB2C0
        nop