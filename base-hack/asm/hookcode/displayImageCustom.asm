displayImageCustom:
    ; Mult x & y coords
    addiu $t6, $zero, 4
    lw $at, 0x18 ($sp)
    mult $at, $t6
    mflo $at
    sw $at, 0x18 ($sp)
    lw $at, 0x1C ($sp)
    mult $at, $t6
    mflo $at
    sw $at, 0x1C ($sp)
    ; Standard Logic
    addiu $sp, $sp, -0x1A8
    lui $at, 0xFFFF
    sw $a0, 0x1A8 ($sp)
    ori $at, $at, 0x3FFF
    or $a0, $a1, $zero  ; Copy texture addr
    and $t6, $a3, $at
    sw $ra, 0x4C ($sp)
    sw $s0, 0x48 ($sp)
    sw $a1, 0x1AC ($sp)
    sw $a2, 0x1B0 ($sp)
    or $a3, $t6, $zero
    beq $a3, $zero, displayImageCustom_codec0
    addiu $at, $zero, 1
    beq $a3, $at, displayImageCustom_codec1
    addiu $at, $zero, 3
    beq $a3, $at, displayImageCustom_next
    addiu $s0, $zero, 0x20
    b displayImageCustom_next
    addiu $s0, $zero, 0x10

    displayImageCustom_codec0:
        b displayImageCustom_next
        addiu $s0, $zero, 4

    displayImageCustom_codec1:
        b displayImageCustom_next
        addiu $s0, $zero, 8

    displayImageCustom_next:
        j 0x8068C614
        or $v0, $a0, $zero

.align 0x10