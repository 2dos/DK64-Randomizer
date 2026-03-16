FileScreenDLCode:
    addiu $s0, $t4, -0x140
    jal display_text
    addiu $a0, $s2, 8
    j 0x80029690
    addiu $s2, v0, 0

FileSelectDLCode:
    jal 0x806ABB98
    sra $a2, $t3, 0x10
    addiu $a0, v0, 0
    lwc1 $f6, 0xF8 ($sp)
    lui $a1, 0x4080
    mtc1 $a1, $f0
    mul.s $f6, $f6, $f0
    trunc.w.s $f6, $f6
    jal displayHash
    mfc1 $a1, $f6
    j 0x80028E98
    nop

KongUnlockCorrectCode:
    addiu $s0, $s0, 0x3805
    jal correctKongFaces
    addiu $s2, $s2, 0x5B2
    j 0x800298DC
    nop

GoToPassword:
    jal isFileEmpty
    or $a0, $zero, $zero
    bnez $v0, GoToPassword_write
    addiu $a1, $zero, 6 ; multiplayer root (will be password screen)
    addiu $a1, $zero, 3 ; file progress

    GoToPassword_write:
        j 0x80028D0C
        sb $a1, 0x13 ($s0)