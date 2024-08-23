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

makeCannonsRequireBlast:
    ; check control state
    lui $at, hi(CurrentActorPointer_0)
    lw $at, lo(CurrentActorPointer_0) ($at)
    lbu $t0, 0x154 ($at)
    addiu $v0, $zero, 1
    sb $v0, 0x144 ($at)
    addiu $at, $zero, 20
    beq $t0, $at, has_blast_vanilla_jump
    addiu $at, $zero, 1
    beq $t0, $at, has_blast_vanilla_jump
    nop
    ; Check blast
    lui $v0, 0x8080
    lbu $v0, 0xC950 ($v0)
    andi $v0, $v0, 1
    bnez $v0, has_blast ; Does have blast
    nop
    ; Enable Translucency
    lui $at, hi(CurrentActorPointer_0)
    lw $at, lo(CurrentActorPointer_0) ($at)
    lw $t0, 0x60 ($at)
    lui $v0, 0xFFFF
    ori $v0, $v0, 0x7FFF
    and $t0, $t0, $v0
    sw $t0, 0x60 ($at)
    lh $t0, 0x128 ($at)
    slti $t0, $t0, 100
    bnez $t0, blast_set_noclip
    nop
    addiu $t0, $zero, 100 ; translucency
    sh $t0, 0x128 ($at)

    blast_set_noclip:
        addiu $t0, $zero, 1 ; noclip
        sb $t0, 0x144 ($at)
        ; Go back to vanilla code
        addiu $at, $zero, 4
        addiu $v0, $zero, 1
        j 0x8067FE84
        addiu $t0, $zero, 1

    has_blast:
        ; Disable Translucency
        lui $v0, hi(CurrentActorPointer_0)
        lw $v0, lo(CurrentActorPointer_0) ($v0)
        lw $at, 0x60 ($v0)
        ori $at, $at, 0x8000
        sw $at, 0x60 ($v0)
        addiu $t0, $zero, 2 ; noclip
        sb $t0, 0x144 ($v0)
        ; Go back to vanilla code
    
    has_blast_vanilla_jump:
        addiu $at, $zero, 4
        j 0x8067FE2C
        addiu $v0, $zero, 1

fixCannonBlastNoclip:
    lui $t7, 0x8080
    lbu $t7, 0xC950 ($t7)
    andi $t7, $t7, 1
    bnez $t7, fixCannonBlastNoclip_hasBlast ; Does have blast
    nop
    addiu $a3, $zero, 1

    fixCannonBlastNoclip_hasBlast:
        sb $a3, 0x144 ($s0)
        j 0x806806BC
        lw $t7, 0x0 ($s2)

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

brightenMMMEnemies:
    ori $t4, $t2, 0xFF
    lui $t5, hi(CurrentMap)
    lw $t5, lo(CurrentMap) ($t5)
    addiu $t6, $zero, 0x42
    beq $t5, $t6, brightenMMMEnemies_brighen ; Hard
    addiu $t6, $zero, 0x44
    beq $t5, $t6, brightenMMMEnemies_brighen ; Easy
    addiu $t6, $zero, 0x45
    beq $t5, $t6, brightenMMMEnemies_brighen ; Normal
    addiu $t6, $zero, 0x7C
    bne $t5, $t6, brightenMMMEnemies_finish ; Insane
    nop

    brightenMMMEnemies_brighen:
        li $t4, -1

    brightenMMMEnemies_finish:
        j 0x80631388
        sw $t4, 0x4 ($v0)

staticWaterDamage:
    lui $at, 0x8080
    sb $s4, 0x94B0 ($at)
    j 0x80668420
    sb $s4, 0x9484 ($at)

checkBeforeApplyingQuicksand: ; $t4 contains colliding_actor->actor_type
    addiu $at, $zero, 0xB7
    beq $at, $t4, correctActor
    addiu $at, $zero, 0xCE
    beq $at, $t4, correctActor
    addiu $at, $zero, 0x105
    beq $at, $t4, correctActor
    addiu $at, $zero, 0x11D
    beq $at, $t4, correctActor
    addiu $at, $zero, 0x154
    beq $at, $t4, correctActor
    nop

    applyQuicksand: ; not a flying enemy (or not aztec), apply quicksand just as usual
        lui $at, 0x8080
        j 0x80668428
        sb $s4, 0x94AF ($at)

    correctActor:
        lui $at, hi(CurrentMap)
        lw $at, lo(CurrentMap) ($at) ; CurrentMap
        addiu $t4, $zero, 0x26 ; angry aztec
        bne $at, $t4, applyQuicksand ; not aztec
        nop

    noApplyQuicksand:
        lui $at, 0x8080
        j 0x80668428
        nop

disableHelmKeyBounce:
    jal 0x806A6DB4
    or $a0, $zero, $zero
    lui $a1, hi(CurrentMap)
    lw $a1, lo(CurrentMap) ($a1)
    addiu $a2, $zero, 0x6F
    beq $a1, $a2, applyWaterFloat
    nop

    skipWaterFloat:
        j 0x806A74D8
        addiu $t2, $zero, 0x78

    applyWaterFloat:
        j 0x806A747C
        nop

unscareBeaver:
    andi $t3, $t2, 0x7FFF
    sh $t3, 0x1a ($v0)
    lui $a0, hi(CurrentActorPointer_0)
    lw $a0, lo(CurrentActorPointer_0) ($a0)
    addiu $a1, $zero, 36
    j 0x806AD748
    sb $a1, 0x144 ($a0)

scareBeaver:
    sb $t9, 0x154 ($t0)
    lw $t1, 0x0 ($a3)
    lui $a0, hi(CurrentActorPointer_0)
    lw $a0, lo(CurrentActorPointer_0) ($a0)
    addiu $a1, $zero, 35
    j 0x806AD730
    sb $a1, 0x144 ($a0)

AlterHeadSize:
    addiu $t1, $t1, 0x6
    ; Check Actor
    lui $t7, 0x8074
    lw $t7, 0x6E20 ($t7) ; Focused Model
    beq $t7, $zero, AlterHeadSize_Finish
    nop
    lw $s0, 0x58 ($t7) ; Actor Type
    slti $a1, $s0, 344
    beq $a1, $zero, AlterHeadSize_Finish ; Not within first 344 actors
    sra $t7, $s0, 3
    lui $a1, hi(big_head_actors)
    addu $a1, $a1, $t7
    lbu $a1, lo(big_head_actors) ($a1)
    andi $t7, $s0, 7
    addiu $s0, $zero, 0x80
    srav $t7, $s0, $t7
    and $a1, $a1, $t7
    beq $a1, $zero, AlterHeadSize_Finish ; Not allowed for big head mode
    nop
    ; No need to check whether setting is enabled, assume this is only called if setting is enabled
    lui $t7, hi(BigHeadMode)
    lbu $t7, lo(BigHeadMode) ($t7)
    sll $t7, $t7, 8
    lui $a1, 0x8074
    addiu $a1, $a1, 0x7268
    sh $t7, 0x0 ($a1)
    sh $t7, 0x2 ($a1)
    sh $t7, 0x4 ($a1)

    AlterHeadSize_Finish:
        lw $s0, 0x38 ($a0)
        j 0x8061A4D0
        lhu $t7, 0x0 ($s7)

AlterHeadSize_0:
    ; Check Actor
    lui $t7, 0x8074
    lw $t7, 0x6E20 ($t7) ; Focused Model
    beq $t7, $zero, AlterHeadSize_0_Finish
    nop
    lw $s0, 0x58 ($t7) ; Actor Type
    slti $a1, $s0, 344
    beq $t9, $zero, AlterHeadSize_0_Finish ; Not within first 344 actors
    sra $t7, $s0, 3
    lui $t9, hi(big_head_actors)
    addu $t9, $t9, $t7
    lbu $t9, lo(big_head_actors) ($t9)
    andi $t7, $s0, 7
    addiu $s0, $zero, 0x80
    srav $t7, $s0, $t7
    and $t9, $t9, $t7
    beq $t9, $zero, AlterHeadSize_0_Finish ; Not allowed for big head mode
    nop
    ; No need to check whether setting is enabled, assume this is only called if setting is enabled
    lui $t9, hi(BigHeadMode)
    lbu $t9, lo(BigHeadMode) ($t9)
    sll $t9, $t9, 8
    lui $s0, 0x8074
    addiu $s0, $s0, 0x7268
    sh $t9, 0x0 ($s0)
    sh $t9, 0x2 ($s0)
    sh $t9, 0x4 ($s0)
    
    AlterHeadSize_0_Finish:
        ; Run replaced code
        sll $s1, $s1, 1
        j 0x806198DC
        addu $t9, $s5, $s1

makeKongTranslucent:
    lui $v1, hi(CurrentMap)
    lw $v1, lo(CurrentMap) ($v1)
    addiu $at, $zero, 0xCF
    bne $v1, $at, makeKongTranslucent_finish ; not in chunky phase
    nop
    addiu $at, $zero, 0x2
    bne $t1, $at, makeKongTranslucent_clearTranslucency ; not hunky
    nop
    lui $v1, hi(CutsceneActive)
    lbu $v1, lo(CutsceneActive) ($v1)
    addiu $at, $zero, 0x1
    beq $v1, $at, makeKongTranslucent_clearTranslucency ; In Cutscene
    nop
    lui $v1, hi(CurrentActorPointer_0)
    lw $v1, lo(CurrentActorPointer_0) ($v1)
    ; Enable Translucency
    lw $t2, 0x60 ($v1)
    lui $at, 0xFFFF
    ori $at, $at, 0x7FFF
    and $t2, $t2, $at
    sw $t2, 0x60 ($v1)
    ; Reduce Translucency
    lh $t2, 0x128 ($v1)
    addiu $t2, $t2, -4
    slti $at, $t2, 100
    beq $at, $zero, makeKongTranslucent_setTranslucency
    nop
    addiu $t2, $zero, 100

    makeKongTranslucent_setTranslucency:
        b makeKongTranslucent_finish
        sh $t2, 0x128 ($v1)

    makeKongTranslucent_clearTranslucency:
        lui $v1, hi(CurrentActorPointer_0)
        lw $v1, lo(CurrentActorPointer_0) ($v1)
        ; Disable Translucency
        lw $t2, 0x60 ($v1)
        ori $t2, $t2, 0x8000
        sw $t2, 0x60 ($v1)

    makeKongTranslucent_finish:
        addiu $at, $zero, 0x1
        j 0x806CB780
        lui $v1, 0x8080

expandTBarrelResponse:
    lw $t6, 0x0 ($s1)
    lw $t7, 0x58 ($t6) ; load actor type
    addiu $at, $zero, 134 ; training barrel
    beq $t7, $at, expandTBarrelResponse_isResponse
    nop
    j 0x80680ADC
    addiu $at, $zero, 0x1C ; Regular Bonus

    expandTBarrelResponse_isResponse:
        j 0x80680AE4
        nop

fixLankyPhaseHandState:
    lui $t0, hi(CutsceneActive)
    lbu $t0, lo(CutsceneActive) ($t0)
    beqz $t0, fixLankyPhaseHandState_nohead
    nop
    lui $t0, hi(CutsceneIndex)
    lh $t0, lo(CutsceneIndex) ($t0)
    addiu $t9, $zero, 26
    beq $t0, $t9, fixLankyPhaseHandState_hashead
    addiu $t9, $zero, 27
    beq $t0, $t9, fixLankyPhaseHandState_hashead
    addiu $t9, $zero, 28
    beq $t0, $t9, fixLankyPhaseHandState_hashead
    nop

    fixLankyPhaseHandState_nohead:
        lw $t0, 0x0 ($s1)
        j 0x806C3268
        addiu $t9, $zero, 1

    fixLankyPhaseHandState_hashead:
        lw $t0, 0x0 ($s1)
        j 0x806C3268
        addiu $t9, $zero, 5

blockTreeClimbing:
    jal canPlayerClimb
    nop
    bnez $v0, blockTreeClimbing_canclimb
    nop
    lbu $a0, 0x6 ($s3) ; check model 2 status
    bnez $a0, blockTreeClimbing_noclimb ; is model 2, cannot climb
    nop

    blockTreeClimbing_canclimb:
        or $a0, $s2, $zero
        lw $a1, 0x64 ($sp)
        j 0x8072F3E4
        or $a2, $s3, $zero


    blockTreeClimbing_noclimb:
        j 0x8072F474
        or $a0, $s2, $zero