Jump_RemoveKrazyKKLagImpact:
    j RemoveKrazyKKLagImpact
    nop

PatchBonusCode:
    lui $t3, hi(Jump_RemoveKrazyKKLagImpact)
    lw $t3, lo(Jump_RemoveKrazyKKLagImpact) ($t3)
    lui $t4, 0x8003
    sw $t3, 0x95D4 ($t4)
    jr ra
    sw $zero, 0x95D8 ($t4)

RemoveKrazyKKLagImpact:
    lh $t4, 0x0 ($t0)
    lui $t5, hi(StoredLag)
    lhu $t5, lo(StoredLag) ($t5)
    j 0x800295DC
    subu $t5, $t4, $t5

ArcadeMapCheck:
    addiu $at, $zero, 2
    beq $a0, $at, ArcadeMapCheck_IsArcade
    addiu $at, $zero, 216
    beq $a0, $at, ArcadeMapCheck_IsArcade
    addiu $at, $zero, 217
    beq $a0, $at, ArcadeMapCheck_IsArcade
    addiu $at, $zero, 218
    beq $a0, $at, ArcadeMapCheck_IsArcade
    addiu $at, $zero, 219
    beq $a0, $at, ArcadeMapCheck_IsArcade
    addiu $at, $zero, 220
    beq $a0, $at, ArcadeMapCheck_IsJetpac
    nop
    j 0x805FE96C
    nop

    ArcadeMapCheck_IsArcade:
        j 0x805FE960
        addiu $t1, $zero, 3

    ArcadeMapCheck_IsJetpac:
        j 0x805FE960
        addiu $t1, $zero, 4

ArcadeIntroCheck:
    lui $t3, hi(CurrentMap)
    lw $t3, lo(CurrentMap) ($t3)
    addiu $t4, $zero, 2
    lui $at, 0x8005
    beq $t3, $t4, ArcadeIntroCheck_finish
    or $t5, $v1, $zero ; Long Intro
    jal 0x800257D8
    nop
    j 0x800251BC
    nop

    ArcadeIntroCheck_finish:
        j 0x80024FDC
        sb $t5, 0xC724 ($at)

checkNewMayhemWin:
    jal wonMinecartMayhem
    nop
    beq $v0, $zero, checkNewMayhemWin_no
    nop
    ; Has won
    j 0x8002522C
    nop

    checkNewMayhemWin_no:
        j 0x80025254
        nop