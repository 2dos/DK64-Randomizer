BarrelMovesFixes:
    lbu $t0, 0x4238 ($t0) ; Load Barrel Moves Array Slot
    addi $t0, $t0, -1 ; Reduce move_value by 1
    addiu v1, $zero, 1
    sllv $t0, v1, $t0 ; Get bitfield value
    and v1, $t0, $t9
    beqz v1, BarrelMovesFixes_Finish
    nop
    addiu v1, $zero, 1

    BarrelMovesFixes_Finish:
        j 0x806F6EB4
        nop

ChimpyChargeFix:
    andi $t6, $t6, 1
    lui v1, 0x8080
    j 0x806E4938
    addiu v1, v1, 0xBB40

OStandFix:
    lbu $t2, 0xCA0C ($t2)
    andi $t2, $t2, 1
    j 0x806E48B4
    addiu $a0, $zero, 0x25

HunkyChunkyFix2:
    bnel v1, $at, HunkyChunkyFix2_Finish
    li $at, 4
    andi $a2, $a0, 1
    blezl $a2, HunkyChunkyFix2_Finish
    li $at, 4
    j 0x8067ECC8
    nop

    HunkyChunkyFix2_Finish:
        j 0x8067ECD0
        nop

DisableGunInCrowns:
    subu $t5, $t5, $v0
    lui $t4, 0x10 ; In crown
    ori $t4, $t4, 0x200 ; Disable oranges/gun
    j 0x806E6008
    and $t3, $t2, $t4