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
    lui $a1, hi(ReplacementLobbyExitsArray)
    sll $t7, $t6, 1
    addu $a1, $a1, $t7
    lhu $a1, lo(ReplacementLobbyExitsArray) ($a1)
    addu $a0, $a0, $t7
    jal 0x805FF378
    lhu $a0, lo(ReplacementLobbiesArray) ($a0)
    jal resetMapContainer
    nop
    j 0x80600070
    nop

checkFlag_ItemRando:
    jal getFlagBlockAddress
    sh $a2, 0x22 ($sp)
    lw $a0, 0x24 ($sp)
    addiu $a1, $sp, 0x22
    or $a2, v0, $zero
    jal updateFlag
    addiu $a3, $zero, 0
    j 0x80731170
    nop

setFlag_ItemRando:
    jal getFlagBlockAddress
    sh $a3, 0x32 ($sp)
    lw $a0, 0x38 ($sp)
    addiu $a1, $sp, 0x32
    or $a2, v0, $zero
    jal updateFlag
    addiu $a3, $zero, 1
    j 0x80731300
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