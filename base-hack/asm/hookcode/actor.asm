damageMultiplerCode:
    bgez $a3, damageMultiplerCode_Finish
    lb $t9, 0x2FD (v0)
    subu $t2, $zero, $a3
    slti $t2, $t2, 12
    beqz $t2, damageMultiplerCode_Finish
    nop
    lui $t2, hi(DamageMultiplier)
    lbu $t2, lo(DamageMultiplier) ($t2)
    multu $a3, $t2
    mflo $a3

    damageMultiplerCode_Finish:
        j 0x806C9A84
        addu $t0, $t9, $a3

tagPreventCode:
    lui $a1, hi(preventTagSpawn)
    lbu $a1, lo(preventTagSpawn) ($a1)
    beqz $a1, tagPreventCode_Vanilla
    nop
    lh $a1, 0x0 ($s1)
    addiu $a1, $a1, 0x10
    addiu $t8, $zero, 98
    beq $a1, $t8, tagPreventCode_Prevent
    nop
    addiu $t8, $zero, 136
    beq $a1, $t8, tagPreventCode_Prevent
    nop
    addiu $t8, $zero, 137
    beq $a1, $t8, tagPreventCode_Prevent
    nop

    tagPreventCode_Vanilla:
        lh $a1, 0x0 ($s1)
        j 0x8068953C
        subu $t3, $t3, $zero

    tagPreventCode_Prevent:
        j 0x8068968C
        nop

destroyAllBarrelsCode:
    lw $t6, 0x0 ($s1)
    sb v0, 0x131 ($t6)
    lui $a0, hi(Gamemode)
    lbu $a0, lo(Gamemode) ($a0)
    addiu $t0, $zero, 3
    beq $a0, $t0, destroyAllBarrelsCode_Finish
    nop
    lui $a0, hi(bonusAutocomplete)
    lbu $a0, lo(bonusAutocomplete) ($a0)
    andi $t0, $a0, 1
    beqz $t0, destroyAllBarrelsCode_Helm
    nop
    lw $t0, 0x58 ($t6)
    addiu v0, $zero, 0x1C
    bne $t0, v0, destroyAllBarrelsCode_Helm
    nop
    addiu $t0, $zero, 0xC
    sb $t0, 0x154 ($t6)
    sb $zero, 0x155 ($t6)
    addiu $t0, $zero, 3
    sb $t0, 0x185 ($t6)

    destroyAllBarrelsCode_Helm:
    andi $t0, $a0, 2
    beqz $t0, destroyAllBarrelsCode_Finish
    nop
    lw $t0, 0x58 ($t6)
    addiu v0, $zero, 0x6B
    bne $t0, v0, destroyAllBarrelsCode_Finish
    nop
    addiu $t0, $zero, 0xC
    sb $t0, 0x154 ($t6)
    sb $zero, 0x155 ($t6)
    addiu $t0, $zero, 3
    sb $t0, 0x185 ($t6)

    destroyAllBarrelsCode_Finish:
    j 0x80680D18
    nop

destroyAllBarrelsCodeNew:
    lui $a3, hi(CurrentActorPointer_0)
    lw $a3, lo(CurrentActorPointer_0) ($a3)
    lui v0, hi(Gamemode)
    lbu v0, lo(Gamemode) (v0)
    addiu $a2, $zero, 3
    beq v0, $a2, destroyAllBarrelsCodeNew_Finish
    nop
    lui v0, hi(bonusAutocomplete)
    lbu v0, lo(bonusAutocomplete) (v0)
    andi $a2, v0, 1
    beqz $a2, destroyAllBarrelsCode_Helm
    nop
    lw $a2, 0x58 ($a3)
    addiu $a1, $zero, 0x1C
    bne $a1, $a2, destroyAllBarrelsCodeNew_Helm
    nop
    addiu $a1, $zero, 0xC
    sb $a1, 0x154 ($a3)
    sb $zero, 0x155 ($a3)
    addiu $a1, $zero, 3
    sb $a1, 0x185 ($a3)

    destroyAllBarrelsCodeNew_Helm:
        andi $a2, v0, 2
        beqz $a2, destroyAllBarrelsCodeNew_Finish
        nop
        lw $a2, 0x58 ($a3)
        addiu $a1, $zero, 0x6B
        bne $a1, $a2, destroyAllBarrelsCodeNew_Finish
        nop
        addiu $a1, $zero, 0xC
        sb $a1, 0x154 ($a3)
        sb $zero, 0x155 ($a3)
        addiu $a1, $zero, 3
        sb $a1, 0x185 ($a3)

    destroyAllBarrelsCodeNew_Finish:
        lui v0, 0x8080
        j 0x80681228
        addiu v0, v0, 0xBB70

GuardAutoclear:
    ; Check Overlay
    lui $a1, 0x8080
    lw $a1, 0xBB64 ($a1)
    andi $a0, $a1, 0x4000
    bnez $a0, GuardAutoclear_IsSnoop
    nop
    sra $a1, $a1, 16
    andi $a0, $a1, 0x10
    bnez $a0, GuardAutoclear_IsSnoop
    nop

    GuardAutoclear_NotSnoop:
        jal guardCatch ; Void Warp
        nop
        b GuardAutoclear_Finish
        nop

    GuardAutoclear_IsSnoop:
        addiu $a0, $zero, 0x43
        jal 0x806EB0C0
        lw $a1, 0x0 ($s0)

    GuardAutoclear_Finish:
        j 0x806AE564
        nop

GuardDeathHandle:
    jal newGuardCode
    nop
    lui v1, 0x8080
    lw $s0, 0xBB40 (v1)
    j 0x806AF754
    nop

AutowalkFix:
    ; Free Variables
    ; at, t2, a0, t7, t8
    lui $a0, hi(TransitionSpeed)
    lhu $a0, lo(TransitionSpeed) ($a0)
    andi $a0, $a0, 0x8000 ; Get sign
    beqz $a0, AutowalkFix_Vanilla ; No transition exit
    nop
    lui $t7, hi(DestMap)
    lw $t7, lo(DestMap) ($t7)
    lui $t8, hi(DestExit)
    lw $t8, lo(DestExit) ($t8)
    addiu $t2, $zero, 0x22
    bne $t7, $t2, AutowalkFix_NotAztecDoor
    addiu $a0, $zero, 3
    beq $t8, $a0, AutowalkFix_Finish
    lui $at, 0x44F2

    AutowalkFix_NotAztecDoor:
        addiu $t2, $zero, 0x1A
        bne $t7, $t2, AutowalkFix_NotCrusher
        addiu $a0, $zero, 8
        lui $at, 0x4536
        beq $t8, $a0, AutowalkFix_Finish
        addiu $at, $at, 0x4000

    AutowalkFix_NotCrusher:
        addiu $t2, $zero, 0x57
        bne $t7, $t2, AutowalkFix_NotCastle
        addiu $a0, $zero, 15
        lui $at, 0x452F
        beq $t8, $a0, AutowalkFix_Finish ; Castle Tree
        addiu $at, $at, 0x9000
        addiu $a0, $zero, 11
        lui $at, 0x4552
        beq $t8, $a0, AutowalkFix_Finish ; Castle Ballroom
        addiu $at, $at, 0x4000
        addiu $a0, $zero, 21
        lui $at, 0x45FD
        beq $t8, $a0, AutowalkFix_Finish ; Castle Entry (Cancel Autowalk)
        addiu $at, $at, 0x2000

    AutowalkFix_NotCastle:
        addiu $t2, $zero, 0x70
        bne $t7, $t2, AutowalkFix_Vanilla
        addiu $a0, $zero, 1
        beq $t8, $a0, AutowalkFix_Finish
        lui $at, 0x4361

    AutowalkFix_Vanilla:
        lui $at, 0x42C8

    AutowalkFix_Finish:
        j 0x806F3E7C
        or $t2, $zero, $zero

CannonForceCode:
    lui $a0, hi(CurrentMap)
    lw $a0, lo(CurrentMap) ($a0)
    addiu v0, $zero, 0x22
    beq $a0, v0, CannonForceCode_IsIsles
    nop
    j 0x8067B694
    nop

    CannonForceCode_CheckFlag:
        jal 0x8067B450
        or $a0, $s0, $zero
        j 0x8067B68C
        nop

    CannonForceCode_IsIsles:
        lui $a0, hi(LobbiesOpen)
        lbu $a0, lo(LobbiesOpen) ($a0)
        beqz $a0, CannonForceCode_CheckFlag
        nop
        j 0x8067B6CC
        nop

DKCollectableFix:
    lhu v0, 0x4A ($s0)
    addiu $t8, $zero, 0xD ; CB Single
    beq v0, $t8, DKCollectableFix_IsCollectable
    nop
    addiu $t8, $zero, 0x2B ; CB Bunch
    beq v0, $t8, DKCollectableFix_IsCollectable
    nop
    addiu $t8, $zero, 0x1D ; Coin
    beq v0, $t8, DKCollectableFix_IsCollectable
    nop
    sra $t8, $a0, 0x10
    j 0x806324CC
    or $a0, $t8, $zero

    DKCollectableFix_IsCollectable:
        j 0x806324CC
        addiu $a0, $zero, 385

KeyCompressionCode:
    sra $s5, $t7, 0x10
    addiu $t5, $zero, 1
    sb $t5, 0x154 ($t4)
    j 0x806BD330
    sh $t5, 0x146 ($t4)

VineCode:
    ; | 0x00800000
    ; & 0xFBFF7FFF
    addiu $at, $zero, 70
    sh $at, 0x128 ($s0) ; Make transparent
    addiu $at, $zero, 0xFF
    sb $at, 0x16A ($s0) ; R
    sb $zero, 0x16B ($s0) ; G
    sb $zero, 0x16C ($s0) ; B
    lui $at, 0x80
    or $t7, v0, $at ; Enable RGB Mask
    lui $at, 0xFBFF
    ori $at, $at, 0x7FFF
    j 0x80698414
    and $t7, $t7, $at ; Enable Opacity filter

VineShowCode:
    ; | 0x04008004
    ; & 0xFF7FFFFF
    lui $at, 0x400
    ori $at, $at, 0x8004
    or v0, v0, $at
    lui $at, 0xFF7F
    ori $at, $at, 0xFFFF
    j 0x80698428
    and $t8, v0, $at

SpriteFix:
    sb $zero, 0x0 ($t0)
    lui $t1, hi(CurrentActorPointer_0)
    lw $t1, lo(CurrentActorPointer_0) ($t1)
    lw $t1, 0x58 ($t1)
    addiu $t3, $zero, 0x36 ; Race Coin
    beq $t1, $t3, SpriteFix_Finish
    addiu $t9, $zero, 0
    addiu $t9, $zero, 1

    SpriteFix_Finish:
        j 0x806A6710
        sb $t9, 0x1 ($t0)

HandleSlamCheck:
    ; handles slam check, and passes it through a system which compares it to the slam level dicated by switch adjustments if necessary
    lh $t4, 0x2 ($s0)
    lui $t6, hi(RandomSwitches)
    lbu $t6, lo(RandomSwitches) ($t6)
    beqz $t6, HandleSlamCheck_Finish ; No Random Switches, exert vanilla behaviour
    or $t1, $zero, $zero

    ; check level - level index will be stored in reg t2
    lui $t6, hi(CurrentMap)
    lw $t6, lo(CurrentMap) ($t6)
    lui $t2, hi(levelIndexMapping)
    addu $t2, $t6, $t2
    lbu $t2, lo(levelIndexMapping) ($t2)
    sltiu $at, $t2, 8
    beqz $at, HandleSlamCheck_Finish ; Isnt part of levels japes->castle
    nop

    ; check if map is a bad map, where we prohibit this effect being exerted
    addiu $at, $zero, 0x9A ; Mad Jack
    beq $t6, $at, HandleSlamCheck_Finish
    nop

    ; All checks have passed, slam level will be dictated by level
    lui $t6, hi(SwitchLevel)
    addu $t6, $t6, $t2
    lbu $t4, lo(SwitchLevel) ($t6)

    HandleSlamCheck_Finish:
        j 0x8063ed84
        nop