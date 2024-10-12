FileScreenDLCode_Jump:
    j FileScreenDLCode
    nop
FileSelectDLCode_Jump:
    j FileSelectDLCode
    nop
Jump_MenuUnlock:
    j KongUnlockCorrectCode
    nop

FileScreenDLCode_Write:
    lui $t3, hi(FileScreenDLCode_Jump)
    lw $t3, lo(FileScreenDLCode_Jump) ($t3)
    lui $t4, 0x8003
    sw $t3, 0x937C ($t4) ; Store Hook
    sw $zero, 0x9380 ($t4) ; Store NOP

    lui $t3, hi(FileSelectDLCode_Jump)
    lw $t3, lo(FileSelectDLCode_Jump) ($t3)
    lui $t4, 0x8003
    sw $t3, 0x8E90 ($t4) ; Store Hook
    sw $zero, 0x8E94 ($t4) ; Store NOP

    lui $t3, hi(Jump_MenuUnlock)
    lw $t3, lo(Jump_MenuUnlock) ($t3)
    lui $t4, 0x8003
    sw $t3, 0x98B8 ($t4) ; Store Hook
    sw $zero, 0x98BC ($t4) ; Store NOP

    ; Fix DK ? RGBA
    lui $t3, 0x8003
    addiu $t3, $t3, 0x37DC
    addiu $t4, $zero, 0xFF
    sb $t4, 0x0 ($t3)
    sb $t4, 0x3 ($t3)
    addiu $t4, $zero, 0xD7
    sb $t4, 0x1 ($t3)
    sb $zero, 0x2 ($t3)
    
    jr ra
    nop

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

encPass:
    addi $sp, $sp, -8
	sw $ra, 0x4 ($sp)
    or $t0, $zero, $zero
    or $v0, $zero, $zero

    encPass_1:
        addu $t2, $a0, $t0
        lbu $t3, 0x0 ($t2)
        sltiu $at, $t0, 5
        beqz $at, encPass_2
        or $t4, $zero, $zero
        addu $t2, $a1, $t0
        lbu $t4, 0x0 ($t2)
        
    encPass_2:
        addiu $t2, $t0, 4
        sll $t2, $t2, 1
        sllv $t5, $t3, $t2
        addiu $t2, $t0, 1
        sllv $t6, $t4, $t2
        xor $t7, $t5, $t6
        xor $t5, $t3, $t4
        addu $t7, $t7, $t5
        sllv $t5, $t7, $t0
        sra $t6, $t7, 3
        or $t5, $t5, $t6
        xor $t7, $t7, $t5
        xor $v0, $v0, $t7
        addi $t0, $t0, 1
        slti $at, $t0, 8
        bnez $at, encPass_1
	    lw $ra, 0x4 ($sp)

	jr $ra
	addiu $sp, $sp, 8