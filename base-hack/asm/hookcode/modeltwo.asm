ObjectRotate:
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x288
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x90
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x18D
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x13C
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xDE
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xE0
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xE1
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xDD
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xDF
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x48
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x28F
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x5B
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x1F2
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x1F3
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x1F5
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x1F6
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x59
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x257
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x258
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x259
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x25A
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x25B
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x25C
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0xB7
    beq $v0, $at, ObjectRotate_ApplyRotate
    addiu $at, $zero, 0x25D
    beq $v0, $at, ObjectRotate_ApplyReverseRotate
    nop
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

ScaleObjectCollision_0:
    lh $t2, 0x10 ($t1)
    mtc1 $t2, $f18
    cvt.s.w $f18, $f18
    ; Operation to perform | old + ((scale - 1) * (20 + old))
    ; scale - 1
    lwc1 $f16, 0x1C ($s0)
    lui $t2, 0x3F80
    mtc1 $t2, $f10
    sub.s $f16, $f16, $f10
    ; 20 + old
    lui $t2, 0x41A0
    mtc1 $t2, $f10
    add.s $f10, $f10, $f18
    ; old + ((scale - 1) * (20 + old))
    mul.s $f10, $f10, $f16
    add.s $f16, $f10, $f18
    cvt.w.s $f16, $f16
    mfc1 $t2, $f16
    j 0x806F62BC
    sw $t6, 0x10 ($sp)

ScaleObjectCollision_1:
    lh $t3, 0x12 ($t2)
    mtc1 $t3, $f8
    cvt.s.w $f8, $f8
    lwc1 $f10, 0x1C ($s0)
    mul.s $f10, $f10, $f8
    j 0x806F6310
    nop