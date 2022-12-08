CoinHUDReposition:
    addiu $t8, $zero, 0x26
    lui $t7, hi(CurrentMap)
    lw $t7, lo(CurrentMap) ($t7)
    addiu $a2, $zero, 1
    beq $t7, $a2, CoinHUDReposition_Finish
    nop
    addiu $a2, $zero, 5
    beq $t7, $a2, CoinHUDReposition_Finish
    nop
    addiu $a2, $zero, 0x19
    beq $t7, $a2, CoinHUDReposition_Finish
    nop

    CoinHUDReposition_Lower:
        addiu $t8, $zero, 0x4C

    CoinHUDReposition_Finish:
        j 0x806F88D0
        addiu $t7, $zero, 0x122

GiveItemPointerToMulti:
    lui $t8, hi(MultiBunchCount)
    addiu $t8, $t8, lo(MultiBunchCount)
    sw $t8, 0x0 ($s0)
    j 0x806F8618
    sw $t6, 0xC ($s0)

TextHandler:
    lui $t9, hi(PauseText)
    lbu $t9, lo(PauseText) ($t9)
    beqz $t9, TextHandler_NoPause
    nop

    TextHandler_Pause:
        j 0x8070E8B8
        nop

    TextHandler_NoPause:
        lw $t9, 0x60 ($a1)
        j 0x8070E844
        lui $at, 0xFDFF

InvertCameraControls:
    addu $t7, $t7, $t6
    lb $t7, 0xD63F ($t7)
    lui $a0, hi(InvertedControls)
    lbu $a0, lo(InvertedControls) ($a0)
    beqz $a0, InvertCameraControls_Finish
    nop
    sub $t7, $zero, $t7

    InvertCameraControls_Finish:
        j 0x806EA714
        nop

HUDDisplayCode:
    addiu $a0, $sp, 0x6C
    sw $s0, 0x10 ($sp)
    jal writeHUDAmount
    lw $a3, 0x78 ($sp)
    j 0x806F9F90
    or $s0, v0, $zero

HomingDisable:
    lbu $t1, 0x2 ($t0)
    lui $t2, hi(ForceStandardAmmo)
    lbu $t2, lo(ForceStandardAmmo) ($t2)
    beqz $t2, HomingDisable_Finish
    nop
    lui $t2, hi(ToggleAmmoOn)
    lbu $t2, lo(ToggleAmmoOn) ($t2)
    beqz $t2, HomingDisable_Finish
    nop
    andi $t1, $t1, 0xFFFD

    HomingDisable_Finish:
        j 0x806E22B8
        andi $t2, $t1, 0x2

HomingHUDHandle:
    lui $a0, hi(ForceStandardAmmo)
    lbu $a0, lo(ForceStandardAmmo) ($a0)
    beqz $a0, HomingHUDHandle_Finish
    nop
    addiu $a3, $zero, 0x2

    HomingHUDHandle_Finish:
        or $a0, $a3, $zero
        j 0x806EB57C
        or $a1, $zero, $zero

SkipCutscenePans:
    lui $t1, hi(CutsceneActive)
    addiu v0, $zero, 1
    lbu $t1, lo(CutsceneActive) ($t1)
    bne $t1, v0, SkipCutscenePans_Persist
    nop
    lui $t1, hi(CutsceneIndex)
    lhu $t1, lo(CutsceneIndex) ($t1)
    sltiu v0, $t1, 64
    beqz v0, SkipCutscenePans_Persist
    nop
    lui $t1, hi(CurrentMap)
    lw $t1, lo(CurrentMap) ($t1)
    sltiu v0, $t1, 216
    beqz v0, SkipCutscenePans_Persist
    nop
    lui $t1, hi(CutsceneIndex)
    lhu $t1, lo(CutsceneIndex) ($t1)
    addiu $t6, $zero, 32
    subu v0, $t1, $t6
    sltiu $t1, $t1, 32
    beqz $t1, SkipCutscenePans_PostShiftDetect
    addiu $t1, $zero, 1
    lui $t1, hi(CutsceneIndex)
    lhu v0, lo(CutsceneIndex) ($t1)
    addiu $t1, $zero, 0

    SkipCutscenePans_PostShiftDetect:
        ; t1 = offset, v0 = shift
        lui $t6, hi(CurrentMap)
        lw $t6, lo(CurrentMap) ($t6)
        sll $t6, $t6, 1
        addu $t6, $t6, $t1
        sll $t6, $t6, 2
        lui $t1, hi(cs_skip_db)
        addiu $t1, $t1, lo(cs_skip_db)
        addu $t6, $t6, $t1
        lw $t6, 0x0 ($t6)
        addiu $t1, $zero, 1
        sllv $t1, $t1, v0
        and $t6, $t6, $t1
        beqz $t6, SkipCutscenePans_Persist
        nop
        lui $t6, hi(CutsceneStateBitfield)
        lhu $t6, lo(CutsceneStateBitfield) ($t6)
        andi $t6, $t6, 4
        beqz $t6, SkipCutscenePans_Skip
        nop

    SkipCutscenePans_Persist:
        lw $t1, 0x0 ($s1)
        j 0x8061E68C
        lui v0, 0x807F

    SkipCutscenePans_Skip:
        j 0x8061E8A4
        nop

PlayCutsceneVelocity:
    lui $t9, hi(CutsceneStateBitfield)
    lhu $t9, lo(CutsceneStateBitfield) ($t9)
    andi $t9, $t9, 4
    bnez $t9, PlayCutsceneVelocity_Finish
    nop
    lui $t9, hi(CutsceneIndex)
    lhu $t9, lo(CutsceneIndex) ($t9)
    sltiu $at, $t9, 64
    beqz $at, PlayCutsceneVelocity_Finish
    nop
    addiu $t4, $zero, 32
    subu $t4, $t9, $t4
    sltiu $at, $t9, 32
    beqz $at, PlayCutsceneVelocity_CheckSlot
    addiu $t3, $zero, 1
    addiu $t3, $zero, 0
    or $t4, $t9, $zero

    PlayCutsceneVelocity_CheckSlot:
        ; t3 = offset, t4 = shift
        lui v0, hi(CurrentMap)
        lw v0, lo(CurrentMap) (v0)
        sltiu $at, v0, 216
        beqz $at, PlayCutsceneVelocity_Finish
        nop
        lui $t1, hi(cs_skip_db)
        addiu $t1, $t1, lo(cs_skip_db)
        sll v0, v0, 1
        addu v0, v0, $t3
        sll v0, v0, 2
        addu $t1, $t1, v0
        lw $t1, 0x0 ($t1)
        addiu v0, $zero, 1
        sllv v0, v0, $t4
        and $t1, $t1, v0
        beqz $t1, PlayCutsceneVelocity_Finish
        nop
        j 0x8061CE5C
        lw v0, 0x0 ($a1)

    PlayCutsceneVelocity_Finish:
        lui $t9, 0x8075
        j 0x8061CE40
        swc1 $f0, 0xB8 ($t8)

ModifyCameraColor:
    lui $t0, hi(EnemyInView)
    lbu $t0, lo(EnemyInView) ($t0)
    beqz $t0, ModifyCameraColor_Finish
    li $t0, -1
    lui $t0, 0xFF
    addiu $t0, $t0, 0xFF

    ModifyCameraColor_Finish:
        j 0x806FF38C
        lui $at, 0x3F00