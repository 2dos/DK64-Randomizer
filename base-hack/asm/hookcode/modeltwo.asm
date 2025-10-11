normal_rotate: dh 0x288, 0x90, 0x18D, 0x13C, 0xDE, 0xE0, 0xE1, 0xDD, 0xDF, 0x48, 0x28F, 0x5B, 0x1F2, 0x1F3, 0x1F5, 0x1F6, 0x59, 0x257, 0x258, 0x259, 0x25A, 0x25B, 0x25C, 0xB7, 0x25F, 0x260, 0x261, 0x262, 0x27E, 0x289, 0x28A, 0x28B, 0x28C, 0x291, 0x292, 0x293, 0x198
backwards_rotate: dh 0x25D, 0x264, 0x265, 0x299, 0x294

.align 4
ObjectRotate:
    beq $v0, $at, ObjectRotate_ApplyRotate
    nop
    ; Define Loop 1
    or $a0, $zero, $zero
    lui $a1, hi(normal_rotate)
    addiu $a1, $a1, lo(normal_rotate)
    addiu $a2, $zero, 37
    
    ; Loop 1
    ObjectRotate_Loop1:
    lh $at, 0x0 ($a1)
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $a0, $a0, 1
    bne $a0, $a2, ObjectRotate_Loop1
    addiu $a1, $a1, 2

    ; Define Loop 2
    ObjectRotate_Define2:
    or $a0, $zero, $zero
    lui $a1, hi(backwards_rotate)
    addiu $a1, $a1, lo(backwards_rotate)
    addiu $a2, $zero, 5

    ; Loop 2
    ObjectRotate_Loop2:
    lh $at, 0x0 ($a1)
    beq $v0, $at, ObjectRotate_ApplyReverseRotate
    addiu $a0, $a0, 1
    bne $a0, $a2, ObjectRotate_Loop2
    addiu $a1, $a1, 2

    ; End Loop
    j 0x80637150
    nop

    ObjectRotate_ApplyRotate:
        j 0x80637160
        nop

    ObjectRotate_ApplyReverseRotate:
        lwc1 $f6, 0x14 ($s0)
        lui $at, 0x4024
        mtc1 $at, $f11
        mtc1 $zero, $f10
        cvt.d.s $f8, $f6
        j 0x80637178
        sub.d $f16, $f8, $f10

WriteDefaultShopBone:
    lwc1 $f0, 0x8 ($t9)
    swc1 $f0, 0x0 ($t2)
    lw $t3, 0x28 ($sp)
    lwc1 $f0, 0x4 ($t9)
    swc1 $f0, 0x0 ($t3)
    lwc1 $f0, 0x0 ($t9)
    j 0x8063366C
    swc1 $f0, 0x0 ($a3)

SetupModelTwoHandler:
    addu $t0, $t9, $s0
    swc1 $f16, 0x10 ($t0)
    lbu $t1, 0x10 ($s1)
    sb $t1, 0x8D ($t0)
    lbu $t1, 0x11 ($s1)
    sb $t1, 0x8E ($t0)
    lbu $t1, 0x12 ($s1)
    j 0x80632204
    sb $t1, 0x8F ($t0)

ActorToModelTwoHandler:
    addu $a2, $t9, $t0
    ; Parse actor
    lw $a1, 0x124 ($s2)  ; Load actor extra data
    beqz $a1, ActorToModelTwoHandler_finish
    nop
    lbu $a3, 0xC ($a1)
    sb $a3, 0x8D ($a2)
    lbu $a3, 0xD ($a1)
    sb $a3, 0x8E ($a2)
    lbu $a3, 0xE ($a1)
    sb $a3, 0x8F ($a2)
    
    ActorToModelTwoHandler_finish:
        j 0x806F792C
        addiu $a2, $a2, 0x8C

ModelTwoToSetupState:
    lwc1 $f10, 0xC ($t8)
    swc1 $f10, 0xC ($v1)
    lbu $t9, 0x8D ($t8)
    sb $t9, 0x10 ($v1)
    lbu $t9, 0x8E ($t8)
    sb $t9, 0x11 ($v1)
    lbu $t9, 0x8F ($t8)
    j 0x8063BA0C
    sb $t9, 0x12 ($v1)