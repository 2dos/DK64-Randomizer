SaveToFileFixes:
    bnez $s0, SaveToFileFixes_Not0
    andi $a1, $s3, 0xFF
    b SaveToFileFixes_Finish
    addiu $a0, $zero, 10 ; Stores it in unused slot

    SaveToFileFixes_Not0:
        addiu $a0, $s0, 4

    SaveToFileFixes_Finish:
        j 0x8060DFFC
        nop

SaveHelmHurryCheck:
    sw $s2, 0x28 ($sp)
    jal canSaveHelmHurry
    sw $s1, 0x24 ($sp)
    or $t6, v0, $zero
    j 0x8060DEFC
    addiu $at, $zero, 1

initCode:
    jal 0x80609140
    sw $zero, 0x14 ($sp)
    jal fixMusicRando
    nop
    jal quickInit
    nop
    j 0x805FBDF4
    nop

displayListCode:
    jal displayListModifiers
    or $a0, $s0, $zero
    or $s0, v0, $zero
    lui $a0, 0x8075
    addiu $a0, $a0, 0x531C
    lhu v1, 0x0 ($a0)
    lui v0, 0x8075
    j 0x80714184
    lbu v0, 0x5314 (v0)

updateLag:
    lui $t6, hi(FrameReal)
    lw $a0, lo(FrameReal) ($t6)
    lui $t6, hi(FrameLag)
    lw $a1, lo(FrameLag) ($t6)
    subu $a1, $a0, $a1
    lui $t6, hi(StoredLag)
    sh $a1, lo(StoredLag) ($t6)
    lui $t6, 0x8077
    j 0x8060067C
    lbu $t6, 0xAF14 ($t6)

InstanceScriptCheck:
    addiu $t1, $zero, 1
    addi $t4, $t4, -1 ; Reduce move_index by 1
    sllv $t4, $t1, $t4 ; 1 << move_index
    addiu $t1, $zero, 0
    and $at, $t6, $t4 ; at = kong_moves & move_index
    beqz $at, InstanceScriptCheck_Fail
    nop

    InstanceScriptCheck_Success:
        j 0x8063EE14
        nop

    InstanceScriptCheck_Fail:
        j 0x8063EE1C
        nop

EarlyFrameCode:
    jal earlyFrame
    nop
    jal 0x805FC668
    nop
    j 0x805FC404
    nop

DynamicCodeFixes:
    jal overlay_changes
    nop
    lui $a1, 0x8074
    j 0x80610950
    lui $t1, 0x8074

getLobbyExit:
    lui $a1, hi(replacement_lobby_exits_array)
    sll $t7, $t6, 1
    addu $a1, $a1, $t7
    lhu $a1, lo(replacement_lobby_exits_array) ($a1)
    addu $a0, $a0, $t7
    jal 0x805FF378
    lhu $a0, lo(replacement_lobbies_array) ($a0)
    jal resetMapContainer
    nop
    j 0x80600070
    nop

adjustExitRead:
    bgez $a0, adjustExitRead_checkCount
    nop
    j 0x806C97F0
    nop

    adjustExitRead_checkCount:
        lui $v0, hi(ExitCount)
        j 0x806C97E8
        lbu $v0, lo(ExitCount) ($v0)

invertPan:
    addiu $t7, $zero, 0x7F
    subu $t6, $t7, $t6
    lw $t7, 0x5C ($sp)
    j 0x80737710
    sb $t6, 0x41 ($t7)

disableFBStore:
    ; If FB pointer is null, do not store framebuffer
    beq $a0, $zero, disableFBStore_jump
    lui $a3, 0x8074
    j 0x8070A850
    lui $t0, 0x8074

    disableFBStore_jump:
        jr $ra
        nop

disableFBZip0:
    beq $a0, $zero, disableFBZip0_jump
    lui $t6, 0x8075
    j 0x8070B064
    addiu $sp, $sp, -0x50

    disableFBZip0_jump:
        jr $ra
        nop

disableFBZip1:
    beq $a2, $zero, disableFBZip1_jump
    nop
    addiu $sp, $sp, -0xC0
    j 0x80709BCC
    sw $ra, 0x3C ($sp)

    disableFBZip1_jump:
        jr $ra
        nop

disableFBZip2:
    beq $a0, $zero, disableFBZip2_jump
    lui $t6, 0x807F
    j 0x80611354
    lw $t6, 0x5A64 ($t6)

    disableFBZip2_jump:
        jr $ra
        nop

disableFBMisc:
    lw $a0, 0x5D80 ($a0)
    beq $a0, $zero, disableFBMisc_jump
    nop
    jal 0x8070A848
    nop
    j 0x80629238
    nop

    disableFBMisc_jump:
        lw $ra, 0x14 ($sp)
        jr $ra
        addiu $sp, $sp, 0x20

fixNullLagBoost:
    lw $t5, 0x4478 ($t5)
    bnez $t5, fixNullLagBoost_end
    nop
    addiu $t5, $zero, 1 ; Set any null lag boost to 1

    fixNullLagBoost_end:
    j   0x806CCA98
    lui $at, 0x4F80

storeWaterSurfaceCount:
    lbu $v0, 0x3 ($t7)
    sb $v0, 0x93C5 ($at)
    j 0x8065F230
    sb $zero, 0x93C4 ($at)

dynflagcheck_0:
    lui $a1, hi(CurrentMap)
    lw $a1, lo(CurrentMap) ($a1)
    jal isDynFlag
    lhu $a0, 0xFFF8 ($s0)
    j 0x806F49F4
    nop

dynflagcheck_1:
    lui $a1, hi(CurrentMap)
    lw $a1, lo(CurrentMap) ($a1)
    jal isDynFlag
    lhu $a0, 0x0000 ($s7)
    j 0x806F4998
    nop

dynflagcheck_2:
    lui $a1, hi(CurrentMap)
    lw $a1, lo(CurrentMap) ($a1)
    jal isDynFlag
    lhu $a0, 0x0028 ($s1)
    j 0x80632148
    nop

dynflagcheck_3:
    or $a1, $s4, $zero
    jal isDynFlag
    lhu $a0, 0x0028 ($s0)
    j 0x80631E44
    nop

pleaseDontStopIslesMusic:
    addiu $at, $at, 0xA0A8  ; currentMap pointer
    lw $a0, 0x0 ($at)
    addiu $at, $zero, 0x22
    beq $at, $a0, mapIsIsles
    lbu $a0, 0xb ($s1)
    
    cancelTheSong:
    JAL cancelMusic
    nop

    PDSTMReturn:  ; because "return" would possibly be too common
    j 0x8060378C
    nop

    mapIsIsles:
    addiu $at, $zero, 0x6E
    bne $at, $a0, PDSTMReturn
    nop
    b cancelTheSong
    nop

PercussionInstruments:
    ; Percussion instruments
    .byte 2 ; Rokotom
    .byte 3 ; Taiko Drum
    .byte 8 ; Bongos
    .byte 9 ; Drum Kit
    .byte 11 ; Tom Tom
    .byte 29 ; Timpani
    .byte 34 ; Drum Roll / Snares
    .byte 93 ; Concert Drum
    .byte 0 ; Null terminator

.align 4

LogPercussion:
    lw $t9, 0x0 ($t8)
    lbu $t4, 0x30 ($t8) ; Inst Index
    ; addiu $t4, $t4, 1
    ; Quick code to filter out non-relevant maps quickly
    lui $t0, hi(CutsceneActive)
    lbu $t0, lo(CutsceneActive) ($t0)
    addiu $t1, $zero, 3
    beq $t0, $t1, LogPercussion_log
    addiu $t1, $zero, 4
    bne $t0, $t1, LogPercussion_end
    nop

    LogPercussion_log:
        lui $t1, hi(PercussionInstruments)
        addiu $t1, $t1, lo(PercussionInstruments)
        
        LogPercussion_loop:
            lbu $t2, 0x0 ($t1)
            ;
            beq $t2, $zero, LogPercussion_end
            addiu $t1, $t1, 1
            beq $t4, $t2, LogPercussion_note
            lui $t2, hi(PercussionPlayed)
            b LogPercussion_loop
            nop

        LogPercussion_note:
            addiu $t3, $zero, 1
            sb $t3, lo(PercussionPlayed) ($t2)

    LogPercussion_end:
        j 0x8073A54C
        sw $t9, 0x14 ($sp)

InstIndexStore:
    ; vacant vars - t4, t9, t1
    lw $t0, 0xD0 ($sp) ; Seqp
    lw $t3, 0x90 ($sp) ; Inst index
    lbu $t5, 0xC3 ($sp) ; chan
    ; get chan state
    sll $t4, $t5, 2
    subu $t4, $t4, $t5
    lw $t9, 0x60 ($t0)
    sll $t4, $t4, 2
    addu $t4, $t4, $t5
    sll $t4, $t4, 2
    addu $t1, $t9, $t4
    j 0x80735444
    sb $t3, 0x30 ($t1) ; 0x30 seems unused

InstanceMalloc:
    lh $a0, 0x0 ($s0)  ; Condition Macro Count
    sll $a1, $a0, 3 ; Space for condition macros
    addu $a2, $s0, $a1
    lh $a2, 0x2 ($a2)  ; Execution Macro Count
    sll $a2, $a2, 3  ; Space for execution macros
    addu $a1, $a1, $a2  ; Space for all macros
    jal dk_malloc
    addiu $a0, $a1, 8  ; Include space for the counts of each macro type + end pointer
    j 0x8063DD30
    nop

InstanceWriteShift:
    sll $a2, $s4, 1
    addu $a0, $s2, $t8
    j 0x8063DD80
    addiu $a0, $a0, 8

InstanceGetExec_0:
    lbu $t4, 0x4 ($s2)  ; Get cond macro count
    or $s0, $zero, $zero
    sll $s1, $t4, 3  ; Get space allocated for cond macros
    addu $t4, $s2, $s1
    addiu $s1, $t4, 0x8  ; Get pointer to exec macros
    j 0x8063E29C
    lbu $t4, 0x6 ($s2)  ; Get exec count